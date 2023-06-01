def sort_data(data):
    # 获取数据
    pos_list = data["data"]["pos"]
    neg_list = data["data"]["neg"]
    neu_list = data["data"]["neu"]
    labels = data["data"]["xAxis"]

    # 根据pos_list进行排序，并将其他列表按照相同顺序重新排序
    sorted_data = sorted(zip(pos_list, neg_list, neu_list, labels), reverse=True)

    # 解压缩排序后的数据
    sorted_pos, sorted_neg, sorted_neu, sorted_labels = zip(*sorted_data)

    # 更新原始数据字典
    data["data"]["pos"] = sorted_pos
    data["data"]["neg"] = sorted_neg
    data["data"]["neu"] = sorted_neu
    data["data"]["xAxis"] = sorted_labels

    return data
