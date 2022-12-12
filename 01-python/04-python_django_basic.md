## 1.简介

特点：

- 提供项目工程管理的自动化脚本工具

- 数据库ORM支持（对象关系映射 ， Object Relational Mapping）
- 模板
- 表单
- Admin管理站点
- 文件管理
- 认证权限
- session机制
- 缓存

mvt

文档：

​	https://www.djangoproject.com/

​	https://yiyibooks.cn/xx/Django_1.11.6/index.html

	https://yiyibooks.cn/xx/Django_1.11.6/contents.html(推荐)



## 2.基本使用



### 2.1基本环境

创建虚拟环境：

```
mkvirtualenv -p python3 test_django
```

安装django:

```
pip install django==1.11.1
```

其他指令：

```
workon 
deactivate

pip list 
pip freeze 
pip uninstall 
```



### 2.2创建工程

创建工程：

```
方式一：
django-admin startproject 工程名称

方式二：
python manage.py startproject xxx

```

运行：

```
python manage.py runserver
```



### 2.3创建子应用

创建子应用：

```
python manage.py startapp xxx
```

安装子应用：

```
 INSTALLED_APPS= ["users.apps.UsersConfig"]
```

创建视图：

```
方式一：
# views.py
from django.http import HttpResponse

def index(request):
    """
    index视图
    :param request: 包含了请求信息的请求对象
    :return: 响应对象
    """
    return HttpResponse("hello the world!")
    
# 在users/urls.py文件中定义路由信息。  
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^index/$', views.index),
]

# 在工程总路由demo/urls.py中添加子应用的路由数据
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    # django默认包含的
    url(r'^admin/', admin.site.urls), 
    # 添加
    url(r'^users/', include('users.urls')), 
]


方式二：
# views.py
class IndexView(View):
	def get(self, request):
         return HttpResponse("demo1 hello")

# 在users/urls.py文件中定义路由信息。  
from django.conf.urls import url
from . import views

# urlpatterns是被django自动识别的路由列表变量
urlpatterns = [
    url(r'^index/$', views.IndexView.as_view()),
]
```



### 2.4路由解析

```
# 路由自上而下解析
# 总路由
urlpatterns = [
    # django默认包含的
    url(r'^admin/', admin.site.urls),  

    # 添加
    url(r'^users/', include('users.urls', namespace="demo1")), 
]

# 子应用中的子路由
urlpatterns = [
    url(r'^index/$', views.index, name='index'),
]

# 路由反解析
def index(request):
	# return reverse("users::index")  # 报错 响应不能为字符串
	  return HttpResponseRedirect(reverse("demo1:index"))
	  
# 路径结尾斜线/   
通常以斜线/结尾，其好处是用户访问不以斜线/结尾的相同路径时，Django会把用户重定向到以斜线/结尾的路径上，而不会返回404不存在

虽然路由结尾带/能带来上述好处，但是却违背了HTTP中URL表示资源位置路径的设计理念。
是否结尾带/以所属公司定义风格为准
```





## 3.配置

BASE_DIR

```
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
```



本地语言和时间

```
初始化的工程默认语言和时区为英语和UTC标准时区
LANGUAGE_CODE = 'en-us'  # 语言
TIME_ZONE = 'UTC'        # 时区

将语言和时区修改为中国大陆信息
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
```



静态文件

```
STATICFILES_DIRS 存放查找静态文件的目录
STATIC_URL       访问静态文件的URL前缀

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

# 访问： 
我们向static_files目录中添加一个index.html文件，在浏览器中就可以使用127.0.0.1:8000/static/index.html来访问

或者我们在static_files目录中添加了一个子目录和文件goods/detail.html，在浏览器中就可以使用127.0.0.1:8000/static/goods/detail.html来访问


# 补充：
当DEBUG=False工作在生产模式时，Django不再对外提供静态文件，需要使用collectstatic命令来收集静态文件或者交由其他静态文件服务器来提供
```



## 4.请求

路径参数

```
# weather/([a-z]+)/(\d{4})/

# 未命名参数按定义顺序传递，如：
url(r'^weather/([a-z]+)/(\d{4})/$', views.weather),

def weather(request, city, year):
    print('city=%s' % city)
    print('year=%s' % year)
    return HttpResponse('OK')
    
# 命名参数按名字传递，如：
url(r'^weather/(?P<city>[a-z]+)/(?P<year>\d{4})/$', views.weather),

def weather(request, year, city):
    print('city=%s' % city)
    print('year=%s' % year)
    return HttpResponse('OK')
```



