## mysql基础

> 以下基于ubuntu



### 1. 安装及配置

```
服务端：
sudo apt-get install mysql-server
sudo service mysql start
sudo service mysql stop
sudo service mysql restart

ps -ef | grep mysql


客户端：
sudo apt-get install mysql-client
mysql -uroot -p  -h 127.0.0.1 -P 3306

navicat
sqlyog


配置：
/etc/mysql/mysql.conf.d/mysql.conf

bind-address表示服务器绑定的ip，默认为127.0.0.1
port表示端口，默认为3306
datadir表示数据库目录，默认为/var/lib/mysql
general_log_file表示普通日志，默认为/var/log/mysql/mysql.log
log_error表示错误日志，默认为/var/log/mysql/error.log
```



### 2. 数据类型

```
可以通过查看帮助文档查阅所有支持的数据类型
使用数据类型的原则是：够用就行，尽量使用取值范围小的，而不用大的，这样可以更多的节省存储空间

常用数据类型如下：
    整数：bit, tinyint, mediumint, int, bigint
    小数：float, double, decimal
    字符串：varchar, char, text, blob
    日期时间: date, time, datetime, timestamp
    枚举类型: enum

    特别说明的类型如下：
        decimal表示浮点数，如decimal(5,2)表示共存5位数，小数占2位
        char表示固定长度的字符串，如char(3)，如果填充'ab'时会补一个空格为'ab '
        varchar表示可变长度的字符串，如varchar(3)，填充'ab'时就会存储'ab'
        字符串text表示存储大文本，当字符大于4000时推荐使用
        对于图片、音频、视频等文件，不存储在数据库中，而是上传到某个服务器上，然后在表中存储这个文件的保存路径
        更全的数据类型可以参考http://blog.csdn.net/anxpp/article/details/51284106

# 约束
    主键primary key：物理上存储的顺序
    自增长auto_increment：  alter table xxx auto_increment = 新的值;     
    非空not null：此字段不允许填写空值
    惟一unique：此字段的值不允许重复
    默认default：当不填写此值时会使用默认值，如果填写时以填写为准
    外键foreign key：对关系字段进行约束，当为关系字段填写值时，会到关联的表中查询此值是否存在，如果存在则填写成功，如果不存在则填写失败并抛出异常
    说明：虽然外键约束可以保证数据的有效性，但是在进行数据的crud（增加、修改、删除、查询）时，都会降低数据库的性能，所以不推荐使用，那么数据的有效性怎么保证呢？答：可以在逻辑层进行控制
    
    foreign key (当前表中的字段名) references 关联表的表名(关联表的字段名)

# 数值类型(常用)
    类型	字节大小	有符号范围(Signed)	无符号范围(Unsigned)
    bit         1    1-64     按照二进制来存储  比如插入3， 存储的 b`11`     
    TINYINT	    1	-128 ~ 127	0 ~ 255
    SMALLINT	2	-32768 ~ 32767	0 ~ 65535
    MEDIUMINT	3	-8388608 ~ 8388607	0 ~ 16777215
    INT/INTEGER	4	-2147483648 ~2147483647	0 ~ 4294967295
    BIGINT	    8	-9223372036854775808 ~ 9223372036854775807	0 ~ 18446744073709551615

    float       4
    double      8
    decimal(M,D)     不确定, M是总位数，D是小数点后的位数

#字符串
    类型	  字节大小	示例
    CHAR	0-255	类型:char(3) 输入 'ab', 实际存储为'ab ', 输入'abcd', 会报错， 适合手机号，邮箱等
    VARCHAR	0-65535	 类型:varchar(3) 输 'ab',实际存储为'ab', 输入'abcd', 实际存储为'abc'，会有1-3个字节要预留， 适合长度不确定的
    		
    		char(3) 
    			1.代表的字符数，不是字节数， utf8 存储占用的字节数是 3 * 3 。。。 不区分字符还是汉字
    			2.固定长度，会有空间的浪费
    			3.char 查询速度大于 varchar
 
    			utf8 最多可以存储 65535/3 个字节  
                 gbk  最多可以存储 65535/2 个字节
             
    BLOB     0-65535(0-2^16-1)       二进制数据类型, 还有longBLOB
    TEXT	 0-65535	大文本,      不能有默认值, 还有mediumText, longText

#日期时间类型
    类型	字节大小	示例
    DATE	    4	'2020-01-01'     日期  年月日
    TIME	    3	'12:29:59'       时间  时分秒
    DATETIME	8	'2020-01-01 12:29:59'  年月日时分秒
    YEAR	    1	'2017'
    TIMESTAMP	4	'1970-01-01 00:00:01' UTC ~ '2038-01-01 00:00:01' UTC 
    				insert, update自动更新

#枚举类型：
    enum
    set
```

