# -*- coding:utf-8 -*-
'''
Created on 2017. 3. 13.

@author: sanghyun
'''

from datetime import datetime
import hashlib
import httplib
import os
from urllib import urlencode
from urllib2 import HTTPError

from flask import json
from flask.globals import request, session

import logging

# Load loggin configuration
with open('logging.json', 'rt') as f:
    logconfig = json.load(f)
logging.config.dictConfig(logconfig)
    
# Real 
apiServerUrl = '192.168.1.134'
apiServerPort = '8090'

#real
billingServiceServerUrl = '192.168.1.134'
billingServiceServerPort = '8090'
billingServiceServerDefaultPath = '/billingService'

# Real
kpcApiServerUrl = '192.168.1.125' 
kpcApiServerPort = '8083'
kpcApiServerDefaultPath = '/KpcPaymentApiService'

# Real
kpcLegacyApiServerUrl = '192.168.1.125'
kpcLegacyApiServerPort = '8086'
kpcLegacyApiServerDefaultPath = '/KpcLegacyApiService'

#real
kconApiServerUrl = '192.168.1.125' 
kconApiServerPort = '8083'
kconApiServerDefaultPath = '/KConService'
kconID= 'r2'
kconPW= 'backoffice'

#real
smsApiServerUrl = '192.168.1.134'
smsApiServerPort = '8180'
smsApiServerDefaultPath = '/service'

#real
redisServerUrl = '192.168.1.140'
redisServerPort = '6381'
 
UPLOAD_FOLDER = "fileUpload"
API_SERVER_BACKOFFICE = '1'
API_SERVER_KPC_PAYMENT = '2'
API_SERVER_KPC_LEGACY = '3'
API_SERVER_BILLINGSERVICE = '4'
API_SERVER_KCON = '5'
API_SERVER_SMS = '6'
ALLOWED_EXTENSIONS = set(['xls', 'xlsx', 'png', 'jpg', 'jpeg', 'gif'])
EXCEL_FILE_DOWNLOAD_COUNT = 20000 
EXCEL_FILE_MAKE_LIMT_COUNT = 40000
ENV_TYPE = os.environ.get('R2_PROFILE', 'DEV')

def getEnv():
    return ENV_TYPE

def setEnv(serverType="REAL"):
    # TODO : 신규 api server url 추가시 반드시 global 추가 필수!
    global apiServerUrl      
    global apiServerPort          
    global billingServiceServerUrl
    global billingServiceServerPort
    global billingServiceServerDefaultPath 
    global kpcApiServerUrl   
    global kpcApiServerPort       
    global kpcApiServerDefaultPath
    global kpcLegacyApiServerUrl
    global kpcLegacyApiServerPort 
    global kpcLegacyApiServerDefaultPath     
    global kconApiServerUrl
    global kconApiServerPort 
    global kconApiServerDefaultPath
    global ENV_TYPE   
    global redisServerUrl
    global redisServerPort
    global smsApiServerUrl
    global smsApiServerPort
    global smsApiServerDefaultPath
    ENV_TYPE = serverType 

    if ENV_TYPE == "LOCAL" :
        apiServerUrl = 'localhost'
#         apiServerUrl = '192.168.1.124'
        apiServerPort = '8090'
        billingServiceServerUrl = 'localhost'
#         billingServiceServerUrl = '192.168.5.124'
        billingServiceServerPort = '8090'
        billingServiceServerDefaultPath = '/billingService'
        kpcApiServerUrl = '192.168.5.119'
        kpcApiServerPort = '8083'
        kpcApiServerDefaultPath = '/KpcPaymentApiService'
        kpcLegacyApiServerUrl = '192.168.5.119'
        #kpcLegacyApiServerUrl = 'localhost'
        kpcLegacyApiServerPort = '8086'
        kpcLegacyApiServerDefaultPath = '/KpcLegacyApiService'
        #kconApiServerUrl = '192.168.5.119'
        kconApiServerUrl = 'localhost'
        kconApiServerPort = '8083'
        kconApiServerDefaultPath = '/KConService'
        redisServerUrl = '192.168.5.67'
        redisServerPort = '6381'        
        smsApiServerUrl = '192.168.5.124'
        smsApiServerPort = '8180'
        smsApiServerDefaultPath = '/service'
    elif ENV_TYPE == "DEV" :
