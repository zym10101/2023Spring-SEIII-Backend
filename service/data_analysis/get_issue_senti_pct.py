from dao.IssueDao import get_by_create_time_all
import pandas as pd
import plotly.graph_objs as go


def get_pct(repo_name, start_time, end_time, polarity):
    issues = get_by_create_time_all(repo_name, start_time, end_time)

    if len(issues) == 0:
        return f"该时间段内，{repo_name} issue为空！"

    pos_count = 0
    neg_count = 0
    neutral_count = 0

    for issue in issues:
        result = int(issue.pos_body) + int(issue.neg_body)
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


def get_issue_pos_pct(repo_name, start_time, end_time):
    pct = get_pct(repo_name, start_time, end_time, "pos")
    if pct.startswith("该时间段内"):
        return f"该时间段内，{repo_name} issue为空！"
    else:
        return pct


def get_issue_neg_pct(repo_name, start_time, end_time):
    pct = get_pct(repo_name, start_time, end_time, "neg")
    if pct.startswith("该时间段内"):
        return f"该时间段内，{repo_name} issue为空！"
    else:
        return pct


# interval格式: “xxD”，如”60D“表示60天
def plot_pct_over_time(repo_name, start_time, end_time, interval):
    if get_issue_pos_pct(repo_name, start_time, end_time) != f"该时间段内，{repo_name} issue为空！":
        # 准备数据，将总体之间划分为指定间隔
        index = pd.date_range(start_time, end_time, freq=interval)
        # 定义空数组用于保存结果
        pos_list = []
        neg_list = []
        # 循环遍历这些时间点
        for i in range(len(index)):
            start_t = index[i]
            end_t = index[i+1]
            pos_list.append(get_issue_pos_pct(repo_name, start_t, end_t))
            neg_list.append(get_issue_neg_pct(repo_name, start_t, end_t))
        # 将数据转化为dataframe对象
        pos_pct = pd.Series(pos_list)
        neg_pct = pd.Series(neg_list)

        # 创建两条折线，基计得分和消极得分
        trace1 = go.Scatter(
            x=index,
            y=pos_pct,
            mode='lines',
            name='积极文本占比'
        )
        trace2 = go.Scatter(
            x=index,
            y=neg_pct,
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
