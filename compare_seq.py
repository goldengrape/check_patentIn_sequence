
# coding: utf-8

# # 序列比对工具
# 
# ## 说明
# 
# * 将需要检查的文件上传/copy 到指定的目录下. 默认是在 demo目录
# * 按照下面的要求指定所需的参数
# * 在菜单中选择Cell -> Run All
# * 整理后的文件将保存在指定的目录下, 以csv方式保存. 

# # 读取数据

# ## 指定参数

# ### 文件参数
# 
# * 原始数据文件的存放路径: input_path
# * 最终比对结果的存放路径: output_path
# * 比对用的源文件: "source":docx_name
# * 比对用的目标文件: "target":txt_name
# 
# 注意, 源文件中的序列是目标文件序列的**子集**

# In[1]:


if __name__=="__main__":
    input_path='demo'
    output_path='demo'
    
    docx_name='AAA.docx'
    txt_name='BBB.txt'
    
#     docx_name='AAA_F.docx' # 阳性测试
#     txt_name='BBB_F.txt'   # 阳性测试
    
    source_target_dict={"source":docx_name,
                        "target":txt_name}
#     source_target_dict={"source":txt_name,
#                         "target":docx_name}


# ### 内容参数

# #### docx文件类型中, 需要指定每个表格的内容参数
# * head: 表头所占的行数
# * seqtype: 序列的类型, 是chain, 还是CDR
# * chaintype: chain的type, 是重链HeavyChain还是轻链LightChain, 注意如果是CDR, 用HC/LC标记

# In[2]:


if __name__=="__main__":
    table_catalog_dict={
        0: {"head": 1, "seqtype":'chain', "chaintype":'HeavyChain'},
        1: {"head": 1, "seqtype":'chain', "chaintype":'LightChain'},
        2: {"head": 2, "seqtype":'CDR', "chaintype":'HC'}, 
        3: {"head": 2, "seqtype":'CDR', "chaintype":'LC'}, 
        4: {"head": 1, "seqtype":'chain', "chaintype":'HeavyChain'},
        5: {"head": 1, "seqtype":'chain', "chaintype":'LightChain'},
    }


# #### TXT文件中, 需要指定名称中的关键词
# 
# 在txt文件中, 需要根据ID的名称判断序列的类型, 因此需要使用下面的字典进行指定, 例如: 
# 名称中包含有"Heavy","heavy","VH","vh" 都将被识别成HeavyChain

# In[3]:


# if __name__=="__main__":
#     marker_words_dict={
#         "HeavyChain":["Heavy","heavy","VH","vh"],
#         "LightChain":["Light","light","VL","vl"],
#         "HCCDR1":["HC CDR1"],
#         "HCCDR2":["HC CDR2"],
#         "HCCDR3":["HC CDR3"],
#         "LCCDR1":["LC CDR1"],
#         "LCCDR2":["LC CDR2"],
#         "LCCDR3":["LC CDR3"],
#     }


# ## 载入依赖包
# 
# 在azure notebook上运行时, 由于远程服务器在1小时后会自动关闭并清除所有安装内容, 所以临时安装的依赖软件包并不能正常加载. 需要使用服务器上的预制程序进行设置: 
# 建立script.txt文件: 
# ```txt
# export PATH=~/anaconda3_410/bin:$PATH
# conda install -c anaconda biopython --yes
# pip install python-docx
# ```
# 然后在setting中加载. 这样每次启动azure notebook时会自动安装biopython和python-docx

# In[4]:


# pandas包, 需安装
import pandas as pd
from pandas import DataFrame, Series

# python-docx包, 需安装
from docx import Document

# biopython包, 需安装
from Bio.SeqUtils import seq1

# 系统自带包, 无需安装
from collections import OrderedDict # 有序字典
import re
import os

# 自建包
from save_sequence import save_seq_to_csv 
# from readDOC import read_sequence_from_docx
# from readTXT import read_sequence_from_TXT
from reconstruct_TXT import reconstruct_TXT
from reconstruct_DOC import reconstruct_DOC


