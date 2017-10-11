# --*-- encoding:utf-8 --*--

import json
import time

class parseFundHold:
    """
    @summary : 根据得到的基金持仓情况，获得股票详情
    """
    def __init__(self):
        self.holdPath = './fundhold/'
        self.savePath = './result/'


    def parseStock(self, fundMode, startYear, quarter, timeMode=1):
        """
        @summary : 获得前述的的基金持仓情况
        @params : fundMode 1 股票型 2 混合型 3 全部
        @params : startYear 分析持仓年份
        @params : quarter 分析持仓的季度
        @params : parseMode 1 为持仓份额分析， 2 为持仓频率分析
        """
        if fundMode is 1:
            fundHoldPath = self.holdPath + "stockhold."
            modeStr = "stock"
        elif fundMode is 2:
            fundHoldPath = self.holdPath + "mixhold."
            modeStr = "mix"
        elif fundMode is 3:
            fundHoldPath = self.holdPath + "allhold."
            modeStr = "all"
        if timeMode is 1:
            timeStr = '.q'
        elif timeMode is 2:
            timeStr = '.m'
        fundHoldPath += str(startYear) + timeStr + str(quarter)
        fundHoldFile = open(fundHoldPath)
        fundHoldRes = fundHoldFile.read()
        fundHoldRes = json.loads(fundHoldRes)
        
        stockFreqDict = {}
        stockShareDict = {}
        stockAmountDict = {}
        for iter in fundHoldRes:
            holdDetail = fundHoldRes[iter]
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
        
        freqSaveName = "./stock/" + modeStr + "freq." + str(startYear) + timeStr + str(quarter)
        shareSaveName = "./stock/" + modeStr + "share." + str(startYear) + timeStr + str(quarter)
        amountSaveName = "./stock/" + modeStr + "amount." + str(startYear) + timeStr + str(quarter)
        freqFile = open(freqSaveName, "w")
        shareFile = open(shareSaveName, "w")
        amountFile = open(amountSaveName, "w")
        
        freqFile.write(freqStr)
        shareFile.write(shareStr)
        amountFile.write(amountStr)

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
        startPath = "./stock/allstock/allstock." + str(startYear) + '.q' + str(quarter) 

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
    
    def parseTopDiff(self, year, quarter, timeMode=1):
        """
        @summary 分析持仓变动， 找出变动的股票
        @summary timeMode 1 quarter 2 month
        """
        if timeMode is 1:
            timeStr = ".q"
        elif timeMode is 2:
            timeStr = ".m"

        endFile = "./stock/allamount." + str(year) + timeStr + str(quarter)  

        diffFile = "./stock/alldiff/alldiff." + str(year) + ".q" + str(quarter) 
        endFile = open(endFile).readlines()
        diffFile = open(diffFile).readlines()
        topHoldList = []
        for iter in endFile:
            iter = iter.strip()
            iter = iter.split("\t")
            topHoldList.append([iter[0], float(iter[1])])

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
        saveStr =  "./stock/topdiff/topdiff." + str(year) + timeStr + str(quarter)
        open(saveStr, "w").write(resStr)
        
if __name__ == "__main__":
    a = parseFundHold()
    a.parseTopDiff(2016, 3, 1)
    a.parseTopDiff(2016, 3, 2)
    a.parseTopDiff(2016, 4, 1)
    a.parseTopDiff(2016, 4, 2)
