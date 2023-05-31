from service.data_analysis.get_comment_senti_pct import get_comment_pct_by_time
from service.data_analysis.get_senti_pct_by_user import get_issue_senti_pct_by_user, get_comment_senti_pct_by_user
from utils.DateUtil import convert_to_iso8601


def plot_user_issue_pct_change(repo_name, user, intervals):
    index = []
    for i in range(len(intervals)-1):
        index.append(str(intervals[i]) + '~' + str(intervals[i + 1]))
    # 定义空数组用于保存结果
    pos_list = []
    neg_list = []
    # 循环遍历这些时间点
    for i in range(len(intervals)-1):
        start_t = intervals[i]
        end_t = intervals[i + 1]
        pos_list.append(get_issue_senti_pct_by_user(repo_name, user, convert_to_iso8601(start_t), convert_to_iso8601(end_t), 'pos'))
        neg_list.append(get_issue_senti_pct_by_user(repo_name, user, convert_to_iso8601(start_t), convert_to_iso8601(end_t), 'neg'))

    return [index, pos_list, neg_list, '用户issue情绪文本占比波动图', 'Date']


def plot_user_comment_pct_change(repo_name, user, intervals):
    index = []
    for i in range(len(intervals) - 1):
        index.append(str(intervals[i]) + '~' + str(intervals[i + 1]))
    # 定义空数组用于保存结果
    pos_list = []
    neg_list = []
    # 循环遍历这些时间点
    for i in range(len(intervals) - 1):
        start_t = intervals[i]
        end_t = intervals[i + 1]
        pos_list.append(
            get_comment_senti_pct_by_user(repo_name, user, convert_to_iso8601(start_t), convert_to_iso8601(end_t), 'pos'))
        neg_list.append(
            get_comment_senti_pct_by_user(repo_name, user, convert_to_iso8601(start_t), convert_to_iso8601(end_t), 'neg'))

    return [index, pos_list, neg_list, '用户comment情绪文本占比波动图', 'Date']
