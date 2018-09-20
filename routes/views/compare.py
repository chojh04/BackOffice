# -*- coding:utf-8 -*-
from flask import redirect, url_for, render_template
from flask.globals import session
from flask_admin import BaseView, expose

from util import navigator, common


class Compare(BaseView):
    @expose('/')
    def index(self):
        return redirect(url_for('.payment_compare_history_inq'))

    # 대사 관리 > 결제 대사 내역 조회 > (거래처/서비스/기간별) 대사 내역 조회
    @expose("/payment-compare-history-inquiry/payment-compare-history-inq")
    def payment_compare_history_inq(self):
        self.menuItems = session['navigator']
        self.pageAuth = common.getPageAuth()
        return render_template("views/pages/merchant/inquiry/merchant-inq.html", admin_view=self)

    # 대사 관리 > 충전 대사 내역 조회 > (거래처/서비스/기간별) 충전 내역 조회
    @expose("/charge-compare-history-inquiry/charge-compare-history-inq")
    def charge_compare_history_inq(self):
        self.menuItems = session['navigator']
        self.pageAuth = common.getPageAuth()
        return render_template("views/pages/merchant/inquiry/merchant-inq.html", admin_view=self)

    # 대사 관리 > 판매 대사 내역 조회 > (거래처/서비스/기간별) 판매 내역 조회
    @expose("/sales-compare-history-inquiry/sales-compare-history-inq")
    def sales_compare_history_inq(self):
        self.menuItems = session['navigator']
        self.pageAuth = common.getPageAuth()
        return render_template("views/pages/merchant/inquiry/merchant-inq.html", admin_view=self)
