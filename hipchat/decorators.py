import sys
from hipchat import HipChat
from cStringIO import StringIO


class stdout_as_message(object):

    def __init__(self, token, room_id, message_from, **kwargs):
        """Init and set vars"""
        self.token = token
        self.room_id = room_id
        self.message_from = message_from
        self.kwargs = kwargs

    def __call__(self, function):
        """Call the function"""

        def wrapped_function(*args, **kwargs):

            try:
                sys.stdout = StringIO()
                function_to_exec = function(*args,**kwargs)
                out = sys.stdout.getvalue()
                messager = HipChat(self.token)
                messager.message_room(message=out, room_id=self.room_id, message_from=self.message_from, **self.kwargs)
            finally:
                sys.stdout.close()
                sys.stdout = sys.__stdout__
            return function_to_exec

        return wrapped_function