#        apiServerUrl = '192.168.5.124'
        apiServerUrl = 'localhost'
        apiServerPort = '8090'
        billingServiceServerUrl = '192.168.5.124'
#         billingServiceServerUrl = '192.168.5.124'
        billingServiceServerPort = '8090'
        billingServiceServerDefaultPath = '/billingService'
        kpcApiServerUrl = '192.168.5.119'
        kpcApiServerPort = '8083'
        kpcApiServerDefaultPath = '/KpcPaymentApiService'
        kpcLegacyApiServerUrl = '192.168.5.119'
        #kpcLegacyApiServerUrl = 'localhost'
        kpcLegacyApiServerPort = '8086'
        kpcLegacyApiServerDefaultPath = '/KpcLegacyApiService'
        kconApiServerUrl = '192.168.5.119'
        #kconApiServerUrl = 'localhost'
        kconApiServerPort = '8083'
        kconApiServerDefaultPath = '/KConService'
        redisServerUrl = '192.168.5.67'
        redisServerPort = '6381'        
        smsApiServerUrl = '192.168.5.124'
        smsApiServerPort = '8180'
        smsApiServerDefaultPath = '/service'
    
def getServerUrl(apiServerType):
    if apiServerType == API_SERVER_KPC_PAYMENT:
        return kpcApiServerUrl + ':'+ kpcApiServerPort
    elif apiServerType == API_SERVER_KPC_LEGACY:
        return kpcLegacyApiServerUrl + ':'+ kpcLegacyApiServerPort    
    elif apiServerType == API_SERVER_BILLINGSERVICE:
        return billingServiceServerUrl + ':'+ billingServiceServerPort
    elif apiServerType == API_SERVER_KCON:
        return kconApiServerUrl + ':'+ kconApiServerPort
    elif apiServerType == API_SERVER_SMS:
        return smsApiServerUrl + ':'+ smsApiServerPort
    else:
        return apiServerUrl + ':'+ apiServerPort

def getDefaultUrl(apiServerType):
    if apiServerType == API_SERVER_KPC_PAYMENT:
        return kpcApiServerDefaultPath
    elif apiServerType == API_SERVER_KPC_LEGACY:
        return kpcLegacyApiServerDefaultPath
    elif apiServerType == API_SERVER_BILLINGSERVICE:
        return billingServiceServerDefaultPath
    elif apiServerType == API_SERVER_KCON:        
        return kconApiServerDefaultPath
    elif apiServerType == API_SERVER_SMS:        
        return smsApiServerDefaultPath
    return ""

def paramEscape(param):
    if param is None :
        return ''
    else :
        return param.replace('/','').replace('-','').replace(',','') .replace(':','')

def commaReplace(param):
    if param is None :
        return ''
    else :
        return param.replace(',','')

def setNoneToBlank(param):
    if param is None :
        return ''
    return param

def setStringToNumber(param):
    if param is None  or param == '':
        return 0
    return int(param)

def setStringToLong(param):
    if param is None  or param == '':
        return 0
    return long(param)

def getData(apiUrl , queryData,apiServerType=API_SERVER_BACKOFFICE):
    url = getDefaultUrl(apiServerType) + apiUrl
    if (len(queryData) > 0) :
        url =  url  + "?" + urlencode(queryData)

    logger = logging.getLogger(__name__)
    logger.debug("api url : "+getServerUrl(apiServerType)+url)
    logger.debug("api url : "+url)

    conn = httplib.HTTPConnection(getServerUrl(apiServerType), timeout=120)
    conn.request('GET', url, "", headers={"Content-Type" : "application/json; charset=utf-8"})
    response = conn.getresponse()
    responseData = response.read()
    
    logger.debug("responseData : "+responseData)
    
    return json.loads(responseData)

def getApiData(apiUrl , queryData,apiServerType=API_SERVER_BACKOFFICE):
    url = getDefaultUrl(apiServerType) + apiUrl
    if (len(queryData) > 0) :
        url =  url  + "?" +  urlencode(queryData)
      
    logger = logging.getLogger(__name__)
    logger.debug("api url : "+url)

    conn = httplib.HTTPConnection(getServerUrl(apiServerType), timeout=120)
    conn.request('GET', url, "", headers={"Content-Type" : "application/json; charset=utf-8"})
    response = conn.getresponse()
    responseData = response.read()

    logger.debug("responseData : "+responseData)
    
    readData = json.loads(responseData)
    resultList = {}
    count = 0
    summary = {}
    if "resultList" in readData and readData["resultList"] != None:
        resultList = readData["resultList"]
    if  "list" in readData and readData["list"] != None:
        resultList = readData["list"]
    if "summary" in readData and readData["summary"] != None:
        summary = readData["summary"]
        if "count" in readData["summary"]:
            count = readData["summary"]["count"]
        elif "listTotalCount" in readData["summary"]: # kconApi
            count = readData["summary"]["listTotalCount"]
    return {
        'recordsFiltered' : count, # 페이징 처리용 total
        'recordsTotal' : count, # 페이징 처리용 total
        'data' : resultList,
        'totalData' : summary
    }
    
