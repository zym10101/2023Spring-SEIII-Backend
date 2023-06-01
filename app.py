import json
import os
import time
import jpype
from dotenv import load_dotenv
import concurrent.futures
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import threading

# 导入dao层相关内容
from dao.Database import db
from dao.LabelDao import get_labels_8, get_labels
from dao.UserDao import get_issue_users, get_comment_users

# 导入所需model
from model.User import User
from model.Issue import Issue
from model.Label import Label
from model.Comment import Comment
from model.Account import Account

# 导入service层相关内容
from service.data_analysis.body_washer_and_cal import body_washer_and_cal
from service.data_analysis.get_senti_pct_by_label import get_all_senti_pct_by_label
from service.data_analysis.plot_lable_pct_change import plot_issue_pct_change_by_label, plot_all_pct_change_by_label, \
    plot_comment_pct_change_by_label
from service.data_analysis.plot_reaction_pct import plot_issue_reaction_pct, plot_comment_reaction_pct, \
    plot_all_reaction_pct
from service.data_analysis.plot_repo_pct_change import plot_repo_issue_pct_change, plot_repo_comment_pct_change, \
    plot_repo_all_pct_change
from service.data_analysis.plot_user_pct_change import plot_user_comment_pct_change, plot_user_issue_pct_change, \
    plot_user_all_pct_change
from service.scraper.GitHubScraper import GitHubScraper
from service.scraper.Params import Params
from utils.Email import send_crawling_completed
from service.text_annotation.get_aspect_cluster import getAspectCluster

# tmp
from dao import IssueDao

# 导入环境变量
from utils.Env import DB_HOSTNAME, DB_DATABASE, DB_USERNAME, DB_PASSWORD, DB_PORT, ACCESS_TOKEN

# 导入所需工具类
from utils import DateUtil
from utils.get_plot_intervals import get_plot_intervals

# 使用Flask类创建一个app对象
# __name__：代表当前app.py这个模块
# 1. 以后出现bug可以帮助快速定位
# 2. 对于寻找模板文件有一个相对路径
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] \
    = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/{DB_DATABASE}?charset=utf8mb4"

# 创建线程池
thread_pool = concurrent.futures.ThreadPoolExecutor()

# 在 Flask 中，应用程序实例和扩展是分离的，这意味着你需要在应用程序和扩展之间建立连接。
# 当创建一个 SQLAlchemy 实例时，它并不知道与哪个 Flask 应用程序关联，所以需要使用 db.init_app(app) 方法将其关联起来。
# 具体来说，db.init_app(app) 方法的作用是将 Flask 应用程序的配置信息加载到 SQLAlchemy 中，并初始化 SQLAlchemy 的数据库连接。
# 在 Flask-SQLAlchemy 中，db 是一个 SQLAlchemy 实例，包含了一系列的模型和操作数据库的方法。
db.init_app(app)

