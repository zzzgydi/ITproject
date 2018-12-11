# -*- coding=utf-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from server.DBmanagement.PublishDBmanagement import PublishDBManagement


class PublishManagement:
    publish = 0

    def __init__(self):
        self.publish = PublishDBManagement()

    def publishBook(self, bookid, name, price, detail, isbn, number, picture):
        result = self.publish.publishBook(bookid, name, price, detail, isbn, number, picture)
        return result
