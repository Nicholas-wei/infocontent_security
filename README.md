# infocontent_security
信息系统安全的课程PJ👦🧑👨
报告：https://shimo.im/docs/rccpy6jd8wdvwPCW
## 11.21
目前完成的
`zhihu.py`爬取一个话题下面的所有问题，文章，并借着爬取问题下面的所有回答。
`bilibili.py`爬取b站视频下的评论。但是注意需要先获取av号。这个是用在线bv->av转换网址https://fripside.cn/BvToAv.php即可
## 11.24
更新zhihu.py中爬取时间的方法。重命名为zhihu_time.py因为对原先代码做了一些改动。可以输出JSON数据包到本地。包含回答、文章的url和最后一次更新时间。

## 11.25
`NLP_analysis.py` 使用 `snownlp` 库将所有从知乎抓取到的文本按照逗号切分，并且分析语句的感情特征，最后统计每个文件的综合情感值，并记录正面情绪和负面情绪的语句数。

## 11.26
`HOT_analysis.py` 将时间统计为日，周，月信息，代码不够优雅，尚待更进一步的优化和分析（图形化等）。修改 `zhishutime.py` ，使其输出包含热度时间的 `json` 文件。

## 11.27
更新`zhihu.py`修改了会重复爬取回答的问题逻辑。现在爬取的结果量会小很多。新增每个回答的`创建时间`,`更新时间`,`回答者性别`(1代表男性，0代表女性，-1代表女博士(doge))`
除此之外，更新过滤逻辑，过滤更多html编码，过滤文件名使得文件名合法。

## 11.30
更新`data`下面的数据文件</br>
新增`word2vec_zhihu.py`分析知乎回答数据，结果输出新词、相关度高词toplist,相关度低词toplist

## 12.01
更新了 `newNLP.py` 文件，利用 `jieba` `Counter` 实现分词性的（n,v,a）词频统计分析。
由于元宇宙的情感分析客观读不佳，将 `NLP_analysis.py` 改用为分析  `bilibili` 数据的情感态度。
