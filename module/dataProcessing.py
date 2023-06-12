import time

import pandas as pd
import warnings
from datetime import datetime, timedelta
import exchange_calendars as ecals
import requests
import operator
from bs4 import BeautifulSoup

startTime = time.time()

######## FutureWarring 방지 ########
warnings.simplefilter(action='ignore', category=FutureWarning)  # FutureWarning 제거


### 한국거래소 영업일 계산
def calculateBusinessDay(day):
    # day = x 일때, x 일전 영업일을 출력]
    XKRX = ecals.get_calendar("XKRX")  # 한국 코드
    day = day * -1
    count = 0
    targetDay = 0
    dayCount = day + 2
    todayDay = ""

    for x in range(dayCount - 1):
        while targetDay != x + 1:
            if XKRX.is_session(datetime.today().date() - timedelta(days=count)):
                targetDay = targetDay + 1
            count = count + 1
        todayDay = str(datetime.today().date() - timedelta(days=count - 1)).replace("-", "")

    return todayDay

def dicHighestPrice(df, day):

    dicResult = {}

    for idx, row in df.iterrows():
        tmpFlag = False

        for i in range(1, day+1):
            if idx + i < len(df):
                if row['고가'] < df.loc[idx + i]['고가']:
                    tmpFlag = True
                    break
            if idx - i > 0:
                if row['고가'] < df.loc[idx - i]['고가']:
                    tmpFlag = True
                    break
        if not tmpFlag:
            dicResult[row['날짜']] = row['고가']

    return dicResult

def dicLowestPrice(df, day):

    dicResult = {}

    for idx, row in df.iterrows():
        tmpFlag = False

        for i in range(1, day+1):
            if idx + i < len(df):
                if row['저가'] > df.loc[idx + i]['저가']:
                    tmpFlag = True
                    break
            if idx - i > 0:
                if row['저가'] > df.loc[idx - i]['저가']:
                    tmpFlag = True
                    break
        if not tmpFlag:
            dicResult[row['날짜']] = row['저가']

    return dicResult

# n 일자 전후로 최소값, 최대값 유지 됬던 날짜의 주식정보
def RemainNDayPriceHighLowPrice(df, day, gubun):
    result = []

    for i in range(0, len(df) - 1):
        bContinue = True

        if gubun.upper() == "HIGH":
            iPrice = df.iloc[i]['고가']
        if gubun.upper() == "LOW":
            iPrice = df.iloc[i]['저가']

        # 최대값 날짜 구하기
        if gubun.upper() == "HIGH":
            if bContinue:
                for j in range(1, day):
                    iTargetDay = i - j
                    if iTargetDay < 0:
                        continue
                    if df.iloc[iTargetDay]['고가'] > iPrice:
                        bContinue = False
                    if not bContinue:
                        break

            if bContinue:
                for j in range(1, day):
                    iTargetDay = i + j
                    if iTargetDay > len(df.index) - 1:
                        continue
                    if df.iloc[iTargetDay]['고가'] > iPrice:
                        bContinue = False
                    if not bContinue:
                        break

        # 최소값 날짜 구하기
        if gubun.upper() == "LOW":
            if bContinue:
                for j in range(1, day):
                    iTargetDay = i - j
                    if iTargetDay < 0:
                        continue
                    if df.iloc[iTargetDay]['저가'] < iPrice:
                        bContinue = False
                    if not bContinue:
                        break

            if bContinue:
                for j in range(1, day):
                    iTargetDay = i + j
                    if iTargetDay > len(df.index) - 1:
                        continue
                    if df.iloc[iTargetDay]['저가'] < iPrice:
                        bContinue = False
                    if not bContinue:
                        break

        if bContinue:
            if len(result) == 0:
                result.append(df.iloc[i]['날짜'] + "^" + str(iPrice) + "^" + str(i))
            else:
                if result[-1].split("^")[1] != str(iPrice):
                    result.append(df.iloc[i]['날짜'] + "^" + str(iPrice) + "^" + str(i))

    return result


