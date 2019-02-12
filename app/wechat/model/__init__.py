# coding=utf-8
"""
    Created by Jegoo on 2019-02-12 13:25
"""
from app import db


class BaseModel(db.Model):
    __abstract__ = True


from .exercise import *
from .grade import *
from .record import *
from .user import *
