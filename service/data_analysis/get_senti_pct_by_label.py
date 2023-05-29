from dao import IssueDao


def get_labels(repo_name, start_time, end_time):
    labels = IssueDao.get_labels(repo_name, start_time, end_time)
    print(labels)