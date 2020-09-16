import jieba
import math
import re
from jieba.analyse import *
#读入两个txt文件存入s1,s2字符串中
s1 = open('./sim_0.8/orig.txt','r',encoding='utf-8').read()
s2 = open('./sim_0.8/orig_0.8_add.txt','r',encoding='utf-8').read()
for keyword, weight in extract_tags(s1, withWeight=True):
    print('%s %s' % (keyword, weight))
print("\n")
for keyword, weight in extract_tags(s2, withWeight=True):
    print('%s %s' % (keyword, weight))
print("\n")
for keyword, weight in textrank(s1, withWeight=True):
    print('%s %s' % (keyword, weight))
print("\n")
for keyword, weight in textrank(s2, withWeight=True):
    print('%s %s' % (keyword, weight))
print("\n")
#利用jieba分词与停用词表，将词分好并保存到向量中
s1_cut=[]
s2_cut=[]
for keyword, weight in extract_tags(s1, withWeight=True):
    s1_cut.append(keyword)

for keyword, weight in extract_tags(s2, withWeight=True):
    s2_cut.append(keyword)
word_set = set(s1_cut).union(set(s2_cut))

#用字典保存两篇文章中出现的所有词并编上号
word_dict = dict()
i = 0
for word in word_set:
    word_dict[word] = i
    i += 1


#根据词袋模型统计词在每篇文档中出现的次数，形成向量
s1_cut_code = [0]*len(word_dict)

for word in s1_cut:
    s1_cut_code[word_dict[word]]+=1

s2_cut_code = [0]*len(word_dict)
for word in s2_cut:
    s2_cut_code[word_dict[word]]+=1

# 计算余弦相似度
sum = 0
sq1 = 0
sq2 = 0
for i in range(len(s1_cut_code)):
    sum += s1_cut_code[i] * s2_cut_code[i]
    sq1 += pow(s1_cut_code[i], 2)
    sq2 += pow(s2_cut_code[i], 2)

try:
    result = round(float(sum) / (math.sqrt(sq1) * math.sqrt(sq2)), 3)
except ZeroDivisionError:
    result = 0.0
print("\n余弦相似度为：%f"%result)