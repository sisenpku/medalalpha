# --*-- encoding:utf-8 --*--

import os
import json
import time
import urllib2
from bs4 import BeautifulSoup as bs

class getFund():
    """
    @summary : 根据基金code，获得持仓情况
    """
    def __init__(self, sortStartDate='', sortEndDate='', detailStartYear=''):
        """
        @summary : 构造函数
        """
        self.topStockUrl = "http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=gp&rs=&gs=0&sc=1yzf&st=desc&sd=" + sortStartDate + "&ed=" + sortEndDate + "&qdii=&tabSubtype=,,,,,&pi=1&pn=50&dx=1&v=0.8995030106537492"
        self.topMixUrl = "http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=hh&rs=&gs=0&sc=1yzf&st=desc&sd=" + sortStartDate + "&ed=" + sortEndDate + "&qdii=&tabSubtype=,,,,,&pi=1&pn=50&dx=1&v=0.29806853523180044"
        #基金详情URL部分
        self.baseUrl = "http://fund.eastmoney.com/f10/FundArchivesDatas.aspx?type=jjcc&code="
        self.postUrl = "&topline=10&year=" + detailStartYear + "&month=12&rt=0.9672935634127076"
        self.startYear = detailStartYear
        self.detailYear = detailStartYear

    def getFundByDate(self):
        """
        @summary : 根据日期，获得指定的基金排行
        @return [('519772', 13.0667), ('470028', 12.4717)]
        """
        url1 = self.topStockUrl
        url2 = self.topMixUrl
    
        stockFund = urllib2.urlopen(url1)
        time.sleep(2)
        mixedFund = urllib2.urlopen(url2)
        stockFund = stockFund.read()
        mixedFund = mixedFund.read()

        stockFund = stockFund.split("=")[1].strip(";")
        mixedFund = mixedFund.split("=")[1].strip(";")
    
        stockFund = stockFund.strip("\n")
        stockFund = stockFund.split("[")
        stockFund = stockFund[1].split("]")[0]
        stockFund = stockFund.split(",")
        count = 0
        stockFundDict = {}
        for iter in stockFund:
            count += 1
            if count % 25 == 1:
                fundCode = iter.strip('"')
            if count % 25 == 9:
                fundRaise = float(iter)
                stockFundDict[fundCode] = fundRaise

        stockFundDict = sorted(stockFundDict.iteritems(), key=lambda asd:asd[1], reverse=True)

        mixedFund = mixedFund.strip("\n")
        mixedFund = mixedFund.split("[")[1].split("]")[0].split(",")
        count = 0
        mixedFundDict = {}
        for iter in mixedFund:
            count += 1
            if count % 25 == 1:
                fundCode = iter.strip('"')
            if count % 25 == 9:
                fundRaise = float(iter)
                mixedFundDict[fundCode] = fundRaise
        mixedFundDict = sorted(mixedFundDict.iteritems(), key=lambda asd:asd[1], reverse=True)
        return stockFundDict, mixedFundDict

    def getFundDetail(self, fundCode, quarter):
        #stockFund, mixedFund = getFundByDate()    
        #stockFund = [item[0] for item in stockFund] 
        #mixedFund = [item[0] for item in mixedFund] 
        url = self.baseUrl + str(fundCode) + self.postUrl

        #最终返回的dict key 为rank， value为
        try:
            result = list(self.getFundHoldDetail(url, fundCode, quarter))
            return result
        except:
            print fundCode  

    def getFundHoldDetail(self, url, fundCode, quarter):
        """
        @根据url，获得基金的持仓情况
        """
        quarterList = [self.startYear + '-03-31', self.startYear + '-06-30', \
                      self.startYear + '-09-30', self.startYear + '-12-31']
        holdDate = quarterList[quarter - 1]
        try:
            urlFile = urllib2.urlopen(url)
            urlContent = urlFile.read()
            urlContent = urlContent.split('content:"')[1]
            urlContent = urlContent.split('",arryear')[0]
            soup = bs(urlContent)
            latestDay = soup.find_all('font')
            indexCount = 0
            for iter in latestDay:
                if iter.get_text().encode('utf-8') in quarterList:
                    indexCount += 1
                if iter.get_text().encode('utf-8') == holdDate:
                    latestDay = holdDate 
                    tableList = soup.find_all('table')
                    holdList =  tableList[indexCount - 1].find_all('tr')
                    count = 0
                    resultList = []
                    for item in holdList:
                        count += 1
                        if count == 1:
                            continue
                        if count >= 12:
                            break
                        attrList = item.find_all('td')
                        result = self.parseAttr(attrList, fundCode)
                        resultList.append(result)
                    return resultList
        except Exception, e:
            return None, fundCode, url

    def parseAttr(self, listAttr, fundCode):
        """
        @summary : 具体解析某一行持仓情况
        """
        count = 0
        stockCode = 0
        href = ''
        ration = 0.0
        totalHold = 0.0
        stockCode = listAttr[1].text.encode("utf-8")
        href = listAttr[1].find_all('a')[0].get('href')
        totalHold = listAttr[-1].text
        try:
            totalHold = totalHold.encode('utf-8')
            totalHold = float(totalHold)
        except:
            index = totalHold.index(',')
            totalHold = totalHold[:index] + totalHold[index+1:]
            totalHold = totalHold.encode("utf-8")
            totalHold = float(totalHold)
        ration = listAttr[-3].text.encode("utf-8").strip("%")
        ration = float(ration) / 100.0
        return fundCode, stockCode, href, ration, totalHold

    def getTopFundHold(self, fundMode, quarter, timeMode=1):
        """
        @summary : 得到所有top基金的持仓情况
        @parmas : fundMode 1 股票型，2 混合型，3 全部
        @parmas : timeMode 1 quater， 2 month
        """
        if timeMode is 1:
            timeStr = ".q"
        elif timeMode is 2:
            timeStr = ".m"
        if fundMode is 1:
            topFilePath = "./funddata/topstock." + self.detailYear + timeStr + str(quarter)
            saveName = "./fundhold/stockhold." + self.detailYear + timeStr + str(quarter) 
        elif fundMode is 2:
            topFilePath = "./funddata/topmix." + self.detailYear + timeStr + str(quarter)
            saveName = "./fundhold/mixhold." + self.detailYear + timeStr + str(quarter) 
        elif fundMode is 3:
            topFilePath = "./funddata/topall." + self.detailYear + timeStr + str(quarter)
            saveName = "./fundhold/allhold." + self.detailYear + timeStr + str(quarter) 
        topFile = open(topFilePath)
        topCodeList = topFile.readlines()
        rank = 0
        retDict = {}
        positiveCount = 0
        for iter in topCodeList:
            fundCode = iter.strip()
            fundCodeAndRaise = iter.split("\t")
            fundCode = fundCodeAndRaise[0]
            raiseRatio = float(fundCodeAndRaise[1])
            if raiseRatio > 0.0:
                positiveCount += 1
            rank += 1
            url = self.baseUrl + str(fundCode) + self.postUrl
            try:
                holdRes = list(self.getFundHoldDetail(url, fundCode, quarter))
            except:
                holdRes = [fundCode, None]
            retDict[rank] = holdRes
        resStr = json.dumps(retDict)
        saveFile = open(saveName, "w")
        saveFile.write(resStr)
        return

    def getAllFundHold(self,  quarter, fundMode=1):
        """
        @summary : 得到所有top基金的持仓情况
        @params : quarter 季度
        @params : fundMode 1 stockFund 2 mixFund
        """
        if fundMode is 1:
            fundCode = os.listdir('fundvalue/stock/')
        elif fundMode is 2: 
            fundCode = os.listdir('fundvalue/mix/')
        rank = 1
        resDict = {}
        for code in fundCode:
            fundCode = code.strip() 
            url = self.baseUrl + str(fundCode) + self.postUrl
            try:
                holdRes = list(self.getFundHoldDetail(url, fundCode, quarter))            
            except:
                holdRes = [fundCode, None]
            print holdRes
            resDict[rank] = holdRes
            rank += 1
        saveName = './allfundhold/' 
        if fundMode is 1:
            saveName += 'stockall.' + str(self.detailYear) + '.q' + str(quarter)
        elif fundMode is 2:
            saveName += 'mixall.' + str(self.detailYear) + '.q' + str(quarter)
        resStr = json.dumps(resDict)
        saveFile = open(saveName, "w")
        saveFile.write(resStr)
        return

if __name__ == "__main__":
    a = getFund(detailStartYear='2016')
    a.getAllFundHold(1,1)
    a.getAllFundHold(1,2)
