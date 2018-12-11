# -*- coding=utf-8 -*-
'''
@Author: GyDi
@Date: 2018-11-25 13:34:37
@Description: 
'''

#加入以下三行是为了测试路径, 部署项目时可以删除
# import os
# import sys
# sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from backend.data.DBContext import DBContext
import backend.manager.bbtsql.gysql as gy
import backend.manager.bbtsql.usersql as usql
from backend.model.SEenum import EState

from backend.manager import Tools
from backend.data.DBContext import DBContext


def check_login(stuid, pwd):
    '''
    @msg: 检查登录, 传入学号和密码
    @return: Userid -- 学号密码匹配
             None   -- 学号密码不匹配或者没有这个学号
    '''
    result = None
    with DBContext() as context:
        context.exec(usql.sql_check_acct, (stuid, ))
        result = context.get_cursor().fetchone()
        if not result:
            return {'state': EState.ActErr}
        else:
            context.get_cursor().execute(usql.sql_check_login, (stuid, pwd))
            result = context.get_cursor().fetchone()
            if not result:
                return {'state': EState.PwdErr}
    return {
        'state': EState.OK,
        'userid': result[0],
        'departid': result[1],
        'stuid': result[2]
    }


_CONST_USER = ('userid', 'stuid', 'pwd', 'departid', 'name', 'position',
               'nickname', 'gender', 'birthday', 'email', 'qq', 'period',
               'intro', 'avatar')


def view_person_info(userid):
    '''
    @msg: 查看个人信息, 返回错误信息, 以及用户信息列表
    '''
    with DBContext() as con:
        if con.exec(usql.sql_view_pinfo, (userid, )):
            res = con.get_cursor().fetchone()
            resdict = Tools.tuple_to_dict(_CONST_USER, res)
            return {"state": EState.OK, "userinfo": resdict}
        return {"state": EState.Error}


#修改个人信息
def revise_person_info(userid, userinfo_p):
    '''
    @msg: 通过userid修改用户的其他信息
    @return: state=0, 300
    '''
    try:
        tu = (userinfo_p['nickname'], userinfo_p['gender'],
              userinfo_p['birthday'], userinfo_p['email'], userinfo_p['qq'],
              userid)
    except:
        return {"state": EState.FormErr}
    with DBContext() as con:
        if con.exec(usql.sql_revise_pinfo, tu):
            return {"state": EState.OK}
        else:
            return {"state": EState.Error}


#修改用户的 0 1 2 个信息
def revise_person_012_info(userid, key, val):
    sql_ = "update user set {}=? where userid=?;".format(key)
    print("TMPP:", sql_)
    print("Key:{}, Val:{}".format(key, val))
    with DBContext() as con:
        if con.exec(sql_, (val, userid)):
            return {"state": EState.OK}
    return {"state": EState.Error}


_CONST_MSG = ('msgid', 'type', 'applicant', 'name', 'depart', 'receiver',
              'targetdep', 'time', 'fileurl', 'content')


def view_all_msg(userid, stuid, departid):
    '''
    @msg:  查看自己发出的, 自己收到的, 自己部门收到的
    @return: state, published, received, departrev
    '''
    result = dict({"state": EState.OK})
    with DBContext() as con:
        if not con.exec(usql.sql_user_pub, (userid, )):
            return {'state': EState.DBErr}
        result['published'] = Tools.list_tuple_2dict(
            _CONST_MSG,
            con.get_cursor().fetchall())
        if not con.exec(usql.sql_user_receive, (stuid, )):  #这里改成用学号来查...
            return {'state': EState.DBErr}
        result['received'] = Tools.list_tuple_2dict(
            _CONST_MSG,
            con.get_cursor().fetchall())
        if not con.exec(usql.sql_user_depart_rev, (departid, )):
            return {'state': EState.DBErr}
        result['departrev'] = Tools.list_tuple_2dict(
            _CONST_MSG,
            con.get_cursor().fetchall())
    return result


#将type的值映射成数据表名
CONST_TYPE = ('No', 'No', 'personapy', 'personapy', 'postapy', 'ticketapy',
              'goodsapy')


#通过migid和type寻找申请的具体信息
def get_apy_by_id(msgid, type_):
    '''
    @msg: 根据msgid在数据库中查找对应'type'的数据
          如果`type=0或1或>6`, 返回错误, 这个函数不处理
          除申请信息以外的信息
    @return: 匹配该id的一条数据
    '''
    if not (isinstance(type_, int) and type_ > 1 and type_ < 7):
        return None
    with DBContext() as con:
        if con.exec(usql.sql_get_apy, (CONST_TYPE[type_], msgid)):
            return con.get_cursor().fetchone()
        return None