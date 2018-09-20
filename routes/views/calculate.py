# -*- coding:utf-8 -*-
from flask import redirect, url_for, render_template
from flask.globals import session
from flask_admin import BaseView, expose

from util import navigator, common


class Calculate(BaseView):
    @expose('/')
    def index(self):
        return redirect(url_for('.popcard_detail_inq'))

    # 정산 관리 > 정산 등록 > (위탁 서비스) 정산 자료 Excel 등록
    @expose("/regist/calculate-data-excel-reg")
    def calculate_data_excel_reg(self):
        self.menuItems = session['navigator']
        self.pageAuth = common.getPageAuth()
        return render_template("views/pages/merchant/inquiry/merchant-inq.html", admin_view=self)

    # 정산 관리 > 정산 등록 > (거래처/서비스/기간별) 정산 등록 내역 조회
    @expose("/regist/calculate-regist-history-reg")
    def calculate_regist_history_reg(self):
        self.menuItems = session['navigator']
        self.pageAuth = common.getPageAuth()
        return render_template("views/pages/merchant/inquiry/merchant-inq.html", admin_view=self)

    # 정산 관리 > 정산 등록 내역 조회 > (거래처/서비스/기간별) 정산 내역 조회
    @expose("/regist/calculate-history-reg")
    def calculate_history_reg(self):
        self.menuItems = session['navigator']
        self.pageAuth = common.getPageAuth()
        return render_template("views/pages/merchant/inquiry/merchant-inq.html", admin_view=self)
