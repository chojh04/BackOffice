# -*- coding:utf-8 -*-
import json

from flask import Blueprint, request
from flask.globals import session

from util.common import paramEscape, getApiData, postApiData, getApiSingleData, \
    strToLong, getParameter, getData, setStringToNumber, postData
from util.common import putApiData, deleteApiData, setNoneToBlank, \
    request_get, request_post, request_put, API_SERVER_BACKOFFICE


from util.notification import KpcNotification

merchantApi = Blueprint("merchantApi", __name__)

@merchantApi.route("/api/totalMerchants", methods=['GET'])
def totalMerchants():
    form_data = json.loads(request.args.get("formData"))
    if(form_data["target"] == ""):
        queryData = {
            'limit': setStringToNumber(request.args.get("length")),
            'offset': setStringToNumber(request.args.get("start")),
            'representId': getParameter(form_data,"merchantId"),
            'name': getParameter(form_data,"name"),
            'alias':getParameter(form_data,"alias"),
            'status': getParameter(form_data,"status"),
            'bizRegNo': paramEscape(getParameter(form_data,"bizRegNo")),
            
        }
        result_data = getApiData("/merchants/totalMerchants" ,queryData)
        return json.dumps(result_data) 
    elif(form_data["target"] == "2"):
        return merchants()
    return represents()

@merchantApi.route("/api/merchants/merchant/represent", methods=['POST','GET', "PUT", "DELETE"])
def represent():
    if (request.method == 'GET') :
        return getRepresent() 
    elif (request.method == 'POST') :
        return createMerchant()
    elif (request.method == 'PUT') :
        return updateMerchant()
    elif (request.method == 'DELETE') :
        return deleteRepresent()

def createMerchant():
    form_data = request.json
    merchantData = {
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
        "reqEmpId"       : session['empId'],
        "apprEmpId"      : getParameter(form_data,"apprEmpId"),
    }
    #return json.dumps(postApiData("/merchants/represent", postRepresentData))
    toNotiData = {
        "toEmpId": getParameter(form_data,"apprEmpId")
        ,"fromEmpId": session['empId']
        ,"message" : "대표 거래처 등록 승인 신청"
    }
    fromNotiData = {
        "toEmpId": session['empId']
        ,"fromEmpId": getParameter(form_data,"apprEmpId")
        ,"message" : "대표 거래처 등록 승인 신청"
    }
#     resultData = postData("/approvals/merchant/insert", merchantData,{})
    
    reponseResult = request_post("/approvals/request/merchant", merchantData, '1')
    
    if "status"  in reponseResult and reponseResult["status"] == "200" :
        KpcNotification().push_user_notification(toNotiData)
        KpcNotification().push_user_notification(fromNotiData)
    return json.dumps(reponseResult)
    
