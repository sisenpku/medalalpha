# --*-- encoding:utf-8 --*--

import os
import json
import time
import urllib2
from bs4 import BeautifulSoup as bs
from getAllFund import getAllFund

class getFundValue:
    """
    @summary : 获取所有天天基金网上的基金代码
    """

    def __init__(self, stockFundFile='./funddata/stockFundCode', mixFundFile='./funddata/mixFundCode'):
        """
        @summary : 初始化函数 设定per为300
        """
        self.baseUrl = 'http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&per=500&sdate=&edate=&rt=0.01649088312777347&page=1&code='
        self.stockFile = stockFundFile
        self.mixFile = mixFundFile
        self.succStock = './fundvalue/stock/'
        self.succMix = './fundvalue/mix/'
        

    def getAllFundFromFile(self, fundMode):
        """
        @summary : 从存储文件中得到需要的基金代码 
        @params : fundMode  1 为股票型基金
                            2 为混合型基金
        """
        if fundMode == 1:
            fundFile = self.stockFile
            filePath = self.succStock
        else:
            fundFile = self.mixFile
            filePath = self.succMix
        fundList = os.listdir(filePath)
        return fundList

    def getValue(self, fundMode):
        """
        @summary : 根据基金代码获得基金每日净值
        """
        fundList = self.getAllFundFromFile(fundMode)
        baseSavePath = './fundvalue/'
        if fundMode == 1:
            baseSavePath += 'stock/'
        else:
            baseSavePath += 'mix/'
        succCount = 0
        for iter in fundList:
            try:
                url = self.baseUrl + iter
                valueFile = urllib2.urlopen(url)
                valueContent = valueFile.read()
                valueContent = valueContent.split('content:"')[1].split('",records')[0]
                soup = bs(valueContent)
                lineCount = 0
                valueStr = ''
                for item in soup.select('tr'):
                    lineCount += 1
                    if lineCount == 1:
                        continue
                    valueDetail = item.select('td')
                    valueDate = valueDetail[0].text
                    value = valueDetail[1].text
                    valueStr += valueDate + "\t" + value + "\n"
                saveFilePath = baseSavePath + iter
                saveFile = open(saveFilePath, "w")
                saveFile.write(valueStr)
                succCount += 1
                print "get fund " + iter + str(succCount) 
            except:
                time.sleep(4)
                pass
        return

    def updateFund(self, fundMode=1):
        """
        @summary : 每日更新基金净值
        @params : fundMode 1 stock 2 mix
        """
        allFund = getAllFund() 
        fundValue = allFund.getFund(fundMode)[1]
        if fundMode == 1:
            filePath = self.succStock
        else:
            filePath = self.succMix
        timeNow = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        fundCount = len(fundValue)
        succCount = 0
        for fundCode in fundValue:
            valueDict = fundValue[fundCode]
            for iter in valueDict:
                if valueDict[iter] != None:
                    try:
                        fundFile = filePath + fundCode
                        if os.path.exists(fundFile) == True:
                            fundDetail = open(fundFile).readlines()
                            dateList = [x.split("\t")[0] for x in fundDetail]
                            if iter in dateList:
                                continue 
                        resStr = iter + "\t" + valueDict[iter] + "\n"
                        if os.path.exists(fundFile) == True:
                            fund = open(fundFile, "a")
                        else:
                            fund = open(fundFile, "w")
                        fund.write(resStr)
                        print fundCode
                        fund.close()
                        succCount += 1
                    except Exception, e:
                        pass
        print succCount 
        print fundCount
    
    def updateFundValue(self):
        """
        @summary : 每日更新基金数据
        """
        updateRes = True
        failCount = 0
        while updateRes:
            try: 
                self.updateFund(1)
                updateRes = False
            except Exception, e:
                print e
                failCount += 1
                if failCount != 10:
                    updateRes = True
                else:
                    updateRes = False
                    print "try fail 10 times"
        updateRes = True
        failCount = 0
        while updateRes:
            try:
                self.updateFund(2)
                updateRes = False
            except:
                failCount += 1
                if failCount != 10:
                    updateRes = True
                else:
                    updateRes = False
                    print "try mix fund fail 10 times"
                
if __name__ == '__main__':
    b = getFundValue()
    #b.updateFundValue()
    a = b.getValue(1)
    a = b.getValue(2)
