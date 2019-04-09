#!/usr/bin/env python  
# encoding: utf-8  


__author__ = "Leon"

from airtest.core.api import *
from poco.exceptions import PocoNoSuchNodeException
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from queue import Queue
from airtest.core.android import Android
import datetime
import time
import random

# 应用包名和启动Activity
dongfang_package_name = 'com.songheng.eastnews'

activity = 'com.oa.eastfirst.activity.WelcomeActivity'

device_1 = '9DHUSC5DTGIFIR95'

poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)

auto_setup(__file__)


# 收益来源
# 0.顶部的时长领取金币
# 1.任务：包含签到、
# 1.收益
# 2.阅读新闻
# 3.评论


class DongFangTouTiao(object):
    """
    东方头条
    """

    def __init__(self):
        # 保留最新的5条新闻标题
        self.news_titles = []

        # 跳过的页数
        self.skip_page = 0

        self.__connect_device()

        # define elements id
        self.news_title_id = "pj"
        self.news_ad_id = "a0h"
        self.app_first_ad_id1 = "tt_splash_skip_tv"
        self.app_first_ad_id2 = "apv"
        self.news_home_page_id = "gb"
        self.top_coin_id = "ati"
        self.time_icon_id = "arg"
        self.video_id = "kx"
        self.video_home_page_id = "a25"
        self.video_play_id = "q6"
        self.video_replay_id = "asn"
        self.video_share_id = "a9y"
        self.video_ad_id = "a5i"
        self.video_type_id = "com.songheng.eastfirst.business.video.view.widget.ijkplayer.TextureRenderView"
        self.current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def run(self):

        # start app
        self.__stop_app(dongfang_package_name)
        self.__start_app(dongfang_package_name, activity)
        self.__pre_and_skip_ads()

        # get top gold coin
        self.get_top_title_coin()

        # Check out recommended news
        self.__skip_same_pages()
        watch_news_starttime = datetime.datetime.now()

        while True:
            self.watch_news_recommend()
        
            print('查看一页完成，继续查看下一页的新闻。')
        
            # 顶部金币领取
            self.get_top_title_coin()
        
            # 滑动下一页的新闻
            poco.swipe([0.5, 0.8], [0.5, 0.3], duration=1)

            news_time = datetime.datetime.now()
            news_interval_time = (news_time - watch_news_starttime).seconds
            if news_interval_time >= 1800:
                print("看新闻时间超过1小时，跳转到视频频道")
                break

        # View videos
        self.__video()

    def __connect_device(self):
        connect_device('Android:///{0}'.format(device_1))

 
    def __start_app(self, package_name, activity):
        start_app(dongfang_package_name)

    def __stop_app(self, package_name):
        stop_app(dongfang_package_name)

    def __dongfang_element(self, elementid):
        element = '{0}:id/{1}'.format(dongfang_package_name, elementid)
        return element

    def watch_news_recommend(self):
        """
        查看新闻
        :return:
        """

        # 1.推荐的所有新闻元素
        lv_elements = poco(self.__dongfang_element(self.news_home_page_id)).children()

        if not lv_elements.exists():
            print('新闻列表不存在')
            return

        # 下面的循环经常会报错：PocoNoSuchNodeException
        # 遍历每一条新闻
        for news_element in lv_elements:

            # 1.查看要闻
            self.__read_key_news()

            # 2.新闻标题
            news_title = news_element.offspring(self.__dongfang_element(self.news_title_id))

            # 3.注意：必须保证元素加载完全
            # 下面会报错：hrpc.exceptions.RpcRemoteException: java.lang.IndexOutOfBoundsException
            try:
                if not news_title.exists():
                    print("【标题】元素加载不完全")
                    continue
            except Exception as e:
                print("******注意注意注意！exist()方法报错******")
                print("判断下面两个东西是否存在")
                print(e)
                self.__back_to_list()
                print('回到首页')
                return

            # 4.过滤广告
            # 到这里标识此条新闻：是一条有效的新闻【包含广告】
            # 注意：部分广告【包含点击标题就自动下载，左下角显示广告字眼等】要过滤掉
            # 场景一：
            if news_element.attr('name') == 'android.widget.FrameLayout':
                print('广告！这是一个FrameLayout广告，标题是:%s' % news_title.get_text())
                continue

            # 常见二：有效角标识是广告的图标【广告】
            ads_tips_element2 = news_element.offspring(self.__dongfang_element(self.news_ad_id))
            if ads_tips_element2.exists():
                print('广告！广告标题是：%s' % news_title.get_text())
                continue

            # 已经查看过了，过滤掉
            if news_title.get_text() in self.news_titles:
                print('已经看过了，不看了！')
                continue

            # ==========================================================================
            # 5.查看新闻
            # 下面是一条有效的新闻
            # 新闻类型
            # 文字0、视频1、图片2
            news_type = self.get_news_type(news_element)

            if 5 == len(self.news_titles):
                self.news_titles.pop()
            self.news_titles.insert(0, news_title.get_text())

            print('==' * 30)
            print('当前时间:%s' % self.current_time)
            print('准备点击刷新闻，这条新闻的标题是:%s' % news_title.get_text())

            # 以上还在主界面
            # 如果是正常的新闻就点击进去
            news_title.click()

            # 等待新闻元素都加载完全
            sleep(3)

            print('这条新闻类型:%d' % news_type)

            print('已阅读新闻包含：')
            for temp_title in self.news_titles:
                print(temp_title)

            # 记录时长的标识
            # 不存在就直接返回
            if not self.__red_coin():
                continue

            oldtime = datetime.datetime.now()

            # 文字
            if news_type == 0:
                while True:
                    print("循环-滑动查看内容")
                    self.__swipe(True if random.randint(0, 20) == 0 else False)
                    sleep(2)

                    # 如果发现有【点击查看全文】按钮，点击查看全文
                    see_all_article_element = poco('点击查看全文')
                    see_all_article_element1 = poco('点击阅读全文')
                    if see_all_article_element.exists():
                        print('点击展开全文内容...')
                        see_all_article_element.focus('center').click()
                    elif see_all_article_element1.exists():
                        print('点击阅读全文内容...')
                        see_all_article_element1.focus('center').click()

                        # 注意：有的时候点击展开全文，会点击到图片，需要规避一下
                        '''
                        while poco('{0}:id/lz'.format(dongfang_package_name)).exists():
                            print('不小心点到图片了，返回到新闻详情页面')
                            self.__back_keyevent()
                        '''

                    newtime = datetime.datetime.now()
                    interval_time = (newtime - oldtime).seconds
                    if interval_time >= 40:
                        print('阅读30秒新闻完成')
                        break
                    self.__read_key_news()
            # 视频
            elif news_type == 1:
                while True:
                    print("循环-滑动查看视频")
                    newtime = datetime.datetime.now()
                    interval_time = (newtime - oldtime).seconds
                    if interval_time >= 50:
                        print('观看30秒视频完成')
                        break
                    self.__read_key_news()

            print('==' * 30)

            self.__back_to_list()

    def __video(self):
        """
        查看视频
        :return:
        """
        poco(self.__dongfang_element(self.video_id)).click()
        watch_video_starttime = datetime.datetime.now()

        while True:
            # 视频列表
            poco(self.__dongfang_element(self.video_home_page_id)).wait_for_appearance()
            sleep(2)

            self.__read_key_news()

            video_elements = poco(self.__dongfang_element(self.video_home_page_id)).children()

            print('video items是否存在：')
            print(video_elements.exists())

            # 遍历视频
            # 注意：视频播放完全可以提前返回
            for video_element in video_elements:
                #过滤视频广告
                ads_tips_element = video_element.offspring(name=self.__dongfang_element(self.video_ad_id), text='广告')
                if ads_tips_element.exists():
                    print('广告！这是一个广告，标题是:%s' % video_element.get_text())
                    continue

                # 1.标题元素
                video_title_element = video_element.offspring(self.__dongfang_element(self.news_title_id))
                # 播放按钮
                video_play_element = video_element.offspring(self.__dongfang_element(self.video_play_id))

                # 2.必须保证【视频标题】和【播放按钮】都可见
                if not video_title_element.exists() or not video_play_element.exists():
                    continue

                # 3.标题
                video_title = video_element.offspring(self.__dongfang_element(self.news_title_id)).get_text()

                print('当前视频的标题是:%s,播放当前视频' % video_title)

                # 点击播放视频
                video_play_element.focus("center").click()

                # 记录时长的标识
                # 不存在就直接返回
                if not self.__red_coin():
                    continue

                # 4.播放视频
                self.play_video()

                print('播放下一个视频')

                self.__back_keyevent()

            # 滑动到下一页的视频
            poco.swipe([0.5, 0.8], [0.5, 0.3], duration=0.2)

            video_time = datetime.datetime.now()
            video_time_interval = (video_time - watch_video_starttime).seconds

            if video_time_interval >= 1800:
                print("观看视频已经超过1小时，跳转到另外一个app")
                break

    def __red_coin(self):
        red_coin_element = poco(self.__dongfang_element(self.time_icon_id))
        if not red_coin_element.exists():
            print('当前新闻没有红包，返回！')
            self.__back_keyevent()
            return False
        else:
            return True

    def __swipe(self, up_or_down):
        """
        滑动单条新闻
        :param up_or_down: true：往上滑动；false：往下滑动【慢慢滑动】
        :return:
        """
        if not up_or_down:
            poco.swipe([0.5, 0.6], [0.5, 0.4], duration=0.5)
        else:
            poco.swipe([0.5, 0.4], [0.5, 0.6], duration=0.5)

    def get_news_type(self, news_element):
        """
        获取新闻的类型【文字0、视频1、图片2】
        :param news_element:
        :return:
        """
        # 默认是文字新闻
        type = 0
        video_element = poco(self.video_type_id)
        if video_element.exists():
            type = 1

        return type

    def __wait_for_element_exists(self, elements):
        """
        一直等待元素出现
        :param elements: 元素列表
        :return:
        """
        try:
            while True:
                # 元素是否存在
                element_exists = True

                # 元素列表
                for element in elements:
                    if not element.exists():
                        element_exists = False
                        break
                    else:
                        continue

                if element_exists:
                    break
                else:
                    print('元素暂时找不到，继续等待')
                    continue
        except PocoNoSuchNodeException as e:
            print('找不到这个元素异常')

    def __pre_and_skip_ads(self):
        """
        预加载和跳过广告
        :return:
        """
        # 1.广告页面元素的出现
        # 两种样式：跳过、跳过广告*秒

        try:
            print("读取首次广告。。。。")
            poco(self.__dongfang_element(self.app_first_ad_id2)).wait_for_appearance(10)
        except:
            poco(self.__dongfang_element(self.app_first_ad_id1)).wait_for_appearance(10)

        ads_element = poco(name=self.__dongfang_element(self.app_first_ad_id1), textMatches='.*| 跳过$')
        ads_element1 = poco(name='android.widget.TextView', text='跳过')


        # 跳过广告(0s)
        if ads_element.exists():
            print('跳过广告1!!!')
            ads_element.click()
        if ads_element1.exists():
            print('跳过广告2!!!')
            ads_element1.click()

        # 2.等到到达主页面
        poco(self.__dongfang_element(self.news_home_page_id)).wait_for_appearance(120)

    def __read_key_news(self):
        """
        处理【要闻】对话框，需要阅读
        :return:
        """
        # 对于弹出来的要闻对话框，需要处理
        key_news_element = poco(name='{0}:id/xq'.format(dongfang_package_name), text='立即查看')
        if key_news_element.exists():
            print('要闻推送！需要看一下')
            key_news_element.click()

            # TODO  需不需要另外停留
            sleep(3)
            self.__back_keyevent()

    def play_video(self):
        """
        播放一个视频
        :return:
        """

        # 开始时间
        start_time = datetime.datetime.now()

        while True:
            # 视频播放结束或者超过30秒
            scale_element = poco(self.__dongfang_element(self.video_replay_id))

            if scale_element.exists():
                print('视频播放完了，结束播放。')
                break

                # 结束时间
            end_time = datetime.datetime.now()

            # 时间间隔
            interval_time = (end_time - start_time).seconds

            if interval_time > 50:
                print('播放超过30秒，结束播放。')
                break

    def get_top_title_coin(self):
        """
        顶部金币领取
        仅仅在新闻首页的时候才可以领取
        :return:
        """
        get_coin_element = poco(name=self.__dongfang_element(self.top_coin_id), text="领取")

        if get_coin_element.exists():
            print('顶部有金币可以领取！')
            get_coin_element.click()
            sleep(2)

            print('领完金币后可以关闭对话框！')
            # 关掉对话框
            self.__back_keyevent()
        else:
            print('顶部没有金币或者不在首页')

    def __skip_same_pages(self):
        """
        往下滑动【跳过】几页
        :param num:
        :return:
        """
        current_page = 0
        while current_page < self.skip_page:
            poco.swipe([0.5, 0.8], [0.5, 0.3], duration=1)
            current_page += 1

        print('跳过结束，继续获取金币')

    def __back_keyevent(self):
        """
        返回的时候可能会出现关键要闻
        :return:
        """
        self.__read_key_news()
        keyevent('BACK')

    def __back_to_list(self):
        """
        回退到首页
        :return:
        """
        print('准备回到首页')
        while not poco(self.__dongfang_element(self.news_home_page_id)).exists():
            print('回退一次')
            self.__back_keyevent()


if __name__ == "__main__":
    dftt = DongFangTouTiao()
    dftt.run()
