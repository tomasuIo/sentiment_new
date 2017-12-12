#encoding=utf-8
import xlrd
class read_file_part:
    positive = ['PA', 'PE', 'PD', 'PH', 'PG', 'PB', 'PK']
    negative = ['NA', 'NB', 'NJ', 'NH', 'PF', 'NI', 'NC', 'NG', 'NE', 'ND', 'NN', 'NK', 'NL', 'PC']

    extreme = ""        ##极其|extreme / 最|most           2
    very    = ""        ##很|very                          1.25
    more    = ""        ##较|more                          1.2
    _ish    = ""        ##稍|-ish                          0.8
    insufficiently = "" ##欠|insufficiently                0.5
    over    = ""        ##超|over                          1.5
    noword  = ""        ##否定词
    emotion = []        ##情感词
    emotionnum   = 0         ##情感词总数

    def _read_file_(self, filename):
        file_object = open(filename,encoding="utf-8")
        try:
            word = file_object.read().split()
        finally:
            file_object.close()
        return word

    def _read_dllg_emotion_file(self):
        # 打开文件
        bk = xlrd.open_workbook('G:\\PyCharm\\SentimentNew\\Modules\\hbviwf\\'+ u'/情感词汇本体' + '.xlsx')
        # 打开工作表
        sh = bk.sheet_by_name("Sheet1")
        # 获取行数
        self.emotionnum = sh.nrows-1
        word = [[] for i in range(1, sh.nrows)]
        for i in range(1, sh.nrows):
            word[i-1] = sh.row_values(i)
        return word

    def __init__(self):
        self.extreme = self._read_file_('G:\\PyCharm\\SentimentNew\\Modules\\hbviwf\\'+u'知网Hownet情感词典\\'+'extreme.txt')
        self.very = self._read_file_('G:\\PyCharm\\SentimentNew\\Modules\\hbviwf\\'+u'知网Hownet情感词典\\'+'very.txt')
        self.more = self._read_file_('G:\\PyCharm\\SentimentNew\\Modules\\hbviwf\\'+u'知网Hownet情感词典\\'+'more.txt')
        self._ish = self._read_file_('G:\\PyCharm\\SentimentNew\\Modules\\hbviwf\\'+u'知网Hownet情感词典\\'+'-ish.txt')
        self.insufficiently = self._read_file_('G:\\PyCharm\\SentimentNew\\Modules\\hbviwf\\'+u'知网Hownet情感词典'+'\\insufficiently.txt')
        self.over = self._read_file_('G:\\PyCharm\\SentimentNew\\Modules\\hbviwf\\'+u'知网Hownet情感词典'+'\\over.txt')
        self.noword = self._read_file_('G:\\PyCharm\\SentimentNew\\Modules\\hbviwf\\' + u'/否定' + '.txt')
        self.emotion = self._read_dllg_emotion_file()