查询参数

```
# /qs/?a=1&b=2&a=3

def qs(request):
    a = request.GET.get('a')
    b = request.GET.get('b')
    alist = request.GET.getlist('a')
    print(a)  # 3
    print(b)  # 2
    print(alist)  # ['1', '3']
    return HttpResponse('OK')
    
 
# 补充：
1.HttpRequest对象的属性GET、POST都是QueryDict类型的对象
2.查询字符串不区分请求方式，即假使客户端进行POST方式的请求，依然可以通过request.GET获取请求中的查询字符串数据
```



请求体

```
# 单类型字符串，可以是JSON字符串，可以是XML字符串
# Django默认开启了CSRF防护，会对上述请求方式进行CSRF防护验证，在测试时可以关闭CSRF防护机制，方法为在settings.py文件中注释掉CSRF中间件， csrf只会对post, delete, put, patch有效，对get不存在影响

# 非表单
可以通过request.body属性获取最原始的请求体数据，自己按照请求体格式（JSON、XML等）进行解析。request.body返回bytes类型

def get_body_json(request):
    json_str = request.body
    json_str = json_str.decode()  	 # python3.6 无需执行此步
    req_data = json.loads(json_str)
    print(req_data['a'])
    print(req_data['b'])
    return HttpResponse('OK')

# 表单
def get_body(request):
    a = request.POST.get('a')
    b = request.POST.get('b')
    alist = request.POST.getlist('a')
    print(a)
    print(b)
    print(alist)
    return HttpResponse('OK')
```



请求头

```
# 可以通过request.META属性获取请求头headers中的数据，request.META为字典类型

# 常见的请求头如：
CONTENT_LENGTH – The length of the request body (as a string).
CONTENT_TYPE – The MIME type of the request body.
HTTP_ACCEPT – Acceptable content types for the response.
HTTP_ACCEPT_ENCODING – Acceptable encodings for the response.
HTTP_ACCEPT_LANGUAGE – Acceptable languages for the response.
HTTP_HOST – The HTTP Host header sent by the client.
HTTP_REFERER – The referring page, if any.
HTTP_USER_AGENT – The client’s user-agent string.
QUERY_STRING – The query string, as a single (unparsed) string.
REMOTE_ADDR – The IP address of the client.
REMOTE_HOST – The hostname of the client.
REMOTE_USER – The user authenticated by the Web server, if any.
REQUEST_METHOD – A string such as "GET" or "POST".
SERVER_NAME – The hostname of the server.
SERVER_PORT – The port of the server (as a string).


# 具体使用如:
def get_headers(request):
    print(request.META['CONTENT_TYPE'])
    return HttpResponse('OK')
```



其他

```
method
users
FILES
path 
encoding
```



## 5.响应

httpresponse

```
HttpResponse(content=响应体, content_type=响应体数据类型, status=状态码)
```

httpresponse子类

```
HttpResponseRedirect 301
HttpResponsePermanentRedirect 302
HttpResponseNotModified 304
HttpResponseBadRequest 400
HttpResponseNotFound 404
HttpResponseForbidden 403
HttpResponseNotAllowed 405
HttpResponseGone 410
HttpResponseServerError 500
```

JsonResponse

```
from django.http import JsonResponse

def demo_view(request):
    return JsonResponse({'city': 'beijing', 'subject': 'python'})
```

redirect

```
from django.shortcuts import redirect

def demo_view(request):
    return redirect('/index.html')
```





## 6.cookie&session

```
# cookie
httpresponse.set_cookie()
request.COOKIES.get("")

# session
存储方式：
# 默认，数据库
SESSION_ENGINE='django.contrib.sessions.backends.db'   

# 本地缓存
SESSION_ENGINE='django.contrib.sessions.backends.cache' 

# 优先从本机内存中存取，如果没有则从数据库中存取。
SESSION_ENGINE='django.contrib.sessions.backends.cached_db'

# redis
安装扩展
pip install django-redis

2）配置
在settings.py文件中做如下设置

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# session基本操作
request.session.flush()   # 删除整条数据
request.session.clear()	  # 在存储中删除值部分
request.session["xxx"]="yyy"
request.session.get("键"，“默认值”)
request.session.set_expiry("")  # 如果value为None，那么session有效期将采用系统默认值，默认为两周，可以通过在settings.py中设置SESSION_COOKIE_AGE来设置全局默认值。
```



