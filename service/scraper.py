import requests
import json
from abc import ABC, abstractmethod
from model.vo.issue import User, Issue, Label, IssueComment


class IssueSaveStrategy(ABC):
    @abstractmethod
    def save(self, issues_):
        pass


class CsvSaveStrategy(IssueSaveStrategy):
    def __init__(self, path='./GitHubIssue.csv', mode='a'):
        self.path = path
        self.mode = mode

    def save(self, issues_):
        """
            authored by zt
        """
        with open(self.path, self.mode, encoding='utf-8') as f:
            if self.mode != 'a':
                f.write(','.join(['title', 'body', 'labels', 'created_at', 'user', 'reactions']))
                f.write('\n')

            for issue in issues_:
                labels = json.dumps(issue['labels'], indent=2)
                if not isinstance(issue['labels'], str):
                    labels = '|'.join(label['name'] for label in issue['labels']),
                else:
                    labels = issue['labels']
                reactions = json.dumps(issue['reactions'], indent=2).replace('\n', '').replace('\r', ' ').replace('\t',
                                                                                                                  ' ').replace(
                    ',', ';')
                user = json.dumps(issue['user'], indent=2).replace('\n', '').replace('\r', ' ').replace('\t',
                                                                                                        ' ').replace(
                    ',', ';')
                if not issue['body']:
                    issue['body'] = ''
                if not issue['title']:
                    issue['title'] = ''
                body = issue['body'].replace('\n', ' ').replace('\t', ' ').replace('\r', ' ').replace(',', ';')
                line = ','.join(
                    [issue['title'].replace(',', ';'), body, '&'.join(labels), issue['created_at'], user, reactions])
                f.write(line)
                f.write('\n')


class JsonSaveStrategy(IssueSaveStrategy):
    def __init__(self, path='./GitHubIssue.txt'):
        self.path = path

    def save(self, issues):
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(issues, f, indent=2)


class MysqlSaveStrategy(IssueSaveStrategy):
    def __init__(self, database, c):
        self.db = database
        # 待存储的类，该类需要实现save方法
        self.c = c

    def save(self, issues):
        for issue in issues:
            self.c.save(self.db.session, issue)
        self.db.session.commit()


class GitHubScraper(ABC):
    def get(self, repo_name='apache/superset', state='all', per_page=100, begin_page=1, end_page=10):
        # 初始化参数
        repo_name = repo_name.strip('/')
        url = self.url_template.format(repo_name)
        page_num = begin_page
        params = {'state': state, 'page': page_num, 'per_page': per_page}
        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json'}
        if self.access_token is not None:
            headers['Authorization'] = f'token {self.access_token}'

        # 返回结果列表
        issues_ = []

        # 循环处理每一页响应
        while True:
            print(f'正在爬取第{page_num}页')
            response = requests.get(url, headers=headers, params=params)
            json_data = json.loads(response.text)

            # 处理每一个issue
            for issue in json_data:
                issues_.append(issue)

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
        self.issue_save_strategy.save(issues_)

    access_token = None
    issue_save_strategy = None
    url_template = None
    c = None


class GitHubIssueScraper(GitHubScraper):
    def __init__(self, access_token=None, issue_save_strategy=CsvSaveStrategy()):
        if access_token is not None or access_token != "":
            self.access_token = access_token
        else:
            self.access_token = None
        self.issue_save_strategy = issue_save_strategy
        self.url_template = 'https://api.github.com/repos/{}/issues'
        self.c = Issue


class GitHubIssueCommentScraper(GitHubScraper):
    def __init__(self, access_token=None, issue_save_strategy=CsvSaveStrategy()):
        self.access_token = access_token
        self.issue_save_strategy = issue_save_strategy
        self.url_template = 'https://api.github.com/repos/{}/issues/comments'
        self.c = IssueComment


if __name__ == '__main__':
    s = GitHubIssueScraper()
    # s = GitHubIssueScraper(issue_save_strategy=JsonSaveStrategy())
    iss = s.get(per_page=2)
    s.save(iss)
