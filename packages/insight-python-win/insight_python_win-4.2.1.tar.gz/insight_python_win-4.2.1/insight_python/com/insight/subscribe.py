#!/usr/bin/python3
# -*- coding: utf-8 -*-
import time

from .. import data_handle
from ..interface.mdc_gateway_base_define import SyncWait


def subscribe_tick_by_id(htsc_code, mode='coverage'):
    '''
    :param htsc_code: 华泰证券ID，支持多ID查询，list类型
    :param mode: 订阅方式 覆盖(coverage)， 新增（add）， 减少(decrease)， 取消(cancel)， 默认为coverage
    '''

    mode_map = {"coverage": 1, "add": 2, "decrease": 3, "cancel": 4}
    exchange_suffix_list = ['SH', 'SZ', 'CSI', 'CNI', 'BJ', 'HKSC', 'HGHQ', 'CF', 'SHF', 'DCE', 'ZCE']

    if not htsc_code:
        print('htsc_code can not be empty')
        return False

    if isinstance(htsc_code, str):
        htsc_code = [htsc_code]

    if isinstance(htsc_code, list) and isinstance(mode, str):
        htsc_codes_list = []
        for code in htsc_code:
            try:
                suffix = code.split(".")[-1]
                if suffix in exchange_suffix_list:
                    htsc_codes_list.append({'HTSCSecurityID': code, 'EMarketDataType': 1})
                else:
                    print('htsc_code {} does not support'.format(code))
                    return False
            except:
                print('htsc_code {} format error'.format(code))
                return False

        datatype = mode_map.get(mode)
        if datatype:
            data_handle.get_interface().subscribebyid(datatype, htsc_codes_list)
            time.sleep(SyncWait.wait_time)
        else:
            print("mode dose not exist")
    else:
        print("query or mode format error")


def subscribe_tick_by_type(query=None, mode='coverage'):
    '''
    :param query: 交易市场及对应的证券类型，元组类型，支持多市场多交易类型订阅，list类型 [(exchange1,security_type1),(exchange2,security_type2)]
    :param mode: 订阅方式 覆盖(coverage)， 新增（add）， 减少(decrease)， 取消(cancel)， 默认为coverage
    '''

    mode_map = {"coverage": 1, "add": 2, "decrease": 3, "cancel": 4}

    exchange_map = {'XSHG': 101, 'XSHE': 102, 'CSI': 703, 'CNI': 702, 'XBSE': 106, 'HKSC': 204, 'HGHQ': 205,
                    'CCFX': 301, 'XSGE': 302, 'XDCE': 601, 'XZCE': 602}

    security_type_map = {'index': 1, 'stock': 2, 'fund': 3, 'bond': 4, 'option': 7, 'future': 8}

    if not query:
        print('query can not be empty')
        return False

    if isinstance(query, list) and isinstance(mode, str):

        marketdatatype_list = []

        for marketdatatype in query:
            if isinstance(marketdatatype, tuple) and len(marketdatatype) == 2:
                try:
                    exchange = exchange_map[marketdatatype[0]]
                    security_type = security_type_map[marketdatatype[1]]
                    marketdatatype_list.append(
                        {'ESecurityIDSource': exchange, 'ESecurityType': security_type, 'EMarketDataType': 1})
                except:
                    print("exchange or security_type dose not exist")
                    return False

        datatype = mode_map.get(mode)
        if datatype:
            data_handle.get_interface().subscribebytype(datatype, marketdatatype_list)
            time.sleep(SyncWait.wait_time)
        else:
            print("mode dose not exist")
    else:
        print("query or mode format error")


