# ChatBot-
可以添加在聊天系统里的组件, 包含功能有星座(运势, 财运, 今日, 明日, 本周, 本月),  怼人, 新闻功能
model.py运行文件
news_part.py 微博新闻处理方法
question_classifier.py问题分类模型(星座,新闻,脏话,攻击语句)
weibo.py 通过TF-IDF计算每条微博新闻的关键词

新闻功能是可以输入带有新闻的语句 直接随即返回一条新闻
如果输入中包含某一条新闻的关键词的话, 也会返回新闻. 可能是没有过滤停用词或当前新闻数据不适合使用TF-IDF,这一功能的覆盖面过大. 影响效果

先运行weibo.py通过TF-IDF生成weibo新闻语料的关键词文件
再运行model.py进行运行

代码逻辑待优化, 本来是作为一个小组件存在的. 还存在很多不足, 希望大家多多提供宝贵意见
返回False时转为自己的聊天机器人
![image](https://github.com/LiuYingKai/ChatBot_parts/blob/master/%E5%8C%B9%E9%85%8D%E6%A8%A1%E5%9D%97/1.png)
