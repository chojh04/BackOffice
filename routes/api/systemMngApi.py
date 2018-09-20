# -*- coding:utf-8 -*-
import json
import os
import threading

from flask import Blueprint, request
from flask.globals import session
from flask.helpers import send_from_directory

from util.common import paramEscape, getApiData, postApiData, getApiSingleData, \
    strToLong, deleteApiDataByJson, getParameter, getData, setStringToNumber, \
    API_SERVER_BILLINGSERVICE, postData, sendSms, getEnv
from util.common import putApiData, deleteApiData, setNoneToBlank, \
    request_get, request_post, request_put, API_SERVER_BACKOFFICE


systemMngApi = Blueprint("systemMngApi", __name__)

@systemMngApi.route("/api/systemMng/employee/passwordChange", methods=['PUT'])
def putPasswordChange():
    form_data = request.json
    putPasswordData = {
        "employeeId"   : session['empId'], #String, //직원 ID
        "beforePassword" : getParameter(form_data,"beforePassword"),
        "newPassword"    : getParameter(form_data,"newPassword"),
    }
    print putPasswordData
    return json.dumps(putApiData("/employees/employee/password", putPasswordData , {}))


@systemMngApi.route("/api/systemMng/employees", methods=['GET'])
def employeess():
    form_data = json.loads(request.args.get("formData"))
    name = ""
    divisionId = ""
    teamId = ""
    if "name" in form_data : 
        name = setNoneToBlank(form_data["name"])
    if "divisionId" in form_data : 
        divisionId = setNoneToBlank(form_data["divisionId"])
    if "teamId" in form_data : 
        teamId = setNoneToBlank(form_data["teamId"])
    queryData = {
        'limit': setStringToNumber(request.args.get("length")),
        'offset': setStringToNumber(request.args.get("start")),
        'name': name,
        'division': divisionId,
        'team': teamId,
    }
    result_data = getApiData("/employees" ,queryData)
    return json.dumps(result_data)

@systemMngApi.route("/api/systemMng/employee/auth-list", methods=['GET'])
def auths():
    form_data = ""
    if request.args.get("formData") is not None :
        form_data = json.loads(request.args.get("formData"))
    queryData = {
        'empId'     : getParameter(form_data,"empId"),
        'menuName'  : getParameter(form_data,"menuName"),
        'parMenuId' : getParameter(form_data,"parMenuId"),
    }
    resultData = request_get("/employee/auth-list", queryData, API_SERVER_BACKOFFICE)
    return json.dumps(resultData)
    
@systemMngApi.route("/api/systemMng/employees/employee", methods=['POST','GET', "PUT", "DELETE"])
def employees():
    if (request.method == 'GET') :
        return getEmployees() 
    elif (request.method == 'POST') :
        return postemployees()
    elif (request.method == 'PUT') :
        return putemployees()
    elif (request.method == 'DELETE') :
        return deleteemployees()

def postemployees():
    form_data = request.json
    postRepresentData = {
        "employeeId"   : getParameter(form_data,"employeeId"), #String, //사원번호
        "divisionId"   : getParameter(form_data,"divisionId"), #String, //부서 ID
        "teamId"       : getParameter(form_data,"teamId"    ), #String, //팀 ID 
        "name"         : getParameter(form_data,"name"      ), #String, //이름
        "password"     : getParameter(form_data , "password"), #String, 
        "position"     : getParameter(form_data,"position"), #String, //직위
        "birthDate"    : paramEscape(form_data["birthDate"]), #String, //생년월일
        "gender"       : getParameter(form_data,"gender"), #String, //성별  
        "phone"        : paramEscape(form_data["phone"]), #String, //휴대전화
        "email"        : getParameter(form_data,"email"), #String, //이메일 
        "enteringDate" : paramEscape(getParameter(form_data,"enteringDate")), #String   //입사일자
        "createId"     : session['empId'] #String   //등록자 ID
    }

    return json.dumps(postApiData("/employees/employee", postRepresentData))
    
