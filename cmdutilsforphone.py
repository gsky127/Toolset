#!/user/bin/env python
#-*- coding:utf-8 -*-

'''
这是一个对常用的adb 命令进行封装的文件，其目的是为了让adb命令调用起来更简单
author: Qb.Gao
date  : 2018/8
'''

import os
from time import sleep
import time

# 重连动作
def reconnectAction(deviceid):
    devlist = getdevlist()
    print(f'设备{deviceid}正在尝试重连.')
    id = 1
    while deviceid not in devlist:
        print(f'第{id}次 ', end = ' ')
        devlist = getdevlist()
        id = id + 1
    print(f'\n设备{deviceid}重新建立连接成功.')
    sleep(1)

# 执行普通的cmd命令
def exeCmd(cmdInfo, deviceid):
    if deviceid == '':
        cmd = 'adb shell ' + cmdInfo[0]
    else:
        cmd = 'adb -s ' + deviceid + ' shell ' + cmdInfo[0]
    print(f'设备{deviceid}:exeCmd():{cmdInfo[1]}.')
    if os.system(cmd) != 0:
        return False
    else:
        return True

# 按键动作
def pressKeyevent(keycodeInfo, deviceid = ''):
    if deviceid == '':
        cmd = 'adb shell input keyevent ' + keycodeInfo[0]
    else:
        cmd = 'adb -s ' + deviceid + ' shell input keyevent ' + keycodeInfo[0]
    print(f'设备{deviceid}:pressKeyevent():{keycodeInfo[1]}.')
    if os.system(cmd) != 0:
        return False
    else:
        return True
    
# 点击屏幕的动作
def clickScreen(positionInfo, deviceid = ''):
    if deviceid == '':
        cmd = 'adb shell input tap ' + positionInfo[0]
    else:
        cmd = 'adb -s ' + deviceid + ' shell input tap ' + positionInfo[0]  
    print(f'设备{deviceid}:clickScreen():{positionInfo[1]}.')
    if os.system(cmd) != 0:
        return False
    else:
        return True

# 输入文本信息
def inputText(tTextInfo, deviceid = ''):
    if deviceid == '':
        cmd = 'adb shell input text ' + tTextInfo[0]
    else:
        cmd = 'adb -s ' + deviceid + ' shell input text ' + tTextInfo[0]   
    print(f'设备{deviceid}:inputText():{tTextInfo[1]}.')
    if os.system(cmd) != 0:
        return False
    else:
        return True
    
# 滑动屏幕的动作
def swipeScreen(positionInfo, deviceid = ''):
    if deviceid == '':
        cmd = 'adb shell input swipe ' + positionInfo[0]
    else:
        cmd = 'adb -s ' + deviceid + ' shell input swipe ' + positionInfo[0]  
    print(f'设备{deviceid}:swipeScreen():{positionInfo[1]}.')
    if os.system(cmd) != 0:
        return False
    else:
        return True

# 运行app
def launchApp(appactivityInfo, deviceid = ''):
    if deviceid == '':
        cmd = 'adb shell am start ' + appactivityInfo[0]
    else:
        cmd = 'adb -s ' + deviceid + ' shell am start ' + appactivityInfo[0]   
    print(f'设备{deviceid}:launchApp():{appactivityInfo[1]}.')
    if os.system(cmd) != 0:
        return False
    else:
        return True
        
# 获取username,  如chinaren
def getusername():
    namelist = os.popen('echo %username%').readlines()
    username = namelist[0].replace("\n", "")
    # 获取当前的username
    return username

# 获取设备id列表
def getdevlist():
    devlist = []
    connectfile = os.popen('adb devices')
    list = connectfile.readlines()
    # print(list)
    for i in range(len(list)):
        if list[i].find('\tdevice') != -1:
            temp = list[i].split('\t')
            devlist.append(temp[0])
    return devlist
    
