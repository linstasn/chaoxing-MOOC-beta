# coding:utf-8
from flask import Flask
from console_erya.config import ip, port, debug
from flask_restful import reqparse, Api, Resource
from console_erya.global_var import globalvar
from console_erya import console
from flask_cors import *
import shutil
import os
import time
import re

r = '(?<!/)&'
app = Flask(__name__)
CORS(app, supports_credentials=True)
api = Api(app)

__author__ = 'bankroft'
__version__ = '0.34 debug'
__blog__ = 'https://www.bankroft.cn'


class Main(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('search_school', type=str, location='args')
        parser.add_argument('instance_name', type=str, location='args')
        parser.add_argument('get_course', type=str, location='args')
        # parser.add_argument('get_ver_code', type=bool, location='args')
        parser.add_argument('author', type=str, location='args')
        args = parser.parse_args()
        if args['author']:
            return [{'author': __author__}]
        if args['instance_name']:
            con = globalvar.get(args['instance_name'])
            if con:
                if args['search_school']:
                        tmp = con.search_school(args['search_school'])
                        return [{'status': 100, 'message': '', 'data': tmp}]
                # elif args['get_ver_code'] == False:
                #     if con.status['select_school'] and not con.status['login']:
                #         tmp = con.get_login_ver_code()
                #         return [{'status': 100, 'message': '先登陆', 'data': tmp}]
                #     else:
                #         return [{'status': 404, 'message': '步骤错误'}]
                # elif args['get_ver_code']:
                #     if con.status['select_school'] and not con.status['login']:
                #         tmp = con.get_login_ver_code(refresh=True)
                #         return [{'status': 100, 'message': '先登陆', 'data': tmp}]
                #     else:
                #         return [{'status': 404, 'message': '步骤错误'}]
                elif args['get_course']:
                    if con.status['login']:
                        tmp = con.get_course()
                        return [{'status': 100, 'message': '', 'data': tmp}]
                    else:
                        return [{'status': 404, 'message': '先登陆'}]
                else:
                    return [{'status': 404, 'message': '参数错误'}]
            else:
                return [{'status': 404, 'message': '实例不存在'}]
        else:
            return [{'status': 404, 'message': '参数错误'}]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('select_school', type=int, location='form')
        parser.add_argument('instance_name', type=str, location='form')
        parser.add_argument('student_num', type=str, location='form')
        parser.add_argument('browse_watch', type=int, location='form')
        parser.add_argument('pwd', type=str, location='form')
        parser.add_argument('ver_code', type=str, location='form')
        parser.add_argument('init', type=str, help='添加实例名称', location='form')
        args = parser.parse_args()
        if args['init']:
            if globalvar.get(args['init']):
                con = globalvar.get(args['instance_name'])
                con.quit()
            globalvar.add({args['init']: console.Console()})
            return [{'status': 100, 'message': ''}]
        if args['instance_name']:
            con = globalvar.get(args['instance_name'])
            if con:
                if args['select_school'] is not None:
                    if con.status['search_school']:
                        # 先搜索
                        return [{'status': 100, 'message': '', 'data': con.select_school(args['select_school'])}]
                    else:
                        # 未搜索就选择学校
                        return [{'status': 404, 'message': '先搜索学校'}]
                elif args['student_num'] and args['pwd'] and args['ver_code']:
                    if con.status['select_school']:
                        tmp = con.login(args['student_num'], args['pwd'], args['ver_code'])
                        if tmp[1]:
                            return [{'status': 100, 'message': '', 'data': tmp[0]}]
                        else:
                            return [{'status': 404, 'message': tmp[0]}]
                    else:
                        return [{'status': 404, 'message': '先选择学校'}]
                elif args['browse_watch'] is not None:
                    return [{'status': 100, 'message': '', 'data': con.browse_watch(args['browse_watch'])}]
                else:
                    return [{'status': 404, 'message': '参数错误'}]
            else:
                return [{'status': 404, 'message': '实例不存在'}]
        else:
            return [{'status': 404, 'message': '参数错误'}]


class GetInfo(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('start', type=int, location='args')
        parser.add_argument('status', type=str, location='args')
        args = parser.parse_args()
        if args['status']:
            return [{'status': 100, 'message': '正在运行'}]
        if args['start']:
            start = int(args['start'])
            data = []
            shutil.copyfile('erya.log', 'erya.log.tmp')
            with open('erya.log.tmp', encoding='utf-8') as f:
                for x in f.readlines():
                    try:
                        t = time.mktime(time.strptime(x.split(',')[0], '%Y-%m-%d %H:%M:%S'))
                        if t > start:
                            data.append(re.split(r, x)[1:])
                    except:
                        continue
            os.remove('erya.log.tmp')
            return [{'status': 100, 'message': '', 'data': data}]
        else:
            return [{'status': 404, 'message': '参数错误'}]


api.add_resource(Main, '/rest_console')
# 参数待定
api.add_resource(GetInfo, '/getinfo')


if __name__ == '__main__':
    print('='*60)
    print('|{0}Author:%9s{1}|'.format(' '*20, ' '*22) % __author__)
    print('|{0}Version:%10s{1}|'.format(' '*20, ' '*20) % __version__)
    print('|{0}Blog:%24.24s{1}|'.format(' '*20, ' '*9) % __blog__)
    print('='*60)
    app.run(host=ip, port=port, debug=debug)
    # app.run(debug=True)
# from xmlrpc.server import SimpleXMLRPCServer
# from xmlrpc.server import SimpleXMLRPCRequestHandler
# from console_erya.console import Console
#
#
# # Restrict to a particular path.
# class RequestHandler(SimpleXMLRPCRequestHandler):
#     rpc_paths = ('/RPC2',)
#
#
# from jsonrpc import JSONRPCResponseManager
#
#
# if __name__ == '__main__':
#     with SimpleXMLRPCServer(("localhost", 8000),
#                             requestHandler=RequestHandler) as server:
#
#         server.register_instance(Console())
#
#         # Run the server's main loop
#         server.serve_forever()
