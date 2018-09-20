# -*- coding:utf-8 -*-
'''
Created on 2017. 4. 26.

@author: sanghyun
'''
import json
import os
import threading
import time
import zipfile
import hashlib
import httplib
import sys

from datetime import datetime 

from urllib import urlencode
from urllib2 import HTTPError
from flask import Blueprint, request
from flask.globals import session, current_app
import xlsxwriter


from routes.api.systemMngApi import postBatchMng, putBatchMng
from util.common import getServerUrl, getParameter, getApiData, getData, API_SERVER_KPC_LEGACY, API_SERVER_BACKOFFICE,\
    paramEscape, postData, postApiData, postListApiData, putApiData, \
    setStringToNumber, parseDate, EXCEL_FILE_MAKE_LIMT_COUNT, \
    EXCEL_FILE_DOWNLOAD_COUNT, setUnicodeEncodeTypeToEucKr, setUnicodeFormatToEucKr, getServerUrl, \
    request_get, request_post, API_SERVER_BACKOFFICE


cardApi = Blueprint("cardApi", __name__)

@cardApi.route("/api/card/popCard", methods=['GET'])
def popCardMng():
    
    target = getParameter({}, "target")
    cardNumber = paramEscape(getParameter({}, "cardNumber"))
    giftNo = paramEscape(getParameter({}, "cardNumber"))
    if target == "1" : 
        giftNo = ""
    else : 
        cardNumber = ""    
    queryData = {
        'cardNumber' : cardNumber,
        'giftNo'     : giftNo
    }
    result_data = getData("/admin/v1/card" ,queryData , API_SERVER_KPC_LEGACY)
    return json.dumps(result_data)

@cardApi.route("/api/card/popCard/popCardTransfer", methods=["POST"])
def popCardTransfer():
    form_data = request.json
    postcardData = {
        "fromCardNumber" : paramEscape(getParameter(form_data,"fromCardNumber")), #String, 보내는 카드번호
        "toCardNumber"   : paramEscape(getParameter(form_data,"toCardNumber")), #String, 받는 카드번호
        "amount"         : paramEscape(getParameter(form_data,"amount")) #String, 금액
    }
    return json.dumps(postData("/admin/v1/card/transfer", {}, postcardData , API_SERVER_KPC_LEGACY))
    
@cardApi.route("/api/card/cardDealList", methods=["GET"])
def cardDealList():
    form_data = json.loads(request.args.get("formData"))
    target = getParameter(form_data, "target")
    cardNumber = paramEscape(getParameter(form_data, "cardNumber"))
    giftNo = paramEscape(getParameter(form_data, "cardNumber"))
    if target == "1" : 
        giftNo = ""
    else : 
        cardNumber = ""
    orderType = getParameter(form_data, "orderType")
    searchDate = getParameter(form_data , "startDate").split(' - ')
    startDate = paramEscape(searchDate[0])
    endDate = paramEscape(searchDate[1])    
    
    queryData = {
        'startDate'  : startDate,
        'endDate'    : endDate,
        'cardNumber' : cardNumber,
        'giftNo'     : giftNo,
        'order'      : orderType,
        'status'     : getParameter(form_data, "status"),
        'offset'     : setStringToNumber(request.args.get("start")),
        'limit'      : setStringToNumber(request.args.get("length")),        
    }
    result_data = postListApiData("/admin/v1/card/usages/detail" ,queryData , API_SERVER_KPC_LEGACY)
    return json.dumps(result_data)

@cardApi.route('/api/card/excelAll', methods=['GET'])
def cardDealExcelAll():
    form_data = json.loads(request.args.get("formData"))
    target = getParameter(form_data, "target")
    cardNumber = paramEscape(getParameter(form_data, "cardNumber"))
    giftNo = paramEscape(getParameter(form_data, "cardNumber"))
    if target == "1" : 
        giftNo = ""
    else : 
        cardNumber = ""
    orderType = getParameter(form_data, "orderType")
    searchDate = getParameter(form_data , "startDate").split(' - ')
    startDate = paramEscape(searchDate[0])
    endDate = paramEscape(searchDate[1])    
    
    queryData = {
        'startDate'  : startDate,
        'endDate'    : endDate,
        'cardNumber' : cardNumber,
        'giftNo'     : giftNo,
        'order'      : orderType,
        'status'     : getParameter(form_data, "status"),
        'offset'     : 0,
        'limit'      : EXCEL_FILE_DOWNLOAD_COUNT,        
        'empId'      : session['empId']
    }
    rootPath = current_app.root_path
    t1 = threading.Thread(target=cardDealExcelFile,args=[queryData,rootPath])
    t1.daemon = True
    t1.start()
    
    return "엑셀 작업요청"

def cardDealExcelFile(queryData,rootPath):
    excelZip = None
    jobStatus = 0
    batchId = None
    try:
        fileCnt = 1
        makeTime = str(int(round(time.time()*1000)))
        uploads = os.path.join(rootPath, "fileDownload" , "excel" , makeTime)
        if not os.path.isdir(uploads):
            os.makedirs(uploads)
        zipFileName = u'카드정보_'+ datetime.now().strftime('%Y%m%d') +'.zip'
        #작업 시작 메시지 추가
        batchId = postBatchMng({
            "reqId"    : queryData['empId'],
            "status"   : "BAT-0001" , # 진행중
            "filePath" : os.path.join(uploads ,zipFileName),
            "content"  : "카드정보 엑셀 배치작업",
            "errMsg"   : ""
        })["data"]["batchId"]
        fileName = '카드정보_' + datetime.now().strftime('%Y%m%d') + '_' +  str(fileCnt) +  '.xlsx'
        workbook = xlsxwriter.Workbook(os.path.join(uploads ,setUnicodeEncodeTypeToEucKr(fileName)))
        worksheet = workbook.add_worksheet()
        money_format = workbook.add_format()
        money_format.set_num_format('_- #,##0_-;[red]- #,##0_-;_- "-"_-;_-@_-')
        row = 0
        worksheet.write(row, 0  ,"상태")
        worksheet.write(row, 1  ,"거래처명")
        worksheet.write(row, 2  ,"서비스명")
        worksheet.write(row, 3  ,"지불수단")
        worksheet.write(row, 4  ,"지불형태")
        worksheet.write(row, 5  ,"점포코드")
        worksheet.write(row, 6  ,"점포명(사용처)")
        worksheet.write(row, 7  ,"POS")
        worksheet.write(row, 8  ,"거래번호")
        worksheet.write(row, 9  ,"거래일")
        worksheet.write(row, 10 ,"거래시간")
        worksheet.write(row, 11 ,"거래금액")
        worksheet.write(row, 12 ,"결제금액")
        worksheet.write(row, 13 ,"할인금액")
        worksheet.write(row, 14 ,"잔액")
        while True : 
            result_data = postListApiData("/admin/v1/card/usages/detail" ,queryData , API_SERVER_KPC_LEGACY)
            print result_data
            for data in result_data["data"]:
                row += 1
                worksheet.write(row, 0  ,data["status"])
                worksheet.write(row, 1  ,data["merchantName"])
                worksheet.write(row, 2  ,data["serviceName"])
                worksheet.write(row, 3  ,data["payMethod"])
                worksheet.write(row, 4  ,data["payType"])
                worksheet.write(row, 5  ,data["posCode"])
                worksheet.write(row, 6  ,data["posName"])
                worksheet.write(row, 7  ,data["pos"])
                worksheet.write(row, 8  ,data["orderNo"])
                worksheet.write(row, 9  ,parseDate(data["dealDate"] ,'%Y%m%d','%Y-%m-%d'))
                worksheet.write(row, 10 ,parseDate(data["dealDate"] + " "+ data["dealTime"] ,'%Y%m%d %H%M%S' ,'%H:%M:%S'))
                worksheet.write_number(row, 11  ,long(data["orderAmount"]), money_format)
                if(data["dealAmount"]>0) :
                    worksheet.write_number(row, 12  ,long(data["dealAmount"]), money_format)
                else :
                    worksheet.write(row, 12  ,"-",workbook.add_format({'align':'right'}))
                if(data["dcAmount"]>0) :
                    worksheet.write_number(row, 13  ,long(data["dcAmount"]), money_format)
                else :
                    worksheet.write(row, 13  ,"-",workbook.add_format({'align':'right'}))
                worksheet.write(row, 14 ,data["amount"])
                
            queryData["offset"] = queryData["offset"] + EXCEL_FILE_DOWNLOAD_COUNT 
            if len(result_data["data"]) < EXCEL_FILE_DOWNLOAD_COUNT : 
                break
        workbook.close()

        excelZip = zipfile.ZipFile(os.path.join(uploads ,zipFileName),'w')
        for folder, subfolders, files in os.walk(uploads):
            for file in files:
                if file.endswith('.xlsx'):
#                    excelZip.write(os.path.join(folder ,file), os.path.relpath(os.path.join(folder ,file) , uploads), compress_type=zipfile.ZIP_DEFLATED)
                    excelZip.write(os.path.join(folder ,file), setUnicodeFormatToEucKr(file), compress_type=zipfile.ZIP_DEFLATED)
        
                    
    except Exception as err:
        #에러 메시지 추가
        putBatchMng({
            "batchId"  : str(batchId),
            "reqId"    : queryData['empId'],
            "status"   : "BAT-0003" , # 진행중
            "errMsg"   : str(err)
        })
        jobStatus = 1
        print err
    finally:
        if excelZip != None:
            excelZip.close()
        if jobStatus == 0 :    
            putBatchMng({
                "batchId"  : str(batchId),
                "reqId"    : queryData['empId'],
                "status"   : "BAT-0002" , # 진행중
                "errMsg"   : ""
            })               
        #성공 메시지 추가
        print "성공"
