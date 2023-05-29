from dao.IssueDao import get_by_reactions
from service.data_analysis import get_issue_senti_pct


def get_issue_senti_pct_by_reaction(repo, reaction, start_time, end_time, polarity):
    issues = get_by_reactions(repo, reaction, start_time, end_time)
    return get_issue_senti_pct.get_issue_pct(issues, polarity)


def get_comment_senti_pct_by_reaction(repo, reaction, start_time, end_time, polarity):
    return []
