## 1. udp 

```
常用于广播
ip address：标记网络上的电脑
mac address:

ens33, ens40

ctrl+a(行首),ctrl+e（行尾）
sudo ifconfig ens40 down/up

ip地址分类：
ipv4:xxx.xxx.xxx.xxx 
ipv6:xxxx::xxx:xxxx:xxxx:xxxx(16进制)


网络号（00000000，后7位） + 主机号（1——254）
a类: 0（1-127）
b类: 10（128-191）
c类：110（192）
d类：多点广播
e类：实验开发用

netstat -an  查看端口状态

2.port
目标ip+ 目标port
源ip+ 源port
content:

3.socket(重点)
import socket
#tcp
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#udp
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

s.close()

4.udp接受发送数据
udp_socket.sendto(b"haha",('192.168.11.158',3306))
send_data = ""
send_data.encode("utf-8")

网络调试助手,不在同一个网段 ，ping

5.绑定端口
udp_socket.bind((ip,port))
udp_socket.recvfrom(1024)

receive_data[0].decode("gbk") #发送过来到的内容
receive_data[1]  #ip，port

6.udp聊天 （半双工）
抽取发送和接受消息的方法
```

## 2. tcp

```
socket是同时可以收发数据的
单工
半双工
全双工  socket

tcp:可靠传输，三次握手
采用应答机制
超时重传
错误校验
流量控制和阻塞管理


tcp,udp不同:
有序数据传输
重发丢失的数据
舍弃丢失的数据
无差错的数据
阻塞/流量控制


1.tcp客服端，服务端
tcp客户端：
创建套接字：
创建连接 connect((ip,port))  三次握手在此阶段
发送消息 send(send_data.encode("utf-8"))
接受消息 recv
关闭


tcp服务端：
创建套接字
bind
listen变为被动连接
accept等待客户端的连接
recv/send接受发送数据

2.下载文件
with使用注意事项：write/  read(用try,except)

对方close/send  服务端解阻塞，通过判断长度是否为0，判断是否下线


3.tcp3次握手，4次挥手


4.tcp短连接，长连接
短连接：每次传递数据都需要建立连接，关闭数据
长连接：建立一次连接，多次传递数据，关闭连接
```



## 3. 线程


```
1.
t1 = threading.Thread(target=sing)
t2 = threading.Thread(target=dance)
t1.start()
t2.start()

并行：真的多任务
并发：假的多任务

2.打印线程名，线程数
threading.enumerate()
#如果创建thread执行的函数，运行结束意味着这个子线程结束了
调用start() 之后才创建线程，target开始执行

3.创建线程的另一种方式：
class MyThread(threading.Thread)
	def run(self):
		pass

if __name__ == "__main__":
	t = MyThread()
	t.start()
	
4.start---bootstrap---bootstrapinner---run()

5.线程共享全局变量
可变不可变（global 与否）
nums.append()/extend() (ok) ；nums+=[100,200](error,需全局globel)

可变变量(__iadd__(),__add__())/不可变变量(__add__())的+=


6.多线程共享全局变量
t1 = threading.Thread(target=test1,args=(g_nums,)，kwargs)

def xxx(temp,**kwargs)

7.互斥锁
mutex = threading.Lock()
mutex.acquire()
mutex.release()

线程池
银行家算法
```



## 4. 进程

