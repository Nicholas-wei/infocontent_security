import requests
import re
import os
import time
import json
from pyquery import PyQuery as pq



store_path = "E:\\zhihuPJ\\"





def filter_content(text,limit=20):
    # 从响应数据中提取
    ret=[]
    jsonobj = json.loads(text)
    limit=len(jsonobj['data'])
    for i in range(0,limit):
        answer = jsonobj['data'][i]['content']
        # 设置正则过滤<p></p>标签
        res_tr = r'<p data-pid="........">(.*?)</p>'
        result =  re.findall(res_tr,answer,re.S|re.M)
        if(len(answer)==0):
            continue
        else:
            string=''.join((str(a) for a in result))
            ret.append(string)
            # print(string)
    return ret



class questionDetail():
    # 问题号
    qid=0
    # 问题发起时间
    q_createTime=0
    # 问题名称
    q_title=""


class answerDetail():
    create_time = 0
    voteup_count = 0
    content = ""
    name = ""


class articalDetail():
    # 文章发起时间
    art_create_time = 0
    # 文章名称
    art_title = ""
    # 文章赞同数量
    voteup_cnt = 0
    # 评论数量
    connent_cnt = 0
    # 作者名称
    name = ""
    # 文章编号
    id = 0



class filter_struct():
    name = ""
    index = 0



