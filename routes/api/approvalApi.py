# -- coding:utf-8 --
'''
Created on 2017. 3. 13.

@author: sanghyun
'''
from datetime import datetime, timedelta
import json
import os
import threading
import time
import zipfile
import sys

from flask import Blueprint, request
from flask.globals import session, current_app
import xlsxwriter

from routes.api.systemMngApi import postBatchMng, putBatchMng

from util.common import  paramEscape, getApiData, getParameter, getData, \
    postData, setStringToLong, kconID, kconPW, API_SERVER_KCON, putData, postApiData, \
    parseDate, deleteData, strToLong, EXCEL_FILE_DOWNLOAD_COUNT, EXCEL_FILE_MAKE_LIMT_COUNT, setUnicodeEncodeTypeToEucKr, setUnicodeFormatToEucKr, \
    getEnv, sendSms, request_get, request_get_for_datatables, request_post, request_put, API_SERVER_BACKOFFICE



approvalApi = Blueprint('approvalApi', __name__)

@approvalApi.route('/api/approval/getApprovers', methods=['GET'])
def payments():
    queryData = {
        'menuId': getParameter({}, "menuId"),
        'loginEmpId' : session['empId']
    }
    print queryData
    result_data = getData("/approvals/approvers" ,queryData)
    return json.dumps(result_data)

@approvalApi.route('/api/approval/kcon/approvals', methods=['GET'])
def getKconApprovals():
    formData = json.loads(request.args.get("formData"))
    searchDate = getParameter(formData , "startDate").split(' - ')
    startDate = paramEscape(searchDate[0])
    endDate = paramEscape(searchDate[1])
    queryData = {
        'title'      : getParameter(formData, "title"),
        'typeCode'   : getParameter(formData, "type"),
        'typeDetail' : getParameter(formData, "typeDetail"),
        'reqEmpName' : getParameter(formData, "reqEmpName"),
        'status'     : getParameter(formData, "status"),
        'startDate'  : startDate,
        'endDate'    : endDate,
        'empId'      : session['empId'],
        'offset'     : strToLong(request.args.get("start")),
        'limit'      : strToLong(request.args.get("length")),
    }
    result_data = getApiData("/approval/kcon/approvals" ,queryData)
    return json.dumps(result_data)

@approvalApi.route('/api/approval/kcon/approvals/history', methods=['GET'])
def getKconApprovalsHistory():
    formData = json.loads(request.args.get("formData"))
    searchDate = getParameter(formData , "startDate").split(' - ')
    startDate = paramEscape(searchDate[0])
    endDate = paramEscape(searchDate[1])
    queryData = {
        'title'      : getParameter(formData, "title"),
        'typeCode'   : getParameter(formData, "type"),
        'typeDetail' : getParameter(formData, "typeDetail"),
        'reqEmpName' : getParameter(formData, "reqEmpName"),
        'status'     : getParameter(formData, "status"),
        'startDate'  : startDate,
        'endDate'    : endDate,
        'historyType': getParameter(formData, "historyType"),
        'empId'      : session['empId'],
        'offset'     : strToLong(request.args.get("start")),
        'limit'      : strToLong(request.args.get("length")),
    }
    result_data = getApiData("/approval/kcon/approvals/history" ,queryData)
    return json.dumps(result_data)

@approvalApi.route('/api/approval/kcon/approvals/kconTmp', methods=['GET'])
def getKconApprovalTmp():
    queryData = {
        'tmpSeq' : getParameter({}, "tmpSeq"),
        'empId'  : session['empId'],
    }
    result_data = getData("/approval/kcon/approvals/kconTmp" ,queryData, {})
    return json.dumps(result_data)

def kconApproval(formData):
    queryData = {
        'seq'    : setStringToLong(paramEscape(getParameter(formData, "seq"))),
        'tmpSeq' : setStringToLong(paramEscape(getParameter(formData, "tmpSeq"))),
        'empId'  : session['empId'],
    }
    postData("/approval/approval" ,queryData, {})
    resultGetData = getData("/approval/kcon/approvals/kconTmp" ,queryData, {})
    apprTypeCode = resultGetData["apprTypeCode"]
    if apprTypeCode == "APPR-0501" and resultGetData["productId"] != None :
        putCouponData = {
            'merchantId'     : kconID, 
            'merchantPw'     : kconPW,        
            "productId"      : resultGetData["productId"],
            "title"          : resultGetData["title"],
            "expireDays"     : resultGetData["expireDays"],
            "expireDaysType" : resultGetData["expireDaysType"],
            "registrator"    : resultGetData["register"],
        }
        # TODO : 이지점에 PUSH 추가
        return putData("/kcons/brochures/brochure", {}, putCouponData , API_SERVER_KCON)
    elif (apprTypeCode == "APPR-0502" or apprTypeCode == "APPR-0503") and resultGetData["productId"] != None :
        putCouponData = {
            'merchantId'     : kconID, 
            'merchantPw'     : kconPW,        
            "productId"      : resultGetData["productId"]
        }
        # TODO : 이지점에 PUSH 추가
        return putData("/kcons/brochure/restrict", {}, putCouponData , API_SERVER_KCON)
    elif apprTypeCode == "APPR-0504" and resultGetData["productId"] != None :
        deleteCouponData = {
            'merchantId'     : kconID, 
            'merchantPw'     : kconPW,        
            "productId"      : resultGetData["productId"]
        }
        # TODO : 이지점에 PUSH 추가
        return deleteData("/kcons/brochures/brochure", {}, deleteCouponData , API_SERVER_KCON)    
    else :
        postCouponData = {
            'merchantId'     : kconID, 
            'merchantPw'     : kconPW,
            "title"          : resultGetData["title"],
            "typeDetail"     : resultGetData["typeDetail"],
            "type"           : resultGetData["typeCode"],
            "amount"         : resultGetData["amount"],
            "expireDays"     : resultGetData["expireDays"],
            "expireDaysType" : resultGetData["expireDaysType"],
            "seller"         : "STOC-0001",
            "usage"          : resultGetData["usage"],
            "couponLength"   : 16,
            "status"         : "01",
            "register"       : resultGetData["register"],         
        } 
        # TODO : 이지점에 PUSH 추가
        return postData("/kcons/brochures/brochure", {}, postCouponData , API_SERVER_KCON)    

@approvalApi.route('/api/approval/kcon/approvals/approval', methods=['POST'])
def postKconApproval():
    formData = request.json
    return json.dumps(kconApproval(formData))
    
@approvalApi.route('/api/approval/kcon/approvals/approvalArray', methods=['POST'])
def approvalArray():
    formData = request.json
    resultFlag = True
    for data in formData:
        resultData = kconApproval(data)
        print resultData
        if resultData["code"] != "K000" :
            resultFlag = False
    if resultFlag:
        return json.dumps({"code" : "K000"})
    else :
        return json.dumps({"code" : "K001" , "message" : "승인 처리중 오류가 발생하였습니다.\n관리자에게 문의 바랍니다."})

@approvalApi.route('/api/approval/reject', methods=['POST'])
def postReject():
    return json.dumps(approvalReject(request.json))

@approvalApi.route('/api/approval/kcon/approvals/rejectArray', methods=['POST'])
def kconRejectArray():
    formData = request.json
    for data in formData:
        resultData = approvalReject(data)
        print(resultData)
        if resultData["status"] != "200" :
            resultFlag = False
    if resultFlag:
        return json.dumps({"code" : "K000"})
    else :
        return json.dumps({"code" : "K001" , "message" : "반려 처리중 오류가 발생하였습니다.\n관리자에게 문의 바랍니다."})
    
   