def getApiSingleData(apiUrl, queryData,apiServerType=API_SERVER_BACKOFFICE):

    # use logger
    logger = logging.getLogger(__name__)

    apiReadData = {
        "status" : "",
        "message" : "",
    }
    try :
        url = apiUrl
        if apiServerType != API_SERVER_BACKOFFICE : 
            url =  kpcApiServerDefaultPath + url        
        if (len(queryData) > 0) :
            url =  url  + "?" +  urlencode(queryData)
        conn = httplib.HTTPConnection(getServerUrl(apiServerType), timeout=120)
        
        logger.debug("api url : "+url)
        
        conn.request('GET', url, "", headers={"Content-Type" : "application/json; charset=utf-8"})
        response = conn.getresponse()
        readData = response.read()
        
        logger.debug("responseData : "+readData)
        
        apiReadData = json.loads(readData)
    except HTTPError as err:
        apiReadData["status"] = err.code
        errorMsg = "오류가 발생하였습니다.\n해당 메시지를 스크린 캡쳐하여 담당자에 문의 바랍니다.\n" + err.read() 
        apiReadData["message"] = errorMsg

    return apiReadData

def postApiData(apiUrl ,data ,apiServerType=API_SERVER_BACKOFFICE):

    # use logger
    logger = logging.getLogger(__name__)

    readData = {
        "status" : "",
        "message" : "",
        "data" : "",
    }
    try :
        url = getDefaultUrl(apiServerType) + apiUrl
        
        logger.debug("api url : "+url)
        logger.debug(data)
            
        conn = httplib.HTTPConnection(getServerUrl(apiServerType), timeout=120)
        conn.request('POST', url, json.dumps(data), headers={"Content-Type" : "application/json; charset=utf-8"})
        response = conn.getresponse()
        responseReadData = response.read()
        
        logger.debug("responseStatus : %s", response.status)       
        logger.debug("responseData : " + responseReadData)       
        
        apiReadData = json.loads(responseReadData)
        readData["status"] = response.status
        readData["message"] = apiReadData["message"]        
        readData["data"] = apiReadData        
    except HTTPError as err:
        readData["status"] = err.code
        errorMsg = "오류가 발생하였습니다.\n해당 메시지를 스크린 캡쳐하여 담당자에 문의 바랍니다.\n" + err.read() 
        readData["message"] = errorMsg
                
    return readData

def postListApiData(apiUrl , queryData,apiServerType=API_SERVER_BACKOFFICE):

    # use logger        
    logger = logging.getLogger(__name__)

    url = getDefaultUrl(apiServerType) + apiUrl
    if (len(queryData) > 0) :
        url =  url  + "?" +  urlencode(queryData)
    resultList = []
    count = 0
    summary = {
        "count": 0, "limit": 10, "offset": 0
    }
    try :
        logger.debug("api url : "+url)
        
        conn = httplib.HTTPConnection(getServerUrl(apiServerType), timeout=120)
        conn.request('POST', url, "", headers={"Content-Type" : "application/json; charset=utf-8"})
        response = conn.getresponse()
        responseData = response.read()
        
        logger.debug("responseData : "+responseData)
        
        readData = json.loads(responseData)
        if "resultList" in readData:
            resultList = readData["resultList"]
        if  "list" in readData and readData["list"] != None:
            resultList = readData["list"]
        if "summary" in readData and readData["summary"] != None:
            summary = readData["summary"]
            count = readData["summary"]["count"]         
    except Exception as err:
        logger.error(err)
    return {
        'recordsFiltered' : count, # 페이징 처리용 total
        'recordsTotal' : count, # 페이징 처리용 total
        'data' : resultList,
        'totalData' : summary
    }

