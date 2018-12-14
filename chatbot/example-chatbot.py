from Legobot.Connectors.Slack import Slack
from Legobot.Lego import Lego
from Legobot.Legos.Help import Help
from legos.generic import Generic
import logging
import os
import threading

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
ch.setFormatter(formatter)
logger.addHandler(ch)

config_path = os.path.join(  # config file is in the same dir as chabot.py
    os.path.abspath(os.path.dirname(__file__)),
    'config.yaml'
)

lock = threading.Lock()
baseplate = Lego.start(None, lock)
baseplate_proxy = baseplate.proxy()

baseplate_proxy.add_child(Slack, token='')  # add slack token here
baseplate_proxy.add_child(Help)
baseplate_proxy.add_child(Generic, config_path=config_path)
