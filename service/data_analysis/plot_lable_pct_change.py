from dao.LabelDao import get_labels_8
from service.data_analysis.get_senti_pct_by_label import get_issue_senti_pct_by_label, get_comment_senti_pct_by_label
from utils.DateUtil import convert_to_iso8601
from utils.plot_pct_change import plot_pct_change


# labels为label name列表，默认为选定范围内全部，也可以用户指定
def plot_issue_pct_change_by_label(repo, start_time, end_time, labels=None):
    if labels is None:
        labels = get_labels_8(repo, start_time, end_time)
    pos_list = []
    neg_list = []
    for label in labels:
        pos_list.append(get_issue_senti_pct_by_label(
            repo, label, convert_to_iso8601(start_time), convert_to_iso8601(end_time), 'pos'))
        neg_list.append(get_issue_senti_pct_by_label(
            repo, label, convert_to_iso8601(start_time), convert_to_iso8601(end_time), 'neg'))

    return plot_pct_change(labels, pos_list, neg_list, 'issue的labels情绪文本占比图', 'Labels')


def plot_comment_pct_change_by_label(repo, start_time, end_time, labels=None):
    if labels is None:
        labels = get_labels_8(repo, start_time, end_time)
    pos_list = []
    neg_list = []
    for label in labels:
        pos_list.append(get_comment_senti_pct_by_label(
            repo, label, convert_to_iso8601(start_time), convert_to_iso8601(end_time), 'pos'))
        neg_list.append(get_comment_senti_pct_by_label(
            repo, label, convert_to_iso8601(start_time), convert_to_iso8601(end_time), 'neg'))

    return plot_pct_change(labels, pos_list, neg_list, 'comment的labels情绪文本占比图', 'Labels')
