from dao.UserDao import get_issues_by_id
from dao.UserDao import get_comments_by_id
import dao.IssueDao
from service.data_analysis import get_issue_senti_pct, get_comment_senti_pct, get_all_senti_pct
from service.data_analysis.get_comment_senti_pct import get_comment_pct
from service.data_analysis.get_issue_senti_pct import get_issue_pct


# 根据label name获取这个label的情绪值占比
def get_issue_senti_pct_by_user(repo_name, user, begin_time, end_time, polarity):
    issues = get_issues_by_id(repo_name, begin_time, end_time, user)
    return get_issue_senti_pct.get_issue_pct(issues, polarity)


def get_comment_senti_pct_by_user(repo_name, user, begin_time, end_time, polarity):
    comments = get_comments_by_id(repo_name, begin_time, end_time, user)
    return get_comment_senti_pct.get_comment_pct(comments, polarity)


def get_all_senti_pct_by_user(repo_name, user, begin_time, end_time, polarity, weighting):
    issues = get_issues_by_id(repo_name, begin_time, end_time, user)
    comments = get_comments_by_id(repo_name, begin_time, end_time, user)
    if len(issues)==0:
        weighting = 0
    if len(comments)==0:
        weighting = 1
    result = get_issue_pct(issues, polarity) * weighting + get_comment_pct(comments, polarity) * (1 - weighting)
    return result
