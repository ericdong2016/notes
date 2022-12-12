# gin

## 1. 文档

```
https://www.tizi365.com/archives/268.html     // gin入门版

https://www.jianshu.com/p/98965b3ff638/       // gin 中文版

https://github.com/gin-gonic/gin/blob/master/README.md

https://github.com/gin-gonic/examples/       // gin代码示例


# 参考资料
https://www.bilibili.com/video/BV1gJ411p7xC?from=search&seid=13293894302045145985

https://www.bilibili.com/video/BV1xf4y1m7bW?from=search&seid=13293894302045145985

https://www.bilibili.com/video/BV1Ka4y1a7wN?from=search&seid=13293894302045145985

https://www.bilibili.com/video/BV1RQ4y1N7bC?from=search&seid=13293894302045145985

https://www.bilibili.com/video/BV1pz4y1D7Sx?from=search&seid=13293894302045145985


# 重点看博客中的其他内容
https://laravelacademy.org/books/gin-tutorial

https://laravelacademy.org/books/high-performance-mysql

https://laravelacademy.org/books/microservices

https://laravelacademy.org/books/network-protocols

# 极客兔兔
https://geektutu.com/post/quick-go-gin.html#%E7%83%AD%E5%8A%A0%E8%BD%BD%E8%B0%83%E8%AF%95-Hot-Reload

https://geektutu.com/post/gee.html

https://geektutu.com/post/high-performance-go.html

https://geektutu.com/post/qa-golang.html

# 插件化开发
https://studygolang.com/articles/13977
```



## 2. 简介

```
Gin是一个golang的微框架，封装比较优雅，API友好，源码注释比较明确，具有快速灵活，容错方便等特点

对于golang而言，web框架的依赖要远比Python，Java之类的要小。自身的net/http足够简单，性能也非常不错

借助框架开发，不仅可以省去很多常用的封装带来的时间，也有助于团队的编码风格和形成规范
```



## 3. 安装与测试

安装：

```sh
go get -u github.com/gin-gonic/gin
```
`
注意：确保 GOPATH GOROOT 已经配置
`

导入：
```go
import "github.com/gin-gonic/gin"
```

测试:

```go
package main

import (
    "net/http"
    "github.com/gin-gonic/gin"
)

func main() {
   // 1.创建路由
   r := gin.Default()
   // 2.绑定路由规则，执行的函数
   // gin.Context，封装了request和response
   r.GET("/", func(c *gin.Context) {
      c.String(http.StatusOK, "hello World!")
   })
   // 3.监听端口，默认在8080
   // Run("里面不指定端口号默认为8080")
   r.Run(":8000")
}
```



## 4. 架构





## 5. 路由

> gin 框架中采用的路由库是 httprouter
>
> httprouter原理分析:
>
> https://zhuanlan.zhihu.com/p/139411081
>
> https://blog.csdn.net/weixin_41315492/article/details/103905721
>
> https://www.cnblogs.com/foxy/p/9469401.html

### 5.1 基本路由

一条路由规则由三部分组成：

- http请求方法
- url路径
- 控制器函数

#### 1. 请求方法

常用的http请求方法有下面4种:

- GET
- POST
- PUT
- DELETE

#### 2. 路径规则

url路径有三种写法：

- 静态url路径
- 带路径参数的url路径
- 带星号（*）模糊匹配(正则匹配)参数的url路径

下面看下各种url路由的例子

```
// 例子1, 静态Url路径, 即不带任何参数的url路径
/users/center
/user/111
/food/123

// 例子2, 带路径参数的url路径, url路径上面带有参数, 参数由冒号（:）跟着一个字符串定义。
// 路径参数值可以是数值，也可以是字符串

//定义参数:id， 可以匹配/user/1, /user/899, /user/xiaoli 这类Url路径
/user/:id
//定义参数:id， 可以匹配/food/2, /food/100, /food/apple 这类Url路径
/food/:id
//定义参数:type和:page， 可以匹配/foods/2/1, /food/100/25, /food/apple/30 这类Url路径
/foods/:type/:page

// 例子3. 带星号（*）模糊匹配参数的url路径
// 星号代表匹配任意路径的意思, 必须在*号后面指定一个参数名，后面可以通过这个参数获取*号匹配的内容。

//以/foods/* 开头的所有路径都匹配
//匹配：/foods/1， /foods/200, /foods/1/20, /foods/apple/1 
/foods/*path
//可以通过path参数获取*号匹配的内容。
```

#### 3. 控制器函数

控制器函数定义：

```
func xxx(c *gin.Context)

控制器函数接受一个上下文参数。
可以通过上下文参数，获取http请求参数，响应http请求。
```



#### 4. 使用示例

```
//实例化gin实例对象。
r := gin.Default()
	
//定义post请求, url路径为：/users, 绑定saveUser控制器函数
r.POST("/users", saveUser)

//定义get请求，url路径为：/users/:id（:id是参数，例如: /users/10, 会匹配这个url模式），绑定getUser控制器函数
r.GET("/users/:id", getUser)

//定义put请求
r.PUT("/users/:id", updateUser)

//定义delete请求
r.DELETE("/users/:id", deleteUser)


//控制器函数实现
func saveUser(c *gin.Context) {
    ...忽略实现...
}

func getUser(c *gin.Context) {
    ...忽略实现...
}

func updateUser(c *gin.Context) {
    ...忽略实现...
}

func deleteUser(c *gin.Context) {
    ...忽略实现...
}
```

> 提示：实际项目开发中不要把路由定义和控制器函数都写在一个go文件，不方便维护，可以参考第一章的项目结构，规划自己的业务模块。



### 5.2 分组路由

```go
func main() {
    router := gin.Default()

    // Simple group: v1
    v1 := router.Group("/v1")
    {
        v1.POST("/login", loginEndpoint)
        v1.POST("/submit", submitEndpoint)
        v1.POST("/read", readEndpoint)
    }

    // Simple group: v2
    v2 := router.Group("/v2")
    {
        v2.POST("/login", loginEndpoint)
        v2.POST("/submit", submitEndpoint)
        v2.POST("/read", readEndpoint)
    }

    router.Run(":8080")
}
```

上面的例子将会注册下面的路由信息：

- /v1/login
- /v1/submit
- /v1/read
- /v2/login
- /v2/submit
- /v2/read

路由分组，其实就是设置了同一类路由的url前缀。



### 5.3 路由拆分

#### 5.3.1 路由拆分成多个文件

当我们的业务规模继续膨胀，单独的一个routers文件或包已经满足不了我们的需求了

```go
func SetupRouter() *gin.Engine {
    r := gin.Default()
    r.GET("/topgoer", helloHandler)
    r.GET("/xx1", xxHandler1)
    r.GET("/xx30", xxHandler30)
    return r
}
```

因为我们把所有的路由注册都写在一个SetupRouter函数中的话就会太复杂了。

我们可以分开定义多个路由文件，例如：

```
gin_demo
├── go.mod
├── go.sum
├── main.go
└── routers
    ├── blog.go
    └── shop.go
```

routers/shop.go中添加一个LoadShop的函数，将shop相关的路由注册到指定的路由器：

```
func LoadShop(e *gin.Engine)  {
    e.GET("/hello", helloHandler)
    e.GET("/goods", goodsHandler)
    e.GET("/checkout", checkoutHandler)
}
```

routers/blog.go中添加一个LoadBlog的函数，将blog相关的路由注册到指定的路由器：

