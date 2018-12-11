import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from server.DBmanagement.OrderDBmanagement import OrderDBmanagement

class OrderManagement:
    odbm = 0

    def __init__(self):
        self.odbm = OrderDBmanagement()

    def purchaseBook(self, buyerid, bookid, number):
        orderid = self.odbm.addNewOrder(buyerid, bookid, number)
        return orderid

    def viewOrders(self, userid):
        orders = self.odbm.viewOrders(userid)
        return orders

    def viewOrderDetail(self, orderid):
        orderDetail = self.odbm.viewOrderDetail(orderid)
        return orderDetail

    def changeOrderState(self, orderid, state):
        boolean = self.odbm.changeOrderState(orderid, state)
        return boolean