"""    
@cardApi.route("/api/card/refund", methods=["POST"])
def cardRefund():
    form_data = request.json
    postcardData = {
        "cardNumber" : paramEscape(getParameter(form_data,"cardNumber")), #String, 보내는 카드번호
    }
    return json.dumps(postData("/admin/v1/card/refund", {}, postcardData , API_SERVER_KPC_LEGACY))
"""

#잔액환불 승인요청
@cardApi.route("/api/card/balanceRefund", methods=["POST"])
def cardbalanceRefund():
    form_data = request.json    
    
    requestData = {        
        #"refTitle"          :   "R2 팝카드 잔액환불",                        #요청 Title
        "refTitle"           :   getParameter(form_data,"cardNumber"),   #승인 목록을 검색하기 위한 Keyword
        "workType"          :   "AWRK-0011",                            #승인 요청 구분(Code)
        "reqType"           :   "AREQ-0001", 
        "reqEmpId"          :   session['empId'],                       #요청자
        "apprEmpId"         :   getParameter(form_data,"apprEmpId"),    #승인자
        "reqMemo"           :   getParameter(form_data,"reqMemo"),      #요청 사유
        "keyword"           :   getParameter(form_data,"cardNumber"),       #승인 목록을 검색하기 위한 Keyword
        "seq"               :   getParameter(form_data,"seq"),          #승인요청 번호
        "contentSeq"        :   getParameter(form_data,"contentSeq"),   #승인 data 등록번호
        "refId"             :   getParameter(form_data,"cardNumber"),       #중복승인을 막기 위한 고유 검색 Keyword     
        
        "contentData"       :   json.dumps({
            "apiUrl"            :   getServerUrl(API_SERVER_KPC_LEGACY)+"/KpcLegacyApiService/admin/v1/card/refund", #승인 후 처리될 API Url   
            "cardNumber"        :   getParameter(form_data,"cardNumber"),
            "giftNo"            :   getParameter(form_data,"giftNo"),
            "balance"           :   paramEscape(getParameter(form_data,"balance")),                  
            "refundCommision"   :   paramEscape(getParameter(form_data,"refundCommision")),                 
            "customerName"      :   getParameter(form_data,"customerName"),               
            "customerTel"       :   paramEscape(getParameter(form_data,"customerTel")), 
            "refundBankCode"    :   getParameter(form_data,"bankCode"), 
            "refundBankAccountNo" : getParameter(form_data,"bankAccountNo"),
            "refundBankHolder"    : getParameter(form_data,"bankHolder")
        })
    }   
   
    reponseResult = postApiData("/approval/request/approval", requestData, API_SERVER_BACKOFFICE)    
    return json.dumps(reponseResult)

#잔액환불 승인요청 수정
@cardApi.route("/api/card/balanceRefund", methods=["PUT"])
def modifyCardbalanceRefund():
    form_data = request.json    
    
    requestData = {        
        #"refTitle"          :   "R2 팝카드 잔액환불",                        #요청 Title
        "refTitle"           :   getParameter(form_data,"cardNumber"),   #승인 목록을 검색하기 위한 Keyword
        "workType"          :   "AWRK-0011",                            #승인 요청 구분(Code)
        "reqEmpId"          :   session['empId'],                       #요청자
        "apprEmpId"         :   getParameter(form_data,"apprEmpId"),    #승인자
        "reqMemo"           :   getParameter(form_data,"reqMemo"),      #요청 사유
        "keyword"           :   getParameter(form_data,"cardNumber"),       #승인 목록을 검색하기 위한 Keyword
        "seq"               :   getParameter(form_data,"seq"),          #승인요청 번호
        "contentSeq"        :   getParameter(form_data,"contentSeq"),   #승인 data 등록번호
        "refId"             :   getParameter(form_data,"cardNumber"),       #중복승인을 막기 위한 고유 검색 Keyword     
        
        "contentData"       :   json.dumps({
            "apiUrl"            :   getServerUrl(API_SERVER_KPC_LEGACY)+"/KpcLegacyApiService/admin/v1/card/refund", #승인 후 처리될 API Url       
            "cardNumber"        :   getParameter(form_data,"cardNumber"),
            "giftNo"            :   getParameter(form_data,"giftNo"),
            "balance"           :   paramEscape(getParameter(form_data,"balance")),                  
            "refundCommision"   :   paramEscape(getParameter(form_data,"refundCommision")),                 
            "customerName"      :   getParameter(form_data,"customerName"),               
            "customerTel"       :   paramEscape(getParameter(form_data,"customerTel")), 
            "refundBankCode"    :   getParameter(form_data,"bankCode"), 
            "refundBankAccountNo" : getParameter(form_data,"bankAccountNo"),
            "refundBankHolder"    : getParameter(form_data,"bankHolder")
        })
    }   
   
    reponseResult = putApiData("/approval/request/approval", requestData, {}, API_SERVER_BACKOFFICE)    
    return json.dumps(reponseResult)

#잔액 환불 신청 정보가 있는지 확인
@cardApi.route('/api/card/<cardNo>/balance-refund/exist', methods=['GET'])
def existBalanceRefund(cardNo):
    return json.dumps(request_get("/approvals/request/"+cardNo+"/exist", None, API_SERVER_BACKOFFICE)) 

#잔액 환불불가 처리
@cardApi.route('/api/card/balance-refund/rejection', methods=['POST'])
def rejectBalanceRefund():
    
    formData = request.json

    rejectData = {
        'refundSeqList': formData.get('sequenceList'),
        'rejectEmpId': session['empId'],
        'refundRejectionMemo': formData.get('rejectRefundMemo'),
    }

    resultData = request_post("/card/balance-refund/rejection", rejectData, API_SERVER_BACKOFFICE)
    
    return json.dumps(resultData)

#카드 사용제한 설정/해제
@cardApi.route("/api/card/restrict", methods=['POST'])
def cardRestrict():
    #사용제한 설정
    form_data = request.json
    if paramEscape(form_data["restrictYN"])=="Y":   
        requestData = {
            'giftNo' : paramEscape(form_data["giftNo"]),
            'cardNumber' : paramEscape(form_data["cardNumber"]),
            'insertAdminId' : paramEscape(session["empId"]),
            'restrictYN' : paramEscape(form_data["restrictYN"]),
            'restrictDesc' : paramEscape(form_data["desc2"])           
        }   
        result_data = postData("/admin/v1/card/restrict" ,{}, requestData , API_SERVER_KPC_LEGACY)
    
    #사용제한 해제    
    elif paramEscape(form_data["restrictYN"])=="N":        
        requestData = {        
            #"refTitle"          :   "R2 팝카드 사용제한 해제",                     #요청 Title
            "refTitle"           :  getParameter(form_data,"cardNumber"),   #승인 목록을 검색하기 위한 Keyword
            "workType"          :   "AWRK-0012",                            #승인 요청 구분(Code)
            "reqType"           :   "AREQ-0005",                       #요청자
            "reqEmpId"          :   session['empId'],                            #요청구분
            "apprEmpId"         :   getParameter(form_data,"apprEmpId"),    #승인자
            "reqMemo"           :   getParameter(form_data,"desc2"),        #요청 사유
            "keyword"           :   getParameter(form_data,"cardNumber"),   #승인 목록을 검색하기 위한 Keyword
            "contentSeq"        :   getParameter(form_data,"contentSeq"),   #승인 data 등록번호
            "refId"             :   getParameter(form_data,"cardNumber"),   #중복승인을 막기 위한 고유 검색 Keyword    
            
            "contentData"       :   json.dumps({
                "apiUrl"            :   getServerUrl(API_SERVER_KPC_LEGACY)+"/KpcLegacyApiService/admin/v1/card/restrict", #승인 후 처리될 API Url
                "giftNo" : paramEscape(form_data["giftNo"]),
                "cardNumber" : paramEscape(form_data["cardNumber"]),
                "insertAdminId" : paramEscape(session["empId"]),
                "restrictYN" : paramEscape(form_data["restrictYN"]),
                "restrictDesc" : paramEscape(form_data["desc2"])                
            })
        }   
        result_data = postApiData("/approval/request/approval" , requestData , API_SERVER_BACKOFFICE)    
    return json.dumps(result_data)


