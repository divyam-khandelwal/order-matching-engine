class InputMessage(object):
    def handle(self, message_str):
        raise NotImplementedError

class OutputMessage(object):
    def handle(self, message_str):
        raise NotImplementedError