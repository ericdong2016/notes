# gorm

```
todo:
1. plunk有什么用？  查询一列值
2. 预加载有什么用？
3. db.Exec()  和   db.Raw() 区别？
5. 模型
```



## 1. 文档

```
// 文档
http://gorm.book.jasperxu.com/

https://blog.csdn.net/u010525694/article/details/94294890

https://github.com/jinzhu/gorm

GORM V2 moved to    https://github.com/go-gorm/gorm

GORM V1 Doc         https://v1.gorm.io/docs


// 参考资料
https://gorm.io/zh_CN/docs/models.html
https://www.liwenzhou.com/posts/Go/gorm/
https://www.liwenzhou.com/posts/Go/gorm_crud/
https://www.bilibili.com/video/BV1U7411V78R?p=2&spm_id_from=pageDriver
https://www.bilibili.com/video/BV1ST4y1T7NR?from=search&seid=1191073550013094486

https://blog.csdn.net/qq_23179075/article/details/88066241
https://www.cnblogs.com/jiujuan/p/12676195.html

// example
https://github.com/adlerhsieh/gorm_example/blob/master/crud.go
https://github.com/herusdianto/gorm_crud_example/blob/master/helpers/paginations.go
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
go get -u gorm.io/gorm
go get -u gorm.io/driver/mysql
```



## 4.  快速入门

```go
package main

import (
	"gorm.io/driver/mysql"
	"gorm.io/gorm"
)

type Product struct {
  gorm.Model
  Code string
  Price uint
}

func main() {
  db, err := gorm.Open(mysql.Open("root:123456@tcp(127.0.0.1:3306)/gorm_test?charset=utf8&parseTime=True&loc=Local"), &gorm.Config{})
  if err != nil {
    panic("连接数据库失败")
  }
  defer db.Close()

  // 自动迁移模式
  db.AutoMigrate(&Product{})

  // 创建
  db.Create(&Product{ Code: "L1212", Price: 1000 })

  // 读取
  var product Product
  // SELECT * FROM `products` WHERE `products`.`id` = 4 AND `products`.`deleted_at` IS NULL
  db.First(&product, 1) // 查询id为1的product
  // SELECT * FROM `products` WHERE `products`.`deleted_at` IS NULL
  db.First(&product)    // 查询id为1的product
  // SELECT * FROM `products` WHERE code='DF41' AND `products`.`deleted_at` IS NULL
  db.Debug().Find(&product, "code=?", "DF41")

  // UPDATE `products` SET `price`=201,`updated_at`='2022-08-23 09:27:00.675' WHERE `products`.`deleted_at` IS NULL
  db.Debug().Model(&product).Update("price", 201)

  // 删除 - 删除product
  // UPDATE `products` SET `deleted_at`='2022-08-23 09:29:44.285' WHERE `products`.`deleted_at` IS NULL
  db.Delete(&product)
}
```



## 5. 模型

### 5.1 定义

模型是标准的 struct，由 Go 的基本数据类型，实现了 [Scanner](https://pkg.go.dev/database/sql/?tab=doc#Scanner) 和 [Valuer](https://pkg.go.dev/database/sql/driver#Valuer) 接口的自定义类型及其指针或别名组成。

```go
type User struct {
  ID           uint
  Name         string
  Email        *string		    
  Age          uint8
  Birthday     *time.Time       // 指针，可以作为零值操作
  MemberNumber sql.NullString   // 零值类型
  ActivatedAt  sql.NullTime
  CreatedAt    time.Time
  UpdatedAt    time.Time
}

type User struct {
  gorm.Model
  Name         string
  Age          sql.NullInt64				   // 零值类型
  Birthday     *time.Time
  Email        string  `gorm:"type:varchar(100);unique_index"`
  Role         string  `gorm:"size:255"` 	    // 设置字段大小为255
  MemberNumber *string `gorm:"unique;not null"` // 设置会员号（member number）唯一并且不为空
  Num          int     `gorm:"AUTO_INCREMENT"`  // 设置 num 为自增类型
  Address      string  `gorm:"index:addr"`      // 给address字段创建名为addr的索引
  IgnoreMe     int     `gorm:"-"` 			   // 忽略本字段
}
```

### 5.2 约定

#### 5.2.1 gorm.Model

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
  Name      string
  CreatedAt time.Time
}
```



#### 5.2.3 结构体标签

**字段标签**

声明 model 时，tag 是可选的，GORM 支持以下 tag： tag 名大小写不敏感，但建议使用 `camelCase` 风格

| 标签名                 | 说明                                                         |
| :--------------------- | :----------------------------------------------------------- |
| column                 | 指定 db 列名                                                 |
| type                   | 列数据类型，推荐使用兼容性好的通用类型，例如：所有数据库都支持 bool、int、uint、float、string、time、bytes 并且可以和其他标签一起使用，例如：`not null`、`size`, `autoIncrement`… 像 `varbinary(8)` 这样指定数据库数据类型也是支持的。在使用指定数据库数据类型时，它需要是完整的数据库数据类型，如：`MEDIUMINT UNSIGNED not NULL AUTO_INCREMENT` |
| size                   | 指定列大小，例如：`size:256`                                 |
| primaryKey             | 指定列为主键                                                 |
| unique                 | 指定列为唯一                                                 |
| default                | 指定列的默认值                                               |
| precision              | 指定列的精度                                                 |
| scale                  | 指定列大小                                                   |
| not null               | 指定列为 NOT NULL                                            |
| autoIncrement          | 指定列为自动增长                                             |
| autoIncrementIncrement | 自动步长，控制连续记录之间的间隔                             |
| embedded               | 嵌套字段                                                     |
| embeddedPrefix         | 嵌入字段的列名前缀                                           |
| autoCreateTime         | 创建时追踪当前时间，对于 `int` 字段，它会追踪秒级时间戳，您可以使用 `nano`/`milli` 来追踪纳秒、毫秒时间戳，例如：`autoCreateTime:nano` |
| autoUpdateTime         | 创建/更新时追踪当前时间，对于 `int` 字段，它会追踪秒级时间戳，您可以使用 `nano`/`milli` 来追踪纳秒、毫秒时间戳，例如：`autoUpdateTime:milli` |
| index                  | 根据参数创建索引，多个字段使用相同的名称则创建复合索引，查看 [索引](https://gorm.io/zh_CN/docs/indexes.html) 获取详情 |
| uniqueIndex            | 与 `index` 相同，但创建的是唯一索引                          |
| check                  | 创建检查约束，例如 `check:age > 13`，查看 [约束](https://gorm.io/zh_CN/docs/constraints.html) 获取详情 |
| <-                     | 设置字段写入的权限， `<-:create` 只创建、`<-:update` 只更新、`<-:false` 无写入权限、`<-` 创建和更新权限 |
| ->                     | 设置字段读的权限，`->:false` 无读权限                        |
| -                      | 忽略该字段，`-` 无读写权限                                   |
| comment                | 迁移时为字段添加注释                                         |



**关联标签**

| 标签             | 描述                                     |
| :--------------- | :--------------------------------------- |
| foreignKey       | 指定当前模型的列作为连接表的外键         |
| references       | 指定引用表的列名，其将被映射为连接表外键 |
| polymorphic      | 指定多态类型，比如模型名                 |
| polymorphicValue | 指定多态值、默认表名                     |
| many2many        | 指定连接表表名                           |
| joinForeignKey   | 指定连接表的外键列名，其将被映射到当前表 |
| joinReferences   | 指定连接表的外键列名，其将被映射到引用表 |
| constraint       | 关系约束，例如：`OnUpdate`、`OnDelete`   |



#### 5.2.2 表名约定

> 表名是结构体名称的复数形式

```go
//1. 默认表名是`users`
type User struct {}

