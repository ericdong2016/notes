## 1. 索引&性能优化&慢查询

### 1.1 索引入门

```
# 1.sql性能下降, 执行慢的原因
数据过多                            分库分表
sql写的烂，关联了太多表(join)        sql优化，拆分表
索引失效或者没有索引    			  索引优化            
服务器没有调优及mysql参数没有调优     my.cnf

# 2.索引分类
主键索引
普通索引
唯一索引
复合索引
hash
full-text

# 3.索引结构
btree
b+tree
full-text
hash
r-tree（范围查找）
聚簇索引，非聚簇索引


# 4.哪些情况需要创建索引
      主键自动建立唯一索引
      频繁作为查询条件的字段应该创建索引(where后面的语句)
      查询中与其它表关联的字段，外键关系建立索引
      单键/组合索引的选择问题，who？(在高并发下倾向创建组合索引)
      查询中排序的字段，排序字段若更改为索引去访问将大大提高速度
      查询中统计或者分组字段

# 5.哪些情况不要创建索引
	表记录太少
    经常增删改的表
      Why:提高了查询速度，同时却会降低更新表的速度，如对表进行INSERT、UPDATE和DELETE。 因为更新表时，MySQL不仅要保存数据，还要保存一下索引文件
    Where条件里用不到的字段不创建索引
    数据重复且分布平均的表字段，因此应该只为最经常查询和最经常排序的数据列建立索引。 注意，如果某个数据列包含许多重复的内容，为它建立索引就没有太大的实际效果。


# 6.explain
常见瓶颈：
	cpu
	io
	锁
	服务器性能： top, free, iostat, vmstat 查看系统性能
	
作用：
    表的读取顺序
    哪些索引可以使用
    数据读取操作的操作类型
    哪些索引被实际使用
    表之间的引用
    每张表有多少行被优化器查询

explain sql语句;

id  select_type   table   type   possible_keys   key   key_len   ref   rows   extra

1	SIMPLE	      proc	 system					                     0	  Const row not found


id:
	作用：
		select查询的序列号，包含一组数字, 表示读取的顺序
	分类：
		id相同，执行的顺序从上至下(看table, 就能看出顺序)
		id不同，id越大，先执行
		id有相同也有不同，id大的先执行，id相同的看table的顺序（derivedx, 衍生，x执行的是id）
	

select_type：
	作用：
		能够读取的操作类型
	常见字段：
		simple    		//简单的select查询，不包含子查询或者union
		primary		    //查询中包含子查询，最外层的
		subquery	    //查询中包含子查询，内层的
		derived         //在from列表中包含的子查询被标记为derived,mysql递归这些子查询，把结果放在临时表中
		union           //第二个select出现在union之后，则被标记为union
		union_result    //从union表获取的结果的select
		
type:
	作用：
		显示查询使用了什么索引，可以看出sql是否优化过
		
	分类：(优化效果从上到下依次递减), 以下列出的是部分，还有更全的
		system    //表只有一行记录(等于系统表)，这是const类型的特例，平时一般不会出现
		const     //表示通过索引一次就找到了，常用于primary_key或者unique 索引, 将主键置于where条件中，mysql就能将该查询转换为一个常量，平时一般不会出现
		eq_ref    //唯一性索引扫描，对于每个索引键，表中只有一条记录与之匹配，常见于主键或者唯一索引(类似于公司ceo只有一个)
		ref       //非唯一性索引扫描，返回匹配某个单独值的所有行（研发部的程序员），属于查找和扫描的混合体
				 //使用场景： create index xxx on table(field1, field2); explain select * from tab where field1 = "" ;     发现 type 是 ref
		range     //只检索给定范围的行，使用一个索引来选择行，key列显示使用了哪个索引，一般就是where中 between , < , > , in等的扫描，只扫描部分， 比全表扫描好
				 //使用场景： explain select * from tab where id in (1,2,6);
		index     //full index scan, index和all的区别在于只遍历索引树，通常比all快，索引文件比数据文件小
		all       //表明是全表扫描，全表从硬盘中读取数据，百万上的一定要优化
		null     
		
	要求：
		至少达到range,  最好达到ref
		
possible_keys:
	作用：
		可能用到了哪些索引，一个或者多个，但不一定被实际使用
		
key:
	作用：
		实际用到的索引
	分类：
		如果未null, 则没有使用索引
		如果查询使用了覆盖索引（解决like查询问题），则该索引仅出现在key列表中，该索引和查询select 重叠
	
key_len:
	作用：
		使用的字节数，显示的最大可能长度， 实际在相同结果的前提下，长度越小越好
	
ref:
	作用：
		显示索引的哪一列被使用了，如果可能的话，最好是一个常数，显示哪些列或者常量被用于索引上的值(=后面的值)

rows：
	作用：
		根据表统计信息及索引选用情况，大致估算出找到所需的记录 所需要读取的行数
		
extra:
	作用：
		包括不适合在其他列中显示但是十分重要的信息
		
	分类：
		using filesort    //问题大， 九死一生
						//文件内排序：mysql无法利用索引完成排序
						//索引是 col1, col2, col3 
						//\G竖版
						//order by 字段上建索引
		                  //explain select col1 from t1 where col1="ac" order by col3\G;        err 
                           //explain select col1 from t1 where col1="ac" order by col2, col3\G;  ok
         
         using temporary   //问题十分大，十死一生
         				 //索引是col1, col2, group by 个数跟索引格式一致
         				 //explain select col1 from t1 where col1 in ("ac", "ab") group by col2;
         				 //explain select col1 from t1 where col1 in ("ac","ab") group by col1, col2;
         
		using index		 //好，表明相应的select操作使用了覆盖索引，避免访问了表的数据行，效率高，如果同时出现了using where, 表明索引被用来执行索引键值的查找
		
						// 覆盖索引: 建的索引字段和查的字段是一致的，只从索引中返回select 列表中的字段，不必根据索引再次读取数据文件，即查询列被索引覆盖
		 
		using where      
						//索引是col1, col2
						//explain select col2  from t1 where col1="ab"; //using index, using where
						//explain select col1, col2 from t1;            //using index 
					
		using join buffer: 提示可以将缓存区buffer调大些
		
		impossible where:  查询条件有问题
	
总结：
id, type, key, row, extra 最为重要
```



### 1.2 性能优化

> explain + 慢sql (> 5s ) 分析
>
> show profile
>
> sql 参数调优



#### 优化原则