## 7.类视图

视图

```
# views.py

class RegisterView(View):
    """类视图：处理注册"""
    def get(self, request):
        """处理GET请求，返回注册页面"""
        return render(request, 'register.html')

    def post(self, request):
        """处理POST请求，实现注册逻辑"""
        return HttpResponse('这里实现注册逻辑')
          
# urlpatterns = [
    # 视图函数：注册
    # url(r'^register/$', views.register, name='register'),
    # 类视图： 注册
    url(r'^register/$',   views.RegisterView.as_view(), name='register'),
]
```

自定义视图

```
# views.py
def my_decorator(func):
    def wrapper(request, *args, **kwargs):
        print('自定义装饰器被调用了')
        print('请求路径%s' % request.path)
        return func(request, *args, **kwargs)
    return wrapper
        
# 为全部请求方法添加装饰器
@method_decorator(my_decorator, name='dispatch')
class DemoView(View):
    def get(self, request):
        print('get方法')
        return HttpResponse('ok')

    def post(self, request):
        print('post方法')
        return HttpResponse('ok')


# 为特定请求方法添加装饰器
@method_decorator(my_decorator, name='get')
class DemoView(View):
    def get(self, request):
        print('get方法')
        return HttpResponse('ok')

    def post(self, request):
        print('post方法')
        return HttpResponse('ok')
        
        
或者
class DemoView(View):

    @method_decorator(my_decorator)  # 为get方法添加了装饰器
    def get(self, request):
        print('get方法')
        return HttpResponse('ok')

    @method_decorator(my_decorator)  # 为post方法添加了装饰器
    def post(self, request):
        print('post方法')
        return HttpResponse('ok')

    def put(self, request):  # 没有为put方法添加装饰器
        print('put方法')
        return HttpResponse('ok')
        
```

mixin

```
class ListModelMixin(object):
    """
    list扩展类
    """
    def list(self, request, *args, **kwargs):
        ...

class CreateModelMixin(object):
    """
    create扩展类
    """
    def create(self, request, *args, **kwargs):
        ...

class BooksView(CreateModelMixin, ListModelMixin, View):
    """
    同时继承两个扩展类，复用list和create方法
    """
    def get(self, request):
        self.list(request)
        ...

    def post(self, request):
        self.create(request)
        ...

class SaveOrderView(CreateModelMixin, View):
    """
    继承CreateModelMixin扩展类，复用create方法
    """
    def post(self, request):
        self.create(request)
        ...
```



## 8.中间件

> 参考 ubuntu16_new 中的day06 
>
> 和 多重装饰器是一样的，就近原则

```
# 可以介入Django的请求和响应处理过程，修改Django的输入或输出

中间件工厂函数需要接收一个可以调用的get_response对象。
返回的中间件也是一个可以被调用的对象，并且像视图一样需要接收一个request对象参数，返回一个response对象。

def simple_middleware(get_response):
    # 此处编写的代码仅在Django第一次配置和初始化的时候执行一次。

    def middleware(request):
        # 此处编写的代码会在每个请求处理视图前被调用。

        response = get_response(request)

        # 此处编写的代码会在每个请求处理视图之后被调用。

        return response

    return middleware
    
定义好中间件后，需要在settings.py 文件中添加注册中间件
MIDDLEWARE = [
    'users.middleware.my_middleware',  # 添加中间件
]

# 注意：
多个中间件
请求视图被处理前，中间件由上至下依次执行
请求视图被处理后，中间件由下至上依次执行
内层函数外的初始化除外, 先初始化下面的，后初始化上面的

def my_middleware(get_response):
    print('init 被调用')
    def middleware(request):
        print('before request 被调用')
        response = get_response(request)
        print('after response 被调用')
        return response

    return middleware


def my_middleware2(get_response):
    print('init2 被调用')
    def middleware(request):
        print('before request 2 被调用')
        response = get_response(request)
        print('after response 2 被调用')
        return response

    return middleware
    
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'middleware.my_middleware',
    'middleware.my_middleware2',
]

init2 被调用
init 被调用
before request 被调用
before request 2 被调用
after response 2 被调用
after response 被调用
```