def subscribe_kline_by_id(htsc_code=None, frequency=None, mode='coverage'):
    '''
    :param htsc_code: 华泰证券ID，支持多ID查询，list类型
    :param mode: 订阅方式 覆盖(coverage)， 新增（add）， 减少(decrease)， 取消(cancel)， 默认为coverage
    :param frequency: 频率，list类型，秒K（15s），分钟K（‘1min’）
    '''

    frequency_map = {'15s': 26, '1min': 20}
    mode_map = {"coverage": 1, "add": 2, "decrease": 3, "cancel": 4}
    exchange_suffix_list = ['SH', 'SZ', 'CSI', 'CNI', 'BJ', 'HKSC', 'HGHQ', 'CF', 'SHF', 'DCE', 'ZCE']

    if not frequency:
        frequency = ["1min"]

    if not htsc_code:
        print('htsc_code can not be empty')
        return False

    if isinstance(htsc_code, str):
        htsc_code = [htsc_code]

    if isinstance(htsc_code, list) and isinstance(frequency, list) and isinstance(mode, str):

        htsc_codes_list = []

        for fq in frequency:
            fq_code = frequency_map.get(fq)
            if fq_code:
                for code in htsc_code:
                    try:
                        suffix = code.split(".")[-1]
                        if suffix in exchange_suffix_list:
                            htsc_codes_list.append({'HTSCSecurityID': code, 'EMarketDataType': fq_code})
                        else:
                            print('htsc_code {} does not support'.format(code))
                            return False
                    except:
                        print('htsc_code {} format error'.format(code))
                        return False
            else:
                print(f"fq {fq} dose not exist")
                return False

        datatype = mode_map.get(mode)
        if datatype:
            data_handle.get_interface().subscribebyid(datatype, htsc_codes_list)
            time.sleep(SyncWait.wait_time)
        else:
            print("mode dose not exist")
    else:
        print("query or mode format error")


def subscribe_kline_by_type(query=None, frequency=None, mode='coverage'):
    '''
    :param query: 交易市场及对应的证券类型，元组类型，支持多市场多交易类型订阅，list类型 [(exchange1,security_type1),(exchange2,security_type2)]
    :param mode: 订阅方式  覆盖(coverage)， 新增（add）， 减少(decrease)， 取消(cancel)， 默认为coverage
    :param frequency: 频率，list类型，秒K（15s），分钟K（‘1min’）
    '''

    mode_map = {"coverage": 1, "add": 2, "decrease": 3, "cancel": 4}
    frequency_map = {'15s': 26, '1min': 20}
    exchange_map = {'XSHG': 101, 'XSHE': 102, 'CSI': 703, 'CNI': 702, 'XBSE': 106, 'HKSC': 204, 'HGHQ': 205,
                    'CCFX': 301, 'XSGE': 302, 'XDCE': 601, 'XZCE': 602}

    security_type_map = {'index': 1, 'stock': 2, 'fund': 3, 'bond': 4, 'option': 7, 'future': 8}

    if not frequency:
        frequency = ["1min"]

    if not query:
        print('query can not be empty')
        return False

    if isinstance(query, list) and isinstance(frequency, list) and isinstance(mode, str):

        marketdatatype_list = []

        for fq in frequency:
            fq_code = frequency_map.get(fq)
            if fq_code:
                for marketdatatype in query:
                    if isinstance(marketdatatype, tuple) and len(marketdatatype) == 2:
                        try:
                            exchange = exchange_map[marketdatatype[0]]
                            security_type = security_type_map[marketdatatype[1]]
                            marketdatatype_list.append(
                                {'ESecurityIDSource': exchange, 'ESecurityType': security_type,
                                 'EMarketDataType': fq_code})
                        except:
                            print("exchange or security_type dose not exist")
                            return False
            else:
                print(f"{fq} dose not exist")
                return False

        datatype = mode_map.get(mode)
        if datatype:
            data_handle.get_interface().subscribebytype(datatype, marketdatatype_list)
            time.sleep(SyncWait.wait_time)
        else:
            print("mode dose not exist")
    else:
        print("query or mode format error")


