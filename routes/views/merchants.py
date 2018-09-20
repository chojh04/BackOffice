# -*- coding:utf-8 -*-
from flask import redirect, url_for, render_template
from flask.globals import request, session
from flask_admin import BaseView, expose

from routes.api.systemMngApi import  getEmployee
from util import navigator, common


class Merchants(BaseView):
    @expose('/')
    def index(self):
        return redirect(url_for('.merchant_inq'))

    # 거래처 관리 > 거래처 조회 > 대표/일반 거래처 조회
    @expose("/inquiry/merchantInq")
    def merchantInq(self):
        self.menuItems = session['navigator']
        self.pageAuth = common.getPageAuth()
        return render_template("views/pages/merchants/inquiry/merchantInq.html", admin_view=self)

    # 거래처 관리 > 거래처 조회 > 서비스 별 조회
    @expose("/inquiry/merchantServiceInq")
    def merchantServiceInq(self):
        self.menuItems = session['navigator']
        self.pageAuth = common.getPageAuth()
        return render_template("views/pages/merchants/inquiry/merchantServiceInq.html", admin_view=self)

    # 거래처 관리 > (대표) 거래처 등록 > 대표 거래처 등록
    @expose("/represent/merchantReg")
    def representMerchantReg(self):
        
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
        
        return render_template("views/pages/merchants/represent/merchantReg.html", admin_view=viewData)

    # 거래처 관리 > (대표) 거래처 등록 > 대표 거래처 상세보기
    @expose("/represent/merchantDetail")
    def representMerchantDetail(self):
        self.menuItems = session['navigator']
        self.pageAuth = common.getPageAuth()
        self.merchantId = request.args.get("merchantId")
        if request.args.get("merchantId") is None :
            self.isNew = "true"
        else :
            self.isNew = "false"        
        return render_template("views/pages/merchants/represent/merchantDetail.html", admin_view=self)
    
    # 거래처 관리 > (대표) 거래처 등록 > 대표 거래처 수정
    @expose("/update")
    def representMerchantUpt(self):
        
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
            
            
        resultViewData = {
            "menuItems" : session['navigator'],
            "pageAuth" : common.getPageAuth(),
            "merchantId" : request.args.get("merchantId"),
            'reApproval' : reAppoval,
            'updateApproval' : updateApproval,
            'apprSeq' : apprSeq
        }
        
        return render_template("views/pages/merchants/represent/merchant-update.html", admin_view=resultViewData)

    # 거래처 관리 > 일반 거래처 수정
    @expose("/sub-merchant/update")
    def subMerchantUpt(self):
        
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
                       
        resultViewData = {
            "menuItems" : session['navigator'],
            "pageAuth" : common.getPageAuth(),
            "merchantId" : request.args.get("merchantId"),
            'reApproval' : reAppoval,
            'updateApproval' : updateApproval,
            'apprSeq' : apprSeq
        }
        
        return render_template("views/pages/merchants/subMerchant/merchant-update.html", admin_view=resultViewData)

    # 거래처 관리 > 거래처 서비스 > 서비스 기본 정보 수정
    @expose("/sub-merchant/service/update")
    def merchantServiceUpdate(self):
        
        isNew = ""
        reAppoval = "false";
        apprSeq = "";

        if request.args.get("serviceId") is None :
            isNew = "true"
        else :
            isNew = "false"
            
        reApprSeq = request.args.get('reApprSeq')
        if reApprSeq is not None:
            reAppoval = "true";
            apprSeq = reApprSeq 
            
        updateApproval = "false"
        updateApprSeq = request.args.get('updateApprSeq')
        
        if updateApprSeq is not None:
            updateApproval = "true";
            apprSeq = updateApprSeq 
            
        viewData = {
            'serviceId' : request.args.get("serviceId"),
            'menuItems' : session['navigator'],
            'pageAuth' : common.getPageAuth(),
            'reApproval' : reAppoval,
            'updateApproval' : updateApproval,
            'apprSeq' : apprSeq,
            'isNew' : isNew
            }      
        
        return render_template("views/pages/merchants/service/service-update.html", admin_view=viewData)
    
    # 거래처 관리 > (대표) 거래처 등록 > 등록/수정/삭제 내역 조회
    @expose("/represent/merchanthistoryInq")
    def representMerchantHistoryInq(self):
        self.menuItems = session['navigator']
        self.pageAuth = common.getPageAuth()
        return render_template("views/pages/merchants/represent/merchantHistoryInq.html", admin_view=self)

    # 거래처 관리 > 거래처 등록 > 거래처 등록
    @expose("/merchant/merchantReg")
    def merchantReg(self):
            
        isNew = ""
        reAppoval = "false";
        apprSeq = "";

        if request.args.get("merchantId") is None :
            isNew = "true"
        else :
            isNew = "false"
            
        reApprSeq = request.args.get('reApprSeq')
        if reApprSeq is not None:
            reAppoval = "true";
            apprSeq = reApprSeq 
            
        updateApproval = "false"
        updateApprSeq = request.args.get('updateApprSeq')
        
        if updateApprSeq is not None:
            updateApproval = "true";
            apprSeq = updateApprSeq 
            
        viewData = {
            'merchantId' : request.args.get("merchantId"),
            'menuItems' : session['navigator'],
            'pageAuth' : common.getPageAuth(),
            'reApproval' : reAppoval,
            'updateApproval' : updateApproval,
            'apprSeq' : apprSeq,
            'isNew' : isNew
            }
            
        return render_template("views/pages/merchants/subMerchant/merchantReg.html", admin_view=viewData)

    # 거래처 관리 > 거래처 등록 > 거래처 상세보기
    @expose("/merchant/merchantDetail")
    def merchantDetail(self):
        self.menuItems = session['navigator']
        self.pageAuth = common.getPageAuth()
        self.merchantId = request.args.get("merchantId")
        if request.args.get("merchantId") is None :
            self.isNew = "true"
        else :
            self.isNew = "false"
        return render_template("views/pages/merchants/subMerchant/merchantDetail.html", admin_view=self)

    # 거래처 관리 > 거래처 등록 > 등록/수정/삭제 내역 조회
    @expose("/merchant/merchantHistoryInq")
    def merchantHistoryInq(self):
        self.menuItems = session['navigator']
        self.pageAuth = common.getPageAuth()
        return render_template("views/pages/merchants/subMerchant/merchantHistoryInq.html", admin_view=self)

    # 거래처 관리 > 거래처 서비스 등록 > 서비스 기본 정보 등록
    @expose("/service/merchantServiceReg")
    def merchantServiceReg(self):
        
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
            'merchantId' : request.args.get("merchantId"),
            'reApproval' : reAppoval,
            'updateApproval' : updateApproval,
            'apprSeq' : apprSeq
            }
                
        return render_template("views/pages/merchants/service/merchantServiceReg.html", admin_view=viewData)

    # 거래처 관리 > 거래처 서비스 등록 > 서비스 기본 정보 수정
    @expose("/service/merchantServiceUpt")
    def merchantServiceUpt(self):
        self.menuItems = session['navigator']
        self.pageAuth = common.getPageAuth()
        self.serviceId = request.args.get("serviceId")
        if request.args.get("serviceId") is None :
            self.isNew = "true"
        else :
            self.isNew = "false"              
        return render_template("views/pages/merchants/service/merchantServiceUpt.html", admin_view=self)
    
    # 거래처 관리 > 거래처 서비스 등록 > 서비스 기본 정보 상세보기
    @expose("/service/merchantServiceDetail")
    def merchantServiceDetail(self):
        self.menuItems = session['navigator']
        self.pageAuth = common.getPageAuth()
        self.serviceId = request.args.get("serviceId")
        if request.args.get("serviceId") is None :
            self.isNew = "true"
        else :
            self.isNew = "false"         
        return render_template("views/pages/merchants/service/merchantServiceDetail.html", admin_view=self)


    # 거래처 관리 > 거래처 서비스 등록 > 서비스 정산 정보 등록
    @expose("/service/merchantBillingReg")
    def merchantBillingReg(self):
        
        isNew = ""
        reAppoval = "false";
        apprSeq = "";

        if request.args.get("serviceId") is None :
            self.isNew = "true"
        else :
            self.isNew = "false"
            
        reApprSeq = request.args.get('reApprSeq')
        if reApprSeq is not None:
            reAppoval = "true";
            apprSeq = reApprSeq 
            
        updateApproval = "false"
        updateApprSeq = request.args.get('updateApprSeq')
        
        if updateApprSeq is not None:
            updateApproval = "true";
            apprSeq = updateApprSeq 
            
        viewData = {
            'serviceId' : request.args.get("serviceId"),
            'menuItems' : session['navigator'],
            'pageAuth' : common.getPageAuth(),
            'reApproval' : reAppoval,
            'updateApproval' : updateApproval,
            'apprSeq' : apprSeq,
            'isNew' : isNew
            }
        
        return render_template("views/pages/merchants/service/merchantBillingReg.html", admin_view=viewData)

    # 거래처 관리 > 거래처 서비스 등록 > 서비스 정산 정보 수정