//2. 设置User的表名为`profiles`
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

//3. 全局禁用表名复数
db.SingularTable(true) //如果设置为true,`User`的默认表名为`user`,使用`TableName`设置的表名不受影响


//4. 也可以通过Table()指定表名
// 使用User结构体创建名为`deleted_users`的表
db.Table("deleted_users").CreateTable(&User{})

var deleted_users []User
db.Table("deleted_users").Find(&deleted_users)
//// SELECT * FROM deleted_users;

db.Table("deleted_users").Where("name = ?", "jinzhu").Delete()
//// DELETE FROM deleted_users WHERE name = 'jinzhu';

//5. 更改默认表名
您可以通过定义`DefaultTableNameHandler`对默认表名应用任何规则。

gorm.DefaultTableNameHandler = func (db *gorm.DB, defaultTableName string) string  {
    return "prefix_" + defaultTableName;
}
```



#### 5.2.3 列名约定

> 列名默认是字段名的蛇形小写

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

#### 5.2.5 主键约定

> 默认字段ID为主键

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

#### 5.2.6 CreatedAt

> 该字段的值将会是初次创建记录的时间
>

```go
db.Create(&user) // 将会设置`CreatedAt`为当前时间

// 要更改它的值, 你需要使用`Update`
db.Model(&user).Update("CreatedAt", time.Now())
```



#### 5.2.7 UpdatedAt

> 该字段的值将会是每次更新记录的时间

```go
db.Save(&user) 							  // 将会设置`UpdatedAt`为当前时间
db.Model(&user).Update("name", "jinzhu")    // 将会设置`UpdatedAt`为当前时间
```



#### 5.2.8 DeletedAt

用于存储记录的删除时间，如果字段存在，删除具有`DeletedAt`字段的记录，它不会冲数据库中删除，但只将字段`DeletedAt`设置为当前时间，并在查询时无法找到记录，请参阅[软删除](http://gorm.book.jasperxu.com/crud.html#sd)





### 5.3 关联关系(难点)

> 先看后面的， 子表

####  5.3.1 belongs to

```go
type Company struct {
  ID   int
  Name string
}

// `User` 属于 `Company`，`CompanyID` 是外键
type User struct {
  gorm.Model
  Name      string
  CompanyID int
  Company   Company
}

db.Model(&user).Related(&Company)
// SELECT * FROM Company WHERE id = 111;  // 111是user的外键CompanyID
```

指定外键(重写外键，自定义外键)

```go
type User struct {
  gorm.Model
  Name         string
  CompanyRefer int
  Company      Company `gorm:"foreignKey:CompanyRefer"`
  // 使用 CompanyRefer 作为外键
}

type Company struct {
  ID   int
  Name string
}
```

重写引用

```go
type User struct {
  gorm.Model
  Name      string
  CompanyID string
  Company   Company `gorm:"references:Code"` // 使用 Code 作为引用
}

type Company struct {
  ID   int
  Code string
  Name string
}
```

crud

```
具体使用： https://gorm.io/zh_CN/docs/associations.html#Association-Mode

预加载：
GORM允许通过使用Preload或者Joins来主动加载实体的关联关系，具体内容请参考，预加载（主动加载）

外键约束：
你可以通过OnUpdate, OnDelete配置标签来增加关联关系的级联操作，如下面的例子，通过GORM可以完成用户和公司的级联更新和级联删除操作：

type User struct {
  gorm.Model
  Name      string
  CompanyID int
  Company   Company `gorm:"constraint:OnUpdate:CASCADE,OnDelete:SET NULL;"`
}

