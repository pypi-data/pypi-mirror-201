"""
本模块包含驱动网络请求的主要对象.
"""

从 requests.models 导入 RequestEncodingMixin, RequestHooksMixin
从 requests.models 导入 Request, PreparedRequest, Response
从 汉化通用 导入 _反向注入
从 .请求参数 导入 _请求方法字典

类 〇请求编码混入(RequestEncodingMixin):
    @property
    套路 路径url(分身):
        """Build the path URL to use."""
        返回 分身.path_url

_反向注入(〇请求编码混入, RequestEncodingMixin)


类 〇请求钩子混入(RequestHooksMixin):
    套路 注册钩子(分身, 事件, 钩子):
        """Properly register a hook."""
        分身.deregister_hook(事件, 钩子)

    套路 取消注册钩子(分身, 事件, 钩子):
        """Deregister a previously registered hook.
        Returns True if the hook existed, False if not.
        """
        返回 分身.deregister_hook(事件, 钩子)

_反向注入(〇请求钩子混入, RequestHooksMixin)


类 〇请求(Request):
    """A user-created :class:`Request <Request>` object.

    Used to prepare a :class:`PreparedRequest <PreparedRequest>`, which is sent to the server.

    :param method: HTTP method to use.
    :param url: URL to send.
    :param headers: dictionary of headers to send.
    :param files: dictionary of {filename: fileobject} files to multipart upload.
    :param data: the body to attach to the request. If a dictionary or
        list of tuples ``[(key, value)]`` is provided, form-encoding will
        take place.
    :param json: json for the body to attach to the request (if files or data is not specified).
    :param params: URL parameters to append to the URL. If a dictionary or
        list of tuples ``[(key, value)]`` is provided, form-encoding will
        take place.
    :param auth: Auth handler or (user, pass) tuple.
    :param cookies: dictionary or CookieJar of cookies to attach to this request.
    :param hooks: dictionary of callback hooks, for internal usage.

    Usage::

      >>> import requests
      >>> req = requests.Request('GET', 'https://httpbin.org/get')
      >>> req.prepare()
      <PreparedRequest [GET]>
    """

    套路 __init__(分身, 方法=空, url=空, 头信息=空, 文件々=空, 数据=空,
                  参数々=空, 认证=空, 酷卡々=空, 钩子々=空, json=空):
        方法 = _请求方法字典.获取(方法, 方法)
        super().__init__(method=方法, url=url, headers=头信息, files=文件々,
                         data=数据, params=参数々, auth=认证, cookies=酷卡々,
                         hooks=钩子々, json=json)

    def __repr__(self):
        return '<请求 [%s]>' % (self.method)

    套路 准备(分身):
        """构造一个 '就绪请求' 对象以供发送并返回该对象."""
        返回 分身.prepare()

    @property
    套路 方法(分身):
        返回 分身.method
    
    @property
    套路 头信息(分身):
        返回 分身.headers
    
    @property
    套路 文件々(分身):
        返回 分身.files
    
    @property
    套路 数据(分身):
        返回 分身.data
    
    @property
    套路 参数々(分身):
        返回 分身.params
    
    @property
    套路 认证(分身):
        返回 分身.auth
    
    @property
    套路 酷卡々(分身):
        返回 分身.cookies

_反向注入(〇请求, Request)


类 〇就绪请求(PreparedRequest):
    """The fully mutable :class:`PreparedRequest <PreparedRequest>` object,
    containing the exact bytes that will be sent to the server.

    Instances are generated from a :class:`Request <Request>` object, and
    should not be instantiated manually; doing so may produce undesirable
    effects.

    Usage::

      >>> import requests
      >>> req = requests.Request('GET', 'https://httpbin.org/get')
      >>> r = req.prepare()
      >>> r
      <PreparedRequest [GET]>

      >>> s = requests.Session()
      >>> s.send(r)
      <Response [200]>
    """
    套路 准备(分身, 方法=空, url=空, 头信息=空, 文件々=空, 数据=空,
                  参数々=空, 认证=空, 酷卡々=空, 钩子々=空, json=空):
        方法 = _请求方法字典.获取(方法, 方法)
        """Prepares the entire request with the given parameters."""
        分身.prepare(method=方法, url=url, headers=头信息, files=文件々,
                    data=数据, params=参数々, auth=认证, cookies=酷卡々,
                    hooks=钩子々, json=json)

    def __repr__(self):
        return '<就绪请求 [%s]>' % (self.method)

    套路 拷贝(分身):
        返回 分身.copy()

    套路 准备方法(分身, 方法):
        方法 = _请求方法字典.获取(方法, 方法)
        """Prepares the given HTTP method."""
        分身.prepare_method(方法)
    
    套路 准备url(分身, url, 参数々):
        """Prepares the given HTTP URL."""
        分身.prepare_url(url, 参数々)
    
    套路 准备头信息(分身, 头信息):
        """Prepares the given HTTP headers."""
        分身.prepare_headers(url, 头信息)
    
    套路 准备请求体(分身, 数据, 文件々, json=空):
        """Prepares the given HTTP body data."""
        分身.prepare_body(数据, 文件々, json=json)
    
    套路 准备内容长度(分身, 请求体):
        """Prepare Content-Length header based on request method and body"""
        分身.prepare_content_length(请求体)
    
    套路 准备认证(分身, 认证, url=''):
        """Prepares the given HTTP auth data."""
        分身.prepare_auth(认证, url=url)
    
    套路 准备酷卡々(分身, 酷卡々):
        """Prepares the given HTTP cookie data.

        This function eventually generates a ``Cookie`` header from the
        given cookies using cookielib. Due to cookielib's design, the header
        will not be regenerated if it already exists, meaning this function
        can only be called once for the life of the
        :class:`PreparedRequest <PreparedRequest>` object. Any subsequent calls
        to ``prepare_cookies`` will have no actual effect, unless the "Cookie"
        header is removed beforehand.
        """
        分身.prepare_cookies(酷卡々)
    
    套路 准备钩子々(分身, 钩子々):
        """Prepares the given hooks."""
        分身.prepare_hooks(钩子々)

    @property
    套路 方法(分身):
        返回 分身.method
    
    @property
    套路 头信息(分身):
        返回 分身.headers
    
    @property
    套路 请求体(分身):
        返回 分身.body
    
    @请求体.赋值器
    套路 请求体(分身, 值):
        分身.body = 值
    
    @property
    套路 钩子々(分身):
        返回 分身.hooks

