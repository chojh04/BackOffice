# -*- coding:utf-8 -*-
import hashlib
import json
from flask import Blueprint, session, request

from util import navigator
from util.common import getApiSingleData, getData, getParameter


userApi = Blueprint("userApi", __name__)

@userApi.route("/api/user/login", methods=['POST'])
def login():

    result_data = {
        "auth": False,
        "message": ""
        }
    reqData = request.get_json()
    if request.headers.getlist("X-Forward-FOR") :
        ip = request.headers.getlist("X-Forward-FOR")
    else :
        ip = request.environ.get('REMOTE_ADDR')
    param = {
             'id'  : getParameter(reqData, "id") 
            ,'pwd' : getParameter(reqData, "pwd")
            ,'loginIp' : ip
        }
    apiData = getApiSingleData("/login" ,param)
    if "empId" in apiData:
        result_data = {"auth": True,"message": ""}   
        session['empId'] = apiData['empId'] 
        session['name'] = apiData['name'] 
        session['position'] = apiData['position'] 
        session['email'] = apiData['email']
        session['phone'] = apiData['phone']
        resultData = getData('/systemMng/authMenus' , {"empId" : apiData['empId']})
        resultHighMenuList = resultData['resultHighMenuList']
        subUrlAuthList     = resultData['resultSubUrlList']
        resultCommCodeList = resultData['resultCommCodeList']
        menuItems = []
        session['navigator'] = menuItems
        for data in resultHighMenuList :
            if data['level'] == '1' :
                menuItems.append(data)
            elif data['level'] == '2' :
                subMenuArray = []
                for menu in menuItems :
                    if data['parMenuId'] == menu['menuId']:
                        if "subMenu" in menu:
                            subMenuArray = menu["subMenu"]
                        subMenuArray.append(data)
                        menu['subMenu'] = subMenuArray
            else :
                subMenuArray = []
                for highMenu in menuItems :
                    for secondMenu in highMenu["subMenu"]:
                        if data['parMenuId'] == secondMenu['menuId']:
                            if "subMenu" in secondMenu:
                                subMenuArray = secondMenu["subMenu"]
                            subMenuArray.append(data)
                            secondMenu['subMenu'] = subMenuArray
        session['navigator'] = menuItems
        session['subUrlAuthList'] = subUrlAuthList
        session['commCodeList'] = resultCommCodeList
    else :
        result_data = apiData
    return json.dumps(result_data)


@userApi.route("/api/user/passwordCheck", methods=['POST'])
def passwordCheck():

    apiData = getApiSingleData("/login" ,{"id": session["email"],  
                                          "pwd" :  getParameter(request.get_json() , "pwd"),
                                          "loginIp" : request.environ.get('REMOTE_ADDR')
                                          })
    if "empId" in apiData:
        return json.dumps({"data" : "1"})
    else :
        return json.dumps({"data" : "0"})