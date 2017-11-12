
# coding: utf-8

# # 保存成csv文件

# In[2]:


import os
import pandas as pd


# In[ ]:


def build_filename(output_path,fname,new_ext):
    fname, ext = os.path.splitext(fname)
    output_filename=os.path.join(output_path,fname+new_ext)
    return output_filename


# In[4]:


def save_seq_to_csv(seq_dataframe,output_path,fname):
    output_filename=build_filename(output_path,fname,'.csv')
    seq_dataframe.to_csv(output_filename)
    return 1


# # 保存成fasta文件
# 
# 提取时貌似有一些字符串上的转换问题, 暂时不保存成fasta文件

# In[5]:


# from Bio.Seq import Seq
# from Bio.SeqRecord import SeqRecord
# from Bio.Alphabet import generic_protein
# from Bio import SeqIO


# In[8]:


def save_seq_to_fasta(seq_dataframe,output_path,fname):
    output_filename=build_filename(output_path,fname,'.fasta')
    seqList=list()
    for ID in seq_dataframe.index:
        Description=seq_dataframe.loc[ID,"chaintype"].to_string #是否用to_string?
        sequence=seq_dataframe.loc[ID,"SEQUENCE"]
        rec = SeqRecord(
                Seq(sequence, generic_protein),
                id=ID+"|"+Description,
                description=Description)
        seqList.append(rec)        
    SeqIO.write(seqList, output_filename, "fasta")
    return True


# In[ ]:




