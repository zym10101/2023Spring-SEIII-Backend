from sqlalchemy import *

from dao.Database import db
from model.User import User
from model.Issue import Issue
from model.Label import Label
from model.IssueComment import IssueComment
from model.Comment import Comment


def get_issue_users(repo_name, begin_time, end_time):
    users_list = [issue.user for issue in Issue.query \
        .filter(Issue.repository_url.endswith(repo_name)) \
        .filter(Issue.created_at.between(begin_time, end_time)) \
        .all()]
    users = list(set(element for sublist in users_list for element in sublist))
    user_names = [user.login for user in users]
    return user_names


def get_comment_users(repo_name, begin_time, end_time):
    users_list = [comment.user for comment in Comment.query.filter(Issue.repository_url.endswith(repo_name)) \
        .filter(Issue.created_at.between(begin_time, end_time)).all()]
    users = list(set(element for sublist in users_list for element in sublist))
    user_names = [user.login for user in users]
    return user_names


def get_id_by_name(user_name):
    user = User.query.filter(User.login == user_name)
    for u in user:
        uid = u.id
    return uid


def get_by_id(uid):
    return User.query.get(uid)


def get_issues_by_id(repo_name, begin_time, end_time, username):
    uid = get_id_by_name(username)
    issues = Issue.query.filter(Issue.repository_url.endswith(repo_name)) \
        .filter(Issue.created_at.between(begin_time, end_time)) \
        .filter(Issue.user_id == uid) \
        .all()
    return issues


def get_comments_by_id(repo_name, begin_time, end_time, username):
    uid = get_id_by_name(username)
    comments = Comment.query.filter(Comment.issue_url.contains(repo_name)) \
        .filter(Comment.user_id == uid) \
        .filter(Issue.created_at.between(begin_time, end_time)) \
        .join(IssueComment) \
        .join(Issue) \
        .all()
    return comments


if __name__ == '__main__':
    from app_template import app
    from datetime import datetime

    # with app.app_context():
    #     uid = 22429695
    #     issues = get_comments_by_id('apache/superset', '2023-02-15', '2023-04-15', uid)
    #     print(1)
