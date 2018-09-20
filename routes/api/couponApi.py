# -*- coding:utf-8 -*-
'''
Created on 2017. 4. 21.

@author: sanghyun
'''
from datetime import datetime 
import json
from mhlib import isnumeric
import os
import sys
import threading
import time
import zipfile

from flask import Blueprint, request
from flask.globals import session, current_app
import xlsxwriter

from routes.api.systemMngApi import postBatchMng, putBatchMng, \
    postCommonSystemHistory
from util.common import paramEscape, getApiData, postApiData, getApiSingleData, \
    strToLong, deleteApiDataByJson, getParameter, getData, putData, \
    API_SERVER_KPC_PAYMENT, setStringToNumber, postData, deleteData, parseDate, \
    EXCEL_FILE_MAKE_LIMT_COUNT, EXCEL_FILE_DOWNLOAD_COUNT, API_SERVER_KCON, \
    kconID, kconPW, setUnicodeEncodeTypeToEucKr, setUnicodeFormatToEucKr
from util.common import putApiData, deleteApiData, setNoneToBlank, \
    request_get, request_post, request_put, API_SERVER_BACKOFFICE
from exceptions import Exception

couponApi = Blueprint("couponApi", __name__)

@couponApi.route("/api/coupon/charge/couponChargeMng", methods=['GET', "PUT"])
def couponChargeMng():
    if (request.method == 'GET') :
        return getCouponChargeMng() 
    elif (request.method == 'PUT') :
        return putCouponChargeMng()
    
def getCouponChargeMng():
    queryData = {
        'couponType': '100', #100: 충전권 , 200 : 교환권
        'couponNo'  : getParameter({}, "couponNo"),
    }
    returnData = {
        "detailData" : {},
        "listData" : {}
    }
    result_data = getData("/admin/v1/coupon" ,queryData , API_SERVER_KPC_PAYMENT)
    returnData["detailData"] = result_data
    if result_data["code"] == "K000" and setNoneToBlank(result_data["useDate"]) != "":
        useDate = datetime.fromtimestamp(result_data["useDate"] / 1e3)
        queryData["startDate"] = useDate.strftime('%Y%m%d')
        queryData["endDate"] = useDate.strftime('%Y%m%d')
        queryData["limit"] = 10
        queryData["offset"] = 0
        result_data2 = getApiData("/admin/v1/coupon/usages" ,queryData , API_SERVER_KPC_PAYMENT)
        if "data" in result_data2 and len(result_data2["data"]) > 0:
            returnData["listData"] = result_data2["data"][0]
    return json.dumps(returnData)

def putCouponChargeMng():
    form_data = request.json
    postCouponData = {
        "actionType"   : "300", #String, //동작타입 - 100:사용제한 , 200: 사용제한 , 300: 사용기간 연장
        "couponNo"     : getParameter(form_data,"couponNo") #String, //부서 ID
    }

    return json.dumps(putData("/admin/v1/coupon", {}, postCouponData , API_SERVER_KPC_PAYMENT))    

@couponApi.route("/api/coupon/charge/couponChargeMng/useLimit", methods=['PUT'])
def couponUseLimit():
    form_data = request.json
    postCouponData = {
        "actionType"   : "100", #String, //동작타입 - 100:사용제한 , 200: 사용제한 해제 , 300: 사용기간 연장
        "couponNo"     : getParameter(form_data,"couponNo") #String, //부서 ID
    }

    return json.dumps(putData("/admin/v1/coupon", {}, postCouponData , API_SERVER_KPC_PAYMENT))
    
@couponApi.route("/api/coupon/charge/couponChargeMng/useLimitCancel", methods=['PUT'])
def couponUseLimitCancel():
    form_data = request.json
    postCouponData = {
        "actionType"   : "200", #String, //동작타입 - 100:사용제한 , 200: 사용제한 해제 , 300: 사용기간 연장
        "couponNo"     : getParameter(form_data,"couponNo") #String, //부서 ID
    }

    return json.dumps(putData("/admin/v1/coupon", {}, postCouponData , API_SERVER_KPC_PAYMENT))    

@couponApi.route("/api/coupon/charge/couponCharges", methods=['GET'])
def couponCharges():
    formData = json.loads(request.args.get("formData"))
    searchDate = getParameter(formData , "startDate").split(' - ')
    startDate = searchDate[0]
    endDate = searchDate[1]
    queryData = {
        'limit'     : setStringToNumber(getParameter({},"length")),
        'offset'    : setStringToNumber(getParameter({},"start")),        
        'startDate' : paramEscape(startDate),        
        'endDate'   : paramEscape(endDate),        
        'status'    : getParameter(formData,"status"),        
        'couponNo'  : getParameter(formData,"couponNo"),        
        'orderNo'   : getParameter(formData,"orderNo"),        
    }
    result_data = getApiData("/admin/v1/coupon/usages" , queryData , API_SERVER_KPC_PAYMENT)
    return json.dumps(result_data)
    
@couponApi.route("/api/coupon/brochures/brochure", methods=['POST'])
def couponBrochure():
    form_data = request.json
    postCouponData = {
        "title"          : getParameter(form_data,"title"),
        "typeDetail"     : getParameter(form_data,"typeDetail"),
        "typeCode"       : getParameter(form_data,"type"),
        "amount"         : paramEscape(getParameter(form_data,"amount")),
        "expireDays"     : paramEscape(getParameter(form_data,"expireDays")),
        "expireDaysType" : getParameter(form_data,"expireDaysType"),
        "seller"         : "STOC-0001",
        "usage"          : getParameter(form_data,"usage"),
        "couponLength"   : "16",
        "status"         : "01",
        "reqEmpId"       : session['empId'],         
        "apprEmpId"      : getParameter(form_data,"apprEmpId")
    }
    
    response = request_post("/approvals/request/kcon/brochure", postCouponData, '1')
    return json.dumps(response);

@couponApi.route("/api/coupon/brochures/brochure", methods=['PUT'])
def putCouponBrochure():
    form_data = request.json
    getCouponData = {
        'merchantId'  : kconID, 
        'merchantPw'  : kconPW,           
        "productId"   : getParameter(form_data,"productId"),
        "register"    : session['empId'],
    }
    brochureData = getData("/kcons/brochures/brochure",  getCouponData , API_SERVER_KCON)
    postCouponData = {
        "productId"      : brochureData["productId"],
        "title"          : getParameter(form_data,"title"),
        "typeDetail"     : brochureData["typeDetail"],
        "typeCode"       : brochureData["type"],
        "amount"         : brochureData["amount"],
        "expireDays"     : strToLong(paramEscape(getParameter(form_data,"expireDays"))),
        "expireDaysType" : getParameter(form_data,"expireDaysType"),
        "seller"         : "STOC-0001",
        "usage"          : brochureData["usage"],
        "couponLength"   : "16",
        "status"         : "01",
        "reqEmpId"       : session['empId'],         
        "reqMemo"        : getParameter(form_data,"reqMemo"),
        "apprEmpId"      : getParameter(form_data,"apprEmpId"),
    } 
    # TODO : 이지점에 PUSH 추가
    reponseResult = request_put("/approvals/request/kcon/brochure", postCouponData, '1')
    return json.dumps(reponseResult)


