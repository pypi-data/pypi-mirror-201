import sys
import os
import argparse
import threading
import urllib3
import logging
import shutil
import datetime
from pkg_resources import get_distribution
from pkg_resources import parse_version
import platform

# sys.path.append("..")
from mecord import xy_pb 
from mecord import utils
from mecord import xy_user
from mecord import mecord_service
from mecord import mecord_widget
from mecord import store

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
subparsers = parser.add_subparsers()
parser_widget = subparsers.add_parser("deviceid", help="获取当前设备ID")
parser_widget = subparsers.add_parser("set_multitask_num", help="设置同时处理任务数量")
parser_widget = subparsers.add_parser("get_multitask_num", help="获取同时处理任务数量")
parser_widget = subparsers.add_parser("unbind", help="取消mecord绑定的数据")
parser_widget = subparsers.add_parser("show_token", help="展示当前设备token")
parser_widget = subparsers.add_parser("add_token", help="填入其他设备token")
parser_widget = subparsers.add_parser("report", help="反馈")
parser_widget = subparsers.add_parser("widget", help="widget模块")
parser_widget.add_argument("init", type=str, default=None, help="创建widget, 注意: 需要在空目录调用")
parser_widget.add_argument("publish", type=str, default=None, help="发布模块")
parser_widget.add_argument("list", type=str, default=None, help="本地支持的widget列表")
parser_widget.add_argument("add", type=str, default=None, help="添加新的本地widget执行库")
parser_widget.add_argument("remove", type=str, default=None, help="删除指定的widget")
parser_widget.add_argument("pending_task", type=str, default=None, help="获取指定任务的待处理任务数量")
parser_service = subparsers.add_parser("service", help="service模块")
parser_service.add_argument("start", type=str, default=None, help="start task loop service")

def service():
    if xy_user.User().isLogin() == False:
        utils.mecordPrint('please login first! \nUsage: mecord deviceid & Use Mecord Application scan it')
        return
    map = store.widgetMap()
    if len(map) == 0:
        utils.mecordPrint("please add widget first! \nUsage: mecord widget add [widget python path]")
        return
    if len(sys.argv) <= 2:
        utils.mecordPrint('please set command! Usage: mecord service start')
        return

    command = sys.argv[2]
    service = mecord_service.MecordService()
    if command == 'start':
        if service.is_running():
            utils.mecordPrint('Service is already running.')
        else:
            utils.mecordPrint('Starting service...')
            service.start()
    elif command == 'stop':
        if not service.is_running():
            utils.mecordPrint('Service is not running.')
        else:
            utils.mecordPrint('Stopping service...')
            service.stop()
    elif command == 'restart':
        utils.mecordPrint('Restarting service...')
        service.restart()
    elif command == 'status':
        if service.is_running():
            utils.mecordPrint('Service is running.')
        else:
            utils.mecordPrint('Service is not running.')
    else:
        utils.mecordPrint("Unknown command:", command)
        utils.mecordPrint("Usage: python service.py [start|stop|restart|status]")
        
def widget():
    if xy_user.User().isLogin() == False:
        utils.mecordPrint('please login first! \nUsage: mecord deviceid & Use Mecord Application scan it')
        return
    if len(sys.argv) <= 2:
        utils.mecordPrint('please set command! Usage: mecord widget [init|publish]')
        return

    command = sys.argv[2] 
    work_path = os.getcwd()
    if len(sys.argv) > 3:
        work_path = sys.argv[3]
    if command == 'init':
        mecord_widget.createWidget(work_path)
    elif command == 'publish':
        mecord_widget.publishWidget(work_path)
    elif command == 'list':
        map = store.widgetMap()
        if len(map) == 0:
            utils.mecordPrint("local widget is empty")
        maxJust = 20
        for it in map:
            if len(it) > maxJust:
                maxJust= len(it)
        for it in map:
            utils.mecordPrint(f"{it.ljust(maxJust + 4)} {map[it]}")
    elif command == 'add':
        mecord_widget.addWidgetToEnv(work_path)
    elif command == 'remove':
        mecord_widget.remove(work_path)
    elif command == 'pending_task':
        mecord_widget.getTaskCount(work_path)
    else:
        utils.mecordPrint("Unknown command:", command)
        utils.mecordPrint("Usage: mecord widget [init|publish|list|add|remove|pending_task]")

