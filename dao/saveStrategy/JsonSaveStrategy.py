import json
from dao.saveStrategy.AbstractSaveStrategy import AbstractSaveStrategy


class JsonSaveStrategy(IssueSaveStrategy):
    def __init__(self, path='output/GitHubIssue.txt'):
        self.f = open(path, 'a', encoding='utf-8')

    def save(self, issues):
        json.dump(issues, self.f, indent=2)

    def __del__(self):
        self.f.close()
