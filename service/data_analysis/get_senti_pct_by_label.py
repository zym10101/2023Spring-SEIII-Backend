import dao.CommentDao
import dao.IssueDao
from service.data_analysis import get_issue_senti_pct, get_comment_senti_pct, get_all_senti_pct


# 根据label name获取拥有这个label的issue的情绪值占比
def get_issue_senti_pct_by_label(repo_name, label_name, begin_time, end_time, polarity):
    issues = dao.IssueDao.get_issues_by_label_name(repo_name, label_name, begin_time, end_time)
    return get_issue_senti_pct.get_issue_pct(issues, polarity)


# 根据label name获取拥有这个label的issue的comment的情绪值占比
def get_comment_senti_pct_by_label(repo_name, label_name, begin_time, end_time, polarity):
    comments = dao.CommentDao.get_comments_by_label_name(repo_name, label_name, begin_time, end_time)
    return get_comment_senti_pct.get_comment_pct(comments, polarity)


def get_all_senti_pct_by_label(repo_name, label_name, begin_time, end_time, polarity, weighting):
    issues = dao.IssueDao.get_issues_by_label_name(repo_name, label_name, begin_time, end_time)
    return get_all_senti_pct.get_all_pct(issues, polarity, weighting)
