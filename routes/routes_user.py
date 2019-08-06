from urllib.parse import unquote_plus


from flask import (
    render_template,
    current_app,
    Blueprint,
    redirect,
    request,
    url_for,
    jsonify
)

from models.session import Session
from models.token import Token
from models.user import User

from routes import (
    current_user,
    random_string,
    login_required,
    oauth_required
)

from utils import log
from models.user import User
# 不要这么 import
# from xx import a, b, c, d, e, f

user = Blueprint('user', __name__)


@user.route('/user/login', methods=['POST'])
def login():
    """
    登录页面的路由函数
    """
    form = request.form

    u, result = User.login(form)
    # session 会话
    # token 令牌
    # 设置一个随机字符串来当令牌使用
    session_id = random_string()
    form = dict(
        session_id=session_id,
        user_id=u.id,
    )
    Session.new(form)

    redirect_to_index = redirect(
        url_for('user.login_view', result=result)
    )
    response = current_app.make_response(redirect_to_index)
    response.set_cookie('session_id', value=session_id)
    return response


@user.route('/user/login/view', methods=['GET'])
def login_view():
    u = current_user()
    result = request.args.get('result', '')
    result = unquote_plus(result)
    return render_template(
        'login.html',
        username=u.username,
        result=result,
    )


@user.route('/user/register', methods=['POST'])
def register():
    """
    注册页面的路由函数
    """
    form = request.form

    u, result = User.register(form.to_dict())
    log('register post', result)
    return redirect(
        url_for('user.register_view', result=result)
    )


@user.route('/user/register/view', methods=['GET'])
def register_view():
    result = request.args.get('result', '')
    result = unquote_plus(result)

    return render_template('register.html', result=result)


@user.route('/user/profile/view', methods=['GET'])
@login_required
def profile_view():
    u = current_user()
    return render_template('profile.html', username=u.username)


@user.route('/user/info', methods=['GET'])
# @login_required
@oauth_required
def user_info(user):
    # print('request', request)
    # authorization = request.headers.get('Authorization')
    # access_token = authorization[6:]
    # token = Token.find_by(access_token=access_token)
    # user_id = token.user_id
    # user = User.find_by(id=user_id)
    r = {
        'name': user.username,
    }
    r = jsonify(r)
    return r
