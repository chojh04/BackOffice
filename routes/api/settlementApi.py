# -*- coding:utf-8 -*-
import datetime
import json
import os
import sys
import threading
import time
import zipfile

from flask import Blueprint, request
from flask.globals import session, current_app
import xlsxwriter

from routes.api.systemMngApi import postBatchMng, putBatchMng
from util.common import paramEscape, getApiData, getParameter, getData, setStringToNumber, \
    API_SERVER_BILLINGSERVICE, parseDate, EXCEL_FILE_MAKE_LIMT_COUNT, \
    EXCEL_FILE_DOWNLOAD_COUNT, setUnicodeEncodeTypeToEucKr, setUnicodeFormatToEucKr

settlementApi = Blueprint("settlementApi", __name__)

@settlementApi.route("/api/settlementApi/settlement/gsStatistics", methods=['GET'])
def getGsSettlementStatistics():
    form_data = json.loads(request.args.get("formData"))
    searchDate = getParameter(form_data , "startDate").split(' - ')
    startDate = paramEscape(searchDate[0])
    endDate = paramEscape(searchDate[1])    
    
    queryData = {
        "jobDivider" : getParameter(form_data,"selType"), #String, //직원 ID
        "startDate"  : startDate,
        "endDate"    : endDate,
         
    }
    resultData = getApiData("/v1/settlement/gsStatistics", queryData , API_SERVER_BILLINGSERVICE)
    print(resultData)
    return json.dumps(resultData)

@settlementApi.route("/api/settlementApi/settlement/hmStatistics", methods=['GET'])
def getHmSettlementStatistics():
    form_data = json.loads(request.args.get("formData"))
    searchDate = getParameter(form_data , "startDate").split(' - ')
    startDate = paramEscape(searchDate[0])
    endDate = paramEscape(searchDate[1])    
    
    queryData = {
        "jobDivider" : getParameter(form_data,"selType"), #String, //직원 ID
        "startDate"  : startDate,
        "endDate"    : endDate,
         
    }
    resultData = getApiData("/v1/settlement/hmStatistics", queryData , API_SERVER_BILLINGSERVICE)
    print(resultData)
    return json.dumps(resultData)

@settlementApi.route("/api/settlementApi/settlement/gsStatistics/errorDetail", methods=['GET'])
def errorDetail():
    form_data = json.loads(request.args.get("formData"))
    queryData = {
        "jobDivider" : getParameter(form_data,"jobDivider"),
        "workDt" : getParameter(form_data,"workDt"), 
        'limit': setStringToNumber(request.args.get("length")),
        'offset': setStringToNumber(request.args.get("start")),
    }
    resultData = getApiData("/v1/settlement/gsStatistics/errorDetail", queryData , API_SERVER_BILLINGSERVICE)
    return json.dumps(resultData)

@settlementApi.route("/api/settlementApi/settlement/hmStatistics/errorDetail", methods=['GET'])
def hmErrorDetail():
    form_data = json.loads(request.args.get("formData"))
    queryData = {
        "jobDivider" : getParameter(form_data,"jobDivider"),
        "workDt" : getParameter(form_data,"workDt"), 
        'limit': setStringToNumber(request.args.get("length")),
        'offset': setStringToNumber(request.args.get("start")),
    }
    resultData = getApiData("/v1/settlement/hmStatistics/errorDetail", queryData , API_SERVER_BILLINGSERVICE)
    return json.dumps(resultData)

@settlementApi.route("/api/settlementApi/settlement/gsStatistics/errorDetailExcel", methods=['GET'])
def errorDetailExcel():
    form_data = {}
    queryData = {
        "jobDivider" : getParameter(form_data,"jobDivider"),
        "workDt" : getParameter(form_data,"workDt"),
        'offset': 0,
        'limit': EXCEL_FILE_DOWNLOAD_COUNT,         
        "empId" : session['empId']
    }
    rootPath = current_app.root_path
    t1 = threading.Thread(target=makeSettlementErrorExcelFile,args=[queryData,rootPath])
    t1.daemon = True
    t1.start()
    
    return "엑셀 작업요청"

