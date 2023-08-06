#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   DataLoader.py
@Time    :   2022/10/12 15:00:10
@Author  :   Shenxian Shi 
@Version :   
@Contact :   shishenxian@bluemoon.com.cn
@Desc    :   None
'''

# here put the import lib
import sys
import os
import logging
from typing import Union
sys.path.append(os.getcwd())
sys.path.append('..')

from easy_db.db import ImpalaDB, HiveDB

from dm_platform_utils.utils import read_yml, process_dtypes


LOG_FORMAT = logging.Formatter(
    '%(asctime)s - %(filename)s[line:%(lineno)d] %(levelname)s ' 
    '- %(message)s'
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
sh = logging.StreamHandler()
sh.setFormatter(LOG_FORMAT)
logger.addHandler(sh)


def get_data(path):
    _ROOT = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(_ROOT, 'conf', path)


SQL_INFO = read_yml(get_data('sql.yml'))
PROCESS_DICT = read_yml(get_data('process_dtypes.yml'))


class DataLoader(object):
    """
    数据读取模块
    """
    
    def __init__(self, engine='impala', project='gyxt', host: str=None, port: Union[str, int]=None):
        """ Constructor

        Args:
            engine (str, optional): 取数引擎. Defaults to 'impala'.
            project (str, optional): 项目, gyxt or smart_operation. Defaults to 'gyxt'.
            host (str, optional): ip. Defaults to None.
            port (int, str, optional): 端口. Defaults to None.

        Raises:
            ValueError
        """
        self.project = project
        if engine == 'impala':
            self.conn = ImpalaDB(host=host, port=port)
        elif engine == 'hive':
            self.conn = HiveDB(host=host, port=port)
        else:
            raise ValueError('Engine should be either "impala" or "hive".')
        
    def get_data(self, dim:str = 'first_dim', date_type:str = 'month',
                 data_date:str = None):
        """ 取数

        Args:
            dim (str, optional): 业务维度. Defaults to 'first_dim'.
            date_type(str, optional): 日期类型. Defaults to 'month'. 
            data_date(str, optional): 日期. Defaults to None.
        """
        from datetime import datetime
        from dateutil.relativedelta import relativedelta
        
        date_fmt = '%Y%m' if date_type == 'month' else '%Y%m%d'
        if data_date is None:
            data_date = datetime.now().strftime(date_fmt)
        if 'dim' in dim:
            if dim in ['third_dim', 'fourth_dim', 'fifth_dim']:
                target_year = datetime.strptime(data_date, date_fmt) - \
                    relativedelta(years=1)
                lower_date = datetime.strftime(target_year, '%Y') + '01'
                upper_date = datetime.strftime(target_year, '%Y') + '12'
                sql = SQL_INFO[self.project][dim] % (
                    lower_date, upper_date, data_date, date_type
                )
            else:
                sql = SQL_INFO[self.project][dim] % (data_date, date_type)
        else:
            sql = SQL_INFO[self.project][dim][date_type] % data_date
        df = self.conn.select_df(sql=sql)
        data = process_dtypes(data=df, conf=PROCESS_DICT)
        return data

    def get_raw_data(self, dim:str = 'fifth_dim', data_date:str = None):
        """源数据取数

        Args:
            dim (str, optional): _description_. Defaults to None.
            date_type (str, optional): _description_. Defaults to None.
            data_date (str, optional): _description_. Defaults to None.
        """
        from datetime import datetime
        from dateutil.relativedelta import relativedelta
        

        if data_date is None:
            data_date = datetime.now().strftime('%Y%m%d')
        
        if 'dim' in dim:
            try:
                sql = SQL_INFO['gyxt_raw'][dim]
            except:
                logger.info('Only fifth dimension implemented.')
        df = self.conn.select_df(sql)
        data = process_dtypes(data=df, conf=PROCESS_DICT)
        return data
