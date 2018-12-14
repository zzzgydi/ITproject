# -*- coding=utf-8 -*-

import os
from flask import session, request, jsonify, make_response
from server.mutex.State import State
from server.DBmanagement.PublishDBmanagement import PublishDBmanagement
import json
import uuid

_file_folder = "database/Files/"


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
        #请求图片资源
        if picture:
            try:
                image_data = open(os.path.join(_file_folder, picture), "rb")
                if image_data:
                    image_data = image_data.read()
                    response = make_response(image_data)
                    response.headers['Content-Type'] = 'image/png'
                    return response
            except:
                print("Unvalid picture asked")
        pass

