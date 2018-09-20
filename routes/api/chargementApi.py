# -*- coding:utf-8 -*-
import json
import httplib
from flask import Blueprint, session, request

chargementApi = Blueprint("chargementApi", __name__)

# 임시 데이터 
chargement_data = [
    {
        "merchantId": "test1111",
        "shopCode": "testShopCode11234",
        "approvalDate": '2017-02-09 14:05:05',
        "cancelDate": '2017-02-09 14:05:05',
        "orderNo": 1111,
        "approvalNo": 11234,
        "amount": "500,000",
        "cancelAmount": "0",
        "billingAmount": "500,000",
        "status": "결제"
    },
    {
        "merchantId": "test1112",
        "shopCode": "testShopCode12223",
        "approvalDate": '2017-02-09 14:05:05',
        "cancelDate": '2017-02-09 14:05:05',
        "orderNo": 2222,
        "approvalNo": 2222,
        "amount": "500,000",
        "cancelAmount": "400,000",
        "billingAmount": "100,000",
        "status": "부분취소"
    },
    {
        "merchantId": "test1113",
        "shopCode": "testShopCode12244",
        "approvalDate": '2017-02-09 14:05:05',
        "cancelDate": '2017-02-09 14:05:05',
        "orderNo": 3333,
        "approvalNo": 3333,
        "amount": "400,000",
        "cancelAmount": "400,000",
        "billingAmount": "0",
        "status": "취소"
    },
]


@chargementApi.route("/api/chargement/history-inq", methods=['POST', 'GET'])
def history():
    # url = 'http://kpcApiServer/'
    # data = request.get_json()
    # headers = {'Content-Type' : 'application/json'}
    #
    # r = requests.post(url, data=json.dumps(data), headers=headers)
    # order_column = request.query.columns[req.query.order[0].column].data; // order 대상 컬럼
    # order_dir = req.query.order[0].dir; // order asc/desc 구분자
    # start= req.query.start;
    # end = req.query.start;
    # formData = req.query.formData;
    print(request.args.get("order[0][column]"))
    order_column = request.args.get("columns["+request.args.get("order[0][column]")+"][data]")  # order 대상 컬럼
    order_dir = request.args.get("order[0][dir]")  # order asc/desc 구분자
    start = request.args.get("start")
    end = request.args.get("length")
    form_data = json.loads(request.args.get("formData"))

    print(form_data)
    print(form_data["startDate"])
    print(form_data["endDate"])
    print(form_data["selGubun1"])
    print(form_data["selGubun2"])
    print(form_data["selGubun3"])
    print("order_column : " + order_column)
    print("order_dir : " + order_dir)
    print("start : " + start)
    print("end : " + end)
    result_data = {
        "recordsFiltered" : len(chargement_data), # 페이징 처리용 total
        "data" : chargement_data,
        "totalData" : {
            "sum" : "1,400,000",
            "cancelSum" : "800,000",
            "billingSum" : "1,400,000"
        }
    }
    return json.dumps(result_data)

@chargementApi.route("/api/chargement/cancel-history-inq", methods=['POST', 'GET'])
def cancel_history():
    # url = 'http://kpcApiServer/'
    # data = request.get_json()
    # headers = {'Content-Type' : 'application/json'}
    #
    # r = requests.post(url, data=json.dumps(data), headers=headers)
    # order_column = request.query.columns[req.query.order[0].column].data; // order 대상 컬럼
    # order_dir = req.query.order[0].dir; // order asc/desc 구분자
    # start= req.query.start;
    # end = req.query.start;
    # formData = req.query.formData;
    print(request.args.get("order[0][column]"))
    order_column = request.args.get("columns["+request.args.get("order[0][column]")+"][data]")  # order 대상 컬럼
    order_dir = request.args.get("order[0][dir]")  # order asc/desc 구분자
    start = request.args.get("start")
    end = request.args.get("length")
    form_data = json.loads(request.args.get("formData"))

    print(form_data)
    print(form_data["startDate"])
    print(form_data["endDate"])
    print(form_data["selGubun1"])
    print(form_data["selGubun2"])
    print(form_data["selGubun3"])
    print("order_column : " + order_column)
    print("order_dir : " + order_dir)
    print("start : " + start)
    print("end : " + end)
    result_data = {
        "recordsFiltered" : len(chargement_data), # 페이징 처리용 total
        "data" : chargement_data
    }
    return json.dumps(result_data)