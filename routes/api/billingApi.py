# -- coding:utf-8 --
'''
Created on 2017. 3. 30.

@author: sanghyun
'''
import json
import os
import threading
import zipfile
import time
import datetime
import xlsxwriter

from flask import Blueprint, request
from flask.globals import current_app, session
from werkzeug import secure_filename

from routes.api.systemMngApi import postBatchMng, putBatchMng
from util.common import  API_SERVER_BACKOFFICE, paramEscape, putApiData, postApiData, getApiData, getApiSingleData, getData, allower_file, UPLOAD_FOLDER, \
    getParameter, setStringToNumber, EXCEL_FILE_DOWNLOAD_COUNT, parseDate, \
    EXCEL_FILE_MAKE_LIMT_COUNT, setUnicodeEncodeTypeToEucKr, setUnicodeFormatToEucKr
from types import NoneType



billingApi = Blueprint('billingApi', __name__)

@billingApi.route('/api/billing/fileUpload' , methods=['POST'])
def fileUpload():
    print os.path.join(os.getcwd(), UPLOAD_FOLDER, "test")
    print request.files
    if 'qqfile' not in request.files:
        print 'filenotFound'
        return json.dumps({
            "success" : "false",
            "error" : "fileNotFound"
        })
    file = request.files['qqfile']
    if file.filename == '':
        print 'No selected file'
        return 'fileNotFound'
    else :
        filename = secure_filename(file.filename)
        file.save(os.path.join(os.getcwd(), UPLOAD_FOLDER, filename)) 
    return json.dumps({
            'success' : "true"
        })
    
@billingApi.route('/api/billing/billingHistory' , methods=['GET'])
def billingHistory():
    form_data = json.loads(request.args.get("formData"))
    searchDate = getParameter(form_data , "searchDate").split(' - ')
        
    queryData = {
        'startDate': paramEscape(searchDate[0]),
        'endDate': paramEscape(searchDate[1]),
        'serviceType': getParameter(form_data,"serviceType"),
        'dateType': getParameter(form_data,"dateType"),
        'merchantId': getParameter(form_data,"merchantId"),
        'serviceId': getParameter(form_data,"serviceId"),
        'billingDuration': getParameter(form_data,"bilcType"),
        'adjustType': getParameter(form_data,"adjustType"),
        'offset': setStringToNumber(request.args.get("start")),
        'limit': setStringToNumber(request.args.get("length")),
        'excelAllFlag' : '0'
    }
    result_data = getApiData("/billings" ,queryData)
    return json.dumps(result_data)

@billingApi.route('/api/billing/billingDetail', methods=['GET'])
def billingDetail():
    url = "/billing?seq=" + request.args.get("seq")
    
    result_data = getApiSingleData(url, {})
    return json.dumps(result_data)

@billingApi.route('/api/billing/billings' , methods=['GET'])
def billings():
    form_data = json.loads(request.args.get("formData"))
    searchDate = getParameter(form_data , "searchDate").split(' - ')
    
    queryData = {
        'merchantId': getParameter(form_data, "merchantId"),
        'serviceId': getParameter(form_data, "serviceId"),
        'serviceType': getParameter(form_data, "serviceType"),
        'dateType': getParameter(form_data, "dateType"),
        'startDate': paramEscape(searchDate[0]),
        'endDate': paramEscape(searchDate[1]),
        'billingType': getParameter(form_data, "billingType"),
        'status': getParameter(form_data, "status"),        
        'offset': setStringToNumber(request.args.get("start")),
        'limit': setStringToNumber(request.args.get("length")),
        'excelAllFlag' : '0'
    }
    
    result_data = getApiData("/regbillings", queryData)
    
    return json.dumps(result_data)

@billingApi.route('/api/billing/billingsDetail' , methods=['GET'])
def billingsDetail():
    url = "/regbilling?seq=" + request.args.get("seq")
    
    result_data = getApiSingleData(url, {})
    
    return json.dumps(result_data)

