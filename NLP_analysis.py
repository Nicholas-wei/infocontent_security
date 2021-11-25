import os
import jieba
from snownlp import SnowNLP

# Gensim？snowNLP？

path = "D:\\data_analysis\zhihuPJ"


def get_all_file(path):

    dirs = os.listdir(path)
    files = []
    for dir in dirs:
        file = path+ "\\" + str(dir)
        files.append(file)
    return files

#def cut_all_file(files):
cuted = []
files = get_all_file(path)
#for file in files:
    # f = open(file,"r",encoding='UTF-8')
    #cuted.append(jieba.lcut(f.read()))
    #print(file)

f = open(files[3],"r",encoding='UTF-8')
while True:
    line = f.readline()
    if not line:
        break
    lines = line.strip().split("，")
    for sentence in lines:
        NLPdata = SnowNLP(sentence)
        seg_words = ""
        for word in NLPdata.words:
            seg_words += "_"
            seg_words += word
        print(sentence + "\t" + seg_words + "\t" + str(NLPdata.sentiments) + "\n")

#for x in NLPdata.words:

#NLPdata = SnowNLP(data)
#print(NLPdata)