def UpPricePre5DayPattern(code):
    df = GetStockPrice(code)
    cntH = 0
    cntL = 0
    pre1 = [cntH, cntL]
    pre2 = [cntH, cntL]
    pre3 = [cntH, cntL]
    pre4 = [cntH, cntL]
    pre5 = [cntH, cntL]

    df = df.reset_index(drop=True)

    dicIndexPattern = {}

    # 종가 상승 마감에 대해 전1일부터 전5일까지의 패턴
    for i in range(0, len(df.index) - 5):
        sTmp = ""
        if df.iloc[i]['종가'] > df.iloc[i]['시가']:  # 종가 상승 마감
            if df.iloc[i + 1]['종가'] > df.iloc[i + 1]['시가']:
                sTmp = "H" + sTmp
            else:
                sTmp = "L" + sTmp
            if df.iloc[i + 2]['종가'] > df.iloc[i + 2]['시가']:
                sTmp = "H" + sTmp
            else:
                sTmp = "L" + sTmp
            if df.iloc[i + 3]['종가'] > df.iloc[i + 4]['시가']:
                sTmp = "H" + sTmp
            else:
                sTmp = "L" + sTmp
            if df.iloc[i + 4]['종가'] > df.iloc[i + 4]['시가']:
                sTmp = "H" + sTmp
            else:
                sTmp = "L" + sTmp
            if df.iloc[i + 5]['종가'] > df.iloc[i + 5]['시가']:
                sTmp = "H" + sTmp
            else:
                sTmp = "L" + sTmp

            if sTmp not in dicIndexPattern.keys():
                dicIndexPattern[sTmp] = 1
            else:
                dicIndexPattern[sTmp] += 1

    print(len(df))
    print(sum(dicIndexPattern.values()))

    # 밸류 값에 대해 내림차순
    dicIndexPattern = sorted(dicIndexPattern.items(), key=operator.itemgetter(1), reverse=True)

    for key in dicIndexPattern:
        print(key)


def ExpectNextHighPrice(code, df):
    try:
        lstLowDays = RemainNDayPriceHighLowPrice(df, 30, "low")
        lstHighDays = RemainNDayPriceHighLowPrice(df, 30, "high")

        if len(lstLowDays) < 3 or len(lstHighDays) < 2:
            return None

        LowDay0 = datetime.strptime(lstLowDays[0].split("^")[0], "%Y.%m.%d")
        LowDay1 = datetime.strptime(lstLowDays[1].split("^")[0], "%Y.%m.%d")
        LowDay2 = datetime.strptime(lstLowDays[2].split("^")[0], "%Y.%m.%d")
        LowPrice0 = int(float(lstLowDays[0].split("^")[1]))
        LowPrice1 = int(float(lstLowDays[1].split("^")[1]))
        LowPrice2 = int(float(lstLowDays[2].split("^")[1]))

        LowDayDiff1 = int(str(LowDay0 - LowDay1).split(" ")[0])
        LowDayDiff2 = int(str(LowDay1 - LowDay2).split(" ")[0])

        LowPriceDiff1 = int(float(LowPrice0) - float(LowPrice1))
        LowPriceDiff2 = int(float(LowPrice1) - float(LowPrice2))
        dayPerLowPrice2 = int(LowPriceDiff2 / LowDayDiff2)

        HighDay1 = datetime.strptime(lstHighDays[0].split("^")[0], "%Y.%m.%d")
        HighDay2 = datetime.strptime(lstHighDays[1].split("^")[0], "%Y.%m.%d")

        HighPrice1 = int(float(lstHighDays[0].split("^")[1]))
        HighPrice2 = int(float(lstHighDays[1].split("^")[1]))

        HighDayDiff2 = int(str(HighDay1 - HighDay2).split(" ")[0])
        HighDayDiff1 = (LowDayDiff1 + LowDayDiff2 + HighDayDiff2) / 3

        # 계산값
        ExpectHighDay0 = HighDay1 + timedelta(days=HighDayDiff1)
        ExpectLowDay0 = LowDay1 + timedelta(days=HighDayDiff1)

        ExpectLowPrice0 = int(dayPerLowPrice2 * HighDayDiff1 + LowPrice1)
        ExpectHighPrice1 = int(dayPerLowPrice2 * HighDayDiff1 + HighPrice2)

        ExpectActHighPrice0 = dayPerLowPrice2 * LowDayDiff1 + HighPrice1
        ExpectAsmHighPrice0 = dayPerLowPrice2 * LowDayDiff1 + ExpectHighPrice1

        # 조건 예외사항 뽑기

        if ExpectHighDay0 < LowDay0:
            return None
        if LowDay0 < HighDay1:
            return None
        if ExpectLowPrice0 * 1.1 <= LowPrice0 or ExpectLowPrice0 * 0.9 >= LowPrice0:
            return None
        if ExpectHighPrice1 * 1.1 <= HighPrice1 or ExpectHighPrice1 * 0.9 >= HighPrice1:
            return None

        sReturn = "{0}" \
                  "code : {1}{0}" \
                  "ExpectLowDay0 : {2}{0}" \
                  "LowDay0 : {3}{0}" \
                  "LowDay1 : {4}{0}" \
                  "LowDay2 : {5}{0}" \
                  "LowPrice0 : {6}{0}{0}" \
                  "ExpectHighDay0 : {7}{0}" \
                  "HighDay1 : {8}{0}" \
                  "HighDay2 : {9}{0}" \
                  "ExpectActHighPrice0 : {10}{0}" \
                  "ExpectActHighPrice1 : {11}{0}" \
                  "LowPriceDiff1 : {12}{0}" \
            .format("<br>", code,
                    ExpectLowDay0.strftime("%Y.%m.%d"),
                    LowDay0.strftime("%Y.%m.%d"),
                    LowDay1.strftime("%Y.%m.%d"),
                    LowDay2.strftime("%Y.%m.%d"),
                    LowPrice0,
                    ExpectHighDay0.strftime("%Y.%m.%d"),
                    HighDay1.strftime("%Y.%m.%d"),
                    HighDay2.strftime("%Y.%m.%d"),
                    ExpectActHighPrice0,
                    ExpectAsmHighPrice0,
                    LowPriceDiff1)

    except Exception as e:
        return str(code) + "\n" + str(e)

    return sReturn


