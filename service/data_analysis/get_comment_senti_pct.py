from dao.IssueDao import get_by_create_time_all


# 获取一段时间内所有issue的comment列表积极/消极情绪值占比
def get_comment_pct_by_time(repo_name, start_time, end_time, polarity):
    issues = get_by_create_time_all(repo_name, start_time, end_time)

    if len(issues) == 0:
        return f"该时间段内，{repo_name} issue为空！"

    pos_count = 0
    neg_count = 0
    neutral_count = 0

    for issue in issues:
        comments = issue.issue_comments
        for comment in comments:
            result = int(comment.pos_body) + int(comment.neg_body)
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


# 根据issue名获取单个issue的comment列表积极/消极情绪值占比
def get_comment_pct_by_issue(issue, polarity):
    comments = issue.issue_comments

    if len(comments) == 0:
        return f"该issue的comment为空！"

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
        return pos_count / len(comments)
    else:
        return neg_count / len(comments)
