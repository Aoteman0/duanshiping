# coding=gbk
import json
import os
import random
from PIL import Image
import time
from multiprocessing import Queue
import uiautomator2 as u2
from concurrent.futures import ThreadPoolExecutor

# 哔哩哔哩:tv.danmaku.bili
# 抖音火山版:com.ss.android.ugc.live
# 微视:com.tencent.weishi
# 抖音:com.ss.android.ugc.aweme
# 西瓜视频:com.ss.android.article.video
# 快手:com.smile.gifmaker

def handel_watch():
    with d.watch_context() as ctx:
        while not data_queue.empty():
            ctx.when("稍后再说").click()
            ctx.when("跳过").click()
            #ctx.when(d(textContains='跳过')).click()#不可用
            ctx.when("以后再说").click()
            ctx.when("下次再说").click()
            ctx.when("暂不开启").click()
            ctx.when("我知道了").click()
            ctx.when("残忍离开").click()
            ctx.when("拒绝").click()
            ctx.when("不感兴趣").click()
            ctx.when("立即更新").call(lambda d: d.press("back"))
            ctx.when("立即升级").click()
            #ctx.wait_stable()
            time.sleep(s/2)

# 滑屏操作
def swipe_us(f):
    # 视频时间间隔
    global s
    s = random.choice(range(3,20))+random.random()
    x_a = d.window_size()[0] / 2
    y_a = d.window_size()[1] * (9 / 10)
    y_b = d.window_size()[1] * (1 / 10)
    # u 向上滑屏    d 向下滑屏
    if f == 'u':
        d.swipe(x_a, y_a, x_a, y_b, 0.1)
        # print(self.s, '秒',"向上滑")
        # 滑完视频等待时间
        time.sleep(s)
    if f == 'd':
        d.swipe(x_a, y_b * 3, x_a, y_a * 3 / 5, 0.1)
        # print("向下滑")
    # self.d.swipe_ext("up")

# 软件启动
def app_start_new(name_dict):
    name=name_dict['name']
    try:
        d.app_start(name_dict['start'], use_monkey=True)
        time.sleep(1)
        d.freeze_rotation()#关闭屏幕旋转
        print("%s视频正在启动"%name)
        try:
            if d(textContains='跳过').exists(timeout=10):
                d.press("back")
                print("跳过")
        except:
            print("没有跳过按钮")
        #handel_watch()
        try:
            if d(resourceId=name_dict['resourceId'], text=name_dict['text']).exists(timeout=10):
                if name != 'bili':
                    print(name + '视频启动成功！')
                    app_swipe(name,name_dict)
                elif name == 'bili':
                    bili(name, name_dict)
        except Exception as e:
            image = d.screenshot()
            image.save("photo/启动失败%s.jpg"%int(time.time()))
            d.press("back")
            error_red("%s启动失败！"%name_dict['start'])
    except Exception as e:
        error_red("%s启动失败！"%name_dict['start'])
        app_stop(name, name_dict['start'])

# ------------------------
# 视频滑动和点赞
def app_swipe(name,name_dict):
    tmp = '0'
    dianz = 1
    for i in range(num_video):
        swipe_us('u')
        try:
            try:
                tmp_new = d(resourceId=name_dict['resourceId_user']).get_text(timeout=5)
                # print(tmp, tmp_new)
            except:
                tmp_new = tmp
            # 判断滑动前视频用户名是否相同，避免弹框影响滑动
            if tmp == tmp_new:
                #handel_watch()
                d.press("back")
                print("back")
                swipe_us('u')
            else:
                if random.choice([1, 2, 3, 4, 5]) == 1:
                    if name_dict['className_like'] == '':
                        d(resourceId=name_dict['reesourceId_like']).click(timeout=5)
                    else:
                        d(className=name_dict['className_like'], resourceId=name_dict['reesourceId_like']).click(timeout=5)
                    print("%s点赞成功%d次"%(name,dianz))
                    dianz += 1
        except Exception as e:
            image = d.screenshot()
            image.save("photo/点赞失败%s.jpg" % int(time.time()))
            error_red("%s点赞失败！第%s行"%(name,str(e.__traceback__.tb_lineno)))
        tmp = tmp_new
        print('\33[1;34m 等待时间:%d秒  %s刷了%d次视频\33[0m'%(s,name,(i + 1)))
    # 视频刷完调出循环 关闭软件
    app_stop(name, name_dict['start'])

# bili视频
def bili(name,name_dict):
    tmp = '0'
    shiping = 0
    dianz = 1
    for i in range(num_video):
        swipe_us('d')
        time.sleep(1)
        try:
            text_str = d(resourceId='tv.danmaku.bili:id/desc').get_text(timeout=10)
            # print(tmp,text_str)
        except Exception as e:
            error_red("获取视频失败" + "  " + str(e.__traceback__.tb_lineno))
            text_str = tmp
            #handel_watch()
            d.press("back")
        if tmp == text_str:
            swipe_us('d')
        else:
            d(resourceId='tv.danmaku.bili:id/cover_layout').click(timeout=10)
            shiping += 1
            print('\33[1;34m ' + '等待时间' + str(s) + '秒', name + '刷了' + str(shiping) + '次视频' + ' \33[0m')
            time.sleep(s)
            try:  # 判断b站视频为竖屏还是横屏 点赞不一样
                if random.choice([1, 2, 3, 4, 5]) == 1:
                    if '竖屏' in text_str:
                        d(resourceId='tv.danmaku.bili:id/like_icon').click(timeout=10)
                    else:
                        d(resourceId='tv.danmaku.bili:id/recommend_icon').click(timeout=10)
                    print("点赞成功" + str(dianz) + '次')
                    dianz += 1
                    tmp = text_str
                d.press("back")
            except Exception as e:
                # image = d.screenshot()
                # image.save("photo/bili视频点赞失败%s.jpg" % int(time.time()))
                error_red("bili视频点赞失败" + "  " + str(e.__traceback__.tb_lineno))
                d.press("back")
    # 视频刷完调出循环 关闭软件
    app_stop(name, name_dict['start'])

    # 错误提示高亮
def error_red(s):
    print('\33[1;31m ' + s + ' \33[0m')

# 停止app
def app_stop(name, start):
    d.app_stop(start)
    time.sleep(2)
    error_red(name + "视频停止了")

def screen_on():
    if not d.info.get('screenOn'):
        d.unlock()
        time.sleep(2)
def app():
    screen_on()
    while not data_queue.empty():
        name_dict=data_queue.get()
        if name_dict["name"]!="null":
            app_start_new(name_dict)
        else:break

ip = '192.168.5.198'
ip2 = '192.168.0.17'
num_video = 50  # 刷10个视频
s = 6
pool = ThreadPoolExecutor(2)
data_queue=Queue()
with open('data.json', 'r') as f:
    data_str = json.loads(f.read())
    for i in data_str:
        data_queue.put(i)
#d= u2.connect_wifi(ip2+":8886")

if __name__ == '__main__':
    # try:
    #
    #     #os.system("adb shell /data/local/tmp/atx-agent server -d --stop")
    #     #os.system("adb tcpip 8889")
    #     os.system("adb connect " + ip2)
    #     os.system("adb shell /data/local/tmp/atx-agent server -d")
    # except:
    #     pass
    while True:
        try:
            d= u2.connect_wifi(ip)
            pool.submit(app)
            pool.submit(handel_watch)
            break
        except Exception as e:
            print(e.__traceback__.tb_lineno, e)
            continue
