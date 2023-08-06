#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   DataWriter.py
@Time    :   2022/10/12 15:00:15
@Author  :   Shenxian Shi 
@Version :   
@Contact :   shishenxian@bluemoon.com.cn
@Desc    :   None
'''

# here put the import lib
import sys
import os
import json
import logging
from copy import deepcopy
from functools import wraps
sys.path.append(os.getcwd())

import pandas as pd
import requests

from easy_db.db import encrypt_dict
from bmai_dm_hbase.hbase_client import HBaseClient



LOG_FORMAT = logging.Formatter(
    '%(asctime)s - %(filename)s[line:%(lineno)d] %(levelname)s ' 
    '- %(message)s'
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
sh = logging.StreamHandler()
sh.setFormatter(LOG_FORMAT)
logger.addHandler(sh)

url_prefix = {
    'test':'https://tai.bluemoon.com.cn/aad-gateway/aad-data-mining',
    'prd': 'https://ai.bluemoon.com.cn/aad-gateway/aad-data-mining'
}


class APIError(Exception):
    def __init__(self, error_info) -> None:
        super().__init__(self)
        self.error_info = error_info

    def __str__(self) -> str:
        return self.error_info


class DataWriter(object):
    """
    数据写出模块, 包含直接写出hbase、调用接口写数等
    """
    def __init__(self, info: dict) -> None:
        """
        Construtor
        
        Args:
            info (dict): 包含一切所需信息的字典, 必须包含token_param, model_name, model_version, hbase, env
            
                token_param: dict, 登录接口所需的account(员工编号)与pwd(密码), {'account': xxx, 'pwd': xxx}
                model_name: str, 模型名称
                model_version: str, 模型版本
                hbase: dict, 测试和生产环境的ip、端口、表名、列族、行键名
                    {
                        'test': {
                            'host': xxx, 
                            'port': xxx,
                            'table_name': xxx,
                            'rowkeys_col': xxx,
                            'family': xxx
                        },
                        'prd': ...
                    }
                env: str, 'test' or 'prd'
        """
        self.content_dic = {
            'token_url': {'Content-Type': 'application/x-www-form-urlencoded'},
            'model_data_url': {'Content-Type': 'application/json'},
            'model_data_get': {'Content-Type': 'application/json'},
            'dm_dim_url': {'Content-Type': 'application/json'},
            'dm_dim_get': {'Content-Type': 'application/json'},
            'event_get': {'Content-Type': 'application/json'},
            'event_url': {'Content-Type': 'application/x-www-form-urlencoded'}
        }
        TOKEN_URL = '/system/login'
        MODEL_DATA_URL = '/modelRepository/saveOrUpdate'
        MODEL_DATA_GET = '/modelRepository/list'
        DM_DIM_URL = '/dimension/saveOrUpdate'
        DM_DIM_GET = '/dimension/list'
        EVENT_GET = '/eventFeedback/getEventGoodsListByEventType'
        EVENT_URL = '/eventFeedback/editTransferGoodsPace'
        self.TOKEN_URL = url_prefix[info['env']] + TOKEN_URL
        self.MODEL_DATA_URL = url_prefix[info['env']] + MODEL_DATA_URL
        self.MODEL_DATA_GET = url_prefix[info['env']] + MODEL_DATA_GET
        self.DM_DIM_URL = url_prefix[info['env']] + DM_DIM_URL
        self.DM_DIM_GET = url_prefix[info['env']] + DM_DIM_GET
        self.EVENT_GET = url_prefix[info['env']] + EVENT_GET
        self.EVENT_URL = url_prefix[info['env']] + EVENT_URL
        
        if not isinstance(info, dict):
            raise TypeError('Param info must be a dictionary.')
        elif ('model_name' not in info.keys()) | ('model_version' not in info.keys()):
            raise KeyError('"model_name" and "model_version" should be in param "info".')    
        self.info = info
        self.token = None
        self.header = {
            'Accept': '*/*'
        }
        self._model_data = None
        self._dim_data = None
        self.token = None
        self.parent_md5_id = None
        self._set_md5()
        self.encrypt_cols = [
            'parent_model_cd', 'model_date', 'data_date', 
            'date_type', 'first_dim', 'second_dim', 
            'third_dim', 'fourth_dim', 'fifth_dim'
            ]
        self.env = info['env']
        
    def _set_md5(self, model_name: str = None, model_version: str = None):
        model_name = model_name if model_name else self.info['model_name']
        model_version = model_version if model_version else self.info['model_version']
        self.parent_md5_id = encrypt_dict(
            {
                'modelName': model_name,
                'modelVersion': model_version
            },
            secret=self.info.get('md5_secret', None)
        )
    
    def get_token(func):
        # noinspection PyCallingNonCallable
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            hbase_info = self.info['hbase'][self.info['env']]
            hbase = HBaseClient(host=hbase_info['host'],
                            port=hbase_info['port'],
                            env=self.info['env'])
            hbase.build_pool()
            rk = encrypt_dict(self.info['token_param'])
            _, token_data = hbase.query(
                table_name='pred_system:dm_login_token',
                row_keys=rk
            )
            try:
                self.token = token_data[0][1]['INFO:token'.encode()].decode()
                self.header.update({'token': self.token})
            except KeyError:
                pass
            if not self.check_token():
                res = json.loads(requests.post(self.TOKEN_URL, params=self.info['token_param']).text)
                self.token = res['data']['token']
                self.header.update({'token': self.token})
                hbase.insert(
                    table_name='pred_system:dm_login_token',
                    datas={
                    rk: {
                        'token': self.token, 
                        'account': self.info['token_param']['account'],
                        'pwd': self.info['token_param']['pwd']
                    }
                })
                
            out = func(self, *args, **kwargs)
            return out
        return wrapper
            
    def check_token(self):
        self.header.update(self.content_dic['model_data_get'])
        test_res = json.loads(requests.get(url=self.MODEL_DATA_GET, headers=self.header).text)
        if (test_res['responseCode'] != 200) & ('token' in test_res['responseMsg']):
            return 0
        else:
            return 1
    
    @get_token
    def _get_model_data(self):
        """获取模型管理表数据
        """
        self.header.update(self.content_dic['model_data_get'])
        res = requests.get(url=self.MODEL_DATA_GET, headers=self.header).text
        self._model_data = pd.DataFrame(json.loads(res)['data'])
        
    def _check_model(self, target: dict, key_name: str):
        """

        Args:
            key_name (str): 'model_name' or 'model_version'

        Raises:
            ValueError
        """
        name_trans = {
            'modelName': 'model_name',
            'modelVersion': 'model_version'
        }
        if target.get(key_name, ''):
            if self.info[name_trans[key_name]] != target[key_name]:
                raise ValueError(
                        f'Key {key_name} in "data" and '
                        '"info" should be the same.'
                    )
        else:
            logger.info(
                f'Key {key_name} does not exist in the data dict, '
                f'fill in the {key_name} of "self.info" instead.'
            )
            target.update({key_name: self.info[name_trans[key_name]]})
    
    @get_token
    def check_model_data(self):
        """ 判断模型管理表数据是否存在
        此为简化步骤用。insert函数没有设限, 亦可进行更新操作, 只是需要传入的是全部字段, 比较繁琐
        
        Returns:
            bool: 0--不存在, 1--存在
        """
        self._get_model_data()
        if self.parent_md5_id in self._model_data['modelId'].values:
            return 1
        else:
            return 0
    
    @get_token
    def insert_model_data(self, data: dict):
        """模型管理表新增数据
           自带检查modelName, modelVersion功能
        Args:
            data (dict): 模型管理表字段信息, 可带modelName, modelVersion字段, 
                         但必须与__init__中info的modelName, modelVersion相同
        """
        from psycopg2.errors import ProgrammingError
        self._check_model(target=data, key_name='modelName')
        self._check_model(target=data, key_name='modelVersion')
        self._get_model_data()
        self.header.update(self.content_dic['model_data_url'])
        
        if data['modelName'] in self._model_data['modelName']:
            raw_sort = self._model_data.loc[
                    self._model_data['modelName'] == data['modelName'],
                    'modelSort'
                ].max()
            model_sort = raw_sort + 1
        else:
            model_sort = 1
            
        if data.get('deleteFlag', None) is not None:
            logger.warning(
                'Column deleteFlag is immutable, it could only be '
                'changed by web page.'
            )
        elif data.get('releaseStatus', None):
            logger.warning(
                'Column releaseStatus is immutable, it could only be '
                'changed by web page.'
            )
            
        try:
            if data.get('modelName', None) is not None:
                assert(data.get('modelName') == self.info['model_name']), \
                    '"modelName" must be equal to "model_name" in the yml file.'
            if data.get('modelVersion', None) is not None:
                assert(data.get('modelVersion') == self.info['model_version']), \
                    '"modelVersion" must be equal to "model_version" in the yml file.'

            new_data = {
                'dateType': data['dateType'],
                'deleteFlag': 0,
                'deployStatus': data['deployStatus'],
                'dimLevel': data['dimLevel'],
                'lastEndTime': data['lastEndTime'],
                'lastRunTime': data['lastRunTime'],
                'lastStartTime': data['lastStartTime'],
                'modelDesc': data['modelDesc'],
                'modelName': data.get('modelName', self.info['model_name']),
                'modelParam': data['modelParam'],
                'modelSort': model_sort,
                'modelStatus': data['modelStatus'],
                'modelVersion': data.get('modelVersion', self.info['model_version']),
                'releaseStatus': 0,
                'modelId': self.parent_md5_id
            }
        except KeyError:
            raise KeyError(
                'Column not found, or invalid column name. \n'
                'Please input all columns for the first insertion, except for "modelId", "modelSort", '
                '"releaseStatus" and "deleteFlag".\n'
                '"modelParam" must be in json string, which is generated by json.dumps().\n'
                '"modelName" and "modelVersion" are not necessary in this case, '
                'they are already contained in "info".\n'
                'Please use lower camel case, Eg. "modelName".'
            )
            
        res = requests.post(self.MODEL_DATA_URL, data=json.dumps(new_data), headers=self.header)
        res_code = json.loads(res.text)
        if res_code['responseCode'] != 200:
            raise APIError(f"Insertion failed, response code: {res_code['responseCode']}. "
                         f"Response msg: {res_code['responseMsg']}.")
        else:
            logger.info('Inserting done.')
        
    @get_token 
    def update_model_data(self, data: dict):
        """模型管理表更新数据

        Args:
            data (dict): 所需修改的数据, 可带model_name, model_version字段, 
                         但必须与__init__中info的model_name, model_version相同

        Raises:
        """
        from psycopg2.errors import ProgrammingError
        self._check_model(target=data, key_name='modelName')
        self._check_model(target=data, key_name='modelVersion')
        self._get_model_data()
        self.header.update(self.content_dic['model_data_url'])
        
        if self.parent_md5_id not in self._model_data['modelId'].values:
            raise ProgrammingError(
                'Primary key does not exist, please use '
                '"insert_model_data" method instead.'
            )
        else:
            if (data.get('modelId', None) is not None) & \
                (data.get('modelId') != self.parent_md5_id):
                logger.warning(
                    'You are updating another model, not '
                    f"{self.info['model_name']} -- {self.info['model_version']}"
                )
                
            data.update({'modelId': data.get('modelId', self.parent_md5_id)})
        
        if data.get('deleteFlag', None) is not None:
            logger.warning(
                'Column deleteFlag is immutable, it could only be '
                'changed by web page.'
            )
            del data['deleteFlag'] 
        elif data.get('releaseStatus', None):
            logger.warning(
                'Column releaseStatus is immutable, it could only be '
                'changed by web page.'
            )
            del data['releaseStatus']
        
        res = requests.post(self.MODEL_DATA_URL, data=json.dumps(data), headers=self.header)
        res_code = json.loads(res.text)
        if res_code['responseCode'] != 200:
            raise APIError(f"Updating failed, response code: {res_code['responseCode']}.\
                          response msg: {res_code['responseMsg']}.")
        else:
            logger.info('Updating done.')
    
    @get_token
    def _get_dim_data(self):
        self.header.update(self.content_dic['dm_dim_get'])

        res = requests.get(url=self.DM_DIM_GET, headers=self.header).text
        self._dim_data = pd.DataFrame(json.loads(res)['data'])
        
    @get_token
    def insert_dim_data(self, data: dict):
        """ 树形结构维度表插入数据

        Args:
            data (dict): 需插入的数据
        """
        self._get_dim_data()
        self.header.update(self.content_dic['dm_dim_url'])

        res = requests.post(self.DM_DIM_URL, data=json.dumps(data), headers=self.header)
        res_code = json.loads(res.text)
        if res_code['responseCode'] != 200:
            raise APIError(f"Insertion failed, "
                         f"response code: {res_code['responseCode']}. "
                         f"response msg: {res_code['responseMsg']}.")
        else:
            logger.info('Inserting done.')
    
    @get_token
    def update_dim_data(self, data: dict) -> None:
        """ 树形结构维度表更新数据

        Args:
            data (dict): 需修改的数据
        """
        self._get_dim_data()
        self.header.update(self.content_dic['dm_dim_url'])

        if not data.get('isUpdate', ''):
            data.update({'isUpdate': True})
        res = requests.post(self.DM_DIM_URL, data=json.dumps(data), headers=self.header)
        res_code = json.loads(res.text)
        if res_code['responseCode'] != 200:
            raise APIError(f"Updating failed, response code: {res_code['responseCode']}.\
                          response msg: {res_code['responseMsg']}.")
        else:
            logger.info('Updating done.')
    
    def _trans_hbase(self, data: pd.DataFrame, rowkeys_col: str, family: str):
        """ 检查row key是否存在, 不存在则按此名字生成
            为data的列名全部补上列族前缀
        
        Args:
            data (pd.DataFrame): the df has to be transformed.
            rowkeys_col (str): row key's column name
            family (str): 列族
        """
        from easy_db.db import encrypt_df
        data['parent_model_cd'] = self.parent_md5_id
        if rowkeys_col not in data.columns:
            data = encrypt_df(
                data, 
                self.encrypt_cols,
                secret=self.info.get('md5_secret', None)
            )
            data.rename(columns={'uuid': rowkeys_col}, inplace=True)
        raw_cols = data.columns.tolist()
        new_cols = []
        for col in raw_cols:
            if family in col:
                new_cols.append(col)
            elif col != rowkeys_col:
                new_cols.append(family + ':' + col)
            else:
                new_cols.append(col)
        data.columns = new_cols
    
    @get_token
    def get_event_data(self, data: dict):
        """获取事件数据

        Args:
            data (dict): 包含接口参数
                        参数有：
                            eventType: 事件类型 1-活动 2-直播 3-新品上市 4-店铺转品 5-月度规划 6-转品 99-其他
                            pageNum: 分页页码,示例值(1)
                            pageSize: 分页大小,示例值(1000)
        """
        self.header.update(self.content_dic['event_get'])

        res = requests.post(url=self.EVENT_GET, data=json.dumps(data), headers=self.header).text
        self.event_data = pd.DataFrame(json.loads(res)['data']['list'])

    @get_token
    def edit_event_pace(self, data: dict):
        """修改转品事件进度

        Args:
            data (dict): 包含接口参数
                        参数有：
                            eventId: 	事件id
                            pace: 转品进度, 示例: 0%~99.99%, 百分百仅支持:100%
        """
        self.header.update(self.content_dic['event_url'])

        res = requests.post(self.EVENT_URL, data=data, headers=self.header)
        res_code = json.loads(res.text)
        if res_code['responseCode'] != 200:
            raise APIError(f"Editting failed, response code: {res_code['responseCode']}.\
                          response msg: {res_code['responseMsg']}.")
        else:
            logger.info('Editting done.')

    def insert_forecast(self, data: pd.DataFrame):
        """ 预测数据写出

        Args:
            data (pd.DataFrame): The forecast results.
        """
        if not isinstance(data, pd.DataFrame):
            raise TypeError('Param data must be a pd.DataFrame')
        hbase_info = self.info['hbase'][self.info['env']]
        df = deepcopy(data)
        self._trans_hbase(
            data=df,
            rowkeys_col=hbase_info['rowkeys_col'], 
            family=hbase_info['family']
        )
        
        hbase = HBaseClient(host=hbase_info['host'],
                            port=hbase_info['port'],
                            env=self.info['env'])
        hbase.build_pool()
        hbase.insert_df(
            table_name=hbase_info['table_name'],
            df=df, 
            rowkeys_col=hbase_info['rowkeys_col']
        )
        logger.info(
            f"{self.info['model_name']} {self.info['model_version']} -- "
            "Inserting hbase successfully."
        )
