from dao.Database import db
from model.User import User
from model.Issue import Issue
from model.Label import Label


class IssueDaoClass:
    def __init__(self):
        self.session = db.session

    def save_single(self, json):
        # 1.创建 User\Label ORM对象
        user_ = User(json['user'])
        labels_ = []
        for label_ in json['labels']:
            labels_.append(Label(label_))

        # 2.创建 issue ORM对象
        issue_ = Issue(json)
        issue_.labels = labels_
        print(issue_.labels)

        # 3.将ORM对象添加到db.session中
        self.session.merge(user_)
        self.session.merge(issue_)

        # 4.确认提交
        self.session.commit()


IssueDao = IssueDaoClass()