```
1.最佳左前缀法则/全值匹配（如果索引了多列，要遵守最左前缀法则。指的是查询从索引的最左前列开始并且不跳过索引中的列。）
  
2.不在索引列上做任何操作（计算、函数、(自动or手动)类型转换），会导致索引失效而转向全表扫描

3.存储引擎不能使用索引中范围条件右边的列
	范围条件右边与范围条件使用的同一个组合索引，右边的才会失效。若是不同索引则不会失效
	
4.尽量使用覆盖索引(只访问索引的查询(索引列和查询列一致))，减少select *

5.mysql 在使用不等于(!= 或者<>)的时候无法使用索引会导致全表扫描

6.is not null 也无法使用索引, 但是is null是可以使用索引的

7.like以通配符开头('%abc...')mysql索引失效会变成全表扫描的操作
  问题：解决like '%字符串%'时索引不被使用的方法？？
  
8.少用or, 用它来连接时会索引失效

9.字符串不加单引号索引失效  行锁变表锁




## 优化建议（鬼都看不懂）
1. 尽可能减少join语句中的nestedloop的循环的总次数，"永远用小的结果集驱动大的结果集"(left join ,inner join)
2. 优先优化nestedloop中的内层循环
3. 保证join 被驱动表join条件已经被索引
4. 当无法保证被驱条件的join条件被索引且内存资源充足的条件下，不要太吝啬joinbuffer的设置
5. 子查询尽量不要放在被驱动表，有可能使用不到索引


## 优化1
    CREATE TABLE staffs (
      id INT PRIMARY KEY AUTO_INCREMENT,
      NAME VARCHAR (24)  NULL DEFAULT '' COMMENT '姓名',
      age INT NOT NULL DEFAULT 0 COMMENT '年龄',
      pos VARCHAR (20) NOT NULL DEFAULT '' COMMENT '职位',
      add_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '入职时间'
    ) CHARSET utf8 COMMENT '员工记录表' ;


    INSERT INTO staffs(NAME,age,pos,add_time) VALUES('z3',22,'manager',NOW());
    INSERT INTO staffs(NAME,age,pos,add_time) VALUES('July',23,'dev',NOW());
    INSERT INTO staffs(NAME,age,pos,add_time) VALUES('2000',23,'dev',NOW());
    INSERT INTO staffs(NAME,age,pos,add_time) VALUES(null,23,'dev',NOW());
    SELECT * FROM staffs;

    ALTER TABLE staffs ADD INDEX idx_staffs_nameAgePos(name, age, pos);
    
    最佳左前缀法则： 
    	如果索引了多列，要遵守最左前缀法则。指的是查询从索引的最左前列开始并且不跳过索引中的列。
    	
## 优化2
	EXPLAIN SELECT * FROM staffs WHERE left(NAME, 4) = 'July';
	
	不在索引列上做任何操作（计算、函数、(自动or手动)类型转换），会导致索引失效而转向全表扫描
	
## 优化3
	EXPLAIN SELECT * FROM staffs WHERE NAME = 'July' AND age > 25 AND pos = 'dev';
	
	存储引擎不能同时使用到索引范围条件右边的列(范围条件右边与范围条件使用的同一个组合索引，右边的会失效。 范围之后全失效)
	
## 优化4
	 EXPLAIN SELECT name, age, pos  FROM staffs WHERE NAME = 'July' AND age = 25 AND pos = 'dev';
	 
	 尽量使用覆盖索引(只访问索引的查询(索引列和查询列一致))，减少select *
	 
## 优化5
	EXPLAIN SELECT name, age, pos  FROM staffs WHERE NAME != 'July' AND age = 25 AND pos = 'dev';
	
	mysql 在使用不等于(!= 或者<>)的时候无法使用索引会导致全表扫描
	
	使用 != 和 <> 的字段索引失效( != 针对数值类型。 <> 针对字符类型
	前提 where and 后的字段在混合索引中的位置比比当前字段靠后  where age != 10 and name='xxx'  , 这种情况下，mysql自动优化，将 name='xxx' 放在 age ！=10 之前，name 依然能使用索引。只是 age 的索引失效)
	
	
## 优化6
	EXPLAIN SELECT name, age, pos  FROM staffs WHERE NAME is not NULL;
	
	is not null 也无法使用索引, 但是is null是可以使用索引的

## 优化7  此条不是很成立
	EXPLAIN SELECT name, age, pos  FROM staffs WHERE NAME like '%July%';

    EXPLAIN SELECT name, age, pos  FROM staffs WHERE NAME like '%July';

    EXPLAIN SELECT name, age, pos  FROM staffs WHERE NAME like 'July%';
    
	like ‘%abc%’  type 类型会变成 all
	like ‘abc%’   type 类型为 range ，算是范围，可以使用索引

	like以通配符开头('%abc...')mysql索引失效会变成全表扫描的操作
  	问题：解决like '%字符串%'时索引不被使用的方法？？

## 优化8
	EXPLAIN SELECT name, age, pos  FROM staffs WHERE NAME = 917 ;

	EXPLAIN SELECT name, age, pos  FROM staffs WHERE NAME = '917' ;
	
	底层进行转换使索引失效，使用了函数造成索引失效
	
	字符串不加单引号索引失效    行锁变表锁
	
## 优化9
	 EXPLAIN SELECT name, age, pos  FROM staffs WHERE NAME = 'July' or age = 25;
	 
	 EXPLAIN SELECT name, age, pos  FROM staffs WHERE NAME = 'July' and  age = 25;
	 
	 少用or, 用它来连接时会索引失效
	

总结：
假设index(a,b,c)
Where语句	                                                    索引是否被使用
where a = 3	                                                  Y,使用到a
where a = 3 and b = 5	                                      Y,使用到a，b
where a = 3 and b = 5 and c = 4	                              Y,使用到a,b,c
where b = 3 或者 where b = 3 and c = 4  或者 where c = 4	   N
where a = 3 and c = 5	                                      使用到a， 但是c不可以，b中间断了
where a = 3 and b > 4 and c = 5	                              使用到a和b， c不能用在范围之后，b后断了
where a = 3 and b like 'kk%' and c = 4	                      Y,使用到a,b,c
where a = 3 and b like '%kk' and c = 4	                      Y,只用到a
where a = 3 and b like '%kk%' and c = 4	                      Y,只用到a
where a = 3 and b like 'k%kk%' and c = 4	                  Y,使用到a,b,c

可以不得已而为之
```



#### 单表优化