```go
func LoadBlog(e *gin.Engine) {
    e.GET("/post", postHandler)
    e.GET("/comment", commentHandler)
}
```

在main函数中实现最终的注册逻辑如下：

```go
func main() {
    r := gin.Default()
    routers.LoadBlog(r)
    routers.LoadShop(r)
    if err := r.Run(); err != nil {
        fmt.Println("startup service failed, err:%v\n", err)
    }
}
```

#### 5.3.2 路由拆分到不同的APP

有时候项目规模实在太大，那么我们就更倾向于把业务拆分的更详细一些，例如把不同的业务代码拆分成不同的APP。

因此我们在项目目录下单独定义一个app目录，用来存放我们不同业务线的代码文件，这样就很容易进行横向扩展。大致目录结构如下：

```
gin_demo
├── app
│   ├── blog
│   │   ├── handler.go
│   │   └── router.go
│   └── shop
│       ├── handler.go
│       └── router.go
├── go.mod
├── go.sum
├── main.go
└── routers
    └── routers.go
```

其中app/blog/router.go用来定义post相关路由信息，具体内容如下：

```go
func Routers(e *gin.Engine) {
    e.GET("/post", postHandler)
    e.GET("/comment", commentHandler)
}
```

app/shop/router.go用来定义shop相关路由信息，具体内容如下：

```go
func Routers(e *gin.Engine) {
    e.GET("/goods", goodsHandler)
    e.GET("/checkout", checkoutHandler)
}
```

routers/routers.go中根据需要定义Include函数用来注册子app中定义的路由，Init函数用来进行路由的初始化操作：

```go
type Option func(*gin.Engine)

var options = []Option{}

// 注册app的路由配置
func Include(opts ...Option) {
    options = append(options, opts...)
}

// 初始化
func Init() *gin.Engine {
    r := gin.New()
    for _, opt := range options {
        opt(r)
    }
    return r
}
```

main.go中按如下方式先注册子app中的路由，然后再进行路由的初始化：

```go
func main() {
    // 加载多个APP的路由配置
    routers.Include(shop.Routers, blog.Routers)
    // 初始化路由
    r := routers.Init()
    if err := r.Run(); err != nil {
        fmt.Println("startup service failed, err:%v\n", err)
    }
}
```

转自：https://www.liwenzhou.com/posts/Go/gin_routes_registry/





## 6. 请求

### 6.1 获取get参数

#### 6.1.1  url参数

*/path?id=1234&name=Manu&value=*111

常用函数：

- **func** (c *Context) **Query**(key string)  string
- **func** (c *Context) **DefaultQuery**(key, defaultValue string)  string
- **func** (c *Context) **GetQuery**(key string)  (string, bool)

例子：

```
func Handler(c *gin.Context) {
	//获取name参数, 通过Query获取的参数值是String类型。
	name := c.Query("name")

    //获取name参数, 跟Query函数的区别是，可以通过第二个参数设置默认值。
    name := c.DefaultQuery("name", "tizi365")

	//获取id参数, 通过GetQuery获取的参数值也是String类型, 
	// 区别是GetQuery返回两个参数，第一个是参数值，第二个参数是参数是否存在的bool值，可以用来判断参数是否存在。
	id, ok := c.GetQuery("id")
    if !ok {
	   // 参数不存在
	}
}
```

提示：GetQuery函数，判断参数是否存在的逻辑是，参数值为空，参数也算存在，只有没有提交参数，才算参数不存在。



#### 6.1.2  api参数

***/user/:id*** 这类型路由绑定的参数，这个例子绑定了一个参数id。

常用函数：

- **func** (c *Context) **Param**(key string)  string

例子：

```
r := gin.Default()
	
r.GET("/user/:id", func(c *gin.Context) {
	// 获取url参数id
	id := c.Param("id")
})
```



### 6.2 获取post参数

获取Post请求参数的常用函数：

- **func** (c *Context) **PostForm**(key string)  string
- **func** (c *Context) **DefaultPostForm**(key, defaultValue string)  string
- **func** (c *Context) **GetPostForm**(key string)  (string, bool)

例子：

```
func Handler(c *gin.Context) {
	//获取name参数, 通过PostForm获取的参数值是String类型。
	name := c.PostForm("name")

	// 跟PostForm的区别是可以通过第二个参数设置参数默认值
	name := c.DefaultPostForm("name", "tizi365")

	//获取id参数, 通过GetPostForm获取的参数值也是String类型,
	// 区别是GetPostForm返回两个参数，第一个是参数值，第二个参数是参数是否存在的bool值，可以用来判断参数是否存在。
	id, ok := c.GetPostForm("id")
	if !ok {
	    // 参数不存在
	}
}
```

### 6.3 获取混合参数

#### 6.3.1 

```
POST /post?id=1234&page=1 
Content-Type: application/x-www-form-urlencoded
query string params:    name=manu&message=this_is_great
```

```go

func main() {
    router := gin.Default()
    router.POST("/post", func(c *gin.Context) {

        id := c.Query("id")
        page := c.DefaultQuery("page", "0")
        name := c.PostForm("name")
        message := c.PostForm("message")

        fmt.Printf("id: %s; page: %s; name: %s; message: %s", id, page, name, message)
    })
    router.Run(":8080")
}
```

```
id: 1234; page: 1; name: manu; message: this_is_great
```

#### 6.3.2 

> map 作为  查询参数或者 postform参数

```
POST /post?ids[a]=1234&ids[b]=hello
Content-Type: application/x-www-form-urlencoded
request body: 
			names[first]=thinkerou  
			names[second]=tianou
```

```
func main() {
	router := gin.Default()

	router.POST("/post", func(c *gin.Context) {
		ids := c.QueryMap("ids")
		names := c.PostFormMap("names")

		fmt.Printf("ids: %v; names: %v", ids, names)
	})
	router.Run(":8080")
}
```

```
ids: map[b:hello a:1234], names: map[second:tianou first:thinkerou]
```



### 6.4 文件上传

#### 6.4.1 单文件

```go
// 慎用 file.Filename ，参考 Content-Disposition on MDN 和 #1693
// 上传文件的文件名可以由用户自定义，所以可能包含非法字符串，为了安全起见，应该由服务端统一文件名规则

func main() {
    router := gin.Default()
    // 给表单限制上传大小 (默认 32 MiB)
    // router.MaxMultipartMemory = 8 << 20  // 8 MiB
    router.POST("/upload", func(c *gin.Context) {
        // 单文件
        file, _ := c.FormFile("file")
        log.Println(file.Filename)

        // 上传文件到指定的路径
        // c.SaveUploadedFile(file, dst)

        c.String(http.StatusOK, fmt.Sprintf("'%s' uploaded!", file.Filename))
    })
    router.Run(":8080")
}

//curl:
curl -X POST http://localhost:8080/upload \
  -F "file=@/Users/appleboy/test.zip" \
  -H "Content-Type: multipart/form-data"
```



#### 6.4.2 多文件

