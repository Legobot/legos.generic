from Legobot.Lego import Lego
import os
import sys
import threading

REPO_PATH = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    '..'
)
LEGO_PATH = os.path.join(REPO_PATH, 'legos')
sys.path.append(LEGO_PATH)
from generic import Generic  # noqa: E402

LOCK = threading.Lock()
BASEPLATE = Lego.start(None, LOCK)
CONFIG_PATH = os.path.join(REPO_PATH, 'tests', 'config.yaml')
LEGO = Generic(BASEPLATE, LOCK, config_path=CONFIG_PATH)


def test_get_name():
    assert LEGO.get_name() == 'Generic'


def test_load_file(caplog):
    test_file = os.path.join(REPO_PATH, 'tests', 'test_file')
    assert LEGO._load_file(test_file) == 'some text'
    assert LEGO._load_file('x') is None
    assert 'Error loading file' in caplog.messages[0]
    assert LEGO._load_file('x', 'default') == 'default'


def test_validate_config(caplog):
    config = {
        'configs': [
            {
                'id': 'SomeId',
                'listening_for': {
                    'type': 'startswith',
                    'value': [
                        'some value'
                    ]
                },
                'handler': {
                    'type': 'config',
                    'selector': 'random',
                    'responses': [
                        '1',
                        '2',
                        '3'
                    ]
                },
                'help': {
                    'text': 'Some help text'
                }
            }
        ]
    }
    LEGO._validate_config(config)
    assert not caplog.messages
    config = {}
    LEGO._validate_config(config)
    assert 'Error validating config' in caplog.messages[0]


def test_load_config():
    LEGO._load_config(CONFIG_PATH)
    assert len(LEGO.config) == 3
    for c in LEGO.config:
        assert 'id' in c
        assert 'listening_for' in c
        assert 'handler' in c
        assert 'help' in c

    for i in ['Test', 'Yaml', 'Json']:
        assert i in LEGO.listeners


def test_listening_for():
    assert LEGO.listening_for({'text': '!yaml'})
    assert LEGO.match_id == 'Yaml'
    assert LEGO.listening_for({'text': '!test'})
    assert LEGO.match_id == 'Test'
    assert LEGO.listening_for({'text': '!json'})
    assert LEGO.match_id == 'Json'
    assert not LEGO.listening_for({'text': 'some random text'})


def test_match_startswith():
    assert not LEGO._match_startswith('x', None)
    assert not LEGO._match_startswith('x', 'y')
    assert LEGO._match_startswith('x', 'xy')
    assert not LEGO._match_startswith(['x', 'y'], 'z')
    assert LEGO._match_startswith(['x', 'y'], 'yz')


def test_select_from_responses():
    assert not LEGO._select_from_responses({}, None)
    assert LEGO._select_from_responses(
        {'selector': 'single'}, ['x', 'y']) == 'x'
    assert LEGO._select_from_responses(
        {}, ['y', 'x']) == 'y'
    assert LEGO._select_from_responses(
        {'selector': 'random'}, ['1', '2']) in ['1', '2']


def test_get_config_by_id():
    assert LEGO._get_config_by_id('abc') == {}
    assert LEGO._get_config_by_id('Test')['id'] == 'Test'


def test_get_help():
    assert LEGO.get_help() == ('!help Generic [Test | Yaml | Json] for '
                               'specific help.')
    assert LEGO.get_help(sub='Test') == '!test to return some test text'


def test_build_response():
    LEGO.match_id = 'X'
    assert not LEGO._build_response()
    LEGO.match_id = 'Json'
    assert LEGO._build_response() == 'This is a response from a json file'

BASEPLATE.stop()