```
    -- 建表
    CREATE TABLE IF NOT EXISTS `article` (
    `id` INT(10) UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `author_id` INT(10) UNSIGNED NOT NULL,
    `category_id` INT(10) UNSIGNED NOT NULL,
    `views` INT(10) UNSIGNED NOT NULL,
    `comments` INT(10) UNSIGNED NOT NULL,
    `title` VARBINARY(255) NOT NULL,
    `content` TEXT NOT NULL
    );

    INSERT INTO `article`(`author_id`, `category_id`, `views`, `comments`, `title`, `content`) VALUES
    (1, 1, 1, 1, '1', '1'),
    (2, 2, 2, 2, '2', '2'),
    (1, 1, 3, 3, '3', '3');

    SELECT * FROM article;


    # 查询 category_id 为1 且  comments 大于 1 的情况下,views 最多的 article_id。 
    EXPLAIN SELECT id,author_id FROM article WHERE category_id = 1 AND comments > 1 ORDER BY views DESC LIMIT 1;
    # 结论：很显然, type 是 ALL, 即最坏的情况。Extra 里还出现了 Using filesort, 也是最坏的情况。优化是必须的。


    # 开始优化：
    # 1.1 新建索引+删除索引
    create index idx_article_ccv on article(category_id,comments,views);
    show index from article; 

    # 1.2 第2次EXPLAIN
    EXPLAIN SELECT id,author_id FROM `article` WHERE category_id = 1 AND comments > 1 ORDER BY views DESC LIMIT 1;

    #结论：
    #type 变成了 range, 这是可以忍受的。但是 extra 里使用 Using filesort 仍是无法接受的。
    #但是我们已经建立了索引,为啥没用呢?
    #这是因为按照 BTree 索引的工作原理,
    # 先排序 category_id,
    # 如果遇到相同的 category_id 则再排序 comments, 如果遇到相同的 comments 则再排序 views。
    #当 comments 字段在联合索引里处于中间位置时,
    #因 comments > 1 条件是一个范围值(所谓 range ),
    #MySQL 无法利用索引再对后面的 views 部分进行检索, 即 range 类型查询字段后面的索引无效。


    # 1.3 删除第一次建立的索引
    DROP INDEX idx_article_ccv ON article;

    # 1.4 第2次新建索引
    create index idx_article_cv on article(category_id, views);

    # 1.5 第3次EXPLAIN
    EXPLAIN SELECT id,author_id FROM article WHERE category_id = 1 AND comments > 1 ORDER BY views DESC LIMIT 1;
    #结论：可以看到,type 变为了 ref, Extra 中的 Using filesort 也消失了,结果非常理想。
```





#### 双表优化

```
    -- 建表
    CREATE TABLE IF NOT EXISTS `class` (
    `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
    `card` INT(10) UNSIGNED NOT NULL,
    PRIMARY KEY (`id`)
    );
    CREATE TABLE IF NOT EXISTS `book` (
    `bookid` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
    `card` INT(10) UNSIGNED NOT NULL,
    PRIMARY KEY (`bookid`)
    );

    INSERT INTO class(card) VALUES(FLOOR(1 + (RAND() * 20)));
    INSERT INTO class(card) VALUES(FLOOR(1 + (RAND() * 20)));
    INSERT INTO class(card) VALUES(FLOOR(1 + (RAND() * 20)));
    INSERT INTO class(card) VALUES(FLOOR(1 + (RAND() * 20)));
    INSERT INTO class(card) VALUES(FLOOR(1 + (RAND() * 20)));
    INSERT INTO class(card) VALUES(FLOOR(1 + (RAND() * 20)));
    INSERT INTO class(card) VALUES(FLOOR(1 + (RAND() * 20)));
    INSERT INTO class(card) VALUES(FLOOR(1 + (RAND() * 20)));
    INSERT INTO class(card) VALUES(FLOOR(1 + (RAND() * 20)));
    INSERT INTO class(card) VALUES(FLOOR(1 + (RAND() * 20)));
    INSERT INTO class(card) VALUES(FLOOR(1 + (RAND() * 20)));
    INSERT INTO class(card) VALUES(FLOOR(1 + (RAND() * 20)));
    INSERT INTO class(card) VALUES(FLOOR(1 + (RAND() * 20)));
    INSERT INTO class(card) VALUES(FLOOR(1 + (RAND() * 20)));
    INSERT INTO class(card) VALUES(FLOOR(1 + (RAND() * 20)));
    INSERT INTO class(card) VALUES(FLOOR(1 + (RAND() * 20)));
    INSERT INTO class(card) VALUES(FLOOR(1 + (RAND() * 20)));
    INSERT INTO class(card) VALUES(FLOOR(1 + (RAND() * 20)));
    INSERT INTO class(card) VALUES(FLOOR(1 + (RAND() * 20)));
    INSERT INTO class(card) VALUES(FLOOR(1 + (RAND() * 20)));


    INSERT INTO book(card) VALUES(FLOOR(1 + (RAND() * 20)));
    INSERT INTO book(card) VALUES(FLOOR(1 + (RAND() * 20)));
    INSERT INTO book(card) VALUES(FLOOR(1 + (RAND() * 20)));
    INSERT INTO book(card) VALUES(FLOOR(1 + (RAND() * 20)));
    INSERT INTO book(card) VALUES(FLOOR(1 + (RAND() * 20)));
    INSERT INTO book(card) VALUES(FLOOR(1 + (RAND() * 20)));
    INSERT INTO book(card) VALUES(FLOOR(1 + (RAND() * 20)));
    INSERT INTO book(card) VALUES(FLOOR(1 + (RAND() * 20)));
    INSERT INTO book(card) VALUES(FLOOR(1 + (RAND() * 20)));
    INSERT INTO book(card) VALUES(FLOOR(1 + (RAND() * 20)));
    INSERT INTO book(card) VALUES(FLOOR(1 + (RAND() * 20)));
    INSERT INTO book(card) VALUES(FLOOR(1 + (RAND() * 20)));
    INSERT INTO book(card) VALUES(FLOOR(1 + (RAND() * 20)));
    INSERT INTO book(card) VALUES(FLOOR(1 + (RAND() * 20)));
    INSERT INTO book(card) VALUES(FLOOR(1 + (RAND() * 20)));
    INSERT INTO book(card) VALUES(FLOOR(1 + (RAND() * 20)));
    INSERT INTO book(card) VALUES(FLOOR(1 + (RAND() * 20)));
    INSERT INTO book(card) VALUES(FLOOR(1 + (RAND() * 20)));
    INSERT INTO book(card) VALUES(FLOOR(1 + (RAND() * 20)));
    INSERT INTO book(card) VALUES(FLOOR(1 + (RAND() * 20)));


    # 下面开始explain分析
    EXPLAIN SELECT * FROM class LEFT JOIN book ON class.card = book.card;
    #结论：type 有All

    # 添加索引优化
    ALTER TABLE `book` ADD INDEX Y ( `card`);

    # 第2次explain
    EXPLAIN SELECT * FROM class LEFT JOIN book ON class.card = book.card;
    #可以看到第二行的 type 变为了 ref, rows 也变成了优化比较明显。
    #这是由左连接特性决定的。LEFT JOIN 条件用于确定如果从右表搜索行,左边一定都有,
    #所以右边是我们的关键点, 一定需要建立索引。


    # 删除旧索引 + 新建 + 第3次explain
    DROP INDEX Y ON book;
    ALTER TABLE class ADD INDEX X (card);
    EXPLAIN SELECT * FROM class LEFT JOIN book ON class.card = book.card;


    # 结论
    # 左连接 索引建在右表
    # 右连接 索引建在左表
    
    1、保证被驱动表的join字段已经被索引
    2、left join 时，选择小表(右边的表？)作为驱动表，大表作为被驱动表。
    3、inner join 时，mysql会自己帮你把小结果集的表选为驱动表。
    4、子查询尽量不要放在被驱动表，有可能使用不到索引。