@couponApi.route("/api/coupon/brochures/brochure/delete", methods=['DELETE'])
def deleteCouponBrochure():
    form_data = request.json
    couponData = {
        "productId"   : getParameter(form_data,"productId"),
        "reqEmpId"       : session['empId'],
        "apprEmpId"      : getParameter(form_data,"apprEmpId"),
        "reqMemo"        : getParameter(form_data,"reqMemo"),
    }
    reponseResult = request_put("/approvals/request/kcon/brochure/delete", couponData, '1')

    return json.dumps(reponseResult) 

@couponApi.route("/api/coupon/brochures/brochure/publishStop", methods=['PUT'])
def publishStop():
    
    getCouponData = {
        'merchantId'  : kconID, 
        'merchantPw'  : kconPW,           
        "productId"   : getParameter(request.json,"id"),
        "register"    :  session['empId'],
    }
    brochureData = getData("/kcons/brochures/brochure",  getCouponData , API_SERVER_KCON)
    postCouponData = {
        'merchantId'     : kconID, 
        'merchantPw'     : kconPW,
        "productId"      : brochureData["productId"],
        "title"          : brochureData["title"],
        "typeDetail"     : brochureData["typeDetail"],
        "typeCode"       : brochureData["type"],
        "amount"         : brochureData["amount"],
        "expireDays"     : brochureData["expireDays"],
        "expireDaysType" : brochureData["expireDaysType"],
        "seller"         : "STOC-0001",
        "usage"          : brochureData["usage"],
        "couponLength"   : "16",
        "status"         : brochureData["status"],
        "register"       : session['empId'],         
        "apprEmpId"      : getParameter(request.json,"apprEmpId"),
        "menuId"         : getParameter(request.json,"menuId"),  
    } 
    # TODO : 이지점에 PUSH 추가
    return json.dumps(postData("/approval/kcon/publishStop", postCouponData,{}))

@couponApi.route("/api/coupon/brochures/brochure", methods=['GET'])
def getCouponBrochure():
    postCouponData = {
        'merchantId'  : kconID, 
        'merchantPw'  : kconPW,           
        "productId"   : getParameter({},"id"),
        "register"    :  session['empId'],
    }
    return json.dumps(getData("/kcons/brochures/brochure",  postCouponData , API_SERVER_KCON))

@couponApi.route("/api/coupon/brochures", methods=['GET'])
def getCouponBrochures():
    formData = json.loads(request.args.get("formData"))
    searchDate = getParameter(formData , "startDate").split(' - ')
    startDate = searchDate[0]
    endDate = searchDate[1]
    queryData = {
        'merchantId'  : kconID, 
        'merchantPw'  : kconPW,        
        'limit'       : setStringToNumber(getParameter({},"length")),
        'offset'      : setStringToNumber(getParameter({},"start")),        
        'productId'   : getParameter(formData,"productId"),        
        'title'       : getParameter(formData,"name"),        
        'type'        : getParameter(formData,"type"),        
        'typeDetail'  : getParameter(formData,"typeDetail"),        
        'amount'      : setStringToNumber(paramEscape(getParameter(formData,"amount"))),        
        'status'      : getParameter(formData,"status"),        
        'startDate'   : paramEscape(startDate),        
        'endDate'     : paramEscape(endDate),        
        "register"    : getParameter(formData,"registrator"),
    }
    result_data = getApiData("/kcons/brochures" , queryData , API_SERVER_KCON)
    return json.dumps(result_data)    


@couponApi.route('/api/coupon/brochures/excelAll', methods=['GET'])
def brochurespaymentsExcelAll():
    formData = {}
    searchDate = getParameter(formData , "startDate").split(' - ')
    startDate = searchDate[0]
    endDate = searchDate[1]    
    queryData = {
        'limit'       : EXCEL_FILE_DOWNLOAD_COUNT,
        'offset'      : 0,        
        'merchantId'  : kconID, 
        'merchantPw'  : kconPW,        
        'productId'   : getParameter(formData,"id"),        
        'title'       : getParameter(formData,"name"),        
        'type'        : getParameter(formData,"type"),        
        'typeDetail'  : getParameter(formData,"typeDetail"),        
        'amount'      : setStringToNumber(paramEscape(getParameter(formData,"amount"))),        
        'status'      : getParameter(formData,"status"),        
        'startDate'   : paramEscape(startDate),        
        'endDate'     : paramEscape(endDate),        
        "register"    : getParameter(formData,"registrator"),
        'empId'       : session['empId']
    }
    print queryData
    rootPath = current_app.root_path
    t1 = threading.Thread(target=makeBrochuresExcelFile,args=[queryData,rootPath])
    t1.daemon = True
    t1.start()
    
    return "엑셀 작업요청"


