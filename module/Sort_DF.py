import module.DF_Process as DF_Process
import module.dataProcessing as dataProcessing

def CheckDateMAPattern(df, day, gubun, sDate):
    # 해당 날짜에 day이동평균선이 gubun의 증감을 따르면 True 를 리턴
    '''
    
    :param df: 네이버에서 받은 일별 시세 데이터 
    :param day: n 이동평균선 의 n 값
    :param gubun: ex> 'uuudd' 과거부터 5일동안 이동평균선이 3일증가, 2일감소 하는 패턴
    :param sDate: 파악하고 싶은 대상 일자
    :return: true, false
    '''

    dfDateKey = df.set_index('날짜')
    idxTargetDate = dfDateKey.index.get_loc(sDate)

    # day, sDate 를 구할수 없으면 False
    if idxTargetDate + day  > len(df) or idxTargetDate + len(gubun) > len(df):
        return False

    dic = {}

    # 이동평균 구하기
    for idx, row in df.iterrows():

        if idx + day  > len(df) :
            break

        n = day
        tmp = 0

        for j in range(0, n):
            tmp += int(df.loc[idx + j]['종가'])

        movingAverage = tmp / n
        movingAverage = int(movingAverage)
        dic[row['날짜']] = movingAverage
        print(row['날짜'])

    for idx, c in enumerate(gubun[::-1]):

        if c == 'u':
            if list(dic.values())[idxTargetDate + idx] <= list(dic.values())[idxTargetDate + idx + 1]:
                return False
        if c == 'd':
            if list(dic.values())[idxTargetDate + idx] >= list(dic.values())[idxTargetDate + idx + 1]:
                return False
    return True