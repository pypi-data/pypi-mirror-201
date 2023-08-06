# coding: utf8

"""
写入者
将记录写入到文件，不处理pos
"""

import os
import datetime

from . import constants
from .bill import Bill
from .log import logger


class Writer(object):
    directory = None
    unit_fmt = None

    cur_unit = None
    cur_file = None

    def __init__(self, directory, unit_fmt=None):
        self.directory = directory
        self.unit_fmt = unit_fmt or constants.UNIT_FMT

    def write(self, data):
        """
        写入, 仅支持转换为字符串，因为文件中是以\n换行分割
        :param data:
        :return:
        """
        # 必须是bytes类型
        if not isinstance(data, bytes):
            data = data.encode('utf-8')

        now = datetime.datetime.now()

        try:
            unit = now.strftime(self.unit_fmt)
            if unit != self.cur_unit and self.cur_file:
                # 说明切换文件了，或者之前没有文件
                self.cur_file.close()
                self.cur_file = None

            if not self.cur_file:
                full_file_path = os.path.join(self.directory, unit)
                full_directory = os.path.dirname(full_file_path)
                if not os.path.exists(full_directory):
                    os.makedirs(full_directory)

                # unbuffered
                # 因为如果使用buffer，就会导致如果写入的大小超过了缓冲区大小，就会先立即写入磁盘一部分，剩下的在flush的时候才写入，这就混乱了
                self.cur_file = open(full_file_path, 'ab', buffering=0)
                # 打开文件成功之后，才来修改unit
                self.cur_unit = unit

            bill = Bill()

            bill.body = data

            str_bill = bill.pack()

            # python2 的write返回None
            # python3 的write返回实际写入的大小
            # 但是在测试的时候，写几兆的数据也能全部写入，还不知道实现上是否有什么区别
            self.cur_file.write(str_bill)
            # 不缓冲的情况下，不需要强制写入
            # self.cur_file.flush()

            return True
        except:
            logger.error('exc occur. data: %r', data, exc_info=True)
            return False
