# -*- coding: utf-8 -*-
# @Time    : 2023/1/31 16:42:40
# @Author  : Pane Li
# @File    : tools.py
"""
tools

"""
import logging
import os.path
import random
import re
import string
import subprocess
import threading
import time
import datetime
from typing import List
from inhandtest.file import del_file
import pytz
import requests
from inhandtest.file import file_hash


def loop_inspector(flag='status', timeout=90, interval=5, assertion=True):
    """装饰器，期望接收函数返回的值为True，如果为False时进行轮询，直至超时失败，如果正确就退出

    :param flag:  功能名称，用以输出日志，如果不填  默认为’状态’二字
    :param timeout:  循环检测超时时间
    :param interval:  循环检测时间间隔
    :param assertion: 默认期望断言，如果为False时 返回值
    :return:  assertion为False时，返回函数的值
    """

    def timeout_(func):
        def inspector(*args, **kwargs):
            for i in range(0, timeout + 1, interval):
                result = func(*args, **kwargs)
                if not result:
                    logging.info(f'{flag} assert failure, wait for {interval}s inspection')
                    time.sleep(interval)
                    continue
                else:
                    logging.info(f'{flag} assert normal')
                    return result
            else:
                if assertion:
                    raise AssertionError(f'{flag} assert timeout failure')

        return inspector

    return timeout_


def dict_merge(*dicts) -> dict:
    """合并多个字典

    :param dicts:
    :return:
    """
    result = {}
    for dict_ in dicts:
        if dict_ is not None:
            result.update(dict_)
    return result


def dict_flatten(in_dict, separator=":", dict_out=None, parent_key=None) -> dict:
    """ 平铺字典

    :param in_dict: 输入的字典
    :param separator: 连接符号
    :param dict_out:
    :param parent_key:
    :return: dict
    """
    if dict_out is None:
        dict_out = {}

    for k, v in in_dict.items():
        k = f"{parent_key}{separator}{k}" if parent_key else k
        if isinstance(v, dict):
            dict_flatten(in_dict=v, dict_out=dict_out, parent_key=k)
            continue

        dict_out[k] = v

    return dict_out


def timezone_change(time_str, src_timezone, dst_timezone=None, time_format=None) -> str:
    """
    将任一时区的时间转换成指定时区的时间
    如果没有指定目的时区，则默认转换成当地时区  时区参考https://www.beijing-time.org/shiqu/

    :param time_str:
    :param src_timezone: 要转换的源时区，如"Asia/Shanghai" 即东八区， 'Europe/London' 零时区  'Canada/Eastern' 西五区 UTC-5
    :param dst_timezone: 要转换的目的时区，如"Asia/Shanghai", 如果没有指定目的时区，则默认转换成当地时区
    :param time_format: 默认格式"%Y-%m-%d %H:%M:%S"
    :return: str, 字符串时间格式
    """
    if not time_format:
        time_format = "%Y-%m-%d %H:%M:%S"

    # 将字符串时间格式转换成datetime形式
    old_dt = datetime.datetime.strptime(time_str, time_format)

    # 将源时区的datetime形式转换成GMT时区(UTC+0)的datetime形式
    dt = pytz.timezone(src_timezone).localize(old_dt)
    utc_dt = pytz.utc.normalize(dt.astimezone(pytz.utc))

    # 将GMT时区的datetime形式转换成指定的目的时区的datetime形式
    if dst_timezone:
        _timezone = pytz.timezone(dst_timezone)
        new_dt = _timezone.normalize(utc_dt.astimezone(_timezone))
    else:
        # 未指定目的时间，默认转换成当地时区
        new_dt = utc_dt.astimezone()
    # 转换成字符串时间格式
    return new_dt.strftime(time_format)


