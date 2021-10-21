def load_data_set():
    data_set = [['I1', 'I2', 'I5'], ['I2', 'I4'], ['I2', 'I3'], ['I1', 'I2', 'I4'], ['I1', 'I3'],
                ['I2', 'I3'], ['I1', 'I3'], ['I1', 'I2', 'I3', 'I5'], ['I1', 'I2', 'I3']]
    return data_set


def create_C1(data_set):
    C1 = []
    for t in data_set:
        for item in t:
            item_set = frozenset([item])
            if item_set not in C1:
                C1.append(item_set)
    return C1


def is_apriori(Ck_item, Lksub1):
    for item in Ck_item:
        sub_Ck = Ck_item - frozenset([item])
        if sub_Ck not in Lksub1:
            return False
    return True


def create_Ck(Lksub1, k):
    Ck = []
    len_Lksub1 = len(Lksub1)
    for i in range(len_Lksub1):
        for j in range(i + 1, len_Lksub1):
            l1 = list(Lksub1[i])  # 原本是frozenset类型
            l2 = list(Lksub1[j])
            l1.sort()
            l2.sort()
            if l1[0:k - 2] == l2[0:k - 2]:
                Ck_item = Lksub1[i] | Lksub1[j]
                if is_apriori(Ck_item, Lksub1):  # 如果Ck_item是频繁项集，那么它的所有子集都是频繁项集
                    Ck.append(Ck_item)
    return Ck  # 候选k项集


def generate_Lk_by_Ck(data_set, Ck, min_sup, support_data):
    Lk = []
    item_count = {}  # 字典  用来计算项的支持度
    for t in data_set:  # 遍历所有dataset
        for item in Ck:  # 计算所有候选项集中每个项的支持度
            if item.issubset(t):
                if item not in item_count:
                    item_count[item] = 1
                else:
                    item_count[item] += 1
    t_num = float(len(data_set))
    for item in item_count:
        if (item_count[item] / t_num) >= min_sup:
            Lk.append(item)
            support_data[item] = item_count[item] / t_num  # support_data字典类型 记录支持度
    return Lk


def generate_L(data_set, min_sup, k):
    support_data = {}
    C1 = create_C1(data_set)

    Li = generate_Lk_by_Ck(data_set, C1, min_sup, support_data)  # L1频繁项集

    L = []  # 保存所有频繁项集
    L.append(Li)
    for i in range(2, k + 1):
        Ci = create_Ck(Li, i)
        Li = generate_Lk_by_Ck(data_set, Ci, min_sup, support_data)
        L.append(Li)
    return L, support_data


def generate_big_rules(L, support_data, min_conf):
    big_rule_list = []
    sub_set_list = []
    for i in range(0, len(L)):
        for freq_set in L[i]:  # freq-set：频繁项        L[i]：频繁i项集
            for sub_set in sub_set_list:
                if sub_set.issubset(freq_set):
                    conf = support_data[freq_set] / support_data[freq_set - sub_set]
                    big_rule = (freq_set - sub_set, sub_set, conf)
                    if conf >= min_conf and big_rule not in big_rule_list:
                        big_rule_list.append(big_rule)
            sub_set_list.append(freq_set)
    return big_rule_list


if __name__ == "__main__":
    min_sup = 2 / 9
    min_conf = 5 / 9
    data_set = load_data_set()
    L, support_data = generate_L(data_set, min_sup, k = 3)

    big_rules_list = generate_big_rules(L, support_data, min_conf)
    for Lk in L:
        print("\nfrequent " + str(len(Lk[0])) + "-itemsets\t\tsupport")
        for freq_set in Lk:
            print(set(freq_set), support_data[freq_set])
    print()
    print("Big Rules")
    for item in big_rules_list:
        print(set(item[0]), "=>", set(item[1]), "conf: ", item[2])
