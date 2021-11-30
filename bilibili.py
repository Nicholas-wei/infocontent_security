import requests
import os
from pyquery import PyQuery as pq
from bs4 import BeautifulSoup

header = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0",
		  "Cookie": ""}
comments = []
original_url = "https://api.bilibili.com/x/v2/reply?jsonp=jsonp&type=1&oid=891728781&sort=2&pn="

path = "E:\\biliPJ\\"

class videoDetails():
    # 视屏名称
    name = ""
    # bv号
    bv_numver = 0

global videos
videos = [videoDetails()]


class spider_bili():
    def getBVindex(self):
        url = "https://search.bilibili.com/all?keyword=元宇宙"
        res = requests.get(url,headers = header).text
        doc = pq(res)
        page_object = doc(".mixin-list").items()
        content = ""
        for x in page_object:
            content+=x.text()
        
    def getReview(self,path,original_url,id):
        comments.clear()
        file = open(path+str(id)+".txt","w+",encoding = "utf-8")
        for page in range(0,50):
            url = original_url + str(page)
            print(url)
            html = requests.get(url, headers=header)
            data = html.json()
            if data['data']['replies']:
                for _ in data['data']['replies']:
                    comments.append(_['content']['message'])        
                for item in comments:
                    # print(item)
                    file.write(str(item)+'\n')
                    # os.system("pause")
                print("page%d完成写入"%page)
                comments.clear()
        file.close()




if __name__ == "__main__":
    oid = [762837053,891728781,676369398,549002191,806502431,717037354,891208937,251819416,676856817]
    sp = spider_bili()
    
    store_path = path
    for i in range(4,9):
        my_oid = oid[i]
        original_url = "https://api.bilibili.com/x/v2/reply?jsonp=jsonp&type=1&oid="+str(my_oid)+"&sort=2&pn="
        sp.getReview(store_path,original_url,my_oid)
        print("完成%d",i)