# ## 读取文件
# 
# 文件通过两个程序读入: 
# * read_sequence_from_docx 用于读取docx文件, 
# * read_sequence_from_txt 用于读取txt文件
# 
# 由于可能调换source文件和target文件的对应方式, 所以使用了字典source_target_dict来记录对应关系. 
# 使用文件名的末尾3位来判断文件的类型, 是docx/txt
# 
# 文件读取后经过清理, 转换成pandas DataFrame的数据形式进行操作处理. 并且将转换后的DataFrame保存为**同名csv文件**, 存放在output_path文件夹之下

# In[5]:


def read_source_target_file(input_path,output_path,docx_name,txt_name,
                            source_target_dict,
                            table_catalog_dict,
                            ):
#     docx_df=read_sequence_from_docx(input_path,docx_name,output_path,table_catalog_dict)
#     txt_df=read_sequence_from_TXT(input_path,txt_name,output_path,marker_words_dict)
    docx_df=reconstruct_DOC(input_path,docx_name,output_path,table_catalog_dict)
    txt_df= reconstruct_TXT(input_path,txt_name,output_path)
    source_name=source_target_dict["source"]
    target_name=source_target_dict["target"]

    if (source_name[-3:].lower()=="ocx" or source_name[-3:].lower()=="doc") and target_name[-3:].lower()=="txt":
        source_df=docx_df
        target_df=txt_df
    elif source_name[-3:].lower()=="txt" and (source_name[-3:].lower()=="ocx" or source_name[-3:].lower()=="doc") :
        source_df= txt_df
        target_df= docx_df
    return (source_df,target_df)


# In[6]:


# 以下为文件读取方面的测试
# 应当输出两个数据表格
if __name__=="__main__":
    # 读取文件
    (source_df,target_df)=read_source_target_file(input_path,output_path,docx_name,txt_name,
                            source_target_dict,
                            table_catalog_dict,
                            )
    # 测试读取文件
    print(source_df.iloc[0:4])
    print(target_df.iloc[0:4])


# # 文件内部序列比对
# CDR序列是否出现在chain序列中

# ## 函数is_find
# 函数is_find表示是否可以找到有chain序列包含CDR序列, 
# 输入部分是: 
# * 被检查的数据表df_2check,
# * CDR的ID编号
# * CDR的类型, 可能是HC/LC CDR 1/2/3共6种之一
# * 被检查的chain类型, HCCDR对应检查的是HeavyChain. 以此类推
# 如果能够在chain序列中找到, 就返回True, 否则返回False

# In[7]:


def is_find(df_2check,checker_name,checker_type,target_type):
    
    # 根据checker_ID找到chain和CDR的序列集合, 交给一个数据表df_checker_and_target
    # 例如ID="C8"的序列包含有C8的HeavyChain, LightChain, HCCDR123, LCCDR123
    df_checker_and_target = df_2check.loc[df_2check["NAME"]==checker_name]
    
    # 根据checker_type 和 target_type 分别找到checker的条目和target的条目
    checker_item=df_checker_and_target[ df_checker_and_target['CHAINTYPE']==checker_type ]
    target_item=df_checker_and_target[ df_checker_and_target['CHAINTYPE']==target_type ]
    
    # 要取得checker内所包含的序列字符串, 目前没有发现更优雅的方式,
    # 理论上DataFrame是和numpy的array等效, 所以可以用list强行转换, 
    # list中只有一个项目, 所以用[0]提取出来
    if  type(checker_item) != pd.core.frame.DataFrame :
        return False

    
    checker_seq=list(checker_item["SEQUENCE"])[0] #WTF
    
    # dataframe.str.find是在字符串中寻找checker_seq的位置, 如果没有发现, 位置就返回为-1
    # 返回的数值也是以dataframe object的形式存储
    result = (target_item["SEQUENCE"].str.find(checker_seq)>=0)
    
    # 偶尔会出现不明原因的bug, 导致result中没有任何结果, 也就是一个空list
    # 判断一个list是否为空, 可以使用not list( )的方法
    if not list(result):
        res=False
    else:
        res=list(result)[0]
    return res


# ## 函数check_CDR_in_seq
# 检查数据表df_2check中, 是否每一个CDR都能找到对应的chain
# * 首先从HCCDR123, LCCDR123中选择1个类别的CDR, 例如HCCDR1
# * 根据配对字典找到其对应的被检查类别, 例如HeavyChain
# * 然后依次遍历该CDR种类下所有的项目, 使用is_find函数进行查找
# 
# 最终返回结果以pandas dataframe的形式进行

