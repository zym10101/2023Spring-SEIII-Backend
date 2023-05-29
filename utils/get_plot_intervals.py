import pandas as pd

# 生成绘图的时间间隔
#
# start_time (str或datetime):间隔的开始时间。
# end_time (str或datetime):间隔的结束时间。
# freq (str或DateOffset，可选):间隔的频率。如果指定，忽略periods参数。
# periods (int，可选):要生成的间隔数。默认值是8。
#
# 返回表示时间间隔的datetime对象列表。
def get_plot_intervals(start_time, end_time, freq=None, periods=8):
    if freq is not None:
        intervals = pd.date_range(start=start_time, end=end_time, freq=freq).tolist()
    else:
        intervals = pd.date_range(start=start_time, end=end_time, periods=periods+1).tolist()[1:]
    dates = pd.DatetimeIndex(intervals).date.tolist()
    return [d.strftime('%Y-%m-%d') for d in dates]

if __name__ == '__main__':
    print(get_plot_intervals('2022-01-01', '2022-01-09'))