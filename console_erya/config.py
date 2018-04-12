# coding:utf-8
import configparser
from pathlib import Path
from os import getcwd
# from pymongo import MongoClient, errors
# from console_erya.questions import query_http_server

conf = configparser.ConfigParser()
# print(__file__)
# print(getcwd())
conf.read(str(Path(getcwd()) / 'config.ini'), encoding='utf-8')
ip = conf.get('Server', 'ip')
port = conf.getint('Server', 'port')

# chrome 驱动
chrome_drive_path = str(Path(getcwd()) / 'chromedriver.exe') if not conf.get('chromedriver', 'path', fallback=False) else conf.get('chromedriver', 'path', fallback=False)

# http请求地址(查询)
questions_request_query = conf.get('queryHTTP', 'url_query', fallback=False)

# http请求地址(更新)
questions_request_update = conf.get('queryHTTP', 'url_update', fallback=False)

# # 数据库地址
# db_ip = conf.get('queryDatabase', 'ip', fallback=False)
#
# # 数据库端口
# db_port = conf.getint('queryDatabase', 'port', fallback=False)
#
# # 数据库名称
# db_name = conf.get('queryDatabase', 'name', fallback=False)
#
# # 数据集合名称
# db_database_collection = conf.get('queryDatabase', 'collection', fallback=False)
#
# # 数据库账号
# db_username = conf.get('queryDatabase', 'username', fallback=False)
#
# # 数据库密码
# db_pwd = conf.get('queryDatabase', 'pwd', fallback=False)
#
# if db_ip and db_port:
#     client = MongoClient(db_ip, db_port)
#     db = client.get_database(db_name)
#     if db_username and db_pwd:
#         try:
#             db.authenticate(db_username, db_pwd)
#             table = db.get_collection(db_database_collection)
#         except errors.OperationFailure:
#             table = None

# 微信题库公众号
wechat_mp = [x for x in conf.get('wechat', 'wechat').split()]


# 开启debug模式(自动截图)
debug = conf.getboolean('program', 'debug', fallback=False)

# 题库查询方式 query_mongo_database
# questions_query_method = query_mongodb if conf.getint('queryMethod', 'm', fallback=False) == 1 else query_http_server
# questions_query_method = query_http_server

# 截图
screen_png = str(Path(getcwd()) / 'temp' /'test.png')

# temp文件夹
folder_temp_path = str(Path(getcwd()) / 'temp')

# 截图tmp
screen_png_tmp = str(Path(getcwd()) / 'temp' / 'tmp.png')

# 图片模板
templates_pic_path = str(Path(getcwd()) / 'templates_pic')

# 视频中间测试提交1_1
video_test_submit1_1 = str(Path(getcwd()) / 'templates_pic' / 'submit1_1.png')

# 视频中间测试提交1_2
video_test_submit1_2 = str(Path(getcwd()) / 'templates_pic' / 'submit1_2.png')

# 视频中间测试提交1_3
video_test_submit1_3 = str(Path(getcwd()) / 'templates_pic' / 'submit1_3.png')

# 视频中间测试提交2_1
video_test_submit2_1 = str(Path(getcwd()) / 'templates_pic' / 'submit2_1.png')

# 视频中间测试提交2_2
video_test_submit2_2 = str(Path(getcwd()) / 'templates_pic' / 'submit2_2.png')

# 视频中间测试提交继续1
video_test_continue1 = str(Path(getcwd()) / 'templates_pic' / 'continue1.png')

# 视频中间测试提交继续2
video_test_continue2 = str(Path(getcwd()) / 'templates_pic' / 'continue2.png')

# 视频暂停时开始按钮1(470, 795, 490, 820)
video_pause_continue1 = str(Path(getcwd()) / 'templates_pic' / 'pause1.png')

# 视频暂停时开始按钮2(470, 795, 490, 820)
video_pause_continue2 = str(Path(getcwd()) / 'templates_pic' / 'pause2.png')

# 视频暂停时开始按钮3(470, 773, 490, 795)
video_pause_continue3 = str(Path(getcwd()) / 'templates_pic' / 'pause3.png')

