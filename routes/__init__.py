import os.path
import functools

from flask import (
    request,
    url_for,
    redirect,
)
from jinja2 import (
    Environment,
    FileSystemLoader,
)

from models.session import Session
from models.user import User
from models.oauth import Oauth
from models.token import Token
from utils import log

import random
import json


def random_string():
    """
    生成一个随机的字符串
    """
    seed = 'bdjsdlkgjsklgelgjelgjsegker234252542342525g'
    s = ''
    for i in range(16):
        # 这里 len(seed) - 2 是因为我懒得去翻文档来确定边界了
        random_index = random.randint(0, len(seed) - 2)
        s += seed[random_index]
    return s


def current_user():
    if 'session_id' in request.cookies:
        session_id = request.cookies['session_id']
        s = Session.find_by(session_id=session_id)
        if s is None or s.expired():
            return User.guest()
        else:
            user_id = s.user_id
            u = User.find_by(id=user_id)
            return u
    else:
        return User.guest()


def login_required(route_function):
    """
    这个函数看起来非常绕，所以你不懂也没关系
    就直接拿来复制粘贴就好了
    """

    @functools.wraps(route_function)
    def f():
        log('login_required')
        u = current_user()
        if u.is_guest():
            log('游客用户')
            return redirect(url_for('user.login_view'))
        else:
            log('登录用户', route_function)
            return route_function()

    return f


def oauth_required(route_function):
    """
    这个函数看起来非常绕，所以你不懂也没关系
    就直接拿来复制粘贴就好了
    """

    @functools.wraps(route_function)
    def f():
        log('oauth_required')
        authorization = request.headers.get('Authorization')
        access_token = authorization[6:]
        token = Token.find_by(access_token=access_token)
        user_id = token.user_id
        user = User.find_by(id=user_id)
        if user == None:
            log('未授权')
            return redirect(url_for('user.login_view'))
        else:
            log('已授权用户', route_function)
            return route_function(user)

    return f