#카드 사용제한 설정/해제 수정
@cardApi.route("/api/card/restrict", methods=['PUT'])
def cardRestrictModify():
    #사용제한 설정
    form_data = request.json
    if paramEscape(form_data["restrictYN"])=="Y":   
        requestData = {
            'giftNo' : paramEscape(form_data["giftNo"]),
            'cardNumber' : paramEscape(form_data["cardNumber"]),
            'insertAdminId' : paramEscape(session["empId"]),
            'restrictYN' : paramEscape(form_data["restrictYN"]),
            'restrictDesc' : paramEscape(form_data["desc2"])           
        }   
        result_data = postData("/admin/v1/card/restrict" ,{}, requestData , API_SERVER_KPC_LEGACY)
    
    #사용제한 해제    
    elif paramEscape(form_data["restrictYN"])=="N":
        
        requestData = {        
            #"refTitle"          :   "R2 팝카드 사용제한 해제",                     #요청 Title
            "refTitle"           :  getParameter(form_data,"cardNumber"),   #승인 목록을 검색하기 위한 Keyword
            "workType"          :   "AWRK-0012",                            #승인 요청 구분(Code)
            "reqType"           :   "AREQ-0005",                       #요청자
            "reqEmpId"          :   session['empId'],                            #요청구분
            "apprEmpId"         :   getParameter(form_data,"apprEmpId"),    #승인자
            "reqMemo"           :   getParameter(form_data,"desc2"),        #요청 사유
            "keyword"           :   getParameter(form_data,"cardNumber"),   #승인 목록을 검색하기 위한 Keyword
            "seq"               :   getParameter(form_data,"seq"),          #승인요청 번호
            "contentSeq"        :   getParameter(form_data,"contentSeq"),   #승인 data 등록번호
            "refId"             :   getParameter(form_data,"cardNumber"),   #중복승인을 막기 위한 고유 검색 Keyword    
            
            "contentData"       :   json.dumps({
                "apiUrl"            :   getServerUrl(API_SERVER_KPC_LEGACY)+"/KpcLegacyApiService/admin/v1/card/restrict", #승인 후 처리될 API Url
                "giftNo" : paramEscape(form_data["giftNo"]),
                "cardNumber" : paramEscape(form_data["cardNumber"]),
                "insertAdminId" : paramEscape(session["empId"]),
                "restrictYN" : paramEscape(form_data["restrictYN"]),
                "restrictDesc" : paramEscape(form_data["desc2"])                
            })
        }   
        
        result_data = putApiData("/approval/request/approval" ,requestData ,{} , API_SERVER_BACKOFFICE)    
    return json.dumps(result_data)
 

@cardApi.route("/api/card/balanceRefund/detail", methods=['GET'])
def balanceRefundDetail():
    seq = json.loads(request.args.get("seq"))
    queryData = {
        "seq" : seq
        }
    print(seq)
    result_data = getApiData("/card/approveCardBalnaceRefund" ,queryData , API_SERVER_BACKOFFICE)
    return json.dumps(result_data)


@cardApi.route("/api/card/balanceRefund/list", methods=['GET'])
def balanceRefundList():
    form_data = json.loads(request.args.get("formData"))
    searchDate = getParameter(form_data , "searchDate").split(' - ')
    startDate = paramEscape(searchDate[0]) 
    endDate = paramEscape(searchDate[1])    
   
    queryData = {     
        'cardNumber'   : getParameter(form_data, "cardNumber"),
        'customerName' : getParameter(form_data,"customerName"),   
        'dateType'     : getParameter(form_data, "dateType"),
        'startDate'    : startDate,
        'endDate'      : endDate,
        'dateOrderType': getParameter(form_data, "dateOrderType"),
        'dateOrderDesc': getParameter(form_data, "dateOrderDesc"),                 
        'procStatus'       : getParameter(form_data, "procStatus"),              
        'offset'       : setStringToNumber(getParameter({},"start")),
        'limit'        : setStringToNumber(getParameter({},"length"))    
    }
    result_data = getApiData("/card/approveCardBalnaceRefunds" ,queryData , API_SERVER_BACKOFFICE)
    return json.dumps(result_data)


@cardApi.route("/api/card/balanceRefund/list/excel", methods=['GET'])
def balanceRefundListExcel():
    form_data = json.loads(request.args.get("formData"))
    searchDate = getParameter(form_data , "searchDate").split(' - ')
    startDate = paramEscape(searchDate[0]) 
    endDate = paramEscape(searchDate[1])    
   
    queryData = {             
        'cardNumber'   : getParameter(form_data, "cardNumber"),
        'customerName' : getParameter(form_data,"customerName"),   
        'dateType'     : getParameter(form_data, "dateType"),
        'startDate'    : startDate,
        'endDate'      : endDate,
        'dateOrderType': getParameter(form_data, "dateOrderType"),
        'dateOrderDesc': getParameter(form_data, "dateOrderDesc"),                 
        'procStatus'       : getParameter(form_data, "procStatus"),              
        'offset'       : setStringToNumber(getParameter({},"start")),
        'limit'        : setStringToNumber(getParameter({},"length")),
        'excelAllFlag':'1',    
        'empId'      : session['empId']
    }
    rootPath = current_app.root_path
    t1 = threading.Thread(target=cardRefundExcelFile,args=[queryData,rootPath])
    t1.daemon = True
    t1.start()
    
    return "엑셀 작업요청"


#잔액환불 완료
@cardApi.route("/api/card/balanceRefund/approve", methods=["POST"])
def cardbalanceRefundApprove():
    form_data = request.json
    
    approvalData = {
        'refundList' : form_data,
        'empId': session['empId']
        }

    resultData = request_post("/card/CardBalnaceRefund/approve", approvalData, API_SERVER_BACKOFFICE)
    return json.dumps(resultData)


#잔액환불 거부
@cardApi.route("/api/card/balanceRefund/reject", methods=["POST"])
def cardbalanceRefundReject():
    form_data = request.json
    print(form_data)
    approvalData = {
        'refundList' : getParameter(form_data, "refundList"),
        'reqMemo' : getParameter(form_data, "refundDesc"),
        'empId': session['empId']
        }

    resultData = request_post("/card/CardBalnaceRefund/reject", approvalData, API_SERVER_BACKOFFICE)
    return json.dumps(resultData)


@cardApi.route("/api/card/usages", methods=['GET'])
def usages():
    form_data = json.loads(request.args.get("formData"))
    searchDate = getParameter(form_data , "searchDate").split(' - ')
    startDate = paramEscape(searchDate[0]).split(" ")[0]
    startTime = paramEscape(searchDate[0]).split(" ")[1] + "00"
    endDate = paramEscape(searchDate[1]).split(" ")[0] 
    endTime = paramEscape(searchDate[1]).split(" ")[1] + "59"
    target = getParameter(form_data, "target")
    cardNumber = paramEscape(getParameter(form_data, "cardNumber"))
    queryData = {
        'cardNumber'   : target == "1" and cardNumber or "",
        'orderNo'      : target == "2" and cardNumber or "",
        'serviceId'    : target == "3" and cardNumber or "",
        'startGiftNo'  : paramEscape(getParameter(form_data, "startGiftNo")),
        'endGiftNo'    : paramEscape(getParameter(form_data, "endGiftNo")),
        'amount'       : paramEscape(getParameter(form_data, "amount")),
        'merchantName' : getParameter(form_data, "merchantName"),
        'dateType'     : getParameter(form_data, "dateType"),
        'startDate'    : startDate,
        'startTime'    : startTime,
        'endDate'      : endDate,
        'endTime'      : endTime,
        'storeName'      : getParameter(form_data,"storeName"),
        'storeCode'      : getParameter(form_data,"storeCode"),        
        'status'      : getParameter(form_data, "status"),
        'payKind'      : getParameter(form_data, "payKind"),
        'payMethod'    : getParameter(form_data, "payMethod"),
        'order'    : getParameter(form_data, "order"),            
        'offset'       : setStringToNumber(getParameter({},"start")),
        'limit'        : setStringToNumber(getParameter({},"length"))    
    }
    result_data = postListApiData("/admin/v1/card/usages" ,queryData , API_SERVER_KPC_LEGACY)
    return json.dumps(result_data)


@cardApi.route('/api/card/usages/excel', methods=['GET'])
def usagesExcelAll():
    form_data = {}
    searchDate = getParameter(form_data , "searchDate").split(' - ')
    startDate = paramEscape(searchDate[0]).split(" ")[0]
    startTime = paramEscape(searchDate[0]).split(" ")[1] + "00"
    endDate = paramEscape(searchDate[1]).split(" ")[0] 
    endTime = paramEscape(searchDate[1]).split(" ")[1] + "59"
    target = getParameter(form_data, "target")
    cardNumber = paramEscape(getParameter(form_data, "cardNumber"))
    queryData = {
        'cardNumber'   : target == "1" and cardNumber or "",
        'orderNo'      : target == "2" and cardNumber or "",
        'serviceId'    : target == "3" and cardNumber or "",
        'startGiftNo'  : paramEscape(getParameter(form_data, "startGiftNo")),
        'endGiftNo'    : paramEscape(getParameter(form_data, "endGiftNo")),
        'amount'       : paramEscape(getParameter(form_data, "amount")),
        'merchantName' : getParameter(form_data, "merchantName"),
        'dateType'     : getParameter(form_data, "dateType"),
        'startDate'    : startDate,
        'startTime'    : startTime,
        'endDate'      : endDate,
        'endTime'      : endTime,
        'storeName'      : getParameter(form_data,"storeName"),
        'storeCode'      : getParameter(form_data,"storeCode"),        
        'status'      : getParameter(form_data, "status"),
        'payKind'      : getParameter(form_data, "payKind"),
        'payMethod'    : getParameter(form_data, "payMethod"),
        'order'    : getParameter(form_data, "order"),      
        'offset'     : 0,
        'limit'      : EXCEL_FILE_DOWNLOAD_COUNT,        
        'empId'      : session['empId']
    }
    rootPath = current_app.root_path
    t1 = threading.Thread(target=cardExcelFile,args=[queryData,rootPath])
    t1.daemon = True
    t1.start()
    
    return "엑셀 작업요청"

