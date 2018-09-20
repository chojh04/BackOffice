'''
Created on 2017. 6. 12.

@author: sanghyun
'''
# -*- coding:utf-8 -*-
from flask import redirect, url_for, render_template
from flask.globals import session, request
from flask_admin import BaseView, expose

from util import navigator, common


url = "views/pages/settlementMng/"

class SettlementMng(BaseView):
    
    @expose('/')
    def index(self):
        return redirect(url_for('.gsretailInq'))    
    
    @expose("/gs/gsSettlementInq")
    def gsretailInq(self):
        self.menuItems = session['navigator']
        self.pageAuth = common.getPageAuth()
        return render_template(url + "gs/gsretailInq.html", admin_view=self)
    
    @expose("/gs/gsSettlementDetail")
    def gsSettlementDetail(self):
        self.menuItems = session['navigator']
        self.pageAuth = common.getPageAuth()
        return render_template(url + "gs/gsSettlementDetail.html", admin_view=self)
    
    @expose("/gs/gsSettlementInconsistencyInq")
    def gsSettlementInconsistencyInq(self):
        self.menuItems = session['navigator']
        self.pageAuth = common.getPageAuth()
        session['menuId'] = common.getNonAuthMenuId(request.path)
        return render_template(url + "gs/gsSettlementInconsistencyInq.html", admin_view=self)
    
    @expose("/hm/hmSettlementInq")
    def hmInq(self):
        self.menuItems = session['navigator']
        self.pageAuth = common.getPageAuth()
        return render_template(url + "hm/hmInq.html", admin_view=self)
    
    @expose("/hm/hmSettlementDetail")
    def hmSettlementDetail(self):
        self.menuItems = session['navigator']
        self.pageAuth = common.getPageAuth()
        return render_template(url + "hm/hmSettlementDetail.html", admin_view=self)
    
    @expose("/hm/hmSettlementInconsistencyInq")
    def hmSettlementInconsistencyInq(self):
        self.menuItems = session['navigator']
        self.pageAuth = common.getPageAuth()
        session['menuId'] = common.getNonAuthMenuId(request.path)
        return render_template(url + "hm/hmSettlementInconsistencyInq.html", admin_view=self)
    