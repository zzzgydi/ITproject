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
                context.exec("SELECT price from book where bookid=?", (bookid[i], ))
                result = context.get_cursor().fetchone()[0]
                print("书的单价为", result)
                total = int(number[i])*result
                context.exec("INSERT INTO orders values(?,?,?,?,?,?)", (bookid[i], orderid, t, number, total, state))
                result = context.get_cursor().fetchone()
                print("将订单写入数据库Orders", result)
                context.exec("SELECT userid from user_book_publish where bookid=?", (bookid[i], ))
                result = context.get_cursor().fetchone()[0]
                print("当前书的发布者id是", result)
                context.exec("INSERT INTO user_order values(?,?,?,?)", (bookid[i], orderid, buyerid, result))
                result = context.get_cursor().fetchone()
                print("将订单写入数据库User_Order", result)
        return orderid

    def viewOrders(self, userid):
        temp = []
        with DBContext() as context:
            context.exec("SELECT orderid from user_order where buyerid=? ", (userid, ))
            result = context.get_cursor().fetchall()
            for i in range(len(result)):
                # context.exec("SELECT * from orders where orderid=? ", (result[i][0],))
                temp[i] = result[i][0]  # 订单号数组
        return temp

    def viewOrderDetail(self, orderid):
        #temp = []
        with DBContext() as context:
            context.exec("SELECT * from orders where orderid=? ", (orderid, ))  # 一个订单可能包含多本书
            result = context.get_cursor().fetchall()  # 订单详情
            #for i in range(len(result)):
                #temp[i] = result[i]
        #return {'bookid': result[0], 'orderid': orderid, 'time': result[2], 'number': result[3], 'total': result[4],
                #'state': result[5]}
        return result

    def changeOrderState(self, orderid, state):
        with DBContext() as context:
            context.exec("SELECT * FROM orders where orderid=?", (orderid,))
            result = context.get_cursor().fetchone()
            context.exec("UPDATE orders set state=? where orderid=? ", (state, orderid))
        if not result:
            boolean = False
        else:
            boolean = True
        print("是否存在订单", boolean)
        return boolean

if __name__ == '__main__':
    pass
    #with DBContext() as context:
        #context.exec("INSERT INTO user_order values(?,?,?,?)", ("BOOK1", "ORDER1", "BUYERID", "SELLERID"))
        #context.exec("INSERT INTO user_order values(?,?,?,?)", ("BOOK2", "ORDER2", "BUYERID", "SELLERID"))
        #context.exec("INSERT INTO user_order values(?,?,?,?)", ("BOOK3", "ORDER3", "BUYERID", "SELLERID"))
    #with DBContext() as context:
        #context.exec("SELECT orderid from user_order where buyerid=?", ("BUYERID",))
        #result = context.get_cursor().fetchall()
        #print(result)
    #OrderDBmanagement().viewOrders(userid="BUYERID")
    #with DBContext() as context:
        #context.exec("SELECT * from orders", ())
        #result = context.get_cursor().fetchall()
        #print(result)
    #OrderDBmanagement().changeOrderState("11","hh")
    #with DBContext() as context:
        #context.exec("SELECT * from orders", ())
        #result = context.get_cursor().fetchall()
        #print(result)
