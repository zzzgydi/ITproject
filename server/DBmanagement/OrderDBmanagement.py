# -*- coding=utf-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from server.data.DBContext import DBContext
import time


class OrderDBmanagement:
    def __init__(self):
        pass

    def addNewOrder(self, buyerid, bookid, number):
        t = time.time()
        t = int(round(t * 1000))  # 毫秒级时间戳
        orderid = buyerid + str(t)
        state = "待付款"
        with DBContext() as context:
            for i in range(len(bookid)):
                context.get_cursor().execute("SELECT price from book where bookid=?", (bookid[i], ))
                result = context.get_cursor().fetchone()[0]
                print("书的单价为", result)
                total = int(number[i])*result
                context.get_cursor().execute("INSERT INTO orders values(?,?,?,?,?,?)", (bookid[i], orderid, t, number, total, state))
                result = context.get_cursor().fetchone()
                print("将订单写入数据库Orders", result)
                context.get_cursor().execute("SELECT userid from user_book_publish where bookid=?", (bookid[i], ))
                result = context.get_cursor().fetchone()[0]
                print("当前书的发布者id是", result)
                context.get_cursor().execute("INSERT INTO user_order values(?,?,?,?)", (bookid[i], orderid, buyerid, result))
                result = context.get_cursor().fetchone()
                print("将订单写入数据库User_Order", result)
        return orderid

    def viewOrders(self, userid):
        temp = []
        with DBContext() as context:
            context.get_cursor().execute("SELECT orderid from user_order where buyerid=? ", (userid, ))
            result = context.get_cursor().fetchall()
            for i in range(len(result)):
                # context.get_cursor().execute("SELECT * from orders where orderid=? ", (result[i][0],))
                temp[i] = result[i][0]  # 订单号数组
        return temp

    def viewOrderDetail(self, orderid):
        with DBContext() as context:
            context.get_cursor().execute("SELECT * from orders where orderid=? ", (orderid, ))
            result = context.get_cursor().fetchone()  # 订单详情
        return result

    def changeOrderState(self, orderid, state):
        with DBContext() as context:
            context.get_cursor().execute("SELECT * FROM orders where orderid=?", (orderid,))
            result = context.get_cursor().fetchone()
            context.get_cursor().execute("UPDATE orders set state=? where orderid=? ", (state, orderid))
        if not result:
            boolean = False
        else:
            boolean = True
        print("是否存在订单", boolean)
        return boolean

if __name__ == '__main__':
    pass
    #with DBContext() as context:
        #context.get_cursor().execute("INSERT INTO user_order values(?,?,?,?)", ("BOOK1", "ORDER1", "BUYERID", "SELLERID"))
        #context.get_cursor().execute("INSERT INTO user_order values(?,?,?,?)", ("BOOK2", "ORDER2", "BUYERID", "SELLERID"))
        #context.get_cursor().execute("INSERT INTO user_order values(?,?,?,?)", ("BOOK3", "ORDER3", "BUYERID", "SELLERID"))
    #with DBContext() as context:
        #context.get_cursor().execute("SELECT orderid from user_order where buyerid=?", ("BUYERID",))
        #result = context.get_cursor().fetchall()
        #print(result)
    #OrderDBmanagement().viewOrders(userid="BUYERID")
    #with DBContext() as context:
        #context.get_cursor().execute("SELECT * from orders", ())
        #result = context.get_cursor().fetchall()
        #print(result)
    #OrderDBmanagement().changeOrderState("11","hh")
    #with DBContext() as context:
        #context.get_cursor().execute("SELECT * from orders", ())
        #result = context.get_cursor().fetchall()
        #print(result)