def cardExcelFile(queryData,rootPath):
    excelZip = None
    jobStatus = 0
    batchId = None
    try:
        fileCnt = 1
        makeTime = str(int(round(time.time()*1000)))
        uploads = os.path.join(rootPath, "fileDownload" , "excel" , makeTime)
        if not os.path.isdir(uploads):
            os.makedirs(uploads)
        zipFileName = u'카드정보_'+ datetime.now().strftime('%Y%m%d') +'.zip'
        #작업 시작 메시지 추가
        batchId = postBatchMng({
            "reqId"    : queryData['empId'],
            "status"   : "BAT-0001" , # 진행중
            "filePath" : os.path.join(uploads ,zipFileName),
            "content"  : "카드정보 엑셀 배치작업",
            "errMsg"   : ""
        })["data"]["batchId"]
        fileName = '카드정보_' + datetime.now().strftime('%Y%m%d') + '_' + str(fileCnt) +  '.xlsx'
        workbook = xlsxwriter.Workbook(os.path.join(uploads ,setUnicodeEncodeTypeToEucKr(fileName)))
        worksheet = workbook.add_worksheet()
        money_format = workbook.add_format()
        money_format.set_num_format('_- #,##0_-;[red]- #,##0_-;_- "-"_-;_-@_-')
        row = 0
        worksheet.write(row, 0  ,"거래처명")
        worksheet.write(row, 1  ,"서비스명")
        worksheet.write(row, 2  ,"점포코드")
        worksheet.write(row, 3  ,"점포명(사용처)")        
        worksheet.write(row, 4  ,"구분")
        worksheet.write(row, 5  ,"지불수단")
        worksheet.write(row, 6  ,"지불형태")
        worksheet.write(row, 7  ,"영업일")
        worksheet.write(row, 8  ,"거래일")
        worksheet.write(row, 9  ,"거래시간")
        worksheet.write(row, 10 ,"거래번호")
        worksheet.write(row, 11 ,"승인번호")
        worksheet.write(row, 12 ,"금액")
        worksheet.write(row, 13 ,"사용카드번호")
        while True : 
            result_data = postListApiData("/admin/v1/card/usages" ,queryData , API_SERVER_KPC_LEGACY)
            for data in result_data["data"]:
                row += 1
                worksheet.write(row, 0  ,data["merchantName"])
                worksheet.write(row, 1  ,data["serviceName"])
                worksheet.write(row, 2  ,data["posCode"])
                worksheet.write(row, 3  ,data["posName"])                
                worksheet.write(row, 4  ,data["payStatus"])
                worksheet.write(row, 5  ,data["payMethod"])
                worksheet.write(row, 6  ,data["payType"])
                worksheet.write(row, 7  ,parseDate(data["businessDate"] ,'%Y%m%d' ,'%Y-%m-%d'))
                worksheet.write(row, 8  ,parseDate(data["approvalDate"] ,'%Y%m%d%H%M%S' ,'%Y-%m-%d'))
                worksheet.write(row, 9  ,parseDate(data["approvalDate"] , '%Y%m%d%H%M%S', '%H:%M:%S'))
                worksheet.write(row, 10 ,data["orderNo"])
                worksheet.write(row, 11 ,data["approvalNo"])
                worksheet.write_number(row, 12  ,long(data["amount"]), money_format)
                worksheet.write(row, 13 ,data["cardNumber"])
                
                if row >= EXCEL_FILE_MAKE_LIMT_COUNT :
                    row = 0
                    fileCnt += 1
                    fileName = '카드정보_' + datetime.now().strftime('%Y%m%d') + '_' + str(fileCnt) +  '.xlsx'
                    # 디비 조회건수 * 2 row 생성시 파일 재생성
                    workbook.close()
                    workbook = xlsxwriter.Workbook(os.path.join(uploads ,setUnicodeEncodeTypeToEucKr(fileName)))
                    worksheet = workbook.add_worksheet()
                    worksheet.write(row, 0  ,"거래처명")
                    worksheet.write(row, 1  ,"서비스명")                    
                    worksheet.write(row, 2  ,"점포코드")
                    worksheet.write(row, 3  ,"점포명(사용처)")
                    worksheet.write(row, 4  ,"구분")
                    worksheet.write(row, 5  ,"지불수단")
                    worksheet.write(row, 6  ,"지불형태")
                    worksheet.write(row, 7  ,"영업일")
                    worksheet.write(row, 8  ,"거래일")
                    worksheet.write(row, 9  ,"거래시간")
                    worksheet.write(row, 10 ,"거래번호")
                    worksheet.write(row, 11 ,"승인번호")
                    worksheet.write(row, 12 ,"금액")
                    worksheet.write(row, 13 ,"사용카드번호")                           
            queryData["offset"] = queryData["offset"] + EXCEL_FILE_DOWNLOAD_COUNT 
            if len(result_data["data"]) < EXCEL_FILE_DOWNLOAD_COUNT : 
                break
        workbook.close()
        excelZip = zipfile.ZipFile(os.path.join(uploads ,zipFileName),'w')
        
        for folder, subfolders, files in os.walk(uploads):
            for file in files:
                if file.endswith('.xlsx'):
                    excelZip.write(os.path.join(folder ,file), setUnicodeFormatToEucKr(file), compress_type=zipfile.ZIP_DEFLATED)                    
    except Exception as err:
        #에러 메시지 추가
        putBatchMng({
            "batchId"  : str(batchId),
            "reqId"    : queryData['empId'],
            "status"   : "BAT-0003" , # 진행중
            "errMsg"   : str(err)
        })
        jobStatus = 1
        print("Error on line {}".format(sys.exc_info()[-1].tb_lineno))
        print err
    finally:
        if excelZip != None:
            excelZip.close()
        if jobStatus == 0 :    
            putBatchMng({
                "batchId"  : str(batchId),
                "reqId"    : queryData['empId'],
                "status"   : "BAT-0002" , # 진행중
                "errMsg"   : ""
            })               
        #성공 메시지 추가
        print "성공"
        
'''
결제,충전에 대한 거래 취소 API
'''
@cardApi.route("/api/card/cancelCardDeal", methods=['POST'])
def cancelCardDeal():
    
    data = request.json
    
    cardData = {
        "onlineId" : paramEscape(getParameter(data,"merchantId")),              #온라인아이디
        "onlinePwd" : paramEscape(getParameter(data,"merchantPwd")),            #온라인아이디 비밀번호
        "approvalNo" : paramEscape(getParameter(data,"approvalNo")),            #승인번호
        "approvalDate" : paramEscape(getParameter(data,"approvalDate")),            #승인시간
        "cardNo" : paramEscape(getParameter(data,"cardNo")),                    #카드번호
        "orderNo" : paramEscape(getParameter(data,"orderNo")),                  #거래번호
        "transactionCode" : paramEscape(getParameter(data,"transactionCode")),  #거래코드(결제취소:PC, 충전취소:CC)
        "amount" : paramEscape(getParameter(data,"amount")),                    #거래금액
        "requestDate" : datetime.now().strftime('%Y%m%d%H%M%S'),                #요청일자
        "cancelType" : paramEscape(getParameter(data,"cancelType")),            #취소타입(D1: 전체취소) 해당 API는 전체취소
        "cancelMemo" : paramEscape(getParameter(data,"cancelMemo")),             #취소사유
        "branchCode" : paramEscape(getParameter(data,"posCode"))             #점포코드
    }
    
    return json.dumps(cancelCardDealApi("/CardService/admin/v1/card/transaction", {}, cardData))

'''
결제,충전 취소에 대한 내부 cardService-api
'''
def cancelCardDealApi(apiUrl ,data , queryData):
    readData = {
        "status" : "",
        "message" : "",
    }
    try :
        url = apiUrl
        if (len(queryData) > 0) :
            url =  url  + "?" + urlencode(queryData)

        conn = httplib.HTTPConnection(getServerUrl(API_SERVER_KPC_LEGACY), timeout=120)
        print(url)
        conn.request('POST', url, json.dumps(data), headers={"Content-Type" : "application/json; charset=utf-8"})
        response = conn.getresponse()
        readResponseData = response.read()
        print(readResponseData)
        readData = json.loads(readResponseData)
    except HTTPError as err:
        readData["status"] = err.code
        errorMsg = "오류가 발생하였습니다.\n해당 메시지를 스크린 캡쳐하여 담당자에 문의 바랍니다.\n" + err.read() 
        readData["message"] = errorMsg

    return readData


@cardApi.route("/api/card/restrictHistory", methods=["GET"])
def getCardRestirctHistory():
    queryData = {
        'giftNo': getParameter({},"giftNo"),        
        'start': getParameter({},"start"),
        'length': getParameter({},"length")
    }  
    
    return json.dumps(getApiData("/admin/v1/card/restrict", queryData, API_SERVER_KPC_LEGACY))

    

