## flask

```
app.py中rule的添加流程
blueprints.py中rule的添加流程
views.py中视图请求的过程
ｗerkzeug/routing  serving  ***
		/routing  rule, map, mapadapter


blueprints.py:

    def route(self, rule, **options):
        """Like :meth:`Flask.route` but for a blueprint.  The endpoint for the
        :func:`url_for` function is prefixed with the name of the blueprint.
        """
        def decorator(f):
            endpoint = options.pop("endpoint", f.__name__)
            self.add_url_rule(rule, endpoint, f, **options)
            return f
        return decorator

    def add_url_rule(self, rule, endpoint=None, view_func=None, **options):
        """Like :meth:`Flask.add_url_rule` but for a blueprint.  The endpoint for
        the :func:`url_for` function is prefixed with the name of the blueprint.
        """
        if endpoint:
            assert '.' not in endpoint, "Blueprint endpoint's should not contain dot's"
        self.record(lambda s:s.add_url_rule(rule, endpoint, view_func, **options))
       
     
     def record(self, func):
        """Registers a function that is called when the blueprint is
        registered on the application.  This function is called with the
        state as argument as returned by the :meth:`make_setup_state`
        method.
        """
        if self._got_registered_once and self.warn_on_modifications:
            from warnings import warn
            warn(Warning('The blueprint was already rtegistered once '
                         'but is getting modified now.  These changes '
                         'will not show up.'))
        self.deferred_functions.append(func)
        
      
      def register(self, app, options, first_registration=False):
        """Called by :meth:`Flask.register_blueprint` to register a blueprint
        on the application.  This can be overridden to customize the register
        behavior.  Keyword arguments from
        :func:`~flask.Flask.register_blueprint` are directly forwarded to this
        method in the `options` dictionary.
        """
        
        self._got_registered_once = True
        state = self.make_setup_state(app, options, first_registration)
        # 静态文件的添加
        if self.has_static_folder:
            state.add_url_rule(self.static_url_path + '/<path:filename>',
                               view_func=self.send_static_file,
                               endpoint='static')

        for deferred in self.deferred_functions:
            deferred(state)
            
 app.py 
 	def register_blueprint(self, blueprint, **options):
        """Registers a blueprint on the application.

        .. versionadded:: 0.7
        """
        first_registration = False
        if blueprint.name in self.blueprints:
            assert self.blueprints[blueprint.name] is blueprint, \
                'A blueprint\'s name collision occurred between %r and ' \
                '%r.  Both share the same name "%s".  Blueprints that ' \
                'are created on the fly need unique names.' % \
                (blueprint, self.blueprints[blueprint.name], blueprint.name)
        else:
            self.blueprints[blueprint.name] = blueprint
            first_registration = True
            
        # 调用上面蓝图中的register
        blueprint.register(self, options, first_registration)
        
     
        
     def add_url_rule(self, rule, endpoint=None, view_func=None, **options):
	    # 重点
        self.url_map.add(rule)
        
        if view_func is not None:
            old_func = self.view_functions.get(endpoint)
            if old_func is not None and old_func != view_func:
                raise AssertionError('View function mapping is overwriting an '
                                     'existing endpoint function: %s' % endpoint)
            self.view_functions[endpoint] = view_func


werkzeug/routing.py 
	mapadapter  dispatch ---> match 
	map         add 
	rule        match      baseconverter


Q:
  views.py下的 as_view下面的dispatch怎么执行？？？
  
  views.py   as_view/view/dispatch_request --- app.py/ wsgi_app---full_dispatch_request--- dispatch_request
  
  views.py 
        def dispatch_request(self):
            """Subclasses have to override this method to implement the
            actual view function code.  This method is called with all
            the arguments from the URL rule.
            """
            raise NotImplementedError()

        @classmethod
        def as_view(cls, name, *class_args, **class_kwargs):
            """Converts the class into an actual view function that can be used
            with the routing system.  Internally this generates a function on the
            fly which will instantiate the :class:`View` on each request and call
            the :meth:`dispatch_request` method on it.

            The arguments passed to :meth:`as_view` are forwarded to the
            constructor of the class.
            """
            def view(*args, **kwargs):
                self = view.view_class(*class_args, **class_kwargs)
                # 执行dispatch_request
                return self.dispatch_request(*args, **kwargs)

            if cls.decorators:
                view.__name__ = name
                view.__module__ = cls.__module__
                for decorator in cls.decorators:
                    view = decorator(view)

            # we attach the view class to the view function for two reasons:
            # first of all it allows us to easily figure out what class-based
            # view this thing came from, secondly it's also used for instantiating
            # the view class so you can actually replace it with something else
            # for testing purposes and debugging.
            view.view_class = cls
            view.__name__ = name
            view.__doc__ = cls.__doc__
            view.__module__ = cls.__module__
            view.methods = cls.methods
            return view
    
   
   app.py 
        def wsgi_app(self, environ, start_response):
            ctx = self.request_context(environ)
            ctx.push()
            error = None
            try:
                try:
                	# ***************************************
                    response = self.full_dispatch_request()
                    
                except Exception as e:
                    error = e
                    response = self.make_response(self.handle_exception(e))
                return response(environ, start_response)
            finally:
                if self.should_ignore_error(error):
                    error = None
            	ctx.auto_pop(error)
            	
     def full_dispatch_request(self):
        """Dispatches the request and on top of that performs request
        pre and postprocessing as well as HTTP exception catching and
        error handling.

        .. versionadded:: 0.7
        """
        self.try_trigger_before_first_request_functions()
        try:
            request_started.send(self)
            rv = self.preprocess_request()
            if rv is None:
                rv = self.dispatch_request()
        except Exception as e:
            rv = self.handle_user_exception(e)
        response = self.make_response(rv)
        response = self.process_response(response)
        request_finished.send(self, response=response)
        return response
        
      def dispatch_request(self):
        req = _request_ctx_stack.top.request
        
        if req.routing_exception is not None:
            self.raise_routing_exception(req)
            
        rule = req.url_rule
        
        if getattr(rule, 'provide_automatic_options', False) \
           and req.method == 'OPTIONS':
            return self.make_default_options_response()
        
        return self.view_functions[rule.endpoint](**req.view_args)


others:
sessions.py(有serializer的身影）
	def open_session(self, app, request):
        s = self.get_signing_serializer(app)
        if s is None:
            return None
        val = request.cookies.get(app.session_cookie_name)
        if not val:
            return self.session_class()
        max_age = total_seconds(app.permanent_session_lifetime)
        try:
            data = s.loads(val, max_age=max_age)
            return self.session_class(data)
        except BadSignature:
            return self.session_class()

    def save_session(self, app, session, response):
        domain = self.get_cookie_domain(app)
        path = self.get_cookie_path(app)
        if not session:
            if session.modified:
                response.delete_cookie(app.session_cookie_name,
                                       domain=domain, path=path)
            return
        httponly = self.get_cookie_httponly(app)
        secure = self.get_cookie_secure(app)
        expires = self.get_expiration_time(app, session)
        val = self.get_signing_serializer(app).dumps(dict(session))
        response.set_cookie(app.session_cookie_name, val,
                            expires=expires, httponly=httponly,
                            domain=domain, path=path, secure=secure)
```





