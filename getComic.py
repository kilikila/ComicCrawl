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


main_href="http://www.ikanman.com/"
#seed_href="http://www.ikanman.com/comic/17726/"
seed_href="http://www.ikanman.com/comic/12468/"

head_href="https:"
phantomjs_path=r"D:\mySoftware\phantomjs-2.1.1-windows\bin\phantomjs.exe"

img_dirs=r"E:\Data\Comic\血魔人"
imgSave= SaveFile(img_dirs)
#imgSave.creatDirs(-1)
def main():
    #漫画集合
    chaperList=[]

    driver = PhDriver(phantomjs_path, seed_href, "chapter-list-1")
    bsObj = BeautifulSoup(driver.getPgSrc(), "html.parser")

    chapter_li=bsObj.find(id='chapter-list-1').findAll("a",{"class":{"status0"}})

    for li_ in chapter_li:
        chaperList.append((li_["href"],li_["title"]))
    
    for i in range(len(chaperList)):
        print("------" + str(i+1)+"--------") #---------------
        getChapter(chaperList[i][0],chaperList[i][1],i+1,driver)
        
    driver.close()
    pass

def getChapter(href,name,index_c,driver):
    bsObj=BeautifulSoup(driver.getPage(main_href + href, "pagination"), "html.parser")
    bsDiv_next = bsObj.find("div", id="pagination")
    while (not bsDiv_next.find("span", class_="disabled")) or (bsDiv_next.find("span",class_="current").get_text()=="1"):
        page_i = bsObj.find("div", id="pagination").find("span", class_="current").get_text()

        #获取图片
        bsImgUrl = bsObj.find(id="mangaFile")["src"]+".webp"
        #imgSave.creatDirs(-1)
        if (bsImgUrl):
           #str(index_c)
            imgSave.saveImg(bsImgUrl,name+"/"+page_i+".jpg")
        print(page_i) #-----------------------------

        nextTag = driver.triggerElements("#pagination .next", "click", lambda dri: driver.getElementByCss("#pagination .current").text!=page_i)
        if nextTag:
            bsObj=BeautifulSoup(driver.getPgSrc(), "html.parser")
            bsDiv_next = bsObj.find("div", id="pagination")

if __name__== '__main__':
    main()
    pass