def putemployees():
    form_data = request.json
    putRepresentData = {
        "employeeId"   : form_data["employeeId"  ], #String, //직원 ID 
        "divisionId"   : form_data["divisionId"  ], #String, //부서 ID
        "teamId"       : form_data["teamId"      ], #String, //팀 ID 
        "name"         : form_data["name"        ], #String, //이름
        "position"     : form_data["position"    ], #String, //직위
        "birthDate"    : paramEscape(form_data["birthDate"]), #String, //생년월일
        "gender"       : form_data["gender"      ], #String, //성별  
        "phone"        : paramEscape(form_data["phone"]), #String, //휴대전화
        "email"        : form_data["email"       ], #String, //이메일 
        "enteringDate" : paramEscape(form_data["enteringDate"]), #String   //입사일자
        "leaveDate"    : paramEscape(form_data["leaveDate"]), #String   //퇴사일자
        "updateId"     :session['empId'] # 수정자
    }
    result = json.dumps(putApiData("/employees/employee", putRepresentData , {}))
    sendSmsPhoneNo = getData("/employees/sendSmsPhoneNo", {"recieverId":form_data["employeeId"  ], "senderId":session['empId']})
    print getEnv()
    if "code" not in sendSmsPhoneNo:
        
        if getEnv() != "DEV" :
            recieverPhone = sendSmsPhoneNo["recieverPhone"]
            recieverName = sendSmsPhoneNo["recieverName"]
            senderPhone = sendSmsPhoneNo["senderPhone"]
            senderName = sendSmsPhoneNo["senderName"]
            managerPhone = sendSmsPhoneNo["managerPhone"]
#             if getEnv() == "DEV" : 
#                 recieverPhone = '01088966045'
#                 senderPhone = '01088966045'
#                 managerPhone = '01088966045'
                        
            smsMsg = "[R2] "+ senderName + "님이 " + recieverName + "님의 직원정보를 변경하였습니다."
            sendSms(recieverPhone , smsMsg)
            if recieverPhone != senderPhone :
                sendSms(senderPhone , smsMsg)
            if recieverPhone != managerPhone and senderPhone != managerPhone and managerPhone != None:
                sendSms(managerPhone , smsMsg)            
        
    # 문자 메시지 전송
    return result
    
def deleteemployees():
    print request.args.get("employeeId")
    
    queryData = {
        'employeeId': setNoneToBlank(request.args.get("employeeId")),
    }
    return json.dumps(deleteApiData("/employees/employee", queryData))    

def getEmployees():
    param = {
            "employeeId" : setNoneToBlank(request.args.get("employeeId")),
            "name" : setNoneToBlank(request.args.get("name")),
            "email" : setNoneToBlank(request.args.get("email")),
        }    
    result_data = getApiSingleData("/employees/employee" ,param)
    print result_data
    return json.dumps(result_data)

def getEmployee(employeeId):
    param = {
            "employeeId" : setNoneToBlank(employeeId),
            "name" : "",
            "email" : "",
        }    
    result_data = getApiSingleData("/employees/employee" ,param)
    print result_data
    return json.dumps(result_data)

@systemMngApi.route("/api/systemMng/menus", methods=['GET'])
def menus():
    form_data = ""
    if request.args.get("formData") is not None :
        form_data = json.loads(request.args.get("formData"))
    queryData = {
        'name'      : getParameter(form_data,"name"),
        'menuId'    : getParameter(form_data,"menuId"),
        'parMenuId' : getParameter(form_data,"parMenuId"),
        'selType'   : getParameter(form_data,"selType"),
    }
    print queryData
    result_data = getApiData("/systemMng/menus" ,queryData)
    return json.dumps(result_data)


@systemMngApi.route("/api/systemMng/menus/menu", methods=['POST','GET', "PUT", "DELETE"])
def menu():
    if (request.method == 'GET') :
        return getEmployees() 
    elif (request.method == 'POST') :
        return postMenu()
    elif (request.method == 'PUT') :
        return putMenu()
    elif (request.method == 'DELETE') :
        return deleteMenu()