def cardRefundExcelFile(queryData,rootPath):
    excelZip = None
    jobStatus = 0
    batchId = None
    try:
        fileCnt = 1
        makeTime = str(int(round(time.time()*1000)))
        uploads = os.path.join(rootPath, "fileDownload" , "excel" , makeTime)
        if not os.path.isdir(uploads):
            os.makedirs(uploads)
        zipFileName = u'잔액환불 내역_'+ queryData['startDate'] + '~' + queryData['endDate'] +'.zip'
        #작업 시작 메시지 추가
        batchId = postBatchMng({
            "reqId"    : queryData['empId'],
            "status"   : "BAT-0001" , # 진행중
            "filePath" : os.path.join(uploads ,zipFileName),
            "content"  : "카드 잔액환불정보 엑셀 배치작업",
            "errMsg"   : ""
        })["data"]["batchId"]
        fileName = '잔액환불 내역_' +  queryData['startDate'] + '~' + queryData['endDate'] + '_' + str(fileCnt) +  '.xlsx'
        workbook = xlsxwriter.Workbook(os.path.join(uploads ,setUnicodeEncodeTypeToEucKr(fileName)))
        worksheet = workbook.add_worksheet()
        money_format = workbook.add_format()
        money_format.set_num_format('_- #,##0_-;[red]- #,##0_-;_- "-"_-;_-@_-')
        row = 0
        worksheet.write(row, 0  ,"번호")
        worksheet.write(row, 1  ,"카드번호")
        worksheet.write(row, 2  ,"진행상태")
        worksheet.write(row, 3  ,"고객명")        
        worksheet.write(row, 4  ,"접수일")
        worksheet.write(row, 5  ,"승인일")
        worksheet.write(row, 6  ,"환불일")
        worksheet.write(row, 7  ,"접수시 잔액")
        worksheet.write(row, 8  ,"환불 수수료")
        worksheet.write(row, 9  ,"실환불금액")
        worksheet.write(row, 10 ,"환불은행")
        worksheet.write(row, 11 ,"환불계좌")
        worksheet.write(row, 12 ,"예금주")        
        while True : 
            
            result_data = getApiData("/card/approveCardBalnaceRefunds" ,queryData , API_SERVER_BACKOFFICE)
            for data in result_data["data"]:
                row += 1
                receptionDt = data["receptionDt"];
                approvalDt = data["approvalDt"];
                refundDt = data["refundDt"];
                if receptionDt != None :
                    receptionDt = datetime.fromtimestamp(data["receptionDt"] / 1e3)                   
                    receptionDt = receptionDt.strftime('%Y-%m-%d')
                if data["approvalDt"]  != None :
                    approvalDt = datetime.fromtimestamp(data["approvalDt"] / 1e3)
                    approvalDt = approvalDt.strftime('%Y-%m-%d')
                if data["refundDt"] != None :
                    refundDt = datetime.fromtimestamp(data["refundDt"] / 1e3)
                    refundDt = refundDt.strftime('%Y-%m-%d')
                else :
                    refundDt = '-'
                worksheet.write(row, 0  ,row)
                worksheet.write(row, 1  ,data["cardNumber"])
                worksheet.write(row, 2  ,'환불'+data["statusName"])
                worksheet.write(row, 3  ,data["customerName"])                
                worksheet.write(row, 4  ,receptionDt)
                worksheet.write(row, 5  ,approvalDt)
                worksheet.write(row, 6  ,refundDt)
                worksheet.write(row, 7  ,long(data["balance"]), money_format)
                worksheet.write(row, 8  ,long(data["refundCommision"]), money_format)
                worksheet.write(row, 9  ,long(data["balance"])-long(data["refundCommision"]), money_format)
                worksheet.write(row, 10 ,data["bankName"])
                worksheet.write(row, 11 ,data["bankAccNo"])
                worksheet.write(row, 12  ,data["bankHolder"])
                
                if row >= EXCEL_FILE_MAKE_LIMT_COUNT :
                    row = 0
                    fileCnt += 1
                    fileName = '잔액환불 내역_' +  queryData['startDate'] + '~' + queryData['endDate'] + '_' + str(fileCnt) +  '.xlsx'
                    # 디비 조회건수 * 2 row 생성시 파일 재생성
                    workbook.close()
                    workbook = xlsxwriter.Workbook(os.path.join(uploads ,setUnicodeEncodeTypeToEucKr(fileName)))
                    worksheet = workbook.add_worksheet()
                    worksheet.write(row, 0  ,"번호")
                    worksheet.write(row, 1  ,"카드번호")
                    worksheet.write(row, 2  ,"진행상태")
                    worksheet.write(row, 3  ,"고객명")        
                    worksheet.write(row, 4  ,"접수일")
                    worksheet.write(row, 5  ,"승인일")
                    worksheet.write(row, 6  ,"환불일")
                    worksheet.write(row, 7  ,"접수시 잔액")
                    worksheet.write(row, 8  ,"환불 수수료")
                    worksheet.write(row, 9  ,"실환불금액")
                    worksheet.write(row, 10 ,"환불은행")
                    worksheet.write(row, 11 ,"환불계좌")
                    worksheet.write(row, 12 ,"예금주")                            
            queryData["offset"] = queryData["offset"] + EXCEL_FILE_DOWNLOAD_COUNT 
            if len(result_data["data"]) < EXCEL_FILE_DOWNLOAD_COUNT : 
                break
        workbook.close()
        excelZip = zipfile.ZipFile(os.path.join(uploads ,zipFileName),'w')
        
        for folder, subfolders, files in os.walk(uploads):
            for file in files:
                if file.endswith('.xlsx'):
                    excelZip.write(os.path.join(folder ,file), setUnicodeFormatToEucKr(file), compress_type=zipfile.ZIP_DEFLATED)                    
    except Exception as err:
        #에러 메시지 추가
        putBatchMng({
            "batchId"  : str(batchId),
            "reqId"    : queryData['empId'],
            "status"   : "BAT-0003" , # 진행중
            "errMsg"   : str(err)
        })
        jobStatus = 1
        print("Error on line {}".format(sys.exc_info()[-1].tb_lineno))
        print err
    finally:
        if excelZip != None:
            excelZip.close()
        if jobStatus == 0 :    
            putBatchMng({
                "batchId"  : str(batchId),
                "reqId"    : queryData['empId'],
                "status"   : "BAT-0002" , # 진행중
                "errMsg"   : ""
            })               
        #성공 메시지 추가
        print "성공"
        
#카드 기간별 잔액 관리 리스트 요청      
@cardApi.route("/api/card/balance/daily-balance-list",  methods=['GET'])
def cardDailyBalanceList():
    formData = json.loads(request.args.get("formData"))
    searchDate = getParameter(formData , "startDate").split(' - ')
    startDate = paramEscape(searchDate[0])
    endDate = paramEscape(searchDate[1])
    queryData = {
        'startDate'     : startDate,
        'endDate'       : endDate,
        'limit'         : setStringToNumber(getParameter({},"length")),
        'offset'        : setStringToNumber(getParameter({},"start")),
        'orderBy'       : getParameter(formData, "orderBy")
    }
    result_data = getApiData("/balance/daily-balance-list" , queryData ,API_SERVER_BACKOFFICE)
    return json.dumps(result_data)       

#카드 기간별 잔액 관리 리스트 엑셀 다운로드 요청            
@cardApi.route("/api/card/balance/daily-balance-list/excelAll", methods=['GET'])
def cardDailyBalanceListExcelAll():
    formData = {}
    searchDate = getParameter(formData , "startDate").split(' - ')
    startDate = paramEscape(searchDate[0])
    endDate = paramEscape(searchDate[1])
    queryData = {
        'startDate'     : startDate,
        'endDate'       : endDate,
        'limit'         : EXCEL_FILE_DOWNLOAD_COUNT,
        'offset'        : 0,
        'orderBy'       : getParameter(formData, "orderBy"),
        'empId'         : session['empId']
    }
    
    rootPath = current_app.root_path
    t1 = threading.Thread(target=cardDailyBalanceListExcelFile,args=[queryData,rootPath])
    t1.daemon = True
    t1.start()
    return "엑셀 작업요청"

