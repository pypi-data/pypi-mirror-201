

import os
from concurrent_log_handler import ConcurrentRotatingFileHandler as RotatingFileHandler
from concurrent_log_handler import logging
import sys
import datetime, time
from pytz import timezone
from hashlib import md5, sha1
import re
from typing import *


# color mapping
color = {
    'debug': '97',
    'info': '92',
    'warning': '96',
    'error': '93',
    'critical': '91',
    'b': '94',
    'p': '95',
    'z': '107'
}




def encrypt(char: Any, method='md5'):
    """
    :param char:        any character
    :param method:      recently only support md5 or sha1
    :return:
    """
    char = str(char)
    if method == 'md5':
        m = md5()
    elif method == 'sha1':
        m = sha1()
    m.update(char.encode('utf8'))
    return m.hexdigest()




class MyFormatter(logging.Formatter):
    """
    custom Format for console output with colors
    """


    # \033[95m|\033[0m


    def __init__(self, fmt=None, datefmt=None, style='%'):
        super(MyFormatter, self).__init__()


    def format(self, record):
        msg = record.getMessage()
        # add color by log level name
        level_name = re.search('【(.*?)】', msg).group(1)
        msg = msg.replace(f'【{level_name}】', f'\033[1m【{level_name}】\033[0m\033[{color[level_name.lower()]}m')
        msg = f'\033[{color[level_name.lower()]}m' + msg.replace('|', f'\033[95m\033[1m|\033[0m\033[{color[level_name.lower()]}m') + '\033[0m'
        record.message = msg
        # if self.usesTime():
        #     record.asctime = self.formatTime(record, self.datefmt)
        s = self.formatMessage(record)
        if record.exc_info:
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            if s[-1:] != "\n":
                s = s + "\n"
            s = s + record.exc_text
        if record.stack_info:
            if s[-1:] != "\n":
                s = s + "\n"
            s = s + self.formatStack(record.stack_info)
        return s




