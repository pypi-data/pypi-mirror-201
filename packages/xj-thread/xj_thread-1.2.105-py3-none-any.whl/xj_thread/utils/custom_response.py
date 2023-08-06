# encoding: utf-8
"""
@project: djangoModel->tool
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 返回协议封装工具
@created_time: 2022/6/15 14:14
"""
import json

from django.http import JsonResponse
from rest_framework import status


# json 结果集返回
def parse_json(result):
    if not result is None:
        if type(result) is str:
            try:
                result = json.loads(result.replace("'", '"').replace('\\r', "").replace('\\n', "").replace('\\t', "").replace('\\t', ""))
            except Exception as e:
                return result
        if type(result) is list or type(result) is tuple:
            for index, value in enumerate(result):
                result[index] = parse_json(value)
        if type(result) is dict:
            for k, v in result.items():
                result[k] = parse_json(v)
    return result


# 数据返回规则
def util_response(data='', err=0, msg='ok', tip=0, http_status=status.HTTP_200_OK, is_need_parse_json=True):
    """
    http 返回协议封装
    :param data: 返回的数据体
    :param err: 错误码，一般以1000开始，逐一增加。登录错误为6000-6999。
    :param msg: 错误信息，一般为服务返回协议中的err
    :param tip: 提示信息，当err为0时候需要前端提示则使用该字段传递提示信息。
    :param http_status: 返回状态码
    :return: response对象
    """
    data = parse_json(data) if is_need_parse_json else data
    if http_status == status.HTTP_200_OK:
        return JsonResponse({'err': err, 'msg': msg, "tip": tip, 'data': data, })
    else:
        return JsonResponse({'err': http_status, 'msg': msg, "tip": tip}, status=http_status)