#카드 기간별 잔액 관리 리스트 엑셀 다운로드 처리    
def cardDailyBalanceListExcelFile(queryData,rootPath):
    excelZip = None
    jobStatus = 0
    batchId = None
    try:
        fileCnt = 1
        makeTime = str(int(round(time.time()*1000)))
        uploads = os.path.join(rootPath, "fileDownload" , "excel" , makeTime)
        if not os.path.isdir(uploads):
            os.makedirs(uploads)
        zipFileName = u'카드_기간별_잔액관리'+ datetime.now().strftime('%Y%m%d') +'.zip'
        #작업 시작 메시지 추가
        batchId = postBatchMng({
            "reqId"    : queryData['empId'],
            "status"   : "BAT-0001" , # 진행중
            "filePath" : os.path.join(uploads ,zipFileName),
            "content"  : "카드 기간별 잔액관리 엑셀 배치작업",
            "errMsg"   : ""
        })["data"]["batchId"]
        
        fileName = '카드_기간별_잔액관리(' +  queryData['startDate'] + '~' + queryData['endDate'] + ').xlsx'
        workbook = xlsxwriter.Workbook(os.path.join(uploads ,setUnicodeEncodeTypeToEucKr(fileName)))
        worksheet = workbook.add_worksheet()
        money_format = workbook.add_format()
        money_format.set_num_format('_- #,##0_-;[red]- #,##0_-;_- "-"_-;_-@_-')
        
        title_format = workbook.add_format({'align':'center', 'valign':'vcenter', 'bold':True, 'border':1,'fg_color':'#A9D0F5'})
        string_format = workbook.add_format({'align':'center', 'valign':'vcenter'})
        
        summary_money_format = workbook.add_format({'fg_color' : '#E5E5E5'});
        summary_money_format.set_num_format('_- #,##0_-;[red]- #,##0_-;_- "-"_-;_-@_-')
        
        row = 0
        worksheet.write(row, 0  ,"번호", title_format)
        worksheet.write(row, 1  ,"일자", title_format)
        worksheet.write(row, 2  ,"이월잔액", title_format)
        worksheet.write(row, 3  ,"충전", title_format)
        worksheet.write(row, 4  ,"충전취소", title_format)
        worksheet.write(row, 5  ,"충전합계", title_format)
        worksheet.write(row, 6  ,"결제", title_format)
        worksheet.write(row, 7  ,"결제취소", title_format)
        worksheet.write(row, 8  ,"결제합계", title_format)
        worksheet.write(row, 9  ,"환불", title_format)
        worksheet.write(row, 10  ,"잔액", title_format)

        while True : 
            searchData  = getApiData("/balance/daily-balance-list" , queryData ,API_SERVER_BACKOFFICE)
            
            summaryData = searchData["totalData"]
            for data in searchData["data"]:
                
                row += 1
                worksheet.write(row, 0  ,row, string_format)    
                worksheet.write(row, 1  ,data["balanceDate"], money_format)
                worksheet.write(row, 2  ,data["prevBalance"], money_format)
                worksheet.write(row, 3  ,data["chargeAmount"], money_format)
                worksheet.write(row, 4  ,data["cancelChargeAmount"], money_format)        
                worksheet.write(row, 5  ,data["chargeSum"], money_format)
                worksheet.write(row, 6  ,data["payAmount"], money_format)
                worksheet.write(row, 7  ,data["cancelPayAmount"], money_format)
                worksheet.write(row, 8  ,data["paySum"], money_format)
                worksheet.write(row, 9  ,data["refundAmount"], money_format)
                worksheet.write(row, 10 ,data["balance"], money_format)
               # worksheet.write(row, 7  ,parseDate(data["expireDt"] ,'%Y-%m-%d %H:%M:%S.0','%Y-%m-%d'), string_format)
                
                
                if row >= EXCEL_FILE_MAKE_LIMT_COUNT :
                    row = 0
                    fileCnt += 1
                    fileName = '카드_기간별_잔액관리(' +  queryData['startDate'] + '~' + queryData['endDate'] + ').xlsx'
                    # 디비 조회건수 * 2 row 생성시 파일 재생성
                    workbook.close()
                    workbook = xlsxwriter.Workbook(os.path.join(uploads ,setUnicodeEncodeTypeToEucKr(fileName)))
                    worksheet = workbook.add_worksheet()
                    worksheet.write(row, 0  ,"번호", title_format)
                    worksheet.write(row, 1  ,"일자", title_format)
                    worksheet.write(row, 2  ,"이월잔액", title_format)
                    worksheet.write(row, 3  ,"충전", title_format)
                    worksheet.write(row, 4  ,"충전취소", title_format)
                    worksheet.write(row, 5  ,"충전합계", title_format)
                    worksheet.write(row, 6  ,"결제", title_format)
                    worksheet.write(row, 7  ,"결제취소", title_format)
                    worksheet.write(row, 8  ,"결제합계", title_format)
                    worksheet.write(row, 9  ,"환불", title_format)
                    worksheet.write(row, 10  ,"잔액", title_format)
                    
            row += 1
            worksheet.write(row, 0  ,"", summary_money_format)    
            worksheet.write(row, 1  ,"", summary_money_format)
            worksheet.write(row, 2  ,summaryData["prevBalance"], summary_money_format)
            worksheet.write(row, 3  ,summaryData["chargeAmount"], summary_money_format)
            worksheet.write(row, 4  ,summaryData["cancelChargeAmount"], summary_money_format)        
            worksheet.write(row, 5  ,summaryData["chargeSum"], summary_money_format)
            worksheet.write(row, 6  ,summaryData["payAmount"], summary_money_format)
            worksheet.write(row, 7  ,summaryData["cancelPayAmount"], summary_money_format)
            worksheet.write(row, 8  ,summaryData["paySum"], summary_money_format)
            worksheet.write(row, 9  ,summaryData["refundAmount"], summary_money_format)
            worksheet.write(row, 10 ,summaryData["balance"], summary_money_format)
            # worksheet.write(row, 7  ,parseDate(data["expireDt"] ,'%Y-%m-%d %H:%M:%S.0','%Y-%m-%d'), string_format)
            
            if row >= EXCEL_FILE_MAKE_LIMT_COUNT :
                row = 0
                fileCnt += 1
                fileName = '카드_기간별_잔액관리(' +  queryData['startDate'] + '~' + queryData['endDate'] + ').xlsx'
                # 디비 조회건수 * 2 row 생성시 파일 재생성
                workbook.close()
                workbook = xlsxwriter.Workbook(os.path.join(uploads ,setUnicodeEncodeTypeToEucKr(fileName)))
                worksheet = workbook.add_worksheet()
                worksheet.write(row, 0  ,"번호", title_format)
                worksheet.write(row, 1  ,"일자", title_format)
                worksheet.write(row, 2  ,"이월잔액", title_format)
                worksheet.write(row, 3  ,"충전", title_format)
                worksheet.write(row, 4  ,"충전취소", title_format)
                worksheet.write(row, 5  ,"충전합계", title_format)
                worksheet.write(row, 6  ,"결제", title_format)
                worksheet.write(row, 7  ,"결제취소", title_format)
                worksheet.write(row, 8  ,"결제합계", title_format)
                worksheet.write(row, 9  ,"환불", title_format)
                worksheet.write(row, 10  ,"잔액", title_format)
                
    
            queryData["offset"] = queryData["offset"] + EXCEL_FILE_DOWNLOAD_COUNT 
            if len(searchData["data"])+1 < EXCEL_FILE_DOWNLOAD_COUNT : 
                break
        workbook.close()
        excelZip = zipfile.ZipFile(os.path.join(uploads ,zipFileName),'w')
        for folder, subfolders, files in os.walk(uploads):
            for file in files:
                if file.endswith('.xlsx'):
                    excelZip.write(os.path.join(folder ,file), setUnicodeFormatToEucKr(file), compress_type=zipfile.ZIP_DEFLATED)
                    
    except Exception as err:
        #에러 메시지 추가
        putBatchMng({
            "batchId"  : str(batchId),
            "reqId"    : queryData['empId'],
            "status"   : "BAT-0003" , # 진행중
            "errMsg"   : str(err)
        })
        jobStatus = 1
        print err
        
    finally:
        if excelZip != None:
            excelZip.close()
        if jobStatus == 0 :    
            putBatchMng({
                "batchId"  : str(batchId),
                "reqId"    : queryData['empId'],
                "status"   : "BAT-0002" , # 진행중
                "errMsg"   : ""
            })               
        #성공 메시지 추가
        print "성공"
        
#카드 기간별 잔액 관리 거래별 요약조회 리스트 요청
#(충전:TRNT-0001, 결제:TRNT-0002, 환불:TRNT-0003)     
@cardApi.route("/api/card/balance/transaction-summary",  methods=['GET'])
def cardDailyBalanceTransactionSummary():
    formData = json.loads(request.args.get("formData"))
    searchDate = getParameter(formData , "startDate").split(' - ')
    startDate = paramEscape(searchDate[0])
    endDate = paramEscape(searchDate[1])
    transactionType = request.args.get("transactionType");
    queryData = {
        'startDate'      : startDate,
        'endDate'        : endDate,
        'transactionType': transactionType,
        'limit'          : setStringToNumber(getParameter({},"length")),
        'offset'         : setStringToNumber(getParameter({},"start")),
    }
    result_data = getApiData("/balance/transaction-summary" , queryData ,API_SERVER_BACKOFFICE)
    return json.dumps(result_data)       


#카드 기간별 잔액 관리 거래별 요약조회 리스트 엑셀 다운로드 요청            
#충전합계: TRNT-0001(충전)
@cardApi.route("/api/card/balance/transaction-summary/cargeSum/excelAll", methods=['GET'])
def cardDailyBalanceTransactionSummaryCargeSumExcelAll():
    formData = {}
    searchDate = getParameter(formData , "startDate").split(' - ')
    startDate = paramEscape(searchDate[0])
    endDate = paramEscape(searchDate[1])
    queryData = {
        'startDate'     : startDate,
        'endDate'       : endDate,
        'transactionType': "TRNT-0001",
        'limit'         : EXCEL_FILE_DOWNLOAD_COUNT,
        'offset'        : 0,
        'orderBy'       : getParameter(formData, "orderBy"),
        'empId'         : session['empId']
    }
    
    rootPath = current_app.root_path
    t1 = threading.Thread(target=cardChargeSumListExcelFile,args=[queryData,rootPath])
    t1.daemon = True
    t1.start()
    return "엑셀 작업요청"

