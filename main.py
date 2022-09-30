import requests
from flask import Flask
from flask import Response
import configparser
from flask import request
from users import User
from users import Chat
from users import Message
from telegram import Telegram
import data

config = configparser.ConfigParser()
config.read('config/main.ini')

app = Flask(__name__)

tgram = Telegram(config["AUTH"]["bot_token"])


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        msg = request.get_json()
        print(msg)
        msg: Message = Message.parse_message(tgram, msg)
        if msg.text == 'users':
            tgram.tel_send_message(msg.msgChat.id, User.list())
        if msg.text.lower()[0:4:] == 'file':
            #  tgram.tel_send_message(msg.msgChat.id, "тут будет запрос файла от бота.")
            file_id = msg.text.split(' ')[1]
            contnt = data.get_file_by_id(file_id)
            tgram.send_photo(msg.msgChat.id, contnt)
            #  TODO: make file retrieval by id mechanism.
        else:
            tgram.tel_send_message(msg.msgChat.id,  "Сообщение принято. Вот оно: \n "+msg.text)
            if len(msg.files) != 0:
                text = 'также приняты файлы: \n'
                for f in msg.files:
                    text = text+f+'\n'
                tgram.tel_send_message(msg.msgChat.id, text)

        return Response('ok', status=200)
    else:
        return "Привет я тестовый димкабот-1!"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