def postMenu():
    form_data = request.json
    postRepresentData = {
        "menuId"    : form_data["menuId"    ], #String, // 메뉴 ID
        "name"      : form_data["name"      ], #String, // 메뉴 명
        "parMenuId" : form_data["parMenuId" ], #String, // 상위 메뉴 ID 
        "menuUrl"   : form_data["menuUrl"   ], #String, // 메뉴 URL 
        "createId"  : session['empId'] #String   //등록자 ID
    }

    return json.dumps(postApiData("/systemMng/menus/menu", postRepresentData))


def putMenu():
    form_data = request.json
    postRepresentData = {
        "menuId"    : form_data["menuId"    ], #String, // 메뉴 ID
        "name"      : form_data["name"      ], #String, // 메뉴 명
        "parMenuId" : form_data["parMenuId" ], #String, // 상위 메뉴 ID 
        "menuUrl"   : form_data["menuUrl"   ], #String, // 메뉴 URL 
        "updateId"  : session['empId'] #String   //등록자 ID
    }

    return json.dumps(putApiData("/systemMng/menus/menu", postRepresentData, ""))

def deleteMenu():
    form_data = request.json
    postRepresentData = {
        "menuId"    : form_data["menuId"    ], #String, // 메뉴 ID
        "name"      : form_data["name"      ], #String, // 메뉴 명
        "parMenuId" : form_data["parMenuId" ], #String, // 상위 메뉴 ID 
        "menuUrl"   : form_data["menuUrl"   ], #String, // 메뉴 URL 
        "updateId"  : session['empId'] #String   //등록자 ID
    }

    return json.dumps(deleteApiDataByJson("/systemMng/menus/menu", postRepresentData))

@systemMngApi.route("/api/systemMng/employee/auth", methods=['POST'])
def postEemployeeAuth():
    formData = request.json
    for data in formData :
        data["createId"] = session['empId']
        data["updateId"] = session['empId']
        
    resultData = request_post("/employee/auth", formData, API_SERVER_BACKOFFICE)

    return json.dumps(resultData)

@systemMngApi.route("/api/systemMng/menus/menuSubUrl", methods=['POST','GET', "PUT", "DELETE"])
def menuSubUrl():
    if (request.method == 'GET') :
        return getMenuSubUrl() 
    elif (request.method == 'POST') :
        return postMenuSubUrl()
    elif (request.method == 'PUT') :
        return putMenuSubUrl()
    elif (request.method == 'DELETE') :
        return deleteMenuSubUrl()

def postMenuSubUrl():
    data = request.json
    postRepresentData = {
        "parMenuId"  : getParameter(data , "parMenuId" ), #String, // 메뉴 ID
        "name"       : getParameter(data , "name"      ), #String, // 메뉴 명
        "url"        : getParameter(data , "url"       ), #String, // 메뉴 URL 
        "createId"   : session['empId'] #String   //등록자 ID
    }
    return json.dumps(postApiData("/systemMng/menus/menuSubUrl", postRepresentData))

def getMenuSubUrl():
    param = {
            "parMenuId" : getParameter({} ,"parMenuId"),
        }    
    result_data = getData("/systemMng/menus/menuSubUrl" ,param)
    print result_data
    return json.dumps(result_data)

def deleteMenuSubUrl():
    queryData = {
        'urlId': getParameter(request.json ,"urlId"),
    }
    return json.dumps(deleteApiData("/systemMng/menus/menuSubUrl", queryData))    

def putMenuSubUrl():
    data = request.json
    postRepresentData = {
        "urlId"      : getParameter(data,"urlId"), #String, // seq
        "url"        : getParameter(data,"url"  ), #String, // URL 
        "name"       : getParameter(data,"name" ), #String, // 화면명
        "updateId"   : session['empId'] #String   //수정자 ID
    }
    return json.dumps(putApiData("/systemMng/menus/menuSubUrl", postRepresentData, ""))

@systemMngApi.route("/api/systemMng/common/commonCodes", methods=['GET'])
def commonCodes():
    form_data = ""
    if request.args.get("formData") is not None :
        form_data = json.loads(request.args.get("formData"))
    queryData = {
        'typeCode': getParameter(form_data,"type"),
        'code': getParameter(form_data,"code"),
        'codeName': getParameter(form_data,"name")
    }
    result_data = getApiData("/systemMng/common/commonCodes" ,queryData)
    return json.dumps(result_data)

