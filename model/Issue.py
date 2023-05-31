from dao.Database import db
from model.IssueLabel import IssueLabel
from model.IssueComment import IssueComment
from model.User import User
from datetime import datetime


# Issue
class Issue(db.Model):
    def __init__(self, issue_dict):
        self.id = issue_dict['id']
        self.url = issue_dict['url']
        self.html_url = issue_dict['html_url']
        self.repository_url = issue_dict['repository_url']
        self.labels_url = issue_dict['labels_url']
        self.comments_url = issue_dict['comments_url']
        self.events_url = issue_dict['events_url']
        self.number = issue_dict['number']
        self.node_id = issue_dict['node_id']
        self.title = issue_dict['title']

        self.user_id = issue_dict['user']['id']
        self.user = User.query.get(self.user_id)

        self.state = issue_dict['state']
        self.locked = issue_dict['locked']
        self.assignee = issue_dict['assignee']['id'] if issue_dict['assignee'] else None
        self.assignees = ",".join(list(map(str, [assignee['id'] for assignee in issue_dict['assignees']])))
        self.milestone = issue_dict['milestone']['title'] if issue_dict['milestone'] else None
        self.comments = issue_dict['comments']
        self.created_at = datetime.strptime(issue_dict['created_at'], '%Y-%m-%dT%H:%M:%SZ')
        self.updated_at = datetime.strptime(issue_dict['updated_at'], '%Y-%m-%dT%H:%M:%SZ')
        self.closed_at = datetime.strptime(issue_dict['closed_at'], '%Y-%m-%dT%H:%M:%SZ') if issue_dict[
            'closed_at'] else None
        self.author_association = issue_dict['author_association']
        self.active_lock_reason = issue_dict['active_lock_reason']

        self.draft = issue_dict['draft'] if 'draft' in issue_dict.keys() else None
        if 'pull_request' in issue_dict.keys():
            self.pull_request_url = issue_dict['pull_request']['url']
            self.pull_request_html_url = issue_dict['pull_request']['html_url']
            self.pull_request_diff_url = issue_dict['pull_request']['diff_url']
            self.pull_request_patch_url = issue_dict['pull_request']['patch_url']
            self.pull_request_merged_at = issue_dict['pull_request']['merged_at']

        if issue_dict['body'] is not None and len(str(issue_dict['body'])) < 65536:
            self.body = issue_dict['body'].encode('utf-8')
        else:
            self.body = ""

        self.pos_body = None
        self.neg_body = None
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
        self.performed_via_github_app = issue_dict['performed_via_github_app']['name'] if issue_dict[
            'performed_via_github_app'] else None
        self.state_reason = issue_dict['state_reason']

    __tablename__ = "issue"
    # 此issue的唯一标识符
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
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
    # 此issue的标签列表
    labels = db.relationship('Label', secondary=IssueLabel, backref=db.backref('issues', lazy='dynamic'))
    # 此issue的comments列表
    issue_comments = db.relationship('Comment', secondary=IssueComment, backref=db.backref('issues', lazy='dynamic'))
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
    # 问题是否处于草稿状态
    draft = db.Column(db.Boolean, nullable=True)
    # 拉取请求的API URL，可以使用该URL获取有关拉取请求的详细信息
    pull_request_url = db.Column(db.Text, nullable=True)
    # 拉取请求的HTML URL，可以使用该URL在网页浏览器中打开拉取请求
    pull_request_html_url = db.Column(db.Text, nullable=True)
    # 拉取请求的差异（diff）URL，可以使用该URL查看拉取请求中更改的具体差异
    pull_request_diff_url = db.Column(db.Text, nullable=True)
    # 拉取请求的补丁（patch）URL，可以使用该URL下载拉取请求的补丁文件
    pull_request_patch_url = db.Column(db.Text, nullable=True)
    # 拉取请求合并的时间戳。如果该值为null，则表示该拉取请求尚未合并
    pull_request_merged_at = db.Column(db.Text, nullable=True)
    # 此issue的主体，即详细说明
    body = db.Column(db.Text, nullable=True)
    # body部分SentiStrength评分
    pos_body = db.Column(db.Text, nullable=True)
    neg_body = db.Column(db.Text, nullable=True)
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

    @staticmethod
    def read_by_row(session):
        for issue in session.query(Issue):
            yield issue

    def to_dict(self):
        issue_dict = {
            'id': self.id,
            'url': self.url,
            'repository_url': self.repository_url,
            'labels_url': self.labels_url,
            'comments_url': self.comments_url,
            'events_url': self.events_url,
            'html_url': self.html_url,
            'node_id': self.node_id,
            'number': self.number,
            'title': self.title,
            'user': self.user.to_dict() if self.user else None,
            'labels': [label.to_dict() for label in self.labels],
            'issue_comments': [issue_comment.to_dict() for issue_comment in self.issue_comments],
            'state': self.state,
            'locked': self.locked,
            'assignee': self.assignee,
            'assignees': self.assignees,
            'milestone': self.milestone,
            'comments': self.comments,
            'created_at': self.created_at.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'updated_at': self.updated_at.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'closed_at': self.closed_at.strftime('%Y-%m-%dT%H:%M:%SZ') if self.closed_at else None,
            'author_association': self.author_association,
            'active_lock_reason': self.active_lock_reason,
            'draft': self.draft,
            'pull_request_url': self.pull_request_url,
            'pull_request_html_url': self.pull_request_html_url,
            'pull_request_diff_url': self.pull_request_diff_url,
            'pull_request_patch_url': self.pull_request_patch_url,
            'pull_request_merged_at': self.pull_request_merged_at,
            'body': self.body,
            'pos_body': self.pos_body,
            'neg_body': self.neg_body,
            'reactions_url': self.reactions_url,
            'reactions_total_count': self.reactions_total_count,
            'reactions_plus_one': self.reactions_plus_one,
            'reactions_minus_one': self.reactions_minus_one,
            'reactions_laugh': self.reactions_laugh,
            'reactions_hooray': self.reactions_hooray,
            'reactions_confused': self.reactions_confused,
            'reactions_heart': self.reactions_heart,
            'reactions_rocket': self.reactions_rocket,
            'reactions_eyes': self.reactions_eyes,
            'timeline_url': self.timeline_url,
            'performed_via_github_app': self.performed_via_github_app,
            'state_reason': self.state_reason
        }

        return issue_dict
