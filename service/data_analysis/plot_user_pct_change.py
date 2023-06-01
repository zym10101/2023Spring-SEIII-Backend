from service.data_analysis.get_comment_senti_pct import get_comment_pct_by_time
from service.data_analysis.get_senti_pct_by_user import get_issue_senti_pct_by_user, get_comment_senti_pct_by_user, \
    get_all_senti_pct_by_user
from utils.DateUtil import convert_to_iso8601


def plot_user_issue_pct_change(repo_name, user, intervals):
    index = []
    for i in range(len(intervals)-1):
        index.append(str(intervals[i]) + '~' + str(intervals[i + 1]))
    # 定义空数组用于保存结果
    pos_list = []
    neg_list = []
    neu_list = []
    # 循环遍历这些时间点
    for i in range(len(intervals)-1):
        start_t = intervals[i]
        end_t = intervals[i + 1]
        pos = get_issue_senti_pct_by_user(repo_name, user, convert_to_iso8601(start_t), convert_to_iso8601(end_t), 'pos')
        if pos == -1:
            pos = 0.0
            neg = 0.0
            neu = 0.0
        else:
            neg = get_issue_senti_pct_by_user(repo_name, user, convert_to_iso8601(start_t), convert_to_iso8601(end_t), 'neg')
            neu = 1 - pos - neg

        pos_list.append(round(pos, 4))
        neg_list.append(round(neg, 4))
        neu_list.append(round(neu, 4))

    return {"title": "用户issue情绪文本占比波动图",
            "data":{
                "pos": pos_list,
                "neg": neg_list,
                "neu": neu_list,
                "xAxis": index
            }
            }
    # return [index, pos_list, neu_list, neg_list, 'Date']
    # return [index, pos_list, neu_list, neg_list, '用户issue情绪文本占比波动图', 'Date']


def plot_user_comment_pct_change(repo_name, user, intervals):
    index = []
    for i in range(len(intervals) - 1):
        index.append(str(intervals[i]) + '~' + str(intervals[i + 1]))
    # 定义空数组用于保存结果
    pos_list = []
    neg_list = []
    neu_list = []
    # 循环遍历这些时间点
    for i in range(len(intervals) - 1):
        start_t = intervals[i]
        end_t = intervals[i + 1]
        pos = get_comment_senti_pct_by_user(repo_name, user, convert_to_iso8601(start_t), convert_to_iso8601(end_t), 'pos')
        if pos == -1:
            pos = 0.0
            neg = 0.0
            neu = 0.0
        else:
            neg = get_comment_senti_pct_by_user(repo_name, user, convert_to_iso8601(start_t), convert_to_iso8601(end_t), 'neg')
            neu = 1 - pos - neg

        pos_list.append(round(pos, 4))
        neg_list.append(round(neg, 4))
        neu_list.append(round(neu, 4))

    return {"title": "用户comment情绪文本占比波动图",
            "data": {
                "pos": pos_list,
                "neg": neg_list,
                "neu": neu_list,
                "xAxis": index
            }
            }
    # return [index, pos_list, neu_list, neg_list, 'Date']
    # return [index, pos_list, neu_list, neg_list, '用户comment情绪文本占比波动图', 'Date']


def plot_user_all_pct_change(repo_name, user, intervals, weighting):
    index = []
    for i in range(len(intervals) - 1):
        index.append(str(intervals[i]) + '~' + str(intervals[i + 1]))
    # 定义空数组用于保存结果
    pos_list = []
    neg_list = []
    neu_list = []
    # 循环遍历这些时间点
    for i in range(len(intervals) - 1):
        start_t = intervals[i]
        end_t = intervals[i + 1]
        pos = get_all_senti_pct_by_user(repo_name, user, convert_to_iso8601(start_t), convert_to_iso8601(end_t), 'pos', weighting)
        if pos == -1:
            pos = 0.0
            neg = 0.0
            neu = 0.0
        else:
            neg = get_all_senti_pct_by_user(repo_name, user, convert_to_iso8601(start_t), convert_to_iso8601(end_t), 'neg', weighting)
            neu = 1 - pos - neg

        pos_list.append(round(pos, 4))
        neg_list.append(round(neg, 4))
        neu_list.append(round(neu, 4))

    return {"title": "用户issue+comment情绪文本占比波动图",
            "data": {
                "pos": pos_list,
                "neg": neg_list,
                "neu": neu_list,
                "xAxis": index
            }
            }
    # return [index, pos_list, neu_list, neg_list, 'Date']