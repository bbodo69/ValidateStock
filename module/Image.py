import matplotlib.pyplot as plt
import module.dataProcessing as dataProcessing
import os

def SaveDFImage(code, df, sFilePath):
    tmpFolder = os.path.dirname(sFilePath)

    if not os.path.isdir(tmpFolder):
        os.makedirs(tmpFolder)

    # df 를 이미지로 저장
    plt.plot(df['날짜'], df['종가'])

    plt.title(code)
    # plt.legend(loc='upper left')
    plt.gca().invert_xaxis()  # x 축 반전
    plt.xticks([0, len(df) / 2, len(df) - 1], rotation=30)  # x 축 thick 지정 갯수 출력
    plt.savefig(sFilePath)
    plt.clf()


def SaveDFImageMinute(code, df, sFilePath):
    # df 를 이미지로 저장
    plt.plot(df['체결시각'], df['체결가'])

    plt.title(code)
    # plt.legend(loc='upper left')
    plt.gca().invert_xaxis()  # x 축 반전
    plt.xticks([0, len(df) / 2, len(df) - 1], rotation=30)  # x 축 thick 지정 갯수 출력
    plt.savefig(sFilePath)
    plt.clf()


def SaveDFImageWithScatter(code, df, sFilePath):
    lstHighDayPriceIdx = dataProcessing.RemainNDayPriceHighLowPrice(df, 30, "High")
    lstLowDayPriceIdx = dataProcessing.RemainNDayPriceHighLowPrice(df, 30, "Low")

    # df 를 이미지로 저장
    # plt.plot(df['날짜'], df['종가'], label=code)
    plt.plot(df['날짜'], df['종가'])

    for i in lstHighDayPriceIdx:
        xPoint = i.split("^")[0]
        yPoint = int(float(i.split("^")[1]))
        plt.scatter(xPoint, yPoint, color="red")  # 위치에 점 찍기

    for i in lstLowDayPriceIdx:
        xPoint = i.split("^")[0]
        yPoint = int(float(i.split("^")[1]))
        plt.scatter(xPoint, yPoint, color="Blue")  # 위치에 점 찍기

    # plt.grid(color='gray', linestyle='--')
    plt.title(code)
    # plt.legend(loc='upper left')
    plt.gca().invert_xaxis()  # x 축 반전
    plt.xticks([0, len(df) / 2, len(df) - 1], rotation=30)  # x 축 thick 지정 갯수 출력
    plt.savefig(sFilePath)
    plt.clf()


def SaveDFImageWithScatter2(df, x, y, dicScatterData, title, savePath):
    '''
    :param df: 네이버 주식 시세 df, dataProcess.GetStockInfo 결과값
    :param x: x 축, 날짜
    :param y: y 축, 종가
    :param dicScatterData: key : '날짜',  value : ['가격', '구분']
    :param title: 이미지 상당 제목명
    :param savePath: 이미지 파일 저장위치
    :return:
    '''

    color = 'blue'

    # df 를 이미지로 저장
    plt.plot(df[x], df[y])

    # for i in dicScatterData:
    #     print(i)
    # print(dicScatterData)

    for i in dicScatterData:
        xPoint = i
        yPoint = dicScatterData[i]['가격']

        if dicScatterData[i]['구분'] == 0:
            color = 'blue'
        elif dicScatterData[i]['구분'] == 1:
            color = 'red'
        elif dicScatterData[i]['구분'] == 2:
            color = 'black'

        plt.scatter(xPoint, yPoint, color=color)  # 위치에 점 찍기

    # plt.grid(color='gray', linestyle='--')
    plt.title(title)
    # plt.legend(loc='upper left')
    plt.gca().invert_xaxis()  # x 축 반전
    plt.xticks([0, len(df) / 2, len(df) - 1], rotation=30)  # x 축 thick 지정 갯수 출력
    plt.savefig(savePath)
    plt.clf()


def SaveDFImageAddInfo(code, df, sFilePath, iBuyPrice, iExpectPrice, sExpectHighDay0):
    # df 를 이미지로 저장
    # plt.plot(df['날짜'], df['종가'], label=code)
    plt.plot(df['날짜'], df['종가'])

    # y 라인 그리기
    plt.axhline(y=iBuyPrice, color='Black', linestyle='-')
    plt.axhline(y=iExpectPrice, color='Blue', linestyle='-')
    plt.text(0, iBuyPrice * 1.02, str(iBuyPrice))
    plt.text(0, iExpectPrice * 0.98, str(iExpectPrice))

    # plt.scatter(xPoint, yPoint, color="red")  # 위치에 점 찍기
    # plt.text(xPoint, yPoint, str(yPoint))  # 위치에 텍스트 추가

    # 그리드 설정
    # plt.grid(color='gray', linestyle='--')
    plt.title(str(code) + " / " + sExpectHighDay0)
    # plt.legend(loc='upper left')
    plt.gca().invert_xaxis()  # x 축 반전
    plt.xticks([0, len(df) / 2, len(df) - 1], rotation=30)  # x 축 thick 지정 갯수 출력
    plt.savefig(sFilePath)
    plt.clf()


