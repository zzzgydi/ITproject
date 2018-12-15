# -*- coding=utf-8 -*-

from flask import session, request, jsonify
from server.mutex.State import State
from server.DBmanagement.AdminDBmanagement import AdminDBmanagement
import json




class AdminManagement(object):
    @staticmethod
    def admin_login():
        try:
            reqdata = json.loads(request.data)
            adminid = reqdata['adminid']
            pwd = reqdata['pwd']
        except:
            return jsonify({'state': State.FormErr})
        result = AdminDBmanagement.admin_login(adminid, pwd)
        if result and result['state'] == State.OK:
            session['adminid'] = adminid
        return jsonify(result)


    @staticmethod
    def search_unreviewed_book():
        # 查询未审核的书
        result = AdminDBmanagement.search_unreviewed_book()
        return jsonify(result)



