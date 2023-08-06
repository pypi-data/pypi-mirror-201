# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 08:53:25 2023

@author: Suliang

Email: suliang_321@sina.com

TO: QDer, GO GO GO!

"""

import io
import time
import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import datetime as dt

from tqdm import tqdm
from ftplib import FTP


class DataChannel():
    def __init__(self, username, password, host='124.223.105.49'):
        """
        host: FTP服务器地址
        username: 账号
        password: 密码
        """
        
        self.ftp = FTP(timeout=100)
        self.ftp.encoding = 'gbk'
        
        self.ftp.connect(host)
        try:
            self.ftp.login(username, password)
        except:
            print('【{}】用户信息有误，请检查输入是否正确。'.format(username))
        self.ftp.set_pasv(True)
        print("【{}】已成功链接服务器...有问题请联系suliang".format(username))
        self.factor_info = self.get_factor_info()
        
    def connect(self, username, password, host='124.223.105.49'):
        self.ftp = FTP()
        self.ftp.encoding = 'gbk'
        self.ftp.connect(host)
        self.ftp.login(username, password)
        self.ftp.set_pasv(True)
        print("【{}】已成功链接服务器...有问题请联系suliang".format(username))
    
    def get_factor_info(self):
        # 获取当前可供现在的因子列表
        factor_list = []
        self.ftp.dir(r'/因子库', factor_list.append)
        factor_list = [x.split(' ')[-1] for x in factor_list]
        result = pd.DataFrame(index=pd.Series(factor_list, name='因子名称'))
        for factor_name in factor_list:
            file_list = []
            self.ftp.dir(r'\因子库\{}'.format(factor_name), file_list.append)
            file_list = sorted([x.split(' ')[-1].split('.')[0] for x in file_list])[1:]
            result.loc[factor_name, '起始日期'], result.loc[factor_name, '最新日期'] = min(file_list), max(file_list)
        print(result)
        return result
    
    def get_factor(self, factor_name, end_date=None, start_date='20180101', is_stated=True):
        # 下载因子数据
        def read_file(ftp, remotepath):
            file = io.BytesIO()
            ftp.retrbinary('RETR ' + remotepath, file.write)
            file.seek(0)
            if remotepath.split('.')[-1] == 'csv':
                result = pd.read_csv(file, engine='python', encoding='utf_8_sig')
            elif remotepath.split('.')[-1] == 'txt':
                result = pd.read_table(file, encoding='gbk', header=None)
            return result
        
        # 输出因子说明
        factor_statement = read_file(self.ftp, r'\因子库\{}\0.因子计算说明.txt'.format(factor_name))
        [print(x[0]) for x in list(factor_statement.values)]
        time.sleep(1)
        
        # 获取因子历史样本的日期列表
        fn = lambda x: x.split('/')[-1]
        date_list = pd.Series([x.split('.')[0] for x in list(self.ftp.nlst(r'\因子库\{}'.format(factor_name)))]).map(fn).iloc[1:]
        
        if end_date is None:
            end_date = dt.datetime.now().strftime('%Y%m%d')
            temp_date_list = sorted(date_list[(date_list>=start_date)&(date_list<=end_date)])
        elif isinstance(end_date, list):
            temp_date_list = sorted(set(end_date).intersection(set(date_list)))
        else:
            temp_date_list = sorted(date_list[(date_list>=start_date)&(date_list<=end_date)])
        
        # 读取数据, 速度可能偏慢
        result = []
        for date in tqdm(temp_date_list):
            result.append(read_file(self.ftp, r'\因子库\{}\{}.csv'.format(factor_name, date)))
        result = pd.concat(result,keys=temp_date_list,names=['日期']).reset_index().set_index(['日期', '证券代码'])['因子暴露'].unstack()
        return result
    
    def download_file(self, remotepath, localpath):
        """
        remotepath: 远程路径
        localpath: 本地路径
        """
        fp = open(localpath, 'wb')
        self.ftp.retrbinary('RETR ' + remotepath, fp.write)
        self.ftp.set_debuglevel(0)
        fp.close()
        return None
    
    def upload_file(self, remotepath, localpath):
        """
        remotepath: 远程路径
        localpath: 本地路径
        """
        fp = open(localpath, 'rb')
        self.ftp.storbinary('STOR ' + remotepath, fp)
        self.ftp.set_debuglevel(0)
        fp.close()
        return None

if __name__  == '__main__':
    dc = DataChannel('suliang', '863228920')
    time.sleep(10)
    dc.get_factor_info()