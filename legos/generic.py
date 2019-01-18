import json
import jsonschema
from Legobot.Lego import Lego
import logging
import os
import random
from six import string_types
import yaml

logger = logging.getLogger(__name__)
SCHEMA_PATH = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    'schema.yaml'
)


class Generic(Lego):
    def __init__(self, baseplate, lock, *args, **kwargs):
        super().__init__(baseplate, lock)
        if 'config_path' not in kwargs:
            config_path = os.path.join(
                os.getcwd(),
                'config.yaml'
            )
        else:
            config_path = kwargs['config_path']
        self._load_config(config_path)
        logger.debug('CONFIG: {}'.format(self.config))
        logger.debug('LISTENERS: {}'.format(self.listeners))

    def _load_config(self, config_path):
        self.config = yaml.safe_load(self._load_file(config_path, 'configs: '))
        self._validate_config(self.config)
        self.config = self.config.get('configs', [])
        self.listeners = {c['id']: c['listening_for']
                          for c in self.config}

    def _validate_config(self, config):
        schema = yaml.safe_load(self._load_file(SCHEMA_PATH))
        try:
            jsonschema.validate(config, schema)
        except Exception as e:
            logger.error('Error validating config: {}'.format(e))

    def _load_file(self, path, default=None):
        try:
            with open(path, 'r') as f:
                return f.read()
        except Exception as e:
            logger.error('Error loading file: {}\n{}'.format(path, e))
            return default

    def listening_for(self, message):
        if message.get('text'):
            listener_map = {
                'startswith': self._match_startswith
            }
            try:
                for cid, listener in self.listeners.items():
                    ltype = listener.get('type', 'startswith')
                    if listener_map[ltype](listener.get('value'),
                                           message.get('text')):
                        self.match_id = cid
                        return True

                return False
            except Exception as e:
                logger.error(('Generic lego failed to check the message text:'
                             ' {}').format(e))
                return False

    def handle(self, message):
        opts = self.build_reply_opts(message)
        response = self._build_response()
        if response:
            self.reply(message, response, opts)

    def _match_startswith(self, value, text):
        if not isinstance(text, string_types):
            return False

        if isinstance(value, string_types):
            return text.startswith(value)
        elif isinstance(value, list):
            for v in value:
                if text.startswith(v):
                    return True

        return False

    def _select_from_responses(self, handler, responses):
        if not responses:
            return None

        response_map = {
            'single': responses[0],
            'random': random.choice(responses)  # nosec
        }
        return response_map[handler.get('selector', 'single')]

    def _build_config_response(self, handler):
        responses = handler.get('responses')

        return self._select_from_responses(handler, responses)

    def _build_file_response(self, handler):
        fpath = handler.get('path')
        if not fpath:
            return None

        if handler.get('file_type') == 'yaml':
            load_file = yaml.safe_load(self._load_file(
                fpath, default='None: None'))
        elif handler.get('file_type') == 'json':
            load_file = json.loads(self._load_file(fpath, default='{}'))
        else:
            return None

        if load_file.get(self.match_id):
            responses = load_file[self.match_id].get('responses')
            return self._select_from_responses(handler, responses)

        return None

    def _get_config_by_id(self, cid):
        configs = [c for c in self.config if c.get('id') == cid]
        if configs:
            return configs[0]

        return {}

    def _build_response(self):
        handler = self._get_config_by_id(self.match_id).get('handler')
        if handler:
            handler_func_map = {
                'default': None,
                'config': self._build_config_response(handler),
                'file': self._build_file_response(handler)
            }
            return handler_func_map[handler.get('type', 'default')]

        return None

    def get_name(self):
        return 'Generic'

    def get_help(self, **kwargs):
        subcommands = {c['id']: c['help']['text']
                       for c in self.config}
        if ('sub' in kwargs):
            return subcommands[kwargs['sub']]
        else:
            return '!help Generic [{}] for specific help.'.format(
                ' | '.join([c['id'] for c in self.config])
            )