def check_windows_process(process: str or int or list, kill=False) -> bool or List[bool]:
    """ 检测进程是否运行
    :param process: str|int|list, 进程名称或进程pid(不一定是应用程序名称！), eg:'3CDaemon'|'mosquitto'|49040 如果有多个时使用list传入
    :param kill: True|False 当为True时，将检测到的进程杀死
    :return: boolean
    """

    def _search(process_):
        if process_:
            if isinstance(process_, str) or isinstance(process_, int):
                command = f'tasklist |findstr {process_}'
            else:
                raise Exception("not support process type")
            logging.info(command)
            p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='gbk')
            task_result = p.communicate()[0].strip()
            logging.info(f'find {process_} process is: {task_result}')
            try:
                task_result = re.sub('\s+', ' ', task_result).split(' ')
                if len(task_result) == 6:
                    server_name = task_result[0]
                else:
                    server_name = False
            except Exception:
                server_name = False
            return server_name
        else:
            return False

    if not kill:
        if isinstance(process, list):
            return [_search(name_) for name_ in process]
        else:
            return _search(process)
    else:
        process = process if isinstance(process, list) else [process]
        for name_ in process:
            if isinstance(name_, str):
                pid = _search(name_)
                if pid:
                    logging.info(f'taskkill /F /IM {pid}')
                    p = subprocess.Popen(f'taskkill /F /IM {pid}', shell=True, stdout=subprocess.PIPE,
                                         stderr=subprocess.STDOUT, encoding='gbk')
                    logging.info(p.communicate()[0])
                    time.sleep(3)  # 删除服务应等待几秒，服务完全退出
                else:
                    logging.info(f'not found task {name_}')
            elif isinstance(name_, int):
                logging.info(f'taskkill /pid {name_} /F')
                p = subprocess.Popen(f'taskkill /pid {name_} /F', shell=True, stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT, encoding='gbk')
                logging.info(p.communicate()[0])
                time.sleep(3)  # 删除服务应等待几秒，服务完全退出
            else:
                raise Exception("not support process type")


def kill_windows_port(ip_, port: int or list) -> None:
    """ 杀死windows 相关端口服务

    :param ip_: 本机IP地址
    :param port: int|list, 端口号，可以是多个
    """
    import socket

    def kill_one_port(one_port: int):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind((ip_, one_port))
            except socket.error as e:
                command = f"taskkill /F /PID {one_port}"
                p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                     encoding='gbk')
                task_result = p.communicate()[0].strip()
                logging.info(f'port {one_port} is already in use, and kill result is {task_result}')
            else:
                s.close()

    [kill_one_port(port_) for port_ in port] if isinstance(port, list) else kill_one_port(port)


def download_svn_package(svn: dict, file_path, check_package=True) -> None:
    """

    :param svn: dict {'url': $url, 'username': $username, 'password': $password} 固件全路径
    :param file_path: 本地存放固件文件夹路径
    :param check_package: True|False 支持下载完文件后校验文件正确性
    :return:
    """
    from requests.auth import HTTPBasicAuth
    from requests.adapters import HTTPAdapter

    if svn.get("url") and svn.get('username') and svn.get('password') and file_path:
        url_path = svn.get("url")
        firmware_name = url_path.split('/')[-1]
        local_firmware_path = os.path.join(file_path, firmware_name)
        svn_hash_file_path = url_path.replace(firmware_name, 'sha256.txt')
        auth = HTTPBasicAuth(svn.get('username'), svn.get('password'))
        if not os.path.isfile(local_firmware_path):
            logging.info(f"download {local_firmware_path} from svn and wait for a moment!")
            s = requests.Session()
            s.mount('http://', HTTPAdapter(max_retries=3))  # 本身请求失败会重试3次
            for i in range(3):  # 文件下载错误再继续下载
                r = s.get(url_path, auth=auth)
                if r.status_code == 401:
                    raise Exception("svn username or password error")
                elif r.status_code == 200:
                    with open(local_firmware_path, 'wb') as fi_:  # 覆盖写入
                        fi_.write(r.content)
                    r_hash_file = s.get(svn_hash_file_path, auth=auth)
                    if check_package:
                        for co_ in r_hash_file.content.split(b'\n'):
                            if co_.decode('utf-8').endswith(firmware_name):
                                hash_sha256_value = co_.decode('utf-8').split(' ')[0].upper()
                                break
                        else:
                            raise Exception(f'{svn_hash_file_path} not contain {firmware_name} hash_sha256 value')
                        if file_hash(local_firmware_path, 'sha256') == hash_sha256_value:
                            logging.info(f'{local_firmware_path} download success')
                            break
                        else:
                            logging.warning(f'download package failed, try {i + 1} time')
                    else:
                        break
                else:
                    raise Exception("svn server down error")
            else:
                raise Exception('download package failed')


