import os
import module.Common as Common
import module.excel_collection as excel_collection
import module.dataProcessing as dataProcessing
import pandas as pd

rootPath = 'C:\Python_Stocks'
inputFolderPath = os.path.join(rootPath, 'input')
outputFolderPath = os.path.join(rootPath, 'output')
resultFolderPath = os.path.join(rootPath, 'result')
imgFolderPath = os.path.join(rootPath, 'img')

masterFilePath = os.path.join(inputFolderPath, 'Master.xlsx')
sheetName = 'KOSPI'
resultFilePath = os.path.join(resultFolderPath, 'result.xlsx')

# 이동평균 증감 패턴에 따른 과거 데이터 매도 매수 파악

df = excel_collection.readExcelToDataFrame(masterFilePath, sheetName) # 코스피 코드 받아오기

for idx, row in df.iterrows():

    dfCode = dataProcessing.GetStockPrice(row['code'])

    # 배당락, 병합, 분할 표준화
    dfCode = dataProcessing.standardizationStockSplit(dfCode)
    
    # 코드별 조건 검사


# 폴더 초기화
Common.clearFolder(imgFolderPath)