# resp_dict_1 = json.loads(
#     '{"url":"https://api.github.com/repos/apache/superset/issues/24057",'
#     '"repository_url":"https://api.github.com/repos/apache/superset",'
#     '"labels_url":"https://api.github.com/repos/apache/superset/issues/24057/labels{/name}",'
#     '"comments_url":"https://api.github.com/repos/apache/superset/issues/24057/comments",'
#     '"events_url":"https://api.github.com/repos/apache/superset/issues/24057/events",'
#     '"html_url":"https://github.com/apache/superset/issues/24057","id":1710376301,"node_id":"I_kwDOAlosUs5l8kVt",'
#     '"number":24057,"title":"Need RBAC consultation","user":{"login":"bukreevai","id":18184117,'
#     '"node_id":"MDQ6VXNlcjE4MTg0MTE3","avatar_url":"https://avatars.githubusercontent.com/u/18184117?v=4",'
#     '"gravatar_id":"","url":"https://api.github.com/users/bukreevai","html_url":"https://github.com/bukreevai",'
#     '"followers_url":"https://api.github.com/users/bukreevai/followers",'
#     '"following_url":"https://api.github.com/users/bukreevai/following{/other_user}",'
#     '"gists_url":"https://api.github.com/users/bukreevai/gists{/gist_id}",'
#     '"starred_url":"https://api.github.com/users/bukreevai/starred{/owner}{/repo}",'
#     '"subscriptions_url":"https://api.github.com/users/bukreevai/subscriptions",'
#     '"organizations_url":"https://api.github.com/users/bukreevai/orgs",'
#     '"repos_url":"https://api.github.com/users/bukreevai/repos",'
#     '"events_url":"https://api.github.com/users/bukreevai/events{/privacy}",'
#     '"received_events_url":"https://api.github.com/users/bukreevai/received_events","type":"User",'
#     '"site_admin":false},"labels":[],"state":"open","locked":false,"assignee":null,"assignees":[],"milestone":null,'
#     '"comments":1,"created_at":"2023-05-15T15:53:19Z","updated_at":"2023-05-15T16:20:10Z","closed_at":null,'
#     '"author_association":"NONE","active_lock_reason":null,"body":"Can someone help with RBAC on Apache Superset: '
#     'what grants are needed for the Charts tab to display user charts I tried everything, nothing is given to the '
#     'interface/chart/list/ page","reactions":{'
#     '"url":"https://api.github.com/repos/apache/superset/issues/24057/reactions","total_count":0,"+1":0,"-1":0,'
#     '"laugh":0,"hooray":0,"confused":0,"heart":0,"rocket":0,"eyes":0},'
#     '"timeline_url":"https://api.github.com/repos/apache/superset/issues/24057/timeline",'
#     '"performed_via_github_app":null,"state_reason":null}')#


with app.app_context():
    db.create_all()

jvm_shutdown = False


@app.route("/")
def index():
    return render_template("index.html")


# 登陆注册相关功能
@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')

    if not username or not password or not email:
        return jsonify(
            {
                'state': 0,
                'message': 'Missing required fields'
            }), 400

    account = Account.query.filter_by(username=username).first()
    if account:
        return jsonify(
            {
                'state': 0,
                'message': 'Username already exists'
            }), 409

    account = Account.query.filter_by(email=email).first()
    if account:
        return jsonify(
            {
                'state': 0,
                'message': 'Email already exists'
            }), 409

    new_account = Account(username=username, password=password, email=email)
    db.session.add(new_account)
    db.session.commit()

    return jsonify(
        {
            'state': 1,
            'message': 'Registration successful'
        }), 201


@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return jsonify(
            {
                'state': 0,
                'message': 'Missing required fields'
            }), 400

    account = Account.query.filter_by(username=username).first()
    if not account or account.password != password:
        return jsonify(
            {
                'state': 0,
                'message': 'Invalid username or password'
            }), 401

    return jsonify(
        {
            'state': 1,
            'message': 'Login successful'
        }), 200


# @app.route("/user/info", methods=["GET", "POST"])
# def user_info():
#     """
#     获取当前用户信息
#     :return:
#     """
#     token = request.headers.get("token")
#     if token == "666666":
#         return jsonify({
#             "code": 0,
#             "data": {
#                 "id": "1",
#                 "userName": "admin",
#                 "realName": "张三",
#                 "userType": 1
#             }
#         })
#     return jsonify({
#         "code": 99990403,
#         "msg": "token不存在或已过期"
#     })


# @app.route("/resp/add-single")
# def resp_add_single():
#     # 1.创建 User\Label ORM对象
#     user_ = User(resp_dict_1['user'])
#     labels_ = []
#     for each in resp_dict_1['labels']:
#         labels_.append(Label(each))
#
#     # 2.创建 issue ORM对象
#     issue_ = Issue(resp_dict_1)
#     issue_.labels = labels_
#     print(issue_.labels)
#
#     # 3.将ORM对象添加到db.session中
#     db.session.merge(user_)
#     db.session.merge(issue_)
#
#     # 4.commit操作
#     db.session.commit()
#
#     return "用户创建成功!"


# @app.route("/project/info", methods=["POST"])
# def project_info():
#     global repo
#     repo = str(json.loads(request.data)['name'])[19:]
#     return repo


# # 请求：http://127.0.0.1:5000/issue/get-and-save-db
# @app.route("/issue/get-and-save-db")
# def get_and_save_issue():
#     if repo == "":
#         return "项目名称不能为空！"
#     issue_scraper = GitHubIssueScraper(access_token=ACCESS_TOKEN)
#     iss, comments_urls = issue_scraper.get_and_save(repo_name=repo, per_page=100, end_page=5)
#     return iss