```
app.run 流程分析：
flask\app.py  ---> werkzeug\serving.py  ---> socketserver.py
```



```
flask如何处理多个请求而不冲突的
globals.py
	def _lookup_req_object(name):
        top = _request_ctx_stack.top
        if top is None:
            raise RuntimeError(_request_ctx_err_msg)
        return getattr(top, name)

    def _lookup_app_object(name):
        top = _app_ctx_stack.top
        if top is None:
            raise RuntimeError(_app_ctx_err_msg)
        return getattr(top, name)

    def _find_app():
        top = _app_ctx_stack.top
        if top is None:
            raise RuntimeError(_app_ctx_err_msg)
        return top.app

     _request_ctx_stack = LocalStack()
    _app_ctx_stack = LocalStack()
    current_app = LocalProxy(_find_app)
    request = LocalProxy(partial(_lookup_req_object, 'request'))
    session = LocalProxy(partial(_lookup_req_object, 'session'))
    g = LocalProxy(partial(_lookup_app_object, 'g'))


LocalStack() ---> local.py

        
class LocalStack(object):
    """This class works similar to a :class:`Local` but keeps a stack
    of objects instead.  This is best explained with an example::

        >>> ls = LocalStack()
        >>> ls.push(42)
        >>> ls.top
        42
        >>> ls.push(23)
        >>> ls.top
        23
        >>> ls.pop()
        23
        >>> ls.top
        42

    They can be force released by using a :class:`LocalManager` or with
    the :func:`release_local` function but the correct way is to pop the
    item from the stack after using.  When the stack is empty it will
    no longer be bound to the current context (and as such released).

    By calling the stack without arguments it returns a proxy that resolves to
    the topmost item on the stack.

    .. versionadded:: 0.6.1
    """

    def __init__(self):
        self._local = Local()
    
    def __call__(self):
        def _lookup():
            rv = self.top
            if rv is None:
            raise RuntimeError("object unbound")
            return rv
         # 重点， 指向了LocalProxy
		return LocalProxy(_lookup)   
		

class Local(object):
    __slots__ = ("__storage__", "__ident_func__")

    def __init__(self):
        object.__setattr__(self, "__storage__", {})
        # 重点, get_ident, 见下方get_ident, 在最初导包的地方
        object.__setattr__(self, "__ident_func__", get_ident)

    def __iter__(self):
        return iter(self.__storage__.items())

    def __call__(self, proxy):
        """Create a proxy for a name."""
        # 重点，调用的底层是 LocalProxy(self,  proxy)
        return LocalProxy(self, proxy)

    def __release_local__(self):
        self.__storage__.pop(self.__ident_func__(), None)
        

try:
    from greenlet import getcurrent as get_ident
except ImportError:
    try:
        from thread import get_ident
    except ImportError:
        from _thread import get_ident
        


下面重点研究下localProxy

@implements_bool
class LocalProxy(object):
    """Acts as a proxy for a werkzeug local.  Forwards all operations to
    a proxied object.  The only operations not supported for forwarding
    are right handed operands and any kind of assignment.

    Example usage::

        from werkzeug.local import Local
        l = Local()

        # these are proxies
        request = l('request')
        user = l('user')


        from werkzeug.local import LocalStack
        _response_local = LocalStack()

        # this is a proxy
        response = _response_local()

    Whenever something is bound to l.user / l.request the proxy objects
    will forward all operations.  If no object is bound a :exc:`RuntimeError`
    will be raised.

    To create proxies to :class:`Local` or :class:`LocalStack` objects,
    call the object as shown above.  If you want to have a proxy to an
    object looked up by a function, you can (as of Werkzeug 0.6.1) pass
    a function to the :class:`LocalProxy` constructor::

        session = LocalProxy(lambda: get_current_request().session)

    .. versionchanged:: 0.6.1
       The class can be instantiated with a callable as well now.
    """
    
    
    pass
```



