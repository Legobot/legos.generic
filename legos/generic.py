from Legobot.Lego import Lego
import logging
import yaml
#  add any other imports here.

logger = logging.getLogger(__name__)


class Generic(Lego):
    def __init__(self, baseplate, lock, *args, **kwargs):
        super().__init__(baseplate, lock)

    def listening_for(self, message):
        # This method is where you define what triggers your lego.
        # Every message on the wire will be sent here.
        # If this method returns True the message gets sent to handle()
        # This example checks for messages that start with !Legos
        if message.get('text'):
            try:
                return message.get('text').starswith('!Legos')
            except Exception as e:
                logger.error(('LegoName lego failed to check the message text:'
                             ' {}').format(e))
                return False

    def handle(self, message):
        # This method is the main traffic cop, once the lego is triggered.
        # Handles the subsequent logic, execution and replies
        opts = self.build_reply_opts(message)  # builds the reply options
        # Call another method to do something before replying
        response = self._build_response()
        if response:
            self.reply(message, response, opts)

    def _build_response(self):
        # This is a method specific to this lego. Build as many as you want.
        # It will return a response to the handler, or a None if ____ (you
        # fill in the blank.)
        if True:
            return 'Thanks for using the example lego.'
        else:
            return None

    def get_name(self):
        # Returns the name of the Lego
        return 'LegoName'

    def get_help(self):
        # Returns a help message for when someone types !help lego_name in chat
        return 'type !Legos for a response.'