### 3. 基本命令

```
查看版本：            select version();
显示当前时间：         select now();
查看当前使用的数据库： select database();
```

### 4. 数据库基本指令

```
show databases;

use xxx;

create database  IF NOT EXISTS python charset utf8 collate utf8_bin/utf8_general_ci engine innodb;

drop database python;

注释：
-- 至少一个空格
#
/**/
```

### 5. 表操作基本指令

```
# 查看有哪些表
    show tables;
    show tables from 库名;

# 创建表
## 建表的过程中如果有关键字，`` 包裹即可
    create table user(
        id int unsigned auto_increment primary key not null,
        name varchar(20) default "",
    );

# 查看创建表的语句
	show create table 表名;

# 查看表结构
	desc xxx; 


# 修改表字段
添加字段：  
    alter table students 
    add birthday datetime  after xxx字段;

修改字段名：
    alter table 表名 
    change 原名 新名 类型及约束;
    例：
    alter table students 
    change birthday birth datetime not null;
    
修改字段类型：
    alter table 表名 
    modify 列名 类型及约束;
    例：
    alter table students 
    modify birth date not null;
    
删除字段：
    alter table 表名 
    drop 列名;
    例：
    alter table students 
    drop birthday;
    
修改表的字符集
	alter table xxx charset utf8;
  
# 修改表名
	rename table xx to xxx;

# 删除表
	drop table students;
```

### 6. 增删改查

```
# 查找数据
select * from classes;
select id, name from classes;

# 插入数据
insert into students values(0,'郭靖',1,'蒙古','2016-1-2')
insert into students (name,hometown,birthday) values ('黄蓉','桃花岛','2016-3-2');
# 还可以一次性插入多行数据
insert into classes values(0,'python1'),(0,'python2');
insert into students(name) values('杨康'),('杨过'),('小龙女');

# 更新
## 如果没有where条件，相当于对所有记录做更新
update students set gender=0, hometown='北京' where id=5;

# 删除
## 如果没有where条件，相当于对所有记录做删除
delete from students where id = 1;
```

### 7. 查询进阶

