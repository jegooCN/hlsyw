# coding=utf-8
"""
    Created by Jegoo on 2019-01-13 13:12
"""
from flask import Flask
from contextlib import contextmanager
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy

import app.config as config


# from .model import db


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e


db = SQLAlchemy()


def create_app():
    app = Flask(__name__, static_url_path='')
    # 导入配置
    app.config.from_object(config)
    # 注册数据库db
    db.init_app(app)
    # 生成数据库数据
    init_dbs_data(db, app)
    # 注册蓝图
    register_buleprint(app)

    return app


def register_buleprint(app):
    # from .wechat import wechat
    # app.register_blueprint(wechat)
    pass


def init_dbs_data(db, app):
    from .wechat import model

    with app.app_context():
        db.create_all()
