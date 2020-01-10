# -*- coding: utf-8 -*-
# 星座财运
# 星座运势
# 星座描述
# 骚话回复
import ahocorasick
import random
import json
from news_part import *
import news_part
import os
import jiagu
class QuestionClassifier:
    def __init__(self):
        # cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        #　特征词路径
        # self.star_path = os.path.join(cur_dir, 'dict/star.txt')
        #todo 录取新闻json
        # with open('./dict/weibo.json', 'r', encoding='utf-8') as fp:
        #     data = json.load(fp)
        #     self.news_json_dict = data['RECORDS']
        self.dirty_total = [i.strip() for i in open('dict/dirty.conv', encoding='utf-8') if i.strip()]
        self.attack_total = [i.strip() for i in open('dict/attack.conv', encoding='utf-8') if i.strip()]
        self.joke_list = [i.strip() for i in open('dict/joke.conv',encoding='utf-8')if i.strip()]
        self.dirty_wds = []
        self.dirty_dict = {}
        self.news_dict = news_list
        self.news_ner = news_ners
        # self.news_dict , self.news_ner = news_ner()
        for i in range(0, len(self.dirty_total), 2):
            self.dirty_wds.append(self.dirty_total[i])
            self.dirty_dict[self.dirty_total[i]] = self.dirty_total[i + 1]
        self.attack_wds = []
        self.attack_dict = {}
        for i in range(0, len(self.attack_total), 2):
            self.attack_wds.append(self.attack_total[i])
            self.attack_dict[self.attack_total[i]] = self.attack_total[i + 1]
        self.star_wds = [i.strip() for i in open('dict/star.conv',encoding='utf-8') if i.strip()]
        # self.dirty_wds = [i.strip() for i in open('dict/dirty.conv',encoding='utf-8') if i.strip()]
        self.joke_wds = ['笑话', '讲笑话']
        self.news_wds = ['新闻']+ list(self.news_ner)
        self.region_words = set(self.star_wds + self.dirty_wds+self.joke_wds + self.attack_wds + self.news_wds )
        # 构造actree
        self.region_tree = self.build_actree(list(self.region_words))
        # 构建词典
        self.wdtype_dict = self.build_wdtype_dict()
        self.star_qws = ['运势', '运气', '运']
    def unknow_anwser(self):
        un_answer = ['主人你好像把我绕晕了', '等等,我还没反应过来', '聊聊我能听懂的事情吧']
        idx = random.randint(0,(len(un_answer)-1))
        return un_answer[idx]
    def build_actree(self, wordlist):
        actree = ahocorasick.Automaton()
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree

    '''问句过滤'''

    def check_rec(self, question):
        region_wds = []
        for i in self.region_tree.iter(question):  # i 的形状(index, (index, word))
            wd = i[1][1]  # word
            region_wds.append(wd)
            '''注释部分暂时不用, 多知识时再添加'''
        stop_wds = []
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1)
        final_wds = [i for i in region_wds if i not in stop_wds]
        final_dict = {i: self.wdtype_dict.get(i) for i in final_wds}

        return final_dict
        # return region_wds
    '''答案词典们, 以后考虑使用neo4j来代替'''
    star_fate_dict = {
        '白羊座':'白羊座的人会有深刻的想法和关键的改变，但是你们所有人都在期待一个难忘的2020年的开始。这仅仅是个开始——接受建议，对自己宽容一点',
        '金牛座':'一月不可预测的天王星在金牛座，预示着在2020年新的想法和内在的不安.如果你的工作需要谈话、写作、教学或说服他人，那么这些行星会支持你。只要记住，没有什么是容易的，所取得成就都是持久坚持的结果。',
        '双子座':'对双子座来说，处理任何与家庭、项目、计划有关的事情都不是一件容易的事情——他们要求苛刻，工作缓慢，需要耐心。这个月你不能突破界限或象征性的封印，但你可以为自己和你爱的人建立更安全的东西。',
        '巨蟹座':'巨蟹座1月的月食会激发你最深的情感和激动的精神感觉。你可以调到任何你想要的，如果你正在学习，探索新的想法，或计划一次旅行，那么你会受到启发。',
        '狮子座':'2020年对于狮子座来说是个人工作快速发展，事业腾飞的一年。他们在年初就能够凭借着土星与冥王星相合落于摩羯宫，从而迎来更为稳定的事业运。',
        '处女座':'对于处女座来说,有时创造力需要耐心。你已经播下了种子，现在你必须等待，直到你看到新芽。所以，敞开你的心扉，接受各种可能性——尤其是那些与旅行、教学、学习或外国人有关的可能性。慢慢来，命里有时终须有。',
        '天秤座':'对于天秤座来说，2020年是一个变化较大的一年，在这一年里他们的各项运势都不是很稳定，尤其是在工作中需要面临很多选择。所以在这一年里天秤座们必须要做好心理准备，当问题了来临之后可以冷静对待。',
        '天蝎座':'对于天蝎座来说,你所写的、所说的、所宣传的都会对一月份产生真正的影响。你与他人的联系是至关重要的，所以一定要保持联系，或者出去走走——即使你真的不想这样。这里也有一条双行道——你将与你生活中的其他人、邻居和更远的地方打交道——可能比平时更多。',
        '射手座':'射手座今年会热衷于推动事情向前发展，或者让其他人加入到激动人心的计划或项目中来。如果你把精力用在关心和关注上，你就能以积极的方式开始2020年。但是你也要实际一点，不要因为别人花了时间或者你梦想的结果迟迟没有实现而失去它。',
        '魔羯座':'2020年伊始，你是真正的宇宙摩羯座——海山羊。主要是关于你，也可能是你的伴侣，工作伙伴，以及友谊。这对你来说可能是一个非凡的时刻，但它也带来了很多责任——对你们中的许多人来说——还有一些非常重要的决定。',
        '水瓶座':'一月份开始，水瓶座有很多事情要考虑。很多事情似乎都超出了你的控制范围，所以不要为那些烦人的新年计划感到压力。与此同时，大步前进，保持灵活。2020年的春天对于很多水瓶座的人来说是一个改变游戏规则的时刻——你的新年即将从那时开始。',
        '双鱼座':'双鱼座很难应对2020年中各项运势的变化，在这一年里土星与冥王星相合，而且还会在年初落入到他们的第十一宫当中，这会给双鱼座的工作、生活带来极大地改变。尤其是在人际交往方面他们会面临人缘“干涸”，身边能够信任的人并不多，这对于双鱼座的影响还是相当大的。'
    }
    star_dict = {
        '白羊座':'白羊座有一种让人看见就觉得开心的感觉',
        '双子座':'双子座喜欢追求新鲜感，有点儿小聪明，就是耐心不够',
        '金牛座':'金牛座很保守，喜欢稳定，一旦有什么变动就会觉得心里不踏实',
        '巨蟹座':'巨蟹座的情绪容易敏感，也缺乏安全感，容易对一件事情上心',
        '狮子座':'狮子座有着宏伟的理想，总想靠自己的努力成为人上人',
        '处女座':'处女座虽然常常被黑，但你还是依然坚持追求自己的完美主义',
        '天秤座':'天秤座常常追求平等、和谐，擅于察言观色，交际能力很强',
        '天蝎座':'天蝎座精力旺盛、占有欲极强，对于生活很有目标',
        '射手座':'射手座崇尚自由，勇敢、果断、独立，身上有一股勇往直前的劲儿',
        '魔羯座':'摩羯座是十二星座中最有耐心，为事最小心、也是最善良的星座',
        '水瓶座':'水瓶座的人很聪明，他们最大的特点是创新，追求独一无二的生活',
        '双鱼座':'双鱼座是十二宫最后一个星座，他集合了所有星座的优缺点于一身'
    }
    star_fortunes_dict = {
        '白羊座': '白羊座财运方面运势普通，投资理财方面比较谨慎、小心，不熟悉的项目是不会考虑入手的',
        '双子座': '双子座财运方面运势平平，投资理财方面比较随缘，没什么特别大的发财野心',
        '金牛座': '金牛座财运方面运势一般，投资理财方面能够走出某些误区，找到更合适的项目了',
        '狮子座': '狮子座财运方面运势平平，投资理财方面别高估了自己的能力，多请教专业人士为宜',
        '处女座': '处女座财运方面运势一般，投资理财方面你也许会通过一系列的筛选，找到适合自己的项目',
        '天秤座': '天秤座财运方面运势还好，投资理财方面可能会有人给你提供一些机会',
        '天蝎座': '天蝎座财运方面运势普通，投资理财方面不宜操之过急，要小心误入陷阱造成损失',
        '射手座': '射手座财运方面运势普通，投资理财方面可能会投入多、收益少',
        '魔羯座': '摩羯座财运方面运势一般，投资理财方面好的项目会有不少人都盯着，想要入手不是件简单的事情',
        '水瓶座': '水瓶座财运方面运势还好，投资理财方面会有些较大的布局改变，收益能获得不少',
        '双鱼座': '双鱼座财运方面运势一般，投资理财方面胆子放大一点，做决定别犹豫'
    }
    star_today = {
        '白羊座': '白羊座今日运势还好，你会变得更加理性、豁达了，精神上也不再纠结了。感情方面运势尚可，你看待亲密关系会理智一些，不需要担心和纠结的事情也不会再和伴侣纠缠了。事业方面运势还好，工作中会变得更加大胆一点，能积极主动去争取自己想要做的任务，不再是唯唯诺诺的状态了。财运方面运势普通，投资理财方面会打开思路，考虑问题也会更加全面一些。健康方面运势平平，精神状态会有所恢复。',
        '双子座': '双子座今日运势稍好，你在生活、工作中能遇到比较愿意帮助人的好伙伴。感情方面运势尚佳，亲密关系中你的另一半会提供给你较多的情绪价值，他/她常常鼓励你、支持你、为你加油打气。事业方面运势较好，职场中与客户打交道会简单一点，对方比较好说话，你有什么实际困难的话，也愿意多体谅一点。财运方面运势一般，投资理财方面怎么想的就怎么去做为好，别犹豫太久。健康方面运势普通，情绪比较稳定。',
        '金牛座': '金牛座今日运势尚可，你和周围人的关系变得更加亲近了，不再觉得自己孤单了。感情方面运势还好，你和另一半的家人、朋友相处时会变得更加自然一点，不再感觉很拘束了。事业方面运势尚可，团队中大家的人际关系还是可以的，彼此之间多能相互帮助，不会看到别人进步就眼红拆台。财运方面运势平平，投资理财方面可以选择大机构的比较可靠的项目入手。健康方面运势一般，多与人接触的话，能让心情变好',
        '巨蟹座': '巨蟹座今日运势平平，你要小心工作、生活中那些只会甜言蜜语，却不做实事的人。感情方面运势稍弱，亲密关系中你会发现另一半有点爱忽悠人，总是说一些没边际的大话、许诺根本不可能实现的事。事业方面运势平平，职场中你在协调工作时会发现有些话好听、事难办的情况出现，“滚刀肉”似的人很难对付。财运方面运势普通，尽量克制一下花钱的冲动，节约点为好。健康方面运势一般，多补水为宜',
        '狮子座': '狮子座今日运势普通，你可能会为团体中的某些事情而费神。感情方面运势平平，亲密关系中你和另一半没办法回避物质层面的问题，为了更好的交往下去，这个话题还是要理性地探讨一下的好。事业方面运势普通，你在团队中可能会感觉自己的能力施展不开，想要有所作为却不太容易。财运方面运势稍弱，投资理财方面可能会有一些家居方面的开销，尽量控制预算为宜。健康方面运势一般，少些大吃大喝比较好',
        '处女座': '处女座今日运势较弱，生活、工作中会比较贪图享乐，不太愿意吃苦。感情方面运势一般，你和另一半相处时会感觉对方有些以自我为中心，很少会顾及到你的感受。事业方面运势稍弱，职场中也许会遇到外行领导内行的事情，另外客户也会提出一些稀奇古怪的要求非要让你完成。财运方面运势较弱，投资理财方面别太自信了，选择项目不能看表面，要关注内核才行。健康方面运势普通，生活中烟酒要节制一点',
        '天秤座': '天秤座今日运势尚可，你在工作、生活中是个比较善解人意的人，内心非常柔软。感情方面运势还好，亲密关系中你很愿意和伴侣分享自己在生活上的事情，很重视彼此之间的交流。事业方面运势尚可，工作中你总是能千方百计地为客户解决问题，因为会颇受对方信赖，专业能力也得到了认可。财运方面运势普通，投资理财方面有点凭心情做决定，还是尽量客观一点为好。健康方面运势平平，精气神还可以',
        '天蝎座': '天蝎座今日运势还好，你对生活、工作等方面有不少计划想要去实现。感情方面运势尚可，你觉得和另一半的亲密关系会发展得越来越好的，对此总是信心十足的样子。事业方面运势还好，你在工作上的野心不小，想要拓展自己的人脉和职场维度，希望能获得更多的关注和支持。财运方面运势一般，投资理财方面会进行比较大的布局，对你来说想追求的不是单单获得收益这么简单。健康方面运势尚可，多运动对身体好',
        '射手座': '射手座今日运势还好，当下是开始新生活的一个契机，尽量把握好为宜。感情方面运势尚可，你和另一半的亲密关系会有一个正向发展的机会，只要你们双方都是较积极的态度，那么未来的感情生活还是可以期待的。事业方面运势还好，工作中可能会有个晋升的机会，是否把握得住就看你的了。财运方面运势普通，投资理财方面会有适合自己的项目出现。健康方面运势尚可，想要增强体质的话，运动和营养都是必不可少的',
        '魔羯座': '摩羯座今日运势尚可，你对自己的工作、生活都能安排得井井有条。感情方面运势还好，你和另一半在一起时有什么事情都愿意两人一起商量着办，不会一个人做主而忽视对方的意见。事业方面运势尚可，工作中的效率还是很高的，基本上都能按照时间节点完成任务，处理问题也十分利落。财运方面运势一般，投资理财方面还是实际一点的好，有些负担太高的项目最好别参加。健康方面运势普通，营养要均衡',
        '水瓶座': '水瓶座今日运势稍好，你要尽量控制住自己冲动、莽撞的一面，遇事多冷静一点为宜。感情方面运势还好，你在亲密关系中是占据主动权的一方，但是也要注意别太霸道了，多给伴侣一些私人空间为好。事业方面运势稍好，工作中掌控局面的能力很强，不会被别人牵着鼻子走，做事不紧不慢地很有自己的节奏。财运方面运势平平，投资理财方面最好入手一些可控性比较强的项目。健康方面运势尚可，身体比较健康。',
        '双鱼座': '双鱼座今日运势一般，工作、生活中要用心一点，别总是开小差。感情方面运势平平，亲密关系中少任性一点，多体谅一下伴侣的辛苦为好，否则对方也会嫌你烦的。事业方面运势普通，工作中也许会遇到不太靠谱的同事来协助你做事，一定要多加检查、确认才行，否则出了问题主责还是你的。财运方面运势一般，投资理财方面别想起什么就做什么，多打听清楚了再出手的好。健康方面运势稍弱，多休养为宜'
    }
    star_tommorow = {
        '白羊座': '白羊座明日运势尚可，工作、生活中会有不少幸运的事情发生。感情方面运势还好，你和伴侣之间的亲密关系会有质的飞跃，彼此也会觉得对方是非常合意的另一半。事业方面运势尚可，工作中即便有些小插曲你也能解决得很好，职场中愿意向你伸出援手的人也不少。财运方面运势稍好，投资理财方面可能会接触到一些意想不到的项目，获得的收益也是在意料之外的。健康方面运势一般，适当活动筋骨为宜。',
        '双子座': '双子座明日运势还好，你对不少知识都很感兴趣，总想要学习一番。感情方面运势尚可，亲密关系中和伴侣沟通时尽量要有比较积极的回应才好，如果你总是不回应，对方也就无法知道你的想法了。事业方面运势还好，工作中有很强的好奇心，也比较善于学习新的专业知识，是个非常要求上进的人。财运方面运势尚可，投资理财方面如果可以多总结经验的话，就能找到适合自己的项目了。健康方面运势普通，多补水为好。',
        '金牛座': '金牛座明日运势一般，生活、工作中的一些事情会让你花费较多的精力。感情方面运势普通，你和另一半的亲密关系多是按部就班地发展着，两人相处得也是比较熟悉了。事业方面运势还好，工作中尽量多花些精神在项目上为好，不要被其他闲事牵扯精力，也要注意按计划完成好手中的工作。财运方面运势平平，投资理财方面没什么太大的变动，按原定计划进行就好。健康面运势一般，想要保持活力，运动是必不可少的。',
        '巨蟹座': '巨蟹座明日运势不错，你对当下的工作、生活都是很满意的，面对这一切你也很有信心。感情方面运势稍好，你和伴侣的亲密关系已经发展得比较稳定了，彼此之间也加深了不少了解。事业方面运势尚可，工作中已经可以独当一面了，上司也会把更加重要的工作交给你去负责。财运方面运势还好，投资理财方面只要能保持住理智，不胡乱做决定的话，获得收益还是较轻松的。健康方面运势平平，适当运动即可。',
        '狮子座': '狮子座明日运势普通，你要多关注一下自己的心理情况，凡事别想太多，放轻松为宜。感情方面运势稍弱，你在亲密关系中不要过于爱撒娇，或是没完没了地说一些负能量的事情，毕竟不好的事没人愿意一直听。事业方面运势普通，做事时要注意别把不良情绪带进工作中，尽量保持自己的专业度。财运方面运势平平，投资理财方面拿不准主意的时候，可以咨询一下专业人士。健康方面运势一般，少点胡思乱想为好。',
        '处女座': '处女座明日运势较弱，生活、工作中的某些事情结束了不一定就是坏事，正所谓不破不立。感情方面运势平平，你也许需要好好整理一下自己的心情，面对亲密关系你到底是怎么想的，最好对自己坦诚一点。事业方面运势稍弱，工作中出现什么变动的话也别紧张，先看看事情的走向趋势再做打算。财运方面运势较弱，经济情况不算乐观，有些不必要的开始最好消减掉。健康方面运势普通，小心感冒、发烧问题。',
        '天秤座': '天秤座明日运势稍好，你面对生活、工作中的压力是毫不惧怕的，有种越战越勇之感。感情方面运势尚可，你的另一半是个不太浪漫的严肃人，他/她和你相处时也是一板一眼的，虽然人有点木讷却很可靠。事业方面运势不错，工作中只要严格执行上司的命令，按他/她说的去做就没问题，千万别自己做主。财运方面运势普通，投资理财方面眼光还可以，能选到合适的项目。健康方面运势还好，身体比较健康。',
        '天蝎座': '天蝎座明日运势尚可，你会逐渐走出思想困境，更加自信地面对生活、工作。感情方面运势还好，你对待亲密关系不再是自己给自己找别扭了，和伴侣相处也变得更加真诚、真实了一些。事业方面运势尚可，工作中你会主动抛弃思想包袱，更加轻松地、自信地处理工作上遇到的问题。财运方面运势普通，投资理财方面试着多关注一下新兴项目会有助你进行选择。健康方面运势平平，身体和精神都要保持放松才行。',
        '射手座': '射手座明日运势一般，你会感觉精神压力稍小一些了，有些一直头疼的事情也在慢慢解决中。感情方面运势平平，亲密关系中你和另一半能够正视彼此之间的问题，坦承地交换意见。事业方面运势一般，工作中一些棘手的事情正在得到解决，你也能从繁重的工作压力中稍微喘一口气了。财运方面运势普通，投资理财方面与其纠结怎么选择，还不如大胆一点为好。健康方面运势稍弱，要注意失眠、精神衰弱的问题。',
        '魔羯座': '摩羯座明日运势平平，你在生活、工作中可能需要别人的帮助才能做好事情。感情方面运势一般，亲密关系中你依靠伴侣的时候较多，生活中有什么事情都想找伴侣商量商量后再说。事业方面运势平平，工作中想要获得某种支持，可能需要通过竞争才行，并不是随随便便就是能到支援的。财运方面运势稍弱，投资理财方面资金有限，到底要选择什么样的项目要费点脑筋了。健康方面运势普通，适当活动筋骨即可。',
        '水瓶座': '水瓶座明日运势稍弱，你做事有点吊儿郎当的，如果这种态度不改变的话就什么都干不好。感情方面运势平平，亲密关系中太过于自由是不行的，如果你对伴侣来说和脱了线的风筝一样，那么交往又有什么意义呢。事业方面运势较弱，工作时最好打起精神来，别稀里糊涂的，做正事要有做正事的样子。财运方面运势稍弱，投资理财方面别有太强的投机心理，小心上当受骗。健康方面运势一般，外出时要注意安全',
        '双鱼座': '双鱼座明日运势尚可，你做事的积极性很高，总是充满自信一般。感情方面运势还好，你和另一半相处时彼此都很喜欢积极互动，这样会增强你们之间的默契度。事业方面运势尚可，你可能会去负责新的业务，接触一些新的客户、同事，这对你增长见识、开阔眼界还是很有帮助的。财运方面运势平平，投资理财方面有些新机会出现，你可以多关注一下有没有适合自己的项目。健康方面运势普通，积极参加运动对身体好。'
    }
    star_thisweek = {
        '白羊座': '本周白羊座的整体运势表现大体平顺，本周白羊的运势关键词为脚踏实地，本周不需要你天花乱坠地遐想，做好自己手头的各种事情就能获得好的收获。',
        '金牛座': '本周金牛座的整体运势表现大致稳定，本周的运势关键词为找到自我，本周不用太在乎他人的眼光，可以按照自己的心意去行事。',
        '双子座': '本周双子座的整体运势表现大致平稳，本周的运势关键词为得到援手，本周在关键时刻你总是能够得到支持和帮助，让你感觉很欣慰。',
        '巨蟹座': '本周巨蟹座的整体运势表现大体尚佳，本周的运势关键词为理解万岁，本周你要尝试去换位思考，好好处理人际关系中的一些矛盾。',
        '狮子座': '本周狮子座的整体运势表现大体稳定，本周的运势关键词为救赎自我，本周不要总是钻牛角尖，尝试换一个角度去看待问题。',
        '处女座': '本周处女座的整体运势表现大致顺畅，本周的运势关键词为寻求答案，你可能对某些事情心中会充满疑问，本周是你寻找答案的好时机。',
        '天秤座': '本周天秤座的整体运势表现大体向好，本周的运势关键词为尝试突破，你要懂得放弃求稳的心态，多多寻找新的挑战。',
        '天蝎座': '本周天蝎座的整体运势表现大致平顺，本周的运势关键词为敞开胸怀，你可以在本周放松身心地去做一些事情，也会遇到比较好的运势。',
        '射手座': '本周射手座的整体运势表现大体顺畅，本周的运势关键词为感性思维，本周你会遇到一些事情，有时候尝试用直觉去解决也未尝不可。',
        '魔羯座': '本周摩羯座的整体运势表现大体稳定，本周的运势关键词为寻求安慰，本周你在情绪上会有一些难受和压抑，你需要找到放松的出口。',
        '水瓶座': '本周水瓶座的整体运势表现大致平稳，本周你的运势关键词为携手并进，本周你要找到和你志同道合伙伴，前行的路上会更加顺利。',
        '双鱼座': '本周双鱼座的整体运势表现大体尚佳，本周你的运势关键词为内心平静，本周你需要放弃一些胡思乱想的想法，保持心态的平和比较重要。'
    }
    star_month = {
        '白羊座': '本月白羊座的整体星座运势表现大体稳定，本月白羊座会在处事行事方面有一些新的感悟，也许是想法，也许是经验，好好去分析和积累这些东西，或许你能获得看待世界和对待情感的更好的角度',
        '双子座': '本月双子座的整体星座运势表现大体平顺，本月双子座在各个方面都有一个较为理想的表现，但你需要明白有时候急功近利并不是一件好事，在平稳的处境中，平和的心态和经验的积累似乎更加重要',
        '金牛座': '本月金牛座整体星座运势表现大体平稳，本月金牛座或许需要做好妥协的准备，金牛座不缺乏不撞南墙不回头的勇气，但在选择和决定的时候，还需要更加明智和理性',
        '巨蟹座': '本月巨蟹座的整体星座运势表现大致顺畅，巨蟹座能在本月获得较好的运气，处理各项事务的时候都能获得需要的帮助，也让你能够及时化险为夷，得到圆满的结局。',
        '狮子座': '本月狮子座的整体星座运势表现大体平稳，本月狮子座需要学会收敛自己的脾性，不可让自己的个性过于锋芒毕露，否则你很容易为自己的自满自足而得到不乐意的结果',
        '处女座': '本月处女座的整体星座运势表现大体平顺，处女座在本月会面临一些消极和难受的情绪，但你要相信大方向的积极和光明，还有一份美好在等待着你',
        '天秤座': '本月天秤座的整体星座运势表现大致顺利，本月天秤座或许可以找到自己想要的生活，也让自己的心情保持愉悦和平和，在人际交往方面也能够擦出新的火花',
        '天蝎座': '本月天蝎座的整体星座运势表现大致不错，本月天蝎座能够顺其自然的行事，不用太过顾及他人的要求和想法，努力享受片刻的轻松和美好',
        '射手座': '本月射手座的整体星座运势表现大致平稳，本月射手座在各个方面的进展似乎有一些缓慢，你很难看见即可达成的结果，等待将会成为最近这段时间你的关键词',
        '魔羯座': '本月摩羯座的整体星座运势表现大致稳定，摩羯座在本月的运势需要依靠自己的努力才能获得更加满意的结果，而经历的这段过程也会成为你的一个财富',
        '水瓶座': '本月水瓶座的整体星座运势表现大体稳定，本月水瓶座似乎想要找到一些平静的生活方式，在社交等方面也会显得比较收敛，活跃度有所降低',
        '双鱼座': '本月双鱼座的整体星座运势表现大致平顺，本月双鱼座会想要完成长久以来的一些梦想，你似乎也找到了新的动力，心情会变得更加明朗'
    }



    '''构造词对应的类型'''

    def build_wdtype_dict(self):
        wd_dict = dict()
        for wd in self.region_words:
            wd_dict[wd] = []
            if wd in self.news_wds:
                wd_dict[wd].append('news')
            if wd in self.star_wds:
                wd_dict[wd].append('star')
            if wd in self.dirty_wds:
                wd_dict[wd].append('dirty')
            if wd in self.attack_wds:
                wd_dict[wd].append('attack')
            if wd in self.joke_wds:
                wd_dict[wd].append('joke')

        return wd_dict

    '''基于特征词进行分类'''

    def check_words(self, wds, sent):
        for wd in wds:
            if wd in sent:
                return True
        return False

    '''基于特征词进行分类'''

    def check_news_words(self, wds, news_dict):
        ner_count = 0
        wds = jiagu.seg(wds)
        for idx in range(len(news_dict)):
            sent = news_dict[idx]
            for wd in wds:
                if wd in sent:
                    return True,idx
        return False,None
    '''主函数'''
    def classify(self, question):
        s2s = False
        data = {}
        medical_dict = self.check_rec(question)
        if not medical_dict:
            return False
        data['args'] = medical_dict
        #收集问句当中所涉及到的实体类型
        types = []
        star_n = 'no'
        dirty_n = 'no'
        attack_n = 'no'
        news_n = 'no'
        joke_n = 'no'
        for type_ in medical_dict.values():
            types += type_
        question_types = []
        for k, v in medical_dict.items():
            if 'star'in v:
                if star_n != 'no':
                    continue
                else:
                    star_n = k
                # break
            elif ('news' in v) and k != '新闻':
                # break
                continue
            elif 'dirty'in v:
                dirty_n = k
                # break
            elif 'attack' in v:
                attack_n = k
                # break
            elif 'joke'in v:
                joke_n = k
                break
        if self.check_words(['新闻'], question) and ('news' in types):
            question_type = 'news'
            question_types.append(question_type)
            return news_rec()

        if self.check_words(self.star_wds, question) and self.check_words(['财运','财'], question) and ('star' in types):
            question_type = 'star_fortunes'
            question_types.append(question_type)
            return self.star_fortunes_dict[star_n]

        if self.check_words(self.star_wds, question) and self.check_words(['今天','今日'], question) and ('star' in types):
            question_type = 'star'
            question_types.append(question_type)
            return self.star_today[star_n]

        if self.check_words(self.star_wds, question) and self.check_words(['明天','明'], question) and ('star' in types):
            question_type = 'star'
            question_types.append(question_type)
            return self.star_tommorow[star_n]
        if self.check_words(self.star_wds, question) and self.check_words(['这周','本周','周'], question) and ('star' in types):
            question_type = 'star'
            question_types.append(question_type)
            return self.star_thisweek[star_n]

        if self.check_words(self.star_wds, question) and self.check_words(['这个月','这月','本月','月份','月'], question) and ('star' in types):
            question_type = 'star'
            question_types.append(question_type)
            return self.star_month[star_n]

        if self.check_words(self.star_wds, question) and self.check_words(self.star_qws, question) and ('star' in types):
            question_type = 'star_fate'
            question_types.append(question_type)
            return self.star_fate_dict[star_n]

        if self.check_words(self.star_wds, question) and ('star' in types):
            question_type = 'star'
            question_types.append(question_type)
            return self.star_dict[star_n]

        if self.check_words(self.dirty_wds, question) and ('dirty' in types):
            question_type = 'dirty'
            question_types.append(question_type)
            return self.dirty_dict[dirty_n]

        if self.check_words(self.attack_wds, question)and self.check_words(['你'], question) and ('attack' in types):
            question_type = 'attack'
            question_types.append(question_type)
            return self.attack_dict[attack_n]
        if self.check_words(self.attack_wds, question)and not(self.check_words(['你'], question)) and ('attack' in types):
            question_type = 'attack'
            question_types.append(question_type)
            return self.attack_dict[attack_n]

        if self.check_words(self.joke_wds, question) and ('joke' in types):
            question_type = 'joke'
            question_types.append(question_type)
            j_idx = random.randint(0,(len(self.joke_list)-1))
            return self.joke_list[j_idx]
        newschack,news_idx = self.check_news_words(question,self.news_dict)
        if newschack and ('news' in types):
            question_type = 'news'
            question_types.append(question_type)
            return news_chack(news_idx)


# if __name__ == '__main__':
    # chack_model = QuestionClassifier()
    # text = str(input('星座测试:'))
    # # text = '本周双子座的运势处女座怎么样'
    # topic = 'None'
    # question_type ='None'
    # list = chack_model.check_medical(text)
    # print(list)
    # if len(list)==0:
    #     print('返回生成回答')
    # for wd in list:
    #     if wd in chack_model.star_dict:
    #         question_type = 'star'
    #         for wd in list:
    #             if wd in chack_model.star_qws:
    #                 question_type = 'star_fate'
    #
    # for wd in list:
    #     if wd in chack_model.star_dict:
    #         if question_type == 'star':
    #             print(chack_model.star_dict[wd])
    #             break
    #         elif question_type == 'star_fate':
    #             print(chack_model.star_fate_dict[wd])
    #             break

    # for wd in list:
    #     if wd in chack_model.star_dict:
    #         topic= 'star'
    #         for wd in list:
    #             if wd in chack_model.star_qws:
    #                 question_type = 'fate'
    #         break
    # if topic == 'star':
    #     if question_type == 'fate':
    #         print(chack_model.star_fate_dict[wd])
    #     elif question_type == 'None':
    #         print(chack_model.)