# # 请求：http://127.0.0.1:5000/issue/comments/get-and-save-db
# @app.route("/issue/comments/get-and-save-db")
# def get_and_save_issue_comments():
#     if repo == "":
#         return "项目名称不能为空！"
#     s = GitHubIssueCommentScraper(access_token=ACCESS_TOKEN)
#     iss = s.get_and_save(repo_name=repo, per_page=100, end_page=5)
#     return iss


# 注意：此接口将在后续废弃!!!由crawling替代
# 请求：http://127.0.0.1:5000/issue/get-and-save-db
# 在爬取issue的同时完成对响应comments的爬取
# @app.route("/issue/get-and-save-db")
# def get_and_save_all():
#     # if repo == "":
#     #     return "项目名称不能为空！"
#     params = Params()
#     params.add_param('since', DateUtil.convert_to_iso8601("2023-03-15"))
#     params.add_param('until', DateUtil.convert_to_iso8601("2023-03-17"))
#     scraper = GitHubScraper(access_token=ACCESS_TOKEN)
#     iss = scraper.crawling_issues_and_comments("www.github/apache/superset", params.to_dict())
#     return iss


# 获取仓库最早issue时间
@app.route("/issue/earliest")
def issue_earliest():
    repo_name = request.args.get("repo", default="", type=str)
    scraper = GitHubScraper(access_token=ACCESS_TOKEN)
    params = Params()
    return scraper.get_earliest_date(repo_name, params.to_dict())


# 在爬取issue的同时完成对响应comments的爬取
@app.route("/crawling", methods=["POST"])
def crawling():
    start = time.time()  # 记录函数开始时间

    data = json.loads(request.data)
    repo_name = str(data.get('repo', ''))
    since = str(data.get('since', ''))
    until = str(data.get('until', ''))
    to_email = str(data.get('email', ''))
    if repo_name == '':
        return "项目名称不能为空！"
    params = Params()
    if since != '':
        params.add_param('since', DateUtil.convert_to_iso8601(since))
    if until != '':
        params.add_param('until', DateUtil.convert_to_iso8601(until))
    scraper = GitHubScraper(access_token=ACCESS_TOKEN)
    iss = scraper.crawling_issues_and_comments(repo_name, params.to_dict())

    # 计算情绪值，只会对新增数据进行情绪值计算
    body_washer_and_cal(db)

    end = time.time()  # 记录函数结束时间
    elapsed_time = end - start  # 计算函数执行时间
    print("函数执行时间：", elapsed_time, "秒")

    start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start))
    send_crawling_completed(to_email, repo_name, start_time)

    return iss


# 同时爬取一个仓库的所有issue和comment，然后做关联
@app.route("/crawling/new", methods=["POST"])
def crawling_new():
    def crawl_comments(repo_name_, params_, max_page=20):
        with app.app_context():
            scraper.crawling_only_comments(repo_name_, params_, max_page)

    def crawl_issues(repo_name_, params_, max_page=20):
        with app.app_context():
            scraper.crawling_only_issues(repo_name_, params_, max_page)

    start = time.time()  # 记录函数开始时间

    data = json.loads(request.data)
    repo_name = str(data.get('repo', ''))
    since = str(data.get('since', ''))
    until = str(data.get('until', ''))
    to_email = str(data.get('email', ''))
    if repo_name == '':
        return "项目名称不能为空！"
    params = Params()
    if since != '':
        params.add_param('since', DateUtil.convert_to_iso8601(since))
    if until != '':
        params.add_param('until', DateUtil.convert_to_iso8601(until))
    scraper = GitHubScraper(access_token=ACCESS_TOKEN)

    # scraper.crawling_only_comments(repo_name, params.to_dict(), max_page=10)
    # scraper.crawling_only_issues(repo_name, params.to_dict(), max_page=10)
    # 创建线程对象
    comments_thread = threading.Thread(target=crawl_comments, args=(repo_name, params.to_dict(), 20))
    issues_thread = threading.Thread(target=crawl_issues, args=(repo_name, params.to_dict(), 20))
    # 启动线程
    comments_thread.start()
    issues_thread.start()
    # 等待线程执行完毕
    comments_thread.join()
    issues_thread.join()

    # 两个任务都结束后做关联
    scraper.create_association(repo_name)

    # 计算情绪值，只会对新增数据进行情绪值计算
    body_washer_and_cal(db)

    end = time.time()  # 记录函数结束时间
    elapsed_time = end - start  # 计算函数执行时间
    print("函数执行时间：", elapsed_time, "秒")

    start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start))

    send_crawling_completed(to_email, repo_name, start_time)

    return "success"


@app.route("/download", methods=["POST"])
def download():
    data = json.loads(request.data)
    repo_name = str(data.get('repo', ''))
    since = str(data.get('since', ''))
    until = str(data.get('until', ''))
    result = IssueDao.get_by_create_time_all(repo_name, since, until)
    result_json = [issue.to_dict() for issue in result]
    return jsonify(result_json)


# 仅爬取issue
@app.route("/crawling/issue", methods=["POST"])
def crawling_issue():
    start = time.time()  # 记录函数开始时间

    data = json.loads(request.data)
    repo_name = str(data.get('repo', ''))
    since = str(data.get('since', ''))
    until = str(data.get('until', ''))
    to_email = str(data.get('email', ''))
    if repo_name == '':
        return "项目名称不能为空！"
    params = Params()
    if since != '':
        params.add_param('since', DateUtil.convert_to_iso8601(since))
    if until != '':
        params.add_param('until', DateUtil.convert_to_iso8601(until))
    scraper = GitHubScraper(access_token=ACCESS_TOKEN)
    iss = scraper.crawling_only_issues(repo_name, params.to_dict())

    # 计算情绪值，只会对新增数据进行情绪值计算
    body_washer_and_cal(db)

    end = time.time()  # 记录函数结束时间
    elapsed_time = end - start  # 计算函数执行时间
    print("函数执行时间：", elapsed_time, "秒")

    start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start))
    send_crawling_completed(to_email, repo_name, start_time)

    return iss


# 仅爬取comment
@app.route("/crawling/comment", methods=["POST"])
def crawling_comment():
    start = time.time()  # 记录函数开始时间

    data = json.loads(request.data)
    repo_name = str(data.get('repo', ''))
    since = str(data.get('since', ''))
    until = str(data.get('until', ''))
    to_email = str(data.get('email', ''))
    if repo_name == '':
        return "项目名称不能为空！"
    params = Params()
    if since != '':
        params.add_param('since', DateUtil.convert_to_iso8601(since))
    if until != '':
        params.add_param('until', DateUtil.convert_to_iso8601(until))
    scraper = GitHubScraper(access_token=ACCESS_TOKEN)
    iss = scraper.crawling_only_comments(repo_name, params.to_dict())

    # 计算情绪值，只会对新增数据进行情绪值计算
    body_washer_and_cal(db)

    end = time.time()  # 记录函数结束时间
    elapsed_time = end - start  # 计算函数执行时间
    print("函数执行时间：", elapsed_time, "秒")

    start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start))
    send_crawling_completed(to_email, repo_name, start_time)

    return iss


# 请求：http://127.0.0.1:5000/cal-senti
# 逻辑已经加到了crawling_issue中，此接口仅作备用
# 分析issue_body和comment_body的情绪值并存入数据库
# 如果新爬取了数据，只会对新增数据进行情绪值计算
@app.route("/cal-senti")
def issue_cal_senti():
    body_washer_and_cal(db)
    return f"情绪值分析完毕"


# 随着app的启动，开启jvm，保证只开启这一个jvm
# python进程关闭时，会自动关闭
jpype.startJVM(classpath="./sentistrength/SentiStrength-1.0-SNAPSHOT.jar")


# 请求：http://127.0.0.1:5000/analyse/pie/all
# 项目issue+comment情绪文本占比饼图
# weighting: issue情绪值权重，默认为0.7
@app.route("/analyse/pie/all", methods=["GET"])
def draw_all_pct():
    data = request.args
    repo_name = str(data.get('repo_name', ''))
    start_time = str(data.get('start_time', ''))
    end_time = str(data.get('end_time', ''))
    weighting = data.get('weighting', 0.7)
    intervals = [start_time, end_time]
    weighting = float(weighting)
    return jsonify(plot_repo_all_pct_change(repo_name, start_time, end_time, intervals, weighting))


