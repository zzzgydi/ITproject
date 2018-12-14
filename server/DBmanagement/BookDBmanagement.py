# -*- coding=utf-8 -*-

from server.data.DBContext import DBContext
from server.mutex.State import State
from server.mutex import Tools
import time
import random

_sql_search = "select bookid, name, price, detail, ISBN, number, picture, state, author, class from book where name like ?;"
_sql_getbook_info = "select bookid, name, price, detail, ISBN, number, picture, state, author, class from book where bookid=?;"
_sql_insert_collect = "insert into User_Book_Collect values(?, ?, ?);"
_sql_get_sellerid = "select sellerid from user_book_publish where userid=?;"
_sql_modify_state = "update book set state = ? where bookid = ?"
_key_book_info = ('bookid', 'name', 'price', 'detail', 'ISBN', 'number', 'picture', 'state', 'author', 'class')


class BookDBmanagement(object):

    @staticmethod
    def getSearchBook(keyword):
        #通过关键字查询书籍列表
        #构造模糊搜索
        fuzzy = "%" + keyword + "%"
        with DBContext() as con:
            if not con.exec(_sql_search, (fuzzy,)):
                return {'state': State.DBErr}
            tempList = con.get_cursor().fetchall()
        try:
            res = Tools.list_tuple2dict(_key_book_info, tempList)
        except:
            return {'state': State.Error}
        return {'state': State.OK, 'booklist': res}
    pass

    @staticmethod
    def getSellerID(bookid):
        with DBContext() as con:
            if not con.exec(_sql_get_sellerid, (bookid,)):
                return {'state': State.DBErr}
            res = con.get_cursor().fetchone()
            return {'state': State.OK, 'userid': res}
        pass
    pass

    @staticmethod
    def getBookInfo(bookid):
        #通过书籍id查询书籍信息
        with DBContext() as con:
            if not con.exec(_sql_getbook_info, (bookid,)):
                return {'state': State.DBErr}
            tempList = con.get_cursor().fetchone()
            if not tempList:
                return {'state': State.BookNExit}
            return {'state': State.OK, 'bookinfo': Tools.tuple2dict(_key_book_info, tempList)}
        pass
    pass

    @staticmethod
    def collectBook(userid, bookid):
        #通过关联用户和书籍进行收藏
        with DBContext() as con:
            ts = time.time()
            ts = int(ts)  # 秒级时间戳
            dt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts)) 
            if not con.exec(_sql_insert_collect, (userid, bookid, dt)):
                return {'state': State.DBErr, "sucess": False}
            return {'state': State.OK, 'sucess': True}
        pass
    pass

    @staticmethod
    def changeBookState(userid, bookid, newstate):
        with DBContext() as con:
            if not con.exec(_sql_modify_state, (newstate, bookid)):
                return {'state': State.DBErr, "sucess": False}
            return {'state': State.OK, 'sucess': True}
        pass
    pass
