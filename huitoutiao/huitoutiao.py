#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################
# 判断一个完整新闻包含元素
# 1. com.cashtoutiao:id/ll_view
# 2. com.cashtoutiao:id/tv_title
# 3. com.cashtoutiao:id/tv_src
#
# 判断是否为广告
# find_elements_by_id("com.cashtoutiao:id/tv_src")[0].text = 广告
#
# 判断视频
# find_elements_by_id("com.cashtoutiao:id/alivc_player_state").exists()
###############################

from appium import webdriver
from libs.settings import *
import time
import datetime


class HuiTouTiao():
    def __init__(self):

        self.desired_caps = {
            'platformName': 'Android',
            'deviceName': '127.0.0.1:62001',
            'platformVersion': '4.4.2',
            # apk包名
            'appPackage': 'com.cashtoutiao',
            # apk的launcherActivity
            'appActivity': 'com.cashtoutiao.common.ui.SplashActivity',
            # 定义appium 无操作超时时间
            'newCommandTimeout': "2000000"
        }
        self.appium_address = 'http://127.0.0.1:4723/wd/hub'
        self.timeout = 15
        self.news_list = []

        self.__start_app()

    def __start_app(self):
        # start huitoutiao app
        self.driver = webdriver.Remote(self.appium_address, self.desired_caps)
        # 等待资源加载，最多等待15s
        # self.driver.implicitly_wait(5)
        time.sleep(5)

    def __login_app(self):
        # 登陆app
        username = self.driver.find_elements_by_id(EL_USERNAME)
        password = self.driver.find_elements_by_id(EL_PASSWORD)
        if username:
            print("Login HuiTouTiao App！！！")
            username[0].send_keys(USERNAME)
            password[0].send_keys(PASSWORD)
            self.driver.find_elements_by_id(EL_LOGIN_BUTTON)[0].click()
            # 等待资源加载
            # self.driver.implicitly_wait(5)
            time.sleep(3)
        self.start_time = datetime.datetime.now()
        print("##############阅读开始时间：{0}".format(self.start_time))

    def watch_news(self):
        """
        使用views 来抓取新闻，是为了区分广告、视频、新闻
        :return:
        """

        views = self.driver.find_elements_by_id(EL_VIEW)

        if not views:
            print("Don't have news！！！")
            return

        for view in views:
            title = view.find_elements_by_id(EL_TITLE)

            # 判断新闻是否完整
            if not view.find_elements_by_id(EL_TV_SRC) or not title:
                print("The news is incomplete！！！")
                continue

            title_name = title[0].text

            # 判断是否已经看过
            if title_name in self.news_list:
                print("The news has been read or is null ！！！")
                continue

            if view.find_elements_by_id(EL_POINT_AD):
                print("The news is a ad: {title}".format(title = title[0].text))
                continue

            if view.find_elements_by_id(EL_ALIVC_PLAYER_STATE):
                print("The nes is a video: {title}".format(title = title[0].text))
                # self.watch_videos(view, title)
                continue

            # click news title
            for t in title:
                print("=========================================")
                print("Read news: 《 {t} 》".format(t = title_name))
                t.click()
                # self.driver.implicitly_wait(10)

                # Slide down 8 times
                for n in range(6):
                    self.driver.swipe(100, 1090, 100, 200, duration=2000)
                    print("Slide down {n} times".format(n = n))
                    try:
                        all = self.driver.find_element_by_accessibility_id("展开全文")
                        if all:
                            all.click()
                    except:
                        continue

                self.news_list.append(title_name)
                if len(self.news_list) > 10:
                    print("news_list pop one！！！")
                    self.news_list.pop()

                print("Back to news front page！！！")
                # Back to news front page
                self.driver.find_elements_by_id(EL_IV_BACK)[0].click()

    def watch_videos(self, view, title):
        print("watch videos 《 {title} 》".format(title = title[0].text))
        view.find_elements_by_id(EL_ALIVC_PLAYER_STATE)[0].click()
        n = 0
        while n < 40:
            time.sleep(1)
            n = n + 1
        self.driver.find_elements_by_id(EL_ALIVC_TITLE_BACK)[0].click()

    def get_top_coin(self):
        el_top_coin = self.driver.find_elements_by_id(EL_COUNT_DOWN_TV)
        if el_top_coin and el_top_coin[0].text == "点击领取":
            print("Get the top coin！！！")
            el_top_coin[0].click()
            time.sleep(2)
            try:
                self.driver.find_elements_by_id(EL_TV_LEFT)[0].click()
            except:
                return


    def run(self):
        self.__login_app()
        while True:
            self.get_top_coin()

            self.watch_news()

            print('查看一页完成，继续查看下一页的新闻。')
            # 滑动下一页的新闻
            self.driver.swipe(100, 1090, 100, 200, duration=2000)

            now_time = datetime.datetime.now()
            if (now_time - self.start_time).seconds > 600:
                self.get_top_coin()

            time.sleep(2)

if __name__ == "__main__":
    HuiTouTiao().run()
