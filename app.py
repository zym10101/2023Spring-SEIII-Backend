import json
import concurrent.futures
from flask import Flask, render_template, request, jsonify

# 导入database
from dao.Database import db

# 导入所需model
from model.User import User
from model.Issue import Issue
from model.Label import Label
from model.IssueComment import IssueComment

from service.dataAnalysis.BodyWasher import body_washer
from service.scraper.GitHubIssueScraper import GitHubIssueScraper
from service.scraper.GitHubIssueCommentScraper import GitHubIssueCommentScraper

# 导入环境变量
from utils.Env import DB_HOSTNAME, DB_DATABASE, DB_USERNAME, DB_PASSWORD, DB_PORT

# 使用Flask类创建一个app对象
# __name__：代表当前app.py这个模块
# 1. 以后出现bug可以帮助快速定位
# 2. 对于寻找模板文件有一个相对路径
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] \
    = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/{DB_DATABASE}?charset=utf8mb4"

repo = ""

# 创建线程池
thread_pool = concurrent.futures.ThreadPoolExecutor()

# 在 Flask 中，应用程序实例和扩展是分离的，这意味着你需要在应用程序和扩展之间建立连接。
# 当创建一个 SQLAlchemy 实例时，它并不知道与哪个 Flask 应用程序关联，所以需要使用 db.init_app(app) 方法将其关联起来。
# 具体来说，db.init_app(app) 方法的作用是将 Flask 应用程序的配置信息加载到 SQLAlchemy 中，并初始化 SQLAlchemy 的数据库连接。
# 在 Flask-SQLAlchemy 中，db 是一个 SQLAlchemy 实例，包含了一系列的模型和操作数据库的方法。
db.init_app(app)

with app.app_context():
    db.create_all()


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


# # 请求：http://127.0.0.1:5000/issue/get-and-save-db
# @app.route("/issue/get-and-save-db")
# def issue_get_and_save_db():
#     if repo == "":
#         return "项目名称不能为空！"
#     issue_scraper = GitHubIssueScraper(issue_save_strategy=MysqlSaveStrategy(db, Issue),
#                                        access_token=ACCESS_TOKEN)
#     iss, comments_urls = issue_scraper.get_and_save(repo_name=repo, per_page=100, end_page=5)
#     return iss


# 请求：http://127.0.0.1:5000/issue/comments/get-and-save-db
@app.route("/issue/comments/get-and-save-db")
def issue_comments_get_and_save_db():
    if repo == "":
        return "项目名称不能为空！"
    s = GitHubIssueCommentScraper(access_token=ACCESS_TOKEN)
    iss = s.get_and_save(repo_name=repo, per_page=100, end_page=5)
    return iss


# 请求：http://127.0.0.1:5000/get-and-save-db
# 在爬取issue的同时完成对响应comments的爬取
@app.route("/get-and-save-db")
def issue_get_and_save_db():
    if repo == "":
        return "项目名称不能为空！"
    # 用于爬取问题
    issue_scraper = GitHubIssueScraper(access_token=ACCESS_TOKEN)
    # 用于爬取问题的评论
    comment_scraper = GitHubIssueCommentScraper(access_token=ACCESS_TOKEN)
    iss, comments_urls = issue_scraper.get_and_save(repo_name=repo, per_page=100, end_page=5)
    thread_pool.map(comment_scraper.get_and_save_by_url, comments_urls)
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
    s = GitHubIssueScraper()
    iss = s.get_and_save(repo_name=repo, per_page=2)
    return f"数据保存到csv成功! 请前往项目根目录下{path}查看"


# 请求：http://127.0.0.1:5000/issue/get-and-cal-Senti
@app.route("/issue/get-and-cal-Senti")
def issue_get_and_cal_Senti():
    # if repo == "":
    #     return "项目名称不能为空！"
    s = GitHubIssueScraper(access_token=ACCESS_TOKEN)
    iss = s.get_and_save(repo_name="apache/superset", per_page=100, end_page=5)

    body_washer(db)

    return iss


# 以下是一些Flask示例代码
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
