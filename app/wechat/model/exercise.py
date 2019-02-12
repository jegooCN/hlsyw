# coding=utf-8
"""
    Created by Jegoo on 2019-02-12 13:22
"""
from sqlalchemy import and_
from app import db


class Exercise(db.Model):
    __tablename__ = 'exercise'

    exercise_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    description = db.Column(db.String(200))
    grade_id = db.Column(db.ForeignKey('grade.grade_id'), index=True)
    image_path = db.Column(db.String(800))
    release_date = db.Column(db.Date, nullable=False)
    state = db.Column(db.Integer, nullable=False)
    remark = db.Column(db.String(800))
    create_time = db.Column(db.DateTime, nullable=False)

    grade = db.relationship('Grade', primaryjoin='Exercise.grade_id == Grade.grade_id', backref='exercises')

    @classmethod
    def get_by_date_grade(cls, release_date, grade):
        """
        根据今天日期和年级获取每日一题
        :param release_date: 当天日期
        :param grade: 年级对象
        :return:
        """
        return cls.query.filter(
            and_(and_(Exercise.release_date == release_date, Exercise.grade == grade), Exercise.state == 1)).first()

    @classmethod
    def create(cls, title=None, description=None, grade=None, image_path=None, release_date=None, state=1, remark=None,
               create_time=None):
        """
        新建每日一题
        """
        with db.auto_commit():
            old_exercise = cls.get_by_date_grade(release_date, grade)
            # 已有每日一题时，改原有的每日一题状态，使不可用
            if old_exercise:
                old_exercise.state = 2
            exercise = cls(title=title, description=description, grade=grade, image_path=image_path,
                           release_date=release_date, state=state, remark=remark, create_time=create_time)
            db.session.add(exercise)
            return True
