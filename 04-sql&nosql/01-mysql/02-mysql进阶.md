## 文档
```
https://www.mysqlzh.com/
https://www.mysql.com/cn/
https://dev.mysql.com/doc/refman/5.7/en/
```

## 1. 单表查询

> select [选项] 列名 [from 表名] [where 条件]  [group by 分组] [order by 排序] [having 条件] [limit 限制]
> set names gbk;     #  更改编码

### 1.1 E-R 图
```
方框--- 实体
圆框--- 属性
菱形--- 关系
```

### 1.2 聚合函数

> https://www.cnblogs.com/bigbigbigo/p/10952895.html
>
> https://dev.mysql.com/doc/refman/5.7/en/    左侧有专题

```
sum()
avg()
min()
max()
count()
```

### 1.3 通配符 & 模糊查询
```
_  :  表示任意一个字符
%  :  表示任意字符
^  :  以什么开头
$  ： 以什么结尾

e.g:
    1、满足“T_m”的有（A、C）
        A：Tom         B：Toom       C：Tam         D：Tm     E：Tmo
    
    2、满足“T_m_”的有（B、C  ）
        A:Tmom   B:Tmmm  C:T1m2    D:Tmm     E:Tm
    
    3、满足“张%”的是（A、B、C、D）
        A:张三     B：张三丰     C：张牙舞爪      D：张      E：小张
    
    4、满足“%诺基亚%”的是（A、B、C、D）
        A：诺基亚2100   B：2100诺基亚   C：把我的诺基亚拿过来   D：诺基亚
         
e.g:
    select * from stu where stuname like '张%';
    
    select * from stu where stuname like 'T_m';
```


### 1.4 group by  
```
# 按性别分组，显示每组的平均年龄
 select avg(stuage) as '年龄',stusex from stu group by stusex;

# 通过group_concat()函数将同一组的值连接起来显示
select group_concat(stuname), stusex from stu group by stusex;


# 多列分组
select stuaddress,stusex,avg(stuage) from stu group by stuaddress,stusex;

tips:
    1、分组后的结果默认会按升序排列显示
    2、也是可以使用desc实现分组后的降序
```

### 1.5 having
```
select * from stu where stusex='男';    # 从数据库中查找
select * from stu having stusex='男';   # 从结果集中查找

# error 数据库中没有total
select  stusex , count(*) total from stu group by stusex  where total > 5
# ok    前面的结果机中有total
select  stusex , count(*) total from stu group by stusex  having total > 5  

having和where的区别：
where是对原始数据进行筛选，having是对结果集进行筛选。 
```

### 1.6 order by

```

```



### 1.7 limit

```
limit  起始位置 显示长度        # 起始位置可以省略，默认是从0开始
```

### 1.8 选项
```
all：显示所有数据 【默认】
distinct：去除结果集中重复的数据

select distinct stuaddress from stu;
```






## 2. 多表查询
### 2.1 内连接
```
inner join

语法一：select 列名 from 表1 inner join 表2 on 表1.公共字段 = 表2.公共字段
语法二：select 列名 from 表1, 表2  where 表1.公共字段 = 表2.公共字段

e.g:
    select stuname, stusex, writtenexam, labexam from stuinfo inner join stumarks on stuinfo.stuno = stumarks.stuno;
    

脚下留心：显示公共字段需要指定表名 

多学一招：三个表的内连接如何实现？
    select * from 表1 inner join 表2 on 表1.公共字段=表2.公共字段 inner join 表3 on 表2.公共字段=表3.公共字段
```

### 2.2 外连接
```
left join（以左边的表为标准，如果右边的表没有对应的记录，用NULL填充。）
    
 select stuname,writtenexam, labexam from stuinfo left join stumarks on stuinfo.stuno=stumarks.stuno;
    +----------+-------------+---------+
    | stuname  | writtenexam | labexam |
    +----------+-------------+---------+
    | 张秋丽        |          77 |      82 |
    | 李文才        |          50 |      90 |
    | 李斯文        |          80 |      58 |
    | 欧阳俊雄      |          65 |      50 |
    | 诸葛丽丽      |        NULL |    NULL |
    | 争青小子      |          56 |      48 |
    | 梅超风        |        NULL |    NULL |
    +----------+-------------+---------+
    
right join: 
    
    
full  join: 使用 UNION 可以间接实现 full JOIN 功能
```

