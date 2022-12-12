# xorm

## 1. 文档

```
http://xorm.topgoer.com/                        //推荐

https://gitea.com/xorm/xorm#
```



## 2. 简介

xorm是一个简单而强大的Go语言ORM库. 通过它可以使数据库操作非常简便。xorm的目标并不是让你完全不去学习SQL，我们认为SQL并不会为ORM所替代，但是ORM将可以解决绝大部分的简单SQL需求。xorm支持两种风格的混用。



### 2.1 特性

- 支持Struct和数据库表之间的灵活映射，并支持自动同步
- 事务支持
- 同时支持原始SQL语句和ORM操作的混合执行
- 使用连写来简化调用
- 支持使用Id, In, Where, Limit, Join, Having, Table, SQL, Cols等函数和结构体等方式作为条件
- 支持级联加载Struct
- Schema支持（仅Postgres）
- 支持缓存
- 支持根据数据库自动生成xorm的结构体
- 支持记录版本（即乐观锁）
- 内置SQL Builder支持
- 通过EngineGroup支持读写分离和负载均衡



### 2.2 支持的数据库

xorm当前支持的驱动和数据库如下：

- Mysql: [github.com/go-sql-driver/mysql](https://github.com/go-sql-driver/mysql)
- MyMysql: [github.com/ziutek/mymysql/godrv](https://github.com/ziutek/mymysql/godrv)
- Postgres: [github.com/lib/pq](https://github.com/lib/pq)
- Tidb: [github.com/pingcap/tidb](https://github.com/pingcap/tidb)
- SQLite: [github.com/mattn/go-sqlite3](https://github.com/mattn/go-sqlite3)
- MsSql: [github.com/denisenkom/go-mssqldb](https://github.com/denisenkom/go-mssqldb)
- MsSql: [github.com/lunny/godbc](https://github.com/lunny/godbc)
- Oracle: [github.com/mattn/go-oci8](https://github.com/mattn/go-oci8) (试验性支持)
- ql: [github.com/cznic/ql](https://github.com/cznic/ql) (试验性支持)



### 2.3 安装

```go
go get xorm.io/xorm
```



### 2.4 文档

- [GoWalker代码文档](http://gowalker.org/github.com/go-xorm/xorm)
- [Godoc代码文档](http://godoc.org/github.com/go-xorm/xorm)





## 3. 创建orm引擎

> Engine Group 引擎用于对读写分离的数据库或者负载均衡的数据库进行操作

所有操作均需要事先创建并配置 ORM 引擎才可以进行。

XORM支持两种 ORM 引擎，即 Engine 引擎和 Engine Group 引擎。

Engine 引擎用于对单个数据库进行操作，**Engine Group 引擎用于对读写分离的数据库或者负载均衡的数据库进行操作**。

Engine 引擎和 EngineGroup 引擎的API基本相同，所有适用于 Engine 的API基本上都适用于 EngineGroup，并且可以比较容易的从 Engine 引擎迁移到 EngineGroup引擎。



### 3.1 创建Engine引擎

单个ORM引擎，也称为Engine。一个APP可以同时存在多个Engine引擎，一个Engine一般只对应一个数据库。Engine通过调用`xorm.NewEngine`生成，如：

```Go
import (
    _ "github.com/go-sql-driver/mysql"
    "github.com/go-xorm/xorm"
)

var engine *xorm.Engine

func main() {
    var err error
    engine, err = xorm.NewEngine("mysql", "root:123@/test?charset=utf8")
}
```

or

```Go
import (
    _ "github.com/mattn/go-sqlite3"
    "github.com/go-xorm/xorm"
)

var engine *xorm.Engine

func main() {
    var err error
    engine, err = xorm.NewEngine("sqlite3", "./test.db")
}
```

- 一般情况下如果只操作一个数据库，只需要创建一个`engine`即可。**`engine`是GoRoutine安全的**。

- 创建完成`engine`之后，并没有立即连接数据库，此时可以通过`engine.Ping()`来进行数据库的连接测试是否可以连接到数据库。另外对于某些数据库有连接超时设置的，可以通过起一个定期Ping的Go程来保持连接鲜活。

- **对于有大量数据并且需要分区的应用，也可以根据规则来创建多个Engine**，比如：

```Go
var err error
for i:=0;i<5;i++ {
    engines[i], err = xorm.NewEngine("sqlite3", fmt.Sprintf("./test%d.db", i))
}
```

- engine可以通过`engine.Close`来手动关闭，但是一般情况下可以不用关闭，在程序退出时会自动关闭。



NewEngine传入的参数和`sql.Open`传入的参数完全相同，因此，在使用某个驱动前，请查看此驱动中关于传入参数的说明文档。以下为各个驱动的连接符对应的文档链接：

- [sqlite3](http://godoc.org/github.com/mattn/go-sqlite3#SQLiteDriver.Open)
- [mysql dsn](https://github.com/go-sql-driver/mysql#dsn-data-source-name)
- [mymysql](http://godoc.org/github.com/ziutek/mymysql/godrv#Driver.Open)
- [postgres](http://godoc.org/github.com/lib/pq)



#### 3.1.1 设置日志

日志是一个接口，通过设置日志，可以显示SQL，警告以及错误等，默认的显示级别为INFO。

- `engine.ShowSQL(true)`，则会在控制台打印出生成的SQL语句；
- `engine.Logger().SetLevel(core.LOG_DEBUG)`，则会在控制台打印调试及以上的信息；

如果希望将信息不仅打印到控制台，而是保存为文件，那么可以通过类似如下的代码实现，`NewSimpleLogger(w io.Writer)`接收一个io.Writer接口来将数据写入到对应的设施中。

```Go
f, err := os.Create("sql.log")
if err != nil {
    println(err.Error())
    return
}
engine.SetLogger(xorm.NewSimpleLogger(f))
```

当然，如果希望将日志记录到syslog中，也可以如下：

```Go
logWriter, err := syslog.New(syslog.LOG_DEBUG, "rest-xorm-example")
if err != nil {
    log.Fatalf("Fail to create xorm system logger: %v\n", err)
}

logger := xorm.NewSimpleLogger(logWriter)
logger.ShowSQL(true)
engine.SetLogger(logger)
```



#### 3.1.2 设置连接池

engine内部支持连接池接口和对应的函数。

- 如果需要设置连接池的空闲数大小，可以使用`engine.SetMaxIdleConns()`来实现。
- 如果需要设置最大打开连接数，则可以使用`engine.SetMaxOpenConns()`来实现。





### 3.2 创建Engine Group引擎

通过创建引擎组EngineGroup来实现对从数据库(Master/Slave)读写分离的支持。在创建引擎章节中，我们已经介绍过了，在xorm里面，可以同时存在多个Orm引擎，一个Orm引擎称为Engine，一个Engine一般只对应一个数据库，而EngineGroup一般则对应一组数据库。EngineGroup通过调用xorm.NewEngineGroup生成，如：

```Go
import (
    _ "github.com/lib/pq"
    "github.com/xormplus/xorm"
)

var eg *xorm.EngineGroup

func main() {
    conns := []string{
        "postgres://postgres:root@localhost:5432/test?sslmode=disable;", // 第一个默认是master
        "postgres://postgres:root@localhost:5432/test1?sslmode=disable;", // 第二个开始都是slave
        "postgres://postgres:root@localhost:5432/test2?sslmode=disable",
    }

    var err error
    eg, err = xorm.NewEngineGroup("postgres", conns)
}
```

或者

```Go
import (
    _ "github.com/lib/pq"
    "github.com/xormplus/xorm"
)

var eg *xorm.EngineGroup

func main() {
    var err error
    master, err := xorm.NewEngine("postgres", "postgres://postgres:root@localhost:5432/test?sslmode=disable")
    if err != nil {
        return
    }

    slave1, err := xorm.NewEngine("postgres", "postgres://postgres:root@localhost:5432/test1?sslmode=disable")
    if err != nil {
        return
    }

    slave2, err := xorm.NewEngine("postgres", "postgres://postgres:root@localhost:5432/test2?sslmode=disable")
    if err != nil {
        return
    }

       slaves := []*xorm.Engine{slave1, slave2}
    eg, err = xorm.NewEngineGroup(master, slaves)
}
```

创建完成EngineGroup之后，并没有立即连接数据库，此时可以通过eg.Ping()来进行数据库的连接测试是否可以连接到数据库，该方法会依次调用引擎组中每个Engine的Ping方法。另外对于某些数据库有连接超时设置的，可以通过起一个定期Ping的Go程来保持连接鲜活。EngineGroup可以通过eg.Close()来手动关闭，但是一般情况下可以不用关闭，在程序退出时会自动关闭。

- NewEngineGroup方法

```Go
func NewEngineGroup(args1 interface{}, args2 interface{}, policies ...GroupPolicy) (*EngineGroup, error)
```

前两个参数的使用示例如上，有两种模式。 

模式一：通过给定DriverName，DataSourceName来创建引擎组，每个引擎使用相同的Driver。每个引擎的DataSourceNames是[]string类型，第一个元素是Master的DataSourceName，之后的元素是Slave的DataSourceName。 

模式二：通过给定*xorm.Engine，[]*xorm.Engine来创建引擎组，每个引擎可以使用不同的Driver。第一个参数为Master的*xorm.Engine，第二个参数为Slave的[]*xorm.Engine。 NewEngineGroup方法，第三个参数为policies，为Slave给定负载策略，该参数将在负载策略章节详细介绍，如示例中未指定，则默认为轮询负载策略。



- Master方法

  ```Go
  func (eg *EngineGroup) Master() *Engine
  ```

  返回Master数据库引擎

  

- Slave方法

  ```Go
  func (eg *EngineGroup) Slave() *Engine
  ```

  依据给定的负载策略返回一个Slave数据库引擎

  

- Slaves方法

  ```Go
  func (eg *EngineGroup) Slaves() []*Engine
  ```

  返回所以Slave数据库引擎

  

- GetSlave方法

  ```Go
  func (eg *EngineGroup) GetSlave(i int) *Engine
  ```

  依据一组Slave数据库引擎[]*xorm.Engine下标返回指定Slave数据库引擎。通过给定DriverName，DataSourceName来创建引擎组，则DataSourceName的第二个元素的数据库为下标0的Slave数据库引擎。

  

- SetPolicy方法

  ```Go
  func (eg *EngineGroup) SetPolicy(policy GroupPolicy) *EngineGroup
  ```

  设置引擎组负载策略



### 3.3 EngineGroup负载策略

通过xorm.NewEngineGroup创建EngineGroup时，第三个参数为policies，我们可以通过该参数来指定Slave访问的负载策略。如创建EngineGroup时未指定，则默认使用轮询的负载策略。

xorm中内置五种负载策略，分别为随机访问负载策略，权重随机访问负载策略，轮询访问负载策略，权重轮询访问负载策略和最小连接数访问负载策略。开发者也可以通过实现GroupPolicy接口，来实现自定义负载策略。



#### 3.3.1 随机访问

```Go
import (
    _ "github.com/lib/pq"
    "github.com/xormplus/xorm"
)

var eg *xorm.EngineGroup

func main() {
    conns := []string{
        "postgres://postgres:root@localhost:5432/test?sslmode=disable;",
        "postgres://postgres:root@localhost:5432/test1?sslmode=disable;",
        "postgres://postgres:root@localhost:5432/test2?sslmode=disable",
    }

    var err error
    eg, err = xorm.NewEngineGroup("postgres", conns, xorm.RandomPolicy())
}
```

#### 3.3.2 权重随机访问

```Go
import (
    _ "github.com/lib/pq"
    "github.com/xormplus/xorm"
)

var eg *xorm.EngineGroup

func main() {
    conns := []string{
        "postgres://postgres:root@localhost:5432/test?sslmode=disable;",
        "postgres://postgres:root@localhost:5432/test1?sslmode=disable;",
        "postgres://postgres:root@localhost:5432/test2?sslmode=disable",
    }

    var err error
    //此时设置的test1数据库和test2数据库的随机访问权重为2和3
    eg, err = xorm.NewEngineGroup("postgres", conns, xorm.WeightRandomPolicy([]int{2, 3}))
}
```

#### 3.3.3 轮询访问

```Go
import (
    _ "github.com/lib/pq"
    "github.com/xormplus/xorm"
)

var eg *xorm.EngineGroup

func main() {
    conns := []string{
        "postgres://postgres:root@localhost:5432/test?sslmode=disable;",
        "postgres://postgres:root@localhost:5432/test1?sslmode=disable;",
        "postgres://postgres:root@localhost:5432/test2?sslmode=disable",
    }

    var err error
    eg, err = xorm.NewEngineGroup("postgres", conns, xorm.RoundRobinPolicy())
}
```

#### 3.3.4 权重轮询访问

```Go
import (
    _ "github.com/lib/pq"
    "github.com/xormplus/xorm"
)

var eg *xorm.EngineGroup

func main() {
    conns := []string{
        "postgres://postgres:root@localhost:5432/test?sslmode=disable;",
        "postgres://postgres:root@localhost:5432/test1?sslmode=disable;",
        "postgres://postgres:root@localhost:5432/test2?sslmode=disable",
    }

    var err error
    //此时设置的test1数据库和test2数据库的轮询访问权重为2和3
    eg, err = xorm.NewEngineGroup("postgres", conns, xorm.WeightRoundRobinPolicy([]int{2, 3}))
}
```

- 最小连接数访问负载策略

```Go
import (
    _ "github.com/lib/pq"
    "github.com/xormplus/xorm"
)

var eg *xorm.EngineGroup

func main() {
    conns := []string{
        "postgres://postgres:root@localhost:5432/test?sslmode=disable;",
        "postgres://postgres:root@localhost:5432/test1?sslmode=disable;",
        "postgres://postgres:root@localhost:5432/test2?sslmode=disable",
    }

    var err error
    eg, err = xorm.NewEngineGroup("postgres", conns, xorm.LeastConnPolicy())
}
```

#### 3.3.5 自定义负载策略

你也可以通过实现 GroupPolicy 接口来实现自定义负载策略。

```Go
type GroupPolicy interface {
    Slave(*EngineGroup) *Engine
}
```



## 4. 表结构

xorm支持将一个struct映射为数据库中对应的一张表。映射规则可以查看：[名称映射规则](http://xorm.topgoer.com/chapter-02/chapter-02/1.mapping.md)。



### 4.1 名称映射规则

名称映射规则主要负责结构体名称到表名和结构体field到表字段的名称映射。由core.IMapper接口的实现者来管理，xorm内置了三种IMapper实现：`core.SnakeMapper` ， `core.SameMapper`和`core.GonicMapper`。

- SnakeMapper 支持struct为驼峰式命名，表结构为下划线命名之间的转换，这个是默认的Maper；
- SameMapper 支持结构体名称和对应的表名称以及结构体field名称与对应的表字段名称相同的命名；
- GonicMapper 和SnakeMapper很类似，但是对于特定词支持更好，比如ID会翻译成id而不是i_d。

当前SnakeMapper为默认值，如果需要改变时，在engine创建完成后使用

```Go
engine.SetMapper(core.SameMapper{})
```

同时需要注意的是：

- 如果你使用了别的命名规则映射方案，也可以自己实现一个IMapper。
- 表名称和字段名称的映射规则默认是相同的，当然也可以设置为不同，如：

```Go
engine.SetTableMapper(core.SameMapper{})
engine.SetColumnMapper(core.SnakeMapper{})
```

When a struct auto mapping to a database's table, the below table describes how they change to each other:

| go type's kind                                       | value method                        | xorm type    |
| ---------------------------------------------------- | ----------------------------------- | ------------ |
| implemented Conversion                               | Conversion.ToDB / Conversion.FromDB | Text         |
| int, int8, int16, int32, uint, uint8, uint16, uint32 |                                     | Int          |
| int64, uint64                                        |                                     | BigInt       |
| float32                                              |                                     | Float        |
| float64                                              |                                     | Double       |
| complex64, complex128                                | json.Marshal / json.UnMarshal       | Varchar(64)  |
| []uint8                                              |                                     | Blob         |
| array, slice, map except []uint8                     | json.Marshal / json.UnMarshal       | Text         |
| bool                                                 | 1 or 0                              | Bool         |
| string                                               |                                     | Varchar(255) |
| time.Time                                            |                                     | DateTime     |
| cascade struct                                       | primary key field value             | BigInt       |
|                                                      |                                     |              |
| struct                                               | json.Marshal / json.UnMarshal       | Text         |
| Others                                               |                                     | Text         |



### 4.2 前缀映射等改变名称映射

> 前缀映射，后缀映射和缓存映射

- 通过 `core.NewPrefixMapper(core.SnakeMapper{}, "prefix")` 可以创建一个在SnakeMapper的基础上在命名中添加统一的前缀，当然也可以把SnakeMapper{}换成SameMapper或者你自定义的Mapper。

  例如，如果希望所有的表名都在结构体自动命名的基础上加一个前缀而字段名不加前缀，则可以在engine创建完成后执行以下语句：

  ```
  tbMapper := core.NewPrefixMapper(core.SnakeMapper{}, "prefix_")
  engine.SetTableMapper(tbMapper)
  ```

  执行之后，结构体 `type User struct` 默认对应的表名就变成了 `prefix_user` 了，而之前默认的是 `user`

  

- 通过 `core.NewSuffixMapper(core.SnakeMapper{}, "suffix")` 可以创建一个在SnakeMapper的基础上在命名中添加统一的后缀，当然也可以把SnakeMapper换成SameMapper或者你自定义的Mapper。

  

- 通过 `core.NewCacheMapper(core.SnakeMapper{})` 可以创建一个组合了其它的映射规则，起到在内存中缓存曾经映射过的命名映射。

### 4.3 Table和Tag改变名称映射

如果所有的命名都是按照IMapper的映射来操作的，那当然是最理想的。但是如果碰到某个表名或者某个字段名跟映射规则不匹配时，我们就需要别的机制来改变。xorm提供了如下几种方式来进行：

- 如果结构体拥有`TableName() string`的成员方法，那么此方法的返回值即是该结构体对应的数据库表名。
- 通过`engine.Table()`方法可以改变struct对应的数据库表的名称，通过sturct中field对应的Tag中使用`xorm:"'column_name'"`可以使该field对应的Column名称为指定名称。这里使用两个单引号将Column名称括起来是为了防止名称冲突，因为我们在Tag中还可以对这个Column进行更多的定义。如果名称不冲突的情况，单引号也可以不使用。

到此名称映射的所有方法都给出了，一共三种方式，这三种是有优先级顺序的。

- 表名的优先级顺序如下：
  - `engine.Table()` 指定的临时表名优先级最高
  - `TableName() string` 其次
  - `Mapper` 自动映射的表名优先级最后
- 字段名的优先级顺序如下：
  - 结构体tag指定的字段名优先级较高
  - `Mapper` 自动映射的表名优先级较低



### 4.4 属性定义

我们在field对应的Tag中对Column的一些属性进行定义，定义的方法基本和我们写SQL定义表结构类似，比如：

```go
type User struct {
    Id   int64
    Name string  `xorm:"varchar(25) notnull unique 'usr_name' comment('姓名')"`
}
```

对于不同的数据库系统，数据类型其实是有些差异的。因此xorm中对数据类型有自己的定义，基本的原则是尽量兼容各种数据库的字段类型，具体的字段对应关系可以查看[字段类型对应表](http://xorm.topgoer.com/chapter-02/5.types.html)。对于使用者，一般只要使用自己熟悉的数据库字段定义即可。

具体的Tag规则如下，另Tag中的关键字均不区分大小写，但字段名根据不同的数据库是区分大小写：

| name                                             | 当前field对应的字段的名称，可选，如不写，则自动根据field名字和转换规则命名，如与其它关键字冲突，请使用单引号括起来。 |
| ------------------------------------------------ | ------------------------------------------------------------ |
| pk                                               | 是否是Primary Key，如果在一个struct中有多个字段都使用了此标记，则这多个字段构成了复合主键，单主键当前支持int32,int,int64,uint32,uint,uint64,string这7种Go的数据类型，复合主键支持这7种Go的数据类型的组合。 |
| 当前支持30多种字段类型，详情参见本文最后一个表格 | 字段类型                                                     |
| autoincr                                         | 是否是自增                                                   |
| [not ]null 或 notnull                            | 是否可以为空                                                 |
| unique或unique(uniquename)                       | 是否是唯一，如不加括号则该字段不允许重复；如加上括号，则括号中为联合唯一索引的名字，此时如果有另外一个或多个字段和本unique的uniquename相同，则这些uniquename相同的字段组成联合唯一索引 |
| index或index(indexname)                          | 是否是索引，如不加括号则该字段自身为索引，如加上括号，则括号中为联合索引的名字，此时如果有另外一个或多个字段和本index的indexname相同，则这些indexname相同的字段组成联合索引 |
| extends                                          | 应用于一个匿名成员结构体或者非匿名成员结构体之上，表示此结构体的所有成员也映射到数据库中，extends可加载无限级 |
| -                                                | 这个Field将不进行字段映射                                    |
| ->                                               | 这个Field将只写入到数据库而不从数据库读取                    |
| <-                                               | 这个Field将只从数据库读取，而不写入到数据库                  |
| created                                          | 这个Field将在Insert时自动赋值为当前时间                      |
| updated                                          | 这个Field将在Insert或Update时自动赋值为当前时间              |
| deleted                                          | 这个Field将在Delete时设置为当前时间，并且当前记录不删除      |
| version                                          | 这个Field将会在insert时默认为1，每次更新自动加1              |
| default 0或default(0)                            | 设置默认值，紧跟的内容如果是Varchar等需要加上单引号          |
| json                                             | 表示内容将先转成Json格式，然后存储到数据库中，数据库中的字段类型可以为Text或者二进制 |
| comment                                          | 设置字段的注释（当前仅支持mysql）                            |

另外有如下几条自动映射的规则：

1.如果field名称为`Id`而且类型为`int64`并且没有定义tag，则会被xorm视为主键，并且拥有自增属性。如果想用`Id`以外的名字或非int64类型做为主键名，必须在对应的Tag上加上`xorm:"pk"`来定义主键，加上`xorm:"autoincr"`作为自增。这里需要注意的是，有些数据库并不允许非主键的自增属性。

2.string类型默认映射为`varchar(255)`，如果需要不同的定义，可以在tag中自定义，如：`varchar(1024)`

3.支持`type MyString string`等自定义的field，支持Slice, Map等field成员，这些成员默认存储为Text类型，并且默认将使用Json格式来序列化和反序列化。也支持数据库字段类型为Blob类型。如果是Blob类型，则先使用Json格式序列化再转成[]byte格式。如果是[]byte或者[]uint8，则不做转换二十直接以二进制方式存储。具体参见 [Go与字段类型对应表](http://xorm.topgoer.com/chapter-02/chapter-02/5.types.md)

4.实现了Conversion接口的类型或者结构体，将根据接口的转换方式在类型和数据库记录之间进行相互转换，这个接口的优先级是最高的。

```Go
type Conversion interface {
  FromDB([]byte) error
  ToDB() ([]byte, error)
}
```



5.如果一个结构体包含一个Conversion的接口类型，那么在获取数据时，必须要预先设置一个实现此接口的struct或者struct的指针。此时可以在此struct中实现`BeforeSet(name string, cell xorm.Cell)`方法来进行预先给Conversion赋值。例子参见 [testConversion](https://github.com/go-xorm/tests/blob/master/base.go#L1826)



下表为xorm类型和各个数据库类型的对应表：

| xorm       | mysql      | sqlite3 | postgres            | remark                   |
| ---------- | ---------- | ------- | ------------------- | ------------------------ |
| BIT        | BIT        | INTEGER | BIT                 |                          |
| TINYINT    | TINYINT    | INTEGER | SMALLINT            |                          |
| SMALLINT   | SMALLINT   | INTEGER | SMALLINT            |                          |
| MEDIUMINT  | MEDIUMINT  | INTEGER | INTEGER             |                          |
| INT        | INT        | INTEGER | INTEGER             |                          |
| INTEGER    | INTEGER    | INTEGER | INTEGER             |                          |
| BIGINT     | BIGINT     | INTEGER | BIGINT              |                          |
|            |            |         |                     |                          |
| CHAR       | CHAR       | TEXT    | CHAR                |                          |
| VARCHAR    | VARCHAR    | TEXT    | VARCHAR             |                          |
| TINYTEXT   | TINYTEXT   | TEXT    | TEXT                |                          |
| TEXT       | TEXT       | TEXT    | TEXT                |                          |
| MEDIUMTEXT | MEDIUMTEXT | TEXT    | TEXT                |                          |
| LONGTEXT   | LONGTEXT   | TEXT    | TEXT                |                          |
|            |            |         |                     |                          |
| BINARY     | BINARY     | BLOB    | BYTEA               |                          |
| VARBINARY  | VARBINARY  | BLOB    | BYTEA               |                          |
|            |            |         |                     |                          |
| DATE       | DATE       | NUMERIC | DATE                |                          |
| DATETIME   | DATETIME   | NUMERIC | TIMESTAMP           |                          |
| TIME       | TIME       | NUMERIC | TIME                |                          |
| TIMESTAMP  | TIMESTAMP  | NUMERIC | TIMESTAMP           |                          |
| TIMESTAMPZ | TEXT       | TEXT    | TIMESTAMP with zone | timestamp with zone info |
|            |            |         |                     |                          |
| REAL       | REAL       | REAL    | REAL                |                          |
| FLOAT      | FLOAT      | REAL    | REAL                |                          |
| DOUBLE     | DOUBLE     | REAL    | DOUBLE PRECISION    |                          |
|            |            |         |                     |                          |
| DECIMAL    | DECIMAL    | NUMERIC | DECIMAL             |                          |
| NUMERIC    | NUMERIC    | NUMERIC | NUMERIC             |                          |
|            |            |         |                     |                          |
| TINYBLOB   | TINYBLOB   | BLOB    | BYTEA               |                          |
| BLOB       | BLOB       | BLOB    | BYTEA               |                          |
| MEDIUMBLOB | MEDIUMBLOB | BLOB    | BYTEA               |                          |
| LONGBLOB   | LONGBLOB   | BLOB    | BYTEA               |                          |
| BYTEA      | BLOB       | BLOB    | BYTEA               |                          |
|            |            |         |                     |                          |
| BOOL       | TINYINT    | INTEGER | BOOLEAN             |                          |
| SERIAL     | INT        | INTEGER | SERIAL              | auto increment           |
| BIGSERIAL  | BIGINT     | INTEGER | BIGSERIAL           | auto increment           |



**Go与字段类型对应表**

如果不使用tag来定义field对应的数据库字段类型，那么系统会自动给出一个默认的字段类型，对应表如下：

| go type's kind                                       | value method                        | xorm type    |
| ---------------------------------------------------- | ----------------------------------- | ------------ |
| implemented Conversion                               | Conversion.ToDB / Conversion.FromDB | Text         |
| int, int8, int16, int32, uint, uint8, uint16, uint32 |                                     | Int          |
| int64, uint64                                        |                                     | BigInt       |
| float32                                              |                                     | Float        |
| float64                                              |                                     | Double       |
| complex64, complex128                                | json.Marshal / json.UnMarshal       | Varchar(64)  |
| []uint8                                              |                                     | Blob         |
| array, slice, map except []uint8                     | json.Marshal / json.UnMarshal       | Text         |
| bool                                                 | 1 or 0                              | Bool         |
| string                                               |                                     | Varchar(255) |
| time.Time                                            |                                     | DateTime     |
| cascade struct                                       | primary key field value             | BigInt       |
|                                                      |                                     |              |
| struct                                               | json.Marshal / json.UnMarshal       | Text         |
| Others                                               |                                     | Text         |



### 4.5 基本操作

#### 4.5.1 获取数据库信息

- DBMetas()

xorm支持获取表结构信息，通过调用`engine.DBMetas()`可以获取到数据库中所有的表，字段，索引的信息。

- TableInfo()

根据传入的结构体指针及其对应的Tag，提取出模型对应的表结构信息。这里不是数据库当前的表结构信息，而是我们通过struct建模时希望数据库的表的结构信息



#### 4.5.2 建表和判断

- CreateTables()

创建表使用`engine.CreateTables()`，参数为一个或多个空的对应Struct的指针。同时可用的方法有Charset()和StoreEngine()，如果对应的数据库支持，这两个方法可以在创建表时指定表的字符编码和使用的引擎。Charset()和StoreEngine()当前仅支持Mysql数据库。

- IsTableEmpty()

判断表是否为空，参数和CreateTables相同

- IsTableExist()

判断表是否存在

- DropTables()

删除表使用`engine.DropTables()`，参数为一个或多个空的对应Struct的指针或者表的名字。如果为string传入，则只删除对应的表，如果传入的为Struct，则删除表的同时还会删除对应的索引。



#### 4.5.3 创建索引

- CreateIndexes

根据struct中的tag来创建索引

- CreateUniques

根据struct中的tag来创建唯一索引



#### 4.5.4 同步数据库结构

同步能够部分智能的根据结构体的变动检测表结构的变动，并自动同步。目前有两个实现：

- Sync

Sync将进行如下的同步操作：

```
* 自动检测和创建表，这个检测是根据表的名字
* 自动检测和新增表中的字段，这个检测是根据字段名
* 自动检测和创建索引和唯一索引，这个检测是根据索引的一个或多个字段名，而不根据索引名称
```

调用方法如下：

```Go
err := engine.Sync(new(User), new(Group))
```

- Sync2

Sync2对Sync进行了改进，目前推荐使用Sync2。Sync2函数将进行如下的同步操作：

```
* 自动检测和创建表，这个检测是根据表的名字
* 自动检测和新增表中的字段，这个检测是根据字段名，同时对表中多余的字段给出警告信息
* 自动检测，创建和删除索引和唯一索引，这个检测是根据索引的一个或多个字段名，而不根据索引名称。因此这里需要注意，如果在一个有大量数据的表中引入新的索引，数据库可能需要一定的时间来建立索引。
* 自动转换varchar字段类型到text字段类型，自动警告其它字段类型在模型和数据库之间不一致的情况。
* 自动警告字段的默认值，是否为空信息在模型和数据库之间不匹配的情况

以上这些警告信息需要将`engine.ShowWarn` 设置为 `true` 才会显示。
```

调用方法和Sync一样：

```Go
err := engine.Sync2(new(User), new(Group))
```



#### 4.5.5 导入导出sql

**Dump数据库结构和数据**

如果需要在程序中Dump数据库的结构和数据可以调用

```
engine.DumpAll(w io.Writer)
```

和

`engine.DumpAllToFile(fpath string)`。

DumpAll方法接收一个io.Writer接口来保存Dump出的数据库结构和数据的SQL语句，这个方法导出的SQL语句并不能通用。只针对当前engine所对应的数据库支持的SQL。



Import 执行数据库SQL脚本**

如果你需要将保存在文件或者其它存储设施中的SQL脚本执行，那么可以调用

```
engine.Import(r io.Reader)
```

和

```
engine.ImportFile(fpath string)
```

同样，这里需要对应的数据库的SQL语法支持。



#### 4.5.6 sql查询

- Query

也可以直接执行一个SQL查询，即Select命令。在Postgres中支持原始SQL语句中使用 ` 和 ? 符号。

```Go
sql := "select * from userinfo"
results, err := engine.Query(sql)
```

当调用 `Query` 时，第一个返回值 `results` 为 `[]map[string][]byte` 的形式。

`Query` 的参数也允许传入 `*builder.Buidler` 对象

```Go
// SELECT * FROM table
results, err := engine.Query(builder.Select("*").From("table"))
```

- QueryInterface

和 `Query` 类似，但是返回值为 `[]map[string]interface{}`



- QueryString

和 `Query` 类似，但是返回值为 `[]map[string]string`

​	

#### 4.5.7 执行sql

也可以直接执行一个SQL命令，即执行Insert， Update， Delete 等操作。此时不管数据库是何种类型，都可以使用 ` 和 ? 符号。

```Go
sql = "update `userinfo` set username=? where id=?"
res, err := engine.Exec(sql, "xiaolun", 1)
```





## 5. 插入数据

插入数据使用Insert方法，Insert方法的参数可以是一个或多个Struct的指针，一个或多个Struct的Slice的指针。

如果传入的是Slice并且当数据库支持批量插入时，Insert会使用批量插入的方式进行插入。

- 插入一条数据，此时可以用Insert或者InsertOne

```Go
user := new(User)
user.Name = "myname"
affected, err := engine.Insert(user)
// INSERT INTO user (name) values (?)
```

在插入单条数据成功后，如果该结构体有自增字段(设置为autoincr)，则自增字段会被自动赋值为数据库中的id。这里需要注意的是，如果插入的结构体中，自增字段已经赋值，则该字段会被作为非自增字段插入。

```Go
fmt.Println(user.Id)
```

- 插入同一个表的多条数据，此时如果数据库支持批量插入，那么会进行批量插入，但是这样每条记录就无法被自动赋予id值。如果数据库不支持批量插入，那么就会一条一条插入。

```Go
users := make([]User, 1)
users[0].Name = "name0"
...
affected, err := engine.Insert(&users)
```

- 使用指针Slice插入多条记录，同上

```Go
users := make([]*User, 1)
users[0] = new(User)
users[0].Name = "name0"
...
affected, err := engine.Insert(&users)
```

- 插入多条记录并且不使用批量插入，此时实际生成多条插入语句，每条记录均会自动赋予Id值。

```Go
users := make([]*User, 1)
users[0] = new(User)
users[0].Name = "name0"
...
affected, err := engine.Insert(users...)
```

- 插入不同表的一条记录

```Go
user := new(User)
user.Name = "myname"
question := new(Question)
question.Content = "whywhywhwy?"
affected, err := engine.Insert(user, question)
```

- 插入不同表的多条记录

```Go
users := make([]User, 1)
users[0].Name = "name0"
...
questions := make([]Question, 1)
questions[0].Content = "whywhywhwy?"
affected, err := engine.Insert(&users, &questions)
```

- 插入不同表的一条或多条记录

  ```Go
  user := new(User)
  user.Name = "myname"
  ...
  questions := make([]Question, 1)
  questions[0].Content = "whywhywhwy?"
  affected, err := engine.Insert(user, &questions)
  ```

这里需要注意以下几点：

- 这里虽然支持同时插入，但这些插入并没有事务关系。因此有可能在中间插入出错后，后面的插入将不会继续。此时前面的插入已经成功，如果需要回滚，请开启事务。
- 批量插入会自动生成`Insert into table values (),(),()`的语句，因此各个数据库对SQL语句有长度限制，因此这样的语句有一个最大的记录数，根据经验测算在150条左右。大于150条后，生成的sql语句将太长可能导致执行失败。因此在插入大量数据时，目前需要自行分割成每150条插入一次。



**创建时间Created**

Created可以让您在数据插入到数据库时自动将对应的字段设置为当前时间，需要在xorm标记中使用created标记，如下所示进行标记，对应的字段可以为time.Time或者自定义的time.Time或者int,int64等int类型。

```Go
type User struct {
    Id int64
    Name string
    CreatedAt time.Time `xorm:"created"`
}
```

或

```Go
type JsonTime time.Time
func (j JsonTime) MarshalJSON() ([]byte, error) {
    return []byte(`"`+time.Time(j).Format("2006-01-02 15:04:05")+`"`), nil
}

type User struct {
    Id int64
    Name string
    CreatedAt JsonTime `xorm:"created"`
}
```

或

```Go
type User struct {
    Id int64
    Name string
    CreatedAt int64 `xorm:"created"`
}
```

在Insert()或InsertOne()方法被调用时，created标记的字段将会被自动更新为当前时间或者当前时间的秒数（对应为time.Unix())，如下所示：

```Go
var user User
engine.Insert(&user)
// INSERT user (created...) VALUES (?...)
```

最后一个值得注意的是时区问题，默认xorm采用Local时区，所以默认调用的time.Now()会先被转换成对应的时区。要改变xorm的时区，可以使用：

```Go
engine.TZLocation, _ = time.LoadLocation("Asia/Shanghai")
```





## 6. 查询数据

所有的查询条件不区分调用顺序，但必须在调用Get，Exist,  Sum,  Find，Count, Iterate, Rows这几个函数之前调用。同时需要注意的一点是，在调用的参数中，如果采用默认的`SnakeMapper`所有的字符字段名均为映射后的数据库的字段名，而不是field的名字。

### 6.1 查询条件

查询和统计主要使用`Get`, `Find`, `Count`, `Rows`, `Iterate`这几个方法，同时大部分函数在调用`Update`, `Delete`时也是可用的。在进行查询时可以使用多个方法来形成查询条件，条件函数如下：

- Alias(string)

给Table设定一个别名

```Go
engine.Alias("o").Where("o.name = ?", name).Get(&order)
```

- And(string, …interface{})

和Where函数中的条件基本相同，作为条件

```Go
engine.Where(...).And(...).Get(&order)
```

- Asc(…string)

指定字段名正序排序，可以组合

```Go
engine.Asc("id").Find(&orders)
```

- Desc(…string)

指定字段名逆序排序，可以组合

```Go
engine.Asc("id").Desc("time").Find(&orders)
```

- ID(interface{})

传入一个主键字段的值，作为查询条件，如

```Go
var user User
engine.ID(1).Get(&user)
// SELECT * FROM user Where id = 1
```

如果是复合主键，则可以

```Go
engine.ID(core.PK{1, "name"}).Get(&user)
// SELECT * FROM user Where id =1 AND name= 'name'
```

传入的两个参数按照struct中pk标记字段出现的顺序赋值。

- Or(interface{}, …interface{})

和Where函数中的条件基本相同，作为条件

- OrderBy(string)

按照指定的顺序进行排序

- Select(string)

指定select语句的字段部分内容，例如：

```Go
engine.Select("a.*, (select name from b limit 1) as name").Find(&beans)

engine.Select("a.*, (select name from b limit 1) as name").Get(&bean)
```

- SQL(string, …interface{})

执行指定的Sql语句，并把结果映射到结构体。有时，当选择内容或者条件比较复杂时，可以直接使用Sql，例如：

```Go
engine.SQL("select * from table").Find(&beans)
```

- Where(string, …interface{})

和SQL中Where语句中的条件基本相同，作为条件

```Go
engine.Where("a = ? AND b = ?", 1, 2).Find(&beans)

engine.Where(builder.Eq{"a":1, "b": 2}).Find(&beans)

engine.Where(builder.Eq{"a":1}.Or(builder.Eq{"b": 2})).Find(&beans)
```

- In(string, …interface{})

某字段在一些值中，这里需要注意必须是[]interface{}才可以展开，由于Go语言的限制，[]int64等不可以直接展开，而是通过传递一个slice。第二个参数也可以是一个*builder.Builder 指针。示例代码如下：

```Go
// select from table where column in (1,2,3)
engine.In("cloumn", 1, 2, 3).Find()

// select from table where column in (1,2,3)
engine.In("column", []int{1, 2, 3}).Find()

// select from table where column in (select column from table2 where a = 1)
engine.In("column", builder.Select("column").From("table2").Where(builder.Eq{"a":1})).Find()
```

- Cols(…string)

只查询或更新某些指定的字段，默认是查询所有映射的字段或者根据Update的第一个参数来判断更新的字段。例如：

```Go
engine.Cols("age", "name").Get(&usr)
// SELECT age, name FROM user limit 1
engine.Cols("age", "name").Find(&users)
// SELECT age, name FROM user
engine.Cols("age", "name").Update(&user)
// UPDATE user SET age=? AND name=?
```

- AllCols()

查询或更新所有字段，一般与Update配合使用，因为默认Update只更新非0，非""，非bool的字段。

```Go
engine.AllCols().Id(1).Update(&user)
// UPDATE user SET name = ?, age =?, gender =? WHERE id = 1
```

- MustCols(…string)

某些字段必须更新，一般与Update配合使用。

- Omit(...string)

和cols相反，此函数指定排除某些指定的字段。注意：此方法和Cols方法不可同时使用。

```Go
// 例1：
engine.Omit("age", "gender").Update(&user)
// UPDATE user SET name = ? AND department = ?
// 例2：
engine.Omit("age, gender").Insert(&user)
// INSERT INTO user (name) values (?) // 这样的话age和gender会给默认值
// 例3：
engine.Omit("age", "gender").Find(&users)
// SELECT name FROM user //只select除age和gender字段的其它字段
```

- Distinct(…string)

按照参数中指定的字段归类结果。

```Go
engine.Distinct("age", "department").Find(&users)
// SELECT DISTINCT age, department FROM user
```

注意：当开启了缓存时，此方法的调用将在当前查询中禁用缓存。因为缓存系统当前依赖Id，而此时无法获得Id

- Table(nameOrStructPtr interface{})

传入表名称或者结构体指针，如果传入的是结构体指针，则按照IMapper的规则提取出表名

- Limit(int, …int)

限制获取的数目，第一个参数为条数，第二个参数表示开始位置，如果不传则为0

- Top(int)

相当于Limit(int, 0)

- Join(string,interface{},string)

第一个参数为连接类型，当前支持INNER, LEFT OUTER, CROSS中的一个值， 第二个参数为string类型的表名，表对应的结构体指针或者为两个值的[]string，表示表名和别名， 第三个参数为连接条件

```
详细用法参见 [5.Join的使用](5.join.md)
```

- GroupBy(string)

Groupby的参数字符串

- Having(string)

Having的参数字符串



### 6.2 临时开关方法

- NoAutoTime()

如果此方法执行，则此次生成的语句中Created和Updated字段将不自动赋值为当前时间

- NoCache()

如果此方法执行，则此次生成的语句则在非缓存模式下执行

- NoAutoCondition()

禁用自动根据结构体中的值来生成条件

```Go
engine.Where("name = ?", "lunny").Get(&User{Id:1})
// SELECT * FROM user where name='lunny' AND id = 1 LIMIT 1
engine.Where("name = ?", "lunny").NoAutoCondition().Get(&User{Id:1})
// SELECT * FROM user where name='lunny' LIMIT 1
```

- UseBool(...string)

当从一个struct来生成查询条件或更新字段时，xorm会判断struct的field是否为0,"",nil，如果为以上则不当做查询条件或者更新内容。因为bool类型只有true和false两种值，因此默认所有bool类型不会作为查询条件或者更新字段。如果可以使用此方法，如果默认不传参数，则所有的bool字段都将会被使用，如果参数不为空，则参数中指定的为字段名，则这些字段对应的bool值将被使用。

- NoCascade()

是否自动关联查询field中的数据，如果struct的field也是一个struct并且映射为某个Id，则可以在查询时自动调用Get方法查询出对应的数据。



### 6.3 Get方法

查询单条数据使用`Get`方法，在调用Get方法时需要传入一个对应结构体的指针，同时结构体中的非空field自动成为查询的条件和前面的方法条件组合在一起查询。

如：

1) 根据Id来获得单条数据:

```Go
user := new(User)
has, err := engine.Id(id).Get(user)
// 复合主键的获取方法
// has, errr := engine.Id(xorm.PK{1,2}).Get(user)
```

2) 根据Where来获得单条数据：

```Go
user := new(User)
has, err := engine.Where("name=?", "xlw").Get(user)
```

3) 根据user结构体中已有的非空数据来获得单条数据：

```Go
user := &User{Id:1}
has, err := engine.Get(user)
```

或者其它条件

```Go
user := &User{Name:"xlw"}
has, err := engine.Get(user)
```

返回的结果为两个参数，一个`has`为该条记录是否存在，第二个参数`err`为是否有错误。不管err是否为nil，has都有可能为true或者false。



### 6.4 Exist系列方法

判断某个记录是否存在可以使用`Exist`, 相比`Get`，`Exist`性能更好。

```Go
has, err := testEngine.Exist(new(RecordExist))
// SELECT * FROM record_exist LIMIT 1
has, err = testEngine.Exist(&RecordExist{
        Name: "test1",
    })
// SELECT * FROM record_exist WHERE name = ? LIMIT 1
has, err = testEngine.Where("name = ?", "test1").Exist(&RecordExist{})
// SELECT * FROM record_exist WHERE name = ? LIMIT 1
has, err = testEngine.SQL("select * from record_exist where name = ?", "test1").Exist()
// select * from record_exist where name = ?
has, err = testEngine.Table("record_exist").Exist()
// SELECT * FROM record_exist LIMIT 1
has, err = testEngine.Table("record_exist").Where("name = ?", "test1").Exist()
// SELECT * FROM record_exist WHERE name = ? LIMIT 1
```

**与Get的区别**

Get与Exist方法返回值都为bool和error，如果查询到实体存在，则Get方法会将查到的实体赋值给参数

```
user := &User{Id:1}
has,err := testEngine.Get(user)    // 执行结束后，user会被赋值为数据库中Id为1的实体
has,err = testEngine.Exist(user)    // user中仍然是初始声明的user，不做改变
```

**建议**

如果你的需求是：判断某条记录是否存在，若存在，则返回这条记录。

建议直接使用Get方法。

如果仅仅判断某条记录是否存在，则使用Exist方法，Exist的执行效率要比Get更高。



### 6.5 Find方法

查询多条数据使用`Find`方法，Find方法的第一个参数为`slice`的指针或`Map`指针，即为查询后返回的结果，第二个参数可选，为查询的条件struct的指针。

1) 传入Slice用于返回数据

```Go
everyone := make([]Userinfo, 0)
err := engine.Find(&everyone)

pEveryOne := make([]*Userinfo, 0)
err := engine.Find(&pEveryOne)
```

2) 传入Map用户返回数据，map必须为`map[int64]Userinfo`的形式，map的key为id，因此对于复合主键无法使用这种方式。

```Go
users := make(map[int64]Userinfo)
err := engine.Find(&users)

pUsers := make(map[int64]*Userinfo)
err := engine.Find(&pUsers)
```

3) 也可以加入各种条件

```Go
users := make([]Userinfo, 0)
err := engine.Where("age > ? or name = ?", 30, "xlw").Limit(20, 10).Find(&users)
```

4) 如果只选择单个字段，也可使用非结构体的Slice

```Go
var ints []int64
err := engine.Table("user").Cols("id").Find(&ints)
```



### 6.6 Join方法(***)

- Join(string,interface{},string)

第一个参数为连接类型，当前支持INNER, LEFT OUTER, CROSS中的一个值， 第二个参数为string类型的表名，表对应的结构体指针或者为两个值的[]string，表示表名和别名， 第三个参数为连接条件。

以下将通过示例来讲解具体的用法：

假如我们拥有两个表user和group，每个User只在一个Group中，那么我们可以定义对应的struct

```Go
type Group struct {
    Id int64
    Name string
}
type User struct {
    Id int64
    Name string
    GroupId int64 `xorm:"index"`
}
```

OK。问题来了，我们现在需要列出所有的User，并且列出对应的GroupName。利用extends和Join我们可以比较优雅的解决这个问题。代码如下：

```Go
type UserGroup struct {
    User `xorm:"extends"`
    Name string
}

func (UserGroup) TableName() string {
    return "user"
}

users := make([]UserGroup, 0)
engine.Join("INNER", "group", "group.id = user.group_id").Find(&users)
```

这里我们将User这个匿名结构体加了xorm的extends标记（实际上也可以是非匿名的结构体，只要有extends标记即可），这样就减少了重复代码的书写。实际上这里我们直接用Sql函数也是可以的，并不一定非要用Join。

```Go
users := make([]UserGroup, 0)
engine.Sql("select user.*, group.name from user, group where user.group_id = group.id").Find(&users)
```

然后，我们忽然发现，我们还需要显示Group的Id，因为我们需要链接到Group页面。这样又要加一个字段，算了，不如我们把Group也加个extends标记吧，代码如下：

```Go
type UserGroup struct {
    User `xorm:"extends"`
    Group `xorm:"extends"`
}

func (UserGroup) TableName() string {
    return "user"
}

users := make([]UserGroup, 0)
engine.Join("INNER", "group", "group.id = user.group_id").Find(&users)
```

这次，我们把两个表的所有字段都查询出来了，并且赋值到对应的结构体上了。

这里要注意，User和Group分别有Id和Name，这个是重名的，但是xorm是可以区分开来的，不过需要特别注意UserGroup中User和Group的顺序，如果顺序反了，则有可能会赋值错误，但是程序不会报错。

这里的顺序应遵循如下原则：

结构体中extends标记对应的结构顺序应和最终生成SQL中对应的表出现的顺序相同。

还有一点需要注意的，如果在模板中使用这个UserGroup结构体，对于字段名重复的必须加匿名引用，如：

对于不重复字段，可以{{.GroupId}}，对于重复字段{{.User.Id}} 和{{.Group.Id}}

这是2个表的用法，3个或更多表用法类似，如：

```Go
type Type struct {
    Id int64
    Name string
}

type UserGroupType struct {
    User `xorm:"extends"`
    Group `xorm:"extends"`
    Type `xorm:"extends"`
}

users := make([]UserGroupType, 0)
engine.Table("user").Join("INNER", "group", "group.id = user.group_id").
    Join("INNER", "type", "type.id = user.type_id").
    Find(&users)
```

同时，在使用Join时，也可同时使用Where和Find的第二个参数作为条件，Find的第二个参数同时也允许为各种bean来作为条件。Where里可以是各个表的条件，Find的第二个参数只是被关联表的条件。

```Go
engine.Table("user").Join("INNER", "group", "group.id = user.group_id").
    Join("INNER", "type", "type.id = user.type_id").
    Where("user.name like ?", "%"+name+"%").Find(&users, &User{Name:name})
```

当然，如果表名字太长，我们可以使用别名：

```Go
engine.Table("user").Alias("u").
    Join("INNER", []string{"group", "g"}, "g.id = u.group_id").
    Join("INNER", "type", "type.id = u.type_id").
    Where("u.name like ?", "%"+name+"%").Find(&users, &User{Name:name})
```



### 6.7 Iterate方法

Iterate方法提供逐条执行查询到的记录的方法，他所能使用的条件和Find方法完全相同

```Go
err := engine.Where("age > ? or name=?)", 30, "xlw").Iterate(new(Userinfo), func(i int, bean interface{})error{
    user := bean.(*Userinfo)
    //do somthing use i and user
})
```



### 6.8 Count方法

统计数据使用`Count`方法，Count方法的参数为struct的指针并且成为查询条件。

```Go
user := new(User)
total, err := engine.Where("id >?", 1).Count(user)
```



### 6.9 Rows方法

Rows方法和Iterate方法类似，提供逐条执行查询到的记录的方法，不过Rows更加灵活好用。

```Go
user := new(User)
rows, err := engine.Where("id >?", 1).Rows(user)
if err != nil {
}
defer rows.Close()
for rows.Next() {
    err = rows.Scan(user)
    //...
}
```



### 6.10  Sum系列方法

求和数据可以使用`Sum`, `SumInt`, `Sums` 和 `SumsInt` 四个方法，Sums系列方法的参数为struct的指针并且成为查询条件。

- Sum 求某个字段的和，返回float64

```Go
type SumStruct struct {
    Id int64
    Money int
    Rate float32
}

ss := new(SumStruct)
total, err := engine.Where("id >?", 1).Sum(ss, "money")
fmt.Printf("money is %d", int(total))
```

- SumInt 求某个字段的和，返回int64

```Go
type SumStruct struct {
    Id int64
    Money int
    Rate float32
}

ss := new(SumStruct)
total, err := engine.Where("id >?", 1).SumInt(ss, "money")
fmt.Printf("money is %d", total)
```

- Sums 求某几个字段的和， 返回float64的Slice

```Go
ss := new(SumStruct)
totals, err := engine.Where("id >?", 1).Sums(ss, "money", "rate")

fmt.Printf("money is %d, rate is %.2f", int(total[0]), total[1])
```

- SumsInt 求某几个字段的和， 返回int64的Slice

```Go
ss := new(SumStruct)
totals, err := engine.Where("id >?", 1).SumsInt(ss, "money")

fmt.Printf("money is %d", total[0])
```



## 7. 更新数据

### 7.1 update

更新数据使用`Update`方法，Update方法的第一个参数为需要更新的内容，可以为一个结构体指针或者一个Map[string]interface{}类型。当传入的为结构体指针时，只有非空和0的field才会被作为更新的字段。当传入的为Map类型时，key为数据库Column的名字，value为要更新的内容。

`Update`方法将返回两个参数，第一个为 更新的记录数，需要注意的是 `SQLITE` 数据库返回的是根据更新条件查询的记录数而不是真正受更新的记录数。

```Go
user := new(User)
user.Name = "myname"
affected, err := engine.Id(id).Update(user)
```

这里需要注意，Update会自动从user结构体中提取非0和非nil得值作为需要更新的内容，因此，如果需要更新一个值为0，则此种方法将无法实现，因此有两种选择：

- 1.通过添加Cols函数指定需要更新结构体中的哪些值，未指定的将不更新，指定了的即使为0也会更新。

```Go
affected, err := engine.Id(id).Cols("age").Update(&user)
```

- 2.通过传入map[string]interface{}来进行更新，但这时需要额外指定更新到哪个表，因为通过map是无法自动检测更新哪个表的。

```Go
affected, err := engine.Table(new(User)).Id(id).Update(map[string]interface{}{"age":0})
```



### 7.2 version(乐观锁)

要使用乐观锁，需要使用version标记

```Go
type User struct {
    Id int64
    Name string
    Version int `xorm:"version"`
}
```

在Insert时，version标记的字段将会被设置为1，在Update时，Update的内容必须包含version原来的值。

```Go
var user User
engine.Id(1).Get(&user)
// SELECT * FROM user WHERE id = ?
engine.Id(1).Update(&user)
// UPDATE user SET ..., version = version + 1 WHERE id = ? AND version = ?
```



### 7.3 updated(更新时间)

Updated可以让您在记录插入或每次记录更新时自动更新数据库中的标记字段为当前时间，需要在xorm标记中使用updated标记，如下所示进行标记，对应的字段可以为time.Time或者自定义的time.Time或者int,int64等int类型。

```Go
type User struct {
    Id int64
    Name string
    UpdatedAt time.Time `xorm:"updated"`
}
```

在Insert(), InsertOne(), Update()方法被调用时，updated标记的字段将会被自动更新为当前时间，如下所示：

```Go
var user User
engine.Id(1).Get(&user)
// SELECT * FROM user WHERE id = ?
engine.Id(1).Update(&user)
// UPDATE user SET ..., updaetd_at = ? WHERE id = ?
```

如果你希望临时不自动插入时间，则可以组合NoAutoTime()方法：

```Go
engine.NoAutoTime().Insert(&user)
```

这个在从一张表拷贝字段到另一张表时比较有用。



## 8. 删除数据

### 8.1 delete

删除数据`Delete`方法，参数为struct的指针并且成为查询条件。

```Go
user := new(User)
affected, err := engine.Id(id).Delete(user)
```

`Delete`的返回值第一个参数为删除的记录数，第二个参数为错误。

注意：当删除时，如果user中包含有bool,float64或者float32类型，有可能会使删除失败。具体请查看 [FAQ](http://xorm.topgoer.com/chapter-07/#160)



### 8.2 deleted(软删除)

Deleted可以让您不真正的删除数据，而是标记一个删除时间。使用此特性需要在xorm标记中使用deleted标记，如下所示进行标记，对应的字段必须为time.Time类型。

```Go
type User struct {
    Id int64
    Name string
    DeletedAt time.Time `xorm:"deleted"`
}
```

在Delete()时，deleted标记的字段将会被自动更新为当前时间而不是去删除该条记录，如下所示：

```Go
var user User
engine.Id(1).Get(&user)
// SELECT * FROM user WHERE id = ?
engine.Id(1).Delete(&user)
// UPDATE user SET ..., deleted_at = ? WHERE id = ?
engine.Id(1).Get(&user)
// 再次调用Get，此时将返回false, nil，即记录不存在
engine.Id(1).Delete(&user)
// 再次调用删除会返回0, nil，即记录不存在
```

那么如果记录已经被标记为删除后，要真正的获得该条记录或者真正的删除该条记录，需要启用Unscoped，如下所示：

```Go
var user User
engine.Id(1).Unscoped().Get(&user)
// 此时将可以获得记录
engine.Id(1).Unscoped().Delete(&user)
// 此时将可以真正的删除记录
```

## 9. 事务

当使用事务处理时，需要创建Session对象。在进行事物处理时，可以混用ORM方法和RAW方法，如下代码所示：

```Go
session := engine.NewSession()
defer session.Close()
// add Begin() before any action
err := session.Begin()
user1 := Userinfo{Username: "xiaoxiao", Departname: "dev", Alias: "lunny", Created: time.Now()}
_, err = session.Insert(&user1)
if err != nil {
    session.Rollback()
    return
}
user2 := Userinfo{Username: "yyy"}
_, err = session.Where("id = ?", 2).Update(&user2)
if err != nil {
    session.Rollback()
    return
}

_, err = session.Exec("delete from userinfo where username = ?", user2.Username)
if err != nil {
    session.Rollback()
    return
}

// add Commit() after all actions
err = session.Commit()
if err != nil {
    return
}
```

- 注意如果您使用的是mysql，数据库引擎为innodb事务才有效，myisam引擎是不支持事务的。



## 10. 缓存

xorm内置了一致性缓存支持，不过默认并没有开启。要开启缓存，需要在engine创建完后进行配置，如： 启用一个全局的内存缓存

```Go
cacher := xorm.NewLRUCacher(xorm.NewMemoryStore(), 1000)
engine.SetDefaultCacher(cacher)
```

上述代码采用了LRU算法的一个缓存，缓存方式是存放到内存中，缓存struct的记录数为1000条，缓存针对的范围是所有具有主键的表，没有主键的表中的数据将不会被缓存。 如果只想针对部分表，则：

```Go
cacher := xorm.NewLRUCacher(xorm.NewMemoryStore(), 1000)
engine.MapCacher(&user, cacher)
```

如果要禁用某个表的缓存，则：

```Go
engine.MapCacher(&user, nil)
```

设置完之后，其它代码基本上就不需要改动了，缓存系统已经在后台运行。

当前实现了内存存储的CacheStore接口MemoryStore，如果需要采用其它设备存储，可以实现CacheStore接口。

不过需要特别注意不适用缓存或者需要手动编码的地方：

1. 当使用了`Distinct`,`Having`,`GroupBy`方法将不会使用缓存
2. 在`Get`或者`Find`时使用了`Cols`,`Omit`方法，则在开启缓存后此方法无效，系统仍旧会取出这个表中的所有字段。
3. 在使用Exec方法执行了方法之后，可能会导致缓存与数据库不一致的地方。因此如果启用缓存，尽量避免使用Exec。如果必须使用，则需要在使用了Exec之后调用ClearCache手动做缓存清除的工作。比如：

```Go
engine.Exec("update user set name = ? where id = ?", "xlw", 1)
engine.ClearCache(new(User))
```

缓存的实现原理如下图所示：

![cache design](http://xorm.topgoer.com/chapter-11/cache_design.png)



## 11. 事件

xorm支持两种方式的事件，一种是在Struct中的特定方法来作为事件的方法，一种是在执行语句的过程中执行事件。

- BeforeInsert()

  在将此struct插入到数据库之前执行

- BeforeUpdate()

  在将此struct更新到数据库之前执行

- BeforeDelete()

  在将此struct对应的条件数据从数据库删除之前执行

- `func BeforeSet(name string, cell xorm.Cell)`

  在 Get 或 Find 方法中，当数据已经从数据库查询出来，而在设置到结构体之前调用，name为数据库字段名称，cell为数据库中的字段值。

- `func AfterSet(name string, cell xorm.Cell)`

  在 Get 或 Find 方法中，当数据已经从数据库查询出来，而在设置到结构体之后调用，name为数据库字段名称，cell为数据库中的字段值。

- AfterInsert()

  在将此struct成功插入到数据库之后执行

- AfterUpdate()

  在将此struct成功更新到数据库之后执行

- AfterDelete()

  在将此struct对应的条件数据成功从数据库删除之后执行



在语句执行过程中的事件方法为：

- Before(beforeFunc interface{})

临时执行某个方法之前执行

```Go
before := func(bean interface{}){
    fmt.Println("before", bean)
}
engine.Before(before).Insert(&obj)
```

- After(afterFunc interface{})

  临时执行某个方法之后执行

```Go
after := func(bean interface{}){
    fmt.Println("after", bean)
}
engine.After(after).Insert(&obj)
```

其中beforeFunc和afterFunc的原型为func(bean interface{}).



## 12. 工具

xorm 是一组数据库操作命令行工具。

### 12.1 源码安装

```go
go get xorm.io/cmd/xorm
```

同时你需要安装如下依赖:

- github.com/go-xorm/xorm
- Mysql: [github.com/go-sql-driver/mysql](https://github.com/go-sql-driver/mysql)
- MyMysql: [github.com/ziutek/mymysql/godrv](https://github.com/ziutek/mymysql/godrv)
- Postgres: [github.com/lib/pq](https://github.com/lib/pq)
- SQLite: [github.com/mattn/go-sqlite3](https://github.com/mattn/go-sqlite3)

** 对于sqlite3的支持，你需要自己进行编译 `go build -tags sqlite3` 因为sqlite3需要cgo的支持。

### 12.2 命令列表

有如下可用的命令：

- **reverse** 反转一个数据库结构，生成代码
- **shell** 通用的数据库操作客户端，可对数据库结构和数据操作
- **dump** Dump数据库中所有结构和数据到标准输出
- **source** 从标注输入中执行SQL文件
- **driver** 列出所有支持的数据库驱动

### 12.3 reverse

Reverse command is a tool to convert your database struct to all kinds languages of structs or classes. After you installed the tool, you can type

```
xorm help reverse
```

to get help

example:

sqlite: `xorm reverse sqite3 test.db templates/goxorm`

mysql: `xorm reverse mysql root:@/xorm_test?charset=utf8 templates/goxorm`

mymysql: `xorm reverse mymysql xorm_test2/root/ templates/goxorm`

postgres: `xorm reverse postgres "dbname=xorm_test sslmode=disable" templates/goxorm`

will generated go files in `./model` directory

### 12.4 Template and Config

Now, xorm tool supports go and c++ two languages and have go, goxorm, c++ three of default templates. In template directory, we can put a config file to control how to generating.

````
lang=go
genJson=1
```

lang must be go or c++ now. genJson can be 1 or 0, if 1 then the struct will have json tag.

### 12.5 Shell

Shell command provides a tool to operate database. For example, you can create table, alter table, insert data, delete data and etc.

`xorm shell sqlite3 test.db` will connect to the sqlite3 database and you can type `help` to list all the shell commands.

### 12.6 Dump

Dump command provides a tool to dump all database structs and data as SQL to your standard output.

`xorm dump sqlite3 test.db` could dump sqlite3 database test.db to standard output. If you want to save to file, just type `xorm dump sqlite3 test.db > test.sql`.

### 12.7 Source

`xorm source sqlite3 test.db < test.sql` will execute sql file on the test.db.

### 12.8 Driver

List all supported drivers since default build will not include sqlite3.

### 12.9 LICENSE

BSD License http://creativecommons.org/licenses/BSD/



## 13. 常见问题

Q: 如何使用Like？

A：

```Go
engine.Where("column like ?", "%"+char+"%").Find
```



Q: 怎么同时使用xorm的tag和json的tag？

A：使用空格

```Go
type User struct {
    Name string `json:"name" xorm:"name"`
}
```



Q: 我的struct里面包含bool类型，为什么它不能作为条件也没法用Update更新？

A：默认bool类型因为无法判断是否为空，所以不会自动作为条件也不会作为Update的内容。可以使用UseBool函数，也可以使用Cols函数

```Go
engine.Cols("bool_field").Update(&Struct{BoolField:true})
// UPDATE struct SET bool_field = true
```



Q: 我的struct里面包含float64和float32类型，为什么用他们作为查询条件总是不正确？

A：默认float32和float64映射到数据库中为float,real,double这几种类型，这几种数据库类型数据库的实现一般都是非精确的。因此作为相等条件查询有可能不会返回正确的结果。如果一定要作为查询条件，请将数据库中的类型定义为Numeric或者Decimal。

```Go
type account struct {
money float64 `xorm:"Numeric"`
}
```



Q: 为什么Update时Sqlite3返回的affected和其它数据库不一样？

A：Sqlite3默认Update时返回的是update的查询条件的记录数条数，不管记录是否真的有更新。而Mysql和Postgres默认情况下都是只返回记录中有字段改变的记录数。



Q: xorm有几种命名映射规则？

A：目前支持SnakeMapper, SameMapper和GonicMapper三种。SnakeMapper支持结构体和成员以驼峰式命名而数据库表和字段以下划线连接命名；SameMapper支持结构体和数据库的命名保持一致的映射。GonicMapper在SnakeMapper的基础上对一些特定名词，比如ID的映射会映射为id，而不是像SnakeMapper那样为i_d。



Q: xorm支持复合主键吗？

A：支持。在定义时，如果有多个字段标记了pk，则这些字段自动成为复合主键，顺序为在struct中出现的顺序。在使用Id方法时，可以用`Id(xorm.PK{1, 2})`的方式来用。



Q: xorm如何使用Join？

A：一般我们配合Join()和extends标记来进行，比如我们要对两个表进行Join操作，我们可以这样：

```
type Userinfo struct {
    Id int64
    Name string
    DetailId int64
}

type Userdetail struct {
    Id int64
    Gender int
}

type User struct {
    Userinfo `xorm:"extends"`
    Userdetail `xorm:"extends"`
}

var users = make([]User, 0)
err := engine.Table(&Userinfo{}).Join("LEFT", "userdetail", "userinfo.detail_id = userdetail.id").Find(&users)
```

请注意这里的Userinfo在User中的位置必须在Userdetail的前面，因为他在join语句中的顺序在userdetail前面。如果顺序不对，那么对于同名的列，有可能会赋值出错。

当然，如果Join语句比较复杂，我们也可以直接用Sql函数

```
err := engine.Sql("select * from userinfo, userdetail where userinfo.detail_id = userdetail.id").Find(&users)
```

- 如果有自动增长的字段，Insert如何写？ 答：Insert时，如果需要自增字段填充为自动增长的数值，请保持自增字段为0；如果自增字段为非0，自增字段将会被作为普通字段插入。

- 如果设置数据库时区？ 答：

  ```Go
  location, err = time.LoadLocation("Asia/Shanghai")
  engine.TZLocation = location
  ```







# gorm

## 1. 文档

```
http://gorm.book.jasperxu.com/

https://blog.csdn.net/u010525694/article/details/94294890

https://github.com/jinzhu/gorm

GORM V2 moved to    https://github.com/go-gorm/gorm

GORM V1 Doc         https://v1.gorm.io/docs/


// 参考资料
https://gorm.io/zh_CN/docs/models.html
https://www.liwenzhou.com/posts/Go/gorm/
https://www.liwenzhou.com/posts/Go/gorm_crud/
https://www.bilibili.com/video/BV1U7411V78R?p=2&spm_id_from=pageDriver
https://www.bilibili.com/video/BV1ST4y1T7NR?from=search&seid=1191073550013094486

https://blog.csdn.net/qq_23179075/article/details/88066241
https://www.cnblogs.com/jiujuan/p/12676195.html
```



## 2. 简介

- 全功能ORM（几乎）
- 关联（包含一个，包含多个，属于，多对多，多种包含）
- Callbacks（创建/保存/更新/删除/查找之前/之后）
- 预加载（急加载）
- 事务
- 复合主键
- SQL Builder
- 自动迁移
- 日志
- 可扩展，编写基于GORM回调的插件
- 每个功能都有测试
- 开发人员友好



## 3. 安装

```
go get -u github.com/jinzhu/gorm
```



## 4.  快速开始

```go
package main

import (
    "github.com/jinzhu/gorm"
    _ "github.com/jinzhu/gorm/dialects/sqlite"
)

type Product struct {
  gorm.Model
  Code string
  Price uint
}

func main() {
  db, err := gorm.Open("sqlite3", "test.db")
  if err != nil {
    panic("连接数据库失败")
  }
  defer db.Close()

  // 自动迁移模式
  db.AutoMigrate(&Product{})

  // 创建
  db.Create(&Product{Code: "L1212", Price: 1000})

  // 读取
  var product Product
  db.First(&product, 1) // 查询id为1的product
  db.First(&product, "code = ?", "L1212") // 查询code为l1212的product

  // 更新 - 更新product的price为2000
  db.Model(&product).Update("Price", 2000)

  // 删除 - 删除product
  db.Delete(&product)
}
```



## 5. 数据库

### 5.1 连接数据库

要连接到数据库首先要导入驱动程序。例如

```go
import _ "github.com/go-sql-driver/mysql"
```

为了方便记住导入路径，GORM包装了一些驱动。

```go
import _ "github.com/jinzhu/gorm/dialects/mysql"
// import _ "github.com/jinzhu/gorm/dialects/postgres"
// import _ "github.com/jinzhu/gorm/dialects/sqlite"
// import _ "github.com/jinzhu/gorm/dialects/mssql"
```

- MySQL

注：为了处理`time.Time`，您需要包括`parseTime`作为参数。 （[更多支持的参数](https://github.com/go-sql-driver/mysql#parameters)）

```go
import (
    "github.com/jinzhu/gorm"
    _ "github.com/jinzhu/gorm/dialects/mysql"
)

func main() {
  db, err := gorm.Open("mysql", "user:password@/dbname?charset=utf8&parseTime=True&loc=Local")
  defer db.Close()
}
```

- PostgreSQL

```go
import (
    "github.com/jinzhu/gorm"
    _ "github.com/jinzhu/gorm/dialects/postgres"
)

func main() {
  db, err := gorm.Open("postgres", "host=myhost user=gorm dbname=gorm sslmode=disable password=mypassword")
  defer db.Close()
}
```

- Sqlite3

```
import (
    "github.com/jinzhu/gorm"
    _ "github.com/jinzhu/gorm/dialects/sqlite"
)

func main() {
  db, err := gorm.Open("sqlite3", "/tmp/gorm.db")
  defer db.Close()
}
```

- 不支持的数据库

GORM正式支持上述的数据库，如果您使用的是不受支持的数据库请按照下面的连接编写对应数据库支持文件。 https://github.com/jinzhu/gorm/blob/master/dialect.go



### 5.2 自动迁移

自动迁移模式将保持更新到最新。

警告：自动迁移**仅仅会创建表**，缺少列和索引，并且不会改变现有列的类型或删除未使用的列以保护数据。

```go
db.AutoMigrate(&User{})

db.AutoMigrate(&User{}, &Product{}, &Order{})

// 创建表时添加表后缀
db.Set("gorm:table_options", "ENGINE=InnoDB").AutoMigrate(&User{})
```

### 5.3 检查表是否存在

```go
// 检查表`users`是否存在
db.HasTable("users")

// 检查模型`User`表是否存在
db.HasTable(&User{})
```



### 5.4 创建表

```go
// 创建表
db.CreateTable(&User{})

// 创建表`users'时将“ENGINE = InnoDB”附加到SQL语句
db.Set("gorm:table_options", "ENGINE=InnoDB").CreateTable(&User{})
```



### 5.5 删除表

```go
// 删除模型`User`的表
db.DropTable(&User{})

// 删除表`users`
db.DropTable("users")

// 删除模型`User`的表和表`products`
db.DropTableIfExists(&User{}, "products")
```

### 5.6 修改列

修改列的类型为给定值

```go
// 修改模型`User`的description列的数据类型为`text`
db.Model(&User{}).ModifyColumn("description", "text")
```

### 5.7 删除列

```go
// 删除模型`User`的description列
db.Model(&User{}).DropColumn("description")
```

### 5.8 外键

```go
// 添加主键
// 1st param : 外键字段
// 2nd param : 外键表(字段)
// 3rd param : ONDELETE
// 4th param : ONUPDATE
db.Model(&User{}).AddForeignKey("city_id", "cities(id)", "RESTRICT", "RESTRICT")
```



### 5.9 索引

```go
// 为`name`列添加索引`idx_user_name`
db.Model(&User{}).AddIndex("idx_user_name", "name")

// 为`name`, `age`列添加索引`idx_user_name_age`
db.Model(&User{}).AddIndex("idx_user_name_age", "name", "age")

// 添加唯一索引
db.Model(&User{}).AddUniqueIndex("idx_user_name", "name")

// 为多列添加唯一索引
db.Model(&User{}).AddUniqueIndex("idx_user_name_age", "name", "age")

// 删除索引
db.Model(&User{}).RemoveIndex("idx_user_name")
```



## 6. 模型

### 6.1 模型定义

```go
type User struct {
    gorm.Model
    Birthday     time.Time
    Age          int
    Name         string  `gorm:"size:255"`       // string默认长度为255, 使用这种tag重设。
    Num          int     `gorm:"AUTO_INCREMENT"` // 自增

    CreditCard        CreditCard      // One-To-One (拥有一个 - CreditCard表的UserID作外键)
    Emails            []Email         // One-To-Many (拥有多个 - Email表的UserID作外键)

    BillingAddress    Address         // One-To-One (属于 - 本表的BillingAddressID作外键)
    BillingAddressID  sql.NullInt64

    ShippingAddress   Address         // One-To-One (属于 - 本表的ShippingAddressID作外键)
    ShippingAddressID int

    IgnoreMe          int `gorm:"-"`   // 忽略这个字段
    Languages         []Language `gorm:"many2many:user_languages;"` // Many-To-Many , 'user_languages'是连接表
}

type Email struct {
    ID      int
    UserID  int     `gorm:"index"` // 外键 (属于), tag `index`是为该列创建索引
    Email   string  `gorm:"type:varchar(100);unique_index"` // `type`设置sql类型, `unique_index` 为该列设置唯一索引
    Subscribed bool
}

type Address struct {
    ID       int
    Address1 string         `gorm:"not null;unique"` // 设置字段为非空并唯一
    Address2 string         `gorm:"type:varchar(100);unique"`
    Post     sql.NullString `gorm:"not null"`
}

type Language struct {
    ID   int
    Name string `gorm:"index:idx_name_code"` // 创建索引并命名，如果找到其他相同名称的索引则创建组合索引
    Code string `gorm:"index:idx_name_code"` // `unique_index` also works
}

type CreditCard struct {
    gorm.Model
    UserID  uint
    Number  string
}
```

### 6.2 约定

#### 6.2.1 gorm.Model 结构体

基本模型定义`gorm.Model`，包括字段`ID`，`CreatedAt`，`UpdatedAt`，`DeletedAt`，你可以将它嵌入你的模型，或者只写你想要的字段

```go
// 基本模型的定义
type Model struct {
  ID        uint `gorm:"primary_key"`
  CreatedAt time.Time
  UpdatedAt time.Time
  DeletedAt *time.Time
}

// 添加字段 `ID`, `CreatedAt`, `UpdatedAt`, `DeletedAt`
type User struct {
  gorm.Model
  Name string
}

// 只需要字段 `ID`, `CreatedAt`, `Name`
type User struct {
  ID        uint
  CreatedAt time.Time
  Name      string
}
```



#### 6.2.2 表名是结构体名称的复数形式

```go
type User struct {} // 默认表名是`users`

// 设置User的表名为`profiles`
func (User) TableName() string {
  return "profiles"
}

func (u User) TableName() string {
    if u.Role == "admin" {
        return "admin_users"
    } else {
        return "users"
    }
}

// 全局禁用表名复数
db.SingularTable(true) // 如果设置为true,`User`的默认表名为`user`,使用`TableName`设置的表名不受影响
```

#### 6.2.3 更改默认表名

您可以通过定义`DefaultTableNameHandler`对默认表名应用任何规则。

```go
gorm.DefaultTableNameHandler = func (db *gorm.DB, defaultTableName string) string  {
    return "prefix_" + defaultTableName;
}
```



#### 6.2.4 列名是字段名的蛇形小写

```go
type User struct {
  ID uint             // 列名为 `id`
  Name string         // 列名为 `name`
  Birthday time.Time  // 列名为 `birthday`
  CreatedAt time.Time // 列名为 `created_at`
}

// 重设列名
type Animal struct {
    AnimalId    int64     `gorm:"column:beast_id"`         // 设置列名为`beast_id`
    Birthday    time.Time `gorm:"column:day_of_the_beast"` // 设置列名为`day_of_the_beast`
    Age         int64     `gorm:"column:age_of_the_beast"` // 设置列名为`age_of_the_beast`
}
```

#### 6.2.5 字段ID为主键

```go
type User struct {
  ID   uint  // 字段`ID`为默认主键
  Name string
}

// 使用tag `primary_key`用来设置主键
type Animal struct {
  AnimalId int64 `gorm:"primary_key"` // 设置AnimalId为主键
  Name     string
  Age      int64
}
```

#### 6.2.6 字段CreatedAt用于存储记录的创建时间

创建具有`CreatedAt`字段的记录将被设置为当前时间

```go
db.Create(&user) // 将会设置`CreatedAt`为当前时间

// 要更改它的值, 你需要使用`Update`
db.Model(&user).Update("CreatedAt", time.Now())
```



#### 6.2.7 字段UpdatedAt用于存储记录的修改时间

> save后，默认gorm.models 中的UpdatedAt  会保存当前时间

保存具有`UpdatedAt`字段的记录将被设置为当前时间

```go
db.Save(&user) 							  // 将会设置`UpdatedAt`为当前时间
db.Model(&user).Update("name", "jinzhu") // 将会设置`UpdatedAt`为当前时间
```



#### 6.2.8 字段DeletedAt用于存储记录的删除时间，如果字段存在

删除具有`DeletedAt`字段的记录，它不会冲数据库中删除，但只将字段`DeletedAt`设置为当前时间，并在查询时无法找到记录，请参阅[软删除](http://gorm.book.jasperxu.com/crud.html#sd)





### 6.3 关联

####  6.3.1 属于

```go
// `User`属于`Profile`, `ProfileID`为外键
type User struct {
  gorm.Model
  Profile   Profile
  ProfileID int
}

type Profile struct {
  gorm.Model
  Name string
}

db.Model(&user).Related(&profile)
//// SELECT * FROM profiles WHERE id = 111; // 111是user的外键ProfileID
```

指定外键

```go
type Profile struct {
    gorm.Model
    Name string
}

type User struct {
    gorm.Model
    Profile      Profile `gorm:"ForeignKey:ProfileRefer"` // 使用ProfileRefer作为外键
    ProfileRefer int
}
```

指定外键和关联外键

```go
type Profile struct {
    gorm.Model
    Refer string
    Name  string
}

type User struct {
    gorm.Model
    Profile   Profile `gorm:"ForeignKey:ProfileID;AssociationForeignKey:Refer"`
    ProfileID int
}
```



#### 6.3.2 包含一个

```go
// User 包含一个 CreditCard, UserID 为外键
type User struct {
    gorm.Model
    CreditCard   CreditCard
}

type CreditCard struct {
    gorm.Model
    UserID   uint
    Number   string
}

var card CreditCard
db.Model(&user).Related(&card, "CreditCard")
//// SELECT * FROM credit_cards WHERE user_id = 123; // 123 is user's primary key
// CreditCard是user的字段名称，这意味着获得user的CreditCard关系并将其填充到变量
// 如果字段名与变量的类型名相同，如上例所示，可以省略，如：
db.Model(&user).Related(&card)
```

指定外键

```go
type Profile struct {
  gorm.Model
  Name      string
  UserRefer uint
}

type User struct {
  gorm.Model
  Profile Profile `gorm:"ForeignKey:UserRefer"`
}
```

指定外键和关联外键

```go
type Profile struct {
  gorm.Model
  Name   string
  UserID uint
}

type User struct {
  gorm.Model
  Refer   string
  Profile Profile `gorm:"ForeignKey:UserID;AssociationForeignKey:Refer"`
}
```



#### 6.3.3 包含多个

```go
// User 包含多个 emails, UserID 为外键
type User struct {
    gorm.Model
    Emails   []Email
}

type Email struct {
    gorm.Model
    Email   string
    UserID  uint
}

db.Model(&user).Related(&emails)
//// SELECT * FROM emails WHERE user_id = 111; // 111 是 user 的主键
```

指定外键

```go
type Profile struct {
  gorm.Model
  Name      string
  UserRefer uint
}

type User struct {
  gorm.Model
  Profiles []Profile `gorm:"ForeignKey:UserRefer"`
}
```

指定外键和关联外键

```go
type Profile struct {
  gorm.Model
  Name   string
  UserID uint
}

type User struct {
  gorm.Model
  Refer   string
  Profiles []Profile `gorm:"ForeignKey:UserID;AssociationForeignKey:Refer"`
}
```



#### 6.3.4 多对多

```go
// User 包含并属于多个 languages, 使用 `user_languages` 表连接
type User struct {
    gorm.Model
    Languages         []Language `gorm:"many2many:user_languages;"`
}

type Language struct {
    gorm.Model
    Name string
}

db.Model(&user).Related(&languages, "Languages")
//// SELECT * FROM "languages" INNER JOIN "user_languages" ON "user_languages"."language_id" = "languages"."id" WHERE "user_languages"."user_id" = 111
```

指定外键和关联外键

```go
type CustomizePerson struct {
  IdPerson string             `gorm:"primary_key:true"`
  Accounts []CustomizeAccount `gorm:"many2many:PersonAccount;ForeignKey:IdPerson;AssociationForeignKey:IdAccount"`
}

type CustomizeAccount struct {
  IdAccount string `gorm:"primary_key:true"`
  Name      string
}
```

译者注：这里设置好像缺失一部分



#### 6.3.5 多种包含

支持多种的包含一个和包含多个的关联

```go
type Cat struct {
    Id    int
    Name  string
    Toy   Toy `gorm:"polymorphic:Owner;"`
  }

  type Dog struct {
    Id   int
    Name string
    Toy  Toy `gorm:"polymorphic:Owner;"`
  }

  type Toy struct {
    Id        int
    Name      string
    OwnerId   int
    OwnerType string
  }
```

注意：多态属性和多对多显式不支持，并且会抛出错误。



#### 6.3.6 关联模式

关联模式包含一些帮助方法来处理关系事情很容易。

```go
// 开始关联模式
var user User
db.Model(&user).Association("Languages")
// `user`是源，它需要是一个有效的记录（包含主键）
// `Languages`是关系中源的字段名。
// 如果这些条件不匹配，将返回一个错误，检查它：
// db.Model(&user).Association("Languages").Error


// Query - 查找所有相关关联
db.Model(&user).Association("Languages").Find(&languages)


// Append - 添加新的many2many, has_many关联, 会替换掉当前 has_one, belongs_to关联
db.Model(&user).Association("Languages").Append([]Language{languageZH, languageEN})
db.Model(&user).Association("Languages").Append(Language{Name: "DE"})


// Delete - 删除源和传递的参数之间的关系，不会删除这些参数
db.Model(&user).Association("Languages").Delete([]Language{languageZH, languageEN})
db.Model(&user).Association("Languages").Delete(languageZH, languageEN)


// Replace - 使用新的关联替换当前关联
db.Model(&user).Association("Languages").Replace([]Language{languageZH, languageEN})
db.Model(&user).Association("Languages").Replace(Language{Name: "DE"}, languageEN)


// Count - 返回当前关联的计数
db.Model(&user).Association("Languages").Count()


// Clear - 删除源和当前关联之间的关系，不会删除这些关联
db.Model(&user).Association("Languages").Clear()
```



## 7. crud

### 7.1 创建

#### 7.1.1. 创建记录

```go
user := User{Name: "Jinzhu", Age: 18, Birthday: time.Now()}

db.NewRecord(user) // => 主键为空返回`true`

db.Create(&user)

db.NewRecord(user) // => 创建`user`后返回`false`
```

#### 7.1.2. 默认值

您可以在gorm tag中定义默认值，然后插入SQL将忽略具有默认值的这些字段，并且其值为空，并且在将记录插入数据库后，gorm将从数据库加载这些字段的值。

```go
type Animal struct {
    ID   int64
    Name string `gorm:"default:'galeone'"`
    Age  int64
}

var animal = Animal{Age: 99, Name: ""}
db.Create(&animal)
// INSERT INTO animals("age") values('99');
// SELECT name from animals WHERE ID=111; // 返回主键为 111
// animal.Name => 'galeone'
```

#### 7.1.3. 在Callbacks中设置主键

如果要在BeforeCreate回调中设置主字段的值，可以使用scope.SetColumn，例如：

```go
func (user *User) BeforeCreate(scope *gorm.Scope) error {
  scope.SetColumn("ID", uuid.New())
  return nil
}
```

#### 7.1.4. 扩展创建选项

```go
// 为Instert语句添加扩展SQL选项
db.Set("gorm:insert_option", "ON CONFLICT").Create(&product)
// INSERT INTO products (name, code) VALUES ("name", "code") ON CONFLICT;
```



### 7.2 查询

```go
// 获取第一条记录，按主键排序
db.First(&user)
//// SELECT * FROM users ORDER BY id LIMIT 1;

// 获取最后一条记录，按主键排序
db.Last(&user)
//// SELECT * FROM users ORDER BY id DESC LIMIT 1;

// 获取所有记录
db.Find(&users)
//// SELECT * FROM users;

// 使用主键获取记录
db.First(&user, 10)
//// SELECT * FROM users WHERE id = 10;
```

#### 7.2.1 Where查询条件 (简单SQL)

```go
// 获取第一个匹配记录
db.Where("name = ?", "jinzhu").First(&user)
//// SELECT * FROM users WHERE name = 'jinzhu' limit 1;

// 获取所有匹配记录
db.Where("name = ?", "jinzhu").Find(&users)
//// SELECT * FROM users WHERE name = 'jinzhu';

db.Where("name <> ?", "jinzhu").Find(&users)

// IN
db.Where("name in (?)", []string{"jinzhu", "jinzhu 2"}).Find(&users)

// LIKE
db.Where("name LIKE ?", "%jin%").Find(&users)

// AND
db.Where("name = ? AND age >= ?", "jinzhu", "22").Find(&users)

// Time
db.Where("updated_at > ?", lastWeek).Find(&users)

db.Where("created_at BETWEEN ? AND ?", lastWeek, today).Find(&users)
```

#### 7.2.2 Where查询条件 (Struct & Map)

注意：当使用struct查询时，GORM将只查询那些具有值的字段

```go
// Struct
db.Where(&User{Name: "jinzhu", Age: 20}).First(&user)
//// SELECT * FROM users WHERE name = "jinzhu" AND age = 20 LIMIT 1;

// Map
db.Where(map[string]interface{}{"name": "jinzhu", "age": 20}).Find(&users)
//// SELECT * FROM users WHERE name = "jinzhu" AND age = 20;

// 主键的Slice
db.Where([]int64{20, 21, 22}).Find(&users)
//// SELECT * FROM users WHERE id IN (20, 21, 22);
```

#### 7.2.3 Not条件查询

```go
db.Not("name", "jinzhu").First(&user)
//// SELECT * FROM users WHERE name <> "jinzhu" LIMIT 1;

// Not In
db.Not("name", []string{"jinzhu", "jinzhu 2"}).Find(&users)
//// SELECT * FROM users WHERE name NOT IN ("jinzhu", "jinzhu 2");

// Not In slice of primary keys
db.Not([]int64{1,2,3}).First(&user)
//// SELECT * FROM users WHERE id NOT IN (1,2,3);

db.Not([]int64{}).First(&user)
//// SELECT * FROM users;

// Plain SQL
db.Not("name = ?", "jinzhu").First(&user)
//// SELECT * FROM users WHERE NOT(name = "jinzhu");

// Struct
db.Not(User{Name: "jinzhu"}).First(&user)
//// SELECT * FROM users WHERE name <> "jinzhu";
```

#### 7.2.4 带内联条件的查询

注意：使用主键查询时，应仔细检查所传递的值是否为有效主键，以避免SQL注入

```go
// 按主键获取
db.First(&user, 23)
//// SELECT * FROM users WHERE id = 23 LIMIT 1;

// 简单SQL
db.Find(&user, "name = ?", "jinzhu")
//// SELECT * FROM users WHERE name = "jinzhu";

db.Find(&users, "name <> ? AND age > ?", "jinzhu", 20)
//// SELECT * FROM users WHERE name <> "jinzhu" AND age > 20;

// Struct
db.Find(&users, User{Age: 20})
//// SELECT * FROM users WHERE age = 20;

// Map
db.Find(&users, map[string]interface{}{"age": 20})
//// SELECT * FROM users WHERE age = 20;
```

#### 7.2.5 Or条件查询

```go
db.Where("role = ?", "admin").Or("role = ?", "super_admin").Find(&users)
//// SELECT * FROM users WHERE role = 'admin' OR role = 'super_admin';

// Struct
db.Where("name = 'jinzhu'").Or(User{Name: "jinzhu 2"}).Find(&users)
//// SELECT * FROM users WHERE name = 'jinzhu' OR name = 'jinzhu 2';

// Map
db.Where("name = 'jinzhu'").Or(map[string]interface{}{"name": "jinzhu 2"}).Find(&users)
```

#### 7.2.6 查询链

Gorm有一个可链接的API，你可以这样使用它

```go
db.Where("name <> ?","jinzhu").Where("age >= ? and role <> ?",20,"admin").Find(&users)
//// SELECT * FROM users WHERE name <> 'jinzhu' AND age >= 20 AND role <> 'admin';

db.Where("role = ?", "admin").Or("role = ?", "super_admin").Not("name = ?", "jinzhu").Find(&users)
```

#### 7.2.7 扩展查询选项

```go
// 为Select语句添加扩展SQL选项
db.Set("gorm:query_option", "FOR UPDATE").First(&user, 10)
//// SELECT * FROM users WHERE id = 10 FOR UPDATE;
```

#### 7.2.8 FirstOrInit

获取第一个匹配的记录，或者使用给定的条件初始化一个新的记录（仅适用于struct，map条件）

```go
// Unfound
db.FirstOrInit(&user, User{Name: "non_existing"})
//// user -> User{Name: "non_existing"}

// Found
db.Where(User{Name: "Jinzhu"}).FirstOrInit(&user)
//// user -> User{Id: 111, Name: "Jinzhu", Age: 20}

db.FirstOrInit(&user, map[string]interface{}{"name": "jinzhu"})
//// user -> User{Id: 111, Name: "Jinzhu", Age: 20}
```

#### 7.2.9 Attrs

如果未找到记录，则使用参数初始化结构，如果找到，不修改

```go
// Unfound
db.Where(User{Name: "non_existing"}).Attrs(User{Age: 20}).FirstOrInit(&user)
//// SELECT * FROM USERS WHERE name = 'non_existing';
//// user -> User{Name: "non_existing", Age: 20}

db.Where(User{Name: "non_existing"}).Attrs("age", 20).FirstOrInit(&user)
//// SELECT * FROM USERS WHERE name = 'non_existing';
//// user -> User{Name: "non_existing", Age: 20}

// Found
db.Where(User{Name: "Jinzhu"}).Attrs(User{Age: 30}).FirstOrInit(&user)
//// SELECT * FROM USERS WHERE name = jinzhu';
//// user -> User{Id: 111, Name: "Jinzhu", Age: 20}
```

#### 7.2.10 Assign

将参数分配给结果，不管它是否被找到

```go
// Unfound
db.Where(User{Name: "non_existing"}).Assign(User{Age: 20}).FirstOrInit(&user)
//// user -> User{Name: "non_existing", Age: 20}

// Found
db.Where(User{Name: "Jinzhu"}).Assign(User{Age: 30}).FirstOrInit(&user)
//// SELECT * FROM USERS WHERE name = jinzhu';
//// user -> User{Id: 111, Name: "Jinzhu", Age: 30}
```



#### 7.2.11 FirstOrCreate

获取第一个匹配的记录，或创建一个具有给定条件的新记录（仅适用于struct, map条件）

```go
// Unfound
db.FirstOrCreate(&user, User{Name: "non_existing"})
//// INSERT INTO "users" (name) VALUES ("non_existing");
//// user -> User{Id: 112, Name: "non_existing"}

// Found
db.Where(User{Name: "Jinzhu"}).FirstOrCreate(&user)
//// user -> User{Id: 111, Name: "Jinzhu"}
```



#### 7.2.12 Select

指定要从数据库检索的字段，默认情况下，将选择所有字段;

```go
db.Select("name, age").Find(&users)
//// SELECT name, age FROM users;

db.Select([]string{"name", "age"}).Find(&users)
//// SELECT name, age FROM users;

db.Table("users").Select("COALESCE(age,?)", 42).Rows()
//// SELECT COALESCE(age,'42') FROM users;
```

#### 7.2.13 Order

在从数据库检索记录时指定顺序，将重排序设置为`true`以覆盖定义的条件

```go
db.Order("age desc, name").Find(&users)
//// SELECT * FROM users ORDER BY age desc, name;

// Multiple orders
db.Order("age desc").Order("name").Find(&users)
//// SELECT * FROM users ORDER BY age desc, name;

// ReOrder
db.Order("age desc").Find(&users1).Order("age", true).Find(&users2)
//// SELECT * FROM users ORDER BY age desc; (users1)
//// SELECT * FROM users ORDER BY age; (users2)
```

#### 7.2.14 Limit

指定要检索的记录数

```go
db.Limit(3).Find(&users)
//// SELECT * FROM users LIMIT 3;

// Cancel limit condition with -1
db.Limit(10).Find(&users1).Limit(-1).Find(&users2)
//// SELECT * FROM users LIMIT 10; (users1)
//// SELECT * FROM users; (users2)
```

#### 7.2.15 Offset

指定在开始返回记录之前要跳过的记录数

```go
db.Offset(3).Find(&users)
//// SELECT * FROM users OFFSET 3;

// Cancel offset condition with -1
db.Offset(10).Find(&users1).Offset(-1).Find(&users2)
//// SELECT * FROM users OFFSET 10; (users1)
//// SELECT * FROM users; (users2)
```

#### 7.2.16 Count

获取模型的记录数

```go
db.Where("name = ?", "jinzhu").Or("name = ?", "jinzhu 2").Find(&users).Count(&count)
//// SELECT * from USERS WHERE name = 'jinzhu' OR name = 'jinzhu 2'; (users)
//// SELECT count(*) FROM users WHERE name = 'jinzhu' OR name = 'jinzhu 2'; (count)

db.Model(&User{}).Where("name = ?", "jinzhu").Count(&count)
//// SELECT count(*) FROM users WHERE name = 'jinzhu'; (count)

db.Table("deleted_users").Count(&count)
//// SELECT count(*) FROM deleted_users;
```

#### 7.2.17 Group & Having

```go
rows, err := db.Table("orders").Select("date(created_at) as date, sum(amount) as total").Group("date(created_at)").Rows()
for rows.Next() {
    ...
}

rows, err := db.Table("orders").Select("date(created_at) as date, sum(amount) as total").Group("date(created_at)").Having("sum(amount) > ?", 100).Rows()
for rows.Next() {
    ...
}

type Result struct {
    Date  time.Time
    Total int64
}
db.Table("orders").Select("date(created_at) as date, sum(amount) as total").Group("date(created_at)").Having("sum(amount) > ?", 100).Scan(&results)
```

#### 7.2.18 Join

指定连接条件

```go
rows, err := db.Table("users").Select("users.name, emails.email").Joins("left join emails on emails.user_id = users.id").Rows()
for rows.Next() {
    ...
}

db.Table("users").Select("users.name, emails.email").Joins("left join emails on emails.user_id = users.id").Scan(&results)

// 多个连接与参数
db.Joins("JOIN emails ON emails.user_id = users.id AND emails.email = ?", "jinzhu@example.org").Joins("JOIN credit_cards ON credit_cards.user_id = users.id").Where("credit_cards.number = ?", "411111111111").Find(&user)
```



#### 7.2.19 Pluck

将模型中的单个列作为地图查询，如果要查询多个列，可以使用[Scan](http://gorm.book.jasperxu.com/crud.html#Scan)

```go
var ages []int64
db.Find(&users).Pluck("age", &ages)

var names []string
db.Model(&User{}).Pluck("name", &names)

db.Table("deleted_users").Pluck("name", &names)

// 要返回多个列，做这样：
db.Select("name, age").Find(&users)
```



#### 7.2.20 Scan

将结果扫描到另一个结构中。

```go
type Result struct {
    Name string
    Age  int
}

var result Result
db.Table("users").Select("name, age").Where("name = ?", 3).Scan(&result)

// Raw SQL
db.Raw("SELECT name, age FROM users WHERE name = ?", 3).Scan(&result)
```



#### 7.2.21 Scopes

将当前数据库连接传递到`func(*DB) *DB`，可以用于动态添加条件

```go
func AmountGreaterThan1000(db *gorm.DB) *gorm.DB {
    return db.Where("amount > ?", 1000)
}

func PaidWithCreditCard(db *gorm.DB) *gorm.DB {
    return db.Where("pay_mode_sign = ?", "C")
}

func PaidWithCod(db *gorm.DB) *gorm.DB {
    return db.Where("pay_mode_sign = ?", "C")
}

func OrderStatus(status []string) func (db *gorm.DB) *gorm.DB {
    return func (db *gorm.DB) *gorm.DB {
        return db.Scopes(AmountGreaterThan1000).Where("status in (?)", status)
    }
}

db.Scopes(AmountGreaterThan1000, PaidWithCreditCard).Find(&orders)
// 查找所有信用卡订单和金额大于1000

db.Scopes(AmountGreaterThan1000, PaidWithCod).Find(&orders)
// 查找所有COD订单和金额大于1000

db.Scopes(OrderStatus([]string{"paid", "shipped"})).Find(&orders)
// 查找所有付费，发货订单
```

#### 7.2.22 指定表名

```go
// 使用User结构定义创建`deleted_users`表
db.Table("deleted_users").CreateTable(&User{})

var deleted_users []User
db.Table("deleted_users").Find(&deleted_users)
//// SELECT * FROM deleted_users;

db.Table("deleted_users").Where("name = ?", "jinzhu").Delete()
//// DELETE FROM deleted_users WHERE name = 'jinzhu';
```



### 7.3 预加载

```go
db.Preload("Orders").Find(&users)
//// SELECT * FROM users;
//// SELECT * FROM orders WHERE user_id IN (1,2,3,4);

db.Preload("Orders", "state NOT IN (?)", "cancelled").Find(&users)
//// SELECT * FROM users;
//// SELECT * FROM orders WHERE user_id IN (1,2,3,4) AND state NOT IN ('cancelled');

db.Where("state = ?", "active").Preload("Orders", "state NOT IN (?)", "cancelled").Find(&users)
//// SELECT * FROM users WHERE state = 'active';
//// SELECT * FROM orders WHERE user_id IN (1,2) AND state NOT IN ('cancelled');

db.Preload("Orders").Preload("Profile").Preload("Role").Find(&users)
//// SELECT * FROM users;
//// SELECT * FROM orders WHERE user_id IN (1,2,3,4); // has many
//// SELECT * FROM profiles WHERE user_id IN (1,2,3,4); // has one
//// SELECT * FROM roles WHERE id IN (4,5,6); // belongs to
```

#### 7.3.1. 自定义预加载SQL

您可以通过传递`func(db *gorm.DB) *gorm.DB`（与[Scopes](http://gorm.book.jasperxu.com/crud.html#Scopes)的使用方法相同）来自定义预加载SQL，例如：

```go
db.Preload("Orders", func(db *gorm.DB) *gorm.DB {
    return db.Order("orders.amount DESC")
}).Find(&users)
//// SELECT * FROM users;
//// SELECT * FROM orders WHERE user_id IN (1,2,3,4) order by orders.amount DESC;
```

#### 7.3.2. 嵌套预加载

```go
db.Preload("Orders.OrderItems").Find(&users)
db.Preload("Orders", "state = ?", "paid").Preload("Orders.OrderItems").Find(&users)
```



### 7.4 更新

#### 7.4.1 更新全部字段

`Save`将包括执行更新SQL时的所有字段，即使它没有更改

```go
db.First(&user)

user.Name = "jinzhu 2"
user.Age = 100
db.Save(&user)

//// UPDATE users SET name='jinzhu 2', age=100, birthday='2016-01-01', updated_at = '2013-11-17 21:34:10' WHERE id=111;
```

#### 7.4.2 更新更改字段

如果只想更新更改的字段，可以使用`Update`, `Updates`

```go
// 更新单个属性（如果更改）
db.Model(&user).Update("name", "hello")
//// UPDATE users SET name='hello', updated_at='2013-11-17 21:34:10' WHERE id=111;

// 使用组合条件更新单个属性
db.Model(&user).Where("active = ?", true).Update("name", "hello")
//// UPDATE users SET name='hello', updated_at='2013-11-17 21:34:10' WHERE id=111 AND active=true;

// 使用`map`更新多个属性，只会更新这些更改的字段
db.Model(&user).Updates(map[string]interface{}{"name": "hello", "age": 18, "actived": false})
//// UPDATE users SET name='hello', age=18, actived=false, updated_at='2013-11-17 21:34:10' WHERE id=111;

// 使用`struct`更新多个属性，只会更新这些更改的和非空白字段
db.Model(&user).Updates(User{Name: "hello", Age: 18})
//// UPDATE users SET name='hello', age=18, updated_at = '2013-11-17 21:34:10' WHERE id = 111;

// 警告:当使用struct更新时，FORM将仅更新具有非空值的字段
// 对于下面的更新，什么都不会更新为""，0，false是其类型的空白值
db.Model(&user).Updates(User{Name: "", Age: 0, Actived: false})
```

#### 7.4.3 更新选择的字段

如果您只想在更新时更新或忽略某些字段，可以使用`Select`, `Omit`

```go
db.Model(&user).Select("name").Updates(map[string]interface{}{"name": "hello", "age": 18, "actived": false})
//// UPDATE users SET name='hello', updated_at='2013-11-17 21:34:10' WHERE id=111;

db.Model(&user).Omit("name").Updates(map[string]interface{}{"name": "hello", "age": 18, "actived": false})
//// UPDATE users SET age=18, actived=false, updated_at='2013-11-17 21:34:10' WHERE id=111;
```

#### 7.4.4 更新更改字段但不进行Callbacks

以上更新操作将执行模型的`BeforeUpdate`, `AfterUpdate`方法，更新其`UpdatedAt`时间戳，在更新时保存它的`Associations`，如果不想调用它们，可以使用`UpdateColumn`, `UpdateColumns`

```go
// 更新单个属性，类似于`Update`
db.Model(&user).UpdateColumn("name", "hello")
//// UPDATE users SET name='hello' WHERE id = 111;

// 更新多个属性，与“更新”类似
db.Model(&user).UpdateColumns(User{Name: "hello", Age: 18})
//// UPDATE users SET name='hello', age=18 WHERE id = 111;
```

#### 7.4.5 Batch Updates 批量更新

`Callbacks`在批量更新时不会运行

```go
db.Table("users").Where("id IN (?)", []int{10, 11}).Updates(map[string]interface{}{"name": "hello", "age": 18})
//// UPDATE users SET name='hello', age=18 WHERE id IN (10, 11);

// 使用struct更新仅适用于非零值，或使用map[string]interface{}
db.Model(User{}).Updates(User{Name: "hello", Age: 18})
//// UPDATE users SET name='hello', age=18;

// 使用`RowsAffected`获取更新记录计数
db.Model(User{}).Updates(User{Name: "hello", Age: 18}).RowsAffected
```

#### 7.4.6 使用SQL表达式更新

```go
DB.Model(&product).Update("price", gorm.Expr("price * ? + ?", 2, 100))
//// UPDATE "products" SET "price" = price * '2' + '100', "updated_at" = '2013-11-17 21:34:10' WHERE "id" = '2';

DB.Model(&product).Updates(map[string]interface{}{"price": gorm.Expr("price * ? + ?", 2, 100)})
//// UPDATE "products" SET "price" = price * '2' + '100', "updated_at" = '2013-11-17 21:34:10' WHERE "id" = '2';

DB.Model(&product).UpdateColumn("quantity", gorm.Expr("quantity - ?", 1))
//// UPDATE "products" SET "quantity" = quantity - 1 WHERE "id" = '2';

DB.Model(&product).Where("quantity > 1").UpdateColumn("quantity", gorm.Expr("quantity - ?", 1))
//// UPDATE "products" SET "quantity" = quantity - 1 WHERE "id" = '2' AND quantity > 1;
```



#### 7.4.7 在Callbacks中更改更新值

如果要使用`BeforeUpdate`, `BeforeSave`更改回调中的更新值，可以使用`scope.SetColumn`，例如

```go
func (user *User) BeforeSave(scope *gorm.Scope) (err error) {
  if pw, err := bcrypt.GenerateFromPassword(user.Password, 0); err == nil {
    scope.SetColumn("EncryptedPassword", pw)
  }
}
```



#### 7.4.8 额外更新选项

```go
// 为Update语句添加额外的SQL选项
db.Model(&user).Set("gorm:update_option", "OPTION (OPTIMIZE FOR UNKNOWN)").Update("name, "hello")
//// UPDATE users SET name='hello', updated_at = '2013-11-17 21:34:10' WHERE id=111 OPTION (OPTIMIZE FOR UNKNOWN);
```



### 7.5 删除/软删除

**警告** 删除记录时，需要确保其主要字段具有值，GORM将使用主键删除记录，如果主要字段为空，GORM将删除模型的所有记录

```go
// 删除存在的记录
db.Delete(&email)
//// DELETE from emails where id=10;

// 为Delete语句添加额外的SQL选项
db.Set("gorm:delete_option", "OPTION (OPTIMIZE FOR UNKNOWN)").Delete(&email)
//// DELETE from emails where id=10 OPTION (OPTIMIZE FOR UNKNOWN);
```

#### 7.5.1 批量删除

删除所有匹配记录

```go
db.Where("email LIKE ?", "%jinzhu%").Delete(Email{})
//// DELETE from emails where email LIKE "%jinhu%";

db.Delete(Email{}, "email LIKE ?", "%jinzhu%")
//// DELETE from emails where email LIKE "%jinhu%";
```

#### 7.5.2 软删除

如果模型有`DeletedAt`字段，它将自动获得软删除功能！ 那么在调用`Delete`时不会从数据库中永久删除，而是只将字段`DeletedAt`的值设置为当前时间。

```go
db.Delete(&user)
//// UPDATE users SET deleted_at="2013-10-29 10:23" WHERE id = 111;

// 批量删除
db.Where("age = ?", 20).Delete(&User{})
//// UPDATE users SET deleted_at="2013-10-29 10:23" WHERE age = 20;

// 软删除的记录将在查询时被忽略
db.Where("age = 20").Find(&user)
//// SELECT * FROM users WHERE age = 20 AND deleted_at IS NULL;

// 使用Unscoped查找软删除的记录
db.Unscoped().Where("age = 20").Find(&users)
//// SELECT * FROM users WHERE age = 20;

// 使用Unscoped永久删除记录
db.Unscoped().Delete(&order)
//// DELETE FROM orders WHERE id=10;
```



### 7.6 关联

默认情况下，当创建/更新记录时，GORM将保存其关联，如果关联具有主键，GORM将调用Update来保存它，否则将被创建。

```go
user := User{
    Name:            "jinzhu",
    BillingAddress:  Address{Address1: "Billing Address - Address 1"},
    ShippingAddress: Address{Address1: "Shipping Address - Address 1"},
    Emails:          []Email{
                                        {Email: "jinzhu@example.com"},
                                        {Email: "jinzhu-2@example@example.com"},
                   },
    Languages:       []Language{
                     {Name: "ZH"},
                     {Name: "EN"},
                   },
}

db.Create(&user)
//// BEGIN TRANSACTION;
//// INSERT INTO "addresses" (address1) VALUES ("Billing Address - Address 1");
//// INSERT INTO "addresses" (address1) VALUES ("Shipping Address - Address 1");
//// INSERT INTO "users" (name,billing_address_id,shipping_address_id) VALUES ("jinzhu", 1, 2);
//// INSERT INTO "emails" (user_id,email) VALUES (111, "jinzhu@example.com");
//// INSERT INTO "emails" (user_id,email) VALUES (111, "jinzhu-2@example.com");
//// INSERT INTO "languages" ("name") VALUES ('ZH');
//// INSERT INTO user_languages ("user_id","language_id") VALUES (111, 1);
//// INSERT INTO "languages" ("name") VALUES ('EN');
//// INSERT INTO user_languages ("user_id","language_id") VALUES (111, 2);
//// COMMIT;

db.Save(&user)
```

参考[Associations](http://gorm.book.jasperxu.com/associations.html)更多详细信息

#### 7.6.1 创建/更新时跳过保存关联

默认情况下保存记录时，GORM也会保存它的关联，你可以通过设置`gorm:save_associations`为`false`跳过它。

```go
db.Set("gorm:save_associations", false).Create(&user)

db.Set("gorm:save_associations", false).Save(&user)
```

#### 7.6.2 tag设置跳过保存关联

您可以使用tag来配置您的struct，以便在创建/更新时不会保存关联

```go
type User struct {
  gorm.Model
  Name      string
  CompanyID uint
  Company   Company `gorm:"save_associations:false"`
}

type Company struct {
  gorm.Model
  Name string
}
```



## 8. callback

您可以将回调方法定义为模型结构的指针，在创建，更新，查询，删除时将被调用，如果任何回调返回错误，gorm将停止未来操作并回滚所有更改。

### 8.1 创建对象

创建过程中可用的回调

```go
// begin transaction 开始事物
BeforeSave
BeforeCreate
// save before associations 保存前关联
// update timestamp `CreatedAt`, `UpdatedAt` 更新`CreatedAt`, `UpdatedAt`时间戳
// save self 保存自己
// reload fields that have default value and its value is blank 重新加载具有默认值且其值为空的字段
// save after associations 保存后关联
AfterCreate
AfterSave
// commit or rollback transaction 提交或回滚事务
```

### 8.2 更新对象

更新过程中可用的回调

```go
// begin transaction 开始事物
BeforeSave
BeforeUpdate
// save before associations 保存前关联
// update timestamp `UpdatedAt` 更新`UpdatedAt`时间戳
// save self 保存自己
// save after associations 保存后关联
AfterUpdate
AfterSave
// commit or rollback transaction 提交或回滚事务
```

### 8.3 删除对象

删除过程中可用的回调

```go
// begin transaction 开始事物
BeforeDelete
// delete self 删除自己
AfterDelete
// commit or rollback transaction 提交或回滚事务
```

### 8.4 查询对象

查询过程中可用的回调

```go
// load data from database 从数据库加载数据
// Preloading (edger loading) 预加载（加载）
AfterFind
```

### 8.5 回调示例

```go
func (u *User) BeforeUpdate() (err error) {
    if u.readonly() {
        err = errors.New("read only user")
    }
    return
}

// 如果用户ID大于1000，则回滚插入
func (u *User) AfterCreate() (err error) {
    if (u.Id > 1000) {
        err = errors.New("user id is already greater than 1000")
    }
    return
}
```

gorm中的保存/删除操作正在事务中运行，因此在该事务中所做的更改不可见，除非提交。 如果要在回调中使用这些更改，则需要在同一事务中运行SQL。 所以你需要传递当前事务到回调，像这样：

```go
func (u *User) AfterCreate(tx *gorm.DB) (err error) {
    tx.Model(u).Update("role", "admin")
    return
}
func (u *User) AfterCreate(scope *gorm.Scope) (err error) {
  scope.DB().Model(u).Update("role", "admin")
    return
}
```



## 9. 高级用法

### 9.1 错误处理

执行任何操作后，如果发生任何错误，GORM将其设置为`*DB`的`Error`字段

```go
if err := db.Where("name = ?", "jinzhu").First(&user).Error; err != nil {
    // 错误处理...
}

// 如果有多个错误发生，用`GetErrors`获取所有的错误，它返回`[]error`
db.First(&user).Limit(10).Find(&users).GetErrors()

// 检查是否返回RecordNotFound错误
db.Where("name = ?", "hello world").First(&user).RecordNotFound()

if db.Model(&user).Related(&credit_card).RecordNotFound() {
    // 没有信用卡被发现处理...
}
```

### 9.2 事物

要在事务中执行一组操作，一般流程如下。

```go
// 开始事务
tx := db.Begin()

// 在事务中做一些数据库操作（从这一点使用'tx'，而不是'db'）
tx.Create(...)

// ...

// 发生错误时回滚事务
tx.Rollback()

// 或提交事务
tx.Commit()
```

#### 9.2.1 一个具体的例子

```go
func CreateAnimals(db *gorm.DB) err {
  tx := db.Begin()
  // 注意，一旦你在一个事务中，使用tx作为数据库句柄

  if err := tx.Create(&Animal{Name: "Giraffe"}).Error; err != nil {
     tx.Rollback()
     return err
  }

  if err := tx.Create(&Animal{Name: "Lion"}).Error; err != nil {
     tx.Rollback()
     return err
  }

  tx.Commit()
  return nil
}
```



### 9.3 SQL构建

#### 9.3.1 执行原生SQL

```go
db.Exec("DROP TABLE users;")
db.Exec("UPDATE orders SET shipped_at=? WHERE id IN (?)", time.Now, []int64{11,22,33})

// Scan
type Result struct {
    Name string
    Age  int
}

var result Result
db.Raw("SELECT name, age FROM users WHERE name = ?", 3).Scan(&result)
```

#### 9.3.2 sql.Row & sql.Rows

获取查询结果为`*sql.Row`或`*sql.Rows`

```go
row := db.Table("users").Where("name = ?", "jinzhu").Select("name, age").Row() // (*sql.Row)
row.Scan(&name, &age)

rows, err := db.Model(&User{}).Where("name = ?", "jinzhu").Select("name, age, email").Rows() // (*sql.Rows, error)
defer rows.Close()
for rows.Next() {
    ...
    rows.Scan(&name, &age, &email)
    ...
}

// Raw SQL
rows, err := db.Raw("select name, age, email from users where name = ?", "jinzhu").Rows() // (*sql.Rows, error)
defer rows.Close()
for rows.Next() {
    ...
    rows.Scan(&name, &age, &email)
    ...
}
```

#### 9.3.3 迭代中使用sql.Rows的Scan

```go
rows, err := db.Model(&User{}).Where("name = ?", "jinzhu").Select("name, age, email").Rows() // (*sql.Rows, error)
defer rows.Close()

for rows.Next() {
  var user User
  db.ScanRows(rows, &user)
  // do something
}
```

### 9.4 通用数据库接口sql.DB

从`*gorm.DB`连接获取通用数据库接口[*sql.DB](http://golang.org/pkg/database/sql/#DB)

```go
// 获取通用数据库对象`*sql.DB`以使用其函数
db.DB()

// Ping
db.DB().Ping()
```

#### 9.4.1 连接池

```go
db.DB().SetMaxIdleConns(10)
db.DB().SetMaxOpenConns(100)
```



### 9.5 复合主键

将多个字段设置为主键以启用复合主键

```go
type Product struct {
    ID           string `gorm:"primary_key"`
    LanguageCode string `gorm:"primary_key"`
}
```



### 9.6 日志

Gorm有内置的日志记录器支持，默认情况下，它会打印发生的错误

```go
// 启用Logger，显示详细日志
db.LogMode(true)

// 禁用日志记录器，不显示任何日志
db.LogMode(false)

// 调试单个操作，显示此操作的详细日志
db.Debug().Where("name = ?", "jinzhu").First(&User{})
```

#### 9.6.1 自定义日志

参考GORM的默认记录器如何自定义它https://github.com/jinzhu/gorm/blob/master/logger.go

```go
db.SetLogger(gorm.Logger{revel.TRACE})
db.SetLogger(log.New(os.Stdout, "\r\n", 0))
```



## 10. 开发

### 10.1. 架构

Gorm使用可链接的API，`*gorm.DB`是链的桥梁，对于每个链API，它将创建一个新的关系。

```go
db, err := gorm.Open("postgres", "user=gorm dbname=gorm sslmode=disable")

// 创建新关系
db = db.Where("name = ?", "jinzhu")

// 过滤更多
if SomeCondition {
    db = db.Where("age = ?", 20)
} else {
    db = db.Where("age = ?", 30)
}
if YetAnotherCondition {
    db = db.Where("active = ?", 1)
}
```

当我们开始执行任何操作时，GORM将基于当前的`*gorm.DB`创建一个新的`*gorm.Scope`实例

```go
// 执行查询操作
db.First(&user)
```

并且基于当前操作的类型，它将调用注册的`creating`, `updating`, `querying`, `deleting`或`row_querying`回调来运行操作。

对于上面的例子，将调用`querying`，参考[查询回调](http://gorm.book.jasperxu.com/callbacks.html#querying-an-object)



### 10.2. 写插件

GORM本身由`Callbacks`提供支持，因此您可以根据需要完全自定义GORM

#### 10.2.1. 注册新的callback

```go
func updateCreated(scope *Scope) {
    if scope.HasColumn("Created") {
        scope.SetColumn("Created", NowFunc())
    }
}

db.Callback().Create().Register("update_created_at", updateCreated)
// 注册Create进程的回调
```

#### 10.2.2 删除现有的callback

```go
db.Callback().Create().Remove("gorm:create")
// 从Create回调中删除`gorm:create`回调
```

#### 10.2.3 替换现有的callback

```go
db.Callback().Create().Replace("gorm:create", newCreateFunction)
// 使用新函数`newCreateFunction`替换回调`gorm:create`用于创建过程
```

#### 10.2.4 注册callback顺序

```go
db.Callback().Create().Before("gorm:create").Register("update_created_at", updateCreated)
db.Callback().Create().After("gorm:create").Register("update_created_at", updateCreated)
db.Callback().Query().After("gorm:query").Register("my_plugin:after_query", afterQuery)
db.Callback().Delete().After("gorm:delete").Register("my_plugin:after_delete", afterDelete)
db.Callback().Update().Before("gorm:update").Register("my_plugin:before_update", beforeUpdate)
db.Callback().Create().Before("gorm:create").After("gorm:before_create").Register("my_plugin:before_create", beforeCreate)
```

#### 10.2.5 预定义回调

GORM定义了回调以执行其CRUD操作，在开始编写插件之前检查它们。

- [Create callbacks](https://github.com/jinzhu/gorm/blob/master/callback_create.go)
- [Update callbacks](https://github.com/jinzhu/gorm/blob/master/callback_update.go)
- [Query callbacks](https://github.com/jinzhu/gorm/blob/master/callback_query.go)
- [Delete callbacks](https://github.com/jinzhu/gorm/blob/master/callback_delete.go)
- Row Query callbacks Row Query callbacks将在运行`Row`或`Rows`时被调用，默认情况下没有注册的回调，你可以注册一个新的回调：

```go
func updateTableName(scope *gorm.Scope) {
  scope.Search.Table(scope.TableName() + "_draft") // append `_draft` to table name
}

db.Callback().RowQuery().Register("publish:update_table_name", updateTableName)
```



## 11.更新日志

> v1.0, 20170111

**破坏性变更**

- `gorm.Open`返回类型为`*gorm.DB`而不是`gorm.DB`
- 更新只会更新更改的字段

大多数应用程序不会受到影响，只有当您更改回调中的更新值（如`BeforeSave`，`BeforeUpdate`）时，应该使用`scope.SetColumn`，例如：

```go
func (user *User) BeforeUpdate(scope *gorm.Scope) {
  if pw, err := bcrypt.GenerateFromPassword(user.Password, 0); err == nil {
    scope.SetColumn("EncryptedPassword", pw)
    // user.EncryptedPassword = pw  // 不工作，更新时不会包括EncryptedPassword字段
  }
}
```

- 软删除的默认查询作用域只会检查`deleted_at IS NULL`

之前它会检查deleted_at小于0001-01-02也排除空白时间，如：

```go
SELECT * FROM users WHERE deleted_at IS NULL OR deleted_at <= '0001-01-02'
```

但是没有必要，如果你使用`*time.Time`作为模型的`DeletedAt`，它已经被`gorm.Model`使用了，所以SQL就足够了

```go
SELECT * FROM users WHERE deleted_at IS NULL
```

所以如果你使用`gorm.Model`，那么你是好的，没有什么需要改变，只要确保所有记录的空白时间为`deleted_at`设置为`NULL`，示例迁移脚本：

```go
import (
    "github.com/jinzhu/now"
)

func main() {
  var models = []interface{}{&User{}, &Image{}}
  for _, model := range models {
    db.Unscoped().Model(model).Where("deleted_at < ?", now.MustParse("0001-01-02")).Update("deleted_at", gorm.Expr("NULL"))
  }
}
```

- 新的ToDBName逻辑

在GORM将struct，Field的名称转换为db名称之前，只有那些来自[golint](https://github.com/golang/lint/blob/master/lint.go#L702)的常见初始化（如`HTTP`，`URI`）是特殊处理的。

所以字段`HTTP`的数据库名称将是`http`而不是`h_t_t_p`，但是一些其他的初始化，如`SKU`不在golint，它的数据库名称将是`s_k_u`，这看起来很丑陋，这个版本固定这个，任何大写的初始化应该正确转换。

- 错误`RecordNotFound`已重命名为`ErrRecordNotFound`
- `mssql`驱动程序已从默认驱动程序中删除，导入它用`import _ "github.com/jinzhu/gorm/dialects/mssql"`
- `Hstore`已移至`github.com/jinzhu/gorm/dialects/postgres`







# golang-orm对比

```
Gorm
文档连接：http://gorm.book.jasperxu.com/
1.支持的数据库有：mysql、postgre、sqlite、sqlserver
2、hook机制（Before/After Create/Save/Updaye/Delete/Find）
3、对象关系Has One，Has Many，Belongs To，Many To Many，Polymorphism
4、热加载(***)
5、支持原生sql在这里插入代码片
6、支持事务：在创建，更新，查询，删除时将被调用，如果任何回调返回错误，gorm将停止未来操作并回滚所有更改。
7、链式api
8、内置日志记录器

Gorm有内置的日志记录器支持，默认情况下，它会打印发生的错误
// 启用Logger，显示详细日志
db.LogMode(true)
// 禁用日志记录器，不显示任何日志
db.LogMode(false)
// 调试单个操作，显示此操作的详细日志
db.Debug().Where("name = ?", "jinzhu").First(&User{})


Xorm
文档连接：https://lunny.gitbooks.io/xorm-manual-zh-cn/index.html
下载：go get github.com/go-xorm/xorm

1、支持的数据库有：Mysql、MyMysql、Postgre、SQlite、Mssql
2、支持事务：当使用事务处理时，需要创建Session对象
3、链式api
4、支持原始SQL语句和ORM操作的混合执行
5、查询缓存
	xorm内置了一致性缓存支持，不过默认并没有开启。要开启缓存，需要在engine创建完后进行配置，如： 启用一个全局的内存缓存
    cacher := xorm.NewLRUCacher(xorm.NewMemoryStore(), 1000)
    engine.SetDefaultCacher(cacher)
6、可根据数据库反转生成代码，即根据数据库自动生成xorm的结构体(***)
7、级联加载
8、提供sql语句日志输出
9、支持批量查询处理(***)
10 自动化的读写分离/主从式(***)    


相同点：
    各orm支持的数据库都基本相同（主流数据库都支持）
    支持事务性、链式查询等
    
不同点：
    xorm、gorose支持批量查询处理
    xorm支持主从式读写分离
    gorm支持热加载
    
	gorose便于在多个数据库切换
    文档全面性gorm>xorm>gorose
```



