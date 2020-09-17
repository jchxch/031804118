import math
import os
from jieba.analyse import *
import sys


def openfile(argv1, argv2):
    s1 = []
    s2 = []
    try:
        s1 = open(argv1, 'r', encoding='utf-8').read()
        s2 = open(argv2, 'r', encoding='utf-8').read()
    except IOError:
        print("文件打开失败")
    return s1, s2


def dictionaries_cut(s1, s2):
    s1_cut = []
    s2_cut = []
    s1_rate = 0
    s2_rate = 0
    for keyword, weight in extract_tags(s1, withWeight=True):
        if s1_rate > 0.75:
            break
        else:
            s1_rate = s1_rate + weight
            s1_cut.append(keyword)
    for keyword, weight in extract_tags(s2, withWeight=True):
        if s2_rate > 0.75:
            break
        else:
            s2_rate = s2_rate + weight
            s2_cut.append(keyword)
    return s1_cut, s2_cut


def dictionaries_dict(s1_cut, s2_cut):
    word_set = set(s1_cut).union(set(s2_cut))
    word_dict = dict()
    i = 0
    for word in word_set:
        word_dict[word] = i
        i += 1
    return word_dict


def word_cut_count(s1_cut, s2_cut, word_dict):
    s1_cut_code = [0] * len(word_dict)

    for word in s1_cut:
        s1_cut_code[word_dict[word]] += 1

    s2_cut_code = [0] * len(word_dict)
    for word in s2_cut:
        s2_cut_code[word_dict[word]] += 1
    return s1_cut_code, s2_cut_code


def cos(s1_cut_code, s2_cut_code):
    sum_code = 0
    sq1 = 0
    sq2 = 0
    for i in range(len(s1_cut_code)):
        sum_code += s1_cut_code[i] * s2_cut_code[i]
        sq1 += pow(s1_cut_code[i], 2)
        sq2 += pow(s2_cut_code[i], 2)

    try:
        result = round(float(sum_code) / (math.sqrt(sq1) * math.sqrt(sq2)), 3)
    except ZeroDivisionError:
        result = 0.0
    print("\n余弦相似度为：%.2f" % result)
    return round(result, 2)


def answer(argv1, argv2, argv3, an):
    file = open(argv3, 'a+', encoding='utf-8')
    file1 = os.path.basename(argv1)
    file2 = os.path.basename(argv2)
    file.write(file1 + "与" + file2 + "余弦相似度为:" + an + "\n")
    file.close()


t1, t2 = openfile(sys.argv[1], sys.argv[2])
t1_cut, t2_cut = dictionaries_cut(t1, t2)
text_dict = dictionaries_dict(t1_cut, t2_cut)
t1_cut_code, t2_cut_code = word_cut_count(t1_cut, t2_cut, text_dict)
an1 = cos(t1_cut_code, t2_cut_code)
answer(sys.argv[1], sys.argv[2], sys.argv[3], str(an1))

# 测试集
# def test(a,b):
#     t1, t2 = openfile(a, b)
#     t1_cut, t2_cut = dictionaries_cut(t1, t2)
#     text_dict = dictionaries_dict(t1_cut, t2_cut)
#     t1_cut_code, t2_cut_code = word_cut_count(t1_cut, t2_cut, text_dict)
#     an1 = cos(t1_cut_code, t2_cut_code)
#     return an1
# test('./sim_0.8/orig.txt','./sim_0.8/orig_0.8_add.txt')
# test('./sim_0.8/orig.txt','./sim_0.8/orig_0.8_del.txt')
# test('./sim_0.8/orig.txt','./sim_0.8/orig_0.8_dis_1.txt')
# test('./sim_0.8/orig.txt','./sim_0.8/orig_0.8_dis_3.txt')
# test('./sim_0.8/orig.txt','./sim_0.8/orig_0.8_dis_7.txt')
# test('./sim_0.8/orig.txt','./sim_0.8/orig_0.8_dis_10.txt')
# test('./sim_0.8/orig.txt','./sim_0.8/orig_0.8_dis_15.txt')
# test('./sim_0.8/orig.txt','./sim_0.8/orig_0.8_mix.txt')
# test('./sim_0.8/orig.txt','./sim_0.8/orig_0.8_rep.txt')
# t1, t2 = openfile('./sim_0.8/orig.txt', './sim_0.8/orig_0.8_add.txt')
# t1_cut, t2_cut = dictionaries_cut(t1, t2)
# text_dict = dictionaries_dict(t1_cut, t2_cut)
# t1_cut_code, t2_cut_code = word_cut_count(t1_cut, t2_cut, text_dict)
# an1 = cos(t1_cut_code, t2_cut_code)
