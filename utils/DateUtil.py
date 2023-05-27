from datetime import datetime


def convert_to_iso8601(date_string):
    """
    日期格式转换器
    :param date_string: 日期字符串，如'2023-05-27'
    :return: ISO 8601格式日期字符串
    """
    input_format = '%Y-%m-%d'
    date_obj = datetime.strptime(date_string, input_format)
    iso8601_date = date_obj.strftime('%Y-%m-%dT%H:%M:%SZ')
    return iso8601_date