```
1.进程的状态：
新建---就绪---运行---死亡
	   等待（阻塞）

2.进程的创建：
method1:
import multiprocessing
p1 = multiprocessing.Process(target=test1)

method2:
class MyProcess(multiprocessing.Process)
	pass

p1 = MyProcess()
p1.start()

process语法：
start()
is_alive()
join(timeout) 等完成后执行后面的代码
terminate()

3.pid,ppid()
os.getpid()
os.getppid()

主进程挂了，子进程不会挂
主线程挂了，子线程也会挂掉


传参
（target = test,args=(),kwargs={}）
ipython3/help(multiprocessing.Process)


进程不能共享全局变量

================对比======================
功能：
进程：资源的总称，qq多开
线程：一个qq中的的多任务

定义：
进程是系统进行资源分配和调度的一个独立单位
线程是进程的一个实体,是CPU调度和分派的基本单位

区别：
一个程序至少有一个进程,一个进程至少有一个线程.
线程的划分尺度小于进程(资源比进程少)，使得多线程程序的并发性高。
进程在执行过程中拥有独立的内存单元，而多个线程共享内存，从而极大地提高了程序的运行效率
线程不能够独立执行，必须依存在进程中
可以将进程理解为工厂中的一条流水线，而其中的线程就是这个流水线上的工人

优缺点：
线程执行开销小，但不利于资源的管理和保护；而进程正相反

4.进程间通讯---队列（同一程序，同一电脑）
socket
队列
文件

from multiprocessing import Queue

q = Queue(3)
q.put()  #阻塞
q.get()
q.get_nowait() 
q.put_nowait()

full()
empty()
qsize()

实例：我们以Queue为例，在父进程中创建两个子进程，一个往Queue里写数据，一个从Queue里读数据：

5.进程池  （先close再join）
导包注意是大写的Pool

p = Pool()
p.apply_async(worker,(i,))
p.close()
p.join()

进程池中的队列：  Manager创建
from multiprocessing import Manager,Pool

q = Manager().Queue()
p.apply_async(worker,(q,))
```



## 5. 协程

```
1.迭代器
isinstance(xxx,Iterator/Iterable)
iter(class)
next(iterator_ref)

作用:生成数据的方式，且占用空间小
区别：xrange和range
其他：list(iterable)  生成iterable，再遍历;tuple(iterable)

buildins：
map(set,filter,slice,zip,complex,bytearrays, bytes,以及各种报错)

2.生成器（一类特殊的迭代器）
method1:g = (x for x in range(10))
method2: yield

next()
send():获取值的同时往里面传参数（send(None)）
注意：生成器只能遍历一次


3.协程yield
4.greenlet
5.gevent
6.文件下载器 (todo)

7.线程，进程，协程的区别

进程是资源分配的单位
线程是操作系统调度的单位
协程是一个cpu单元，占用资源小，效率高
多线程，多进程可能是并行，协程在一个线程中，是并发
```



## 6. 正则表达式

```
1.示例：
import re
result = re.match("d","donghuan")
result.group(option)

2.规则
[abc] a、b 或 c（简单类）
[^abc] 任何字符，除了 a、b ,c（否定）
[a-zA-Z] a 到 z 或 A 到 Z，两头的字母包括在内（范围）
[0-9] 0到9的字符都包括
[a-d[m-p]] a 到 d 或 m 到 p：[a-dm-p]（并集）
[a-z&&[def]] d、e 或 f（交集）
[a-z&&[^bc]] a 到 z，除了 b 和 c：[ad-z]（减去）
[a-z&&[^m-p]] a 到 z，而非 m 到 p：[a-lq-z]（减去）

. 任何一个字符（除了\n）
\d 数字：[0-9]
\D 非数字： [^0-9]
\s 空白字符：[ \t\n\x0B\f\r] //空格,\t:制表符,\n:换行,\x0B:垂直制表符,\f:翻页,\r:回车
\S 非空白字符：[^\s] 
\w 单词字符：[a-zA-Z_0-9] ,各种语言中的字符
\W 非单词字符：[^\w] 


X?  X，出现一次或一次也没有
X*  X，出现零次到多次
X+  X，出现一次到多次
X{n} X，出现恰好 n 次 
X{n,} X，出现至少 n 次
X{n,m} X，出现至少 n 次，但是不超过 m 次 

边界：
^  匹配字符串开头


$  匹配字符串结尾
\b 匹配一个单词的边界
\B 匹配非单词边界

分组：
| 匹配左右任意一个表达式 
(ab) 将括号中字符作为一个分组（匹配不同的邮箱(163|126|qq)）
\num 引用分组num匹配到的字符串   
(?P<name>)分组起别名 （P只能小写？？？）
(?P=name)引用别名为name分组匹配到的字符串

python原生字符串 r

re模块的高级用法：
search()
findall()---list（不需要用group）
sub(regex,替换的（可以是方法），待替换的):将匹配到的数据进行替换
split()---list

贪婪(默认，匹配越多越好)和非贪婪？
注意：看是开头（不正常，越多越好）还是结尾（正常的，越少越好）
re.match(r"aa(\d+?)","aa2343ddd").group(1)  
结果：2

re.match(r"aa(\d+?)ddd","aa2343ddd").group(1)
结果：2343


3.补充：
3.1 re.S 可以让.匹配\n

3.2
"""
fjajd
ladjlf
fjlkadj 
"""
可以换行

3.3如果需要用到某些字符（跟规则冲突），添加\,进行转义
```



