# -*- coding=utf-8 -*-

from server.data.DBContext import DBContext
from server.mutex.State import State
from server.mutex import Tools


class AdminDBmanagement(object):
    @staticmethod
    def admin_login(adminid, pwd):
        #管理员登录
        _sql_admin_login = "select * from admin where adminid=? and password=?;"
        with DBContext() as con:
            if not con.exec(_sql_admin_login, (adminid, pwd)):
                return {'state': State.Error}
            return {'state': State.OK}
        pass


    @staticmethod
    def admin_register():
        '''
        默认注册6个管理员
        往后暂不提供注册功能
        '''
        _sql_admin_reg = "insert into admin values (?,?);"
        _const_admin = [
            ('gydi', 'gydi'), ('jiashuo', 'jiashuo'), ('chang', 'chang'),
            ('wujie', 'wujie'), ('guangyun', 'guangyun'), ('shijie', 'shijie'),
            ('test', 'test'), ('other', 'other')
        ]
        with DBContext() as con:
            con.get_cursor().executemany(_sql_admin_reg, _const_admin)
            if con.is_error():
                return {'state': State.DBErr}
            return {'state': State.OK}
        pass

    @staticmethod
    def view_publish():
        pass

    @staticmethod
    def search_unreviewed_book():
        # 查询未审核的书
        _sql_book_state_ = "select bookid from book where state = \"待审核\""
        with DBContext as con:
