from dao.LabelDao import get_labels_8
from service.data_analysis.get_senti_pct_by_label import get_issue_senti_pct_by_label, get_comment_senti_pct_by_label, \
    get_all_senti_pct_by_label
from utils.DateUtil import convert_to_iso8601


# labels为label name列表，默认为选定范围内全部，也可以用户指定
def plot_issue_pct_change_by_label(repo, start_time, end_time, labels=None):
    if labels is None:
        labels = get_labels_8(repo, start_time, end_time)
    pos_list = []
    neg_list = []
    neu_list = []
    for label in labels:
        pos = get_issue_senti_pct_by_label(
            repo, label, convert_to_iso8601(start_time), convert_to_iso8601(end_time), 'pos')
        neg = get_issue_senti_pct_by_label(
            repo, label, convert_to_iso8601(start_time), convert_to_iso8601(end_time), 'neg')
        neu = 1 - pos - neg
        pos_list.append(pos)
        neg_list.append(neg)
        neu_list.append(neu)

    return {"title": "issue的labels情绪文本占比图",
            "data": {
                "pos": pos_list,
                "neg": neg_list,
                "neu": neu_list,
                "xAxis": labels
            },

            }
    # return [labels, pos_list, neu_list, neg_list, 'Labels']
    # return [labels, pos_list, neu_list, neg_list, 'issue的labels情绪文本占比图', 'Labels']


def plot_comment_pct_change_by_label(repo, start_time, end_time, labels=None):
    if labels is None:
        labels = get_labels_8(repo, start_time, end_time)
    pos_list = []
    neg_list = []
    neu_list = []
    for label in labels:
        pos = get_comment_senti_pct_by_label(
            repo, label, convert_to_iso8601(start_time), convert_to_iso8601(end_time), 'pos')
        neg = get_comment_senti_pct_by_label(
            repo, label, convert_to_iso8601(start_time), convert_to_iso8601(end_time), 'neg')
        neu = 1 - pos - neg
        pos_list.append(pos)
        neg_list.append(neg)
        neu_list.append(neu)

    return {"title": "comment的labels情绪文本占比图",
            "data": {
                "pos": pos_list,
                "neg": neg_list,
                "neu": neu_list,
                "xAxis": labels
            },

            }
    # return [labels, pos_list, neu_list, neg_list, 'Labels']
    # return [labels, pos_list, neu_list, neg_list, 'comment的labels情绪文本占比图', 'Labels']


def plot_all_pct_change_by_label(repo, start_time, end_time, weighting, labels=None):
    if labels is None:
        labels = get_labels_8(repo, start_time, end_time)
    pos_list = []
    neg_list = []
    neu_list = []
    for label in labels:
        pos = get_all_senti_pct_by_label(
            repo, label, convert_to_iso8601(start_time), convert_to_iso8601(end_time), 'pos', weighting)
        neg = get_all_senti_pct_by_label(
            repo, label, convert_to_iso8601(start_time), convert_to_iso8601(end_time), 'neg', weighting)
        neu = 1 - pos - neg
        pos_list.append(pos)
        neg_list.append(neg)
        neu_list.append(neu)

    return {"title": "issue+comment的labels情绪文本占比图",
            "data": {
                "pos": pos_list,
                "neg": neg_list,
                "neu": neu_list,
                "xAxis": labels
            },

            }
    # return [labels, pos_list, neu_list, neg_list, 'Labels']