## 7. 进阶1

### 7.1 gil

```
1.GIL(全局解释器锁)
多线程gil问题：python解释器（cpython, jpython没有这个问题）的问题
io密集（文件读写，线程，协程（gevent单线程，将等待时间利用来做其他事情））/计算密集（继承）

method1:
	jpython解释器
method2：
	c语言解决gil问题:
	生成so库文件：gcc xxx.c -shared -o libxxx.so

from ctypes import *
lib = cdll.loadLibraty("./libdead_loop.so")
```



### 7.2 深拷贝，浅拷贝

```
import copy
c = copy.deepcopy(a)
id 不同，内容独立
c = copy.copy(a)/ c = a（id相同）

情况1：包含list,dic
a = [11,22]
b = [33,44]
c = [a,b]

e = copy.copy(c)
e,c id 不同，id(e[0]),id(c[0])相同，说明创建了一份新的（将a,b拷贝出来）

e中存的是之前c指向的a，b的引用

情况2：
a = [11,22]
b = [33,44]
c = [a,b]

e = copy.deepcopy(c)
e,c id 不同，id(e[0]),id(c[0])不同

e中存的是完全独立的（复制出来的）a，b的内容（引用）

情况3：
a = [11,22]
b = [33,44]
c = [a,b]

d  = copy.copy(c)
e = copy.deepcopy(c)

c.append([55,66]) #如果a.append/b.append()
d # [[11,22],[33,44]]
e # [[11,22],[33,44]]


情况4：tuple
a = (11,22)
b= copy.copy(a)/copy.deepcopy(a)
id(a),id(b)相同 ,tuple不可变
等价于：
a=b

a = [11,22]
b = [33,44]
c = (a,b)
d = copy.copy(c) id相同
e = copy.deepcopy(c)  id不同

元组里面的是不可变的，copy,deepcopy都一样
元组里面的是可变的，copy一样,deepcopy不一样

情况5；
切片copy  浅拷贝
字典.copy (字典中的key放的都是引用)


说明：
分片和copy.copy()一样是浅拷贝
字典的copy(),浅拷贝

浅拷贝对不可变类型和可变类型的copy不同
copy.copy对于可变类型，会进行浅拷贝
copy.copy对于不可变类型，不会拷贝，仅仅是指向
```



### 7.3 私有化

```
_x:私有化属性或方法，不能被其他包导入
__xx:避免与子类的属性命名冲突，无法在外部访问
__xx__:魔法对象或属性（例如：__init__）
xx_:避免与python关键字的冲突
```



### 7.4 导包

```
# import 
import sys
sys.path

# ipython   #import才能用
from imp import reload
reload(aa) 

help(reload) 

导常量的时候注意用import common ，不要用 from common import *
```

### 7.5 多继承

```
# 多继承，mro顺序
python没有重载
用super()不用类名（导致父类调多次）

tips:super(grason,self).__init__()

print(parent.__mro__)  #调用的先后顺序
c3算法
```



### 7.6 args, kwargs 拆包



### 7.7 类对象，实例对象等

```
类对象，实例对象；类属性，实例属性；静态方法(staticMethod)，实例方法，类方法(classMethod)
@classMethod
def cls_fun(cls):
	pass
	
@staticMethod
def static_func():
	pass
	
实例对象.__class__
```



### 7.8 property

