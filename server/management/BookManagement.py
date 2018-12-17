# -*- coding=utf-8 -*-

from flask import session, request, jsonify
from server.mutex.State import State
from server.DBmanagement.BookDBmanagement import BookDBmanagement
import json


class BookManagement(object):

    @staticmethod
    def searchBook():
        try:
            reqdata = json.loads(request.data)
            keyword = reqdata['keyword']
        except:
            return jsonify({'state': State.FormErr})
        result = BookDBmanagement.getSearchBook(keyword)
        return jsonify(result)  # result 包含state

    @staticmethod
    def viewBook():
        try:
            reqdata = json.loads(request.data)
            bookid = reqdata['bookid']
        except:
            return jsonify({'state': State.FormErr})
        result = BookDBmanagement.getBookInfo(bookid)
        return jsonify(result)

    @staticmethod
    def collectBook():
        if 'userid' not in session:
            return jsonify({'state': State.NotLogin})
        try:
            reqdata = json.loads(request.data)
            userid = session['userid']
            bookid = reqdata['bookid']
        except:
            return jsonify({'state': State.FormErr})
        result = BookDBmanagement.collectBook(userid, bookid)
        return jsonify(result)

    @staticmethod
    def get_book_class():
        # 根据书籍分类来获取书籍
        try:
            reqdata = json.loads(request.data)
            bookclass = reqdata['bookclass']
            res = BookDBmanagement.get_class_books(bookclass)
            if res['state'] == State.FormErr:
                res = BookDBmanagement.get_recommand(24)
            return jsonify(res)
        except:
            return jsonify({'state': State.FormErr})
