# 定义同时开启的处理请求的进程数量，根据网站流量适当调整
workers = 4
# 采用gevent库，支持异步处理请求，提高吞吐量
worker_class = "gevent"
# 监听IP放宽，以便于Docker之间、Docker和宿主机之间的通信
bind = "0.0.0.0:80"
# 访问日志和错误日志
accesslog = './log/gunicorn_access.txt'
errorlog = './log/gunicorn_error.txt'