@billingApi.route('/api/billing/billingHistory/excelAll', methods=['GET'])
def excelAll():    
    searchDate = getParameter({} , "searchDate").split(' - ')
      
    queryData = {
        'startDate': paramEscape(searchDate[0]),
        'endDate': paramEscape(searchDate[1]),
        'serviceType': getParameter({}, "serviceType"),
        'dateType': getParameter({}, "dateType"),
        'merchantId': getParameter({}, "merchantId"),
        'serviceId': getParameter({}, "serviceId"),
        'billingDuration': getParameter({}, "bilcType"),
        'empId' : session['empId'],
        'offset': setStringToNumber(request.args.get("start")),
        'limit': setStringToNumber(request.args.get("length")),
        'excelAllFlag': '1'      
    }
    
    rootPath = current_app.root_path
    t1 = threading.Thread(target=makeBillingExcelFile,args=[queryData,rootPath])
    t1.daemon = True
    t1.start()
    
    return "엑셀 작업요청"

def makeBillingExcelFile(queryData,rootPath):
    excelZip = None
    jobStatus = 0
    batchId = None
    try:
        fileCnt = 1
        makeTime = str(int(round(time.time()*1000)))
        uploads = os.path.join(rootPath, "fileDownload" , "excel" , makeTime)
        if not os.path.isdir(uploads):
            os.makedirs(uploads)
        zipFileName = u'정산명세서_'+ datetime.datetime.now().strftime('%Y%m%d') +'.zip'
        #작업 시작 메시지 추가
        batchId = postBatchMng({
            "reqId"    : queryData['empId'],
            "status"   : "BAT-0001" , # 진행중
            "filePath" : os.path.join(uploads ,zipFileName),
            "content"  : "정산명세서 엑셀 배치작업",
            "errMsg"   : ""
        })["data"]["batchId"]            
        fileName = '정산명세서_' + datetime.datetime.now().strftime('%Y%m%d') + '_' +  str(fileCnt) +  '.xlsx'
        workbook = xlsxwriter.Workbook(os.path.join(uploads ,setUnicodeEncodeTypeToEucKr(fileName)))
        worksheet = workbook.add_worksheet()
        money_format = workbook.add_format({'align':'right'})
        money_format.set_num_format('_- #,##0_-;[red]- #,##0_-;_- "-"_-;_-@_-')
        
        title_format = workbook.add_format({'align':'center', 'valign':'vcenter', 'bold':True, 'border':1,'fg_color':'#A9D0F5'})
        string_format = workbook.add_format({'align':'center', 'valign':'vcenter'})
        row = 1
        
        worksheet.write(0, 0, "순번", title_format)
        worksheet.write(0, 1, "거래처명", title_format)
        worksheet.write(0, 2, "서비스명", title_format)
        worksheet.write(0, 3, "정산기간", title_format)
        worksheet.write(0, 4, "정산지급일", title_format)
        worksheet.write(0, 5, "거래구분", title_format)
        worksheet.write(0, 6, "거래금액", title_format)
        worksheet.write(0, 7, "거래 취소 금액", title_format)
        worksheet.write(0, 8, "총 거래금액", title_format)
        worksheet.write(0, 9, "결제금액", title_format)
        worksheet.write(0, 10, "할인금액", title_format)
        worksheet.write(0, 11, "정산 타입", title_format)
        worksheet.write(0, 12, "정산주기", title_format)
        worksheet.write(0, 13, "거래건수", title_format)
        worksheet.write(0, 14, "정산 수수료", title_format)
        worksheet.write(0, 15, "수수료 타입", title_format)
        worksheet.write(0, 16, "부가세 타입", title_format)
        worksheet.write(0, 17, "수수료", title_format)
        worksheet.write(0, 18, "부가세", title_format)
        worksheet.write(0, 19, "수수료 합계", title_format)
        worksheet.write(0, 20, "정산금액", title_format)
        worksheet.write(0, 21, "은행", title_format)
        worksheet.write(0, 22, "예금주", title_format)
        worksheet.write(0, 23, "계좌번호", title_format) 
        
        while True : 
            searchData = getData("/billings" ,queryData)
            
            for data in searchData["resultList"]:
                row += 1
                if(data["merchantCommision"] is not None) :
                    merchantComission = data["merchantCommision"]+"%" if data["merchantCommType"] =="FEE-0001" else data["merchantCommision"]+"원" if data["merchantCommType"]=="FEE-0002" else "-"
                else :  
                    merchantComission = "-"
                worksheet.write(row, 0, (row-1), string_format)
                worksheet.write(row, 1, data["submerchantName"], string_format)
                worksheet.write(row, 2, data["serviceName"], string_format)
                worksheet.write(row, 3, data["approvalDtMin"]+" ~ "+data["approvalDtMax"], string_format)
                worksheet.write(row, 4, data["billingDt"], string_format)
                worksheet.write(row, 5, data["typeName"], string_format)                
                worksheet.write(row, 6, data["amount"],money_format)
                worksheet.write(row, 7, data["cancelAmount"],money_format)
                worksheet.write(row, 8, data["totalAmount"],money_format)
                worksheet.write(row, 9, data["payAmount"],money_format)
                worksheet.write(row, 10, data["dcAmount"],money_format)
                worksheet.write(row, 11, data["billingCommType"], string_format)
                worksheet.write(row, 12, data["billingDuration"], string_format)
                worksheet.write(row, 13, data["cnt"], string_format)
                worksheet.write(row, 14, merchantComission, string_format)
                worksheet.write(row, 15, data["commTypeName"], string_format)
                worksheet.write(row, 16, data["taxTypeName"], string_format)
                worksheet.write(row, 17, data["commision"],money_format)
                worksheet.write(row, 18, data["tax"],money_format)
                worksheet.write(row, 19, data["commTotal"],money_format)
                worksheet.write(row, 20, data["billingAmount"],money_format)
                worksheet.write(row, 21, data["bankNm"], string_format)
                worksheet.write(row, 22, data["bankHolder"], string_format)
                worksheet.write(row, 23, data["bankAccNo"], string_format)
            
                if row >= EXCEL_FILE_MAKE_LIMT_COUNT :
                    row = 2
                    fileCnt += 1
                    fileName = '거래내역_결제_' +  datetime.datetime.now().strftime('%Y%m%d') + '_' + str(fileCnt) +  '.xlsx'
                    # 디비 조회건수 * 2 row 생성시 파일 재생성
                    workbook.close()
                    workbook = xlsxwriter.Workbook(os.path.join(uploads ,setUnicodeEncodeTypeToEucKr(fileName)))
                    worksheet = workbook.add_worksheet()
                    money_format = workbook.add_format()
                    money_format.set_num_format('_- #,##0_-;[red]- #,##0_-;_- "-"_-;_-@_-')
                    worksheet.write(0, 0, "순번", title_format)
                    worksheet.write(0, 1, "거래처명", title_format)
                    worksheet.write(0, 2, "서비스명", title_format)
                    worksheet.write(0, 3, "정산기간", title_format)
                    worksheet.write(0, 4, "정산지급일", title_format)
                    worksheet.write(0, 5, "거래구분", title_format)
                    worksheet.write(0, 6, "거래금액", title_format)
                    worksheet.write(0, 7, "거래 취소 금액", title_format)
                    worksheet.write(0, 8, "총 거래금액", title_format)
                    worksheet.write(0, 9, "결제금액", title_format)
                    worksheet.write(0, 10, "할인금액", title_format)
                    worksheet.write(0, 11, "정산 타입", title_format)
                    worksheet.write(0, 12, "정산주기", title_format)
                    worksheet.write(0, 13, "거래건수", title_format)
                    worksheet.write(0, 14, "정산 수수료", title_format)
                    worksheet.write(0, 15, "수수료 타입", title_format)
                    worksheet.write(0, 16, "부가세 타입", title_format)
                    worksheet.write(0, 17, "수수료", title_format)
                    worksheet.write(0, 18, "부가세", title_format)
                    worksheet.write(0, 19, "수수료 합계", title_format)
                    worksheet.write(0, 20, "정산금액", title_format)
                    worksheet.write(0, 21, "은행", title_format)
                    worksheet.write(0, 22, "예금주", title_format)
                    worksheet.write(0, 23, "계좌번호", title_format)                      
            queryData["offset"] = queryData["offset"] + EXCEL_FILE_DOWNLOAD_COUNT 
            if len(searchData["resultList"]) < EXCEL_FILE_DOWNLOAD_COUNT : 
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

