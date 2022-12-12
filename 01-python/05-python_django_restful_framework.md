# 知识点总结

> 核心： 记住apiview,  genericapiview能提供什么属性，方法(能力)，参考xmind



## 基本视图类

### 1）APIView

#### 特点

1. **需要自定义get、post、put等请求方法，并且自己实现方法内部的所有逻辑。**

2. **必须用实例化类的方式来调用序列化器**（genericApiview,  则可以通过 serializer_class = xxx）

   ```
   serializer = BookInfoSerializer(books, many=True) 
   ```

#### 使用场景

1. 视图中实现的功能比较简单

2. 对序列化器依赖不强，[只需要序列化数据，不要其他的验证，保存修改等操作]

3. 与数据库交互不多(比如查询)

4. **提供了csrf免除， 鉴权，认证，限流，错误处理**(重点)

   

#### 示例

```
from rest_framework.views import APIView
from rest_framework.response import Response

# url(r'^books/$', views.BookListView.as_view()),
class BookListView(APIView):
    def get(self, request):
        books = BookInfo.objects.all()
        serializer = BookInfoSerializer(books, many=True)
        # 可以调用 serializer.is_valid() 
        # serializer.data 拿到的是序列化数据
        return Response(serializer.data)
    
    # or 
    
    def get(self, request， image_code_id):
        books = BookInfo.objects.all()
        serializer = BookInfoSerializer(books, many=True)
        return Response(serializer.data)
```



### 2）GenericAPIView

#### 特点

1. 同样需要自定义get、post等方法，但是可以配合**扩展类**，简化视图编写

2. **为列表视图和详情视图提供了通用支持方法，可以减少代码编写**，比如

   ```python
   get_queryset(self)
   get_serializer(self, args, *kwargs) 
   ```
####  使用场景

1. **列表需要分页，过滤(重点)**
2. **配合扩展类，  可以简化视图编写**
3. **列表视图和详情视图提供了通用支持方法, 可以减少代码编写**

#### 属性

```
列表视图与详情视图通用：
    queryset         列表视图的查询集
    serializer_class 视图使用的序列化器

列表视图使用：
	filter_backends  过滤控制类
    pagination_class 分页控制类
    
详情页视图使用：
    lookup_field     查询单一数据库对象时使用的条件字段，默认为'pk'
    lookup_url_kwarg 查询单一数据时URL中的参数关键字名称，默认与look_field相同
```

#### 方法

列表视图与详情视图通用：

    get_queryset(self)
        返回视图使用的查询集，是列表视图与详情视图获取数据的基础，默认返回queryset属性，可以重写，例如：
        def get_queryset(self):
            user = self.request.user
            return user.accounts.all()
            
    get_serializer_class(self)
        返回序列化器类，默认返回serializer_class，可以重写，例如：
        def get_serializer_class(self):
            if self.request.user.is_staff:
                return FullAccountSerializer
            return BasicAccountSerializer
            
    get_serializer(self, args, *kwargs)
        返回序列化器对象，被其他视图或扩展类使用，如果我们在视图中想要获取序列化器对象，可以直接调用此方法。
        注意，在提供序列化器对象的时候，REST framework会向对象的context属性补充三个数据：request、format、view，这三个数据对象可以在定义序列化器时使用。

详情视图使用：

```
 get_object(self) 
        返回详情视图所需的模型类数据对象，默认使用lookup_field参数来过滤queryset。 在试图中可以调用该方法获取详情信息的模型类对象。若详情访问的模型类对象不存在，会返回404。该方法会默认使用APIView提供的check_object_permissions方法检查当前对象是否有权限被访问。
```



#### 示例

```
url(r'^books/(?P<pk>\d+)/$', views.BookDetailView.as_view()),

class BookDetailView(GenericAPIView):
    queryset = BookInfo.objects.all()
    serializer_class = BookInfoSerializer
    
    def get(self, request, pk):
        book = self.get_object()
        serializer = self.get_serializer(book)
        return Response(serializer.data)
```



