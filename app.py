import json
import os

from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify

from model.vo.issue import db, User, Issue, Label, IssueComment
from service.scraper import CsvSaveStrategy, MysqlSaveStrategy, GitHubIssueScraper, GitHubIssueCommentScraper

# 使用Flask类创建一个app对象
# __name__：代表当前app.py这个模块
# 1. 以后出现bug可以帮助快速定位
# 2. 对于寻找模板文件有一个相对路径
app = Flask(__name__)

load_dotenv()
DB_HOSTNAME = os.environ.get('DB_HOSTNAME')
DB_PORT = os.environ.get('DB_PORT')
DB_USERNAME = os.environ.get('DB_USERNAME')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_DATABASE = os.environ.get('DB_DATABASE')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
app.config['SQLALCHEMY_DATABASE_URI'] \
    = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/{DB_DATABASE}?charset=utf8mb4"

repo = ""

# 在 Flask 中，应用程序实例和扩展是分离的，这意味着你需要在应用程序和扩展之间建立连接。
# 当创建一个 SQLAlchemy 实例时，它并不知道与哪个 Flask 应用程序关联，所以需要使用 db.init_app(app) 方法将其关联起来。
# 具体来说，db.init_app(app) 方法的作用是将 Flask 应用程序的配置信息加载到 SQLAlchemy 中，并初始化 SQLAlchemy 的数据库连接。
# 在 Flask-SQLAlchemy 中，db 是一个 SQLAlchemy 实例，包含了一系列的模型和操作数据库的方法。
db.init_app(app)

resp_dict_1 = json.loads(
    '{"url":"https://api.github.com/repos/apache/superset/issues/24057",'
    '"repository_url":"https://api.github.com/repos/apache/superset",'
    '"labels_url":"https://api.github.com/repos/apache/superset/issues/24057/labels{/name}",'
    '"comments_url":"https://api.github.com/repos/apache/superset/issues/24057/comments",'
    '"events_url":"https://api.github.com/repos/apache/superset/issues/24057/events",'
    '"html_url":"https://github.com/apache/superset/issues/24057","id":1710376301,"node_id":"I_kwDOAlosUs5l8kVt",'
    '"number":24057,"title":"Need RBAC consultation","user":{"login":"bukreevai","id":18184117,'
    '"node_id":"MDQ6VXNlcjE4MTg0MTE3","avatar_url":"https://avatars.githubusercontent.com/u/18184117?v=4",'
    '"gravatar_id":"","url":"https://api.github.com/users/bukreevai","html_url":"https://github.com/bukreevai",'
    '"followers_url":"https://api.github.com/users/bukreevai/followers",'
    '"following_url":"https://api.github.com/users/bukreevai/following{/other_user}",'
    '"gists_url":"https://api.github.com/users/bukreevai/gists{/gist_id}",'
    '"starred_url":"https://api.github.com/users/bukreevai/starred{/owner}{/repo}",'
    '"subscriptions_url":"https://api.github.com/users/bukreevai/subscriptions",'
    '"organizations_url":"https://api.github.com/users/bukreevai/orgs",'
    '"repos_url":"https://api.github.com/users/bukreevai/repos",'
    '"events_url":"https://api.github.com/users/bukreevai/events{/privacy}",'
    '"received_events_url":"https://api.github.com/users/bukreevai/received_events","type":"User",'
    '"site_admin":false},"labels":[],"state":"open","locked":false,"assignee":null,"assignees":[],"milestone":null,'
    '"comments":1,"created_at":"2023-05-15T15:53:19Z","updated_at":"2023-05-15T16:20:10Z","closed_at":null,'
    '"author_association":"NONE","active_lock_reason":null,"body":"Can someone help with RBAC on Apache Superset: '
    'what grants are needed for the Charts tab to display user charts I tried everything, nothing is given to the '
    'interface/chart/list/ page","reactions":{'
    '"url":"https://api.github.com/repos/apache/superset/issues/24057/reactions","total_count":0,"+1":0,"-1":0,'
    '"laugh":0,"hooray":0,"confused":0,"heart":0,"rocket":0,"eyes":0},'
    '"timeline_url":"https://api.github.com/repos/apache/superset/issues/24057/timeline",'
    '"performed_via_github_app":null,"state_reason":null}')
with app.app_context():
    db.create_all()
    # with db.engine.connect() as conn:
    #     rs = conn.execute("select * from tmp")
    #     print(rs.fetchone())


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/user/info", methods=["GET", "POST"])
def user_info():
    """
    获取当前用户信息
    :return:
    """
    token = request.headers.get("token")
    if token == "666666":
        return jsonify({
            "code": 0,
            "data": {
                "id": "1",
                "userName": "admin",
                "realName": "张三",
                "userType": 1
            }
        })
    return jsonify({
        "code": 99990403,
        "msg": "token不存在或已过期"
    })


@app.route("/resp/add-single")
def resp_add_single():
    # 1.创建 User\Label ORM对象
    user_ = User(resp_dict_1['user'])
    labels_ = []
    for each in resp_dict_1['labels']:
        labels_.append(Label(each))

    # 2.创建 issue ORM对象
    issue_ = Issue(resp_dict_1)
    issue_.labels = labels_
    print(issue_.labels)

    # 3.将ORM对象添加到db.session中
    db.session.merge(user_)
    db.session.merge(issue_)

    # 4.commit操作
    db.session.commit()

    return "用户创建成功!"


@app.route("/project/info", methods=["POST"])
def project_info():
    global repo
    repo = str(json.loads(request.data)['name'])[19:]
    return repo


# 请求：http://127.0.0.1:5000/issue/get-and-save-db
# 在爬取issue的同时完成对响应comments的爬取
@app.route("/issue/get-and-save-db")
def issue_get_and_save_db():
    if repo == "":
        return "项目名称不能为空！"
    issue_scraper = GitHubIssueScraper(issue_save_strategy=MysqlSaveStrategy(db, Issue),
                                       access_token=ACCESS_TOKEN)
    iss, comments_urls = issue_scraper.get_and_save(repo_name=repo, per_page=100, end_page=5)
    return iss


# 请求：http://127.0.0.1:5000/issue/comments/get-and-save-db
@app.route("/issue/comments/get-and-save-db")
def issue_comments_get_and_save_db():
    if repo == "":
        return "项目名称不能为空！"
    s = GitHubIssueCommentScraper(issue_save_strategy=MysqlSaveStrategy(db, IssueComment),
                                  access_token=ACCESS_TOKEN)
    iss = s.get_and_save(repo_name=repo, per_page=100, end_page=5)
    return iss


# 请求：http://127.0.0.1:5000/issue/get-and-save-db
# 在爬取issue的同时完成对响应comments的爬取
@app.route("/get-and-save-db")
def issue_get_and_save_db():
    if repo == "":
        return "项目名称不能为空！"
    # 用于爬取问题
    issue_scraper = GitHubIssueScraper(issue_save_strategy=MysqlSaveStrategy(db, Issue),
                                       access_token=ACCESS_TOKEN)
    # 用于爬取问题的评论
    comment_scraper = GitHubIssueCommentScraper(issue_save_strategy=MysqlSaveStrategy(db, IssueComment),
                                                access_token=ACCESS_TOKEN)
    iss, comments_urls = issue_scraper.get_and_save(repo_name=repo, per_page=100, end_page=5)
    for url in comments_urls:
        comment_scraper.get_and_save_by_url(url=url, per_page=100, end_page=5)
    return iss


# # 请求：http://127.0.0.1:5000/issue/comments/get-and-save-db
# @app.route("/issue/comments/get-and-save-db")
# def issue_comments_get_and_save_db2():
#     if repo == "":
#         return "项目名称不能为空！"
#     s = GitHubIssueCommentScraper(issue_save_strategy=MysqlSaveStrategy(db, IssueComment),
#                                   access_token=ACCESS_TOKEN)
#     iss = s.get_and_save(repo_name=repo, per_page=100, end_page=5)
#     return iss


# 请求：http://127.0.0.1:5000/issue/get-and-save-csv
@app.route("/issue/get-and-save-csv")
def issue_get_and_save_csv():
    path = './data/issues-tmp.csv'
    s = GitHubIssueScraper(issue_save_strategy=CsvSaveStrategy(path))
    iss = s.get_and_save(repo_name=repo, per_page=2)
    return f"数据保存到csv成功! 请前往项目根目录下{path}查看"


#
#
# @app.route("/user/query")
# def user_query():
#     # 1.get查找：根据主键查找
#     # user_ = User.query.get(1)
#     # print(f"{user_.id}, {user_.username}, {user_.password}")
#     # 2.filter_by查找：返回flask_sqlalchemy.query.Query类数组
#     users = User.query.filter_by(username="zhangsan")
#     for u in users:
#         print(f"{u.id}, {u.username}, {u.password}")
#     return "数据查找成功!"
#
#
# @app.route("/user/update")
# def user_update():
#     user_ = User.query.filter_by(username="zhangsan").first()
#     user_.password = "222222"
#     db.session.commit()
#     return "数据修改成功!"
#
#
# @app.route("/user/delete")
# def user_delete():
#     user_ = User.query.filter_by(username="zhangsan").first()
#     db.session.delete(user_)
#     db.session.commit()
#     return "数据删除成功!"
#
#
# # 创建路由和视图函数的映射
# @app.route("/")
# def root():
#     # jinja2
#     return render_template('Index.html')
#
#
# @app.route("/profile")
# def blog_list():
#     return "我是博客列表！"
#
#
# @app.route("/blog/<int:blog_id>")
# def blog_detail():
#     return f"您访问的博客是：{blog_id}"
#
#
# @app.route("/book/list")
# def book_list():
#     # request.args：类字典类型
#     page = request.args.get("page", default=1, type=int)
#     return f"您获取的是第{page}页图书列表"


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