```
class Foo:
    def func(self):
        pass

    # 定义property属性
    @property
    def prop(self):
        pass
		
仅有一个self参数
调用时无需括号

形式：
1.装饰器
2.类属性


形式一：装饰器
经典类，具有一种@property装饰器（python2）
class Goods:
    @property
    def price(self):
        return "laowang"

obj = Goods()
result = obj.price  # 自动执行 @property 修饰的 price 方法，并获取方法的返回值
print(result)

新式类，具有三种@property装饰器：(python3)
class Goods:
    """python3中默认继承object类
        以python2、3执行此程序的结果不同，因为只有在python3中才有@xxx.setter  @xxx.deleter
    """
    @property
    def price(self):
        print('@property')

    @price.setter
    def price(self, value):
        print('@price.setter')

    @price.deleter
    def price(self):
        print('@price.deleter')
		
obj = Goods()
obj.price = 123    # 自动执行 @price.setter 修饰的 price 方法，并将  123 赋值给方法的参数
del obj.price      # 自动执行 @price.deleter 修饰的 price 方法

形式二：类属性方式
class Foo(object):
    def get_bar(self):
        print("getter...")
        return 'laowang'

    def set_bar(self, value): 
        """必须两个参数"""
        print("setter...")
        return 'set value' + value

    def del_bar(self):
        print("deleter...")
        return 'laowang'

    BAR = property(get_bar, set_bar, del_bar, "description...")

obj = Goods()
obj.PRICE         # 获取商品价格
obj.PRICE = 200   # 修改商品原价
del obj.PRICE     # 删除商品原价


应用：
Django框架中应用了property属性
property取代getter和setter方法

class Money(object):
    def __init__(self):
        self.__money = 0
    # 使用装饰器对money进行装饰，那么会自动添加一个叫money的属性，当调用获取money的值时，调用装饰的方法
    @property
    def money(self):
        return self.__money

    # 使用装饰器对money进行装饰，当对money设置值时，调用装饰的方法
    @money.setter
    def money(self, value):
        if isinstance(value, int): 
            self.__money = value
        else:
            print("error:不是整型数字")

a = Money()
a.money = 100
print(a.money)
```



### 7.9 魔法属性

```
魔法属性：
__doc__；表示类的描述信息
__module__ （表示当前操作的对象在那个模块）和 __class__（表示当前操作的对象的类是什么）：
__dict__：类或对象中的所有属性（可看到私有属性）
__call__:对象后面的括号执行 ，调用
__getitem__、__setitem__、__delitem__：用于索引操作，如字典。以上分别表示获取、设置、删除数据
__getslice__、__setslice__、__delslice__：该三个方法用于分片操作，如：列表



https://www.jb51.net/article/156169.htm


# 魔法属性
__dict__ ： 存储了类定义的所有类属性、类方法等组成的键值对，但不包括继承而来的属性和方法

__doc__  :  该属性记录了类的说明文档

__module__: 该属性记录类定义的位置，如果定义的位置正好是主程序，那么该值为"_main_",否则是类属于的模块的名字

__slot__ :  该属性起到限制动态绑定属性和方法的作用，该属性是一个元组，默认是不存在的，需要手动定义并且只对当前的类起作用，只有添加到元组中的名字才能被动态添加属性，否则报错！
    e.g:
        class Person(object):
        # 限制动态添加的属性或者方法
        __slots__ = ('name','age','run')
        
        def __init__(self):
            self.height = 100 # 不会报错

        def run(self):
            print('run')
        
        if __name__ == "__main__":
            from types import MethodType
            person = Person()
            person.name = 'cai'
            person.run = MethodType(run,person)
            person.run()
            
            
            
# 魔法方法
__new__()

__init__()

__repr__()

__call__()
    In [39]: class FatBoss: 
    ...:     """描述信息：我就是超级胖子老板，问你怕不怕""" 
    ...:     def __init__(self,name): 
    ...:         self.name = name 
    ...:     def func(self): 
    ...:         pass 
    ...:     def __del__(self): 
    ...:         print("哎呀，我被销毁啦。") 
    ...:     def __call__(self,*args,**kwargs): 
    ...:         print("胖子老板：没事你call我干嘛") 
    ...:         
    In [40]: fb = FatBoss("我就是胖子老板")   
    
    In [43]: fb()                                                                             
    胖子老板：没事你call我干嘛

__getattr__()         获取一个不存在的属性
__getattribute__()    获取一个存在的属性

__getitem__(), __setitem__()    索引
e.g:
    In [56]: class FatBoss: 
    ...:     def __getitem__(self,key): 
    ...:         print('__getitem__',key) 
    ...:     def __setitem__(self,key,value): 
    ...:         print("__setitem__",key,value) 
    ...:     def __delitem__(self,key): 
    ...:         print("__delitem__",key) 
    ...:                                                                                  

    In [57]: fb = FatBoss()                                                                   
    
    In [58]: result = fb['f1']                                                                
    __getitem__ f1
    
    In [59]: fb['f2'] = "我就是胖子老板"                                                      
    __setitem__ f2 我就是胖子老板
    
    In [60]: del obj['f1'] 



__getslice__(),__setslice__()   分片
e.g.:
    class Foo(object):

    def __getslice__(self, i, j):
        print('__getslice__', i, j)

    def __setslice__(self, i, j, sequence):
        print('__setslice__', i, j)

    def __delslice__(self, i, j):
        print('__delslice__', i, j)

    obj = Foo()
    
    obj[-1:1]                   # 自动触发执行 __getslice__
    obj[0:1] = [11,22,33,44]    # 自动触发执行 __setslice__
    del obj[0:2]                # 自动触发执行 __delslice__
```



