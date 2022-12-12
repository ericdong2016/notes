# beego

## 0. 升级说明



## 1. 文档

```
https://beego.me/docs          

http://www.topgoer.com/beego%E6%A1%86%E6%9E%B6/

https://studygolang.com/articles/811
```

## 2. 架构
```
//2.1 简介
作者：谢孟军，主要设计灵感来源于tornado、sinatra、flask这三个框架，但是结合了Go本身的一些特性(interface、struct继承等)而设计的一个框架

//2.2 架构   
   			beego 
   			
cache  config  context  httplibs

logs   orm     session  toolbox


//2.3 执行流程分析：
浏览器 ---> 路由 ---> 参数过滤 ---> 控制器  ---> 模型/toolbox  
       	   视图 <--- 输出过滤 <---	   
```

## 3. 安装

```
// 安装beego, bee, 默认已经安装了go sdk
go get -v -u github.com/astaxie/beego
go get -v -u github.com/beego/bee

//配置环境变量（bee 默认在 gopath/bin, 所以需要将gopath/bin 添加到环境变量）
    # linux: 编辑.bashrc
    
        vim .bashrc
        //在最后一行插入
        export PATH="$GOPATH/bin:$PATH"
        //然后保存退出
        source .bashrc
        
    # windows: 本地电脑---环境变量
    
    
// 创建项目，运行项目
bee new xxx   // 创建项目   e.g.:  D:\mycode\go\src\step3\D02_beego\bee new beegoTest    
bee run       // 运行项目，支持热更新

其他命令：
    Usage:
    	bee command [arguments]
    
        The commands are:
            version     show the bee & beego version
            new         create an application base on beego framework
            run         run the app which can hot compile at local development
            pack        compress an beego project
            
    
            dockerize   Generates a Dockerfile for your Beego application(这个命令可以通过生成Dockerfile文件来实现docker化你的应用, e.g.: bee dockerize -image="library/golang:1.6.4" -expose=9000)
            generate    Source code generator(自动化的生成代码的，包含了从数据库一键生成 model，还包含了 scaffold 的)
            migrate     run database migrations(这个命令是应用的数据库迁移命令，主要是用来每次应用升级，降级的SQL管理)
            
            hprose      Creates an RPC application based on Hprose and Beego frameworks
            fix         Fixes your application by complating newer versions
            api         create an api application base on beego framework
            bale        packs non-Go files to Go source files  
            dlv         Start a debugging session using Delve
            rs          Run customized scripts
            server      serving static content over HTTP on port

        Use bee help [command] for more information about a command.
    
注意：
    通过bee 创建的项目代码都是在 $GOPATH/src 目录下面的


Q: 新建项目, 发现新建到了user/H/go/src/...  如何更改新建的项目目录?
A: 更改系统环境变量中的 gopath( gopath: d:/mycode/go) 及 pycharm 的gopath （global gopath）


Q: git https 无法获取，请配置本地的 git，关闭 https 验证
A: git config --global http.sslVerify false

```

## 4. 配置文件
> 疑问：何时加载   分析 beego.run() 源码即可知晓



### 4.1 基本配置

```
conf/app.conf

// 默认配置
appname = beegotest
httpaddr = "127.0.0.1"
httpport = 9090
runmode ="dev"

// 数据库
mysqluser = "root"
mysqlpass = "rootpass"
mysqlurls = "127.0.0.1"
mysqldb   = "beego"
```

app配置

![](imgs\1-app配置.png)

![](imgs\2-app配置.png)



web配置

![](imgs\3-web配置.png)

![](imgs\4-web配置.png)

![](imgs\5-web配置.png)



监听配置

![](imgs\6-监听配置.png)

![](imgs\7-监听配置.png)

![](imgs\8-监听配置.png)



session配置

![](imgs\9-session配置.png)



log配置

![](imgs\10-log配置.png)



### 4.2 获取配置文件中的信息

```
// 获取配置文件中的信息
beego.AppConfig.String("mysqluser")
beego.AppConfig.String("mysqlpass")
beego.AppConfig.String("mysqlurls")
beego.AppConfig.String("mysqldb")

AppConfig中的方法：
	Set(key, val string) error
    String(key string) string
    Strings(key string) []string
    Int(key string) (int, error)
    Int64(key string) (int64, error)
    Bool(key string) (bool, error)
    Float(key string) (float64, error)
    DefaultString(key string, defaultVal string) string
    DefaultStrings(key string, defaultVal []string)
    DefaultInt(key string, defaultVal int) int
    DefaultInt64(key string, defaultVal int64) int64
    DefaultBool(key string, defaultVal bool) bool
    DefaultFloat(key string, defaultVal float64) float64
    DIY(key string) (interface{}, error)
    GetSection(section string) (map[string]string, error)
    SaveConfigFile(filename string) error
```



### 4.3 不同环境配置

> 解析的时候优先解析 runmode (dev, prod, test)下的配置，然后解析默认的配置

```
// 在配置文件里面支持 section，可以有不同的 Runmode 的配置，默认优先读取 runmode 下的配置信息，例如下面的配置文件：
// app.conf
appname = beepkg
httpaddr = "127.0.0.1"
httpport = 9090
runmode ="dev"
autorender = false
recoverpanic = false
viewspath = "myview"

[dev]
httpport = 8080
[prod]
httpport = 8088
[test]
httpport = 8888
```



### 4.4 多个配置文件

```
INI 格式配置支持 include 方式，引用多个配置文件，例如下面的两个配置文件效果同上：

// app.conf

appname = beepkg
httpaddr = "127.0.0.1"
httpport = 9090

include "app2.conf"


// app2.conf
runmode ="dev"
autorender = false
recoverpanic = false
viewspath = "myview"

[dev]
httpport = 8080
[prod]
httpport = 8088
[test]
httpport = 8888
```



### 4.5 环境变量配置

```
// 配置文件解析支持从环境变量中获取配置项，配置项格式： ${ 环境变量 } 
// 例如: 下面的配置中优先使用环境变量中配置的 runmode 和 httpport，如果有配置环境变量 ProRunMode 则优先使用该环境变量值。如果不存在或者为空，则使用 “dev” 作为 runmode, httpport同理

app.conf
runmode  = "${ ProRunMode || dev }"
httpport = "${ ProPort || 9090 }"

```



## 5. 路由

> get, post 后面的方法 要 大写
>
> 冒号，分号等不能有空格



### 5.1 基础路由

```
最简单的 beego 路由由 URI 和闭包函数组成

//基本 GET 路由
beego.Get("/",func(ctx *context.Context){
     ctx.Output.Body([]byte("hello world"))
})

//基本 POST 路由
beego.Post("/alice",func(ctx *context.Context){
     ctx.Output.Body([]byte("bob"))
})

//注册一个可以响应任何 HTTP 的路由
beego.Any("/foo",func(ctx *context.Context){
     ctx.Output.Body([]byte("bar"))
})

//所有的支持的基础函数如下所示
beego.Get(router, beego.FilterFunc)
beego.Post(router, beego.FilterFunc)
beego.Put(router, beego.FilterFunc)
beego.Patch(router, beego.FilterFunc)
beego.Head(router, beego.FilterFunc)
beego.Options(router, beego.FilterFunc)
beego.Delete(router, beego.FilterFunc)
beego.Any(router, beego.FilterFunc)


// 支持自定义的 handler 实现    todo
有些时候我们已经实现了一些 rpc 的应用,但是想要集成到 beego 中,或者其他的 httpserver 应用,集成到 beego 中来.现在可以很方便的集成:
    s := rpc.NewServer()
    s.RegisterCodec(json.NewCodec(), "application/json")
    s.RegisterService(new(HelloService), "")    // helloservice是啥？ rpc里面的service?
    beego.Handler("/rpc", s)
    
    
	beego.Handler(router, http.Handler) 这个函数是关键,第一个参数表示路由 URI, 第二个就是你自己实现的 http.Handler, 注册之后就会把所有 rpc 作为前缀的请求分发到 http.Handler 中进行处理.这个函数其实还有第三个参数就是是否是前缀匹配,默认是 false, 如果设置了 true, 那么就会在路由匹配的时候前缀匹配,即 /rpc/user 这样的也会匹配去运行
```



### 5.2 固定路由

```
固定路由也就是全匹配的路由，如下所示：

beego.Router("/", &controllers.MainController{})
beego.Router("/admin", &admin.UserController{})
beego.Router("/admin/index", &admin.ArticleController{})
beego.Router("/admin/addpkg", &admin.AddController{})

如上所示的路由就是我们最常用的路由方式，一个固定的路由，一个控制器，然后根据用户请求方法不同请求控制器中对应的方法，典型的 RESTful 方式。
```



### 5.3 正则路由

```
为了用户更加方便的路由设置，beego 参考了 sinatra 的路由实现，支持多种方式的路由：

// beego.Router(“/api/?:id”, &controllers.RController{})
默认匹配 //例如对于URL”/api/123”可以匹配成功，此时变量”:id”值为”123”

// beego.Router(“/api/:id”, &controllers.RController{})
默认匹配 //例如对于”/api/123”可以匹配成功，此时变量”:id”值为”123”，但”/api/“匹配失败

// beego.Router(“/api/:id([0-9]+)“, &controllers.RController{})
自定义正则匹配 //例如对于”/api/123”可以匹配成功，此时变量”:id”值为”123”

// beego.Router(“/user/:username([\\w]+)“, &controllers.RController{})
正则字符串匹配 //例如对于”/user/astaxie”可以匹配成功，此时变量”:username”值为”astaxie”

// beego.Router(“/download/*.*”, &controllers.RController{})
*匹配方式 //例如对于URL”/download/file/api.xml”可以匹配成功，此时变量”:path”值为”file/api”， “:ext”值为”xml”

// beego.Router(“/download/ceshi/*“, &controllers.RController{})
*全匹配方式 //例如对于URL”/download/ceshi/file/api.json”可以匹配成功，此时变量”:splat”值为”file/api.json”

// beego.Router(“/:id:int”, &controllers.RController{})
int 类型设置方式，匹配 :id为int 类型，框架帮你实现了正则 ([0-9]+)

// beego.Router(“/:hi:string”, &controllers.RController{})
string 类型设置方式，匹配 :hi 为 string 类型。框架帮你实现了正则 ([\w]+)

// beego.Router(“/cms_:id([0-9]+).html”, &controllers.CmsController{})
带有前缀的自定义正则匹配 :id 为正则类型。匹配 cms_123.html 这样的 url , :id = 123



可以在 Controller 中通过如下方式获取上面的变量：
    this.Ctx.Input.Param(":id")
    this.Ctx.Input.Param(":username")
    this.Ctx.Input.Param(":splat")
    this.Ctx.Input.Param(":path")
    this.Ctx.Input.Param(":ext")
```



### 5.4 自定义方法

> 分号，逗号，冒号 后面不要空格，切记

```
上面列举的是默认的请求方法名（请求的 method 和函数名一致，例如 GET 请求执行 Get 函数，POST 请求执行 Post 函数），如果用户期望自定义函数名，那么可以使用如下方式：

	beego.Router("/",&IndexController{},"*:Index")
	使用第三个参数，第三个参数就是用来设置对应 method 到函数名，定义如下

    * 表示任意的 method 都执行该函数，使用 httpmethod:funcname 格式来展示
    多个不同的格式使用 ; 分割
    多个 method 对应同一个 funcname，method 之间通过 ,  来分割
    
以下是一个 RESTful 的设计示例：
    beego.Router("/api/list", &RestController{}, "*:ListFood")
    beego.Router("/api/create", &RestController{}, "post:CreateFood")

以下是多个 HTTP Method 指向同一个函数，通过 , 进行分割的示例：
	beego.Router("/api", &RestController{}, "get,post:ApiFunc")
	
以下是不同的 method 对应不同的函数，通过 ; 进行分割的示例：
	beego.Router("/simple", &SimpleController{}, "get:GetFunc;post:PostFunc")
	

可用的 HTTP Method：
    *: 包含以下所有的函数
    get: GET 请求
    post: POST 请求
    put: PUT 请求
    delete: DELETE 请求
    patch: PATCH 请求
    options: OPTIONS 请求
    head: HEAD 请求
    
如果同时存在 * 和对应的 HTTP Method，那么优先执行 HTTP Method 的方法，例如同时注册了如下所示的路由：
	beego.Router("/simple",&SimpleController{},"*:AllFunc;post:PostFunc")
	
那么执行 POST 请求的时候，执行 PostFunc 而不执行 AllFunc。
```



### 5.5 自动路由

> 不够直观





### 5.6 注解路由

> 不够直观

```
// CMS API
type CMSController struct {
    beego.Controller
}

func (c *CMSController) URLMapping() {
    c.Mapping("StaticBlock", c.StaticBlock)
    c.Mapping("AllBlock", c.AllBlock)
}


// @router /staticblock/:key [get]
func (this *CMSController) StaticBlock() {

}

// @router /all/:key [get]
func (this *CMSController) AllBlock() {

}


// 可以在 router.go 中通过如下方式注册路由：
beego.Include(&CMSController{})

beego自动会进行源码分析，注意只会在 dev 模式下进行生成，生成的路由放在 “/routers/commentsRouter.go” 文件中。这样上面的路由就支持了如下的路由：
    GET /staticblock/:key
    GET /all/:key
```