@settlementApi.route("/api/settlementApi/settlement/hmStatistics/errorDetailExcel", methods=['GET'])
def hmErrorDetailExcel():
    form_data = {}
    queryData = {
        "jobDivider" : getParameter(form_data,"jobDivider"),
        "workDt" : getParameter(form_data,"workDt"),
        'offset': 0,
        'limit': EXCEL_FILE_DOWNLOAD_COUNT,         
        "empId" : session['empId']
    }
    rootPath = current_app.root_path
    t1 = threading.Thread(target=makeHmSettlementErrorExcelFile,args=[queryData,rootPath])
    t1.daemon = True
    t1.start()
    
    return "엑셀 작업요청"


def makeSettlementErrorExcelFile(queryData,rootPath):
    excelZip = None
    jobStatus = 0
    batchId = None
    
    jobDivider = str(queryData.get('jobDivider'));
    if jobDivider is None :
        jobDivider = ""    
    
    try:
        fileCnt = 1
        makeDate = datetime.datetime.now().strftime('%Y%m%d')
        makeTime = str(int(round(time.time()*1000)))
        uploads = os.path.join(rootPath, "fileDownload" , "excel" , makeTime)
        if not os.path.isdir(uploads):
            os.makedirs(uploads)
        zipFileName = u'GS대사_불일치('+jobDivider+u')_'+ makeDate +'.zip'
        #작업 시작 메시지 추가
        batchId = postBatchMng({
            "reqId"    : queryData['empId'],
            "status"   : "BAT-0001" , # 진행중
            "filePath" : os.path.join(uploads ,zipFileName),
            "content"  : "GS대사 불일치",
            "errMsg"   : ""
        })["data"]["batchId"]            
        fileName = 'GS대사_불일치('+jobDivider+')_'+ makeDate+ '_' + str(fileCnt) + '.xlsx'
        workbook = xlsxwriter.Workbook(os.path.join(uploads , setUnicodeEncodeTypeToEucKr(fileName)))
        worksheet = workbook.add_worksheet()
        money_format = workbook.add_format()
        money_format.set_num_format('_- #,##0_-;[red]- #,##0_-;_- "-"_-;_-@_-')
        row = 0
        worksheet.write(row, 0  ,"거래처")
        worksheet.write(row, 1  ,"영업일자")
        worksheet.write(row, 2  ,"점포코드")
        worksheet.write(row, 3  ,"점포명(사용처)")
        worksheet.write(row, 4  ,"지불상태")
        worksheet.write(row, 5  ,"상태")
        worksheet.write(row, 6  ,"주문번호")
        worksheet.write(row, 7  ,"승인번호")
        worksheet.write(row, 8  ,"승인일자")
        worksheet.write(row, 9  ,"승인시간")
        worksheet.write(row, 10  ,"거래금액")
        worksheet.write(row, 11 ,"카드번호")
        worksheet.write(row, 12 ,"불일치내역")
        while True : 
            searchData = getData("/v1/settlement/gsStatistics/errorDetailAll" ,queryData,API_SERVER_BILLINGSERVICE)
            for data in searchData["resultList"]:
                row += 1
                worksheet.write(row, 0  ,data["jobDivider"])
                worksheet.write(row, 1  ,data["saleDt"])
                worksheet.write(row, 2  ,data["storeCd"])
                worksheet.write(row, 3  ,data["storeNm"])
                worksheet.write(row, 4  ,data["dealType"])
                worksheet.write(row, 5  ,data["dealDivider"])
                worksheet.write(row, 6  ,data["dealNo"])
                worksheet.write(row, 7  ,data["approvalNo"])
                worksheet.write(row, 8  ,parseDate(data["approvalDt"] ,'%Y%m%d' ,'%Y-%m-%d'))
                
                if data["approvalTime"] is None:
                    worksheet.write(row, 9, "")
                else:
                    worksheet.write(row, 9, parseDate(data["approvalDt"] + " " + data["approvalTime"],'%Y%m%d %H%M%S' ,'%H:%M:%S'))
                
                worksheet.write_number(row, 10  ,long(data["dealAmt"]), money_format)
                worksheet.write(row, 11 ,data["cardNo"])
                worksheet.write(row, 12 ,data["statusNm"])
                if row >= EXCEL_FILE_MAKE_LIMT_COUNT :
                    row = 0
                    fileCnt += 1
                    fileName = 'GS대사_불일치('+jobDivider+')_'+ makeDate+ '_' + str(fileCnt) + '.xlsx'
                    
                    # 디비 조회건수 * 2 row 생성시 파일 재생성
                    workbook.close()
                    workbook = xlsxwriter.Workbook(os.path.join(uploads , setUnicodeEncodeTypeToEucKr(fileName)))
                    money_format = workbook.add_format()
                    money_format.set_num_format('_- #,##0_-;[red]- #,##0_-;_- "-"_-;_-@_-')
                    worksheet = workbook.add_worksheet()
                    worksheet.write(row, 0  ,data["jobDivider"])
                    worksheet.write(row, 1  ,data["saleDt"])
                    worksheet.write(row, 2  ,data["storeCd"])
                    worksheet.write(row, 3  ,data["storeNm"])
                    worksheet.write(row, 4  ,data["dealType"])
                    worksheet.write(row, 5  ,data["dealDivider"])
                    worksheet.write(row, 6  ,data["dealNo"])
                    worksheet.write(row, 7  ,data["approvalNo"])
                    worksheet.write(row, 8  ,parseDate(data["approvalDt"] ,'%Y%m%d' ,'%Y-%m-%d'))
                                        
                    if data["approvalTime"] is None:
                        worksheet.write(row, 9  ,"")
                    else:
                        worksheet.write(row, 9  ,parseDate(data["approvalDt"] + " " + data["approvalTime"],'%Y%m%d %H%M%S' ,'%H:%M:%S'))
                
                    worksheet.write_number(row, 10  ,long(data["dealAmt"]), money_format)
                    worksheet.write(row, 11 ,data["cardNo"])
                    worksheet.write(row, 12 ,data["statusNm"])                          
            queryData["offset"] = queryData["offset"] + EXCEL_FILE_DOWNLOAD_COUNT 
            if len(searchData["resultList"]) < EXCEL_FILE_DOWNLOAD_COUNT : 
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
        