_max_checkdevice_count = 300 #loop waiting 5min
_cur_checkdevice_count = 0
def checkDeviceInfo():
    global _max_checkdevice_count
    global _cur_checkdevice_count
    if _cur_checkdevice_count > _max_checkdevice_count:
        return
    if xy_pb.GetAigcDeviceInfo():
        if store.isCreateWidget():
            mecord_widget.createDemoWidget()
    else:
        _cur_checkdevice_count += 1
        threading.Timer(1, checkDeviceInfo, ()).start()
        
def unbind():
    xy_pb.DeviceUnbind()
    store.clear()
    utils.mecordPrint(f"your device is return to initialization state!")

def deviceid():
    global _cur_checkdevice_count
    xy_user.User().loginIfNeed()
    uuid = utils.generate_unique_id()
    qrcode_str = f"https://main_page.html?action=scanbind&deviceId={uuid}"
    utils.displayQrcode(qrcode_str)
    utils.mecordPrint(f"your deviceid is : {uuid}, scan qrcode is : {qrcode_str}")
    if xy_user.User().isLogin() == False:
        utils.mecordPrint(f"waiting for scan...")
    _cur_checkdevice_count = 0
    checkDeviceInfo()
        
def joinToken():
    if len(sys.argv) <= 2:
        utils.mecordPrint('can not found token! Usage: mecord add_token {token}')
        return
    if xy_pb.ExpansionWithToken(sys.argv[2]):
        utils.mecordPrint('success')

def showToken():
    t = store.token()
    if len(t) > 0:
        utils.mecordPrint(f"your token is : {t}")
        utils.displayQrcode(t)
    else:
        utils.mecordPrint(f"not have token")

def setMultitaskNum():
    if len(sys.argv) <= 2:
        utils.mecordPrint('please set multitasking number')
        return
    if sys.argv[2].isdigit() == False:
        utils.mecordPrint('multitasking number is not digit')
        return
    if sys.argv[2] < 1:
        utils.mecordPrint(f'multitasking number illegal, {sys.argv[2]} must be greater than 1')
        return
    store.setMultitaskNum(sys.argv[2])
    utils.mecordPrint(f"multitasking number is {sys.argv[2]}")
    
def getMultitaskNum():
    t = store.multitaskNum()
    utils.mecordPrint(f"multitasking number is {t}")

def report():
    utils.reportLog()
    utils.mecordPrint(f"report success")

def version():
    ver = get_distribution("mecord-cli").version
    utils.mecordPrint(f"version is {ver}")

module_func = {
    "widget": widget,
    "service": service,
    "deviceid": deviceid,
    "unbind": unbind,
    "show_token": showToken,
    "add_token": joinToken,
    "set_multitask_num": setMultitaskNum,
    "get_multitask_num": getMultitaskNum,
    "report": report,
    "version": version
}

def main():
    if len(sys.argv) < 2:
        return

    urllib3.disable_warnings()
    logFilePath = f"{os.path.dirname(os.path.abspath(__file__))}/log.log"
    if os.path.exists(logFilePath) and os.stat(logFilePath).st_size > (1024 * 1024 * 5): #5m bak file
        d = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        bakFile = logFilePath.replace(".log", f"_{d}.log")
        shutil.copyfile(logFilePath, bakFile)
        os.remove(logFilePath)
    if parse_version(platform.python_version()) >= parse_version("3.9.0"):
        logging.basicConfig(filename=logFilePath, 
                            format='%(asctime)s %(levelname)s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            encoding="utf-8",
                            level=logging.INFO)
    else:
        logging.basicConfig(filename=logFilePath, 
                            format='%(asctime)s %(levelname)s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            # encoding="utf-8",
                            level=logging.INFO)
    
    try:
        module = sys.argv[1]
        if module in module_func:
            utils.mecordPrint(f"\n============== entry ===========\n", True)
            module_func[module]()
        else:
            utils.mecordPrint(f"Unknown command:{module}")
            utils.mecordPrint("Usage: mecord [deviceid|show_token|add_token|service|widget|version]")
            sys.exit(0)
    except Exception as e:
        utils.mecordPrint(f"uncatch Exception:{e}")
        return
        
if __name__ == '__main__':
        main()