def postData(apiUrl ,data , queryData, apiServerType=API_SERVER_BACKOFFICE):

    # use logger
    logger = logging.getLogger(__name__)

    readData = {
        "status" : "",
        "message" : "",
    }
    try :
        url = getDefaultUrl(apiServerType) + apiUrl
        if (len(queryData) > 0) :
            url =  url  + "?" + urlencode(queryData)
        
        logger.debug("getServerUrl : "+getServerUrl(apiServerType))
        logger.debug("url : "+url)
        logger.debug("api url : "+getServerUrl(apiServerType)+url)
        logger.debug(data)
        
        conn = httplib.HTTPConnection(getServerUrl(apiServerType), timeout=120)
        conn.request('POST', url, json.dumps(data), headers={"Content-Type" : "application/json; charset=utf-8"})
        response = conn.getresponse()
        
        readResponseData = response.read()
        
        logger.debug("responseStatus : %s", response.status)
        logger.debug("responseData : " + readResponseData)
        
        readData = json.loads(readResponseData)
    except HTTPError as err:
        readData["status"] = err.code
        errorMsg = "오류가 발생하였습니다.\n해당 메시지를 스크린 캡쳐하여 담당자에 문의 바랍니다.\n" + err.read() 
        readData["message"] = errorMsg
    return readData

def putApiData(apiUrl ,data , queryData,apiServerType=API_SERVER_BACKOFFICE):

    # use logger
    logger = logging.getLogger(__name__)

    readData = {
        "status" : "",
        "message" : "",
    }
    try :
        url = getDefaultUrl(apiServerType) + apiUrl
        if (len(queryData) > 0) :
            url =  url  + "?" + urlencode(queryData)
            
        logger.debug("api url : "+url)
        logger.debug(data)
            
        conn = httplib.HTTPConnection(getServerUrl(apiServerType), timeout=120)
        conn.request('PUT', url, json.dumps(data), headers={"Content-Type" : "application/json; charset=utf-8"})
        response = conn.getresponse()
        readResponseData = response.read()
        
        logger.debug("responseData : "+readResponseData)
        
        apiReadData = json.loads(readResponseData)
        readData["status"] = response.status
        readData["message"] = apiReadData["message"]        
    except HTTPError as err:
        readData["status"] = err.code
        errorMsg = "오류가 발생하였습니다.\n해당 메시지를 스크린 캡쳐하여 담당자에 문의 바랍니다.\n" + err.read() 
        readData["message"] = errorMsg
                
    return readData

def putData(apiUrl ,data , queryData,apiServerType=API_SERVER_BACKOFFICE):

    # use logger
    logger = logging.getLogger(__name__)

    readData = {
        "status" : "",
        "message" : "",
    }
    try :
        url = getDefaultUrl(apiServerType) + apiUrl      
        if (len(queryData) > 0) :
            url =  url  + "?" + urlencode(queryData)
            
        logger.debug("api url : "+url)
        logger.debug(data)
            
        conn = httplib.HTTPConnection(getServerUrl(apiServerType), timeout=120)
        conn.request('PUT', url, json.dumps(data), headers={"Content-Type" : "application/json; charset=utf-8"})
        response = conn.getresponse()
        readResponseData = response.read()
        
        logger.debug("responseData : "+readResponseData)
        
        readData = json.loads(readResponseData)
    except HTTPError as err:
        readData["status"] = err.code
        errorMsg = "오류가 발생하였습니다.\n해당 메시지를 스크린 캡쳐하여 담당자에 문의 바랍니다.\n" + err.read() 
        readData["message"] = errorMsg
                
    return readData

def deleteData(apiUrl ,data , queryData,apiServerType=API_SERVER_BACKOFFICE):

    # use logger
    logger = logging.getLogger(__name__)

    readData = {
        "status" : "",
        "message" : "",
    }
    try :
        url = getDefaultUrl(apiServerType) + apiUrl      
        if (len(queryData) > 0) :
            url =  url  + "?" + urlencode(queryData)
            
        logger.debug("api url : "+url)
        logger.debug(data)
            
        conn = httplib.HTTPConnection(getServerUrl(apiServerType), timeout=120)
        conn.request('DELETE', url, json.dumps(data), headers={"Content-Type" : "application/json; charset=utf-8"})
        response = conn.getresponse()
        readResponseData = response.read()
        
        logger.debug("responseData : "+readResponseData)
        
        readData = json.loads(readResponseData)
    except HTTPError as err:
        readData["status"] = err.code
        errorMsg = "오류가 발생하였습니다.\n해당 메시지를 스크린 캡쳐하여 담당자에 문의 바랍니다.\n" + err.read() 
        readData["message"] = errorMsg
                
    return readData

