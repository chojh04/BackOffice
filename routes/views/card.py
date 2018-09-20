# -*- coding:utf-8 -*-
from flask import redirect, url_for, render_template
from flask.globals import request, session
from flask_admin import BaseView, expose

from util import navigator, common


class Card(BaseView):
    @expose('/')
    def index(self):
        return redirect(url_for('.popCardMng'))

    @expose("/popCard/popCardMng")
    def popCardMng(self):
        cardNumber = request.args.get('cardNumber') if request.args.get('cardNumber')!="" and request.args.get('cardNumber')!=None else ""  
        apprSeq = request.args.get('apprSeq') if request.args.get('apprSeq')!="" and request.args.get('apprSeq')!=None else ""
        contentSeq = request.args.get('contentSeq') if request.args.get('contentSeq')!="" and request.args.get('contentSeq')!=None else ""
        
        viewData = {
            'menuItems' : session['navigator'],
            'pageAuth' : common.getPageAuth(),
            'cardNumber' : cardNumber,
            'seq' : apprSeq,
            'contentSeq' : contentSeq,
            }
        return render_template("views/pages/card/popcard/popCardMng.html", admin_view=viewData)
    
    @expose("/popCard/popCardUseMng")
    def popCardUseMng(self):
        self.menuItems = session['navigator']
        self.pageAuth = common.getPageAuth()
        return render_template("views/pages/card/popcard/popCardUseMng.html", admin_view=self)

    @expose("/popCard/balanceRefund")
    def popCardBalanceRefund(self):
        
        reAppoval = "false";
        apprSeq = "";
        reApprSeq = request.args.get('reApprSeq')
        if reApprSeq is not None:
            reAppoval = "true";
            apprSeq = reApprSeq 
            
        updateApproval = "false";
        updateApprSeq = request.args.get('updateApprSeq')
        if updateApprSeq is not None:
            updateApproval = "true";
            apprSeq = updateApprSeq 
            
        viewData = {
            'sessionName' :session['name'],
            'menuItems' : session['navigator'],
            'pageAuth' : common.getPageAuth(),
            'reApproval' : reAppoval,
            'updateApproval' : updateApproval,
            'apprSeq' : apprSeq
            }
        
        cardNumber = request.args.get('cardNumber') 
        print(type(cardNumber))
        if  cardNumber != None:
            viewData["cardNumber"] = request.args.get('cardNumber')
        else :
            viewData["cardNumber"] = ''
        return render_template("views/pages/card/popcard/popCardRefundReg.html", admin_view=viewData)
    
    @expose("/popCard/balanceRefundMng")
    def popCardBalanceRefundMng(self):
        viewData = {
            'menuItems' : session['navigator'],
            'pageAuth' : common.getPageAuth()
            }
        
        if len(request.args) > 0:
            viewData["searchData"] = request.args
        else:
            viewData["searchData"] = None
            
        return render_template("views/pages/card/popcard/popCardRefundMng.html", admin_view=viewData)
    
    @expose("/popCard/balanceRefundDetail")
    def popCardBalanceRefundDetail(self):
        viewData = {
            'menuItems' : session['navigator'],
            'pageAuth' : common.getPageAuth(),
            'seq' : request.args.get('seq')
            }
        return render_template("views/pages/card/popcard/popCardRefundDetatil.html", admin_view=viewData)
    
    
    # 카드 기간별 잔액관리 
    @expose("/popCard/popCardDailylBalanceMng")
    def kconPeriodicalBalanceMng(self):
        self.menuItems = session['navigator']
        self.pageAuth = common.getPageAuth()        
        return render_template("views/pages/card/popcard/popCardDailylBalanceMng.html", admin_view=self)   



    