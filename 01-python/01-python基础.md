# 1.简介
人生苦短，我用 Python —— Life is short, you need Python

## 1.1 起源
1991年，吉多·范罗苏姆（Guido van Rossum） 

# 2.第一个Python 程序

```
print("hello python")
```


## 2.1 python开发环境的搭建
[python解释器](https://www.python.org/downloads/windows/)<br>
[pycharm](https://www.jetbrains.com/pycharm/download/#section=windows)


# 3.注释

```
单行注释  #    
多行注释 """ """
```



# 4.运算符
## 4.1 算数运算符

```

+	加	10 + 20 = 30
-	减	10 - 20 = -10
*	乘	10 * 20 = 200
/	除	10 / 20 = 0.5
//	取整除	返回除法的整数部分（商） 9 // 2 输出结果 4
%	取余数	返回除法的余数 9 % 2 = 1
**	幂	又称次方、乘方，2 ** 3 = 8

```

## 4.2 赋值运算符

```
=
    简单的赋值运算符
    c = a + b 将 a + b 的运算结果赋值为 c
+=
    加法赋值运算符
    c += a 等效于 c = c + a
-=
    减法赋值运算符
    c -= a 等效于 c = c - a
*=
    乘法赋值运算符
    c *= a 等效于 c = c * a
/=
    除法赋值运算符
    c /= a 等效于 c = c / a
//=
    取整除赋值运算符
    c //= a 等效于 c = c // a
%=
    取 模 (余数)赋值运算符
    c %= a 等效于 c = c % a
**=
    幂赋值运算符
    c **= a 等效于 c = c ** a
```


## 4.3 比较（关系）运算符

```
==
检查两个操作数的值是否 相等，如果是，则条件成立，返回 True

!=
检查两个操作数的值是否 不相等，如果是，则条件成立，返回 True

>
检查左操作数的值是否 大于 右操作数的值，如果是，则条件成立，返回 True

<
检查左操作数的值是否 小于 右操作数的值，如果是，则条件成立，返回 True

>=
检查左操作数的值是否 大于或等于 右操作数的值，如果是，则条件成立，返回 True

<=
检查左操作数的值是否 小于或等于 右操作数的值，如果是，则条件成立，返回 True

```


## 4.4 逻辑运算符

```
and
    x and y
    只有 x 和 y 的值都为 True，才会返回 True
    否则只要 x 或者 y 有一个值为 False，就返回 False
or
    x or y
    只要 x 或者 y 有一个值为 True，就返回 True
    只有 x 和 y 的值都为 False，才会返回 False
not
    not x
    如果 x 为 True，返回 False
    如果 x 为 False，返回 True


```


## 4.5 成员运算符

```
成员运算符用于 测试 序列中是否包含指定的 成员

in  如果在指定的序列中找到值返回 True，否则返回 False
    3 in (1, 2, 3) 返回 True
    
not in  如果在指定的序列中没有找到值返回 True，否则返回 False
    3 not in (1, 2, 3) 返回 False
```


# 5.变量

```
在 Python 中定义变量是 不需要指定类型

数据类型可以分为 数字型 和 非数字型
数字型 
    整型 (int)
    浮点型（float）
    布尔型（bool） 
        真 True 非 0 数 —— 非零即真
        假 False 0
    复数型 (complex)，主要用于科学计算

非数字型 
    字符串
    列表
    元组
    字典
```


## 5.1 变量的输入

```
print(x)
print("格式化字符串" % 变量1)
print("格式化字符串" % (变量1, 变量2...))

%s 
%d
%f 
%%


input("xxx：")
```


## 5.2 类型转换

```
int("1")
float("1")
```


## 5.3 变量的命名
### 5.3.1 标识符

```
标示符就是程序员定义的 变量名、函数名
名字 需要有 见名知义 的效果


由 字母、下划线 和 数字 组成
不能以数字开头
不能与关键字重名

```

### 5.3.2 关键字

```
就是在 Python 内部已经使用的标识符

```
### 5.3.3 变量命名规则

```
由 字母、下划线 和 数字 组成
不能以数字开头
不能与关键字重名

区分大小写的


eg:
first = "1111111"
first_name = "python"


驼峰命名法
当 变量名 是由二个或多个单词组成时，还可以利用驼峰命名法来命名
小驼峰式命名法 
第一个单词以小写字母开始，后续单词的首字母大写
例如：firstName、lastName


大驼峰式命名法 
每一个单词的首字母都采用大写字母
例如：FirstName、LastName、CamelCase


建议： 下划线链接

```

# 6. if
格式1： 

```
if 1 > 0:
    print("1111111111")
```

格式2： 

```
a = 20
b = 10 
if a > b:
    print("aaaaaaaaaa")
else:
    print("bbbbbbbbb")
```

格式3： 

```
a = 20
b = 10

if a > b :
    print("aaaaaaaaaaaaaa")
elif a == b:
    print("ccccccccccccc")
else:
    print("bbbbbbbbbbbbb")
    
```



# 7. while
## 7.1 代码示例

```
# 1. 定义重复次数计数器
i = 1

# 2. 使用 while 判断条件
while i <= 5:

    # 要重复执行的代码
    print("Hello Python")

    # 处理计数器 i
    i = i + 1

print("循环结束后的 i = %d" % i)

```

## 7.2 break, continue

```
break 某一条件满足时，退出循环，不再执行后续重复的代码
continue 某一条件满足时，不执行后续重复的代码
break 和 continue 只针对 当前所在循环 有效


i = 0
while i < 10:

    # break 某一条件满足时，退出循环，不再执行后续重复的代码
    # i == 3
    if i == 3:
        break

    print(i)

    i += 1

print("over")



i = 0
while i < 10:
    # 当 i == 7 时，不希望执行需要重复执行的代码
    if i == 7:
        # 在使用 continue 之前，同样应该修改计数器
        # 否则会出现死循环
        i += 1

        continue

    # 重复执行的代码
    print(i)

    i += 1
    
```
# 8. for


# 9. 函数

```
函数：就是把 具有独立功能的代码块组织为一个小模块，在需要的时候调用
作用：重用

# eg1:

def say_hello():
    """
    方法说明
    """
    print("好嗨哦")

say_hello()

# eg2---参数
def sum_2_num(num1, num2):

    result = num1 + num2
    
    print("%d + %d = %d" % (num1, num2, result))

sum_2_num(50, 20)

# eg3---返回值
def sum_2_num(num1, num2):
    """对两个数字的求和"""

    return num1 + num2

# 调用函数，并使用 result 变量接收计算结果
result = sum_2_num(10, 20)

print("计算结果是 %d" % result)



# eg4---缺省参数
def print_info(name, title="", gender=True):
    """

    :param title: 职位
    :param name: 班上同学的姓名
    :param gender: True 男生 False 女生
    """

    gender_text = "男生"

    if not gender:
        gender_text = "女生"

    print("%s%s 是 %s" % (title, name, gender_text))


print_info("小明")
print_info("老王", title="炊事班班长")
print_info("小美", gender=False)


# eg5---多值参数（待list,tuple,dict再讲）

引入：有时可能需要 一个函数 能够处理的参数 个数 是不确定的，这个时候，就可以使用 多值参数

python 中有 两种 多值参数： 
参数名前增加 一个 * 可以接收 元组
参数名前增加 两个 * 可以接收 字典


一般在给多值参数命名时，习惯使用以下两个名字：
*args —— 存放 元组 参数，前面有一个 *
**kwargs —— 存放 字典 参数，前面有两个 *

args 是 arguments 的缩写，有变量的含义
kw 是 keyword 的缩写，kwargs 可以记忆 键值对参数


def demo(num, *args, **kwargs):

    print(num)
    print(args)
    print(kwargs)


demo(1, 2, 3, 4, 5, name="小明", age=18, gender=True)

```

# 10. list,tuple, dict
## 10.1 list(列表)
```

# 定义
List（列表） 是 Python中使用最频繁的数据类型，在其他语言中通常叫做 数组，专门用于存储一串信息
列表用 [] 定义，数据 之间使用,分隔，列表的索引从0开始，可以存储不同类型的数据

# 常用方法
1 增加
    列表.insert(索引, 数据) 在指定位置插入数据
    列表.append(数据)  在末尾追加数据
    列表.extend(列表2)  将列表2 的数据追加到列表
2 修改
    列表[索引] = 数据 修改指定索引的数据
    
3 删除
    del 列表[索引]  删除指定索引的数据
    列表.remove[数据]  删除第一个出现的指定数据
    列表.pop  删除末尾数据
    列表.pop(索引)  删除指定索引数据
    列表.clear   清空列表
    
4 统计
    len(列表) 列表长度
    列表.count(数据)  数据在列表中出现的次数
5 排序
    列表.sort()  升序排序
    列表.sort(reverse=True)  降序排序
    列表.reverse()  逆序、反转
    

# 遍历
for name in name_list:
    print(name)


```

## 10.2 tuple(元祖)
```
# 定义
Tuple（元组）与列表类似，不同之处在于元组的 元素不能修改
用于存储 一串 信息，数据 之间使用 , 分隔
元组用 () 定义
元组的 索引 从 0 开始 

# 使用
创建空元组
info_tuple = ()

元组中 只包含一个元素 时，需要 在元素后面添加逗号
info_tuple = (50, )

# 常用操作及循环遍历
info.count  
info.index

tuple1 = (10,20,30)
for i in tuple1:
    print(i)
    
# 应用场景
函数的 参数 和 返回值，一个函数可以接收 任意多个参数，或者 一次返回多个数据

eg:
def add(num1,num2):

    temp1 = num1 + num2
    temp2 = num1 - num2
    
    return temp1,temp2




# 元组和列表之间的转换
使用 list 函数可以把元组转换成列表
list(元组) 

使用 tuple 函数可以把列表转换成元组
tuple(列表)

```

## 10.3 dict(字典)

```
# 定义
字典同样可以用来存储多个数据，通常用于存储 描述一个 物体 的相关信息 

字典和列表的区别：
列表 是 有序 的对象集合
字典 是 无序 的对象集合

字典用 {} 定义
字典使用 键值对 存储数据，键值对之间使用 , 分隔 
键 key 是索引
值 value 是数据
键 和 值 之间使用 : 分隔
键必须是唯一的
值 可以取任何数据类型，但 键 只能使用 字符串、数字或 元组

eg:

xiaoming = {"name": "小明",
            "age": 18,
            "gender": True,
            "height": 1.75}
            
# 常用操作
xiaoming.clear       xiaoming.items       xiaoming.setdefault
xiaoming.copy        xiaoming.keys        xiaoming.update
xiaoming.fromkeys    xiaoming.pop         xiaoming.values
xiaoming.get         xiaoming.popitem    

# 循环遍历
for k in xiaoming:
    print("%s: %s" % (k, xiaoming[k]))
    
# 应用场景
使用 多个键值对，存储描述一个物体的相关信息——描述更复杂的数据信息；

将 多个字典 放在一个列表中，再进行遍历，在循环体内部针对每一个字典进行 相同的处理

eg:
card_list = [{"name": "张三",
              "qq": "12345",
              "phone": "110"},
             {"name": "李四",
              "qq": "54321",
              "phone": "10086"}
             ]
             
```


# 11. 包和模块
## 11.1 模块

```
# 模块的概念
每一个以扩展名 py 结尾的 Python 源代码文件都是一个 模块，
模块 就好比是 工具包，要想使用这个工具包中的工具，就需要先 导入 这个模块

# 导入方式
import 模块名1
import 模块名2 

import 模块名1 as 模块别名

from 模块名1 import 工具名

```

## 11.2 包

```
# 概念
包 是一个 包含多个模块 的 特殊目录
目录下有一个 特殊的文件 __init__.py
包名的 命名方式 和变量名一致，小写字母 + _

utils
    __init__.py
    send_message.py
    receive_message.py
    

from utils import send_message, receive_message

```


# 12. 装饰器
## 12.1 应用场景

```
引入日志
函数执行时间统计
执行函数前预备处理
执行函数后清理功能
权限校验等场景
缓存

```

## 12.2 代码示例
```
eg1:
def w1(func):
    def inner():
        # 验证1
        # 验证2
        # 验证3
        func()
    return inner

@w1
def f1():
    print('f1')
    

eg2:
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

## 12.3 常见形式

```
# 例1:无参数的函数

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

```


```
#例2:被装饰的函数有参数
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

```
# 例3:被装饰的函数有不定长参数
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

```
# 例4:装饰器中的return
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
```



```
#例5: 装饰器带参数,在原有装饰器的基础上，设置外部变量
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
```



# 13. 异常

```
# 概念
程序在运行时，如果 Python 解释器 遇到 到一个错误，会停止程序的执行，并且提示一些错误信息，这就是 异常；

程序停止执行并且提示错误信息 这个动作，我们通常称之为：抛出(raise)异常

# 捕获异常
try:
    # 尝试执行的代码
    pass
except 错误类型1:
    # 针对错误类型1，对应的代码处理
    pass
except (错误类型2, 错误类型3):
    # 针对错误类型2 和 3，对应的代码处理
    pass
except Exception as result:
    print("未知错误 %s" % result)
    
else:
    # 没有异常才会执行的代码
    pass
    
finally:
    # 无论是否有异常，都会执行的代码
    print("无论是否有异常，都会执行的代码")
    
# 自定义异常
Python 中提供了一个 Exception 异常类，
在开发时，如果满足 特定业务需求时，希望 抛出异常，可以： 
创建 一个 Exception 的 对象
使用 raise 关键字 抛出 异常对象

eg:

def input_password():

    # 1. 提示用户输入密码
    pwd = input("请输入密码：")

    # 2. 判断密码长度，如果长度 >= 8，返回用户输入的密码
    if len(pwd) >= 8:
        return pwd

    # 3. 密码长度不够，需要抛出异常
    ex = Exception("密码长度不够")
    
    raise ex


try:
    user_pwd = input_password()
    print(user_pwd)
except Exception as result:
    print("发现错误：%s" % result)
    
    
```


# 14. 文件
## 14.1 常见方法
```
01
    open
    打开文件，并且返回文件操作对象
02
    read/readline
    默认会把文件的 所有内容 一次性读取到内存
    如果文件太大，对内存的占用会非常严重,
    
    readline 方法可以一次读取一行内容
03
    write
    将指定内容写入文件
04
    close
    关闭文件
```

## 14.2 打开文件的方式

```
语法如下：
f = open("文件名", "访问方式")

访问方式说明：
r
以只读方式打开文件。文件的指针将会放在文件的开头，这是默认模式。如果文件不存在，抛出异常

w
以只写方式打开文件。如果文件存在会被覆盖。如果文件不存在，创建新文件

a
以追加方式打开文件。如果该文件已存在，文件指针将会放在文件的结尾。如果文件不存在，创建新文件进行写入

r+
以读写方式打开文件。文件的指针将会放在文件的开头。如果文件不存在，抛出异常

w+
以读写方式打开文件。如果文件存在会被覆盖。如果文件不存在，创建新文件

a+
以读写方式打开文件。如果该文件已存在，文件指针将会放在文件的结尾。如果文件不存在，创建新文件进行写入

```

## 14.3 代码示例
```

# eg1:
# 1. 打开 - 文件名需要注意大小写
file = open("README.txt")

# 2. 读取
text = file.read()
print(text)

# 3. 关闭
file.close()


# eg2: 建议

with open("output.txt", "r") as f:
    f.write("从删库到跑路")

```




# 15. 面向对象
封装
继承
多态

## 15.1封装
```
内置方法 / 属性
01 __new__
    创建对象时，会被 自动 调用
02 __init__
    对象被初始化时，会被 自动 调用
03 __del__
    对象被从内存中销毁前，会被 自动 调用
04 __str__
    返回对象的描述信息，print 函数输出使用
    
    
class Cat:
    """这是一个猫类"""
    
    def __init__(self, name):
        print("初始化方法 %s" % name)
        self.name = name

    def eat(self):
        print("小猫爱吃鱼")

    def drink(self):
        print("小猫在喝水")

tom = Cat("Tom")
tom.drink()
tom.eat()

```


## 15.2继承

```
子类 继承自 父类，可以直接享受父类中已经封装好的方法
子类 中可以根据 职责，封装 子类特有的 属性和方法

继承的语法
class 类名(父类名):
    pass
    
```


## 15.3多态


```
多态 不同的 子类对象 调用相同的 父类方法，产生不同的执行结果

class Dog(object):

    def __init__(self, name):
        self.name = name

    def game(self):
        print("%s 蹦蹦跳跳的玩耍..." % self.name)


class XiaoTianDog(Dog):

    def game(self):
        print("%s 飞到天上去玩耍..." % self.name)


class Person(object):

    def __init__(self, name):
        self.name = name

    def game_with_dog(self, dog):

        print("%s 和 %s 快乐的玩耍..." % (self.name, dog.name))

        # 让狗玩耍
        dog.game()


# 1. 创建一个狗对象
# wangcai = Dog("旺财")
wangcai = XiaoTianDog("飞天旺财")

# 2. 创建一个小明对象
xiaoming = Person("小明")

# 3. 让小明调用和狗玩的方法
xiaoming.game_with_dog(wangcai)
```



