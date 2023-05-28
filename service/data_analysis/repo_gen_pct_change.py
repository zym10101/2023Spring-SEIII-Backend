import plotly.graph_objs as go
from service.data_analysis.get_issue_senti_pct import get_issue_pos_pct, get_issue_neg_pct
import datetime
import math


def plot_pct_over_time(repo_name, start_time, end_time):
    if get_issue_pos_pct(repo_name, start_time, end_time) != f"该时间段内，{repo_name} issue为空！":
        # 准备数据，将总体之间划分为指定间隔，假设为固定的8个间隔
        # 计算日期间隔的总天数
        time_interval = start_time - end_time
        total_days = time_interval.days
        # 计算每个区间的天数
        interval_days = math.ceil(total_days / 8)
        # 计算每个区间的起始日期和结束日期
        current_date = start_time
        intervals = []
        for i in range(8):
            interval_start = current_date
            interval_end = current_date + datetime.timedelta(days=interval_days)
            intervals.append((interval_start, interval_end))
            current_date = interval_end

        # 如果最后一个区间的结束日期不等于总日期间隔的结束日期，则将最后一个区间的结束日期设置为总日期间隔的结束日期
        if intervals[-1][1] != end_time:
            intervals[-1] = (intervals[-1][0], end_time)
        index = []
        for i in range(8):
            index.append(str(intervals[i][0]) + '~' + str(intervals[i][1]))
        # 定义空数组用于保存结果
        pos_list = []
        neg_list = []
        # 循环遍历这些时间点
        for i in range(8):
            start_t = intervals[i][0]
            end_t = intervals[i][1]
            pos_list.append(get_issue_pos_pct(repo_name, start_t, end_t))
            neg_list.append(get_issue_neg_pct(repo_name, start_t, end_t))

        # 创建两条折线，基计得分和消极得分
        trace1 = go.Scatter(
            x=index,
            y=pos_list,
            mode='lines',
            name='积极文本占比'
        )
        trace2 = go.Scatter(
            x=index,
            y=neg_list,
            mode='lines',
            name='消极文本占比'
        )
        # 设置图表布局
        layout = go.Layout(
            title='情绪文本占比波动图',
            xaxis=dict(title='Date'),
            yaxis=dict(title='Score')
        )
        # 绘制图表
        fig = go.Figure(data=[trace1, trace2], layout=layout)
        fig.show()
