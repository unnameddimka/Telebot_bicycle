import datetime
import json
from users import Message


class Board:
    posts: []
    img_url: str

    def __init__(self, img_url):
        self.posts = []
        self.img_url = img_url

    def create_post(self, msg: Message):
        for file_id in msg.files:
            new_post = Post()
            new_post.user = msg.msgFrom.username
            new_post.text = msg.text
            new_post.imgURL = self.img_url+'/'+file_id+'.jpg'
            new_post.date = datetime.datetime.today()
            self.posts.append(new_post)


class Post:
    imgURL: str
    text: str
    user: str
    date: datetime

    def __init__(self):
        self.imgURL = ''
        self.text = ''
        self.user = ''
        self.date = datetime.datetime(2022,1,1)


class BoardEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Board) | isinstance(obj, Post):
            return obj.__dict__
        if isinstance(obj, datetime.datetime):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


class PostEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Post):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)
