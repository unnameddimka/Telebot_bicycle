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
            if "username" in msg.msgFrom.__dict__.keys():
                new_post.user = msg.msgFrom.username
            elif "first_name" in msg.msgFrom.__dict__.keys():
                new_post.user = msg.msgFrom.first_name
            else:
                new_post.user = msg.msgFrom.id
            new_post.text = msg.text
            new_post.imgURL = self.img_url+'/'+file_id+'.jpg'
            new_post.date = datetime.datetime.today()
            self.posts.append(new_post)

    @staticmethod
    def from_json(js_dict: dict):
        brd = Board(js_dict["img_url"])
        for pst in js_dict["posts"]:
            postObj = Post.from_json(pst)
            brd.posts.append(postObj)

        return brd

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

    @staticmethod
    def from_json(js_dict: dict):
        pst = Post()
        pst.text = js_dict["text"]
        pst.user = js_dict["user"]
        pst.imgURL = js_dict["imgURL"]
        pst.date = datetime.datetime.strptime(js_dict["date"], '%Y-%m-%d %H:%M:%S.%f')
        return pst

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
