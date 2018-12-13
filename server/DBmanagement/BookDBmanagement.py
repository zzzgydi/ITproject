# -*- coding=utf-8 -*-

from server.data.DBContext import DBContext
from server.mutex.State import State
from server.mutex import Tools
import time
import random

_sql_search = "select bookid, name, price, detail, ISBN, number, picture, state, author, class from user where name=?;"
_key_book_info = ['bookid', 'name', 'price', 'detail', 'ISBN', 'number', 'picture', 'state', 'author', 'class']


class BookDBmanagement(object):

    @staticmethod
    def getSearchBook(keyword):
        #通过关键字查询书籍列表
        with DBContext() as con:
            if not con.exec(_sql_search, (keyword,)):
                return {'state': State.DBErr}
            tempList = con.get_cursor().fetchall()
            res = []

            for i in range(len(tempList)):
                res.insert(len(res), Tool.tuple2dict(_key_book_info, tempList[i]))
            return {'state': State.OK, 'booklist': res}
        pass
    pass








    @staticmethod
    def getSellerID(phone, pwd):
        # 登录
        with DBContext() as con:
            if not con.exec(_sql_phone, (phone,)):
                return {'state': State.DBErr}
            res = con.get_cursor().fetchone()
            if not res:
                return {'state': State.ActErr}
            if not con.exec(_sql_login, (phone, pwd)):
                return {'state': State.DBErr}
            res = con.get_cursor().fetchone()
            if not res:
                return {'state': State.PwdErr}
            return {'state': State.OK, 'userid': res[0]}
        pass
    pass

    @staticmethod
    def getBookInfo(phone, pwd, idnumber, name, address):
        # 注册新用户
        userid = UserDBmanagement._create_userid()
        with DBContext() as con:
            if not con.exec(_sql_phone, (phone,)):
                return {'state': State.DBErr}
            if con.get_cursor().fetchone():
                return {'state': State.RegErr}
            if not con.exec(_sql_reg, (userid, pwd, phone, idnumber, name, address)):
                return {'state': State.DBErr}
            return {'state': State.OK}
        pass

    @staticmethod
    def collectBook(userid, phone=None, pwd=None,
                    idnumber=None, name=None, address=None):
        # 修改个人信息
        val_list = []
        str_list = []
        if phone:
            str_list.append('phone=?,')
            val_list.append(phone)
        if pwd:
            str_list.append('password=?,')
            val_list.append(pwd)
        if idnumber:
            str_list.append('idnumber=?,')
            val_list.append(idnumber)
        if name:
            str_list.append('name=?,')
            val_list.append(name)
        if address:
            str_list.append('address=?,')
            val_list.append(address)
        if len(str_list) == 0:
            return {'state': State.Error}
        val_list.append(userid)
        val_tuple = tuple(val_list)
        sql_str = _sql_revise_.format(''.join(str_list)[:-1])
        with DBContext() as con:
            if phone and con.exec(_sql_phone, (phone,)):
                if con.get_cursor().fetchone():
                    return {'state': State.RegErr}
            if not con.exec(sql_str, val_tuple):
                return {'state': State.DBErr}
            return {'state': State.OK}
        pass

    @staticmethod
    def changeBookState(userid):
        # 获取用户个人的信息
        with DBContext() as con:
            if not con.exec(_sql_user_info, (userid,)):
                return {'state': State.DBErr}
            res = con.get_cursor().fetchone()
            if not res:
                return {'state': State.Error}
            res = Tools.tuple2dict(_key_user_info, res)
            if not res:
                return {'state': State.Error}
            res['state'] = State.OK
            return res
        pass
