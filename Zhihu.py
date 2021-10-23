import requests
import re
import os
import time
import json


def filter_content(text,limit=20):
    # 从响应数据中提取
    ret=[]
    jsonobj = json.loads(text)
    limit=len(jsonobj['data'])
    for i in range(0,limit):
        answer = jsonobj['data'][i]['content']
        # 设置正则过滤<p></p>标签
        res_tr = r'<p>(.*?)</p>'
        result =  re.findall(res_tr,answer,re.S|re.M)
        if(len(answer)==0):
            continue
        else:
            string=''.join((str(a) for a in result))
            ret.append(string)
            # print(string)
    return ret




class spider():
    def menu(self):
        print("菜单")
        print("1. 爬取回答并保存在本地")
        print("2. 关键词分析")
        print("3. 可视化词云绘制")
        print("4. 高级选项")

    def crawl(self,id,offset,limit=20):
        # 爬取信息，默认为20条
        # offset表示当前回答是第几个回答,limit表示一次获取的回答数量
        headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0"}
        url = "https://www.zhihu.com/api/v4/questions/{}/answers?include=content&limit={}&offset={}&platform=desktop&sort_by=default".format(id, limit,offset)
        res = requests.get(url,headers=headers)
        if res.status_code!=200:
            print("Status not right! Check your network")
            return;
        res.encoding = 'utf-8'
        return res.text

    
    def get_Answers(self,questionID,path):
        # 对crawl的一个封装，获取所有answer并保存在本地
        answer_array=[]
        for m in range(20):
            for offset in range(m*20,m*20+20):
                text = self.crawl(id=questionID,offset=offset)
                text=filter_content(text)
            # 写完20个内容就写入文件
            fout=open(path+"answer"+str(questionID)+".txt","a+",encoding="utf-8")
            for i in range(len(text)):
                fout.write("\n\n"+str(text[i]))
            fout.close()




class keywordAnalysis():





    
if __name__ == "__main__":
    # 文件保存路径
    path="F:\\2021summerImmunedroid\\pjfor\\"
    sp=spider()
    sp.get_Answers(67053079,path)