# In[8]:


def check_CDR_in_seq(df_2check):
    # 配对检查字典
    check_pair_dict={
    "HCCDR1":"HeavyChain",
    "HCCDR2":"HeavyChain",
    "HCCDR3":"HeavyChain",
    "LCCDR1":"LightChain",
    "LCCDR2":"LightChain",
    "LCCDR3":"LightChain"
    }
    
    # 检查结果先暂时存放在list中, 最后再转换成DataFrame
    check_result=list()
    
    # 遍历每一种CDR检查类型
    for checker_type in check_pair_dict.keys():
        target_type=check_pair_dict.get(checker_type)
        checker_name_list=df_2check[ df_2check["CHAINTYPE"]==checker_type ].NAME
        
    # 遍历检查类型中的每一个ID, 同一ID下会有多个序列, 
    # 例如ID="C8"时, C8 HCCDR1/ C8 HCCDR2/ C8 HCCDR3 /C8 Heavychain/ C8 Lightchain
        for checker_name in checker_name_list:
            # 交给is_find函数检查
            if is_find(df_2check,checker_name,checker_type,target_type)==False:
                
                # 单独提取出异常的checker存入列表中
                give_out=df_2check.loc[df_2check["NAME"]==checker_name]
                give_out=give_out[ give_out ["CHAINTYPE"]==checker_type ]
                check_result.append(give_out)
#                 print(give_out)
    # 返回结果中如果是空列表, 就返回空的DataFrame
    if not check_result: # check list isempty
        result=DataFrame() # 此处不可直接使用pd.concat, 否则报错
    else:
        result=DataFrame(pd.concat(check_result))
    return result 


# In[9]:


if __name__=="__main__":
    # 读取文件
    (source_df,target_df)=read_source_target_file(input_path,output_path,docx_name,txt_name,
                            source_target_dict,
                            table_catalog_dict,
                            )    
    #文件内部比对
    df_2check=source_df
    source_df_check_result=check_CDR_in_seq(df_2check)
    print("\n{0}文件中, 不能找到对应序列的有:".format(source_target_dict["source"]))
    print(source_df_check_result) 

    df_2check=target_df
    target_df_check_result=check_CDR_in_seq(df_2check)
    print("\n{0}文件中, 不能找到对应序列的有:".format(source_target_dict["target"]))
    print(target_df_check_result)


# # 文件之间的序列比对

# 所有source文件中的序列, 都应当出现在target文件中

# In[10]:


def check_seq_between(source_df,target_df):
    # 这里希望一并检查ID, SEQUENCE和CHAINTYPE, 因此重置了index, 使得ID也作为column
    newsource_df=source_df.reset_index()
    newtarget_df=target_df.reset_index()
    
    # 结果先暂存至list中
    result_list=list()
    
    # 遍历source数据表中的每一项, 去target数据表中查询
    for iloc in range(newsource_df.shape[0]) :
        source_item = newsource_df.iloc[iloc]
        # 遍历查询比较, 将返回一个数据表, 每一项中以True/False标记是否相同
        same_item=newtarget_df[newtarget_df==source_item]
        
        if source_item["ID"] <=0 : # 如果没有合适的ID, 会使用负数作为标记. 
        # 提取出所有"SEQUENCE"为真 并且 "chaintype" 为真的项目
            tf=any ( # pd.notnull(same_item["ID"]) &  # 当没有合适ID时, 则不比较ID
                     pd.notnull(same_item["SEQUENCE"]) & 
                     pd.notnull(same_item["CHAINTYPE"]) ) 
        else:
            tf=any ( pd.notnull(same_item["ID"]) &  # 只在有合适ID时, 才比较ID
                    pd.notnull(same_item["SEQUENCE"]) & 
                    pd.notnull(same_item["CHAINTYPE"]) ) 
        if tf==False:
            result_list.append(source_item)
            
    if not result_list:
        result=DataFrame()
    else:
        result=pd.concat(result_list)
        
    return result
    


# In[11]:


if __name__=="__main__":
    # 读取文件
    (source_df,target_df)=read_source_target_file(input_path,output_path,docx_name,txt_name,
                            source_target_dict,
                            table_catalog_dict,
                            )    
    # 文件内部比对
    df_2check=source_df
    source_df_check_result=check_CDR_in_seq(df_2check)
    print("\n{0}文件中, 不能找到对应序列的有:".format(source_target_dict["source"]))
    print(source_df_check_result) 

    df_2check=target_df
    target_df_check_result=check_CDR_in_seq(df_2check)
    print("\n{0}文件中, 不能找到对应序列的有:".format(source_target_dict["target"]))
    print(target_df_check_result)
    
    # 文件之间的比对
    result_df=check_seq_between(source_df,target_df)
    print("\n在源文件{0}文件中, 不能找到对应序列的有:".format(source_target_dict["source"]))
    print(result_df)


# # 输出结果

# In[12]:


def explain_result(source_df_check_result,target_df_check_result,result_df,output_path):
    explain=""
    explain +=("被检查的文件有: \n源文件为:\t{0}\n目标文件为:\t{1}".format(source_target_dict["source"],source_target_dict["target"]))
    explain +="\n"+"="*50+"\n"
    explain +=("检查CDR是否出现在相应的序列中: \n")
    explain +=("在源文件{0}中, ".format(source_target_dict["source"]))

    if source_df_check_result.shape[0]==0:
        explain+=("未发现异常\n")
    else:
        explain+="存在 {0} 条异常序列: \n".format(source_df_check_result.shape[0])
        explain+=(str(source_df_check_result))
        explain +="\n"+"="*50+"\n"


    explain+=("\n在目标文件{0}中, ".format(source_target_dict["target"]))

    if target_df_check_result.shape[0]==0:
        explain+=("未发现异常\n")
    else:
        explain+="存在 {0} 条异常序列: \n".format(target_df_check_result.shape[0])
        explain+=(str(target_df_check_result))
        explain +="\n"+"="*50+"\n"


    explain +=("\n检查源文件{0}中的序列是否都出现在目标文件{1}中: \n").format(source_target_dict["source"],source_target_dict["target"])
    if result_df.shape[0]==0:
        explain+=("未发现异常\n")
    else:
        explain+="存在 {0} 条异常序列: \n".format(result_df.shape[0]/5)
        explain+=(str(DataFrame(result_df)))
        explain +="\n"+"="*50+"\n"

    explain +="\n"
    report_filename=os.path.join(output_path,"report.txt")
    f=open(report_filename,'w')
    f.write(explain)
    return explain


# In[13]:


if __name__=="__main__":
    # 读取文件
    (source_df,target_df)=read_source_target_file(input_path,output_path,docx_name,txt_name,
                            source_target_dict,
                            table_catalog_dict,
                            )    
    # 文件内部比对
    df_2check=source_df
    source_df_check_result=check_CDR_in_seq(df_2check)

    df_2check=target_df
    target_df_check_result=check_CDR_in_seq(df_2check)
    
    # 文件之间的比对
    result_df=check_seq_between(source_df,target_df)
    
    # 生成报告
    report=explain_result(source_df_check_result,target_df_check_result,result_df,output_path)
    print(report)


# # 整理封装

# In[14]:


def compare_sequence(input_path,output_path,docx_name,txt_name,
                            source_target_dict,
                            table_catalog_dict,
                            ):
    # 读取文件
    (source_df,target_df)=read_source_target_file(input_path,output_path,docx_name,txt_name,
                            source_target_dict,
                            table_catalog_dict,
                            )
    
    # 文件内部比对
    df_2check=source_df
    source_df_check_result=check_CDR_in_seq(df_2check)

    df_2check=target_df
    target_df_check_result=check_CDR_in_seq(df_2check)
    
    # 文件之间的比对
    result_df=check_seq_between(source_df,target_df)
    
    # 生成报告
    report=explain_result(source_df_check_result,target_df_check_result,result_df,output_path)
    print(report)
    return (source_df_check_result,target_df_check_result,result_df)


# In[15]:


if __name__=="__main__":
    compare_sequence(input_path,output_path,docx_name,txt_name,
                            source_target_dict,
                            table_catalog_dict,
                            )


# In[ ]:




