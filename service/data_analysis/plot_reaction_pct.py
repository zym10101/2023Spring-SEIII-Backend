from service.data_analysis.get_senti_pct_by_reaction import get_issue_senti_pct_by_reaction, \
    get_comment_senti_pct_by_reaction
from utils.DateUtil import convert_to_iso8601
from utils.plot_pct_change import plot_pct_change


def plot_issue_reaction_pct(repo, start_time, end_time):
    reactions = ['plus_one', 'minus_one', 'laugh', 'hooray', 'confused', 'heart', 'rocket', 'eyes']
    pos_list = []
    neg_list = []
    for reaction in reactions:
        pos_list.append(get_issue_senti_pct_by_reaction(
            repo, reaction, convert_to_iso8601(start_time), convert_to_iso8601(end_time), 'pos'))
        neg_list.append(get_issue_senti_pct_by_reaction(
            repo, reaction, convert_to_iso8601(start_time), convert_to_iso8601(end_time), 'neg'))

    return plot_pct_change(reactions, pos_list, neg_list, 'issue的reaction情绪文本占比图', 'reactions')


def plot_comment_reaction_pct(repo, start_time, end_time):
    reactions = ['plus_one', 'minus_one', 'laugh', 'hooray', 'confused', 'heart', 'rocket', 'eyes']
    pos_list = []
    neg_list = []
    for reaction in reactions:
        pos_list.append(get_comment_senti_pct_by_reaction(
            repo, reaction, convert_to_iso8601(start_time), convert_to_iso8601(end_time), 'pos'))
        neg_list.append(get_comment_senti_pct_by_reaction(
            repo, reaction, convert_to_iso8601(start_time), convert_to_iso8601(end_time), 'neg'))

    return plot_pct_change(reactions, pos_list, neg_list, 'comment的reaction情绪文本占比图', 'reactions')
