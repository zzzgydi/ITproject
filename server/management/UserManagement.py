# -*- coding=utf-8 -*-

from flask import session, request, jsonify
from server.mutex.State import State
from server.DBmanagement.UserDBmanagement import UserDBmanagement,AdminDBmanagement
import json


class UserManagement(object):

    @staticmethod
    def login():
        try:
            reqdata = json.loads(request.data)
            phone = reqdata['phone']
            pwd = reqdata['pwd']
        except Exception as e:
            print('Login Error', e)
            return jsonify({'state': State.FormErr})
        result = UserDBmanagement.check_login(phone, pwd)
        if result['state'] != State.OK:
            return jsonify(result)
        session['userid'] = result['userid']
        return jsonify({'state': State.OK})

    @staticmethod
    def register():
        try:
            reqdata = json.loads(request.data)
            phone = reqdata['phone']
            pwd = reqdata['pwd']
            idnumber = reqdata['idnumber']
            name = reqdata['name']
            address = reqdata['address']
        except:
            return jsonify({'state': State.FormErr})
        result = UserDBmanagement.add_user(phone, pwd, idnumber, name, address)
        return jsonify(result)

    @staticmethod
    def revise_info():
        if 'userid' not in session:
            return jsonify({'state': State.NotLogin})
        try:
            reqdata = json.loads(request.data)
            phone = (reqdata['phone'] if 'phone' in reqdata else None)
            pwd = (reqdata['pwd'] if 'pwd' in reqdata else None)
            idnumber = (reqdata['idnumber'] if 'idnumber' in reqdata else None)
            name = (reqdata['name'] if 'name' in reqdata else None)
            address = (reqdata['address'] if 'address' in reqdata else None)
        except Exception as e:
            print("User Revise Error", e)
            return jsonify({'state': State.FormErr})
        # 这一步可能会报异常？？？
        result = UserDBmanagement.revise_info(session['userid'], phone=phone, pwd=pwd,
                                              idnumber=idnumber, name=name, address=address)
        return jsonify(result)

    @staticmethod
    def get_info():
        if 'userid' not in session:
            print("session:", session)
            return jsonify({'state': State.NotLogin})
        result = UserDBmanagement.get_user_info(session['userid'])
        return jsonify(result)


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

