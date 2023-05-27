import requests
import json
import re
from service.scraper.Params import Params
from dao import IssueDao

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
                        match = re.search(r'page=(\d+)', line)
                        if match:
                            total_pages = int(match.group(1))
                            return total_pages
            else:
                # 如果链接标头不存在，则只有一页结果
                return 1
        else:
            print(f"Request failed with status code: {response.status_code}")
        return 0

    async def crawling(self, url, params):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers, params=params) as response:
                return await response.json()

    def fetch_comments(self, comments_url):
        return self.crawling(comments_url, None)

    async def crawling_issues_and_comments(self, repo_name, params):
        issues_url = self.issues_url_template.format(repo_name)
        total_page_num = self._get_total_pages(issues_url, params)
        result = []
        print('共有{}页数据'.format(total_page_num))
        async with aiohttp.ClientSession() as session:
            tasks = []
            for page_no in range(1, total_page_num + 1):
                print('正在爬取第{}页'.format(page_no))
                params['page'] = page_no
                task = asyncio.create_task(self.crawling(issues_url, params))
                tasks.append(task)
            for task in asyncio.as_completed(tasks):
                issues_json = await task
                for issue_json in issues_json:
                    result.append(issue_json)
                    comments_url = issue_json['comments_url']
                    comments_json = await self.crawling(comments_url, None)
                    issue_json['comments_json'] = comments_json
                    IssueDao.save_single(issue_json)
        return result

    # 这是虽然使用线程池但没有添加异步的方法
    # def crawling(self, url, params):
    #     response = requests.get(url, headers=self.headers, params=params)
    #     return json.loads(response.text)
    # def crawling_issues_and_comments(self, repo_name, params):
    #     issues_url = self.issues_url_template.format(repo_name)
    #     total_page_num = self._get_total_pages(issues_url, params)
    #     result = []
    #     print('共有{}页数据'.format(total_page_num))
    #     futures = []
    #     for page_no in range(1, total_page_num + 1):
    #         print('正在爬取第{}页'.format(page_no))
    #         params['page'] = page_no
    #         future = self.thread_pool.submit(self.crawling, issues_url, params)
    #         futures.append(future)
    #     for future in concurrent.futures.as_completed(futures):
    #         issues_json = future.result()
    #         for issue_json in issues_json:
    #             result.append(issue_json)
    #             comments_url = issue_json['comments_url']
    #             comments_future = self.thread_pool.submit(self.fetch_comments, comments_url)
    #             comments_json = comments_future.result()
    #             issue_json['comments_json'] = comments_json
    #             IssueDao.save_single(issue_json)
    #     return result

    # 这是不使用线程池的方法
    # def crawling_issues_and_comments(self, repo_name, params):
    #     issues_url = self.issues_url_template.format(repo_name)
    #     total_page_num = self._get_total_pages(issues_url, params)
    #     result = []
    #     print('共有{}页数据'.format(total_page_num))
    #     for page_no in range(1, total_page_num + 1):
    #         print('正在爬取第{}页'.format(page_no))
    #         params['page'] = page_no
    #         issues_json = self.crawling(issues_url, params)
    #         for issue_json in issues_json:
    #             result.append(issue_json)
    #             comments_url = issue_json['comments_url']
    #             comments_json = self.crawling(comments_url, None)  # 后续再考虑评论数量过多的情况
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
