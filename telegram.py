import uuid

import requests
from urllib import request


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
        local_path = f'./data/files/{fileId}.jpg'  # TODO: handle extension
        response = request.urlopen(url)
        res = response.read()
        file = open(local_path, 'wb')
        file.write(res)
        file.close()
        return fileId

