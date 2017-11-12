
# coding: utf-8

# # 设定参数读取文件

# ## 指定文件路径和文件名

# In[1]:


if __name__=="__main__":
    input_path='demo'
    fname='BBB.txt'
    output_path="demo"


# In[2]:


import re
import os
import json

import pandas as pd
from pandas import DataFrame,Series
from Bio.SeqUtils import seq1
from save_sequence import save_seq_to_csv # 自建包, 保存数据至csv
from patentIn_to_json import patentIn_to_json
from cleaner import chaintype_clean,name_clean,seq_3letters_clean, seq_1letters_clean, ID_clean


# ## 转换并读取JSON

# In[3]:


def read_json_to_dataframe(input_path,fname,output_path):
    json_filename=patentIn_to_json(input_path,fname,output_path)
    data=pd.read_json(json_filename)
    return(data)


# In[4]:


if __name__=="__main__":
    # 转换并读取json
    df=read_json_to_dataframe(input_path,fname,output_path)
    print(df[0:2])


# # 抽取dataframe, 重整

# In[5]:


def reframe_df(df):
    seq_df=df.loc[1:,["<210>","<223>","<seq>"]].copy()
    seq_df.columns=["ID","NAME","SEQUENCE"]
    seq_df['CHAINTYPE']=seq_df.NAME
    seq_df=seq_df.fillna("None")

    return (seq_df)


# In[10]:


if __name__=="__main__":
    # 转换并读取json
    df=read_json_to_dataframe(input_path,fname,output_path)
    
    #抽取dataframe, 重整
    df=reframe_df(df)


# # 清洗
# 
# * 清洗name
# ```python    
# df=name_clean(df,'NAME') ```
# * 清洗3字母序列
# ```python   
#     df=seq_3letters_clean(df,'SEQUENCE')```
#     
# * 清洗单字母序列
# ```python   
#     df=seq_1letters_clean(df,'SEQUENCE')```
# 
# * 根据chaintype关键字清洗chaintype
# ```python   
#     df=chaintype_clean(df,"CHAINTYPE")```

# In[7]:


if __name__=="__main__":
    # 转换并读取json
    df=read_json_to_dataframe(input_path,fname,output_path)
    
    # 抽取dataframe, 重整
    df=reframe_df(df)
    
    # 清洗ID
    df=ID_clean(df,'ID')
    
    # 清洗name
    df=name_clean(df,'NAME')
    
    # 清洗3字母序列
    df=seq_3letters_clean(df,'SEQUENCE')
    
    # 清洗单字母序列
    df=seq_1letters_clean(df,'SEQUENCE')

    # 根据chaintype关键字清洗chaintype
    df=chaintype_clean(df,"CHAINTYPE")
    
    print(df[0:152:20])


# # 保存数据

# In[8]:


if __name__=="__main__":
    # 转换并读取json
    df=read_json_to_dataframe(input_path,fname,output_path)
    
    # 抽取dataframe, 重整
    df=reframe_df(df)
    
    # 清洗ID
    df=ID_clean(df,'ID')
    
    # 清洗name
    df=name_clean(df,'NAME')
    
    # 清洗3字母序列
    df=seq_3letters_clean(df,'SEQUENCE')
    
    # 清洗单字母序列
    df=seq_1letters_clean(df,'SEQUENCE')

    # 根据chaintype关键字清洗chaintype
    df=chaintype_clean(df,"CHAINTYPE")
    
    # 保存数据
    save_seq_to_csv(df,output_path,fname)


# # 封装

# In[9]:


def reconstruct_TXT(input_path,fname,output_path):
    # 转换并读取json
    df=read_json_to_dataframe(input_path,fname,output_path)
    
    # 抽取dataframe, 重整
    df=reframe_df(df)
    
    # 清洗ID
    df=ID_clean(df,'ID')
    
    # 清洗name
    df=name_clean(df,'NAME')
    
    # 清洗3字母序列
    df=seq_3letters_clean(df,'SEQUENCE')
    
    # 清洗单字母序列
    df=seq_1letters_clean(df,'SEQUENCE')

    # 根据chaintype关键字清洗chaintype
    df=chaintype_clean(df,"CHAINTYPE")
    
    # 保存数据
    save_seq_to_csv(df,output_path,fname)
    
    return df
    

