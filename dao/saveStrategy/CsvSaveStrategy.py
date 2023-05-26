import json
from dao.saveStrategy.AbstractSaveStrategy import AbstractSaveStrategy


class CsvSaveStrategy(AbstractSaveStrategy):
    def __init__(self, path='output/GitHubIssue.csv'):
        self.f = open(path, 'a', encoding='utf-8')
        self.f.write(','.join(['title', 'body', 'labels', 'created_at', 'user', 'reactions']))
        self.f.write('\n')

    def save(self, issues_):
        """
            authored by zt
        """
        for issue in issues_:
            labels = json.dumps(issue['labels'], indent=2)
            if not isinstance(issue['labels'], str):
                labels = '|'.join(label['name'] for label in issue['labels']),
            else:
                labels = issue['labels']
            reactions = json.dumps(issue['reactions'], indent=2).replace('\n', '') \
                .replace('\r', ' ').replace('\t', ' ').replace(',', ';')
            user = json.dumps(issue['user'], indent=2).replace('\n', '') \
                .replace('\r', ' ').replace('\t', ' ').replace(',', ';')
            if not issue['body']:
                issue['body'] = ''
            if not issue['title']:
                issue['title'] = ''
            body = issue['body'].replace('\n', ' ').replace('\t', ' ').replace('\r', ' ').replace(',', ';')
            line = ','.join(
                [issue['title'].replace(',', ';'), body, '&'.join(labels), issue['created_at'], user, reactions])
            self.f.write(line)
            self.f.write('\n')

    def __del__(self):
        self.f.close()
