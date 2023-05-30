from sqlalchemy import *

from dao.Database import db
from model.User import User
from model.Issue import Issue
from model.Label import Label
from model.Comment import Comment


def get_by_id(id):
    return User.query.get(id)


def get_issues_and_by_id(id):
    user = get_by_id(id)
    return user.issue


def get_commenys_by_id(id):
    user = get_by_id(id)
    return user.comment


if __name__ == '__main__':
    from app_template import app
    from datetime import datetime

    # with app.app_context():
    #     uid = 40265686
    #     comments, issues = get_all_issues_and_comments_by_id(uid)
    #     print(1)
