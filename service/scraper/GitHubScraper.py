import requests
import json
import re
from service.scraper.Params import Params
from dao import IssueDao
from dao import CommentDao

# 多线程相关
import concurrent.futures
import asyncio
import aiohttp


class GitHubScraper:
    def __init__(self, access_token=None):
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        if access_token is not None:
            self.headers['Authorization'] = f'token {access_token}'
        self.issues_url_template = 'https://api.github.com/repos/{}/issues'
        self.comments_url_template = 'https://api.github.com/repos/{}/issues/comments'
        self.thread_pool = concurrent.futures.ThreadPoolExecutor()

    def _get_total_pages(self, url, params):
        """
        获取可响应的总页数
        :param url: 本次任务中其中一次请求的url
        :param params: 参数字典
        :return: 本次任务共需要请求的总页数
        """
        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code == 200:
            link_header = response.headers.get('Link')
            if link_header:
                lines = link_header.split(',')
                for line in lines:
                    if 'last' in line:
                        match = re.search(r'[\?&]page=(\d+)', line)
                        if match:
                            total_pages = int(match.group(1))
                            return total_pages
            else:
                # 如果链接标头不存在，则只有一页结果
                return 1
        else:
            print(f"Request failed with status code: {response.status_code}")
        return 0

    def get_earliest_date(self, repo_name, params):
        """
        获取仓库最早issue实践
        :param repo_name: 本次任务中其中一次请求的url
        :param params: 参数字典
        :return: 本次任务共需要请求的总页数
        """
        url = self.issues_url_template.format(repo_name)
        last_page_num = self._get_total_pages(url, params)
        params["page"] = last_page_num
        issue_json = self.crawling(url, params)[-1]
        return issue_json['created_at']

    # 这是不使用线程池的方法
    def crawling(self, url, params):
        response = requests.get(url, headers=self.headers, params=params)
        return json.loads(response.text)

    def crawling_issues_and_comments(self, repo_name, params, max_page=10):
        issues_url = self.issues_url_template.format(repo_name)
        total_page_num = self._get_total_pages(issues_url, params)
        result = []
        print('共有{}页数据'.format(total_page_num))
        for page_no in range(1, min(max_page + 1, total_page_num + 1)):
            print('正在爬取第{}页'.format(page_no))
            params['page'] = page_no
            issues_json = self.crawling(issues_url, params)
            for issue_json in issues_json:
                result.append(issue_json)
                comments_url = issue_json['comments_url']
                comments_json = self.crawling(comments_url, None)  # 后续再考虑评论数量过多的情况
                issue_json['comments_json'] = comments_json
                IssueDao.save_single(issue_json)
        return result

    def crawling_only_issues(self, repo_name, params, max_page=10):
        issues_url = self.issues_url_template.format(repo_name)
        total_page_num = self._get_total_pages(issues_url, params)
        print('共有{}页Issue数据'.format(total_page_num))
        for page_no in range(1, min(max_page + 1, total_page_num + 1)):
            print('正在爬取第{}页'.format(page_no))
            params['page'] = page_no
            issues_json_list = self.crawling(issues_url, params)
            IssueDao.save_list(issues_json_list)
        return "success"

    def crawling_only_comments(self, repo_name, params, max_page=10):
        comments_url = self.comments_url_template.format(repo_name)
        total_page_num = self._get_total_pages(comments_url, params)
        print('共有{}页Comment数据'.format(total_page_num))
        for page_no in range(1, min(max_page + 1, total_page_num + 1)):
            print('正在爬取第{}页'.format(page_no))
            params['page'] = page_no
            comments_json_list = self.crawling(comments_url, params)
            CommentDao.save_list(comments_json_list)
        return "success"

    @staticmethod
    def create_association(repo_name):
        print('正在对{}仓库Issue与Comment建立连接'.format(repo_name))
        IssueDao.create_association(repo_name)

    # async def crawling(self, url, params):
    #     async with aiohttp.ClientSession() as session:
    #         async with session.get(url, headers=self.headers, params=params) as response:
    #             return await response.json()
    #
    # def fetch_comments(self, comments_url):
    #     return self.crawling(comments_url, None)
    #
    # async def crawling_issues_and_comments(self, repo_name, params):
    #     issues_url = self.issues_url_template.format(repo_name)
    #     total_page_num = self._get_total_pages(issues_url, params)
    #     result = []
    #     print('共有{}页数据'.format(total_page_num))
    #     async with aiohttp.ClientSession() as session:
    #         tasks = []
    #         for page_no in range(1, min(6, total_page_num + 1)):  # Todo: 暂定最多5页
    #             params['page'] = page_no
    #             task = asyncio.create_task(self.crawling(issues_url, params))
    #             tasks.append(task)
    #         counter = 0
    #         for task in asyncio.as_completed(tasks):
    #             counter += 1
    #             print('正在爬取第{}页'.format(counter))
    #             issues_json = await task
    #             for issue_json in issues_json:
    #                 result.append(issue_json)
    #                 comments_url = issue_json['comments_url']
    #                 comments_json = await self.crawling(comments_url, None)
    #                 issue_json['comments_json'] = comments_json
    #                 IssueDao.save_single(issue_json)
    #     return result

    # # 这是虽然使用线程池但没有添加异步的方法
    # def crawling(self, url, params):
    #     response = requests.get(url, headers=self.headers, params=params)
    #     return json.loads(response.text)
    #
    # def fetch_comments(self, comments_url):
    #     return self.crawling(comments_url, None)
    #
    # def crawling_issues_and_comments(self, repo_name, params):
    #     issues_url = self.issues_url_template.format(repo_name)
    #     total_page_num = self._get_total_pages(issues_url, params)
    #     result = []
    #     print('共有{}页数据'.format(total_page_num))
    #     futures = []
    #     for page_no in range(1, min(6, total_page_num + 1)):
    #         # print('正在爬取第{}页'.format(page_no))
    #         params['page'] = page_no
    #         future = self.thread_pool.submit(self.crawling, issues_url, params)
    #         futures.append(future)
    #     counter = 0
    #     for future in concurrent.futures.as_completed(futures):
    #         counter += 1
    #         print('正在爬取第{}页'.format(counter))
    #         issues_json = future.result()
    #         for issue_json in issues_json:
    #             result.append(issue_json)
    #             comments_url = issue_json['comments_url']
    #             comments_future = self.thread_pool.submit(self.fetch_comments, comments_url)
    #             comments_json = comments_future.result()
    #             issue_json['comments_json'] = comments_json
    #             IssueDao.save_single(issue_json)
    #     return result


if __name__ == '__main__':
    from app_template import app

    with app.app_context():
        s = GitHubScraper()
        p = Params()
        p.add_param('since', '2023-03-15T00:00:00Z')
        p.add_param('until', '2023-03-17T23:59:59Z')
        p.add_param('per_page', '10')
        p.add_param('page', '2')
        print(s.crawling_issues_and_comments('apache/tomcat', p.to_dict()))
