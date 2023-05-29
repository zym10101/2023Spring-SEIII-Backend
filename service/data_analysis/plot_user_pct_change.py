from service.data_analysis.get_issue_senti_pct import get_issue_pos_pct, get_issue_neg_pct
from service.data_analysis.get_comment_senti_pct import get_comment_pct_by_time
from utils.DateUtil import convert_to_iso8601
from utils.plot_pct_change import plot_pct_change


def plot_user_issue_pct_change(repo_name, user, start_time, end_time, intervals):
    if get_issue_pos_pct(repo_name, start_time, end_time) != f"该时间段内，{repo_name} issue为空！":
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
            pos_list.append(get_issue_pos_pct(repo_name, convert_to_iso8601(start_t), convert_to_iso8601(end_t)))
            neg_list.append(get_issue_neg_pct(repo_name, convert_to_iso8601(start_t), convert_to_iso8601(end_t)))

        return plot_pct_change(index, pos_list, neg_list, '用户issue情绪文本占比波动图')


def plot_user_comment_pct_change(repo_name, user, start_time, end_time, intervals):
    if get_comment_pct_by_time(repo_name, start_time, end_time, 'pos') != f"该时间段内，{repo_name} issue为空！":
        index = []
        for i in range(len(intervals)):
            index.append(str(intervals[i]) + '~' + str(intervals[i + 1]))
        # 定义空数组用于保存结果
        pos_list = []
        neg_list = []
        # 循环遍历这些时间点
        for i in range(len(intervals)):
            start_t = intervals[i]
            end_t = intervals[i + 1]
            pos_list.append(get_comment_pct_by_time(repo_name, convert_to_iso8601(start_t), convert_to_iso8601(end_t), 'pos'))
            neg_list.append(get_comment_pct_by_time(repo_name, convert_to_iso8601(start_t), convert_to_iso8601(end_t), 'neg'))

        return plot_pct_change(index, pos_list, neg_list, '用户comment情绪文本占比波动图')
