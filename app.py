# coding=gbk
import json
import os
import random
from PIL import Image
import time
from multiprocessing import Queue
import uiautomator2 as u2
from concurrent.futures import ThreadPoolExecutor

# ��������:tv.danmaku.bili
# ������ɽ��:com.ss.android.ugc.live
# ΢��:com.tencent.weishi
# ����:com.ss.android.ugc.aweme
# ������Ƶ:com.ss.android.article.video
# ����:com.smile.gifmaker

def handel_watch():
    with d.watch_context() as ctx:
        while not data_queue.empty():
            ctx.when("�Ժ���˵").click()
            ctx.when("����").click()
            #ctx.when(d(textContains='����')).click()#������
            ctx.when("�Ժ���˵").click()
            ctx.when("�´���˵").click()
            ctx.when("�ݲ�����").click()
            ctx.when("��֪����").click()
            ctx.when("�����뿪").click()
            ctx.when("�ܾ�").click()
            ctx.when("������Ȥ").click()
            ctx.when("��������").call(lambda d: d.press("back"))
            ctx.when("��������").click()
            #ctx.wait_stable()
            time.sleep(s/2)

# ��������
def swipe_us(f):
    # ��Ƶʱ����
    global s
    s = random.choice(range(3,20))+random.random()
    x_a = d.window_size()[0] / 2
    y_a = d.window_size()[1] * (9 / 10)
    y_b = d.window_size()[1] * (1 / 10)
    # u ���ϻ���    d ���»���
    if f == 'u':
        d.swipe(x_a, y_a, x_a, y_b, 0.1)
        # print(self.s, '��',"���ϻ�")
        # ������Ƶ�ȴ�ʱ��
        time.sleep(s)
    if f == 'd':
        d.swipe(x_a, y_b * 3, x_a, y_a * 3 / 5, 0.1)
        # print("���»�")
    # self.d.swipe_ext("up")

# �������
def app_start_new(name_dict):
    name=name_dict['name']
    try:
        d.app_start(name_dict['start'], use_monkey=True)
        time.sleep(1)
        d.freeze_rotation()#�ر���Ļ��ת
        print("%s��Ƶ��������"%name)
        try:
            if d(textContains='����').exists(timeout=10):
                d.press("back")
                print("����")
        except:
            print("û��������ť")
        #handel_watch()
        try:
            if d(resourceId=name_dict['resourceId'], text=name_dict['text']).exists(timeout=10):
                if name != 'bili':
                    print(name + '��Ƶ�����ɹ���')
                    app_swipe(name,name_dict)
                elif name == 'bili':
                    bili(name, name_dict)
        except Exception as e:
            image = d.screenshot()
            image.save("photo/����ʧ��%s.jpg"%int(time.time()))
            d.press("back")
            error_red("%s����ʧ�ܣ�"%name_dict['start'])
    except Exception as e:
        error_red("%s����ʧ�ܣ�"%name_dict['start'])
        app_stop(name, name_dict['start'])

# ------------------------
# ��Ƶ�����͵���
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
            # �жϻ���ǰ��Ƶ�û����Ƿ���ͬ�����ⵯ��Ӱ�컬��
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
                    print("%s���޳ɹ�%d��"%(name,dianz))
                    dianz += 1
        except Exception as e:
            image = d.screenshot()
            image.save("photo/����ʧ��%s.jpg" % int(time.time()))
            error_red("%s����ʧ�ܣ���%s��"%(name,str(e.__traceback__.tb_lineno)))
        tmp = tmp_new
        print('\33[1;34m �ȴ�ʱ��:%d��  %sˢ��%d����Ƶ\33[0m'%(s,name,(i + 1)))
    # ��Ƶˢ�����ѭ�� �ر����
    app_stop(name, name_dict['start'])

# bili��Ƶ
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
            error_red("��ȡ��Ƶʧ��" + "  " + str(e.__traceback__.tb_lineno))
            text_str = tmp
            #handel_watch()
            d.press("back")
        if tmp == text_str:
            swipe_us('d')
        else:
            d(resourceId='tv.danmaku.bili:id/cover_layout').click(timeout=10)
            shiping += 1
            print('\33[1;34m ' + '�ȴ�ʱ��' + str(s) + '��', name + 'ˢ��' + str(shiping) + '����Ƶ' + ' \33[0m')
            time.sleep(s)
            try:  # �ж�bվ��ƵΪ�������Ǻ��� ���޲�һ��
                if random.choice([1, 2, 3, 4, 5]) == 1:
                    if '����' in text_str:
                        d(resourceId='tv.danmaku.bili:id/like_icon').click(timeout=10)
                    else:
                        d(resourceId='tv.danmaku.bili:id/recommend_icon').click(timeout=10)
                    print("���޳ɹ�" + str(dianz) + '��')
                    dianz += 1
                    tmp = text_str
                d.press("back")
            except Exception as e:
                # image = d.screenshot()
                # image.save("photo/bili��Ƶ����ʧ��%s.jpg" % int(time.time()))
                error_red("bili��Ƶ����ʧ��" + "  " + str(e.__traceback__.tb_lineno))
                d.press("back")
    # ��Ƶˢ�����ѭ�� �ر����
    app_stop(name, name_dict['start'])

    # ������ʾ����
def error_red(s):
    print('\33[1;31m ' + s + ' \33[0m')

# ֹͣapp
def app_stop(name, start):
    d.app_stop(start)
    time.sleep(2)
    error_red(name + "��Ƶֹͣ��")

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
num_video = 50  # ˢ10����Ƶ
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
