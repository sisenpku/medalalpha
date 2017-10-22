# --*-- encoding:utf-8 --*--

import json
import time
import parseHold

class pickStock:
    """
    @summary : 根据得到的基金持仓情况，获得股票详情
    """
    def __init__(self):
        self.result = './result/'

    def pickStockByDiff(self, parseYear, endDate, span, sortRange=50, 
                fundMode=3):
        """
        @summary : 选股票
        """
        parseFund = parseHold.parseFundHold()
        diffResult = parseFund.parseTopDiff(parseYear, endDate, span, sortRange, fundMode)
        diffList = []
        endDate = "".join(endDate.split("-"))
        endDate = str(parseYear) + endDate
        for iter in diffResult:
            tmpList = []
            diffDetail = iter.split("\t")
            diffRatio = float(diffDetail[-1])
            #新股票， 不进入选股池
            if diffRatio == 10000.0:
                continue
            if len(diffDetail[0]) != 6:
                continue
            if diffRatio <= 0.0:
                continue
            tmpList = [diffDetail[0], float(diffDetail[1]), float(diffDetail[2]), float(diffDetail[3])]
            diffList.append(tmpList)
        amountList= sorted(diffList, lambda x, y: cmp(x[1], y[1]), reverse=True) 
        ratioList= sorted(diffList, lambda x, y: cmp(x[3], y[3]), reverse=True) 
        amountStr = []
        freqFile = "./stock/top/" + "topall.freq." + endDate + '.' + str(span) + '.' + str(sortRange)
        freqFile = open(freqFile).readlines()
        freqDict = {}
        for iter in freqFile:
            iter = iter.strip().split("\t")
            freqDict[iter[0]] = iter[1]
        amountJsonList = []
        for iter in amountList:
            try:
                if int(freqDict[iter[0]])  < 2:
                    continue
                amountStr.append(iter[0] + "\t" + str(iter[1]) + "\t" + str(iter[2]) + "\t" + str(iter[3]) + "\t" + freqDict[iter[0]])
                tmpList = [iter[0], iter[1], iter[2], iter[3], freqDict[iter[0]] ]
                amountJsonList.append(tmpList)
            except:
                continue
        ratioStr = []
        for iter in ratioList:
            try:
                if int(freqDict[iter[0]]) < 2:
                    continue
                ratioStr.append(iter[0] + "\t" + str(iter[1]) + "\t" + str(iter[2]) + "\t" + str(iter[3]) + "\t" + freqDict[iter[0]])
            except:
                continue
        amountStr = "\n".join(amountStr)
        ratioStr = "\n".join(ratioStr)
        saveFile = self.result + '/amount/' + endDate + '.' + str(span) + '.' + str(sortRange) 
        open(saveFile, "w").write(amountStr)
        saveFile = self.result + '/ratio/' + endDate + '.' + str(span) + '.' + str(sortRange) 
        open(saveFile, "w").write(amountStr)
        saveFile = self.result+'/amountjson/' + endDate + '.' + str(span) + '.' + str(sortRange)
        jsonStr = json.dumps(amountJsonList)
        open(saveFile, "w").write(jsonStr)

        sortedFile = "./sortedfund/"
        if fundMode is 1:
            saveName = 'topstock.'
        elif fundMode is 2:
            saveName = 'topmix.'
        elif fundMode is 3:
            saveName = 'topall.'
        sortedFile += saveName + endDate + '.' + str(span) + '.' + str(sortRange)
        sortedFile = open(sortedFile).readlines()   
        fundCount = len(sortedFile)
        middleCount = fundCount / 2;
        totalFluctuate = 0.0
        for iter in sortedFile:
            iter = iter.strip().split("\t")
            totalFluctuate += float(iter[1]) 
        maxFluctuate = float(sortedFile[0].strip().split("\t")[1])
        middleFluctuate = float(sortedFile[middleCount].strip().split("\t")[1])
        meanFluctuate = totalFluctuate / fundCount 
        minFluctuate =  float(sortedFile[fundCount - 1].strip().split("\t")[1])
        print "max is " + str(maxFluctuate)
        print "middle is " + str(middleFluctuate)
        print "mean is " + str(meanFluctuate)
        print "min is " + str(minFluctuate)
        
        
if __name__ == "__main__":
    a = pickStock()
    a.pickStockByDiff(2017, "04-20", 45, 50)
