# -*- coding:utf-8 -*-
'''
Created on 2017. 3. 13.

@author: sanghyun
'''

from flask import session
from flask_socketio import emit

from routes.api.notificationApi import getNotisDef

class KpcNotification():
    
    def push_user_notification(self,jsonData):
        user_room = jsonData['toEmpId']
        emit('response' , getNotisDef() , room=user_room , broadcast=True,namespace="/noti")
