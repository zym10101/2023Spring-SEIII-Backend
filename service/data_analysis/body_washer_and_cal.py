import re

import pandas as pd

from model.Issue import Issue, IssueComment
from service.data_analysis.cal_senti import cal_senti


# df = pd.read_csv('../../data/superset_issues.csv', keep_default_na=False)


def body_washer_and_cal(db):
    db.session.begin()

    # 生成器
    issues = Issue.read_by_row(db.session)

    while True:
        try:
            issue = next(issues)
            body_value = issue.body
            pattern1 = r'!?\[.*?\]\(.*?\)'
            pattern2 = r'<.*?>'
            body_value = re.sub(pattern1, ' ', str(body_value))
            body_value = re.sub(pattern2, ' ', str(body_value))
            body_value = str(body_value).replace('<!---', '').replace('-->', '')
            result = cal_senti(body_value).split(" ")
            pos = result[0]
            neg = result[1]
            # issue.body = body_value
            issue.pos_body = pos
            issue.neg_body = neg
            db.session.add(issue)
        except StopIteration:
            break

        # 生成器
    issues_comments = IssueComment.read_by_row(db.session)

    while True:
        try:
            issue_comment = next(issues_comments)
            body_value = issue_comment.body
            pattern1 = r'!?\[.*?\]\(.*?\)'
            pattern2 = r'<.*?>'
            body_value = re.sub(pattern1, ' ', str(body_value))
            body_value = re.sub(pattern2, ' ', str(body_value))
            body_value = str(body_value).replace('<!---', '').replace('-->', '')
            result = cal_senti(body_value).split(" ")
            pos = result[0]
            neg = result[1]
            # issue.body = body_value
            issue_comment.pos_body = pos
            issue_comment.neg_body = neg
            db.session.add(issue_comment)
        except StopIteration:
            break


    # 关闭数据库连接
    db.session.commit()

# # 遍历每一行提取body列的值"
# for issue in issues:
#     body_value = issue.body
#     if body_value == "":
#         body_value = "null"
#     pattern1 = r'!?\[.*?\]\(.*?\)'
#     pattern2 = r'<.*?>'
#     body_value = re.sub(pattern1, ' ', str(body_value))
#     body_value = re.sub(pattern2, ' ', str(body_value))
#     body_value = str(body_value).replace('<!---', '').replace('-->', '')
#
#     df.loc[index, 'body'] = body_value
#
# df.to_csv('../../data/superset_issues.csv', index=False)
# # df['body'].to_csv('../../data/issue-body.csv',index=False)