## 视图扩展类

> 扩展类必须配合GenericAPIView使用
>
> 扩展类内部的方法，在调用序列化器时，都是使用get_serializer
>
> 需要自定义get、post等请求方法，get、post内部调用扩展类对应方法即可,  比如：

```python
class BookListView(ListModelMixin, GenericAPIView):
    queryset = BookInfo.objects.all()
    serializer_class = BookInfoSerializer

    def get(self, request):
        return self.list(request)
```



### 1）ListModelMixin

1. 提供list方法，快速实现列表视图
2. 调用GenericAPIView设置好的结果集
3. 调用GenericAPIView设置好的序列化器

#### 特点

```
列表视图扩展类，提供list(request, *args, **kwargs)方法快速实现列表视图，返回200状态码。

该Mixin的list方法会对数据进行     过滤和分页(重点)
```

#### 示例

```
# 源代码
class ListModelMixin(object):
    """
    List a queryset.
    """
    def list(self, request, *args, **kwargs):
        # 过滤
        queryset = self.filter_queryset(self.get_queryset())
        # 分页
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        # 序列化
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
```

```
# e.g:

from rest_framework.mixins import ListModelMixin

class BookListView(ListModelMixin, GenericAPIView):
    queryset = BookInfo.objects.all()
    serializer_class = BookInfoSerializer

    def get(self, request):
        return self.list(request)
```



### 2）CreateModelMixin

1. 提供`create(request, *args, **kwargs)`方法快速实现创建资源的视图
2. 实际创建功能由序列化的save方法完成,   save方法会去调用序列化器的create方法

#### 特点

```
创建视图扩展类，提供create(request, *args, **kwargs)方法快速实现创建资源的视图，成功返回201状态码。

如果序列化器对前端发送的数据验证失败，返回400错误。
```

#### 示例

```
# 源代码
class CreateModelMixin(object):
    """
    Create a model instance.
    """
    def create(self, request, *args, **kwargs):
        # 获取序列化器
        serializer = self.get_serializer(data=request.data)
        # 验证
        serializer.is_valid(raise_exception=True)
        # 保存
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}
```



### 3）RetrieveModelMixin

1. 提供`retrieve(request, *args, **kwargs)`方法，可以快速实现返回一个存在的数据对象，如果存在，返回200， 否则返回404。

#### 示例

```
# 源代码：

class RetrieveModelMixin(object):
    """
    Retrieve a model instance.
    """
    def retrieve(self, request, *args, **kwargs):
        # 获取对象，会检查对象的权限
        instance = self.get_object()
        # 序列化
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
```



```
# 举例：
class BookDetailView(RetrieveModelMixin, GenericAPIView):
    queryset = BookInfo.objects.all()
    serializer_class = BookInfoSerializer

    def get(self, request, pk):
        return self.retrieve(request)
```



### 4）UpdateModelMixin

1. 提供`update(request, *args, **kwargs)`方法，可以快速实现更新一个存在的数据对象，同时也提供`partial_update(request, *args, **kwargs)`方法，可以实现局部更新， 成功返回200，序列化器校验数据失败时，返回400错误。
2. 内部更新功能调用序列化器的save方法,  save方法会调用序列化器的update方法

#### 示例

```
# 源代码

class UpdateModelMixin(object):
    """
    Update a model instance.
    """
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
```



### 5）DestroyModelMixin

1. 提供`destroy(request, *args, **kwargs)`方法，可以快速实现删除一个存在的数据对象，成功返回204，不存在返回404。
2. 内部模型对象的delete方法

#### 示例

```
# 源代码

class DestroyModelMixin(object):
    """
    Destroy a model instance.
    """
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
```



## 子视图类

### 特点

1. 类视图中**不需要自定义具体的get、post**等请求方法

2. 对GenericAPIView和视图扩展类的进一步封装

   

### 使用场景

1. 对应不同请求，继承相应的子类视图

2. **操作模型类的情况比较多**

    

### 1) CreateAPIView

 

### 2) ListAPIView