#     @expose("/service/merchantBillingUpt")
#     def merchantBillingServiceUpt(self):
#         self.menuItems = session['navigator']
#         self.pageAuth = common.getPageAuth()
#         self.billingId = request.args.get("billingId")
#         if request.args.get("billingId") is None :
#             self.isNew = "true"
#         else :
#             self.isNew = "false"                       
#         return render_template("views/pages/merchants/service/merchantBillingUpt.html", admin_view=self)
    
    # 거래처 관리 > 거래처 서비스 등록 > 서비스 정산 정보 상세보기
    @expose("/service/merchantBillingDetail")
    def merchantBillingServiceDetail(self):
        self.menuItems = session['navigator']
        self.pageAuth = common.getPageAuth()
        self.billingId = request.args.get("billingId")
        if request.args.get("billingId") is None :
            self.isNew = "true"
        else :
            self.isNew = "false"                     
        return render_template("views/pages/merchants/service/merchantBillingDetail.html", admin_view=self)
    
    # 거래처 관리 > 거래처 서비스 > 서비스 정산 정보 수정
    @expose("/sub-merchant/service/billing/update")
    def merchantBillingUpdate(self):

        reAppoval = "false";
        apprSeq = "";
        updateType = ""
        targetId = ""
        if request.args.get("updateType") is None :
            updateType = "billing"
            targetId = request.args.get("serviceBillingId")
        else :
            updateType = "commision"
            targetId = request.args.get("commisionId")
        
        reApprSeq = request.args.get('reApprSeq')
        if reApprSeq is not None:
            reAppoval = "true";
            apprSeq = reApprSeq 
            
        updateApproval = "false";
        updateApprSeq = request.args.get('updateApprSeq')
        if updateApprSeq is not None:
            updateApproval = "true";
            apprSeq = updateApprSeq 
                       
        resultViewData = {
            "menuItems" : session['navigator'],
            "pageAuth" : common.getPageAuth(),
            "targetId" : targetId,
            'reApproval' : reAppoval,
            'updateApproval' : updateApproval,
            'apprSeq' : apprSeq,
            "updateType" : updateType
        }

        return render_template("views/pages/merchants/service/billing-update.html", admin_view=resultViewData)
    
    # 거래처 관리 > 거래처 서비스 > 서비스 정산 수수료 정보 수정
    @expose("/sub-merchant/service/billing/commision/update")
    def merchantBillingCommisionUpdate(self):

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
        
        resultViewData = {
            "menuItems" : session['navigator'],
            "pageAuth" : common.getPageAuth(),
            "serviceId" : request.args.get("serviceId"),
            "serviceBillingId" : request.args.get("serviceBillingId"),
            'reApproval' : reAppoval,
            'updateApproval' : updateApproval,
            'apprSeq' : apprSeq,
            'actionType' : request.args.get("actionType"),
            'lastData' : request.args.get("lastData")
        }

        return render_template("views/pages/merchants/service/billing-commision-update.html", admin_view=resultViewData)
    
    
    # 거래처 관리 > 거래처 서비스 등록 > 등록/수정/삭제 내역 조회
    @expose("/service/merchant-service-history-inq")
    def merchant_service_history_inq(self):
        self.menuItems = session['navigator']
        self.pageAuth = common.getPageAuth()
        return render_template("views/pages/merchants/service/merchant-history-inq.html", admin_view=self)