# 执行cmd命令
def executeCmd(cmd):
    stringList = cmd.splitlines() 
    for i in range(len(stringList)):
        try:
            os.system(stringList[i])
        except KeyboardInterrupt:
            print('\n异常退出: KeyboardInterrupt')
            
# 在指定路径新建一个指定前缀_当前系统时间文件夹,并返回foldername(eg:Mtklog_20180411100455)
def creatfolder(path, folderprefix):
    os.chdir(path)
    foldername = folderprefix + '_' + getnowdatatime(3)
    os.mkdir(foldername)
    return foldername
    
# 判断手机/sdcard/下是否存在指定的文件夹名
def isexistfolder(foldername):
    '''
    :type foldername: str
    :rtype: bool
    '''
    try:
        names = os.popen('adb shell ls /sdcard/').readlines()
        # 将file按line变成List中的项后，每个item是以\n结尾的.故foldername后需要+'\n'
        if foldername + '\n' in names:
            return True
        else:
            return False
    except Exception:
        print(f'根目录下存在中文名files/folder,可能会操作异常!\n')

# 判断当前手机的亮屏状态
def isAwaked(deviceid = ''):
    '''
    判断的依据是'    mAwake=false\n'
    '''
    if deviceid == '':
        cmd = 'adb shell dumpsys window policy'
    else:
        cmd = 'adb -s ' + deviceid + ' shell dumpsys window policy'
    screenAwakevalue = '    mAwake=true\n' 
    allList = os.popen(cmd).readlines()
    if screenAwakevalue in allList:
        return True
    else:
        return False
        
# 获取时间和日期 
def getnowdatatime(flag = 0):
    '''
    flag = 0为时间和日期         eg:2018-04-11 10:04:55
    flag = 1仅获取日期           eg:2018-04-11
    flag = 2仅获取时间           eg:10:04:55
    flag = 3纯数字的日期和时间   eg:20180411100455 
    
    :type flag: int
    :rtype: str
    '''
    now = time.localtime(time.time())
    if flag == 0:
        return time.strftime('%Y-%m-%d_%H-%M-%S', now)
    if flag == 1:
        return time.strftime('%Y-%m-%d', now)
    if flag == 2:
        return time.strftime('%H:%M:%S', now)
    if flag == 3:
        return time.strftime('%Y%m%d%H%M%S', now)
        
# 用于判断当前界面元素的状态        
def isExistElementValue(query, value, deviceid = ''):
    '''
    因为adb shell来执行是没有办法去判断界面元素的执行状态。
    而有时又必须要判断当前的执行状态，则要用到这个函数.
    常用命令：
    adb shell uiautomator dump /sdcard/ui.xml
    adb pull /sdcard/ui.xml ./Desktop/
    http://web.chacuo.net/formatxml
    '''
    from lxml import etree
    if deviceid == '':
        xmlfilename = 'ui.xml'
        uixmlfile = 'adb shell uiautomator dump /sdcard/' + xmlfilename
        pulluixmlToDesktop = 'adb pull /sdcard/' + xmlfilename + ' C:\\Users\\' + getusername() + '\\Desktop\\'
        print(pulluixmlToDesktop)
    else:
        xmlfilename = deviceid + '.xml'
        uixmlfile = 'adb -s ' + deviceid + ' shell uiautomator dump /sdcard/' + xmlfilename
        pulluixmlToDesktop = 'adb -s ' + deviceid + ' pull /sdcard/' + xmlfilename + ' C:\\Users\\' + getusername() + '\\Desktop\\'
        print(pulluixmlToDesktop)
        
    # 保存当前界面xml并pull至桌面
    os.system(uixmlfile)
    os.system(pulluixmlToDesktop)
    
    # 打开xml文档
    tree = etree.parse('C:\\Users\\' + getusername() + '\\Desktop\\' + xmlfilename)
    result = tree.xpath(query)[0]
    print(f'result:{result}')
    if result == value:
        return True
    else:
        return False