def updateMerchant():
    form_data = request.json
    merchantData = {
        "merchantId"     : getParameter(form_data,"merchantId"),                                                    # : String,
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
    toNotiData = {
        "toEmpId": getParameter(form_data,"apprEmpId")
        ,"fromEmpId": session['empId']
        ,"message" : "대표 거래처 수정 승인 신청"
    }
    fromNotiData = {
        "toEmpId": session['empId']
        ,"fromEmpId": getParameter(form_data,"apprEmpId")
        ,"message" : "대표 거래처 수정 승인 신청"
    }
    
    reponseResult = request_put("/approvals/request/merchant", merchantData, '1')
    
    if "status"  in reponseResult and reponseResult["status"] == "200" :
        KpcNotification().push_user_notification(toNotiData)
        KpcNotification().push_user_notification(fromNotiData)
    return json.dumps(reponseResult)
    
def deleteRepresent():
    
    form_data = request.json
    
    queryData = {
        "merchantId"     : getParameter(form_data,"merchantId"),                                                   # : String,
        "reqEmpId"       : session['empId'],
        "apprEmpId"      : getParameter(form_data,"apprEmpId"),
        "reqMemo"        : getParameter(form_data,"reqMemo"),
    }
    toNotiData = {
        "toEmpId": getParameter(form_data,"apprEmpId")
        ,"fromEmpId": session['empId']
        ,"message" : "대표 거래처 삭제 승인 신청"
    }
    fromNotiData = {
        "toEmpId": session['empId']
        ,"fromEmpId": getParameter(form_data,"apprEmpId")
        ,"message" : "대표 거래처 삭제 승인 신청"
    }
    reponseResult = request_put("/approvals/request/merchant/delete", queryData, '1')

    if "status"  in reponseResult and reponseResult["status"] == "200" :
        KpcNotification().push_user_notification(toNotiData)
        KpcNotification().push_user_notification(fromNotiData)        
    return json.dumps(reponseResult)
    
#대표 거래처 정보 조회.
@merchantApi.route("/api/merchants/representative/<merchantId>", methods=['GET'])
def getRepresentativeMerchant(merchantId):
    
    resultData = request_get("/merchants/representative/"+merchantId, None, API_SERVER_BACKOFFICE)

    return json.dumps(resultData)

@merchantApi.route("/api/merchants/represents", methods=['GET'])
def represents():
    form_data = json.loads(request.args.get("formData"))
    queryData = {
        'limit': setStringToNumber(request.args.get("length")),
        'offset': setStringToNumber(request.args.get("start")),
        'representId': getParameter(form_data,"merchantId"),
        'name': getParameter(form_data,"name"),
        'alias':getParameter(form_data,"alias"),
        'status': getParameter(form_data,"status"),
        'bizRegNo': paramEscape(getParameter(form_data,"bizRegNo")),
        
    }
    result_data = getApiData("/merchants/represents" ,queryData)
    print result_data
    return json.dumps(result_data)

@merchantApi.route("/api/merchants", methods=['GET'])
def merchants():
    form_data = json.loads(request.args.get("formData"))
    queryData = {
        'limit': setStringToNumber(request.args.get("length")),
        'offset': setStringToNumber(request.args.get("start")),
        'merchantId': getParameter(form_data,"merchantId"),
        'name': getParameter(form_data,"name"),
        'alias': getParameter(form_data,"alias"),
        'depth': getParameter(form_data,"depth"),
        'childId': getParameter(form_data,"childId"),
        'status': getParameter(form_data,"status"),
        'bizRegNo': paramEscape(getParameter(form_data,"bizRegNo")),
    }
    print queryData
    result_data = getApiData("/merchants" ,queryData)
    print result_data
    return json.dumps(result_data)

@merchantApi.route("/api/merchants/merchant/bznoCheck", methods=['GET'])
def bznoCheck():
    queryData = {
        'merchantId': getParameter({},"merchantId"),
        'bizRegNo': paramEscape(getParameter({},"bizRegNo")),
    }
    result_data = getData("/merchants/merchant/bznoCheck" ,queryData)
    return json.dumps(result_data)

@merchantApi.route("/api/merchants/merchant/svcConnIdCheck", methods=['GET'])
def svcConnIdCheck():
    queryData = {
        'svcConnId': getParameter({},"svcConnIdCheck"),
        'serviceId': "",
    }
    result_data = getData("/merchants/merchant/svcConnIdCheck" ,queryData)
    return json.dumps(result_data)

@merchantApi.route("/api/merchants/merchant/corpNoCheck", methods=['GET'])
def corpNoCheck():
    queryData = {
        'merchantId': getParameter({},"merchantId"),
        'corpRegNo': paramEscape(getParameter({},"corpRegNo")),
    }
    result_data = getData("/merchants/merchant/corpNoCheck" ,queryData)
    return json.dumps(result_data)
    

def getRepresent():
    url = request.args.get("url")
    if url is None : 
        url = "/merchants/represent?representId=" + request.args.get("merchantId")    
    result_data = getApiSingleData(url ,{})
    print result_data
    return json.dumps(result_data)


@merchantApi.route("/api/merchants/merchant", methods=['POST','GET', "PUT", "DELETE"])
def merchant():
    if (request.method == 'GET') :
        return getMerchant() 
    elif (request.method == 'POST') :
        return createSubMerchant()
    elif (request.method == 'PUT') :
        return putMerchant()
    elif (request.method == 'DELETE') :
        return deleteMerchant()

def getMerchant():
    url = request.args.get("url")
    if url is None : 
        url = "/merchants/merchant?merchantId=" + setNoneToBlank(request.args.get("merchantId"))
    result_data = getApiSingleData(url ,{})
    return json.dumps(result_data)

def createSubMerchant():
    form_data = request.json
    subMerchantData = {                                         
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
        "reqEmpId"      : session['empId'],
        "apprEmpId"     : getParameter(form_data,"apprEmpId"),
    }
        
    reponseResult = request_post("/approvals/request/sub-merchant", subMerchantData, '1')
    
    return json.dumps(reponseResult)

def putMerchant():
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
        "reqEmpId"      : session['empId'],
        "reqMemo"     : getParameter(form_data,"reqMemo"),
        "apprEmpId"     : getParameter(form_data,"apprEmpId"),
    }

    reponseResult = request_put("/approvals/request/sub-merchant", subMerchantData, '1')

    return json.dumps(reponseResult)

