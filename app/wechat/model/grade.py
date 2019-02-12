# coding=utf-8
"""
    Created by Jegoo on 2019-02-12 13:23
"""
from app import db


class Grade(db.Model):
    __tablename__ = 'grade'

    grade_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    alias = db.Column(db.String(80))
    description = db.Column(db.String(200))
    index = db.Column(db.Integer)
    grade_type = db.Column(db.String(80))
    remark = db.Column(db.String(200))

    @classmethod
    def get(cls, grade_id):
        """
        根据id获取年级
        :param grade_id:
        :return:
        """
        return cls.query.filter(Grade.grade_id == grade_id).first()
