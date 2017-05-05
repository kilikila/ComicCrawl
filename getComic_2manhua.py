# -*- coding:utf-8 -*-
from os import _exit

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver

from CrawlDrivers.BrowerDriver import PhDriver
from CrawlDrivers.pyDriver import getHtml
from DAO.DB_mysql import DB_Mysql
from DAO.FileSave import SaveFile


main_href="http://www.2manhua.com/"

seed_href="http://www.2manhua.com/comic/25759/" #血色苍穹

head_href="https:"
phantomjs_path=r"D:\mySoftware\phantomjs-2.1.1-windows\bin\phantomjs.exe"

#img_dirs=r"E:\Data\Comic\血魔人"
#img_dirs=r"E:\Data\Comic\人皮衣裳"
#img_dirs=r"E:\Data\Comic\皇帝的独生女"
#img_dirs=r"E:\Data\Comic\爱神巧克力进行时"
img_dirs=r"E:\Data\Comic\血色苍穹"


imgSave= SaveFile(img_dirs)
#imgSave.creatDirs(-1)
def bgCrawl(bg_i):
    #漫画集合
    chaperList=[]

    driver = PhDriver(phantomjs_path, seed_href, "header")
    bsObj = BeautifulSoup(driver.getPgSrc(), "html.parser")

    chapter_li=bsObj.find("div",class_='chapter-list')("a")

    for li_ in chapter_li:
        chaperList.append((li_["href"].split("/")[-1],li_["title"]))
    
    for i in range(len(chaperList)):
        if i+1<bg_i:continue
        print("------" + str(i+1)+"--------") #---------------
        getChapter(chaperList[i][0],chaperList[i][1],i+1,driver)
        
    driver.close()
    pass

def getChapter(href,name,index_c,driver):
    bsObj=BeautifulSoup(driver.getPage(seed_href + href, "pager"), "html.parser")
    bsDiv_next = bsObj.find("div", id="pager")
    imgSave.creatDirs(name)
    while True:#(not bsDiv_next.find("span", class_="disabled")) or (bsDiv_next.find("span",class_="current").get_text()=="1"):
        page_i = bsDiv_next.find("span", class_="current").get_text()

        #获取图片
        bsImgUrl = bsObj.find("img",id="manga")["src"]
        #imgSave.creatDirs(-1)
        if (bsImgUrl):
           #str(index_c)
            imgSave.saveImg(bsImgUrl,name+"/"+page_i+".jpg")
        print(page_i) #-----------------------------

        if page_i==str(len(bsObj.find("select",id="pageSelect")("option"))):break

        nextTag = driver.triggerElements("#next", "click", lambda dri: driver.getElementByCss("#pager .current").text!=page_i)
        if nextTag:
            bsObj=BeautifulSoup(driver.getPgSrc(), "html.parser")
            bsDiv_next = bsObj.find("div", id="pager")

if __name__== '__main__':
    #216
    bgCrawl(137)
    pass