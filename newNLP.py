import os
from snownlp import SnowNLP
import time
import jieba
import jieba.posseg as pseg
from collections import Counter
import re
# 性别1是男，-1是女，这个也可以搞一个图出来

class data:
    createtime = 0
    enduptime = 0
    data = ""


data_path = "D:\\data_analysis\\11.27"
NLPd_path = "D:\\data_analysis\\zhihuPJanalysis\\"
TIME_path = "D:\\data_analysis\\zhihuPJanalysis\\time\\"
stoplist= ['',',','，','。','.','#','!','~','%','^','&','*',' ','、','\'','’','"','@']
# 检查是否为回答，不是则是文章
def check_answer(file):
    f = open(file,'r',encoding='UTF-8')
    s = f.readline()
    if s[0] == '$':
        return True
    else:
        return False

# 检查是否是元宇宙相关
def check_meta(string):
    if string.find("元宇宙") == -1 and string.find("Meta") == -1 and string.find("meta") == -1:
        return False
    else:
        return True


# 获取所有文件名
def get_all_file(data_path):
    dirs = os.listdir(data_path)
    files = []
    for dir in dirs:
        file = data_path + "\\" + str(dir)
        files.append(file)
    return files


# 获取所有文件数据
def get_data(file,answers,articles):
    openf = open(file, 'r', encoding='UTF-8')
    raw_data = openf.readlines()
    i = 0
    if check_answer(file):
        while i < len(raw_data):
            if raw_data[i][0] == '$':
                if check_meta(raw_data[i+4]):
                    createtime = raw_data[i][1:-1].strip()
                    enduptime = raw_data[i+1].strip()
                    sexuality = raw_data[i+2].strip()
                    linkdata  = raw_data[i+3].strip()
                    string    = raw_data[i+4].strip()
                    answers.append({'create time':createtime, 'endup time':enduptime,'sexuality':sexuality,'link':linkdata,'answer':string})
                    i += 5
                else:
                    i += 1
            else:
                i += 1
    else:
        article = {'title':file,'article':openf.readlines()}
        articles.append(article)


# 输出和时间（创建和更新），性别，网址绑定的回答 Json 文件
def time_answers(answers):
    for answer in answers:
        answer['create time'] = time.ctime(int(answer['create time']))
        answer['endup time'] = time.ctime(int(answer['endup time']))
        if answer['sexuality'] == '1':
            answer['sexuality'] = 'man'
        else:
            answer['sexuality'] = 'woman'

    outputf = open(NLPd_path + 'timeresult.json','w',encoding='UTF-8')
    outputf.write('[')
    for i in range(0,len(answers)):
        outputf.write(answers[i].__str__())
        if i != len(answers)-1:
            outputf.write(',\n\n')
    outputf.write(']')


# 切词，用 jieba 进行词性切分
def cut(answers,articles):
    outputf = open(NLPd_path + 'jieba.txt','w',encoding='UTF-8')
    jieba_data = []
    for answer in answers:
        jieba_data.append(answer['answer'])
    for article in articles:
        jieba_data.append(article['article'])
    cut_data = []
    n_data = []
    v_data = []
    a_data = []
    for data in jieba_data:
        rawdata = jieba.lcut(str(data))
        splitdata = pseg.cut(str(data))
        for word,flag in splitdata:
            if flag[0] == 'n':
                n_data.append(word)
            if flag[0] == 'v':
                v_data.append(word)
            if flag[0] == 'a':
                a_data.append(word)
        for word in rawdata:
            if word not in stoplist:
                cut_data.append(word)
                outputf.write(word.__str__() + ' ')
    return cut_data,n_data,v_data,a_data


# 用 Counter 进行词性的词频统计
def word_num(data,flag):
    cutwords = dict(Counter(data))
    outputwords_sorted = sorted(cutwords.items(), key= lambda x : x[1], reverse=True)[:500]
    f = open(TIME_path + str(flag) + '_num.txt','w',encoding='UTF-8')
    f.write(outputwords_sorted.__str__())


# 用 Counter 进行词性的词频统计
def word_num_2(datas):
    f = open(TIME_path + 'time_num.txt','w',encoding='UTF-8')
    for data in datas:
        cutwords = dict(Counter(data['answer']))
        outputwords_sorted = sorted(cutwords.items(), key= lambda x : x[1], reverse=True)[:500]
        f.write(data['time'].__str__())
        f.write(outputwords_sorted.__str__())
        f.write('\n')


def HOT_analysis(answers):
    dates = []
    for answer in answers:
        dates.append(re.split(r' +',time.ctime(int(answer['create time']))))
        num = 0
    datas = []
    i = 0
    j = 0
    while i<len(answers):
        tmp = []
        while j < len(answers):
            if dates[i][0] == dates[j][0] and dates[i][1] == dates[j][1]:
                splitdata = pseg.cut(answers[j]['answer'])
                for word,flag in splitdata:
                    if flag[0] == 'n':
                        tmp.append(word)
                j += 1
            else:
                datas.append({'time':dates[i],'answer':tmp})
                i = j
                break
        if(j == len(answers)):
            break
    word_num_2(datas)



# 主要处理函数，用到了上面的所有辅助函数
def snowNLP_analysis(files):
    answers = []
    articles = []
    for file in files:
        get_data(file,answers,articles)

    answers = sorted(answers,key=lambda tm:(tm['create time']))

    HOT_analysis(answers)
    #time_answers(answers)

    #cut_data,n_data,v_data,a_data = cut(answers,articles)
    #word_num(cut_data,'all')
    #word_num(n_data,'n')
    #word_num(v_data,'v')
    #word_num(a_data,'a')


if __name__ == "__main__":
    jieba.load_userdict("D:\\data_analysis\\zhihuPJanalysis\\jiebadata.txt")
    files = get_all_file(data_path)
    snowNLP_analysis(files)
