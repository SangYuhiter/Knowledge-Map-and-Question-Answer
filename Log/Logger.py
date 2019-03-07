# -*- coding: utf-8 -*-
'''
@File  : Logger.py
@Author: SangYu
@Date  : 2019/3/7 9:23
@Desc  : 日志系统
'''

import logging
import logging.handlers
import datetime

log_path = "../Logs/"


# 开发一个日志系统， 既要把日志输出到控制台， 还要写入日志文件
class MyLog:
    def __init__(self, logger):
        # 创建一个logger
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)

        # all.log文件中记录所有的日志信息，日志格式为：日期和时间 - 日志名 - 日志级别 - 日志信息
        rf_handler = logging.handlers.TimedRotatingFileHandler(log_path + 'all.log', when='midnight', interval=1,
                                                               backupCount=7,encoding="utf-8",
                                                               atTime=datetime.time(0, 0, 0, 0))
        rf_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))

        # error.log文件中单独记录error及以上级别的日志信息，日志格式为：日期和时间 - 日志级别 - 文件名[:行号] - 日志信息
        f_handler = logging.FileHandler(log_path + 'error.log',encoding="utf-8")
        f_handler.setLevel(logging.ERROR)
        f_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))

        # 输出到控制台
        c_handler = logging.StreamHandler()
        c_handler.setLevel(logging.DEBUG)
        c_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))

        self.logger.addHandler(rf_handler)
        self.logger.addHandler(f_handler)
        self.logger.addHandler(c_handler)

    def getlog(self):
        return self.logger


if __name__ == '__main__':
    mylogger = MyLog(logger="test").getlog()
    mylogger.debug("debug")
    mylogger.info("info")
    mylogger.error("error")
