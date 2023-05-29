from dao.IssueDao import get_issues_by_label_name
from model.Comment import Comment
from model.Issue import Issue
from model.IssueComment import IssueComment


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