def deleteMerchant():
    form_data = request.json

    queryData = {
        "subMerchantId"  : getParameter(form_data,"subMerchantId"),                                                   # : String,
        "reqEmpId"       : session['empId'],
        "apprEmpId"      : getParameter(form_data,"apprEmpId"),
        "reqMemo"        : getParameter(form_data,"reqMemo"),
    }
    reponseResult = request_put("/approvals/request/sub-merchant/delete", queryData, '1')

    return json.dumps(reponseResult)    

@merchantApi.route("/api/merchants/sub-merchant/<subMerchantId>/path", methods=['GET'])
def getSubMerchantPath(subMerchantId):

    resultData = request_get("/merchants/sub-merchant/"+subMerchantId+"/path", None, API_SERVER_BACKOFFICE)

    return json.dumps(resultData)

@merchantApi.route("/api/merchants/services", methods=['GET'])
def services():
    formData = json.loads(request.args.get("formData"))
    queryData = {
        'limit': setStringToNumber(request.args.get("length")),
        'offset': setStringToNumber(request.args.get("start")),
        'merchantId': getParameter(formData, "submerchantId"),
        'name': getParameter(formData, "name"),
        'useFlag': getParameter(formData, "useFlag"),
        'serviceId': getParameter(formData, "serviceId"),
        'serviceType': getParameter(formData, "serviceType"),
        'merchantName': getParameter(formData, "merchantName"),
        'billingRegFlag': getParameter(formData, "billingRegFlag"),
        'svcConnId': getParameter(formData, "svcConnId")
    }
    result_data = getApiData("/merchants/services" ,queryData)
    return json.dumps(result_data)

@merchantApi.route("/api/merchants/billings", methods=['GET'])
def billings():
    formData = json.loads(request.args.get("formData"))
    
    serviceId = getParameter(formData, "serviceId"); 
    
    
    resultData = request_get("/sub-merchant/"+serviceId+"/billing/commision-histories", None, API_SERVER_BACKOFFICE)
    return json.dumps(resultData)

@merchantApi.route("/api/merchants/services/service", methods=['POST','GET', "PUT", "DELETE"])
def service():
    if (request.method == 'GET') :
        return getService() 
    elif (request.method == 'POST') :
        return postService()    
    elif (request.method == 'PUT') :
        return putService() 
    elif (request.method == 'DELETE') :
        return deleteService() 
        
def getService():
    url = request.args.get("url")
    if url is None : 
        url = "/merchants/services/service?serviceId=" + request.args.get("serviceId")    
    result_data = getApiSingleData(url ,{})
    print result_data
    return json.dumps(result_data)    

def postService():
    form_data = request.json
    serviceData = {
        "subMerchantId" : getParameter(form_data, "submerchantId"),
        "serviceName"   : getParameter(form_data, "serviceName"),
        "category"      : getParameter(form_data, "category"), 
        "type"   : getParameter(form_data, "type"),
        "saleDivider"   : getParameter(form_data, "saleDivider"),
        "useFlag"       : getParameter(form_data, "useFlag"), 
        "svcConnId"     : getParameter(form_data, "svcConnId"), 
        "svcConnPw"     : getParameter(form_data, "svcConnPw"),
        "agentId"       : getParameter(form_data, "agentId"),
        "agentPw"       : getParameter(form_data, "agentPw"),
        "createDesc"    : "신규등록"                ,
        "createAdmId"   : session['empId'],
        "reqEmpId"      : session['empId'],
        "apprEmpId"     : getParameter(form_data,"apprEmpId"),                      
    }
#     return json.dumps(postApiData("/merchants/services/service", postServiceData))

    reponseResult = request_post("/approvals/request/sub-merchant/service", serviceData, '1')
    
    return json.dumps(reponseResult)

def putService():
    form_data = request.json
    serviceData = {
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
        "apprEmpId"     : getParameter(form_data,"apprEmpId")                            
    }

    reponseResult = request_put("/approvals/request/sub-merchant/service", serviceData, '1')

    return json.dumps(reponseResult)

def deleteService():
    form_data = request.json

    queryData = {
        "serviceId"  : getParameter(form_data,"serviceId"),                                                   # : String,
        "reqEmpId"       : session['empId'],
        "apprEmpId"      : getParameter(form_data,"apprEmpId"),
        "reqMemo"        : getParameter(form_data,"reqMemo"),
    }
    reponseResult = request_put("/approvals/request/sub-merchant/service/delete", queryData, '1')

    return json.dumps(reponseResult)    

@merchantApi.route("/api/merchants/services/service/billing", methods=['POST','GET', "PUT", "DELETE"])
def billing():
    if (request.method == 'GET') :
        return getBilling()
    elif (request.method == 'POST') :
        return postBilling()
    elif (request.method == 'PUT') :
        return putBilling()
    elif (request.method == 'DELETE') :
        return deleteBilling()
    
