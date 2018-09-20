# -- coding:utf-8 --
'''
Created on 2017. 3. 13.

@author: sanghyun
'''
from datetime import datetime, timedelta
import json

from flask import Blueprint, request
from flask.globals import session

from util.common import  paramEscape, getApiData, getParameter, getData, \
    postData, setStringToLong, kconID, kconPW, API_SERVER_KCON, putData, \
    deleteData, strToLong


notificationApi = Blueprint('notificationApi', __name__)

@notificationApi.route('/api/notification/notis', methods=['GET'])
def getNotis():
    formData = json.loads(request.args.get("formData"))
    searchDate = getParameter(formData , "startDate").split(' - ')
    startDate = paramEscape(searchDate[0])
    endDate = paramEscape(searchDate[1])
    
    queryData = {
        'empId'        : session['empId'],
        'reqEmpNm'     : getParameter(formData , "reqEmpNm"),
        'notiType'     : getParameter(formData , "notiType"),
        'startDate'    : startDate,
        'endDate'      : endDate,
        'offset'       : strToLong(request.args.get("start")),
        'limit'        : strToLong(request.args.get("length")),
    }
    return json.dumps(getApiData("/noti/notis" ,queryData))

def getNotisDef():
    current = datetime.now()
    queryData = {
        'empId'        : session['empId'],
        'reqEmpNm'     : "",
        'notiType'     : "",
        'startDate'    : datetime.today().strftime("%Y%m%d"),
        'endDate'      : (current - timedelta(days=7)).strftime("%Y%m%d"),
        'offset'       : 0,
        'limit'        : 10,
    }
    return getData("/noti/notis" ,queryData)