### 7.10 上下文管理器

```
6.1
	任何实现了 __enter__() 和 __exit__() 方法的对象都可称之为上下文管理器
	
6.2 另外方式：
from contextlib import contextmanager

@contextmanager
def my_open(path, mode):
    f = open(path, mode)
    yield f
    f.close()
	
通过 yield 将函数分割成两部分，yield 之前的语句在 __enter__ 方法中执行，yield 之后的语句在 __exit__ 方法中执行。
紧跟在 yield 后面的值是函数的返回值

```



## 8. 进阶2

### 8.1 闭包

```
例子1：
# 定义一个函数
def test(number):

    # 在函数内部再定义一个函数，并且这个函数用到了外边函数的变量，那么将这个函数以及用到的一些变量称之为闭包
    def test_in(number_in):
        print("in test_in 函数, number_in is %d" % number_in)
        return number+number_in
    # 其实这里返回的就是闭包的结果
    return test_in


# 给test函数赋值，这个20就是给参数number
ret = test(20)

# 注意这里的100其实给参数number_in
print(ret(100))

#注 意这里的200其实给参数number_in
print(ret(200))



例子2：
def line_conf(a, b):
    def line(x):
        return a*x + b
    return line

line1 = line_conf(1, 1)
line2 = line_conf(4, 5)
print(line1(5))
print(line2(5))

这个例子中，函数line与变量a,b构成闭包。在创建闭包的时候，我们通过line_conf的参数a,b说明了这两个变量的取值，这样，我们就确定了函数的最终形式(y = x + 1和y = 4x + 5)。我们只需要变换参数a,b，就可以获得不同的直线表达函数。由此，我们可以看到，闭包也具有提高代码可复用性的作用。

如果没有闭包，我们需要每次创建直线函数的时候同时说明a,b,x。这样，我们就需要更多的参数传递，也减少了代码的可移植性。

注意点:

由于闭包引用了外部函数的局部变量，则外部函数的局部变量没有及时释放，消耗内存





修改外部函数中的变量
# python3的方法
def counter(start=0):
    def incr():
        nonlocal start
        start += 1
        return start
    return incr

c1 = counter(5)
print(c1())
print(c1())

c2 = counter(50)
print(c2())
print(c2())

print(c1())
print(c1())

print(c2())
print(c2())


# python2的方法
def counter(start=0):
    count=[start]
    def incr():
        count[0] += 1
        return count[0]
    return incr

c1 = closeure.counter(5)
print(c1())  # 6
print(c1())  # 7
c2 = closeure.counter(100)
print(c2())  # 101
print(c2())  # 102
```



### 8.2 装饰器

#### 8.2.1 示例

```
# 定义函数：完成包裹数据
def makeBold(fn):
    def wrapped():
        return "<b>" + fn() + "</b>"
    return wrapped

# 定义函数：完成包裹数据
def makeItalic(fn):
    def wrapped():
        return "<i>" + fn() + "</i>"
    return wrapped

@makeBold
def test1():
    return "hello world-1"

@makeItalic
def test2():
    return "hello world-2"

@makeBold
@makeItalic
def test3():
    return "hello world-3"

print(test1())
print(test2())
print(test3())


运行结果:
<b>hello world-1</b>
<i>hello world-2</i>
<b><i>hello world-3</i></b>
```

#### 8.2.2 作用

```
引入日志
函数执行时间统计
执行函数前预备处理
执行函数后清理功能
权限校验等场景
缓存
```

#### 8.2.3 无参数的函数

```
from time import ctime, sleep

def timefun(func):
    def wrapped_func():
        print("%s called at %s" % (func.__name__, ctime()))
        func()
    return wrapped_func

@timefun
def foo():
    print("I am foo")

foo()
sleep(2)
foo()

上面代码理解装饰器执行行为可理解成：
foo = timefun(foo)
# foo先作为参数赋值给func后,foo接收指向timefun返回的wrapped_func
foo()
# 调用foo(),即等价调用wrapped_func()
# 内部函数wrapped_func被引用，所以外部函数的func变量(自由变量)并没有释放
# func里保存的是原foo函数对象
```