```
# 查询
select * from students;
select name from students;
select id as 序号, name as 名字, gender as 性别 from students;
select s.id, s.name, s.gender from students as s;
select distinct gender from students;


# 条件：
select * from students where id=1;
where后面支持多种运算符，进行条件的处理

    比较运算符
        等于:     =
        大于:     >
        大于等于: >=
        小于:     <
        小于等于: <=
        不等于:   != 或 <>
        
        
    逻辑运算符
        and
        or
        not
        
    模糊查询
        like
            % 表示任意多个任意字符
            _ 表示一个任意字符
            
            ^ 开头
            $ 结尾
            
    范围查询
        in表示在一个非连续的范围内
            select * from students where id in(1,3,8);
        
        between ... and ...表示在一个连续的范围内
            select * from students where id between 3 and 8;
            
    空判断(is null)
        select * from students where height is null;
        select * from students where height is not null;
        
        安全等于: <=>, 既可以判断空值，也可以判断非空值
    
    优先级由高到低的顺序为：小括号，not，比较运算符，逻辑运算符
        

# 排序：
    select * from 表名 order by 列1 asc | desc [ , 列2 asc|desc, ...]
    
# 聚合函数：
    count()
    sum()
    max()
    min()
    avg()
    ...
    
# 分组：
    group by可用于单个字段分组，也可用于多个字段分组
    e.g: select gender from students group by gender, name;
        
    group by + group_concat()
    group_concat(字段名)可以作为一个输出字段来使用，
    表示分组之后，根据分组结果，使用group_concat()来放置每一组的某字段的值的集合
    e.g: select gender, group_concat(name) from students group by gender;
    
    group by + 集合函数
    select gender, avg(age) from students group by gender;
    
    group by + having
    having 条件表达式：用来分组查询后指定一些条件来输出查询结果
    having作用和where一样，但having只能用于group by
    e.g: select gender, count(*) from students group by gender having count(*)>2;
    
    group by + with rollup
    在最后新增一行，来记录当前列里所有记录的总和
    select gender, group_concat(age) from students group by gender with rollup;


# 分页：
    select * from 表名 limit start, count
        
        
# 连接：
    内连接   中间的
    左连接   左侧的完全显示
    右连接   右侧的完全显示， 对于开发而言，几乎一样，把表的前后顺序调整下就行
    
    select * from 表1 inner或left或right join 表2 on 表1.列 = 表2.列
    
    e.g.:
    select * from students inner join classes on students.cls_id = classes.id;
    select * from students as s left join classes as c on s.cls_id = c.id;
    select * from students as s right join classes as c on s.cls_id = c.id;
    
    select s.name, c.name from students as s inner join classes as c on s.cls_id = c.id;
  
  
# 自关联(自连接)：
    create table areas(
        aid int primary key,
        atitle varchar(20),
        pid int
    );
    
    查询一共有多少个省
    select count(*) from areas where pid is null;
    
    例1：查询省的名称为"山西省"的所有城市
    select city.* from areas as city
    inner join areas as province on city.pid=province.aid  -- 城市的父id = 省的子id
    where province.atitle='山西省';
    
    例2：查询市的名称为"广州市"的所有区县
    select dis.* from areas as dis
    inner join areas as city on city.aid=dis.pid
    where city.atitle='广州市';
    
    
# 子查询：
    分类：  
        标量子查询: 子查询返回的结果是一个数据(一行一列)
        列子查询:   返回的结果是一列(一列多行)
        行子查询:   返回的结果是一行(一行多列)
        表子查询：  子查询返回的结果当成一个表, 子查询临时表
    
        标量子查询
            查询大于平均年龄的学生
            select * from students where age > (select avg(age) from students);
           
        列级子查询    
            查询还有学生在班的所有班级名字
                找出学生表中所有的班级 id
                找出班级表中对应的名字
            select name from classes where id in (select cls_id from students);  
            # 多行子查询
        
        行级子查询(多列子查询)
            需求: 查找班级年龄最大,身高最高的学生
            行元素: 将多个字段合成一个行元素, 在行级子查询中会使用到行元素
            select * from students where (height,age) = (select max(height),max(age) from students);
        
        
        子查询中特定关键字使用
            in | not in子查询: 用于子查询的返回结果多个值。
                e.g.1: 查找笔试成绩及格的同学
                    select * from stuinfo where stuno in (select stuno from stumarks where writtenexam>=60);

                e.g.2: 查询笔试成绩不及格的同学
                    select * from stuinfo where stuno in (select stuno from stumarks where writtenexam<=60);

                e.g.3: 查询没有通过的同学（不及格，缺考）
                    select * from stuinfo where stuno  not in (select stuno from stumarks where writtenexam>=60);

            exists 和 not exists: 
                e.g.1:  如果有人笔试超过80分就显示所有的学生
                    select * from stuinfo where exists (select * from stumarks where writtenexam>=80);

                e.g.2:  如果没有人超过80分就显示所有的学生
                    select * from stuinfo where not exists (select * from stumarks where writtenexam>=80);
                    
            all 和 any:
            	all 是所有的
            	any 其中一个
            	
        自我复制：
        	insert into my_tab01 (id, `name`, sal, job) select eid, ename, sal, job from emp;
        	# error  insert into my_tab01 (id, `name`, sal, job) select * from emp;
        	
        如何去重表中记录：
        	create table my_tab02 like emp;
        	insert into my_temp select distinct * from my_tab02
        	delete from my_tab02
        	
        	insert into my_tab02 select * from my_temp
        	drop table my_temp
    

# 合并查询(也叫联合查询，union)
union [all]

****************************************************************
完整的select语句:
    select distinct *
    from 表名
    where ....
    group by ... having ...
    order by ...
    limit start, count
****************************************************************
```



### 8. 备份和恢复

