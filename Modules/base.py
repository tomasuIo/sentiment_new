# -*- coding: utf-8 -*-
import re
import jieba.posseg
import Modules.LoadDictionary
import os
import os.path
from functools import reduce


#DATA SEGMENT
NoWordSet = set()
PosSenDic = {}
NegSenDic = {}
ExtDic = {}
DicPath = "G:\\PyCharm\\SentimentNew\\res\\dic\\"
NegFilePath = 'G:\\PyCharm\\SentimentNew\\res\corpus\\hotel\\neg\\'
PosFilePath = 'G:\\PyCharm\\SentimentNew\\res\\corpus\\hotel\\pos\\'
SenseWordKindSet = {}


#DATA INIT
with open(DicPath+ "reversed.txt", encoding="utf-8") as f:
    for items in f:
        item = items.strip()
        NoWordSet.add(item)

PosSenDic = Modules.LoadDictionary.loadDict(DicPath, "pos_comment.txt", 1)
Modules.LoadDictionary.appendDict(PosSenDic, DicPath, "pos_sentiment.txt", 1)
NegSenDic = Modules.LoadDictionary.loadDict(DicPath, "neg_sentiment.txt", -1)
Modules.LoadDictionary.appendDict(NegSenDic, DicPath, "neg_comment.txt", -1)
ExtDic = Modules.LoadDictionary.loadExtentDict(DicPath, "extent_Lv_")

SenseWordKindSet = {"a", "ad", "an", "ag", "al", "d", "dg"}


#DATA TEST             #pass
#print(PosSenDic)
#print(NegSenDic)
#print(NoWordSet)
#FUNCTION SEGMENT

def getParagraph(str):
    str = re.split('[。？！；.?!;“”]', str)
    for s in str:
        if s != '':
            yield s.strip()


def getGroup(gen):
    for s in gen:
       s = re.split('[,，]',s)
       if s[-1] == '':
           s.pop()
       for str in s:
           yield str.strip()


def __getScore__(dic, word):
    return dic.get(word, 0)

def findWordInfo(word, kind, All = True):
    dic = {}
    def __setdic__(k, s, p = None):
        dic['n'] = word                   #word
        dic['k'] = k                      #kind
        dic['s'] = s                      #score
        dic['p'] = p                      #property

    if word in NoWordSet:
        __setdic__('no', None, None)
    elif kind in SenseWordKindSet:
        score = __getScore__(ExtDic, word)
        if  score != 0:
            __setdic__(kind, score, 'ext')
        else:
            score = __getScore__(PosSenDic, word)
            if score != 0:
                __setdic__(kind, score, 'pos')
            else:
                score = __getScore__(NegSenDic, word)
                if score != 0:
                    __setdic__(kind, score,'neg')
                else:   #有意义的词被遗漏了
                    __setdic__(kind,score)
                    ignoredWordList.write("{} {} {}\n".format(word,kind,score))
                    pass
    elif kind == 'c':
        __setdic__(kind, None, None)
    elif All:
        __setdic__(kind, None, None)
    if len(dic) > 0:
        return dic
    else: return None


def splictGroupIntoList(str):                #传入一个意群(字符串)返回一个jieba分词系统分词后的词描述字典列表
    _word_list = []
    data = jieba.posseg.cut(str)
    for word, kind in data:
        tmp = findWordInfo(word,kind)
        if tmp:
            _word_list.append(tmp)
    return _word_list


def __check__(word):
    dic = {}
    dic["pos"] = __getScore__(PosSenDic, word)
    dic["neg"] = __getScore__(NegSenDic,word)
    dic["ext"] = __getScore__(ExtDic, word)
    return dic

def __reduceOp__(item1, item2):
    return item1 * item2

def __CaculateScoreOfGroup__(stack = [],ExtInNoAndSen = False):
    if ExtInNoAndSen:
        return reduce(__reduceOp__, stack) * -0.5
    else:
        return reduce(__reduceOp__, stack)


def __meet_conj__(stack):
    pass