@billingApi.route('/api/billing/', methods=['POST'])
def billing():
    form_data = request.json 
    billingSeq = getParameter(form_data,"billingSeq")
    requestData = {
        "refTitle"           :  getParameter(form_data,"serviceName"),   #승인 목록을 검색하기 위한 Keyword
        "workType"          :   "AWRK-0006",                            #승인 요청 구분(Code)
        "reqType"           :   "AREQ-0001", 
        "reqEmpId"          :   session['empId'],                       #요청자
        "apprEmpId"         :   getParameter(form_data,"apprEmpId"),    #승인자
        "reqMemo"           :   "정산명세서 등록",      #요청 사유
        "keyword"           :   getParameter(form_data,"serviceName"),       #승인 목록을 검색하기 위한 Keyword
        "seq"               :   getParameter(form_data,"seq"),          #승인요청 번호
        "contentSeq"        :   getParameter(form_data,"contentSeq"),   #승인 data 등록번호
        "refId"             :   billingSeq,       #중복승인을 막기 위한 고유 검색 Keyword     
        
        "contentData"       :   json.dumps({
            "seq"     :   billingSeq,               
            "billingAmount"     :   getParameter(form_data,"billingAmount"),
            "dcAmount"            :   getParameter(form_data,"dcAmount"),
            "etcAmount"           :   paramEscape(getParameter(form_data,"etcAmount")),                  
            "commTotal"   :   paramEscape(getParameter(form_data,"commTotal")),                 
            "tax"      :   getParameter(form_data,"tax"),               
            "adjustmentAmount"       :   paramEscape(getParameter(form_data,"adjustmentAmount")), 
            "differenceAmount"    :   getParameter(form_data,"differenceAmount"), 
            "amount" : getParameter(form_data,"amount"),
            "commision"    : getParameter(form_data,"commision"),
            "notMatchedAmount"    : getParameter(form_data,"notMatchedAmount"),
            "totTransAmount"    : getParameter(form_data,"totTransAmount"),
            "cancelAmount"    : getParameter(form_data,"cancelAmount"),
            "payAmount"    : getParameter(form_data,"payAmount"),
            "commRatio"    : getParameter(form_data,"commRatio"),
            "descMemo"    : getParameter(form_data,"memo")
        })
    }   

    reponseResult = postApiData("/approval/request/approval", requestData, API_SERVER_BACKOFFICE)    
    return json.dumps(reponseResult)