def deleteApiData(apiUrl ,queryData ,apiServerType=API_SERVER_BACKOFFICE):

    # init logger
    logger = logging.getLogger(__name__)

    readData = {                                                                                                                                                                                                                                                                                                                                                                                       
        "status" : 0,
        "message" : "",
    }

    try :
        url = getDefaultUrl(apiServerType) + apiUrl    
        url = url + "?" + urlencode(queryData)
        
        logger.debug("api url : "+url)      
        
        conn = httplib.HTTPConnection(getServerUrl(apiServerType), timeout=120)
        conn.request('DELETE', url, "", headers={"Content-Type" : "application/json; charset=utf-8"})
        response = conn.getresponse()
        responseData = response.read()
        
        logger.debug("responseStatus : %s", response.status)
        logger.debug("responseData : "+responseData)
        
        apiReadData = json.loads(responseData)
        readData["status"] = response.status
        readData["message"] = apiReadData["message"]        
    except HTTPError as err:
        logger.error(err)
        readData["status"] = err.code
        errorMsg = "오류가 발생하였습니다.\n해당 메시지를 스크린 캡쳐하여 담당자에 문의 바랍니다.\n" + err.read() 
        readData["message"] = errorMsg
    except Exception as err:
        logger.error(err)
                
    return readData

def deleteApiDataByJson(apiUrl, data,apiServerType=API_SERVER_BACKOFFICE):

    # use logger
    logger = logging.getLogger(__name__)

    readData = {                                                                                                                                                                                                                                                                                                                                                                                       
        "status" : 0,
        "message" : "",
    }
    
    try :
        url = getDefaultUrl(apiServerType) + apiUrl
        
        logger.debug("api url : "+url)     
        logger.debug(data)     
                    
        conn = httplib.HTTPConnection(getServerUrl(apiServerType), timeout=120)
        conn.request('DELETE', url, json.dumps(data), headers={"Content-Type" : "application/json; charset=utf-8"})
        response = conn.getresponse()
        responseData = response.read()
        
        logger.debug("responseStatus : %s", response.status)
        logger.debug("responseData : "+responseData)
        
        apiReadData = json.loads(responseData)
        readData["status"] = response.status
        readData["message"] = apiReadData["message"]        
    except HTTPError as err:
        logger.error(err)
        readData["status"] = err.code
        errorMsg = "오류가 발생하였습니다.\n해당 메시지를 스크린 캡쳐하여 담당자에 문의 바랍니다.\n" + err.read() 
        readData["message"] = errorMsg
    except Exception as err:
        logger.error(err)
                
    return readData


def request_get(apiUrl, queryString, apiServerType):
    """ Sends a GET request.
    :param apiUrl: 호출할 apiUrl
    :param queryString: url 쿼리 스트링
    :param apiServerType: 호출할 서버 타입
    """

    # use logger
    logger = logging.getLogger(__name__)

    readData = {
        "status" : "",
        "message" : "",
        "data" : {}
    }

    try :
        url = apiUrl
        if apiServerType != API_SERVER_BACKOFFICE : 
            url =  kpcApiServerDefaultPath + url        
        if queryString is not None :
            url =  url  + "?" +  urlencode(queryString)
        
        logger.debug("getServerUrl : "+getServerUrl(apiServerType))
        logger.debug("url : "+url)
        logger.debug("get api url : "+getServerUrl(apiServerType)+url)
        
        conn = httplib.HTTPConnection(getServerUrl(apiServerType), timeout=120)
        conn.request('GET', url, "", headers={"Content-Type" : "application/json; charset=utf-8"})

        response = conn.getresponse()
        
        responseBody = json.loads(response.read())
        
        logger.debug(responseBody)
        
        if response.status == 200:
            readData["status"] = response.status
            readData["data"] = responseBody;
        elif response.status == 500:
            readData["status"] = response.status
            readData["message"] = responseBody.get("message")

    except HTTPError as err:
        readData["status"] = err.code
        errorMsg = "통신 오류가 발생하였습니다. 담당자에게 문의 바랍니다.\n" + err.read() 
        readData["message"] = errorMsg
    return readData


