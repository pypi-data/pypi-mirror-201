"""
    结果分析计算验证服务
"""
from ats_base.base import req, entrance
from ats_base.common import func
from ats_base.config.configure import CONFIG

udm = entrance.api(CONFIG.get(func.SERVICE, 'udm'))


def acv(module: str, function: str, data, url: str = None):
    """
    数据验证
    :param module:
    :param function:
    :param data:
    :param url:
    :return:
    """
    s_url = _get_service_url(url)
    result = req.post('{}/{}/{}'.format('{}/{}'.format(s_url, 'acv'), module, function), jsons=data)

    if result['code'] == 500:
        raise Exception(result['message'])

    return result['data']


def built_in(module: str, function: str, data, url: str = None):
    """
    内置函数
    :param module:
    :param function:
    :param data:
    :param url:
    :return:
    """
    s_url = _get_service_url(url)
    result = req.post('{}/{}/{}'.format('{}/{}'.format(s_url, 'built_in'), module, function), jsons=data)

    if result['code'] == 500:
        raise Exception(result['message'])

    return result['data']


def _get_service_url(url: str = None):
    if url is not None and func.is_valid_url(url):
        return url

    return udm
