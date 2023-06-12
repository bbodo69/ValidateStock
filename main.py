import os
import module.Common as Common
import module.excel_collection as excel_collection
import module.dataProcessing as dataProcessing
import pandas as pd

rootPath = 'C:/python/101_ValidStock'
inputFolderPath = os.path.join(rootPath, 'input')
outputFolderPath = os.path.join(rootPath, 'output')
resultFolderPath = os.path.join(rootPath, 'result')
imgFolderPath = os.path.join(rootPath, 'img')

masterFilePath = os.path.join(inputFolderPath,'KOSPI.xlsx')
sheetName = 'KOSPI'
resultFilePath = os.path.join(rootPath, 'result.xlsx')

# 이동평균 증감 패턴에 따른 과거 데이터 매도 매수 파악

# 코스피 코드 받아오기
dfKOSPICode = excel_collection.readExcelToDataFrame(masterFilePath, sheetName)
if dfKOSPICode is None:
    print('dfKOSPICode 미존재')
    exit()

# 변수
totalCnt = 0
totalBuyCnt = 0
totalSellCnt = 0

# 코드 DF 작업
for idx, row in dfKOSPICode.iterrows():

    code = row['code']
    dfCode = dataProcessing.GetStockPriceWithPage(code=code, page=100)  # 작업 대상 DF

    # 변수
    cnt = 0
    buyCnt = 0
    sellCnt = 0

    # 조건
    # 이동평균선
    # 자속 상승 하락, 이동평균선 확인가능.
    # 지지, 저항 확인, n일 최하가, 최고가
    
    dicDate = dataProcessing.GetDateFollowingMAPattern(dfCode, 5, 'dduu')

    print(code)
    for i in dicDate:
        print('날짜 : {0}'.format(i))

    # 조건

    break

# 폴더 초기화
# Common.clearFolder(imgFolderPath)

# args = [날짜, 연속일, 퍼센티지]
# return = True or False