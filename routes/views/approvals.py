# -*- coding:utf-8 -*-
from flask import redirect, url_for, render_template
from flask.globals import session
from flask_admin import BaseView, expose

from util import navigator, common


url = "views/pages/approvals/"

class Approvals(BaseView):
    
    @expose('/')
    def index(self):
        return redirect(url_for('.payments'))

    # 승인 내역 관리 > 결제 내역 조회 > 결제 및 결제 취소 내역
    @expose("/payments")
    def payments(self):
        self.menuItems = session['navigator']
        self.pageAuth = common.getPageAuth()
        return render_template(url + "payments.html", admin_view=self)

    # 승인 내역 관리 > 충전 내역 조회 > 충전 및 충전 취소 내역
    @expose("/chargements")
    def chargements(self):
        self.menuItems = session['navigator']
        self.pageAuth = common.getPageAuth()
        return render_template(url + "chargements.html", admin_view=self)

    # 승인 내역 관리 > 판매 내역 조회 > 판매 및 판매 취소 내역
    @expose("/salements")
    def salements(self):
        self.menuItems = session['navigator']
        self.pageAuth = common.getPageAuth()
        return render_template(url + "salements.html", admin_view=self)
