import os
from snownlp import SnowNLP


data_path = "D:\\data_analysis\zhihuPJ"
NLPd_path = "D:\\data_analysis\zhihuPJanalysis"


def get_all_file(data_path):
    dirs = os.listdir(data_path)
    files = []
    for dir in dirs:
        file = data_path + "\\" + str(dir)
        files.append(file)
    return files


def snowNLP_analysis(files):
    file_num = 0
    NLPfiles = []
    for file in files:
        rawf = open(file, "r", encoding='UTF-8')
        nlpf = NLPd_path + "\\" + str(file_num) + ".txt"
        NLPfiles.append(nlpf)
        dataf = open(nlpf, "w", encoding='UTF-8')
        file_num += 1
        while True:
            line = rawf.readline()
            if not line:
                break
            lines = line.strip().split("，")
            for sentence in lines:
                if sentence == '':
                    continue
                NLPdata = SnowNLP(sentence)
                seg_words = ""
                for word in NLPdata.words:
                    seg_words += "_"
                    seg_words += word
                dataf.write(sentence + "\t" + seg_words + "\t" + str(NLPdata.sentiments) + "\n")
        print(str(file_num) + "over！\n")
    return NLPfiles

def sentiment_analysis(NLPfiles):
    good = 0
    bad = 0
    average = 0.0
    n = 0
    for nlpfile in NLPfiles:
        rawf = open(nlpfile,"r",encoding='UTF-8')
        while True:
            line = rawf.readline()
            if not line:
                break
            n += 1
            lines = line.strip().split("\t")
            emotion_num = float(lines[-1])
            if emotion_num > 0.5:
                good += 1
            else:
                bad += 1
            average += emotion_num
        print(average/n)
        print("good:", good)
        print("bad:", bad)


if __name__ == "__main__":
    files = get_all_file(data_path)
    NLPfiles = snowNLP_analysis(files)
    sentiment_analysis(NLPfiles)
