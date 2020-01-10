# -*- coding: utf-8 -*-
from question_classifier import *
# todo 回怼数据库待完善
# todo 新闻模块
# todo -新闻模块流程
#        1,无新闻实体,返回推荐新闻(√)
#        2,存在新闻实体, 返回相似回答()
# todo 数据转入neo4j
print('测试功能块,现在功能有星座(简述,运势,财运,今日,明日,本周,本月),回怼功能, 新闻推送, 新闻回复 ')
while True:
    # a = '我想揍你'
    # a = '今日双子座'
    a = input('测试:')
    result = QuestionClassifier().classify(a)
    if result== None:
        result = QuestionClassifier().unknow_anwser()
    print("AI回复:", result)