def makeHmSettlementErrorExcelFile(queryData,rootPath):
    excelZip = None
    jobStatus = 0
    batchId = None
    try:
        fileCnt = 1
        makeDate = datetime.datetime.now().strftime('%Y%m%d')
        makeTime = str(int(round(time.time()*1000)))
        uploads = os.path.join(rootPath, "fileDownload" , "excel" , makeTime)
        if not os.path.isdir(uploads):
            os.makedirs(uploads)
        zipFileName = u'HM대사_불일치_'+ makeDate +'.zip'
        #작업 시작 메시지 추가
        batchId = postBatchMng({
            "reqId"    : queryData['empId'],
            "status"   : "BAT-0001" , # 진행중
            "filePath" : os.path.join(uploads ,zipFileName),
            "content"  : "HM대사_불일치",
            "errMsg"   : ""
        })["data"]["batchId"]            
        fileName = 'HM대사_불일치_' + makeDate + '_' + str(fileCnt) +  '.xlsx'
        workbook = xlsxwriter.Workbook(os.path.join(uploads ,setUnicodeEncodeTypeToEucKr(fileName)))
        money_format = workbook.add_format()
        money_format.set_num_format('_- #,##0_-;[red]- #,##0_-;_- "-"_-;_-@_-')
        worksheet = workbook.add_worksheet()
        row = 0
        worksheet.write(row, 0  ,"거래처")
        worksheet.write(row, 1  ,"영업일자")
        worksheet.write(row, 2  ,"지불상태")
        worksheet.write(row, 3  ,"주문번호")
        worksheet.write(row, 4  ,"승인번호")
        worksheet.write(row, 5  ,"거래금액")
        worksheet.write(row, 6 ,"불일치내역")
        while True : 
            searchData = getData("/v1/settlement/hmStatistics/errorDetailAll" ,queryData,API_SERVER_BILLINGSERVICE)
            for data in searchData["resultList"]:
                row += 1
                worksheet.write(row, 0  ,data["jobDivider"])
                worksheet.write(row, 1  ,data["saleDt"])
                worksheet.write(row, 2  ,data["dealType"])
                worksheet.write(row, 3  ,data["dealNo"])
                worksheet.write(row, 4  ,data["approvalNo"])
                worksheet.write_number(row, 5  ,long(data["dealAmt"]), money_format)
                worksheet.write(row, 6 ,data["statusNm"])
                if row >= EXCEL_FILE_MAKE_LIMT_COUNT :
                    row = 0
                    fileCnt += 1
                    fileName = 'HM대사_불일치_'+ makeDate +'_' +  str(fileCnt) +  '.xlsx'
                    # 디비 조회건수 * 2 row 생성시 파일 재생성
                    workbook.close()
                    workbook = xlsxwriter.Workbook(os.path.join(uploads ,setUnicodeEncodeTypeToEucKr(fileName)))
                    money_format = workbook.add_format()
                    money_format.set_num_format('_- #,##0_-;[red]- #,##0_-;_- "-"_-;_-@_-')
                    worksheet = workbook.add_worksheet()
                    worksheet.write(row, 0  ,data["jobDivider"])
                    worksheet.write(row, 1  ,data["saleDt"])
                    worksheet.write(row, 2  ,data["dealType"])
                    worksheet.write(row, 3  ,data["dealNo"])
                    worksheet.write(row, 4  ,data["approvalNo"])
                    worksheet.write_number(row, 5  ,long(data["dealAmt"]), money_format)
                    worksheet.write(row, 6 ,data["statusNm"])                          
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

