# coding=utf-8
"""
    Created by Jegoo on 2019-02-12 13:23
"""
from app import db


class Record(db.Model):
    __tablename__ = 'record'

    record_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('wechat_user.user_id'), nullable=False, index=True)
    exercise_id = db.Column(db.ForeignKey('exercise.exercise_id'), nullable=False, index=True)
    r_time = db.Column(db.DateTime, nullable=False)
    r_date = db.Column(db.Date, nullable=False)

    exercise = db.relationship('Exercise', primaryjoin='Record.exercise_id == Exercise.exercise_id', backref='records')
    user = db.relationship('WechatUser', primaryjoin='Record.user_id == WechatUser.user_id', backref='records')

    @classmethod
    def create(cls, user, exercise, today, now):
        """
        新建领取记录
        :param user: 用户
        :param exercise: 每日一题
        :param today: 当天日期
        :param now: 时间
        :return:
        """
        with db.auto_commit():
            recode = cls(user=user, exercise=exercise, r_time=now, r_date=today)
            db.session.add(recode)
            return True
