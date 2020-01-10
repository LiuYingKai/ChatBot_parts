# ChatBot-
可以添加在聊天系统里的组件, 包含功能有星座(运势, 财运, 今日, 明日, 本周, 本月),  怼人, 新闻功能
model.py运行文件
news_part.py 微博新闻处理方法
question_classifier.py问题分类模型(星座,新闻,脏话,攻击语句)
weibo.py 通过TF-IDF计算每条微博新闻的关键词

先运行weibo.py通过TF-IDF生成weibo新闻语料的关键词文件
再运行model.py进行运行

代码逻辑待优化, 本来是作为一个小组件存在的. 还存在很多不足, 希望大家多多提供宝贵意见