@systemMngApi.route("/api/systemMng/common/commonCodeList", methods=['GET'])
def commonCodeList():
    form_data = ""
    if request.args.get("formData") is not None :
        form_data = json.loads(request.args.get("formData"))
    typeCode = getParameter(form_data,"type").split(",")
    result_data = []
    for typeC in typeCode:
        queryData = {
            'typeCode': typeC,
            'code': getParameter(form_data,"code"),
            'codeName': getParameter(form_data,"name")
        }
        result_data.append(getData("/systemMng/common/commonCodes" ,queryData))
    return json.dumps(result_data)

@systemMngApi.route("/api/systemMng/common/typeCodes", methods=['GET'])
def typeCodes():
    queryData = {
        'typeCode': getParameter({},"typeCode"),
    }
    result_data = getData("/systemMng/common/typeCodes" ,queryData)
    return json.dumps(result_data)

@systemMngApi.route("/api/systemMng/common/commonCode", methods=['POST','GET', "DELETE"])
def commonCode():
    if (request.method == 'POST') :
        return postCommonCode()
    elif (request.method == 'DELETE') :
        return deleteCommonCode()
    
def postCommonCode():
    data = request.json
    postRepresentData = {
        "typeCode"  : getParameter(data , "typeCode" ), #String, // 메뉴 ID
        "code"      : getParameter(data , "code"     ), #String, // 메뉴 명
        "codeName"  : getParameter(data , "codeName" ), #String, // 메뉴 명
        "descText"  : getParameter(data , "descText" ), #String, // 메뉴 URL 
        "createId"  : session['empId'] #String   //등록자 ID
    }
    return json.dumps(postApiData("/systemMng/common/commonCode", postRepresentData))
    
def deleteCommonCode():
    data = request.json
    queryData = {
        "typeCode"  : getParameter(data , "typeCode" ), #String, // 메뉴 ID
        "code"      : getParameter(data , "code"     ), #String, // 메뉴 명
        "codeName"  : getParameter(data , "codeName" ), #String, // 메뉴 명
        "descText"  : getParameter(data , "descText" ), #String, // 메뉴 URL 
        "createId"  : session['empId'] #String   //등록자 ID
    }
    return json.dumps(deleteApiDataByJson("/systemMng/common/commonCode", queryData))

@systemMngApi.route("/api/systemMng/common/systemHistory", methods=["GET", "POST"])
def systemHistory():
    if (request.method == 'GET') :
        return getSystemHistory() 
    elif (request.method == 'POST') :
        return postSystemHistory() 
    
def getSystemHistory():
    queryData = {
        'menuId': getParameter({},"menuId"),
        'desc1': getParameter({},"desc1"),
        'desc3': getParameter({},"desc2"),
        'desc2': getParameter({},"desc3"),
        'start': getParameter({},"start"),
        'length': getParameter({},"length"),
    }

    return json.dumps(getApiData("/systemMng/common/systemHistory", queryData)) 

@systemMngApi.route("/api/systemMng/common/systemHistory", methods=["PUT"])
def postSystemHistory():
    data = request.json
    queryData = {
        'menuId': getParameter(data,"menuId"),
        'typeCode': getParameter(data,"typeCode"),
        'desc1': getParameter(data,"desc1"),
        'desc2': getParameter(data,"desc2"),
        'desc3': getParameter(data,"desc3"),
        "regId"  : session['empId'] #String   //등록자 ID
    }

    return json.dumps(postApiData("/systemMng/common/systemHistory", queryData)) 

