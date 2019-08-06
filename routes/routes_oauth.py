import functools

from models.oauth import Oauth
from models.user import User
from models.token import Token

from flask import (
    render_template,
    Blueprint,
    redirect,
    request,
    url_for,
    jsonify
)

from routes import (
    redirect,
    current_user,
    login_required,
)
from utils import log


oauth_view = Blueprint('oauth_view', __name__)


@oauth_view.route('/oauth/index')
@login_required
def index():
    """
    oauth 首页的路由函数
    提取显示所有的oauth
    """
    return render_template('oauth_index.html', oauths=Oauth.all_json())


@oauth_view.route('/oauth/add',  methods=['POST'])
@login_required
def oauth_add():
    """
    添加oauth应用的函数
    """
    # 获取到当前用户
    u = current_user()
    # 获取提交的表单
    form = request.form
    # 创建Oauth并关联user id
    Oauth.add(form.to_dict(), u.id)
    return redirect(
        url_for('oauth_view.index')
    )


@oauth_view.route('/oauth/add/view')
@login_required
def oauth_add_view():
    return render_template('oauth_add.html')


@oauth_view.route('/oauth/authorize', methods=['GET'])
def oauth_authorize():
    # 请求
    # GET http://localhost:3000/oauth/authorize?client_id=mq4jd3qmo8t29ktfjrme&redirect_uri=http://localhost:8080/oauth/redirect
    # 返回
    # redirect(http://localhost:8080/oauth/redirect?code=823ddde2405066dcea75)
    oauth_app = Oauth.find_by(client_id=request.args.get('client_id'))
    token = Token.add({}, oauth_app.user_id, oauth_app.id)
    # 下发一个code
    code = token.code
    log('code', code)
    log('access token:', Token.find_by(code=code).access_token)
    redirect_url = request.args.get('redirect_uri') + '?code=' + code
    # 重定向到客户端的url
    # return render_template('look_url.html', url=redirect_url)
    return redirect(redirect_url)


@oauth_view.route('/oauth/access_token', methods=['POST'])
def oauth_access_token():
    # 请求
    # POST 'http://localhost:3000/oauth/access_token?client_id=t02vqaq1btkdbpitlhdc&client_secret=fncntppuvxy5raezv0l7owohgqfc39pc6bwoqwlh&code=823ddde2405066dcea75'
    # 返回

    # 使用Oauth.find_by找到oauth_app
    # 使用Token.find_by找到token
    # 检查token.user_id与oauth_app.user_id
    # 检查token.oauth_id与oauth_app.id
    # 检查通过返回数据

    client_id = request.args.get('client_id')
    client_secret = request.args.get('client_secret')
    code = request.args.get('code')
    oauth_app = Oauth.find_by(client_id=client_id, client_secret=client_secret)
    token = Token.find_by(code=code)

    vaild = (token.user_id == oauth_app.user_id) and (
        token.oauth_id == oauth_app.id)
    r = {
        'access_token': token.access_token,
        'scope': '',
        'token_type': 'bearer'
    }
    string = jsonify(r)
    if vaild:
        return string
    return jsonify({'access_token': 'error'})