def GetStockPrice(code):
    # 한국 지수별 가격정보 가져오기

    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36'}
    df = pd.DataFrame()

    url = "https://finance.naver.com/item/sise_day.naver?code={}&page={}".format(code, 1)
    res = requests.get(url, headers={'User-agent': 'Mozilla/5.0'})
    
    html = BeautifulSoup(res.text, 'lxml')

    pgrr = html.find('td', class_='pgRR').a['href']

    page = 25

    if page > int(pgrr.split("=")[-1]) + 1: # 총 페이지 보다 높으면 마지막 페이지 가져오기
        page = int(pgrr.split("=")[-1]) + 1

    for page in range(1, page):
        url = "https://finance.naver.com/item/sise_day.naver?code={}&page={}".format(code, page)
        res = requests.get(url, headers={'User-agent': 'Mozilla/5.0'})
        df = pd.concat([df, pd.read_html(res.text, header=0)[0]], axis=0)

    # df.dropna()를 이용해 결측값 있는 행 제거
    df = df.dropna()
    df = df.reset_index(drop=False)

    return df

def GetStockPriceWithPage(code, page):
    # 한국 지수별 가격정보 가져오기

    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36'}
    time = datetime.today().strftime('%Y%m%d')
    time = str(time)+("180000")

    url = "https://finance.naver.com/item/sise_day.naver?code={}&page={}".format(code, 1)
    res = requests.get(url, headers={'User-agent': 'Mozilla/5.0'})
    html = BeautifulSoup(res.text, 'lxml')
    pgrr = html.find('td', class_='pgRR').a['href']

    if page == -1 : # page 를 -1 로 했을 경우 전체 페이지 가져오기
        page = pgrr.split("=")[-1]
        page = int(page)+1

    if page > int(pgrr.split("=")[-1]) + 1: # 총 페이지 보다 높으면 마지막 페이지 가져오기
        page = int(pgrr.split("=")[-1]) + 1
        
    df = pd.DataFrame()
    for i in range(1, page):
        url = "https://finance.naver.com/item/sise_day.naver?code={}&page={}".format(code, time, i)
        res = requests.get(url, headers={'User-agent': 'Mozilla/5.0'})
        df = pd.concat([df, pd.read_html(res.text, header=0)[0]], axis=0)

    # df.dropna()를 이용해 결측값 있는 행 제거
    df = df.dropna()
    df = df.reset_index(drop=False)

    return df

def GetStockPriceMinute(code):
    # 한국 지수별 가격정보 가져오기

    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36'}
    time = datetime.today().strftime('%Y%m%d')
    time = str(time)+("180000")

    url = "https://finance.naver.com/item/sise_time.naver?code={}&thistime={}&page={}".format(code, time, 1)
    res = requests.get(url, headers={'User-agent': 'Mozilla/5.0'})
    html = BeautifulSoup(res.text, 'lxml')
    pgrr = html.find('td', class_='pgRR').a['href']
    page = pgrr.split("=")[-1]
    page = int(page)+1
    df = pd.DataFrame()
    for i in range(1, page):
        url = "https://finance.naver.com/item/sise_time.naver?code={}&thistime={}&page={}".format(code, time, i)
        res = requests.get(url, headers={'User-agent': 'Mozilla/5.0'})
        df = pd.concat([df, pd.read_html(res.text, header=0)[0]], axis=0)

    # df.dropna()를 이용해 결측값 있는 행 제거
    df = df.dropna()
    df = df.reset_index(drop=False)

    return df

