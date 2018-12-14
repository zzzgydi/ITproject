# -*- coding=utf-8 -*-

import os
from flask import session, request, jsonify, make_response
from server.mutex.State import State
from server.DBmanagement.PublishDBmanagement import PublishDBmanagement
import json
import uuid

_file_folder = "database/Files/"
_404_picture = "img_404.jpg"
_500_picture = "img_500.jpg"


class PublishManagement:

    @staticmethod
    def upload_file():
        # 上传图片文件
        # if 'userid' not in session:
        #   return jsonify({"state": State.NotLogin})
        print("file upload...")
        try:
            f = request.files['file']
            picture = str(uuid.uuid4()) + '.' + f.filename.rsplit('.', 1)[1]
            f.save(os.path.join(_file_folder, picture))
            return jsonify({"state": State.OK, "picture": picture})
        except Exception as e:
            print("Upload", e)
            return jsonify({"state": State.FormErr})
        return jsonify({'state': State.Error})

    @staticmethod
    def show_picture(picture):
        # 请求图片资源
        if picture:
            try:
                image_data = open(os.path.join(
                    _file_folder, picture), "rb").read()
            except:
                print("Unvalid picture asked")
                image_data = open(os.path.join(
                    _file_folder, _500_picture), "rb").read()
            response = make_response(image_data)
            response.headers['Content-Type'] = 'image/png'
            return response
        return jsonify({'state': State.FormErr})

    @staticmethod
    def publish_book():
        # 发布书籍
        # if 'userid' not in session:
        #   return jsonify({"state": State.NotLogin})
        try:
            reqdata = json.loads(request.data)
            name = reqdata['name']
            price = reqdata['price']
            detail = reqdata['detail']
            isbn = reqdata['isbn']
            number = reqdata['number']
            picture = reqdata['picture']
            author = reqdata['author']
            bookclass = reqdata['class']
        except:
            return jsonify({'state': State.FormErr})
        result = PublishDBmanagement.publish_book(session['userid'], name, 
                price, detail, isbn, number, picture, author, bookclass)
        return jsonify(result)
