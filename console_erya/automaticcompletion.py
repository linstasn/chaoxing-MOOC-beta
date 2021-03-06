# coding:utf-8
import time
import os
import imagehash
import re
import threading
from .log import *
from .config import *
from .questions import query_http_server
from PIL import Image
from selenium.webdriver.common.action_chains import ActionChains
from selenium import common
from random import randint


class AutomaticCompletion(threading.Thread):
    # 生成choices(string.printable, k=16)
    __select = ''.join([chr(x) for x in range(65, 91)])
    __course = []
    __js = 'window.open("{0}");'

    def __init__(self, driver):
        threading.Thread.__init__(self)
        # self.course_lesson = course_lesson
        self.driver = driver

    def run(self):
        last_lesson = None
        for x in not_completed_lesson['string']:
            while True:
                try:
                    self.driver.switch_to.default_content()
                    # self.driver.find_element('xpath', x).click()
                    ActionChains(self.driver).click(self.driver.find_element(not_completed_lesson['type'], x)).perform()
                    time.sleep(5)
                    if last_lesson == self.driver.find_element(lesson_name['type'], lesson_name['string']).text:
                        logger.error(log_template, '出错', '无法检测视频状态，手动观看【{0}】,输入y确认已完成观看'.format(last_lesson), '结束刷课')
                        while True:
                            if input('是否已手动观看完成？(y)').strip() == 'y':
                                break
                    last_lesson = self.driver.find_element('xpath', '//div[@id="mainid"]/h1').text
                    if self.__watch():
                        last_lesson = None
                    self.__answer()
                    self.__update_db()
                    time.sleep(10)
                except common.exceptions.NoSuchElementException:
                    break
        # for x in self.course_lesson:
        #     logger.info(log_template, 'Watch', x['name'], 'Start')
        #     self.__watch(x['link'])
        #     logger.info(log_template, 'Watch',  x['name'], 'Complete')
        #     logger.info(log_template, 'Answer', x['name'], 'Start')
        #     self.__answer(x['link'])
        #     logger.info(log_template, 'Answer', x['name'], 'Complete')
        #     logger.info(log_template, 'Update database', x['name'], 'Start')
        #     self.__update_db()
        #     logger.info(log_template, 'Update database', x['name'], 'Complete')
        #     self.driver.close()

    def __watch(self):
        # self.driver.switch_to.window(self.driver.window_handles[0])
        # self.driver.execute_script(self.__js.format(lesson))
        # for x in self.driver.window_handles:
        #     self.driver.switch_to.window(x)
        #     if x == learn_page_title:
        #         break
        self.driver.switch_to.default_content()
        # 视频学习部分
        try:
            self.driver.find_element(learn_page_video_button['type'], learn_page_video_button['string']).click()
        except common.exceptions.NoSuchElementException:
            return True
        status = 0
        self.__screenshot_video(os.path.join(folder_temp_path, str(status % 2) + '.png'))
        while True:
            # if debug:
            #     self.driver.get_screenshot_as_file(os.path.join(folder_temp_path, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()).__str__() + '.png'))
            status += 1
            try:
                self.driver.switch_to.default_content()
                for x in learn_page_video_part_iframe:
                    # driver.switch_to.frame(driver.find_elements_by_tag_name(x['name'])[x['index']])
                    self.driver.switch_to.frame(self.driver.find_elements_by_tag_name(x['name'])[x['index']])
                self.driver.find_element(video_complete_status['type'], video_complete_status['string'])
                break
            except common.exceptions.NoSuchElementException:
                pass
            self.driver.switch_to.default_content()
            for x in learn_page_video_iframe:
                # driver.switch_to.frame(driver.find_elements_by_tag_name(x['name'])[x['index']])
                self.driver.switch_to.frame(self.driver.find_elements_by_tag_name(x['name'])[x['index']])
            self.__screenshot_video(os.path.join(folder_temp_path, str(status % 2) + '.png'))
            if imagehash.average_hash(Image.open(os.path.join(folder_temp_path, str(status % 2) + '.png'))) - imagehash.average_hash(Image.open(os.path.join(folder_temp_path, str((status+1) % 2) + '.png'))) != 0:
                time.sleep(5)
            elif Image.open(os.path.join(folder_temp_path, str(status % 2) + '.png')).crop(video_progress_bar1).tobytes() != Image.open(os.path.join(folder_temp_path, str((status + 1) % 2) + '.png')).crop(video_progress_bar1).tobytes():
                time.sleep(5)
            else:
                self.__screenshot_video(screen_png)
                i1 = Image.open(screen_png)
                # 剪切答题提交
                # 两个选项一行title验证
                i2_1 = i1.crop(location_video_test_submit1_1)
                # 两个选项两行title验证
                i2_2 = i1.crop(location_video_test_submit2_1)
                # 两个选项三行title验证
                i2_3 = i1.crop(location_video_test_submit3_1)
                # 三个选项一行title验证
                i3_1 = i1.crop(location_video_test_submit1_3)
                # 四个选项一行title
                i4_1 = i1.crop(location_video_test_submit1_4)
                # i2_2 = i1.crop(site_video_test_submit2)
                # i2_3 = i1.crop(site_video_test_submit3)
                # 两个选项一行title
                if (imagehash.average_hash(i2_1) - imagehash.average_hash(Image.open(video_test_submit1_1))) <= 8:
                    # (imagehash.average_hash(i2_1) - imagehash.average_hash(Image.open(video_test_submit1_2))) <= 5
                    # (imagehash.average_hash(i2_3) - imagehash.average_hash(Image.open(video_test_submit1_3))) <= 5:
                    logger.info(log_template, '视频内答题', '一行title', 'Start')
                    # A
                    ActionChains(self.driver).move_to_element_with_offset(self.driver.find_element_by_tag_name('object'), 260, 124).click().perform()
                    time.sleep(1)
                    # 提交
                    ActionChains(self.driver).move_to_element_with_offset(self.driver.find_element_by_tag_name('object'), 508, 252).click().perform()
                    time.sleep(1)
                    # B
                    ActionChains(self.driver).move_to_element_with_offset(self.driver.find_element_by_tag_name('object'), 260, 184).click().perform()
                    time.sleep(1)
                    # 提交
                    ActionChains(self.driver).move_to_element_with_offset(self.driver.find_element_by_tag_name('object'), 508, 252).click().perform()
                    time.sleep(1)
                    # 继续
                    ActionChains(self.driver).move_to_element_with_offset(self.driver.find_element_by_tag_name('object'), 508, 252).click().perform()
                    time.sleep(1)
                # 两个选项两行title
                elif (imagehash.average_hash(i2_2) - imagehash.average_hash(Image.open(video_test_submit2_1))) <= 5:
                    logger.info(log_template, '视频内答题', '两行title', 'Start')
                    # A
                    ActionChains(self.driver).move_to_element_with_offset(self.driver.find_element_by_tag_name('object'), 260, 167).click().perform()
                    time.sleep(1)
                    # 提交
                    ActionChains(self.driver).move_to_element_with_offset(self.driver.find_element_by_tag_name('object'), 508, 295).click().perform()
                    time.sleep(1)
                    # B
                    ActionChains(self.driver).move_to_element_with_offset(self.driver.find_element_by_tag_name('object'), 260, 217).click().perform()
                    time.sleep(1)
                    # 提交
                    ActionChains(self.driver).move_to_element_with_offset(self.driver.find_element_by_tag_name('object'), 508, 295).click().perform()
                    time.sleep(1)
                    # 提交
                    ActionChains(self.driver).move_to_element_with_offset(self.driver.find_element_by_tag_name('object'), 508, 295).click().perform()
                    time.sleep(1)
                    # self.driver.get_screenshot_as_file(screen_png)
                    # i1 = Image.open(screen_png)
                    # i4_2 = i1.crop(size_video_continue2)
                    # if (imagehash.average_hash(i4_2) - imagehash.average_hash(Image.open(video_test_continue2))) <= 5:
                    #     # (260, 167) A
                    #     # (260, 217) B
                    #     logger.info(log_template, '视频内答题', 'A', 'Right')
                    #     # 点继续
                    #     ActionChains(self.driver).move_to_element_with_offset(self.driver.find_element_by_tag_name('object'), 508, 295).click().perform()
                    # else:
                    #     logger.info(log_template, '视频内答题', 'A', 'Wrong')
                    #     # B
                    #     ActionChains(self.driver).move_to_element_with_offset(self.driver.find_element_by_tag_name('object'), 260, 217).click().perform()
                    #     time.sleep(1)
                    #     # 提交
                    #     ActionChains(self.driver).move_to_element_with_offset(self.driver.find_element_by_tag_name('object'), 508, 295).click().perform()
                    #     time.sleep(1)
                    #     # 继续
                    #     ActionChains(self.driver).move_to_element_with_offset(self.driver.find_element_by_tag_name('object'), 508, 295).click().perform()
                # 两个选项三行title
                elif (imagehash.average_hash(i2_3) - imagehash.average_hash(Image.open(video_test_submit3_1))) <= 5:
                    logger.info(log_template, '视频内答题', '三行title', 'Start')
                    # A
                    ActionChains(self.driver).move_to_element_with_offset(self.driver.find_element_by_tag_name('object'), 260, 191).click().perform()
                    time.sleep(1)
                    # 提交
                    ActionChains(self.driver).move_to_element_with_offset(self.driver.find_element_by_tag_name('object'), 508, 319).click().perform()
                    time.sleep(1)
                    # B
                    ActionChains(self.driver).move_to_element_with_offset(self.driver.find_element_by_tag_name('object'), 260, 241).click().perform()
                    time.sleep(1)
                    # 提交
                    ActionChains(self.driver).move_to_element_with_offset(self.driver.find_element_by_tag_name('object'), 508, 319).click().perform()
                    time.sleep(1)
                    # 提交
                    ActionChains(self.driver).move_to_element_with_offset(self.driver.find_element_by_tag_name('object'), 508, 319).click().perform()
                    time.sleep(1)
                # 三个选项一行title
                elif (imagehash.average_hash(i3_1) - imagehash.average_hash(Image.open(video_test_submit1_3))) <= 5:
                    # A
                    ActionChains(self.driver).move_to_element_with_offset(self.driver.find_element_by_tag_name('object'), 260, 135).click().perform()
                    time.sleep(1)
                    # 继续
                    ActionChains(self.driver).move_to_element_with_offset(self.driver.find_element_by_tag_name('object'), 508, 314).click().perform()
                    time.sleep(1)
                    # B
                    ActionChains(self.driver).move_to_element_with_offset(self.driver.find_element_by_tag_name('object'), 260, 185).click().perform()
                    time.sleep(1)
                    # 继续
                    ActionChains(self.driver).move_to_element_with_offset(self.driver.find_element_by_tag_name('object'), 508, 314).click().perform()
                    time.sleep(1)
                    # C
                    ActionChains(self.driver).move_to_element_with_offset(self.driver.find_element_by_tag_name('object'), 260, 237).click().perform()
                    time.sleep(1)
                    # 继续
                    ActionChains(self.driver).move_to_element_with_offset(self.driver.find_element_by_tag_name('object'), 508, 314).click().perform()
                    time.sleep(1)
                    # 继续
                    ActionChains(self.driver).move_to_element_with_offset(self.driver.find_element_by_tag_name('object'), 508, 314).click().perform()
                    time.sleep(1)
                # 四个选项一行title
                elif (imagehash.average_hash(i4_1) - imagehash.average_hash(Image.open(video_test_submit1_4))) <= 5:
                    logger.info(log_template, '视频内答题', '四个选项一行title', 'Start')
                    # A
                    ActionChains(self.driver).move_to_element_with_offset(self.driver.find_element_by_tag_name('object'), 260, 135).click().perform()
                    time.sleep(1)
                    # 继续
                    ActionChains(self.driver).move_to_element_with_offset(self.driver.find_element_by_tag_name('object'), 508, 365).click().perform()
                    time.sleep(1)
                    # B
                    ActionChains(self.driver).move_to_element_with_offset(self.driver.find_element_by_tag_name('object'), 260, 186).click().perform()
                    time.sleep(1)
                    # 继续
                    ActionChains(self.driver).move_to_element_with_offset(self.driver.find_element_by_tag_name('object'), 508, 365).click().perform()
                    time.sleep(1)
                    # C
                    ActionChains(self.driver).move_to_element_with_offset(self.driver.find_element_by_tag_name('object'), 260, 237).click().perform()
                    time.sleep(1)
                    # 继续
                    ActionChains(self.driver).move_to_element_with_offset(self.driver.find_element_by_tag_name('object'), 508, 365).click().perform()
                    time.sleep(1)
                    # D
                    ActionChains(self.driver).move_to_element_with_offset(self.driver.find_element_by_tag_name('object'), 260, 288).click().perform()
                    time.sleep(1)
                    # 继续
                    ActionChains(self.driver).move_to_element_with_offset(self.driver.find_element_by_tag_name('object'), 508, 365).click().perform()
                    time.sleep(1)
                # 四个选项两行title，无图片无法识别，待定
                # elif (imagehash.average_hash(i4_1) - imagehash.average_hash(Image.open(video_test_submit1_4))) <= 5:
                #     logger.info(log_template, '视频内答题', '四个选项两行title', 'Start')
                #     # A
                #     ActionChains(self.driver).move_to_element_with_offset(self.driver.find_element_by_tag_name('object'), 260, 167).click().perform()
                #     time.sleep(1)
                #     # 继续
                #     ActionChains(self.driver).move_to_element_with_offset(self.driver.find_element_by_tag_name('object'), 508, 397).click().perform()
                #     time.sleep(1)
                #     # B
                #     ActionChains(self.driver).move_to_element_with_offset(self.driver.find_element_by_tag_name('object'), 260, 218).click().perform()
                #     time.sleep(1)
                #     # 继续
                #     ActionChains(self.driver).move_to_element_with_offset(self.driver.find_element_by_tag_name('object'), 508, 397).click().perform()
                #     time.sleep(1)
                #     # C
                #     ActionChains(self.driver).move_to_element_with_offset(self.driver.find_element_by_tag_name('object'), 260, 269).click().perform()
                #     time.sleep(1)
                #     # 继续
                #     ActionChains(self.driver).move_to_element_with_offset(self.driver.find_element_by_tag_name('object'), 508, 397).click().perform()
                #     time.sleep(1)
                #     # D
                #     ActionChains(self.driver).move_to_element_with_offset(self.driver.find_element_by_tag_name('object'), 260, 320).click().perform()
                #     time.sleep(1)
                #     # 继续
                #     ActionChains(self.driver).move_to_element_with_offset(self.driver.find_element_by_tag_name('object'), 508, 397).click().perform()
                #     time.sleep(1)
                elif (imagehash.average_hash(i1.crop(location_video_pause_continue1)) - imagehash.average_hash(Image.open(video_pause_continue1))) <= 8:
                    logger.info(log_template, '视频播放', '点击播放按钮', '点击')
                    self.driver.switch_to.default_content()
                    for x in player_iframe:
                        self.driver.switch_to.frame(self.driver.find_elements_by_tag_name(x['name'])[x['index']])
                    self.driver.find_element_by_tag_name('object').click()
                else:
                    # logger.info(log_template, '视频播放', '刷新页面', '刷新')
                    # self.driver.refresh()
                    return False
        # self.driver.close()
        return True

    def __answer(self):
        sleep_time = 10
        self.driver.switch_to.default_content()
        # 章节测试答题部分
        try:
            self.driver.find_element(learn_page_test_button['type'], learn_page_test_button['string']).click()
        except common.exceptions.NoSuchElementException:
            return True
        start_time = time.time()
        while True:
            if time.time() - start_time > 20:
                logger.error(log_template, '回答', '检测答题', '超时')
                return False
            time.sleep(5)
            self.driver.switch_to.default_content()
            try:
                for x in test_load_complete_tag_iframe:
                    # driver.switch_to.frame(driver.find_elements_by_tag_name(x['name'])[x['index']])
                    self.driver.switch_to.frame(self.driver.find_elements_by_tag_name(x['name'])[x['index']])
            except IndexError:
                continue
            try:
                # 页面是否加载完成
                self.driver.find_element(test_load_complete_tag['type'], test_load_complete_tag['string'])
            except common.exceptions.NoSuchElementException:
                logger.error(log_template, '错误', '未知错误', '继续')
                continue
            break
        self.driver.switch_to.default_content()
        for x in learn_page_test_status_iframe:
            # driver.switch_to.frame(driver.find_elements_by_tag_name(x['name'])[x['index']])
            self.driver.switch_to.frame(self.driver.find_elements_by_tag_name(x['name'])[x['index']])
        try:
            # xpath可能有问题
            self.driver.find_element(test_complete_stataus['type'], test_complete_stataus['string'])
            return True
        except common.exceptions.NoSuchElementException:
            pass
        self.driver.switch_to.default_content()
        for x in learn_page_test_iframe:
            # driver.switch_to.frame(driver.find_elements_by_tag_name(x['name'])[x['index']])
            self.driver.switch_to.frame(self.driver.find_elements_by_tag_name(x['name'])[x['index']])
        tmp = self.driver
        while True:
            try:
                tmp = tmp.find_element_by_class_name('TiMu')
            except common.exceptions.NoSuchElementException:
                break
            title = tmp.find_element_by_class_name('clearfix').text.strip('1234567890').replace('\n', '').strip()
            test_type = title[1:4]
            logger.info(log_template, '正在请求服务器/微信公众号', '查询: ' + title, '...')
            right_answer = query_http_server(op='query', test_type=test_type, title=title[5:])
            if test_type == '判断题':
                if right_answer:
                    logger.info(log_template, '判断', 'Title:  ' + title, 'answer:  ' + '正确')
                    tmp.find_elements_by_tag_name('ul')[0].find_elements_by_tag_name('label')[0].click()
                else:
                    logger.info(log_template, '判断', 'Title:  ' + title, 'answer:  ' + '错误')
                    tmp.find_elements_by_tag_name('ul')[0].find_elements_by_tag_name('label')[1].click()
            elif test_type in ['单选题', '多选题']:
                tag = 0
                if right_answer:
                    logger.info(log_template, '查询到', 'Title:  ' + title, '答案:  ' + '\t'.join(right_answer))
                    for x in tmp.find_elements_by_tag_name('ul')[0].find_elements_by_tag_name('li'):
                        if x.text.split('\n')[1].strip() in right_answer:
                            tag = 1
                            x.click()
                if not tag:
                    logger.info(log_template, '查询答案失败', 'Title:  ' + title, '随机选择一项')
                    sleep_time = 60*noanswer_sleep
                    # 未搜索到该题目答案，随机选择一项
                    tmp.find_elements_by_tag_name('ul')[0].find_elements_by_tag_name('li')[randint(0, len(tmp.find_elements_by_tag_name('ul')[0].find_elements_by_tag_name('li'))-1)].click()
            else:
                logger.error(log_template, '查询', test_type + '\t暂不支持', '跳过')
        # 提交部分
        logger.info(log_template, '提交章节测试', '如果有未查到的单/多选题会等待{0}分钟提交，默认10s后提交'.format(noanswer_sleep.__str__()), '等待')
        time.sleep(sleep_time)
        self.driver.switch_to.default_content()
        for x in test_submit_iframe:
            self.driver.switch_to.frame(self.driver.find_elements_by_tag_name(x['name'])[x['index']])
        self.driver.find_element(submit_test['type'], submit_test['string']).click()
        while True:
            if self.driver.find_element(submit_test_confirm['type'], submit_test_confirm['string']).text != '确定':
                time.sleep(2)
            else:
                break
        self.driver.find_element(submit_test_confirm['type'], submit_test_confirm['string']).click()
        logger.info(log_template, '提交章节测试', '确认', '提交')

    def __update_db(self):
        start_time = time.time()
        while True:
            if time.time() - start_time > 20:
                logger.error(log_template, '更新题库', '检测', '超时')
                return False
            time.sleep(5)
            self.driver.switch_to.default_content()
            try:
                for x in test_load_complete_tag_iframe:
                    # driver.switch_to.frame(driver.find_elements_by_tag_name(x['name'])[x['index']])
                    self.driver.switch_to.frame(self.driver.find_elements_by_tag_name(x['name'])[x['index']])
            except IndexError:
                continue
            try:
                # 页面是否加载完成
                self.driver.find_element(test_load_complete_tag['type'], test_load_complete_tag['string'])
            except common.exceptions.NoSuchElementException:
                logger.error(log_template, '错误', '更新题库页面加载未知错误', '继续')
                continue
            break
        self.driver.switch_to.default_content()
        for x in learn_page_test_iframe_updatedb:
            # driver.switch_to.frame(driver.find_elements_by_tag_name(x['name'])[x['index']])
            self.driver.switch_to.frame(self.driver.find_elements_by_tag_name(x['name'])[x['index']])
        for x in self.driver.find_elements_by_class_name('TiMu'):
            try:
                # 选择题正确icon
                right_or_wrong = x.find_element_by_tag_name('form').find_element_by_tag_name('div').find_element_by_tag_name('i').get_attribute('class')
            except (common.exceptions.NoSuchElementException, IndexError):
                # 判断题正确icon
                right_or_wrong = x.find_elements_by_tag_name('div')[4].find_elements_by_tag_name('i')[1].get_attribute('class')
            if right_or_wrong == 'fr dui':
                title = x.find_elements_by_tag_name('div')[1].text.strip().replace('\n', '')
                my_answer = x.find_elements_by_tag_name('div')[4].text.split('\n')[0].strip('我的答案：').strip()
                test_type = title[1:4]
                if test_type == '判断题':
                    if query_http_server(op='update', title=title[5:], test_type=test_type, answer=my_answer.strip()):
                        logger.info(log_template, '更新题库', title + '\t答案: ' + my_answer, '\t成功')
                    else:
                        logger.info(log_template, '更新题库', title + '\t答案: ' + my_answer, '\t失败')
                elif test_type in ['单选题', '多选题']:
                    ma = re.findall('[{0}]'.format(self.__select), my_answer)
                    r = []
                    for y in ma:
                        r.append(x.find_elements_by_tag_name('li')[self.__select.index(y)].text.strip(self.__select).strip('、').strip())
                    answer = '&'.join(r)
                    if query_http_server(op='update', title=title[5:], test_type=test_type, answer=answer.strip()):
                        logger.info(log_template, '更新题库', title + '\t答案: ' + answer, '\t成功')
                    else:
                        logger.info(log_template, '更新题库', title + '\t答案: ' + answer, '\t失败')
                else:
                    logger.error(log_template, '更新题库', '暂不支持：' + test_type, '跳过')
            elif right_or_wrong == 'fr bandui':
                pass

    def __screenshot_video(self, filename):
        self.driver.get_screenshot_as_file('tmp.png')
        self.driver.switch_to.default_content()
        for x in learn_page_video_iframe:
            # driver.switch_to.frame(driver.find_elements_by_tag_name(x['name'])[x['index']])
            self.driver.switch_to.frame(self.driver.find_elements_by_tag_name(x['name'])[x['index']])
        tmp = self.driver.find_element_by_tag_name('object')
        i = Image.open('tmp.png')
        i.crop(
            (
                tmp.location_once_scrolled_into_view['x'],
                tmp.location_once_scrolled_into_view['y'],
                tmp.location_once_scrolled_into_view['x'] + tmp.size['width'],
                tmp.location_once_scrolled_into_view['y'] + tmp.size['height']
            )
        ).save(filename)
        try:
            os.remove('tmp.png')
        except (FileNotFoundError, PermissionError):
            pass