### 5.7 namespace

```
ns :=
    beego.NewNamespace("/api",
        //此处正式版时改为验证加密请求
        beego.NSCond(func(ctx *context.Context) bool {
            if ua := ctx.Input.Request.UserAgent(); ua != "" {
                return true
            }
            return false
        }),
        beego.NSNamespace("/ios",
            //CRUD Create(创建)、Read(读取)、Update(更新)和Delete(删除)
            beego.NSNamespace("/create",
                // /api/ios/create/node/
                beego.NSRouter("/node", &apis.CreateNodeHandler{}),
                // /api/ios/create/topic/
                beego.NSRouter("/topic", &apis.CreateTopicHandler{}),
            ),
            beego.NSNamespace("/read",
                beego.NSRouter("/node", &apis.ReadNodeHandler{}),
                beego.NSRouter("/topic", &apis.ReadTopicHandler{}),
            ),
            beego.NSNamespace("/update",
                beego.NSRouter("/node", &apis.UpdateNodeHandler{}),
                beego.NSRouter("/topic", &apis.UpdateTopicHandler{}),
            ),
            beego.NSNamespace("/delete",
                beego.NSRouter("/node", &apis.DeleteNodeHandler{}),
                beego.NSRouter("/topic", &apis.DeleteTopicHandler{}),
            )
        ),
    )

beego.AddNamespace(ns)
```



### 5.8 路由过滤器

>  AddFilter 从beego1.3 版本开始已经废除
>
> beego 支持自定义过滤中间件，例如安全验证，强制跳转等。



**过滤函数：**

```
beego.InsertFilter(pattern string, position int, filter FilterFunc, params ...bool)
```

InsertFilter 函数的三个必填参数，一个可选参数

- pattern 路由规则，可以根据一定的规则进行路由，如果你全匹配可以用 `*`
- position 执行 Filter 的地方，五个固定参数如下，分别表示不同的执行过程
  - BeforeStatic 静态地址之前
  - BeforeRouter 寻找路由之前
  - BeforeExec 找到路由之后，开始执行相应的 Controller 之前
  - AfterExec 执行完 Controller 逻辑之后执行的过滤器
  - FinishRouter 执行完逻辑之后执行的过滤器
- filter filter 函数 type FilterFunc func(*context.Context)
- params
  1. 设置 returnOnOutput 的值(默认 true), 如果在进行到此过滤之前已经有输出，是否不再继续执行此过滤器,默认设置为如果前面已有输出(参数为true)，则不再执行此过滤器
  2. 是否重置 filters 的参数，默认是 false，因为在 filters 的 pattern 和本身的路由的 pattern 冲突的时候，可以把 filters 的参数重置，这样可以保证在后续的逻辑中获取到正确的参数，例如设置了 `/api/*` 的 filter，同时又设置了 `/api/docs/*` 的 router，那么在访问 `/api/docs/swagger/abc.js` 的时候，在执行 filters 的时候设置 `:splat` 参数为 `docs/swagger/abc.js`，但是如果不清楚 filter 的这个路由参数，就会在执行路由逻辑的时候保持 `docs/swagger/abc.js`，如果设置了 true，就会重置 `:splat` 参数.



e.g.:   验证用户是否已经登录，应用于全部的请求：

> 这里需要特别注意使用 session 的 Filter 必须在 BeforeStatic 之后才能获取，因为 session 没有在这之前初始化。

```
var FilterUser = func(ctx *context.Context) {
    _, ok := ctx.Input.Session("uid").(int)
    if !ok && ctx.Request.RequestURI != "/login" {
        ctx.Redirect(302, "/login")
    }
}

beego.InsertFilter("/*",beego.BeforeRouter, FilterUser)
```

**正则路由过滤**

```
var FilterUser = func(ctx *context.Context) {
    _, ok := ctx.Input.Session("uid").(int)
    if !ok {
        ctx.Redirect(302, "/login")
    }
}
beego.InsertFilter("/user/:id([0-9]+)",beego.BeforeRouter,FilterUser)
```



**过滤器实现路由**

beego1.1.2 开始 Context.Input 中增加了 RunController 和 RunMethod, 这样我们就可以在执行路由查找之前,在 filter 中实现自己的路由规则.

示例： 

```
var UrlManager = func(ctx *context.Context) {
    // 数据库读取全部的 url mapping 数据
    urlMapping := model.GetUrlMapping()
    for baseurl,rule:=range urlMapping {
        if baseurl == ctx.Request.RequestURI {
            ctx.Input.RunController = rule.controller
            ctx.Input.RunMethod = rule.method
            break
        }
    }
}

beego.InsertFilter("/*", beego.BeforeRouter, UrlManager)
```



  

### 5.9 UrlFor

```
UrlFor() 函数就是用于构建指定函数的 URL 的。它把对应控制器和函数名结合的字符串作为第一个参数，其余参数对应 URL 中的变量。未知变量将添加到 URL 中作为查询参数。

下面是我们注册的路由：
beego.Router("/api/list", &TestController{}, "*:List")
beego.Router("/person/:last/:first", &TestController{})
beego.AutoRouter(&TestController{})


那么通过方式可以获取相应的URL地址：
// 输出 /api/list
beego.URLFor("TestController.List")

// 输出 /person/xie/asta
beego.URLFor("TestController.Get", ":last", "xie", ":first", "asta")

// 输出 /Test/Myext
beego.URLFor("TestController.Myext")

// 输出 /Test/GetUrl
beego.URLFor("TestController.GetUrl")



模板中如何使用
默认情况下，beego 已经注册了 urlfor 函数，用户可以通过如下的代码进行调用
	{{urlfor "TestController.List"}}
为什么不在把 URL 写死在模板中，反而要动态构建？有两个很好的理由：
	1.反向解析通常比硬编码 URL 更直观。同时，更重要的是你可以只在一个地方改变 URL ，而不用到处乱找。
	2.URL 创建会为你处理特殊字符的转义和 Unicode 数据，不用你操心。
```



### 5.10 总结

```
// beego运行过程分析：
1.解析配置文件
    beego 会自动解析在 conf 目录下面的配置文件 app.conf，通过修改配置文件相关的属性，我们可以定义：开启的端口，是否开启 session，应用名称等信息。
    
2. 执行用户的 hookfunc
	beego 会执行用户注册的 hookfunc，默认的已经存在了注册 mime，用户可以通过函数 AddAPPStartHook 注册自己的启动函数。
3.是否开启 session
	会根据上面配置文件的分析之后判断是否开启 session，如果开启的话就初始化全局的 session。
4.是否编译模板
	beego 会在启动的时候根据配置把 views 目录下的所有模板进行预编译，然后存在 map 里面，这样可以有效的提高模板运行的效率，无需进行多次编译。
5.是否开启文档功能
	根据 EnableDocs 配置判断是否开启内置的文档路由功能
6. 是否启动管理模块
	beego 目前做了一个很酷的模块，应用内监控模块，会在 8088 端口做一个内部监听，我们可以通过这个端口查询到 QPS、CPU、内存、GC、goroutine、thread 等统计信息

7. 监听服务端口
	这是最后一步也就是我们看到的访问 8080 看到的网页端口，内部其实调用了 ListenAndServe，充分利用了 goroutine 的优势

一旦 run 起来之后，我们的服务就监听在两个端口了，一个服务端口 8080 作为对外服务，另一个 8088 端口实行对内监控


//1. 基本路由


//2. 高级路由
beego.Router("/api",&controllers.MainController{},"Get:Getfunc")

beego.Router("/api",&controllers.MainController{},"Get,Post:Getfunc")

beego.Router("/api",&controllers.MainController{},"Get:Getfunc; Post:Postfunc")

beego.Router("/api",&controllers.MainController{},"*:Getfunc")

beego.Router("/api",&controllers.MainController{},"*:Getfunc; Post:Postfunc")  //优先访问后面的


//3.正则匹配
beego.Router("/api/?:id", &controllers.MainController{}, "Get:Getfunc")

beego.Router("/api/:id[0-9]", &controllers.MainController{}, "Get:Getfunc")


//正则传递的参数获取
id := c.GetString(":id")

//beego日志
beego.Info()


// 访问文件用
beego.Router("/api/*.*",  &controllers.MainController{}, "Get:Getfunc")
// this.GetString(":path")
// this.GetString(":ext")


// 单个*
// this.GetString(":splat")
```







## 6. 控制器

### 6.1 ControllerInterface

`beego.Controller` 实现了接口 `beego.ControllerInterface`，`beego.ControllerInterface` 定义了如下函数：

- Init(ct *context.Context, childName string, app interface{})

    这个函数主要初始化了 Context、相应的 Controller 名称，模板名，初始化模板参数的容器 Data，app 即为当前执行的 Controller 的 reflecttype，这个 app 可以用来执行子类的方法。

- Prepare()

    这个函数主要是为了用户扩展用的，这个函数会在下面定义的这些 Method 方法之前执行，用户可以重写这个函数实现类似用户验证之类。

- Get()

    如果用户请求的 HTTP Method 是 GET，那么就执行该函数，默认是 405，用户继承的子 struct 中可以实现了该方法以处理 Get 请求。

- Post()

    如果用户请求的 HTTP Method 是 POST，那么就执行该函数，默认是 405，用户继承的子 struct 中可以实现了该方法以处理 Post 请求。

- Delete()

    如果用户请求的 HTTP Method 是 DELETE，那么就执行该函数，默认是 405，用户继承的子 struct 中可以实现了该方法以处理 Delete 请求。

- Put()

    如果用户请求的 HTTP Method 是 PUT，那么就执行该函数，默认是 405，用户继承的子 struct 中可以实现了该方法以处理 Put 请求.

- Head()

    如果用户请求的 HTTP Method 是 HEAD，那么就执行该函数，默认是 405，用户继承的子 struct 中可以实现了该方法以处理 Head 请求。

- Patch()

    如果用户请求的 HTTP Method 是 PATCH，那么就执行该函数，默认是 405，用户继承的子 struct 中可以实现了该方法以处理 Patch 请求.

- Options()

    如果用户请求的HTTP Method是OPTIONS，那么就执行该函数，默认是 405，用户继承的子 struct 中可以实现了该方法以处理 Options 请求。

- Finish()

    这个函数是在执行完相应的 HTTP Method 方法之后执行的，默认是空，用户可以在子 struct 中重写这个函数，执行例如数据库关闭，清理数据之类的工作。

- Render() error

    这个函数主要用来实现渲染模板，如果 beego.AutoRender 为 true 的情况下才会执行。



#### 6.1.1 示例

下面我们再来看一种比较流行的架构，首先实现一个自己的基类 baseController，实现一些初始化的方法，然后其他所有的逻辑继承自该基类：

```
type NestPreparer interface {
        NestPrepare()
}

// baseRouter implemented global settings for all other routers.
type baseController struct {
        beego.Controller
        i18n.Locale
        user    models.User
        isLogin bool
}
// Prepare implemented Prepare method for baseRouter.
func (this *baseController) Prepare() {

        // page start time
        this.Data["PageStartTime"] = time.Now()

        // Setting properties.
        this.Data["AppDescription"] = utils.AppDescription
        this.Data["AppKeywords"] = utils.AppKeywords
        this.Data["AppName"] = utils.AppName
        this.Data["AppVer"] = utils.AppVer
        this.Data["AppUrl"] = utils.AppUrl
        this.Data["AppLogo"] = utils.AppLogo
        this.Data["AvatarURL"] = utils.AvatarURL
        this.Data["IsProMode"] = utils.IsProMode

        if app, ok := this.AppController.(NestPreparer); ok {
                app.NestPrepare()
        }
}
```

上面定义了基类，大概是初始化了一些变量，最后有一个 Init 函数中那个 app 的应用，判断当前运行的 Controller 是否是 NestPreparer 实现，如果是的话调用子类的方法，下面我们来看一下 NestPreparer 的实现：

```
type BaseAdminRouter struct {
    baseController
}

func (this *BaseAdminRouter) NestPrepare() {
    if this.CheckActiveRedirect() {
            return
    }

    // if user isn't admin, then logout user
    if !this.user.IsAdmin {
            models.LogoutUser(&this.Controller)

            // write flash message
            this.FlashWrite("NotPermit", "true")

            this.Redirect("/login", 302)
            return
    }

    // current in admin page
    this.Data["IsAdmin"] = true

    if app, ok := this.AppController.(ModelPreparer); ok {
            app.ModelPrepare()
            return
    }
}

func (this *BaseAdminRouter) Get(){
    this.TplName = "Get.tpl"
}

func (this *BaseAdminRouter) Post(){
    this.TplName = "Post.tpl"
}
```

