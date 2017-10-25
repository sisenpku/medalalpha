# --*-- encoding:utf-8 --*--

import json
import time
import urllib2
from bs4 import BeautifulSoup as bs

class getAllFund:
    """
    @summary : 获取所有天天基金网上的基金代码
    """
    
    def __init__(self):
    
        self.stockFundUrl = "http://fund.eastmoney.com/Data/Fund_JJJZ_Data.aspx?t=1&lx=2&letter=&gsid=&text=&sort=zdf,desc&page=1,9999&feature=|&dt=1506617436923&atfc=&onlySale=0"
        self.mixFundUrl = "http://fund.eastmoney.com/Data/Fund_JJJZ_Data.aspx?t=1&lx=3&letter=&gsid=&text=&sort=zdf,desc&page=1,9999&feature=|&dt=1506617604490&atfc=&onlySale=0"

    def getFund(self, fundMode=1):
        """
        @summary : 获得所有基金的代码
        @parmas : fundMode 1 股票型 2 混合型
        """
        if fundMode == 1:
            url = self.stockFundUrl
        else:
            url = self.mixFundUrl
        fundFile = urllib2.urlopen(url)
        fundContents = fundFile.read()
        showDay = fundContents.split(',showday:')[1]
        showDay = showDay.split('","')
        endDay = showDay[0].strip('["')
        startDay = showDay[1].strip('"]}')
        fundContentsList = fundContents.split("chars:")
        fundContents = fundContentsList[1].split(",count:")[0]
        fundContents = fundContents.split("datas:")[1]
        fundList = fundContents.split('["')[1:]
        fund = []
        fundDict = {}
        for iter in fundList:
            try:
                tmpList = iter.split('",')
                fundCode = tmpList[0]
                fund.append(fundCode)
                endValue = tmpList[3].strip('"')
                startValue = tmpList[5].strip('"')
                if len(endValue) < 3:
                    endValue = None
                if len(startValue) < 3:
                    startValue = None
                fundDict[fundCode] = {startDay:startValue, endDay:endValue}
            except:
                continue
        return fund, fundDict
    
    def getFundCode(self):
        """
        @summary : 获得股票型以及混合型基金的代码
        """
        stockFund = self.getFund(1)[0]
        mixFund = self.getFund(2)[0]
        stockFundStr = "\n".join(stockFund)
        mixFundStr = "\n".join(mixFund)
        stockFundFile = open("./data/funddata/stockFundCode","w")
        stockFundFile.write(stockFundStr)
        mixFundFile = open("./data/funddata/mixFundCode", "w")
        mixFundFile.write(mixFundStr)
        return [stockFund, mixFund]
        
        

if __name__ == '__main__':
    fundHandler = getAllFund() 
    fundHandler.getFund()