type Company struct {
  ID   int
  Name string
}
```



#### 5.3.2 Has One

`has one` 与 另一个模型建立一对一的关联，但它和一对一关系有些许不同。 这种关联表明一个模型的每个实例都包含或拥有另一个模型的一个实例。

```go
例如，您的应用包含 user 和 credit card模型，且每个user只能有一张credit card。

// User有一张 CreditCard, UserID 是外键。
type User struct {
  gorm.Model
  CreditCard CreditCard
}

type CreditCard struct {
  gorm.Model
  Number string
  UserID uint
}

var card CreditCard
db.Model(&user).Related(&card, "CreditCard")
// SELECT * FROM credit_cards WHERE user_id = 123;  // 123 is user's primary key
// CreditCard是user的字段名称，这意味着获得user的CreditCard关系并将其填充到变量
// 如果字段名与变量的类型名相同，如上例所示，可以省略，如：
db.Model(&user).Related(&card)
```

指定外键

```go
对于 has one 关系，同样必须存在外键字段。拥有者将把属于它的模型的主键保存到这个字段。
这个字段的名称通常由 has one 模型的类型加上其 主键 生成，对于上面的例子，它是 UserID。
为 user 添加 credit card 时，它会将 user 的 ID 保存到自己的 UserID 字段。

如果你想要使用另一个字段来保存该关系，你同样可以使用标签 foreignKey 来更改它，例如：

type User struct {
  gorm.Model
  CreditCard CreditCard `gorm:"foreignKey:UserName"` // 使用 UserName 作为外键
}

type CreditCard struct {
  gorm.Model
  Number   string
  UserName string
}
```

重写引用

```go
默认情况下，拥有者实体会将 has one 对应模型的主键保存为外键，您也可以修改它，用另一个字段来保存，例如下面这个使用 Name 来保存的例子。

您可以使用标签 references 来更改它，例如：

type User struct {
  gorm.Model
  Name       string     `gorm:"index"`
  CreditCard CreditCard `gorm:"foreignkey:UserName;references:name"`
}

type CreditCard struct {
  gorm.Model
  Number   string
  UserName string
}
```



多态关联

```
GORM 为 has one 和 has many 提供了多态关联支持，它会将拥有者实体的表名、主键值都保存到多态类型的字段中。

type Cat struct {
  ID    int
  Name  string
  Toy   Toy `gorm:"polymorphic:Owner;"`
}

type Dog struct {
  ID   int
  Name string
  Toy  Toy `gorm:"polymorphic:Owner;"`
}

type Toy struct {
  ID        int
  Name      string
  OwnerID   int
  OwnerType string
}

db.Create(&Dog{Name: "dog1", Toy: Toy{Name: "toy1"}})
// INSERT INTO `dogs` (`name`) VALUES ("dog1")
// INSERT INTO `toys` (`name`,`owner_id`,`owner_type`) VALUES ("toy1","1","dogs")



您可以使用标签 polymorphicValue 来更改多态类型的值，例如：

type Dog struct {
  ID   int
  Name string
  Toy  Toy `gorm:"polymorphic:Owner;polymorphicValue:master"`
}

type Toy struct {
  ID        int
  Name      string
  OwnerID   int
  OwnerType string
}

db.Create(&Dog{Name: "dog1", Toy: Toy{Name: "toy1"}})
// INSERT INTO `dogs` (`name`) VALUES ("dog1")
// INSERT INTO `toys` (`name`,`owner_id`,`owner_type`) VALUES ("toy1","1","master")
```



#### 5.3.3 Has Many

```go
has many 与另一个模型建立了一对多的连接。 不同于 has one，拥有者可以有零或多个关联模型。

例如，您的应用包含 user 和 credit card 模型，且每个 user 可以有多张 credit card。

// User 有多张 CreditCard，UserID 是外键
type User struct {
  gorm.Model
  CreditCards []CreditCard
}

type CreditCard struct {
  gorm.Model
  Number string
  UserID uint
}
```

指定外键

```go
要定义 has many 关系，同样必须存在外键。 默认的外键名是拥有者的类型名加上其主键字段名

例如，要定义一个属于 User 的模型，则其外键应该是 UserID。

此外，想要使用另一个字段作为外键，您可以使用 foreignKey 标签自定义它：

type User struct {
  gorm.Model
  CreditCards []CreditCard `gorm:"foreignKey:UserRefer"`
}

type CreditCard struct {
  gorm.Model
  Number    string
  UserRefer uint
}
```

重写引用

```go
GORM 通常使用拥有者的主键作为外键的值。 对于上面的例子，它是 User 的 ID 字段。
为 user 添加 credit card 时，GORM 会将 user 的 ID 字段保存到 credit card 的 UserID 字段。

同样的，您也可以使用标签 references 来更改它，例如：

type User struct {
  gorm.Model
  MemberNumber string
  CreditCards  []CreditCard `gorm:"foreignKey:UserNumber;references:MemberNumber"`
}

type CreditCard struct {
  gorm.Model
  Number     string
  UserNumber string
}
```



多态关联

```
GORM 为 has one 和 has many 提供了多态关联支持，它会将拥有者实体的表名、主键都保存到多态类型的字段中。

type Dog struct {
  ID   int
  Name string
  Toys []Toy `gorm:"polymorphic:Owner;"`
}

type Toy struct {
  ID        int
  Name      string
  OwnerID   int
  OwnerType string
}

db.Create(&Dog{Name: "dog1", Toy: []Toy{{Name: "toy1"}, {Name: "toy2"}}})
// INSERT INTO `dogs` (`name`) VALUES ("dog1")
// INSERT INTO `toys` (`name`,`owner_id`,`owner_type`) VALUES ("toy1","1","dogs"), ("toy2","1","dogs")


