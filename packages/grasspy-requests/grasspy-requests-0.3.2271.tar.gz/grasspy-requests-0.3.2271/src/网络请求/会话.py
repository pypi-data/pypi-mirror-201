"""
This module provides a Session object to manage and persist settings across
requests (cookies, auth, proxies).
"""
从 requests.sessions 导入 SessionRedirectMixin, Session
从 汉化通用 导入 _反向注入, _关键词参数中转英
从 .请求参数 导入 _请求方法字典, _请求参数字典


类 〇会话重定向混入(SessionRedirectMixin):

    套路 获取重定向目标(分身, 响应):
        """Receives a Response. Returns a redirect URI or ``None``"""
        返回 分身.get_redirect_target(响应)

    套路 应去除认证(分身, 旧url, 新url):
        """Decide whether Authorization header should be removed when redirecting"""
        返回 分身.should_strip_auth(旧url, 新url)

    套路 解决重定向(分身, 响应, 请求, 流=假, 超时=空, 验证=真, 证书=空,
                   代理々=空, 生成请求=假, **适配器关键词参数々):
        """Receives a Response. Returns a generator of Responses or Requests."""
        返回 分身.resolve_redirects(响应, 请求, stream=流, timeout=超时,
                verify=验证, cert=证书, proxies=代理々, yield_requests=生成请求,
                **适配器关键词参数々)

    套路 重建认证(分身, 就绪请求, 响应):
        """When being redirected we may want to strip authentication from the
        request to avoid leaking credentials. This method intelligently removes
        and reapplies authentication where possible to avoid credential loss.
        """
        分身.rebuild_auth(就绪请求, 响应)

    套路 重建代理々(分身, 就绪请求, 代理々) -> dict:
        """This method re-evaluates the proxy configuration by considering the
        environment variables. If we are redirected to a URL covered by
        NO_PROXY, we strip the proxy configuration. Otherwise, we set missing
        proxy keys for this URL (in case they were stripped by a previous
        redirect).

        This method also replaces the Proxy-Authorization header where
        necessary.
        """
        返回 分身.rebuild_proxies(就绪请求, 代理々)

    套路 重建方法(分身, 就绪请求, 响应):
        """When being redirected we may want to change the method of the request
        based on certain specs or browser behavior.
        """
        分身.rebuild_method(就绪请求, 响应)

_反向注入(〇会话重定向混入, SessionRedirectMixin)


