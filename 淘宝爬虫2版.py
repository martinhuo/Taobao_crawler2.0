from selenium import webdriver
from bs4 import BeautifulSoup 
import re 
import time
import random
import pandas
import numpy
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys


product = []
price = []
sales = []
seller = []
location = []
picture = []
link = []
comment = []
errorset = []


chrome_options = webdriver.chrome.options.Options()
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36")
chrome_options.add_argument(f'--window-position={217},{172}')
chrome_options.add_argument(f'--window-size={1020},{1000}')
chrome_options.add_experimental_option("excludeSwitches",['enable-automation']) #关闭自动测试提醒
s = Service(r"C:\Program Files\Google\Chrome\Application\chromedriver.exe")
#驱动目录
browser = webdriver.Chrome(service=s,options=chrome_options)

with open("/Users/huohh/Desktop/python study/script/stealth.min.js") as AA:
    js1 = AA.read()
    #括号内为脚本文件"stealh"存储路径   
browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",{"source": js1})
#导入脚本


url = input("搜索网页地址：")
pn = int(input("爬取页数："))
scantime = int(input("扫码登陆所需时长："))
pagenum = int(input("爬取评论页数："))


def crawler():

    js2 = "window.scrollTo(0,document.body.scrollHeight)"
    browser.execute_script(js2)
    
    content = browser.page_source
    soup = BeautifulSoup(content,"html.parser")
    print(soup)

    content1 = soup.find_all(name = "div",attrs = "pic")
    g1 = str(content1)
    k1 = re.findall('alt="(.*?)"',g1)
    #收集商品名
    print(len(k1))
    print(k1) 

    content2 = soup.find_all(name = "div",attrs = "price g_price g_price-highlight")
    g2 = str(content2)
    k2 = re.findall('<strong>(.*?)</strong>',g2)
    #收集价格
    print(len(k2))
    print(k2)

    content3 = soup.find_all(name = "div",attrs = "deal-cnt")
    g3 = str(content3)
    k3 = re.findall('<div class="deal-cnt">(.*?)人付款</div>',g3)
    #收集销量
    print(len(k3))
    print(k3)

    content4 = soup.find_all(name = "div",attrs = "shop")
    g4 = str(content4)
    k4 = re.findall('<span>(.*?)</span>',g4)
    #收集店铺名
    print(len(k4))
    print(k4)

    content5 = soup.find_all(name = "div",attrs = "location")
    g5 = str(content5)
    k5 = re.findall('<div class="location">(.*?)</div>',g5)
    #收集卖家位置
    print(len(k5))
    print(k5)

    content6 = soup.find_all(name = "div",attrs = "pic")
    g6 = str(content6)
    k6 = re.findall('data-src="(.*?)"',g6)
    #收集商品图片网址
    print(len(k6))
    print(k6)

    content7 = soup.find_all(name = "div",attrs = "pic")
    g7 = str(content7)
    k7 = re.findall('data-href="(.*?)"',g7)
    #收集商品链接
    print(len(k7))
    print(k7) 

    if len(k1) == len(k2) == len(k3) == len(k4) == len(k5) == len(k6) == len(k7) :

        if len(k1) > 0 :
            product.extend(k1)
            price.extend(k2)
            sales.extend(k3)
            seller.extend(k4)
            location.extend(k5)
            picture.extend(k6)
            link.extend(k7)
        else :
            print("failure")
            errorset.append(1)
        
    else :
        print("failure")
        errorset.append(1)
    #判定收集数据项是否匹配，是否为空

testset2 = 0

def crawler_Tmall():
    browser.get("https:" + commenturl)
    time.sleep(2)
    newurl = str(browser.current_url) + "#J_Reviews"
    browser.get(newurl)

    num = pagenum + 1
    for ii in range(1,num):
        time.sleep(2)
        content = browser.page_source
        soup = BeautifulSoup(content,"html.parser")
        print(ii)
        content8 = soup.find_all(name = "div",attrs = "tm-rate-content")
        g8 = str(content8)
        k8 = re.findall('<div class="tm-rate-fulltxt">(.*?)</div>',g8)
        print(len(k8))
        global testset2

        if str(content8) == str(testset2) :
            break
        else :     
            comment.extend(k8)
            testset2 = content8
        
        try :
            search1 = browser.find_element_by_link_text('下一页>>')
            browser.execute_script('arguments[0].click()',search1)
        except :
            if ii == 1 :
                print("评论仅有单页")
            else :
                print("已到最后一页")

testset1 = 0

def crawler_Taobao():
    browser.get("https:" + commenturl)
    time.sleep(2)
    search2 = browser.find_element_by_link_text('评  价')
    browser.execute_script('arguments[0].scrollIntoView()',search2)
    search2.send_keys(Keys.ENTER)

    num = pagenum + 1
    for iii in range(1,num):
        time.sleep(2)
        content = browser.page_source
        soup = BeautifulSoup(content,"html.parser")
        print(iii)
        content9 = soup.find_all(name = "div",attrs = "J_KgRate_ReviewContent tb-tbcr-content")
        g9 = str(content9)
        g9a = g9.replace("\n","")
        g9b = g9a.replace(" ","")
        k9 = re.findall('tb-tbcr-content">(.*?)</div>',g9b)
        print(len(k9))
        global testset1

        if str(content9) == str(testset1) :
            break
        else :     
            comment.extend(k9)
            testset1 = content9

        try :
            search3 = browser.find_element_by_class_name('pg-next')
            browser.execute_script('arguments[0].scrollIntoView()',search3)
            browser.execute_script('arguments[0].click()',search3)
        except :
            if iii == 1 :
                print("评论仅有单页")
                break
            else :
                print("未知错误")

        
page_url1 = url + "0"
browser.get(page_url1)
time.sleep(scantime) #第一次爬取需扫码登录
crawler()


for i in range(1,pn):
    
    page_url = url + str(i*44)

    x = random.randint(1,3)
    y = random.randint(1,9)
    time.sleep(x + 0.1*y) #设置随机休眠时间
    browser.get(page_url)
    crawler()


if len(errorset) > (pn*0.8) :
    print("please retry") #设置容错
else : print("success")


W = pandas.Series(product)
F = pandas.Series(price)
S = pandas.Series(sales)
X = pandas.Series(seller)
Q = pandas.Series(location)
G = pandas.Series(picture)
K = pandas.Series(link)
data = pandas.DataFrame({"产品": W,"价格":F,"销量": S,"商铺":X,"区域":Q,"图片":G,"产品链接":K})
print(data)
data.to_csv("TaoBao价格统计.csv",encoding="utf-8")    


for urlll in link :
    commenturl = str(urlll)
    keyworld1 = "click.simba.taobao"

    if keyworld1 in commenturl :
        print("ignore the advertisment")

    else :
        
        keyworld2 = "detail.tmall.com"
        if keyworld2 in commenturl :
            try :
                crawler_Tmall()
            except :
                print("未知错误")
        else :
            try :
                crawler_Taobao()
            except :
                print("未知错误")

    
CC = pandas.Series(comment)
data1 = pandas.DataFrame({"产品评价": CC})
print(data1)
data1.to_csv("TaoBao评论.csv",encoding="utf-8")     