_反向注入(〇就绪请求, PreparedRequest)


类 〇响应(Response):
    """响应对象, 包含服务器对 HTTP 请求的响应.
    """
    @property
    套路 正常(分身):
        """Returns True if :attr:`status_code` is less than 400, False if not.

        This attribute checks if the status code of the response is between
        400 and 600 to see if there was a client error or a server error. If
        the status code is between 200 and 400, this will return True. This
        is **not** a check to see if the response code is ``200 OK``.
        """
        返回 分身.ok

    @property
    套路 是重定向(分身):
        """True if this Response is a well-formed HTTP redirect that could have
        been processed automatically (by :meth:`Session.resolve_redirects`).
        """
        返回 分身.is_redirect
    
    @property
    套路 是永久重定向(分身):
        """True if this Response one of the permanent versions of redirect."""
        返回 分身.is_permanent_redirect
    
    @property
    套路 下一个(分身):
        """Returns a PreparedRequest for the next request in a redirect chain, if there is one."""
        返回 分身.next
    
    @property
    套路 表观编码方式(分身):
        """The apparent encoding, provided by the charset_normalizer or chardet libraries."""
        返回 分身.apparent_encoding

    套路 迭代内容(分身, 块大小=1, 解码_统一码=假):
        """Iterates over the response data.  When stream=True is set on the
        request, this avoids reading the content at once into memory for
        large responses.  The chunk size is the number of bytes it should
        read into memory.  This is not necessarily the length of each item
        returned as decoding can take place.

        chunk_size must be of type int or None. A value of None will
        function differently depending on the value of `stream`.
        stream=True will read data as it arrives in whatever size the
        chunks are received. If stream=False, data is returned as
        a single chunk.

        If decode_unicode is True, content will be decoded using the best
        available encoding based on the response.
        """
        返回 分身.iter_content(chunk_size=块大小, decode_unicode=解码_统一码)
    
    套路 迭代行々(分身, 块大小=512, 解码_统一码=假, 分隔符=空):
        """Iterates over the response data, one line at a time.  When
        stream=True is set on the request, this avoids reading the
        content at once into memory for large responses.

        .. note:: This method is not reentrant safe.
        """
        返回 分身.iter_lines(chunk_size=块大小, decode_unicode=解码_统一码, delimiter=分隔符)

    @property
    套路 内容(分身):
        """Content of the response, in bytes."""
        返回 分身.content
    
    @property
    套路 文本(分身):
        """Content of the response, in unicode.

        If Response.encoding is None, encoding will be guessed using
        ``charset_normalizer`` or ``chardet``.

        The encoding of the response content is determined based solely on HTTP
        headers, following RFC 2616 to the letter. If you can take advantage of
        non-HTTP knowledge to make a better guess at the encoding, you should
        set ``r.encoding`` appropriately before accessing this property.
        """
        返回 分身.text

    @property
    套路 链接々(分身):
        """Returns the parsed header links of the response, if any."""
        返回 分身.links

    套路 根据状态报错(分身):
        """Raises :class:`HTTPError`, if one occurred."""
        分身.raise_for_status()

    套路 关闭(分身):
        """Releases the connection back to the pool. Once this method has been
        called the underlying ``raw`` object must not be accessed again.

        *Note: Should not normally need to be called explicitly.*
        """
        分身.close()

    @property
    套路 状态码(分身):
        返回 分身.status_code
    
    @property
    套路 头信息(分身):
        返回 分身.headers
    
    @property
    套路 生肉(分身):
        返回 分身.raw
    
    @property
    套路 生肉(分身):
        返回 分身.raw
    
    @property
    套路 编码方式(分身):
        返回 分身.encoding
    
    @编码方式.赋值器
    套路 编码方式(分身, 值):
        分身.encoding = 值

    @property
    套路 历史(分身):
        返回 分身.history
    
    @property
    套路 原因(分身):
        返回 分身.reason
    
    @property
    套路 酷卡々(分身):
        返回 分身.cookies
    
    @property
    套路 经过时间(分身):
        返回 分身.elapsed
    
    @property
    套路 请求(分身):
        返回 分身.request
    
    @property
    套路 连接(分身):
        返回 分身.connection

_反向注入(〇响应, Response)