# MySQL规范

## 一、表命名规范
1.[强制]表名、字段名必须使用小写字母或数字,禁止出现数字开头,不要超过30个字符，尽量见名知意，使用下划线分割; 
2.[强制]禁用保留字,如desc,range,match,delayed等 
3.[强制]临时库、表名，必须以tmp为前缀，以日期为后缀，例如tmp_product_20151229 
4.[强制]备份表、表名，必须以日期为后缀，例如produce_bak_20151229 
 
## 二、表设计规范
1.[强制]表必须有主键，建议使用mysql的自增主键，字段为bigint unsigned类型auto_increment属性 
2.[强制]InnoDB禁止使用外键约束，可以通过程序层面保证。 
3.[强制]创建表的时候对字段和表添加COMMENT 
4.[强制]最多更改和查询的字段放在基础表内，方便完整载入内存；访问频率低的或大字段放到扩展表里，分离冷热数据 
5.[强制]多张关联表之间，适当的冗余字段，可以减少JOIN查询 

## 三、字段设计规范
1.[强制]表达是与否概念的字段,必须使用is_xxx的方式命名。任何字段如果为非负数,必须是unsigned 
2.[强制]当字符串较短，或数据频繁更新时，可以使用CHAR(N)，N表示字符数而非字节数 
3.[强制]当字符串长度可预见时，可以使用VARCHAR(N)，预留10%，N表示字符数而非字节数；注意varchar的字节数是否设置超过256 
4.[强制]使用DECIMAL代替FLOAT和DOUBLE，以存储精确浮点数，例如支付相关数据 
5.[强制]使用INT UNSIGNED存储IPV4，inet_aton()和inet_ntoa()用于IPV4与INT互转 
6.[强制]创建表的时候，字段尽量不要为NULL，使用NOT NULL DEFAULT ‘xxx’，否则count(字段)、concat、not in可能不准；影响索引统计信息，影响组合索引 
7.[强制]整型定义中无需定义显示宽度，比如：使用INT，而不是INT(4) 
8.[强制]不建议使用ENUM类型，可使用TINYINT来代替 
9.[强制]尽可能不使用TEXT、BLOB类型，如果必须使用，建议将过大字段或是不常用的描述型较大字段拆分到其他表中；另外，禁止用数据库存储图片或文件。 

## 四、索引设计
1.[强制]合理创建组合索引，(a,b,c)生成b+树(a)、(a,b)、(a,b,c)，根据最左前缀原则选择性高的字段放在最前 
2.[强制]主键索引名为pk_字段名,唯一索引名为uk_字段名,普通索引名是idx_字段名. 
3.[建议]对经常要查询的列添加索引或者组合索引（选择性高的作为前缀索引） 
4.[建议]为经常需要排序、分组和联合操作的字段建立索引:ORDER BY、GROUP BY、DISTINCT和UNION等操作的字段 
5.[建议]选择性高的字段建立索引：count(distinct col)/count(*) 
6.[建议]经常与其他表进行连接的表，在连接字段上应该建立索引； 
7.[建议]频繁进行数据操作的表，不要建立太多的索引； 
8.[建议]删除无用的索引，避免对执行计划造成负面影响；  

