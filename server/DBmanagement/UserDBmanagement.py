# -*- coding=utf-8 -*-

from server.data.DBContext import DBContext
from server.mutex.State import State
from server.mutex import Tools
import time
import random

_sql_phone = "select userid from user where phone=?;"
_sql_login = "select userid from user where phone=? and password=?;"
_sql_reg = "insert into user (userid,password,phone,idnumber,name,address) values (?,?,?,?,?,?);"
_sql_revise_ = "update user set {} where userid=?;"
_sql_user_info = "select password,address,phone,idnumber,name from user where userid=?;"
_key_user_info = ('password', 'address', 'phone', 'idnumber', 'name')
_sql_view_collect = '''
    select bookid,time,name,price,picture,state,author,class
    from user_book_collect join book using (bookid)
    where userid=?;
'''
_key_view_collect = ('bookid', 'time', 'name', 'price',
                     'picture', 'state', 'author', 'class')
_sql_collect_book = "insert into user_book_collect values (?,?,?);"
_sql_cancel_coll = "delete from user_book_collect where userid=? and bookid=?;"
_sql_user_order = "select book.bookid, book.name, book.price, book.detail, book.isbn, book.number, book.picture, book.state, book.author, book.class, user_book_publish.time from book join user_book_publish using (bookid) where user_book_publish.userid = ?;"
_key_user_order = ('bookid', 'name', 'price', 'detail', 'isbn', 'number', 'picture', 'state', 'author', 'class', 'time')


class UserDBmanagement(object):

    @staticmethod
    def check_login(phone, pwd):
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
    def _create_userid():
        # 创建一个随机userid
        return "{:4d}{:8d}".format(random.randint(0, 9999), int(time.time()))

    @staticmethod
    def add_user(phone, pwd, idnumber, name, address):
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
    def revise_info(userid, phone=None, pwd=None,
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
    def get_user_info(userid):
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
            res.pop('password')
            res['state'] = State.OK
            return res
        pass

    @staticmethod
    def get_collection(userid):
        with DBContext() as con:
            if not con.exec(_sql_view_collect, (userid,)):
                return {'state': State.DBErr}
            res = con.get_cursor().fetchall()
            if not res:
                return {'state': State.Error}
            try:
                res = Tools.list_tuple2dict(_key_view_collect, res)
            except:
                return {'state': State.Error}
            return {'state': State.OK, 'booklist': res}
        pass

    @staticmethod
    def collect_book(userid, bookid):
        with DBContext() as con:
            if not con.exec(_sql_collect_book, (userid, bookid, Tools.get_current_time())):
                return {'state': State.DBErr}
            return {'state': State.OK}
        pass

    @staticmethod
    def cancel_collect(userid, bookid):
        with DBContext() as con:
            if not con.exec(_sql_cancel_coll, (userid, bookid)):
                return {'state': State.DBErr}
            return {'state': State.OK}
        pass

    @staticmethod
    def check_publish(userid):
         #查看发布
        with DBContext() as con:
            if not con.exec(_sql_user_order, (userid,)):
                return {'state': State.DBErr}
            res = con.get_cursor().fetchall()
            if not res:
                return {'state': State.Error}
            try:
                res = Tools.list_tuple2dict(_key_user_order, res)
            except:
                return {'state': State.Error}
            return {'state': State.OK, 'bookinfo': res}
        pass