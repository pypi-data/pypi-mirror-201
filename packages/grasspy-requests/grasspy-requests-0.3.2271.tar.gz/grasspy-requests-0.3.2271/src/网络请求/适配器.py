"""
This module contains the transport adapters that Requests uses to define
and maintain connections.
"""
从 requests.adapters 导入 BaseAdapter, HTTPAdapter
从 汉化通用 导入 _反向注入

匚默认池阻塞 = 假
匚默认池大小 = 10
匚默认重试次数 = 0
匚默认池超时 = 空

类 HTTP适配器(HTTPAdapter):
    """The built-in HTTP Adapter for urllib3.

    Provides a general-case interface for Requests sessions to contact HTTP and
    HTTPS urls by implementing the Transport Adapter interface. This class will
    usually be created by the :class:`Session <Session>` class under the
    covers.

    :param pool_connections: The number of urllib3 connection pools to cache.
    :param pool_maxsize: The maximum number of connections to save in the pool.
    :param max_retries: The maximum number of retries each connection
        should attempt. Note, this applies only to failed DNS lookups, socket
        connections and connection timeouts, never to requests where data has
        made it to the server. By default, Requests does not retry failed
        connections. If you need granular control over the conditions under
        which we retry a request, import urllib3's ``Retry`` class and pass
        that instead.
    :param pool_block: Whether the connection pool should block for connections.

    Usage::

      >>> import requests
      >>> s = requests.Session()
      >>> a = requests.adapters.HTTPAdapter(max_retries=3)
      >>> s.mount('http://', a)
    """

    套路 __init__(分身, 池连接数=匚默认池大小, 池最大大小=匚默认池大小,
                  最大重试次数=匚默认重试次数, 池阻塞=匚默认池阻塞):
        super().__init__(pool_connections=池连接数, pool_maxsize=池最大大小,
                         max_retries=最大重试次数, pool_block=池阻塞)

    套路 初始化池管理器(分身, 连接数, 最大大小, 阻塞=匚默认池阻塞, **池关键词参数々):
        """Initializes a urllib3 PoolManager.

        This method should not be called from user code, and is only
        exposed for use when subclassing the
        :class:`HTTPAdapter <requests.adapters.HTTPAdapter>`.

        :param connections: The number of urllib3 connection pools to cache.
        :param maxsize: The maximum number of connections to save in the pool.
        :param block: Block when no free connections are available.
        :param pool_kwargs: Extra keyword arguments used to initialize the Pool Manager.
        """
        分身.init_poolmanager(连接数, 最大大小, block=阻塞, **池关键词参数々)

    套路 代理管理器_用于(分身, 代理, **代理关键词参数々):
        """Return urllib3 ProxyManager for the given proxy.

        This method should not be called from user code, and is only
        exposed for use when subclassing the
        :class:`HTTPAdapter <requests.adapters.HTTPAdapter>`.

        :param proxy: The proxy to return a urllib3 ProxyManager for.
        :param proxy_kwargs: Extra keyword arguments used to configure the Proxy Manager.
        :returns: ProxyManager
        :rtype: urllib3.ProxyManager
        """
        返回 分身.proxy_manager_for(代理, **代理关键词参数々)

    套路 证书验证(分身, 连接, url, 验证, 证书):
        """Verify a SSL certificate. This method should not be called from user
        code, and is only exposed for use when subclassing the
        :class:`HTTPAdapter <requests.adapters.HTTPAdapter>`.

        :param conn: The urllib3 connection object associated with the cert.
        :param url: The requested URL.
        :param verify: Either a boolean, in which case it controls whether we verify
            the server's TLS certificate, or a string, in which case it must be a path
            to a CA bundle to use
        :param cert: The SSL certificate to verify.
        """
        分身.cert_verify(连接, url, 验证, 证书)

    套路 构建响应(分身, 请求, 响应):
        """Builds a :class:`Response <requests.Response>` object from a urllib3
        response. This should not be called from user code, and is only exposed
        for use when subclassing the
        :class:`HTTPAdapter <requests.adapters.HTTPAdapter>`

        :param req: The :class:`PreparedRequest <PreparedRequest>` used to generate the response.
        :param resp: The urllib3 response object.
        :rtype: requests.Response
        """
        返回 分身.build_response(请求, 响应)

    套路 获取连接(分身, url, 代理々=空):
        """Returns a urllib3 connection for the given URL. This should not be
        called from user code, and is only exposed for use when subclassing the
        :class:`HTTPAdapter <requests.adapters.HTTPAdapter>`.

        :param url: The URL to connect to.
        :param proxies: (optional) A Requests-style dictionary of proxies used on this request.
        :rtype: urllib3.ConnectionPool
        """
        分身.get_connection(url, proxies=代理々)

    套路 关闭(分身):
        """Disposes of any internal state.

        Currently, this closes the PoolManager and any active ProxyManager,
        which closes any pooled connections.
        """
        分身.close()

    套路 请求url(分身, 请求, 代理々):
        """Obtain the url to use when making the final request.

        If the message is being sent through a HTTP proxy, the full URL has to
        be used. Otherwise, we should only use the path portion of the URL.

        This should not be called from user code, and is only exposed for use
        when subclassing the
        :class:`HTTPAdapter <requests.adapters.HTTPAdapter>`.

        :param request: The :class:`PreparedRequest <PreparedRequest>` being sent.
        :param proxies: A dictionary of schemes or schemes and hosts to proxy URLs.
        :rtype: str
        """
        返回 分身.request_url(请求, 代理々)

    套路 添加头信息(分身, 请求, **关键词参数々):
        """Add any headers needed by the connection. As of v2.0 this does
        nothing by default, but is left for overriding by users that subclass
        the :class:`HTTPAdapter <requests.adapters.HTTPAdapter>`.

        This should not be called from user code, and is only exposed for use
        when subclassing the
        :class:`HTTPAdapter <requests.adapters.HTTPAdapter>`.

        :param request: The :class:`PreparedRequest <PreparedRequest>` to add headers to.
        :param kwargs: The keyword arguments from the call to send().
        """
        无操作
    
    def add_headers(self, request, **kwargs):
        self.添加头信息(request, **kwargs)

    套路 代理头信息(分身, 代理):
        """Returns a dictionary of the headers to add to any request sent
        through a proxy. This works with urllib3 magic to ensure that they are
        correctly sent to the proxy, rather than in a tunnelled request if
        CONNECT is being used.

        This should not be called from user code, and is only exposed for use
        when subclassing the
        :class:`HTTPAdapter <requests.adapters.HTTPAdapter>`.

        :param proxy: The url of the proxy being used for this request.
        :rtype: dict
        """
        返回 分身.proxy_headers(代理)

    套路 发送(分身, 请求, 流=假, 超时=空, 验证=真, 证书=空, 代理々=空):
        """Sends PreparedRequest object. Returns Response object.

        :param request: The :class:`PreparedRequest <PreparedRequest>` being sent.
        :param stream: (optional) Whether to stream the request content.
        :param timeout: (optional) How long to wait for the server to send
            data before giving up, as a float, or a :ref:`(connect timeout,
            read timeout) <timeouts>` tuple.
        :type timeout: float or tuple or urllib3 Timeout object
        :param verify: (optional) Either a boolean, in which case it controls whether
            we verify the server's TLS certificate, or a string, in which case it
            must be a path to a CA bundle to use
        :param cert: (optional) Any user-provided SSL certificate to be trusted.
        :param proxies: (optional) The proxies dictionary to apply to the request.
        :rtype: requests.Response
        """
        返回 分身.send(请求, stream=流, timeout=超时, verify=验证,
                      cert=证书, proxies=代理々)

    @property
    套路 最大重试次数(分身):
        返回 分身.max_retries
    
    @property
    套路 配置(分身):
        返回 分身.config

_反向注入(HTTP适配器, HTTPAdapter)