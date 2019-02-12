# coding=utf-8
"""
    Created by Jegoo on 2019-02-12 13:24
"""
from app import db


class WechatUser(db.Model):
    __tablename__ = 'wechat_user'

    user_id = db.Column(db.String(80), primary_key=True, comment='用户id，主键')
    parent_name = db.Column(db.String(80), comment='家长姓名')
    student_name = db.Column(db.String(80), comment='学生姓名')
    wechat_name = db.Column(db.String(80), comment='微信名')
    grade_id = db.Column(db.ForeignKey('grade.grade_id'), nullable=False, index=True, comment='年级id')
    is_subscribe = db.Column(db.String(1), server_default=db.FetchedValue(), comment='是否关注')
    student_sex = db.Column(db.String(10), comment='学生性别')
    phone_num = db.Column(db.String(20), comment='手机号')
    register_time = db.Column(db.DateTime, comment='注册时间')
    remark = db.Column(db.String(200), comment='备注')

    grade = db.relationship('Grade', primaryjoin='WechatUser.grade_id == Grade.grade_id', backref='wechat_users')

    @classmethod
    def get(cls, user_id):
        """
        根据id获取用户
        :param user_id:
        :return:
        """
        return cls.query().filter(WechatUser.user_id == user_id).first()

    @classmethod
    def get_all(cls):
        return cls.query().all()

    @classmethod
    def create(cls, user_id, parent_name=None, student_name=None, wechat_name=None, grade=None,
               is_subscribe='Y', student_sex=None, phone_num=None, register_time=None, remark=None):
        with db.auto_commit():
            user = cls(user_id=user_id, parent_name=parent_name, student_name=student_name,
                       wechat_name=wechat_name, grade=grade, is_subscribe=is_subscribe, student_sex=student_sex,
                       phone_num=phone_num, register_time=register_time, remark=remark)
            db.session.add(user)
            return True

    def change_subscribe_state(self, is_subscribe):
        """
        修改关注状态
        :param is_subscribe: boolean
        :return:
        """
        with db.auto_commit():
            self.is_subscribe = 'Y' if is_subscribe else 'N'
