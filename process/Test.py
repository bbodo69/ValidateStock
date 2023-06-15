import pandas as pd
import module.dataProcessing as dataProcessing
import module.DF_Process as DF_Process
import time

# startTime = time.time()
# df = dataProcessing.GetStockPrice('005930')
#
# dic = dataProcessing.GetMostPriceWithDate(df=df, date='2023.06.13', gubun='저가', day=30, n=2)
#
# print(time.time()-startTime) # 2 초
# print(dic)
#
# trendLine = dataProcessing.getTrandLine(df, dic[1]['날짜'], dic[0]['날짜'], '저가')
#
# print(trendLine)

# dataProcessing.compareTwoDate()

date1 = '2023.05.17'
date2 = '2023.05.18'

print(date1 > date2)
print(date1)