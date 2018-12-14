# -*- coding=utf-8 -*-

from flask import session, request, jsonify
from server.mutex.State import State
from server.DBmanagement.BookDBmanagement import BookDBmanagement
import json


class BookManagement(object):

    @staticmethod
    def searchBook():
        if 'userid' not in session:
            return jsonify({'state': State.NotLogin})
        try:
            reqdata = json.loads(request.data)
            keyword = reqdata['keyword']
        except Exception as e:
            print('Keyword Error', e)
            return jsonify({'state': State.BookNExit})
        result = BookDBmanagement.getSearchBook(keyword)
        return jsonify(result)  # result 包含state

    @staticmethod
    def viewBook():
        if 'userid' not in session:
            return jsonify({'state': State.NotLogin})
        try:
            reqdata = json.loads(request.data)
            bookid = reqdata['bookid']
        except Exception as e:
            print('Login Error', e)
            return jsonify({'state': State.FormErr})
        result = BookDBmanagement.getBookInfo(bookid)
        return jsonify(result)

    @staticmethod
    def collectBook():
        if 'userid' not in session:
            return jsonify({'state': State.NotLogin})
        try:
            reqdata = json.loads(request.data)
            userid = reqdata['userid']
            bookid = reqdata['bookid']
        except Exception as e:
            print('Login Error', e)
            return jsonify({'state': State.FormErr})
        result = BookDBmanagement.collectBook(userid, bookid)
        return jsonify(result)