提供 get 方法

继承自：GenericAPIView、ListModelMixin

```
class SKUListView(ListAPIView):
    serializer_class = SKUSerializer
    # OrderingFilter The URL query parameter used for the ordering.
    filter_backends = (OrderingFilter,)
    ordering_fields = ('create_time', "price", "sales")

    def get_queryset(self):
        # 可通过断点的方式来获取字段, 看 self中 有什么字段，进而获取
        category_id = self.kwargs["category_id"]
        return SKU.objects.filter(category_id=category_id, is_launched=True)
```



### 3) RetireveAPIView

提供 get 方法

继承自: GenericAPIView、RetrieveModelMixin

```
from rest_framework.permissions import IsAuthenticated

class UserDetailView(RetrieveAPIView):
    """
    用户详情
    """
    serializer_class = serializers.UserDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
```



### 4) DestoryAPIView

提供 delete 方法

继承自：GenericAPIView、DestoryModelMixin



### 5) UpdateAPIView

提供 put 和 patch 方法

继承自：GenericAPIView、UpdateModelMixin

```
class EmailView(UpdateAPIView):
    """
    保存用户邮箱
    """
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.EmailSerializer

    def get_object(self, *args, **kwargs):
        return self.request.user
```



### 6) RetrieveUpdateAPIView

提供 get、put、patch方法

继承自： GenericAPIView、RetrieveModelMixin、UpdateModelMixin



### 7) RetrieveDestroyAPIView



### 8) RetrieveUpdateDestory...

提供 get、put、patch、delete方法

继承自：GenericAPIView、RetrieveModelMixin、UpdateModelMixin、DestoryModelMixin



### 9) ListCreateAPIView





## 视图集

### 特点

使用视图集ViewSet，可以将一系列逻辑相关的动作放到一个类中**(适用于一个类需要同时提供增删改查)**：

1. list() 提供一组数据
2. retrieve() 提供单个数据
3. create() 创建数据
4. update() 保存数据
5. destory() 删除数据
6. 自定义视图方法
  

### 优点

1. 视图定义简单
2. 路由简单



### 源码

```
class ViewSet(ViewSetMixin, views.APIView):
    """
    The base ViewSet class does not provide any actions by default.
    """
    pass


class GenericViewSet(ViewSetMixin, generics.GenericAPIView):
    """
    The GenericViewSet class does not provide any actions by default,
    but does include the base set of generic view behavior, such as
    the `get_object` and `get_queryset` methods.
    """
    pass


class ReadOnlyModelViewSet(mixins.RetrieveModelMixin,
                           mixins.ListModelMixin,
                           GenericViewSet):
    """
    A viewset that provides default `list()` and `retrieve()` actions.
    """
    pass


class ModelViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """
    pass

```



### 使用场景

1. **针对一个资源，需要使用的操作比较多(增删改查都有)**
2. 操作数据库比较多
3. 使用序列化器频繁



### 1) ViewSet

继承自`APIView`，作用也与APIView基本类似，提供了**身份认证、权限校验、流量管理**等。

在ViewSet中，没有提供任何动作action方法，需要我们自己实现action方法。

### 2) GenericViewSet

继承自`GenericAPIView`，作用也与GenericAPIVIew类似，提供了**get_object、get_queryset等方法便于列表视图与详情信息视图**的开发。 

**可以和上面各种mix配合使用**



### 3) ModelViewSet

继承自`GenericAPIVIew`，同时包括了ListModelMixin、RetrieveModelMixin、CreateModelMixin、UpdateModelMixin、DestoryModelMixin。



### 4) ReadOnlyModelViewSet

继承自`GenericAPIVIew`，同时包括了ListModelMixin、RetrieveModelMixin。



### 示例

ViewSet视图集类不再实现get()、post()等方法，而是实现动作 **action** 如 list() 、create() 等。

**视图集只在使用as_view()方法的时候**，才会将**action**动作与**具体请求方式**对应上。如：

