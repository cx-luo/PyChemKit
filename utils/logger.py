# -*- coding: utf-8 -*-
# @Time    : 2025/6/20 11:35
# @Author  : chengxiang.luo
# @Email   : chengxiang.luo@pharmaron.com
# @File    : logger.py
# @Software: PyCharm
import logging
import re
from logging import handlers

logfile = __name__ + '.log'
# logger 写在init里
fmt = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
logger = logging.getLogger(logfile)
logger.setLevel(logging.INFO)
logger_handler = handlers.TimedRotatingFileHandler(filename=logfile, when='D',
                                                   backupCount=30, encoding='utf-8', interval=1)
logger_handler.setFormatter(fmt)
# # 如果对日志文件名没有特殊要求的话，可以不用设置suffix和extMatch，如果需要，一定要让它们匹配上。
logger_handler.suffix = '%Y%m%d'
logger_handler.extMatch = re.compile(r"^\d{8}$")
logger.addHandler(logger_handler)