# 视频进度条位置1
video_progress_bar1 = (535, 795, 690, 820)

# 视频进度条位置2
video_progress_bar2 = (535, 775, 690, 800)

# 视频比较尺寸
player_screenshot_site = (470, 300, 1130, 790)

# 图片声音调节
size_volume = (1055, 797, 1085, 815)

# 视频暂停/继续按钮1
site_video_pause_continue1 = (470, 795, 490, 820)

# 视频暂停/继续按钮2
site_video_pause_continue2 = (470, 773, 490, 795)

# 视频内答题 提交 按钮位置1
site_video_test_submit1 = (940, 535, 990, 560)

# 视频内答题 提交 按钮位置2
site_video_test_submit2 = (940, 568, 990, 593)

# 视频内答题 提交 按钮位置2
site_video_test_submit3 = (950, 510, 1000, 535)

# 视频内答题提交成功后继续按钮位置1
size_video_continue1 = (940, 535, 990, 560)

# 视频内答题提交成功后继续按钮位置2
size_video_continue2 = (940, 568, 990, 593)

# 入口url
entrance_url = 'https://passport2.chaoxing.com/login?fid=145&refer=http://i.mooc.chaoxing.com'


# 刷新验证码
refresh_code = {
    'type': 'xpath',
    'string': '//*[@id="numVerCode"]'
}

# 验证码图片存放位置
path_vercode = str(Path(__file__).parent / 'temp')

# 登陆验证码位置
login_code = {
    'type': 'id',
    'string': 'numcode'
}


# 登陆账号输入框位置
login_username = {
    'type': 'id',
    'string': 'unameId'
}


# 登陆密码输入框位置
login_password = {
    'type': 'id',
    'string': 'passwordId'
}

# 登陆按钮位置
login_button = {
    'type': 'xpath',
    'string': '//*[@id="form"]/table/tbody/tr[7]/td[2]/label/input'
}


# 登陆错误结果
login_result = {
    'type': 'xpath',
    'string': '//*[@id="show_error"]'
}


# 登陆验证
login_ver = {
    'type': 'xpath',
    'string': '//*[@id="space_nickname"]/p'
}

# 选择院校
select_school_button = {
    'type': 'xpath',
    'string': '//*[@id="selectSchoolA"]'
}

# 院校搜索框
select_school_search = {
    'type': 'id',
    'string': 'searchSchool1'
}

# 院校搜索按钮
select_school_search_button = {
    'type': 'xpath',
    'string': '//*[@id="dialog1"]/div/div[1]/ul/li[2]/input[2]'
}

# 院校搜索结果
select_school_result = {
    'type': 'xpath',
    'string': '//*[@id="searchForms"]/li'
}

# 待刷课程frame
course_name_list_frame = [
    {
        'name': 'iframe',
        'index': 0
    }
]

# 课程列表
course_name_list = {
    'type': 'xpath',
    'string': '//div[@class="Mconright httpsClass"]'
    #'string': '/html/body/div/div[2]/div[2]/ul/li'
}

# 去除开启复习模式课程, split('\n')[-2].strip() == '已开启复习模式
remove_irrelevant_course = ['\n', -2, '已开启复习模式']

# 课程页面标题
course_page_title = '学习进度页面'

# 学习页面标题
learn_page_title = '学生学习页面'

# 获取课程课时名称
course_lesson_name = {
    'type': 'xpath',
    'string': '/html/body/div[7]/div[1]/div[2]/div[3]/div/div'
}

# 获取课程课时链接
course_lesson_link = {
    'type': 'xpath',
    'string': '//div[@class="leveltwo"]/h3/span[@class="articlename"]/a'
}

# 学习页面进入视频部分iframe
learn_page_video_part_iframe = [
    {
        'name': 'iframe',
        'index': 0
    }
]

# 学习页面视频iframe
learn_page_video_iframe = [
    {
        'name': 'iframe',
        'index': 0
    },
    {
        'name': 'iframe',
        'index': 0
    }
]

# 学习页面章节测试完成状态iframe
learn_page_test_status_iframe = [
    {
        'name': 'iframe',
        'index': 0
    }
]