#카드 기간별 잔액 관리 거래별 요약조회 리스 엑셀 다운로드 처리
#충전합계: TRNT-0001(충전)
def cardChargeSumListExcelFile(queryData,rootPath):
    excelZip = None
    jobStatus = 0
    batchId = None
    try:
        fileCnt = 1
        makeTime = str(int(round(time.time()*1000)))
        uploads = os.path.join(rootPath, "fileDownload" , "excel" , makeTime)
        if not os.path.isdir(uploads):
            os.makedirs(uploads)
        
        zipFileName = u'카드_기간별_충전합계'+ datetime.now().strftime('%Y%m%d') +'.zip'
        #작업 시작 메시지 추가
        batchId = postBatchMng({
            "reqId"    : queryData['empId'],
            "status"   : "BAT-0001" , # 진행중
            "filePath" : os.path.join(uploads ,zipFileName),
            "content"  : "카드 기간별 충전합계 엑셀 배치작업",
            "errMsg"   : ""
        })["data"]["batchId"]
        
        fileName = '카드_기간별_충전합계(' +  queryData['startDate'] + '~' + queryData['endDate'] + ').xlsx'
        workbook = xlsxwriter.Workbook(os.path.join(uploads ,setUnicodeEncodeTypeToEucKr(fileName)))
        worksheet = workbook.add_worksheet()
        money_format = workbook.add_format()
        money_format.set_num_format('_- #,##0_-;[red]- #,##0_-;_- "-"_-;_-@_-')
        
        title_format = workbook.add_format({'align':'center', 'valign':'vcenter', 'bold':True, 'border':1,'fg_color':'#A9D0F5'})
        string_format = workbook.add_format({'align':'center', 'valign':'vcenter'})
        summary_money_format = workbook.add_format({'fg_color' : '#E5E5E5'});
        summary_money_format.set_num_format('_- #,##0_-;[red]- #,##0_-;_- "-"_-;_-@_-')
        
        row = 0
        worksheet.write(row, 0  ,"번호", title_format)
        worksheet.write(row, 1  ,"거래처-서비스명", title_format)
        worksheet.write(row, 2  ,"충전", title_format)
        worksheet.write(row, 3  ,"충전취소", title_format)
        worksheet.write(row, 4  ,"충전합계", title_format)

        while True : 
            searchData = getApiData("/balance/transaction-summary" , queryData ,API_SERVER_BACKOFFICE)
            
            summaryData = searchData["totalData"]
            for data in searchData["data"]:
                
                row += 1
                worksheet.write(row, 0  ,row, string_format)    
                worksheet.write(row, 1  ,data["merchantName"]+" - "+data["serviceName"], string_format)
                worksheet.write(row, 2  ,data["transactionAmount"], money_format)
                worksheet.write(row, 3  ,data["cancelTransactionAmount"], money_format)
                worksheet.write(row, 4  ,data["transactionSum"], money_format)        
              
                
                if row >= EXCEL_FILE_MAKE_LIMT_COUNT :
                    row = 0
                    fileCnt += 1
                    fileName = '카드_기간별_충전합계(' +  queryData['startDate'] + '~' + queryData['endDate'] + ').xlsx'
                    # 디비 조회건수 * 2 row 생성시 파일 재생성
                    workbook.close()
                    workbook = xlsxwriter.Workbook(os.path.join(uploads ,setUnicodeEncodeTypeToEucKr(fileName)))
                    worksheet = workbook.add_worksheet()
                    worksheet.write(row, 0  ,"번호", title_format)
                    worksheet.write(row, 1  ,"거래처-서비스명", title_format)
                    worksheet.write(row, 2  ,"충전", title_format)
                    worksheet.write(row, 3  ,"충전취소", title_format)
                    worksheet.write(row, 4  ,"충전합계", title_format)
              
            row += 1
            worksheet.write(row, 0  ,"", summary_money_format)    
            worksheet.write(row, 1  ,"", summary_money_format)
            worksheet.write(row, 2  ,summaryData["transactionAmount"], summary_money_format)
            worksheet.write(row, 3  ,summaryData["cancelTransactionAmount"], summary_money_format)
            worksheet.write(row, 4  ,summaryData["transactionSum"], summary_money_format)        
              
                
            if row >= EXCEL_FILE_MAKE_LIMT_COUNT :
                row = 0
                fileCnt += 1
                fileName = '카드_기간별_충전합계(' +  queryData['startDate'] + '~' + queryData['endDate'] + ').xlsx'
                # 디비 조회건수 * 2 row 생성시 파일 재생성
                workbook.close()
                workbook = xlsxwriter.Workbook(os.path.join(uploads ,setUnicodeEncodeTypeToEucKr(fileName)))
                worksheet = workbook.add_worksheet()
                worksheet.write(row, 0  ,"번호", title_format)
                worksheet.write(row, 1  ,"거래처-서비스명", title_format)
                worksheet.write(row, 2  ,"충전", title_format)
                worksheet.write(row, 3  ,"충전취소", title_format)
                worksheet.write(row, 4  ,"충전합계", title_format)        
    
            queryData["offset"] = queryData["offset"] + EXCEL_FILE_DOWNLOAD_COUNT 
            if len(searchData["data"])+1 < EXCEL_FILE_DOWNLOAD_COUNT : 
                break
        workbook.close()
        excelZip = zipfile.ZipFile(os.path.join(uploads ,zipFileName),'w')
        for folder, subfolders, files in os.walk(uploads):
            for file in files:
                if file.endswith('.xlsx'):
                    excelZip.write(os.path.join(folder ,file), setUnicodeFormatToEucKr(file), compress_type=zipfile.ZIP_DEFLATED)
                    
    except Exception as err:
        #에러 메시지 추가
        putBatchMng({
            "batchId"  : str(batchId),
            "reqId"    : queryData['empId'],
            "status"   : "BAT-0003" , # 진행중
            "errMsg"   : str(err)
        })
        jobStatus = 1
        print err
        
    finally:
        if excelZip != None:
            excelZip.close()
        if jobStatus == 0 :    
            putBatchMng({
                "batchId"  : str(batchId),
                "reqId"    : queryData['empId'],
                "status"   : "BAT-0002" , # 진행중
                "errMsg"   : ""
            })               
        #성공 메시지 추가
        print "성공"
        

#카드 기간별 잔액 관리 거래별 요약조회 리스트 엑셀 다운로드 요청
#결제합계: TRNT-0002(결제)          
@cardApi.route("/api/card/balance/transaction-summary/paySum/excelAll", methods=['GET'])
def cardDailyBalanceTransactionSummaryPaySumExcelAll():
    formData = {}
    searchDate = getParameter(formData , "startDate").split(' - ')
    startDate = paramEscape(searchDate[0])
    endDate = paramEscape(searchDate[1])
    queryData = {
        'startDate'     : startDate,
        'endDate'       : endDate,
        'transactionType': "TRNT-0002",
        'limit'         : EXCEL_FILE_DOWNLOAD_COUNT,
        'offset'        : 0,
        'orderBy'       : getParameter(formData, "orderBy"),
        'empId'         : session['empId']
    }
    
    
    rootPath = current_app.root_path
    t1 = threading.Thread(target=cardPaySumListExcelFile,args=[queryData,rootPath])
    t1.daemon = True
    t1.start()
    return "엑셀 작업요청"



#카드 기간별 잔액 관리 거래별 요약조회 리스 엑셀 다운로드 처리
#결제합계: TRNT-0002(결제)
def cardPaySumListExcelFile(queryData,rootPath):
    excelZip = None
    jobStatus = 0
    batchId = None
    try:
        fileCnt = 1
        makeTime = str(int(round(time.time()*1000)))
        uploads = os.path.join(rootPath, "fileDownload" , "excel" , makeTime)
        if not os.path.isdir(uploads):
            os.makedirs(uploads)
        
        zipFileName = u'카드_기간별_결제합계'+ datetime.now().strftime('%Y%m%d') +'.zip'
        #작업 시작 메시지 추가
        batchId = postBatchMng({
            "reqId"    : queryData['empId'],
            "status"   : "BAT-0001" , # 진행중
            "filePath" : os.path.join(uploads ,zipFileName),
            "content"  : "카드 기간별 결제합계 엑셀 배치작업",
            "errMsg"   : ""
        })["data"]["batchId"]
        
        fileName = '카드_기간별_결제합계(' +  queryData['startDate'] + '~' + queryData['endDate'] + ').xlsx'
        workbook = xlsxwriter.Workbook(os.path.join(uploads ,setUnicodeEncodeTypeToEucKr(fileName)))
        worksheet = workbook.add_worksheet()
        money_format = workbook.add_format()
        money_format.set_num_format('_- #,##0_-;[red]- #,##0_-;_- "-"_-;_-@_-')
        
        title_format = workbook.add_format({'align':'center', 'valign':'vcenter', 'bold':True, 'border':1,'fg_color':'#A9D0F5'})
        string_format = workbook.add_format({'align':'center', 'valign':'vcenter'})
        summary_money_format = workbook.add_format({'fg_color' : '#E5E5E5'});
        summary_money_format.set_num_format('_- #,##0_-;[red]- #,##0_-;_- "-"_-;_-@_-')
        
        row = 0
        worksheet.write(row, 0  ,"번호", title_format)
        worksheet.write(row, 1  ,"거래처-서비스명", title_format)
        worksheet.write(row, 2  ,"결제", title_format)
        worksheet.write(row, 3  ,"결제취소", title_format)
        worksheet.write(row, 4  ,"결제합계", title_format)

        while True : 
            searchData = getApiData("/balance/transaction-summary" , queryData ,API_SERVER_BACKOFFICE)
            summaryData = searchData["totalData"]
            for data in searchData["data"]:
                
                row += 1
                worksheet.write(row, 0  ,row, string_format)    
                worksheet.write(row, 1  ,data["merchantName"]+" - "+data["serviceName"], string_format)
                worksheet.write(row, 2  ,data["transactionAmount"], money_format)
                worksheet.write(row, 3  ,data["cancelTransactionAmount"], money_format)
                worksheet.write(row, 4  ,data["transactionSum"], money_format)        
              
                
                if row >= EXCEL_FILE_MAKE_LIMT_COUNT :
                    row = 0
                    fileCnt += 1
                    fileName = '카드_기간별_결제합계(' +  queryData['startDate'] + '~' + queryData['endDate'] + ').xlsx'
                    # 디비 조회건수 * 2 row 생성시 파일 재생성
                    workbook.close()
                    workbook = xlsxwriter.Workbook(os.path.join(uploads ,setUnicodeEncodeTypeToEucKr(fileName)))
                    worksheet = workbook.add_worksheet()
                    worksheet.write(row, 0  ,"번호", title_format)
                    worksheet.write(row, 1  ,"거래처-서비스명", title_format)
                    worksheet.write(row, 2  ,"결제", title_format)
                    worksheet.write(row, 3  ,"결제취소", title_format)
                    worksheet.write(row, 4  ,"결제합계", title_format)
                    
            row += 1
            worksheet.write(row, 0  ,"", summary_money_format)    
            worksheet.write(row, 1  ,"", summary_money_format)
            worksheet.write(row, 2  ,summaryData["transactionAmount"], summary_money_format)
            worksheet.write(row, 3  ,summaryData["cancelTransactionAmount"], summary_money_format)
            worksheet.write(row, 4  ,summaryData["transactionSum"], summary_money_format)        
              
                
            if row >= EXCEL_FILE_MAKE_LIMT_COUNT :
                row = 0
                fileCnt += 1
                fileName = '카드_기간별_결제합계(' +  queryData['startDate'] + '~' + queryData['endDate'] + ').xlsx'
                # 디비 조회건수 * 2 row 생성시 파일 재생성
                workbook.close()
                workbook = xlsxwriter.Workbook(os.path.join(uploads ,setUnicodeEncodeTypeToEucKr(fileName)))
                worksheet = workbook.add_worksheet()
                worksheet.write(row, 0  ,"번호", title_format)
                worksheet.write(row, 1  ,"거래처-서비스명", title_format)
                worksheet.write(row, 2  ,"결제", title_format)
                worksheet.write(row, 3  ,"결제취소", title_format)
                worksheet.write(row, 4  ,"결제합계", title_format)        
    
            queryData["offset"] = queryData["offset"] + EXCEL_FILE_DOWNLOAD_COUNT 
            if len(searchData["data"])+1 < EXCEL_FILE_DOWNLOAD_COUNT : 
                break
        workbook.close()
        excelZip = zipfile.ZipFile(os.path.join(uploads ,zipFileName),'w')
        for folder, subfolders, files in os.walk(uploads):
            for file in files:
                if file.endswith('.xlsx'):
                    excelZip.write(os.path.join(folder ,file), setUnicodeFormatToEucKr(file), compress_type=zipfile.ZIP_DEFLATED)
                    
    except Exception as err:
        #에러 메시지 추가
        putBatchMng({
            "batchId"  : str(batchId),
            "reqId"    : queryData['empId'],
            "status"   : "BAT-0003" , # 진행중
            "errMsg"   : str(err)
        })
        jobStatus = 1
        print err
        
    finally:
        if excelZip != None:
            excelZip.close()
        if jobStatus == 0 :    
            putBatchMng({
                "batchId"  : str(batchId),
                "reqId"    : queryData['empId'],
                "status"   : "BAT-0002" , # 진행중
                "errMsg"   : ""
            })               
        #성공 메시지 추가
        print "성공"
        
