from dao.Database import db
from model.User import User
from datetime import datetime


# Comment
class Comment(db.Model):
    def __init__(self, issue_dict):
        self.id = issue_dict['id']
        self.url = issue_dict['url']
        self.issue_url = issue_dict['issue_url']
        self.html_url = issue_dict['html_url']
        self.node_id = issue_dict['node_id']

        self.user_id = issue_dict['user']['id']
        self.user = User.query.get(self.user_id)

        self.created_at = datetime.strptime(issue_dict['created_at'], '%Y-%m-%dT%H:%M:%SZ')
        self.updated_at = datetime.strptime(issue_dict['updated_at'], '%Y-%m-%dT%H:%M:%SZ')
        self.author_association = issue_dict['author_association']
        if issue_dict['body'] is not None:
            self.body = issue_dict['body'].encode('utf-8')
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

        self.performed_via_github_app = issue_dict['performed_via_github_app']['name'] if issue_dict[
            'performed_via_github_app'] else None

    __tablename__ = "comment"
    # 此issue comment的唯一标识符
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    # 此comment的URL
    url = db.Column(db.Text, nullable=False)
    # 以HTML格式显示此issue comment的URL
    html_url = db.Column(db.Text, nullable=False)
    # 此issue comment对应的issue链接
    issue_url = db.Column(db.Text, nullable=True)
    # 此issue comment的节点ID
    node_id = db.Column(db.Text, nullable=False)
    # 此issue comment的作者id
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # 此issue的作者，关联User模型
    user = db.relationship('User', backref='comment', lazy=True)
    # 此issue comment创建的日期和时间
    created_at = db.Column(db.DateTime, nullable=False)
    # 此issue comment最后更新的日期和时间
    updated_at = db.Column(db.DateTime, nullable=False)
    # 此issue comment作者与此存储库的关联程度，例如“成员”或“拥有者”
    author_association = db.Column(db.Text, nullable=False)
    # 此issue comment的主体，即详细说明
    body = db.Column(db.Text, nullable=True)
    # body部分SentiStrength评分
    pos_body = db.Column(db.Text, nullable=True)
    neg_body = db.Column(db.Text, nullable=True)
    # 该issue comment的反应/表情符号的API地址
    reactions_url = db.Column(db.Text, nullable=False)
    # 该issue comment所收到的反应/表情符号总数
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
    # 如果此issue comment通过GitHub应用程序创建，则为应用程序信息。
    performed_via_github_app = db.Column(db.Text, nullable=True)

    # 在dao层完成之前临时加了用一下
    @staticmethod
    def read_by_row(session):
        for comment in session.query(Comment):
            yield comment

    def to_dict(self):
        return {
            'id': self.id,
            'url': self.url,
            'html_url': self.html_url,
            'issue_url': self.issue_url,
            'node_id': self.node_id,
            'user': self.user.to_dict() if self.user else None,
            'created_at': self.created_at.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'updated_at': self.updated_at.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'author_association': self.author_association,
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
            'performed_via_github_app': self.performed_via_github_app
        }
