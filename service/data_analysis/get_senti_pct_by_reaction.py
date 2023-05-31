from dao.IssueDao import get_issues_by_reactions
from dao.CommentDao import get_comments_by_reactions
from service.data_analysis import get_issue_senti_pct, get_comment_senti_pct
from service.data_analysis.get_comment_senti_pct import get_comment_pct
from service.data_analysis.get_issue_senti_pct import get_issue_pct


def get_issue_senti_pct_by_reaction(repo, reaction, start_time, end_time, polarity):
    issues = get_issues_by_reactions(repo, start_time, end_time, reaction)
    return get_issue_senti_pct.get_issue_pct(issues, polarity)


def get_comment_senti_pct_by_reaction(repo, reaction, start_time, end_time, polarity):
    comments = get_comments_by_reactions(repo, start_time, end_time, reaction)
    return get_comment_senti_pct.get_comment_pct(comments, polarity)


def get_all_senti_pct_by_reaction(repo, reaction, start_time, end_time, polarity, weighting):
    issues = get_issues_by_reactions(repo, start_time, end_time, reaction)
    comments = get_comments_by_reactions(repo, start_time, end_time, reaction)
    if len(issues) == 0:
        weighting = 0
    if len(comments) == 0:
        weighting = 1
    result = get_issue_pct(issues, polarity) * weighting + get_comment_pct(comments, polarity) * (1 - weighting)
    return result
