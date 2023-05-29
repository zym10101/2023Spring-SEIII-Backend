from dao.IssueDao import get_by_create_time_all


def get_issue_pct(repo_name, start_time, end_time, polarity):
    issues = get_by_create_time_all(repo_name, start_time, end_time)

    if len(issues) == 0:
        return f"该时间段内，{repo_name} issue为空！"

    pos_count = 0
    neg_count = 0
    neutral_count = 0

    for issue in issues:
        result = int(issue.pos_body) + int(issue.neg_body)
        if result > 0:
            pos_count = pos_count + 1
        elif result == 0:
            neutral_count = neutral_count + 1
        else:
            neg_count = neg_count + 1

    if polarity == "pos":
        return pos_count / len(issues)
    else:
        return neg_count / len(issues)


def get_issue_pos_pct(repo_name, start_time, end_time):
    pct = get_issue_pct(repo_name, start_time, end_time, "pos")
    if pct.startswith("该时间段内"):
        return f"该时间段内，{repo_name} issue为空！"
    else:
        return pct


def get_issue_neg_pct(repo_name, start_time, end_time):
    pct = get_issue_pct(repo_name, start_time, end_time, "neg")
    if pct.startswith("该时间段内"):
        return f"该时间段内，{repo_name} issue为空！"
    else:
        return pct
