import json
from os import path

import requests
from flask import Flask
from flask import Response
import configparser
from flask import request
from users import User
from users import Chat
from users import Message
from telegram import Telegram
import imgboard
import data

config = configparser.ConfigParser()
config.read('config/main.ini')

app = Flask(__name__)

global tgram, board
tgram = Telegram(config["AUTH"]["bot_token"])
if path.isfile(f'{config["DATA"]["file_path"]}/board.js'):
    board_file = open(f'{config["DATA"]["file_path"]}/board.js', 'r')
    board = imgboard.Board.from_json(json.load(board_file))

else:
    board = imgboard.Board(config["NET"]["img_url"])


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

        else:
            tgram.tel_send_message(msg.msgChat.id,  "Сообщение принято. Вот оно: \n "+msg.text)
            if len(msg.files) != 0:
                text = 'также приняты файлы: \n'
                for f in msg.files:
                    text = text+f+'\n'
                tgram.tel_send_message(msg.msgChat.id, text)
                board.create_post(msg)
                #saving board
                boardfile = open(f'{config["DATA"]["file_path"]}/board.js', 'w')
                boardfile.write(json.dumps(board, cls=imgboard.BoardEncoder))
                boardfile.close()
        return Response('ok', status=200)
    else:
        return "Привет я тестовый димкабот-1!"


@app.route('/board', methods=['GET'])
def board_get():
    str_return = json.dumps(board.posts, cls=imgboard.BoardEncoder)
    return Response(str_return, status=200, headers={"Access-Control-Allow-Origin": "*"})
    pass


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
