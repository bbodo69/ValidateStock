def GetBuySellResultUseDatePriceExpireDate(df, date, buyRate, sellRate, exDate):

    dicResult = {}

    # reverse df
    df = df.loc[::-1]
    df = df.reset_index(drop=True)

    dfDateKey = df.set_index('날짜')
    idxDate = dfDateKey.index.get_loc(date)

    buyResult = False
    dicResult['날짜'] = date

    # 매수
    if df.loc[idxDate]['시가'] * buyRate > df.loc[idxDate]['저가']:
        buyPrice = df.loc[idxDate]['시가'] * buyRate
        sellPrice = buyPrice * sellRate
        buyResult = True

    if not buyResult:

        dicResult['가격'] = df.loc[idxDate]['종가']
        dicResult['소요기간'] = 0
        dicResult['구분'] = 2
        return dicResult

    # 매도
    for i in range(1, exDate):
        if idxDate + i + 1> len(df):
            dicResult['가격'] = df.loc[idxDate]['종가']
            dicResult['소요기간'] = 0
            dicResult['구분'] = 0
            return dicResult

        if df.loc[idxDate+i]['고가'] > sellPrice:
            dicResult['가격'] = df.loc[idxDate]['종가']
            dicResult['소요기간'] = i
            dicResult['구분'] = 1
            return dicResult
    dicResult['가격'] = df.loc[idxDate]['종가']
    dicResult['구분'] = 0

    return dicResult