def makeBrochuresExcelFile(queryData,rootPath):
    excelZip = None
    jobStatus = 0
    batchId = None
    try:
        fileCnt = 1
        makeTime = str(int(round(time.time()*1000)))
        uploads = os.path.join(rootPath, "fileDownload" , "excel" , makeTime)
        if not os.path.isdir(uploads):
            os.makedirs(uploads)
        zipFileName = u'KCON_쿠폰등록상품_'+ datetime.now().strftime('%Y%m%d') +'.zip'
        #작업 시작 메시지 추가
        batchId = postBatchMng({
            "reqId"    : queryData['empId'],
            "status"   : "BAT-0001" , # 진행중
            "filePath" : os.path.join(uploads ,zipFileName),
            "content"  : "KCON 상품 등록 조회",
            "errMsg"   : ""
        })["data"]["batchId"]            
        fileName = 'KCON_쿠폰등록상품_' + datetime.now().strftime('%Y%m%d') + '_' + str(fileCnt) +  '.xlsx'
        workbook = xlsxwriter.Workbook(os.path.join(uploads ,setUnicodeEncodeTypeToEucKr(fileName)))
        worksheet = workbook.add_worksheet()
        money_format = workbook.add_format()
        money_format.set_num_format('_- #,##0_-;[red]- #,##0_-;_- "-"_-;_-@_-')
        
        row = 0
        worksheet.write(row, 0  ,"상품ID")
        worksheet.write(row, 1  ,"상품상태")
        worksheet.write(row, 2  ,"폐기여부")
        worksheet.write(row, 3  ,"상품유형")
        worksheet.write(row, 4  ,"상품유형상세")
        worksheet.write(row, 5  ,"권종")
        worksheet.write(row, 6  ,"상품명")
        worksheet.write(row, 7  ,"유효기간")
        worksheet.write(row, 8  ,"등록자")
        worksheet.write(row, 9  ,"등록일")
        while True : 
            searchData = getData("/kcons/brochures" ,queryData, API_SERVER_KCON)
            for data in searchData["list"]:
                row += 1
                worksheet.write(row, 0  ,data["productId"])
                worksheet.write(row, 1  ,data["statusName"])
                worksheet.write(row, 2  ,data["delFlag"])
                worksheet.write(row, 3  ,data["typeName"])
                worksheet.write(row, 4  ,data["typeDetailName"])
                worksheet.write_number(row, 5  ,long(data["amount"]), money_format)
                worksheet.write(row, 6  ,data["title"])
                expireDaysType = data["expireDaysType"];
                expireDaysTypeName = "";
                if expireDaysType =='DATE-0001' :
                    expireDaysTypeName = '발행일로부터 ' + str(data["expireDays"]) + ' 일'  
                elif expireDaysType =='DATE-0002' :
                    expireDaysTypeName = '발행일로부터 ' + str(data["expireDays"]) + ' 개월'                                                
                else :
                    expireDaysTypeName = '발행일로부터 ' + str(data["expireDays"]) + ' 년'                                                
                worksheet.write(row, 7  ,expireDaysTypeName)
                worksheet.write(row, 8  ,data["register"])
                worksheet.write(row, 9  ,data["createDate"])
                if row >= EXCEL_FILE_MAKE_LIMT_COUNT :
                    row = 0
                    fileCnt += 1
                    fileName = 'KCON_쿠폰등록상품_' + datetime.now().strftime('%Y%m%d') + '_' + str(fileCnt) +  '.xlsx'
                    # 디비 조회건수 * 2 row 생성시 파일 재생성
                    workbook.close()
                    workbook = xlsxwriter.Workbook(os.path.join(uploads ,setUnicodeEncodeTypeToEucKr(fileName)))
                    worksheet = workbook.add_worksheet()
                    worksheet.write(row, 0  ,"상품ID")
                    worksheet.write(row, 1  ,"상품상태")
                    worksheet.write(row, 2  ,"폐기여부")
                    worksheet.write(row, 3  ,"상품유형")
                    worksheet.write(row, 4  ,"상품유형상세")
                    worksheet.write(row, 5  ,"권종")
                    worksheet.write(row, 6  ,"상품명")
                    worksheet.write(row, 7  ,"유효기간")
                    worksheet.write(row, 8  ,"등록자")
                    worksheet.write(row, 9  ,"등록일")                             
            queryData["offset"] = queryData["offset"] + EXCEL_FILE_DOWNLOAD_COUNT 
            if len(searchData["list"]) < EXCEL_FILE_DOWNLOAD_COUNT : 
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
        
@couponApi.route("/api/coupon/kcon/detail", methods=['GET'])
def kconDetail():
    formData = json.loads(request.args.get("formData"))
    target = getParameter(formData, "target")
    queryData = {
        'merchantId': kconID, 
        'merchantPw': kconPW,
        'couponNo': target == "1" and getParameter(formData, "couponNo") or "", # 쿠폰번호
        'orderNo': target == "2" and getParameter(formData, "couponNo") or "", # 주문번호
        'limit': setStringToNumber(getParameter({},"length")),
        'offset': setStringToNumber(getParameter({},"start")),        
    }
    result_data = getApiData("/kcons/infos" , queryData ,API_SERVER_KCON)
    return json.dumps(result_data)

@couponApi.route("/api/coupon/kcon/kconPublishInq", methods=['GET'])
def kconPublishInq():
    formData = json.loads(request.args.get("formData"))
    searchDate = getParameter(formData , "startDate").split(' - ')
    startDate = paramEscape(searchDate[0])
    endDate = paramEscape(searchDate[1])
    orderNoType = paramEscape(getParameter(formData, "orderNoType"))
    orderNo = orderNoType == "1" and getParameter(formData, "orderNo") or "" #거래번호
    approvalNo = orderNoType == "2" and paramEscape(getParameter(formData, "orderNo")) or "" #승인번호
    queryData = {
        'merchantId'    : kconID, 
        'merchantPw'    : kconPW,
        'dateType'      : getParameter(formData, "dateType"),
        'startDate'     : startDate,
        'endDate'       : endDate,
        'limit'         : setStringToNumber(getParameter({},"length")),
        'offset'        : setStringToNumber(getParameter({},"start")),
        'prodType'      : getParameter(formData, "prodType"),
        'couponType'    : getParameter(formData, "couponType"),
        'orderNo'       : orderNo,
        'approvalNo'    : approvalNo,
        'restrictFlag'  : getParameter(formData, "restrictFlag"),
        'useFlag'       : getParameter(formData, "useFlag"),
        'couponNo'      : paramEscape(getParameter(formData, "couponNo")),
        'title'         : getParameter(formData, "title"),
        'amount'        : setStringToNumber(paramEscape(getParameter(formData, "amount"))),
    }
    result_data = getApiData("/kcons/approval" , queryData ,API_SERVER_KCON)
    
    prodTypeCode = []
    couponTypeCode = []
    for commCode in session['commCodeList'] :
        if commCode["typeCode"] == "PRTY" :
            prodTypeCode.append(commCode)
        if commCode["typeCode"] == "CPT" :
            couponTypeCode.append(commCode)
    for data in result_data["data"] :
        for prodType in prodTypeCode:
            if data["prodType"] == prodType["code"] :
                data["prodTypeNm"] = prodType["descText"]
        for couponType in couponTypeCode:
            if data["couponType"] == couponType["code"] :
                data["couponTypeNm"] = couponType["descText"]
    return json.dumps(result_data)
        
