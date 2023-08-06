import logging
from configparser import ConfigParser
from datetime import datetime
from logging.handlers import RotatingFileHandler
import os


def create_dir_not_exist(path):
    if not os.path.exists(path):
        os.mkdir(path)

create_dir_not_exist('logs')
rHandler = RotatingFileHandler("logs/%s-log.txt" % datetime.now().strftime('%Y%m%d'), maxBytes=500 * 1024 * 1024,
                               backupCount=100, encoding='UTF-8')
rHandler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
rHandler.setFormatter(formatter)
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)

configParser = ConfigParser()
configParser.read('conf/config.ini')
level = configParser.get('logging', 'level')

logging.basicConfig(level=level,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    handlers=[rHandler, console])

log = logging.getLogger()
log.addHandler(rHandler)
# formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
# # 第四步，将logger添加到handler里面
# rHandler = RotatingFileHandler("%s-log.txt" % datetime.now().strftime('%Y%m%d'), maxBytes=100 * 1024 * 1024, backupCount=10, encoding='UTF-8')
# rHandler.setLevel(logging.DEBUG)
# rHandler.setFormatter(formatter)
#
# console = logging.StreamHandler()
# console.setLevel(logging.INFO)
# console.setFormatter(formatter)
# log.addHandler(rHandler)
# log.addHandler(console)
