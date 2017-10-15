# --*-- encoding:utf-8 --*--

import os
import time
import numpy as np

class fundSort:
    """
    @summary : 获得所有基金的净值增长情况
    """

    def __init__(self):
        """
        @summary : 初始化函数
        """
        self.stockFile = './fundvalue/stock/'
        self.mixFile = './fundvalue/mix/'
        self.saveFile = './sortedfund/'
        
    def getAllFile(self, fundMode):
        """
        @summary : 获得所有存储基金净值数据的目录下的文件
        @params : fundMode 1 为stock
        @parmas : fundMode 2 为mix
        """
        if fundMode is 1:
            filePath = self.stockFile
        else:
            filePath = self.mixFile
        allFile = os.listdir(filePath)
        return allFile
        

    def loadDataSet(self, fundMode=1):
        """
        @summary : 从存储文件中，获得基金的净值数据 
        @params : fundMode  1 为股票型基金
                            2 为混合型基金
        """
        if fundMode == 1:
            fundFilePath = self.stockFile
        else:
            fundFilePath = self.mixFile
        
        fundFile = self.getAllFile(fundMode)
        retDict = {}
        for iter in fundFile:
            filePath = fundFilePath + iter
            tmpFile = open(filePath) 
            tmpFund = tmpFile.readlines()  
            tmpDict = {}
            for item in tmpFund:
                try:
                    item = item.strip().split("\t")
                    timeStr = item[0]
                    timeArr = time.strptime(timeStr, "%Y-%m-%d")
                    timeStamp = int(time.mktime(timeArr))
                    value = float(item[1])
                    tmpDict[timeStamp] = value
                except:
                    continue
            retDict[iter] = tmpDict
        return retDict

    def sortFund(self, parseYear, endDate, span, sortRange=50, fundMode=3):
        """
        @summary : 对所有的基金净值情况进行排序
        @params : fundMode 1 股票型 2 混合型 3 全部
        @params : startDate
        @params: span 排序的时间跨度
        @params: sortRange 取前多少位的基金
        """
        endDate = str(parseYear) + '-' + endDate
        saveDate = "".join(endDate.split("-"))
        if fundMode is 1 or fundMode is 2:
            dataDict = self.loadDataSet(fundMode)
        elif fundMode is 3:
            stockDict = self.loadDataSet(1)
            mixDict = self.loadDataSet(2)
            dataDict = dict(stockDict.items() + mixDict.items()) 

        endArr = time.strptime(endDate, "%Y-%m-%d")
        endTimeStamp = int(time.mktime(endArr))

        startTimeStamp = endTimeStamp - 3600 * 24 * span
        
        timeStampList = dataDict.values()[0].keys()
        while startTimeStamp not in timeStampList:
            startTimeStamp = startTimeStamp - 3600 * 24
        while endTimeStamp not in timeStampList:
            endTimeStamp = endTimeStamp - 3600 * 24
        
        roseDict = {} 
        for iter in dataDict:
            try:
                startValue = dataDict[iter][startTimeStamp]
                endValue = dataDict[iter][endTimeStamp]
                roseSpan = (endValue - startValue) / startValue
                roseDict[iter] = roseSpan
            except Exception,e:
                continue
        retList= sorted(roseDict.items(), lambda x, y: cmp(x[1], y[1]), reverse=True) 
        positiveList = [[x[0], x[1]] for x in retList if float(x[1]) > 0]
        topList = retList[:sortRange]
        topCode = [x[0] + "\t" + str(x[1]) for x in topList]
        retStr = '\n'.join(topCode)
        if fundMode is 1:
            saveName = 'topstock.'
        elif fundMode is 2:
            saveName = 'topmix.'
        elif fundMode is 3:
            saveName = 'topall.'
        saveName += saveDate + '.' + str(span) + '.' + str(sortRange)
        savePath = self.saveFile + saveName
        saveFile = open(savePath, 'w')
        saveFile.write(retStr)
        return topList

if __name__ == "__main__":
    a = fundSort()
    a.sortFund(2017, "10-13",1, 2)
