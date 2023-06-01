from dao.IssueDao import get_by_create_time_all


# 获取一段时间内所有issue的comment列表积极/消极情绪值占比
def get_comment_pct_by_time(repo_name, start_time, end_time, polarity):
    issues = get_by_create_time_all(repo_name, start_time, end_time)

    if len(issues) == 0:
        return -1

    pos_count = 0
    neg_count = 0
    neutral_count = 0
    count = 0

    for issue in issues:
        comments = issue.issue_comments
        for comment in comments:
            count = count + 1
            result = int(comment.pos_body) + int(comment.neg_body)
            if result > 0:
                pos_count = pos_count + 1
            elif result == 0:
                neutral_count = neutral_count + 1
            else:
                neg_count = neg_count + 1

    if count == 0:
        return -1

    if polarity == "pos":
        return round(pos_count / count, 2)
    elif polarity == "neg":
        return round(neg_count / count, 2)


# 根据issue名获取单个issue的comment列表积极/消极情绪值占比
def get_comment_pct_by_issue(issue, polarity):
    comments = issue.issue_comments

    if len(comments) == 0:
        return -1

    pos_count = 0
    neg_count = 0
    neutral_count = 0

    for comment in comments:
        result = int(comment.pos_body) + int(comment.neg_body)
        if result > 0:
            pos_count = pos_count + 1
        elif result == 0:
            neutral_count = neutral_count + 1
        else:
            neg_count = neg_count + 1

    if polarity == "pos":
        return round(pos_count / len(comments), 2)
    elif polarity == "neg":
        return round(neg_count / len(comments), 2)


# 根据comment列表获取积极/消极情绪值占比
def get_comment_pct(comments, polarity):
    if len(comments) == 0:
        return -1

    pos_count = 0
    neg_count = 0
    neutral_count = 0

    for comment in comments:
        result = int(comment.pos_body) + int(comment.neg_body)
        if result > 0:
            pos_count = pos_count + 1
        elif result == 0:
            neutral_count = neutral_count + 1
        else:
            neg_count = neg_count + 1

    if polarity == "pos":
        return round(pos_count / len(comments), 2)
    elif polarity == "neg":
        return round(neg_count / len(comments), 2)