class Log:
    levels = {
        logging.DEBUG: 'debug',
        logging.INFO: 'info',
        logging.WARNING: 'warning',
        logging.ERROR: 'error',
        logging.CRITICAL: 'critical'
    }


    def __init__(self, func=None, name=None, log_path=None, gap=8, seperator='', log_config={}):


        """
        This module allows you to record different contents to diffeent files by different level in different modules in diffrent time.




        For example:
            Suppose we build a project with following constructure:
            project/
                main.py
                thread1.py
                thread2.py
            And, we want to log something belongs to warning level into 'main_warning.log' when main.py starts,
            then we want to log something belongs to info level into 'main_debug'.log' after 10 or more minutes later,
            then we want to log something belongs to error level into 'thread1_error'.log' if there is something wrong in thread1.py,
            and, these log files are all put into a file folder called 'logs'.
            We should:
                In main.py:
                    from llpack import log
                    logger = log.Log(name='main', log_path='logs')
                    logger.warning('main.py starts', "let's go", 'gogogo')
                    logger.info('data load successfully!')
                In thread1.py:
                    from llpack import log
                    logger = log.Log(name='mthread1', log_path='logs')
                    logger.error('error data', your_data)
            A nice convenience for this module is that, if we only warning sth, level including error, warning, debug ... xxx.log fiels won't
            be created utils we record sth belongs to the reletive level.




            For more detail, please go on...








        :param log_path:        path for recording logs, usually adn default is ./logs
        :param name:            log prefix name, [name]_[critical].log or something like that
        :param gap:             timezone diff from UTC to local timezone
                                For exmaple: if your location is Asia/Beijing, then gap should be 8 (GTM + 8)
        :param seperator        a seperator for each log




        Example:
            logger = log.Log(log_path='./log', name='tttt')
            logger.debug('This is a debug message', 'This msg contains there tips for watchers', 'And this is the last tip')
        Result:
            【DEBUG】  2021-07-16 15:20:26.595435 | File:/tmp/test.py | Func:NO_FUNC | Line:9
             Tips:
                tip1:      This is a debug message
                tip2:      This msg contains there tips for watchers
                tip3:      And this is the last tip
        """
        # 0 - 50
        self.log_mapping = {Log.levels[x]: x for x in Log.levels}


        # maxBytes means MB
        self.log_config = {
            'debug': {'maxBytes': 1, 'backupCount': 1},
            'info': {'maxBytes': 1, 'backupCount': 1},
            'warning': {'maxBytes': 1, 'backupCount': 2},
            'error': {'maxBytes': 5, 'backupCount': 5},
            'critical': {'maxBytes': 5, 'backupCount': 5}}
        self.log_config.update(log_config)
        self.init_log_path(log_path)


        # default log name looks like z_[lebel].log
        self.public_name = 'z' if not name else name
        self.gap = gap
        self.seperator = seperator


        self.func = func


        self.decorators = {10: self.debug, 20: self.info, 30: self.warning, 40: self.error, 50: self.critical,
                     'debug': self.debug, 'info': self.info, 'warning': self.warning, 'error': self.error, 'critical': self.critical}


        # initial log container
        self.logs = {}




    def init_log_path(self, log_path=None):
        """
        create folder if folder not exists




        :param log_path:        file folder to store xxx.log files
        :return:
        """


        # get current project path
        def helper():
            root = os.path.dirname(os.path.abspath(__file__))
            if root.find('pack') >= 0:
                root = os.getcwd()
            return root


        #  use current project path by default
        if not log_path:
            log_path = self.log_root = helper()


        # if delivered by "./", use current project path + log_path
        if log_path.startswith('./'):
            self.log_root = helper() + log_path[1:]




        # sometimes we are used to using log or logs
        elif log_path in {'logs', 'log'}:
            self.log_root = helper() + '/' + log_path




        # else log_path maybe an entire path
        else:
            if log_path.split('/')[-1].find('.') >= 0:
                self.log_root = os.path.dirname(log_path)
            else:
                self.log_root = log_path
            if self.log_root == '//':
                self.log_root = '/'
            if not self.log_root.endswith('/'):
                self.log_root += '/'
        if not os.path.exists(self.log_root):
            os.makedirs(self.log_root)
        print('Log path --->>> ', self.log_root)


    def init_config(self, name=None, out=0):
        """
        initial logger handler




        :param name:        log level
        :param out          if a log message should be displayed on console




        """


        logging.Formatter.converter = self.opti_time


        base_format = logging.Formatter()


        # logging.Formatter.converter = customTime
        if name not in self.logs:


            # create logger
            logger = logging.getLogger(encrypt(time.time()))
            # else:
            #     logger = logging.getLogger(self.public_name)
            logger.setLevel(self.log_mapping[name])


            # create handler
            log_path = self.log_root + '/' + self.public_name + '_' + name + '.log'
            base_handler = RotatingFileHandler(log_path,
                                               maxBytes=self.log_config[name]['maxBytes'] * 1024 * 1024,
                                               backupCount=self.log_config[name]['backupCount'])


            # define output format
            base_handler.setFormatter(base_format)
            base_handler.setLevel(self.log_mapping[name])


            # add handler
            logger.addHandler(base_handler)


            # critical level add console handler
            if out:
                console_handler = logging.StreamHandler()
                console_handler.setLevel(self.log_mapping[name])
                # custom format
                console_format = MyFormatter()
                console_handler.setFormatter(console_format)
                logger.addHandler(console_handler)
            self.logs.update({name: logger})


    def update_config(self, name: str, out=0):
        """
        Add log handler dynamically.
        For avoiding all the log files( including empty log files ) added into log_path during initializing.
        """
        name = name.lower()
        assert name in {'debug', 'info', 'warning', 'error', 'critical'}, 'log level is not correct!'
        self.init_config(name, out)


    @staticmethod
    def combine(*msg, level_name, depth=3, seperator='', func_name=None):
        """
        By this func, you can indirectly receive other three params:
            call_module_name:       point to file which call log function
            call_module_line:       poinrt to line which call log function of "call_module_name"
            call_func_name:         poinrt to func which call log function of "call_module_name"




        In this func, message from log will be combine into the format that builtin func log needs, and for convenience as well.
        Param depth=3 means func can backtrack to 3 calls(raw_func--->>>waring[2]--->>>pre_operate[1]--->>>combine[0]) when reaching combine func.
        As I designed, output format looks like




        2020-01-19 12:59:49,144 [pid] | File:     call_module_name | Func:     call_func_name | Line:     call_module_line
        Tips:
            tip0:      msg1
            tip1:      msg2
            tip2:      msg3
            ...




        """
        level_name = level_name.upper()
        call_func_name = func_name or sys._getframe(depth).f_code.co_name
        call_module_line = sys._getframe(depth).f_lineno
        call_module_name = sys._getframe(depth).f_code.co_filename


        if str(call_func_name) == '<module>':
            call_func_name = 'NO_FUNC'


        msg = list(map(str, msg))
        e = msg[-1]
        if isinstance(e, Exception):
            information = msg[:-1]
            if not information:
                information = ['']
        else:
            e = None
            information = msg
        information = ''.join(['\n    ' + 'tip%s:      %s' % (i + 1, information[i]) for i in range(len(information))])
        if e:
            content = f'【{level_name}】  {datetime.datetime.now()}' + \
                      ' | File:' + str(e.__traceback__.tb_frame.f_code.co_filename) + \
                      ' | Func:' + str(e.__traceback__.tb_frame.f_code.co_name) + \
                      ' | Line:' + str(e.__traceback__.tb_lineno) + \
                      ' | Errs:' + str(e) + \
                      ' \n Tips:' + \
                      information
        else:
            content = f'【{level_name}】  {datetime.datetime.now()}' + \
                      ' | File:' + call_module_name + \
                      ' | Func:' + call_func_name + \
                      ' | Line:' + str(call_module_line) + \
                      ' \n Tips:' + \
                      information
        return content + f'\n{seperator}' + '\n'


    def pre_operate(self, *msg, level_name, func_name=None, out=0):
        """
        combine messages and udate new logger handler(if new level of log added)
        """
        information = self.combine(*msg, func_name=func_name, level_name=level_name, depth=3, seperator=self.seperator)
        self.update_config(level_name, out=out)
        return information


    def warning(self, *msg, out=0, func_name=None):
        level_name = sys._getframe().f_code.co_name
        information = self.pre_operate(*msg, func_name=func_name, level_name=level_name, out=out)
        return self.logs[level_name].warning(information)


    def error(self, *msg, out=0, func_name=None):
        level_name = sys._getframe().f_code.co_name
        information = self.pre_operate(*msg, func_name=func_name, level_name=level_name, out=out)
        return self.logs[level_name].error(information)


    def critical(self, *msg, out=0, func_name=None):
        level_name = sys._getframe().f_code.co_name
        information = self.pre_operate(*msg, func_name=func_name, level_name=level_name, out=out)
        return self.logs[level_name].critical(information)


    def debug(self, *msg, out=0, func_name=None):
        level_name = sys._getframe().f_code.co_name
        information = self.pre_operate(*msg, func_name=func_name, level_name=level_name, out=out)
        return self.logs[level_name].debug(information)


    def info(self, *msg, out=0, func_name=None):
        level_name = sys._getframe().f_code.co_name
        information = self.pre_operate(*msg, func_name=func_name, level_name=level_name, out=out)
        return self.logs[level_name].info(information)


    def opti_time(self, *args):
        utc_tz = timezone('UTC')
        new_datetime = datetime.datetime.now(tz=utc_tz) + datetime.timedelta(hours=self.gap)
        return new_datetime.timetuple()


    def catch(self, *msg, level=40, out=0):
        """


        :param msg:
        :param level:
        :param out:
        :return:


        :reference:     loguru._logger.Logger.catch
        """


        tmp = msg[0] if msg else None
        if isinstance(tmp, Callable):
            func = msg[0]
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    self.decorators[level](*msg[1:], e, out=1, func_name=func.__name__)
            return wrapper
        else:
            def wrapper(func):
                def inner_wrapper(*args, **kwargs):
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        self.decorators[level](*msg, e, out=out, func_name=func.__name__)
                return inner_wrapper


            return wrapper

