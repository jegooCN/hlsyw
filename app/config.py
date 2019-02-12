# coding=utf-8
"""
    Created by Jegoo on 2019-01-09 19:34
"""
import os

from datetime import timedelta

# ------数据库设置------
# flask-sqlacodegen --flask --outfile models.py mysql+pymysql://root:@47.111.30.98/hlsyw
# dialect+driver://username:password@host:port/database
DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'root'
PASSWORD = ''
HOST = 'mysql'
# HOST = '47.111.30.98'
PORT = '3306'
DATABASE = 'hlsyw'

SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'\
    .format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False

SQLALCHEMY_BINDS = {
    'users': '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE)
}

# ------session设置------
# 加密盐
SECRET_KEY = os.urandom(24)
# session持续时间，七天
PERMANENT_SESSION_LIFETIME = timedelta(days=7)

# ------基础配置------
# Debug
DEBUG = True