def request_get_for_datatables(apiUrl, queryString, apiServerType):    
    url = getDefaultUrl(apiServerType) + apiUrl
    if (len(queryString) > 0) :
        url =  url  + "?" +  urlencode(queryString)
      
    logger = logging.getLogger(__name__)
    logger.debug("api url : "+url)

    conn = httplib.HTTPConnection(getServerUrl(apiServerType), timeout=120)
    conn.request('GET', url, "", headers={"Content-Type" : "application/json; charset=utf-8"})
    response = conn.getresponse()
    responseData = response.read()

    logger.debug("responseData : "+responseData)
    
    if response.status == 200:
        readData = json.loads(responseData)
    
        return {
            'recordsFiltered' : readData.get('count'), # 페이징 처리용 total
            'recordsTotal' : readData.get('count'), # 페이징 처리용 total
            'data' : readData.get('resultList'),
            'totalData' : {'summary' : { 'count' : readData.get('count') }}
        }
    else:
        return {
            'recordsFiltered' : 0, # 페이징 처리용 total
            'recordsTotal' : 0, # 페이징 처리용 total
            'data' : {},
            'totalData' : {'summary' : { 'count' : 0 }}
        }
        
    
    

def request_post(apiUrl, formData, apiServerType):
    """ Sends a POST request.
    :param apiUrl: 호출할 apiUrl
    :param formData: 넘겨줄 데이터dict
    :param apiServerType: 호출할 서버 타입
    """
    # use logger
    logger = logging.getLogger(__name__)

    readData = {
        "status" : "",
        "message" : "",
    }
    try :
        url = getDefaultUrl(apiServerType) + apiUrl
                
        logger.debug("getServerUrl : "+getServerUrl(apiServerType))
        logger.debug("url : "+url)
        logger.debug("post api url : "+getServerUrl(apiServerType)+url)
        logger.debug(formData)
        
        conn = httplib.HTTPConnection(getServerUrl(apiServerType), timeout=120)
        conn.request('POST', url, json.dumps(formData), headers={"Content-Type" : "application/json; charset=utf-8"})
        response = conn.getresponse()

        logger.debug("response status : "+str(response.status))
                
        if response.status == 200:
            readData["status"] = response.status
        elif response.status == 500:
            responseBody = json.loads(response.read())
            logger.debug("response message : "+responseBody.get("message"))
                
            readData["status"] = response.status
            readData["message"] = responseBody.get("message")
        

    except HTTPError as err:
        readData["status"] = err.code
        errorMsg = "통신 오류가 발생하였습니다. 담당자에게 문의 바랍니다.\n" + err.read() 
        readData["message"] = errorMsg

    return readData
    
    
def request_put(apiUrl, formData, apiServerType):
    """ Sends a PUT request.
    :param apiUrl: 호출할 apiUrl
    :param formData: 넘겨줄 데이터dict
    :param apiServerType: 호출할 서버 타입
    """
    # use logger
    logger = logging.getLogger(__name__)

    readData = {
        "status" : "",
        "message" : "",
    }
    try :
        url = getDefaultUrl(apiServerType) + apiUrl
                
        logger.debug("getServerUrl : "+getServerUrl(apiServerType))
        logger.debug("url : "+url)
        logger.debug("put api url : "+getServerUrl(apiServerType)+url)
        logger.debug(formData)
        
        conn = httplib.HTTPConnection(getServerUrl(apiServerType), timeout=120)
        conn.request('PUT', url, json.dumps(formData), headers={"Content-Type" : "application/json; charset=utf-8"})
        response = conn.getresponse()
        
        logger.debug("response status : "+str(response.status))
        
        if response.status == 200:
            readData["status"] = response.status
        elif response.status == 500:
            responseBody = json.loads(response.read())
            logger.debug("response message : "+responseBody.get("message"))
            readData["status"] = response.status
            readData["message"] = responseBody.get("message")
        

    except HTTPError as err:
        readData["status"] = err.code
        errorMsg = "통신 오류가 발생하였습니다. 담당자에게 문의 바랍니다.\n" + err.read() 
        readData["message"] = errorMsg

    return readData


def nullToZero(param):
    if param is None or param == "": 
        return 0
    else:
        return param
    
def strToLong(param):
    return long(nullToZero(paramEscape(param)))

def allower_file(filename):
    return '.' in filename and \
            filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

