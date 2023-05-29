import pandas as pd
from datetime import datetime


# 生成绘图的时间间隔
#
# start_time (str或datetime):间隔的开始时间。
# end_time (str或datetime):间隔的结束时间。
# freq (str或DateOffset，可选):间隔的频率。如果指定，忽略periods参数。
# periods (int，可选):要生成的间隔数。默认值是8。
#
# 返回表示时间间隔的datetime对象列表。
def get_plot_intervals(start_time, end_time, freq=None, periods=8):
    date1 = datetime.strptime(start_time, '%Y-%m-%d')
    date2 = datetime.strptime(end_time, '%Y-%m-%d')
    delta = date2 - date1
    delta_days = delta.days
    result_str = '{}D'.format(delta_days)
    if int(result_str[:-1]) < 8:
        freq = '1D'
    if freq is not None:
        intervals = pd.date_range(start=start_time, end=end_time, freq=freq).tolist()
    else:
        intervals = pd.date_range(start=start_time, end=end_time, periods=periods+1).tolist()
    dates = pd.DatetimeIndex(intervals).date.tolist()
    return [d.strftime('%Y-%m-%d') for d in dates]


if __name__ == '__main__':
    print(get_plot_intervals('2022-01-01', '2022-01-09'))