这样我们的执行器执行的逻辑是这样的，首先执行 Prepare，这个就是 Go 语言中 struct 中寻找方法的顺序，依次往父类寻找。执行 `BaseAdminRouter` 时，查找他是否有 `Prepare` 方法，没有就寻找 `baseController`，找到了，那么就执行逻辑，然后在 `baseController` 里面的 `this.AppController` 即为当前执行的控制器 `BaseAdminRouter`，因为会执行 `BaseAdminRouter.NestPrepare` 方法。然后开始执行相应的 Get 方法或者 Post 方法。



#### 6.1.2 提前终止运行

```
我们应用中经常会遇到这样的情况，在 Prepare 阶段进行判断，如果用户认证不通过，就输出一段信息，然后直接中止进程，之后的 Post、Get 之类的不再执行，那么如何终止呢？可以使用 StopRun 来终止执行逻辑，可以在任意的地方执行。

调用 StopRun 之后，如果你还定义了 Finish 函数就不会再执行，如果需要释放资源，那么请自己在调用 StopRun 之前手工调用 Finish 函数。

type RController struct {
    beego.Controller
}

func (this *RController) Prepare() {
    this.Data["json"] = map[string]interface{}{"name": "astaxie"}
    this.ServeJSON()
    //this.finish()
    this.StopRun()
}
```



## 7. 请求

### 7.1 获取参数

我们经常需要获取用户传递的数据，包括 Get、POST 等方式的请求，beego 里面会自动解析这些数据：

- GetString(key string) string
- GetStrings(key string) []string
- GetInt(key string) (int64, error)
- GetBool(key string) (bool, error)
- GetFloat(key string) (float64, error)

```
func (this *MainController) Post() {
    jsoninfo := this.GetString("jsoninfo")
    if jsoninfo == "" {
        this.Ctx.WriteString("jsoninfo is empty")
        return
    }
}
```

如果你需要的数据可能是其他类型的，例如是 int 类型而不是 int64，那么你需要这样处理：

```
func (this *MainController) Post() {
    id := this.Input().Get("id")
    intid, err := strconv.Atoi(id)
}
```







###   7.2 获取 Request Body 

在 API 的开发中，我们经常会用到 `JSON` 或 `XML` 来作为数据交互的格式，如何在 beego 中获取 Request Body 里的 JSON 或 XML 的数据呢？

1. 在配置文件里设置 `copyrequestbody = true`
2. 在 Controller 中

```
func (this *ObjectController) Post() {
    var ob models.xxx
    var err error
    if err = json.Unmarshal(this.Ctx.Input.RequestBody, &ob); err == nil {
        objectid := models.AddOne(ob)
        this.Data["json"] = "{\"ObjectId\":\"" + objectid + "\"}"
    } else {
        this.Data["json"] = err.Error()
    }
    this.ServeJSON()
}
```



###   7.3 文件上传

在 beego 中你可以很容易的处理文件上传，就是别忘记在你的 form 表单中增加这个属性 `enctype="multipart/form-data"`，否则你的浏览器不会传输你的上传文件。

文件上传之后一般是放在系统的内存里面，如果文件的 size 大于设置的缓存内存大小，那么就放在临时文件中，默认的缓存内存是 64M，你可以通过如下来调整这个缓存内存大小:

```
beego.MaxMemory = 1<<22
```

或者在配置文件中通过如下设置：

```
maxmemory = 1<<22
```



Beego 提供了两个很方便的方法来处理文件上传：

- GetFile(key string) (multipart.File, *multipart.FileHeader, error)

    该方法主要用于用户读取表单中的文件名 `the_file`，然后返回相应的信息，用户根据这些变量来处理文件上传：过滤、保存文件等。

- SaveToFile(fromfile, tofile string) error

    该方法是在 GetFile 的基础上实现了快速保存的功能
    fromfile 是提交时候的 html 表单中的 name

```
<form enctype="multipart/form-data" method="post">
    <input type="file" name="uploadname" />
    <input type="submit">
</form>
```

示例：

```
func (c *FormController) Post() {
    f, h, err := c.GetFile("uploadname")
    if err != nil {
        log.Fatal("getfile err ", err)
    }
    defer f.Close()
    c.SaveToFile("uploadname", "static/upload/" + h.Filename) // 保存位置在 static/upload, 没有文件夹要先创建
}
```

### 7.4 解析表单数据到struct(了解)

如果要把表单里的内容赋值到一个 struct 里，除了用上面的方法一个一个获取再赋值外，beego 提供了通过另外一个更便捷的方式，就是通过 struct 的字段名或 tag 与表单字段对应直接解析到 struct。

定义 struct：

```
type user struct {
    Id    int         `form:"-"`
    Name  interface{} `form:"username"`
    Age   int         `form:"age"`
    Email string
}
```

表单：

```
<form id="user">
    名字：<input name="username" type="text" />
    年龄：<input name="age" type="text" />
    邮箱：<input name="Email" type="text" />
    <input type="submit" value="提交" />
</form>
```

Controller 里解析：

```
func (this *MainController) Post() {
    u := user{}
    if err := this.ParseForm(&u); err != nil {
        //handle error
    }
}
```

注意：