@settlementApi.route("/api/settlementApi/settlement/gsStatistics/inconsistencyInq", methods=['GET'])
def inconsistencyInq():
    
    form_data = json.loads(request.args.get("formData"))    
    searchDate = getParameter(form_data , "startDate").split(' - ')
    startDate = paramEscape(searchDate[0])
    endDate = paramEscape(searchDate[1])    
    queryData = {
        "jobDivider" : getParameter(form_data,"selType"),
        "startDate" : startDate, 
        "endDate" : endDate, 
        'dateType': getParameter(form_data,"dateType"),
        'dealType': paramEscape(getParameter(form_data,"dealType")),
        'dealDivider': paramEscape(getParameter(form_data,"dealDivider")),
        'orderNo': paramEscape(getParameter(form_data,"orderNo")),
        'limit': setStringToNumber(request.args.get("length")),
        'offset': setStringToNumber(request.args.get("start")),
        'isExcel': getParameter(form_data, "isExcel")
    }

    resultData = getApiData("/v1/settlement/gsStatistics/inconsistency", queryData , API_SERVER_BILLINGSERVICE)
    return json.dumps(resultData)

@settlementApi.route("/api/settlementApi/settlement/hmStatistics/inconsistencyInq", methods=['GET'])
def hmInconsistencyInq():
    form_data = json.loads(request.args.get("formData"))
    searchDate = getParameter(form_data , "startDate").split(' - ')
    startDate = paramEscape(searchDate[0])
    endDate = paramEscape(searchDate[1])    
    queryData = {
        "jobDivider" : getParameter(form_data,"selType"),
        "startDate" : startDate, 
        "endDate" : endDate, 
        'dateType': getParameter(form_data,"dateType"),
        'dealType': paramEscape(getParameter(form_data,"dealType")),
        'dealDivider': paramEscape(getParameter(form_data,"dealDivider")),
        'orderNo': paramEscape(getParameter(form_data,"orderNo")),
        'limit': setStringToNumber(request.args.get("length")),
        'offset': setStringToNumber(request.args.get("start")),
    }
    resultData = getApiData("/v1/settlement/hmStatistics/inconsistency", queryData , API_SERVER_BILLINGSERVICE)
    return json.dumps(resultData)