def get_time_stamp(time_='', delta=0, delta_type='h', time_format='%Y-%m-%dT%H:%M:%SZ') -> str:
    """获取时间戳

    :param time_: 默认获取当前时间
    :param delta: 要增加或者减少的时间
    :param delta_type: 单位 d:天 h:小时 m:分钟 s:秒
    :param time_format: 显示格式 ,为空时返回对应时间的时间戳
    :return:
    """
    delta_type = delta_type.lower()
    if delta_type == 'h':
        delta_time = datetime.timedelta(hours=delta)
    elif delta_type == 'm':
        delta_time = datetime.timedelta(minutes=delta)
    elif delta_type == 's':
        delta_time = datetime.timedelta(seconds=delta)
    elif delta_type == 'd':
        delta_time = datetime.timedelta(days=delta)
    else:
        delta_time = 0
    if not time_:
        time_stamp = datetime.datetime.utcnow() + delta_time
    else:
        time_stamp = datetime.datetime.strptime(time_, time_format) + delta_time
    res = time_stamp.strftime(time_format) if time_format else time_stamp.timestamp()
    return res


def dict_in(expect_dict: dict, contain: dict) -> None:
    """验证字典包含关系

    :param expect_dict: dict {key: value}
    :param contain: dict,  支持${value} 表达式判断
    :return: True or False
    """
    if expect_dict and contain:
        contain_flatten = dict_flatten(contain)  # 平铺字典
        expect_dict_flatten = dict_flatten(expect_dict)  # 平铺字典
        for contain_item, contain_value in contain_flatten.items():
            value = expect_dict_flatten.get(contain_item)
            if isinstance(contain_value, str) and '${value}' in contain_value:
                expect_value = contain_value.replace('${value}', str(value))
                if not eval(expect_value):
                    raise AssertionError(f'expect_item {contain_item} value is {expect_value} is False')
            else:
                assert value == contain_value, f'expect_item {contain_item} value is {contain_value} is False'

        else:
            logging.info(f'{contain} in {expect_dict} assert ok')


def replace_str(old: str or list or dict, replace_value: dict) -> str:
    """深度替换字符串，避免替换重复出问题

    :param old:
    :param replace_value:
    :return:
    """
    new_old = old

    def replace_(replace_str_: str):
        for k_, i_ in zip(replace_value.keys(), range(0, len(replace_value.keys()))):
            replace_str_ = replace_str_.replace(k_, '${' + str(i_) + '}')
        for v_, i_ in zip(replace_value.values(), range(0, len(replace_value.keys()))):
            replace_str_ = replace_str_.replace('${' + str(i_) + '}', v_)
        return replace_str_

    if old and replace_value:
        if isinstance(old, str):
            new_old = replace_(old)
        elif isinstance(old, list):
            new_old = [replace_(str(old_)) for old_ in old]
        elif isinstance(old, dict):
            new_old = {}
            for k, v in old.items():
                new_old.update({replace_(str(k)): v})
        else:
            raise Exception('Not support this type')
    return new_old


