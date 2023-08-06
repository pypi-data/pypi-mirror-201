"""
This module provides utility functions that are used within Requests
that are also useful for external consumption.
"""
导入 sys
导入 requests.utils 为 utils

if sys.platform == 'win32':
    套路 代理_旁路(主机):
        """Return True, if the host should be bypassed.

        Checks proxy settings gathered from the environment, if specified,
        or the registry.
        """
        返回 utils.proxy_bypass(主机)

套路 获取netrc认证(url, 报错=假):
    """Returns the Requests tuple auth for a given url from netrc."""
    返回 utils.get_netrc_auth(url, raise_errors=报错)

套路 猜文件名(对象):
    """Tries to guess the filename of the given object."""
    返回 utils.guess_filename(对象)

套路 提取压缩路径(路径):
    """Replace nonexistent paths that look like they refer to a member of a zip
    archive with the location of an extracted copy of the target, or else
    just return the provided path unchanged.
    """
    返回 utils.extract_zipped_paths(路径)

套路 原子式打开(文件名):
    """Write a file to the disk in an atomic fashion"""
    返回 utils.atomic_open(文件名)

套路 对象转有序字典(值):
    """Take an object and test to see if it can be represented as a
    dictionary. Unless it can not be represented as such, return an
    OrderedDict, e.g.,

    ::

        >>> from_key_val_list([('key', 'val')])
        OrderedDict([('key', 'val')])
        >>> from_key_val_list('string')
        Traceback (most recent call last):
        ...
        ValueError: cannot encode objects that are not 2-tuples
        >>> from_key_val_list({'key': 'val'})
        OrderedDict([('key', 'val')])

    :rtype: OrderedDict
    """
    返回 utils.from_key_val_list(值)

套路 对象转元组列表(值):
    """Take an object and test to see if it can be represented as a
    dictionary. If it can be, return a list of tuples, e.g.,

    ::

        >>> to_key_val_list([('key', 'val')])
        [('key', 'val')]
        >>> to_key_val_list({'key': 'val'})
        [('key', 'val')]
        >>> to_key_val_list('string')
        Traceback (most recent call last):
        ...
        ValueError: cannot encode objects that are not 2-tuples

    :rtype: list
    """
    返回 utils.to_key_val_list(值)

# ...

套路 酷卡包转为字典(酷卡包):
    """Returns a key/value dictionary from a CookieJar.

    :param cj: CookieJar object to extract cookies from.
    :rtype: dict
    """
    返回 utils.dict_from_cookiejar(酷卡包)

套路 添加字典到酷卡包(酷卡包, 酷卡字典):
    返回 utils.add_dict_to_cookiejar(酷卡包, 酷卡字典)

套路 从内容获取编码方式(内容):
    """Returns encodings from given content string.

    :param content: bytestring to extract encodings from.
    """
    返回 utils.get_encodings_from_content(内容)

套路 从头信息获取编码方式(头信息):
    """Returns encodings from given content string.

    :param content: bytestring to extract encodings from.
    """
    返回 utils.get_encoding_from_headers(头信息)

# ...