```python
class BookInfoViewSet(viewsets.ViewSet):

    def list(self, request):
        ...

    def retrieve(self, request, pk=None):
        ...
```

在设置路由时，我们可以如下操作

```python
urlpatterns = [
    url(r'^books/$', BookInfoViewSet.as_view({'get':'list'}),
    url(r'^books/(?P<pk>\d+)/$', BookInfoViewSet.as_view({'get': 'retrieve'})
]
```



### action属性

在视图集中，我们可以通过action对象属性来获取当前请求视图集时的action动作是哪个。

例如：

```python
def get_serializer_class(self):
    if self.action == 'create':
        return OrderCommitSerializer
    else:
        return OrderDataSerializer
```





### 自定义action

添加自定义动作需要使用`rest_framework.decorators.action`装饰器。

以action装饰器装饰的方法名会作为action动作名，与list、retrieve等同。

action装饰器可以接收两个参数：

- **methods**: 该action支持的请求方式，列表传递

- **detail**

    : 表示是action中要处理的是否是视图资源的对象（即是否通过url路径获取主键）

    - True 表示使用通过URL获取的主键对应的数据对象

    - False 表示不使用URL获取主键

        

举例：

```python
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action

class BookInfoViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = BookInfo.objects.all()
    serializer_class = BookInfoSerializer

    # detail为False 表示不需要处理具体的BookInfo对象
    @action(methods=['get'], detail=False)
    def latest(self, request):
        """
        返回最新的图书信息
        """
        book = BookInfo.objects.latest('id')
        serializer = self.get_serializer(book)
        return Response(serializer.data)

    # detail为True，表示要处理具体与pk主键对应的BookInfo对象
    @action(methods=['put'], detail=True)
    def read(self, request, pk):
        """
        修改图书的阅读量数据
        """
        book = self.get_object()
        book.bread = request.data.get('read')
        book.save()
        serializer = self.get_serializer(book)
        return Response(serializer.data)
```

url的定义

```python
urlpatterns = [
    url(r'^books/$', views.BookInfoViewSet.as_view({'get': 'list'})),
    url(r'^books/latest/$', views.BookInfoViewSet.as_view({'get': 'latest'})),
    url(r'^books/(?P<pk>\d+)/$', views.BookInfoViewSet.as_view({'get': 'retrieve'})),
    url(r'^books/(?P<pk>\d+)/read/$', views.BookInfoViewSet.as_view({'put': 'read'})),
]
```





## 序列化器

```
参考xmind drf
```





## 其他

### 1) 认证

可以在配置文件中配置全局默认的认证方案

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',    # 基本认证
        'rest_framework.authentication.SessionAuthentication',  # session认证
    )
}
```

也可以在每个视图中通过设置authentication_classess属性来设置

```python
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.views import APIView

class ExampleView(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    ...
```

认证失败会有两种可能的返回值：

- 401 Unauthorized 未认证
- 403 Permission Denied 权限被禁止





### 2) 权限

权限控制可以限制用户对于**视图**的访问和对于**具体数据对象**的访问。

- 在执行视图的dispatch()方法前，       会先进行视图访问权限的判断
- 在通过get_object()获取具体对象时，会进行对象访问权限的判断

#### 使用

可以在配置文件中设置默认的权限管理类，如

```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}
```

如果未指明，则采用如下默认配置

```python
'DEFAULT_PERMISSION_CLASSES': (
   'rest_framework.permissions.AllowAny',
)
```

也可以在具体的视图中通过permission_classes属性来设置，如

```python
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

class ExampleView(APIView):
    permission_classes = (IsAuthenticated,)
    ...
```

#### 提供的权限

- AllowAny 允许所有用户
- IsAuthenticated 仅通过认证的用户
- IsAdminUser 仅管理员用户
- IsAuthenticatedOrReadOnly 认证的用户可以完全操作，否则只能get读取

#### 举例

```python
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView

class BookDetailView(RetrieveAPIView):
    queryset = BookInfo.objects.all()
    serializer_class = BookInfoSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
