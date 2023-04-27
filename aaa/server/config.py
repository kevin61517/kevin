import logging
import time
from datetime import timedelta
from logging import StreamHandler
import sys


class Config:
    # 預設True(這裡不使用)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # mysql url
    SQLALCHEMY_DATABASE_URI = ""
    # 收回連線時間
    SQLALCHEMY_POOL_RECYCLE = 3600
    # 超時時間
    SQLALCHEMY_POOL_TIMEOUT = 20
    # 連線池大小(默認5)
    SQLALCHEMY_POOL_SIZE = 4
    # 控制在連接池達到最大值後可以創建的連接數。當這些額外的連接回收到連接池後將會被斷開和拋棄。
    SQLALCHEMY_MAX_OVERFLOW = 6
    # 綁定多資料庫
    SQLALCHEMY_BINDS = {'其他資料庫名稱': '其他資料庫URI'}
    SQL_ECHO = False
    SQLALCHEMY_RECORD_QUERIES = True
