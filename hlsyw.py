# coding=utf-8
"""
    Created by Jegoo on 2019-01-09 19:34
"""
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run('0.0.0.0', port=80)
