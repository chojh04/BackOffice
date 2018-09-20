# -*- coding:utf-8 -*-
import os
import sys
import logging.config
import json

from urlparse import urlparse

from flask import Flask, render_template, send_from_directory, session, request
from flask_socketio import SocketIO, join_room, emit

import flask_admin as admin
from routes.api.approvalApi import approvalApi
from routes.api.approvalsApi import approvalsApi 
from routes.api.billingApi import billingApi
from routes.api.cardApi import cardApi
from routes.api.chargementApi import chargementApi
from routes.api.couponApi import couponApi
from routes.api.merchantApi import merchantApi
from routes.api.notificationApi import getNotisDef, notificationApi
from routes.api.paymentApi import paymentApi
from routes.api.salesApi import salesApi
from routes.api.settlementApi import settlementApi
from routes.api.systemMngApi import systemMngApi 
from routes.api.userApi import userApi
from routes.views.approval import Approval
from routes.views.approvals import Approvals
from routes.views.billings import Billings
from routes.views.calculate import Calculate
from routes.views.card import Card
from routes.views.compare import Compare
from routes.views.coupon import Coupon
from routes.views.merchants import Merchants
from routes.views.notification import Notification
from routes.views.sales import Sales
from routes.views.settlementMng import SettlementMng
from routes.views.systemMng import SystemMng
from routes.views.views import backofficeindexview
from util import common
from util.common import setEnv
from util.nocache import nocache
from util.redis_session import RedisSessionInterface

# Load loggin configuration
with open('logging.json', 'rt') as f:
    logconfig = json.load(f)
    
logging.config.dictConfig(logconfig)
logger = logging.getLogger(__name__)

logger.debug("Initialized logger")

# Create Flask application
app = Flask(__name__)
# route end
reload(sys)
sys.setdefaultencoding('utf-8')
# TODO : 로컬/개발 DEV 운영 REAL 
logger.info('env.profile = ' + os.environ.get('R2_PROFILE', 'LOCAL'))
setEnv(os.environ.get('R2_PROFILE', 'DEV'))

socketio=SocketIO(app)

# favicon resource
@app.route('/favicon.ico')
def send_static():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')

# bower_components
@app.route('/bower_components/<path:path>')
def send_bower(path):
    return send_from_directory(os.path.join(app.root_path, 'bower_components'), path)

@app.route('/assets/<path:path>')
@nocache
def send_assets(path):
    return send_from_directory(os.path.join(app.root_path, 'assets'), path)

# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = '123456790'

# session by redis
app.session_interface = RedisSessionInterface()

non_sign_page_list = [
    "/favicon.ico",
    "/api/user/login",
    "/backOffice/login"
]
static_page_list = [
    "/bower_components/",
    "/assets/",
]

# 비로그인 페이지 분기
@app.before_request
def login_check():
    url_path = urlparse(request.url).path
    not_static_page = True
    for static_page in static_page_list:
        if url_path.startswith(static_page):
            not_static_page = False
    if not_static_page and 'empId' not in session and url_path not in non_sign_page_list:
        return render_template("views/pages/login.html") ,401
    
@app.after_request
def after_request(response):
    return response 

# route start
# user api
app.register_blueprint(userApi)
app.register_blueprint(paymentApi)
app.register_blueprint(merchantApi)
app.register_blueprint(approvalsApi)
app.register_blueprint(chargementApi)
app.register_blueprint(billingApi)
app.register_blueprint(systemMngApi)
app.register_blueprint(couponApi)
app.register_blueprint(cardApi)
app.register_blueprint(salesApi)
app.register_blueprint(settlementApi)
app.register_blueprint(approvalApi)
app.register_blueprint(notificationApi)


# Flask views
@app.route('/')
def index():
    return backofficeindexview().index()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('views/404.html'), 404

# Create admin
# views api
admin = admin.Admin(app, 'views')
admin.add_view(backofficeindexview(name='Views', url='/backOffice'))
admin.add_view(Merchants(name='Merchant', url='/merchants'))
admin.add_view(Approvals(name='Approvals', url='/approvals'))
admin.add_view(Billings(name='Billing', url='/billing'))
admin.add_view(SystemMng(name='SystemMng', url='/systemMng'))
admin.add_view(SettlementMng(name='SettlementMng', url='/settlementMng'))
admin.add_view(Calculate(name='Calculate', url='/calculate'))
admin.add_view(Card(name='Card', url='/card'))
admin.add_view(Compare(name='Compare', url='/compare'))
admin.add_view(Coupon(name='Coupon', url='/coupon'))
admin.add_view(Sales(name='Sales', url='/sales'))
admin.add_view(Approval(name='Approval', url='/approval'))
admin.add_view(Notification(name='Notification', url='/notification'))

# @socketio.on('connect' , namespace="/chat")
# def connect_handler():
#     if 'empId' in session:
#         user_room = 'kpcNotiRoom'
#         join_room(user_room)
#         emit('response' , {'meta' : 'WS connected' , 'userName' : 'user_{}'.format(session['empId'])} , broadcast=True)

# end views api
# admin.add_view(BlankView(name='Blank', url='blank', endpoint='blank'))

if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0', port=8080, debug=True)
    logger.info("Service started...")
    #app.run(host='0.0.0.0', port=8080, debug=True)
