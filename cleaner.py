
# coding: utf-8

# # 按照内容更新column

# In[1]:


import re
import pandas as pd
from Bio.SeqUtils import seq1


# In[2]:


def update_column(dataframe_2bClean,col,update_method):
    dataframe_2bClean[col]=[update_method(x) for x in dataframe_2bClean[col]]
    return dataframe_2bClean


# # 根据chaintype关键字清洗chaintype

# In[3]:


def each_chaintype_clean(x_2bclean):
    marker_words_dict={
    "HeavyChain":["Heavy","heavy","VH","vh"],
    "LightChain":["Light","light","VL","vl"],
    "HCCDR1":["HC CDR1","HCCDR1"],
    "HCCDR2":["HC CDR2","HCCDR2"],
    "HCCDR3":["HC CDR3","HCCDR3"],
    "LCCDR1":["LC CDR1","LCCDR1"],
    "LCCDR2":["LC CDR2","LCCDR2"],
    "LCCDR3":["LC CDR3","LCCDR3"],
    }
    result="sequence"
    for chaintype in marker_words_dict.keys():
        for keyword in marker_words_dict.get(chaintype):
            if keyword in x_2bclean:
                result=chaintype
                return result
        
    return result

def chaintype_clean(dataframe_2bClean,col):
    return update_column(dataframe_2bClean,col,each_chaintype_clean)


# # 清理name

# In[4]:


def each_name_clean(ID_2bClean):
    # 先清理掉所有特殊符号字符
    ID_2bClean=re.sub("[^A-Za-z0-9\s]", " ",ID_2bClean)
    # 再清理掉常用的关键词
    clean_word_list=["Heavy","Light","Chain","HC","LC","CDR1","CDR2","CDR3"]
    for clean_word in clean_word_list:
        ID_2bClean=re.sub(clean_word, "",ID_2bClean)
    
    # 如果最后一位为数字, 加上一个空格, 满足\d\s的选择
    ID_2bClean=ID_2bClean.strip()+" "
    # 按照数字后为空格的方式切分
    ID_part1=re.split("\d\s",ID_2bClean)[0]
    ID_part2=re.findall("\d\s",ID_2bClean)
    if len(ID_part2)==0:
        ID=ID_part1
    else:
        ID=ID_part1+ID_part2[0]
#     ID=ID_2bClean
    ID=ID.strip()
    return ID
def name_clean(dataframe_2bClean,col):
    return update_column(dataframe_2bClean,col,each_name_clean)


# # 清洗3字母序列

# In[5]:


def each_seq_3letters_clean(seq_2bClean):
    s=re.findall('[A-Z][a-z][a-z]',seq_2bClean)
    seq=''.join(s)
    seq=seq1(seq)
    return(seq)
def seq_3letters_clean(dataframe_2bClean,col):
    return update_column(dataframe_2bClean,col,each_seq_3letters_clean)


# # 清洗单字母序列

# In[6]:


def each_seq_1letters_clean(seq_2bClean):
    seq_2bClean=seq_2bClean.strip()
    s=re.findall('[A-Z]*',seq_2bClean)
    seq=s[0]
    return(seq)

def seq_1letters_clean(dataframe_2bClean,col):
    return update_column(dataframe_2bClean,col,each_seq_1letters_clean)


# # 清洗ID

# In[7]:


def each_ID_clean(ID_2bClean):
    if type(ID_2bClean) != str:
        ID_2bClean=str(int(ID_2bClean))
    numstr=''.join(re.findall('\d',ID_2bClean))
    if numstr=="": # 如果没有用于生成ID的数字, 则会得到空字符串
        num=-1     # 使用一个负数作为标记, 说明并没有合适的ID
    else:
        num=int(numstr)
    return(num)

def ID_clean(dataframe_2bClean,col):
    return update_column(dataframe_2bClean,col,each_ID_clean)


# In[ ]:




