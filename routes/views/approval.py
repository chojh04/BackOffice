# -*- coding:utf-8 -*-
from flask import redirect, url_for, render_template
from flask.globals import request, session
from flask_admin import BaseView, expose

from util import common

class Approval(BaseView):

    @expose('/')
    def index(self):
        return redirect(url_for('.kconApproval'))
    
    @expose('/<menuUrl>')
    def approvalRequestList(self, menuUrl):
        
        
        viewData = {
            'menuItems' : session['navigator'],
            'pageAuth' : common.getPageAuth()
        }
        
        if len(request.args) > 0:
            viewData["searchData"] = request.args
        else:
            viewData["searchData"] = None
    
        if menuUrl == "request":
            return render_template("views/pages/approval/approval-request-list.html", admin_view=viewData)
        elif menuUrl == "answer":
            return render_template("views/pages/approval/approval-answer-list.html", admin_view=viewData)
        else:
            return redirect(url_for("backofficeindexview.index"))
            
        
    @expose('/<menuType>/detail')
    def approvalRequestDetail(self, menuType):

        workType = request.args.get("apprWorkType");
        
        keepSearchCondition = True;       
        if request.args.get("entryPoint") is None:
            keepSearchCondition = True
        else:
            keepSearchCondition = False
                
        viewData = {
            'menuItems' : session['navigator'],
            'pageAuth' : common.getPageAuth(),
            'menuType' : menuType,
            'workType' : workType,
            'seq' : request.args.get("apprSeq"),
            'status' : request.args.get("apprStatus"),
            }
        if keepSearchCondition:
            viewData["searchData"] = request.args
        else:
            viewData["searchData"] = None
        
        #업무유형이 추가 될때마다 추가.
        if workType == "AWRK-0001" :
            return render_template("views/pages/approval/detail/approval-merchant-detail.html", admin_view=viewData)
        elif workType == "AWRK-0002":
            return render_template("views/pages/approval/detail/approval-sub-merchant-detail.html", admin_view=viewData)
        elif workType == "AWRK-0003":
            return render_template("views/pages/approval/detail/approval-sub-merchant-service-detail.html", admin_view=viewData)
        elif workType == "AWRK-0004":
            return render_template("views/pages/approval/detail/approval-service-billing-detail.html", admin_view=viewData)
        elif workType == "AWRK-0005":
            return render_template("views/pages/approval/detail/approval-coupon-charge-detail.html", admin_view=viewData)
        elif workType == "AWRK-0006":
            return render_template("views/pages/approval/detail/approval-billing-detail.html", admin_view=viewData)
        elif workType == "AWRK-0008":
            return render_template("views/pages/approval/detail/approval-service-billing-detail.html", admin_view=viewData)
        elif workType == "AWRK-0009":
            return render_template("views/pages/approval/detail/approval-kcon-brochure-detail.html", admin_view=viewData)
        elif workType == "AWRK-0010":
            return render_template("views/pages/approval/detail/approval-kcon-coupon-detail.html", admin_view=viewData)
        elif workType == "AWRK-0011":
            return render_template("views/pages/approval/detail/approval-card-balance-refund-detail.html", admin_view=viewData)
        elif workType == "AWRK-0012":
            return render_template("views/pages/approval/detail/approval-popcard-restirct-detail.html", admin_view=viewData)
        else:
            return redirect(url_for("backofficeindexview.index"))

#     @expose('/<workType>/detail/<int:seq>/<processType>')
#     def updateApprovalRequest(self, workType, seq, processType):
#         viewData = {
#             'menuItems' : session['navigator'],
#             'pageAuth' : common.getPageAuth(),
#             'seq' : seq,
#             'menuType' : 'approval',
#             'processType': processType
#             }
#         
#         #업무유형이 추가 될때마다 추가.
#         if workType == "AWRK-0001" :
#             return render_template("views/pages/merchants/represent/merchant-update.html", admin_view=viewData)
#         else:
#             return redirect(url_for("backofficeindexview.index"))
#         


# 
#     @expose('/kcon')
#     def kconApproval(self):
#         self.menuItems = session['navigator']
#         self.pageAuth = common.getPageAuth()
#         return render_template("views/pages/approval/kcon/kconApprovalMng.html", admin_view=self)
#     
#     @expose('/kcon/historyPop')
#     def kconHistoryPop(self):
#         self.menuItems = session['navigator']
#         self.pageAuth = common.getPageAuth()
#         return render_template("views/pages/approval/kcon/kconApprovalHistory.html", admin_view=self)
#         
#     @expose('/merchant/historyPop')
#     def merchantHistoryPop(self):
#         self.menuItems = session['navigator']
#         self.pageAuth = common.getPageAuth()
#         return render_template("views/pages/approval/merchantApprovalHistory.html", admin_view=self)    
# 
#     @expose('/merchant/submerchant/historyPop')
#     def subMerchantHistoryPop(self):
#         self.menuItems = session['navigator']
#         self.pageAuth = common.getPageAuth()
#         return render_template("views/pages/approval/subMerchantApprovalHistory.html", admin_view=self)
#     
#     @expose('/merchant/submerchant/service/historyPop')
#     def subMerchantServiceHistoryPop(self):
#         self.menuItems = session['navigator']
#         self.pageAuth = common.getPageAuth()
#         return render_template("views/pages/approval/serviceApprovalHistory.html", admin_view=self)    
#     
#     @expose('/merchant/submerchant/billing/historyPop')
#     def subMerchantBillingHistoryPop(self):
#         self.menuItems = session['navigator']
#         self.pageAuth = common.getPageAuth()
#         return render_template("views/pages/approval/billingApprovalHistory.html", admin_view=self)
#     
    