@couponApi.route("/api/coupon/kcon/kconPublishInq/excelAll", methods=['GET'])
def kconPublishInqExcelAll():
    formData = {}
    searchDate = getParameter(formData , "startDate").split(' - ')
    startDate = paramEscape(searchDate[0])
    endDate = paramEscape(searchDate[1])
    orderNoType = paramEscape(getParameter(formData, "orderNoType"))
    orderNo = orderNoType == "1" and paramEscape(getParameter(formData, "orderNo")) or "" #거래번호
    approvalNo = orderNoType == "2" and paramEscape(getParameter(formData, "orderNo")) or "" #승인번호
    queryData = {
        'limit'       : EXCEL_FILE_DOWNLOAD_COUNT,
        'offset'      : 0,        
        'merchantId'    : kconID, 
        'merchantPw'    : kconPW,
        'dateType'      : getParameter(formData, "dateType"),
        'startDate'     : startDate,
        'endDate'       : endDate,
        'prodType'      : getParameter(formData, "prodType"),
        'couponType'    : getParameter(formData, "couponType"),
        'orderNo'       : orderNo,
        'approvalNo'    : approvalNo,
        'restrictFlag'  : getParameter(formData, "restrictFlag"),
        'useFlag'       : getParameter(formData, "useFlag"),
        'couponNo'      : paramEscape(getParameter(formData, "couponNo")),
        'title'         : getParameter(formData, "title"),
        'amount'        : setStringToNumber(paramEscape(getParameter(formData, "amount"))),
        'empId'       : session['empId']
    }
    rootPath = current_app.root_path
    t1 = threading.Thread(target=kconPublishInqExcelFile,args=[queryData,rootPath,session['commCodeList']])
    t1.daemon = True
    t1.start()
    
    return "엑셀 작업요청"

def kconPublishInqExcelFile(queryData,rootPath,commCodeList):
    excelZip = None
    jobStatus = 0
    batchId = None
    try:
        fileCnt = 1
        makeTime = str(int(round(time.time()*1000)))
        uploads = os.path.join(rootPath, "fileDownload" , "excel" , makeTime)
        if not os.path.isdir(uploads):
            os.makedirs(uploads)
        zipFileName = u'KCON_발행내역_'+ datetime.now().strftime('%Y%m%d') +'.zip'
        prodTypeCode = []
        couponTypeCode = []
        for commCode in commCodeList :
            if commCode["typeCode"] == "PRTY" :
                prodTypeCode.append(commCode)
            if commCode["typeCode"] == "CPT" :
                couponTypeCode.append(commCode)
        #작업 시작 메시지 추가
        batchId = postBatchMng({
            "reqId"    : queryData['empId'],
            "status"   : "BAT-0001" , # 진행중
            "filePath" : os.path.join(uploads ,zipFileName),
            "content"  : "KCON발행 엑셀 배치작업",
            "errMsg"   : ""
        })["data"]["batchId"]            
        fileName = 'KCON_발행내역_' + datetime.now().strftime('%Y%m%d') + '_' + str(fileCnt) +  '.xlsx'
        workbook = xlsxwriter.Workbook(os.path.join(uploads ,setUnicodeEncodeTypeToEucKr(fileName)))
        worksheet = workbook.add_worksheet()
        money_format = workbook.add_format()
        money_format.set_num_format('_- #,##0_-;[red]- #,##0_-;_- "-"_-;_-@_-')
        row = 0
        worksheet.write(row, 0  ,"쿠폰번호")
        worksheet.write(row, 1  ,"사용여부")
        worksheet.write(row, 2  ,"쿠폰유형")
        worksheet.write(row, 3  ,"쿠폰구분")
        worksheet.write(row, 4  ,"KCON 쿠폰명")
        worksheet.write(row, 5  ,"POP 쿠폰명")
        worksheet.write(row, 6  ,"발행일")
        worksheet.write(row, 7  ,"사용일")
        worksheet.write(row, 8  ,"사용시간")
        worksheet.write(row, 9  ,"거래번호")
        worksheet.write(row, 10 , "승인번호")
        worksheet.write(row,11 , "유효기간")
        worksheet.write(row,12 , "권종")
        worksheet.write(row,13 , "카드번호")
        worksheet.write(row,14 , "사용제한")
        worksheet.write(row,15 , "상품ID")
        worksheet.write(row,16 , "판매처")
        worksheet.write(row,17 , "연동ID")       

        while True : 
            searchData = getData("/kcons/approval" , queryData ,API_SERVER_KCON)
            for data in searchData["list"]:
                row += 1
                useDate = data["useDate"]
                issueDate = data["issueDate"]
                expireDate = data["expireDate"]
                useDateTime = ""
                prodTypeNm = data["prodType"] # 코드명이 없다면 코드로 대체
                couponTypeNm = data["couponType"] # 코드명이 없다면 코드로 대체
                if useDate != None :
                    useDate = datetime.fromtimestamp(data["useDate"] / 1e3)
                    useDateTime = useDate.strftime('%H:%M:%S')
                    useDate = useDate.strftime('%Y-%m-%d')
                if issueDate != None :
                    issueDate = datetime.fromtimestamp(data["issueDate"] / 1e3)
                    issueDate = issueDate.strftime('%Y-%m-%d')
                if expireDate != None :
                    expireDate = datetime.fromtimestamp(data["expireDate"] / 1e3)
                    expireDate = expireDate.strftime('%Y-%m-%d')
                for prodType in prodTypeCode:
                    if prodTypeNm == prodType["code"] :
                        prodTypeNm = prodType["descText"]
                for couponType in couponTypeCode:
                    if couponTypeNm == couponType["code"] :
                        couponTypeNm = couponType["descText"]                       
                    
                worksheet.write(row, 0  ,data["couponNo"])
                worksheet.write(row, 1  ,data["useFlag"])
                worksheet.write(row, 2  ,prodTypeNm)
                worksheet.write(row, 3  ,couponTypeNm)                
                worksheet.write(row, 4  ,data["title"])
                worksheet.write(row, 5  ,data["popCouponName"])
                worksheet.write(row, 6  ,issueDate)
                worksheet.write(row, 7  ,useDate)
                worksheet.write(row, 8  ,useDateTime)
                worksheet.write(row, 9  ,data["orderNo"])
                worksheet.write(row, 10  ,data["approvalNo"])
                worksheet.write(row,11  ,expireDate)
                worksheet.write_number(row, 12  ,long(data["amount"]), money_format)
                worksheet.write(row,13  ,data["cardNumber"])
                worksheet.write(row,14  ,data["restrictFlag"])
                worksheet.write(row,15  ,"")
                worksheet.write(row,16  ,"")
                worksheet.write(row,17  ,data["seller"])
                if row >= EXCEL_FILE_MAKE_LIMT_COUNT :
                    row = 0
                    fileCnt += 1
                    fileName = 'KCON_발행내역_' + datetime.now().strftime('%Y%m%d') + '_' + str(fileCnt) +  '.xlsx'
                    # 디비 조회건수 * 2 row 생성시 파일 재생성
                    workbook.close()
                    workbook = xlsxwriter.Workbook(os.path.join(uploads ,setUnicodeEncodeTypeToEucKr(fileName)))
                    worksheet = workbook.add_worksheet()
                    worksheet.write(row, 0  ,"쿠폰번호")
                    worksheet.write(row, 1  ,"사용여부")
                    worksheet.write(row, 2  ,"쿠폰유형")
                    worksheet.write(row, 3  ,"쿠폰구분")
                    worksheet.write(row, 4  ,"KCON 쿠폰명")
                    worksheet.write(row, 5  ,"POP 쿠폰명")
                    worksheet.write(row, 6  ,"발행일")
                    worksheet.write(row, 7  ,"사용일")
                    worksheet.write(row, 8  ,"사용시간")
                    worksheet.write(row, 9  ,"거래번호")
                    worksheet.write(row, 10 , "승인번호")
                    worksheet.write(row,11 , "유효기간")
                    worksheet.write(row,12 , "권종")
                    worksheet.write(row,13 , "카드번호")
                    worksheet.write(row,14 , "사용제한")
                    worksheet.write(row,15 , "상품ID")
                    worksheet.write(row,16 , "판매처")
                    worksheet.write(row,17 , "연동ID")        
            queryData["offset"] = queryData["offset"] + EXCEL_FILE_DOWNLOAD_COUNT 
            if len(searchData["list"]) < EXCEL_FILE_DOWNLOAD_COUNT : 
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
        