您可以使用标签 polymorphicValue 来更改多态类型的值，例如：

type Dog struct {
  ID   int
  Name string
  Toys []Toy `gorm:"polymorphic:Owner;polymorphicValue:master"`
}

type Toy struct {
  ID        int
  Name      string
  OwnerID   int
  OwnerType string
}

db.Create(&Dog{Name: "dog1", Toys: []Toy{{Name: "toy1"}, {Name: "toy2"}}})
// INSERT INTO `dogs` (`name`) VALUES ("dog1")
// INSERT INTO `toys` (`name`,`owner_id`,`owner_type`) VALUES ("toy1","1","master"), ("toy2","1","master")
```



#### 5.3.4 Many To Many

```go
Many to Many 会在两个 model 中添加一张连接表

例如，您的应用包含了 user 和 language，且一个 user 可以说多种 language，多个 user 也可以说一种 language

// User 拥有并属于多种 language，`user_languages` 是连接表
type User struct {
  gorm.Model
  Languages []Language `gorm:"many2many:user_languages;"`
}

type Language struct {
  gorm.Model
  Name string
}

当使用 GORM 的 AutoMigrate 为 User 创建表时，GORM 会自动创建连接表 user_languages
```

反向引用

```
// User 拥有并属于多种 language，`user_languages` 是连接表
type User struct {
  gorm.Model
  Languages []*Language `gorm:"many2many:user_languages;"`
}

type Language struct {
  gorm.Model
  Name string
  Users []*User `gorm:"many2many:user_languages;"`
}
```

重写外键

```
对于 many2many 关系，连接表会同时拥有两个模型的外键，例如：

type User struct {
  gorm.Model
  Languages []Language `gorm:"many2many:user_languages;"`
}

type Language struct {
  gorm.Model
  Name string
}

// Join Table: user_languages
// foreign key: user_id, reference: users.id
// foreign key: language_id, reference: languages.id


若要重写它们，可以使用标签 foreignKey、references、joinforeignKey、joinReferences。当然，您不需要使用全部的标签，你可以仅使用其中的一个重写部分的外键、引用。

type User struct {
    gorm.Model
    Profiles []Profile `gorm:"many2many:user_profiles;foreignKey:Refer;joinForeignKey:UserReferID;References:UserRefer;JoinReferences:UserRefer"`
    Refer    uint      `gorm:"index:,unique"`
}

type Profile struct {
    gorm.Model
    Name      string
    UserRefer uint `gorm:"index:,unique"`
}

// 这会创建连接表：user_profiles
//   外键：user_refer_id,，引用：users.refer
//   外键：profile_refer，引用：profiles.user_refer
```

自引用 Many2Many

```
type User struct {
  gorm.Model
  Friends []*User `gorm:"many2many:user_friends"`
}

// 会创建连接表：user_friends
// foreign key: user_id, reference: users.id
// foreign key: friend_id, reference: users.id
```



#### 5.3.5 关联模式

> https://gorm.io/zh_CN/docs/associations.html

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



#### 5.3.6 预加载

**预加载**

GORM 允许在 `Preload` 的其它 SQL 中直接加载关系，例如：

```
type User struct {
  gorm.Model
  Username string
  Orders   []Order
}

type Order struct {
  gorm.Model
  UserID uint
  Price  float64
}

// 查找 user 时预加载相关 Order
db.Preload("Orders").Find(&users)
// SELECT * FROM users;
// SELECT * FROM orders WHERE user_id IN (1,2,3,4);

db.Preload("Orders").Preload("Profile").Preload("Role").Find(&users)
// SELECT * FROM users;
// SELECT * FROM orders WHERE user_id IN (1,2,3,4); // has many
// SELECT * FROM profiles WHERE user_id IN (1,2,3,4); // has one
// SELECT * FROM roles WHERE id IN (4,5,6); // belongs to
```



**Joins 预加载**

`Preload` 在一个单独查询中加载关联数据。而 `Join Preload` 会使用 inner join 加载关联数据，例如：

```
db.Joins("Company").Joins("Manager").Joins("Account").First(&user, 1)
db.Joins("Company").Joins("Manager").Joins("Account").First(&user, "users.name = ?", "jinzhu")
db.Joins("Company").Joins("Manager").Joins("Account").Find(&users, "users.id IN ?", []int{1,2,3,4,5})
```

**注意** `Join Preload` 适用于一对一的关系，例如： `has one`, `belongs to`



**预加载全部**

`clause.Associations` can work with `Preload` similar like `Select` when creating/updating, you can use it to `Preload` all associations, for example:

```
type User struct {
  gorm.Model
  Name       string
  CompanyID  uint
  Company    Company
  Role       Role
  Orders     []Order
}

db.Preload(clause.Associations).Find(&users)
```

`clause.Associations` 不会预加载嵌套的关联，但你可以使用[嵌套预加载](https://gorm.io/zh_CN/docs/preload.html#nested_preloading) 例如：

```
db.Preload("Orders.OrderItems.Product").Preload(clause.Associations).Find(&users)
```





**带条件的预加载**

GORM 允许带条件的 Preload 关联，类似于[内联条件](https://gorm.io/zh_CN/docs/query.html#inline_conditions)

```
// 带条件的预加载 Order
db.Preload("Orders", "state NOT IN (?)", "cancelled").Find(&users)
// SELECT * FROM users;
// SELECT * FROM orders WHERE user_id IN (1,2,3,4) AND state NOT IN ('cancelled');