```
# 自定义中间件
process_request(self,request)
process_view(self, request, view_func, view_args, view_kwargs)
process_template_response(self,request,response)
process_exception(self, request, exception)
process_response(self, request, response)

自上而下的：
process_request： 如果有多个中间件都定义了，会按照MIDDLEWARE中的注册顺序，也就是列表的索引值，从前到后依次执行的

process_view： 如果有多个中间件都定义了，跟request一样，会按照MIDDLEWARE中的注册顺序，从前到后依次执行的

process_response： 如果有多个中件间都定义了，按照MIDDLEWARE中的注册顺序倒序执行的，也就是说第一个中间件的process_request方法首先执行，而它的process_response方法最后执行，最后一个中间件process_request方法最后一个执行，它的process_response方法是最先执行


```



## 9.数据库

### 9.1基本配置

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```

### 9.2引入mysql

1. 使用**MySQL**数据库首先需要安装驱动程序

   ```shell
   pip install PyMySQL
   ```

2. 在Django的工程同名子目录的__init__.py文件中添加如下语句

   ```python
   from pymysql import install_as_MySQLdb
   
   install_as_MySQLdb()
   ```

   作用是让Django的ORM能以mysqldb的方式来调用PyMySQL。

3. 修改**DATABASES**配置信息

   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'HOST': '127.0.0.1',  # 数据库主机
           'PORT': 3306,  # 数据库端口
           'USER': 'root',  # 数据库用户名
           'PASSWORD': 'mysql',  # 数据库用户密码
           'NAME': 'django_demo'  # 数据库名字
       }
   }
   ```

4. 在MySQL中创建数据库

   ```mysql
   create database django_demo default charset=utf8;
   ```



### 9.3定义模型类

字段类型

| 类型             | 说明                                                         |
| ---------------- | ------------------------------------------------------------ |
| AutoField        | 自动增长的IntegerField，通常不用指定，不指定时Django会自动创建属性名为id的自动增长属性 |
| BooleanField     | 布尔字段，值为True或False                                    |
| NullBooleanField | 支持Null、True、False三种值                                  |
| CharField        | 字符串，参数max_length表示最大字符个数                       |
| TextField        | 大文本字段，一般超过4000个字符时使用                         |
| IntegerField     | 整数                                                         |
| DecimalField     | 十进制浮点数， 参数max_digits表示总位数， 参数decimal_places表示小数位数 |
| FloatField       | 浮点数                                                       |
| DateField        | 日期， 参数auto_now表示每次保存对象时，自动设置该字段为当前时间，用于"最后一次修改"的时间戳，它总是使用当前日期，默认为False； 参数auto_now_add表示当对象第一次被创建时自动设置当前时间，用于创建的时间戳，它总是使用当前日期，默认为False; 参数auto_now_add和auto_now是相互排斥的，组合将会发生错误 |
| TimeField        | 时间，参数同DateField                                        |
| DateTimeField    | 日期时间，参数同DateField                                    |
| FileField        | 上传文件字段                                                 |
| ImageField       | 继承于FileField，对上传的内容进行校验，确保是有效的图片      |



选项

>  null表示什么都没有，blank表示空白，null=True表示允许什么都没有，blank=True表示允许空白，空白不代表什么都没有，空白字符串就是空白的值；

| 选项        | 说明                                                         |
| ----------- | ------------------------------------------------------------ |
| null        | 如果为True，表示允许为空，默认值是False                      |
| blank       | 如果为True，则该字段允许为空白，默认值是False                |
| db_column   | 字段的名称，如果未指定，则使用属性的名称                     |
| db_index    | 若值为True, 则在表中会为此字段创建索引，默认值是False        |
| default     | 默认                                                         |
| primary_key | 若为True，则该字段会成为模型的主键字段，默认值是False，一般作为AutoField的选项使用 |
| unique      | 如果为True, 这个字段在表中必须有唯一值，默认值是False        |

外键

