# --*-- encoding:utf-8 --*--

import json
import time
import fundSort

class parseFundHold:
    """
    @summary : 根据得到的基金持仓情况，获得股票详情
    """
    def __init__(self):
        self.holdPath = './fundhold/'
        self.savePath = './result/'


    def parseStock(self, startYear, endDate, span, sortRange=50,fundMode=3):
        """
        @summary : 获得top基金的持仓情况
        @params : fundMode 1 股票型 2 混合型 3 全部
        @params : startYear 分析持仓年份
        @params : quarter 分析持仓的季度
        @params : parseMode 1 为持仓份额分析， 2 为持仓频率分析
        """
        if fundMode is 1:
            fundHoldPath = self.holdPath  + "stockhold."
            modeStr = "topstock"
        elif fundMode is 2:
            fundHoldPath = self.holdPath + "mixhold."
            modeStr = "topmix"
        elif fundMode is 3:
            fundHoldPath = self.holdPath + "allhold."
            modeStr = "topall"
        quarter = self.getQuarter(startYear, endDate) 
        if quarter is 1:
            parseYear = startYear - 1
            quarter = 4
        else:
            parseYear = startYear
            quarter -= 1
        try:
            endTime = str(startYear) + '-' + endDate
            saveFile = ''.join(endTime.split('-'))
            sortedFile = "./sortedfund/" + modeStr + '.' + saveFile + '.' + str(span) + "." + str(sortRange)
            sortedFund= open(sortedFile).readlines()
            sortedFundList = [(x.strip().split("\t")[0], x.strip().split("\t")[1]) for x in sortedFund]
        except:
            sortedFund = fundSort.fundSort()
            sortedFundList = sortedFund.sortFund(startYear, endDate, span, sortRange, fundMode)

        fundCode = [x[0] for x in sortedFundList]
        
        mixFundStr = './allfundhold/' + 'mixall.'  + str(parseYear) + '.q' + str(quarter) 
        stockFundStr = './allfundhold/' + 'stockall.'  + str(parseYear) + '.q' + str(quarter) 
        mixFund = open(mixFundStr).readlines()[0]
        mixFund = json.loads(mixFund)
        stockFund = open(stockFundStr).readlines()[0]
        stockFund = json.loads(stockFund)
        
        allFundDict = {}
        for iter in mixFund:
            try:
                allFundDict[mixFund[iter][0][0]] = mixFund[iter]
            except:
                pass
        for iter in stockFund:
            try:
                allFundDict[stockFund[iter][0][0]] = mixFund[iter]
            except:
                pass
        
        stockFreqDict = {}
        stockShareDict = {}
        stockAmountDict = {}
        for iter in fundCode:
            try:
                holdDetail = allFundDict[iter]
            except:
                continue
            for item in holdDetail:
                try:
                    stockCode = item[1].encode('utf-8')
                    stockShare = float(item[3])
                    stockAmount = float(item[4])
                    if stockCode not in stockFreqDict:
                        stockFreqDict[stockCode] = 1
                    else:
                        stockFreqDict[stockCode] += 1
                    if stockCode not in stockShareDict:
                        stockShareDict[stockCode] = stockShare
                    else:
                        stockShareDict[stockCode] += stockShare
                    if stockCode not in stockAmountDict:
                        stockAmountDict[stockCode] = stockAmount
                    else:
                        stockAmountDict[stockCode] += stockAmount
                except:
                    continue
        sortedFreq = sorted(stockFreqDict.items(), lambda x, y: cmp(x[1], y[1]), reverse=True) 
        sortedShare = sorted(stockShareDict.items(), lambda x, y: cmp(x[1], y[1]), reverse=True) 
        sortedAmount = sorted(stockAmountDict.items(), lambda x, y: cmp(x[1], y[1]), reverse=True) 
        sortedFreqList = [x[0] + "\t" + str(x[1]) for x in sortedFreq]
        sortedShareList = [x[0] + "\t" + str(x[1]) for x in sortedShare]
        sortedAmountList = [x[0] + "\t" + str(x[1]) for x in sortedAmount]
        
        freqStr = "\n".join(sortedFreqList)
        shareStr = "\n".join(sortedShareList)
        amountStr = "\n".join(sortedAmountList)
        
        dateStr = ''.join(endDate.split("-"))
        freqSaveName = "./stock/top/" + modeStr + "." + "freq." + str(startYear) + dateStr + "." + str(span) + "." + str(sortRange)
        shareSaveName = "./stock/top/" + modeStr + '.' + "share." + str(startYear) + dateStr + "." + str(span) + "." + str(sortRange)
        amountSaveName = "./stock/top/" + modeStr + "." + "amount." + str(startYear) + dateStr + "." + str(span) + "." + str(sortRange)
        freqFile = open(freqSaveName, "w")
        shareFile = open(shareSaveName, "w")
        amountFile = open(amountSaveName, "w")
        
        freqFile.write(freqStr)
        shareFile.write(shareStr)
        amountFile.write(amountStr)
        return sortedAmountList

    def parseDiff(self, startYear, quarter, timeMode=1):
        """
        @summary 分析持仓变动， 找出变动的股票
        @summary timeMode 1 quarter 2 month
        """
        if timeMode is 1:
            timeStr = ".q"
        elif timeMode is 2:
            timeStr = ".m"

        endFile = "./stock/allamount." + str(startYear) + timeStr + str(quarter)  

        if quarter is 1:
            startYear -= 1
            quarter = 4
        else:
            quarter -= 1
        
        startFile = "./stock/allamount." + str(startYear) + timeStr + str(quarter)  
        
        endFile = open(endFile).readlines()
        startFile = open(startFile).readlines()
        endDict = {}
        startDict = {}
        for iter in endFile:
            iter = iter.strip()
            iter = iter.split("\t")
            endDict[iter[0]] = float(iter[1])

    def parseAll(self, year, quarter):
        """
        @summary 所有基金的持仓情况
        @params : year 分析持仓的月份
        @params : quarter 季度
        """
        mixFund = './allfundhold/mixall.' + str(year) + ".q" + str(quarter)
        stockFund = './allfundhold/stockall.' + str(year) + ".q" + str(quarter)
        mixFund = open(mixFund).readlines()[0]
        stockFund = open(stockFund).readlines()[0]
        mixFund = json.loads(mixFund)
        stockFund = json.loads(stockFund)
        stockDict = {} 
        for fund in mixFund:
            fundDetail = mixFund[fund]
            if None in fundDetail:
                continue
            for stock in fundDetail:
                stockCode = stock[1]
                stockHold = stock[-1]
                if stockCode not in stockDict:
                    stockDict[stockCode] = stockHold
                else:
                    stockDict[stockCode] += stockHold

        for fund in stockFund:
            fundDetail = stockFund[fund]
            if None in fundDetail:
                continue
            for stock in fundDetail:
                stockCode = stock[1]
                stockHold = stock[-1]
                if stockCode not in stockDict:
                    stockDict[stockCode] = stockHold
                else:
                    stockDict[stockCode] += stockHold

        sortedHold = sorted(stockDict.items(), lambda x, y: cmp(x[1], y[1]), reverse=True) 
        sortedList = [x[0] + "\t" + str(x[1]) for x in sortedHold]
        resStr = "\n".join(sortedList)
        saveName = "./stock/allstock/allstock." + str(year) + ".q" + str(quarter) 
        saveFile = open(saveName, "w")
        saveFile.write(resStr)
        return
    
    def parseAllDiff(self, startYear, quarter):
        """
        @summary : 对持仓变动情况进行分析
        """
        endPath = "./stock/allstock/allstock." + str(startYear) + '.q' + str(quarter) 
        savePath = "./stock/alldiff/alldiff." + str(startYear) + '.q' + str(quarter)
        ratioSavePath = "./stock/alldiff/alldiffratio." + str(startYear) + '.q' + str(quarter)
        if quarter is 1:
            startYear -= 1
            quarter = 4
        else:
            quarter -= 1
        print endPath
        startPath = "./stock/allstock/allstock." + str(startYear) + '.q' + str(quarter) 
        print startPath

        startFile = open(startPath).readlines()
        endFile = open(endPath).readlines()
        startDict = {} 
        endDict = {}
        
        for iter in startFile:
            iter = iter.strip().split("\t")
            startDict[iter[0]] = float(iter[1])
        for iter in endFile:
            iter = iter.strip().split("\t")
            endDict[iter[0]] = float(iter[1])
        
        diffDict = {}
        for stockCode in endDict:
            if stockCode in startDict:
                diffDict[stockCode] = endDict[stockCode] - startDict[stockCode] 
            else:
                diffDict[stockCode] = endDict[stockCode]

        sortedDiff = sorted(diffDict.items(), lambda x, y: cmp(x[1], y[1]), reverse=True) 
        sortedList = [x[0] + "\t" + str(x[1]) + "\t" + str(endDict[x[0]])  for x in sortedDiff] 
        count = 0
        for stock in sortedList:
            stockList = stock.split("\t")  
            diffHold = float(stockList[1])
            endHold = float(stockList[2])
            stockCode = stockList[0]
            try:
                if stockCode in startDict:
                    diffRatio = (diffHold / startDict[stockCode]) * 100.0
                else:
                    diffRatio = 10000.0
            except:
                    diffRatio = 10000.0
            tmpStr = "\t" + str(diffRatio)
            sortedList[count] = sortedList[count] + tmpStr
            count += 1
        saveStr = "\n".join(sortedList)  
        open(savePath, "w").write(saveStr)
        ratioDict = {}
        for stock in sortedList:
            stockDetail = stock.split("\t") 
            stockCode = stockDetail[0]
            diff = stockDetail[1]
            endHold = stockDetail[2]
            diffRatio = float(stockDetail[3])
            ratioDict[stockCode] = [diff, endHold, diffRatio]
        sortedDiff = sorted(ratioDict.items(), lambda x, y: cmp(x[1][2], y[1][2]), reverse=True) 
        sortedList = [x[0] + "\t" + x[1][0] + "\t" + x[1][1] + "\t" + str(x[1][2])  for x in sortedDiff] 
        ratioStr = "\n".join(sortedList)
        open(ratioSavePath, "w").write(ratioStr)
        return sortedList
    

    def parseTopDiff(self, parseYear, endDate, span, sortRange=50, 
                fundMode=3):
        """
        @summary 分析持仓变动， 找出变动的股票
        @summary timeMode 1 quarter 2 month
        """
        """
        得到top
        """
        if fundMode is 1:
            saveName = 'topstock.'
        elif fundMode is 2:
            saveName = 'topmix.'
        elif fundMode is 3:
            saveName = 'topall.'
        try:
            endTime = str(parseYear) + '-' + endDate
            saveFile = ''.join(endTime.split('-'))
            sortedFile = "./sortedfund/" + saveName + saveFile + '.' + str(span)  + '.' + str(sortRange)
            sortedFund = open(sortedFile).readlines()
            sortedFundList = [(x.strip().split("\t")[0], x.strip().split("\t")[1]) for x in sortedFund]
        except Exception, e:
            sortedFund = fundSort.fundSort()
            sortedFundList = sortedFund.sortFund(parseYear, endDate, span, sortRange, fundMode)

        quarter = self.getQuarter(parseYear, endDate)
        if quarter is 1:
            year = parseYear - 1 
            quarter = 4
        else:
            year = parseYear
            quarter -= 1
        if fundMode is 1:
            modeStr = "topstock"
        elif fundMode is 2:
            modeStr = "topmix"
        elif fundMode is 3:
            modeStr = "topall"
        try:
            endFile= "./stock/top/" + modeStr + "." + "amount." + str(parseYear) + "." + str(span) + "." + str(sortRange)
            endFile = open(endFile).readlines()
        except:
            endFile = self.parseStock(parseYear, endDate, span, sortRange,fundMode)

        topHoldList = []
        for iter in endFile:
            iter = iter.strip()
            iter = iter.split("\t")
            topHoldList.append([iter[0], float(iter[1])])
        
        try:
            diffFile = "./stock/alldiff/alldiff." + str(year) + ".q" + str(quarter) 
            diffFile = open(diffFile).readlines()
        except:
            diffFile = self.parseAllDiff(year, quarter) 
        diffDict = {} 
        for iter in diffFile:
            iter = iter.strip().split("\t")
            diffDict[iter[0]] = [iter[1], iter[2], iter[3]]
    
        topDiffList = []
        for iter in topHoldList:
            try:
                tmpStr = "\t".join(diffDict[iter[0]])
                topDiffList.append(iter[0] + "\t" + tmpStr)
            except:
                continue
        resStr = "\n".join(topDiffList)
        endDate = "".join(endDate.split("-"))
        saveStr =  "./stock/topdiff/topdiff." + str(parseYear) + str(endDate) + '.' + str(span) + '.' + str(sortRange)
        open(saveStr, "w").write(resStr)
        return topDiffList

    def getQuarter(self, parseYear, endDate):
        """
        @summary : 根据传入的时间，计算季度
        """
        parseDate = str(parseYear) + '-' + endDate 
        endArr = time.strptime(parseDate, "%Y-%m-%d")
        parseTimeStamp = int(time.mktime(endArr))

        q1 = str(parseYear) + '-03-31'
        q1Arr = time.strptime(q1, "%Y-%m-%d")
        q1 = int(time.mktime(q1Arr))

        q2 = str(parseYear) + '-06-30'
        q2Arr = time.strptime(q2, "%Y-%m-%d")
        q2 = int(time.mktime(q2Arr))

        q3 = str(parseYear) + '-09-30'
        q3Arr = time.strptime(q3, "%Y-%m-%d")
        q3 = int(time.mktime(q3Arr))

        q4 = str(parseYear) + '-12-31'
        q4Arr = time.strptime(q4, "%Y-%m-%d")
        q4 = int(time.mktime(q4Arr))

        if parseTimeStamp <= q1:
            return 1
        if parseTimeStamp <= q2:
            return 2
        if parseTimeStamp <= q3:
            return 3
        if parseTimeStamp <= q4:
            return 4

        

if __name__ == "__main__":
    a = parseFundHold()
    #a.parseTopDiff(2016, "01-20", 30, 60)
    b = a.parseAllDiff(2016, 2)
