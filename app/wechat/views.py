# coding=utf-8
"""
    Created by Jegoo on 2019-01-09 20:00
"""
import json

from flask import request, Response, render_template
from wechatpy.utils import check_signature
from wechatpy.parser import parse_message
from wechatpy.exceptions import InvalidSignatureException

from . import wechat
from .control import *

WECHAT_TOKEN = 'SUETESS'


@wechat.route('/unified_entry', methods=['GET', 'POST'])
def unified_entry():
    """
    统一入口
    1. 认证微信的服务器配置
    2. 处理微信的消息和事件
    :return:
    """
    method = request.method
    # GET请求时，为微信的后台认证
    if method == 'GET':
        try:
            signature = request.values.get("signature", '')
            timestamp = request.values.get("timestamp", '')
            nonce = request.values.get("nonce", '')
            echostr = request.values.get("echostr", '')
            check_signature(WECHAT_TOKEN, signature, timestamp, nonce)
        except InvalidSignatureException:
            return json.dumps({
                'state': 'error',
                'message': 'Invalid signature'
            })
        else:
            return echostr
    # POST请求时，为消息或是事件
    elif method == 'POST':
        event = parse_message(request.data)
        if isinstance(event, UnknownMessage):
            return json.dumps({
                'state': 'error',
                'message': 'Unknown Message'
            })
        reply = handle_event(event, request.url_root)
        return Response(reply.render(), content_type="application/xml")


@wechat.route('/register', methods=['GET', 'POST'])
def register():
    """
    学生登记
    :return:
    """
    user_id = request.values.get('user_id')
    return render_template(
        'register.html',
        user_id=user_id
    )


@wechat.route('/exercise', methods=['GET', 'POST'])
def exercise():
    """
    每日一题
    :return:
    """
    user_id = request.values.get('user_id')
    img_path = request.values.get('img_path')
    date = request.values.get('date')
    grade = get_grade_by_user_id(user_id)
    return render_template(
        'exercise.html',
        date=date,
        grade=grade.description,
        img_path=img_path
    )


@wechat.route('/form_register', methods=['GET', 'POST'])
def form_register():
    """
    登录提交
    :return:
    """
    user_id = request.values.get('user_id')
    student_name = request.values.get('student_name')
    phone_num = request.values.get('phone_num')
    grade_id = request.values.get('grade_id')
    if not user_id or user_id == '':
        return render_template(
            'register.html',
            error_msg='登记出错，请重新填写！'
        )
    add_user(user_id, student_name=student_name, phone_num=phone_num, grade_id=grade_id)
    return render_template('success.html')


@wechat.route('/create_exe', methods=['GET', 'POST'])
def create_exe():
    """
    创建每日一题页面
    :return:
    """
    return render_template('create_exe.html')


@wechat.route('/create_exercise', methods=['GET', 'POST'])
def create_exercise():
    """
    添加每日一题
    :return:
    """
    release_date = request.values.get('release_date')
    grade_id = request.values.get('grade_id')
    img_file = request.files.get('img')
    grade = get_grade_by_id(grade_id)
    add_exercise(release_date, grade, img_file)
    return render_template(
        'create_exe.html',
        msg='{} {}已上传成功，可再上传其他！'.format(release_date, grade.description)
    )
