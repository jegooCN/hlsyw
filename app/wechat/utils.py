# coding=utf-8
"""
    Created by Jegoo on 2019-01-10 15:23
"""
import time

from wechatpy.replies import *


def get_today():
    today = time.strftime('%m月%d日', time.localtime(time.time()))
    return today


def create_article_reply(event, title='', description='', image='', url=''):
    """
    创建一个图文回复
    :param event: 事件
    :param title: 图文标题
    :param description: 图文详情
    :param image: 图片路径
    :param url: 跳转url
    :return:
    """
    reply = ArticlesReply(message=event)
    reply.add_article({
        'title': title,
        'description': description,
        'image': image,
        'url': url
    })
    return reply


def create_text_reply(event, content):
    """
    创建一个文本回复
    :param event: 事件
    :param content: 回复内容
    :return:
    """
    relay = TextReply(message=event)
    relay.content = content
    return relay
