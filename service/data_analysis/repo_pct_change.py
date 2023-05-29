import plotly.graph_objs as go
import plotly
from service.data_analysis.get_issue_senti_pct import get_issue_pos_pct, get_issue_neg_pct
from utils.DateUtil import convert_to_iso8601
import json


# intervals参数详见utils.get_plot_intervals
# 关于返回图像：
# 首先使用 `json.dumps()` 方法将 `go.Figure` 对象转换为 JSON 格式的字符串
# 并使用 Flask 的 `render_template` 方法将这个字符串作为参数传递给前端模板。
# 在前端模板中，可以使用 JavaScript 或其他前端框架来解析 JSON 并渲染图表。
def repo_issue_pct_change(repo_name, start_time, end_time, intervals):
    if get_issue_pos_pct(repo_name, start_time, end_time) != f"该时间段内，{repo_name} issue为空！":
        index = []
        for i in range(8):
            index.append(str(intervals[i]) + '~' + str(intervals[i + 1]))
        # 定义空数组用于保存结果
        pos_list = []
        neg_list = []
        # 循环遍历这些时间点
        for i in range(8):
            start_t = intervals[i]
            end_t = intervals[i + 1]
            pos_list.append(get_issue_pos_pct(repo_name, convert_to_iso8601(start_t), convert_to_iso8601(end_t)))
            neg_list.append(get_issue_neg_pct(repo_name, convert_to_iso8601(start_t), convert_to_iso8601(end_t)))

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
            title='项目情绪文本占比波动图',
            xaxis=dict(title='Date'),
            yaxis=dict(title='Score')
        )
        # 绘制图表
        fig = go.Figure(data=[trace1, trace2], layout=layout)
        # fig.show()
        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)