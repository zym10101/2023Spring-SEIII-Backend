from sqlalchemy import *
import re
from dao.Database import db
from model.User import User
from model.Issue import Issue
from model.Label import Label
from model.Comment import Comment


def save_single(json):
    # 1.创建 User\Label\Comment ORM对象
    users_ = [User(json['user'])]
    labels_ = []
    for label_ in json['labels']:
        labels_.append(Label(label_))
    issue_comments_ = []
    if 'comments_json' in json.keys():
        for comment_ in json['comments_json']:
            issue_comments_.append(Comment(comment_))
            users_.append(User(comment_['user']))

    # 2.创建 issue ORM对象
    issue_ = Issue(json)
    issue_.labels = labels_
    issue_.issue_comments = issue_comments_

    # 3.将ORM对象添加到db.session中
    for user in users_:
        db.session.merge(user)
    db.session.merge(issue_)

    # 4.确认提交
    db.session.commit()


def save_list(json_list):
    for json in json_list:
        save_single(json)


def create_association(repo_name):
    # 根据 repo_name 查询 Issue 表
    issues = Issue.query.filter(Issue.repository_url.endswith(repo_name)).all()

    for issue in issues:
        comments_url = issue.comments_url
        issue_number = re.search(r'/(\d+)/comments', comments_url).group(1)
        issue.issue_comments = Comment.query.filter(Comment.issue_url.endswith(issue_number)).all()

    # 保存修改到数据库
    db.session.commit()


def get_by_repository(repo_name):
    return Issue.query.filter(Issue.repository_url.endswith(repo_name)).all()


def get_by_create_time_all(repo_name, begin_time, end_time):  # 左闭右开
    return Issue.query \
        .filter(Issue.repository_url.endswith(repo_name)) \
        .filter(Issue.created_at.between(begin_time, end_time)) \
        .all()


def get_by_create_time_page(repo_name, begin_time, end_time, page_number, page_size):  # 左闭右开
    pagination = Issue.query \
        .filter(Issue.repository_url.endswith(repo_name)) \
        .filter(Issue.created_at.between(begin_time, end_time)) \
        .paginate(page=page_number, per_page=page_size)
    return pagination.items


def get_by_row(repo_name):
    for issue in Issue.query.filter(Issue.repository_url.endswith(repo_name)):
        yield issue


def get_issues_by_label_name(repo_name, label_name, begin_time, end_time):
    labels = Label.query.filter(Label.name == label_name).all()
    label_id = [label.id for label in labels]

    # issues = Issue.query.all()
    # for id in label_id:
    #     for issue in issues:
    #         issue_labels = issue.labels
    #         for issue_label in issue_labels:
    #             if issue_label.id == id:
    #                 print(issue)


    issues = list(set(Issue.query.filter(Issue.labels.any(or_(*[Label.id == id for id in label_id]))) \
                      .filter(Issue.repository_url.endswith(repo_name)) \
                      .filter(Issue.created_at.between(begin_time, end_time)) \
                      .all()))
    return issues


def get_issues_by_reactions(repo_name, begin_time, end_time, reaction, nums=1):
    query = Issue.query \
        .filter(Issue.repository_url.endswith(repo_name)) \
        .filter(Issue.created_at.between(begin_time, end_time))
    column = getattr(Issue, "reactions_" + reaction)
    query = query.filter(column >= nums)
    results = query.all()
    return results


def template():
    # 1.条件查询
    # 查询用户名为 "john" 的用户
    user = User.query.filter(User.username == 'john').first()
    # 查询邮箱以 "@example.com" 结尾的用户
    users = User.query.filter(User.email.endswith('@example.com')).all()
    # 查询 id 在指定范围内的用户
    users = User.query.filter(User.id.between(1, 10)).all()

    # 2.排序查询
    users = User.query.order_by(User.username.asc()).all()

    # 3.分页查询
    page_number = 1
    page_size = 10
    pagination = User.query.paginate(page_number, per_page=page_size)
    users = pagination.items

    # 4.关联查询
    user = User.query.get(user_id)
    posts = user.posts.all()


if __name__ == '__main__':
    from app_template import app
    from datetime import datetime

    with app.app_context():
        create_association('apache/tomcat')
        # begin = datetime(2023, 3, 15)
        # end = datetime(2023, 3, 17)
        # result = get_by_create_time_page('flink', begin, end, 2, 5)
        # for each in result:
        #     print(each.id)
        # print('查询到{}条'.format(len(result)))