```
# 备份
mysqldump -uroot -p 数据库名 > xx.sql

# 恢复
mysql -uroot –p 新数据库名 < xxx.sql
或者 
进入到mysql后，建库，use该库， source xxx.sql



https://blog.csdn.net/DOUBLE121PIG/article/details/119121016
# windows
	mysqldump.exe -uroot -pmysql --databases test --tables xxx, xxx > ssss.sql

# linux
## 备份(仅结构)
    mysqldump -uroot -p -d 数据库名 > xxx.sql           完整的结构
    mysqldump -uroot -p -d 数据库名 表名 > xxx.sql      特定的结构    

## 备份(带数据)
    mysqldump -uroot -p 数据库名> xxx.sql      完整的数据和结构
    mysqldump -h xxx -u xxx -P xxx -p pass --databases/-B test --tables xx, xxx, xx > xxx.sql  特定的数据和结构
    mysqldump -uroot -p 数据库名 -t  数据表名> xxx.sql   仅数据

## 还原
	mysql -h xxx -u xxx -P xxx -p pass  test < xxx.sql
```



### 9. 数据库设计

```
三范式
    第一范式：强调的是列的原子性，即列不能够再分成其他几列    
              e.g.:contact(张三，10086，山东) --> name,tel,addr
    第二范式：
        首先是 1NF，另外包含两部分内容，一是表必须有一个主键；二是没有包含在主键中的列必须完全依赖于主键，而不能只依赖于主键的一部分
        
        e.g.:
            考虑一个订单明细表：【OrderDetail】（OrderID，ProductID，UnitPrice，Discount，Quantity，ProductName）。 因为我们知道在一个订单中可以订购多种产品，所以单单一个 OrderID 是不足以成为主键的，主键应该是（OrderID，ProductID）。显而易见 Discount（折扣），Quantity（数量）完全依赖（取决）于主键（OderID，ProductID），而 UnitPrice，ProductName 只依赖于 ProductID。所以 OrderDetail 表不符合 2NF。不符合 2NF 的设计容易产生冗余数据。

            可以把【OrderDetail】表拆分为【OrderDetail】（OrderID，ProductID，Discount，Quantity）和【Product】（ProductID，UnitPrice，ProductName）来消除原订单表中UnitPrice，ProductName多次重复的情况
        
    第三范式：
        首先是 2NF，另外非主键列必须直接依赖于主键，不能存在传递依赖。即不能存在：非主键列 A 依赖于非主键列 B，非主键列 B 依赖于主键的情况
        
        e.g.:
            考虑一个订单表【Order】（OrderID，OrderDate，CustomerID，CustomerName，CustomerAddr，CustomerCity）主键是（OrderID）。 其中 OrderDate，CustomerID，CustomerName，CustomerAddr，CustomerCity 等非主键列都完全依赖于主键（OrderID），所以符合 2NF。不过问题是 CustomerName，CustomerAddr，CustomerCity 直接依赖的是 CustomerID（非主键列），而不是直接依赖于主键，它是通过传递才依赖于主键，所以不符合 3NF。 通过拆分【Order】为【Order】（OrderID，OrderDate，CustomerID）和【Customer】（CustomerID，CustomerName，CustomerAddr，CustomerCity）从而达到 3NF。
            
    *第二范式（2NF）和第三范式（3NF）的概念很容易混淆，区分它们的关键点在于，2NF：非主键列是否完全依赖于主键，还是依赖于主键的一部分；3NF：非主键列是直接依赖于主键，不能存在依赖传递
            
        
        
ER模型
    实体关系
    staruml
    pdman，一些图形化的数据库软件
    navicat e-r关系设计
    power-design

58到家数据库设计军规：
https://mp.weixin.qq.com/s/Yjh_fPgrjuhhOZyVtRQ-SA?
```



### 10. 事务

> todo

