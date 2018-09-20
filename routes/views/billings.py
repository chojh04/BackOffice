# -*- coding:utf-8 -*-
from flask import redirect, url_for, render_template
from flask.globals import request, session
from flask_admin import BaseView, expose

from util import navigator, common


class Billings(BaseView):

    @expose('/')
    def index(self):
        return redirect(url_for('.billingHistory'))
        
    @expose('/billingHistory')
    def billingHistory(self):
        self.menuItems = session['navigator']
        self.pageAuth = common.getPageAuth()
    
        return render_template("views/pages/billings/billingHistory.html", admin_view=self)

    @expose('/billingDetail')
    def billingDetail(self):
        self.menuItems = session['navigator']
        self.pageAuth = common.getPageAuth()
        
        #예비 정산명세서 Seq
        self.billingSeq = request.args.get("billingSeq")
        
        #정산명세서 Seq
        if request.args.get("regBillingSeq") != None :
            self.regBillingSeq = request.args.get("regBillingSeq")
        elif request.args.get("regBillingSeq") == None :
            self.regBillingSeq = ""
        
        
        #승인 Seq
        if request.args.get("apprSeq") != None :
            self.apprSeq = request.args.get("apprSeq")
        elif request.args.get("apprSeq") == None :
            self.apprSeq = ""
        
        #승인Content Seq
        if request.args.get("contentSeq") != None :
            self.contentSeq = request.args.get("contentSeq")
        elif request.args.get("contentSeq") == None :
            self.contentSeq = ""
        
        return render_template("views/pages/billings/billingDetail.html", admin_view=self)

    @expose('/billings')
    def billings(self):
        self.menuItems = session['navigator']
        self.pageAuth = common.getPageAuth()
        
        return render_template("views/pages/billings/billings.html", admin_view=self)
    
    @expose('/billingsDetail')
    def billingsDetail(self):
        self.menuItems = session['navigator']
        self.pageAuth = common.getPageAuth()
        self.seq = request.args.get("seq")
        
        return render_template("views/pages/billings/billingsDetail.html", admin_view=self)
    