```
在设置外键时，需要通过on_delete选项指明主表删除数据时，对于外键引用表数据如何处理，在django.db.models中包含了可选常量：

    CASCADE 级联，删除主表数据时连通一起删除外键表中数据

    PROTECT 保护，通过抛出ProtectedError异常，来阻止删除主表中被外键应用的数据

    SET_NULL 设置为NULL，仅在该字段null=True允许为null时可用

    SET_DEFAULT 设置为默认值，仅在该字段设置了默认值时可用
    
    DO_NOTHING 不做任何操作，如果数据库前置指明级联性，此选项会抛出IntegrityError异常

    SET() 设置为特定值或者调用特定方法，如：
    	def get_sentinel_user():
    		return get_user_model().objects.get_or_create(username='deleted')[0]

        class MyModel(models.Model):
            user = models.ForeignKey(
                settings.AUTH_USER_MODEL,
                on_delete= models.SET(get_sentinel_user),
            )
```

### 9.4迁移

```
python manage.py makemigrations
python manage.py migrate
```



### 9.5shell工具

```
python manage.py shell
```



### 9.6数据库操作(***)

增加

```
# save
>>> book = BookInfo(
    btitle='西游记',
    bput_date=date(1988,1,1),
    bread=10,
    bcomment=10
)
>>> book.save()

# create
>>> HeroInfo.objects.create(
    hname='沙悟净',
    hgender=0,
    hbook=book
)
<HeroInfo: 沙悟净>
```

修改

```
# save
hero = Hero.objects.get(hname='猪八戒')
hero.hname="xxx"
hero.save()

# update(会返回受影响的行数)
Hero.objects.filter(id=1).update(name="xxx")
```

删除

```
# delete
hero = Hero.objects.get(id=1)
hero.delete()

Hero.objects.filter(id=1).delete()
```



查询