```

#### 自定义权限

如需自定义权限，需继承rest_framework.permissions.BasePermission父类，并实现以下两个任何一个方法或全部

- `.has_permission(self, request, view)`

    是否可以访问视图， view表示当前视图对象

- `.has_object_permission(self, request, view, obj)`

    是否可以访问数据对象， view表示当前视图， obj为数据对象

例如：

```python
class MyPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        """控制对obj对象的访问权限，此案例决绝所有对对象的访问"""
        return False

class BookInfoViewSet(ModelViewSet):
    queryset = BookInfo.objects.all()
    serializer_class = BookInfoSerializer
    permission_classes = [IsAuthenticated, MyPermission]
```



### 3) 限流

可以对接口访问的频次进行限制，以减轻服务器压力。

#### 使用

可以在配置文件中，使用`DEFAULT_THROTTLE_CLASSES` 和 `DEFAULT_THROTTLE_RATES`进行全局配置，

```python
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day'
    }
}
```

`DEFAULT_THROTTLE_RATES` 可以使用 `second`, `minute`, `hour` 或`day`来指明周期。

也可以在具体视图中通过throttle_classess属性来配置，如

```python
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView

class ExampleView(APIView):
    throttle_classes = (UserRateThrottle,)
    ...
```

#### 可选限流类

1） AnonRateThrottle

限制所有匿名未认证用户，使用IP区分用户。

使用`DEFAULT_THROTTLE_RATES['anon']` 来设置频次

2）UserRateThrottle

限制认证用户，使用User id 来区分。

使用`DEFAULT_THROTTLE_RATES['user']` 来设置频次

3）ScopedRateThrottle

限制用户对于每个视图的访问频次，使用ip或user id。

例如：

```
class ContactListView(APIView):
    throttle_scope = 'contacts'
    ...

class ContactDetailView(APIView):
    throttle_scope = 'contacts'
    ...

class UploadView(APIView):
    throttle_scope = 'uploads'
    ...
    
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.ScopedRateThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'contacts': '1000/day',
        'uploads': '20/day'
    }
}
```

#### 实例

```python
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView
from rest_framework.throttling import UserRateThrottle

class BookDetailView(RetrieveAPIView):
    queryset = BookInfo.objects.all()
    serializer_class = BookInfoSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = (UserRateThrottle,)
```



### 4) 过滤

对于列表数据可能需要根据字段进行过滤，我们可以通过添加django-fitlter扩展来增强支持。

```shel
pip install django-filter
```

在配置文件中增加过滤后端的设置：

```python
INSTALLED_APPS = [
    ...
    'django_filters',  # 需要注册应用
]

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',)
}
```

在视图中添加filter_fields属性，指定可以过滤的字段

```python
class BookListView(ListAPIView):
    queryset = BookInfo.objects.all()
    serializer_class = BookInfoSerializer
    filter_fields = ('btitle', 'bread')

# 127.0.0.1:8000/books/?btitle=西游记
```



### 5) 排序

对于列表数据，REST framework提供了**OrderingFilter**过滤器来帮助我们快速指明数据按照指定字段进行排序。



#### 使用

在类视图中设置filter_backends，使用`rest_framework.filters.OrderingFilter`过滤器，REST framework会在请求的查询字符串参数中检查是否包含了ordering参数，如果包含了ordering参数，则按照ordering参数指明的排序字段对数据集进行排序。

前端可以传递的ordering参数的可选字段值需要在ordering_fields中指明。



#### 示例

```python
class BookListView(ListAPIView):
    queryset = BookInfo.objects.all()
    serializer_class = BookInfoSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ('id', 'bread', 'bpub_date')

# 127.0.0.1:8000/books/?ordering=-bread
```



### 6) 分页

REST framework提供了分页的支持。

我们可以在配置文件中设置全局的分页方式，如：

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS':  'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100  # 每页数目
}
```

也可通过自定义Pagination类，来为视图添加不同分页行为。在视图中通过`pagination_class` 属性来指明。

