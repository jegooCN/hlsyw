# coding=utf-8
"""
    Created by Jegoo on 2019-01-09 20:00
"""
from flask import Blueprint

wechat = Blueprint('main', __name__, url_prefix='/wechat')
from . import views