@approvalApi.route("/api/approval/kcon/approvals/reject/reApproval", methods=['POST'])
def postKconRejectReApproval():
    formData = request.json
    postCouponData = {
        'merchantId'     : kconID, 
        'merchantPw'     : kconPW,
        "productId"      : getParameter(formData,"productId"),
        "title"          : getParameter(formData,"title"),
        "typeDetail"     : getParameter(formData,"typeDetail"),
        "typeCode"       : getParameter(formData,"typeCode"),
        "amount"         : paramEscape(getParameter(formData,"amount")),
        "expireDays"     : paramEscape(getParameter(formData,"expireDays")),
        "expireDaysType" : getParameter(formData,"expireDaysType"),
        "seller"         : "STOC-0001",
        "usage"          : getParameter(formData,"usage"),
        "couponLength"   : "16",
        "status"         : "01",
        "register"       : session['empId'],         
        "apprEmpId"      : getParameter(formData,"apprEmpId"),
        "menuId"         : getParameter(formData,"menuId"),
        "tmpSeq"         : getParameter(formData,"tmpSeq"),
        "seq"            : getParameter(formData,"seq"),
    }
    # TODO : 이지점에 PUSH 추가
    return json.dumps(postData("/approval/kcon/approvals/reject/reApproval", postCouponData,{}))

@approvalApi.route('/api/approvals/answer/noti-list', methods=['GET'])
def readApprovalAnswerNotiList():
    queryData = {
        'loginEmpId'        : session['empId'],
        'offset'       : strToLong(request.args.get("start")),
        'limit'        : strToLong(request.args.get("length"))
    }
    return json.dumps(request_get_for_datatables("/approvals/answer/noti-list", queryData, API_SERVER_BACKOFFICE))

@approvalApi.route('/api/approvals/<menuUrl>', methods=['GET'])
def readApprovalRequestList(menuUrl):
    
    if menuUrl == "request" or menuUrl == "answer":
        formData = json.loads(request.args.get("formData"))
        
        reqType = getParameter(formData, "reqType").replace(" ", "");
        
        searchDate = getParameter(formData , "searchDate").split(' - ')
        startDate = paramEscape(searchDate[0])
        endDate = paramEscape(searchDate[1])
        queryData = {
            'workType' : getParameter(formData, "workType"),
            'keyword' : getParameter(formData, "keyword"),
            'status'       : getParameter(formData, "status"),
            'reqType' : reqType,
            'reqEmpName'   : getParameter(formData, "reqEmpName"),
            'apprEmpName'   : getParameter(formData, "apprEmpName"),
            'searchDateType'       : getParameter(formData, "searchDateType"),
            'startDate'    : startDate,
            'endDate'      : endDate,
            'loginEmpId'        : session['empId'],
            'searchDateOrderType'       : getParameter(formData, "searchDateOrderType"),
            'orderType'       : getParameter(formData, "orderType"),
            'offset'       : strToLong(request.args.get("start")),
            'limit'        : strToLong(request.args.get("length"))
        }
        return json.dumps(request_get_for_datatables("/approvals/"+menuUrl ,queryData, API_SERVER_BACKOFFICE))
    else:
        noneData = {
            'recordsFiltered' : 0, # 페이징 처리용 total
            'recordsTotal' : 0, # 페이징 처리용 total
            'data' : {},
            'totalData' : {'summary' : { 'count' : 0 }}
        }
        return json.dumps(noneData);

@approvalApi.route('/api/approvals/detail/<int:seq>', methods=['GET'])
def getApprovalMerchantDetail(seq):

    resultData = request_get("/approvals/detail/"+str(seq), None, API_SERVER_BACKOFFICE)
    return json.dumps(resultData)

@approvalApi.route('/api/approval/Info/<int:seq>', methods=['GET'])
def getApprovalInfo(seq):
    
    requestData = {
        "seq" : seq
    }

    responseData = request_get("/approval/request/approvalInfo", requestData, API_SERVER_BACKOFFICE)   
    
    return json.dumps(responseData)

    
def merchantApproval(formData):
    queryData = {
        'seq'    : setStringToLong(paramEscape(getParameter(formData, "seq"))),
        'tmpSeq' : setStringToLong(paramEscape(getParameter(formData, "tmpSeq"))),
        'empId'  : session['empId'],
    }
    result = postData("/approval/approval" ,queryData, {})

    return result
    
def rejectApprovalList(formData):
    # TODO : 이지점에 PUSH 추가
    return request_post("/approvals/response/rejection", formData, API_SERVER_BACKOFFICE)



def approvalReject(formData):
    # TODO : 이지점에 PUSH 추가
#     return postData("/approvals/reject" ,formData, {})
    return request_post("/approvals/reject", formData, API_SERVER_BACKOFFICE)

@approvalApi.route('/api/approval/merchant/approvals/approval', methods=['POST'])
def postMerchantApproval():
    formData = request.json
    return json.dumps(merchantApproval(formData))

@approvalApi.route("/api/approval/merchant/approvals/reject/reApproval", methods=['POST'])
def postMerchantRejectReApproval():
    formData = request.json
    postRepresentData = {
        "name"           : getParameter(formData,"name"),                   
        "alias"          : getParameter(formData,"alias"),                  
        "ceoNm"          : getParameter(formData,"ceoNm"),                
        "openDt"         : paramEscape(getParameter(formData,"openDt")),  
        "bizRegNo"       : paramEscape(getParameter(formData,"bizRegNo")),  
        "corpRegNo"      : paramEscape(getParameter(formData,"corpRegNo")), 
        "bizKind"        : getParameter(formData,"bizKind"),                
        "bizCond"        : getParameter(formData,"bizCond"),                
        "bizGrp"         : getParameter(formData,"bizGrp"),                 
        "useFlag"        : getParameter(formData,"useFlag"),                
        "zipcode"        : getParameter(formData,"zipcode"),       
        "address"        : getParameter(formData,"address"),       
        "addressDtl"     : getParameter(formData,"addressDtl"), 
        "tel"            : paramEscape(getParameter(formData,"tel")),       
        "fax"            : paramEscape(getParameter(formData,"fax")),        
        "createDesc"     : "신규등록",                                
        "reqEmpId"       : session['empId'],
        "apprEmpId"      : getParameter(formData,"apprEmpId"),
        "tmpSeq"         : getParameter(formData,"tmpSeq"),
        "seq"            : getParameter(formData,"seq"),        
    }
    # TODO : 이지점에 PUSH 추가
    return json.dumps(postData("/approval/merchant/approvals/reject/reApproval", postRepresentData,{}))

@approvalApi.route('/api/approval/submerchant/approvals/submerchantTmp', methods=['GET'])
def getSubMerchantApprovalTmp():
    queryData = {
        'tmpSeq' : getParameter({}, "tmpSeq"),
        'empId'  : session['empId'],
    }
    result_data = getData("/approval/submerchant/approvals/submerchantTmp" ,queryData, {})
    return json.dumps(result_data)

