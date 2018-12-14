# -*- coding=utf-8 -*-
'''
@Author: GyDi
@Description:  存放图片文件的工具类
'''
import os
import uuid
import time
import random
from server.data.DBContext import DBContext

_file_folder = "database/Files/"
#_file_folder = "database\\files\\"   #Windows

_sql_save_file = '''
    insert into files
    values
    (?, ?, ?);
    '''

class FileObj(object):
    _reqfile = None

    def __init__(self, f):
        self._reqfile = f
        self._fileurl = "{}{}".format(random.randint(0,99),int(time.time()))
        self._oldfilename = f.filename
        self._filename = str(uuid.uuid4()) + '.' + self._oldfilename.rsplit('.',1)[1]

    def save_file(self):
        self._reqfile.save(os.path.join(_file_folder, self._filename))      #保存实际文件
        with DBContext() as con:                                    #保存文件索引
            return con.exec(_sql_save_file, (self._fileurl, 
                self._filename, self._oldfilename))
    pass



_sql_find_file = '''
    select filename, oldfilename from files
    where fileurl=?;
    '''
#通过fileurl去获得文件对象
def get_fileobj(fileurl):
    with DBContext() as con:
        if con.exec(_sql_find_file, (fileurl,)):
            t = con.get_cursor().fetchone()
            if t:
                return {'filename': t[0], 'oldfilename': t[1]}
        return None
    pass


