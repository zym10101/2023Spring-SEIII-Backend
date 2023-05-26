from abc import ABC, abstractmethod
import requests


class GitHubScraper(ABC):
    def __init__(self):
        self.access_token = None
        self.url_template = None
        self.c = None

    def _format_headers(self):
        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json'}
        if self.access_token is not None:
            headers['Authorization'] = f'token {self.access_token}'
        return headers

    def get_and_save(self, repo_name, state='all', per_page=100, begin_page=1, end_page=10):
        # 初始化参数
        repo_name = repo_name.strip('/')
        url = self.url_template.format(repo_name)
        page_num = begin_page
        params = {'state': state, 'page': page_num, 'per_page': per_page}
        headers = self._format_headers()

        # 返回结果列表
        issues_ = []
        issue_per_page = []
        # 循环处理每一页响应
        while True:
            print(f'正在爬取第{page_num}页')
            response = requests.get(url, headers=headers, params=params)
            json_data = json.loads(response.text)

            # 处理每一个issue
            for issue in json_data:
                issues_.append(issue)
                issue_per_page.append(issue)
                self.save(issue_per_page)
                issue_per_page = []

            # 检查Link响应头是否有下一页的URL
            link_header = response.headers.get('Link')
            if page_num >= end_page:
                break
            if link_header:
                links = link_header.split(', ')
                for link in links:
                    if 'rel="next"' in link:
                        # next_page_url = link[link.index('<') + 1:link.index('>')]
                        params = {'state': state, 'page': page_num + 1, 'per_page': per_page}
                        break
                page_num += 1
            else:
                break
        return issues_

    def save(self, issues_):
        pass
        # self.issue_save_strategy.save(issues_)
