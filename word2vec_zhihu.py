import json
import jieba
from gensim.models import Word2Vec
from gensim import models
from gensim.models.word2vec import LineSentence
from sklearn.decomposition import PCA
from matplotlib import pyplot

infile='E:\\ZhuhuPJ2\\timeresult.json'
infile2='E:\\ZhuhuPJ2\\test.json'
part = 'E:\\ZhuhuPJ2\\part_word_result.txt'
answer_path = "E:\\ZhuhuPJ2\\pure_answers.txt"
model_path = "E:\\ZhuhuPJ2\\answers.model"
model_path2 = "E:\\ZhuhuPJ2\\answers_smallWindow.model"

def loadDatadet(infile,part_file):
    f=open(infile,'r',encoding = "utf-8")
    sourceInLine=f.readlines()
    dataset=[]
    for line in sourceInLine:
        if(line == "\n"):
            continue
        line = line.replace('[',"")
        line = line.replace(']',"")
        line = line.replace("\'",'\"')
        temp1=line.strip('\n')
        temp1 = temp1.strip(",")
        temp2=temp1.split('\t')
        if(len(temp2)>2000):
            tmp2 = temp2[0:2000]
        dataset.append(temp2)
        fp = open(part_file,"a+",encoding = "utf-8")
        ansinfo = json.loads(temp2[0])
        seg_list = jieba.cut(ansinfo['answer'])
        fp.write(" ".join(seg_list))
        fp.close()
    return dataset



def handle_json(js_list,part_file):
    for item in js_list:
        fp = open(part_file,"a+",encoding = "utf-8")
        ansinfo = json.loads(item[0])
        seg_list = jieba.cut(ansinfo['answer'])
        fp.write(" ".join(seg_list))
        fp.close()
        
            # 这里得到了每一个回答的content
            # print(ansinfo['answer'])



def get_part(ans_path,part_path):
    with open(ans_path,encoding = "utf-8") as fp:
        lines = fp.readlines()
        for line in lines:
            seg_list = jieba.cut(line)
            with open(part_path,"a",encoding = "utf-8") as ff:
                ff.write(" ".join(seg_list))
        print("分词完成")


def get_similar(path):
    data = open(path,"rb")
    # model = Word2Vec(LineSentence(data),sg=1,vector_size=100,window=10, min_count=5, workers=15,sample=1e-3)
    # model.save(model_path)
    model =Word2Vec.load(model_path)
    print("训练完成")
    for e in model.wv.most_similar(negative=['元宇宙'],topn=100):
        print(e[0],e[1])

def get_visualization(path):
    # 版本不对 暂时无法完成
    # 参考链接 https://blog.csdn.net/qy20115549/article/details/86316974
    data = open(path,"rb")
    # model = Word2Vec(LineSentence(data),window=5,min_count=1)
    # model.save(model_path2)
    model =Word2Vec.load(model_path)
    X=model.key_to_index
    pca = PCA(n_components=2)
    result = pca.fit_transform(X)
    # 可视化
    pyplot.scatter(result[:,0],result[:,1])
    words = list(model.wv.vocab)
    for i, word in enumerate(words):
        pyplot.annotate(word,xy=(result[i,0],result[i,1]))
    pyplot.show()



if __name__ == "__main__":
    jieba.load_userdict(r"E:\\ZhuhuPJ2\\dict.txt")
    # js_list=loadDatadet(infile2,part)
    # get_part(answer_path,part)
    get_similar(part)
    # get_visualization(part)