@settlementApi.route("/api/settlementApi/settlement/gsStatistics/errorExcel", methods=['GET'])
def errorExcel():
    form_data = {}
    searchDate = getParameter(form_data , "startDate").split(' - ')
    startDate = paramEscape(searchDate[0])
    endDate = paramEscape(searchDate[1])    
    queryData = {
        "jobDivider" : getParameter(form_data,"selType"),
        "startDate" : startDate, 
        "endDate" : endDate, 
        'dateType': getParameter(form_data,"dateType"),
        'dealType': paramEscape(getParameter(form_data,"dealType")),
        'dealDivider': paramEscape(getParameter(form_data,"dealDivider")),
        'orderNo': paramEscape(getParameter(form_data,"orderNo")),
        'offset': 0,
        'limit': EXCEL_FILE_DOWNLOAD_COUNT,         
        "empId" : session['empId'],
        "isExcel": "Y"
    }
    rootPath = current_app.root_path
    t1 = threading.Thread(target=makeSettlementErrorExcelDurationFile,args=[queryData,rootPath])
    t1.daemon = True
    t1.start()
    
    return "엑셀 작업요청"

@settlementApi.route("/api/settlementApi/settlement/hmStatistics/errorExcel", methods=['GET'])
def hmErrorExcel():
    form_data = {}
    searchDate = getParameter(form_data , "startDate").split(' - ')
    startDate = paramEscape(searchDate[0])
    endDate = paramEscape(searchDate[1])    
    queryData = {
        "jobDivider" : getParameter(form_data,"selType"),
        "startDate" : startDate, 
        "endDate" : endDate, 
        'dateType': getParameter(form_data,"dateType"),
        'dealType': paramEscape(getParameter(form_data,"dealType")),
        'dealDivider': paramEscape(getParameter(form_data,"dealDivider")),
        'orderNo': paramEscape(getParameter(form_data,"orderNo")),
        'offset': 0,
        'limit': EXCEL_FILE_DOWNLOAD_COUNT,         
        "empId" : session['empId']
    }
    rootPath = current_app.root_path
    t1 = threading.Thread(target=makeHmSettlementErrorExcelDurationFile,args=[queryData,rootPath])
    t1.daemon = True
    t1.start()
    
    return "엑셀 작업요청"