# jquery datatble 에서 임의로 추가한 formData json을 파싱 
# 해당 formData가 없다면 request에서 파라미터를 찾아서 return            
def getParameter(formData,paramKey):
    if paramKey in formData : 
        return setNoneToBlank(formData[paramKey])
    return setNoneToBlank(request.args.get(paramKey))

def authCheck(authJson , url , menuId=None):
    for page in session['navigator'] :
        if 'subMenu' in page:
            for subMenu in page['subMenu'] :
                if 'subMenu' in subMenu:
                    for subMenu2 in subMenu['subMenu'] :
                        parseAuthData(authJson,subMenu2,url,menuId)
                else :
                    parseAuthData(authJson,subMenu,url,menuId)

    return authJson

def parseAuthData(authJson , arr , url , menuId):
    if arr['routerLink'] == url or arr['menuId'] == menuId: 
        authJson['selFlag'] = arr['selFlag'] 
        authJson['insFlag'] = arr['insFlag'] 
        authJson['updFlag'] = arr['updFlag'] 
        authJson['delFlag'] = arr['delFlag']
        authJson['apprFlag'] = arr['apprFlag']
        session['menuId'] = arr['menuId']
    return authJson     

def getPageAuth():
    auth_check_page_list = [
        "/merchants",
        "/approvals",
        "/billing",
        "/systemMng",
        "/calculate",
        "/card",
        "/compare",
        "/coupon",
        "/sales",
        "/approval",
    ]
    authJson = {}
    thisPage = request.path
    auth_page = False
    for page in auth_check_page_list:
        if thisPage.startswith(page) :
            auth_page = True    
  
    #현재 페이지 url과 비교하여 권한이 필요한 화면이 아니라면 조회 권한 부여.
    if not auth_page :
        authJson['selFlag'] = '1' 
    else :
        menuId = None
        if len(authJson) == 0 and 'subUrlAuthList' in session :
            subUrlAuthList = session['subUrlAuthList']
            for subPage in subUrlAuthList:
                if subPage["url"] == thisPage :
                    menuId = subPage['parMenuId']
        if 'navigator' in session :
            authJson = authCheck(authJson , request.path, menuId)
            print(session['subUrlAuthList'])
    return authJson

def parseDate(dateStr,nowFormat,changeFormat):
    if setNoneToBlank(dateStr) == "" :
        return ""
    if setNoneToBlank(changeFormat) == "" :
        return dateStr
    try:       
        return datetime.strptime(dateStr,nowFormat).strftime(changeFormat)
    except:
        return ""

def sendSms(recieverPhone, message):
    queryData = {
        'recieverPhone': recieverPhone, 
        'reserveDate': datetime.today().strftime("%Y/%m/%dT%H:%M:%S"),
        "sendType" : 'SMS',
        "message" : message,
        "senderPhone" : '18993206',
    }
    return postData("/reserve/messages/message" , queryData , queryData ,API_SERVER_SMS)    
    
def encSha512(data):
    encData = ""
    if data is not None and data != "":
        hashSha = hashlib.sha512()
        hashSha.update(data)
        encData = hashSha.hexdigest()
    return encData   

    """
    getNonAuthMenuId(url) 
    현재 url별 권한 체크를 할때 menuId를 session에 저장을하는데,
    권한체크를 하지 않는 메뉴는 menuId를 가져올 수 없어서 Layout기능을 위해 하드코딩...
    서버 정보가 바뀔경우 맞춰주어야 합니다.
    추후 url이나 메뉴이름으로 메뉴정보를 가져오는 API가 필요 -민욱-
    """
def getNonAuthMenuId(url):
    return {
        "/settlementMng/gs/gsSettlementInconsistencyInq": "STL-0002",
        "/settlementMng/hm/hmSettlementInconsistencyInq": "STL-0004"
    }.get(url,"none")
    
    """
    한글 파일명이 in os.walk function 에서 깨지는것 방지하기 위해 unicode의 인코딩을 euc-kr로 지정
    paramType = fileName : str
    """
def setUnicodeEncodeTypeToEucKr(fileName):
    return unicode(fileName).encode('euc-kr')

    """
    os.walk function에서 깨진 한글파일을 압축할때 텍스트 깨지는것을 방지하기 위해
    str > unicode 변경시 euc-kr로 인코딩 지정
    paramType = fileName : str
    """
def setUnicodeFormatToEucKr(fileName):
    return unicode(str(fileName), 'euc-kr')
