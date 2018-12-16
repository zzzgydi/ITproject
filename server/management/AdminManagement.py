# -*- coding=utf-8 -*-

from flask import session, request, jsonify
from server.mutex.State import State
from server.DBmanagement.AdminDBmanagement import AdminDBmanagement
from server.DBmanagement.BookDBmanagement import BookDBmanagement
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
        if 'adminid' not in session:
            return jsonify({'state': State.NotLogin})
        result = AdminDBmanagement.search_unreviewed_book()
        return jsonify(result)

    @staticmethod
    def search_reviewed_book():
        # 查询已审核的书
        if 'adminid' not in session:
            return jsonify({'state': State.NotLogin})
        result = AdminDBmanagement.search_reviewed_book()
        return jsonify(result)

    @staticmethod
    def view_user():
        # 查看用户信息
        if 'adminid' not in session:
            return jsonify({'state': State.NotLogin})
        result = AdminDBmanagement.view_user()
        return jsonify(result)

    @staticmethod
    def book_audit():
        # 审核书籍
        if 'adminid' not in session:
            return jsonify({'state': State.NotLogin})
        try:
            reqdata = json.loads(request.data)
            bookid = reqdata['bookid']
            newstate = reqdata['newstate']
            adminid = session['adminid']
        except:
            return jsonify({'state': State.FormErr})
        result = BookDBmanagement.changeBookState(bookid, newstate)
        if result and result['state'] == State.OK:
            AdminDBmanagement.add_book_admin_table(bookid, adminid)
        return jsonify(result)

    @staticmethod
    def sold_out_book():
        #下架书籍
        if 'adminid' not in session:
            return jsonify({'state': State.NotLogin})
        try:
            reqdata = json.loads(request.data)
            bookid = reqdata['bookid']
        except:
            return jsonify({'state': State.FormErr})
        result = BookDBmanagement.sold_out_book(bookid)
        return jsonify(result)

    @staticmethod
    def check_order():
        #查看订单
        if 'adminid' not in session:
            return jsonify({'state': State.NotLogin})
        result = AdminDBmanagement.check_order()
        return jsonify(result)