#KOCN 사용내역 조회 리스트 요청
@couponApi.route("/api/coupon/kcon/balance-list",  methods=['GET'])
def kconBalanceList():
    formData = json.loads(request.args.get("formData"))
    searchDate = getParameter(formData , "startDate").split(' - ')
    startDate = paramEscape(searchDate[0])
    endDate = paramEscape(searchDate[1])
    queryData = {
        'startDate'     : startDate,
        'endDate'       : endDate,
        'limit'         : setStringToNumber(getParameter({},"length")),
        'offset'        : setStringToNumber(getParameter({},"start")),
        'dateOption'    : getParameter(formData, "dateOption"),
        'couponType'    : getParameter(formData, "couponType"),
        'couponDealType': getParameter(formData, "couponDealType"),
        'title'         : getParameter(formData, "title"),
        'encryptKey'    : 'plain'
    }
    result_data = getApiData("/kcon/balance-list" , queryData ,API_SERVER_KCON)
    return json.dumps(result_data) 

#KOCN 사용내역 엑셀 다운로드 요청            
@couponApi.route("/api/coupon/kcon/balance-list/excelAll", methods=['GET'])
def kconBalanceMngExcelAll():
    formData = {}
    searchDate = getParameter(formData , "startDate").split(' - ')
    startDate = paramEscape(searchDate[0])
    endDate = paramEscape(searchDate[1])
    queryData = {
        'limit'         : EXCEL_FILE_DOWNLOAD_COUNT,
        'offset'        : 0,        
        'startDate'     : startDate,
        'endDate'       : endDate,
        'dateOption'    : getParameter(formData, "dateOption"),
        'couponType'    : getParameter(formData, "couponType"),
        'couponDealType': getParameter(formData, "couponDealType"),
        'title'         : getParameter(formData, "title"),
        'empId'         : session['empId']
    }
    
    rootPath = current_app.root_path
    t1 = threading.Thread(target=kconBalanceMngExcelFile,args=[queryData,rootPath])
    t1.daemon = True
    t1.start()
    return "엑셀 작업요청"