db.Where("state = ?", "active").Preload("Orders", "state NOT IN (?)", "cancelled").Find(&users)
// SELECT * FROM users WHERE state = 'active';
// SELECT * FROM orders WHERE user_id IN (1,2) AND state NOT IN ('cancelled');
```



**自定义预加载 SQL**

您可以通过 `func(db *gorm.DB) *gorm.DB` 实现自定义预加载 SQL，例如：

```
db.Preload("Orders", func(db *gorm.DB) *gorm.DB {
  return db.Order("orders.amount DESC")
}).Find(&users)
// SELECT * FROM users;
// SELECT * FROM orders WHERE user_id IN (1,2,3,4) order by orders.amount DESC;
```



**嵌套预加载**

GORM 支持嵌套预加载，例如：

```
db.Preload("Orders.OrderItems.Product").Preload("CreditCard").Find(&users)

// 自定义预加载 `Orders` 的条件
// 这样，GORM 就不会加载不匹配的 order 记录
db.Preload("Orders", "state = ?", "paid").Preload("Orders.OrderItems").Find(&users)
```



## 6. 数据库

> 从此处开始看

### 6.1 连接数据库

要连接到数据库首先要导入驱动程序。例如

```go
"gorm.io/driver/mysql"
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
  db, err := gorm.Open("mysql", "user:password@/tcp(192.168.31.141:3306)/dbname?charset=utf8&parseTime=True&loc=Local")
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



### 6.2 自动迁移

自动迁移模式将保持更新到最新。

前提： 需要先建库

警告：自动迁移**仅仅会创建表**，缺少列和索引，并且**不会改变现有列的类型或删除未使用的列**以保护数据。

```go
db.AutoMigrate(&User{})

db.AutoMigrate(&User{}, &Product{}, &Order{})

// 创建表时添加表后缀
db.Set("gorm:table_options", "ENGINE=InnoDB").AutoMigrate(&User{})
```

### 6.3 检查表是否存在

```go
// 检查表`users`是否存在
db.HasTable("users")

// 检查模型`User`表是否存在
db.HasTable(&User{})
```



### 6.4 创建表

```go
// 创建表
db.CreateTable(&User{})

// 添加扩展SQL选项, 创建表`users'时将 “ENGINE = InnoDB” 附加到SQL语句
db.Set("gorm:table_options", "ENGINE=InnoDB").CreateTable(&User{})
```



### 6.5 删除表

```go
// 删除模型`User`的表
db.DropTable(&User{})

// 删除表`users`
db.DropTable("users")

// 删除`User`表和`products`表
db.DropTableIfExists(&User{}, "products")
```

### 6.6 修改列

修改列的类型为给定值

```go
// 修改模型`User`的description列的数据类型为`text`
db.Model(&User{}).ModifyColumn("description", "text")
```

### 6.7 删除列

```go
// 删除模型`User`的description列
db.Model(&User{}).DropColumn("description")
```

### 6.8 外键

```go
// 添加主键
// 1st param : 外键字段
// 2nd param : 外键表(字段)
// 3rd param : ONDELETE
// 4th param : ONUPDATE
db.Model(&User{}).AddForeignKey("city_id", "cities(id)", "RESTRICT", "RESTRICT")
```



### 6.9 索引

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







## 7. crud

### 7.1 创建

#### 7.1.1. 创建记录

> 不存在返回true, 存在返回false

```go
user := User{Name: "Jinzhu", Age: 18, Birthday: time.Now()}

db.NewRecord(user) // => 主键为空返回`true`

db.Create(&user)

db.NewRecord(user) // => 创建`user`后返回`false`
```

#### 7.1.2. 默认值

您可以在gorm tag中定义默认值，然后插入SQL具有默认值的这些字段，并且其值为空，在记录插入数据库后，gorm将从数据库加载这些字段的值。

```go
type Animal struct {
    ID   int64
    Name string `gorm:"default:'galeone'"`
    Age  int64
}

var animal = Animal{Age: 99, Name: ""}
db.Create(&animal)
// INSERT INTO animals("age") values('99');
// SELECT name from animals WHERE Age=99;
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
// 为Instert语句添加扩展SQL选项, 类似的还有创建表时，添加引擎
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

// 使用具体的主键获取记录
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

注意：当使用struct查询时，GORM将**只查询那些具有值的字段**， 也就是下列的name或者age没有值，该条件将会失效，sql中没有该条件

```go
// Struct
db.Where(&User{Name: "jinzhu", Age: 20}).First(&user)
//// SELECT * FROM users WHERE name = "jinzhu" AND age = 20 LIMIT 1;

// Map
db.Where(map[string]interface{}{"name": "jinzhu", "age": 20}).Find(&users)
//// SELECT * FROM users WHERE name = "jinzhu" AND age = 20;

// 主键的Slice 等价于 in (id1, id2, id3)
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

// Plain SQL  ???
db.Not("name = ?", "jinzhu").First(&user)
//// SELECT * FROM users WHERE NOT(name = "jinzhu");

// Struct
db.Not(User{Name: "jinzhu"}).First(&user)
//// SELECT * FROM users WHERE name <> "jinzhu";
```

#### 7.2.4 带内联条件的查询

注意：使用主键查询时，应仔细检查所传递的值是否为有效主键，以避免SQL注入，更推荐使用where

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
// Unfound， 初始化
db.Where(User{Name: "non_existing"}).Attrs(User{Age: 20}).FirstOrInit(&user)
//// SELECT * FROM USERS WHERE name = 'non_existing';
//// user -> User{Name: "non_existing", Age: 20}

db.Where(User{Name: "non_existing"}).Attrs("age", 20).FirstOrInit(&user)
//// SELECT * FROM USERS WHERE name = 'non_existing';
//// user -> User{Name: "non_existing", Age: 20}