def submerchantApproval(formData):
    queryData = {
        'seq'    : setStringToLong(paramEscape(getParameter(formData, "seq"))),
        'tmpSeq' : setStringToLong(paramEscape(getParameter(formData, "tmpSeq"))),
        'empId'  : session['empId'],
    }
    postData("/approval/approval" ,queryData, {})
    resultGetData = getData("/approval/submerchant/approvals/submerchantTmp" ,queryData, {})
    apprTypeCode = resultGetData["apprTypeCode"]
    if apprTypeCode == "APPR-0201" and resultGetData["submerchantId"] != None :
        putMerchantData = {
            "submerchantId" : getParameter(resultGetData,"submerchantId"),   
            "parentId"      : getParameter(resultGetData,"parentId"),   
            "name"          : getParameter(resultGetData,"name"),   
            "alias"         : getParameter(resultGetData,"alias"),    
            "ceoName"       : getParameter(resultGetData,"ceoNm"),    
            "openDate"      : paramEscape(getParameter(resultGetData,"openDt")) ,    
            "bizRegNo"      : paramEscape(getParameter(resultGetData,"bizRegNo")),    
            "corpRegNo"     : paramEscape(getParameter(resultGetData,"corpRegNo")),    
            "bizKind"       : getParameter(resultGetData,"bizKind"),    
            "bizCond"       : getParameter(resultGetData,"bizCond"),    
            "zipcode"       : getParameter(resultGetData,"zipcode"),    
            "address"       : getParameter(resultGetData,"address"),    
            "addressDetail" : getParameter(resultGetData,"addressDtl"),    
            "bizGrp"        : getParameter(resultGetData,"typeCode"),    
            "tel"           : paramEscape(getParameter(resultGetData,"tel")),    
            "fax"           : paramEscape(getParameter(resultGetData,"fax")),    
            "taxCustName"   : getParameter(resultGetData,"taxCustNm"),    
            "taxTel"        : paramEscape(getParameter(resultGetData,"taxTel")),    
            "taxFax"        : paramEscape(getParameter(resultGetData,"taxFax")),    
            "taxPhone"      : paramEscape(getParameter(resultGetData,"taxPhone")),    
            "taxEmail"      : getParameter(resultGetData,"taxEmail"),    
            "bankNm"        : getParameter(resultGetData,"bankNm"),    
            "bankAccNo"     : getParameter(resultGetData,"bankAccNo"),    
            "bankHolder"    : getParameter(resultGetData,"bankHolder"),    
            "salesNm"       : getParameter(resultGetData,"salesNm"),    
            "salesTel"      : getParameter(resultGetData,"salesTel"),    
            "billingNm"     : getParameter(resultGetData,"billingNm"),    
            "billingTel"    : getParameter(resultGetData,"billingTel"),    
            "kpcSalesNm"    : getParameter(resultGetData,"kpcSalesNm"),    
            "kpcSalesTel"   : getParameter(resultGetData,"kpcSalesTel"),    
            "kpcBillingNm"  : getParameter(resultGetData,"kpcBillingNm"),    
            "kpcBillingTel" : getParameter(resultGetData,"kpcBillingTel"),    
            "agentId"       : getParameter(resultGetData,"agentId"),    
            "agentPw"       : getParameter(resultGetData,"agentPw"),    
            "useFlag"       : getParameter(resultGetData,"useFlag") ,    
            "urlHome"       : getParameter(resultGetData,"urlHome") ,  
            "reqEmpId"      : getParameter(resultGetData,"reqEmpId"),
            "apprEmpId"     : session['empId'],             
            "encAgentPw"    : getParameter(resultGetData,"agentPw"),    
        }
        # TODO : 이지점에 PUSH 추가
        return putData("/merchants/merchant", putMerchantData , {})
    elif apprTypeCode == "APPR-0202" and resultGetData["submerchantId"] != None :
        deleteSubMerchantData = {
            "merchantId"      : resultGetData["submerchantId"]
        }
        print "submerchantId : " + resultGetData["submerchantId"]
        # TODO : 이지점에 PUSH 추가
        return deleteData("/merchants/merchant", {}, deleteSubMerchantData)
    else :
        postMerchantData = {                                         
            "parentId"      : getParameter(resultGetData,"parentId"),   
            "name"          : getParameter(resultGetData,"name"),   
            "alias"         : getParameter(resultGetData,"alias"),    
            "ceoName"       : getParameter(resultGetData,"ceoNm"),    
            "openDate"      : paramEscape(getParameter(resultGetData,"openDt")) ,    
            "bizRegNo"      : paramEscape(getParameter(resultGetData,"bizRegNo")),    
            "corpRegNo"     : paramEscape(getParameter(resultGetData,"corpRegNo")),    
            "bizKind"       : getParameter(resultGetData,"bizKind"),    
            "bizCond"       : getParameter(resultGetData,"bizCond"),    
            "zipcode"       : getParameter(resultGetData,"zipcode"),    
            "address"       : getParameter(resultGetData,"address"),    
            "addressDetail" : getParameter(resultGetData,"addressDtl"),    
            "bizGrp"        : getParameter(resultGetData,"typeCode"),    
            "tel"           : paramEscape(getParameter(resultGetData,"tel")),    
            "fax"           : paramEscape(getParameter(resultGetData,"fax")),    
            "taxCustName"   : getParameter(resultGetData,"taxCustNm"),    
            "taxTel"        : paramEscape(getParameter(resultGetData,"taxTel")),    
            "taxFax"        : paramEscape(getParameter(resultGetData,"taxFax")),    
            "taxPhone"      : paramEscape(getParameter(resultGetData,"taxPhone")),    
            "taxEmail"      : getParameter(resultGetData,"taxEmail"),    
            "bankNm"        : getParameter(resultGetData,"bankNm"),    
            "bankAccNo"     : getParameter(resultGetData,"bankAccNo"),    
            "bankHolder"    : getParameter(resultGetData,"bankHolder"),    
            "salesNm"       : getParameter(resultGetData,"salesNm"),    
            "salesTel"      : getParameter(resultGetData,"salesTel"),    
            "billingNm"     : getParameter(resultGetData,"billingNm"),    
            "billingTel"    : getParameter(resultGetData,"billingTel"),    
            "kpcSalesNm"    : getParameter(resultGetData,"kpcSalesNm"),    
            "kpcSalesTel"   : getParameter(resultGetData,"kpcSalesTel"),    
            "kpcBillingNm"  : getParameter(resultGetData,"kpcBillingNm"),    
            "kpcBillingTel" : getParameter(resultGetData,"kpcBillingTel"),    
            "agentId"       : getParameter(resultGetData,"agentId"),    
            "agentPw"       : getParameter(resultGetData,"agentPw"),    
            "useFlag"       : getParameter(resultGetData,"useFlag"),    
            "urlHome"       : getParameter(resultGetData,"urlHome")
        }
        # TODO : 이지점에 PUSH 추가
        return postData("/merchants/merchant", postMerchantData,{})    

@approvalApi.route('/api/approval/submerchant/approvals/approval', methods=['POST'])
def postSubMerchantApproval():
    formData = request.json
    return json.dumps(submerchantApproval(formData))

@approvalApi.route("/api/approval/submerchant/approvals/reject/reApproval", methods=['POST'])
def postSubMerchantRejectReApproval():
    formData = request.json
    postMerchantData = {                                         
        "parentId"      : getParameter(formData,"parentId"),   
        "name"          : getParameter(formData,"name"),   
        "alias"         : getParameter(formData,"alias"),    
        "ceoName"       : getParameter(formData,"ceoNm"),    
        "openDate"      : paramEscape(getParameter(formData,"openDt")) ,    
        "bizRegNo"      : paramEscape(getParameter(formData,"bizRegNo")),    
        "corpRegNo"     : paramEscape(getParameter(formData,"corpRegNo")),    
        "bizKind"       : getParameter(formData,"bizKind"),    
        "bizCond"       : getParameter(formData,"bizCond"),    
        "zipcode"       : getParameter(formData,"zipcode"),    
        "address"       : getParameter(formData,"address"),    
        "addressDetail" : getParameter(formData,"addressDtl"),    
        "bizGrp"        : getParameter(formData,"bizGrp"),    
        "tel"           : paramEscape(getParameter(formData,"tel")),    
        "fax"           : paramEscape(getParameter(formData,"fax")),    
        "taxCustName"   : getParameter(formData,"taxCustNm"),    
        "taxTel"        : paramEscape(getParameter(formData,"taxTel")),    
        "taxFax"        : paramEscape(getParameter(formData,"taxFax")),    
        "taxPhone"      : paramEscape(getParameter(formData,"taxPhone")),    
        "taxEmail"      : getParameter(formData,"taxEmail"),    
        "bankNm"        : getParameter(formData,"bankNm"),    
        "bankAccNo"     : getParameter(formData,"bankAccNo"),    
        "bankHolder"    : getParameter(formData,"bankHolder"),    
        "salesNm"       : getParameter(formData,"salesNm"),    
        "salesTel"      : getParameter(formData,"salesTel"),    
        "billingNm"     : getParameter(formData,"billingNm"),    
        "billingTel"    : getParameter(formData,"billingTel"),    
        "kpcSalesNm"    : getParameter(formData,"kpcSalesNm"),    
        "kpcSalesTel"   : getParameter(formData,"kpcSalesTel"),    
        "kpcBillingNm"  : getParameter(formData,"kpcBillingNm"),    
        "kpcBillingTel" : getParameter(formData,"kpcBillingTel"),    
        "agentId"       : getParameter(formData,"agentId"),    
        "agentPw"       : getParameter(formData,"agentPw"),    
        "useFlag"       : getParameter(formData,"useFlag"),    
        "urlHome"       : getParameter(formData,"urlHome"),
        "reqEmpId"      : session['empId'],
        "apprEmpId"     : getParameter(formData,"apprEmpId"),
        "tmpSeq"        : getParameter(formData,"tmpSeq"),
        "seq"           : getParameter(formData,"seq"),            
        "encAgentPw"    : getParameter(formData,"encAgentPw"),            
    }
    # TODO : 이지점에 PUSH 추가
    return json.dumps(postData("/approval/submerchant/approvals/reject/reApproval", postMerchantData,{}))