```
get()  # 查询单一结果，如果不存在会抛出模型类.DoesNotExist异常
all()
count()

filter()
	过滤条件的表达语法如下：
        属性名称__比较运算符=值
        # 属性名称和比较运算符间使用两个下划线，所以属性名不能包括多个下划线
        
	相等
	包含(btitle_contains="xxx")
	startswith&endswith(btitle__endswith='部')  # 以上运算符都区分大小写，在这些运算符前加上i表示不区分大小写，如iexact、icontains、istartswith、iendswith.
	
	isnull             # BookInfo.objects.filter(btitle__isnull=False)
	in：是否包含在范围内。# BookInfo.objects.filter(id__in=[1, 3, 5])
	gt 大于 (greater then)
    gte 大于等于 (greater then equal)
    lt 小于 (less then)
    lte 小于等于 (less then equal)
    日期查询：
    	year、month、day、week_day、hour、minute、second：对日期时间类型的属性进行运算
    	# BookInfo.objects.filter(bpub_date__gt=date(1990, 1, 1))
    	
    F对象
    	之前的查询都是对象的属性与常量值比较，两个属性比较用F对象
    	from django.db.models import F
        BookInfo.objects.filter(bread__gte=F('bcomment'))
        
    Q对象(&,|)
    	BookInfo.objects.filter(bread__gt=20,id__lt=3)
        或
        BookInfo.objects.filter(bread__gt=20).filter(id__lt=3)
        
        BookInfo.objects.filter(Q(bread__gt=20) | Q(pk__lt=3))
        
        BookInfo.objects.filter(~Q(pk=3))
        
    聚合函数
    	使用aggregate()过滤器调用聚合函数。聚合函数包括：Avg 平均，Count 数量，Max 最大，Min 最小，Sum 求和，被定义在django.db.models中, 结果是一个字典类型。
    	
    	Bookinfo.objects.aggregate(Sum("bcomment"))  {'bcomment__sum': 21}
    	
****************************************************************************************************    	
    	aggregate()和annotate() 区别
        	https://blog.csdn.net/weixin_42134789/article/details/84567365
    	
    		aggregate()为 所有    QuerySet生成汇总值，           做统计, 返回结果类型为Dict。
    		annotate() 为 每一个  QuerySet在指定属性上生成汇总值，做分组, 返回结果类型QuerySet。单行操作
    		
    		e.g:
    			计算平均年龄和最高身高:
    			dict = Student.objects.aggregate(age=Avg("age"), max=Max("age"))   {'avg': 10.5, 'max': 20}
    			
    			查询一个学生的有多少任课老师：
    			https://docs.djangoproject.com/en/1.10/ref/models/querysets/#annotate
    			t = Student.objects.annotate(Count('Teacher'))
    			t[0].name
    			
    			t = Student.objects.annotate(number_of_entries = Count('Teacher'))
    			t[0].number_of_entries
    			t.count()
    			
                
          annotate方法与Filter方法联用
          有时我们需要先对数据集先筛选再分组，有时我们还需要先分组再对查询集进行筛选。根据需求不同，我们可以合理地联用annotate方法和filter方法。注意: annotate和filter方法联用时使用顺序很重要。

           # 先按爱好分组，再统计每组学生数量, 然后筛选出学生数量大于1的爱好。
Hobby.objects.annotate(student_num=Count('student')).filter(student_num__gte  = 1)  只能是等于
           # 先按爱好分组，筛选出以'd'开头的爱好，再统计每组学生数量。          		Hobby.objects.filter(name__startswith="d").annotate(student_num=Count('student‘))



          annotate与order_by()联用
		  我们同样可以使用order_by方法对annotate方法返回的数据集进行排序。
			   # 先按爱好分组，再统计每组学生数量, 然后按每组学生数量大小对爱好排序。
                Hobby.objects.annotate(student_num=Count('student')).order_by('student_num')
                Hobby.objects.annotate(student_num=Count('student')).order_by('-student_num')
                # 统计最受学生欢迎的5个爱好。
                Hobby.objects.annotate(student_num=Count('student')).order_by('-student_num')[:5]


           annotate与values()联用
           我们在前例中按学生对象进行分组，我们同样可以按学生姓名name来进行分组。唯一区别是本例中，如果两个学生具有相同名字，那么他们的爱好数量将叠加。
           # 按学生名字分组，统计每个学生的爱好数量。
           Student.objects.values('name').annotate(Count('hobbies'))

           你还可以使用values方法从annotate返回的数据集里提取你所需要的字段，如下所示:
           # 按学生名字分组，统计每个学生的爱好数量。
		   Student.objects.annotate(hobby_count=Count('hobbies')).values('name', 'hobby_count')
			
		
			aggregate + annotations
            >>> from django.db.models import Count, Avg
            >>> Book.objects.annotate(num_authors=Count('authors')).aggregate(Avg('num_authors'))
            { 'num_authors__avg': 1.66 }
            
            
            当你只需要某些列的时候可以使用 values 或者 values_list
            

       prefetch_related()和select_related()  不建议使用，底层sql查询爆炸，而且很多坑
	   https://blog.csdn.net/u012804178/article/details/70261994
****************************************************************************************************
    排序
    	BookInfo.objects.all().order_by('bread')  # 升序
        BookInfo.objects.all().order_by('-bread') # 降序

    关联查询
    	一对多：
    	    b = BookInfo.objects.get(id=1)
            b.heroinfo_set.all()
    	多对一：
    	    h = HeroInfo.objects.get(id=1)
            h.hbook
            h.hbook_id
        
    关联过滤查询：
    	由多模型类条件查询一模型类数据:
        语法如下：
        	多模型类名小写__属性名__条件运算符=值
        	BookInfo.objects.filter(heroinfo__hname='孙悟空')
        	
        由一模型类条件查询多模型类数据:
        语法如下：
            一模型关联属性名__属性名__条件运算符=值
            HeroInfo.objects.filter(hbook__btitle='天龙八部')
       
# 进阶
优化
对接sqlalchemy

# query_set 限制查询集
qs = BookInfo.objects.all()[0:2]    #  类似limit(), offset()
```



### 9.7管理器

```
默认objects
主要作用：
	1.修改原始查询集，重写all()方法
		a）打开booktest/models.py文件，定义类BookInfoManager

            #图书管理器
            class BookInfoManager(models.Manager):
                def all(self):
                    #默认查询未删除的图书信息
                    #调用父类的成员语法为：super().方法名
                    return super().filter(is_delete=False)
                    
        b）在模型类BookInfo中定义管理器

            class BookInfo(models.Model):
                ...
                books = BookInfoManager()
                # objects = BookInfoManager()
                
        c）使用方法
        	BookInfo.books.all()
        	
	2.在管理器类中补充定义新的方法
		a）打开booktest/models.py文件，定义方法create_book。
            class BookInfoManager(models.Manager):
                #创建模型类，接收参数为属性赋值
                def create_book(self, title, pub_date):
                    #创建模型类对象self.model可以获得模型类
                    book = self.model()
                    book.btitle = title
                    book.bpub_date = pub_date
                    book.bread=0
                    book.bcommet=0
                    book.is_delete = False
                    # 将数据插入进数据表
                    book.save()
                    return book
                    
            b）为模型类BookInfo定义管理器books语法如下
                class BookInfo(models.Model):
                      ...
                    books = BookInfoManager()
                    
            c）调用语法如下：

            	book=BookInfo.books.create_book("abc",date(1980,1,1))
```



