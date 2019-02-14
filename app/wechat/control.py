# coding=utf-8
"""
    Created by Jegoo on 2019-01-10 15:29
"""
import datetime
import wechatpy

from wechatpy.events import *
from wechatpy.messages import *

from .utils import *
from .model import *

# from .db_handler import UserDao, GradeDao, ExerciseDao, RecordDao

# 开发者ID(AppID)
APP_ID = 'wx6e6f16617daa4b58'
# 开发者密码(AppSecret)
APP_SECRET = 'a3672b16a4dde63ad0655221a2d4ec94'
# 微信服务
wechat_client = wechatpy.WeChatClient(APP_ID, APP_SECRET)

admin_users = ['oejQe05i2ZF95lIMuPoAKzfTjkxA', 'oejQe0xeihIEcT0ukB6z8l_P0oVk']


def handle_event(event, root_url):
    """
    处理微信的事件
    :param root_url: 项目根url
    :param event: 解析后的事件
    :return:
    """
    # 用户id，对应的微信open_id
    user_id = event.source
    user = WechatUser.get(user_id)

    # 关注事件
    if isinstance(event, SubscribeEvent):
        if user:
            grade = user.grade
            # 用户已登记，则返回登记信息，确定是否重新登记
            user.change_subscribe_state(user, True)
            content = '您已登记过学生信息，如下：\n\n学生姓名：{}\n手机号码：{}\n所属年级：{}({})' \
                      '\n\n如需重新登记，请回复“学生登记”；如需获取每日一题，请回复“每日一题”。' \
                .format(user.student_name, user.phone_num, grade.name, grade.alias)
            return create_text_reply(event, content)
        else:
            # 还未登记，则发送登记链接
            title = '学生登记'
            image = '{}image/07.jpg'.format(root_url)
            url = '{}wechat/register?user_id={}'.format(root_url, event.source)
            return create_article_reply(event, title=title, image=image, url=url)

    if isinstance(event, UnsubscribeEvent):
        # 取消关注事件，改变user的关注状态
        user.change_subscribe_state(user, False)
        return create_text_reply(event, '感谢您的支持！')

    if isinstance(event, TextMessage):
        # 文本信息事件
        content = event.content

        if content == '每日一题':
            if user:
                grade = user.grade
                today = datetime.date.today()
                exercise = Exercise.get_by_date_grade(today, grade)
                if exercise:
                    title = '{} {}({})每日一题'.format(get_today(), grade.name, grade.alias)
                    image = '{}image/05.jpg'.format(root_url)
                    url = '{}wechat/exercise?user_id={}&img_path={}&date={}'.format(root_url, user_id,
                                                                                    exercise.image_path,
                                                                                    exercise.release_date)
                    # 添加领取每日一题记录
                    now = datetime.datetime.now()
                    Record.create(user, exercise, today, now)
                    return create_article_reply(event, title=title, image=image, url=url, description='小坚持，大成长！')
                else:
                    return create_text_reply(event, '今天的每日一题还没出炉呢，稍后再来或是联系老师吧！')
            else:
                return create_text_reply(event, '您还未登记学生信息，回复“学生登记”。')

        if content == '学生登记':
            title = '学生登记'
            image = '{}image/07.jpg'.format(root_url)
            url = '{}wechat/register?user_id={}'.format(root_url, event.source)
            return create_article_reply(event, title=title, image=image, url=url, description='学生信息录入')

        if content == '上传' and user_id in admin_users:
            title = '每日一题上传'
            image = '{}image/10.jpg'.format(root_url)
            url = '{}wechat/create_exe?user_id={}'.format(root_url, event.source)
            return create_article_reply(event, title=title, image=image, url=url, description='记得每天上传哦！')

        if content == '学生列表' and user_id in admin_users:
            user_list = WechatUser.get_all()
            user_info = '\n'.join(
                ['{}\t{}'.format(u.student_name, u.grade.description) for u in user_list])
            content = '姓名\t年级\n{}'.format(user_info)
            return create_text_reply(event, content)

        if content == '领取情况' and user_id in admin_users:
            today = datetime.date.today()
            user_list = WechatUser.get_all()
            data = []
            # 根据每个人的领取记录，如果有当天的记录，返回有
            for u in user_list:
                r_text = '×'
                for r in u.records:
                    if r.r_date == today:
                        r_text = '√'
                        break
                data.append((u.student_name, r_text))
            info = '\n'.join(['{}\t{}'.format(d[0], d[1]) for d in data])
            content = '学生\t领取情况\n{}'.format(info)
            return create_text_reply(event, content)

        content = '如需学生登记，请回复“学生登记”；如需获取每日一题，请回复“每日一题”。'
        return create_text_reply(event, content)


def add_user(user_id, parent_name=None, student_name=None, wechat_name=None, grade_id=None,
             is_subscribe=None, student_sex=None, phone_num=None, register_time=None, remark=None):
    """
    新增用户
    :return:
    """
    # grade = Grade.get(grade_id)
    if not register_time:
        register_time = datetime.datetime.now()
    WechatUser.create_or_update(user_id=user_id, parent_name=parent_name, student_name=student_name,
                                wechat_name=wechat_name, grade_id=grade_id, is_subscribe=is_subscribe,
                                student_sex=student_sex, phone_num=phone_num, register_time=register_time,
                                remark=remark)


def get_grade_by_user_id(user_id):
    return WechatUser.get(user_id).grade


def get_grade_by_id(grade_id):
    return Grade.get(grade_id)


def add_exercise(release_date, grade, img_file):
    file_name = int(time.time())
    img_path = 'app/static/exercise_pic/{}.png'.format(file_name)
    img_file.save(img_path)
    now = datetime.datetime.now()
    return Exercise.create(release_date=release_date, grade=grade, image_path=img_path.replace('app/static/', ''),
                           create_time=now)