### 2.3 交叉连接
```
cross join

1、如果没有连接表达式返回的是笛卡尔积
    select * from t1 cross join t2;       # 返回笛卡尔积
    
    +------+-------+------+-------+
    | id   | name  | id   | score |
    +------+-------+------+-------+
    |    1 | tom   |    1 |    88 |
    |    2 | berry |    1 |    88 |
    |    1 | tom   |    2 |    99 |
    |    2 | berry |    2 |    99 |
    +------+-------+------+-------+
    
2、如果有连接表达式等价于内连接
     select * from t1 cross join t2 where t1.id = t2.id;
     
    +------+-------+------+-------+
    | id   | name  | id   | score |
    +------+-------+------+-------+
    |    1 | tom   |    1 |    88 |
    |    2 | berry |    2 |    99 |
    +------+-------+------+-------+
    
```

### 2.4 自然连接
```
简化外连接的写法，通过同名字段来判断
e.g:
    # 自然内连接
        select * from stuinfo natural join stumarks;
        
    # 自然左外连接
        select * from stuinfo natural left join stumarks;

    # 自然右外连接
        select * from stuinfo natural right join stumarks;
        
自然连接结论：
1. 表连接通过同名的字段来连接的
2. 如果没有同名的字段返回笛卡尔积
3. 会对结果进行整理，整理的规则如下
   a)	连接字段保留一个
   b)	连接字段放在最前面
   c)   左外连接左边在前，右外连接右表在前
```



### 2.5 using

```
1. 用来指定连接字段。(解决多个同名字段)
2. using()也会对连接字段进行整理，整理方式和自然连接是一样的。
select * from stuinfo inner join stumarks using(stuno);   # using指定字段
```



### 2.6  union(联合查询, 合并查询)
```
将多个select语句结果集纵向联合起来
	select stuno,stuname from stu   union   select id, name from Go1;

e.g: 查询上海的男生和北京的女生
    select stuname,stuaddress,stusex from stu where (stuaddress='上海' and stusex='男') or (stuaddress='北京' and stusex='女');
 
     select stuname,stuaddress,stusex from stu where stuaddress='上海' and stusex='男' union select stuname,stuaddress,stusex from stu where stuaddress='北京' and stusex='女';
    
union的选项: 
    all：     显示所有数据, 不去重
    distinct：去除重复的数据【默认】, 不写就是去重
    
union的注意事项：
    1、union两边的select语句的字段个数必须一致 
    2、union两边的select语句的字段名可以不一致，最终按第一个select语句的字段名。
    3、union两边的select语句中的数据类型可以不一致。
```

### 2.7 子查询

```
select 语句 where 条件 (select … from 表)

e.g.1： 查找笔试80分的学生
    select * from stuinfo where stuno = (select stuno from stumarks where writtenexam=80);

e.g.2:  查找笔试最高分的学生
    select * from stuinfo where stuno=(select stuno from stumarks order by writtenexam desc limit
    
    select * from stuinfo where stuno=(select stuno from stumarks where writtenexam=(select max(writtenexam) from stumarks));
    
    脚下留心：上面的例题，子查询只能返回一个值。如果子查询返回多个值就不能用"="了,需要用 in
    
    
in | not in子查询: 用于子查询的返回结果多个值。
    e.g.1: 查找笔试成绩及格的同学
        select * from stuinfo where stuno in (select stuno from stumarks where writtenexam>=60);
        
    e.g.2: 查询不及格的同学
         select * from stuinfo where stuno  in (select stuno from stumarks where writtenexam<=60);
         
    e.g.3: 查询没有通过的同学（不及格，缺考）
        select * from stuinfo where stuno not in (select stuno from stumarks where writtenexam>=60);
    
exists 和 not exists : 
    e.g.1:  如果有人笔试超过80分就显示所有的学生
        select * from stuinfo where exists (select * from stumarks where writtenexam>=80);
        
    e.g.2:  如果没有人超过80分就显示所有的学生
        select * from stuinfo where not exists (select * from stumarks where writtenexam>=80);
    
    
分类：
    1、标量子查询：子查询返回的结果就一个
    2、列子查询：  子查询返回的结果是一个列表
    3、行子查询：  子查询返回的结果是一行
    4、表子查询：  子查询返回的结果当成一个表， 子查询临时表
    
    e.g.1: 查询成绩最高的男生和女生
        select stuname,stusex,ch from stu where (stusex,ch) in (select stusex,max(ch) from stu group by stusex);
        
    e.g.2: 查询成绩最高的男生和女生
        select stuname,stusex,ch from (select * from stu order by ch desc) as t group by stusex;
        
    脚下留心：from后面是一个表，如果子查询的结果当成表来看，必须将子查询的结果取别名。
    
```



## 3. 内置函数&预处理&存储过程

### 3.1 内置函数(***)

> https://dev.mysql.com/doc/refman/5.7/en/built-in-function-reference.html