类 〇会话(Session):
    """A Requests session.

    Provides cookie persistence, connection-pooling, and configuration.

    Basic Usage::

      >>> import requests
      >>> s = requests.Session()
      >>> s.get('https://httpbin.org/get')
      <Response [200]>

    Or as a context manager::

      >>> with requests.Session() as s:
      ...     s.get('https://httpbin.org/get')
      <Response [200]>
    """

    套路 准备请求(分身, 请求):
        """Constructs a :class:`PreparedRequest <PreparedRequest>` for
        transmission and returns it. The :class:`PreparedRequest` has settings
        merged from the :class:`Request <Request>` instance and those of the
        :class:`Session`.

        :param request: :class:`Request` instance to prepare with this
            session's settings.
        :rtype: requests.PreparedRequest
        """
        返回 分身.prepare_request(请求)

    套路 请求(分身, 方法, url, 参数々=空, 数据=空, 头信息=空, 酷卡々=空, 
             文件々=空, 认证=空, 超时=空, 允许重定向=真, 代理々=空, 钩子々=空,
             流=空, 验证=空, 证书=空, json=空):
        """Constructs a :class:`Request <Request>`, prepares it and sends it.
        Returns :class:`Response <Response>` object.

        :param method: method for the new :class:`Request` object.
        :param url: URL for the new :class:`Request` object.
        :param params: (optional) Dictionary or bytes to be sent in the query
            string for the :class:`Request`.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param json: (optional) json to send in the body of the
            :class:`Request`.
        :param headers: (optional) Dictionary of HTTP Headers to send with the
            :class:`Request`.
        :param cookies: (optional) Dict or CookieJar object to send with the
            :class:`Request`.
        :param files: (optional) Dictionary of ``'filename': file-like-objects``
            for multipart encoding upload.
        :param auth: (optional) Auth tuple or callable to enable
            Basic/Digest/Custom HTTP Auth.
        :param timeout: (optional) How long to wait for the server to send
            data before giving up, as a float, or a :ref:`(connect timeout,
            read timeout) <timeouts>` tuple.
        :type timeout: float or tuple
        :param allow_redirects: (optional) Set to True by default.
        :type allow_redirects: bool
        :param proxies: (optional) Dictionary mapping protocol or protocol and
            hostname to the URL of the proxy.
        :param stream: (optional) whether to immediately download the response
            content. Defaults to ``False``.
        :param verify: (optional) Either a boolean, in which case it controls whether we verify
            the server's TLS certificate, or a string, in which case it must be a path
            to a CA bundle to use. Defaults to ``True``. When set to
            ``False``, requests will accept any TLS certificate presented by
            the server, and will ignore hostname mismatches and/or expired
            certificates, which will make your application vulnerable to
            man-in-the-middle (MitM) attacks. Setting verify to ``False`` 
            may be useful during local development or testing.
        :param cert: (optional) if String, path to ssl client cert file (.pem).
            If Tuple, ('cert', 'key') pair.
        :rtype: requests.Response
        """
        方法 = _请求方法字典.获取(方法, 方法)
        返回 分身.request(方法, url, params=参数々, data=数据, headers=头信息, cookies=酷卡々,
                         files=文件々, auth=认证, timeout=超时, allow_redirects=允许重定向,
                         proxies=代理々, hooks=钩子々, stream=流, verify=验证, cert=证书, json=json)

    def 查_get(self, url, **关键词参数々):
        r"""Sends a GET request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param \*\*关键词参数々: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """

        关键词参数々 = _关键词参数中转英(关键词参数々, _请求参数字典)
        关键词参数々.setdefault('allow_redirects', True)
        return self.request('GET', url, **关键词参数々)

    def 权_options(self, url, **关键词参数々):
        r"""Sends a OPTIONS request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param \*\*关键词参数々: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """

        关键词参数々 = _关键词参数中转英(关键词参数々, _请求参数字典)
        关键词参数々.setdefault('allow_redirects', True)
        return self.request('OPTIONS', url, **关键词参数々)

    def 头_head(self, url, **关键词参数々):
        r"""Sends a HEAD request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param \*\*关键词参数々: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """

        关键词参数々 = _关键词参数中转英(关键词参数々, _请求参数字典)
        关键词参数々.setdefault('allow_redirects', False)
        return self.request('HEAD', url, **关键词参数々)

    def 增_post(self, url, 数据=None, json=None, **关键词参数々):
        r"""Sends a POST request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param json: (optional) json to send in the body of the :class:`Request`.
        :param \*\*关键词参数々: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """

        关键词参数々 = _关键词参数中转英(关键词参数々, _请求参数字典)
        return self.request('POST', url, data=数据, json=json, **关键词参数々)

    def 改_put(self, url, 数据=None, **关键词参数々):
        r"""Sends a PUT request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param \*\*关键词参数々: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """

        关键词参数々 = _关键词参数中转英(关键词参数々, _请求参数字典)
        return self.request('PUT', url, data=数据, **关键词参数々)

    def 补_patch(self, url, 数据=None, **关键词参数々):
        r"""Sends a PATCH request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param \*\*关键词参数々: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """

        关键词参数々 = _关键词参数中转英(关键词参数々, _请求参数字典)
        return self.request('PATCH', url, data=数据, **关键词参数々)

    def 删_delete(self, url, **关键词参数々):
        r"""Sends a DELETE request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param \*\*关键词参数々: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """

        关键词参数々 = _关键词参数中转英(关键词参数々, _请求参数字典)
        return self.request('DELETE', url, **关键词参数々)

    套路 发送(分身, 请求, **关键词参数々):
        """Send a given PreparedRequest.

        :rtype: requests.Response
        """
        关键词参数々 = _关键词参数中转英(关键词参数々, _请求参数字典)
        返回 分身.send(请求, **关键词参数々)

    套路 合并环境设置(分身, url, 代理々, 流, 验证, 证书):
        """
        Check the environment and merge it with some settings.

        :rtype: dict
        """
        返回 分身.merge_environment_settings(url, 代理々, 流, 验证, 证书)

    套路 获取适配器(分身, url):
        """
        Returns the appropriate connection adapter for the given URL.

        :rtype: requests.adapters.BaseAdapter
        """
        返回 分身.get_adapter(url)

    套路 关闭(分身):
        """Closes all adapters and as such the session"""
        分身.close()

    套路 挂载(分身, 前缀, 适配器):
        """Registers a connection adapter to a prefix.

        Adapters are sorted in descending order by prefix length.
        """
        分身.mount(前缀, 适配器)

    @property
    套路 头信息(分身):
        返回 分身.headers
    
    @property
    套路 酷卡々(分身):
        返回 分身.cookies
    
    @property
    套路 认证(分身):
        返回 分身.cert
    
    @认证.赋值器
    套路 认证(分身, 值):
        分身.cert = 值
    
    @property
    套路 代理々(分身):
        返回 分身.proxies
    
    @property
    套路 钩子々(分身):
        返回 分身.hooks
    
    @property
    套路 参数々(分身):
        返回 分身.params
    
    @property
    套路 验证(分身):
        返回 分身.verify
    
    @property
    套路 证书(分身):
        返回 分身.cert
    
    @property
    套路 适配器々(分身):
        返回 分身.adapters
    
    @property
    套路 流(分身):
        返回 分身.stream
    
    @property
    套路 信任环境(分身):
        返回 分身.trust_env
    
    @property
    套路 最大重定向次数(分身):
        返回 分身.max_redirects

_反向注入(〇会话, Session)