# -*- coding=utf-8 -*-

from server.management.UserManagement import UserManagement



def post_login():
    return UserManagement.login()