### 9.8 orm调优

```
https://blog.csdn.net/u012804178/article/details/70261994

django.db.connection： django自身提供，比较底层， 可以用来记录当前查询花费的时间（知道了SQL语句查询的时间，当然就知道那里慢了)

	from django.db import connection
	result = Author.objects.aggregate(avg_age=Avg('age'))
	print(connection.queries) 　　# 打印执行时所有的查询语句

django-debug-toolbar： 可以在web端直接看到debug结果
```



## 10.模板

配置

在工程中创建模板目录templates。

在settings.py配置文件中修改**TEMPLATES**配置项的DIRS值：

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # 此处修改
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```



定义模板

在templates目录中新建一个模板文件，如index.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <h1>{{ city }}</h1>
</body>
</html>
```



模板渲染

步骤：

1. 找到模板 loader.get_template(模板文件在模板目录中的相对路径) -> 返回模板对象
2. 渲染模板 模板对象.render(context=None, request=None) -> 返回渲染后的html文本字符串 context 为模板变量字典，默认值为None request 为请求对象，默认值为None

```python
from django.http import HttpResponse
from django.template import loader

def index(request):
    # 1.获取模板
    template=loader.get_template('index.html')

    context={'city': '北京'}
    # 2.渲染模板
    return HttpResponse(template.render(context))
```



简化：

```
from django.shortcuts import render

def index(request):
    context={'city': '北京'}
    return render(request,'index.html',context)
```





模板语法

> 可参考Jinja2语法
>
> 如果跟vue一起用，解决办法

```
# 变量
{{变量}}

# for
{% for item in 列表 %}
循环逻辑
{{forloop.counter}}表示当前是第几次循环，从1开始
{%empty%} 列表为空或不存在时执行此逻辑
{% endfor %}


# if 
{% if ... %}
逻辑1
{% elif ... %}
逻辑2
{% else %}
逻辑3
{% endif %}


# 运算符
运算符左右两侧不能紧挨变量或常量，必须有空格
{% if a == 1 %}  # 正确

# 过滤器
	变量|过滤器:参数
	
# 注释
	1）单行注释语法如下：
		{#...#}
    2）多行注释使用comment标签，语法如下：
        {% comment %}
        {% endcomment %}
    
# 模板继承
	父模板
		{% block 名称 %}
        预留区域，可以编写默认内容，也可以没有默认内容
        {% endblock  名称 %}
	子模板
		{% block 名称 %}
        实际填充内容
        {{ block.super }}用于获取父模板中block的内容
        {% endblock 名称 %}
```





## 11.admin&xadmin

### admin

使用Django的管理模块，需要按照如下步骤操作：

1. 管理界面本地化
2. 创建管理员
3. 注册模型类
4. 自定义管理页面



#### 10.1 管理界面本地化

在settings.py中设置语言和时区

```python
LANGUAGE_CODE = 'zh-hans' # 使用中国语言
TIME_ZONE = 'Asia/Shanghai' # 使用中国上海时间
```



#### 10.2 创建管理员

```
python manage.py createsuperuser 
输入用户名
输入密码

浏览器访问： http://127.0.0.1:8000/admin/


补充： 如果想要修改密码可以执行
python manage.py changepassword 用户名
```



#### 10.3 注册模型类

打开booktest/admin.py文件，编写如下代码：

```
from django.contrib import admin
from booktest.models import BookInfo,HeroInfo

admin.site.register(BookInfo)
admin.site.register(HeroInfo)
```



#### 10.4 定义管理页面

