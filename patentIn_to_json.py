
# coding: utf-8

# # 读取并整理txt

# # 读取txt

# In[1]:


import re
import os


# ## 指定文件路径和文件名

# In[2]:


if __name__=="__main__":
    input_path='demo'
    fname='BBB.txt'
    output_path="demo"


# ## 打开文件, 读入文件
# 

# In[3]:


def read_content_fromTXT(input_path,fname):
    filename=os.path.join(input_path,fname)
    txtfile = open(filename,'r')
    sContent=txtfile.read()
    txtfile.close()
    return sContent


# In[4]:


if __name__=="__main__":
    # 打开并读入文件
    sContent=read_content_fromTXT(input_path,fname)


# # 转换成JSON

# ## 增加标签
# 使每一个条目都统一成为
# ```
# <标签名> 内容
# ```
# 
# * 在SEQUENCE LISTING前增加标签000
# * 在400标签之后增加序列标签
# 

# In[5]:


def add_000_to_title(sContent):
    sContent="<000>"+sContent
    return sContent


# In[6]:


if __name__=="__main__":
    # 打开并读入文件
    sContent=read_content_fromTXT(input_path,fname)
    
    # 在SEQUENCE LISTING前增加标签000
    sContent= add_000_to_title(sContent)
    #print(sContent)
    


# In[7]:


def add_tag_after_tag(sContent,add_tag,target_tag):
#     target_tag="<400>"
#     add_tag="<seq>"
    target=target_tag+".*\n"
    words=re.findall(target,sContent)
    for w in words:
        sContent=re.sub(w,w+add_tag,sContent)
    return(sContent)


# In[8]:


if __name__=="__main__":
    # 打开并读入文件
    sContent=read_content_fromTXT(input_path,fname)
    
    # 在SEQUENCE LISTING前增加标签000
    sContent= add_000_to_title(sContent)
    
    # 在400标签下一行增加标签seq
    sContent=add_tag_after_tag(sContent,"<seq>","<400>")
    #print(sContent)


# ## 替换所有的换行
# 需要在增加了seq标签以后进行

# In[9]:


def sub_all_return(sContent):
    sContent=re.sub("\n","",sContent)

#     sContent=re.sub(","," ",sContent) # 去掉原有的逗号
    sContent=re.sub("<",",\n<",sContent)
    sContent=sContent[2:] # 去掉首行多余的东西
    return sContent


# In[10]:


if __name__=="__main__":
    # 打开并读入文件
    sContent=read_content_fromTXT(input_path,fname)
    
    # 在SEQUENCE LISTING前增加标签000
    sContent= add_000_to_title(sContent)
    
    # 在400标签下一行增加标签seq
    sContent=add_tag_after_tag(sContent,"<seq>","<400>")
    
    # 替换所有的换行
    sContent=sub_all_return(sContent)
    #print(sContent)


# ## 以210分界, 作为对象加大括号

# In[11]:


def add_to_obj(sContent):
    sContent=re.sub('<210>','},\n{\n<210>',sContent)
    sContent='{\n'+sContent+'\n}'
    return sContent


# In[12]:


if __name__=="__main__":
    # 打开并读入文件
    sContent=read_content_fromTXT(input_path,fname)
    
    # 在SEQUENCE LISTING前增加标签000
    sContent= add_000_to_title(sContent)
    
    # 在400标签下一行增加标签seq
    sContent=add_tag_after_tag(sContent,"<seq>","<400>")
    
    # 替换所有的换行
    sContent=sub_all_return(sContent)
    
    # 以210分界, 作为对象加大括号
    sContent= add_to_obj(sContent)
    print(sContent)
    


# ## 加入方括号成为键值数组
# 
# * 在首次出现2xx的标签时, 加入左反括号[
# * 在文件末尾加入右方括号]

# In[13]:


def add_square(sContent):
    sContent='['+sContent+']'
    return sContent


# In[14]:


if __name__=="__main__":
    # 打开并读入文件
    sContent=read_content_fromTXT(input_path,fname)
    
    # 在SEQUENCE LISTING前增加标签000
    sContent= add_000_to_title(sContent)
    
    # 在400标签下一行增加标签seq
    sContent=add_tag_after_tag(sContent,"<seq>","<400>")
    
    # 替换所有的换行
    sContent=sub_all_return(sContent)
    
    # 以210分界, 作为对象加大括号
    sContent= add_to_obj(sContent)
    
    #加入方括号成为键值数组
    sContent=add_square(sContent)
    # print(sContent)


# ## 重整所有的标签

# In[15]:


def sub_all_tag(sContent):
    sContent=re.sub('<','"<',sContent)
    sContent=re.sub('>','>" : " ',sContent)
    sContent=re.sub(',\n','",\n',sContent)
    sContent=re.sub(',\n}",','\n},',sContent)
    sContent=re.sub('\n}]','"\n}]',sContent)
    return sContent


# In[16]:


if __name__=="__main__":
    # 打开并读入文件
    sContent=read_content_fromTXT(input_path,fname)
    
    # 在SEQUENCE LISTING前增加标签000
    sContent= add_000_to_title(sContent)
    
    # 在400标签下一行增加标签seq
    sContent=add_tag_after_tag(sContent,"<seq>","<400>")
    
    # 替换所有的换行
    sContent=sub_all_return(sContent)
    
    # 以210分界, 作为对象加大括号
    sContent= add_to_obj(sContent)
    
    # 加入方括号成为键值数组
    sContent=add_square(sContent)
    
    # 重整所有的标签
    sContent=sub_all_tag(sContent)

    print(sContent)


# # 保存成JSON

# In[17]:


def write_content_toJSON(output_path,fname,content):
    fname, ext = os.path.splitext(fname)
    output_filename=os.path.join(output_path,fname+'.json')

    jsonfile = open(output_filename,'w')
    jsonfile.write(content)
    jsonfile.close()
    return output_filename


# In[18]:


if __name__=="__main__":
    # 打开并读入文件
    sContent=read_content_fromTXT(input_path,fname)
    
    # 在SEQUENCE LISTING前增加标签000
    sContent= add_000_to_title(sContent)
    
    # 在400标签下一行增加标签seq
    sContent=add_tag_after_tag(sContent,"<seq>","<400>")
    
    # 替换所有的换行
    sContent=sub_all_return(sContent)
    
    # 以210分界, 作为对象加大括号
    sContent= add_to_obj(sContent)
    
    # 加入方括号成为键值数组
    sContent=add_square(sContent)
    
    # 重整所有的标签
    sContent=sub_all_tag(sContent)
    
    # 保存为json
    output_filename=write_content_toJSON(output_path,fname,sContent)


# # 整合封装

# In[19]:


def patentIn_to_json(input_path,fname,output_path):
     # 打开并读入文件
    sContent=read_content_fromTXT(input_path,fname)
    
    # 在SEQUENCE LISTING前增加标签000
    sContent= add_000_to_title(sContent)
    
    # 在400标签下一行增加标签seq
    sContent=add_tag_after_tag(sContent,"<seq>","<400>")
    
    # 替换所有的换行
    sContent=sub_all_return(sContent)
    
    # 以210分界, 作为对象加大括号
    sContent= add_to_obj(sContent)
    
    # 加入方括号成为键值数组
    sContent=add_square(sContent)
    
    # 重整所有的标签
    sContent=sub_all_tag(sContent)
    
    # 保存为json
    output_filename=write_content_toJSON(output_path,fname,sContent)
    
    return output_filename