```





#### order by调优

> 最左前缀
>
> 不要出现范围查询
>
> 设置mysql系统参数

```
	MySQL支持二种方式的排序，FileSort和Index，Index效率高. 它指MySQL扫描索引本身完成排序。FileSort方式效率较低。
	
	ORDER BY子句，尽量使用Index方式排序, 避免使用FileSort方式排序
  
  	ORDER BY满足两情况，会使用Index方式排序:
        1.ORDER BY 语句使用索引最左前缀
        2.使用Where子句与Order BY子句 条件列组合满足索引最左前列, where子句中不出现索引的范围查询(即explain中出现range，age > 20, 会导致 order by 索引失效) 
   	
   	 
    CREATE TABLE tblA(
      id int primary key not null auto_increment,
      age INT,
      birth TIMESTAMP NOT NULL,
      name varchar(200)
    );

    INSERT INTO tblA(age,birth,name) VALUES(22,NOW(),'abc');
    INSERT INTO tblA(age,birth,name) VALUES(23,NOW(),'bcd');
    INSERT INTO tblA(age,birth,name) VALUES(24,NOW(),'def');

    CREATE INDEX idx_A_ageBirth ON tblA(age,birth,name);

    SELECT * FROM tblA; 

    explain select * from  tblA order by age asc, birth desc;   //会产生filesort
      
    结论：
        尽可能在索引列上完成排序操作，遵照最佳左前缀
        如果不在索引列上，filesort有两种算法： mysql就要启动双路排序和单路排序(单路通常好于双路)， 优化策略：增大 sort_buffer_size, max_length_for_sort_data参数设置， 去掉select 中不需要的字段
```



#### group by调优

```
1.group by 实质是先排序后进行分组，遵照索引的最佳左前缀
2.当无法使用索引列，增大max_length_for_sort_data参数的设置 + 增大sort_buffer_size参数的设置
3.where 高于having， 能写在where限定的条件就不要去having限定了。
```



#### limit调优

```
  EXPLAIN  SELECT  SQL_NO_CACHE * FROM emp  ORDER  BY  deptno   LIMIT 10000,40
  
  那我们就给deptno这个字段加上索引吧
  create index emp on emp(deptno);
  
  EXPLAIN  SELECT  SQL_NO_CACHE * FROM emp  ORDER  BY  deptno LIMIT 10000,40
  然并卵。
 
  优化：
  	先利用覆盖索引把要取的数据行的主键取到，然后再用这个主键列与数据表做关联：(查询的数据量小了)
  EXPLAIN  SELECT  SQL_NO_CACHE * FROM emp INNER JOIN (SELECT id FROM emp e ORDER BY deptno LIMIT 10000,40) a ON a.id=emp.id

 实践证明：
    1. order by 后的字段（XXX）有索引
    2. sql 中有 limit 时
    
    当 select 后的字段  含有索引包含的字段时 ， 显示 using index
    当 select 后的字段  不含有索引包含的字段时，显示 using filesort
```



#### distinct调优

> 尽量不要使用 distinct 关键字去重

```
     id  shp_id    kcdz                
------  ------ --------------------
     3       1    北京市昌平区  
     4       1    北京市昌平区  
     5       5    北京市昌平区  
     6       3    重庆              
     8       8    天津              

例子：
select kcdz form t_mall_sku where id in( 3,4,5,6,8 )       //将产生重复数据

select distinct kcdz form t_mall_sku where id in( 3,4,5,6,8 )  //使用 distinct 关键字去重消耗性能
      
优化：
	select  kcdz form t_mall_sku where id in( 3,4,5,6,8 )  group by kcdz  // 能够利用到索引
```



#### 子查询调优

```
实验：
   
   有索引 大表驱动小表
    select sql_no_cache sum(sal) from emp where deptno in (select deptno from dept);
    select sql_no_cache sum(sal) from emp where exists (select 1 from dept where emp.deptno=dept.deptno);  ##用 exists 是否存在，存在返回一条记录，exists 是作为一个查询判断用，所以 select 后返回什么不重要。
    select sql_no_cache sum(sal) from emp inner  join dept on  emp.deptno=dept.deptno;

    有索引 小表驱动大表
    select sql_no_cache sum(e.sal) from (select * from emp where id<10000) e  where  exists (select 1 from  emp where e.deptno=emp.deptno);
    select sql_no_cache sum(e.sal) from (select * from emp where id<10000) e inner join (select distinct deptno from  emp) m on m.deptno=e.deptno;
     select sql_no_cache sum(sal) from emp where deptno in (select deptno from dept);

    无索引 小表驱动大表
    select sql_no_cache sum(e.sal) from (select * from emp where id<10000) e  where  exists (select 1 from  emp where e.deptno=emp.deptno);
    select sql_no_cache sum(e.sal) from (select * from emp where id<10000) e inner join (select distinct deptno from  emp) m on m.deptno=e.deptno;
     select sql_no_cache sum(sal) from emp where deptno in (select deptno from dept);

    无索引 大表驱动小表
    select sql_no_cache sum(sal) from emp where deptno in (select deptno from dept);
    select sql_no_cache sum(sal) from emp where exists (select 1 from dept where emp.deptno = dept.deptno);
    select sql_no_cache sum(sal) from emp inner join dept on  emp.deptno=dept.deptno;


