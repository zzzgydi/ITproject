# -*- coding=utf-8 -*-

import json
import os
from flask import Flask, render_template, jsonify, url_for
from flask import request, redirect, make_response
from datetime import timedelta
from server.management.UserManagement import UserManagement
from server.management.AdminManagement import AdminManagement
from server.management.OrderManagement import OrderManagement
from server.management.PublishManagement import PublishManagement
from server.management.BookManagement import BookManagement

app = Flask(__name__,
            static_folder="./client/static",
            template_folder="./client")


#app.config['SECRET_KEY'] = "ITPROJECT2018"
# 设置为24位的字符,每次运行服务器都是不同的，所以服务器启动一次上次的session就清除。
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)  # 设置session的保存时间。


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")

#gydi
app.add_url_rule('/api/login', view_func=UserManagement.login, methods=['POST'])
app.add_url_rule('/api/register', view_func=UserManagement.register, methods=['POST'])
app.add_url_rule('/api/reviseinfo', view_func=UserManagement.revise_info, methods=['POST'])
app.add_url_rule('/api/getuserinfo', view_func=UserManagement.get_info)
app.add_url_rule('/api/getcollect', view_func=UserManagement.get_collect)
app.add_url_rule('/api/collect', view_func=UserManagement.collect_book, methods=['POST'])
app.add_url_rule('/api/cancelcoll', view_func=UserManagement.cancel_collect, methods=['POST'])
#图片相关
app.add_url_rule('/api/upload', view_func=PublishManagement.upload_file, methods=['POST'])
app.add_url_rule('/show/<string:picture>', view_func=PublishManagement.show_picture)
#管理员登录
app.add_url_rule('/admin/api/login', view_func=AdminManagement.admin_login, methods=['POST'])

#武杰
app.add_url_rule('/api/addorder', view_func=OrderManagement.purchaseBook, methods=['POST'])
app.add_url_rule('/api/orders', view_func=OrderManagement.viewOrders, methods=['POST'])
app.add_url_rule('/api/orderdetail', view_func=OrderManagement.viewOrderDetail, methods=['POST'])
app.add_url_rule('/api/changestate', view_func=OrderManagement.changeOrderState, methods=['POST'])

#发布书籍
app.add_url_rule('/api/publish', view_func=PublishManagement.publish_book, methods=['POST'])

#查找书籍
app.add_url_rule('/api/search', view_func=BookManagement.searchBook, methods=['POST'])
#查看书籍详情
app.add_url_rule('/api/viewbook', view_func=BookManagement.viewBook, methods=['POST'])

#管理员-查看未审核书籍
app.add_url_rule('/api/unreviewed', view_func=AdminManagement.search_unreviewed_book, methods=['POST'])
#管理员-查看用户
app.add_url_rule('/api/viewuser', view_func=AdminManagement.view_user, methods=['POST'])
#管理员-审核书籍
app.add_url_rule('/api/changestate', view_func=AdminManagement.book_audit, methods=['POST'])

#下架书籍
app.add_url_rule('/api/soldoutbook', view_func=AdminManagement.sold_out_book, methods=['POST'])






if __name__ == "__main__":
    app.run(debug=False)


