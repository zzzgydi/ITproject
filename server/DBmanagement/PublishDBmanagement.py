# -*- coding=utf-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from server.data.DBcontext import DBContext

class PublishDBManagement:
    def __init__(self):
        pass

    def publishBook(self, bookid, name, price, detail, isbn, number, picture):
        with DBContext() as context:
            context.get_cursor().execute("INSERT INTO book VALUES (?,?,?,?,?,?,?)",
                                         (bookid, name, price, detail, isbn, number, picture))
            result = context.get_cursor().fetchone()
        if not result:
            return False
        else:
            return True
