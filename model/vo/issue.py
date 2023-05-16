from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


# 表示该 GitHub issue 的作者的相关信息
class User(db.Model):
    def __init__(self, init_dict):
        self.login = init_dict['login']
        self.id = init_dict['id']
        self.node_id = init_dict['node_id']
        self.avatar_url = init_dict['avatar_url']
        self.gravatar_id = init_dict['gravatar_id']
        self.url = init_dict['url']
        self.html_url = init_dict['html_url']
        self.followers_url = init_dict['followers_url']
        self.following_url = init_dict['following_url']
        self.gists_url = init_dict['gists_url']
        self.starred_url = init_dict['starred_url']
        self.subscriptions_url = init_dict['subscriptions_url']
        self.organizations_url = init_dict['organizations_url']
        self.repos_url = init_dict['repos_url']
        self.events_url = init_dict['events_url']
        self.received_events_url = init_dict['received_events_url']
        self.type = init_dict['type']
        self.site_admin = init_dict['site_admin']

    __tablename__ = "user"
    # GitHub用户名
    login = db.Column(db.Text, nullable=False)
    # 用户ID
    id = db.Column(db.Integer, primary_key=True)
    # 用户节点ID
    node_id = db.Column(db.Text, nullable=False)
    # 头像链接
    avatar_url = db.Column(db.Text, nullable=False)
    # Gravatar ID
    gravatar_id = db.Column(db.Text, nullable=False)
    # 用户 GitHub API 链接
    url = db.Column(db.Text, nullable=False)
    # 用户 GitHub 主页链接
    html_url = db.Column(db.Text, nullable=False)
    # 用户关注者的 GitHub API 链接
    followers_url = db.Column(db.Text, nullable=False)
    # 用户正在关注的人的 GitHub API 链接
    following_url = db.Column(db.Text, nullable=False)
    # 用户 Gists 的 GitHub API 链接
    gists_url = db.Column(db.Text, nullable=False)
    # 用户收藏的项目的 GitHub API 链接
    starred_url = db.Column(db.Text, nullable=False)
    # 用户订阅的仓库的 GitHub API 链接
    subscriptions_url = db.Column(db.Text, nullable=False)
    # 用户所在的组织的 GitHub API 链接
    organizations_url = db.Column(db.Text, nullable=False)
    # 用户仓库的 GitHub API 链接
    repos_url = db.Column(db.Text, nullable=False)
    # 用户 GitHub 活动的 GitHub API 链接
    events_url = db.Column(db.Text, nullable=False)
    # 用户收到的 GitHub 活动的 GitHub API 链接
    received_events_url = db.Column(db.Text, nullable=False)
    # 用户类型（"User" 或 "Organization"）
    type = db.Column(db.Text, nullable=False)
    # 用户是否为 GitHub 网站管理员
    site_admin = db.Column(db.Text, nullable=False)


# # 记录了该问题/issue收到的各种反应/表情符号的数量和相关信息
# class Reactions(db.Model):
#     def __init__(self, reactions_dict):
#         self.url = reactions_dict['url']
#         self.total_count = reactions_dict['total_count']
#         self.plus_one = reactions_dict['+1']
#         self.minus_one = reactions_dict['-1']
#         self.laugh = reactions_dict['laugh']
#         self.hooray = reactions_dict['hooray']
#         self.confused = reactions_dict['confused']
#         self.heart = reactions_dict['heart']
#         self.rocket = reactions_dict['rocket']
#         self.eyes = reactions_dict['eyes']
#
#     __tablename__ = "reactions"
#     # 数据库中该记录索引
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     # issue id
#     issue_id = db.Column(db.Integer, db.ForeignKey('issue.id'))
#     # 该问题/issue的反应/表情符号的API地址
#     url = db.Column(db.Text, nullable=False)
#     # 该问题/issue所收到的反应/表情符号总数
#     total_count = db.Column(db.Integer, nullable=False)
#     # 点赞的数量
#     plus_one = db.Column(db.Integer, nullable=False)
#     # 踩的数量
#     minus_one = db.Column(db.Integer, nullable=False)
#     # 大笑的数量
#     laugh = db.Column(db.Integer, nullable=False)
#     # 庆祝的数量
#     hooray = db.Column(db.Integer, nullable=False)
#     # 困惑的数量
#     confused = db.Column(db.Integer, nullable=False)
#     # 爱心的数量
#     heart = db.Column(db.Integer, nullable=False)
#     # 火箭的数量
#     rocket = db.Column(db.Integer, nullable=False)
#     # 眼睛的数量
#     eyes = db.Column(db.Integer, nullable=False)


