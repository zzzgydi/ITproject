# -*- coding=utf-8 -*-

from server.data.DBContext import DBContext
from server.mutex.State import State
from server.mutex import Tools
import time
import random

_book_class = ('计算机', '工程科学', '经济管理', '自然科学', '英语', '数学', '文学艺术', '政治法律', '其他')
_sql_pub_book = "insert into book values (?,?,?,?,?,?,?,?,?,?);"
_sql_pub_book2 = "insert into user_book_publish values (?,?,?);"

class PublishDBmanagement:

    @staticmethod
    def publish_book(userid, name, price, detail, isbn, number, picture, author, bookclass):
        _bookid = "B{:04d}{:10d}".format(
            random.randint(0, 9999), int(time.time()))
        if len(name) < 0:
            return {'state': State.FormErr}
        try:
            _price = float(price)
            _number = int(number)
        except:
            return {'state': State.FormErr}
        _detail = (detail if len(detail) > 0 else "无详情")
        _isbn = (isbn if len(isbn) > 0 else "无")
        _state = "待审核"
        _author = (author if len(author) > 0 else "无")
        _class = (bookclass if bookclass in _book_class else "其他")
        _time = Tools.get_current_time()
        with DBContext() as con:
            if not con.exec(_sql_pub_book, (_bookid, name, _price, _detail,
                _isbn, _number, picture, _state, _author, _class)):
                return {'state': State.DBErr}
            if not con.exec(_sql_pub_book2, (_bookid, userid, _time)):
                return {'state': State.DBErr}
            return {'state': State.OK}
        pass