global question_id # 用于存放话题下所有问题编号
question_id = [questionDetail()]
global artical_id #用于存放所有文章编号
artical_id = [articalDetail()]
global filtercase
filtercase = [filter_struct()]



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


    def get_topic_text(self,url):
        # 获取话题下面的所有问题的问题号
        # url = 'https://www.zhihu.com/api/v4/topics/'+str(id)+'/feeds/top_activity?include=data%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Danswer%29%5D.target.content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Danswer%29%5D.target.is_normal%2Ccomment_count%2Cvoteup_count%2Ccontent%2Crelevant_info%2Cexcerpt.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Darticle%29%5D.target.content%2Cvoteup_count%2Ccomment_count%2Cvoting%2Cauthor.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Dpeople%29%5D.target.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.annotation_detail%2Ccontent%2Chermes_label%2Cis_labeled%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Canswer_type%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.paid_info%3Bdata%5B%3F%28target.type%3Darticle%29%5D.target.annotation_detail%2Ccontent%2Chermes_label%2Cis_labeled%2Cauthor.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dquestion%29%5D.target.annotation_detail%2Ccomment_count%3B&limit=10&after_id=0'
        headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        }
        res = requests.get(url,headers = headers)
        res.encoding = 'Unicode'
        return res.text

    def handle_topic_text(self,text):
        json_data = json.loads(text)
        lst = json_data['data']
        nextUrl = json_data['paging']['next']
        if not lst:
            return
        for item in lst:
            type = item['target']['type']
        
            if type == 'answer':
                # 问题
                question = item['target']['question']
                ctime = item['target']['created_time']
                id = question['id']
                title = question['title']
                tmp = questionDetail()
                tmp.q_createTime = ctime
                tmp.q_title = title
                tmp.qid = id
                question_id.append(tmp)
                
            elif type == 'article':
                #文章
                zhuanlan = item['target']
                id = zhuanlan['id']
                title = zhuanlan['title']
                url = zhuanlan['url']
                vote = zhuanlan['voteup_count']
                cmts = zhuanlan['comment_count']
                auth = zhuanlan['author']['name']
                create_time = zhuanlan['created']
                # print("专栏：",id,title)
                tmp = articalDetail()
                tmp.art_create_time = create_time
                tmp.connent_cnt = cmts
                tmp.art_title = title
                tmp.name = auth
                tmp.id = id
                artical_id.append(tmp)


            elif type == 'question':
                # 问题
                question = item['target']
                id = question['id']
                title = question['title']
                auth = zhuanlan['author']['name']
                url = 'https://www.zhihu.com/question/' + str(id)
                # print("问题：",id,title)
                tmp = questionDetail()
                tmp.q_createTime = ctime
                tmp.q_title = title
                tmp.qid = id
                question_id.append(tmp)

        return nextUrl
    

    def get_artical(self,id):
        headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        }
        url = "https://zhuanlan.zhihu.com/p/" + str(id)
        res = requests.get(url,headers = headers).text
        # 由于artical传送时通过html传输，使用pyquery解析数据
        doc = pq(res)
        artical = doc(".Post-RichTextContainer").items()
        content = ""
        for x in artical:
            content += x.text()
        a = open(store_path+"temp.txt","w",encoding = "utf-8")
        a.write(content)
        a.close()
        content = ""
        a = open(store_path+"temp.txt","r",encoding = "utf-8")
        lines = a.readlines()
        for line in lines:
            if('css' in line):
                continue
            content+=line
        a.close()
        os.system("rm "+store_path+"temp.txt")
        return content
        


    def question_filter(self,a):
        tmp_case = []
        filter_index = []
        result = [] # 去除重复之后的数组
        for i in range(0,len(a)):
            if a[i].q_title not in tmp_case:
                tmp_case.append(a[i].q_title)
            else:
                filter_index.append(i)

        for i in range(0,len(a)):
            if(i in filter_index):
                continue
            result.append(a[i])
        return result




    def main_crawl(self,id):
        # 获取话题号id下面的所有内容,主爬虫函数
        times = 0   # 表示获取爬虫下面的多少页内容。一般一页内容包含10个问题或者文章或者回答
        url = "https://www.zhihu.com/api/v4/topics/21753891/feeds/top_activity?include=data%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Danswer%29%5D.target.content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Danswer%29%5D.target.is_normal%2Ccomment_count%2Cvoteup_count%2Ccontent%2Crelevant_info%2Cexcerpt.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Darticle%29%5D.target.content%2Cvoteup_count%2Ccomment_count%2Cvoting%2Cauthor.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Dpeople%29%5D.target.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.annotation_detail%2Ccontent%2Chermes_label%2Cis_labeled%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Canswer_type%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.paid_info%3Bdata%5B%3F%28target.type%3Darticle%29%5D.target.annotation_detail%2Ccontent%2Chermes_label%2Cis_labeled%2Cauthor.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dquestion%29%5D.target.annotation_detail%2Ccomment_count%3B&limit=10&after_id=0"
        for times in range(0,5):
            text = self.get_topic_text(url)
            url = self.handle_topic_text(text)
        
        # 如果问题重复了，需要筛选一下。文章则不需要
        tmp_case = []
        filter_index = []
        result = [] # 去除重复之后的数组
        global question_id
        global artical_id
        for i in range(0,len(question_id)):
            if question_id[i].q_title not in tmp_case:
                tmp_case.append(question_id[i].q_title)
            else:
                filter_index.append(i)

        for i in range(0,len(question_id)):
            if(i in filter_index):
                continue
            result.append(question_id[i])
        question_id = result

        # 写入文件——基本想法是产生以下文件
        # 1. 每个问题标题以及下面的回答。每个问题生成一个文件（不在此函数中）
        # 2. 所有文章标题+所有问题标题
        # 3. 所有回答和所有文章整合成一个txt

        # part1,part of part3
        
        #everything = open(store_path + "all.txt","a+",encoding = "utf-8")
        #for item in question_id:
        #    if(item.qid==0):
        #        continue
        #    name = item.q_title.replace("？","")
        #    filename = store_path + str(name) + ".txt"
            
        #    self.get_Answers(item.qid,filename,item.q_title)
        #    # 写入everything文件
        #    question = open(filename,"r",encoding = "utf-8")
        #    content = question.readlines()
        #    for _ in content:
        #        everything.write(_+"\n")
        #everything.close()
        


        # part2
        file_title = open(store_path+"titles","w+",encoding = "utf-8")
        for itemq in question_id:
            file_title.write(itemq.q_title+'\n')
        for itema in artical_id:
            file_title.write(itema.art_title+'\n')
        file_title.close()

        # part3, write artical
        everything = open(store_path + "all.txt","a+",encoding = "utf-8")
        for itema in artical_id:
            content = self.get_artical(itema.id)
            everything.write(content)
            everything.close()





    def filter_search_questions(self,text):
        # 得到每个问题的具体信息。主要是可以获得到一个消息的网页代码
        search_result=[]
        jsonobj=json.loads(text)
        for obj in jsonobj['data']:
            if obj['type'] == "search_result":
                tmp_keywordResult = SearchKetwordResult()
                question_url=obj["object"]["url"]
                print ("url found: " + tmp_keywordResult.q_url)
                headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0","x-ab-param":"zr_slotpaidexp=1;pf_adjust=1;tp_dingyue_video=0;se_ffzx_jushen1=0;tp_zrec=1;top_test_4_liguangyi=1;qap_question_visitor= 0;tp_topic_style=0;zr_expslotpaid=1;qap_question_author=0;tp_contents=1;pf_noti_entry_num=2","x-ab-pb":"CsYBMgMKBOAEjQQyBbEF1wu0AMoCEQXYAlcDjATYBfQLjAXjBdwL1gQZBUMFVQV/BYwCEgUBCwcMOwLnBbULPwDBBFIFDwsqA88L8wMLBA4FfQI3DIkMNATRBCkFogP4A54F9AM0DIQCnwK3A1cEoANkBDcFwgVDAEABxwKbC9oE9gV0AVYFgAWmBLIFtApSCxQFzAJPA3IDoQNqAVADaQFFBDMFYAvkChUF6QRWDEcAuQL2AnUEUQWLBewK4AtCBOMEGwDXAjMEEmMAAQAEAAEAAAAAAAABAQAAAAAAAAAAAAAAAAEAAAMAAQABAQsAAAABAQAABQABAQEAAAABAAEAAQABFQEAAgECAAABAAAAAQIAAAEAAAABAAAAAAIBAQAVAAABAAEAAgIAAAA=","x-zse-93":"101_3_2.0","x-zse-96":"2.0_a_x0bi9BHhtYQ7F0zqF8r69BkHFxcMY8Z9N0bHH0FhNx"}
                res=requests.get(question_url,headers=headers)
                jsonobj_q=json.load(res.text)
                tmp_keywordResult.q_title=jsonobj_q["question"]["title"]
                tmp_keywordResult.q_createTime=jsonobj_q["question"]["created"]
                tmp_keywordResult.qid=jsonobj_q["question"]["id"]
                tmp_keywordResult.askergender = jsonobj_q["author"]["gender"]
                tmp_keywordResult.askerinfoURL=jsonobj_q["author"]["url"]
                

    
    def get_Search(self,keyword,path):
        text = self.search_questions(keyword,0,20)
        if text == -1:
            return -1
        text=self.filter_search_questions(text)




    def get_Answers(self,questionID,path,question_title):
        # 对crawl的一个封装，获取所有answer并保存在本地
        # answer_array=[]
        for m in range(20):
            for offset in range(m*20,m*20+20):
                text = self.crawl(id=questionID,offset=offset)
                text=filter_content(text)
            # 写完20个内容就写入文件
                fout=open(path,"a+",encoding="utf-8")
                for i in range(len(text)):
                    tmp_text = str(text[i]).replace("<b>"," ")
                    tmp_text = tmp_text.replace("<a>","")
                    tmp_text = tmp_text.replace("</a>"," ")
                    tmp_text = tmp_text.replace("</b>","")
                    tmp_text = tmp_text.replace("<br>"," ")
                    tmp_text = tmp_text.replace("</br>"," ")
                    fout.write("\n\n"+str(tmp_text))
                fout.close()
            print("问题{}写入完成"%question_id)









    
if __name__ == "__main__":

    
    # 文件保存路径
    sp=spider()
    # 测试爬取信息内容
    # sp.get_Answers(500003760,store_path)

    # 测试爬取artical 内容
    # content = sp.get_artical(362459067)
    # print(content)


    # 测试总爬取
    topic_id = 21753891
    sp.main_crawl(id)

