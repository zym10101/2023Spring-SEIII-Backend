from sqlalchemy import or_

from dao.IssueDao import get_by_create_time_all
from model.Issue import Issue
from model.Label import Label


def get_labels(repo_name, begin_time, end_time):
    labels_list = [issue.labels for issue in Issue.query \
        .filter(Issue.repository_url.endswith(repo_name)) \
        .filter(Issue.created_at.between(begin_time, end_time)) \
        .all()]
    labels = list(set(element for sublist in labels_list for element in sublist))
    label_id = [label.id for label in labels]
    labels = Label.query.filter(or_(*[Label.id == id for id in label_id])).with_entities(Label.name).all()
    label_names = list(set([label.name for label in labels]))
    return label_names


def get_labels_8(repo_name, begin_time, end_time):
    issues = get_by_create_time_all(repo_name, begin_time, end_time)
    label_count = {}
    for issue in issues:
        for label in issue.labels:
            if label.id in label_count:
                label_count[label.id] += 1
            else:
                label_count[label.id] = 1

    if len(label_count) > 8:
        sorted_labels = sorted(label_count.items(), key=lambda x: x[1], reverse=True)[:8]
    else:
        sorted_labels = sorted(label_count.items(), key=lambda x: x[1], reverse=True)
    top_labels = [Label.query.get(label_id) for label_id, count in sorted_labels]
    return list(set([label.name for label in top_labels]))
