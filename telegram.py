import uuid

import requests
from urllib import request
import data


class Telegram:

    def __init__(self, TOKEN:str):
        self.token = TOKEN

    def tel_send_message(self, chat_id, text):
        url = f'https://api.telegram.org/bot{self.token}/sendMessage'
        payload = {
            'chat_id': chat_id,
            'text': text
        }

        r = requests.post(url, json=payload)
        return r

    def get_file_by_id(self, file_id: str):
        print(f'getting file by id {file_id}')
        url = f'https://api.telegram.org/bot{self.token}/getFile'
        payload = {
            'file_id': file_id
        }
        r = requests.get(url, json=payload)
        resp = r.json()['result']

        url = f'https://api.telegram.org/file/bot{self.token}/{resp["file_path"]}'
        fileId = str(uuid.uuid1())
        print(f'opening url {url}')
        response = request.urlopen(url)
        data.put_file_by_id(fileId, response.read())
        return fileId

    def send_photo(self, chat_id, content):
        url = f'https://api.telegram.org/bot{self.token}/sendPhoto'
        payload = {
            'chat_id': chat_id,
            'photo': content
        }
        post_data = {'chat_id': chat_id}
        post_file = {'photo': content}
        r = requests.post(url, data=post_data, files=post_file)

        return r

