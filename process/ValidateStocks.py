import os
import module.Common as Common
import module.excel_collection as excel_collection
import module.dataProcessing as dataProcessing
import module.resultBuySell as resultBuySell
import module.Sort_DF as Sort_Df
import module.Image as Image
import pandas as pd
import datetime

rootPath = 'C:\Python_Stocks'
inputFolderPath = os.path.join(rootPath, 'input')
outputFolderPath = os.path.join(rootPath, 'output')
resultFolderPath = os.path.join(rootPath, 'result')
imgFolderPath = os.path.join(rootPath, 'imgMV')

masterFilePath = os.path.join(inputFolderPath, 'Master.xlsx')
sheetName = 'KOSPI'
resultFilePath = os.path.join(resultFolderPath, 'result.xlsx')

dfTotal = pd.DataFrame(columns=['종목코드', 'totalCnt', 'totalCnt0', 'totalCnt1', 'totalCnt2', 'period', 'avgPeriod'])

avgSellPriod = 0
totalSellPeriod = 0
totalCnt = 0
totalCnt0 = 0
totalCnt1 = 0
totalCnt2 = 0

# 이동평균 증감 패턴에 따른 과거 데이터 매도 매수 파악

df = excel_collection.readExcelToDataFrame(masterFilePath, sheetName)  # 코스피 코드 받아오기

def usingMostPrice():
    # 폴더 초기화
    Common.clearFolder(imgFolderPath)

    for idx, row in df.iterrows():
        #
        # if row['code'] != '003570':
        #     continue

        # 초기화
        dfCode = dataProcessing.GetStockPrice(row['code'])
        dicScatterDate = {}
        imgFilePath = os.path.join(imgFolderPath, row['code'] + 'png')

        # 배당락, 병합, 분할 표준화
        dfCode = dataProcessing.standardizationStockSplit(dfCode)
        targetDate = datetime.datetime.now().strftime('%Y.%m.%d')
        targetDate = '2023.06.27'

        dicMostHighPrice = dataProcessing.GetMostPriceBeforeTargetDate(df=dfCode , targetDate=targetDate, day=7, gubun="고가", n=30)
        dicMostLowPrice = dataProcessing.GetMostPriceBeforeTargetDate(df=dfCode, targetDate=targetDate, day=7, gubun="저가", n=30)

        dicMostHighPriceScatter = {}
        dicMostLowPriceScatter = {}

        if dicMostHighPrice is None or dicMostLowPrice is None:
            continue

        for i in dicMostHighPrice :
            dicMostHighPriceScatter[dicMostHighPrice[i]['날짜']] = dicMostHighPrice[i]['가격']

        for i in dicMostLowPrice :
            dicMostLowPriceScatter[dicMostLowPrice[i]['날짜']] = dicMostLowPrice[i]['가격']

        Image.SaveDFImageWithScatter3(df = dfCode, x = '날짜', dicScatterData = dicScatterDate, dicTotalHighPrice=dicMostHighPriceScatter, dicTotalLowPrice=dicMostLowPriceScatter, title = row['code'], savePath = imgFilePath)

        print('{0} / {1} ::: totalCnt : {2}, totalCnt0 : {3}, totalCnt1 : {4}, totalCnt2 : {5}'.format(idx + 1, len(df), totalCnt, totalCnt0, totalCnt1, totalCnt2))

def useMVPattern():
    # 폴더 초기화
    Common.clearFolder(imgFolderPath)

    iBuyCnt = 0
    iSellCnt = 0
    iSellProfitCnt = 0
    iSellLossCnt = 0
    iNotSellCnt = 0

    for idx, row in df.iterrows():
        print(row['code'])
        #
        # if row['code'] != '003570':
        #     continue

        # 초기화
        dfCode = dataProcessing.GetStockPrice(row['code'])
        dicScatterDate = {}
        imgFilePath = os.path.join(imgFolderPath, row['code'] + 'png')

        # 배당락, 병합, 분할 표준화
        dfCode = dataProcessing.standardizationStockSplit(dfCode)
        dic = dataProcessing.GetDateFollowingMAPattern(df=dfCode, day=5, gubun='dduu')

        # dicMost = dataProcessing.GetMostPriceBeforeTargetDate(df=dfCode, day=15, n=5, gubun='저가', targetDate='2023.07.13')
        # dicMost = dataProcessing.GetMostPriceFromDF(df=dfCode, day=15, n=5, gubun='저가', targetDate='2023.07.13')
        dicMost = dataProcessing.GetMostPriceBeforeAfter(df=dfCode, before=15, after=3, n=5, gubun='저가', targetDate='2023.07.13')

        print(dicMost)

        # idx 키 값 날짜.
        dfDateKey = dfCode.set_index('날짜')