def CheckReturnPosition(df, gubun, countTick):

    tick = GetTickFromMinuteDF(df)
    max = int(df.max()['체결가'])
    min = int(df.min()['체결가'])
    currentPrice = df.loc[0]['체결가']
    diffTickPrice = tick * countTick

    if gubun.upper() == 'UP':
        if currentPrice == max - diffTickPrice or currentPrice == max - diffTickPrice - tick:
            print("UP체결시각 : {0}, 체결가 : {1}".format(df.loc[0]['체결시각'], df.loc[0]['체결가']))
            return currentPrice

    if gubun.upper() == 'DOWN':
        if currentPrice == min + diffTickPrice or currentPrice == min + diffTickPrice + tick:
            print("DOWN체결시각 : {0}, 체결가 : {1}".format(df.loc[0]['체결시각'], df.loc[0]['체결가']))
            return currentPrice

def CheckReturnPositionInOrder(df, gubun, countTick):

    tick = GetTickFromMinuteDF(df)
    max = 0
    min = 9999999
    diffTickPrice = tick * countTick

    df = df.loc[::-1]

    if gubun.upper() == 'UP':

        for idx, row in df.iterrows():
            if row['체결가'] > max:
                max = row['체결가']
            if row['체결가'] + diffTickPrice == max:
                print("UP체결시각 : {0}, 체결가 : {1}".format(row['체결시각'], row['체결가']))

        if gubun.upper() == 'DOWN':

            for idx, row in df.iterrows():
                if row['체결가'] < min:
                    min = row['체결가']
                if row['체결가'] - diffTickPrice == min:
                    print("UP체결시각 : {0}, 체결가 : {1}".format(row['체결시각'], row['체결가']))

def GetTickFromDF(df):
    '''
    호가 단위
    2천원 미만  1원
    2천원 이상  ~5천원 미만	    5원
    5천원 이상  ~2만원 미만	    10원
    2만원 이상  ~5만원 미만	    50원
    5만원 이상  ~20만원 미만	    100원
    20만원 이상 ~50만원 미만	    500원
    50만원 이상              	1,000원
    '''

    price = int(df.iloc[0]['시가'])

    if price < 2000:
        return 1
    elif 2000 <= price < 5000:
        return 5
    elif 5000 <= price < 20000:
        return 10
    elif 20000 <= price < 50000:
        return 50
    elif 50000 <= price < 200000:
        return 100
    elif 200000 <= price < 500000:
        return 500
    elif 500000 <= price:
        return 1000

def GetTickFromMinuteDF(df):
    '''
    호가 단위
    2천원 미만  1원
    2천원 이상  ~5천원 미만	    5원
    5천원 이상  ~2만원 미만	    10원
    2만원 이상  ~5만원 미만	    50원
    5만원 이상  ~20만원 미만	    100원
    20만원 이상 ~50만원 미만	    500원
    50만원 이상              	1,000원
    '''

    df = df.iloc[::-1]
    price = int(df.iloc[0]['체결가'])

    if price < 2000:
        return 1
    elif 2000 <= price < 5000:
        return 5
    elif 5000 <= price < 20000:
        return 10
    elif 20000 <= price < 50000:
        return 50
    elif 50000 <= price < 200000:
        return 100
    elif 200000 <= price < 500000:
        return 500
    elif 500000 <= price:
        return 1000

def GetMovingAverage(df, day):
    # 이동평균선 계산
    dic = {}

    for idx, row in df.iterrows():

        if idx + day > len(df):
            break

        n = day

        tmp = 0
        for j in range(0, n):
            tmp += int(df.loc[idx + j]['종가'])
        movingAverage = tmp / n
        movingAverage = int(movingAverage)

        dic[row['날짜']] = movingAverage

    return dic

