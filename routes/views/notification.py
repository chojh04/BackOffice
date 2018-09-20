# -*- coding:utf-8 -*-
from flask import redirect, url_for, render_template
from flask.globals import request, session
from flask_admin import BaseView, expose

from util import navigator, common


class Notification(BaseView):

    @expose('/')
    def index(self):
        return redirect(url_for('.notiPop'))
    
    @expose('/noti/popup')
    def notiPop(self):
        self.menuItems = session['navigator']
        self.pageAuth = common.getPageAuth()
        return render_template("views/pages/notification/noti/notiPopup.html", admin_view=self)    
