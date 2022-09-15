import requests
from flask import Flask
from flask import Response
import configparser
from flask import request
from users import User
from users import Chat
from users import Message

config = configparser.ConfigParser()
config.read('config/main.ini')

TOKEN = config["AUTH"]["bot_token"]
app = Flask(__name__)




def tel_send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text
    }

    r = requests.post(url, json=payload)
    return r


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        msg = request.get_json()
        print(msg)
        msg: Message = Message.parse_message(msg)
        if msg.text == 'users':
            tel_send_message(msg.msgChat.id,User.list())
        else:
            tel_send_message(msg.msgChat.id,  "Сообщение принято. Вот оно: \n "+msg.text)

        return Response('ok', status=200)
    else:
        return "Привет я тестовый димкабот-1!"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