@approvalApi.route('/api/approval/service/approvals/serviceTmp', methods=['GET'])
def getServiceApprovalTmp():
    queryData = {
        'tmpSeq' : getParameter({}, "tmpSeq"),
        'empId'  : session['empId'],
    }
    result_data = getData("/approval/submerchant/service/approvals/serviceTmp" ,queryData, {})
    return json.dumps(result_data)

@approvalApi.route("/api/approval/service/approvals/reject/reApproval", methods=['POST'])
def postServiceRejectReApproval():
    formData = request.json
    putServiceData = {
        "serviceId"     : getParameter(formData, "serviceId"), 
        "submerchantId" : getParameter(formData, "submerchantId"),
        "name"          : getParameter(formData, "name"), 
        "category"      : getParameter(formData, "category"),
        "serviceType"   : getParameter(formData, "serviceType"),
        "useFlag"       : getParameter(formData, "useFlag"), 
        "saleDivider"   : getParameter(formData, "saleDivider"),
        "svcConnId"     : getParameter(formData, "svcConnId"),
        "svcConnPw"     : getParameter(formData, "svcConnPw"),
        "updateAdmId"   : session['empId'],
        "reqEmpId"      : session['empId'],
        "apprEmpId"     : getParameter(formData,"apprEmpId"),
        "tmpSeq"        : getParameter(formData,"tmpSeq"),
        "seq"           : getParameter(formData,"seq")        
    }    
    # TODO : 이지점에 PUSH 추가
    return json.dumps(postData("/approval/submerchant/service/approvals/reject/reApproval", putServiceData,{}))

def serviceApproval(formData):
    queryData = {
        'seq'    : setStringToLong(paramEscape(getParameter(formData, "seq"))),
        'tmpSeq' : setStringToLong(paramEscape(getParameter(formData, "tmpSeq"))),
        'empId'  : session['empId'],
    }
    postData("/approval/approval" ,queryData, {})
    resultGetData = getData("/approval/submerchant/service/approvals/serviceTmp" ,queryData, {})
    apprTypeCode = resultGetData["apprTypeCode"]
    if apprTypeCode == "APPR-0301" and resultGetData["serviceId"] != None :
        putServiceData = {
            "serviceId"     : getParameter(resultGetData, "serviceId"),
            "submerchantId" : getParameter(resultGetData, "submerchantId"),
            "name"          : getParameter(resultGetData, "name"),
            "category"      : getParameter(resultGetData, "category"), 
            "serviceType"   : getParameter(resultGetData, "serviceType"),
            "saleDivider"   : getParameter(resultGetData, "saleDivider"),
            "useFlag"       : getParameter(resultGetData, "useFlag"), 
            "svcConnId"     : getParameter(resultGetData, "svcConnId"), 
            "svcConnPw"     : getParameter(resultGetData, "svcConnPw"),
            "updateDesc"    : "신규등록" ,
            "updateAdmId"   : session['empId'],
        }
        # TODO : 이지점에 PUSH 추가
        return putData("/merchants/services/service", putServiceData,{})
    elif apprTypeCode == "APPR-0302" and resultGetData["serviceId"] != None :
        deleteServiceData = {
            "serviceId"      : resultGetData["serviceId"]
        }
        # TODO : 이지점에 PUSH 추가
        return deleteData("/merchants/services/service",{}, deleteServiceData)
    else :
        postServiceData = {
            "submerchantId" : getParameter(resultGetData, "submerchantId"),
            "serviceName"   : getParameter(resultGetData, "name"),
            "category"      : getParameter(resultGetData, "category"), 
            "serviceType"   : getParameter(resultGetData, "serviceType"),
            "saleDivider"   : getParameter(resultGetData, "saleDivider"),
            "useFlag"       : getParameter(resultGetData, "useFlag"), 
            "svcConnId"     : getParameter(resultGetData, "svcConnId"), 
            "svcConnPw"     : getParameter(resultGetData, "svcConnPw"),
            "createDesc"    : "신규등록",
            "createAdmId"   : session['empId'],
        }
        # TODO : 이지점에 PUSH 추가
        return postData("/merchants/services/service", postServiceData,{})

@approvalApi.route('/api/approval/service/approvals/approval', methods=['POST'])
def postServiceApproval():
    formData = request.json
    return json.dumps(serviceApproval(formData))

@approvalApi.route('/api/approval/billing/approvals/billingTmp', methods=['GET'])
def getBillingApprovalTmp():
    queryData = {
        'tmpSeq' : getParameter({}, "tmpSeq"),
        'empId'  : session['empId'],
    }
    result_data = getData("/approval/submerchant/billing/approvals/billingTmp" ,queryData, {})
    return json.dumps(result_data)

@approvalApi.route("/api/approval/billing/approvals/reject/reApproval", methods=['POST'])
def postBillingRejectReApproval():
    formData = request.json
    putBillingData = {
        "serviceBillingId" : getParameter(formData ,"serviceBillingId"       ),         
        "serviceId"        : getParameter(formData ,"serviceId"              ),         
        "name"             : getParameter(formData ,"name"                   ), 
        "bankNm"           : getParameter(formData ,"bankCd"                 ), 
        "bankAccNo"        : getParameter(formData ,"bankAccNo"              ), 
        "bankHolder"       : getParameter(formData ,"bankHolder"             ), 
        "billingNm"        : getParameter(formData ,"billingNm"              ), 
        "billingTel"       : getParameter(formData ,"billingTel"             ), 
        "billingEmail"     : getParameter(formData ,"billingEmail"           ), 
        "billingEmail"     : getParameter(formData ,"billingEmail"           ), 
        "kpcBillingNm"     : getParameter(formData ,"kpcBillingNm"           ), 
        "kpcBillingTel"    : getParameter(formData ,"kpcBillingTel"          ), 
        "kpcBillingEmail"  : getParameter(formData ,"kpcBillingEmail"        ), 
        "divider"          : getParameter(formData ,"divider"                ), 
        "code"             : getParameter(formData ,"code"                   ), 
        "billingDuration"  : getParameter(formData ,"billingDuration"        ), 
        "billingDt"        : paramEscape(getParameter(formData ,"billingDt") ), 
        "merchantCommType" : getParameter(formData ,"merchantCommType"       ), 
        "merchantTaxType"  : getParameter(formData ,"merchantTaxType"        ), 
        "merchantCommision": getParameter(formData ,"merchantCommision"      ), 
        "aplEndDt"         : paramEscape(getParameter(formData ,"aplEndDate")), 
        "updateAdmId"      : session['empId'],
        "reqEmpId"         : session['empId'],
        "apprEmpId"        : getParameter(formData,"apprEmpId"               ),
        "tmpSeq"           : getParameter(formData,"tmpSeq"                  ),
        "seq"              : getParameter(formData,"seq"                     ),         
    }
    # TODO : 이지점에 PUSH 추가
    return json.dumps(postData("/approval/submerchant/billing/approvals/reject/reApproval", putBillingData,{}))


