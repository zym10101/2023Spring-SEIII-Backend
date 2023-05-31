from service.data_analysis.get_senti_pct_by_reaction import get_issue_senti_pct_by_reaction, \
    get_comment_senti_pct_by_reaction
from utils.DateUtil import convert_to_iso8601


def plot_issue_reaction_pct(repo, start_time, end_time):
    reactions = ['plus_one', 'minus_one', 'laugh', 'hooray', 'confused', 'heart', 'rocket', 'eyes']
    pos_list = []
    neg_list = []
    neu_list = []
    for reaction in reactions:
        pos = get_issue_senti_pct_by_reaction(
            repo, reaction, convert_to_iso8601(start_time), convert_to_iso8601(end_time), 'pos')
        neg = get_issue_senti_pct_by_reaction(
            repo, reaction, convert_to_iso8601(start_time), convert_to_iso8601(end_time), 'neg')
        neu = 1 - pos - neg
        pos_list.append(pos)
        neg_list.append(neg)
        neu_list.append(neu)

    return {"title": "issue的reaction情绪文本占比图",
            "data": {
                "pos": pos_list,
                "neg": neg_list,
                "neu": neu_list,
                "xAxis": reactions
            },

            }
    # return [reactions, pos_list, neu_list, neg_list, 'reactions']
    # return [reactions, pos_list, neu_list, neg_list, 'issue的reaction情绪文本占比图', 'reactions']


def plot_comment_reaction_pct(repo, start_time, end_time):
    reactions = ['plus_one', 'minus_one', 'laugh', 'hooray', 'confused', 'heart', 'rocket', 'eyes']
    pos_list = []
    neg_list = []
    neu_list = []
    for reaction in reactions:
        pos = get_comment_senti_pct_by_reaction(
            repo, reaction, convert_to_iso8601(start_time), convert_to_iso8601(end_time), 'pos')
        neg = get_comment_senti_pct_by_reaction(
            repo, reaction, convert_to_iso8601(start_time), convert_to_iso8601(end_time), 'neg')
        neu = 1 - pos - neg
        pos_list.append(pos)
        neg_list.append(neg)
        neu_list.append(neu)

    return {"title": "comment的reaction情绪文本占比图",
            "data": {
                "pos": pos_list,
                "neg": neg_list,
                "neu": neu_list,
                "xAxis": reactions
            },

            }
    # return [reactions, pos_list, neu_list, neg_list, 'reactions']
    # return [reactions, pos_list, neu_list, neg_list, 'comment的reaction情绪文本占比图', 'reactions']
