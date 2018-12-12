# -*- coding=utf-8 -*-

import json
import os
from flask import Flask, render_template, jsonify, url_for
from flask import request, redirect, make_response
from datetime import timedelta
from server.management.UserManagement import UserManagement


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


app.add_url_rule('/api/login', view_func=UserManagement.login, methods=['POST'])
app.add_url_rule('/api/register', view_func=UserManagement.register, methods=['POST'])
app.add_url_rule('/api/reviseinfo', view_func=UserManagement.revise_info, methods=['POST'])
app.add_url_rule('/api/getuserinfo', view_func=UserManagement.get_info, methods=['POST', 'GET'])


if __name__ == "__main__":
    app.run(debug=False)