## 五、sql规范
1.[强制]生产环境慎用count(*)统计大表数据量，可以查看系统表估算当前表数据量
SELECT table_name,table_rows FROM information_schema.tables
WHERE TABLE_SCHEMA = 'evo_rcs' and table_name='job_state_change' ORDER BY table_rows DESC;
2.[强制]生产环境禁止使用select * from table，一定要指定需要的字段，来减少无用数据的查询请求（消耗多余cpu，io，内存，带宽）。
3.[强制]生产环境查看数据使用limit M,N限制返回的数据量；分批获取大量数据时，禁止大偏移量的limit M,N语句，使用主键游标 where PK>… limit N
4.[强制] DELETE和UPDATE操作是不是有带WHERE条件;对于不带WHERE条件的或是WHERE条件的范围比较大的SQL要极度小心
5.[强制] 创建表的时候不要添加drop操作，应为CREATE TABLE IF NOT EXISTS TABLEXXX .......；
6.[强制] 禁止隐式转换，数值类型禁止加引号，字符和日期类型必须加引号。索引字段隐式转换会导致该字段索引不可用
7.[建议] 使用like进行模糊查询时应注意
关键词%yue%，由于yue前面用到了“%”，因此该查询必然走全表扫描，除非必要，否则不要在关键词前加%，
select*from contact where username like ‘%yue%’
8.[建议] 对查询的列不要使用函数或者运算。否则索引无法使用
错误：select * from tableName where id+1 = 1000;
正确：select * from tableName where id = 999;
9.[建议] 在select……from之间尽量避免使用子查询，而改用表关联
10.[建议] sql中存在in、not in、not exists等子查询时，应尽量改写为等连接和外连接，因为mysql对于子查询的查询转换并不太友好。


## 六、数据库账号权限管理
 1）创建用户并赋予相应的操作权限：
方法一：
CREATE USER '用户名称'@'主机ip'IDENTIFIED BY '用户密码';
grant 权限 on 数据库.表 to '用户名'@'登录主机ip';
flush privileges;
** **
方法二：
grant 权限 on 数据库.表 to '用户名'@'登录主机ip' IDENTIFIED BY '用户密码';
flush privileges;
 
知识点：
权限： select ,update,delete,insert(表数据)、create,alert,drop(表结构)、 create routine,alert routine,execute(存储过程)、all/all privileges(所有权限)
数据库：数据库名或者*(所有数据库)
表：表名或者*(某数据库下所有表)，*.*表示所有数据库的所有表
主机：主机ip或者%(任何其他主机)
 
2）用户管理
a.mysql中用户由'user'@'host'组成，查看数据库中用户：
select user,host from mysql.user;
b.删除用户
drop user 'user'@'host';
c.查看用户权限
show grants for 'user'@'host';

## 七、数据修改前备份
 1）通过navicate对数据进行删、改之前先进行备份，以防误操作。例如：
update basic_agv set warehouse_id=2 where agv_code='CARRIER_172021020086';
 
备份语句：
select * from basic_agv where agv_code='CARRIER_172021020086';
 
2）navicate导出查出的数据
导出--选择SQL脚本文件
![image.png](https://cdn.nlark.com/yuque/0/2020/png/2593751/1604469465101-296451f3-4181-48e5-9b3c-cbdf93fd831e.png#align=left&display=inline&height=225&margin=%5Bobject%20Object%5D&name=image.png&originHeight=449&originWidth=698&size=114285&status=done&style=none&width=349)![image.png](https://cdn.nlark.com/yuque/0/2020/png/2593751/1604469520476-6571afc5-9131-4dee-8b85-d473fc790c51.png#align=left&display=inline&height=230&margin=%5Bobject%20Object%5D&name=image.png&originHeight=459&originWidth=502&size=57400&status=done&style=none&width=251)
![image.png](https://cdn.nlark.com/yuque/0/2020/png/2593751/1604469542312-266c3438-932f-4001-a7f1-df22bb33fa09.png#align=left&display=inline&height=119&margin=%5Bobject%20Object%5D&name=image.png&originHeight=238&originWidth=579&size=76539&status=done&style=none&width=289.5)




 
注：
a.创建当日文件夹存放备份数据
b.sql文件用被修改的数据的表名命名
 
3）记录好操作数据库操作的sql及结果，以便问题追踪
a.创建一个word文档用于记录sql及结果信息，命名为《数据库sql执行记录》，记录内容如下：

 ![image.png](https://cdn.nlark.com/yuque/0/2020/png/2593751/1604469610662-8ea25048-4634-488a-b738-1ce8f7a1b750.png#align=left&display=inline&height=238&margin=%5Bobject%20Object%5D&name=image.png&originHeight=475&originWidth=1213&size=129877&status=done&style=none&width=606.5)
 
