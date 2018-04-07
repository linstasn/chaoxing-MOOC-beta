# coding:utf-8
import logging
import time
import os
import imagehash
import string
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

    def __init__(self, course_lesson, driver):
        threading.Thread.__init__(self)
        self.course_lesson = course_lesson
        self.driver = driver

    def run(self):
        for x in self.course_lesson:
            logger.info(log_template, 'Watch', x['name'], 'Start')
            self.__watch(x['link'])
            logger.info(log_template, 'Watch',  x['name'], 'Complete')
            logger.info(log_template, 'Answer', x['name'], 'Start')
            self.__answer(x['link'])
            logger.info(log_template, 'Answer', x['name'], 'Complete')
            logger.info(log_template, 'Update database', x['name'], 'Start')
            self.__update_db()
            logger.info(log_template, 'Update database', x['name'], 'Complete')
            self.driver.close()

    def __watch(self, lesson):
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.execute_script(self.__js.format(lesson))
        for x in self.driver.window_handles:
            self.driver.switch_to.window(x)
            if x == learn_page_title:
                break
        self.driver.switch_to.default_content()
        # 视频学习部分
        self.driver.find_element(learn_page_video_button['type'], learn_page_video_button['string']).click()
        status = 0
        self.driver.get_screenshot_as_file(os.path.join(folder_temp_path, str(status % 2) + '.png'))
        while True:
            if debug:
                self.driver.get_screenshot_as_file(os.path.join(folder_temp_path, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()).__str__() + '.png'))
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
            self.driver.get_screenshot_as_file(os.path.join(folder_temp_path, str(status % 2) + '.png'))
            if imagehash.average_hash(Image.open(os.path.join(folder_temp_path, str(status % 2) + '.png')).crop(player_screenshot_site)) - imagehash.average_hash(Image.open(os.path.join(folder_temp_path, str((status+1) % 2) + '.png')).crop(player_screenshot_site)) != 0:
                time.sleep(10)
            elif Image.open(os.path.join(folder_temp_path, str(status % 2) + '.png')).crop(video_progress_bar).tobytes() != Image.open(os.path.join(folder_temp_path, str((status+1) % 2) + '.png')).crop(video_progress_bar).tobytes():
                time.sleep(10)
            else:
                self.driver.get_screenshot_as_file(screen_png)
                i1 = Image.open(screen_png)
                # 剪切答题提交
                i2_1 = i1.crop(site_video_test_submit1)
                i2_2 = i1.crop(site_video_test_submit2)
                # 剪切视频暂停按钮
                i3 = i1.crop(site_video_pause_continue)
                # 一行title
                if (imagehash.average_hash(i2_1) - imagehash.average_hash(Image.open(video_test_submit1_1))) <= 5:
                    logger.info(log_template, '视频内答题', '一行title', 'Start')
                    ActionChains(self.driver).move_to_element_with_offset(self.driver.find_element_by_tag_name('object'), 260, 124).click().perform()
                    time.sleep(1)
                    ActionChains(self.driver).move_to_element_with_offset(self.driver.find_element_by_tag_name('object'), 508, 252).click().perform()
                    time.sleep(2)
                    self.driver.get_screenshot_as_file(screen_png)
                    i1 = Image.open(screen_png)
                    # 提交后是否正确
                    i4_1 = i1.crop(size_video_continue1)
                    if (imagehash.average_hash(i4_1) - imagehash.average_hash(Image.open(video_test_continue1))) <= 5:
                        logger.info(log_template, '视频内答题', 'A', 'Right')
                        # 点继续
                        ActionChains(self.driver).move_to_element_with_offset(self.driver.find_element_by_tag_name('object'), 508, 252).click().perform()
                    else:
                        logger.info(log_template, '视频内答题', 'A', 'Wrong')
                        # 选B
                        ActionChains(self.driver).move_to_element_with_offset(self.driver.find_element_by_tag_name('object'), 260, 184).click().perform()
                        time.sleep(1)
                        # 点继续
                        ActionChains(self.driver).move_to_element_with_offset(self.driver.find_element_by_tag_name('object'), 508, 252).click().perform()
                        # 点继续
                        ActionChains(self.driver).move_to_element_with_offset(self.driver.find_element_by_tag_name('object'), 508, 252).click().perform()
                        logger.info(log_template, '视频内答题', 'B', 'Right')
                # 两行title
                elif (imagehash.average_hash(i2_2) - imagehash.average_hash(Image.open(video_test_submit2_1))) <= 5:
                    logger.info(log_template, '视频内答题', '两行title', 'Start')
                    # A
                    ActionChains(self.driver).move_to_element_with_offset(self.driver.find_element_by_tag_name('object'), 260, 167).click().perform()
                    time.sleep(1)
                    # 提交
                    ActionChains(self.driver).move_to_element_with_offset(self.driver.find_element_by_tag_name('object'), 508, 295).click().perform()
                    time.sleep(1)
                    self.driver.get_screenshot_as_file(screen_png)
                    i1 = Image.open(screen_png)
                    i4_2 = i1.crop(size_video_continue2)
                    if (imagehash.average_hash(i4_2) - imagehash.average_hash(Image.open(video_test_continue2))) <= 5:
                        # (260, 167) A
                        # (260, 217) B
                        logger.info(log_template, '视频内答题', 'A', 'Right')
                        # 点继续
                        ActionChains(self.driver).move_to_element_with_offset(self.driver.find_element_by_tag_name('object'), 508, 295).click().perform()
                    else:
                        logger.info(log_template, '视频内答题', 'A', 'Wrong')
                        # B
                        ActionChains(self.driver).move_to_element_with_offset(self.driver.find_element_by_tag_name('object'), 260, 217).click().perform()
                        time.sleep(1)
                        # 提交
                        ActionChains(self.driver).move_to_element_with_offset(self.driver.find_element_by_tag_name('object'), 508, 295).click().perform()
                        time.sleep(1)
                        # 继续
                        ActionChains(self.driver).move_to_element_with_offset(self.driver.find_element_by_tag_name('object'), 508, 295).click().perform()
                elif ((imagehash.average_hash(i3) - imagehash.average_hash(Image.open(video_pause_continue1))) <= 5) or\
                        ((imagehash.average_hash(i3) - imagehash.average_hash(Image.open(video_pause_continue2))) <= 5):
                    logger.info(log_template, '视频播放', '点击播放按钮', '点击')
                    self.driver.switch_to.default_content()
                    for x in player_iframe:
                        self.driver.switch_to.frame(self.driver.find_elements_by_tag_name(x['name'])[x['index']])
                    self.driver.find_element_by_tag_name('object').click()
                else:
                    logger.info(log_template, '视频播放', '刷新页面', '刷新')
                    self.driver.refresh()
        self.driver.close()
        return True

    def __answer(self, lesson):
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.execute_script(self.__js.format(lesson))
        for x in self.driver.window_handles:
            self.driver.switch_to.window(x)
            if x == learn_page_title:
                break
        self.driver.switch_to.default_content()
        # 章节测试答题部分
        self.driver.find_element(learn_page_test_button['type'], learn_page_test_button['string']).click()
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
        titles = self.driver.find_elements(learn_page_test_title['type'], learn_page_test_title['string'])
        selects = self.driver.find_elements(learn_page_test_select_separate['type'], learn_page_test_select_separate['string'])
        selects_text = [x.text.strip().lstrip(string.ascii_uppercase).strip() for x in self.driver.find_elements(learn_page_test_select_separate['type'], learn_page_test_select_separate['string'])]
        # 选项尾指针
        select_num_foot = 0
        judge_num = 0
        tag = 0
        for index, x in enumerate(titles):
            # 选择题首选项
            select_num_head = select_num_foot
            test_type = x.text.strip()[1:4]
            title = x.text.strip()[5:]
            if test_type in ['单选题', '多选题']:
                # 是否选择正确答案
                answer_tag = 0
                select = self.driver.find_elements(learn_page_test_select_gather['type'], learn_page_test_select_gather['string'])[index - tag].text
                logger.info(log_template, '请求服务器/微信公众号', '查询: ' + title, '...')
                right_answer = query_http_server(op='query', test_type=test_type, title=title)
                for y in selects_text[select_num_foot:]:
                    if y in select:
                        if right_answer:
                            if y in right_answer:
                                selects[select_num_foot].click()
                                answer_tag = 1
                                logger.info(log_template, '查询成功', 'Title:  '+title, 'Right answer:  '+'\t'.join(right_answer))
                        select_num_foot += 1
                    else:
                        break
                if not answer_tag:
                    logger.error(log_template, '查询', 'Title:  ' + title, '失败')
                    randint_select = randint(select_num_head, select_num_foot-1)
                    selects[randint_select].click()
                    logger.info(log_template, '随机选择', 'Title: ' + title, str(selects[randint_select].text.replace('\n', ' ').strip()))
                # # 选项字符串
                # try:
                #     select = self.driver.find_elements(learn_page_test_select_gather['type'], learn_page_test_select_gather['string'])[index - tag]
                # except IndexError:
                #     continue
                # # 分割选项
                # sel = [t.strip('、').strip() for t in re.split('[{0}]'.format(self.__select), select.text) if t.strip('、').strip()]
                # right_answer = self.__require_server(op='query', test_type=test_type, title=title)
                # for i, v in enumerate(sel):
                #     if v in right_answer:
                #         self.driver.find_elements(learn_page_test_select_separate['type'], learn_page_test_select_separate['string'])[select_num_foot].click()
                #     logger.info('asdfasdf'+v+'==='+str(select_num_foot))
                #     select_num_foot += 1
            elif test_type == '判断题':
                tag += 1
                right_answer = query_http_server(op='query', test_type=test_type, title=title)
                if right_answer:
                    logger.info(log_template, '判断', 'Title:  ' + title, 'Right answer:  ' + right_answer.__str__())
                    self.driver.find_elements(test_page_true_or_false_select['type'], test_page_true_or_false_select['string'])[judge_num].click()
                else:
                    self.driver.find_elements(test_page_true_or_false_select['type'], test_page_true_or_false_select['string'])[judge_num+1].click()
                    logger.info(log_template, '判断', 'Title:  ' + title, 'Right answer:  ' + right_answer.__str__())
                judge_num += 2
            else:
                logger.error(log_template, '查询', test_type+ '\t暂不支持', '跳过')
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
                logger.error(log_template, '错误', '未知错误', '继续')
                continue
            break
        self.driver.switch_to.default_content()
        for x in learn_page_test_iframe_updatedb:
            # driver.switch_to.frame(driver.find_elements_by_tag_name(x['name'])[x['index']])
            self.driver.switch_to.frame(self.driver.find_elements_by_tag_name(x['name'])[x['index']])
        # 题目题干
        titles = self.driver.find_elements(learn_page_test_title_updatedb['type'], learn_page_test_title_updatedb['string'])
        # 各题得分
        scores = self.driver.find_elements(learn_page_test_score_updatedb['type'], learn_page_test_score_updatedb['string'])
        # 我的回答
        my_answer = self.driver.find_elements(get_my_answer['type'], get_my_answer['string'])
        # 选项内容
        select = self.driver.find_elements(test_select_split_updatedb['type'], test_select_split_updatedb['string'])
        tag = 0
        for index, value in enumerate(scores):
            try:
                if float(value.text.strip('分')) != 0:
                    test_type = titles[index].text.strip()[1:4]
                    title = titles[index].text.replace('\n', ' ').strip()[5:]
                    if test_type in ['单选题', '多选题']:
                        my_ans = re.findall('[{0}]'.format(self.__select), my_answer[index].text)
                        sel = [x.strip('、').strip() for x in re.split('[{0}]'.format(self.__select), select[index-tag].text) if x]
                        right_answer = []
                        for x in my_ans:
                            right_answer.append(sel[self.__select.index(x)])
                        answer = '&'.join(right_answer)
                        if query_http_server(op='update', title=title, test_type=test_type, answer=answer.strip()):
                            logger.info(log_template, '更新题库', title + '\t答案: ' + answer, '\t成功')
                        else:
                            logger.error(log_template, '更新题库', title + '\t答案: ' + answer, '\t失败')
                    elif test_type == '判断题':
                        tag += 1
                        answer = my_answer[index].text.strip('我的答案：').strip()
                        if query_http_server(op='update', title=title, test_type=test_type, answer=answer):
                            logger.info(log_template, '更新题库', title + '\t答案: ' + answer, '\t成功')
                        else:
                            logger.error(log_template, '更新题库', title + '\t答案: ' + answer, '\t失败')
                    else:
                        logger.error(log_template, '更新题库', test_type + '\t暂不支持', '跳过')
                        continue
                else:
                    query_http_server(op='addtitle', title=titles['index'].text.strip())
            except (ValueError, TypeError):
                logger.error(log_template, '错误', '未知错误', '继续')
