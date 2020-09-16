import jieba
import math
import re
#读入两个txt文件存入s1,s2字符串中
s1 = open('./sim_0.8/orig.txt','r').read()
s2 = open('./sim_0.8/orig_0.8_add.txt','r').read()

#利用jieba分词与停用词表，将词分好并保存到向量中
stopwords=[]
fstop=open('stop_words.txt','r',encoding='utf-8-sig')
for eachWord in fstop:
    eachWord = re.sub("\n", "", eachWord)
    stopwords.append(eachWord)
fstop.close()
s1_cut = [i for i in jieba.cut(s1, cut_all=True) if (i not in stopwords) and i!='']
s2_cut = [i for i in jieba.cut(s2, cut_all=True) if (i not in stopwords) and i!='']
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