@systemMngApi.route("/api/systemMng/common/batchMngs", methods=["GET"])
def batchMngs():
    form_data = json.loads(request.args.get("formData"))
    searchDate = getParameter(form_data , "startDate").split(' - ')
    startDate = paramEscape(searchDate[0])
    endDate = paramEscape(searchDate[1])    
    queryData = {
        # 관리자는 id없이 조회 하도록 할예정
        'limit': setStringToNumber(request.args.get("length")),
        'offset': setStringToNumber(request.args.get("start")),        
        'reqId': session['empId'],
        'startDate': startDate,
        'endDate': endDate,
        'status': getParameter(form_data,"status"),
    }

    return json.dumps(getApiData("/systemMng/common/batchMngs", queryData))     

def postBatchMng(queryData):
    return postApiData("/systemMng/common/batchMng", queryData)

def putBatchMng(queryData):
    return putApiData("/systemMng/common/batchMng", queryData , "")          

@systemMngApi.route("/api/systemMng/common/batchMng", methods=["GET"])
def batchMng():
    queryData = {
        "seq" : getParameter({}, "seq"),
        "reqId" : session['empId']
    }
    batchData = getData("/systemMng/common/batchMng", queryData)
    filePath = setNoneToBlank(batchData["filePath"])
    slashPosition = filePath.replace('\\', '/').rindex('/')
    folderPath = filePath[:slashPosition] 
    fileName = filePath[slashPosition + 1 :]
    return send_from_directory(directory=folderPath , filename = fileName , as_attachment = True)
     
@systemMngApi.route("/api/systemMng/common/batchMng", methods=["POST"])
def deleteBatchMng():
    formData = request.json
    seq = getParameter(formData, "seq")
    queryData = {
        "seq" : seq,
        "reqId" : session['empId']
    }
    batchData = getData("/systemMng/common/batchMng", queryData)
    filePath = setNoneToBlank(batchData["filePath"])
    print filePath
    if filePath != "" :
        if os.path.isfile(filePath):
            os.remove(filePath)
    return json.dumps(deleteApiData("/systemMng/common/batchMng", queryData))


@systemMngApi.route("/api/systemMng/common/tableColumnMng", methods=['POST'])
def postTableColumnMng():
    formData = request.json
    postRepresentData = {
        "menuId"    : getParameter(formData,"menuId"), 
        "empId"     : session['empId'], 
        "tableId"   : getParameter(formData,"tableId"), 
        "descText"  : getParameter(formData,"descText"), 
        "createId"  : session['empId']
    }
    print postRepresentData
    return json.dumps(postApiData("/systemMng/common/tableColumnMng", postRepresentData))

@systemMngApi.route("/api/systemMng/common/getTableColumnMng", methods=['POST'])
def getTableColumnMng():
    formData = request.json
    data = {
        "menuId"    : getParameter(formData,"menuId"), 
        "empId"     : session['empId'], 
        "tableId"   : getParameter(formData,"tableId") 
    }
    print data
    return json.dumps(getData("/systemMng/common/tableColumnMng", data))    
    
def postCommonSystemHistory(data):
    queryData = {
        'menuId'  : data["menuId"],
        'typeCode': data["typeCode"],
        'desc1': data["desc1"],
        'desc2': data["desc2"],
        'desc3': data["desc3"],
        "regId"  : session['empId'] #String   //등록자 ID
    }

    return json.dumps(postApiData("/systemMng/common/systemHistory", queryData))     

@systemMngApi.route("/api/systemMng/common/settlement", methods=['POST'])
def inconsistencyInq():
    form_data = request.json
    queryData = {
        "jobDivider" : getParameter(form_data,"jobDivider"),
        'settleDate': paramEscape(getParameter(form_data,"settleDate")),
    }
    jobType = getParameter(form_data,"jobType")
    t1 = threading.Thread(target=settlementJob,args=[queryData,jobType])
    t1.daemon = True
    t1.start()    
    
    return json.dumps({"message" : "성공"})     

def settlementJob(queryData,jobType):
    if jobType == "UPLOAD" :
        postData("/v1/settlement/upload", queryData , queryData ,  API_SERVER_BILLINGSERVICE)
    elif jobType == "DOWNLOAD" :
        postData("/v1/settlement/download", queryData , queryData , API_SERVER_BILLINGSERVICE)
    else :
        postData("/v1/settlement", queryData , queryData, API_SERVER_BILLINGSERVICE)    