def GetGroupScore(group = [{}], stream =None):#传入一个由描述词的字典组成的列表, 得到一个意群的分值
    if len(group) > 0:
        stack = []
        copystack = []
        GroupScore = 0
        NoWordFirst = False
        HaveSenWord = False
        ExtInNoAndSen = False
        if group[0].get("k") == 'no':
            NoWordFirst = True
            group.pop(0)
            stack.append(-1)
            copystack.append(-1)
        for item in group:
            if item.get('p') == 'pos' or item.get('p') == 'neg':
                HaveSenWord = True
                stack.append(item.get('s'))
            elif item.get('p') == 'ext':
                stack.append(item.get('s'))
                if NoWordFirst == True and HaveSenWord == False:
                    ExtInNoAndSen = True
            elif item.get('k') == 'c':
                __meet_conj__(stack)
                pass
            elif item.get('k') == 'no':
                stack.append(-1)
        copystack.append(stack)
        if HaveSenWord:
            GroupScore = __CaculateScoreOfGroup__(stack, ExtInNoAndSen)
        return GroupScore, copystack
    return 0, None


def fromPath(path,filename):
    with open(path+filename,'r',encoding='UTF-8') as f:
        document = f.read()

teststr1 = "我很不开心"
teststr2 = "我不很开心"
teststr3 = '我难过而且悲伤'
teststr4 = '第一印象不好'
teststr5 = '这件事不好说'

str = '''服务态度极其差，前台接待好象没有受过培训，连基本的礼貌都不懂，竟然同时接待几个客人；    
大堂副理更差，跟客人辩解个没完，要总经理的电话投诉竟然都不敢给。要是没有作什么亏心事情，跟本不用这么怕。'''

document = ""
with open('G:\\PyCharm\\SentimentNew\\res\corpus\\neg_all.txt','r',encoding='UTF-8') as f:
    document = f.read()


def __getFileNameInDir__(path):
    if path.endswith('.txt'):
        yield ''
    else:
        for parents, directorys, filenames in os.walk(path):
            for filename in filenames:
                yield filename

'''
with open(NegFilePath+"\\neg.160.txt",'r',encoding='UTF-8') as f:
    stack = []
    doc = f.read()
    doc = '第二天在床头柜上放了20港币，所以第二天的卫生比第一天还要好，，，==0'
    pgen = getParagraph(doc)
    ggen = getGroup(pgen)
    for item in ggen:
        stack.append(item)
    print(stack)
'''


def handleError(ErrorKind,*params):
    kinds = {1: "sense word ignored", 2: "wrong score"}
    kind =kinds.get(ErrorKind,0)
    stream = None
    if kind == 1:
        with open('ingored.txt', 'a', encoding='UTF-8') as f:
            stream = f
            pass
    elif kind == 2:
        with open('wrongScore.txt','a',encoding='UTF-8') as f:
            stream = f


wrongFileList = open('wrongScore.txt','a',encoding='UTF-8')
ignoredWordList = open('ignoredWord.txt','a',encoding='UTF-8')


def getScoreOfTextFromDir(path):   #传入一个路径, 可以是一个文件夹的路径(以'//'结尾, 也可以是一个txt文件的路径
    filenames = __getFileNameInDir__(path)
    cx = 0
    for filename in filenames:
         with open(path + filename, 'r', encoding='UTF-8') as f:
             doc = f.read()
             # doc = '老的, , ,标准间改善.  '
             pgen = getParagraph(doc)
             ggen = getGroup(pgen)
             ScoreSum = 0
             for group in ggen:
                 wordList = splictGroupIntoList(group)
                 score, stack = GetGroupScore(wordList)

                 #本段是测试用,以后要写一个专门的侧屋处理函数, 待完成
                 if score < 0:
                     print(group, score, stack)
                 elif score > 0:
                     print(group, stack, wordList)
                 else:
                     print(group, wordList)

                 ScoreSum += score
             if ScoreSum > 0:
                 cx += 1
                 wrongFileList.write("{}\n".format(filename))
                 print(filename, ScoreSum)
    print("total:\t{}".format(cx))
    wrongFileList.close()



testFilePath = 'G:\\PyCharm\\SentimentNew\\res\\corpus\\hotel\\neg\\neg.108.txt'
#getScoreOfTextFromDir(testFilePath)
#getScoreOfTextFromDir(PosFilePath)
getScoreOfTextFromDir(NegFilePath)

'''
group = '房间很脏'
wordList = splictGroupIntoList(group)
score, stack = GetGroupScore(wordList)
#本段是测试用, 以后要写一个专门的侧屋处理函数, 待完成
if score < 0:
    print(group, score, stack)
elif score > 0:
    print(group, stack, wordList)
else:
    print(group, wordList)


ignoredWordList.close()
'''