#### 8.2.4  被装饰的函数有参数

```
from time import ctime, sleep

def timefun(func):
    def wrapped_func(a, b):
        print("%s called at %s" % (func.__name__, ctime()))
        print(a, b)
        func(a, b)
    return wrapped_func

@timefun
def foo(a, b):
    print(a+b)

foo(3,5)
sleep(2)
foo(2,4)
```



#### 8.2.5 被装饰的函数有不定长参数

```
from time import ctime, sleep

def timefun(func):
    def wrapped_func(*args, **kwargs):
        print("%s called at %s"%(func.__name__, ctime()))
        func(*args, **kwargs)
    return wrapped_func

@timefun
def foo(a, b, c):
    print(a+b+c)

foo(3,5,7)
sleep(2)
foo(2,4,9)
```



#### 8.2.6 装饰器中的return

```
from time import ctime, sleep

def timefun(func):
    def wrapped_func():
        print("%s called at %s" % (func.__name__, ctime()))
        func()
    return wrapped_func

@timefun
def foo():
    print("I am foo")

@timefun
def getInfo():
    return '----hahah---'

foo()
sleep(2)
foo()


print(getInfo())

执行结果:
foo called at Fri Nov  4 21:55:35 2016
I am foo
foo called at Fri Nov  4 21:55:37 2016
I am foo
getInfo called at Fri Nov  4 21:55:37 2016
None


如果修改装饰器为return func()，则运行结果：
foo called at Fri Nov  4 21:55:57 2016
I am foo
foo called at Fri Nov  4 21:55:59 2016
I am foo
getInfo called at Fri Nov  4 21:55:59 2016
----hahah---
```



#### 8.2.7 设置外置变量

```
#decorator2.py

from time import ctime, sleep

def timefun_arg(pre="hello"):
    def timefun(func):
        def wrapped_func():
            print("%s called at %s %s" % (func.__name__, ctime(), pre))
            return func()
        return wrapped_func
    return timefun

# 下面的装饰过程
# 1. 调用timefun_arg("itcast")
# 2. 将步骤1得到的返回值，即time_fun返回， 然后time_fun(foo)
# 3. 将time_fun(foo)的结果返回，即wrapped_func
# 4. 让foo = wrapped_fun，即foo现在指向wrapped_func
@timefun_arg("itcast")
def foo():
    print("I am foo")

@timefun_arg("python")
def too():
    print("I am too")

foo()
sleep(2)
foo()

too()
sleep(2)
too()


可以理解为
foo()==timefun_arg("itcast")(foo)()
```



#### 8.2.8 类装饰器

```
装饰器函数其实是这样一个接口约束，它必须接受一个callable对象作为参数，然后返回一个callable对象。在Python中一般callable对象都是函数，但也有例外。只要某个对象重写了 __call__() 方法，那么这个对象就是callable的。

class Test():
    def __call__(self):
        print('call me!')

t = Test()
t()  # call me

类装饰器demo
class Test(object):
    def __init__(self, func):
        print("---初始化---")
        print("func name is %s"%func.__name__)
        self.__func = func
    def __call__(self):
        print("---装饰器中的功能---")
        self.__func()

#说明：
#1. 当用Test来装作装饰器对test函数进行装饰的时候，首先会创建Test的实例对象
#   并且会把test这个函数名当做参数传递到__init__方法中
#   即在__init__方法中的属性__func指向了test指向的函数
#
#2. test指向了用Test创建出来的实例对象
#
#3. 当在使用test()进行调用时，就相当于让这个对象()，因此会调用这个对象的__call__方法
#
#4. 为了能够在__call__方法中调用原来test指向的函数体，所以在__init__方法中就需要一个实例属性来保存这个函数体的引用
#   所以才有了self.__func = func这句代码，从而在调用__call__方法中能够调用到test之前的函数体
@Test
def test():
    print("----test---")
test()
showpy()#如果把这句话注释，重新运行程序，依然会看到"--初始化--"


运行结果如下：
---初始化---
func name is test
---装饰器中的功能---
----test---
```