def generate_string(length, digits=True, lowercase=True, uppercase=True, special_chars=True, chinese_chars=False,
                    peer_chinese_chars_len=1):
    """生成指定长度的密码，可以选择包含类型，如（数字、大小写字母、特殊字符、中文）

    :param length: 密码长度
    :param digits: 是否包含数字
    :param lowercase: 是否包含小写字母
    :param uppercase: 是否包含大写字母
    :param special_chars: 是否包含特殊字符
    :param chinese_chars: 是否包含中文字符
    :param peer_chinese_chars_len: 每个中文的长度算几，默认是1， 可以选择为2
    :return: 生成的密码
    """
    all_type = {'chinese_chars': chinese_chars, 'digits': digits, 'lowercase': lowercase, 'uppercase': uppercase,
                'special_chars': special_chars}

    def shuffle_string(string_):
        """
        将输入的字符串打乱顺序并返回
        """
        # 将字符串转换为列表
        chars = list(string_)
        # 使用random.shuffle函数打乱列表顺序
        random.shuffle(chars)
        # 将列表转换为字符串并返回
        return ''.join(chars)

    def random_chinese_character():
        return random.choice(
            '读取指定目录下的机内码与转换工具在没修改编码格式时无法正确打印汉字解决方法为只要在文件开头加入勉强你我他是姐妹兄弟任务简体字列表')

    def generate_random(length_, type_='digits'):
        if type_ == 'digits':
            return ''.join(str(random.randint(0, 9)) for _ in range(length_))
        elif type_ == 'lowercase':
            return ''.join(random.choice(string.ascii_lowercase) for _ in range(length_))
        elif type_ == 'uppercase':
            return ''.join(random.choice(string.ascii_uppercase) for _ in range(length_))
        elif type_ == 'special_chars':
            return ''.join(random.choice(string.punctuation) for _ in range(length_))
        elif type_ == 'chinese_chars':
            length_ = int(length_ / 2) if peer_chinese_chars_len != 1 else length_
            return ''.join(random_chinese_character() for _ in range(length_))

    # 定义字符集
    def split_number(num, n, contain_even_=True):
        """
        将一个数字拆分成n个数字相加得来
        :param num: 要拆分的数字
        :param n: 拆分成n个数字相加
        :param contain_even_: 包含偶数
        :return: 拆分后的数字列表
        """
        value = []
        for i in range(n, 0, -1):
            if i != 1:
                if num - i > 0:
                    if contain_even_:
                        one = random.randrange(2, num - i, 2)
                        contain_even_ = False
                    else:
                        one = random.randint(1, num - i)
                    num = num - one
                elif num - i == 0:
                    if contain_even_:
                        raise Exception('The minimum generated string does not support the inclusion of Chinese char')
                    one = 1
                    num = num - one
                else:
                    raise Exception('the length of the generated string does not meet the kind requirement')
            else:
                one = num
            value.append(one)
        return value

    contain_char = [type_ for type_, exist_ in all_type.items() if exist_]
    result = ''
    if contain_char:
        contain_even = False if peer_chinese_chars_len == 1 else True
        len_spilt = split_number(length, len(contain_char), contain_even)
        for char_, len_ in zip(contain_char, len_spilt):
            result = result + generate_random(len_, char_)

    return shuffle_string(result)


def pytest_report_save(file_path, days=60, report_file_start_with='Report') -> str:
    """ 按照最大保存时间清理过期报告文件，清理时只限Report_2023-04-03-17这种格式， 且返回当前时间的报告文件名

    :param file_path: Report 文件所在的上级目录，
    :param days: Report 文件要保存的时间
    :param report_file_start_with: 报告文件的开头
    :return: 返回当前报告的文件名称， ex：Report_2023-04-03-17
    """

    def report_expired(file_name: str) -> bool:
        expired = False
        try:
            if report_file_start_with in file_name and file_name != report_file_start_with:
                report_time = file_name.replace(report_file_start_with + '_', '')
                report_time = datetime.datetime.strptime(report_time, '%Y-%m-%d-%H')
                if (datetime.datetime.now() - report_time).days >= days:
                    expired = True
        except Exception:
            pass
        finally:
            return expired

    if os.path.isdir(file_path):
        for i in os.listdir(file_path):
            if report_expired(i):
                import shutil
                shutil.rmtree(os.path.join(file_path, i))
                logging.info(f'{i} has expired days {days}, auto remove')

    return '_'.join([report_file_start_with, get_time_stamp(delta=+8, time_format='%Y-%m-%d-%H')])


def stop_thread(thread):
    """某些线程会在后台一直运行，当在外界满足一定条件时，是可以停掉的

    :param thread: 定义的线程
    :return:
    """
    import ctypes
    import inspect

    def _async_raise(tid, exctype):
        """raises the exception, performs cleanup if needed"""
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if res == 0:
            raise ValueError("invalid thread id or thread already stop")
        elif res != 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")
        else:
            logging.info(f'threading {thread} stop success')

    try:
        _async_raise(thread.ident, SystemExit)
    except Exception as e:
        logging.warning(e)


if __name__ == '__main__':
    import sys

    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO,
                        stream=sys.stdout)
    # print(pytest_report_save('D:\Python_project\pypi_common'))
    # print(generate_password(length=2, lowercase=True, uppercase=True, special_chars=True, chinese_chars=True))
    # print(get_time_stamp('2022-02-18T13:39:32Z', -2))