def SaveDFImageWithBuyPrice(code, df, sFilePath, iBuyPrice):
    # df 를 이미지로 저장
    # plt.plot(df['날짜'], df['종가'], label=code)
    plt.plot(df['날짜'], df['종가'])

    # y 라인 그리기
    plt.axhline(y=iBuyPrice, color='Black', linestyle='-')
    plt.text(0, iBuyPrice * 1.02, str(iBuyPrice))

    # plt.scatter(xPoint, yPoint, color="red")  # 위치에 점 찍기
    # plt.text(xPoint, yPoint, str(yPoint))  # 위치에 텍스트 추가

    # 그리드 설정
    # plt.grid(color='gray', linestyle='--')
    plt.title(str(code))
    # plt.legend(loc='upper left')
    plt.gca().invert_xaxis()  # x 축 반전
    plt.xticks([0, len(df) / 2, len(df) - 1], rotation=30)  # x 축 thick 지정 갯수 출력
    plt.savefig(sFilePath)
    plt.clf()
    plt.close("all")


def SaveDFImageWithScatter2(df, x, y, dicScatterData, title, savePath):
    '''
    :param df: 네이버 주식 시세 df, dataProcess.GetStockInfo 결과값
    :param x: x 축
    :param y: y 축
    :param dicScatterData: key : '날짜',  value : ['가격', '구분']
    :param title: 이미지 상당 제목명
    :param savePath: 이미지 파일 저장위치
    :return:
    '''
    # df 를 이미지로 저장
    plt.plot(df[x], df[y])

    # for i in dicScatterData:
    #     print(i)
    # print(dicScatterData)
    for i in dicScatterData:
        xPoint = i
        yPoint = dicScatterData[i]['가격']

        if dicScatterData[i]['구분'] == 0:
            color = 'blue'
            facecolor = 'blue'
        elif dicScatterData[i]['구분'] == 1:
            color = 'red'
            facecolor = 'none'
        elif dicScatterData[i]['구분'] == 2:
            color = 'black'
            facecolor = 'black'
        elif dicScatterData[i]['구분'] == 3:
            color = 'Green'
            facecolor = 'Green'
        elif dicScatterData[i]['구분'] == 4:
            color = 'Yellow'
            facecolor = 'Yellow'
        plt.scatter(xPoint, yPoint, color=color, facecolor=facecolor)  # 위치에 점 찍기

    # plt.grid(color='gray', linestyle='--')
    plt.title(title)
    # plt.legend(loc='upper left')
    plt.gca().invert_xaxis()  # x 축 반전
    plt.xticks([0, len(df) / 2, len(df) - 1], rotation=30)  # x 축 thick 지정 갯수 출력
    plt.savefig(savePath)
    plt.clf()
    plt.close("all")

def SaveDFImageWithScatter3(df, x, dicScatterData, dicTotalHighPrice, dicTotalLowPrice, title, savePath):
    '''
    :param df: 네이버 주식 시세 df, dataProcess.GetStockInfo 결과값
    :param x: x 축
    :param y: y 축
    :param dicScatterData: key : '날짜',  value : ['가격', '구분']
    :param title: 이미지 상당 제목명
    :param savePath: 이미지 파일 저장위치
    :return:
    '''

    # df 를 이미지로 저장
    plt.figure(figsize=(20, 15))
    plt.plot(df[x], df['종가'], label = 'end')
    plt.plot(df[x], df['고가'], label='high', linestyle='dashed')
    plt.plot(df[x], df['저가'], label='low', linestyle='dashed')

    # for i in dicScatterData:
    #     print(i)
    # print(dicScatterData)

    for i in dicScatterData:
        xPoint = i
        yPoint = dicScatterData[i]['가격']

        if dicScatterData[i]['구분'] == 0:
            color = 'blue'
        elif dicScatterData[i]['구분'] == 1:
            color = 'red'
        elif dicScatterData[i]['구분'] == 2:
            color = 'black'

        plt.scatter(xPoint, yPoint, color=color, s=100)  # 위치에 점 찍기

    for i in dicTotalLowPrice:
        xPoint = i
        yPoint = dicTotalLowPrice[i]
        plt.scatter(xPoint, yPoint, color='yellow', s=100)  # 위치에 점 찍기

    for i in dicTotalHighPrice:
        xPoint = i
        yPoint = dicTotalHighPrice[i]
        plt.scatter(xPoint, yPoint, color='green', s=100)  # 위치에 점 찍기

    # plt.grid(color='gray', linestyle='--')
    plt.title(title)
    # plt.legend(loc='upper left')
    plt.gca().invert_xaxis()  # x 축 반전
    plt.xticks([0, len(df) / 2, len(df) - 1], rotation=30)  # x 축 thick 지정 갯수 출력

    plt.savefig(savePath)
    plt.clf()
    plt.close("all")