```
# 四大特性：（acid）
原子性 (不可再分割，要么成功，要么失败);文件操作（a+）
一致性（结果是一致的，有增有减）
隔离性（一个事务在最终提交前，对其他事务是不可见的）
持久性（是持久化存储的）

start transaction/set autocommit=off /begin;
	insert into goods_cates(name) values('小霸王游戏机');
savepoint aaa;
rollback [to xxx];
commit;

事务需要innodb, myIsam不行

# 隔离级别
脏读：       一个读取到另一个还未提交的
不可重复读： 一个事务中多次查询，由于其他事务做了修改或删除，每次返回不同的结果集
幻读：		 一个事务中多次查询，由于其他事务做了插入，每次返回不同的结果集

www.cnblogs.com/liyus/p/10556563.html
串行		 全可避免，加锁
可重复读    可避免脏读，不可重复读，一定程度上能避免幻读，不加锁
读已提交    可避免脏读(快照，保证一致性还不需要加锁)
读未提交	啥都避免不了

//查看当前会话的隔离级别
select @@tx_isolation;

//设置当前会话的隔离级别
 set session transaction isolation  level read uncommited;

//查看当前系统的隔离级别
select @@global.tx_isolation;

//设置当前系统的隔离级别
 set global transaction isolation  level read uncommited;
 或者
 更改my.ini 文件


e.g1: 演示读未提交
select @@tx_isolation;                     select @@tx_isolation;
								        set session transaction isolation  level read uncommited;
begin;                                     begin;
use xxx;						         use xxx;
create table account;
select * from account;                     select * from account;
insert into account values();          
select * from account;		               select * from account;     #发现能看到数据，脏读
update account set money=800 where id =xx; 
insert into account values(200, "jack", 2000);	
commit;								     select * from account;    #发现能看到数据，不可重复读和幻读


e.g2: 演示读已提交
select @@tx_isolation;                     select @@tx_isolation;
								        set session transaction isolation  level read commited;
begin;                                     begin;
use xxx;						         use xxx;
#create table account;
insert into account values();          
select * from account;		               select * from account;    #发现不能看到数据，可避免脏读
update account set money=800 where id =xx; 
commit;								     select * from account;    #发现能看到数据，不可重复读和幻读



e.g3: 演示可重复读， 不加锁
select @@tx_isolation;                     select @@tx_isolation;
								        set session transaction isolation  level repeatable read;
begin;                                     begin;
use xxx;						         use xxx;
#create table account;
insert into account values();          	    select * from account;   #发现不能看到新的数据，可避免脏读
update account set money=800 where id =xx;  select * from account;   #发现不能看到新的数据，可避免脏读
commit;								     select * from account;   #发现不能看到新的数据，可避免不可重																复读和幻读


e.g4: 演示可串行化， 加锁
select @@tx_isolation;                     select @@tx_isolation;
								        set session transaction isolation  level repeatable read;
begin;                                     begin;
use xxx;						         use xxx;
#create table account;
insert into account values();          	    
update account set money=800 where id =xx;  select * from account;   #发现不能看到新的数据，卡死在那里
commit;								     lock wait timeout exceeded 
										select * from account;   #发现能看到新的数据，可避免不可重																复读和幻读, 脏读


# 存储引擎
myisam, innodb, memory(基于hash, 存储在内存中，对临时表有用), csv, archive, mrg myisam等

# 查看支持哪些引擎
show engines;

alter table `表名` engine = 存储引擎 ;


myisam 和 innodb 区别:
myisam:
	1.添加速度快
	2.不支持事务， 外键
	3.支持表锁
	
innodb:
	1.添加速度较快
	2.支持事务，外键
	3.支持行锁
```



### 11. 索引

```
# 显示索引名：
show index from test_index;

# 创建索引：
create index 索引名 on  表名(字段名)
create index 索引名 on 表名(字段名（长度）)
## 创建主键索引

## 索引分类：
主键索引： 比如 id, primary_key, 一个表只能有一个主键，不允许有空值
唯一索引： unique, 索引列的值必须唯一，但允许有空值
普通索引： index
组合索引： 指多个字段上创建的索引，只有在查询条件中使用了创建索引时的第一个字段，索引才会被使用。使用组合索引时遵循最左前缀集合
hash索引： 字段, hash后的字段， 以键值对的方式
全文索引： fulltext（适用于myisam）, 建议用es

# 删除索引：
drop index title_index on 表名
## 删除主键索引

# 为创建索引，性能检测：
select @@profiling 
set profiling =1;

select * from xxx where id =99999;
show profiles;

# 创建索引，性能检测：
create index title_index on xxx
select * from xxx where id =99999;
show profiles;


注意：
1.建立太多的索引将会影响更新和插入的速度，因为它需要同样更新每个索引文件
2.占用磁盘空间(原有的ibd文件大小会增加，创建过程是耗时的)
3.只对创建了索引的列才有效
4.查询变得快，dml有影响

原理：
1. 无索引，全表扫描
2. 有索引，二叉树


索引失效的注意事项：
1.索引不会包含有null值的列
只要列中包含有null值都将不会被包含在索引中，复合索引中只要有一列含有null值，那么这一列对于此复合索引就是无效的。所以我们在数据库设计时不要让字段的默认值为null。
2.使用短索引
对串列进行索引，如果可能应该指定一个前缀长度。例如，如果有一个char(255)的列，如果在前10个或20个字符内，多数值是惟一的，那么就不要对整个列进行索引。短索引不仅可以提高查询速度而且可以节省磁盘空间和I/O操作。
3.索引列排序
查询只使用一个索引，因此如果where子句中已经使用了索引的话，那么order by中的列是不会使用索引的。因此数据库默认排序可以符合要求的情况下不要使用排序操作；尽量不要包含多个列的排序，如果需要最好给这些列创建复合索引。    排序变成组合索引
4.like语句操作
一般情况下不推荐使用like操作，如果非使用不可，如何使用也是一个问题。like "%aaa%" 不会使用索引而like "aaa%"可以使用索引。
5.不要在列上进行运算
这将导致索引失效而进行全表扫描，例如
SELECT * FROM table_name WHERE YEAR(column_name) < 2017;
6.不使用not in和<>操作
```



