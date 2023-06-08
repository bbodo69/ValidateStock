import os
import exchange_calendars as ecals
import datetime

def clearFolder(folderPath): # 절대 경로 입력

    # 폴더 없을시, 생성
    if not os.path.isdir(folderPath):
        os.makedirs(folderPath)

    files = os.listdir(folderPath)

    for i in files:
        os.remove(os.path.join(folderPath, i))

def deleteFile(filePath):

    folderPath = os.path.dirname(filePath)
    if not os.path.isdir(folderPath):
        os.makedirs(folderPath)

    if os.path.isfile(filePath):
        os.remove(filePath)

def calculateBusinessDay(day):
    # day = x 일때, x 일전 영업일을 출력
    day = day * -1
    XKRX = ecals.get_calendar("XKRX")  # 한국 코드

    count = 0
    targetDay = 0
    dayCount = day + 2

    for x in range(dayCount - 1):
        while targetDay != x + 1:
            if XKRX.is_session(datetime.date.today() - datetime.timedelta(days=count)):
                targetDay = targetDay + 1
            count = count + 1
        retDay = str(datetime.date.today() - datetime.timedelta(days=count - 1)).replace("-", ".")

    return retDay