'''
        # 이동평균 따르는 dic 반복
        for i in dic:
            upDownMV = dataProcessing.getUpDownMV(df=dfCode, day=60, date=i)

            if upDownMV != 0:
                continue

            isSell = False
            idxTargetDate = dfDateKey.index.get_loc(i)
            buyPrice = dfCode.loc[idxTargetDate]['시가'] * 0.995
            sellPrice = buyPrice * 1.025
            dicMost = dataProcessing.GetMostPriceFromDF(df=dfCode, targetDate=i, day=7, n=2, gubun='고가')
            # print("{0} < {1} = {2}".format(buyPrice, dfCode.loc[idxTargetDate]['저가'], buyPrice < dfCode.loc[idxTargetDate]['저가']))

            # 비어있으면 넘기기
            if dicMost is None:
                continue

            # 고가 2개 미만이면 넘기기.
            if len(dicMost) < 2:
                continue

#### 넘길 조건 추가 영영 ###
            # 최근 고가가 이전 고가보다 가격이 낮으면 넘기기.
            if dicMost[0]['가격'] < dicMost[1]['가격'] :
                continue

#########################

            # 사지 못하는 경우
            if buyPrice < dfCode.loc[idxTargetDate]['저가']:
                continue

            # 밑에는 사는 경우.
            iBuyCnt += 1

            # 위 날짜 데이터 이후 날짜들 확인
            for j in range(0, idxTargetDate + 1):
                tmpIdx = idxTargetDate - j
                if tmpIdx < 0 :
                    break
                # 익절
                if sellPrice < dfCode.loc[tmpIdx]['고가']:
                    # dicScatterDate[dfCode.loc[idxTargetDate]['날짜']] = {}
                    # dicScatterDate[dfCode.loc[idxTargetDate]['날짜']]['가격'] = buyPrice
                    # dicScatterDate[dfCode.loc[idxTargetDate]['날짜']]['구분'] = 1
                    iSellProfitCnt += 1
                    isSell = True

                # 손절
                # if buyPrice * 0.97 > dfCode.loc[tmpIdx]['저가']:
                #     dicScatterDate[dfCode.loc[idxTargetDate]['날짜']] = {}
                #     dicScatterDate[dfCode.loc[idxTargetDate]['날짜']]['가격'] = buyPrice
                #     dicScatterDate[dfCode.loc[idxTargetDate]['날짜']]['구분'] = 0
                #     iSellLossCnt += 1
                #     isSell = True

                if isSell:
                    break

            # 팔리지 않은 경우
            if not isSell:
                dicScatterDate[dfCode.loc[idxTargetDate]['날짜']] = {}
                dicScatterDate[dfCode.loc[idxTargetDate]['날짜']]['가격'] = buyPrice
                dicScatterDate[dfCode.loc[idxTargetDate]['날짜']]['구분'] = 0
                iNotSellCnt += 1
                print("날짜 : {0}, 가격 : {1} / 날짜 : {2}, 가격 : {3}".format(dicMost[0]['날짜'], dicMost[0]['가격'], dicMost[1]['날짜'], dicMost[1]['가격']))

                dicScatterDate[dicMost[0]['날짜']] = {}
                dicScatterDate[dicMost[0]['날짜']]['가격'] = dicMost[0]['가격']
                dicScatterDate[dicMost[0]['날짜']]['구분'] = 3
                dicScatterDate[dicMost[1]['날짜']] = {}
                dicScatterDate[dicMost[1]['날짜']]['가격'] = dicMost[1]['가격']
                dicScatterDate[dicMost[1]['날짜']]['구분'] = 4

        if len(dicScatterDate) > 0 :
            Image.SaveDFImageWithScatter2(df=dfCode, savePath=imgFilePath, dicScatterData=dicScatterDate, x='날짜', y='종가', title=row['code'])

        print("{0}/{1} | {2}, {3}, {4}".format(idx + 1, len(df), iBuyCnt, iSellProfitCnt, iNotSellCnt))
'''
useMVPattern()