def GetDateFollowingMAPattern(df, day, gubun):
    # GetPositionUseMA
    # df에 증감이 gubun을 따르는 day이동평균 인 지점을 dic['날짜'] = value 로 return

    # 이동평균 구하기
    dic = {}
    dicResult = {}

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', -1)

    for idx, row in df.iterrows():
        if idx + day > len(df):
            break

        n = day
        tmp = 0

        for j in range(0, n):
            tmp += int(df.loc[idx + j]['종가'])

        movingAverage = tmp / n
        movingAverage = int(movingAverage)
        dic[row['날짜']] = movingAverage

    for idx, key in enumerate(dic):

        if len(dic) < idx + len(gubun) + 1:
            break
        for idxJ, c in enumerate(gubun[::-1]):

            tmpFlag = False
            if c == 'u':
                if list(dic.values())[idx + idxJ] <= list(dic.values())[idx + idxJ + 1]:
                    tmpFlag = True
                    break
            if c == 'd':
                if list(dic.values())[idx + idxJ] >= list(dic.values())[idx + idxJ + 1]:
                    tmpFlag = True
                    break

        if tmpFlag == False:
            dicResult[key] = dic[key]

    return dicResult

def GetMV(df, day):
    # df에 증감이 gubun을 따르는 day이동평균 인 지점을 dic['날짜'] = value 로 return

    # 이동평균 구하기
    dic = {}

    for idx, row in df.iterrows():
        if idx + day > len(df):
            break

        n = day
        tmp = 0

        for j in range(0, n):
            tmp += int(df.loc[idx + j]['종가'])

        movingAverage = tmp / n
        movingAverage = int(movingAverage)
        dic[row['날짜']] = movingAverage

    return dic

def GetMVPattern(dic, gubun):

    dicResult = {}

    for idx, key in enumerate(dic):
        if len(dic) < idx + len(gubun) + 1:
            break

        check = True

        for idxJ, c in enumerate(gubun[::-1]):
            if c == 'u':
                if list(dic.values())[idx + idxJ] <= list(dic.values())[idx + idxJ + 1]:
                    check = False
                    break
            if c == 'd':
                if list(dic.values())[idx + idxJ] >= list(dic.values())[idx + idxJ + 1]:
                    check = False
                    break

        if check:
            dicResult[key] = dic[key]

    return dicResult

def checkStockSplit(df, day):
    for idx, row in df.iterrows():
        if idx > day:
            return True

        if idx + 1 > len(df):
            return True

        if df.loc[idx]['종가'] > df.loc[idx + 1]['종가'] * 1.6:
            print(idx)
            return False
        if df.loc[idx]['종가'] < df.loc[idx + 1]['종가'] * 0.4:
            print(idx)
            return False


def standardizationStockSplit(df):
    global gab

    gab = 1
    totalGab = 1

    for idx, row in df.iterrows():

        if idx + 2 > len(df):
            break

        gabCheck = True

        if df.loc[idx]['종가'] + df.loc[idx]['전일비'] == df.loc[idx + 1]['종가'] or df.loc[idx]['종가'] - df.loc[idx]['전일비'] == \
                df.loc[idx + 1]['종가']:
            gabCheck = False

        if gabCheck:
            if df.loc[idx]['종가'] > df.loc[idx + 1]['종가']:
                gab = (df.loc[idx]['종가'] - df.loc[idx]['전일비']) / df.loc[idx + 1]['종가']
                if totalGab != 1:
                    df.iloc[idx, df.columns.get_loc('종가')] = int(df.loc[idx]['종가'] * totalGab)
                    df.iloc[idx, df.columns.get_loc('시가')] = int(df.loc[idx]['시가'] * totalGab)
                    df.iloc[idx, df.columns.get_loc('고가')] = int(df.loc[idx]['고가'] * totalGab)
                    df.iloc[idx, df.columns.get_loc('저가')] = int(df.loc[idx]['저가'] * totalGab)
                totalGab = gab * totalGab
                continue

            if df.loc[idx]['종가'] < df.loc[idx + 1]['종가']:
                gab = (df.loc[idx]['종가'] + df.loc[idx]['전일비']) / df.loc[idx + 1]['종가']
                if totalGab != 1:
                    df.iloc[idx, df.columns.get_loc('종가')] = int(df.loc[idx]['종가'] * totalGab)
                    df.iloc[idx, df.columns.get_loc('시가')] = int(df.loc[idx]['시가'] * totalGab)
                    df.iloc[idx, df.columns.get_loc('고가')] = int(df.loc[idx]['고가'] * totalGab)
                    df.iloc[idx, df.columns.get_loc('저가')] = int(df.loc[idx]['저가'] * totalGab)
                totalGab = gab * totalGab
                continue

        if totalGab != 1:
            df.iloc[idx, df.columns.get_loc('종가')] = int(df.loc[idx]['종가'] * totalGab)
            df.iloc[idx, df.columns.get_loc('시가')] = int(df.loc[idx]['시가'] * totalGab)
            df.iloc[idx, df.columns.get_loc('고가')] = int(df.loc[idx]['고가'] * totalGab)
            df.iloc[idx, df.columns.get_loc('저가')] = int(df.loc[idx]['저가'] * totalGab)

    df = df.iloc[:-1]

    return df

