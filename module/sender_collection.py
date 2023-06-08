import requests
import warnings
from string import Template
from EmailSender import *

######## FutureWarring 방지 ########
warnings.simplefilter(action='ignore', category=FutureWarning)  # FutureWarning 제거

def SendLine(sMessage):
    try:
        TARGET_URL = 'https://notify-api.line.me/api/notify'
        TOKEN = 'HyzsVdhFD7USNTk4YsB21GXZvtPssAzPER9kTb0j7Xw'  # 발급받은 토큰
        headers = {'Authorization': 'Bearer ' + TOKEN}
        data = {'message': sMessage}

        requests.post(TARGET_URL, headers=headers, data=data)

    except Exception as ex:
        print(ex)

def SendEmail(sSubject, ContentArgs, ImagesDict, sSender, lstReceiver):
    # SMTP 이용 이메일 전송
    # ContentArgs : {code : code 관련 내용}
    # ImagesDict : {code : saveFilePath}
    emailsender = EmailSender()

    combineContents = ""

    for i in ContentArgs:
        if len(ImagesDict) > 0:
            combineContents += "<img src='cid:" + ImagesDict[i] + "'>"
        combineContents += "<br>"
        combineContents += ContentArgs[i]
        combineContents += "<br>"
        combineContents += "<br>"

    Subject = sSubject
    Content = Template(
        "<html><head></head><body>" + combineContents + "</body></html>"
    )
    # ContentArgs = {}  # 대치어:딕셔너리
    # ImagesDict = {}
    AttachmentsDict = {}  # 첨부파일:딕셔너리(파일명:경로)

    emailsender.EmailContent(Subject, Content, ContentArgs, ImagesDict, AttachmentsDict)

    from_addr = ("주식정보", sSender)  # 보내는 사람(이름과 메일주소):튜플
    to_addrs = lstReceiver  # 수신자:리스트
    cc_addrs = []  # 참조:리스트

    emailsender.EmailSend(from_addr, to_addrs, cc_addrs)