```
---------------------socket1_udp--------------------------------
1. 常用于广播
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

----------------socket2_tcp----------------
socket是同时可以收发数据的
单工
半双工
全双工  socket

vi    +10

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

扩展：访问一个网址的过程



------------------多任务1_线程----------------
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

8.多线程udp聊天

-----------------多任务2_进程----------------
1.进程的状态：
新建---就绪---运行---死亡
	   等待（阻塞）

2.进程的创建：
vi快速注释：V  :  normal i #

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

6.文件拷贝

------------------多任务3_协程--------------------
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

----------------------------------正则表达式----------------------------
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

4.练习：提取url,html中的文本(分组)

案例：TODO

----------------------------------http协议，http服务器1----------------------------------
1.chrome调试器(F12),firefox(ctrl+shift+i)使用
network:
element：

右键选项分析

2.http协议了解
请求：请求头，请求体
响应：响应头（响应行），响应体

3。
3次握手：syn11 + syn33 /ack12 + ack34

4次挥手：
客户端不再发送（关闭发）：client_socket.close()
服务端（关闭收）：ok() 确认数据
服务端不再发送（关闭发）：new_socket.close()
客户端（关闭收）：ok


最长等待时间 2msl（2-5min）
端口占用问题的解决：(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

0 
<h1>
内容编码
链接进度  new_socket.close()两次（子进程中复制了一份父类的）


-----http协议，http服务器2-------------
http基于socket中的tcp
1.多进程服务器
2.多线程服务器 bad file descriptor  new_socket.close()搞得鬼
3.gevent服务器
4.单线程非阻塞
python3建议将tab键换成4个空格
server_socket.recv()  #不传参出问题，没有默认值

5.epoll服务器
内存映射
事件通知

epoll(解决了个数，轮询问题:"select/poll(轮询))


----------网络通信过程(d11)--------
抓包:  面试前todo
网络协议：网络接口层(物理层，链路层,mac地址)，网际层(ip,arp,)，传输层（tcp,udp（端口）），应用层（应用层，表示层，回话层）
osi:应用层，表示层，回话层，传输层，网络层，数据链路层，物理层
网络号+主机号

arp -a
arp -d  删除项，可达到删除流量限制

访问一个网络的过程：面试前todo
1.输入域名，默认网关（router mac地址），dns服务器解析域名
2.tcp的三次握手
3.发送数据包，服务端解析数据包
4.tcp的4次挥手

nat转换


---------------------python提高1------------------
1.GIL(全局解释器锁)
多线程gil问题：python解释器（cpython,jpython没有这个问题）的问题
io密集（文件读写，线程，协程（gevent单线程，将等待时间利用来做其他事情））/计算密集（继承）

method1:jpython解释器
method2：
c语言解决gil问题:
生成so库文件：gcc xxx.c -shared -o libxxx.so

from ctypes import *
lib = cdll.loadLibraty("./libdead_loop.so")

胶水语言：如何调其他的语言？？？

2.深拷贝，浅拷贝 (todo)
import copy
c = copy.deepcopy(a)
id 不同，内容独立
c = copy.copy(a)/ c = a（id相同）

情况一：包含list,dic
a = [11,22]
b = [33,44]
c = [a,b]

e = copy.copy(c)
e,c id 不同，id(e[0]),id(c[0])相同，说明创建了一份新的（将a,b拷贝出来）

e中存的是之前c指向的a，b的引用

情况二：
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

3.私有化
_x:私有化属性或方法，不能被其他包导入
__xx:避免与子类的属性命名冲突，无法在外部访问
__xx__:魔法对象或属性（例如：__init__）
xx_:避免与python关键字的冲突

4.import
import sys
sys.path

ipython   #import才能用
from imp import reload
reload(aa) 

help(reload) 

导常量的时候注意用import common ，不要用 from common import *


-------------------python提高2------------------
1.多继承，mro顺序
python没有重载
用super()不用类名（导致父类调多次）

tips:super(grason,self).__init__()

print(parent.__mro__)  #调用的先后顺序
c3算法

2.args,kwargs的拆包

3.类对象，实例对象；类属性，实例属性；静态方法(staticMethod)，实例方法，类方法(classMethod)
@classMethod
def cls_fun(cls):
	pass
	
@staticMethod
def static_func():
	pass
	
实例对象.__class__


4.property
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
2.在类中定义值为property对象的类属性

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

5.魔法属性（了解）
__doc__；表示类的描述信息
__module__ （表示当前操作的对象在那个模块）和 __class__（表示当前操作的对象的类是什么）：
__dict__：类或对象中的所有属性（可看到私有属性）
__call__:对象后面的括号执行 ，调用
__getitem__、__setitem__、__delitem__：用于索引操作，如字典。以上分别表示获取、设置、删除数据
__getslice__、__setslice__、__delslice__：该三个方法用于分片操作，如：列表


6.with，上下文管理器：
6.1任何实现了 __enter__() 和 __exit__() 方法的对象都可称之为上下文管理器
6.2另外方式：
from contextlib import contextmanager

@contextmanager
def my_open(path, mode):
    f = open(path, mode)
    yield f
    f.close()
	
通过 yield 将函数分割成两部分，yield 之前的语句在 __enter__ 方法中执行，yield 之后的语句在 __exit__ 方法中执行。
紧跟在 yield 后面的值是函数的返回值

--------------mysql_1------------
1.navicat/命令行
sudo -s 切换达到root/su 
关系型数据库：
列---字段
行---记录
表
库

主键（唯一），外键（当前键是另外一张表的主键）
不区分大小写

sudo apt-get install mysql-server/mysql-client
sudo apt-get search mysql

与python 交互：pip install pymysql /import pymysql 

2.安装
sudo apt-get install mysql

查询：
ps -aux | grep "mysql"

启动
sudo service mysql start
开机启动
sudo /etc/init.d/mysql restart 

停止
sudo service mysql stop
重启
sudo service mysql restart

配置：
mysql/mysql.cnf.d/   vi mysqld.cnf port等相关信息
mysql/conf.d/   

navicat安装：
删除 .navicat64 
  
wine Mono：运行windows的软件

3.数据类型，约束
数据类型：
int,bit(0,1实现类似boolean效果)
decimal(5,2)
varchar,char,text
date,time,datetime,year,timestamp
enum()  #可插入数字来区分，从1开始

TINYINT   1  -128-127(有符号） 0-256（无符号）
SMALLLINT 2  0-65535
MEDIUMINT 3  
INT       4
BIGINT    8

约束：
primary key 
not null
unique
foreign key(会降低数据库性能，最好在逻辑层控制)
default :


对于图片，视频等，在数据库中存路径，将图片上传到文件服务器

4.命令行：

mysql -u root -p
quit/exit

数据库：
show databases;
use xxx  /select database()

create database xxx charset=utf8   
(show create database xxx 查看创建数据库编码类型)
drop database xxx   #删不掉的注意使用``（tab键上面的）


数据表：
show tables;
desc user ; #查看表结构
select * from xxx;

create table user(id int unsigned primary key not null auto_increment,name varchar(20),age int default 0 );

insert into user values(0,"laowang",18)
alter table user add/change（原名 新名）/modidy  字段 类型；

补充：change 多个字段
alter table goods  
change cate_name cate_id int unsigned not null,
change brand_name brand_id int unsigned not null;

alter table user drop birth;


select * from user;
drop table user

表记录crud:
insert into user values(0/null/default,...)  
insert into user(age,name) values()   
insert into user(age,name) values(),()#多行插入

update user set age=19,name="xx" where id = 2;

delete from user where id = 9;

select * from xxx;
select id,name from xxx;
select * from xxx where id = 9;
select name as 姓名 from user where ....;

去除重复：distinct()

直接在控制台
备份：
mysqldump -uroot -p xxx > python.sql

还原：
mysql -uroot -p xxx < python.sql

导入：
先得建表,同时use该表，最后source xxx.sql

物理删除：
逻辑删除：update/alter  bit  

tips:
(linux)
edit  (vi 下写多个数据库语句)
;

---------------mysql_2-------------
1.条件查询
比较查询：
>,< ,=,!=

逻辑运算：
and ,or (不建议使用),not

模糊查询：(效率较低)
like(%（一个或多个）   _(一个) )
rlike(正则表达式)

范围查询：
in（不建议使用）
not in 
between...and...(闭区间)
not between...and...

空判断：
is null
is not null

2.排序：
order...by...(asc升序，desc(降序))

exm: order by height desc ,id desc(多个字段)

3.聚合函数
sum()
count()  exm: select count(*) from students where gender = 1;
max()
min()
avg()
round()  exm:round(123.23,1)  #四舍五入

4.分组(通常和聚合一起用)
group by 
group_concat()
having

5.分页
limit m (个数)/limit m,n  # m: 起始下标，n：个数

6.连接查询：多个表交集查询
inner join ...on
exm : select * from students inner join classes on students.cls_id = class.id
select student.* ,class.name from ...


left join(左连接)：(以左边的为基准，找不到的显示null)
right join（右连接） 

7.自关联
案例：省级联动
method1:表1：所有的省；表2： 所有的市；表三：所有的区
method2:一张表中不同的p_id :

导入数据库：
source area.sql

select * from area as province inner join areas as city on city.pid = province.aid having province.atitle = "山东省" limit 15;

8.子查询
select * from students where height = (select max(height) from students)

列级子查询：select name from classes where id in (select cls_id from students);
行级子查询：select * from students where (height,age) = (select max(height),max(age) from students);
in：主查询 where 条件 in (列子查询)

数据库设计软件：powerdesign

9.数据库设计（了解）：
三范式：
E-R模型：

一对一：
多对一：多里添加外键
多对多：需要第三张表（聚合表）


10.总结：
完整的select语句：

select distinct *
from 表名
where ....
group by ... having ...
order by ...
limit start,count


--------------mysql_3-----------
1.创建商品分类表(todo)  
写入数据到新表(没有value)： insert into goods_cates(name) select cate_name from goods group by cate_name;
同步数据（update ...(条件) set xxx = yyy）：update goods as g inner join goods_cates as c on g.cate_name=c.name set g.cate_name=c.id;

mysql 开发文档
表的最小长度 6个字段

2.创建商品品牌表（create ...select...有bug （auto_increment混乱，重启mysql restart 解决）,不建议使用）
2.1 create table goods_brands (
    id int unsigned primary key auto_increment,
    name varchar(40) not null) select brand_name as name from goods group by brand_name;


2.2 修改表结构：（多个change）
alter table goods  
change cate_name cate_id int unsigned not null,
change brand_name brand_id int unsigned not null;

2.3 外键：(问题：不加能同步数据么？)
alter table goods add foreign key (cate_id) references goods_cates(id)

2.4 创建数据表的时候就设置外键约束
create table goods(
    id int primary key auto_increment not null,
    name varchar(40) default '',
    price decimal(5,2),
    cate_id int unsigned,
    brand_id int unsigned,
    is_show bit default 1,
    is_saleoff bit default 0,
    foreign key(cate_id) references goods_cates(id),
    foreign key(brand_id) references goods_brands(id)
);

然后再去插入数据


2.5 取消外键约束
show create table goods; （可看到外键名称）
alter table goods drop foreign key 外键名称（？？？外键名称需要用（）包围）;

2.6 总结：
在实际开发中,很少会使用到外键约束,会极大的降低表更新的效率(每次插入都需要查询)

3.订单表(在创建表的时候插入外键)
4.顾客表
5.订单详情表


6.python和mysql的交互

6.2 pip3 install pymysql(pip install xx.whl)
导包解决办法：pycharm 的问题

Pymysql 默认开启事务
#可增加属性autocommit = false或者conn.autocommit = false
#查看是否是自动提交 conn.get_autocommit() 

#代码中切换数据库  connect.select_db("")
#query()


#游标：cursor.excutemany(插入数据要快)

conn = connect(host="localhost",port =3306,database= "jing_dong",user="root",password="123",charset="utf8")
cls = conn.cursor()

cls.excute()

#查询
cls.fetchall()
cls.fetchone()


#增删改
conn.commit()

cls.close()
conn.close()

6.3防止sql注入
param = []
conn.excute("select * from goods where name = %s",param)

注意：
1.除了主键外的其他字段默认值不能是0，null,只能是default
2.Pymysql 默认开启事务
commit()
rollback()

3."{0} {1}".format(("danier"),("h"))


自接创建带外键的表：
注册：
登录：
下订单：

--------------mysql_4---------------
1.视图（不用,类似python解释器，在sql语句和数据库之间隔了一层，虚拟表）
创建:
create view v_goods_info as select ...
查看：
select * from v_goods_info
删除：
drop view v_goods_info

2.事务
四大特性：（acid）
原子性(不可再分割，要么成功，要么失败);文件操作（a+）
一致性（结果是一致的，有增有减）
隔离性（一个事务在最终提交前，对其他事务是不可见的）
持久性（是持久化存储的）

start transaction/begin;
...
rollback;
commit;


3.索引（大量的查询，树形结构）
显示索引名：
show index from test_index;
创建索引：
create index title_index on 表名(字段（长度）)
删除索引：
drop index title_index on 表名


未开启索引性能检测：
set profiling =1;
select * from xxx where id =99999;
show profiles;

开启索引性能检测：
create index title_index on xxx


注意：
建立太多的索引将会影响更新和插入的速度，因为它需要同样更新每个索引文件
占用磁盘空间

4.账户管理
#权限：create、alter、drop、insert、update、delete、select、all privileges
#创建用户，设置密码，权限
grant select on jing_dong.* to 'laowang'@'localhost' identified by '123456'

#新用户登录
mysql -ulaowang -p

#修改密码
update user set authentication_string = password[''] where user = "laowang"
flush privileges

#修改权限
grand 新权限 on jing_dong.* to 'laowang'@'localhost' with grand option
flush privileges;

#删除用户
method1:
drop user 'laowang@%'

method2:
delete from user where user='用户名';
flush privileges

#远程连接：
修改mysql.cnf ,注释掉bind-address
mysql -uxxx -pxxx -h+ip

查看所有用户：
select host,user,authentication_string from user;

查看用户有哪些权限：
show grants for laowang@localhost;

root密码忘记重置

5.主从配置(提高性能：主服务器生成数据，从服务器上分析；)
数据备份
读写分离
负载均衡
redis

步骤：
1.主备份：
直接在root
(mysqldump -uroot -p123 jing_dong > jd.sql)
mysqldump -uroot -p123 --all-databases --lock-all-tables >jd.sql

2.从恢复：
mysql -uroot -p123 < jd.sql

3.设定主 id,日志文件,
sudo vim /etc/mysql/mysql.conf/mysqld.cnf

#下面保证不注释
server-id =1 
log-bin 

service mysql start

4.从 id
server-id =2 (一般用ip)

service mysql start

5.同步

主服务器（mysql）
GRANT REPLICATION SLAVE ON *.* TO 'slave'@'%' identified by 'slave';
FLUSH PRIVILEGES;

主服务器(mysql)
SHOW MASTER STATUS;
从服务器：
change master to master_host='192.168.11.150', master_user='slave', master_password='slave',master_log_file='mysql-bin.000005', master_log_pos=590;


查看：
start slave;
show slave status;

show master stutus;

注意：连接网线


---------------mini_web1-------------
1.wsgi协议(服务器和web框架直接解耦的协议)
vim  /mai  n向下找，N向上找
vim  %s///g
ctrl +R 强制刷新

---------------mini_web2------------
1.闭包
全局变量
nonlocal x (python3；python2有cluse...)  

2.装饰器
多个装饰器装的过程：从下至上； 程序执行的过程：从上至下
作为拦截器（intercepter） ???

类装饰器可以传参（在方法__call__(self,param)）


字符串替换：
"我的名字是：{0}；我的姓名是：{1}".format("daniel","18")

sorted()排序：

导入数据库，先要use，在source xxx.sql


---------------mini_web4------------
1.logging
1.1写入到文件
logging.basicConfig(level=logging.INFO,  
                        filename='./log.txt',  
                        filemode='a',  
                        format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')  
						

logging.basicConfig(level = logging.INFO)
logging.info("访问的是，%s" % file_name)
logging.warning()


1.2既写入到文件中，又输出到终端
import logging  

# 第一步，创建一个logger  
logger = logging.getLogger()  
logger.setLevel(logging.INFO)  # Log等级总开关  

# 第二步，创建一个handler，用于写入日志文件  
logfile = './log.txt'  
fh = logging.FileHandler(logfile, mode='a')  # open的打开模式这里可以进行参考
fh.setLevel(logging.DEBUG)  # 输出到file的log等级的开关  

# 第三步，再创建一个handler，用于输出到控制台  
ch = logging.StreamHandler()  
ch.setLevel(logging.WARNING)   # 输出到console的log等级的开关  

# 第四步，定义handler的输出格式  
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")  
fh.setFormatter(formatter)  
ch.setFormatter(formatter)  

# 第五步，将logger添加到handler里面  
logger.addHandler(fh)  
logger.addHandler(ch)  

# 日志  
logger.debug('这是 logger debug message')  
logger.info('这是 logger info message')  
logger.warning('这是 logger warning message')  
logger.error('这是 logger error message')  
logger.critical('这是 logger critical message')

2.测试api
3.urllib.parse.unquote("")
```

