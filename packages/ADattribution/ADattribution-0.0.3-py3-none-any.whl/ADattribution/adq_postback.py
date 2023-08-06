#!/usr/bin/env python3
# coding = utf8
"""
@ Author : ZeroSeeker
@ e-mail : zeroseeker@foxmail.com
@ GitHub : https://github.com/ZeroSeeker
@ Gitee : https://gitee.com/ZeroSeeker
"""
from urllib import parse
import requests


def adq_postback(
        callback_url,
        action_type,
        action_value=None
):
    """
    回传功能
    :param callback_url: 回传参数
    :param action_type: 回传类型
    :param action_value: 回传类型对于金额
    """
    callback_str_decode = parse.unquote(callback_url)
    if action_value is None:
        actions = [
                {
                    "action_type": action_type
                }
            ]
    else:
        actions = [
            {
                "action_type": action_type,
                "value": str(action_value)
            }
        ]
    response = requests.request(
        method='POST',
        url=callback_str_decode,
        json={
            "actions": actions
        }
    )
    response_json = response.json()
    if response_json.get('code') == 0:
        return True
    else:
        return False

