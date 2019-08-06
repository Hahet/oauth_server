from models.token import Token
from models.token import random_string


def test_1():
    form = {
        "code": random_string(20),
        "access_token": random_string(40),
    }
    t = Token(form)
    assert t.code == form['code']
    assert t.access_token == form['access_token']


def test_2():
    form = {
        "code": random_string(20),
        "access_token": random_string(40),
    }
    user_id = 0
    oauth_id = 1
    Token.add(form, user_id, oauth_id)
    code = form['code']
    t = Token.find_by(code=code)
    assert t.code == form['code']
    assert t.access_token == form['access_token']
