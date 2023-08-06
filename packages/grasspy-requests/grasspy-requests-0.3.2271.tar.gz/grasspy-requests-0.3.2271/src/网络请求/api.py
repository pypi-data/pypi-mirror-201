"""
本模块实现网络请求 API.
"""

导入 requests
从 .请求参数 导入 _请求方法字典, _请求参数字典
从 汉化通用 导入 _关键词参数中转英


套路 请求(方法, url, **关键词参数々):
    """构造并发送一个请求对象.

    :param method: method for the new :class:`Request` object: ``GET``, ``OPTIONS``, ``HEAD``, ``POST``, ``PUT``, ``PATCH``, or ``DELETE``.
    :param url: URL for the new :class:`Request` object.
    :param params: (optional) Dictionary, list of tuples or bytes to send
        in the query string for the :class:`Request`.
    :param data: (optional) Dictionary, list of tuples, bytes, or file-like
        object to send in the body of the :class:`Request`.
    :param json: (optional) A JSON serializable Python object to send in the body of the :class:`Request`.
    :param headers: (optional) Dictionary of HTTP Headers to send with the :class:`Request`.
    :param cookies: (optional) Dict or CookieJar object to send with the :class:`Request`.
    :param files: (optional) Dictionary of ``'name': file-like-objects`` (or ``{'name': file-tuple}``) for multipart encoding upload.
        ``file-tuple`` can be a 2-tuple ``('filename', fileobj)``, 3-tuple ``('filename', fileobj, 'content_type')``
        or a 4-tuple ``('filename', fileobj, 'content_type', custom_headers)``, where ``'content-type'`` is a string
        defining the content type of the given file and ``custom_headers`` a dict-like object containing additional headers
        to add for the file.
    :param auth: (optional) Auth tuple to enable Basic/Digest/Custom HTTP Auth.
    :param timeout: (optional) How many seconds to wait for the server to send data
        before giving up, as a float, or a :ref:`(connect timeout, read
        timeout) <timeouts>` tuple.
    :type timeout: float or tuple
    :param allow_redirects: (optional) Boolean. Enable/disable GET/OPTIONS/POST/PUT/PATCH/DELETE/HEAD redirection. Defaults to ``True``.
    :type allow_redirects: bool
    :param proxies: (optional) Dictionary mapping protocol to the URL of the proxy.
    :param verify: (optional) Either a boolean, in which case it controls whether we verify
            the server's TLS certificate, or a string, in which case it must be a path
            to a CA bundle to use. Defaults to ``True``.
    :param stream: (optional) if ``False``, the response content will be immediately downloaded.
    :param cert: (optional) if String, path to ssl client cert file (.pem). If Tuple, ('cert', 'key') pair.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response

    用法:

      >>> 导入 网络请求 
      >>> 响应 = 网络请求.请求('GET', 'https://www.grasspy.cn')
      >>> 响应
      <响应 [200]>
    """

    方法 = _请求方法字典.获取(方法, 方法)
    关键词参数々 = _关键词参数中转英(关键词参数々, _请求参数字典)
    返回 requests.request(方法, url, **关键词参数々)


套路 查_get(url, 参数々=空, **关键词参数々):
    r"""发送一个 '查' (GET, 查询、查看或获取内容) 请求.

    :param url: URL for the new :class:`Request` object.
    :param params: (optional) Dictionary, list of tuples or bytes to send
        in the query string for the :class:`Request`.
    :param \*\*kwargs: Optional arguments that ``request`` takes.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """

    关键词参数々 = _关键词参数中转英(关键词参数々, _请求参数字典)
    返回 requests.request('get', url, params=参数々, **关键词参数々)


套路 权_options(url, **关键词参数々):
    r"""发送一个 '权' (OPTIONS, 权限相关) 请求.

    :param url: URL for the new :class:`Request` object.
    :param \*\*kwargs: Optional arguments that ``request`` takes.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """

    关键词参数々 = _关键词参数中转英(关键词参数々, _请求参数字典)
    返回 requests.request('options', url, **关键词参数々)


套路 头_head(url, **关键词参数々):
    r"""发送一个 '头' (HEAD) 请求.

    :param url: URL for the new :class:`Request` object.
    :param \*\*kwargs: Optional arguments that ``request`` takes. If
        `allow_redirects` is not provided, it will be set to `False` (as
        opposed to the default :meth:`request` behavior).
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """

    关键词参数々 = _关键词参数中转英(关键词参数々, _请求参数字典)
    关键词参数々.设默认值('allow_redirects', False)
    返回 requests.request('head', url, **关键词参数々)


套路 增_post(url, 数据=None, json=None, **关键词参数々):
    r"""发送一个 '增' (POST, 增加或提交内容) 请求.

    :param url: URL for the new :class:`Request` object.
    :param data: (optional) Dictionary, list of tuples, bytes, or file-like
        object to send in the body of the :class:`Request`.
    :param json: (optional) json data to send in the body of the :class:`Request`.
    :param \*\*kwargs: Optional arguments that ``request`` takes.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """

    关键词参数々 = _关键词参数中转英(关键词参数々, _请求参数字典)
    return requests.request('post', url, data=数据, json=json, **关键词参数々)


套路 改_put(url, 数据=空, **关键词参数々):
    r"""发送一个 '改' (PUT, 全局修改或更新) 请求.

    :param url: URL for the new :class:`Request` object.
    :param data: (optional) Dictionary, list of tuples, bytes, or file-like
        object to send in the body of the :class:`Request`.
    :param json: (optional) json data to send in the body of the :class:`Request`.
    :param \*\*kwargs: Optional arguments that ``request`` takes.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    
    关键词参数々 = _关键词参数中转英(关键词参数々, _请求参数字典)
    返回 requests.request('put', url, data=数据, **关键词参数々)


套路 补_patch(url, 数据=空, **关键词参数々):
    r"""发送一个 '补' (PATCH, 局部修改或更新) 请求.

    :param url: URL for the new :class:`Request` object.
    :param data: (optional) Dictionary, list of tuples, bytes, or file-like
        object to send in the body of the :class:`Request`.
    :param json: (optional) json data to send in the body of the :class:`Request`.
    :param \*\*kwargs: Optional arguments that ``request`` takes.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """

    关键词参数々 = _关键词参数中转英(关键词参数々, _请求参数字典)
    返回 requests.request('patch', url, data=数据, **关键词参数々)


套路 删_delete(url, **关键词参数々):
    r"""发送一个 '删' (DELETE, 删除) 请求.

    :param url: URL for the new :class:`Request` object.
    :param \*\*kwargs: Optional arguments that ``request`` takes.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """

    关键词参数々 = _关键词参数中转英(关键词参数々, _请求参数字典)
    返回 requests.request('delete', url, **关键词参数々)