```
from django.contrib import admin
class BookInfoAdmin(admin.ModelAdmin):
    pass

使用自定义的管理界面
# 方式一：注册参数
admin.site.register(BookInfo, BookInfoAdmin)

# 方式二：装饰器
@admin.register(BookInfo)
class BookInfoAdmin(admin.ModelAdmin):
    pass
```



#### 10.5 列表页

```
list_per_page = 5      # 分页
actions_on_top = True  # 动作栏的位置
actions_on_bottom = True
list_display = ['id', 'hname', 'hcomment', 'hbook']   # 页面上展示那些数据
list_filter = ['hbook', 'hgender']                   # 右侧过滤选项(大类)
search_fields = ['hname',"id"]                      # 上面搜索框的搜索选项

方法作为列：
	列可以是模型字段，还可以是模型方法，要求方法有返回值。
	通过设置short_description属性，可以设置在admin站点中显示的列名
	
	1）打开booktest/models.py文件，修改BookInfo类如下：
    class BookInfo(models.Model):
        def pub_date(self):
            return self.bpub_date.strftime('%Y年%m月%d日')
		
		# 设置方法字段在admin中显示的标题
        pub_date.short_description = '发布日期' 
        
        # 方法列是不能排序的，如果需要排序需要为方法指定排序依据, admin_order_field=模型类字段
        # 关闭/打开该选项，可通过在站点上点击id，title, pub_date来观察效果
        pub_date.admin_order_field = 'bpub_date'
        
    2）打开booktest/admin.py文件，修改BookInfoAdmin类如下：
    class BookInfoAdmin(admin.ModelAdmin):
    	list_display = ['id','atitle','pub_date']
    	
    
关联对象：
	无法直接访问关联对象的属性或方法，可以在模型类中封装方法，访问关联对象的成员。

    1）打开booktest/models.py文件，修改HeroInfo类如下：
    class HeroInfo(models.Model):
        ...
        def read(self):
            return self.hbook.bread

        read.short_description = '图书阅读量'
        
    2）打开booktest/admin.py文件，修改HeroInfoAdmin类如下：
    class HeroInfoAdmin(admin.ModelAdmin):
        ...
        list_display = ['id', 'hname', 'hbook', 'read']
    
```



#### 10.6 编辑页

```
fields: # 默认显示所有
	  e.g.: fields = ['btitle', 'bpub_date']
	  
分组显示:
	fieldset=(
    ('组1标题',{'fields':('字段1','字段2')}),
    ('组2标题',{'fields':('字段3','字段4')}),
)
	e.g.:
		class BookInfoAdmin(admin.ModelAdmin):
            # fields = ['btitle', 'bpub_date']  # 跟drf框架不要混淆
            
            # 不能跟上面同时使用
            fieldsets = (
                ('基本', {'fields': ['btitle', 'bpub_date']}),
                ('高级', {
                    'fields': ['bread', 'bcomment'],
                    'classes': ('collapse',)  # 是否折叠显示
                })
            )
	
关联对象：
	#子类TabularInline：以表格的形式嵌入。
	#子类StackedInline：以块的形式嵌入。

	class HeroInfoStackInline(admin.StackedInline):
        model = HeroInfo  # 要编辑的对象
        extra = 2         # 附加编辑的数量
       
    class BookInfoAdmin(admin.ModelAdmin):
    	inlines = [HeroInfoTabularInline]
    
```



#### 10.7 站点信息

```
# admin.py

admin.site.site_header = '图书管理网站后台'
admin.site.site_title = '图书管理网'
admin.site.index_title = '欢迎使用111'
```



#### 10.8 上传图片

```
安装相应的包：
pip install Pillow

配置：
# settings.py
MEDIA_ROOT=os.path.join(BASE_DIR,"static_files/media")

为模型类添加ImageField字段：
class BookInfo(models.Model):
    image = models.ImageField(upload_to='booktest', verbose_name='图片', null=True)
	# upload_to 选项指明该字段的图片保存在MEDIA_ROOT目录中的哪个子目录
	
进行数据库迁移操作：
python manage.py makemigrations
python manage.py migrate
	
测试：
进入Admin站点的图书管理页面，选择一个图书，能发现多出来一个上传图片的字段(前提：fields包含该字段)
选择一张图片并保存后，图片会被保存在static/media/booktest/目录下。
在数据库中，我们能看到image字段被设置为图片的路径
```



### xadmin

