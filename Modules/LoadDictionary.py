def loadDict(path,fileName, score):
	wordDict = {}
	with open(path+fileName,encoding="utf-8") as fin:
		for line in fin:
			word = line.strip()
			wordDict[word] = score
	return wordDict


def appendDict(wordDict,path, fileName, score):
	with open(path+fileName,encoding="utf-8") as fin:
		for line in fin:
			word = line.strip()
			wordDict[word] = score


def __get_score__(x):
	return {0:0.5, 1:0.8 , 2:1.2, 3:1.25, 4:1.5, 5:2}.get(x,0)


def loadExtentDict(path,fileName):
	extentDict = {}
	for i in range(6):
		score = __get_score__(i)
		with open(path+fileName + str(i + 1) + ".txt",encoding='utf-8') as fin :
			for line in fin:
				word = line.strip()
				extentDict[word] = score
	return extentDict