def makeSettlementErrorExcelDurationFile(queryData,rootPath):
    excelZip = None
    jobStatus = 0
    batchId = None 

    jobDivider = str(queryData.get('jobDivider'))
    if jobDivider is None :
        jobDivider = ""
        
    try:
        fileCnt = 1
        makeDate = datetime.datetime.now().strftime('%Y%m%d')
        makeTime = str(int(round(time.time()*1000)))
        uploads = os.path.join(rootPath, "fileDownload" , "excel" , makeTime)
        if not os.path.isdir(uploads):
            os.makedirs(uploads)
        zipFileName = u'GS대사_불일치('+jobDivider+u')_'+ makeDate +'.zip'
        #작업 시작 메시지 추가
        batchId = postBatchMng({
            "reqId"    : queryData['empId'],
            "status"   : "BAT-0001" , # 진행중
            "filePath" : os.path.join(uploads ,zipFileName),
            "content"  : "GS대사 불일치",
            "errMsg"   : ""
        })["data"]["batchId"]            
        fileName = 'GS대사_불일치('+jobDivider+')_' + makeDate + '_' + str(fileCnt) +  '.xlsx'
        workbook = xlsxwriter.Workbook(os.path.join(uploads ,setUnicodeEncodeTypeToEucKr(fileName)))
        worksheet = workbook.add_worksheet()
        money_format = workbook.add_format()
        money_format.set_num_format('_- #,##0_-;[red]- #,##0_-;_- "-"_-;_-@_-')
        row = 0
        worksheet.write(row, 0  ,"거래처")
        worksheet.write(row, 1  ,"영업일자")
        worksheet.write(row, 2  ,"점포코드")
        worksheet.write(row, 3  ,"점포명(사용처)")
        worksheet.write(row, 4  ,"지불상태")
        worksheet.write(row, 5  ,"상태")
        worksheet.write(row, 6  ,"주문번호")
        worksheet.write(row, 7  ,"승인번호")
        worksheet.write(row, 8  ,"승인일자")
        worksheet.write(row, 9  ,"승인시간")
        worksheet.write(row, 10  ,"거래금액")
        worksheet.write(row, 11 ,"카드번호")
        worksheet.write(row, 12 ,"불일치내역")
        worksheet.write(row, 13 ,"취소사유")
        while True : 
            searchData = getData("/v1/settlement/gsStatistics/inconsistency" ,queryData,API_SERVER_BILLINGSERVICE)
            print searchData
            for data in searchData["resultList"]:
                row += 1
                worksheet.write(row, 0  ,data["jobDivider"])
                worksheet.write(row, 1  ,data["saleDt"])
                worksheet.write(row, 2  ,data["storeCd"])
                worksheet.write(row, 3  ,data["storeNm"])
                worksheet.write(row, 4  ,data["dealType"])
                worksheet.write(row, 5  ,data["dealDivider"])
                worksheet.write(row, 6  ,data["dealNo"])
                worksheet.write(row, 7  ,data["approvalNo"])
                worksheet.write(row, 8  ,parseDate(data["approvalDt"] ,'%Y%m%d' ,'%Y-%m-%d'))

                if data["approvalTime"] is None:
                    worksheet.write(row, 9  ,"")
                else:
                    worksheet.write(row, 9  ,parseDate(data["approvalDt"] + " " + data["approvalTime"],'%Y%m%d %H%M%S' ,'%H:%M:%S'))
                                
                worksheet.write_number(row, 10  ,long(data["dealAmt"]), money_format)

                worksheet.write(row, 11 ,data["cardNo"])
                worksheet.write(row, 12 ,data["statusNm"])
                worksheet.write(row, 13 ,data["cancelMemo"])
                if row >= EXCEL_FILE_MAKE_LIMT_COUNT :
                    row = 0
                    fileCnt += 1
                    fileName = 'GS대사_불일치('+jobDivider+')_'+ makeDate + '_' + str(fileCnt) +  '.xlsx'
                    # 디비 조회건수 * 2 row 생성시 파일 재생성
                    workbook.close()
                    workbook = xlsxwriter.Workbook(os.path.join(uploads , setUnicodeEncodeTypeToEucKr(fileName)))
                    money_format = workbook.add_format()
                    money_format.set_num_format('_- #,##0_-;[red]- #,##0_-;_- "-"_-;_-@_-')
                    worksheet = workbook.add_worksheet()
                    worksheet.write(row, 0  ,data["jobDivider"])
                    worksheet.write(row, 1  ,data["saleDt"])
                    worksheet.write(row, 2  ,data["storeCd"])
                    worksheet.write(row, 3  ,data["storeNm"])
                    worksheet.write(row, 4  ,data["dealType"])
                    worksheet.write(row, 5  ,data["dealDivider"])
                    worksheet.write(row, 6  ,data["dealNo"])
                    worksheet.write(row, 7  ,data["approvalNo"])
                    worksheet.write(row, 8  ,parseDate(data["approvalDt"] ,'%Y%m%d' ,'%Y-%m-%d'))
                    
                    if data["approvalTime"] is None:
                        worksheet.write(row, 9  ,"")
                    else:
                        worksheet.write(row, 9  ,parseDate(data["approvalDt"] + " " + data["approvalTime"],'%Y%m%d %H%M%S' ,'%H:%M:%S'))
                                
                        worksheet.write_number(row, 10  ,long(data["dealAmt"]), money_format)
                    
                    worksheet.write(row, 11 ,data["cardNo"])
                    worksheet.write(row, 12 ,data["statusNm"])
                    worksheet.write(row, 13 ,data["cancelMemo"])                          
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
        print("Error on line {}".format(sys.exc_info()[-1].tb_lineno))
        print(err)
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


