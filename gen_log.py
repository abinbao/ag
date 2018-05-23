# coding:utf-8

import logging.handlers
import logging
"""
@desc 日志
"""

LOG_FILE = 'ag_cube_v1.log'
logging.basicConfig()
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1024 * 1024, backupCount=5)
fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
formatter = logging.Formatter(fmt)
handler.setFormatter(formatter)
logger = logging.getLogger('')
logger.addHandler(handler)
logger.setLevel(logging.WARN)