- StructTag form 的定义和 [renderform方法](https://beego.me/docs/mvc/view/view.md#renderform-使用) 共用一个标签
- 定义 struct 时，字段名后如果有 form 这个 tag，则会以把 form 表单里的 name 和 tag 的名称一样的字段赋值给这个字段，否则就会把 form 表单里与字段名一样的表单内容赋值给这个字段。如上面例子中，会把表单中的 username 和 age 分别赋值给 user 里的 Name 和 Age 字段，而 Email 里的内容则会赋给 Email 这个字段。
- 调用 Controller ParseForm 这个方法的时候，传入的参数必须为一个 struct 的指针，否则对 struct 的赋值不会成功并返回 `xx must be a struct pointer` 的错误。
- 如果要忽略一个字段，有两种办法，一是：字段名小写开头，二是：`form` 标签的值设置为 `-`



### 7.5 数据绑定(了解)

支持从用户请求中直接数据 bind 到指定的对象,例如请求地址如下

```
?id=123&isok=true&ft=1.2&ol[0]=1&ol[1]=2&ul[]=str&ul[]=array&user.Name=astaxie
var id int
this.Ctx.Input.Bind(&id, "id")  //id ==123

var isok bool
this.Ctx.Input.Bind(&isok, "isok")  //isok ==true

var ft float64
this.Ctx.Input.Bind(&ft, "ft")  //ft ==1.2

ol := make([]int, 0, 2)
this.Ctx.Input.Bind(&ol, "ol")  //ol ==[1 2]

ul := make([]string, 0, 2)
this.Ctx.Input.Bind(&ul, "ul")  //ul ==[str array]

user struct{Name}
this.Ctx.Input.Bind(&user, "user")  //user =={Name:"astaxie"}
```



## 8. 响应

> 注意 struct 属性应该 为 exported Identifier， 首字母应该大写



### 8.1 json

```
func (this *AddController) Get() {
    mystruct := { ... }
    this.Data["json"] = &mystruct
    this.ServeJSON()
}
```

调用 ServeJSON 之后，会设置 `content-type` 为 `application/json`，然后同时把数据进行 JSON 序列化输出。



### 8.2 xml 

```
func (this *AddController) Get() {
    mystruct := { ... }
    this.Data["xml"]=&mystruct
    this.ServeXML()
}
```

调用 ServeXML 之后，会设置 `content-type` 为 `application/xml`，同时数据会进行 XML 序列化输出。



### 8.3 jsonp

```
func (this *AddController) Get() {
    mystruct := { ... }
    this.Data["jsonp"] = &mystruct
    this.ServeJSONP()
}
```

调用 ServeJSONP 之后，会设置 `content-type` 为 `application/javascript`，然后同时把数据进行 JSON 序列化，然后根据请求的 callback 参数设置 jsonp 输出。



### 8.4 redirect

```

```



### 8.5 渲染

```

```



## 9. session&cookie

### 9.1 Cookie

用来一定时间的保存用户数据，数据存储在客户端（网站的客户端就是浏览器），启用的时候能设置Cookie的有效时间，当时间截至的时候，Cookie失效.

存储: 

```go
this.Ctx.SetCookie(key,value,time)//第一个参数是Cookie的key值，第二个参数是Cookie的value值，第三个参数是设置的Cookie的有效时间。
```

取出：

```go
this.Ctx.GetCookie(key)//参数是Cookie的key值，返回值是对应的value值。当没有对应的Cookie或者Cookie已失效，返回空字符串
```

删除：

```go
this.Ctx.SetCookie(key,value,0)//第一个参数是Cookie的key值，第二个参数任意值，第三个参数把Cookie的值设置为小于0，就马上失效。
```



### 9.2 Session

#### 9.2.1 配置

从 beego1.1.3 版本开始移除了第三方依赖库,也就是如果你想使用 mysql、redis、couchbase、memcache、postgres 这些引擎,那么你首先需要安装, 命令如下： 

```
go get -u github.com/astaxie/beego/session/mysql
```

然后在你的 main 函数中引入该库, 和数据库的驱动引入是一样的:

```
import _ "github.com/astaxie/beego/session/mysql"
```



当 SessionProvider 为 file，SessionProviderConfig 是指保存文件的目录，如下所示：

```
beego.BConfig.WebConfig.Session.SessionProvider="file"
beego.BConfig.WebConfig.Session.SessionProviderConfig = "./tmp"
```

当 SessionProvider 为 mysql 时，SessionProviderConfig 是链接地址，采用 [go-sql-driver](https://github.com/go-sql-driver/mysql)，如下所示：

```
beego.BConfig.WebConfig.Session.SessionProvider = "mysql"
beego.BConfig.WebConfig.Session.SessionProviderConfig = "username:password@protocol(address)/dbname?param=value"

需要特别注意的是，在使用 mysql 存储 session 信息的时候，需要事先在 mysql 创建表，建表语句如下
    CREATE TABLE `session` (
        `session_key` char(64) NOT NULL,
        `session_data` blob,
        `session_expiry` int(11) unsigned NOT NULL,
        PRIMARY KEY (`session_key`)
    ) ENGINE=MyISAM DEFAULT CHARSET=utf8;
```

当 SessionProvider 为 redis 时，SessionProviderConfig 是 redis 的链接地址，采用了 [redigo](https://github.com/garyburd/redigo)，如下所示：

```
beego.BConfig.WebConfig.Session.SessionProvider = "redis"
beego.BConfig.WebConfig.Session.SessionProviderConfig = "127.0.0.1:6379"
```

当 SessionProvider 为 memcache 时，SessionProviderConfig 是 memcache 的链接地址，采用了 [memcache](https://github.com/beego/memcache)，如下所示：

```
beego.BConfig.WebConfig.Session.SessionProvider = "memcache"
beego.BConfig.WebConfig.Session.SessionProviderConfig = "127.0.0.1:7080"
```

当 SessionProvider 为 postgresql 时，SessionProviderConfig 是 postgres 的链接地址，采用了 [postgres](https://github.com/lib/pq)，如下所示：

```
beego.BConfig.WebConfig.Session.SessionProvider = "postgresql"
beego.BConfig.WebConfig.Session.SessionProviderConfig = "postgres://pqgotest:password@localhost/pqgotest?sslmode=verify-full"
```

当 SessionProvider 为 couchbase 时，SessionProviderConfig 是 couchbase 的链接地址，采用了 [couchbase](https://github.com/couchbaselabs/go-couchbase)，如下所示：

```
beego.BConfig.WebConfig.Session.SessionProvider = "couchbase"
beego.BConfig.WebConfig.Session.SessionProviderConfig = "http://bucketname:bucketpass@myserver:8091"
```



#### 9.2.2  使用

数据存储在服务器，Beego启用Sesssion的时候需要在配置文件中开启Session功能。在Beego使用中，一般不设置Session的时间，当浏览器关闭的时候，Session失效。

- 如果想要在项目中使用Session功能，需要先在配置文件中

```
Sessionon=true
```

- 存储Session的代码:

```go
this.SetSession(key,value)//两个参数，一个是Session的key，第二个是Session的Value
```

- 获取Session的代码：


```go
this.GetSession(key)//参数是Session的key值，返回值是Session对应的value值，类型是interface{}
```

- 删除Session的代码：


```go
this.DelSession(key)//参数是Session的key值
```



#### 9.2.3 注意点

*因为 session 内部采用了 gob 来注册存储的对象，例如 struct，所以如果你采用了非 memory 的引擎，请自己在 main.go 的 init 里面注册需要保存的这些结构体，不然会引起应用重启之后出现无法解析的错误*  



## 10. csrf

### 10.1 配置

beego 有内建的 XSRF 的防范机制，要使用此机制，你需要在应用配置文件中加上 `enablexsrf` 设定：

```
enablexsrf = true
xsrfkey = 61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o
xsrfexpire = 3600
```

或者直接在 main 入口处这样设置：

```
beego.EnableXSRF = true
beego.XSRFKEY = "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o"
beego.XSRFExpire = 3600  //过期时间，默认1小时
```



*如果开启了 XSRF，那么 beego 的 Web 应用将对所有用户设置一个 `_xsrf` 的 cookie 值（默认过期 1 小时），如果 `POST PUT DELET` 请求中没有这个 cookie 值，那么这个请求会被直接拒绝。如果你开启了这个机制，那么在所有被提交的表单中，你都需要加上一个域来提供这个值。你可以通过在模板中使用 专门的函数 `XSRFFormHTML()` 来做到这一点：*

*过期时间上面我们设置了全局的过期时间 `beego.XSRFExpire`，但是有些时候我们也可以在控制器中修改这个过期时间，专门针对某一类处理逻辑：*

```
func (this *HomeController) Get(){
    this.XSRFExpire = 7200
    this.Data["xsrfdata"]=template.HTML(this.XSRFFormHTML())
}
```




### 10.2  form中使用

在 Controller 中这样设置数据：

```
func (this *HomeController) Get(){
    this.Data["xsrfdata"]=template.HTML(this.XSRFFormHTML())
}
```

然后在模板中这样设置：

```
<form action="/new_message" method="post">
  {{ .xsrfdata }}
  <input type="text" name="message"/>
  <input type="submit" value="Post"/>
</form>
```





### 10.3 JavaScript 中使用

如果你提交的是 AJAX 的 POST 请求，你还是需要在每一个请求中通过脚本添加上 _xsrf 这个值。下面是在 AJAX 的 POST 请求，使用了 jQuery 函数来为所有请求都添加 _xsrf 值：

jQuery cookie插件：https://github.com/carhartl/jquery-cookie
		base64 插件：http://phpjs.org/functions/base64_decode/

```
jQuery.postJSON = function(url, args, callback) {
   var xsrf, xsrflist;
   xsrf = $.cookie("_xsrf");
   xsrflist = xsrf.split("|");
   args._xsrf = base64_decode(xsrflist[0]);
    $.ajax({url: url, data: $.param(args), dataType: "text", type: "POST",
        success: function(response) {
        callback(eval("(" + response + ")"));
    }});
};
```

### 10.4 扩展 jQuery

通过扩展 ajax 给每个请求加入 xsrf 的 header

需要你在 html 里保存一个 `_xsrf` 值

```
func (this *HomeController) Get(){
    this.Data["xsrf_token"] = this.XSRFToken()
}
```

放在你的 head 中

```
<head>
    <meta name="_xsrf" content="{{.xsrf_token}}" />
</head>
```

扩展 ajax 方法，将 `_xsrf` 值加入 header，扩展后支持 jquery post/get 等内部使用了 ajax 的方法

```
var ajax = $.ajax;
$.extend({
    ajax: function(url, options) {
        if (typeof url === 'object') {
            options = url;
            url = undefined;
        }
        options = options || {};
        url = options.url;
        var xsrftoken = $('meta[name=_xsrf]').attr('content');
        var headers = options.headers || {};
        var domain = document.domain.replace(/\./ig, '\\.');
        if (!/^(http:|https:).*/.test(url) || eval('/^(http:|https:)\\/\\/(.+\\.)*' + domain + '.*/').test(url)) {
            headers = $.extend(headers, {'X-Xsrftoken':xsrftoken});
        }
        options.headers = headers;
        return ajax(url, options);
    }
});
```

对于 PUT 和 DELETE 请求（以及不使用将 form 内容作为参数的 POST 请求）来说，你也可以在 HTTP 头中以 X-XSRFToken 这个参数传递 XSRF token。



*如果你需要针对每一个请求处理器定制 XSRF 行为，你可以重写 Controller 的 CheckXSRFCookie 方法。例如你需要使用一个不支持 cookie 的 API， 你可以通过将 `CheckXSRFCookie()` 函数设空来禁用 XSRF 保护机制。然而如果 你需要同时支持 cookie 和非 cookie 认证方式，那么只要当前请求是通过 cookie 进行认证的，你就应该对其使用 XSRF 保护机制，这一点至关重要。*



### 10.5 controller 中禁用csrf

XSRF 之前是全局设置的一个参数, 如果设置了那么所有的 API 请求都会进行验证,但是有些时候API 逻辑是不需要进行验证的,   因此现在支持在controller 级别设置屏蔽:

```
type AdminController struct{
    beego.Controller
}

func (a *AdminController) Prepare() {
    a.EnableXSRF = false
}
```



## 11. 错误处理

> beego 框架默认支持 401、403、404、500、503 这几种错误的处理

### 11.1 Abort

```
func (this *MainController) Get() {
    this.Abort("401")
}
```



### 11.2 ErrorHandler

```
e.g.1:
	beego 更加人性化的还有一个设计就是支持用户自定义字符串错误类型处理函数，例如下面的代码，用户注册了一个数据库出错的处理页面：

    func dbError(rw http.ResponseWriter, r *http.Request){
        t,_:= template.New("dberror.html").ParseFiles(beego.BConfig.WebConfig.ViewsPath+"/dberror.html")
        data :=make(map[string]interface{})
        data["content"] = "database is now down"
        t.Execute(rw, data)
    }

    func main() {
        beego.ErrorHandler("dbError",dbError)
        beego.Router("/", &controllers.MainController{})
        beego.Run()
    }

e.g.2:
	用户可以自定义相应的错误处理，例如下面重新定义 404 页面：

    func page_not_found(rw http.ResponseWriter, r *http.Request){
        t,_:= template.New("404.html").ParseFiles(beego.BConfig.WebConfig.ViewsPath+"/404.html")
        data :=make(map[string]interface{})
        data["content"] = "page not found"
        t.Execute(rw, data)
    }

    func main() {
        beego.ErrorHandler("404",page_not_found)
        beego.Router("/", &controllers.MainController{})
        beego.Run()
    }
```



### 11.3 ErrorController

```
从 1.4.3 版本开始，支持 Controller 方式定义 Error 错误处理函数，这样就可以充分利用系统自带的模板处理，以及 context 等方法。
// controllers/xxx.go
package controllers
import (
    "github.com/astaxie/beego"
)

type ErrorController struct {
    beego.Controller
}

func (c *ErrorController) Error404() {
    c.Data["content"] = "page not found"
    c.TplName = "404.tpl"
}

func (c *ErrorController) Error501() {
    c.Data["content"] = "server error"
    c.TplName = "501.tpl"
}


func (c *ErrorController) ErrorDb() {
    c.Data["content"] = "database is now down"
    c.TplName = "dberror.tpl"
}

//通过上面的例子我们可以看到，所有的函数都是有一定规律的，都是 Error 开头，后面的名字就是我们调用 Abort 的名字，例如 Error404 函数其实调用对应的就是 Abort("404")

//我们就只要在 beego.Run 之前采用 beego.ErrorController 注册这个错误处理函数就可以了
// main.go 
package main
import (
    _ "btest/routers"
    "btest/controllers"

    "github.com/astaxie/beego"
)

func main() {
    beego.ErrorController(&controllers.ErrorController{})
    beego.Run()
}
```



## 12. 日志

beego 的日志处理是基于 logs 模块搭建的，内置了一个变量 `BeeLogger`，默认已经是 `logs.BeeLogger` 类型，初始化了 console，也就是默认输出到 `console`



### 12.1 基本使用

```
beego.Emergency("this is emergency")
beego.Alert("this is alert")
beego.Critical("this is critical")
beego.Error("this is error")            // 
beego.Warning("this is warning")
beego.Notice("this is notice")
beego.Informational("this is informational")  // 
beego.Debug("this is debug")				  // 
```



### 12.2 设置输出

我们的程序往往期望把信息输出到 log 中，现在设置输出到文件很方便，如下所示：

```
beego.SetLogger("file", `{"filename":"logs/test.log"}`)
```

这个默认情况就会同时输出到两个地方，一个 console，一个 file，如果只想输出到文件，就需要调用删除操作：

```
beego.BeeLogger.DelLogger("console")
```



###   12.3 设置级别

日志的级别如上所示的代码这样分为八个级别：

```
LevelEmergency
LevelAlert
LevelCritical
LevelError
LevelWarning
LevelNotice
LevelInformational
LevelDebug
```

级别依次降低，默认全部打印，但是一般我们在部署环境，可以通过设置级别设置日志级别：

```
beego.SetLevel(beego.LevelInformational)
```



###   12.4 输出文件名和行号

日志默认不输出调用的文件名和文件行号,如果你期望输出调用的文件名和文件行号,可以如下设置, 开启传入参数 true, 关闭传入参数 false, 默认是关闭的. 

```
beego.SetLogFuncCall(true)
```





## 13. orm(***)

### 13.0 简介

```
1、 beego ORM 是一个强大的 Go 语言 ORM 框架。她的灵感主要来自 Django ORM 和 SQLAlchemy。
    目前该框架仍处于开发阶段，可能发生任何导致不兼容的改动。
    支持数据库驱动：
        MySQL：github.com/go-sql-driver/mysql
        PostgreSQL：github.com/lib/pq
        Sqlite3：github.com/mattn/go-sqlite3
    
2、 ORM 特性：
    支持 Go 的所有类型存储
    轻松上手，采用简单的 CRUD 风格
    自动 Join 关联表
    跨数据库兼容查询
    允许直接使用 SQL 查询／映射
    严格完整的测试保证 ORM 的稳定与健壮  
    
3. 安装 ORM：
	go get github.com/astaxie/beego/orm
  
4、 调试查询日志
在开发环境下(我们不建议您在部署产品后这样做)，您可以使用以下指令来开启查询调试模式, 开启后将会输出所有查询语句，包括执行、准备、事务等。

func main() {
    orm.Debug = true
    
// result
[ORM] - 2013-08-09 13:18:16 - [Queries/default] - [    db.Exec /     0.4ms] -   [INSERT INTO `user` (`name`) VALUES (?)] - `slene`


```



### 13.1 模型定义

#### 13.1.1 表名

默认的表名规则，使用驼峰转蛇形：

```
AuthUser -> auth_user
Auth_User -> auth__user
DB_AuthUser -> d_b__auth_user
```

除了开头的大写字母以外，遇到大写会增加 `_`，原名称中的下划线保留。



####   13.1.2 字段选项

> 多个设置间使用 `;` 分隔，设置的值如果是多个，使用 `,` 分隔。

- #### auto

    当 Field 类型为 int, int32, int64, uint, uint32, uint64 时，可以设置字段为自增健

    - 当模型定义里没有主键时，符合上述类型且名称为 `Id` 的 Field 将被视为自增健。

    鉴于 go 目前的设计，即使使用了 uint64，但你也不能存储到他的最大值。依然会作为 int64 处理。

- #### pk

    设置为主键，适用于自定义其他类型为主键

- #### size

    string 类型字段默认为 varchar(255) ， 设置 size 以后，db type 将使用 varchar(size)

    ```
    Title string `orm:"size(60)"` 
    ```

- #### null

    数据库表默认为 `NOT NULL`，设置 null 代表 `ALLOW NULL`

    ```
    Name string `orm:"null"`
    ```

- #### default
  
  为字段设置默认值，类型必须符合（目前仅用于级联删除时的默认值）
      
    ```
    type User struct {
        ...
        Status int `orm:"default(1)"`
        ...
    }
    ```

- #### digits / decimals

    设置 float32, float64 类型的浮点精度

    ```
    Money float64 `orm:"digits(12);decimals(4)"`
    ```

    总长度 12 小数点  , 后 4 位   `99999999.9999`

- #### auto_now / auto_now_add

    ```
    Created time.Time `orm:"auto_now_add;type(datetime)"`
    Updated time.Time `orm:"auto_now;type(datetime)"`
    ```

    - auto_now 每次 model 保存时都会对时间自动更新
    - auto_now_add 第一次保存时才设置时间
    - 对于批量的 update 此设置是不生效的

- #### type

    设置为 date 时，time.Time 字段的对应 db 类型使用 date

    ```
    Created time.Time `orm:"auto_now_add;type(date)"`
    ```

    设置为 datetime 时，time.Time 字段的对应 db 类型使用 datetime

    ```
    Created time.Time `orm:"auto_now_add;type(datetime)"`
    ```

- #### description

    > 该字段存在问题  参考 ：  https://www.jianshu.com/p/5610a82293a5

    为字段添加注释

    ```
    // 错误
    type User struct {
        ...
        Status int `orm:"default(1)" description:"这是状态字段"`
        ...
    }
    
    // 正确
    type User struct {
        ...
        Status int `orm:"default(1) description(这是状态字段)"`
        ...
    }
    ```

    注意:  注释中禁止包含引号

    

- #### index

    为单个字段增加索引

- #### unique

    为单个字段增加 unique 键

    ```
    Name string `orm:"unique"`
    ```

- #### column

    为字段设置 db 字段的名称

    ```
    Name string `orm:"column(user_name)"`
    ```


- #### 忽略字段

    设置 `-` 即可忽略 struct 中的字段

    ```
    type User struct {
    ...
        AnyField string `orm:"-"`
    ...
    }
    ```





#### 13.1.3 表关系

##### rel / reverse

**一对一**： 

```
type User struct {
    ...
    Profile *Profile `orm:"null;rel(one); on_delete(set_null)"`
    ...
}
```

对应的反向关系 

```
type Profile struct {
    ...
    User *User `orm:"reverse(one)"`
    ...
}
```



**一对多**:

```
type Post struct {
    ...
    User *User `orm:"rel(fk)"` // RelForeignKey relation
    ...
}
```

对应的反向关系 

```
type User struct {
    ...
    Posts []*Post `orm:"reverse(many)"` // fk 的反向关系
    ...
}
```



**多对多**：

```
type Post struct {
    ...
    Tags []*Tag `orm:"rel(m2m)"` // ManyToMany relation
    ...
}
```

对应的反向关系 

```
type Tag struct {
    ...
    Posts []*Post `orm:"reverse(many)"`
    ...
}
```



##### rel_table / rel_through

此设置针对 `orm:"rel(m2m)"` 的关系字段

```
rel_table       设置自动生成的 m2m 关系表的名称
rel_through     如果要在 m2m 关系中使用自定义的 m2m 关系表
                通过这个设置其名称，格式为 pkg.path.ModelName
                eg: app.models.PostTagRel
                PostTagRel 表需要有到 Post 和 Tag 的关系
```

当设置 rel_table 时会忽略 rel_through

设置方法：

```
orm:"rel(m2m);rel_table(the_table_name)"
orm:"rel(m2m);rel_through(pkg.path.ModelName)"
```



##### on_delete

设置对应的 rel 关系删除时，如何处理关系字段。

```
cascade        级联删除(默认值)
set_null       设置为 NULL，需要设置 null = true
set_default    设置为默认值，需要设置 default 值
do_nothing     什么也不做，忽略



type User struct {
    ...
    Profile *Profile `orm:"null;rel(one);on_delete(set_null)"`
    ...
}
type Profile struct {
    ...
    User *User `orm:"reverse(one)"`
    ...
}

// 删除 Profile 时将设置 User.Profile 的数据库字段为 NULL



e.g.:
    type User struct {
        Id int
        Name string
    }

    type Post struct {
        Id int
        Title string
        User *User `orm:"rel(fk)"`
    }
    
    假设 Post -> User 是 ManyToOne 的关系，也就是外键。

    o.Filter("Id", 1).Delete()
    这个时候即会删除 Id 为 1 的 User 也会删除其发布的 Post, 不想删除的话，需要设置 set_null

    type Post struct {
        Id int
        Title string
        User *User `orm:"rel(fk);null; on_delete(set_null)"`
    }
    那这个时候，删除 User 只会把对应的 Post.user_id 设置为 NULL
    
    当然有时候为了高性能的需要，多存点数据无所谓啊，造成批量删除才是问题。
    type Post struct {
        Id int
        Title string
        User *User `orm:"rel(fk);null;on_delete(do_nothing)"`
    }
    那么只要删除的时候，不操作 Post 就可以了。


```




### 13.2 基本操作

##### 13.2.1 初始化

```
	// models.go 
	
	func init(){
		// set default database
    orm.RegisterDataBase("default", "mysql", 		"username:password@tcp(127.0.0.1:3306)/db_name?charset=utf8", 30)

    // register model
    orm.RegisterModel(new(User))

    // create table
    orm.RunSyncdb("default", false, true)
	}

tips:
    将该部分拿到model中,  同时将orm 初始化的三行代码移动过来，在main.go 中(项目初始化的时候)import
```



##### 13.2.2 数据库设置

```
目前 ORM 支持三种数据库，以下为测试过的 driver

import (
    _ "github.com/go-sql-driver/mysql"
    _ "github.com/lib/pq"
    _ "github.com/mattn/go-sqlite3"
)


2.1 RegisterDriver
三种默认数据库类型
// For version 1.6
orm.DRMySQL
orm.DRSqlite
orm.DRPostgres

// < 1.6
orm.DR_MySQL
orm.DR_Sqlite
orm.DR_Postgres



2.2 RegisterDataBase
ORM 必须注册一个别名为 default 的数据库，作为默认使用。 ORM 使用 golang 自己的连接池

// 参数1        数据库的别名，用来在 ORM 中切换数据库使用
// 参数2        driverName
// 参数3        对应的链接字符串
orm.RegisterDataBase("default", "mysql", "root:root@/orm_test?charset=utf8")

// 参数4(可选)  设置最大空闲连接
// 参数5(可选)  设置最大数据库连接 (go >= 1.2)
maxIdle := 30
maxConn := 30
orm.RegisterDataBase("default", "mysql", "root:root@/orm_test?charset=utf8", maxIdle, maxConn)


2.3 SetMaxIdleConns
根据数据库的别名，设置数据库的最大空闲连接：
	orm.SetMaxIdleConns("default", 30)

2.4 SetMaxOpenConns
根据数据库的别名，设置数据库的最大数据库连接 (go >= 1.2)：
	orm.SetMaxOpenConns("default", 30)

2.5 时区设置
ORM 默认使用 time.Local 本地时区
    1.作用于 ORM 自动创建的时间
    2. 从数据库中取回的时间转换成 ORM 本地时间

如果需要的话，你也可以进行更改
// 设置为 UTC 时间
orm.DefaultTimeLoc = time.UTC
	ORM 在进行 RegisterDataBase 的同时，会获取数据库使用的时区，然后在 time.Time 类型存取时做相应转换，以匹配时间系统，从而保证时间不会出错。

注意:
    鉴于 Sqlite3 的设计，存取默认都为 UTC 时间
    使用 go-sql-driver 驱动时，请注意参数设置，从某一版本开始，驱动默认使用 UTC 时间，而非本地时间，所以请指定时区参数或者全部以 UTC 时间存取 例如：root:root@/orm_test?charset=utf8&loc=Asia%2FShanghai
    参见 loc / parseTime
```



##### 13.2.3 注册模型

```
如果使用 orm.QuerySeter 进行高级查询的话，这个是必须的。反之，如果只使用 Raw 查询和 map struct，是无需这一步的。您可以去查看 Raw SQL 查询

3.1 RegisterModel
将你定义的 Model 进行注册，最佳设计是有单独的 models.go 文件，在他的 init 函数中进行注册。


3.2 RegisterModelWithPrefix： 使用表名前缀
orm.RegisterModelWithPrefix("prefix_", new(User))
创建后的表名为 prefix_user

3.3 NewOrmWithDB
有时候需要自行管理连接池与数据库链接（比如：go 的链接池无法让两次查询使用同一个链接的）
但又想使用 ORM 的查询功能

var driverName, aliasName string
// driverName 是驱动的名称
// aliasName 是当前 db 的自定义别名
var db *sql.DB
...
o := orm.NewOrmWithDB(driverName, aliasName, db)

3.4 GetDB
从已注册的数据库返回 *sql.DB 对象，默认返回别名为 default 的数据库。

db, err := orm.GetDB()
if err != nil {
    fmt.Println("get default DataBase")
}

db, err := orm.GetDB("alias")
if err != nil {
    fmt.Println("get alias DataBase")
}

3.5 ResetModelCache
重置已经注册的模型 struct，一般用于编写测试用例
	orm.ResetModelCache()

```

##### 13.2.4 orm接口方法(***)

*使用 ORM 必然接触的 Ormer 接口，我们来熟悉一下*

*切换数据库，或者，进行事务处理，都会作用于这个 Ormer 对象，以及其进行的任何查询。*

*所以,  需要 **切换数据库** 和 **事务处理** 的话，不要使用全局保存的 Ormer 对象*



type Ormer interface {

- [Read(interface{}, …string) error](https://beego.me/docs/mvc/model/object.md#read)
- [ReadOrCreate(interface{}, string, …string) (bool, int64, error)](https://beego.me/docs/mvc/model/object.md#readorcreate)
- [Insert(interface{}) (int64, error)](https://beego.me/docs/mvc/model/object.md#insert)
- [InsertMulti(int, interface{}) (int64, error)](https://beego.me/docs/mvc/model/object.md#insertmulti)
- [Update(interface{}, …string) (int64, error)](https://beego.me/docs/mvc/model/object.md#update)
- [Delete(interface{}) (int64, error)](https://beego.me/docs/mvc/model/object.md#delete)
- [LoadRelated(interface{}, string, …interface{}) (int64, error)](https://beego.me/docs/mvc/model/query.md#载入关系字段)
- [QueryM2M(interface{}, string) QueryM2Mer](https://beego.me/docs/mvc/model/query.md#多对多关系操作)
- [QueryTable(interface{}) QuerySeter](https://beego.me/docs/mvc/model/orm.md#querytable)
- [Using(string) error](https://beego.me/docs/mvc/model/orm.md#using)
- [Begin() error](https://beego.me/docs/mvc/model/transaction.md)
- [Commit() error](https://beego.me/docs/mvc/model/transaction.md)
- [Rollback() error](https://beego.me/docs/mvc/model/transaction.md)
- [Raw(string, …interface{}) RawSeter](https://beego.me/docs/mvc/model/orm.md#raw)
- [Driver() Driver](https://beego.me/docs/mvc/model/orm.md#driver)

}



##### 13.2.5 crud



-  Read / Insert / Update / Delete 

   > 如果已知主键的值，那么可以使用这些方法进行 CRUD 操作
   
   
```
    o := orm.NewOrm()
    user := new(User)
    user.Name = "slene"
   
    fmt.Println(o.Insert(user))
   
    user.Name = "Your"
    fmt.Println(o.Update(user))
    fmt.Println(o.Read(user))
    fmt.Println(o.Delete(user))
```





- Read

    ```
    o := orm.NewOrm()
    user := User{Id: 1}

    err := o.Read(&user)

    if err == orm.ErrNoRows {
        fmt.Println("查询不到")
    } else if err == orm.ErrMissPK {
        fmt.Println("找不到主键")
    } else {
        fmt.Println(user.Id, user.Name)
    }
    ```

	Read 默认通过查询主键赋值，可以使用指定的字段进行查询：

    ```
    user := User{Name: "slene"}
    err = o.Read(&user, "Name")

    ```

	对象的其他字段值将会是对应类型的默认值



- ReadOrCreate

	尝试从数据库读取，不存在的话就创建一个

	默认必须传入一个参数作为条件字段，同时也支持多个参数多个条件字段

    ```
    o := orm.NewOrm()
    user := User{Name: "slene"}
    // 三个返回参数依次为：是否新创建的，对象 Id 值，错误
    if created, id, err := o.ReadOrCreate(&user, "Name"); err == nil {
        if created {
            fmt.Println("New Insert an object. Id:", id)
        } else {
            fmt.Println("Get an object. Id:", id)
        }
    }
    ```

- Insert

    第一个返回值为自增健 Id 的值

    ```
    o := orm.NewOrm()
    var user User
    user.Name = "slene"
    user.IsActive = true
    
    id, err := o.Insert(&user)
    if err == nil {
        fmt.Println(id)
    }
    ```

    创建后会自动对 auto 的 field 赋值

    

- InsertMulti

    同时插入多个对象
    类似sql语句

    ```
    insert into table (name, age) values("slene", 28),("astaxie", 30),("unknown", 20)
    ```

		第一个参数 bulk 为并列插入的数量，第二个为对象的slice， 返回值为成功插入的数量。bulk 为 1 时，将会顺序插入 slice 中的数据
		
		users := []User{
		    {Name: "slene"},
    	    {Name: "astaxie"},
    	    {Name: "unknown"},
    	
    	}
    	successNums, err := o.InsertMulti(100, users)
	
    
    ​	
    
- Update

    第一个返回值为影响的行数

    ```
    o := orm.NewOrm()
    user := User{Id: 1}
    if o.Read(&user) == nil {
        user.Name = "MyName"
        if num, err := o.Update(&user); err == nil {
            fmt.Println(num)
        }
    }
    ```

	Update 默认更新所有的字段，可以更新指定的字段：

    ```
    // 只更新 Name
    o.Update(&user, "Name")
    // 指定多个字段
    // o.Update(&user, "Field1", "Field2", ...)
    ```

- Delete

    第一个返回值为影响的行数

    ```
    o := orm.NewOrm()
    if num, err := o.Delete(&User{Id: 1}); err == nil {
        fmt.Println(num)
    }
    ```

    Delete 操作会对反向关系进行操作，此例中 Post 拥有一个到 User 的外键。删除 User 的时候。如果 on_delete 设置为默认的级联操作，将删除对应的 Post 。 Changed in 1.0.3** 删除以后不会删除 auto field 的值





### 13.3 高级操作

##### 13.3.1 **queryseter** 概念

ORM 以 **QuerySeter** 来组织查询，每个返回 **QuerySeter** 的方法都会获得一个新的 **QuerySeter** 对象。

基本使用方法:

```
o := orm.NewOrm()

// 获取 QuerySeter 对象，user 为表名
qs := o.QueryTable("user")

// 也可以直接使用对象作为表名
user := new(User)
qs = o.QueryTable(user) // 返回 QuerySeter
```

#####   13.3.2  expr

字段组合的前后顺序依照表的关系，比如 User 表拥有 Profile 的外键，那么对 User 表查询对应的 Profile.Age 为条件，则使用 `Profile__Age` 注意，字段的分隔符号使用双下划线 `__`，除了描述字段， expr 的尾部可以增加操作符以执行对应的 sql 操作。比如 `Profile__Age__gt` 代表 Profile.Age > 18 的条件查询。

注释后面将描述对应的 sql 语句，仅仅是描述 expr 的类似结果，并不代表实际生成的语句。

```
qs.Filter("id", 1) // WHERE id = 1
qs.Filter("profile__age", 18) // WHERE profile.age = 18
qs.Filter("Profile__Age", 18) // 使用字段名和 Field 名都是允许的
qs.Filter("profile__age", 18) // WHERE profile.age = 18
qs.Filter("profile__age__gt", 18) // WHERE profile.age > 18
qs.Filter("profile__age__gte", 18) // WHERE profile.age >= 18
qs.Filter("profile__age__in", 18, 20) // WHERE profile.age IN (18, 20)

qs.Filter("profile__age__in", 18, 20).Exclude("profile__lt", 1000)
// WHERE profile.age IN (18, 20) AND NOT profile_id < 1000
```



##### 13.3.3   operators

当前支持的操作符号：

- [exact](https://beego.me/docs/mvc/model/query.md#exact) / [iexact](https://beego.me/docs/mvc/model/query.md#iexact) 等于
- [contains](https://beego.me/docs/mvc/model/query.md#contains) / [icontains](https://beego.me/docs/mvc/model/query.md#icontains) 包含
- [gt / gte](https://beego.me/docs/mvc/model/query.md#gt-%2F-gte) 大于 / 大于等于
- [lt / lte](https://beego.me/docs/mvc/model/query.md#lt-%2F-lte) 小于 / 小于等于
- [startswith](https://beego.me/docs/mvc/model/query.md#startswith) / [istartswith](https://beego.me/docs/mvc/model/query.md#istartswith) 以…起始
- [endswith](https://beego.me/docs/mvc/model/query.md#endswith) / [iendswith](https://beego.me/docs/mvc/model/query.md#iendswith) 以…结束
- [in](https://beego.me/docs/mvc/model/query.md#in)
- [isnull](https://beego.me/docs/mvc/model/query.md#isnull)

后面 `i` 开头的表示：大小写不敏感



##### 13.3.4 queryseter接口

- type QuerySeter interface {

    - [Filter(string, …interface{}) QuerySeter](https://beego.me/docs/mvc/model/query.md#filter)
    - [Exclude(string, …interface{}) QuerySeter](https://beego.me/docs/mvc/model/query.md#exclude)
    - [SetCond(*Condition) QuerySeter](https://beego.me/docs/mvc/model/query.md#setcond)
    - [Limit(int, …int64) QuerySeter](https://beego.me/docs/mvc/model/query.md#limit)
    - [Offset(int64) QuerySeter](https://beego.me/docs/mvc/model/query.md#offset)
    - [GroupBy(…string) QuerySeter](https://beego.me/docs/mvc/model/query.md#groupby)
    - [OrderBy(…string) QuerySeter](https://beego.me/docs/mvc/model/query.md#orderby)
    - [Distinct() QuerySeter](https://beego.me/docs/mvc/model/query.md#distinct)
    - [RelatedSel(…interface{}) QuerySeter](https://beego.me/docs/mvc/model/query.md#relatedsel)
    - [Count() (int64, error)](https://beego.me/docs/mvc/model/query.md#count)
    - [Exist() bool](https://beego.me/docs/mvc/model/query.md#exist)
    - [Update(Params) (int64, error)](https://beego.me/docs/mvc/model/query.md#update)
    - [Delete() (int64, error)](https://beego.me/docs/mvc/model/query.md#delete)
    - [PrepareInsert() (Inserter, error)](https://beego.me/docs/mvc/model/query.md#prepareinsert)
    - [All(interface{}, …string) (int64, error)](https://beego.me/docs/mvc/model/query.md#all)
    - [One(interface{}, …string) error](https://beego.me/docs/mvc/model/query.md#one)
    - [Values(*[]Params, …string) (int64, error)](https://beego.me/docs/mvc/model/query.md#values)
    - [ValuesList(*[]ParamsList, …string) (int64, error)](https://beego.me/docs/mvc/model/query.md#valueslist)
    - [ValuesFlat(*ParamsList, string) (int64, error)](https://beego.me/docs/mvc/model/query.md#valuesflat)

    }

    

- 每个返回 QuerySeter 的 api 调用时都会新建一个 QuerySeter，不影响之前创建的。

- 高级查询使用 Filter 和 Exclude 来做常用的条件查询。囊括两种清晰的过滤规则：包含， 排除



###### Filter

用来过滤查询结果，起到 **包含条件** 的作用

多个 Filter 之间使用 `AND` 连接

```
qs.Filter("profile__isnull", true).Filter("name", "slene")
// WHERE profile_id IS NULL AND name = 'slene'
```

###### Exclude

用来过滤查询结果，起到 **排除条件** 的作用

使用 `NOT` 排除条件

多个 Exclude 之间使用 `AND` 连接

```
qs.Exclude("profile__isnull", true).Filter("name", "slene")
// WHERE NOT profile_id IS NULL AND name = 'slene'
```

###### SetCond

自定义条件表达式

```
cond := orm.NewCondition()
cond1 := cond.And("profile__isnull", false).AndNot("status__in", 1).Or("profile__age__gt", 2000)

qs := orm.QueryTable("user")
qs = qs.SetCond(cond1)
// WHERE ... AND ... AND NOT ... OR ...

cond2 := cond.AndCond(cond1).OrCond(cond.And("name", "slene"))
qs = qs.SetCond(cond2).Count()
// WHERE (... AND ... AND NOT ... OR ...) OR ( ... )
```

###### Limit

限制最大返回数据行数，第二个参数可以设置 `Offset`

```
var DefaultRowsLimit = 1000 // ORM 默认的 limit 值为 1000

// 默认情况下 select 查询的最大行数为 1000
// LIMIT 1000

qs.Limit(10)
// LIMIT 10

qs.Limit(10, 20)
// LIMIT 10 OFFSET 20 注意跟 SQL 反过来的

qs.Limit(-1)
// no limit

qs.Limit(-1, 100)
// LIMIT 18446744073709551615 OFFSET 100
// 18446744073709551615 是 1<<64 - 1 用来指定无 limit 限制 但有 offset 偏移的情况
```

###### Offset

设置 偏移行数

```
qs.Offset(20)
// LIMIT 1000 OFFSET 20
```

###### GroupBy

```
qs.GroupBy("id", "age")
// GROUP BY id,age
```

###### OrderBy

参数使用 **expr**

在 expr 前使用减号 `-` 表示 `DESC` 的排列

```
qs.OrderBy("id", "-profile__age")
// ORDER BY id ASC, profile.age DESC

qs.OrderBy("-profile__age", "profile")
// ORDER BY profile.age DESC, profile_id ASC
```

###### Distinct

对应 sql 的 `distinct` 语句, 返回不重复的值.

```
qs.Distinct()
// SELECT DISTINCT
```

###### RelatedSel

关系查询，参数使用 **expr**

```
var DefaultRelsDepth = 5 // 默认情况下直接调用 RelatedSel 将进行最大 5 层的关系查询

qs := o.QueryTable("post")

qs.RelatedSel()
// INNER JOIN user ... LEFT OUTER JOIN profile ...

qs.RelatedSel("user")
// INNER JOIN user ...
// 设置 expr 只对设置的字段进行关系查询

// 对设置 null 属性的 Field 将使用 LEFT OUTER JOIN
```

###### Update

依据当前查询条件，进行批量更新操作

```
num, err := o.QueryTable("user").Filter("name", "slene").Update(orm.Params{
    "name": "astaxie",
})
fmt.Printf("Affected Num: %s, %s", num, err)
// SET name = "astaixe" WHERE name = "slene"
```

原子操作增加字段值

```
// 假设 user struct 里有一个 nums int 字段
num, err := o.QueryTable("user").Update(orm.Params{
    "nums": orm.ColValue(orm.ColAdd, 100),
})
// SET nums = nums + 100
```

orm.ColValue 支持以下操作

```
ColAdd      // 加
ColMinus    // 减
ColMultiply // 乘
ColExcept   // 除
```

###### Delete

依据当前查询条件，进行批量删除操作

```
num, err := o.QueryTable("user").Filter("name", "slene").Delete()
fmt.Printf("Affected Num: %s, %s", num, err)
// DELETE FROM user WHERE name = "slene"
```

###### PrepareInsert

用于一次 prepare 多次 insert 插入，以提高批量插入的速度。

```
var users []*User
...
qs := o.QueryTable("user")
i, _ := qs.PrepareInsert()
for _, user := range users {
    id, err := i.Insert(user)
    if err == nil {
        ...
    }
}
// PREPARE INSERT INTO user (`name`, ...) VALUES (?, ...)
// EXECUTE INSERT INTO user (`name`, ...) VALUES ("slene", ...)
// EXECUTE ...
// ...
i.Close() // 别忘记关闭 statement
```

###### Count

依据当前的查询条件，返回结果行数

```
cnt, err := o.QueryTable("user").Count() // SELECT COUNT(*) FROM USER
fmt.Printf("Count Num: %s, %s", cnt, err)
```

###### Exist

```
exist := o.QueryTable("user").Filter("UserName", "Name").Exist()
fmt.Printf("Is Exist: %s", exist)
```

###### All

返回对应的结果集对象

All 的参数支持 *[]Type 和 *[]*Type 两种形式的 slice

```
var users []*User
num, err := o.QueryTable("user").Filter("name", "slene").All(&users)
fmt.Printf("Returned Rows Num: %s, %s", num, err)
```

All / Values / ValuesList / ValuesFlat 受到 [Limit](https://beego.me/docs/mvc/model/query.md#limit) 的限制，默认最大行数为 1000

可以指定返回的字段：

```
type Post struct {
    Id      int
    Title   string
    Content string
    Status  int
}

// 只返回 Id 和 Title
var posts []Post
o.QueryTable("post").Filter("Status", 1).All(&posts, "Id", "Title")
```

对象的其他字段值将会是对应类型的默认值

###### One

尝试返回单条记录

```
var user User
err := o.QueryTable("user").Filter("name", "slene").One(&user)
if err == orm.ErrMultiRows {
    // 多条的时候报错
    fmt.Printf("Returned Multi Rows Not One")
}
if err == orm.ErrNoRows {
    // 没有找到记录
    fmt.Printf("Not row found")
}
```

可以指定返回的字段：

```
// 只返回 Id 和 Title
var post Post
o.QueryTable("post").Filter("Content__istartswith", "prefix string").One(&post, "Id", "Title")
```

对象的其他字段值将会是对应类型的默认值




###### Values

返回结果集的 key => value 值

key 为Model里的Field name, value的值是interface{}类型,例如，如果你要将value赋值给struct中的某字段，需要根据结构体对应字段类型使用[断言](https://golang.org/ref/spec#Type_assertions)获取真实值。举例:`Name : m["Name"].(string)`

```
var maps []orm.Params
num, err := o.QueryTable("user").Values(&maps)
if err == nil {
    fmt.Printf("Result Nums: %d\n", num)
    for _, m := range maps {
        fmt.Println(m["Id"], m["Name"])
    }
}
```

返回指定的 Field 数据

**TODO**: 暂不支持级联查询 **RelatedSel** 直接返回 Values

但可以直接指定 expr 级联返回需要的数据

```
var maps []orm.Params
num, err := o.QueryTable("user").Values(&maps, "id", "name", "profile", "profile__age")
if err == nil {
    fmt.Printf("Result Nums: %d\n", num)
    for _, m := range maps {
        fmt.Println(m["Id"], m["Name"], m["Profile"], m["Profile__Age"])
        // map 中的数据都是展开的，没有复杂的嵌套
    }
}
```

###### ValuesList

顾名思义，返回的结果集以slice存储

结果的排列与 Model 中定义的 Field 顺序一致

返回的每个元素值以 string 保存

```
var lists []orm.ParamsList
num, err := o.QueryTable("user").ValuesList(&lists)
if err == nil {
    fmt.Printf("Result Nums: %d\n", num)
    for _, row := range lists {
        fmt.Println(row)
    }
}
```

当然也可以指定 expr 返回指定的 Field

```
var lists []orm.ParamsList
num, err := o.QueryTable("user").ValuesList(&lists, "name", "profile__age")
if err == nil {
    fmt.Printf("Result Nums: %d\n", num)
    for _, row := range lists {
        fmt.Printf("Name: %s, Age: %s\m", row[0], row[1])
    }
}
```

###### ValuesFlat

只返回特定的 Field 值，将结果集展开到单个 slice 里

```
var list orm.ParamsList
num, err := o.QueryTable("user").ValuesFlat(&list, "name")
if err == nil {
    fmt.Printf("Result Nums: %d\n", num)
    fmt.Printf("All User Names: %s", strings.Join(list, ", "))
}
```





##### 13.3.5  关系查询

以例子里的[模型定义](https://beego.me/docs/mvc/model/orm.md)来看下怎么进行关系查询

###### 一对一

```
// 已经取得了 User 对象，查询 Profile：
user := &User{Id: 1}
o.Read(user)
if user.Profile != nil {
    o.Read(user.Profile)
}
```

直接关联查询：

```
user := &User{}
o.QueryTable("user").Filter("Id", 1).RelatedSel().One(user)
// 自动查询到 Profile
fmt.Println(user.Profile)
// 因为在 Profile 里定义了反向关系的 User，所以 Profile 里的 User 也是自动赋值过的，可以直接取用。
fmt.Println(user.Profile.User)

// [SELECT T0.`id`, T0.`name`, T0.`profile_id`, T1.`id`, T1.`age` FROM `user` T0 INNER JOIN `profile` T1 ON T1.`id` = T0.`profile_id` WHERE T0.`id` = ? LIMIT 1000] - `1`
```

通过 User 反向查询 Profile：

```
var profile Profile
err := o.QueryTable("profile").Filter("User__Id", 1).One(&profile)
if err == nil {
    fmt.Println(profile)
}
```



###### 多对一

```
// Post 和 User 是 ManyToOne 关系，也就是 ForeignKey 为 User
type Post struct {
    Id    int
    Title string
    User  *User  `orm:"rel(fk)"`
    Tags  []*Tag `orm:"rel(m2m)"`
}
var posts []*Post
num, err := o.QueryTable("post").Filter("User", 1).RelatedSel().All(&posts)
if err == nil {
    fmt.Printf("%d posts read\n", num)
    for _, post := range posts {
        fmt.Printf("Id: %d, UserName: %d, Title: %s\n", post.Id, post.User.UserName, post.Title)
    }
}
// [SELECT T0.`id`, T0.`title`, T0.`user_id`, T1.`id`, T1.`name`, T1.`profile_id`, T2.`id`, T2.`age` FROM `post` T0 INNER JOIN `user` T1 ON T1.`id` = T0.`user_id` INNER JOIN `profile` T2 ON T2.`id` = T1.`profile_id` WHERE T0.`user_id` = ? LIMIT 1000] - `1`
```

根据 Post.Title 查询对应的 User：

RegisterModel 时，ORM 也会自动建立 User 中 Post 的反向关系，所以可以直接进行查询

```
var user User
err := o.QueryTable("user").Filter("Post__Title", "The Title").Limit(1).One(&user)
if err == nil {
    fmt.Printf(user)
}
```



###### 多对多

```
// Post 和 Tag 是 ManyToMany 关系, 设置 rel(m2m) 以后，ORM 会自动创建中间表

type Post struct {
    Id    int
    Title string
    User  *User  `orm:"rel(fk)"`
    Tags  []*Tag `orm:"rel(m2m)"`
}
type Tag struct {
    Id    int
    Name  string
    Posts []*Post `orm:"reverse(many)"`
}
```

一条 Post 纪录可能对应不同的 Tag 纪录,一条 Tag 纪录可能对应不同的 Post 纪录，所以 Post 和 Tag 属于多对多关系,通过 tag name 查询哪些 post 使用了这个 tag

```
var posts []*Post
num, err := dORM.QueryTable("post").Filter("Tags__Tag__Name", "golang").All(&posts)
```

通过 post title 查询这个 post 有哪些 tag

```
var tags []*Tag
num, err := dORM.QueryTable("tag").Filter("Posts__Post__Title", "Introduce Beego ORM").All(&tags)
```



#####   13.3.6 载入关系字段

LoadRelated 用于载入模型的关系字段，包括所有的 rel/reverse - one/many 关系

ManyToMany 关系字段载入

```
// 载入相应的 Tags
post := Post{Id: 1}
err := o.Read(&post)
num, err := o.LoadRelated(&post, "Tags")
// 载入相应的 Posts
tag := Tag{Id: 1}
err := o.Read(&tag)
num, err := o.LoadRelated(&tag, "Posts")
```

User 是 Post 的 ForeignKey，对应的 ReverseMany 关系字段载入

```
type User struct {
    Id    int
    Name  string
    Posts []*Post `orm:"reverse(many)"`
}

user := User{Id: 1}
err := dORM.Read(&user)
num, err := dORM.LoadRelated(&user, "Posts")
for _, post := range user.Posts {
    //...
}
```



#####   13.3.7 多对多关系操作

- type QueryM2Mer interface {

    - [Add(…interface{}) (int64, error)](https://beego.me/docs/mvc/model/query.md#querym2mer-add)
    - [Remove(…interface{}) (int64, error)](https://beego.me/docs/mvc/model/query.md#querym2mer-remove)
    - [Exist(interface{}) bool](https://beego.me/docs/mvc/model/query.md#querym2mer-exist)
    - [Clear() (int64, error)](https://beego.me/docs/mvc/model/query.md#querym2mer-clear)
    - [Count() (int64, error)](https://beego.me/docs/mvc/model/query.md#querym2mer-count)

    }

创建一个 QueryM2Mer 对象

```
o := orm.NewOrm()
post := Post{Id: 1}
m2m := o.QueryM2M(&post, "Tags")
// 第一个参数的对象，主键必须有值
// 第二个参数为对象需要操作的 M2M 字段
// QueryM2Mer 的 api 将作用于 Id 为 1 的 Post
```

###### Add

```
tag := &Tag{Name: "golang"}
o.Insert(tag)

num, err := m2m.Add(tag)
if err == nil {
    fmt.Println("Added nums: ", num)
}
```

Add 支持多种类型 Tag *Tag []*Tag []Tag []interface{}

```
var tags []*Tag
...
// 读取 tags 以后
...
num, err := m2m.Add(tags)
if err == nil {
    fmt.Println("Added nums: ", num)
}
// 也可以多个作为参数传入
// m2m.Add(tag1, tag2, tag3)
```

###### Remove

从M2M关系中删除 tag

Remove 支持多种类型 Tag *Tag []*Tag []Tag []interface{}

```
var tags []*Tag
...
// 读取 tags 以后
...
num, err := m2m.Remove(tags)
if err == nil {
    fmt.Println("Removed nums: ", num)
}
// 也可以多个作为参数传入
// m2m.Remove(tag1, tag2, tag3)
```

###### Exist

判断 Tag 是否存在于 M2M 关系中

```
if m2m.Exist(&Tag{Id: 2}) {
    fmt.Println("Tag Exist")
}
```

###### Clear

清除所有 M2M 关系

```
nums, err := m2m.Clear()
if err == nil {
    fmt.Println("Removed Tag Nums: ", nums)
}
```

###### Count

计算 Tag 的数量

```
nums, err := m2m.Count()
if err == nil {
    fmt.Println("Total Nums: ", nums)
}
```





### 13.4 原生sql

**优点：**

- 使用 Raw SQL 查询，无需使用 ORM 表定义
- 多数据库，都可直接使用占位符号  ? ，自动转换
- 查询时的参数，支持使用 Model Struct 和 Slice, Array



**方法：**

type RawSeter interface {

- [Exec() (sql.Result, error)](https://beego.me/docs/mvc/model/rawsql.md#exec)
- [QueryRow(…interface{}) error](https://beego.me/docs/mvc/model/rawsql.md#queryrow)
- [QueryRows(…interface{}) (int64, error)](https://beego.me/docs/mvc/model/rawsql.md#queryrows)
- [SetArgs(…interface{}) RawSeter](https://beego.me/docs/mvc/model/rawsql.md#setargs)
- [Values(*[]Params, …string) (int64, error)](https://beego.me/docs/mvc/model/rawsql.md#values)
- [ValuesList(*[]ParamsList, …string) (int64, error)](https://beego.me/docs/mvc/model/rawsql.md#valueslist)
- [ValuesFlat(*ParamsList, string) (int64, error)](https://beego.me/docs/mvc/model/rawsql.md#valuesflat)
- [RowsToMap(*Params, string, string) (int64, error)](https://beego.me/docs/mvc/model/rawsql.md#rowstomap)
- [RowsToStruct(interface{}, string, string) (int64, error)](https://beego.me/docs/mvc/model/rawsql.md#rowstostruct)
- [Prepare() (RawPreparer, error)](https://beego.me/docs/mvc/model/rawsql.md#prepare)

}



**初始化**

    o := orm.NewOrm()
    var r RawSeter
    r = o.Raw("UPDATE user SET name = ? WHERE name = ?", "testing", "slene")

  






**Exec**

执行 sql 语句，返回 [sql.Result](http://gowalker.org/database/sql#Result) 对象

```
res, err := o.Raw("UPDATE user SET name = ?", "your").Exec()
if err == nil {
    num, _ := res.RowsAffected()
    fmt.Println("mysql row affected nums: ", num)
}
```



**QueryRow**

QueryRow 和 QueryRows 提供高级 sql mapper 功能

支持 struct

```
type User struct {
    Id       int
    UserName string
}

var user User
err := o.Raw("SELECT id, user_name FROM user WHERE id = ?", 1).QueryRow(&user)
```

> from beego 1.1.0 取消了多个对象支持 [ISSUE 384](https://github.com/astaxie/beego/issues/384)



**QueryRows**

QueryRows 支持的对象还有 map 规则是和 QueryRow 一样的，但都是 slice

```
type User struct {
    Id       int
    UserName string
}

var users []User
num, err := o.Raw("SELECT id, user_name FROM user WHERE id = ?", 1).QueryRows(&users)
if err == nil {
    fmt.Println("user nums: ", num)
}
```

> from beego 1.1.0 取消了多个对象支持 [ISSUE 384](https://github.com/astaxie/beego/issues/384)





**SetArgs**

改变 Raw(sql, args…) 中的 args 参数，返回一个新的 RawSeter

用于单条 sql 语句，重复利用，替换参数然后执行。

```
res, err := r.SetArgs("arg1", "arg2").Exec()
res, err := r.SetArgs("arg1", "arg2").Exec()
...
```



**Values / ValuesList / ValuesFlat**

Raw SQL 查询获得的结果集 Value 为 `string` 类型，NULL 字段的值为空 , from beego 1.1.0
Values, ValuesList, ValuesFlat 的参数，可以指定返回哪些 Columns 的数据,  通常情况下，是无需指定的，因为 sql 语句中你可以自行设置 SELECT 的字段



**Values**

返回结果集的 key => value 值

```
var maps []orm.Params
num, err := o.Raw("SELECT user_name FROM user WHERE status = ?", 1).Values(&maps)
if err == nil && num > 0 {
    fmt.Println(maps[0]["user_name"]) // slene
}
```



**ValuesList**

返回结果集 slice

```
var lists []orm.ParamsList
num, err := o.Raw("SELECT user_name FROM user WHERE status = ?", 1).ValuesList(&lists)
if err == nil && num > 0 {
    fmt.Println(lists[0][0]) // slene
}
```



**ValuesFlat**

返回单一字段的平铺 slice 数据

```
var list orm.ParamsList
num, err := o.Raw("SELECT id FROM user WHERE id < ?", 10).ValuesFlat(&list)
if err == nil && num > 0 {
    fmt.Println(list) // []{"1","2","3",...}
}
```



**RowsToMap**

SQL 查询结果是这样

| name  | value |
| ----- | ----- |
| total | 100   |
| found | 200   |

查询结果匹配到 map 里

```
res := make(orm.Params)
nums, err := o.Raw("SELECT name, value FROM options_table").RowsToMap(&res, "name", "value")
// res is a map[string]interface{}{
//  "total": 100,
//  "found": 200,
// }
```



**RowsToStruct**

SQL 查询结果是这样

| name  | value |
| ----- | ----- |
| total | 100   |
| found | 200   |

查询结果匹配到 struct 里

```
type Options struct {
    Total int
    Found int
}

res := new(Options)
nums, err := o.Raw("SELECT name, value FROM options_table").RowsToStruct(res, "name", "value")
fmt.Println(res.Total) // 100
fmt.Println(res.Found) // 200
```

> 匹配支持的名称转换为 snake -> camel, eg: SELECT user_name  需要你的 struct 中定义有 UserName



**Prepare**

用于一次 prepare 多次 exec，以提高批量执行的速度。


    p, err := o.Raw("UPDATE user SET name = ? WHERE name = ?").Prepare()
    res, err := p.Exec("testing", "slene")
    res, err  = p.Exec("testing", "astaxie")
    
    p.Close() // 别忘记关闭 statement







### 13.5 构造查询(***)

**QueryBuilder** 提供了一个简便，流畅的 SQL 查询构造器。在不影响代码可读性的前提下用来快速的建立 SQL 语句。

**QueryBuilder** 在功能上与 ORM 重合， 但是各有利弊。**ORM 更适用于简单的 CRUD 操作，而 QueryBuilder 则更适用于复杂的查询，例如查询中包含子查询和多重联结**。

使用方法:

```
type User struct {
    Name string
    Age  int
}
var users []User

// 获取 QueryBuilder 对象. 需要指定数据库驱动参数。
// 第二个返回值是错误对象，在这里略过
qb, _ := orm.NewQueryBuilder("mysql")

// 构建查询对象
qb.Select("user.name",
    "profile.age").
    From("user").
    InnerJoin("profile").On("user.id_user = profile.fk_user").
    Where("age > ?").
    OrderBy("name").Desc().
    Limit(10).Offset(0)

// 导出 SQL 语句
sql := qb.String()

// 执行 SQL 语句
o := orm.NewOrm()
o.Raw(sql, 20).QueryRows(&users)
```

完整 API 接口:

```
type QueryBuilder interface {
    Select(fields ...string) QueryBuilder
    From(tables ...string) QueryBuilder
    InnerJoin(table string) QueryBuilder
    LeftJoin(table string) QueryBuilder
    RightJoin(table string) QueryBuilder
    On(cond string) QueryBuilder
    Where(cond string) QueryBuilder
    And(cond string) QueryBuilder
    Or(cond string) QueryBuilder
    In(vals ...string) QueryBuilder
    OrderBy(fields ...string) QueryBuilder
    Asc() QueryBuilder
    Desc() QueryBuilder
    Limit(limit int) QueryBuilder
    Offset(offset int) QueryBuilder
    GroupBy(fields ...string) QueryBuilder
    Having(cond string) QueryBuilder
    Subquery(sub string, alias string) string
    String() string
}
```



### 13.6 事务处理

```
o := NewOrm()
err := o.Begin()
// 事务处理过程
...

...
// 此过程中的所有使用 o Ormer 对象的查询都在事务处理范围内
if SomeError {
    err = o.Rollback()
} else {
    err = o.Commit()
}
```



### 13.7 命令模式

- 注册模型与数据库以后，调用 RunCommand 执行 orm 命令。

        ```
        func main() {
            // orm.RegisterModel...
            // orm.RegisterDataBase...
            ...
            orm.RunCommand()
        }
        
        go build main.go
        ./main orm
        
        # 直接执行可以显示帮助
        # 如果你的程序可以支持的话，直接运行 go run main.go orm 也是一样的效果
        ```

 

- 自动建表

  
        ./main orm syncdb -h
        Usage of orm command: syncdb:
          -db="default": DataBase alias name
          -force=false: drop tables before create
          -v=false: verbose info
    
    
    使用 `-force=1` 可以 drop table 后再建表
    使用 `-v` 可以查看执行的 sql 语句  



- 调用自动建表：

  
        // 数据库别名
        name := "default"
        
        // drop table 后再建表
        force := true
        
        // 打印执行过程
        verbose := true
        
        // 遇到错误立即返回
        err := orm.RunSyncdb(name, force, verbose)
        
        if err != nil {
            fmt.Println(err)
        }
    

    自动建表功能在非 force 模式下，是会自动创建新增加的字段的。也会创建新增加的索引。

    对于改动过的旧字段，旧索引，需要用户自行进行处理。

    

- 打印建表SQL， 默认使用别名为 default 的数据库。
        ```
    ./main orm sqlall -h
    Usage of orm command: syncdb:  -db="default": DataBase alias name
        ```





## 14. 模板

### 14.1 视图函数(模板函数)

> beego支持用户定义视图函数，但是必须在beego.Run()调用之前

```
需求： html标签属性不能直接进行数学运算。这时候我们就要想办法，不在视图里面操作，并且给pageIndex减1，方法有很多，这里呢，老师给你们介绍一种beego处理这种简单业务逻辑的方法，视图函数

使用条件: beego支持用户定义视图函数，但是必须在beego.Run()调用之前
```

- 先定义函数

```
func hello(in string)(out string){
    out = in + "world"
    return
}
```

- 添加映射

  添加映射是把后台的函数名和视图中调用的函数名关联起来，两个名字可以不一样。用的方法是AddFuncMap(),第一个参数是视图中调用的函数名，第二个参数是后台的函数名

  ```go
  beego.AddFuncMap("hi",hello)   // 这一步必须在beego.Run()之前调用
  ```

- 在视图中调用，有两种形式

  第一种调用视图函数

  ```html
  {{.Content | hi }}
  ```

  > 注意，这里面的 .Content是传递给函数的参数，类型要一致，函数的返回值将在这里显示,  只能传递一个参数

  第二种调用视图函数

  ```html
  {{hi .Content}}
  ```

  > 第二种方法刚好和第一种方法顺序反过来，是先写函数名，再写参数，如果参数比较多，可以一直往后写。这种方法在开发中也比较常用。



- beego默认封装的视图函数

|   函数名   |                           函数作用                           | 使用方法                                         |
| :--------: | :----------------------------------------------------------: | ------------------------------------------------ |
| dateformat |               实现了时间的格式化，返回字符串。               | {{dateformat .Time “2006-01-02T15:04:05Z07:00”}} |
|    date    | 实现了类似 PHP 的 date 函数，可以很方便的根据字符串返回时间 。 | {{date .T “Y-m-d H:i:s”}}                        |
|  compare   |  实现了比较两个对象的比较，如果相同返回 true，否者 false。   | {{compare .A .B}}                                |
|   substr   |          实现了字符串的截取，支持中文截取的完美截取          | {{substr .Str 0 30}}                             |
|  html2str  | 实现了把 html 转化为字符串，剔除一些 script、css 之类的元素，返回纯文本信息 。 | {{html2str .Htmlinfo}}                           |
|  str2html  |         实现了把相应的字符串当作 HTML 来输出，不转义         | {{str2html .Strhtml}}                            |





## 15. 其他

### 15.1 静态资源

```
// 该代码在在 main.go 文件中 beego.Run() 之前加入
beego.SetStaticPath("/down1", "download1")
beego.Run()
```



### 15.2 进程内监控

> 为了安全，建议用户在防火墙中把 8088 端口给屏蔽了。你可以在 conf/app.conf 中打开它

#### 15.2.1 配置

默认监控是关闭的，你可以通过设置参数配置开启监控：

```
EnableAdmin = true
```

而且你还可以修改监听的地址和端口：

```
AdminAddr = "localhost"
AdminPort = 8088
```

打开浏览器，输入 URL：`http://localhost:8088/`，你会看到一句欢迎词：`Welcome to Admin Dashboard`。

#### 15.2.2 请求统计信息

访问统计的 URL 地址 `http://localhost:8088/qps`

#### 15.2.3 性能调试

你可以查看程序性能相关的信息, 进行性能调优.

#### 15.2.4 健康检查

需要手工注册相应的健康检查逻辑，才能通过 URL`http://localhost:8088/healthcheck` 获取当前执行的健康检查的状态。

#### 15.2.5 定时任务

用户需要在应用中添加了 [task](https://beego.me/docs/module/toolbox.md#task)，才能执行相应的任务检查和手工触发任务。

- 检查任务状态 URL：`http://localhost:8088/task`
- 手工执行任务 URL：`http://localhost:8088/task?taskname=任务名`

#### 15.2.6 配置信息

应用开发完毕之后，我们可能需要知道在运行的进程到底是怎么样的配置，beego 的监控模块提供了这一功能。

- 显示所有的配置信息: `http://localhost:8088/listconf?command=conf`
- 显示所有的路由配置信息: `http://localhost:8088/listconf?command=router`
- 显示所有的过滤设置信息: `http://localhost:8088/listconf?command=filter`







### 15.3 api文档

>  `bee api beeapi` 新建一个 API 应用， 是否必须？ bee new 是否可以，手动添加doc
>
>  参数变化，如何文档自动更新呢？

#### 15.3.1 全局设置

必须设置在 `routers/router.go` 中，文件的注释，最顶部：

```
// @APIVersion 1.0.0
// @Title mobile API
// @Description mobile has every tool to get any job done, so codename for the new mobile APIs.
// @Contact astaxie@gmail.com
package routers
```

全局的注释如上所示，是显示给全局应用的设置信息，有如下这些设置

- @APIVersion
- @Title
- @Description
- @Contact
- @TermsOfServiceUrl
- @License
- @LicenseUrl



#### 15.3.2 路由解析须知

目前自动化文档只支持如下的写法的解析，即 namespace+Include 的写法,其他写法函数不会自动解析，而且只支持二级解析，一级版本号，二级分别表示应用模块

```
func init() {
    ns :=
        beego.NewNamespace("/v1",
            beego.NSNamespace("/customer",
                beego.NSInclude(
                    &controllers.CustomerController{},
                    &controllers.CustomerCookieCheckerController{},
                ),
            ),
            beego.NSNamespace("/catalog",
                beego.NSInclude(
                    &controllers.CatalogController{},
                ),
            ),
            beego.NSNamespace("/newsletter",
                beego.NSInclude(
                    &controllers.NewsLetterController{},
                ),
            ),
            beego.NSNamespace("/cms",
                beego.NSInclude(
                    &controllers.CMSController{},
                ),
            ),
            beego.NSNamespace("/suggest",
                beego.NSInclude(
                    &controllers.SearchController{},
                ),
            ),
        )
    beego.AddNamespace(ns)
}

```

#### 15.3.3 应用注释

```
package controllers

import "github.com/astaxie/beego"

// CMS API
type CMSController struct {
    beego.Controller
}

func (c *CMSController) URLMapping() {
    c.Mapping("StaticBlock", c.StaticBlock)
    c.Mapping("Product", c.Product)
}

// @Title getStaticBlock
// @Description get all the staticblock by key
// @Param   key     path    string  true        "The email for login"
// @Success 200 {object} models.ZDTCustomer.Customer
// @Failure 400 Invalid email supplied
// @Failure 404 User not found
// @router /staticblock/:key [get]
func (c *CMSController) StaticBlock() {

}

// @Title Get Product list
// @Description Get Product list by some info
// @Success 200 {object} models.ZDTProduct.ProductList
// @Param   category_id     query   int false       "category id"
// @Param   brand_id    query   int false       "brand id"
// @Param   query   query   string  false       "query of search"
// @Param   segment query   string  false       "segment"
// @Param   sort    query   string  false       "sort option"
// @Param   dir     query   string  false       "direction asc or desc"
// @Param   offset  query   int     false       "offset"
// @Param   limit   query   int     false       "count limit"
// @Param   price           query   float       false       "price"
// @Param   special_price   query   bool        false       "whether this is special price"
// @Param   size            query   string      false       "size filter"
// @Param   color           query   string      false       "color filter"
// @Param   format          query   bool        false       "choose return format"
// @Failure 400 no enough input
// @Failure 500 get products common error
// @router /products [get]
func (c *CMSController) Product() {
	// pass
}
```

- @Title

    这个 API 所表达的含义，是一个文本，空格之后的内容全部解析为 title

- @Description

    这个 API 详细的描述，是一个文本，空格之后的内容全部解析为 Description

- @Param (***)

    参数，表示需要传递到服务器端的参数，有五列参数，使用空格或者 tab 分割，五个分别表示的含义如下

    1. 参数名

    2. 参数类型，可以有的值是 formData、query、path、body、header，

        formData 表示是 post 请求的数据，

        query 表示带在 url 之后的参数，

        path 表示请求路径上得参数，例如上面例子里面的 key，

        body 表示是一个 raw 数据请求，

        header 表示带在 header 信息中得参数。

    3. 参数类型

    4. 是否必须

    5. 注释

- @Success

    成功返回给客户端的信息，三个参数，第一个是 status code。第二个参数是返回的类型，必须使用 {} 包含，第三个是返回的对象或者字符串信息，如果是 {object} 类型，那么 bee 工具在生成 docs 的时候会扫描对应的对象，这里填写的是想对你项目的目录名和对象，例如 `models.ZDTProduct.ProductList` 就表示 `/models/ZDTProduct` 目录下的 `ProductList` 对象。

    > 三个参数必须通过空格分隔

- @Failure

    失败返回的信息，包含两个参数，使用空格分隔，第一个表示 status code，第二个表示错误信息

- @router

    路由信息，包含两个参数，使用空格分隔，第一个是请求的路由地址，支持正则和自定义路由，和之前的路由规则一样，第二个参数是支持的请求方法,  放在 `[]` 之中，如果有多个方法，那么使用 `,` 分隔。



#### 15.3.4 生成文档

- 第一开启应用内文档开关，在配置文件中设置：`EnableDocs = true`

- 然后在你的 `main.go` 函数中引入 `_ "beeapi/docs"`（beego 1.7.0 之后版本不需要添加该引用）。

- 这样你就已经内置了 docs 在你的 API 应用中，然后你就使用

     `bee run -gendoc=true -downdoc=true` 

    让我们的 API 应用跑起来，`-gendoc=true` 表示每次自动化的 build 文档，`-downdoc=true` 就会自动的下载 swagger 文档查看器

- 现在打开你的浏览器查看一下效果：  localhost:8888/swagger



#### 15.3.5 可能存在的问题

CORS 两种解决方案：

- 方案一：把 swagger 集成到应用中，下载请到[swagger](https://github.com/beego/swagger/releases),然后放在项目目录下：

    ```
    if beego.BConfig.RunMode == "dev" {
        beego.BConfig.WebConfig.DirectoryIndex = true
        beego.BConfig.WebConfig.StaticDir["/swagger"] = "swagger"
    }
    ```

- 方案二：API 增加 CORS 支持

    ```
    ctx.Output.Header("Access-Control-Allow-Origin", "*")
    ```

