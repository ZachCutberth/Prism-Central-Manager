# Change the number of prismmq consumers and restart the prismmq service.
# By Zach Cutberth

from configobj import ConfigObj
import sys
import win32serviceutil
import time

consumers = sys.argv[1]

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

def update_consumers(consumers):
    prismmq_ini = ConfigObj('c:\\ProgramData\\RetailPro\\Server\\Conf\\PrismMQService.ini')

    prismmq_ini['PRISM']['D2DRECVTHREADCNT'] = consumers
    prismmq_ini.write()

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

update_consumers(consumers)
restart_prismmq()