# coding:utf-8
from flask import Flask, request, Response
from jsonrpcserver import methods
# from flask_jsonrpc import JSONRPC
from console_erya.config import ip, port
from console_erya import console

AUTHOR = 'Bankroft'

app = Flask(__name__)
# jsonrpc = JSONRPC(app, service_url='/api', enable_web_browsable_api=True)

con = None


@app.route('/api', methods=['POST'])
def index():
    req = request.get_data().decode()
    response = methods.dispatch(req)
    return Response(str(response), response.http_status,
                    mimetype='application/json')


@methods.add
def init():
    global con
    if con:
        return {'code': 404, 'message': '已存在driver'}
    else:
        con = console.Console()
        return {'code': 100, 'message': '成功'}


# @jsonrpc.method('search_school')
@methods.add
def search_school(school_name):
    global con
    if con:
        tmp = con.search_school(school_name)
        return tmp
    else:
        return {'code': 404, 'message': 'driver不存在'}


# @jsonrpc.method('select_school')
@methods.add
def select_school(index):
    global con
    if con:
        try:
            i = int(index)
        except (TypeError, ValueError):
            return {'code': 404, 'message': 'index 不可整数化'}
        tmp = con.select_school(i)
        return tmp
    else:
        return {'code': 404, 'message': 'driver不存在'}


# @jsonrpc.method('get_login_ver_code')
@methods.add
def get_ver_code(refresh):
    global con
    if con:
        return con.get_login_ver_code(refresh=refresh)
    else:
        return {'code': 404, 'message': 'driver不存在'}


# @jsonrpc.method('login')
@methods.add
def login(student_num, pwd, ver_code):
    global con
    if con:
        tmp = con.login(student_num=student_num, password=pwd, code=ver_code)
        return tmp
    else:
        return {'code': 404, 'message': 'driver不存在'}


# @jsonrpc.method('get_course')
@methods.add
def get_course():
    global con
    if con:
        tmp = con.get_course()
        return tmp
    else:
        return {'code': 404, 'message': 'driver不存在'}


# @jsonrpc.method('start')
@methods.add
def start(index):
    global con
    if con:
        try:
            i = int(index)
        except (TypeError, ValueError):
            return {'code': 404, 'message': 'index 不可整数化'}
        con.browse_watch(course_id=i)
        return {'code': 100, 'message': '成功'}
    else:
        return {'code': 404, 'message': 'driver不存在'}


# @jsonrpc.method('test')
@methods.add
def test():
    return 'Test'


if __name__ == '__main__':
    app.run(host=ip, port=port, debug=True)