结论：
        有索引的情况下 
        	用 inner join 是最好的, 其次是 in,  exists最糟糕

        无索引的情况下
        	小表驱动大表 因为 join 方式需要distinct, 没有索引distinct消耗性能较大, 所以exists性能最佳, in其次, join性能最差
        	
        	大表驱动小表, in 和 exists 的性能应该是接近的, in稍微好一点, 但是inner join 由于使用了 join buffer 所以快很多; 如果 left join 则最慢
```



### 1.3 慢查询

#### 基本概念

```
# 定义
超过long_query_time 定义的时间，就叫慢查询，默认值为10, 通常大于5s就是慢查询

# 查看是否开启及如何开启
  查看
    SHOW VARIABLES LIKE '%slow_query_log%';
    
  开启
  	// 使用set global slow_query_log=1 开启了慢查询日志只对当前数据库生效，如果MySQL重启后则会失效， 永久有效，需要更改my.conf 通常不这么干
    set global slow_query_log=1; 
    
  
# 使用
    查看当前多少秒算慢
      SHOW VARIABLES LIKE 'long_query_time%';

    设置慢的阙值时间（大于，不是大于等于）
      set global long_query_time=3;   //修改为阙值到3秒钟的就是慢sql

    为什么设置后看不出变化？
        需要重新连接或新开一个会话才能看到修改值。 SHOW VARIABLES LIKE 'long_query_time%';
     或者
        通过set session long_query_time=3来改变当前session变量;

    记录慢SQL并后续分析
		select sleep(10);
		
		tail -f xxx.log

    查询当前系统中有多少条慢查询记录
    	show global status like '%Slow_queries%';
    	
    	
   	#更改配置（一般不用）
   		mysqld
   			slow_query_log=1;
             slow_query_log_file=/var/lib/mysql/atguigu-slow.log
             long_query_time=3;
             log_output=FILE
```



#### mysqldumpslow

> 生产用

```
mysqldumpslow --help
	    s: 是表示按照何种方式排序；
        c: 访问次数
        l: 锁定时间
        r: 返回记录
        t: 查询行数
        al:平均锁定时间
        ar:平均返回记录数
        at:平均查询时间
        t:即为返回前面多少条的数据；
        g:后边搭配一个正则匹配模式，大小写不敏感的；
	
	常用参考：
	    得到返回记录集最多的10个SQL
        mysqldumpslow -s r -t 10 /var/lib/mysql/xx-slow.log

        得到访问次数最多的10个SQL
        mysqldumpslow -s c -t 10 /var/lib/mysql/xx-slow.log

        得到按照时间排序的前10条里面含有左连接的查询语句
        mysqldumpslow -s t -t 10 -g "left join" /var/lib/mysql/xx-slow.log

        另外建议在使用这些命令时结合 | 和more 使用 ，否则有可能出现爆屏情况
        mysqldumpslow -s r -t 10 /var/lib/mysql/xxx-slow.log | more


```



#### 批量插入1000w条数据

```

    # 建库
    create database bigData;
    use bigData;


    # 建表dept
    CREATE TABLE dept(  
    id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,  
    deptno MEDIUMINT UNSIGNED NOT NULL DEFAULT 0,   
    dname VARCHAR(20) NOT NULL DEFAULT "",  
    loc VARCHAR(13) NOT NULL DEFAULT ""  
    ) ENGINE=INNODB DEFAULT CHARSET=UTF8 ;  


    # 建表emp
    CREATE TABLE emp  
    (  
    id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,  
    empno MEDIUMINT UNSIGNED NOT NULL DEFAULT 0, /*编号*/  
    ename VARCHAR(20) NOT NULL DEFAULT "", /*名字*/  
    job VARCHAR(9) NOT NULL DEFAULT "",/*工作*/  
    mgr MEDIUMINT UNSIGNED NOT NULL DEFAULT 0,/*上级编号*/  
    hiredate DATE NOT NULL,/*入职时间*/  
    sal DECIMAL(7,2) NOT NULL,/*薪水*/  
    comm DECIMAL(7,2) NOT NULL,/*红利*/  
    deptno MEDIUMINT UNSIGNED NOT NULL DEFAULT 0 /*部门编号*/  
    )ENGINE=INNODB DEFAULT CHARSET=UTF8 ; 

	
	show variables like 'log_bin_trust_function_creators';
	
	set global log_bin_trust_function_creators=1;
	
	# 定义函数
	## 用于随机产生字符串
     DELIMITER $$
    CREATE FUNCTION rand_string(n INT) RETURNS VARCHAR(255)
    BEGIN   
     DECLARE chars_str VARCHAR(100) DEFAULT   'abcdefghijklmnopqrstuvwxyzABCDEFJHIJKLMNOPQRSTUVWXYZ'; 
     ##声明一个 字符窜长度为 100 的变量 chars_str ,默认值 
     DECLARE return_str VARCHAR(255) DEFAULT '';
     DECLARE i INT DEFAULT 0;
     ##循环开始
     WHILE i < n DO  
     SET return_str =CONCAT(return_str,SUBSTRING(chars_str,FLOOR(1+RAND()*52),1));
     ##concat 连接函数  ，substring(a,index,length) 从index处开始截取
     SET i = i + 1;
     END WHILE;
     RETURN return_str;
    END $$

    #假如要删除
    #drop function rand_string;


    ##用于随机产生部门编号
    DELIMITER $$
    CREATE FUNCTION rand_num( ) 
    RETURNS INT(5)  
    BEGIN   
     DECLARE i INT DEFAULT 0;  
     SET i = FLOOR(100+RAND()*10);  
    RETURN i;  
    END $$
   
   
   # 创建存储过程
      创建往emp表中插入数据的存储过程
      	DELIMITER $$
        CREATE PROCEDURE insert_emp10000(IN START INT(10),IN max_num INT(10))  
        BEGIN  
        DECLARE i INT DEFAULT 0;   
        #set autocommit =0 把autocommit设置成0  ；提高执行效率
         SET autocommit = 0;    
         REPEAT  ##重复
         SET i = i + 1;  
         INSERT INTO emp10000 (empno, ename ,job ,mgr ,hiredate ,sal ,comm ,deptno ) VALUES ((START+i) ,rand_string(6),'SALESMAN',0001,CURDATE(),FLOOR(1+RAND()*20000),FLOOR(1+RAND()*1000),rand_num());  
         UNTIL i = max_num   ##直到  上面也是一个循环
         END REPEAT;  ##满足条件后结束循环
         COMMIT;   ##执行完成后一起提交
         END $$
      
      创建往dept表中插入数据的存储过程
      	DELIMITER $$
        CREATE PROCEDURE insert_dept(IN START INT(10),IN max_num INT(10))  
        BEGIN  
        DECLARE i INT DEFAULT 0;   
         SET autocommit = 0;    
         REPEAT  
         SET i = i + 1;  
         INSERT INTO dept (deptno ,dname,loc ) VALUES (START +i ,rand_string(10),rand_string(8));  
         UNTIL i = max_num  
         END REPEAT;  
         COMMIT;  
         END $$ 
	
	# 调用存储过程
		# dept
		DELIMITER ;
		CALL insert_dept(100,10); 
		
		# 往emp表添加50万条数据
        DELIMITER ;    #将 结束标志换回 ;
        CALL insert_emp(100001,500000); 
        CALL insert_emp10000(100001,10000); 