def billingApproval(formData):
    queryData = {
        'seq'    : setStringToLong(paramEscape(getParameter(formData, "seq"))),
        'tmpSeq' : setStringToLong(paramEscape(getParameter(formData, "tmpSeq"))),
        'empId'  : session['empId'],
    }
    postData("/approval/approval" ,queryData, {})
    resultGetData = getData("/approval/submerchant/billing/approvals/billingTmp" ,queryData, {})
    apprTypeCode = resultGetData["apprTypeCode"]
    if apprTypeCode == "APPR-0401" and resultGetData["serviceBillingId"] != None :
        putBillingData = {
            "serviceBillingId" : getParameter(resultGetData ,"serviceBillingId"),           
            "serviceId"        : getParameter(resultGetData ,"serviceId"),           
            "name"             : getParameter(resultGetData ,"name"), 
            "bankNm"           : getParameter(resultGetData ,"bankCd"),   
            "bankAccNo"        : getParameter(resultGetData ,"bankAccNo"),  
            "bankHolder"       : getParameter(resultGetData ,"bankHolder"),  
            "billingNm"        : getParameter(resultGetData ,"billingNm"),   
            "billingTel"       : getParameter(resultGetData ,"billingTel"),   
            "billingEmail"     : getParameter(resultGetData ,"billingEmail"),  
            "billingEmail"     : getParameter(resultGetData ,"billingEmail"),  
            "kpcBillingNm"     : getParameter(resultGetData ,"kpcBillingNm"),  
            "kpcBillingTel"    : getParameter(resultGetData ,"kpcBillingTel"),  
            "kpcBillingEmail"  : getParameter(resultGetData ,"kpcBillingEmail"),  
            "divider"          : getParameter(resultGetData ,"divider"),   
            "code"             : getParameter(resultGetData ,"code"),   
            "billingDuration"  : getParameter(resultGetData ,"billingDuration"),  
            "billingDt"        : paramEscape(getParameter(resultGetData ,"billingDt")),  
            "merchantCommType" : getParameter(resultGetData ,"merchantCommType"),   
            "merchantTaxType"  : getParameter(resultGetData ,"merchantTaxType"),  
            "merchantCommision": getParameter(resultGetData ,"merchantCommision"),  
            "aplEndDt"         : paramEscape(getParameter(resultGetData ,"aplEndDt")),  
            "updateAdmId"      : session['empId'],
        }
        # TODO : 이지점에 PUSH 추가
        return putData("/merchants/services/service/billing", putBillingData , {})
    else :
        postBillingData = {
            "serviceId"        : getParameter(resultGetData,"serviceId"),           
            "name"             : getParameter(resultGetData,"name"), 
            "bankNm"           : getParameter(resultGetData,"bankCd"),   
            "bankAccNo"        : getParameter(resultGetData,"bankAccNo"),   
            "bankHolder"       : getParameter(resultGetData,"bankHolder"),   
            "billingNm"        : getParameter(resultGetData,"billingNm"),   
            "billingTel"       : getParameter(resultGetData,"billingTel"),   
            "billingEmail"     : getParameter(resultGetData,"billingEmail"),   
            "billingEmail"     : getParameter(resultGetData,"billingEmail"),   
            "kpcBillingNm"     : getParameter(resultGetData,"kpcBillingNm"),   
            "kpcBillingTel"    : getParameter(resultGetData,"kpcBillingTel"),   
            "kpcBillingEmail"  : getParameter(resultGetData,"kpcBillingEmail"),  
            "divider"          : getParameter(resultGetData,"divider"),  
            "code"             : getParameter(resultGetData,"code"),   
            "billingDuration"  : getParameter(resultGetData,"billingDuration"),   
            "billingDt"        : paramEscape(getParameter(resultGetData,"billingDt")),  
            "merchantCommType" : getParameter(resultGetData,"merchantCommType"),  
            "merchantTaxType"  : getParameter(resultGetData,"merchantTaxType"),   
            "merchantCommision": getParameter(resultGetData,"merchantCommision"),   
            "createAdmId"      : session['empId'], 
        }
        # TODO : 이지점에 PUSH 추가
        return postData("/merchants/services/service/billing", postBillingData,{})

@approvalApi.route('/api/approval/billing/approvals/approval', methods=['POST'])
def postBillingApproval():
    formData = request.json
    return json.dumps(billingApproval(formData))

@approvalApi.route('/api/approval/merchant/approvals/history', methods=['GET'])
def getMerchantApprovalsHistory():
    formData = json.loads(request.args.get("formData"))
    searchDate = getParameter(formData , "startDate").split(' - ')
    startDate = paramEscape(searchDate[0])
    endDate = paramEscape(searchDate[1])
    queryData = {
        'name'       : getParameter(formData, "name"),
        'reqEmpNm'   : getParameter(formData, "reqEmpName"),
        'typeCode'   : getParameter(formData, "type"),
        'historyType': getParameter(formData, "historyType"),
        'startDate'  : startDate,
        'endDate'    : endDate,
        'empId'      : session['empId'],
        'offset'     : strToLong(request.args.get("start")),
        'limit'      : strToLong(request.args.get("length")),
    }
    result_data = getApiData("/approval/merchant/approvals/history" ,queryData)
    return json.dumps(result_data)

@approvalApi.route('/api/approval/submerchant/approvals/history', methods=['GET'])
def getSubMerchantApprovalsHistory():
    formData = json.loads(request.args.get("formData"))
    searchDate = getParameter(formData , "startDate").split(' - ')
    startDate = paramEscape(searchDate[0])
    endDate = paramEscape(searchDate[1])
    queryData = {
        'name'       : getParameter(formData, "name"),
        'reqEmpNm'   : getParameter(formData, "reqEmpName"),
        'typeCode'   : getParameter(formData, "type"),
        'historyType': getParameter(formData, "historyType"),
        'startDate'  : startDate,
        'endDate'    : endDate,
        'empId'      : session['empId'],
        'offset'     : strToLong(request.args.get("start")),
        'limit'      : strToLong(request.args.get("length")),
    }
    result_data = getApiData("/approval/submerchant/approvals/history" ,queryData)
    return json.dumps(result_data)

@approvalApi.route('/api/approval/service/approvals/history', methods=['GET'])
def getSubMerchantServiceApprovalsHistory():
    formData = json.loads(request.args.get("formData"))
    searchDate = getParameter(formData , "startDate").split(' - ')
    startDate = paramEscape(searchDate[0])
    endDate = paramEscape(searchDate[1])
    queryData = {
        'name'       : getParameter(formData, "name"),
        'reqEmpNm'   : getParameter(formData, "reqEmpName"),
        'typeCode'   : getParameter(formData, "type"),
        'historyType': getParameter(formData, "historyType"),
        'startDate'  : startDate,
        'endDate'    : endDate,
        'empId'      : session['empId'],
        'offset'     : strToLong(request.args.get("start")),
        'limit'      : strToLong(request.args.get("length")),
    }
    result_data = getApiData("/approval/submerchant/service/approvals/history" ,queryData)
    return json.dumps(result_data)

@approvalApi.route('/api/approval/billing/approvals/history', methods=['GET'])
def getSubMerchantBillingApprovalsHistory():
    formData = json.loads(request.args.get("formData"))
    searchDate = getParameter(formData , "startDate").split(' - ')
    startDate = paramEscape(searchDate[0])
    endDate = paramEscape(searchDate[1])
    queryData = {
        'name'       : getParameter(formData, "name"),
        'reqEmpNm'   : getParameter(formData, "reqEmpName"),
        'typeCode'   : getParameter(formData, "type"),
        'historyType': getParameter(formData, "historyType"),
        'startDate'  : startDate,
        'endDate'    : endDate,
        'empId'      : session['empId'],
        'offset'     : strToLong(request.args.get("start")),
        'limit'      : strToLong(request.args.get("length")),
    }
    result_data = getApiData("/approval/submerchant/billing/approvals/history" ,queryData)
    return json.dumps(result_data)

"""
승인 요청 취소
"""
@approvalApi.route('/api/approvals/request/cancellation', methods=['PUT'])
def cancalApproval():
    formData = request.json
        
    cancelData = {
        'seq' : formData,
        'loginEmpId': session['empId'],
        }
            
    resultData = request_put("/approvals/request/cancellation", cancelData, API_SERVER_BACKOFFICE);

    return json.dumps(resultData)

