# 使用python
FROM python
# 作者信息
MAINTAINER jegoo, jegoo_cn@hotmial.com
# 源文件存放及工作目录
WORKDIR /opt/hlsyw
# 复制python的第三方库文件requirements.txt，并安装所有第三方库
COPY Pipfile ./
COPY Pipfile.lock ./
RUN pip install -p
# 复制本地的源文件到容器中
# COPY . .

# 用gunicorn执行flask应用
CMD ["gunicorn", "hlsyw:app", "-c", "conf/gunicorn.conf.py"]