```



#### show profiles

```
	Show  variables like 'profiling';
	
	set profiling=1;
	
    select * from emp group by id%10 limit 150000;
    select * from emp group by id%20  order by 5
      
    show profiles;   
    
   	show  profile cpu, block io for query n(n为上一步前面的问题SQL query_id);
            type:  
             | ALL              --显示所有的开销信息
             | BLOCK IO         --显示块IO相关开销  
             | CONTEXT SWITCHES --上下文切换相关开销  
             | CPU              --显示CPU相关开销信息  
             | IPC              --显示发送和接收相关开销信息  
             | MEMORY           --显示内存相关开销信息  
             | PAGE FAULTS      --显示页面错误相关开销信息  
             | SOURCE           --显示和Source_function，Source_file，Source_line相关的开销信息  
             | SWAPS            --显示交换次数相关开销的信息
	
	
	日常开发需要注意的4个指标：
      1.converting HEAP to MyISAM  查询结果太大，内存都不够用了往磁盘上搬了。
      2.Creating tmp table         创建临时表
        拷贝数据到临时表
        用完再删除
      3.Copying to tmp table on disk    把内存中临时表复制到磁盘，危险！！！
      4.locked
```



#### 全局查询日志

> 尽量不要在生产环境开启这个功能。

```
方式一，配置启用：
        在mysql的my.cnf中，设置如下：
            #开启
            general_log=1   
            # 记录日志文件的路径
            general_log_file=/path/logfile
            #输出格式
            log_output=FILE
        
方式二，编码启用：
        set global general_log=1;
        
        #全局日志可以存放到日志文件中，也可以存放到Mysql系统表中。存放到日志中性能更好一些，存储到表中
        set global log_output='TABLE';
        
        #此后你所编写的sql语句，将会记录到mysql库里的general_log表，可以用下面的命令查看
        select * from mysql.general_log;
```



## 2. 锁

> 和事务，事务隔离级别有关

### 2.1 概述

```
生活中购物，那么如何解决是你买到还是另一个人买到的问题？

这里肯定要用到事务，我们先从库存表中取出物品数量，然后插入订单，付款后插入付款表信息，然后更新商品数量。在这个过程中，使用锁可以对有限的资源进行保护，解决隔离和并发的矛盾。
```

### 2.2 分类

```
# 从对数据操作的类型（读\写）分
  读锁(共享锁)：针对同一份数据，多个读操作可以同时进行而不会互相影响。
  写锁（排它锁）：当前写操作没有完成前，它会阻断其他写锁和读锁。
  
# 从对数据操作的粒度分
  表锁
  行锁
  
  为了尽可能提高数据库的并发度，每次锁定的数据范围越小越好，理论上每次只锁定当前操作的数据的方案会得到最大的并发度，但是管理锁是很耗资源的事情（涉及获取，检查，释放锁等动作），因此数据库系统需要在高并发响应和系统性能两方面进行平衡，这样就产生了“锁粒度（Lock granularity）”的概念。
 
	一种提高共享资源并发发性的方式是让锁定对象更有选择性。尽量只锁定需要修改的部分数据，而不是所有的资源。更理想的方式是，只对会修改的数据片进行精确的锁定。任何时候，在给定的资源上，锁定的数据量越少，则系统的并发程度越高，只要相互之间不发生冲突即可。
```

### 2.3 表锁

```
# 特点
偏向MyISAM存储引擎，开销小，加锁快；无死锁；锁定粒度大，发生锁冲突的概率最高,并发度最低。

# 建表
 【表级锁分析--建表SQL】
create table mylock(
 id int not null primary key auto_increment,
 name varchar(20)
)engine myisam;
 
insert into mylock(name) values('a');
insert into mylock(name) values('b');
insert into mylock(name) values('c');
insert into mylock(name) values('d');
insert into mylock(name) values('e');
 
select * from mylock;
 
【手动增加表锁】
 lock table 表名字1 read(write)，表名字2 read(write)，其它;
 
【查看表上加过的锁】
 show open tables;    // in_use 为1的
 
【释放表锁】
 unlock tables;   

# 加读锁
详见word中的例子

# 加写锁
详见word中的例子


# 结论
MyISAM在执行查询语句（SELECT）前，会自动给涉及的所有表加读锁，在执行增删改操作前，会自动给涉及的表加写锁。 

MySQL的表级锁有两种模式：
 表共享读锁（Table Read Lock）
 表独占写锁（Table Write Lock）

 锁类型   他人可读	他人可写
 读锁	    是	   否
 写锁	    否	   否
 
结论：
  1、对MyISAM表的读操作（加读锁），不会阻塞其他进程对同一表的读请求，但会阻塞对同一表的写请求。只有当读锁释放后，才会执行其它进程的写操作。 
  
  2、对MyISAM表的写操作（加写锁），会阻塞其他进程对同一表的读和写操作，只有当写锁释放后，才会执行其它进程的读写操作。
  
  简而言之，就是读锁会阻塞写，但是不会堵塞读。而写锁则会把读和写都堵塞
```

### 2.4 行锁

```
# 特点
 偏向InnoDB存储引擎，开销大，加锁慢；会出现死锁；锁定粒度最小，发生锁冲突的概率最低,并发度也最高。
 
 InnoDB与MyISAM的最大不同有两点：一是支持事务（TRANSACTION）；二是采用了行级锁

# 建表
create table test_innodb_lock (a int(11),b varchar(16))engine=innodb;
 
insert into test_innodb_lock values(1,'b2');
insert into test_innodb_lock values(3,'3');
insert into test_innodb_lock values(4,'4000');
insert into test_innodb_lock values(5,'5000');
insert into test_innodb_lock values(6,'6000');
insert into test_innodb_lock values(7,'7000');
insert into test_innodb_lock values(8,'8000');
insert into test_innodb_lock values(9,'9000');
insert into test_innodb_lock values(1,'b1');
 
