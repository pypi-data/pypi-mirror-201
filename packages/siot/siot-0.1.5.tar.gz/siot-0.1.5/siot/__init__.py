#-*- coding: utf-8 -*-
'''
# file siot.py

# brief         download into pc or raspberryPi and run the demo
# Copyright     Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
# licence       The MIT License (MIT)
# author        [LuoYufeng](yufeng.luo@dfrobot.com)
# version       V1.0
# date          2020-5-28
'''

name = "DFRobot_siot"

__all__ = ['init', 'connect', 'publish','publish_save', 'subscribe', '_on_connect', '_on_disconnect','_languageIsZh', 'set_callback', 'getsubscribe', 'stop', 'publloopish', '_loop']

__version__ = '0.1.5'


import threading
import paho.mqtt.client as mqtt
import time
import random

timer = None
_sysLanguageIsZH = True


def _languageIsZh():
    import platform
    import subprocess
    import locale
    try:
        os_info = platform.system()
        if os_info == 'Windows' or os_info == 'Linux':
            current_locale, encoding = locale.getdefaultlocale()
            if 'zh' in current_locale.lower():
                return True
            else:
                return False
        elif os_info == 'Darwin':
            cmd = "defaults read -g AppleLanguages | tr -d [:space:]; exit 0"
            output = subprocess.check_output(cmd, shell=True).decode().strip()
            language = output.split(',')[0]
            if language.startswith('zh'):
                return True
            else:
                return False
        else:
            return True
    except Exception as e:
        print("Failed to get system language.")
        print(e)
        return True

_sysLanguageIsZH = _languageIsZh()


def printInf():
    global _host, _port, _user, _password,_clientid
    print(" ")
    print("lib version:",__version__)
    print("server:%s port:%s user:%s password:%s client_id:%s"%(_host,_port,_user,_password,_clientid))
    print(" ")

def _on_connect(client, userdata, flags, rc):
    
    if str(rc)=="0":
        if _sysLanguageIsZH:
            print("\n连接结果: 连接成功 ")
        print("\nConnection result: The connection is successful")
    elif str(rc)=="1":
        if _sysLanguageIsZH:
            print("\n连接结果: 协议版本错误 ")
        print("\nConnection result: wrong protocol version")
        printInf()
    elif str(rc)=="2":
        if _sysLanguageIsZH:
            print("\n连接结果: 无效的客户端标识 ")
        print("\nConnection result: Invalid client ID")
        printInf()
    elif str(rc)=="3":
        if _sysLanguageIsZH:
            print("\n连接结果: 服务器无法使用 ")
        print("\nConnection result: server unavailable")
        printInf()
    elif str(rc)=="4":
        if _sysLanguageIsZH:
            print("\n连接结果: 错误的用户名或密码 ")
        print("\nConnection result: bad username or password")
        printInf()
    else:
        if _sysLanguageIsZH:
            print("\n连接结果: 未经授权 "+str(rc)) 
        print("\nConnection result: Unauthorized "+str(rc)) 
        printInf()

def _on_disconnect(client, userdata, rc):
    if rc == 0:
        if _sysLanguageIsZH:
            print("\n连接结果: 断开成功 ")
        print("\nConnection result: Disconnected successfully")
    else:
        if _sysLanguageIsZH:
            print("\n网络受限 "+str(rc)) 
        print("\nlimited network "+str(rc)) 
        printInf()


def init(client_id=None, server=None, port=1883, user=None, password=None, cb1=_on_connect, cb2=_on_disconnect):
    global _host, _port, _user, _password,_clientid, client
    _host = server
    _port = port
    _user = user
    _password = password

    if len(client_id)==0 or client_id==None:
        client_id = str(int(time.time()))+str(random.randint(1, 10000))
    _clientid = client_id

    printInf()

    client = mqtt.Client(client_id)
    client.on_connect = cb1
    client.on_disconnect = cb2

def connect():
    client.username_pw_set(_user, _password)
    client.connect(_host, _port, 60)

def publish(topic, data):
    client.publish(str(topic), str(data),qos=0)

def publish_save(topic, data,qos=1):
    client.publish(str(topic), str(data),qos=qos)
   
def subscribe(topic, cb):
    client.on_message  = cb
    client.subscribe(topic)

def set_callback(cb):
    client.on_message = cb

def getsubscribe(topic):
    client.subscribe(topic)

def stop():
    client.disconnect()
    if timer != None:
        timer.cancel()
 
def loop(timeout=None):
    thread = threading.Thread(target=_loop, args=(timeout,))
    # thread.setDaemon(True)
    thread.start()
    
def _loop(timeout=None):
    if not timeout:
        client.loop_forever()
    else:
        client.loop(timeout)