# 章节测试内容更新数据库iframe
learn_page_test_iframe_updatedb = [
    {
        'name': 'iframe',
        'index': 0
    },
    {
        'name': 'iframe',
        'index': 0
    },
    {
        'name': 'iframe',
        'index': 0
    }
]

# 章节测试内容iframe
learn_page_test_iframe = [
    {
        'name': 'iframe',
        'index': 0
    },
    {
        'name': 'iframe',
        'index': 0
    },
    {
        'name': 'iframe',
        'index': 0
    }
]

# 学习页面视频按钮
learn_page_video_button = {
    'type': 'xpath',
    'string': '//span[@title="视频"]'
}

# 学习页面章节测验按钮
learn_page_test_button = {
    'type': 'xpath',
    'string': '//span[@title="章节测验"]'
}

# 视频完成状态，如果xpath不报错则表示已完成
video_complete_status = {
    'type': 'xpath',
    'string': '//div[@class="ans-attach-ct ans-job-finished"]'
}

# 章节测验完成状态，如果xpath不报错则表示已完成
test_complete_stataus = {
    'type': 'xpath',
    'string': '//div[@class="ans-attach-ct ans-job-finished"]/div'
}


# 章节测试问题更新数据库
learn_page_test_title_updatedb = {
    'type': 'xpath',
    'string': '//*[@id="ZyBottom"]/div/div/div/div[1]'
}

# 章节测试得分更新数据库
learn_page_test_score_updatedb = {
    'type': 'xpath',
    'string': '//*[@id="ZyBottom"]//div/span[2]/span'
}

# 章节测试问题
learn_page_test_title = {
    'type': 'xpath',
    'string': '//div[@class="TiMu"]/div[1]/div[1]'
}

# 章节测试选择题选项
learn_page_test_select_gather = {
    'type': 'xpath',
    'string': '//div[@class="TiMu"]/div[2]/ul'
}

# 章节测试选择题各选项
learn_page_test_select_separate = {
    'type': 'xpath',
    'string': '//div[@class="TiMu"]//ul[@class="Zy_ulTop w-top fl"]/li'
}

# 章节测试判断题选择
test_page_true_or_false_select = {
    'type': 'xpath',
    'string': '//div[@class="Py_tk"]//li//input'
}

# 章节测试更新数据库选项获取
test_select_split_updatedb = {
    'type': 'xpath',
    'string': '//div[@class="TiMu"]//ul'
}

# 获取我的答案
get_my_answer = {
    'type': 'xpath',
    'string': '//div[@class="Py_answer clearfix"]/span[1]'
}

# 章节测验提交 //*[@id="ZyBottom"]/div/div[4]/div[4]/div[5]/a[2]  //*[@id="ZyBottom"]/div[1]/div[4]/div[5]/a[2]
submit_test = {
    'type': 'xpath',
    'string': '//div[@class="ZY_sub clearfix"]/a[2]'
}

# 章节测验确认提交
submit_test_confirm = {
    'type': 'xpath',
    'string': '//*[@id="confirmSubWin"]/div/div/a[1]'
}

# 章节测试加载完成标志
test_load_complete_tag = {
    'type': 'xpath',
    'string': '//*[@id="RightCon"]/div/div/div[1]/h3'
}

# 章节测试加载完成标志iframe
test_load_complete_tag_iframe = [
    {
        'name': 'iframe',
        'index': 0
    },
    {
        'name': 'iframe',
        'index': 0
    },
    {
        'name': 'iframe',
        'index': 0
    }
]

# driver超时设置
timeout = 10

# 播放器iframe
player_iframe = [
    {
        'name': 'iframe',
        'index': 0
    },
    {
        'name': 'iframe',
        'index': 0
    }
]

# 章节测试提交frame
test_submit_iframe = [
    {
        'name': 'iframe',
        'index': 0
    },
    {
        'name': 'iframe',
        'index': 0
    },
    {
        'name': 'iframe',
        'index': 0
    }
]

# 课时列表完成状态
list_complete_status = {
    'type': 'xpath',
    'string': '//span[@class="icon"]/em'
}

# 课时列表完成状态em class属性
list_em_complete_class = 'openlock'
