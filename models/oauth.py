import time
import string
import random

from models import Model

def random_string(l):
    a = string.ascii_lowercase + string.digits
    return ''.join(random.choices(a, k=l))


class Oauth(Model):
    """
    针对我们的数据 Oauth
    我们要做 4 件事情
    C create 创建数据
    R read 读取数据
    U update 更新数据
    D delete 删除数据

    Oauth.new() 来创建一个 Oauth
    """

    def __init__(self, form):
        super().__init__(form)
        # 和别的数据关联的方式, 用 user_id 表明拥有它的 user 实例
        self.user_id = form.get('user_id', None)
        self.created_time = form.get('created_time', -1)
        self.updated_time = form.get('updated_time', -1)

    @classmethod
    def add(cls, form, user_id):
        t = Oauth(form)
        t.user_id = user_id
        t.created_time = int(time.time())
        t.updated_time = t.created_time
        t.save()
        return t