def makeHmSettlementErrorExcelDurationFile(queryData,rootPath):
    excelZip = None
    jobStatus = 0
    batchId = None
    try:
        fileCnt = 1
        makeDate = datetime.datetime.now().strftime('%Y%m%d')
        makeTime = str(int(round(time.time()*1000)))
        uploads = os.path.join(rootPath, "fileDownload" , "excel" , makeTime)
        if not os.path.isdir(uploads):
            os.makedirs(uploads)
        zipFileName = u'HM대사_불일치_'+ makeDate +'.zip'
        #작업 시작 메시지 추가
        batchId = postBatchMng({
            "reqId"    : queryData['empId'],
            "status"   : "BAT-0001" , # 진행중
            "filePath" : os.path.join(uploads ,zipFileName),
            "content"  : "HM대사_불일치",
            "errMsg"   : ""
        })["data"]["batchId"]            
        fileName = 'HM대사_불일치_' + makeDate + '_' +  str(fileCnt) +  '.xlsx'
        workbook = xlsxwriter.Workbook(os.path.join(uploads ,setUnicodeEncodeTypeToEucKr(fileName)))
        money_format = workbook.add_format()
        money_format.set_num_format('_- #,##0_-;[red]- #,##0_-;_- "-"_-;_-@_-')
        worksheet = workbook.add_worksheet()
        row = 0
        worksheet.write(row, 0  ,"거래처")
        worksheet.write(row, 1  ,"영업일자")
        worksheet.write(row, 2  ,"지불상태")
        worksheet.write(row, 3  ,"주문번호")
        worksheet.write(row, 4  ,"승인번호")
        worksheet.write(row, 5  ,"거래금액")
        worksheet.write(row, 6 ,"불일치내역")
        while True : 
            searchData = getData("/v1/settlement/hmStatistics/inconsistency" ,queryData,API_SERVER_BILLINGSERVICE)
            print searchData
            for data in searchData["resultList"]:
                row += 1
                worksheet.write(row, 0  ,data["jobDivider"])
                worksheet.write(row, 1  ,data["saleDt"])
                worksheet.write(row, 2  ,data["dealType"])
                worksheet.write(row, 3  ,data["dealNo"])
                worksheet.write(row, 4  ,data["approvalNo"])
                worksheet.write_number(row, 5  ,long(data["dealAmt"]), money_format)
                worksheet.write(row, 6 ,data["statusNm"])
                if row >= EXCEL_FILE_MAKE_LIMT_COUNT :
                    row = 0
                    fileCnt += 1
                    fileName = 'HM대사_불일치_' + makeDate + '_' +  str(fileCnt) +  '.xlsx'
                    # 디비 조회건수 * 2 row 생성시 파일 재생성
                    workbook.close()
                    workbook = xlsxwriter.Workbook(os.path.join(uploads ,setUnicodeEncodeTypeToEucKr(fileName)))
                    money_format = workbook.add_format()
                    money_format.set_num_format('_- #,##0_-;[red]- #,##0_-;_- "-"_-;_-@_-')
                    worksheet = workbook.add_worksheet()
                    worksheet.write(row, 0  ,data["jobDivider"])
                    worksheet.write(row, 1  ,data["saleDt"])
                    worksheet.write(row, 2  ,data["dealType"])
                    worksheet.write(row, 3  ,data["dealNo"])
                    worksheet.write(row, 4  ,data["approvalNo"])
                    worksheet.write_number(row, 5  ,long(data["dealAmt"]), money_format)
                    worksheet.write(row, 6 ,data["statusNm"])                          
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
        print("Error on line {}".format(sys.exc_info()[-1].tb_lineno))
        print(err)
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
