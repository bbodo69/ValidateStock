import os
import module.Common as Common
import module.excel_collection as excel_collection
import pandas as pd

rootPath = 'C:\Python_Stocks'
inputFolderPath = os.path.join(rootPath, 'input')
outputFolderPath = os.path.join(rootPath, 'output')
resultFolderPath = os.path.join(rootPath, 'result')
imgFolderPath = os.path.join(rootPath, 'img')

masterFilePath = os.path.join(rootPath, 'Master.xlsx')
sheetName = 'KOSPI'
resultFilePath = os.path.join(rootPath, 'result.xlsx')

# 이동평균 증감 패턴에 따른 과거 데이터 매도 매수 파악

df = excel_collection.readExcelToDataFrame(masterFilePath, sheetName)

# 폴더 초기화
Common.clearFolder(imgFolderPath)