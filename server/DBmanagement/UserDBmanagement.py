# -*- coding=utf-8 -*-

from server.data.DBContext import DBContext
from server.mutex.State import State
import time
import random

_sql_login_ = "select userid from user where phone=?;"
_sql_login = "select userid from user where phone=? and password=?;"
_sql_reg = "insert into user (userid,password,phone,idnumber,name) values (?,?,?,?,?);"


class UserDBmanagement(object):
    # 登录
    def check_login(self, phone, pwd):
        with DBContext() as con:
            if not con.exec(_sql_login_, (phone,)):
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

    def _create_userid(self):
        # 创建一个随机userid
        return "{:4d}{:8d}".format(random.randint(0, 9999), int(time.time()))


    def add_user(self, phone, pwd, idnumber, name):
        # 注册新用户
        userid = self._create_userid()
        with DBContext() as con:
            if not con.exec(_sql_reg, (userid, pwd, phone, idnumber, name)):
                return {'state': State.DBErr}
            return {'state': State.OK}
        pass
    
    def revise_info(self):
        pass
        