# 请求：http://127.0.0.1:5000/analyse/pie/issue
# 项目issue情绪文本占比饼图
@app.route("/analyse/pie/issue", methods=["GET"])
def draw_issue_pct():
    # print(request.data)
    # data = json.loads(request.data)
    data = request.args
    repo_name = str(data.get('repo_name', ''))
    start_time = str(data.get('start_time', ''))
    end_time = str(data.get('end_time', ''))
    print(repo_name, start_time, end_time)
    intervals = [start_time, end_time]

    return jsonify(plot_repo_issue_pct_change(repo_name, start_time, end_time, intervals))


# 请求：http://127.0.0.1:5000/analyse/pie/comment
# 项目comment情绪文本占比饼图
@app.route("/analyse/pie/comment", methods=["GET"])
def draw_comment_pct():
    # data = json.loads(request.data)
    data = request.args
    repo_name = str(data.get('repo_name', ''))
    start_time = str(data.get('start_time', ''))
    end_time = str(data.get('end_time', ''))
    intervals = [start_time, end_time]
    return jsonify(plot_repo_comment_pct_change(repo_name, start_time, end_time, intervals))


# 请求：http://127.0.0.1:5000/analyse/line/all
# 项目issue+comment情绪文本占比波动图
# weighting: issue情绪值权重，默认为0.7
@app.route("/analyse/line/all", methods=["GET"])
def draw_all_pct_change():
    data = request.args
    repo_name = str(data.get('repo_name', ''))
    start_time = str(data.get('start_time', ''))
    end_time = str(data.get('end_time', ''))
    freq = data.get('freq', None)
    periods = int(data.get('periods', 8))
    weighting = data.get('weighting', 0.7)
    intervals = get_plot_intervals(start_time, end_time, freq, periods)
    weighting = float(weighting)
    return jsonify(plot_repo_all_pct_change(repo_name, start_time, end_time, intervals, weighting))


# 请求：http://127.0.0.1:5000/analyse/line/issue
# 项目issue情绪文本占比波动图
@app.route("/analyse/line/issue", methods=["GET"])
def draw_issue_pct_change():
    print("line")
    data = request.args
    # data = json.loads(request.data)
    repo_name = str(data.get('repo_name', ''))
    start_time = str(data.get('start_time', ''))
    end_time = str(data.get('end_time', ''))
    freq = data.get('freq', None)
    periods = int(data.get('periods', 8))
    intervals = get_plot_intervals(start_time, end_time, freq, periods)
    return jsonify(plot_repo_issue_pct_change(repo_name, start_time, end_time, intervals))


# 请求：http://127.0.0.1:5000/analyse/line/comment
# 项目comment情绪文本占比波动图
@app.route("/analyse/line/comment", methods=["GET"])
def draw_comment_pct_change():
    print("line")
    # data = json.loads(request.data)
    data = request.args
    repo_name = str(data.get('repo_name', ''))
    start_time = str(data.get('start_time', ''))
    end_time = str(data.get('end_time', ''))
    freq = data.get('freq', None)
    periods = int(data.get('periods', 8))
    intervals = get_plot_intervals(start_time, end_time, freq, periods)
    return jsonify(plot_repo_comment_pct_change(repo_name, start_time, end_time, intervals))


# 请求：http://127.0.0.1:5000/get-issue-labels
# 获取某一项目的某一时间段内issue所有的label的name列表
@app.route("/get-issue-labels", methods=["GET"])
def get_issue_labels():
    data = request.args
    repo_name = str(data.get('repo_name', ''))
    start_time = str(data.get('start_time', ''))
    end_time = str(data.get('end_time', ''))
    return get_labels(repo_name, start_time, end_time)


# 请求：http://127.0.0.1:5000/get-most-used-labels
# 获取某一项目的某一时间段内对应issue最多的8个label的name列表
@app.route("/get-most-used-labels", methods=["GET"])
def get_most_used_labels():
    data = request.args
    repo_name = str(data.get('repo_name', ''))
    start_time = str(data.get('start_time', ''))
    end_time = str(data.get('end_time', ''))
    return get_labels_8(repo_name, start_time, end_time)