def subscribe_trans_and_order_by_id(htsc_code=None, mode='add'):
    '''
    :param htsc_code: 华泰证券ID，支持多ID查询，list类型
    :param mode: 订阅方式
    '''

    mode_map = {"coverage": 1, "add": 2, "decrease": 3, "cancel": 4}
    exchange_suffix_list = ['SH', 'SZ']

    if not htsc_code:
        print('htsc_code can not be empty')
        return False

    if isinstance(htsc_code, list) and isinstance(mode, str):
        htsc_codes_list = []
        for code in htsc_code:
            try:
                suffix = code.split(".")[-1]
                if suffix in exchange_suffix_list:
                    htsc_codes_list.append({'HTSCSecurityID': code, 'EMarketDataType': 3})
                    htsc_codes_list.append({'HTSCSecurityID': code, 'EMarketDataType': 2})
                else:
                    print('htsc_code {} does not support'.format(code))
                    return False
            except:
                print('htsc_code {} format error'.format(code))
                return False

        datatype = mode_map.get(mode)
        if datatype:
            data_handle.get_interface().subscribebyid(datatype, htsc_codes_list)
            time.sleep(SyncWait.wait_time)
        else:
            print("mode dose not exist")
    else:
        print("query or mode format error")


def subscribe_trans_and_order_by_type(query=None, mode='add'):
    '''
    :param query: 交易市场，支持多市场查询，list类型 [(exchange1,security_type1),(exchange2,security_type2)]
    :param mode: 订阅方式
    '''

    mode_map = {"coverage": 1, "add": 2, "decrease": 3, "cancel": 4}

    exchange_map = {'XSHG': 101, 'XSHE': 102}

    security_type_map = {'stock': 2, 'fund': 3, 'bond': 4}

    if isinstance(query, list) and isinstance(mode, str):

        marketdatatype_list = []

        for marketdatatype in query:
            if isinstance(marketdatatype, tuple) and len(marketdatatype) == 2:
                try:
                    exchange = exchange_map[marketdatatype[0]]
                    security_type = security_type_map[marketdatatype[1]]
                    marketdatatype_list.append(
                        {'ESecurityIDSource': exchange, 'ESecurityType': security_type, 'EMarketDataType': 2})
                    marketdatatype_list.append(
                        {'ESecurityIDSource': exchange, 'ESecurityType': security_type, 'EMarketDataType': 3})
                except:
                    print("exchange or security_type dose not exist")
                    return False

        datatype = mode_map.get(mode)
        if datatype:
            data_handle.get_interface().subscribebytype(datatype, marketdatatype_list)
            time.sleep(SyncWait.wait_time)
        else:
            print("mode dose not exist")
    else:
        print("query or mode format error")


def subscribe_derived(type=None, htsc_code=None, exchange=None, frequency='1min', mode='coverage'):
    '''
    :param type: 订阅数据类型
    :param htsc_code : 华泰证券ID，支持多ID订阅，list类型
    :param exchange : 证券市场代码
    :param frequency: 频率
    :param mode: 订阅方式 覆盖(coverage)， 新增（add）， 减少(decrease)， 取消(cancel)， 默认为coverage
    :param additional:
    '''

    if isinstance(htsc_code, str):
        htsc_code = [htsc_code]

    if not isinstance(htsc_code, list):
        print('htsc_code format error')
        return False

    mode_map = {"coverage": 1, "add": 2, "decrease": 3, "cancel": 4}
    datatype = mode_map.get(mode)
    if not datatype:
        print("mode dose not exist")
        return False

    if type == 'north_bound':
        north_bound_htsc_code_list = ['SCHKSBSH.HT', 'SCHKSBSZ.HT', 'SCSHNBHK.HT', 'SCSZNBHK.HT']
        if htsc_code:
            sub_htsc_code_list = []
            for code in htsc_code:
                if code in north_bound_htsc_code_list:
                    sub_htsc_code_list.append(code)

            if sub_htsc_code_list:
                sub_params = []
                for sub_code in sub_htsc_code_list:
                    sub_params.append({'HTSCSecurityID': sub_code, 'EMarketDataType': 1})

                data_handle.get_interface().subscribebyid(datatype, sub_params)
                time.sleep(SyncWait.wait_time)

            else:
                print('invalid htsc_code')
                return False

        else:
            print('htsc_code can not be empty')
            return False

    else:
        print('type dose not exist')



# 阻塞当前线程，防止本模块执行退出操作
def sync():
    # print("input any key to exit >>>")
    line = input()
    if len(str(line)) > 0:
        print("sync: input-->>" + str(line) + ",then exit this sync.")
