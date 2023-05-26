import re

import pandas as pd

from model.vo.issue import Issue

# df = pd.read_csv('../../data/superset_issues.csv', keep_default_na=False)


def body_washer(db):
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
            issue.body = body_value
            db.session.add(issue)
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