"""
승인 요청 승인
"""
@approvalApi.route('/api/approvals/response/approval', methods=['POST'])
def merchantApprovalArray():
    formData = request.json
    
    approvalData = {
        'approvalList' : formData,
        'empId': session['empId']
        }

    resultData = request_post("/approvals/response/approval", approvalData, API_SERVER_BACKOFFICE)

    return json.dumps(resultData)

"""
승인 요청 반려
"""
@approvalApi.route('/api/approvals/response/rejection', methods=['POST'])
def merchantRejectArray():
    
    formData = request.json
    
    rejectData = {
        'rejectApprSeqList': formData.get('sequenceList'),
        'apprEmpId': session['empId'],
        'apprMemo': formData.get('apprMemo'),
    }

    resultData = rejectApprovalList(rejectData)
    
    return json.dumps(resultData)

#대표거래처 - 승인 대기중인 승인정보 수정
@approvalApi.route('/api/approvals/request/merchant/<apprContentSeq>/<processType>', methods=['PUT'])
def updateApprovalRequestForMerchant(apprContentSeq, processType):
    form_data = request.json
    merchantData = {
        "merchantId"     : getParameter(form_data,"merchantId"),                  
        "name"           : getParameter(form_data,"name"),                  
        "alias"          : getParameter(form_data,"alias"),                 
        "ceoName"        : getParameter(form_data,"ceoName"),               
        "openDate"       : paramEscape(getParameter(form_data,"openDate")), 
        "bizRegNo"       : paramEscape(getParameter(form_data,"bizRegNo")), 
        "corpRegNo"      : paramEscape(getParameter(form_data,"corpRegNo")),
        "bizKind"        : getParameter(form_data,"bizKind"),               
        "bizCond"        : getParameter(form_data,"bizCond"),               
        "bizGrp"         : getParameter(form_data,"bizGrp"),                
        "useFlag"        : getParameter(form_data,"useFlag"),               
        "zipCode"        : getParameter(form_data,"zipCode"),  
        "address"        : getParameter(form_data,"address"),        
        "addressDetail"  : getParameter(form_data,"addressDetail"),  
        "tel"            : paramEscape(getParameter(form_data,"tel")),      
        "fax"            : paramEscape(getParameter(form_data,"fax")),
        "createDesc"     : "수정 요청",        
        "reqMemo"        : getParameter(form_data,"reqMemo"),
        "reqEmpId"       : session['empId'],
        "apprEmpId"      : getParameter(form_data,"apprEmpId")
    }
    
    reponseResult = request_put("/approvals/request/merchant/"+apprContentSeq+"/"+processType, merchantData, '1')

    return json.dumps(reponseResult)

#일반거래처 - 승인 대기중인 승인정보 수정
@approvalApi.route('/api/approvals/request/sub-merchant/<apprContentSeq>/<processType>', methods=['PUT'])
def updateApprovalRequestForSubMerchant(apprContentSeq, processType):
    form_data = request.json
    subMerchantData = {
        "subMerchantId" : getParameter(form_data,"subMerchantId"),   
        "parentId"      : getParameter(form_data,"parentId"),   
        "name"          : getParameter(form_data,"name"),   
        "alias"         : getParameter(form_data,"alias"),    
        "ceoName"       : getParameter(form_data,"ceoName"),    
        "openDate"      : paramEscape(getParameter(form_data,"openDate")) ,    
        "bizRegNo"      : paramEscape(getParameter(form_data,"bizRegNo")),    
        "corpRegNo"     : paramEscape(getParameter(form_data,"corpRegNo")),    
        "bizKind"       : getParameter(form_data,"bizKind"),    
        "bizCond"       : getParameter(form_data,"bizCond"),    
        "zipCode"       : getParameter(form_data,"zipcode"),    
        "address"       : getParameter(form_data,"address"),    
        "addressDetail" : getParameter(form_data,"addressDetail"),    
        "type"        : getParameter(form_data,"bizGrp"),    
        "tel"           : paramEscape(getParameter(form_data,"tel")),    
        "fax"           : paramEscape(getParameter(form_data,"fax")),    
        "taxCustName"   : getParameter(form_data,"taxCustNm"),    
        "taxTel"        : paramEscape(getParameter(form_data,"taxTel")),    
        "taxFax"        : paramEscape(getParameter(form_data,"taxFax")),    
        "taxPhone"      : paramEscape(getParameter(form_data,"taxPhone")),    
        "taxEmail"      : getParameter(form_data,"taxEmail"),    
        "bankName"        : getParameter(form_data,"bankNm"),    
        "bankAccountNo"     : getParameter(form_data,"bankAccNo"),    
        "bankHolder"    : getParameter(form_data,"bankHolder"),    
        "salesName"       : getParameter(form_data,"salesNm"),    
        "salesTel"      : getParameter(form_data,"salesTel"),    
        "billingName"     : getParameter(form_data,"billingNm"),    
        "billingTel"    : getParameter(form_data,"billingTel"),    
        "kpcSalesName"    : getParameter(form_data,"kpcSalesNm"),    
        "kpcSalesTel"   : getParameter(form_data,"kpcSalesTel"),    
        "kpcBillingName"  : getParameter(form_data,"kpcBillingNm"),    
        "kpcBillingTel" : getParameter(form_data,"kpcBillingTel"),    
        "agentId"       : getParameter(form_data,"agentId"),    
        "agentPw"       : getParameter(form_data,"agentPw"),    
        "useFlag"       : getParameter(form_data,"useFlag"),    
        "urlHome"       : getParameter(form_data,"urlHome"),
        "createDesc"     : "수정 요청",      
        "reqMemo"        : getParameter(form_data,"reqMemo"),
        "reqEmpId"      : session['empId'],
        "apprEmpId"     : getParameter(form_data,"apprEmpId")
    }
    
    reponseResult = request_put("/approvals/request/sub-merchant/"+apprContentSeq+"/"+processType, subMerchantData, '1')

    return json.dumps(reponseResult)

#거래처서비스 - 승인 대기중인 승인정보 수정
@approvalApi.route('/api/approvals/request/sub-merchant/service/<apprContentSeq>/<processType>', methods=['PUT'])
def updateApprovalRequestForSubMerchantService(apprContentSeq, processType):
    form_data = request.json
    subMerchantData = {
        "serviceId"     : getParameter(form_data, "serviceId"), 
        "subMerchantId" : getParameter(form_data, "submerchantId"),
        "serviceName"   : getParameter(form_data, "serviceName"), 
        "category"      : getParameter(form_data, "category"),
        "type"   : getParameter(form_data, "type"),
        "useFlag"       : getParameter(form_data, "useFlag"), 
        "saleDivider"   : getParameter(form_data, "saleDivider"),
        "svcConnId"     : getParameter(form_data, "svcConnId"),
        "svcConnPw"     : getParameter(form_data, "svcConnPw"),
        "updateAdmId"   : session['empId'],  
        "reqEmpId"      : session['empId'],
        "reqMemo"     : getParameter(form_data,"reqMemo"),
        "apprEmpId"     : getParameter(form_data,"apprEmpId"),   
        "createDesc"     : "수정 요청",      
        "reqMemo"        : getParameter(form_data,"reqMemo"),
        "reqEmpId"      : session['empId'],
        "apprEmpId"     : getParameter(form_data,"apprEmpId")
    }
    
    reponseResult = request_put("/approvals/request/sub-merchant/service/"+apprContentSeq+"/"+processType, subMerchantData, '1')

    return json.dumps(reponseResult)

