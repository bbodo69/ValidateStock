import module.dataProcessing as dataProcessing

dfCode = dataProcessing.GetStockPrice("005930")

temp = dataProcessing.getUpDownMV(df=dfCode, day=60, date="2022.11.03")
print(temp)
temp = dataProcessing.getUpDownMV(df=dfCode, day=60, date="2022.11.04")
print(temp)
temp = dataProcessing.getUpDownMV(df=dfCode, day=60, date="2022.11.07")
print(temp)
temp = dataProcessing.getUpDownMV(df=dfCode, day=60, date="2022.11.08")
print(temp)