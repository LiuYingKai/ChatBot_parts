import ahocorasick
import random
import os
import json
import ahocorasick
# class News_rec:
#     def __init__(self):
#         with open('./dict/weibo.json', 'r', encoding='utf-8') as fp:
#             data = json.load(fp)
#             self.data = data['RECORDS']
#         dirty_total = [i.strip() for i in open('dict/dirty.conv', encoding='utf-8') if i.strip()]
#         news_list = []
#         news_ner = []
#         for idx in range(len(data)):
#             path = 'tf_idf_result/' + f"{idx}_tfidf.conv"
#             ners = [i.strip() for i in open((path), encoding='utf-8') if i.strip()]
#             news_list.append(ners)
#             news_ner += ners
#         self.news_ners = set(news_ner)
#         # 构造actree
#         self.region_tree = self.build_actree(list(self.news_ners))
#
#     def news_rec(self):
#         news_idx = random.randint(0, (len(self.data) - 1))
#         con_idx = random.randint(1, 3)
#         news = self.data[news_idx]['leads']
#         content = self.data[news_idx][f'content{con_idx}']
#         leads_list = news
#         content_list = f'小七觉得{content}'
#         rec = leads_list + content_list
#         return rec
#
#     def build_actree(self,wordlist):
#         actree = ahocorasick.Automaton()
#         for index, word in enumerate(wordlist):
#             actree.add_word(word, (index, word))
#         actree.make_automaton()
#         return actree
#
#     def main():
#         '''
#         新闻模块主函数
#         :return:
#         '''




# def news_ner():
#     '''
# 	创建新闻的关键词列表,每个元素为该新闻关键词的list
# 	:return:
# 	'''
#     news_list = []
#     news_ner = []
#     for idx in range(len(data)):
#         path = 'tf_idf_result/' + f"{idx}_tfidf.conv"
#         ners = [i.strip() for i in open((path), encoding='utf-8') if i.strip()]
#         news_list.append(ners)
#         news_ner += ners
#     news_ner = set(news_ner)
#     return news_list, news_ner
with open('./dict/weibo.json', 'r', encoding='utf-8') as fp:
    data = json.load(fp)
    data = data['RECORDS']
dirty_total = [i.strip() for i in open('dict/dirty.conv', encoding='utf-8') if i.strip()]
news_list = []
news_ner = []
for idx in range(len(data)):
    path = 'tf_idf_result/' + f"{idx}_tfidf.conv"
    ners = [i.strip() for i in open((path), encoding='utf-8') if i.strip()]
    news_list.append(ners)
    news_ner += ners
news_ners = set(news_ner)
# 构造actree



def news_rec():
    news_idx = random.randint(0, (len(data) - 1))
    con_idx = random.randint(1, 3)
    news = data[news_idx]['leads']
    content = data[news_idx][f'content{con_idx}']
    leads_list = news
    content_list = f'小七觉得{content}'
    rec = leads_list + content_list
    return rec


def build_actree( wordlist):
    actree = ahocorasick.Automaton()
    for index, word in enumerate(wordlist):
        actree.add_word(word, (index, word))
    actree.make_automaton()
    return actree

region_tree = build_actree(list(news_ners))


def check_news(self, question):
    region_wds = []
    for i in self.region_tree.iter(question):  # i 的形状(index, (index, word))
        wd = i[1][1]  # word
        region_wds.append(wd)

def news_chack(idx):
    news_j = data[idx]
    # name = f'content{num}'
    news = news_j['leads']
    return news