// Found, 不修改
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

> 问题： FirstOrCreate  和  FirstOrInit 的区别

获取第一个匹配的记录，或创建一个具有给定条件的新记录（仅适用于struct,  map条件）

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

指定要从数据库检索的字段，默认情况下，将选择所有字段。

```go
db.Select("name, age").Find(&users)
//// SELECT name, age FROM users;

db.Select([]string{"name", "age"}).Find(&users)
//// SELECT name, age FROM users;


这个函数主要用来进行空值处理，其参数格式如下： 
COALESCE ( expression, value1,value2...,value-n) 
COALESCE()函数的第一个参数expression为待检测的表达式，而其后的参数个数不定。
COALESCE()函数将会返回包括expression在内的所有参数中的第一个非空表达式。

db.Table("users").Select("COALESCE(age, ?)", 42).Rows()
//// SELECT COALESCE(age, '42') FROM users;    //查找age, 42中非空的记录
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
//// SELECT * FROM users;          (users2， 没有返回数量限制)
```

#### 7.2.15 Offset

指定在开始返回记录之前要跳过的记录数

```go
db.Offset(3).Find(&users)
//// SELECT * FROM users OFFSET 3;

// Cancel offset condition with -1
db.Offset(10).Find(&users1).Offset(-1).Find(&users2)
//// SELECT * FROM users OFFSET 10; (users1)
//// SELECT * FROM users;           (users2)
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

> Rows()  /  Scan(&x)

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
db.Table("users").Joins("JOIN emails ON emails.user_id = users.id AND emails.email = ?", "jinzhu@example.org").Joins("JOIN credit_cards ON credit_cards.user_id = users.id").Where("credit_cards.number = ?", "111").Find(&user)
```



#### 7.2.19 Pluck

查询一列值，如果要查询多个列，可以使用[Scan](http://gorm.book.jasperxu.com/crud.html#Scan)

```go
var ages []int64
db.Find(&users).Pluck("age", &ages)

var names []string
db.Model(&User{}).Pluck("name", &names)

db.Table("deleted_users").Pluck("name", &names)



//商品标题数组
var titles []string
//返回所有商品标题
//等价于：SELECT title FROM `foods`
//Pluck提取了title字段，保存到titles变量
//这里Model函数是为了绑定一个模型实例，可以从里面提取表名。
db.Model(&Food{}).Pluck("title", &titles)



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



#### 7.2.21 Scopes(***)

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

// 查找所有用信用卡订单且金额大于1000
db.Scopes(AmountGreaterThan1000, PaidWithCreditCard).Find(&orders)

// 查找所有COD订单且金额大于1000
db.Scopes(AmountGreaterThan1000, PaidWithCod).Find(&orders)

// 查找所有付费，发货且金额大于1000的订单
db.Scopes(OrderStatus([]string{"paid", "shipped"})).Find(&orders)
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

> 有什么作用？？？

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

user.Name = "jinzhu2"
user.Age = 100
db.Save(&user)

//// UPDATE users SET name='jinzhu 2', age=100, birthday='2016-01-01', updated_at = '2013-11-17 21:34:10' WHERE id=111;
```

#### 7.4.2 更新部分字段

如果只想更新更改的字段，可以使用`Update`,  `Updates`

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

// 警告:当使用struct更新时，GORM将仅更新具有非空值的字段
// 对于下面的更新，什么都不会更新, ""，0，false是其类型的空白值
db.Model(&user).Updates(User{Name: "", Age: 0,  Actived: false})
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

以上更新操作将执行模型的`BeforeUpdate`, `AfterUpdate`方法，进而更新其`UpdatedAt`时间戳，在更新时保存它的`Associations`，如果不想调用它们，可以使用`UpdateColumn`, `UpdateColumns`

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
// map
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
db.Model(&product).Update("price",  gorm.Expr("price * ? + ?", 2, 100))
//// UPDATE "products" SET "price" = price * '2' + '100', "updated_at" = '2013-11-17 21:34:10' WHERE "id" = '2';

db.Model(&product).Updates(map[string]interface{}{"price": gorm.Expr("price * ? + ?", 2, 100)})
//// UPDATE "products" SET "price" = price * '2' + '100', "updated_at" = '2013-11-17 21:34:10' WHERE "id" = '2';

db.Model(&product).UpdateColumn("quantity", gorm.Expr("quantity - ?", 1))
//// UPDATE "products" SET "quantity" = quantity - 1 WHERE "id" = '2';

db.Model(&product).Where("quantity > 1").UpdateColumn("quantity", gorm.Expr("quantity - ?", 1))
//// UPDATE "products" SET "quantity" = quantity - 1 WHERE "id" = '2' AND quantity > 1;
```



#### 7.4.7 使用Callbacks中更改更新值

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

**警告**： 删除记录时，需要确保其主要字段具有值，GORM将使用主键删除记录，如果主要字段为空，GORM将删除模型的所有记录

```go
// 删除存在的记录
db.Delete(&email, 10)
//// DELETE from emails where id=10;

// 为Delete语句添加额外的SQL选项
db.Set("gorm:delete_option", "OPTION (OPTIMIZE FOR UNKNOWN)").Delete(&email, 10)
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

### 9.2 事务

要在事务中执行一组操作，一般流程如下。

```go
// 开始事务
tx := db.Begin()

// 在事务中做一些数据库操作（从这一点使用'tx'，而不是'db'）
tx.Create(...)

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
row := db.Table("users").Where("name = ?", "jinzhu").Select("name, age").Row()  // (*sql.Row)
row.Scan(&name, &age)

rows, err := db.Model(&User{}).Where("name = ?", "jinzhu").Select("name, age, email").Rows() // (*sql.Rows, error)

defer rows.Close()
for rows.Next() {
    rows.Scan(&name, &age, &email)
}

// Raw SQL
rows, err := db.Raw("select name, age, email from users where name = ?", "jinzhu").Rows() // (*sql.Rows, error)
defer rows.Close()
for rows.Next() {
    rows.Scan(&name, &age, &email)
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



### 9.7 context

GORM 通过 `WithContext` 方法提供了 Context 支持



#### 单会话模式

单会话模式通常被用于执行单次操作

```
db.WithContext(ctx).Find(&users)
```



#### 持续会话模式

持续会话模式通常被用于执行一系列操作，例如：

```
tx := db.WithContext(ctx)
tx.First(&user, 1)
tx.Model(&user).Update("role", "admin")
```



#### 在 Hooks/Callbacks 中使用 Context

您可以从当前 `Statement`中访问 `Context` 对象，例如︰

```
func (u *User) BeforeCreate(tx *gorm.DB) (err error) {
  ctx := tx.Statement.Context
  // ...
  return
}
```



#### Chi 中间件示例

在处理 API 请求时持续会话模式会比较有用。例如，您可以在中间件中为 `*gorm.DB` 设置超时 Context，然后使用 `*gorm.DB` 处理所有请求

下面是一个 Chi 中间件的示例：

```
func SetDBMiddleware(next http.Handler) http.Handler {
  return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
    timeoutContext, _ := context.WithTimeout(context.Background(), time.Second)
    ctx := context.WithValue(r.Context(), "DB", db.WithContext(timeoutContext))
    next.ServeHTTP(w, r.WithContext(ctx))
  })
}