#KOCN 사용내역 엑셀 다운로드 처리    
def kconBalanceMngExcelFile(queryData,rootPath):
    excelZip = None
    jobStatus = 0
    batchId = None
    try:
        fileCnt = 1
        makeTime = str(int(round(time.time()*1000)))
        uploads = os.path.join(rootPath, "fileDownload" , "excel" , makeTime)
        if not os.path.isdir(uploads):
            os.makedirs(uploads)
        zipFileName = u'KCON_사용내역_'+ datetime.now().strftime('%Y%m%d') +'.zip'
        #작업 시작 메시지 추가
        batchId = postBatchMng({
            "reqId"    : queryData['empId'],
            "status"   : "BAT-0001" , # 진행중
            "filePath" : os.path.join(uploads ,zipFileName),
            "content"  : "KCON사용내역 엑셀 배치작업",
            "errMsg"   : ""
        })["data"]["batchId"]
        
        fileName = 'KCON_사용내역_조회(' +  queryData['startDate'] + '~' + queryData['endDate'] + ').xlsx'
        workbook = xlsxwriter.Workbook(os.path.join(uploads ,setUnicodeEncodeTypeToEucKr(fileName)))
        worksheet = workbook.add_worksheet()
        money_format = workbook.add_format()
        money_format.set_num_format('#,##0')
        
        title_format = workbook.add_format({'align':'center', 'valign':'vcenter', 'bold':True, 'border':1,'fg_color':'#A9D0F5'})
        string_format = workbook.add_format({'align':'center', 'valign':'vcenter'})
        summary_money_format = workbook.add_format({'fg_color' : '#E5E5E5'});
        summary_money_format.set_num_format('#,##0')
        
        row = 0
        worksheet.write(row, 0  ,"번호", title_format)
        worksheet.write(row, 1  ,"쿠폰명", title_format)
        worksheet.write(row, 2  ,"쿠폰번호", title_format)
        worksheet.write(row, 3  ,"쿠폰유형", title_format)
        worksheet.write(row, 4  ,"쿠폰구분", title_format)
        worksheet.write(row, 5  ,"권종금액", title_format)
        worksheet.write(row, 6  ,"발행일", title_format)
        worksheet.write(row, 7  ,"유효기간", title_format)
        worksheet.write(row, 8  ,"만료여부", title_format)
        worksheet.write(row, 9  ,"발행수량", title_format)
        worksheet.write(row, 10  ,"발행금액", title_format)
        worksheet.write(row, 11 , "이전 사용 수량", title_format)
        worksheet.write(row, 12 , "이전 사용 금액", title_format)
        worksheet.write(row, 13 , "사용 수량", title_format)
        worksheet.write(row, 14 , "사용 금액", title_format)
        worksheet.write(row, 15 , "미사용 수량", title_format)
        worksheet.write(row, 16 , "미사용 금액", title_format)

        while True : 
            searchData = getApiData("/kcon/balance-list" , queryData ,API_SERVER_KCON)
            
            summaryData = searchData["totalData"]
            for data in searchData["data"]:
                row += 1
                
                issueType = data["issueType"];
                if data["issueType"] == "PRTY-0001":
                    issueType = "충전쿠폰"
                elif data["issueType"] == "PRTY-0002":
                    issueType ="충전쿠폰"
                    
                couponDtlType = data["couponDtlType"];
                if data["couponDtlType"] == "CPC-001":
                    couponDtlType = "원쿠폰"
                elif data["couponDtlType"] == "CPC-002":
                    couponDtlType ="충전권"
                elif data["couponDtlType"] == "CPT-001":
                    couponDtlType ="구글교환권"
                    
                expireFlag = data["expireFlag"];
                if data["expireFlag"] == "N":
                    expireFlag = "-"
                elif data["expireFlag"] == "Y":
                    expireFlag ="만료"
                    
                worksheet.write(row, 0  ,row, string_format)    
                worksheet.write(row, 1  ,data["title"], string_format)
                worksheet.write(row, 2  ,data["masterNo"], string_format)
                worksheet.write(row, 3  ,issueType, string_format)
                worksheet.write(row, 4  ,couponDtlType, string_format)        
                worksheet.write(row, 5  ,data["amt"], money_format)
                worksheet.write(row, 6  ,parseDate(data["issueDt"] ,'%Y-%m-%d %H:%M:%S.0','%Y-%m-%d'), string_format)        
                worksheet.write(row, 7  ,parseDate(data["expireDt"] ,'%Y-%m-%d %H:%M:%S.0','%Y-%m-%d'), string_format)
                worksheet.write(row, 8  ,expireFlag, string_format)
                worksheet.write(row, 9  ,data["issueCnt"], money_format)
                worksheet.write(row, 10  ,data["issueAmt"], money_format)
                worksheet.write(row, 11  ,data["beforeCnt"], money_format)
                worksheet.write(row, 12 ,data["beforeAmt"], money_format)
                worksheet.write(row, 13 ,data["useCnt"], money_format)
                worksheet.write(row, 14 ,data["useAmt"], money_format)
                worksheet.write(row, 15 ,data["unusedCnt"], money_format)
                worksheet.write(row, 16 ,data["unusedAmt"], money_format)
                
                
                if row >= EXCEL_FILE_MAKE_LIMT_COUNT :
                    row = 0
                    fileCnt += 1
                    fileName = 'KCON_사용내역_조회(' +  queryData['startDate'] + '~' + queryData['endDate'] + ').xlsx'
                    # 디비 조회건수 * 2 row 생성시 파일 재생성
                    workbook.close()
                    workbook = xlsxwriter.Workbook(os.path.join(uploads ,setUnicodeEncodeTypeToEucKr(fileName)))
                    worksheet = workbook.add_worksheet()
                    worksheet.write(row, 0  ,"번호", title_format)
                    worksheet.write(row, 1  ,"쿠폰명", title_format )
                    worksheet.write(row, 2  ,"쿠폰번호", title_format)
                    worksheet.write(row, 3  ,"쿠폰유형", title_format)
                    worksheet.write(row, 4  ,"쿠폰구분", title_format)
                    worksheet.write(row, 5  ,"권종금액", title_format)
                    worksheet.write(row, 6  ,"발행일", title_format)
                    worksheet.write(row, 7  ,"유효기간", title_format)
                    worksheet.write(row, 8  ,"만료여부", title_format)
                    worksheet.write(row, 9  ,"발행수량", title_format)
                    worksheet.write(row, 10  ,"발행금액", title_format)
                    worksheet.write(row, 11 , "이전 사용 수량", title_format)
                    worksheet.write(row, 12 , "이전 사용 금액", title_format)
                    worksheet.write(row, 13 , "사용 수량", title_format)
                    worksheet.write(row, 14 , "사용 금액", title_format)
                    worksheet.write(row, 15 , "미사용 수량", title_format)
                    worksheet.write(row, 16 , "미사용 금액",title_format)
                    
                    
            row += 1
                    
            worksheet.write(row, 0  ,"", summary_money_format)    
            worksheet.write(row, 1  ,"", summary_money_format)
            worksheet.write(row, 2  ,"", summary_money_format)
            worksheet.write(row, 3  ,"", summary_money_format)
            worksheet.write(row, 4  ,"", summary_money_format)        
            worksheet.write(row, 5  ,"", summary_money_format)
            worksheet.write(row, 6  ,"", summary_money_format)        
            worksheet.write(row, 7  ,"", summary_money_format)
            worksheet.write(row, 8  ,"", summary_money_format)
            worksheet.write(row, 9  ,summaryData["issueCnt"], summary_money_format)
            worksheet.write(row, 10  ,summaryData["issueAmt"], summary_money_format)
            worksheet.write(row, 11  ,summaryData["beforeCnt"], summary_money_format)
            worksheet.write(row, 12 ,summaryData["beforeAmt"], summary_money_format)
            worksheet.write(row, 13 ,summaryData["useCnt"], summary_money_format)
            worksheet.write(row, 14 ,summaryData["useAmt"], summary_money_format)
            worksheet.write(row, 15 ,summaryData["unusedCnt"], summary_money_format)
            worksheet.write(row, 16 ,summaryData["unusedAmt"], summary_money_format)
                
                
            if row >= EXCEL_FILE_MAKE_LIMT_COUNT :
                row = 0
                fileCnt += 1
                fileName = 'KCON_사용내역_조회(' +  queryData['startDate'] + '~' + queryData['endDate'] + ').xlsx'
                # 디비 조회건수 * 2 row 생성시 파일 재생성
                workbook.close()
                workbook = xlsxwriter.Workbook(os.path.join(uploads ,setUnicodeEncodeTypeToEucKr(fileName)))
                worksheet = workbook.add_worksheet()
                worksheet.write(row, 0  ,"번호", title_format)
                worksheet.write(row, 1  ,"쿠폰명", title_format )
                worksheet.write(row, 2  ,"쿠폰번호", title_format)
                worksheet.write(row, 3  ,"쿠폰유형", title_format)
                worksheet.write(row, 4  ,"쿠폰구분", title_format)
                worksheet.write(row, 5  ,"권종금액", title_format)
                worksheet.write(row, 6  ,"발행일", title_format)
                worksheet.write(row, 7  ,"유효기간", title_format)
                worksheet.write(row, 8  ,"만료여부", title_format)
                worksheet.write(row, 9  ,"발행수량", title_format)
                worksheet.write(row, 10  ,"발행금액", title_format)
                worksheet.write(row, 11 , "이전 사용 수량", title_format)
                worksheet.write(row, 12 , "이전 사용 금액", title_format)
                worksheet.write(row, 13 , "사용 수량", title_format)
                worksheet.write(row, 14 , "사용 금액", title_format)
                worksheet.write(row, 15 , "미사용 수량", title_format)
                worksheet.write(row, 16 , "미사용 금액",title_format)
                    
    
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
        


