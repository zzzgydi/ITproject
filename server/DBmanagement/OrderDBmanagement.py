# -*- coding=utf-8 -*-
import time
from server.mutex import Tools
from server.mutex.State import State
from server.data.DBContext import DBContext
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

_const_key_view_orders = ('bookid', 'orderid', 'time', 'total', 'state',
                          'name', 'picture', 'author', 'class', 'phone')


class OrderDBmanagement(object):
    @staticmethod
    def addNewOrder(buyerid, bookid, number):
        ts = time.time()
        ts = int(ts)  # 秒级时间戳
        dt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))
        orderid = buyerid + 'A' + str(ts)
        state = "未完成"
        with DBContext() as context:
            if not context.exec("SELECT price from book where bookid=?", (bookid, )):
                return {'state': State.DBErr}
            result = context.get_cursor().fetchone()
            if not result:
                return {'state': State.NoBookErr}
            result = result[0]
            total = result
            if not context.exec("INSERT INTO orders values(?,?,?,?,?,?)", (bookid, orderid, dt, number, total, state)):
                return {'state': State.DBErr}
            if not context.exec("SELECT userid from user_book_publish where bookid=?", (bookid, )):
                return {'state': State.DBErr}
            result = context.get_cursor().fetchone()
            if not result:
                return {'state': State.NoBookErr}
            result = result[0]
            if not context.exec("INSERT INTO user_order values(?,?,?,?)", (bookid, orderid, buyerid, result)):
                return {'state': State.DBErr}
        return {'orderid': orderid, 'state': State.OK}

    # @staticmethod
    # def viewOrders(userid, buyerornot):
    #     orderidlist = ""
    #     timelist = ""
    #     bookstatelist = ""
    #     namelist = ""
    #     with DBContext() as context:
    #         if buyerornot == "True":
    #             if not context.exec("SELECT orderid from user_order where buyerid=? ", (userid, )):
    #                 return {'state': State.DBErr}
    #             result = context.get_cursor().fetchall()
    #             if not result:
    #                 return {'state': State.OUErr}
    #         else:
    #             if not context.exec("SELECT orderid from user_order where sellerid=? ", (userid, )):
    #                 return {'state': State.DBErr}
    #             result = context.get_cursor().fetchall()
    #             if not result:
    #                 return {'state': State.OUErr}
    #         for i in range(len(result)):
    #             if not context.exec("SELECT * from orders where orderid=? ", (result[i][0],)):
    #                 return {'state': State.DBErr}
    #             orderdetail = context.get_cursor().fetchone()
    #             if not orderdetail:
    #                 return {'state': State.NoOrderErr}
    #             bookid = orderdetail[0]
    #             time = orderdetail[2]
    #             state = orderdetail[5]
    #             if not context.exec("SELECT name from book where bookid=? ", (bookid,)):
    #                 return {'state': State.DBErr}
    #             bookname = context.get_cursor().fetchone()[0]
    #             if not bookname:
    #                 return {'state': State.NoBookErr}
    #             orderidlist = orderidlist + result[i][0] + ",,,"
    #             timelist = timelist + time + ",,,"
    #             bookstatelist = bookstatelist + state + ",,,"
    #             namelist = namelist + bookname + ",,,"
    #     return {'state': State.OK, 'orderid': orderidlist, 'time': timelist, 'bookstate': bookstatelist, 'name': namelist}

    @staticmethod
    def view_orders(userid, buyerornot):
        _sql_view_template = '''
            select bookid,orderid,time,total,orders.state,name,picture,author,class
            from orders join user_order using (bookid,orderid) join book using (bookid) 
            where {}=?;
        '''
        _sql = _sql_view_template.format(
            ('buyerid' if buyerornot == 'True' else 'sellerid'))
        with DBContext() as con:
            if not con.exec(_sql, (userid)):
                return {'state': State.DBErr}
            result = con.get_cursor().fetchall()
            if not result:
                return {'state': State.Error}
            try:
                result = Tools.list_tuple2dict(_const_key_view_orders, result)
            except:
                return {'state': State.Error}
            return {'state': State.OK, 'orderlist': result}
        pass

    @staticmethod
    def viewOrderDetail(orderid, buyerornot):
        with DBContext() as context:
            if not context.exec("SELECT name,time,orders.number,total,orders.state from orders join book using (bookid) where orderid=? ", (orderid, )):
                return {'state': State.DBErr}
            result = context.get_cursor().fetchone()
            if not result:
                return {'state': State.NoOrderErr}
            #bookname = result[0]
            if buyerornot == "True":
                if not context.exec("SELECT address,phone,name from user_order join user on userid=sellerid where orderid=? ", (orderid, )):
                    return {'state': State.DBErr}
                temp = context.get_cursor().fetchone()
                if not temp:
                    return {'state': State.NoOrderErr}
                useraddress = temp[0]
                username = temp[2]
                userphone = temp[1]
            else:
                if not context.exec("SELECT address,phone,name from user_order join user on userid=buyerid where orderid=? ", (orderid, )):
                    return {'state': State.DBErr}
                temp = context.get_cursor().fetchone()
                if not temp:
                    return {'state': State.NoOrderErr}
                useraddress = temp[0]
                username = temp[2]
                userphone = temp[1]
        return {'state': State.OK, 'bookname': result[0], 'orderid': orderid, 'time': result[1], 'number': result[2], 'total': result[3],
                'orderstate': result[4], 'username': username, 'userphone': userphone, 'useraddress': useraddress}

    @staticmethod
    def changeOrderState(orderid, orderstate):
        with DBContext() as context:
            if not context.exec("SELECT * FROM orders where orderid=?", (orderid,)):
                return {'state': State.DBErr}
            result = context.get_cursor().fetchone()
            if not result:
                return {'state': State.NoOrderErr}
            if not context.exec("UPDATE orders set state=? where orderid=? ", (orderstate, orderid)):
                return {'state': State.DBErr}
        return {'state': State.OK}

# if __name__ == '__main__':
    # pass
    # with DBContext() as context:
        #context.exec("INSERT INTO user_order values(?,?,?,?)", ("BOOK1", "ORDER1", "BUYERID", "SELLERID"))
        #context.exec("INSERT INTO user_order values(?,?,?,?)", ("BOOK2", "ORDER2", "BUYERID", "SELLERID"))
        #context.exec("INSERT INTO user_order values(?,?,?,?)", ("BOOK3", "ORDER3", "BUYERID", "SELLERID"))
    # with DBContext() as context:
        #context.exec("SELECT orderid from user_order where buyerid=?", ("BUYERID",))
        #result = context.get_cursor().fetchall()
        # print(result)
    # OrderDBmanagement().viewOrders(userid="BUYERID")
    # with DBContext() as context:
        #context.exec("SELECT * from orders", ())
        #result = context.get_cursor().fetchall()
        # print(result)
    # OrderDBmanagement().changeOrderState("11","hh")
    # with DBContext() as context:
        #context.exec("SELECT * from orders", ())
        #result = context.get_cursor().fetchall()
        # print(result)