def getBilling():
    result_data = getApiSingleData("/merchants/services/service/billing" ,{"serviceBillingId" : getParameter({}, "serviceBillingId")})
    print result_data
    return json.dumps(result_data)    

#서비스정산 등록
def postBilling():
    
    form_data = request.json
    billingData = {                                         
        "serviceId"        : getParameter(form_data,"serviceId"),           
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
        "apprEmpId"        : getParameter(form_data,"apprEmpId")
    }
        
    reponseResult = request_post("/approvals/request/sub-merchant/service/billing", billingData, '1')
    
    return json.dumps(reponseResult)
#     return json.dumps(postApiData("/merchants/services/service/billing", postBillingData))        

def putBilling():
    form_data = request.json
    print "aplEndDate : " + paramEscape(getParameter(form_data ,"aplEndDate"))
    billingData = {                                         
        "serviceBillingId"        : getParameter(form_data,"serviceBillingId"),           
        "commisionId"        : getParameter(form_data,"commisionId"),           
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
        "code"             : getParameter(form_data,"billingCode"),   
        "divider"          : getParameter(form_data,"billingDivider"),  
        "billingDate"      : paramEscape(getParameter(form_data,"billingDt")),  
        "billingDuration"  : getParameter(form_data,"billingDuration"),   
        "billingCommisionType"  : getParameter(form_data,"billingCommType" ),
        "merchantCommisionType" : getParameter(form_data,"merchantCommType"),  
        "merchantCommision": getParameter(form_data,"merchantCommision"),   
        "merchantTaxType"  : getParameter(form_data,"merchantTaxType"),   
        "createAdmId"      : session['empId'], 
        "reqEmpId"         : session['empId'],
        "reqMemo"     : getParameter(form_data,"reqMemo"),
        "apprEmpId"        : getParameter(form_data,"apprEmpId")
    }
#     return json.dumps(putApiData("/merchants/services/service/billing", putBillingData , {}))
    reponseResult = request_put("/approvals/request/sub-merchant/service/billing", billingData, '1')
    return json.dumps(reponseResult)

#미사용
def deleteBilling():
    queryData = {
        'billingId': setNoneToBlank(request.args.get("billingId")),
    }
    return json.dumps(deleteApiData("/merchants/services/service/billing", queryData))    

@merchantApi.route("/api/merchants/services/service/billing/commision", methods=['POST', "PUT", "DELETE"])
def billingCommision():
    
    if (request.method == 'POST') :
        return postBillingCommision()
    elif (request.method == 'PUT') :
        return putBillingCommision()
    elif (request.method == 'DELETE') :
        return deleteBilling()

def postBillingCommision():
    
    form_data = request.json
    billingData = {                                         
        "serviceBillingId"             : getParameter(form_data,"serviceBillingId"),   
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
        "apprEmpId"        : getParameter(form_data,"apprEmpId")
    }
        
    reponseResult = request_post("/approvals/request/sub-merchant/service/billing/commision", billingData, '1')
    
    return json.dumps(reponseResult)

def putBillingCommision():
    
    form_data = request.json
    billingData = {                                         
        "serviceBillingId"             : getParameter(form_data,"serviceBillingId"),
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
        "reqMemo"     : getParameter(form_data,"reqMemo"),
        "apprEmpId"        : getParameter(form_data,"apprEmpId")
    }
        
    reponseResult = request_put("/approvals/request/sub-merchant/service/billing/commision", billingData, '1')
    
    return json.dumps(reponseResult)

#서비스 정산 ID로 정산정보 조회
@merchantApi.route("/api/merchants/sub-merchant/billing/<commisionId>", methods=['GET'])
def readServieBilling(commisionId):
    resultData = request_get("/sub-merchant/billing/"+commisionId, None, API_SERVER_BACKOFFICE)
    return json.dumps(resultData)

#서비스 정산 ID로 서비스의 마지막 정산정보 조회
@merchantApi.route("/api/merchants/sub-merchant/billing/<commisionId>/<searchType>", methods=['GET'])
def readServieLastBilling(commisionId,searchType):
    resultData = request_get("/sub-merchant/billing/"+commisionId+"/"+searchType, None, API_SERVER_BACKOFFICE)
    return json.dumps(resultData)

#수수료ID로 정산정보 조회
@merchantApi.route("/api/merchants/sub-merchant/billing/commision/<commisionId>", methods=['GET'])
def readServieBillingByCommisionId(commisionId):
    resultData = request_get("/sub-merchant/billing/commision/"+commisionId, None, API_SERVER_BACKOFFICE)

    return json.dumps(resultData)

