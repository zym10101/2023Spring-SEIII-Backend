from dao.IssueDao import get_by_create_time_all


def get_all_pct_by_time(repo_name, start_time, end_time, polarity, weighting):
    issues = get_by_create_time_all(repo_name, start_time, end_time)

    if len(issues) == 0:
        return -1

    pos_count = 0
    neg_count = 0
    neutral_count = 0
    count = 0

    for issue in issues:
        count = count + 1
        result = 0
        comments = issue.issue_comments
        for comment in comments:
            count = count + 1
            result = result + int(comment.pos_body) + int(comment.neg_body)
        result = weighting * (int(issue.pos_body) + int(issue.neg_body)) + (1 - weighting) * result
        if result > 0:
            pos_count = pos_count + 1
        elif result == 0:
            neutral_count = neutral_count + 1
        else:
            neg_count = neg_count + 1

    if polarity == "pos":
        return pos_count / count
    elif polarity == "neg":
        return neg_count / count


def get_all_pct(issues, polarity, weighting):
    if len(issues) == 0:
        return -1

    pos_count = 0
    neg_count = 0
    neutral_count = 0
    count = 0

    for issue in issues:
        count = count + 1
        result = 0
        comments = issue.issue_comments
        for comment in comments:
            count = count + 1
            result = result + int(comment.pos_body) + int(comment.neg_body)
        result = weighting * (int(issue.pos_body) + int(issue.neg_body)) + (1 - weighting) * result
        if result > 0:
            pos_count = pos_count + 1
        elif result == 0:
            neutral_count = neutral_count + 1
        else:
            neg_count = neg_count + 1

    if polarity == "pos":
        return pos_count / count
    elif polarity == "neg":
        return neg_count / count