@billingApi.route('/api/billing/', methods=['PUT'])
def putBilling():
    form_data = request.json 
    billingSeq = getParameter(form_data,"billingSeq")
    requestData = {
        "refTitle"           :  getParameter(form_data,"serviceName"),   #승인 목록을 검색하기 위한 Keyword
        "workType"          :   "AWRK-0006",                            #승인 요청 구분(Code)
        "reqType"           :   "AREQ-0001", 
        "reqEmpId"          :   session['empId'],                       #요청자
        "apprEmpId"         :   getParameter(form_data,"apprEmpId"),    #승인자
        "reqMemo"           :   "정산명세서 등록",      #요청 사유
        "keyword"           :   getParameter(form_data,"serviceName"),       #승인 목록을 검색하기 위한 Keyword
        "seq"               :   getParameter(form_data,"seq"),          #승인요청 번호
        "contentSeq"        :   getParameter(form_data,"contentSeq"),   #승인 data 등록번호
        "refId"             :   billingSeq,       #중복승인을 막기 위한 고유 검색 Keyword     
        
        "contentData"       :   json.dumps({
            "seq"     :   billingSeq,               
            "billingAmount"     :   getParameter(form_data,"billingAmount"),
            "dcAmount"            :   getParameter(form_data,"dcAmount"),
            "etcAmount"           :   paramEscape(getParameter(form_data,"etcAmount")),                  
            "commTotal"   :   paramEscape(getParameter(form_data,"commTotal")),                 
            "tax"      :   getParameter(form_data,"tax"),               
            "adjustmentAmount"       :   paramEscape(getParameter(form_data,"adjustmentAmount")), 
            "differenceAmount"    :   getParameter(form_data,"differenceAmount"), 
            "amount" : getParameter(form_data,"amount"),
            "commision"    : getParameter(form_data,"commision"),
            "notMatchedAmount"    : getParameter(form_data,"notMatchedAmount"),
            "totTransAmount"    : getParameter(form_data,"totTransAmount"),
            "cancelAmount"    : getParameter(form_data,"cancelAmount"),
            "payAmount"    : getParameter(form_data,"payAmount"),
            "descMemo"    : getParameter(form_data,"memo")
        })
    }   

    reponseResult = putApiData("/approval/request/approval", requestData, {}, API_SERVER_BACKOFFICE)    
    return json.dumps(reponseResult)