# 请求：http://127.0.0.1:5000/analyse/line/all/label
# issue+comment的labels情绪文本占比图
@app.route("/analyse/line/all/label", methods=["POST"])
def draw_all_pct_change_by_label():
    data = json.loads(request.data)
    repo_name = str(data.get('repo_name', ''))
    start_time = str(data.get('start_time', ''))
    end_time = str(data.get('end_time', ''))
    weighting = data.get('weighting', 0.7)
    labels = data.get('labels', None)
    weighting = float(weighting)
    return jsonify(plot_all_pct_change_by_label(repo_name, start_time, end_time, weighting, labels))


# 请求：http://127.0.0.1:5000/analyse/line/issue/label
# issue的labels情绪文本占比图
@app.route("/analyse/line/issue/label", methods=["POST"])
def draw_issue_pct_change_by_label():
    data = json.loads(request.data)
    repo_name = str(data.get('repo_name', ''))
    start_time = str(data.get('start_time', ''))
    end_time = str(data.get('end_time', ''))
    labels = data.get('labels', None)
    return jsonify(plot_issue_pct_change_by_label(repo_name, start_time, end_time, labels))


# 请求：http://127.0.0.1:5000/analyse/line/comment/label
# comment的labels情绪文本占比图
@app.route("/analyse/line/comment/label", methods=["POST"])
def draw_comment_pct_change_by_label():
    data = json.loads(request.data)
    repo_name = str(data.get('repo_name', ''))
    start_time = str(data.get('start_time', ''))
    end_time = str(data.get('end_time', ''))
    labels = data.get('labels', None)
    return jsonify(plot_comment_pct_change_by_label(repo_name, start_time, end_time, labels))


# 请求：http://127.0.0.1:5000/analyse/line/all/reaction
# issue+comment的reaction情绪文本占比图
@app.route("/analyse/line/all/reaction", methods=["POST"])
def draw_all_pct_change_by_reaction():
    data = json.loads(request.data)
    repo_name = str(data.get('repo_name', ''))
    start_time = str(data.get('start_time', ''))
    end_time = str(data.get('end_time', ''))
    weighting = data.get('weighting', 0.7)
    weighting = float(weighting)
    return plot_all_reaction_pct(repo_name, start_time, end_time, weighting)


# 请求：http://127.0.0.1:5000/analyse/line/issue/reaction
# issue的reaction情绪文本占比图
@app.route("/analyse/line/issue/reaction", methods=["POST"])
def draw_issue_pct_change_by_reaction():
    data = json.loads(request.data)
    repo_name = str(data.get('repo_name', ''))
    start_time = str(data.get('start_time', ''))
    end_time = str(data.get('end_time', ''))
    return jsonify(plot_issue_reaction_pct(repo_name, start_time, end_time))


# 请求：http://127.0.0.1:5000/analyse/line/comment/reaction
# comment的reaction情绪文本占比图
@app.route("/analyse/line/comment/reaction", methods=["POST"])
def draw_comment_pct_change_by_reaction():
    data = json.loads(request.data)
    repo_name = str(data.get('repo_name', ''))
    start_time = str(data.get('start_time', ''))
    end_time = str(data.get('end_time', ''))
    return jsonify(plot_comment_reaction_pct(repo_name, start_time, end_time))


# 请求：http://127.0.0.1:5000/get-issue-users
# 获取issue的所有user
@app.route("/get-issue-users", methods=["POST"])
def get_users_issue():
    data = json.loads(request.data)
    repo_name = str(data.get('repo_name', ''))
    start_time = str(data.get('start_time', ''))
    end_time = str(data.get('end_time', ''))
    return get_issue_users(repo_name, start_time, end_time)


# 请求：http://127.0.0.1:5000/get-comment-users
# 获取comment的所有user
@app.route("/get-comment-users", methods=["POST"])
def get_users_comment():
    data = json.loads(request.data)
    repo_name = str(data.get('repo_name', ''))
    start_time = str(data.get('start_time', ''))
    end_time = str(data.get('end_time', ''))
    return get_comment_users(repo_name, start_time, end_time)


