from dao.IssueDao import get_issues_by_label_name
from dao.Database import db
from model.Comment import Comment
from model.Issue import Issue
from model.IssueComment import IssueComment
from model.User import User


def save_single(json):
    # 1.创建 User\Comment ORM对象
    user = User(json['user'])
    comment = Comment(json)

    # 2.将ORM对象添加到db.session中
    db.session.merge(user)
    db.session.merge(comment)

    # 3.确认提交
    db.session.commit()


def save_list(json_list):
    for json in json_list:
        save_single(json)


# 根据label_name获取对应的issue的comments
def get_comments_by_label_name(repo_name, label_name, begin_time, end_time):
    issues = get_issues_by_label_name(repo_name, label_name, begin_time, end_time)
    comments = []
    for issue in issues:
        comments.extend(issue.issue_comments)
    return comments


def get_comments_by_reactions(repo_name, begin_time, end_time, reaction, nums=1):
    comments = Comment.query \
        .join(IssueComment) \
        .join(Issue) \
        .filter(Issue.repository_url.endswith(repo_name)) \
        .filter(Issue.created_at.between(begin_time, end_time)) \
        .filter(getattr(Comment, "reactions_" + reaction) >= nums) \
        .all()
    # 返回结果
    return comments
