# -*- coding:utf-8 -*-
from flask import redirect, url_for, render_template
from flask.globals import session, request
from flask_admin import BaseView, expose

from util import navigator, common


class Coupon(BaseView):
    @expose('/')
    def index(self):
        return redirect(url_for('.popcard_detail_inq'))

    @expose("/charge/couponChargeMng")
    def couponChargeMng(self):
        
        couponNo = ""
        apprSeq = ""
        apprReqType = ""
        if request.args.get('couponNo') is not None:
            couponNo = request.args.get('couponNo') 
        
        
        updateApproval = "false";
        updateApprSeq = request.args.get('updateApprSeq')
        if updateApprSeq is not None:
            updateApproval = "true";
            apprSeq = updateApprSeq
            
        if request.args.get('apprReqType') is not None:
            apprReqType = request.args.get('apprReqType')
        
        viewData = {
            'menuItems' : session['navigator'],
            'pageAuth' : common.getPageAuth(),
            'couponNo' : couponNo,
            'updateApproval' : updateApproval,
            'apprSeq' : apprSeq,
            'apprReqType' : apprReqType
            }
        
        return render_template("views/pages/coupon/charge/couponChargeMng.html", admin_view=viewData)

    @expose("/charge/couponChargeUseInq")
    def couponChargeUseInq(self):
        self.menuItems = session['navigator']
        self.pageAuth = common.getPageAuth()
        return render_template("views/pages/coupon/charge/couponChargeUseInq.html", admin_view=self)
    
    @expose("/kcon/kconProductReg")
    def kconProductReg(self):
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
            'menuItems' : session['navigator'],
            'pageAuth' : common.getPageAuth(),
            'reApproval' : reAppoval,
            'updateApproval' : updateApproval,
            'apprSeq' : apprSeq
            }
        
        return render_template("views/pages/coupon/kcon/kconProductReg.html", admin_view=viewData)
    
    @expose("/kcon/kconProduct/update")
    def kconProductUpdate(self):
        
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
            'menuItems' : session['navigator'],
            'pageAuth' : common.getPageAuth(),
            'reApproval' : reAppoval,
            'updateApproval' : updateApproval,
            'apprSeq' : apprSeq,
            "productId"   : request.args.get("productId"),
            "register"    :  session['empId']
            }
        
        return render_template("views/pages/coupon/kcon/kcon-product-update.html", admin_view=viewData)
    
    @expose("/kcon/kconProductInq")
    def kconProductInq(self):
        self.menuItems = session['navigator']
        self.pageAuth = common.getPageAuth()
        return render_template("views/pages/coupon/kcon/kconProductInq.html", admin_view=self)

    @expose("/kcon/kconDetail")
    def kconDetail(self):
        
        couponNo = "";
        apprSeq = "";
        apprReqType = ""
        if request.args.get('couponNo') is not None:
            couponNo = request.args.get('couponNo') 
        
        
        updateApproval = "false";
        updateApprSeq = request.args.get('updateApprSeq')
        if updateApprSeq is not None:
            updateApproval = "true";
            apprSeq = updateApprSeq 
        
        if request.args.get('apprReqType') is not None:
            apprReqType = request.args.get('apprReqType')
        
        
        viewData = {
            'menuItems' : session['navigator'],
            'pageAuth' : common.getPageAuth(),
            'couponNo' : couponNo,
            'updateApproval' : updateApproval,
            'apprSeq' : apprSeq,
            'apprReqType' : apprReqType
            }
        return render_template("views/pages/coupon/kcon/kconDetail.html", admin_view=viewData)
        
    @expose("/kcon/kconPublishInq")
    def kconPublishInq(self):
        self.menuItems = session['navigator']
        self.pageAuth = common.getPageAuth()
        return render_template("views/pages/coupon/kcon/kconPublishInq.html", admin_view=self)    
    
    @expose("/kcon/extendDatePop")
    def extendDatePop(self):
        self.menuItems = session['navigator']
        self.pageAuth = common.getPageAuth()
        return render_template("views/pages/coupon/kcon/kconExtendDatePop.html", admin_view=self)    
    
    @expose("/kcon/restrictPop")
    def restrictPop(self):
        self.menuItems = session['navigator']
        self.pageAuth = common.getPageAuth()
        return render_template("views/pages/coupon/kcon/kconRestrictPop.html", admin_view=self)    
    
    # KCON 사용내역 조회 
    @expose("/kcon/kconBalanceMng")
    def kconBalanceMng(self):
        self.menuItems = session['navigator']
        self.pageAuth = common.getPageAuth()
        return render_template("views/pages/coupon/kcon/kconBalanceMng.html", admin_view=self)   
    
    # KCON 기간별 잔액관리 
    @expose("/kcon/kconPeriodicalBalanceMng")
    def kconPeriodicalBalanceMng(self):
        self.menuItems = session['navigator']
        self.pageAuth = common.getPageAuth()
        return render_template("views/pages/coupon/kcon/kconPeriodicalBalanceMng.html", admin_view=self)   
    
    