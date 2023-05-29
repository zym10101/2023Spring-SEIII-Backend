import plotly.graph_objs as go
import plotly
import json


def plot_pct_change(index, pos_list, neg_list):
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