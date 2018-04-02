# coding:utf-8
import configparser
from pathlib import Path
from .questions import *


conf = configparser.ConfigParser()
conf.read(str(Path(__file__).parent.parent / 'config.ini'), encoding='utf-8')

# chrome 驱动
chrome_drive_path = str(Path(__file__).parent / 'chromedriver.exe') if not conf.get('chromedriver', 'path', fallback=False) else conf.get('chromedriver', 'path', fallback=False)

# http请求地址(查询)
questions_request_query = conf.get('queryHTTP', 'url_query', fallback=False)

# http请求地址(更新)
questions_request_update = conf.get('queryHTTP', 'url_update', fallback=False)

# 数据库地址
db_ip = conf.get('queryDatabase', 'ip', fallback=False)

# 数据库端口
db_port = conf.getint('queryDatabase', 'port', fallback=False)

# 数据库名称
db_name = conf.get('queryDatabase', 'name', fallback=False)

# 数据集合名称
db_database_collection = conf.get('queryDatabase', 'collection', fallback=False)

# 数据库账号
db_username = conf.get('queryDatabase', 'username', fallback=False)

# 数据库密码
db_pwd = conf.get('queryDatabase', 'pwd', fallback=False)
