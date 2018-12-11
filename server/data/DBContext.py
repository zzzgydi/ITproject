# -*- coding=utf-8 -*-
'''
 * @Author: GyDi
 * @Craeted: ...
 * @Modified: 2018-11-24 18:44:56
 * @Description: 提供数据库访问的接口
'''

import os
import sqlite3

DB_PATH = "/../../database/mutex.db"    #Linux path
#DB_PATH = "\\..\\..\\database\\mutex.db" #Windows path

class DBContext():
    _current_path = os.path.dirname(__file__) + DB_PATH
    _error = False

    def __enter__(self):
        self.conn = sqlite3.connect(self._current_path)
        self.cursor = self.conn.cursor()
        return self

    def get_connection(self):
        return self.conn

    def get_cursor(self):
        return self.cursor

    def is_error(self):
        return self._error

    def exec(self, sqlstr, args=None):
        '''
        只负责执行sql语句, 返回是否执行成功
        '''
        try:
            if args:
                self.cursor.execute(sqlstr, args)
            else:
                self.cursor.execute(sqlstr)
        except Exception as e:
            print("DBContext Error: ", e)
            self._error = True
            return False
        return True

    def __exit__(self, exc_type, exc_value, traceback):
        # self.cursor.close()
        if exc_type:
            self._error = True
        else:
            self.conn.commit()
        self.conn.close()


'''
可以直接使用with来操作

with dbcontext() as dh:
    dh.get_cursor().execute(...)

'''