# 请求：http://127.0.0.1:5000/get-all-users
# 获取issue+comment的所有user
@app.route("/get-all-users", methods=["POST"])
def get_users_all():
    data = json.loads(request.data)
    repo_name = str(data.get('repo_name', ''))
    start_time = str(data.get('start_time', ''))
    end_time = str(data.get('end_time', ''))
    user_list = get_issue_users(repo_name, start_time, end_time)
    user_list.extend(get_comment_users(repo_name, start_time, end_time))
    return list(set(user_list))


# 请求：http://127.0.0.1:5000/analyse/line/all/user
# 用户issue+comment情绪文本占比波动图
# user: 用户名
@app.route("/analyse/line/all/user", methods=["POST"])
def draw_all_pct_change_by_user():
    data = json.loads(request.data)
    repo_name = str(data.get('repo_name', ''))
    start_time = str(data.get('start_time', ''))
    end_time = str(data.get('end_time', ''))
    freq = data.get('freq', None)
    periods = int(data.get('periods', 8))
    user = str(data.get('user', ''))
    weighting = data.get('weighting', 0.7)
    intervals = get_plot_intervals(start_time, end_time, freq, int(periods))
    weighting = float(weighting)
    return jsonify(plot_user_all_pct_change(repo_name, user, intervals, weighting))


# 请求：http://127.0.0.1:5000/analyse/line/issue/user
# 用户issue情绪文本占比波动图
# user: 用户名
@app.route("/analyse/line/issue/user", methods=["POST"])
def draw_issue_pct_change_by_user():
    data = json.loads(request.data)
    repo_name = str(data.get('repo_name', ''))
    start_time = str(data.get('start_time', ''))
    end_time = str(data.get('end_time', ''))
    freq = data.get('freq', None)
    periods = int(data.get('periods', 8))
    user = str(data.get('user', ''))
    intervals = get_plot_intervals(start_time, end_time, freq, int(periods))
    return jsonify(plot_user_issue_pct_change(repo_name, user, intervals))


# 请求：http://127.0.0.1:5000/analyse/line/comment/user
# 用户comment情绪文本占比波动图
# user: 用户名
@app.route("/analyse/line/comment/user", methods=["POST"])
def draw_comment_pct_change_by_user():
    data = json.loads(request.data)
    repo_name = str(data.get('repo_name', ''))
    start_time = str(data.get('start_time', ''))
    end_time = str(data.get('end_time', ''))
    user = str(data.get('user', ''))
    intervals = [start_time, end_time]
    return jsonify(plot_user_comment_pct_change(repo_name, user, intervals))


# 请求：http://127.0.0.1:5000/annotation
# 根据人工标注结果聚焦版本问题
@app.route("/annotation", methods=["GET"])
def get_aspect_cluster():
    return jsonify(getAspectCluster())

# # 请求：http://127.0.0.1:5000/get-and-save-db
# # 在爬取issue的同时完成对响应comments的爬取
# @app.route("/get-and-save-db")
# def get_and_save_all():
#     if repo == "":
#         return "项目名称不能为空！"
#     # 用于爬取问题
#     issue_scraper = GitHubIssueScraper(access_token=ACCESS_TOKEN)
#     # 用于爬取问题的评论
#     comment_scraper = GitHubIssueCommentScraper(access_token=ACCESS_TOKEN)
#     iss, comments_urls = issue_scraper.get_and_save(repo_name=repo, per_page=100, end_page=5)
#     thread_pool.map(comment_scraper.get_and_save_by_url, comments_urls)
#     return iss


# # 请求：http://127.0.0.1:5000/issue/get-and-save-csv
# @app.route("/issue/get-and-save-csv")
# def issue_get_and_save_csv():
#     path = './data/issues-tmp.csv'
#     s = GitHubIssueScraper()
#     iss = s.get_and_save(repo_name=repo, per_page=2)
#     return f"数据保存到csv成功! 请前往项目根目录下{path}查看"


# @app.route("/email", methods=["POST"])
# def email():
#     receiver_email = str(json.loads(request.data)['email'])
#     send_crawling_completed(receiver_email, repo, '五百年以前')
#     return "邮件发送成功！"


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
    app.run(debug=False, host='0.0.0.0', port=5000)