```go
func main() {
    router := gin.Default()
    // 给表单限制上传大小 (默认 32 MiB)
    // router.MaxMultipartMemory = 8 << 20  // 8 MiB
    router.POST("/upload", func(c *gin.Context) {
        // 多文件
        form, _ := c.MultipartForm()
        files := form.File["upload[]"]

        for _, file := range files {
            log.Println(file.Filename)

            // 上传文件到指定的路径
            // c.SaveUploadedFile(file, dst)
        }
        c.String(http.StatusOK, fmt.Sprintf("%d files uploaded!", len(files)))
    })
    router.Run(":8080")
}

// curl
curl -X POST http://localhost:8080/upload \
  -F "upload[]=@/Users/appleboy/test1.zip" \
  -F "upload[]=@/Users/appleboy/test2.zip" \
  -H "Content-Type: multipart/form-data"
```





### 6.5 绑定参数(难点)

#### 6.5.1 绑定模型

Gin使用 [go-playground/validator.v8](https://github.com/go-playground/validator) 验证参数，[查看完整文档](https://godoc.org/gopkg.in/go-playground/validator.v8#hdr-Baked_In_Validators_and_Tags)。



首先，需要在绑定的字段上设置tag，比如，绑定格式为json，需要这样设置 `json:"fieldname"` 

然后，通过Gin提供的两套绑定方法：

Must bind

- Methods  
- `Bind`, `BindJSON`, `BindXML`, `BindQuery`, `BindYAML` 
- Behavior - 这些方法底层使用 `MustBindWith`，如果存在绑定错误，请求将被以下指令中止 `c.AbortWithError(400, err).SetType(ErrorTypeBind)`，响应状态代码会被设置为400，请求头`Content-Type`被设置为`text/plain; charset=utf-8`。注意，如果你试图在此之后设置响应代码，将会发出一个警告 `[GIN-debug] [WARNING] Headers were already written. Wanted to override status code 400 with 422`，如果你希望更好地控制行为，请使用`ShouldBind`相关的方法


Should bind

  - Methods
      - `ShouldBind(form,包括html中的复选框 或者 一些不确定的场景)`, `ShouldBindJSON`, `ShouldBindXML`, `ShouldBindQuery`, `ShouldBindYAML`, `ShouldBindUri` 
  - Behavior - 这些方法底层使用 `ShouldBindWith`，如果存在绑定错误，则返回错误，开发人员可以正确处理请求和错误。



当我们使用绑定方法时，Gin会根据Content-Type推断出使用哪种绑定器，如果你确定你绑定的是什么，你可以使用`MustBindWith`或者`BindingWith`。

你还可以给字段指定特定规则的修饰符，如果一个字段用`binding:"required"`修饰，并且在绑定时该字段的值为空，那么将返回一个错误。



```
// 绑定为json，xml, form
type Login struct {
    User     string `form:"user" json:"user" xml:"user"  binding:"required"`
    Password string `form:"password" json:"password" xml:"password" binding:"required"`
}

func main() {
    router := gin.Default()

    // Example for binding JSON ({"user": "manu", "password": "123"})
    router.POST("/loginJSON", func(c *gin.Context) {
        var json Login
        if err := c.ShouldBindJSON(&json); err != nil {
            c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
            return
        }
        
        if json.User != "manu" || json.Password != "123" {
            c.JSON(http.StatusUnauthorized, gin.H{"status": "unauthorized"})
            return
        } 
        
        c.JSON(http.StatusOK, gin.H{"status": "you are logged in"})
    })

    // Example for binding XML
    
    //  <?xml version="1.0" encoding="UTF-8"?>
    //  <root>
    //      <user>user</user>
    //      <password>123</password>
    //  </root>
    router.POST("/loginXML", func(c *gin.Context) {
        var xml Login
        if err := c.ShouldBindXML(&xml); err != nil {
            c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
            return
        }
        
        if xml.User != "manu" || xml.Password != "123" {
            c.JSON(http.StatusUnauthorized, gin.H{"status": "unauthorized"})
            return
        } 
        
        c.JSON(http.StatusOK, gin.H{"status": "you are logged in"})
    })


    // Example for binding a HTML form (user=manu&password=123)
    router.POST("/loginForm", func(c *gin.Context) {
        var form Login
        // This will infer what binder to use depending on the content-type header.
        if err := c.ShouldBind(&form); err != nil {
            c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
            return
        }
        
        if form.User != "manu" || form.Password != "123" {
            c.JSON(http.StatusUnauthorized, gin.H{"status": "unauthorized"})
            return
        } 
        
        c.JSON(http.StatusOK, gin.H{"status": "you are logged in"})
    })

    // Listen and serve on 0.0.0.0:8080
    router.Run(":8080")
}
```

**请求示例：**

```
$ curl -v -X POST \
  http://localhost:8080/loginJSON \
  -H 'content-type: application/json' \
  -d '{ "user": "manu", "passwd": "456" }'
  
> POST /loginJSON HTTP/1.1
> Host: localhost:8080
> User-Agent: curl/7.51.0
> Accept: */*
> content-type: application/json
> Content-Length: 18
>
* upload completely sent off: 18 out of 18 bytes
< HTTP/1.1 400 Bad Request
< Content-Type: application/json; charset=utf-8
< Date: Fri, 04 Aug 2017 03:51:31 GMT
< Content-Length: 100
<
{"error":"Key: 'Login.Password' Error:Field validation for 'Password' failed on the 'required' tag"}
```

**跳过验证：**

当使用上面的curl命令运行上面的示例时，返回错误，因为示例中`Password`字段使用了`binding:"required"`，如果我们使用`binding:"-"`，那么它就不会报错。



#### 6.5.2 绑定get参数

`ShouldBindQuery` 函数只绑定Get参数，不绑定post数据，[查看详细信息](https://github.com/gin-gonic/gin/issues/742#issuecomment-315953017)

```
package main

import (
    "log"
    "github.com/gin-gonic/gin"
)

type Person struct {
    Name    string `form:"name"`
    Address string `form:"address"`
}

func main() {
    route := gin.Default()
    route.Any("/testing", startPage)
    route.Run(":8085")
}

func startPage(c *gin.Context) {
    var person Person
     
    if c.ShouldBindQuery(&person) == nil {
        log.Println("====== Only Bind By Query String ======")
        log.Println(person.Name)
        log.Println(person.Address)
    }
    c.String(200, "Success")
}


curl http://127.0.0.1:8085/testing?name=xxx&address=yyy
```



#### 6.5.3 绑定Post参数

```
package main

import (
    "github.com/gin-gonic/gin"
)

type LoginForm struct {
    User     string `form:"user" binding:"required"`
    Password string `form:"password" binding:"required"`
}

func main() {
    router := gin.Default()
    router.POST("/login", func(c *gin.Context) {
        // you can bind multipart form with explicit binding declaration:
        // c.ShouldBindWith(&form, binding.Form)
        // or you can simply use autobinding with ShouldBind method:

        var form LoginForm
        // in this case proper binding will be automatically selected
        if c.ShouldBind(&form) == nil {
            if form.User == "user" && form.Password == "password" {
                c.JSON(200, gin.H{"status": "you are logged in"})
            } else {
                c.JSON(401, gin.H{"status": "unauthorized"})
            }
        }
    })
    router.Run(":8080")
}


curl -v --form user=user --form password=password  http://localhost:8080/login
```



#### 6.5.4 绑定Get或Post

> 没明白什么意思？

```
package main

import (
    "log"
    "time"

    "github.com/gin-gonic/gin"
)

type Person struct {
    Name     string    `form:"name"`
    Address  string    `form:"address"`
    Birthday time.Time `form:"birthday" time_format:"2006-01-02" time_utc:"1"`
}

func main() {
    route := gin.Default()
    route.GET("/testing", startPage)
    route.Run(":8085")
}

func startPage(c *gin.Context) {
    var person Person
    // If `GET`, only `Form` binding engine (`query`) used.
    // 如果是Get，那么接收不到请求中的Post的数据？？
    // 如果是Post, 首先判断 `content-type` 的类型 `JSON` or `XML`, 然后使用对应的绑定器获取数据.
    // See more at https://github.com/gin-gonic/gin/blob/master/binding/binding.go#L48
    
    if c.ShouldBind(&person) == nil {
        log.Println(person.Name)
        log.Println(person.Address)
        log.Println(person.Birthday)
    }

    c.String(200, "Success")
}
```

#### 6.5.5 绑定uri

```
package main

import "github.com/gin-gonic/gin"

// 绑定uri
type Person struct {
    ID string  `uri:"id" binding:"required,uuid"`
    Name string  `uri:"name" binding:"required"`
}

func main() {
    route := gin.Default()
    route.GET("/:name/:id", func(c *gin.Context) {
        var person Person
        if err := c.ShouldBindUri(&person); err != nil {
            c.JSON(400, gin.H{"msg": err})
            return
        }
        c.JSON(200, gin.H{"name": person.Name, "uuid": person.ID})
    })
    route.Run(":8088")
}
```

测试用例：

```
$ curl -v localhost:8088/thinkerou/987fbc97-4bed-5078-9f07-9141ba07c9f3
$ curl -v localhost:8088/thinkerou/not-uuid
```



#### 6.5.6 绑定HTML复选框

main.go

```
type myForm struct {
    Colors []string `form:"colors[]"`
}


func formHandler(c *gin.Context) {
    var fakeForm myForm
    c.ShouldBind(&fakeForm)
    c.JSON(200, gin.H{"color": fakeForm.Colors})
}
```

form.html

```
<form action="/" method="POST">
    <p>Check some colors</p>
    <label for="red">Red</label>
    <input type="checkbox" name="colors[]" value="red" id="red">
    
    <label for="green">Green</label>
    <input type="checkbox" name="colors[]" value="green" id="green">
    
    <label for="blue">Blue</label>
    <input type="checkbox" name="colors[]" value="blue" id="blue">
    
    <input type="submit">
</form>
```

result:

```
{"color":["red","green","blue"]}
```



### 6.6 验证器(难点)

#### 6.6.1 自定义验证器

> v9 后的写法很友好

```
package main

import (
    "net/http"
    "reflect"
    "time"

    "github.com/gin-gonic/gin"
    "github.com/gin-gonic/gin/binding"
    "gopkg.in/go-playground/validator.v8"
)

// Booking contains binded and validated data.
type Booking struct {
	//3.使用， 注意required,bookabledate  之间是没有空格的， 时间格式2006-01-02是个固定值，源码中定义的
    CheckIn  time.Time `form:"check_in" binding:"required,bookabledate" time_format:"2006-01-02"`    
    CheckOut time.Time `form:"check_out" binding:"required,gtfield=CheckIn" time_format:"2006-01-02"`
}

// 1. 定义自定义的验证器，当前日期是否可预订, 用到了反射
// v8/v9
func bookableDate(
	// 标准格式，直接copy
    v *validator.Validate, topStruct reflect.Value, currentStructOrField reflect.Value,
    field reflect.Value, fieldType reflect.Type, fieldKind reflect.Kind, param string,
) bool {
    if date, ok := field.Interface().(time.Time); ok {
        // 验证器逻辑
        today := time.Now()
        if today.Year() > date.Year() || today.YearDay() > date.YearDay() {
            return false
        }
    }
    return true
}

//v10 
var bookableDate validator.Func = func(fl validator.FieldLevel) bool {
   if date, ok := fl.Field().(time.Time); ok {
        // 验证器逻辑
        today := time.Now()
        if today.Year() > date.Year() || today.YearDay() > date.YearDay() {
            return false
        }
    }
    return true
}


func main() {
    route := gin.Default()
	
	// 2. 注册验证器
    if v, ok := binding.Validator.Engine().(*validator.Validate); ok {
        // 前面是验证器使用时的名字，后面是方法
        v.RegisterValidation("bookabledate", bookableDate)
    }	

    route.GET("/bookable", getBookable)
    route.Run(":8085")
}

func getBookable(c *gin.Context) {
    var b Booking
    // 4. 传递参数并验证
    if err := c.ShouldBindWith(&b, binding.Query); err == nil {
        c.JSON(http.StatusOK, gin.H{"message": "Booking dates are valid!"})
    } else {
        c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
    }
}



curl "localhost:8085/bookable?check_in=2018-04-16&check_out=2018-04-17"
{"message":"Booking dates are valid!"}

curl "localhost:8085/bookable?check_in=2018-03-08&check_out=2018-03-07"
{"error":"Key: 'Booking.CheckIn' Error:Field validation for 'CheckIn' failed on the '
```



#### 6.6.2 多语言验证

当业务系统对验证信息有特殊需求时，例如：返回信息需要自定义，手机端返回的信息需要是中文， 而pc端发挥返回的信息需要时英文，如何做到请求一个接口满足上述三种情况。

```go
package main

import (
    "fmt"

    "github.com/gin-gonic/gin"
    "github.com/go-playground/locales/en"
    "github.com/go-playground/locales/zh"
    "github.com/go-playground/locales/zh_Hant_TW"
    ut "github.com/go-playground/universal-translator"
    "gopkg.in/go-playground/validator.v9"
    en_translations "gopkg.in/go-playground/validator.v9/translations/en"
    zh_translations "gopkg.in/go-playground/validator.v9/translations/zh"
    zh_tw_translations "gopkg.in/go-playground/validator.v9/translations/zh_tw"
)

var (
    Uni      *ut.UniversalTranslator
    Validate *validator.Validate
)

type User struct {
    Username string `form:"user_name" validate:"required"`
    Tagline  string `form:"tag_line" validate:"required,lt=10"`
    Tagline2 string `form:"tag_line2" validate:"required,gt=1"`
}

func main() {
    en := en.New()
    zh := zh.New()
    zh_tw := zh_Hant_TW.New()
    Uni = ut.New(en, zh, zh_tw)
    Validate = validator.New()

    route := gin.Default()
    route.GET("/5lmh", startPage)
    route.POST("/5lmh", startPage)
    route.Run(":8080")
}

func startPage(c *gin.Context) {
    //这部分应放到中间件中
    locale := c.DefaultQuery("locale", "zh")
    trans, _ := Uni.GetTranslator(locale)
    switch locale {
    case "zh":
        zh_translations.RegisterDefaultTranslations(Validate, trans)
        break
    case "en":
        en_translations.RegisterDefaultTranslations(Validate, trans)
        break
    case "zh_tw":
        zh_tw_translations.RegisterDefaultTranslations(Validate, trans)
        break
    default:
        zh_translations.RegisterDefaultTranslations(Validate, trans)
        break
    }

    //自定义错误内容
    Validate.RegisterTranslation("required", trans, func(ut ut.Translator) error {
        return ut.Add("required", "{0} must have a value!", true) // see universal-translator for details
    }, func(ut ut.Translator, fe validator.FieldError) string {
        t, _ := ut.T("required", fe.Field())
        return t
    })

    //这块应该放到公共验证方法中
    user := User{}
    c.ShouldBind(&user)
    fmt.Println(user)
    err := Validate.Struct(user)
    if err != nil {
        errs := err.(validator.ValidationErrors)
        sliceErrs := []string{}
        for _, e := range errs {
            sliceErrs = append(sliceErrs, e.Translate(trans))
        }
        c.String(200, fmt.Sprintf("%#v", sliceErrs))
    }
    c.String(200, fmt.Sprintf("%#v", "user"))
}
```

*正确的链接：http://localhost:8080/testing?user_name=枯藤&tag_line=9&tag_line2=33&locale=zh*

*http://localhost:8080/testing?user_name=枯藤&tag_line=9&tag_line2=3&locale=en 返回英文的验证信息*

*http://localhost:8080/testing?user_name=枯藤&tag_line=9&tag_line2=3&locale=zh 返回中文的验证信息*



*查看更多的功能可以查看官网 gopkg.in/go-playground/validator.v9*





## 7. 响应

### 7.1 响应头

```
func(c *gin.Context) {
	//设置http响应 header, key/value方式，支持设置多个header
	c.Header("site","tizi365")
}
```



### 7.1  字符串

通过String函数返回字符串。

函数定义：

```
func (c *Context) String(code int, format string, values ...interface{})
```

参数说明：

| 参数   | 说明                                                         |
| :----- | :----------------------------------------------------------- |
| code   | http状态码                                                   |
| format | 返回结果，支持类似Sprintf函数一样的字符串格式定义，例如,%d 代表插入整数，%s代表插入字符串 |
| values | 任意个format参数定义的字符串格式参数                         |

例子：

```
func Handler(c *gin.Context)  {
	// 例子1：
	c.String(200, "欢迎访问tizi360.com!")
	
	// 例子2： 这里定义了两个字符串参数（两个%s），后面传入的两个字符串参数将会替换对应的%s
	c.String(200,"欢迎访问%s, 你是%s", "tizi360.com!","最靓的仔！")
}
```

> 提示： net/http包定义了多种常用的状态码常量，例如：http.StatusOK == 200， http.StatusMovedPermanently == 301， http.StatusNotFound == 404等，具体可以参考net/http包



### 7.2 JSON/XML/YAML...

> json
>
> xml
>
> yaml
>
> ProtoBuf

```
func main() {
    r := gin.Default()

    // gin.H is a shortcut for map[string]interface{}
    r.GET("/someJSON", func(c *gin.Context) {
        c.JSON(http.StatusOK, gin.H{"message": "hey", "status": http.StatusOK})
    })

    r.GET("/moreJSON", func(c *gin.Context) {
        // You also can use a struct
        var msg struct {
            Name    string `json:"user"`
            Message string
            Number  int
        }
        msg.Name = "Lena"
        msg.Message = "hey"
        msg.Number = 123
        // Note that msg.Name becomes "user" in the JSON
        // Will output  :   {"user": "Lena", "Message": "hey", "Number": 123}
        c.JSON(http.StatusOK, msg)
    })

    r.GET("/someXML", func(c *gin.Context) {
        c.XML(http.StatusOK, gin.H{"message": "hey", "status": http.StatusOK})
    })

    r.GET("/someYAML", func(c *gin.Context) {
        c.YAML(http.StatusOK, gin.H{"message": "hey", "status": http.StatusOK})
    })

    r.GET("/someProtoBuf", func(c *gin.Context) {
        reps := []int64{int64(1), int64(2)}
        label := "test"
        // The specific definition of protobuf is written in the testdata/protoexample file.
        data := &protoexample.Test{
            Label: &label,
            Reps:  reps,
        }
        // Note that data becomes binary data in the response
        // Will output protoexample.Test protobuf serialized data
        c.ProtoBuf(http.StatusOK, data)
    })

    // Listen and serve on 0.0.0.0:8080
    r.Run(":8080")
}
		
```
### 7.3 SecureJSON

> 使用SecureJSON可以防止json劫持，如果返回的数据是数组，则会默认在返回值前加上`"while(1)"`

```
func main() {
    r := gin.Default()

    // 可以自定义返回的json数据前缀
    // r.SecureJsonPrefix(")]}',\n")

    r.GET("/someJSON", func(c *gin.Context) {
        names := []string{"lena", "austin", "foo"}

        // 将会输出:   while(1);["lena","austin","foo"]
        c.SecureJSON(http.StatusOK, names)
    })

    // Listen and serve on 0.0.0.0:8080
    r.Run(":8080")
}
```



### 7.4 jsonp

> 使用JSONP可以跨域传输，如果参数中存在回调参数，那么返回的参数将是回调函数的形式

```
func main() {
    r := gin.Default()

    r.GET("/JSONP", func(c *gin.Context) {
        data := map[string]interface{}{
            "foo": "bar",
        }
        
        // 访问 http://localhost:8080/JSONP?callback=call
        // 将会输出:   call({foo:"bar"})
        c.JSONP(http.StatusOK, data)
    })

    // Listen and serve on 0.0.0.0:8080
    r.Run(":8080")
}
```



### 7.5 AsciiJSON

> 使用AsciiJSON将使特殊字符编码

```
func main() {
    r := gin.Default()

    r.GET("/someJSON", func(c *gin.Context) {
        data := map[string]interface{}{
            "lang": "GO语言",
            "tag":  "<br>",
        }

        // 将输出: {"lang":"GO\u8bed\u8a00","tag":"\u003cbr\u003e"}
        c.AsciiJSON(http.StatusOK, data)
    })

    // Listen and serve on 0.0.0.0:8080
    r.Run(":8080")
}
```



### 7.6 PureJSON

> 通常情况下，JSON会将特殊的HTML字符替换为对应的unicode字符，比如 `<` 替换为 `\u003c`，如果想原样输出html，则使用PureJSON，这个特性在Go 1.6及以下版本中无法使用。

```
func main() {
    r := gin.Default()
    
    // Serves unicode entities
    r.GET("/json", func(c *gin.Context) {
        c.JSON(200, gin.H{
            "html": "<b>Hello, world!</b>",
        })
    })
    
    // Serves literal characters
    r.GET("/purejson", func(c *gin.Context) {
        c.PureJSON(200, gin.H{
            "html": "<b>Hello, world!</b>",
        })
    })
    
    // listen and serve on 0.0.0.0:8080
    r.Run(":8080")
}
```



### 7.7 html

#### 7.7.1 返回html

先要使用 LoadHTMLTemplates() 方法来加载模板文件

```go
func main() {
	router := gin.Default()
	//加载模板
	router.LoadHTMLGlob("templates/*")
	//router.LoadHTMLFiles("templates/template1.html", "templates/template2.html")
	//定义路由
	router.GET("/index", func(c *gin.Context) {
		//根据完整文件名渲染模板，并传递参数
		c.HTML(http.StatusOK, "index.tmpl", gin.H{
			"title": "Main website",
		})
	})
	router.Run(":8080")
}
```

模板结构定义

```html
<html>
	<h1>
		{{ .title }}
	</h1>
</html>
```
#### 7.7.2 模板子目录问题

> 不同文件夹下模板名字可以相同，此时需要 LoadHTMLGlob() 加载两层模板路径

```go
router.LoadHTMLGlob("templates/**/*")
router.GET("/posts/index", func(c *gin.Context) {
	c.HTML(http.StatusOK, "posts/index.tmpl", gin.H{
		"title": "Posts",
	})
	c.HTML(http.StatusOK, "users/index.tmpl", gin.H{
		"title": "Users",
	})
	
}
```

模版文件：templates/posts/index.tmpl

```
{{ define "posts/index.tmpl" }}
<html><h1>
	{{ .title }}
</h1>
<p>Using posts/index.tmpl</p>
</html>
{{ end }}
```

模版文件：templates/users/index.tmpl

```
{{ define "users/index.tmpl" }}
<html><h1>
	{{ .title }}
</h1>
<p>Using users/index.tmpl</p>
</html>
{{ end }}
```

#### 7.7.3 自定义模板渲染器

```
import "html/template"

func main() {
    router := gin.Default()
    html := template.Must(template.ParseFiles("file1", "file2"))
    router.SetHTMLTemplate(html)
    router.Run(":8080")
}
```

#### 7.7.4 自定义渲染分隔符

```
r := gin.Default()
    r.Delims("{[{", "}]}")
    r.LoadHTMLGlob("/path/to/templates")
```



#### 7.7.5 自定义模板函数

> SetFuncMap

main.go

```
import (
    "fmt"
    "html/template"
    "net/http"
    "time"

    "github.com/gin-gonic/gin"
)

func formatAsDate(t time.Time) string {
    year, month, day := t.Date()
    return fmt.Sprintf("%d%02d/%02d", year, month, day)
}

func main() {
    router := gin.Default()
    router.Delims("{[{", "}]}")
    
    
    router.SetFuncMap(template.FuncMap{
        "formatAsDate": formatAsDate,
    })
    
    
    router.LoadHTMLFiles("./testdata/template/raw.tmpl")

    router.GET("/raw", func(c *gin.Context) {
        c.HTML(http.StatusOK, "raw.tmpl", map[string]interface{}{
            "now": time.Date(2017, 07, 01, 0, 0, 0, 0, time.UTC),
        })
    })

    router.Run(":8080")
}
```

raw.tmpl

然后就可以在html中直接使用formatAsDate函数了

```
Date: {[{.now | formatAsDate}]}
```

Result:

```
Date: 2017/07/01
```



### 7.8 静态文件

```
//获取当前文件的相对路径
router.Static("/assets", "/var/www/tizi365/assets")
router.StaticFS("/more_static", http.Dir("my_file_system"))
//获取相对路径下的文件
router.StaticFile("/favicon.ico", "./resources/favicon.ico")

```


### 7.9 重定向

```
r.GET("/redirect", func(c *gin.Context) {
	//支持内部和外部的重定向
    c.Redirect(http.StatusMovedPermanently, "http://www.baidu.com/")
})
```



### 7.10 返回第三方获取的数据

> DataFromReader

```go
func main() {
    router := gin.Default()
    router.GET("/someDataFromReader", func(c *gin.Context) {
        response, err := http.Get("https://raw.githubusercontent.com/gin-gonic/logo/master/color.png")
        if err != nil || response.StatusCode != http.StatusOK {
            c.Status(http.StatusServiceUnavailable)
            return
        }

        reader := response.Body
        contentLength := response.ContentLength
        contentType := response.Header.Get("Content-Type")

        extraHeaders := map[string]string{
            "Content-Disposition": `attachment; filename="gopher.png"`,
        }

        c.DataFromReader(http.StatusOK, contentLength, contentType, reader, extraHeaders)
    })
    router.Run(":8080")
}
```





## 8. cookie&session

### 8.1 cookie

> Cookie
>
> SetCookie

```go
import (
    "fmt"

    "github.com/gin-gonic/gin"
)

func main() {

    router := gin.Default()

    router.GET("/cookie", func(c *gin.Context) {
		
		// 获取cookie
        cookie, err := c.Cookie("gin_cookie")

        if err != nil {
            cookie = "NotSet"
            // 设置cookie
            c.SetCookie("gin_cookie", "test", 3600, "/", "localhost", false, true)
        }

        fmt.Printf("Cookie value: %s \n", cookie)
    })

    router.Run()
}
```

### 8.2 session

```
//  gorilla/sessions为自定义session后端提供cookie和文件系统session以及基础结构
//  在Gin框架中，我们可以依赖gin-contrib/sessions中间件处理session。

gin-contrib/sessions中间件支持的存储引擎：
    cookie
    memstore
    redis
    memcached
    mongodb

go get github.com/gin-contrib/sessions

e.g.1:  基本的session用法
package main

import (
        // 导入session包
	"github.com/gin-contrib/sessions"
       // 导入session存储引擎
	"github.com/gin-contrib/sessions/cookie"
        // 导入gin框架包
	"github.com/gin-gonic/gin"
)

func main() {
	r := gin.Default()
     // 创建基于cookie的存储引擎，secret11111 参数是用于加密的密钥
	store := cookie.NewStore([]byte("secret11111"))
        // 设置session中间件，参数mysession，指的是session的名字，也是cookie的名字
       // store是前面创建的存储引擎，我们可以替换成其他存储引擎
	r.Use(sessions.Sessions("mysession", store))

	r.GET("/hello", func(c *gin.Context) {
                // 初始化session对象
		session := sessions.Default(c)
                
                // 通过session.Get读取session值
                // session是键值对格式数据，因此需要通过key查询数据
		if session.Get("hello") != "world" {
            // 设置session数据
			session.Set("hello", "world")
            // 删除session数据
            session.Delete("tizi365")
            // 保存session数据
			session.Save()
            // 删除整个session
           // session.Clear()
		}
                
		c.JSON(200, gin.H{"hello": session.Get("hello")})
	})
	r.Run(":8000")
}


e.g.2: 基于redis存储引擎的session
如果我们想将session数据保存到redis中，只要将session的存储引擎改成redis即可。
go get github.com/gin-contrib/sessions/redis

package main

import (
	"github.com/gin-contrib/sessions"
	"github.com/gin-contrib/sessions/redis"
	"github.com/gin-gonic/gin"
)

func main() {
	r := gin.Default()
	// 初始化基于redis的存储引擎
	// 参数说明：
	//    第1个参数 - redis最大的空闲连接数
	//    第2个参数 - 数通信协议tcp或者udp
	//    第3个参数 - redis地址, 格式，host:port
	//    第4个参数 - redis密码
	//    第5个参数 - session加密密钥
	store, _ := redis.NewStore(10, "tcp", "localhost:6379", "", []byte("secret"))
	r.Use(sessions.Sessions("mysession", store))

	r.GET("/incr", func(c *gin.Context) {
		session := sessions.Default(c)
		var count int
		v := session.Get("count")
		if v == nil {
			count = 0
		} else {
			count = v.(int)
			count++
		}
		session.Set("count", count)
		session.Save()
		c.JSON(200, gin.H{"count": count})
	})
	r.Run(":8000")
}


```





## 9. 中间件(重点)

### 9.1 简介

在Gin框架中，**中间件**（Middleware）指的是可以拦截**http请求-响应**生命周期的特殊函数，在请求-响应生命周期中可以注册多个中间件，每个中间件执行不同的功能，一个中间执行完再轮到下一个中间件执行。

**中间件的常见应用场景如下：**

- 请求限速
- api接口签名处理
- 权限校验
- 统一错误处理

> 如果你想拦截所有请求做一些事情都可以开发一个中间件函数去实现。
>
> Gin支持设置全局中间件和针对路由分组设置中间件，设置全局中间件意思就是会拦截所有请求，针对分组路由设置中间件，意思就是仅对这个分组下的路由起作用。



### 9.2 无中间件启动

使用

```
r := gin.New()
```

代替

```
// 默认启动方式，包含 Logger、Recovery 中间件
r := gin.Default()
```



### 9.3 自定义中间件

>  全局模式和局部模式
>
> next()

```go
//定义
func Logger() gin.HandlerFunc {
	return func(c *gin.Context) {
		t := time.Now()

		// 在gin上下文中定义变量
		c.Set("example", "12345")

		// 请求前
        
         // 处理请求
		c.Next()
        
		// 请求后
		latency := time.Since(t)
		log.Print(latency)

		// access the status we are sending
		status := c.Writer.Status()
		log.Println(status)
	}
}

//使用
func main() {
	r := gin.New()
    // 全局模式
	r.Use(Logger())

	r.GET("/test", func(c *gin.Context) {
		//获取gin上下文中的变量
		example := c.MustGet("example").(string)

		// 会打印: "12345"
		log.Println(example)
	})
    
    // 局部模式
     //r.GET("/ce", MiddleWare(), func(c *gin.Context) {
       // // 取值
      //  req, _ := c.Get("request")
      //  fmt.Println("request:", req)
      //  // 页面接收
      //  c.JSON(200, gin.H{"request": req})
   // })	

	// 监听运行于 0.0.0.0:8080
	r.Run(":8080")
}

```



### 9.4 BasicAuth

> 内置中间件

```go
// 模拟私有数据
var secrets = gin.H{
	"foo":    gin.H{"email": "foo@bar.com", "phone": "123433"},
	"austin": gin.H{"email": "austin@example.com", "phone": "666"},
	"lena":   gin.H{"email": "lena@guapa.com", "phone": "523443"},
}

func main() {
	r := gin.Default()

	// 使用 gin.BasicAuth 中间件，设置授权用户
	authorized := r.Group("/admin", gin.BasicAuth(gin.Accounts{
		"foo":    "bar",
		"austin": "1234",
		"lena":   "hello2"
	}))

	// 定义路由
	authorized.GET("/secrets", func(c *gin.Context) {
		// 获取提交的用户名（AuthUserKey）
		user := c.MustGet(gin.AuthUserKey).(string)
		if secret, ok := secrets[user]; ok {
			c.JSON(http.StatusOK, gin.H{"user": user, "secret": secret})
		} else {
			c.JSON(http.StatusOK, gin.H{"user": user, "secret": "NO SECRET :("})
		}
	})

	// Listen and serve on 0.0.0.0:8080
	r.Run(":8080")
}
```



### 9.5 同步异步上下文

> 在中间件或处理程序中启动新的Goroutines时，你不应该使用其中的原始上下文，你必须使用只读副本（`c.Copy()`）

```
func main() {
	r := gin.Default()
	//1. 异步
	// goroutine 中只能使用只读的上下文 c.Copy()
	r.GET("/long_async", func(c *gin.Context) {
		cCp := c.Copy()
		
		go func() {
			time.Sleep(5 * time.Second)
			log.Println("Done! in path " + cCp.Request.URL.Path)
		}()
	})
	
	//2. 同步
	// 注意可以使用原始上下文
	r.GET("/long_sync", func(c *gin.Context) {
		time.Sleep(5 * time.Second)

		
		log.Println("Done! in path " + c.Request.URL.Path)
	})

	// Listen and serve on 0.0.0.0:8080
	r.Run(":8080")
}
```





## 10. xorm





## 11. 模板





## 12. 其他

### 12.1 日志

#### 12.1.1 使用

```go
func main() {
    // 禁用控制台颜色
    gin.DisableConsoleColor()

    // 创建记录日志的文件
    f, _ := os.Create("gin.log")
    gin.DefaultWriter = io.MultiWriter(f)

    // 如果需要将日志同时写入文件和控制台，请使用以下代码
    // gin.DefaultWriter = io.MultiWriter(f, os.Stdout)

    router := gin.Default()
    router.GET("/ping", func(c *gin.Context) {
        c.String(200, "pong")
    })

    router.Run(":8080")
}
```



#### 12.1.2  自定义日志

```go
func main() {
    router := gin.New()

    // LoggerWithFormatter 中间件会将日志写入 gin.DefaultWriter
    // By default gin.DefaultWriter = os.Stdout
    router.Use(gin.LoggerWithFormatter(func(param gin.LogFormatterParams) string {

        // 你的自定义格式
        return fmt.Sprintf("%s - [%s] \"%s %s %s %d %s \"%s\" %s\"\n",
                param.ClientIP,
                param.TimeStamp.Format(time.RFC1123),
                param.Method,
                param.Path,
                param.Request.Proto,
                param.StatusCode,
                param.Latency,
                param.Request.UserAgent(),
                param.ErrorMessage,
        )
    }))
    router.Use(gin.Recovery())

    router.GET("/ping", func(c *gin.Context) {
        c.String(200, "pong")
    })

    router.Run(":8080")
}
```

**输出示例：**

```
::1 - [Fri, 07 Dec 2018 17:04:38 JST] "GET /ping HTTP/1.1 200 122.767µs "Mozilla/5.0 (M
```



#### 12.1.3 自定义路由日志

默认的路由日志是这样的：

```
[GIN-debug] POST   /foo                      --> main.main.func1 (3 handlers)
[GIN-debug] GET    /bar                      --> main.main.func2 (3 handlers)
[GIN-debug] GET    /status                   --> main.main.func3 (3 handlers)
```

如果你想以给定的格式记录这些信息（例如 JSON，键值对或其他格式），你可以使用`gin.DebugPrintRouteFunc`来定义格式，在下面的示例中，我们使用标准日志包记录路由日志，你可以使用其他适合你需求的日志工具

```go
import (
    "log"
    "net/http"

    "github.com/gin-gonic/gin"
)

func main() {
    r := gin.Default()
    gin.DebugPrintRouteFunc = func(httpMethod, absolutePath, handlerName string, nuHandlers int) {
        log.Printf("endpoint %v %v %v %v\n", httpMethod, absolutePath, handlerName, nuHandlers)
    }

    r.POST("/foo", func(c *gin.Context) {
        c.JSON(http.StatusOK, "foo")
    })

    r.GET("/bar", func(c *gin.Context) {
        c.JSON(http.StatusOK, "bar")
    })

    r.GET("/status", func(c *gin.Context) {
        c.JSON(http.StatusOK, "ok")
    })

    // Listen and Server in http://0.0.0.0:8080
    r.Run()
}
```



### 12.2 测试

> `net/http/httptest`包是http测试的首选方式

```
package main

func setupRouter() *gin.Engine {
    r := gin.Default()
    r.GET("/ping", func(c *gin.Context) {
        c.String(200, "pong")
    })
    return r
}

func main() {
    r := setupRouter()
    r.Run(":8080")
}
```

测试上面的示例代码

```
package main

import (
    "net/http"
    "net/http/httptest"
    "testing"

    "github.com/stretchr/testify/assert"
)

func TestPingRoute(t *testing.T) {
    router := setupRouter()

    w := httptest.NewRecorder()
    req, _ := http.NewRequest("GET", "/ping", nil)
    router.ServeHTTP(w, req)

    assert.Equal(t, 200, w.Code)
    assert.Equal(t, "pong", w.Body.String())
}
```



### 12.3 自定义http配置

直接像这样使用`http.ListenAndServe()`

```
func main() {
    router := gin.Default()
    http.ListenAndServe(":8080", router)
}
```

或者

```
func main() {
    router := gin.Default()

    s := &http.Server{
        Addr:           ":8080",
        Handler:        router,
        ReadTimeout:    10 * time.Second,
        WriteTimeout:   10 * time.Second,
        MaxHeaderBytes: 1 << 20,
    }
    s.ListenAndServe()
}
```



### 12.4 支持https

example for 1-line LetsEncrypt HTTPS servers.



> autotls.Run(r, "example1.com", "example2.com")

```
package main

import (
    "log"

    "github.com/gin-gonic/autotls"
    "github.com/gin-gonic/gin"
)

func main() {
    r := gin.Default()

    // Ping handler
    r.GET("/ping", func(c *gin.Context) {
        c.String(200, "pong")
    })
	
    log.Fatal(autotls.Run(r, "example1.com", "example2.com"))
}
```

### 12.5 自定义autocert管理器

```go
package main

import (
    "log"

    "github.com/gin-gonic/autotls"
    "github.com/gin-gonic/gin"
    "golang.org/x/crypto/acme/autocert"
)

func main() {
    r := gin.Default()

    // Ping handler
    r.GET("/ping", func(c *gin.Context) {
        c.String(200, "pong")
    })

    m := autocert.Manager{
        Prompt:     autocert.AcceptTOS,
        HostPolicy: autocert.HostWhitelist("example1.com", "example2.com"),
        Cache:      autocert.DirCache("/var/www/.cache"),
    }

    log.Fatal(autotls.RunWithManager(r, &m))
}
```



### 12.6 运行多个服务

```go
package main

import (
    "log"
    "net/http"
    "time"

    "github.com/gin-gonic/gin"
    "golang.org/x/sync/errgroup"
)

var (
    g errgroup.Group
)

func router01() http.Handler {
    e := gin.New()
    e.Use(gin.Recovery())
    e.GET("/", func(c *gin.Context) {
        c.JSON(
            http.StatusOK,
            gin.H{
                "code":  http.StatusOK,
                "error": "Welcome server 01",
            },
        )
    })

    return e
}

func router02() http.Handler {
    e := gin.New()
    e.Use(gin.Recovery())
    e.GET("/", func(c *gin.Context) {
        c.JSON(
            http.StatusOK,
            gin.H{
                "code":  http.StatusOK,
                "error": "Welcome server 02",
            },
        )
    })

    return e
}

func main() {
    server01 := &http.Server{
        Addr:         ":8080",
        Handler:      router01(),
        ReadTimeout:  5 * time.Second,
        WriteTimeout: 10 * time.Second,
    }

    server02 := &http.Server{
        Addr:         ":8081",
        Handler:      router02(),
        ReadTimeout:  5 * time.Second,
        WriteTimeout: 10 * time.Second,
    }

    g.Go(func() error {
        return server01.ListenAndServe()
    })

    g.Go(func() error {
        return server02.ListenAndServe()
    })

    if err := g.Wait(); err != nil {
        log.Fatal(err)
    }
}
```



### 12.7 优雅重启或停止

想要优雅地重启或停止你的Web服务器，使用下面的方法

我们可以使用[fvbock/endless](https://github.com/fvbock/endless)来替换默认的`ListenAndServe`，有关详细信息，请参阅问题[＃296](https://github.com/gin-gonic/gin/issues/296)

```
router := gin.Default()
router.GET("/", handler)
// pass 
endless.ListenAndServe(":4242", router)
```

一个替换方案

-  [manners](https://github.com/braintree/manners)：一个Go HTTP服务器，能优雅的关闭
-  [graceful](https://github.com/tylerb/graceful)：Graceful是一个go的包，支持优雅地关闭http.Handler服务器
-  [grace](https://github.com/facebookgo/grace)：     对Go服务器进行优雅的重启和零停机部署

如果你的Go版本是1.8，你可能不需要使用这个库，考虑使用http.Server内置的[Shutdown()](https://golang.org/pkg/net/http/#Server.Shutdown)方法进行优雅关闭，查看[例子](https://github.com/gin-gonic/gin/tree/master/examples/graceful-shutdown)

```
// +build go1.8

package main

import (
    "context"
    "log"
    "net/http"
    "os"
    "os/signal"
    "time"

    "github.com/gin-gonic/gin"
)

func main() {
    router := gin.Default()
    router.GET("/", func(c *gin.Context) {
        time.Sleep(5 * time.Second)
        c.String(http.StatusOK, "Welcome Gin Server")
    })

    srv := &http.Server{
        Addr:    ":8080",
        Handler: router,
    }

    go func() {
        // service connections
        if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
            log.Fatalf("listen: %s\n", err)
        }
    }()

    // Wait for interrupt signal to gracefully shutdown the server with
    // a timeout of 5 seconds.
    quit := make(chan os.Signal)
    signal.Notify(quit, os.Interrupt)
    <-quit
    log.Println("Shutdown Server ...")

    ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
    defer cancel()
    
    
    if err := srv.Shutdown(ctx); err != nil {
        log.Fatal("Server Shutdown:", err)
    }
    log.Println("Server exiting")
}
```



### 12.8 HTTP/2 服务器推送

`http.Pusher`只支持Go 1.8或更高版本，有关详细信息，请参阅[golang博客](https://blog.golang.org/h2push)

```go
package main

import (
    "html/template"
    "log"

    "github.com/gin-gonic/gin"
)

var html = template.Must(template.New("https").Parse(`
<html>
<head>
  <title>Https Test</title>
  <script src="/assets/app.js"></script>
</head>
<body>
  <h1 style="color:red;">Welcome, Ginner!</h1>
</body>
</html>
`))

func main() {
    r := gin.Default()
    r.Static("/assets", "./assets")
    r.SetHTMLTemplate(html)

    r.GET("/", func(c *gin.Context) {
        if pusher := c.Writer.Pusher(); pusher != nil {
            // use pusher.Push() to do server push
            if err := pusher.Push("/assets/app.js", nil); err != nil {
                log.Printf("Failed to push: %v", err)
            }
        }
        c.HTML(200, "https", gin.H{
            "status": "success",
        })
    })

    // Listen and Server in https://127.0.0.1:8080
    r.RunTLS(":8080", "./testdata/server.pem", "./testdata/server.key")
}
```



### 12.9 构建含模板二进制文件(重点)

> [go-assets ](https://github.com/jessevdk/go-assets)：    将服务器构建成一个包含模板的二进制文件
>
> go-generate:  在编译前自动化生成某类代码(比如： 将 HTML 文件嵌入到 go 源码)   go generate -x

```go
func main() {
    r := gin.New()

    t, err := loadTemplate()
    if err != nil {
        panic(err)
    }
    r.SetHTMLTemplate(t)

    r.GET("/", func(c *gin.Context) {
        c.HTML(http.StatusOK, "/html/index.tmpl",nil)
    })
    r.Run(":8080")
}

// loadTemplate loads templates embedded by go-assets-builder
func loadTemplate() (*template.Template, error) {
    t := template.New("")
    for name, file := range Assets.Files {
        if file.IsDir() || !strings.HasSuffix(name, ".tmpl") {
            continue
        }
        h, err := ioutil.ReadAll(file)
        if err != nil {
            return nil, err
        }
        t, err = t.New(name).Parse(string(h))
        if err != nil {
            return nil, err
        }
    }
    return t, nil
}
```

请参见`examples/assets-in-binary`目录中的例子