#KOCN 기간별 잔액관리 리스트 요청
@couponApi.route("/api/coupon/kcon/balancedaily-list",  methods=['GET'])
def kconBalanceDailyList():
    formData = json.loads(request.args.get("formData"))
    searchDate = getParameter(formData , "startDate").split(' - ')
    startDate = paramEscape(searchDate[0])
    endDate = paramEscape(searchDate[1])
    queryData = {
        'startDate'     : startDate,
        'endDate'       : endDate,
        'limit'         : setStringToNumber(getParameter({},"length")),
        'offset'        : setStringToNumber(getParameter({},"start")),
        'couponType'    : getParameter(formData, "couponType"),
        'couponDealType': getParameter(formData, "couponDealType"), 
        'orderBy'       : getParameter(formData, "orderBy"),
        'title'         : getParameter(formData, "title"),
        'encryptKey'    : 'plain'
    }
    result_data = getApiData("/kcon/balancedaily-list" , queryData ,API_SERVER_KCON)
    return json.dumps(result_data) 

#KOCN 기간별 잔액관리 엑셀 다운로드 요청            
@couponApi.route("/api/coupon/kcon/balancedaily-list/excelAll", methods=['GET'])
def kconBalanceDailyMngExcelAll():
    formData = {}
    searchDate = getParameter(formData , "startDate").split(' - ')
    startDate = paramEscape(searchDate[0])
    endDate = paramEscape(searchDate[1])
    queryData = {
        'limit'         : EXCEL_FILE_DOWNLOAD_COUNT,
        'offset'        : 0,        
        'startDate'     : startDate,
        'endDate'       : endDate,
        'couponType'    : getParameter(formData, "couponType"),
        'couponDealType': getParameter(formData, "couponDealType"),
        'orderBy'       : getParameter(formData, "orderBy"),
        'title'         : getParameter(formData, "title"),
        'empId'         : session['empId']
    }
    
    rootPath = current_app.root_path
    t1 = threading.Thread(target=kconBalanceDailyMngExcelFile,args=[queryData,rootPath])
    t1.daemon = True
    t1.start()
    return "엑셀 작업요청"

 #KOCN 기간별 잔액관리 엑셀 다운로드 처리    
def kconBalanceDailyMngExcelFile(queryData,rootPath):
    excelZip = None
    jobStatus = 0
    batchId = None
    try:
        fileCnt = 1
        makeTime = str(int(round(time.time()*1000)))
        uploads = os.path.join(rootPath, "fileDownload" , "excel" , makeTime)
        if not os.path.isdir(uploads):
            os.makedirs(uploads)
        zipFileName = u'KCON_기간별 잔액 리스트_'+ datetime.now().strftime('%Y%m%d') +'.zip'
        #작업 시작 메시지 추가
        batchId = postBatchMng({
            "reqId"    : queryData['empId'],
            "status"   : "BAT-0001" , # 진행중
            "filePath" : os.path.join(uploads ,zipFileName),
            "content"  : "KCON기간별 잔액 리스트 엑셀 배치작업",
            "errMsg"   : ""
        })["data"]["batchId"]
                    
        fileName = 'KCON_기간별_잔액관리(' +  queryData['startDate'] + '~' + queryData['endDate'] + ').xlsx'
        workbook = xlsxwriter.Workbook(os.path.join(uploads ,setUnicodeEncodeTypeToEucKr(fileName)))
        worksheet = workbook.add_worksheet()
        money_format = workbook.add_format()
        money_format.set_num_format('#,##0')
        
        title_format = workbook.add_format({'align':'center', 'valign':'vcenter', 'bold':True, 'border':1,'fg_color':'#A9D0F5'})
        string_format = workbook.add_format({'align':'center', 'valign':'vcenter'})
        summary_money_format = workbook.add_format({'fg_color' : '#E5E5E5'});
        summary_money_format.set_num_format('#,##0')
        
        row = 0
        worksheet.write(row, 0  ,"번호", title_format)
        worksheet.write(row, 1  ,"일자", title_format)
        worksheet.write(row, 2  ,"이월 미사용 수량", title_format)
        worksheet.write(row, 3  ,"이월 미사용 금액", title_format)
        worksheet.write(row, 4  ,"발행 수량", title_format)
        worksheet.write(row, 5  ,"발행 금액", title_format)
        worksheet.write(row, 6  ,"사용 수량", title_format)
        worksheet.write(row, 7  ,"사용 금액", title_format)
        worksheet.write(row, 8  ,"미사용 수량", title_format)
        worksheet.write(row, 9  ,"미사용 금액", title_format)
        while True : 
            searchData = getApiData("/kcon/balancedaily-list" , queryData ,API_SERVER_KCON)

            summaryData = searchData["totalData"]
            for data in searchData["data"]:
                row += 1
                 
                worksheet.write(row, 0  ,row, string_format)    
                worksheet.write(row, 1  ,parseDate(data["balanceDt"] ,'%Y%m%d','%Y-%m-%d'), string_format)
                worksheet.write(row, 2  ,data["beforeCnt"], money_format)        
                worksheet.write(row, 3  ,data["beforeAmt"], money_format)     
                worksheet.write(row, 4  ,data["issueCnt"], money_format)
                worksheet.write(row, 5  ,data["issueAmt"], money_format)   
                worksheet.write(row, 6  ,data["useCnt"], money_format)
                worksheet.write(row, 7  ,data["useAmt"], money_format)
                worksheet.write(row, 8  ,data["unusedCnt"],money_format)
                worksheet.write(row, 9  ,data["unusedAmt"], money_format)
                
                if row >= EXCEL_FILE_MAKE_LIMT_COUNT :
                    row = 0
                    fileCnt += 1
                    fileName = 'KCON_기간별_잔액관리(' +  queryData['startDate'] + '~' + queryData['endDate'] + ').xlsx'
                    # 디비 조회건수 * 2 row 생성시 파일 재생성
                    workbook.close()
                    workbook = xlsxwriter.Workbook(os.path.join(uploads ,setUnicodeEncodeTypeToEucKr(fileName)))
                    worksheet = workbook.add_worksheet()
                    worksheet.write(row, 0  ,"번호", title_format)
                    worksheet.write(row, 1  ,"일자", title_format)
                    worksheet.write(row, 2  ,"이월 미사용 수량", title_format)
                    worksheet.write(row, 3  ,"이월 미사용 금액", title_format)
                    worksheet.write(row, 4  ,"발행 수량", title_format)
                    worksheet.write(row, 5  ,"발행 금액", title_format)
                    worksheet.write(row, 6  ,"사용 수량", title_format)
                    worksheet.write(row, 7  ,"사용 금액", title_format)
                    worksheet.write(row, 8  ,"미사용 수량", title_format)
                    worksheet.write(row, 9  ,"미사용 금액", title_format)
                    
                    
            row += 1
                 
            worksheet.write(row, 0  ,"", summary_money_format)    
            worksheet.write(row, 1  ,"", summary_money_format)
            worksheet.write(row, 2  ,summaryData["beforeCnt"], summary_money_format)        
            worksheet.write(row, 3  ,summaryData["beforeAmt"], summary_money_format)     
            worksheet.write(row, 4  ,summaryData["issueCnt"], summary_money_format)
            worksheet.write(row, 5  ,summaryData["issueAmt"], summary_money_format)   
            worksheet.write(row, 6  ,summaryData["useCnt"], summary_money_format)
            worksheet.write(row, 7  ,summaryData["useAmt"], summary_money_format)
            worksheet.write(row, 8  ,summaryData["unusedCnt"],summary_money_format)
            worksheet.write(row, 9  ,summaryData["unusedAmt"], summary_money_format)
                
            if row >= EXCEL_FILE_MAKE_LIMT_COUNT :
                row = 0
                fileCnt += 1
                fileName = 'KCON_기간별_잔액관리(' +  queryData['startDate'] + '~' + queryData['endDate'] + ').xlsx'
                # 디비 조회건수 * 2 row 생성시 파일 재생성
                workbook.close()
                workbook = xlsxwriter.Workbook(os.path.join(uploads ,setUnicodeEncodeTypeToEucKr(fileName)))
                worksheet = workbook.add_worksheet()
                worksheet.write(row, 0  ,"번호", title_format)
                worksheet.write(row, 1  ,"일자", title_format)
                worksheet.write(row, 2  ,"이월 미사용 수량", title_format)
                worksheet.write(row, 3  ,"이월 미사용 금액", title_format)
                worksheet.write(row, 4  ,"발행 수량", title_format)
                worksheet.write(row, 5  ,"발행 금액", title_format)
                worksheet.write(row, 6  ,"사용 수량", title_format)
                worksheet.write(row, 7  ,"사용 금액", title_format)
                worksheet.write(row, 8  ,"미사용 수량", title_format)
                worksheet.write(row, 9  ,"미사용 금액", title_format)
            
    
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
        
