# -*- coding=utf-8 -*-
import time
from server.mutex import Tools
from server.mutex.State import State
from server.data.DBContext import DBContext

_const_key_view_orders = ('bookid', 'orderid', 'time', 'total', 'state',
                          'name', 'picture', 'author', 'class')


class OrderDBmanagement(object):
    @staticmethod
    def addNewOrder(buyerid, bookid, number):
        ts = int(time.time())  # 秒级时间戳
        orderid = buyerid + 'A' + str(ts)
        state = "未完成"
        with DBContext() as context:
            if not context.exec("SELECT price,state from book where bookid=?;", (bookid, )):
                return {'state': State.DBErr}
            result = context.get_cursor().fetchone()
            if not result:
                return {'state': State.NoBookErr}
            total = result[0]
            bookstate = result[1]
            if bookstate != "待售":
                return {'state': State.NoSale}
            if not context.exec("INSERT INTO orders values(?,?,?,?,?,?);", (bookid, orderid, Tools.get_current_time(), number, total, state)):
                return {'state': State.DBErr}
            if not context.exec("SELECT userid from user_book_publish where bookid=?;", (bookid, )):
                return {'state': State.DBErr}
            result = context.get_cursor().fetchone()
            if not result:
                return {'state': State.NoBookErr}
            result = result[0]
            if not context.exec("INSERT INTO user_order values(?,?,?,?);", (bookid, orderid, buyerid, result)):
                return {'state': State.DBErr}
            if not context.exec("update book set state='已售' where bookid=?;", (bookid,)):
                return {'state': State.DBErr}
        return {'orderid': orderid, 'state': State.OK, 'price': total}

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
            if not con.exec(_sql, (userid,)):
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
            # bookname = result[0]
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
        if orderstate != "完成" and orderstate != '已取消':
            return {'state': State.Debug}
        with DBContext() as context:
            if not context.exec("SELECT bookid,orders.state,book.state FROM orders join book using (bookid) where orderid=?;", (orderid,)):
                return {'state': State.DBErr}
            result = context.get_cursor().fetchone()
            if not result:
                return {'state': State.NoOrderErr}
            bookid, orders_state, book_state = result
            if orders_state != '未完成' and book_state != '已售':
                return {'state': State.Error}
            if not context.exec("UPDATE orders set state=? where orderid=? ", (orderstate, orderid)):
                return {'state': State.DBErr}
            if orderstate == '已取消' and not context.exec("UPDATE book set state=? where bookid=? ", ('待售', bookid)):
                return {'state': State.DBErr}
        return {'state': State.OK}