create index test_innodb_a_ind on test_innodb_lock(a);
 
create index test_innodb_lock_b_ind on test_innodb_lock(b);
 
select * from test_innodb_lock;



# 演示
参考word 
set autocommit =0 ;
update xxx 
commit;

# 无索引行锁升级为表锁
参考word，由于在column字段b上面建了索引， 如果没有正常使用，会导致行锁变表锁, 比如没加单引号导致索引失效，行锁变表锁	
# 正常
update test_innodb_lock set b = '2' where b = '1000'
# 行锁变表锁	
update test_innodb_lock set b = '2' where b = 1000



# select加锁
  读锁
   select ..lock in share mode    // 共享锁(Share Lock)  读锁
   共享锁又称读锁，是读取操作创建的锁。其他用户可以并发读取数据，但任何事务都不能对数据进行修改（获取数据上的排他锁），直到已释放所有共享锁。 如果事务T对数据A加上共享锁后，则其他事务只能对A再加共享锁，不能加排他锁。获准共享锁的事务只能读数据，不能修改数据。
   
   在查询语句后面增加 LOCK IN SHARE MODE, **Mysql会对查询结果中的每行都加共享锁**，当没有其他线程对查询结果集中的任何一行使用排他锁时，可以成功申请共享锁，否则会被阻塞。其他线程也可以读取使用了共享锁的表（行？），而且这些线程读取的是同一个版本的数据
   
 
  写锁
	select... for update   排他锁（eXclusive Lock）
	排他锁又称写锁，如果事务T对数据A加上排他锁后，则其他事务不能再对A加任任何类型的封锁。获准排他锁的事务既能读数据，又能修改数据
	
	在查询语句后面增加 FOR UPDATE ，**Mysql会对查询结果中的每行都加排他锁**，当没有其他线程对查询结果集中的任何一行使用排他锁时，可以成功申请排他锁，否则会被阻塞
	

# 间隙锁
【定义】
当我们用范围条件而不是相等条件检索数据，并请求共享或排他锁时，InnoDB会给符合条件的已有数据记录的索引项加锁；对于键值在条件范围内但并不存在的记录，叫做“间隙（GAP)”，
InnoDB也会对这个“间隙”加锁，这种锁机制就是所谓的间隙锁（GAP Lock）。

 
【危害】
因为Query执行过程中通过过范围查找的话，他会锁定整个范围内所有的索引键值，即使这个键值并不存在。
间隙锁有一个比较致命的弱点，就是当锁定一个范围键值之后，即使某些不存在的键值也会被无辜的锁定，而造成在锁定的时候无法插入锁定键值范围内的任何数据。在某些场景下这可能会对性能造成很大的危害

session1 										   session2
set autocommit = 0;
update test set b = a * 20 where id > 1 and id <10;    insert into test values(2, "200");

commit ;                                               完成插入


# 行锁分析
通过检查InnoDB_row_lock状态变量来分析系统上的行锁的争夺情况
show status like 'innodb_row_lock%';

对各个状态量的说明如下：
Innodb_row_lock_current_waits：当前正在等待锁定的数量；
Innodb_row_lock_time：从系统启动到现在锁定总时间长度；
Innodb_row_lock_time_avg：每次等待所花平均时间；
Innodb_row_lock_time_max：从系统启动到现在等待最常的一次所花的时间；
Innodb_row_lock_waits：系统启动后到现在总共等待的次数；

比较重要的主要是：
Innodb_row_lock_time_avg（等待平均时长）
Innodb_row_lock_waits（等待总次数）
Innodb_row_lock_time（等待总时长）

尤其是当等待次数很高，而且每次等待时长也不小的时候，我们就需要分析系统中为什么会有如此多的等待，然后根据分析结果着手指定优化计划。
 
最后可以通过下面来查询正在被锁阻塞的sql语句
	SELECT * FROM information_schema.INNODB_TRX\G;
```



### 2.5 页面锁

```
介于表锁和行锁之间的一种锁
```







##  3. 分库分表

> https://blog.csdn.net/u014635472/article/details/79720876
>
> https://www.cnblogs.com/GrimMjx/p/10526821.html              // 分区

### 3.1 分表
#### 3.1.1 水平分表

```
分表策略：通常是用户ID取模，如果不是整数，可以首先将其进行hash获取到整。 
主要解决：解决mysql并发问题


水平分表遇到的问题：
1. 跨表直接连接查询无法进行
2. 我们需要统计数据的时候
3. 如果数据持续增长，达到现有分表的瓶颈，需要增加分表，此时会出现数据重新排列的情况

水平分表解决方案：
1. 第1，2点可以通过增加汇总的冗余表，虽然数据量很大，但是可以用于后台统计或者查询时效性比较底的情况，而且我们可以提前算好某个时间点或者时间段的数据

2. 第3点解决建议：
    1. 可以开始的时候，就分析大概的数据增长率，来大概确定未来某段时间内的数据总量，从而提前计算出未来某段时间内需要用到的分表的个数
    2. 考虑表分区，在逻辑上面还是一个表名，实际物理存储在不同的物理地址上
    3. 分库
```

![](imgs\1-水平拆分.png)



#### 3.1.2 垂直分表

```
垂直拆分原则：
1. 把大字段独立存储到一张表中
2. 把不常用的字段单独拿出来存储到一张表
3. 把经常在一起使用的字段可以拿出来单独存储到一张表
```

![](imgs\2-垂直拆分.png)



```
垂直拆分标准：
1.表的体积大于2G并且行数大于1千万
2.表中包含有text，blob，varchar(1000)以上
3.数据有时效性的，可以单独拿出来归档处理


/*表的体积计算*/
分表前体积：
CREATE TABLE `test1` (
id bigint(20) not null auto_increment,
detail varchar(2000),
createtime  datetime,
validity int default '0',
primary key (id)
);

1000万条数据 bigint 8字节、varchar 2000字节、 datetime  8字节、validity 4字节
(8+2000+8+4) * 10000000 = 20200000000 字节 == 18G


分表后体积：
CREATE TABLE `test1` (
id int not null auto_increment,
createtime  timestamp,
validity tinyint default 0,
primary key (id)
);

(4+4+1) * 10000000 =  0.08G
```



### 3.2 分区

```
定义：分区呢就是把一张表的数据分成N多个区块，这些区块可以在同一个磁盘上，也可以在不同的磁盘上，从逻辑来看还是一个大表。最大分1024，一般分100左右比较适合。 通常按照时间范围分区

