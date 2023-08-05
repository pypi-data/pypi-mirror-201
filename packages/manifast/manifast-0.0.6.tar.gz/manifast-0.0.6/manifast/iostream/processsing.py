#!/usr/bin/env python
# coding=utf-8
'''
brief        :  
Author       : knightdby knightdby@163.com
Date         : 2023-02-24 21:58:02
FilePath     : /manifast/manifast/iostream/processsing.py
Description  : 
LastEditTime : 2023-04-04 15:04:31
LastEditors  : knightdby
Copyright (c) 2023 by Inc, All Rights Reserved.
'''
from multiprocessing import Pool
from tqdm import tqdm


def run(image_path):
    pass


def run_multi_threading(data_list, func):
    '''
    description: 多线程运行函数
    param       {*} data_list 所要处理数据 list
    param       {*} func 处理单条数据函数
    return      {*} 单条数据函数的返回值 list
    '''
    print('data_list size: ', len(data_list))
    with Pool(processes=10) as p:
        processed_data_list = list(
            tqdm(p.imap(func, data_list), total=len(data_list), desc='run multithread'))
    return processed_data_list