```python
class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000
    
class BookDetailView(RetrieveAPIView):
    queryset = BookInfo.objects.all()
    serializer_class = BookInfoSerializer
    pagination_class = LargeResultsSetPagination
```

**注意：如果在视图内关闭分页功能，只需在视图内设置**

```python
pagination_class = None
```



#### 可选分页器

##### 1） **PageNumberPagination**

前端访问网址形式：

```http
GET  http://api.example.org/books/?page=4
```

可以在子类中定义的属性：

- page_size 每页数目
- page_query_param 前端发送的页数关键字名，默认为"page"
- page_size_query_param 前端发送的每页数目关键字名，默认为None
- max_page_size 前端最多能设置的每页数量

```python
from rest_framework.pagination import PageNumberPagination

class StandardPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 10

class BookListView(ListAPIView):
    queryset = BookInfo.objects.all().order_by('id')
    serializer_class = BookInfoSerializer
    pagination_class = StandardPageNumberPagination

# 127.0.0.1/books/?page=1&page_size=2
```

##### 2）**LimitOffsetPagination**

前端访问网址形式：

```http
GET http://api.example.org/books/?limit=100&offset=400
```

可以在子类中定义的属性：

- default_limit 默认限制，默认值与`PAGE_SIZE`设置一直
- limit_query_param limit参数名，默认'limit'
- offset_query_param offset参数名，默认'offset'
- max_limit 最大limit限制，默认None

```python
from rest_framework.pagination import LimitOffsetPagination

class BookListView(ListAPIView):
    queryset = BookInfo.objects.all().order_by('id')
    serializer_class = BookInfoSerializer
    pagination_class = LimitOffsetPagination

# 127.0.0.1:8000/books/?offset=3&limit=2
```



### 7) 版本

REST framework提供了版本号的支持。

在需要获取请求的版本号时，可以通过`request.version`来获取。

默认版本功能未开启，`request.version` 返回None。

开启版本支持功能，需要在配置文件中设置`DEFAULT_VERSIONING_CLASS`

```python
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning'
}
```

其他可选配置：

- **DEFAULT_VERSION** 默认版本号，默认值为None
- **ALLOWED_VERSIONS** 允许请求的版本号，默认值为None
- **VERSION_PARAM** 识别版本号参数的名称，默认值为'version'

#### 支持的版本处理方式

##### **1）AcceptHeaderVersioning**

请求头中传递的Accept携带version

```python
GET /bookings/ HTTP/1.1
Host: example.com
Accept: application/json; version=1.0
```

##### **2）URLPathVersioning**

URL路径中携带

```python
urlpatterns = [
    url(
        r'^(?P<version>(v1|v2))/bookings/$',
        bookings_list,
        name='bookings-list'
    ),
    url(
        r'^(?P<version>(v1|v2))/bookings/(?P<pk>[0-9]+)/$',
        bookings_detail,
        name='bookings-detail'
    )
]
```

##### **3）NamespaceVersioning**

命名空间中定义

```python
# bookings/urls.py
urlpatterns = [
    url(r'^$', bookings_list, name='bookings-list'),
    url(r'^(?P<pk>[0-9]+)/$', bookings_detail, name='bookings-detail')
]

# urls.py
urlpatterns = [
    url(r'^v1/bookings/', include('bookings.urls', namespace='v1')),
    url(r'^v2/bookings/', include('bookings.urls', namespace='v2'))
]
```

##### **4）HostNameVersioning**

主机域名携带

```python
GET /bookings/ HTTP/1.1
Host: v1.example.com
Accept: application/json
```

##### **5）QueryParameterVersioning**

查询字符串携带

```python
GET /something/?version=0.1 HTTP/1.1
Host: example.com
Accept: application/json
```

#### 示例

