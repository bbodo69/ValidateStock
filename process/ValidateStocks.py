import os
import module.Common as Common
import module.excel_collection as excel_collection
import module.dataProcessing as dataProcessing
import module.resultBuySell as resultBuySell
import module.Sort_DF as Sort_Df
import module.Image as Image
import pandas as pd

rootPath = 'C:\Python_Stocks'
inputFolderPath = os.path.join(rootPath, 'input')
outputFolderPath = os.path.join(rootPath, 'output')
resultFolderPath = os.path.join(rootPath, 'result')
imgFolderPath = os.path.join(rootPath, 'img')

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

# 폴더 초기화
Common.clearFolder(imgFolderPath)

df = excel_collection.readExcelToDataFrame(masterFilePath, sheetName)  # 코스피 코드 받아오기

for idx, row in df.iterrows():

    if row['code'] != '000020':
        continue

    # 초기화
    dfCode = dataProcessing.GetStockPrice(row['code'])
    dicScatterDate = {}
    imgFilePath = os.path.join(imgFolderPath, row['code'] + 'png')

    cnt = 0
    cnt0 = 0
    cnt1 = 0
    cnt2 = 0
    period = 0

    # 배당락, 병합, 분할 표준화
    dfCode = dataProcessing.standardizationStockSplit(dfCode)

    # 코드 이동평균선 뽑아오기
    dicMV = dataProcessing.GetMV(dfCode, 5)
    
    # 종목의 이동평균선 패턴 따르는 일자 리턴 
    dicMVPatten = dataProcessing.GetMVPattern(dicMV, 'dduu')

    print(dicMVPatten)

    # 날짜 list 의 가격 정보를 리턴
    dicGubunPrice = dataProcessing.getGubunPriceUseDate(dfCode, list(dicMVPatten.keys()))

    print(dicGubunPrice)

    for i in dicMVPatten.keys():
        # 날짜, 매수날종가, 소요기간, 구분 리턴
        dicBuySellResult = resultBuySell.GetBuySellResultUseDatePriceExpireDate(df=dfCode, date=i, buyRate=0.99, sellRate=1.025, exDate=50)
        dicScatterDate[i] = {}
        dicScatterDate[i]['가격'] = dicBuySellResult['가격']
        dicScatterDate[i]['구분'] = dicBuySellResult['구분']
        if dicBuySellResult['구분'] == 0:
            cnt0 += 1
            totalCnt0 += 1
        elif dicBuySellResult['구분'] == 1:
            period += int(dicBuySellResult['소요기간'])
            cnt1 += 1
            totalCnt1 += 1
        elif dicBuySellResult['구분'] == 2:
            cnt2 += 1
            totalCnt2 += 1
        cnt += 1
        totalCnt += 1

    if cnt1 != 0 :
        avgPeriod = round(period / cnt1, 2)

    totalSellPeriod += period

    if totalSellPeriod != 0 :
        avgSellPeriod = round(totalSellPeriod / totalCnt1, 2)

    Image.SaveDFImageWithScatter2(df = dfCode, x = '날짜', y = '종가', dicScatterData = dicScatterDate, title = row['code'], savePath = imgFilePath)

    dfTotal.loc[len(dfTotal)] = {'종목코드': row['code'], 'totalCnt': totalCnt, 'totalCnt0': totalCnt0, 'totalCnt1': totalCnt1, 'totalCnt2': totalCnt2, 'period' : avgPeriod, 'avgPeriod' : avgSellPeriod}

    excel_collection.saveDFToNewExcel(resultFilePath, 'result', dfTotal)

    print('{0} / {1} ::: totalCnt : {2}, totalCnt0 : {3}, totalCnt1 : {4}, totalCnt2 : {5}'.format(idx + 1, len(df), totalCnt, totalCnt0, totalCnt1, totalCnt2))

