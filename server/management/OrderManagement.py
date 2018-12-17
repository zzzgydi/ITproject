# -*- coding=utf-8 -*-
from server.DBmanagement.OrderDBmanagement import OrderDBmanagement
from flask import session, request, jsonify
from server.mutex.State import State
import json


class OrderManagement(object):
    @staticmethod
    def purchaseBook():
        if 'userid' not in session:
            return jsonify({'state': State.NotLogin})
        try:
            reqdata = json.loads(request.data)
            buyerid = session['userid']
            bookid = reqdata['bookid']
            number = 1
        except:
            return jsonify({'state': State.FormErr})
        result = OrderDBmanagement.addNewOrder(buyerid, bookid, number)
        return jsonify(result)

    @staticmethod
    def viewOrders():
        if 'userid' not in session:
            return jsonify({'state': State.NotLogin})
        try:
            reqdata = json.loads(request.data)
            userid = session['userid']
            buyerornot = reqdata['test']
        except:
            return jsonify({'state': State.FormErr})
        result = OrderDBmanagement.view_orders(userid, buyerornot)
        if result['state'] != State.OK:
                return jsonify({'state': result['state']})
        return jsonify(result)

    @staticmethod
    def viewOrderDetail():
        if 'userid' not in session:
            return jsonify({'state': State.NotLogin})
        try:
            reqdata = json.loads(request.data)
            orderid = reqdata['orderid']
            buyerornot = reqdata['buyerornot']
        except:
            return jsonify({'state': State.FormErr})
        result = OrderDBmanagement.viewOrderDetail(orderid, buyerornot)
        if result['state'] != State.OK:
            return jsonify({'state': result['state']})
        return jsonify(result)

    @staticmethod
    def changeOrderState():
        if 'userid' not in session:
            return jsonify({'state': State.NotLogin})
        try:
            reqdata = json.loads(request.data)
            orderid = reqdata['orderid']
            orderstate = reqdata['orderstate']
        except:
            print('...')
            return jsonify({'state': State.FormErr})
        result = OrderDBmanagement.changeOrderState(orderid, orderstate)
        return jsonify(result)

