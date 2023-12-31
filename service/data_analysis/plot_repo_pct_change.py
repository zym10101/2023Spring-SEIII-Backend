from service.data_analysis.get_all_senti_pct import get_all_pct_by_time
from service.data_analysis.get_issue_senti_pct import get_issue_pct_by_time
from service.data_analysis.get_comment_senti_pct import get_comment_pct_by_time
from utils.DateUtil import convert_to_iso8601


# start_time, end_time使用了convert_to_iso8601方法，输入类型与该方法一致；如果dao层时间类型非iso8601则修改
# intervals参数详见utils.get_plot_intervals
# 关于返回图像：
# 首先使用 `json.dumps()` 方法将 `go.Figure` 对象转换为 JSON 格式的字符串
# 并使用 Flask 的 `render_template` 方法将这个字符串作为参数传递给前端模板。
# 在前端模板中，可以使用 JavaScript 或其他前端框架来解析 JSON 并渲染图表。
def plot_repo_issue_pct_change(repo_name, start_time, end_time, intervals):
    if get_issue_pct_by_time(repo_name, start_time, end_time, 'pos') != f"该时间段内，{repo_name} issue为空！":
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
            pos = get_issue_pct_by_time(repo_name, convert_to_iso8601(start_t), convert_to_iso8601(end_t), 'pos')
            if pos == -1:
                pos = 0.0
                neg = 0.0
                neu = 0.0
            else:
                neg = get_issue_pct_by_time(repo_name, convert_to_iso8601(start_t), convert_to_iso8601(end_t), 'neg')
                neu = 1 - pos - neg

            pos_list.append(round(pos, 4))
            neg_list.append(round(neg, 4))
            neu_list.append(round(neu, 4))

        return {"title": "项目issue",
                "data":{
                    "pos": pos_list,
                    "neg": neg_list,
                    "neu": neu_list,
                    "xAxis": index
                },
                }
        # return [index, pos_list, neu_list, neg_list, '项目issue情绪文本占比波动图', 'Date']


def plot_repo_comment_pct_change(repo_name, start_time, end_time, intervals):
    if get_comment_pct_by_time(repo_name, start_time, end_time, 'pos') != f"该时间段内，{repo_name} issue为空！":
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
            pos = get_comment_pct_by_time(repo_name, convert_to_iso8601(start_t), convert_to_iso8601(end_t), 'pos')
            if pos == -1:
                pos = 0.0
                neg = 0.0
                neu = 0.0
            else:
                neg = get_comment_pct_by_time(repo_name, convert_to_iso8601(start_t), convert_to_iso8601(end_t), 'neg')
                neu = 1 - pos - neg

            pos_list.append(round(pos, 4))
            neg_list.append(round(neg, 4))
            neu_list.append(round(neu, 4))

        return {"title": "项目comment",
                # "data": [pos_list, neu_list, neg_list],
                "data":{
                    "pos": pos_list,
                    "neg": neg_list,
                    "neu": neu_list,
                    "xAxis": index
                },

                }
        # return [index, pos_list, neu_list, neg_list, '项目issue comment情绪文本占比波动图', 'Date']


# weighting是issue权重
def plot_repo_all_pct_change(repo_name, start_time, end_time, intervals, weighting):
    if get_all_pct_by_time(repo_name, start_time, end_time, 'pos', weighting) != f"该时间段内，{repo_name} issue为空！":
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
            pos = get_all_pct_by_time(repo_name, convert_to_iso8601(start_t), convert_to_iso8601(end_t), 'pos',
                                      weighting)
            if pos == -1:
                pos = 0.0
                neg = 0.0
                neu = 0.0
            else:
                neg = get_all_pct_by_time(repo_name, convert_to_iso8601(start_t), convert_to_iso8601(end_t), 'neg',
                                      weighting)
                neu = 1 - pos - neg

            pos_list.append(round(pos, 4))
            neg_list.append(round(neg, 4))
            neu_list.append(round(neu, 4))

        return {"title": "项目issue+comment",
                # "data": [pos_list, neu_list, neg_list],
                "data": {
                    "pos": pos_list,
                    "neg": neg_list,
                    "neu": neu_list,
                    "xAxis": index
                },

                }
        # return [index, pos_list, neu_list, neg_list, 'Date']
