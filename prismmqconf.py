# Change the prismmq configuration and stop, start, or restart the prismmq service.
# By Zach Cutberth

from configobj import ConfigObj
import sys
import win32serviceutil
import time

setting_name = sys.argv[1]

setting_value = sys.argv[2]

service_action = sys.argv[3]

def getServiceStatus(serviceName):
    try:
        service = win32serviceutil.QueryServiceStatus(serviceName)[1]
    except:
        return 'Not Installed'
    if service == 4:
        return 'Running'
    if service == 1:
        return 'Stopped'
    if service == 3:
        return 'Stopping'
    if service == 2:
        return 'Starting'

def checkStatus(service, action):
    if action == 'stop':
        currentStatus = getServiceStatus(service)
        while currentStatus != 'Stopped':
            currentStatus = getServiceStatus(service)
            time.sleep(1)

    if action == 'start':
        currentStatus = getServiceStatus(service)
        while currentStatus != 'Running':
            currentStatus = getServiceStatus(service)
            time.sleep(1)

def update_consumers(setting_value):
    prismmq_ini = ConfigObj('c:\\ProgramData\\RetailPro\\Server\\Conf\\PrismMQService.ini')

    prismmq_ini['PRISM']['D2DRECVTHREADCNT'] = setting_value
    prismmq_ini.write()

def update_loglevel(setting_value):
    prismmq_ini = ConfigObj('c:\\ProgramData\\RetailPro\\Server\\Conf\\PrismMQService.ini')

    prismmq_ini['LOG']['LogLevel'] = setting_value
    prismmq_ini.write()

def stop_prismmq():
    status = getServiceStatus('PrismMQService')
    if status != 'Stopped':
        try:
            win32serviceutil.StopService('PrismMQService')
        except:
            pass
        checkStatus('PrismMQService', 'stop')

def start_prismmq():
    status = getServiceStatus('PrismMQService')
    if status != 'Running':
        try:
            win32serviceutil.StartService('PrismMQService')
        except:
            pass
        checkStatus('PrismMQService', 'start')

def restart_prismmq():
    status = getServiceStatus('PrismMQService')
    if status == 'Running':
        try:
            win32serviceutil.StopService('PrismMQService')
        except:
            pass
        checkStatus('PrismMQService', 'stop')
        try:
            win32serviceutil.StartService('PrismMQService')
        except:
            pass
        checkStatus('PrismMQService', 'start')

    if status == 'Stopped':
        try:
            win32serviceutil.StartService('PrismMQService')
        except:
            pass
        checkStatus('PrismMQService', 'start')

if setting_name == 'consumers':
    update_consumers(setting_value)

if setting_name == 'loglevel':
    update_loglevel(setting_value)

if service_action == 'restart':
    restart_prismmq()

if service_action == 'stop':
    stop_prismmq()

if service_action == 'start':
    start_prismmq()