'''
        # 병합
        if df.loc[idx]['종가'] > df.loc[idx+1]['종가'] * 1.3:
            gab = gab * (df.loc[idx]['종가'] - df.loc[idx]['전일비']) / df.loc[idx+1]['종가']
            totalGab = totalGab * gab
            print(df.loc[idx]['날짜'])
            print(totalGab)
            continue

        # 분할
        if df.loc[idx]['종가'] < df.loc[idx+1]['종가'] * 0.7:
            tmpGab = df.loc[idx + 1]['종가'] / (df.loc[idx]['종가'] + df.loc[idx]['전일비'])
            gab = 1/tmpGab
            totalGab = totalGab * gab
            print(df.loc[idx]['날짜'])
            print(totalGab)
            continue

        if totalGab != 1:
            df.iloc[idx, df.columns.get_loc('종가')] = df.loc[idx]['종가'] * totalGab
            df.iloc[idx, df.columns.get_loc('시가')] = df.loc[idx]['시가'] * totalGab
            df.iloc[idx, df.columns.get_loc('고가')] = df.loc[idx]['고가'] * totalGab
            df.iloc[idx, df.columns.get_loc('저가')] = df.loc[idx]['저가'] * totalGab
    df = df.iloc[:-1]

    return df
'''

# 최신 최저가 최고가 구하기
def getFirstHighLowPrice(df, day, gubun1, gubun2):
    # gunun1 = n 일 동안 고, 저 유지
    # gubun2 = 최고, 최저

    ret = 0

    return ret

def getSecondHighLowPrice(df, date, day, gubun):
    # date = 시작되는 date
    # day = n 일 동안 고, 저 유지
    # gunun = n 일 동안 고, 저 유지

    ret = 0

    return ret

def getGubunPriceUseDate(df, listDate):

    # 날짜 데이터를 가지고, 종가, 고가, 저가, 시가 가져오기
    dicResult = {}

    dfDateKey = df.set_index('날짜')

    for i in listDate:
        dicResult[i] = {}
        dicResult[i]['종가'] = dfDateKey.loc[i]['종가']
        dicResult[i]['고가'] = dfDateKey.loc[i]['고가']
        dicResult[i]['저가'] = dfDateKey.loc[i]['저가']
        dicResult[i]['시가'] = dfDateKey.loc[i]['시가']

    return dicResult






def checkStockSplit(df, day):
    for idx, row in df.iterrows():
        if idx > day:
            return True

        if idx + 1 > len(df):
            return True

        if df.loc[idx]['종가'] > df.loc[idx + 1]['종가'] * 1.6:
            print(idx)
            return False
        if df.loc[idx]['종가'] < df.loc[idx + 1]['종가'] * 0.4:
            print(idx)
            return False


def standardizationStockSplit(df):
    startStockSplit = False

    for idx, row in df.iterrows():
        if idx + 2 > len(df):
            break

        # 병합
        if df.loc[idx]['종가'] > df.loc[idx + 1]['종가'] * 1.6 and not startStockSplit:
            startStockSplit = True
            gab = (df.loc[idx]['종가'] + df.loc[idx]['전일비']) // df.loc[idx + 1]['종가']
            continue

        # 분할
        if df.loc[idx]['종가'] < df.loc[idx + 1]['종가'] * 0.4 and not startStockSplit:
            startStockSplit = True
            gab = df.loc[idx + 1]['종가'] // (df.loc[idx]['종가'] - df.loc[idx]['전일비'])
            gab = 1 / gab
            continue

        if startStockSplit:
            df.iloc[idx, df.columns.get_loc('종가')] = df.loc[idx]['종가'] * gab
            df.iloc[idx, df.columns.get_loc('시가')] = df.loc[idx]['시가'] * gab
            df.iloc[idx, df.columns.get_loc('고가')] = df.loc[idx]['고가'] * gab
            df.iloc[idx, df.columns.get_loc('저가')] = df.loc[idx]['저가'] * gab

    return df