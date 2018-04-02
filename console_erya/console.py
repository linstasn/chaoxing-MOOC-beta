# coding:utf-8
import time
from PIL import Image
from selenium import webdriver, common
from .config_dev import *
from .config_user import chrome_drive_path
import os
from .automaticcompletion import AutomaticCompletion
from random import sample
import string


class Console:
    status = {
        'init': 0,
        'search_school': 0,
        'select_school': 0,
        'login': 0,
        'get_course': 0,
        'browser_watch': 0
    }
    __select_school_result = []
    __course = []
    __course_lesson = []

    def __init__(self):
        prefs = {
            "profile.default_content_setting_values.plugins": 1,
            "profile.content_settings.plugin_whitelist.adobe-flash-player": 1,
            "profile.content_settings.exceptions.plugins.*,*.per_resource.adobe-flash-player": 1,
            "PluginsAllowedForUrls": "https://chaoxing.com"
        }
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(chrome_drive_path, chrome_options=options)
        self.driver.implicitly_wait(timeout)
        self.driver.set_window_size(1920, 1080)
        self.driver.get(entrance_url)
        self.status['init'] = 1
        self.get_login_ver_code()

    def quit(self):
        self.driver.quit()
        del self

    def login(self, student_num, password, code):
        self.operate(login_code['type'], login_code['string'], 'send_key', code)
        self.operate(login_username['type'], login_username['string'], 'send_key', student_num)
        self.operate(login_password['type'], login_password['string'], 'send_key', password)
        self.operate(login_button['type'], login_button['string'], 'click')
        try:
            name = self.driver.find_element(login_ver['type'], login_ver['string']).text
        except common.exceptions.NoSuchElementException:
            try:
                result_text = self.driver.find_element(login_result['type'], login_result['string']).text
            except common.exceptions.NoSuchElementException:
                return False, False
            return str(result_text), False
        self.status['login'] = 1
        return str(name), True

    def search_school(self, school, id_: int=-1):
        """
        院校选择
        :param school:
        :param id_: 搜索结果
        :return:
        """
        self.operate(select_school_button['type'], select_school_button['string'], 'click')  # 选择院校
        self.operate(select_school_search['type'], select_school_search['string'], 'send_key', school)  # 院校搜索关键词输入
        self.operate(select_school_search_button['type'], select_school_search_button['string'], 'click')  # 院校搜索
        self.__select_school_result = self.driver.find_elements(select_school_result['type'], select_school_result['string'])
        self.status['search_school'] = 1
        return [x.text for x in self.__select_school_result]

    def select_school(self, id_: int):
        try:
            self.__select_school_result[id_].click()
        except (TypeError, IndexError):
            return False
        self.status['select_school'] = 1
        return True

    def get_login_ver_code(self, refresh=False):
        """
        获取验证码图片，保存为code.png
        :param refresh: 是否刷新
        :return:
        """
        filename = 'vercode.png'
        if refresh:
            filename = ''.join(sample(string.ascii_letters, 8)) + '.png'
            self.operate(refresh_code['type'], refresh_code['string'], 'click')
        self.driver.get_screenshot_as_file('code.png')  # 保存登陆界面截图
        a = self.driver.find_element_by_id('numVerCode')  # 定位验证码
        l = a.location['x'] + 1
        t = a.location['y'] + 1
        r = a.location['x'] + a.size['width']
        b = a.location['y'] + a.size['height']
        im = Image.open('code.png')
        im = im.crop((l, t, r, b))
        im.save(os.path.join(path_vercode, filename))
        try:
            os.remove('code.png')
        except OSError:
            pass
        return filename

    def get_course(self):
        self.__course = []
        self.driver.switch_to.default_content()
        for x in course_name_list_frame:
            # driver.switch_to.frame(driver.find_elements_by_tag_name(x['name'])[x['index']])
            self.driver.switch_to.frame(self.driver.find_elements_by_tag_name(x['name'])[x['index']])
        for x in self.driver.find_elements(course_name_list['type'], course_name_list['string']):
            if not x.text:
                continue
            try:
                if x.text.split(remove_irrelevant_course[0])[remove_irrelevant_course[1]].strip() == remove_irrelevant_course[2]:
                    continue
                self.__course.append(x)
            except IndexError:
                continue
        self.status['get_course'] = 1
        return [x.text for x in self.__course]

    def browse_watch(self, course_id):
        try:
            course_id = int(course_id)
        except (TypeError, ValueError):
            return False
        if (course_id >= (len(self.__course) - 1)) or (course_id < 0):
            return False
        course = self.__course[course_id]
        course.click()
        time.sleep(5)
        for x in self.driver.window_handles:
            self.driver.switch_to.window(x)
            if self.driver.title == course_page_title:
                break
        # 是否已完成
        complete_status = self.driver.find_elements(list_complete_status['type'], list_complete_status['string'])
        # 课时链接、课时名称、完成状态
        for x, y, z in zip(self.driver.find_elements(course_lesson_link['type'], course_lesson_link['string']), self.driver.find_elements(course_lesson_name['type'], course_lesson_name['string']), self.driver.find_elements(list_complete_status['type'], list_complete_status['string'])):
            if z.get_attribute('class') == list_em_complete_class:
                continue
            tmp = {'name': y.text.replace('\n', '').strip(), 'link': x.get_attribute('href')}
            self.__course_lesson.append(tmp)
        self.driver.close()
        AutomaticCompletion(course_lesson=self.__course_lesson, driver=self.driver).start()
        self.status['browser_watch'] = 1
        return True

    def operate(self, type_, string, op, args=None):
        """
        部分点击、输入等操作
        :param type_:
        :param string:
        :param op:
        :param args:
        :return:
        """
        if op == 'click':
            self.driver.find_element(by=type_, value=string).click()
        elif op == 'send_key':
            self.driver.find_element(by=type_, value=string).clear()
            self.driver.find_element(by=type_, value=string).send_keys(args)

