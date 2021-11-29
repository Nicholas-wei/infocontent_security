import os
from snownlp import SnowNLP
import time
import jieba
import jieba.posseg as pseg
from collections import Counter
# 性别1是男，-1是女，这个也可以搞一个图出来

class data:
    createtime = 0
    enduptime = 0
    data = ""


data_path = "D:\\data_analysis\\11.27"
NLPd_path = "D:\\data_analysis\\zhihuPJanalysis\\"


def check_answer(file):
    f = open(file,'r',encoding='UTF-8')
    s = f.readline()
    if s[0] == '$':
        return True
    else:
        return False


def check_meta(string):
    if string.find("元宇宙") == -1 and string.find("Meta") == -1 and string.find("meta") == -1:
        return False
    else:
        return True


def get_all_file(data_path):
    dirs = os.listdir(data_path)
    files = []
    for dir in dirs:
        file = data_path + "\\" + str(dir)
        files.append(file)
    return files


def snowNLP_analysis(files):
    answers = []
    articles = []
    for file in files:
        if check_answer(file):
            openf = open(file, 'r', encoding='UTF-8')
            raw_data = openf.readlines()
            i = 0
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
            articles.append({'title':file,'article':openf.readlines()})
    answers = sorted(answers,key=lambda tm:(tm['create time']))

    outputf = open(NLPd_path + 'result.json','w',encoding='UTF-8')
    outputf.write('[')
    for i in range(0,len(answers)):
        outputf.write(answers[i].__str__())
        if i != len(answers)-1:
            outputf.write(',\n')
    outputf.write(']')
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

    outputf = open(NLPd_path + 'jieba.txt','w',encoding='UTF-8')
    jieba_data = []
    jieba.load_userdict("D:\\data_analysis\\zhihuPJanalysis\\jiebadata.txt")
    stoplist= ['',',','，','。','.','#','!','~','%','^','&','*',' ','、','\'','’','"','@']
    for answer in answers:
        jieba_data.append(answer['answer'])
    for article in articles:
        jieba_data.append(article['article'])

    cut_data = []
    n_data = []
    for data in jieba_data:
        rawdata = jieba.lcut(str(data)).__str__()
        splitdata = pseg.cut(str(data))
        for word,flag in splitdata:
            if  flag[0] == 'n':
                n_data.append(word)
        for word in rawdata:
            if word not in stoplist:
                cut_data.append(word)
                outputf.write(word.__str__() + ' ')
    cutwords = dict(Counter(n_data))
    outputwords_sorted = sorted(cutwords.items(), key= lambda x : x[1], reverse=True)[:100]
    print(outputwords_sorted)



if __name__ == "__main__":
    files = get_all_file(data_path)
    snowNLP_analysis(files)
