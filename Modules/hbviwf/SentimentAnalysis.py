#encoding=utf-8
from __future__ import print_function, unicode_literals
from Modules.hbviwf.read_file import read_file_part
import jieba
import jieba.posseg
import jieba.analyse
import re
import os

rf = read_file_part()

def _text_processing_(filename):
    file_object = open(filename)
    try:
        Document = file_object.read()
    finally:
        file_object.close()
    Paragraphs = Document.split("\n")
    document_value_list = []
    document_value = 0
    while '' in Paragraphs:                        #这个可以改进
        Paragraphs.remove('')
    for paragraph in Paragraphs:
        Sentences = re.split(r'[。；！？.;!?]', paragraph)
        paragraph_value_list = []
        paragraph_value = 0
        while '' in Sentences:                     #这个可以改进
            Sentences.remove('')
        for sentence in Sentences:
            Groups = re.split(r'[,，]', sentence)
            sentence_value_list = []
            sentence_value = 0
            while '' in Groups:                    #这个可以改进
                Groups.remove('')
            for group in Groups:
                seg_list = jieba.cut(group)
                print('/'.join(seg_list))
                order = 1
                W = 1
                dword_weight = 1
                dword_point = -1
                nword_point = []
                eword_weight = 0
                eword_Polar = 1
                for word in seg_list:
                    if (word in rf.extreme):
                        dword_weight = 2
                        dword_point = order
                    elif (word in rf.very):
                        dword_weight = 1.25
                        dword_point = order
                    elif (word in rf.more):
                        dword_weight = 1.2
                        dword_point = order
                    elif (word in rf._ish):
                        dword_weight = 0.8
                        dword_point = order
                    elif (word in rf.insufficiently):
                        dword_weight = 0.5
                        dword_point = order
                    elif (word in rf.over):
                        dword_weight = 1.5
                        dword_point = order
                    elif (word in rf.noword):
                        nword_point.append(order)
                    else:
                        for i in range(0, rf.emotionnum):
                            if (word == rf.emotion[i][0]):
                                eword_weight = rf.emotion[i][5]
                                if (rf.emotion[i][6] == 1):
                                    eword_Polar = 1
                                elif (rf.emotion[i][6] == 2):
                                    eword_Polar = -1
                                else:
                                    char = rf.emotion[i][4]
                                    if (char in rf.positive):
                                        eword_Polar = 1
                                    elif (char in rf.negative):
                                        eword_Polar = -1
                                    else:
                                        eword_Polar = 0
                                break
                    order = order + 1
                for point in nword_point:
                    if (point > dword_point):
                        W = W * -1
                    else:
                        W = W * 0.5
                group_value = W * dword_weight * eword_Polar * eword_weight
                print("group_value:", group_value)
                print(W, dword_weight, eword_Polar, eword_weight)
                sentence_value_list.append(group_value)
            for gvalue in sentence_value_list:
                sentence_value = sentence_value + gvalue
            sentence_value = sentence_value / len(sentence_value_list)
            paragraph_value_list.append(sentence_value)
        for svalue in paragraph_value_list:
            paragraph_value = paragraph_value + svalue
        paragraph_value = paragraph_value / (len(paragraph_value_list))
        document_value_list.append(paragraph_value)
    for pvalue in document_value_list:
        document_value = document_value + pvalue
    document_value = document_value / len(document_value_list)
    if (document_value > 0):
        print(1)
        return 1
    elif (document_value < 0):
        print(-1)
        return -1
    else:
        print(0)
        return 0

posPath = "G:\\PyCharm\\SentimentNew\\res\\corpus\\hotel\\pos\\";
negPath = "G:\\PyCharm\\SentimentNew\\res\\corpus\\hotel\\neg"

def _pos_success_rate_():
    Percentage = 0
    FindPath = posPath
    FileNames = os.listdir(FindPath)
    for file_name in FileNames:
        filename = os.path.join(FindPath, file_name)
        if 'utf8' in file_name:
            if (_text_processing_(filename) == 1):
                Percentage += 1
    Percentage = Percentage / 10.0
    return Percentage


def _neg_success_rate_():
    Percentage = 0
    FindPath = negPath
    FileNames = os.listdir(FindPath)
    for file_name in FileNames:
        filename = os.path.join(FindPath, file_name)
        if (_text_processing_(filename) == -1):
            Percentage += 1
    Percentage = Percentage / 10.0
    return Percentage

print(_neg_success_rate_())