## django

```
https://blog.csdn.net/victor_monkey/article/details/82017795
https://blog.csdn.net/qq_33339479/category_6800733.html
https://www.jianshu.com/u/a75713ce1dcf


windows: django_source_analy
ubuntu16_new: day04

视图中打断点，看执行过程


# 入口
runserver.py/ inner_run()
		
	    try:
	    	# 参考下面的相关代码，返回的是WSGIHandler(), 实例化了wsgi服务端，执行了相关逻辑
            handler = self.get_handler(*args, **options)  
            
            run(self.addr, int(self.port), handler,
                ipv6=self.use_ipv6, threading=threading, server_cls=self.server_cls)
                
        except socket.error as e:
        	pass 
        	
1. 
runserver.py/get_handler()
	    def get_handler(self, *args, **options):
        	return get_internal_wsgi_application()
        	

basehttp.py/ get_internal_wsgi_application()
		   from django.conf import settings
            app_path = getattr(settings, 'WSGI_APPLICATION')
            if app_path is None:
                return get_wsgi_application()

django.core.wsgi.get_wsgi_application
	def get_wsgi_application():
        django.setup(set_prefix=False)
        return WSGIHandler()
        
2. 
2.1 django.core.servers.basehttp.run

	def run(addr, port, wsgi_handler, ipv6=False, threading=False, server_cls=WSGIServer):
		# 参数中的wsgi_handler 是上面的WSGIHandler()
        server_address = (addr, port)
        if threading:
        	#1. 使用type动态(反射)创建 WSGIServer
            httpd_cls = type(str('WSGIServer'), (socketserver.ThreadingMixIn, server_cls), {})
            
        else:
            httpd_cls = server_cls
        
        #2. 实例化WSGIServer
        # 实例化过程：basehttp.py/WSGIServer---simple_server.WSGIServer---httpserver---TCPServer---baseserver
        
        httpd = httpd_cls(server_address, WSGIRequestHandler, ipv6=ipv6)
        
        if threading:
            httpd.daemon_threads = True
            
        #3.设置wsgiserver的处理函数  wsgi_handler
        httpd.set_app(wsgi_handler)
        #4.运行
        httpd.serve_forever()
        
2.2 django.core.handlers.wsgi.WSGIHandler
	class WSGIHandler()(base.BaseHandler):
        request_class = WSGIRequest

        def __init__(self, *args, **kwargs):
            super(WSGIHandler, self).__init__(*args, **kwargs)
            # 1.初始化各种中间件，其中还会调用到self._get_response()
            self.load_middleware()
		
		# 调用方式 WSGIHandler()， 在上面run()中获取handler的时候调用
        def __call__(self, environ, start_response):
            set_script_prefix(get_script_name(environ))
            signals.request_started.send(sender=self.__class__, environ=environ)
            request = self.request_class(environ)
            	
            # 2. get_response 
            response = self.get_response(request)

            response._handler_class = self.__class__

            status = '%d %s' % (response.status_code, response.reason_phrase)
            response_headers = [(str(k), str(v)) for k, v in response.items()]
            for c in response.cookies.values():
                response_headers.append((str('Set-Cookie'), str(c.output(header=''))))
            
            # ************调用wsgi 服务端, 设置返回的头信息******************
            start_response(force_str(status), response_headers)
            
            if getattr(response, 'file_to_stream', None) is not None and environ.get('wsgi.file_wrapper'):
                response = environ['wsgi.file_wrapper'](response.file_to_stream)
                
            return response
            
2.3 django.core.handlers.base.BaseHandler / get_response, load_middleware, _get_response
	    def get_response(self, request):
	    
            set_urlconf(settings.ROOT_URLCONF)
            # 重点
            # self._middleware_chain = handler 
            # handler = convert_exception_to_response(self._get_response)
            
            response = self._middleware_chain(request)

            try:
                # Apply response middleware, regardless of the response
                for middleware_method in self._response_middleware:
                    response = middleware_method(request, response)
                    
            except Exception: 
            	//pass 

           
            return response
        
        
            
         def load_middleware(self):
            self._request_middleware = []
            self._view_middleware = []
            self._template_response_middleware = []
            self._response_middleware = []
            self._exception_middleware = []

            if settings.MIDDLEWARE is None:
                warnings.warn(
                    "Old-style middleware using settings.MIDDLEWARE_CLASSES is "
                    "deprecated. Update your middleware and use settings.MIDDLEWARE "
                    "instead.", RemovedInDjango20Warning
                )

                handler = convert_exception_to_response(self._legacy_get_response)

                for middleware_path in settings.MIDDLEWARE_CLASSES:
                    mw_class = import_string(middleware_path)
                    try:
                        mw_instance = mw_class()
                    except MiddlewareNotUsed as exc:
                        if settings.DEBUG:
                            if six.text_type(exc):
                                logger.debug('MiddlewareNotUsed(%r): %s', middleware_path, exc)
                            else:
                                logger.debug('MiddlewareNotUsed: %r', middleware_path)
                        continue

                    if hasattr(mw_instance, 'process_request'):
                        self._request_middleware.append(mw_instance.process_request)
                    if hasattr(mw_instance, 'process_view'):
                        self._view_middleware.append(mw_instance.process_view)
                    if hasattr(mw_instance, 'process_template_response'):
                        self._template_response_middleware.insert(0, mw_instance.process_template_response)
                    if hasattr(mw_instance, 'process_response'):
                        self._response_middleware.insert(0, mw_instance.process_response)
                    if hasattr(mw_instance, 'process_exception'):
                        self._exception_middleware.insert(0, mw_instance.process_exception)
            else:
            	# ****************调用self._get_response*********************
                handler = convert_exception_to_response(self._get_response)
                # **********************************************************
                
                for middleware_path in reversed(settings.MIDDLEWARE):
                    middleware = import_string(middleware_path)
                    try:
                        mw_instance = middleware(handler)
                    except MiddlewareNotUsed as exc:
                        if settings.DEBUG:
                            if six.text_type(exc):
                                logger.debug('MiddlewareNotUsed(%r): %s', middleware_path, exc)
                            else:
                                logger.debug('MiddlewareNotUsed: %r', middleware_path)
                        continue

                    if mw_instance is None:
                        raise ImproperlyConfigured(
                            'Middleware factory %s returned None.' % middleware_path
                        )

                    if hasattr(mw_instance, 'process_view'):
                        self._view_middleware.insert(0, mw_instance.process_view)
                    if hasattr(mw_instance, 'process_template_response'):
                        self._template_response_middleware.append(mw_instance.process_template_response)
                    if hasattr(mw_instance, 'process_exception'):
                        self._exception_middleware.append(mw_instance.process_exception)

                    handler = convert_exception_to_response(mw_instance)

            # We only assign to this when initialization is complete as it is used
            # as a flag for initialization being complete.
            self._middleware_chain = handler
        
	
	   def _get_response(self, request):
            response = None

            if hasattr(request, 'urlconf'):
                urlconf = request.urlconf
                set_urlconf(urlconf)
                resolver = get_resolver(urlconf)
            else:
                resolver = get_resolver()

            resolver_match = resolver.resolve(request.path_info)
            callback, callback_args, callback_kwargs = resolver_match
            request.resolver_match = resolver_match

            # Apply view middleware
            for middleware_method in self._view_middleware:
                response = middleware_method(request, callback, callback_args, callback_kwargs)
                if response:
                    break

            if response is None:
                wrapped_callback = self.make_view_atomic(callback)
                try:
                    response = wrapped_callback(request, *callback_args, **callback_kwargs)
                except Exception as e:
                    response = self.process_exception_by_middleware(e, request)

            # Complain if the view returned None (a common error).
            if response is None:
                if isinstance(callback, types.FunctionType):    # FBV
                    view_name = callback.__name__
                else:                                           # CBV
                    view_name = callback.__class__.__name__ + '.__call__'

                raise ValueError(
                    "The view %s.%s didn't return an HttpResponse object. It "
                    "returned None instead." % (callback.__module__, view_name)
                )

            # If the response supports deferred rendering, apply template
            # response middleware and then render the response
            elif hasattr(response, 'render') and callable(response.render):
                for middleware_method in self._template_response_middleware:
                    response = middleware_method(request, response)
                    # Complain if the template response middleware returned None (a common error).
                    if response is None:
                        raise ValueError(
                            "%s.process_template_response didn't return an "
                            "HttpResponse object. It returned None instead."
                            % (middleware_method.__self__.__class__.__name__)
                        )

                try:
                    response = response.render()
                except Exception as e:
                    response = self.process_exception_by_middleware(e, request)

            return response
	
	
2.4 django.urls.resolvers.RegexURLResolver#resolve
	 def resolve(self, path):
        path = force_text(path)  # path may be a reverse_lazy object
        tried = []
        match = self.regex.search(path)
        if match:
            new_path = path[match.end():]
            for pattern in self.url_patterns:
                try:
                    sub_match = pattern.resolve(new_path)
                except Resolver404 as e:
                    sub_tried = e.args[0].get('tried')
                    if sub_tried is not None:
                        tried.extend([pattern] + t for t in sub_tried)
                    else:
                        tried.append([pattern])
                else:
                    if sub_match:
                        sub_match_dict = dict(match.groupdict(), **self.default_kwargs)
                        sub_match_dict.update(sub_match.kwargs)

                        sub_match_args = sub_match.args
                        if not sub_match_dict:
                            sub_match_args = match.groups() + sub_match.args

                        return ResolverMatch(
                            sub_match.func,
                            sub_match_args,
                            sub_match_dict,
                            sub_match.url_name,
                            [self.app_name] + sub_match.app_names,
                            [self.namespace] + sub_match.namespaces,
                        )
                    tried.append([pattern])
            raise Resolver404({'tried': tried, 'path': new_path})
        raise Resolver404({'path': path})
        
 
2.5 例子
举一个resrful风格的例子

from django.conf.urls import url

urlpatterns = [
    url(r'^detial/', view.DetailView.as_view(), name='detail'),
]

class DetailView（Apiview）:
    return Response({"detail"："请求成功"})
    
    
****************************************************
下面主要就url()函数和as_view()函数进行分析

#url函数主要url匹配，处理函数和name传给RegexURLPattern类，并初始化，然后通过该类进行请求url的匹配工作
def url(regex, view, kwargs=None, name=None):                                             	  
    # url函数，其中regex是r'^detial/'， view就是view.DetailView.as_view()， name是‘detail’
    # 判断view是否是列表或者元组，这是显然不是
    if isinstance(view, (list, tuple)):                                                 
		// pass 
        urlconf_module, app_name, namespace = view
        return RegexURLResolver(regex, urlconf_module, kwargs, app_name=app_name, namespace=namespace)
    
    elif callable(view):、
    	# 判断view函数是否是可调用的
    	# 如果是，则初始化RegexURLPattern实例  
    	# django.urls.resolvers.RegexURLPattern
        return RegexURLPattern(regex, view, kwargs, name)                                 
    else:
        raise TypeError('view must be a callable or a list/tuple in the case of include().')
        

#下面重点分析一下as_view()方法，所有的处理函数继承自view函数，调用as_view()方法，然后调用内包函数view（），最后调用处理请求的dispath函数处理请求，获得返回值
# django.views.generic.base.View#as_view
class View(object):
	# 定义请求方法
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']   

    def __init__(self, **kwargs):
        for key, value in six.iteritems(kwargs):                                             		 
        	# 初始化，将输入参数变为类属性
            setattr(self, key, value)

    @classonlymethod
    def as_view(cls, **initkwargs):

        def view(request, *args, **kwargs):
            self = cls(**initkwargs)
            # 判断是否有‘get’没有‘head’，则head请求等同于get请求
            if hasattr(self, 'get') and not hasattr(self, 'head'):                       
                self.head = self.get
                
            # 将输入的参数转变为属性
            self.request = request                                                       
            self.args = args
            self.kwargs = kwargs
            # 调用处理函数
            return self.dispatch(request, *args, **kwargs)                               
        return view

    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() in self.http_method_names:                             
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed) 
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)                                        
```

