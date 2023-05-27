"""
params = {
            'state': state,
            'page': page_num,
            'per_page': per_page,
            'since': '2023-01-01T00:00:00Z',  # 设置开始时间（ISO 8601 格式）
            'until': '2023-05-31T23:59:59Z'  # 设置结束时间（ISO 8601 格式）
        }
"""


class Params:
    def __init__(self):
        self.params = {
            'state': 'all',
            'page': 5,
            'per_page': 100
        }

    def add_param(self, key, value):
        self.params[key] = value

    def to_dict(self):
        return self.params