```
# 数字类
    select rand();			                         # 生成随机数   0~1
    
    select rand(seed);                                # 生成随机数   0~1, 如果seed不变，随机数也不变
    
    select * from stuinfo order by rand() limit 2;    # 随机抽两个学生
    
    select round(3.5);    # 四舍五入
    
    select ceil(3.1);	  # 向上取整
    
    select floor(3.9);	  # 向下取整
    
    select truncate(3.1415926,3);	# 截取数字
    
    abs()
    bin()
    hex()
    format()        # 指定格式输出
    mod()		   # 取余
    conv()          # 进制转换
    
   
# 字符串类
    select ucase('i am a boy!');		# 转成大写
    
    select lcase('I Am A Boy!');		# 转成小写
    
    select left('abcde',3);		        # 从左边开始截取，截取3个
    
    select right('abcde',3);		    # 从右边开始截取，截取3个
    
    select substring('abcde',2,3);	    # 从第2个位置开始截取，截取3个【位置从1开始】
    
    select concat('中国','上海');	     # 字符串相连
    
    select concat(stuname,'-',stusex) from stuinfo;  # 将表中的姓名和性别连接起来

    select stuname, coalesce(writtenexam,'缺考'),coalesce(labexam,'缺考') from stuinfo natural left join stumarks;                   # coalesce(字段1，字段2)  如果字段1不为空就显示字段1，否则，显示字段2
    
    
    select length('锄禾日当午');		        # 字节长度
    
    select char_length('锄禾日当午');		# 字符个数
    
    charset(string)
    instr(string, substring)
    replace()
    strcmp()
    ltrim()
    
# 时间类
	select current_date()
	select current_time()
	select current_timestamp()
     select unix_timestamp();				   # 获取时间戳
     select from_unixtime(unix_timestamp());	# 将时间戳转成年-月-日 小时:分钟:秒的格式
     select now();		                        # 获取当前日期时间
     select timediff();
     select year(now()) 年, month(now()) 月, day(now()) 日, hour(now()) 小, minute(now()) 分钟, second(now()) 秒;
     
     select dayname(now()) 星期, monthname(now()), dayofyear(now())  本年的第几天;
     
     select date()
     select date_add()
   	 select date_sub()
     select datediff(now(),'2008-8-8');	                # 日期相减
     
     select convert(now(), date),convert(now(),time);	# 将now()转成日期和时间
     
     select cast(now() as date),cast(now() as time);    # 将now()转成日期和时间
     

#  加密函数
    select user() from xxx;   # 可以查询登录的用户及Ip
    select database(); 
    
    select md5("xxxx")
    password(xxx) 
    // select * from mysql.user \G;
    
# 判断函数
     select if(10%2=0,'偶数','奇数');
     select ifnull(expr1, expr2)
     select case when expr1 then expr2 when expr3 then expr4 else expr5 end;
     
     select stuname,ch,math, if(ch>=60 && math>=60,'通过','不通过') '是否通过' from stu;
```



### 3.2 预处理(***)

```
预处理：预编译一次，可以多次执行。用来解决一条SQL语句频繁执行的问题。

sql执行过程：
    词法分析
    语法分析
    编译执行

用预处理后，先词法分析，语法分析，后直接编译执行

预处理语句：prepare 预处理名字 from 'sql语句'
执行预处理：execute 预处理名字 [using 变量]

e.g1:
    prepare stmt from 'select * from stuinfo';	# 创建预处理
    execute stmt;	                            # 执行预处理
    
    
e.g2: 传递参数
     delimiter // 
     prepare stmt from 'select * from stuinfo where stuno=?'   -- ?是位置占位符
     
     set @id='s25301';            -- 变量以@开头，通过set给变量赋值
     execute stmt using @id  //   -- 执行预处理，传递参数
    
e.g3: 传递多个参数
    prepare stmt from 'select * from stuinfo where stusex=? and stuaddress=?'
    
    set @sex='男';
    set @addr='北京';
    execute stmt using @sex, @addr  //
```



### 3.3 变量

#### 系统变量

一、全局变量

作用域：针对于所有会话（连接）有效，但不能跨重启

	查看所有全局变量
	SHOW GLOBAL VARIABLES;
	
	查看满足条件的部分系统变量, 比如  character 相关的
	SHOW GLOBAL VARIABLES LIKE '%char%';
	
	查看指定的系统变量的值
	SELECT @@global.autocommit;
	
	为某个系统变量赋值
	SET @@global.autocommit=0;
	SET GLOBAL autocommit=0;

二、会话变量

作用域：针对于当前会话（连接）有效

	查看所有会话变量
	SHOW SESSION VARIABLES;
	
	查看满足条件的部分会话变量
	SHOW SESSION VARIABLES LIKE '%char%';
	
	查看指定的会话变量的值
	SELECT @@autocommit;
	SELECT @@session.tx_isolation;
	
	为某个会话变量赋值
	SET @@session.tx_isolation='read-uncommitted';
	SET SESSION tx_isolation='read-committed';