r := chi.NewRouter()
r.Use(SetDBMiddleware)

r.Get("/", func(w http.ResponseWriter, r *http.Request) {
  db, ok := ctx.Value("DB").(*gorm.DB)

  var users []User
  db.Find(&users)

  // 你的其他 DB 操作...
})

r.Get("/user", func(w http.ResponseWriter, r *http.Request) {
  db, ok := ctx.Value("DB").(*gorm.DB)

  var user User
  db.First(&user)

  // 你的其他 DB 操作...
})
```

> **注意** 通过 `WithContext` 设置的 `Context` 是线程安全的，参考[会话](https://gorm.io/zh_CN/docs/session.html)获取详情



#### Logger

Logger 也可以支持 `Context`，可用于日志追踪，查看 [Logger](https://gorm.io/zh_CN/docs/logger.html) 获取详情



### 9.8  session

GORM 提供了 `Session` 方法，这是一个 [`New Session Method`](https://gorm.io/zh_CN/docs/method_chaining.html)，  它允许创建带配置的新建会话模式：

```
// Session 配置
type Session struct {
  DryRun                 bool
  PrepareStmt            bool
  NewDB                  bool
  SkipHooks              bool
  SkipDefaultTransaction bool
  AllowGlobalUpdate      bool
  FullSaveAssociations   bool
  Context                context.Context
  Logger                 logger.Interface
  NowFunc                func() time.Time
}
```

#### DryRun

生成 `SQL` 但不执行。 它可以用于准备或测试生成的 SQL，例如：

```
// 新建会话模式
stmt := db.Session(&Session{DryRun: true}).First(&user, 1).Statement
stmt.SQL.String() //=> SELECT * FROM `users` WHERE `id` = $1 ORDER BY `id`
stmt.Vars         //=> []interface{}{1}

// 全局 DryRun 模式
db, err := gorm.Open(sqlite.Open("gorm.db"), &gorm.Config{DryRun: true})

// 不同的数据库生成不同的 SQL
stmt := db.Find(&user, 1).Statement
stmt.SQL.String() //=> SELECT * FROM `users` WHERE `id` = $1 // PostgreSQL
stmt.SQL.String() //=> SELECT * FROM `users` WHERE `id` = ?  // MySQL
stmt.Vars         //=> []interface{}{1}
```

你可以使用下面的代码生成最终的 SQL：

```
// 注意：SQL 并不总是能安全地执行，GORM 仅将其用于日志，它可能导致会 SQL 注入
db.Dialector.Explain(stmt.SQL.String(), stmt.Vars...)
// SELECT * FROM `users` WHERE `id` = 1
```

#### 预编译

`PreparedStmt` 在执行任何 SQL 时都会创建一个 prepared statement 并将其缓存，以提高后续的效率，例如：

```
// 全局模式，所有 DB 操作都会创建并缓存预编译语句
db, err := gorm.Open(sqlite.Open("gorm.db"), &gorm.Config{
  PrepareStmt: true,
})

// 会话模式
tx := db.Session(&Session{PrepareStmt: true})
tx.First(&user, 1)
tx.Find(&users)
tx.Model(&user).Update("Age", 18)

// returns prepared statements manager
stmtManger, ok := tx.ConnPool.(*PreparedStmtDB)

// 关闭 *当前会话* 的预编译模式
stmtManger.Close()

// 为 *当前会话* 预编译 SQL
stmtManger.PreparedSQL // => []string{}

// 为当前数据库连接池的（所有会话）开启预编译模式
stmtManger.Stmts // map[string]*sql.Stmt

for sql, stmt := range stmtManger.Stmts {
  sql  // 预编译 SQL
  stmt // 预编译模式
  stmt.Close() // 关闭预编译模式
}
```



#### NewDB

通过 `NewDB` 选项创建一个不带之前条件的新 DB，例如：

```
tx := db.Where("name = ?", "jinzhu").Session(&gorm.Session{NewDB: true})