@couponApi.route("/api/coupon/charge/extendDate", methods=['POST'])
def chargeCouponextendDate():
    formData = request.json
    queryData = {
        "couponNo" : getParameter(formData, "couponNo"),
        "endDate" : paramEscape(getParameter(formData, "endDate")),
        "reqEmpId"  : session['empId'],
        "reqMemo" : getParameter(formData, "reqMemo"),
        "apprEmpId" : getParameter(formData, "apprEmpId")
    }
    reponseResult = request_put("/approvals/request/coupon/charge/extension", queryData, '1')

    return json.dumps(reponseResult) 
        
@couponApi.route("/api/coupon/kcon/extendDate", methods=['POST'])
def extendDate():
    formData = request.json
    queryData = {
        "couponNo" : getParameter(formData, "couponNo"),
        "endDate" : paramEscape(getParameter(formData, "endDate")),
        "reqEmpId"  : session['empId'],
        "reqMemo" : getParameter(formData, "reqMemo"),
        "apprEmpId" : getParameter(formData, "apprEmpId")
    }
    
    reponseResult = request_put("/approvals/request/kcon/coupon/extension", queryData, '1')

    return json.dumps(reponseResult) 
    
#     result_data = postData("/kcons/extend-date" , queryData , queryData ,API_SERVER_KCON)
#     if result_data["code"] == "K000" :
#         for couponNo in result_data["couponNo"]:
#             data = {
#                 'menuId'  : "CPN-1003",
#                 'typeCode': "CUPS-0001",
#                 'desc1': couponNo,
#                 'desc2': paramEscape(getParameter(formData, "endDate")),
#                 'desc3': getParameter(formData, "desc"),
#             }
#             postCommonSystemHistory(data)
#    return json.dumps(result_data)        
        
@couponApi.route("/api/coupon/kcon/restrict", methods=['POST'])
def restrict():
    formData = request.json
    restrict = paramEscape(getParameter(formData, "restrict"))
    queryData = {
        'merchantId': kconID, 
        'merchantPw': kconPW,
        "couponList" : getParameter(formData, "couponList"),
        "restrict" : restrict,
    }
    result_data = postData("/kcons/restrict" , queryData , queryData ,API_SERVER_KCON)
    if result_data["code"] == "K000" :
        for couponNo in result_data["couponNoList"]:
            data = {
                'menuId'  : "CPN-1003",
                'typeCode':  restrict == "Y" and "CUPS-0002" or "CUPS-0003",
                'desc1': couponNo,
                'desc2': "",
                'desc3': getParameter(formData, "desc"),
            }
            postCommonSystemHistory(data)
    return json.dumps(result_data)

@couponApi.route("/api/coupon/kcon/un-restrict", methods=['POST'])
def unRestrict():
    formData = request.json
    queryData = {
        "couponNo" : getParameter(formData, "couponNo"),
        "reqEmpId"  : session['empId'],
        "reqMemo" : getParameter(formData, "reqMemo"),
        "apprEmpId" : getParameter(formData, "apprEmpId")
    }
    
    reponseResult = request_put("/approvals/request/kcon/coupon/un-restriction", queryData, '1')
    
    return json.dumps(reponseResult)

@couponApi.route("/api/coupon/charge/un-restrict", methods=['POST'])
def unRestrictChargeCoupon():
    formData = request.json
    queryData = {
        "couponNo" : getParameter(formData, "couponNo"),
        "reqEmpId"  : session['empId'],
        "reqMemo" : getParameter(formData, "reqMemo"),
        "apprEmpId" : getParameter(formData, "apprEmpId")
    }
    
    reponseResult = request_put("/approvals/request/coupon/charge/un-restriction", queryData, '1')
    
    return json.dumps(reponseResult)