####自定义变量

一、用户变量

声明并初始化：

	SET @变量名=值;
	SET @变量名:=值;
	SELECT @变量名:=值;

赋值：

	方式一：一般用于赋简单的值
	SET 变量名=值;
	SET 变量名:=值;
	SELECT 变量名:=值;
	
	方式二：一般用于赋表中的字段值          ***
	SELECT 字段名或表达式 INTO 变量
	FROM 表;



使用：

	select @变量名;



二、局部变量

声明并初始化：

	declare  变量名 类型 【default 值】;

赋值：

	方式一：一般用于赋简单的值
	SET 变量名=值;
	SET 变量名:=值;
	SELECT 变量名:=值;


	方式二：一般用于赋表 中的字段值          ***
	SELECT 字段名或表达式 INTO 变量
	FROM 表;

使用：

	select 变量名



二者的区别：

```
作用域			定义位置							  语法

用户变量	当前会话，会话的任何地方					加@符号，不用指定类型
局部变量	定义它的BEGIN END中， BEGIN END的第一句话	   一般不用加@,需要指定类型
```



### 3.4 存储过程(***)

```
优点:
    1. 存储过程可以减少网络流量
    2. 允许模块化设计，支持复用
    3. 支持事务


# 语法：
    create procedure 存储过程名(参数)
    begin
    	sql语句;
    end
    
    脚下留心：由于过程中有很多SQL语句，每个语句的结束都要用（;）结束。默认情况下，分号既表示语句结束，又表示向服务器发送SQL语句。我们希望分号仅表示语句的结束，不要将SQL语句发送到服务器执行，通过delimiter来更改结束符（delimiter 声明一次就行）。如果只有一条语句，begin, end 可以省略

    e.g.：
        mysql> delimiter //
        mysql> create procedure proc()     -- 创建存储过程
            -> begin
            -> select * from stuinfo;
            -> end //
        Query OK, 0 rows affected (0.00 sec)
    
    

# 调用
    call 存储过程名()
    
    e.g.:
        call proc() 
        
   
# 删除存储过程
    drop procedure [if exists] 存储过程名;
    
    e.g:
         drop procedure proc;
         
# 查看存储过程的信息
    show create procedure 存储过程名 \G;
    
    e.g.:
        show create procedure proc \G; 
        
    注意： 存储过程名没有括号
        
# 显示所有的存储过程
     show procedure status \G;
     
# 存储过程的参数
    存储过程的参数分为：输入参数（in）【默认】，输出参数（out），输入输出参数（inout）
    存储过程不能使用return返回值，要返回值只能通过'输出参数'来向外传递值。
    
    e.g.1: 传递学号，获取对应的信息
        -> create procedure proc(in param varchar(10))   -- 输入参数
        -> select * from stuinfo where stuno=param
        
        
    e.g.2: 查找同桌
        create procedure proc(name varchar(10))
        -> begin
        -> declare seat tinyint;   -- 声明局部变量
        -> select stuseat into seat from stuinfo where stuname=name;      -- 将座位号保存到变量中
        -> select * from stuinfo where stuseat=seat+1 or stuseat=seat-1;  -- 查找同桌
        -> end //
        
        call proc('李文才') //
        
        
        强调：  
            1、通过declare关键字声明局部变量；全局变量@开头就可以了
            2、给变量赋值有两种方法
            	方法一：set 变量名=值
            	方法二：select 字段 into 变量 from 表 where 条件
            3、声明的变量不能与列名同名
            
        
    e.g.3:  输出参数
        create procedure proc(num int, out result int)  -- out 表示输出参数
        -> begin
        -> set result=num*num;
        -> end //
        
        call proc(10, @result) //
        select @result //
        
    e.g.4:  输入输出参数
        create procedure proc(inout num int)            --  inout 表示是输入输出参数
        -> begin
        -> set num=num*num;
        -> end //
        
         set @num=10;
        -> call proc(@num);
        -> select @num //
```

### 3.5 函数

####创建函数

学过的函数：LENGTH、SUBSTR、CONCAT等
语法：

	CREATE FUNCTION 函数名(参数名 参数类型, ...) RETURNS 返回类型
	BEGIN
		declare x int default xx;
		函数体;
		return x;
	END

####调用函数

	SELECT 函数名（实参列表）



#### 查看和删除

```
show create function xxx;    # select * from mysql.proc;
drop function xxx;
```



####函数和存储过程的区别

			关键字		调用语法	   返回值			            应用场景
	函数	   FUNCTION	  SELECT 函数()  只能是一个,通过returns       一般用于将处理结果做为一个结果并返回
	
	存储过程 PROCEDURE	CALL 存储过程()	可以有0个或多个,无returns	 一般用于批量插入，批量更新