#카드 기간별 잔액 관리 거래별 요약조회 리스트 엑셀 다운로드 요청
#환불합계: TRNT-0003(환불)          
@cardApi.route("/api/card/balance/transaction-summary/refundSum/excelAll", methods=['GET'])
def cardDailyBalanceTransactionSummaryRefundSumExcelAll():
    formData = {}
    searchDate = getParameter(formData , "startDate").split(' - ')
    startDate = paramEscape(searchDate[0])
    endDate = paramEscape(searchDate[1])
    queryData = {
        'startDate'     : startDate,
        'endDate'       : endDate,
        'transactionType': "TRNT-0003",
        'limit'         : EXCEL_FILE_DOWNLOAD_COUNT,
        'offset'        : 0,
        'orderBy'       : getParameter(formData, "orderBy"),
        'empId'         : session['empId']
    }
    
    rootPath = current_app.root_path
    t1 = threading.Thread(target=cardRefundAmountListExcelFile,args=[queryData,rootPath])
    t1.daemon = True
    t1.start()
    return "엑셀 작업요청"  
  
        

#카드 기간별 잔액 관리 거래별 요약조회 리스 엑셀 다운로드 처리]
#환불합계: TRNT-0003(환불)
def cardRefundAmountListExcelFile(queryData,rootPath):
    excelZip = None
    jobStatus = 0
    batchId = None
    try:
        fileCnt = 1
        makeTime = str(int(round(time.time()*1000)))
        uploads = os.path.join(rootPath, "fileDownload" , "excel" , makeTime)
        if not os.path.isdir(uploads):
            os.makedirs(uploads)
        
        zipFileName = u'카드_기간별_환불합계'+ datetime.now().strftime('%Y%m%d') +'.zip'
        #작업 시작 메시지 추가
        batchId = postBatchMng({
            "reqId"    : queryData['empId'],
            "status"   : "BAT-0001" , # 진행중
            "filePath" : os.path.join(uploads ,zipFileName),
            "content"  : "카드 기간별 환불합계 엑셀 배치작업",
            "errMsg"   : ""
        })["data"]["batchId"]
        
        fileName = '카드_기간별_별_환불합계(' +  queryData['startDate'] + '~' + queryData['endDate'] + ').xlsx'
        workbook = xlsxwriter.Workbook(os.path.join(uploads ,setUnicodeEncodeTypeToEucKr(fileName)))
        worksheet = workbook.add_worksheet()
        money_format = workbook.add_format()
        money_format.set_num_format('_- #,##0_-;[red]- #,##0_-;_- "-"_-;_-@_-')
        
        title_format = workbook.add_format({'align':'center', 'valign':'vcenter', 'bold':True, 'border':1,'fg_color':'#A9D0F5'})
        string_format = workbook.add_format({'align':'center', 'valign':'vcenter'})
        summary_money_format = workbook.add_format({'fg_color' : '#E5E5E5'});
        summary_money_format.set_num_format('_- #,##0_-;[red]- #,##0_-;_- "-"_-;_-@_-')
        
        row = 0
        worksheet.write(row, 0  ,"번호", title_format)
        worksheet.write(row, 1  ,"거래처-서비스명", title_format)
        worksheet.write(row, 2  ,"환불금액", title_format)

        while True : 
            searchData = getApiData("/balance/transaction-summary" , queryData ,API_SERVER_BACKOFFICE)
            
            summaryData = searchData["totalData"]
            for data in searchData["data"]:
                
                row += 1
                worksheet.write(row, 0  ,row, string_format)    
                worksheet.write(row, 1  ,data["merchantName"]+" - "+data["serviceName"], string_format)
                worksheet.write(row, 2  ,data["transactionSum"], money_format)        
              
            
                
                if row >= EXCEL_FILE_MAKE_LIMT_COUNT :
                    row = 0
                    fileCnt += 1
                    fileName = '카드_기간별_환불합계(' +  queryData['startDate'] + '~' + queryData['endDate'] + ').xlsx'
                    # 디비 조회건수 * 2 row 생성시 파일 재생성
                    workbook.close()
                    workbook = xlsxwriter.Workbook(os.path.join(uploads ,setUnicodeEncodeTypeToEucKr(fileName)))
                    worksheet = workbook.add_worksheet()
                    worksheet.write(row, 0  ,"번호", title_format)
                    worksheet.write(row, 1  ,"거래처-서비스명", title_format)
                    worksheet.write(row, 2  ,"환불금액", title_format)
                    
                    
            row += 1
            worksheet.write(row, 0  ,"", summary_money_format)    
            worksheet.write(row, 1  ,"", summary_money_format)
            worksheet.write(row, 2  ,summaryData["transactionSum"], summary_money_format)  
            
            if row >= EXCEL_FILE_MAKE_LIMT_COUNT :
                row = 0
                fileCnt += 1
                fileName = '카드_기간별_환불합계(' +  queryData['startDate'] + '~' + queryData['endDate'] + ').xlsx'
                # 디비 조회건수 * 2 row 생성시 파일 재생성
                workbook.close()
                workbook = xlsxwriter.Workbook(os.path.join(uploads ,setUnicodeEncodeTypeToEucKr(fileName)))
                worksheet = workbook.add_worksheet()
                worksheet.write(row, 0  ,"번호", title_format)
                worksheet.write(row, 1  ,"거래처-서비스명", title_format)
                worksheet.write(row, 2  ,"환불금액", title_format)              
                      
    
            queryData["offset"] = queryData["offset"] + EXCEL_FILE_DOWNLOAD_COUNT 
            if len(searchData["data"])+1 < EXCEL_FILE_DOWNLOAD_COUNT : 
                break
        workbook.close()
        excelZip = zipfile.ZipFile(os.path.join(uploads ,zipFileName),'w')
        for folder, subfolders, files in os.walk(uploads):
            for file in files:
                if file.endswith('.xlsx'):
                    excelZip.write(os.path.join(folder ,file), setUnicodeFormatToEucKr(file), compress_type=zipfile.ZIP_DEFLATED)
                    
    except Exception as err:
        #에러 메시지 추가
        putBatchMng({
            "batchId"  : str(batchId),
            "reqId"    : queryData['empId'],
            "status"   : "BAT-0003" , # 진행중
            "errMsg"   : str(err)
        })
        jobStatus = 1
        print err
        
    finally:
        if excelZip != None:
            excelZip.close()
        if jobStatus == 0 :    
            putBatchMng({
                "batchId"  : str(batchId),
                "reqId"    : queryData['empId'],
                "status"   : "BAT-0002" , # 진행중
                "errMsg"   : ""
            })               
        #성공 메시지 추가
        print "성공"