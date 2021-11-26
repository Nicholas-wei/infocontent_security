# infocontent_security
信息系统安全的课程PJ
:)
## 11.21
目前完成的
`zhihu.py`爬取一个话题下面的所有问题，文章，并借着爬取问题下面的所有回答。
`bilibili.py`爬取b站视频下的评论。但是注意需要先获取av号。这个是用在线bv->av转换网址https://fripside.cn/BvToAv.php即可
## 11.24
更新zhihu.py中爬取时间的方法。重命名为zhihu_time.py因为对原先代码做了一些改动。可以输出JSON数据包到本地。包含回答、文章的url和最后一次更新时间。

## 11.25
`NLP_analysis.py` 使用 `snownlp` 库将所有从知乎抓取到的文本按照逗号切分，并且分析语句的感情特征，最后统计每个文件的综合情感值，并记录正面情绪和负面情绪的语句数。

## 11.26
`HOT_analysis.py` 将时间统计为日，周，月信息，尚待更进一步的分析（图形化等）。
