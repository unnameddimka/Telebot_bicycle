import datetime
import json


users = []
# TODO: finish user database. Dump and load on start.

class User:

    def __init__(self):
        self.id: int
        self.is_bot: bool
        self.first_name: str
        self.last_name: str
        self.username: str
        self.language_code: str

        return

    @staticmethod
    def list():
        def obj_dict(obj):
            return obj.__dict__
        return json.dumps(users, default=obj_dict)

    def obj_dict(self):
        return self.__dict__


class Chat:
    def __init__(self):
        self.id: int
        self.first_name: str
        self.last_name: str
        self.username: str
        self.type: str


class Message:

    def __init__(self):
        self.message_id: int
        self.msgFrom: User = User()
        self.msgChat: Chat = Chat()
        self.date: datetime
        self.text: str
        return

    @staticmethod
    def parse_message(message):
        print("message-->", message)
        msg = Message()

        msg.message_id = message['message']['message_id']
        if message['message']['from']['id'] not in [u.id for u in users]:
            msg.msgFrom.__dict__ = message['message']['from']
            users.append(msg.msgFrom)
        else:
            msg.msgFrom = [u for u in users if u.id == message['message']['from']['id']][0]
        msg.msgChat.__dict__ = message['message']['chat']
        if 'text' in message['message']:
            msg.text = message['message']['text']
        else:
            msg.text = ''
        chat_id = message['message']['chat']['id']

        print("chat_id-->", chat_id)
        print("txt-->", msg.text)
        return msg
        # return chat_id, txt