主要解决：解决磁盘io的读写问题, 从而达到提高mysql性能的目的

使用场景：
 	1.对于数据量比较大，但是并发不是很多的情况下，可以采用表分区。
    2.对于数据量比较大，但是并发也比较高的情况下，可以采用分表和分区相结合。

/*range分区*/
create table test_range(
	id int not null default 0
)engine=myisam default charset=utf8
partition by range(id)(
partition p1 values less than (3),
partition p2 values less than (5),
partition p3 values less than maxvalue
);

/*hash分区*/
create table test_hash(
id int not null default 0
)engine=innodb default charset=utf8
partition by hash(id) partitions 10;

/*线性hash分区*/
create table test_linear(
	id int not null default 0
)engine=innodb default charset=utf8
partition by linear hash(id) partitions 10;

/* list分区*/
create table test_list(
	id int not null
) engine=innodb default charset=utf8
partition by list(id)(
partition p0 values in (3,5),
partition p1 values in (2,6,7,9)
);

/* key 分区 */
CREATE TABLE test_key (
    col1 INT NOT NULL
)
PARTITION BY  linear KEY (col1)
PARTITIONS 10;

普通的hash分区  			增加分区后，需要重新计算
线性hash分区（了解）      增加分区后，还是在原来的分区
线性hash 相对于 hash分区  没有那么均匀
Key分区用的比较少，也是hash分区
```



### 3.3 分库

```
分库策略与分表策略的实现很相似，最简单的都是可以通过取模(userID散列、按性别、按省)的方式进行路由(水平切分)；分库也可以按照业务(功能模块)分库，比如订单表和库存表在两个库，要注意处理好跨库事务(垂直切分)。

MERGE引擎	

场景：
	1. 单实例(单机)无法支撑

分表和分库 同时实现。
分库分表的策略相对于前边两种复杂一些，一种常见的路由策略如下：
１、中间变量　＝ user_id%（库数量*每个库的表数量）;
２、库序号　＝　取整（中间变量／每个库的表数量）;
３、表序号　＝　取余（中间变量％每个库的表数量）;

例如：数据库有256个，每一个库中有1024个数据表，用户的user_id＝262145，按照上述的路由策略，可得：
１、中间变量　＝ 262145%（256*1024）= 1;
２、库序号　＝　取整（1／1024）= 0;
３、表序号　＝　1％1024 = 1;
这样的话，对于user_id＝262145，将被路由到第０个数据库的第１个表中。


分库分表标准：
    存储占用100G+
    数据增量每天200w+
    单表条数1亿条+
    
分库分表字段：
　　分库分表字段取值非常重要
        在大多数场景该字段是查询字段
        数值型
　　一般使用userId，可以满足上述条件

常见中间件：
	proxy和客户端式架构。
        proxy模式有MyCat(国内活跃度最高)、DBProxy(美团)， my-proxy等，
        客户端式架构有TDDL(taobao)、Sharding-JDBC(当当应用框架ddframe中)等。
        
	proxy和客户端的区别：
    	proxy模式的话我们的select和update语句都是发送给代理，由这个代理来操作具体的底层数据库。所以必须要求代理本身需要保证高可用，否则数据库没有宕机，proxy挂了，那就走远了。

　　	   客户端模式通常在连接池上做了一层封装，内部与不同的库连接，sql交给smart-client进行处理。通常仅支持一种语言，如果其他语言要使用，需要开发多语言客户端。
　
 
常见问题：
	1. 分布式事务
		seaga, TCC模式就属于柔性事务。
		
	2. 跨表join
		tddl、MyCAT等都支持跨分片join。但是尽力避免跨库join，比如通过字段冗余的方式解决
	
	
```



### 3.4 分片

```
分片就是 分库 + 分表

数据库分片是将一张分布式表按照指定的分片键(Partition Key)和分片模式(Partition Mode)水平拆分成多个数据片，分散在多个数据存储节点中。

分片键:
对于分片的表，要选取一个分片键。
一张分布式表只能有一个分片键，分片键是用于划分和定位表的列，不能修改。

分片模式:
•枚举/列表List
{1 => Cluster A, 2 => Cluster B}

•范围Range (仅支持数字或ASCII字符串类型的分片键)
{[1 - 100] => Cluster A, [101 - 199] => Cluster B}

•散列Hash (仅支持数字或ASCII字符串类型的分片键)
{1024n + 1 => Cluster A, 1024n + 2 => Cluster B}

分片方式类似于分区方式，可以选择枚举，范围Range或者散列哈希。不同的是分片不支持时间range。

分片策略:
在做分片的时候，选择合适的分片规则非常重要，将极大地避免后续数据的处理难度，有以下几点需要关注：
1. 能不分就不分，对于1000万以内的表，不建议分片，通过合适的索引，读写分离等方式，可以更好地解决性能问题。
2. 分片数量不是越多越好，并且尽量均匀分布在多个存储节点上，只在必要的时候进行扩容，增加分片数量。
3. 分片键不能为空，不能修改，所以要选择表中中最常用且不变的字段。
4. 分片键选择时尽量做到可以将事务控制在分片范围内，可以避免出现跨分片的操作。
5. 选择分片规则时，要充分考虑数据的增长模式，数据的访问模式，分片关联性问题，以及分片扩容问题。

	总体上来说，分片的选择是取决于最频繁的查询 SQL 的条件。找出每个表最频繁的SQL，分析其查询条件，以及相互的关系，并结合 ER 图，就能比较准确的选择每个表的分片策略。

如果这些准则你觉得非常麻烦,可以使用一些集成工具,例如oneproxy, mycat等工具来完成数据库的分片.
mycat 实现分库分表
https://blog.csdn.net/kk185800961/article/details/51147029
```



### 3.5 区别

#### 3.5.1 分表和分区

```
1.数据处理上
mysql的分表是真正的分表，一张表分成很多表后，每一个小表都是完正的一张表，都对应三个文件，一个.MYD数据文件，.MYI索引文件，.frm表结构文件。

分区不一样，一张大表进行分区后，他还是一张表，不会变成二张表，但是他存放数据的区块变多了。

2.提高性能上
	 分表后，提高并发能力，从而使mysql性能提高
	 分区后，提高读写性能，提高mysql的性能
```



#### 3.5.2 分区和分库分表

```
　　区别于分区的是，分区一般都是放在单机里的，用的比较多的是时间范围分区，方便归档。只不过分库分表需要代码实现，分区则是mysql内部实现。分库分表和分区并不冲突，可以结合使用。
```



### 3.6 mycat

```
参考mysql下的mycat.html（有道云笔记也有）
```

