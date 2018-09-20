# -*- coding:utf-8 -*-

from flask import redirect, url_for, render_template, session
from flask_admin import expose
from flask_admin.base import BaseView

import flask_admin as admin
from util import navigator, common


# Create customized index view class that handles login & registration
class backofficeindexview(BaseView):

    @expose('/')
    def index(self):
        # if 'username' not in session:
        #     return redirect(url_for('.login_view'))
        self.menuItems = session['navigator']
        self.pageAuth = common.getPageAuth()
        return render_template('views/pages/dashboard.html', admin_view=self)

    @expose('/login', methods=('GET', 'POST'))
    def login_view(self):

        return render_template('views/pages/login.html')

    @expose('/logout')
    def logout_view(self):
        session.clear()
        return redirect(url_for('.login_view'))
    
    @expose('/common/popup/merchants')
    def popup_merchants(self):
        return render_template('views/pages/common/popup/representMerchants.html')
    
    @expose('/common/popup/submerchants')
    def popup_submerchants(self):
        return render_template('views/pages/common/popup/subMerchants.html')
    
    @expose('/common/popup/services')
    def popup_services(self):
        return render_template('views/pages/common/popup/services.html')
    
    @expose('/common/popup/fileUpload')
    def popup_fileUpload(self):
        return render_template('views/pages/common/popup/fileUpload.html')
    
    @expose('/blank')
    def blank(self):
        return render_template('views/pages/blank.html', admin_view=self)
