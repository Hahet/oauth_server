import functools

from models.oauth import Oauth
from models.user import User
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