def SaveDFImageWithScatter4(df, x, dicScatterData, title, savePath):
    '''
    :param df: 네이버 주식 시세 df, dataProcess.GetStockInfo 결과값
    :param x: x 축
    :param y: y 축
    :param dicScatterData: key : '날짜',  value : ['가격', '구분']
    :param title: 이미지 상당 제목명
    :param savePath: 이미지 파일 저장위치
    :return:
    '''

    # df 를 이미지로 저장
    plt.figure(figsize=(20, 15))
    plt.plot(df[x], df['종가'], label = 'end')
    plt.plot(df[x], df['고가'], label='high', linestyle='dashed')
    plt.plot(df[x], df['저가'], label='low', linestyle='dashed')

    # for i in dicScatterData:
    #     print(i)
    # print(dicScatterData)

    for i in dicScatterData:
        xPoint = i
        yPoint = dicScatterData[i]['가격']

        if dicScatterData[i]['구분'] == 0:
            color = 'blue'
        elif dicScatterData[i]['구분'] == 1:
            color = 'red'
        elif dicScatterData[i]['구분'] == 2:
            color = 'black'

        plt.scatter(xPoint, yPoint, color=color)  # 위치에 점 찍기

    # plt.grid(color='gray', linestyle='--')
    plt.title(title)
    # plt.legend(loc='upper left')
    plt.gca().invert_xaxis()  # x 축 반전
    plt.xticks([0, len(df) / 2, len(df) - 1], rotation=30)  # x 축 thick 지정 갯수 출력

    plt.savefig(savePath)
    plt.clf()


def SaveDFImageAddInfo(code, df, sFilePath, iBuyPrice, iExpectPrice, sExpectHighDay0):
    # df 를 이미지로 저장
    # plt.plot(df['날짜'], df['종가'], label=code)
    plt.plot(df['날짜'], df['종가'])

    # y 라인 그리기
    plt.axhline(y=iBuyPrice, color='Black', linestyle='-')
    plt.axhline(y=iExpectPrice, color='Blue', linestyle='-')
    plt.text(0, iBuyPrice * 1.02, str(iBuyPrice))
    plt.text(0, iExpectPrice * 0.98, str(iExpectPrice))

    # plt.scatter(xPoint, yPoint, color="red")  # 위치에 점 찍기
    # plt.text(xPoint, yPoint, str(yPoint))  # 위치에 텍스트 추가

    # 그리드 설정
    # plt.grid(color='gray', linestyle='--')
    plt.title(str(code) + " / " + sExpectHighDay0)
    # plt.legend(loc='upper left')
    plt.gca().invert_xaxis()  # x 축 반전
    plt.xticks([0, len(df) / 2, len(df) - 1], rotation=30)  # x 축 thick 지정 갯수 출력
    plt.savefig(sFilePath)
    plt.clf()


def SaveDFImageWithBuyPrice(code, df, sFilePath, iBuyPrice):
    # df 를 이미지로 저장
    # plt.plot(df['날짜'], df['종가'], label=code)
    plt.plot(df['날짜'], df['종가'])

    # y 라인 그리기
    plt.axhline(y=iBuyPrice, color='Black', linestyle='-')
    plt.text(0, iBuyPrice * 1.02, str(iBuyPrice))

    # plt.scatter(xPoint, yPoint, color="red")  # 위치에 점 찍기
    # plt.text(xPoint, yPoint, str(yPoint))  # 위치에 텍스트 추가

    # 그리드 설정
    # plt.grid(color='gray', linestyle='--')
    plt.title(str(code))
    # plt.legend(loc='upper left')
    plt.gca().invert_xaxis()  # x 축 반전
    plt.xticks([0, len(df) / 2, len(df) - 1], rotation=30)  # x 축 thick 지정 갯수 출력
    plt.savefig(sFilePath)
    plt.clf()