### 12. 视图

> 基本不用, 类似python解释器, 在sql语句和数据库之间隔了一层，虚拟表

```
作用：
    提高了重用性，就像一个函数
    对数据库重构，却不影响程序的运行
    提高了安全性能，可以对不同的用户
    让数据更加清晰
    
# 创建:
create view v_goods_info as select ...

# 查看：
select * from v_goods_info

# 删除：
drop view v_goods_info
```



### 13. 账户管理

```
# 创建账户&授权
grant 权限列表 on 数据库 to '用户名'@'访问主机' identified by '密码';

例：
grant select on jing_dong.* to 'laowang'@'localhost' identified by '123456';
grant all privileges on jing_dong.* to "laoli"@"%"   identified by "12345678"

说明：
    可以操作python数据库的所有表，方式为:jing_dong.*
    访问主机通常使用 百分号% 表示此账户可以使用任何ip的主机登录访问此数据库
    访问主机可以设置成 localhost或具体的ip，表示只允许本机或特定主机访问

# 查看用户有哪些权限
show grants for laowang@localhost;

# 查看所有用户
select host, user, authentication_string from user;

# 修改权限
grant 权限名称 on 数据库 to 账户@主机 with grant option;

grant select, insert on xxx 'laowang'@'localhost' with grant option;
flush privileges;

# 修改密码
使用root登录，修改mysql数据库的user表
update user set authentication_string=password('123') where user='laowang';
flush privileges;


# 删除账户
方式一：
使用root登录
drop user 'laowang'@'%';

方式二：
delete from user where user='laowang';
flush privileges;


# 允许远程访问
vim /etc/mysql/mysql.conf.d/mysqld.cnf
# bind 127.0.0.1
service mysql restart
```



### 14. 主从搭建

```
数据备份
读写分离
负载均衡
更高要求用redis

step1:主备份
        直接在root
        (mysqldump -uroot -p123 jing_dong > jd.sql)
        mysqldump -uroot -p123 --all-databases --lock-all-tables >jd.sql
    
step2.从恢复：
        mysql -uroot -p123 < jd.sql
    
step3.设定主 id,日志文件,
        sudo vim /etc/mysql/mysql.conf/mysqld.cnf
        
        #下面保证不注释
        server-id =1 
        log-bin 
        
        service mysql start
    
step4.从 id
        server-id =2 (一般用ip)
        
        service mysql start
    
step5.同步
        
        主服务器（mysql）
        GRANT REPLICATION SLAVE ON *.* TO 'slave'@'%' identified by 'slave';
        FLUSH PRIVILEGES;
        
        主服务器(mysql)
        SHOW MASTER STATUS\G;
        
        从服务器：
        change master to master_host='192.168.11.150', master_user='slave', master_password='slave', master_log_file='mysql-bin.000005',  master_log_pos=590;
    
    
step6:查看：
        start slave;
        show slave status\G;
        show master stutus\G;
```



### 15. 其他

```
# 数据库性能测试 sysbench
# phpmyadmin
# mycat
# mysql5.7 支持json
# 频繁访问数据：
冗余字段
索引
缓存
```

