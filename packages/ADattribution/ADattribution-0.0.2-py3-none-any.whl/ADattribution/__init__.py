#!/usr/bin/env python3
# coding = utf8
"""
@ Author : ZeroSeeker
@ e-mail : zeroseeker@foxmail.com
@ GitHub : https://github.com/ZeroSeeker
@ Gitee : https://gitee.com/ZeroSeeker
"""
from ua_parser import user_agent_parser
from difflib import SequenceMatcher
from adq_postback import adq_postback


def similarity(
        x: str,
        y: str
) -> float:
    """
    相似性算法，计算两个字符串的相似度；
    结果为介于0到1之间的float，0最不相似，1最相似
    """
    return SequenceMatcher(None, x, y).ratio()


def ip_ua_match(
        ip_x: str,
        ip_y: str,
        ua_x: str,
        ua_y: str,
        min_ip_similarity: float = 1.0,
        min_ua_similarity: float = 1.0,
        ua_similarity_keys: tuple = ('os', 'device')
) -> dict:
    """
    对传入的x端和y端的ip、ua按照条件判断是否匹配
    :param ip_x: x端的ip值
    :param ip_y: y端的ip值
    :param ua_x: x端的ua值
    :param ua_y: y端的ua值
    :param min_ip_similarity: ip最小相似度
    :param min_ua_similarity: ua最小相似度
    :param ua_similarity_keys: ua相似度比较键
    :return status 为True表示匹配成功，False为匹配失败

    判断ip为直接计算字符串的相似度；
    判断ua为，先格式化，然后对格式化后的有值的参数逐个比对，最后按照匹配成功的参数个数作为占总有效参数个数的比例为匹配度

    返回值
        code:
            0-匹配成功
            1-匹配失败，参数类型问题
            2-匹配失败，ip匹配度不满足要求
            3-匹配失败，ua匹配度不满足要求
        status:
            True-匹配成功
            False-匹配失败
        msg: 备注信息
        ip_similarity:
            ip匹配度
        ua_similarity:
            ua匹配度

    ua格式化后：
        {
            'user_agent': {
                'family': 'Other',
                'major': None,
                'minor': None,
                'patch': None
            },  # 浏览器信息
            'os': {
                'family': 'Other',
                'major': None,
                'minor': None,
                'patch': None,
                'patch_minor': None
            },  # 系统信息
            'device': {
                'family': 'Other',
                'brand': None,
                'model': None
            },  # 设备信息
            'string': 'a'  # 原值
        }
    """
    # 参数及格式判断
    if not isinstance(ip_x, str):
        return {
            'code': 1,
            'msg': 'ip_x is not str but %s' % type(ip_x),
            'status': False
        }
    if not isinstance(ip_y, str):
        return {
            'code': 1,
            'msg': 'ip_y is not str but %s' % type(ip_y),
            'status': False
        }
    if not isinstance(ua_x, str):
        return {
            'code': 1,
            'msg': 'ua_x is not str but %s' % type(ua_x),
            'status': False
        }
    if not isinstance(ua_y, str):
        return {
            'code': 1,
            'msg': 'ua_y is not str but %s' % type(ua_y),
            'status': False
        }
    if not isinstance(min_ip_similarity, float):
        return {
            'code': 1,
            'msg': 'min_ip_similarity is not float but %s' % type(min_ip_similarity),
            'status': False
        }

    if min_ip_similarity < 0 or min_ip_similarity > 1:
        return {
            'code': 1,
            'msg': 'min_ip_similarity must between 0 and 1 but %s' % type(min_ip_similarity),
            'status': False
        }

    if not isinstance(min_ua_similarity, float):
        return {
            'code': 1,
            'msg': 'min_ua_similarity is not float but %s' % type(min_ua_similarity),
            'status': False
        }

    if min_ua_similarity < 0 or min_ua_similarity > 1:
        return {
            'code': 1,
            'msg': 'min_ua_similarity must between 0 and 1 but %s' % type(min_ua_similarity),
            'status': False
        }

    # 先判断ip
    ip_similarity = similarity(ip_x, ip_y)
    if ip_similarity < min_ip_similarity:
        return {
            'code': 2,
            'msg': 'ip_similarity is %s (< %s)' % (round(ip_similarity, 2), min_ip_similarity),
            'ip_similarity': ip_similarity,
            'status': False
        }

    # 再判断ua
    ua_x_f = user_agent_parser.Parse(ua_x)
    ua_y_f = user_agent_parser.Parse(ua_y)
    total_point = 0  # 总计算点
    match_point = 0  # 匹配点
    invalid_point = 0  # 无效点
    for ua_similarity_key in ua_similarity_keys:
        ua_x_f_temp = ua_x_f[ua_similarity_key]
        ua_y_f_temp = ua_y_f[ua_similarity_key]
        temp_keys = list()
        temp_keys.extend(ua_x_f_temp.keys())
        temp_keys.extend(ua_y_f_temp.keys())
        temp_keys_set = set(temp_keys)
        for temp_key in temp_keys_set:
            ua_x_value = ua_x_f_temp[temp_key]
            ua_y_value = ua_y_f_temp[temp_key]
            if ua_x_value is None and ua_y_value is None:
                invalid_point += 1
            else:
                total_point += 1
                if ua_x_value == ua_y_value:
                    match_point += 1
    if total_point == 0:
        ua_similarity = 0
    else:
        ua_similarity = match_point / total_point
    if ua_similarity < min_ua_similarity:
        return {
            'code': 3,
            'msg': 'ua_similarity is %s (< %s)' % (round(ua_similarity, 2), min_ua_similarity),
            'ip_similarity': ip_similarity,
            'ua_similarity': ua_similarity,
            'status': False
        }
    return {
        'code': 0,
        'msg': 'ok',
        'ip_similarity': ip_similarity,
        'ua_similarity': ua_similarity,
        'status': True
    }
