from dao.UserDao import get_issues_by_id
from dao.UserDao import get_comments_by_id
import dao.IssueDao
from service.data_analysis import get_issue_senti_pct, get_comment_senti_pct


# 根据label name获取这个label的情绪值占比
def get_issue_senti_pct_by_user(repo_name, user, begin_time, end_time, polarity):
    issues = get_issues_by_id(repo_name, begin_time, end_time, user)
    return get_issue_senti_pct.get_issue_pct(issues,polarity)


def get_comment_senti_pct_by_user(repo_name, user, begin_time, end_time, polarity):
    comments = get_comments_by_id(repo_name, begin_time, end_time, user)
    return get_comment_senti_pct.get_comment_pct(comments, polarity)