# Issue
class Issue(db.Model):
    def __init__(self, issue_dict):
        self.id = issue_dict['id']
        self.url = issue_dict['url']
        self.repository_url = issue_dict['repository_url']
        self.labels_url = issue_dict['labels_url']
        self.comments_url = issue_dict['comments_url']
        self.events_url = issue_dict['events_url']
        self.html_url = issue_dict['html_url']
        self.node_id = issue_dict['node_id']
        self.number = issue_dict['number']
        self.title = issue_dict['title']

        self.user_id = issue_dict['user']['id']
        self.user = User.query.get(self.user_id)

        self.labels = ",".join([label['name'] for label in issue_dict['labels']])
        self.state = issue_dict['state']
        self.locked = issue_dict['locked']
        self.assignee = issue_dict['assignee']['id'] if issue_dict['assignee'] else None
        self.assignees = ",".join([assignee['id'] for assignee in issue_dict['assignees']])
        self.milestone = issue_dict['milestone']['title'] if issue_dict['milestone'] else None
        self.comments = issue_dict['comments']
        self.created_at = datetime.strptime(issue_dict['created_at'], '%Y-%m-%dT%H:%M:%SZ')
        self.updated_at = datetime.strptime(issue_dict['updated_at'], '%Y-%m-%dT%H:%M:%SZ')
        self.closed_at = datetime.strptime(issue_dict['closed_at'], '%Y-%m-%dT%H:%M:%SZ') if issue_dict[
            'closed_at'] else None
        self.author_association = issue_dict['author_association']
        self.active_lock_reason = issue_dict['active_lock_reason']
        self.body = issue_dict['body']

        # self.reactions = [Reactions(reactions_dict) for reactions_dict in issue_dict['reactions']]
        self.reactions_url = issue_dict['reactions']['url']
        self.reactions_total_count = issue_dict['reactions']['total_count']
        self.reactions_plus_one = issue_dict['reactions']['+1']
        self.reactions_minus_one = issue_dict['reactions']['-1']
        self.reactions_laugh = issue_dict['reactions']['laugh']
        self.reactions_hooray = issue_dict['reactions']['hooray']
        self.reactions_confused = issue_dict['reactions']['confused']
        self.reactions_heart = issue_dict['reactions']['heart']
        self.reactions_rocket = issue_dict['reactions']['rocket']
        self.reactions_eyes = issue_dict['reactions']['eyes']

        self.timeline_url = issue_dict['timeline_url']
        # self.performed_via_github_app = issue_dict['performed_via_github_app']['name'] if issue_dict[
        #     'performed_via_github_app'] else None
        self.state_reason = issue_dict['state_reason']

    __tablename__ = "issue"
    # 此issue的唯一标识符
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 此issue的URL
    url = db.Column(db.Text, nullable=False)
    # 包含此issue的存储库的URL
    repository_url = db.Column(db.Text, nullable=False)
    # 此issue的标签URL
    labels_url = db.Column(db.Text, nullable=False)
    # 包含此issue的评论URL
    comments_url = db.Column(db.Text, nullable=False)
    # 此issue的事件URL
    events_url = db.Column(db.Text, nullable=False)
    # 以HTML格式显示此issue的URL
    html_url = db.Column(db.Text, nullable=False)
    # 此issue的节点ID
    node_id = db.Column(db.Text, nullable=False)
    # 此issue的数字标识符
    number = db.Column(db.Integer, nullable=False)
    # 此issue的标题
    title = db.Column(db.Text, nullable=False)
    # 此issue的作者id
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # 此issue的作者，关联User模型
    user = db.relationship('User', backref='issue', lazy=True)
    # 此issue的标签列表，以逗号间隔
    labels = db.Column(db.Text, nullable=False)
    # 此issue的状态，可以是 "open"，"closed"或其他自定义状态
    state = db.Column(db.Text, nullable=False)
    # 如果此issue已被锁定，则为true
    locked = db.Column(db.Boolean, nullable=False)
    # 此issue分配的用户（如果有）
    assignee = db.Column(db.Text, nullable=True)
    # 分配给此issue的所有用户，以逗号间隔
    assignees = db.Column(db.Text, nullable=True)
    # 与此issue相关的里程碑
    milestone = db.Column(db.Text, nullable=True)
    # 与此issue相关的评论数量
    comments = db.Column(db.Integer, nullable=False)
    # 此issue创建的日期和时间
    created_at = db.Column(db.DateTime, nullable=False)
    # 此issue最后更新的日期和时间
    updated_at = db.Column(db.DateTime, nullable=False)
    # 此issue关闭的日期和时间（如果尚未关闭，则为null）
    closed_at = db.Column(db.DateTime, nullable=True)
    # 此issue作者与此存储库的关联程度，例如“成员”或“拥有者”
    author_association = db.Column(db.Text, nullable=False)
    # 如果此issue当前被锁定，则为锁定原因
    active_lock_reason = db.Column(db.Text, nullable=True)
    # 此issue的主体，即详细说明
    body = db.Column(db.Text, nullable=False)
    # # 包含此issue的各种反应的统计信息
    # reactions_id = db.Column(db.Integer, db.ForeignKey('issue.id'))
    # # 包含此issue的各种反应的统计信息
    # reactions = db.relationship('Reactions', backref='issue', lazy=True)
    # 该问题/issue的反应/表情符号的API地址
    reactions_url = db.Column(db.Text, nullable=False)
    # 该问题/issue所收到的反应/表情符号总数
    reactions_total_count = db.Column(db.Integer, nullable=False)
    # 点赞的数量
    reactions_plus_one = db.Column(db.Integer, nullable=False)
    # 踩的数量
    reactions_minus_one = db.Column(db.Integer, nullable=False)
    # 大笑的数量
    reactions_laugh = db.Column(db.Integer, nullable=False)
    # 庆祝的数量
    reactions_hooray = db.Column(db.Integer, nullable=False)
    # 困惑的数量
    reactions_confused = db.Column(db.Integer, nullable=False)
    # 爱心的数量
    reactions_heart = db.Column(db.Integer, nullable=False)
    # 火箭的数量
    reactions_rocket = db.Column(db.Integer, nullable=False)
    # 眼睛的数量
    reactions_eyes = db.Column(db.Integer, nullable=False)
    # 此issue的时间轴URL
    timeline_url = db.Column(db.Text, nullable=True)
    # 如果此issue通过GitHub应用程序创建，则为应用程序信息。
    performed_via_github_app = db.Column(db.Text, nullable=True)
    # 关闭此issue时提供的关闭原因（如果适用）。
    state_reason = db.Column(db.Text, nullable=True)