#서비스정산 - 승인 대기중인 승인정보 수정
@approvalApi.route('/api/approvals/request/sub-merchant/service/billing/<apprContentSeq>/<processType>', methods=['PUT'])
def updateApprovalRequestForSubMerchantBilling(apprContentSeq, processType):
    form_data = request.json
    billingData = {
        "serviceBillingId" : getParameter(form_data,"serviceBillingId"),           
        "serviceId" : getParameter(form_data,"serviceId"),           
        "name"             : getParameter(form_data,"name"), 
        "bankCode"         : getParameter(form_data,"bankCode"),   
        "bankAccountNo"    : getParameter(form_data,"bankAccNo"),   
        "bankHolder"       : getParameter(form_data,"bankHolder"),   
        "managerName"        : getParameter(form_data,"managerName"),   
        "managerTel"       : getParameter(form_data,"managerTel"),   
        "managerEmail"     : getParameter(form_data,"managerEmail"),   
        "kpcManagerName"     : getParameter(form_data,"kpcManagerName"),   
        "kpcManagerTel"    : getParameter(form_data,"kpcManagerTel"),   
        "kpcManagerEmail"  : getParameter(form_data,"kpcManagerEmail"),  
        "code"             : getParameter(form_data,"code"),   
        "divider"          : getParameter(form_data,"divider"),  
        "billingDate"      : paramEscape(getParameter(form_data,"billingDt")),
        "billingStartDate"  : paramEscape(getParameter(form_data,"billingStartDate")),  
        "billingDuration"  : getParameter(form_data,"billingDuration"),   
        "billingCommisionType"  : getParameter(form_data,"billingCommType" ),
        "merchantCommisionType" : getParameter(form_data,"merchantCommType"),  
        "merchantCommision": getParameter(form_data,"merchantCommision"),   
        "merchantTaxType"  : getParameter(form_data,"merchantTaxType"),   
        "createAdmId"      : session['empId'], 
        "reqEmpId"         : session['empId'],
        "reqMemo"        : getParameter(form_data,"reqMemo"),
        "apprEmpId"        : getParameter(form_data,"apprEmpId")
    }
    
    reponseResult = request_put("/approvals/request/sub-merchant/service/billing/"+apprContentSeq+"/"+processType, billingData, '1')

    return json.dumps(reponseResult)


#서비스정산 수수료 - 승인 대기중인 승인정보 수정
@approvalApi.route('/api/approvals/request/sub-merchant/service/billing/commision/<apprContentSeq>/<processType>', methods=['PUT'])
def updateApprovalRequestForBillingCommision(apprContentSeq, processType):
    form_data = request.json
    
    billingData = {                                         
        "serviceBillingId"             : getParameter(form_data,"serviceBillingId"),
        "serviceId" : getParameter(form_data,"serviceId"),    
        "commisionId"             : getParameter(form_data,"commisionId"),
        "code"             : getParameter(form_data,"billingCode"),   
        "divider"          : getParameter(form_data,"billingDivider"),  
        "billingDate"      : paramEscape(getParameter(form_data,"billingDt")),  
        "billingDuration"  : getParameter(form_data,"billingDuration"),   
        "billingCommisionType"  : getParameter(form_data,"billingCommType" ),
        "merchantCommisionType" : getParameter(form_data,"merchantCommType"),  
        "merchantCommision": getParameter(form_data,"merchantCommision"),   
        "merchantTaxType"  : getParameter(form_data,"merchantTaxType"),
        "billingStartDate"  : paramEscape(getParameter(form_data,"billingStartDate")),
        "beforeBillingEndDate"  : getParameter(form_data,"beforeBillingEndDate"),
        "createAdmId"      : session['empId'], 
        "reqEmpId"         : session['empId'],
        "reqMemo"        : getParameter(form_data,"reqMemo"),
        "apprEmpId"        : getParameter(form_data,"apprEmpId")
    }
    
    reponseResult = request_put("/approvals/request/sub-merchant/service/billing/commision/"+apprContentSeq+"/"+processType, billingData, '1')

    return json.dumps(reponseResult)

#KCON 상품 - 승인 대기중인 승인정보 수정
@approvalApi.route('/api/approvals/request/kcon/brochure/<apprContentSeq>/<processType>', methods=['PUT'])
def updateApprovalRequestForKconBrochure(apprContentSeq, processType):
    form_data = request.json
    kconData = {
        'merchantId'     : kconID, 
        'merchantPassword'     : kconPW,
        "productId"      : getParameter(form_data,"productId"),
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
        "reqMemo"        : getParameter(form_data,"reqMemo"),
        "apprEmpId"      : getParameter(form_data,"apprEmpId")
    }
    reponseResult = request_put("/approvals/request/kcon/brochure/"+apprContentSeq+"/"+processType, kconData, '1')

    return json.dumps(reponseResult)

#KCON 쿠폰 - 승인 대기중인 승인정보 수정
@approvalApi.route("/api/approvals/request/kcon/coupon/extension/<apprSeq>/update", methods=['PUT'])
def extendDate(apprSeq):
    formData = request.json
    queryData = {
        "endDate" : paramEscape(getParameter(formData, "endDate")),
        "reqEmpId"  : session['empId'],
        "reqMemo" : getParameter(formData, "reqMemo"),
        "apprEmpId" : getParameter(formData, "apprEmpId")
    }
    
    reponseResult = request_put("/approvals/request/kcon/coupon/extension/"+apprSeq+"/update", queryData, '1')

    return json.dumps(reponseResult)

#충전권 - 승인 대기중인 승인정보 수정
@approvalApi.route("/api/approvals/request/coupon/charge/<apprSeq>/update", methods=['PUT'])
def updateChargeCouponApprovalInfo(apprSeq):
    formData = request.json
    
    queryData = {
        "endDate" : paramEscape(getParameter(formData, "endDate")),
        "reqEmpId"  : session['empId'],
        "reqMemo" : getParameter(formData, "reqMemo"),
        "apprEmpId" : getParameter(formData, "apprEmpId")
    }
    
    reponseResult = request_put("/approvals/request/coupon/charge/"+apprSeq+"/update", queryData, '1')

    return json.dumps(reponseResult)

#카드 잔액환불 - 승인 대기중인 승인정보 수정
@approvalApi.route("/api/approvals/request/card/balance-refund/<apprSeq>/update", methods=['PUT'])
def updateCardBalanceRefundApprovalInfo(apprSeq):
    form_data = request.json
    requestData = {
        "cardNo"            :   getParameter(form_data,"cardNo"),                                                    # : String,
        "balance"           :   paramEscape(getParameter(form_data,"balance")),                  
        "refundCommision"   :   paramEscape(getParameter(form_data,"refundCommision")),                 
        "customerName"      :   getParameter(form_data,"customerName"),               
        "customerTel"       :   paramEscape(getParameter(form_data,"customerTel")), 
        "refundBankCode"    :   getParameter(form_data,"bankCode"), 
        "refundBankAccountNo" : getParameter(form_data,"bankAccountNo"),
        "refundBankHolder"    : getParameter(form_data,"bankHolder"),               
        "refundDesc"        :   getParameter(form_data,"refundDesc"),               
        "reqEmpId"       :      session['empId'],
        "apprEmpId"      :      getParameter(form_data,"apprEmpId")
        }
    reponseResult = request_put("/approvals/request/card/balance-refund/"+apprSeq+"/update", requestData, '1')

    return json.dumps(reponseResult)


#승인요청 정보가 있는지 확인
@approvalApi.route('/api/approvals/request/<refId>/exist', methods=['GET'])
def existApprovalRequest(refId):
    return json.dumps(request_get("/approvals/request/"+refId+"/exist", None, API_SERVER_BACKOFFICE)) 

#서비스에 정산정보가 있는지 확인
@approvalApi.route('/api/approvals/request/billing/exist/<serviceId>', methods=['GET'])
def existBillingByService(serviceId):
    return json.dumps(request_get("/approvals/request/billing/exist/"+str(serviceId), None, API_SERVER_BACKOFFICE)) 

@approvalApi.route('/api/approvals/request/<workType>/<refId>/re-approval/possibility', methods=['GET'])
def possibleReApproval(workType, refId):
    return json.dumps(request_get("/approvals/request/"+workType+"/"+refId+"/re-approval/possibility", None, API_SERVER_BACKOFFICE)) 
    
@approvalApi.route('/api/approvals/notification', methods=['POST'])
def approvalNotifiSmsService():
    formData = request.json
    
    notiInfo = {
            "message" : formData.get("message"),
            "senderId" : session['empId'],
            "receiverId" : formData.get("receiverEmpId"), 
            "approvalType": formData.get("approvalType")
        }
    
    result = approvalNotiSendSms(notiInfo)
    
    return json.dumps(result) 
    
    
    

