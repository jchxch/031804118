import math
# import os  # 调用获取文件路径最后一级的函数的函数库
from jieba.analyse import *
import sys


# 导入两个文本的内容
# @profile()#内存消耗记录显示
def openfile(argv1, argv2):
    s1 = []
    s2 = []
    try:
        s1 = open(argv1, 'r', encoding='utf-8').read()  # 以utf-8格式读取文件
        s2 = open(argv2, 'r', encoding='utf-8').read()
    except IOError:
        print("文件打开失败")
    return s1, s2


# 提取两个文本中累计权重75%的关键词
# @profile()
def dictionaries_cut(s1, s2):
    s1_cut = []
    s2_cut = []
    s1_rate = 0
    s2_rate = 0
    try:
        for keyword, weight in extract_tags(s1, withWeight=True):  # TF-IDF计算词频并排序，keyword为关键词，weight为该词重要度
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
        # s1_cut = extract_tags(s1, topK=200, withWeight=False)
        # s2_cut = extract_tags(s2, topK=200, withWeight=False)
    except AttributeError:
        print("无法计算关键词")
    return s1_cut, s2_cut


# 用两个文本中提取的关键词形成词典
# @profile()
def dictionaries_dict(s1_cut, s2_cut):
    word_set = set(s1_cut).union(set(s2_cut))  # set()无序不重复元素集合合并
    word_dict = dict()
    i = 0
    for word in word_set:
        word_dict[word] = i
        i += 1
    return word_dict


# 生成两个文本对应词的向量
# @profile()
def word_cut_count(s1_cut, s2_cut, word_dict):
    s1_cut_code = [0] * len(word_dict)

    for word in s1_cut:
        s1_cut_code[word_dict[word]] += 1

    s2_cut_code = [0] * len(word_dict)
    for word in s2_cut:
        s2_cut_code[word_dict[word]] += 1
    return s1_cut_code, s2_cut_code


# 余弦相似度计算
# @profile()
# def cos(s1_cut_code, s2_cut_code, str1, str2):#print结果
#     sum_code = 0
#     sq1 = 0
#     sq2 = 0
#     for i in range(len(s1_cut_code)):
#         sum_code += s1_cut_code[i] * s2_cut_code[i]
#         sq1 += pow(s1_cut_code[i], 2)
#         sq2 += pow(s2_cut_code[i], 2)
#
#     try:
#         result = round(float(sum_code) / (math.sqrt(sq1) * math.sqrt(sq2)), 3)
#     except ZeroDivisionError:
#         result = 0.0
#     print(str1 + "与" + str2 + "余弦相似度为：%.2f\n" % result)
#     return round(result, 2)
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
    return round(result, 2)


# 写入答案文件
def answer(argv3, an):
    file = open(argv3, 'a+', encoding='utf-8')
    file.write(an + "\n")
    file.close()


t1, t2 = openfile(sys.argv[1], sys.argv[2])
t1_cut, t2_cut = dictionaries_cut(t1, t2)
text_dict = dictionaries_dict(t1_cut, t2_cut)
t1_cut_code, t2_cut_code = word_cut_count(t1_cut, t2_cut, text_dict)
an1 = cos(t1_cut_code, t2_cut_code)
answer(sys.argv[3], str(an1))

# 测试集
# def test(a, b):
#     t1, t2 = openfile(a, b)
#     t1_cut, t2_cut = dictionaries_cut(t1, t2)
#     text_dict = dictionaries_dict(t1_cut, t2_cut)
#     t1_cut_code, t2_cut_code = word_cut_count(t1_cut, t2_cut, text_dict)
#     an1 = cos(t1_cut_code, t2_cut_code, os.path.basename(a), os.path.basename(b))
#     return an1
#
#
# test('./sim_0.8/orig.txt', './sim_0.8/orig_0_empty.txt')
# test('./sim_0.8/orig.txt', './sim_0.8/orig_0.8_add.txt')
# test('./sim_0.8/orig.txt', './sim_0.8/orig_0.8_del.txt')
# test('./sim_0.8/orig.txt', './sim_0.8/orig_0.8_dis_1.txt')
# test('./sim_0.8/orig.txt', './sim_0.8/orig_0.8_dis_3.txt')
# test('./sim_0.8/orig.txt', './sim_0.8/orig_0.8_dis_7.txt')
# test('./sim_0.8/orig.txt', './sim_0.8/orig_0.8_dis_10.txt')
# test('./sim_0.8/orig.txt', './sim_0.8/orig_0.8_dis_15.txt')
# test('./sim_0.8/orig.txt', './sim_0.8/orig_0.8_mix.txt')
# test('./sim_0.8/orig.txt', './sim_0.8/orig_0.8_rep.txt')
# t1, t2 = openfile('./sim_0.8/orig.txt', './sim_0.8/orig_0.8_add.txt')
# t1_cut, t2_cut = dictionaries_cut(t1, t2)
# text_dict = dictionaries_dict(t1_cut, t2_cut)
# t1_cut_code, t2_cut_code = word_cut_count(t1_cut, t2_cut, text_dict)
# an1 = cos(t1_cut_code, t2_cut_code)
