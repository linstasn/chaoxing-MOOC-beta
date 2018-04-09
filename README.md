## 使用方法：
1. 配置config.ini,文件内有各项说明
2. 命令行运行rest_console.exe文件
3. 发送HTTP请求（ip,port在config.ini Server部分）：

-------------------

### HTTP请求参数
1.  http://ip:port/rest_console   post：{init:标识符}   实例化driver
2. http://ip:port/rest_console  get{search_school:学校名称, instance_name:第一步填写的init标识符}
3. http://ip:port/rest_console  post{select_school:索引(第二步返回的院校索引，0开始), instance_name:第一步填写的init标识符}
4. http://ip:port/rest_console  post{student_num:学号,pwd:密码:ver_code:验证码, instance_name:...}
5. http://ip:port/rest_console  get{get_course:True,instance_name:...}
6. http://ip:port/rest_console  post{browse_watch:索引(第五步获取的课程索引，0开始),instance_name:...}

-------------------

具体使用方法[我的博客](http://www.bankroft.cn/%E8%B6%85%E6%98%9F%EF%BC%88%E5%B0%94%E9%9B%85%EF%BC%9F%EF%BC%89%E5%88%B7%E8%AF%BE-beta/, "my blog")

------------------

### config.ini说明
```ini
[Server]
;配置rest监听地址
ip=127.0.0.1
port=27088

[queryHTTP]
;配置HTTP查询
url_query=http://erya.bankroft.cn/query
url_update=http://erya.bankroft.cn/update

[queryMethod]
;1表示直接连接数据库读取，2表示通过http获取,该项已废除
m=2

[program]
; 配置是否已debug模式启动flask
debug=False

[wechat]
;微信公众号查题，支持多个，以空格分割，使用前请前关注该公众号且回复内容为sharing
;wechat
```