@approvalApi.route('/api/approvals/<menuType>/excel', methods=['GET'])
def makeApprovalRequestListExcel(menuType):
    
    formData = json.loads(request.args.get("formData"))
    
    print(formData)
    
    searchDate = getParameter(formData , "searchDate").split(' - ')
    startDate = paramEscape(searchDate[0])
    endDate = paramEscape(searchDate[1])
    queryData = {
        'workType' : getParameter(formData, "workType"),
        'reqType' : getParameter(formData, "reqType"),
        'keyword' : getParameter(formData, "keyword"),
        'reqEmpName'   : getParameter(formData, "reqEmpName"),
        'apprEmpName'   : getParameter(formData, "apprEmpName"),
        'status'       : getParameter(formData, "status"),
        'searchDateType'       : getParameter(formData, "searchDateType"),
        'startDate'    : startDate,
        'endDate'      : endDate,
        'loginEmpId'        : session['empId'],
        'reqDateOrdering'       : getParameter(formData, "reqDateOrdering"),
        'apprDateOrdering'       : getParameter(formData, "apprDateOrdering"),
        'defaultSearch'       : getParameter(formData, "defaultSearch"),
        'offset'       : strToLong(request.args.get("start")),
        'limit'        : strToLong(request.args.get("length"))
    }
    rootPath = current_app.root_path
    t1 = threading.Thread(target=makeApprovalRequestListExcelFile,args=[queryData,rootPath,menuType])
    t1.daemon = True
    t1.start()
    
    return "엑셀 작업요청"

def makeApprovalRequestListExcelFile(queryData,rootPath,menuType):
    excelZip = None
    jobStatus = 0
    batchId = None
    try:
        fileCnt = 1
        makeTime = str(int(round(time.time()*1000)))
        uploads = os.path.join(rootPath, "fileDownload" , "excel" , makeTime)
        if not os.path.isdir(uploads):
            os.makedirs(uploads)
            
        menuName = ""
        if menuType == "request":
            menuName = "신청"
        elif menuType == "answer":
            menuName = "결제"
            
        zipFileName = u'승인_'+menuName+'내역('+ queryData.get("startDate")+"~"+queryData.get("endDate")+').zip'
        #작업 시작 메시지 추가
        batchId = postBatchMng({
            "reqId"    : queryData['loginEmpId'],
            "status"   : "BAT-0001" , # 진행중
            "filePath" : os.path.join(uploads ,zipFileName),
            "content"  : "승인 "+menuName+"내역 조회",
            "errMsg"   : ""
        })["data"]["batchId"]
        fileName = '승인_'+menuName+'내역('+ queryData.get("startDate")+"~"+queryData.get("endDate")+').xlsx'
        workbook = xlsxwriter.Workbook(os.path.join(uploads ,setUnicodeEncodeTypeToEucKr(fileName)))
        worksheet = workbook.add_worksheet()
        
        worksheet.set_column(0, 0, 10)
        worksheet.set_column(1, 1, 20)
        worksheet.set_column(2, 2, 30)
        worksheet.set_column(3, 3, 20)
        worksheet.set_column(4, 4, 20)
        worksheet.set_column(5, 5, 20)
        worksheet.set_column(6, 6, 20)
        worksheet.set_column(7, 7, 20)
        
        cell_format = workbook.add_format()
        cell_format.set_align("center")
        row = 0
        worksheet.write(row, 0  ,"번호", cell_format)
        worksheet.write(row, 1  ,"승인유형", cell_format)
        worksheet.write(row, 2  ,"키워드", cell_format)
        worksheet.write(row, 3  ,"처리구분", cell_format)
        worksheet.write(row, 4  ,"진행상태", cell_format)
        worksheet.write(row, 5  ,"신청일", cell_format)
        worksheet.write(row, 6  ,"처리일", cell_format)
        worksheet.write(row, 7  ,"승인자", cell_format)

        

        while True : 
            result_data = request_get("/approvals/"+menuType+"/excel" ,queryData, API_SERVER_BACKOFFICE)
            for data in result_data["data"]:
                row += 1
                if data['status']=='ARST-0003' or  data['status']=='ARST-0004' :
                    apprDate = '-'
                else :
                    apprDate = parseDate(data["apprDate"] ,'%Y-%m-%d %H:%M:%S' ,'%Y-%m-%d')
                                         
                worksheet.write(row, 0, row, cell_format)
                worksheet.write(row, 1, data["workTypeName"], cell_format)
                worksheet.write(row, 2, data["refTitle"], cell_format)
                worksheet.write(row, 3, data["reqTypeName"], cell_format)
                worksheet.write(row, 4, data["statusName"], cell_format)
                worksheet.write(row, 5, parseDate(data["reqDate"] ,'%Y-%m-%d %H:%M:%S' ,'%Y-%m-%d'), cell_format)
                worksheet.write(row, 6, apprDate , cell_format)
                worksheet.write(row, 7, data["apprEmpName"], cell_format)
                
                if row >= EXCEL_FILE_MAKE_LIMT_COUNT :
                    row = 0
                    fileCnt += 1
                    fileName = '승인_'+menuName+'내역('+ queryData.get("startDate")+"~"+queryData.get("endDate")+').xlsx'
                    # 디비 조회건수 * 2 row 생성시 파일 재생성
                    workbook.close()
                    workbook = xlsxwriter.Workbook(os.path.join(uploads ,setUnicodeEncodeTypeToEucKr(fileName)))
                    worksheet = workbook.add_worksheet()
                    worksheet.write(row, 0, "번호", cell_format)
                    worksheet.write(row, 1, "승인유형", cell_format)
                    worksheet.write(row, 2, "키워드", cell_format)
                    worksheet.write(row, 3, "처리구분", cell_format)
                    worksheet.write(row, 4, "진행상태", cell_format)
                    worksheet.write(row, 5, "신청일", cell_format)
                    worksheet.write(row, 6, "처리일", cell_format)
                    worksheet.write(row, 7, "승인자", cell_format)
                           
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
            "reqId"    : queryData['loginEmpId'],
            "status"   : "BAT-0003" , # 오류
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
                "reqId"    : queryData['loginEmpId'],
                "status"   : "BAT-0002" , # 완료
                "errMsg"   : ""
            })               
        #성공 메시지 추가
        print "성공"
        
        


"""
특정 이벤트에 대한 SMS 보내기
"""
def approvalNotiSendSms(notiInfo):
    sendSmsPhoneNo = getData("/employees/sendSmsPhoneNo", {"recieverId":notiInfo.get("receiverId"), "senderId":notiInfo.get("senderId")})
    
    print getEnv()
    if "code" not in sendSmsPhoneNo:
        recieverPhone = sendSmsPhoneNo["recieverPhone"]
        recieverName = sendSmsPhoneNo["recieverName"]
        senderName = sendSmsPhoneNo["senderName"]
        
#         if getEnv() == "DEV" : 
#              recieverPhone = '01040969987'

        message = notiInfo.get("message")
        if notiInfo.get("approvalType") == "request":
            message += "신청자 : ("+senderName+"님)"
        elif notiInfo.get("approvalType") == "answer":
            message += "승인자 : ("+senderName+"님)"
        
        # 문자 메시지 전송
        result = sendSms(recieverPhone , notiInfo.get("message"))

        return result

"""
승인 요청 승인
"""
@approvalApi.route('/api/approval/approve', methods=['POST'])
def approveApprovalInfo():
    formData = request.json
    
    approvalData = {
        'approvalList' : formData,
        'empId': session['empId']
        }

    resultData = postApiData("/approval/approve/approvalInfo", approvalData, API_SERVER_BACKOFFICE)

    return json.dumps(resultData)

"""
승인 요청 취소
"""
@approvalApi.route('/api/approval/cancel', methods=['PUT'])
def cancelApprovalInfo():
    formData = request.json
    
    approvalData = {
        'apprSeq' : formData,
        'empId': session['empId']
        }

    resultData = postApiData("/approval/cancel/approvalInfo", approvalData, API_SERVER_BACKOFFICE)

    return json.dumps(resultData)