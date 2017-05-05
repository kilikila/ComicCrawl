# -*- coding:utf-8 -*-
import os
import os.path
import re
import codecs

from chNum2Dig import *

#FileInfos=[{no:,name:,num,typ:}]

#img_dirs=r"E:\Data\Comic\血魔人"
#img_dirs=r"E:\Data\Comic\人皮衣裳"
#img_dirs=r"E:\Data\Comic\皇帝的独生女"
#img_dirs=r"E:\Data\Comic\爱神巧克力进行时"
#img_dirs=r"E:\Data\Comic\无限恐怖"
img_dirs=r"E:\Data\Comic\血色苍穹"

#---------------------------------------------
#需要考虑到冲突->文件按创建时间排序编号(多线程时无效,需要爬取时就进行保存)
#----------------------------------------------

index_err = 0

#获取中文
def getNum(strName):
    global index_err
    str_Num=""
    try:
        #str_Num=str(int(re.findall(r'\d+', strName)[0]))
        numMatch=re.search(r'\d+',strName)
        cnMatch=re.search(CN_POOLSTR+"+",strName)
        if cnMatch:
            if cnMatch.start()<numMatch.start():  #中文匹配在数字匹配之前
                str_Num=str(cn2dig(cnMatch.group(0)))
        if not str_Num:
            str_Num=str(int(numMatch.group(0)))
    except Exception as e:
        index_err += 1
        str_Num="-"+str(index_err)
    finally:
        return str_Num



'''
index_err = 0

#获取中文
def getNum(strName):
    global index_err
    str_Num=""
    try:
        str_Num=str(int(re.findall(r'\d+', strName)[0]))
        #numMatch=re.search(r'\d+',strName)
        #cnMatch=re.search(CN_POOL+"+",strName)
        #if cnMatch.start()
    except Exception as e:
        index_err += 1
        str_Num="-"+str(index_err)
    finally:
        return str_Num

'''

#获取列表
def getFileInfos(url,typ):
    arr=[]
    dirList = os.listdir(url)
    for dir_name in dirList:
        dirPath=os.path.join(url,dir_name)
        if not os.path.isdir(dirPath):continue

        chapter_No=getNum(dir_name)
        file_Num=len(os.listdir(dirPath))

        arr.append({"no":chapter_No,"name":dir_name,"num":str(file_Num),"typ":typ})

    return arr

#info
def getInfoFile(arr,filrName):
    str_arr="FileInfos=["
    for info_t in arr:
        str_t="\n{\'no\':"+info_t["no"]+",\'name\':\'"+info_t["name"]+"\',\'num\':"+info_t["num"]+",\'typ\':\'"+info_t["typ"]+"\'},"
        str_arr+=str_t
    str_arr=str_arr[:-1]+"]"

  #  str_arr.encode('utf-8')  #修改编码方式

    file_object = codecs.open(filrName, 'w','utf-8')
    file_object.write(str_arr)
    file_object.close()

    pass


if __name__== '__main__':
    getInfoFile(getFileInfos(img_dirs,"jpg"),os.path.join(img_dirs,"info.js"))
    pass