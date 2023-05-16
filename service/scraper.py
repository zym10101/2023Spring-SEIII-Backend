import requests
import json
from abc import ABC, abstractmethod
from model.vo.issue import User, Issue, Label


class IssueSaveStrategy(ABC):
    @abstractmethod
    def save(self, issues_):
        pass


class CsvSaveStrategy(IssueSaveStrategy):
    def __init__(self, path='./GitHubIssue.csv'):
        self.path = path

    """
        authored by zt
    """
    def save(self, issues_):
        with open(self.path, 'w', encoding='utf-8') as f:
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
    def __init__(self, database):
        self.db = database

    def save(self, issues):
        for issue in issues:
            # 1.创建 User\Label ORM对象
            user_ = User(issue['user'])
            labels_ = []
            for label_ in issue['labels']:
                labels_.append(Label(label_))

            # 2.创建 issue ORM对象
            issue_ = Issue(issue)
            issue_.labels = labels_
            print(issue_.labels)

            # 3.将ORM对象添加到db.session中
            self.db.session.merge(user_)
            self.db.session.merge(issue_)

        # 4.commit操作
        self.db.session.commit()


class GitHubIssueScraper:
    def __init__(self, access_token=None, issue_save_strategy=CsvSaveStrategy()):
        self.access_token = access_token
        self.issue_save_strategy = issue_save_strategy

    def get_issue(self, repo_name='apache/superset', state='all', per_page=100):
        # 初始化参数
        repo_name = repo_name.strip('/')
        pageNum = 1
        url = f'https://api.github.com/repos/{repo_name}/issues'
        params = {'state': state, 'page': pageNum, 'per_page': per_page}
        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json'}
        if self.access_token is not None:
            headers['Authorization'] = f'token {self.access_token}'

        # 返回结果列表
        issues_ = []

        # 循环处理每一页响应
        while True:
            print(f'正在爬取第{pageNum}页')
            response = requests.get(url, headers=headers, params=params)
            json_data = json.loads(response.text)

            # 处理每一个issue
            for issue in json_data:
                issues_.append(issue)

            # 检查Link响应头是否有下一页的URL
            link_header = response.headers.get('Link')
            if pageNum > 3:
                break
            if link_header:
                links = link_header.split(', ')
                for link in links:
                    if 'rel="next"' in link:
                        # next_page_url = link[link.index('<') + 1:link.index('>')]
                        params = {'state': state, 'page': pageNum + 1, 'per_page': per_page}
                        break
                pageNum += 1
            else:
                break
        return issues_

    def save_issue(self, issues_):
        self.issue_save_strategy.save(issues_)


if __name__ == '__main__':
    s = GitHubIssueScraper()
    # s = GitHubIssueScraper(issue_save_strategy=JsonSaveStrategy())
    iss = s.get_issue(per_page=2)
    s.save_issue(iss)
