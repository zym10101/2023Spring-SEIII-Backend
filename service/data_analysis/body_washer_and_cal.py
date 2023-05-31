import re
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor

import jpype
from multiprocessing import Pool

from model.Issue import Issue
from model.Comment import Comment

from service.data_analysis.cal_senti import cal_senti


# df = pd.read_csv('../../data/superset_issues.csv', keep_default_na=False)


# init = False
# sentistrengths = []
#
#
# def init_sentistrength():
#     global init
#     global sentistrength
#     if not init:
#         for i in range(5):
#             sentistrength = jpype.JClass("uk.ac.wlv.sentistrength.SentiStrength")
#             ss = sentistrength()
#             sentistrengths.append(ss)
#         init = True
#
#
# def cal_senti(body):
#     sentistrength = sentistrengths[0]
#     result = sentistrength.initialiseAndRun(['sentidata', "./sentistrength/SentiStrength_Data/", "text", body])
#     # print(result)
#     return result
#
#
# def process(obj):
#     body_value = obj.body
#     pattern1 = r'!?\[.*?\]\(.*?\)'
#     pattern2 = r'<.*?>'
#     body_value = re.sub(pattern1, ' ', str(body_value))
#     body_value = re.sub(pattern2, ' ', str(body_value))
#     body_value = str(body_value).replace('<!---', '').replace('-->', '')
#     result = cal_senti(body_value).split(" ")
#     pos = result[0]
#     neg = result[1]
#     obj.pos_body = pos
#     obj.neg_body = neg
#     return obj
#
#
# def body_washer_and_cal(db):
#     db.session.begin()
#     init_sentistrength()
#
#     issues = Issue.read_by_row(db.session)
#
#     with ThreadPoolExecutor() as executor:
#         while True:
#             try:
#                 issue = next(issues)
#                 future = executor.submit(process, issue)
#                 result = future.result()
#                 db.session.add(result)
#             except StopIteration:
#                 break
#
#     comments = Comment.read_by_row(db.session)
#
#     with ThreadPoolExecutor() as executor:
#         while True:
#             try:
#                 comment = next(comments)
#                 future = executor.submit(process, comment)
#                 result = future.result()
#                 db.session.add(result)
#             except StopIteration:
#                 break
#
#     db.session.commit()

def body_washer_and_cal(db):
    db.session.begin()

    # 生成器
    issues = Issue.read_by_row(db.session)

    while True:
        try:
            issue = next(issues)
            #生成issue.body的情绪值
            if issue.pos_body is None:
                body_value = issue.body
                if body_value != '':
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
                else:
                    issue.pos_body = 0
                    issue.neg_body = 0
                    db.session.add(issue)
        except StopIteration:
            break

    # 生成器
    issues_comments = Comment.read_by_row(db.session)

    while True:
        try:
            issue_comment = next(issues_comments)
            if issue_comment.pos_body is None:
                body_value = issue_comment.body
                if body_value != '':
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
                else:
                    issue_comment.pos_body = 0
                    issue_comment.neg_body = 0
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