tx.First(&user)
// SELECT * FROM users ORDER BY id LIMIT 1

tx.First(&user, "id = ?", 10)
// SELECT * FROM users WHERE id = 10 ORDER BY id

// 不带 `NewDB` 选项
tx2 := db.Where("name = ?", "jinzhu").Session(&gorm.Session{})
tx2.First(&user)
// SELECT * FROM users WHERE name = "jinzhu" ORDER BY id
```



#### 跳过钩子

如果您想跳过 `钩子` 方法，您可以使用 `SkipHooks` 会话模式，例如：

```
DB.Session(&gorm.Session{SkipHooks: true}).Create(&user)

DB.Session(&gorm.Session{SkipHooks: true}).Create(&users)

DB.Session(&gorm.Session{SkipHooks: true}).CreateInBatches(users, 100)

DB.Session(&gorm.Session{SkipHooks: true}).Find(&user)

DB.Session(&gorm.Session{SkipHooks: true}).Delete(&user)

DB.Session(&gorm.Session{SkipHooks: true}).Model(User{}).Where("age > ?", 18).Updates(&user)
```

#### 禁用嵌套事务

在一个 DB 事务中使用 `Transaction` 方法，GORM 会使用 `SavePoint(savedPointName)`，`RollbackTo(savedPointName)` 为你提供嵌套事务支持。 你可以通过 `DisableNestedTransaction` 选项关闭它，例如：

```
db.Session(&gorm.Session{
  DisableNestedTransaction: true,
}).CreateInBatches(&users, 100)
```

#### AllowGlobalUpdate

GORM 默认不允许进行全局 update/delete，该操作会返回 `ErrMissingWhereClause` 错误。 您可以通过将一个选项设置为 true 来启用它，例如：

```
db.Session(&gorm.Session{
  AllowGlobalUpdate: true,
}).Model(&User{}).Update("name", "jinzhu")
// UPDATE users SET `name` = "jinzhu"
```

#### FullSaveAssociations

在创建、更新记录时，GORM 会通过 [Upsert](https://gorm.io/zh_CN/docs/create.html#upsert) 自动保存关联及其引用记录。 如果您想要更新关联的数据，您应该使用 `FullSaveAssociations` 模式，例如：

```
db.Session(&gorm.Session{FullSaveAssociations: true}).Updates(&user)
// ...
// INSERT INTO "addresses" (address1) VALUES ("Billing Address - Address 1"), ("Shipping Address - Address 1") ON DUPLICATE KEY SET address1=VALUES(address1);
// INSERT INTO "users" (name,billing_address_id,shipping_address_id) VALUES ("jinzhu", 1, 2);
// INSERT INTO "emails" (user_id,email) VALUES (111, "jinzhu@example.com"), (111, "jinzhu-2@example.com") ON DUPLICATE KEY SET email=VALUES(email);
// ...
```

#### Context

通过 `Context` 选项，您可以传入 `Context` 来追踪 SQL 操作，例如：

```
timeoutCtx, _ := context.WithTimeout(context.Background(), time.Second)
tx := db.Session(&Session{Context: timeoutCtx})

tx.First(&user) // 带 timeoutCtx 的查询
tx.Model(&user).Update("role", "admin") // 带 timeoutCtx 的更新
```

GORM 也提供了快捷调用方法 `WithContext`，其实现如下：

```
func (db *DB) WithContext(ctx context.Context) *DB {
  return db.Session(&Session{Context: ctx})
}
```

#### Logger

Gorm 允许使用 `Logger` 选项自定义内建 Logger，例如：

```
newLogger := logger.New(log.New(os.Stdout, "\r\n", log.LstdFlags),
              logger.Config{
                SlowThreshold: time.Second,
                LogLevel:      logger.Silent,
                Colorful:      false,
              })
db.Session(&Session{Logger: newLogger})

db.Session(&Session{Logger: logger.Default.LogMode(logger.Silent)})
```

查看 [Logger](https://gorm.io/zh_CN/docs/logger.html) 获取详情.



#### NowFunc

`NowFunc` 允许改变 GORM 获取当前时间的实现，例如：

```
db.Session(&Session{
  NowFunc: func() time.Time {
    return time.Now().Local()
  },
})
```

#### Debug

`Debug` 只是将会话的 `Logger` 修改为调试模式的快捷方法，其实现如下：

```
func (db *DB) Debug() (tx *DB) {
  return db.Session(&Session{
    Logger:  db.Logger.LogMode(logger.Info),
  })
}
```

#### QueryFields

Select by fields

```
db.Session(&gorm.Session{QueryFields: true}).Find(&user)
// SELECT `users`.`name`, `users`.`age`, ... FROM `users` // 带该选项
// SELECT * FROM `users` // 不带该选项
```



#### CreateBatchSize

Default batch size

```
users = [5000]User{{Name: "jinzhu", Pets: []Pet{pet1, pet2, pet3}}...}

db.Session(&gorm.Session{CreateBatchSize: 1000}).Create(&users)
// INSERT INTO users xxx (需 5 次)
// INSERT INTO pets xxx (需 15 次)
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


// 注册Create进程的回调
db.Callback().Create().Register("update_created_at", updateCreated)

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
- Row Query callbacks      将在运行`Row`或`Rows`时被调用，默认情况下没有注册的回调，你可以注册一个新的回调

```go
func updateTableName(scope *gorm.Scope) {
  scope.Search.Table(scope.TableName() + "_draft") // append `_draft` to table name
}

db.Callback().RowQuery().Register("publish:update_table_name", updateTableName)
```



## 11.更新日志

> v1.0,  20170111

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

