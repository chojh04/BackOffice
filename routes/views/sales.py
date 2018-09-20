# -*- coding:utf-8 -*-
from flask import redirect, url_for, render_template
from flask.globals import session
from flask_admin import BaseView, expose

from util import navigator, common


class Sales(BaseView):
    @expose('/')
    def index(self):
        return redirect(url_for('.dailySales'))

    #  매출관리 > (수동) 매출 등록 > (위탁 서비스) 매출 자료 등록
    @expose("/dailySales")
    def dailySales(self):
        self.menuItems = session['navigator']
        self.pageAuth = common.getPageAuth()
        return render_template("views/pages/sales/dailySales.html", admin_view=self)

