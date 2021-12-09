import json
import jieba
from collections import Counter
from jieba import posseg as pseg

path = "E:\\ZhuhuPJ2\\timeresult.json"


outfile = "E:\\ZhuhuPJ2\\timeresult_replace.json"
out_man_content = "E:\\ZhuhuPJ2\\men_content.txt"
out_women_content = "E:\\ZhuhuPJ2\\women_content.txt"
num_path = "E:\\ZhuhuPJ2\\"

# out = open(outfile,"w",encoding ="utf-8")

#with open(path,"r",encoding = "utf-8") as f:
#    cnt = 0
#    lines = f.readlines()
#    for line in lines:
#        line = lines[cnt]
#        line = line.replace("\'","\"")
#        out.write(line)
#        print(cnt)
#        cnt = cnt+1
#f.close()
#out.close()

global man
man = 0
global women
women = 0



def generate_gendercnt():
    men_file = open(out_man_content,"w",encoding = "utf-8")
    women_file = open(out_women_content,"w",encoding = "utf-8")
    with open(outfile,encoding= "utf-8") as f:
        result = json.load(f)
        for item in result:
            detail = dict(item)
            if(detail["sexuality"] == "man"):
                global man
                man = man+1
                men_file.write(detail["answer"])
            else:
                global women
                women = women+1
                women_file.write(detail["answer"])
    men_file.close()
    women_file.close()




def cut(datas):
    n_data = []
    v_data = []
    a_data = []
    rawdata = jieba.lcut(str(datas))
    splitdata = pseg.cut(str(datas))
    for word,flag in splitdata:
        if flag[0] == 'n':
            n_data.append(word)
        if flag[0] == 'v':
            v_data.append(word)
        if flag[0] == 'a':
            a_data.append(word)
    return n_data,v_data,a_data


def word_num(data,flag):
    cutwords = dict(Counter(data))
    outputwords_sorted = sorted(cutwords.items(), key= lambda x : x[1], reverse=True)[:50]
    f = open(num_path + str(flag) + 'num_adj.txt','w',encoding='UTF-8')
    for t1,t2 in outputwords_sorted:
        f.write(str(t1) + " " + str(t2) + "\n")



def content_analyze(file_path,flag):
    jieba.load_userdict(r"E:\\ZhuhuPJ2\\dict.txt")
    men_file = open(file_path,"r",encoding = "utf-8")
    file_content = men_file.read()
    n = []
    v = []
    a = []
    n,v,a = cut(file_content)
    word_num(a,flag)

if __name__ == "__main__":
    generate_gendercnt()
    print(man,women)
    # content_analyze(out_women_content,"women")

