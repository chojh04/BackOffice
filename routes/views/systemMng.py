# -*- coding:utf-8 -*-
'''
Created on 2017. 4. 5.

@author: sanghyun
'''
from cookielib import request_path
from sys import path
from urllib2 import request_host

from flask import redirect, url_for, render_template, json
from flask.globals import request, session
from flask.wrappers import Request
from flask_admin import BaseView, expose

from util import navigator, common
from util.notification import KpcNotification


class SystemMng(BaseView):
    
    @expose('/')
    def index(self):
        return redirect(url_for('.employees'))
        
    @expose('/employees')
    def employees(self):
        self.menuItems = session['navigator']
        self.pageAuth = common.getPageAuth()
        return render_template("views/pages/systemMng/employees/employeeMngs.html", admin_view=self)
    
    @expose('/employees/employeeReg')
    def employeeReg(self):
        self.menuItems = session['navigator']
        self.pageAuth = common.getPageAuth()
        return render_template("views/pages/systemMng/employees/employeeReg.html", admin_view=self)
    
    @expose('/employees/employeeDetail')
    def employeeDetail(self):
        self.menuItems = session['navigator']
        #print common.getPageAuth()
        self.pageAuth = common.getPageAuth()
        self.employeeId = request.args.get("employeeId")     
        if request.args.get("employeeId") is None :
            self.isNew = "true"
        else :
            self.isNew = "false"               
        return render_template("views/pages/systemMng/employees/employeeDetail.html", admin_view=self)
    
    @expose('/employees/employeeUpt')
    def employeeUpt(self):
        self.menuItems = session['navigator']
        self.pageAuth = common.getPageAuth()
        self.employeeId = request.args.get("employeeId")
        self.commCodeList = session['commCodeList']     
        if request.args.get("employeeId") is None :
            self.isNew = "true" 
        else :
            self.isNew = "false"              
        return render_template("views/pages/systemMng/employees/employeeUpt.html", admin_view=self)
    
    @expose('/employees/passwordChange')
    def passwordChange(self):
        return render_template("views/pages/systemMng/employees/passwordChange.html", admin_view=self)    

    @expose('/menus/menusMng')
    def menusMng(self):
        self.menuItems = session['navigator']
        self.pageAuth = common.getPageAuth()
        return render_template("views/pages/systemMng/menus/menuMng.html", admin_view=self)

    @expose('/menus/subUrlMng')
    def subUrlMng(self):
        self.menuItems = session['navigator']
        self.pageAuth = common.getPageAuth()
        return render_template("views/pages/systemMng/menus/subUrlMng.html", admin_view=self)
    
    @expose('/menus/menuReg')
    def menuReg(self):
        self.menuItems = session['navigator']
        self.pageAuth = common.getPageAuth()
        self.menuId = request.args.get("menuId")     
        if request.args.get("menuId") is None :
            self.isNew = "true"
        else :
            self.isNew = "false"        
        return render_template("views/pages/systemMng/menus/menuReg.html", admin_view=self)
    
    @expose('/menus/userMenuMng')
    def userMenuMng(self):
        self.menuItems = session['navigator']
        self.pageAuth = common.getPageAuth()
        return render_template("views/pages/systemMng/menus/userMenuMng.html", admin_view=self)
    
    @expose('/common/commonCodeMng')
    def systemCodeMng(self):
        self.menuItems = session['navigator']
        self.pageAuth = common.getPageAuth()        
        return render_template("views/pages/systemMng/common/commonCodeMng.html", admin_view=self)
    
    @expose('/common/batchMng')
    def batchInq(self):
        self.menuItems = session['navigator']
        self.pageAuth = common.getPageAuth()        
        return render_template("views/pages/systemMng/common/batchMng.html", admin_view=self)
    
    @expose('/common/settlement')
    def fileUploadTest(self):
        self.menuItems = session['navigator']
        self.pageAuth = common.getPageAuth()        
        return render_template("views/pages/systemMng/common/settlement.html", admin_view=self)

    @expose('/test/socketTest')
    def socketTest(self):
        self.menuItems = session['navigator']
        self.pageAuth = common.getPageAuth()        
        return render_template("views/pages/systemMng/test/socket.html", admin_view=self)
                
    @expose('/test/pushTest')
    def pushTest(self):
        KpcNotification().push_user_notification()
        return render_template('views/pages/blank.html', admin_view=self)
                