from dao.Database import db
from model.User import User
from model.IssueComment import IssueComment


def save_single(self, json):
    # 1.创建 User\Label ORM对象
    user_ = User(json['user'])

    # 2.创建 issue comment ORM对象
    issue_comment_ = IssueComment(json)

    # 3.将ORM对象添加到db.session中
    db.session.merge(user_)
    db.session.merge(issue_comment_)

    # 4.确认提交
    db.session.commit()