```python
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.QueryParameterVersioning'
}
class BookInfoSerializer(serializers.ModelSerializer):
    """图书数据序列化器"""
    class Meta:
        model = BookInfo
        fields = ('id', 'btitle', 'bpub_date', 'bread', 'bcomment')

class BookInfoSerializer2(serializers.ModelSerializer):
    """图书数据序列化器"""
    class Meta:
        model = BookInfo
        fields = ('id', 'btitle', 'bpub_date')

class BookDetailView(RetrieveAPIView):
    queryset = BookInfo.objects.all()

    def get_serializer_class(self):
        if self.request.version == '1.0':
            return BookInfoSerializer
        else:
            return BookInfoSerializer2

# 127.0.0.1:8000/books/2/
# 127.0.0.1:8000/books/2/?version=1.0
```



### 8) 异常处理 Exceptions

REST framework提供了异常处理，我们可以自定义异常处理函数。

```python
from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    # 先调用REST framework默认的异常处理方法获得标准错误响应对象
    response = exception_handler(exc, context)

    # 在此处补充自定义的异常处理
    if response is not None:
        response.data['status_code'] = response.status_code

    return response
```

在配置文件中声明自定义的异常处理

```python
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'my_project.my_app.utils.custom_exception_handler'
}
```

如果未声明，会采用默认的方式，如下

```python
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler'
}
```

例如：

补充上处理关于数据库的异常

```python
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework import status
from django.db import DatabaseError

def exception_handler(exc, context):
    response = drf_exception_handler(exc, context)

    if response is None:
        view = context['view']
        if isinstance(exc, DatabaseError):
            print('[%s]: %s' % (view, exc))
            response = Response({'detail': '服务器内部错误'}, status=status.HTTP_507_INSUFFICIENT_STORAGE)

    return response
```

#### REST framework定义的异常

- APIException 所有异常的父类
- ParseError 解析错误
- AuthenticationFailed 认证失败
- NotAuthenticated 尚未认证
- PermissionDenied 权限决绝
- NotFound 未找到
- MethodNotAllowed 请求方式不支持
- NotAcceptable 要获取的数据格式不支持
- Throttled 超过限流次数
- ValidationError 校验失败



### 9) 自动生成接口文档

REST framework可以自动帮助我们生成接口文档。

接口文档以网页的方式呈现。

自动接口文档能生成的是继承自`APIView`及其子类的视图。

#### 1. 安装依赖

REST framewrok生成接口文档需要`coreapi`库的支持。

```python
pip install coreapi
```

#### 2. 设置接口文档访问路径

在总路由中添加接口文档路径。

文档路由对应的视图配置为`rest_framework.documentation.include_docs_urls`，

参数`title`为接口文档网站的标题。

```python
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    ...
    url(r'^docs/', include_docs_urls(title='My API title'))
]
```

#### 3. 文档描述说明的定义位置

1） 单一方法的视图，可直接使用类视图的文档字符串，如

```python
class BookListView(generics.ListAPIView):
    """
    返回所有图书信息.
    """
```

2）包含多个方法的视图，在类视图的文档字符串中，分开方法定义，如

```python
class BookListCreateView(generics.ListCreateAPIView):
    """
    get:
    返回所有图书信息.

    post:
    新建图书.
    """
```

3）对于视图集ViewSet，仍在类视图的文档字符串中封开定义，但是应使用action名称区分，如

```python
class BookInfoViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    """
    list:
    返回图书列表数据

    retrieve:
    返回图书详情数据

    latest:
    返回最新的图书数据

    read:
    修改图书的阅读量
    """
```

#### 4. 访问接口文档网页

浏览器访问 127.0.0.1:8000/docs/，即可看到自动生成的接口文档。

![接口文档网页](../images/接口文档网页.png)

##### 两点说明：

1） 视图集ViewSet中的retrieve名称，在接口文档网站中叫做read

2）参数的Description需要在模型类或序列化器类的字段中以help_text选项定义，如：

```python
class BookInfo(models.Model):
    ...
    bread = models.IntegerField(default=0, verbose_name='阅读量', help_text='阅读量')
    ...
```

或

```python
class BookReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookInfo
        fields = ('bread', )
        extra_kwargs = {
            'bread': {
                'required': True,
                'help_text': '阅读量'
            }
        }
```