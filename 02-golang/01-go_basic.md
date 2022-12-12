对照具体的代码看



## 1. 注释

```
//

/**/
```

## 2. 变量 

> 注意事项：自动推导，不同数据类型不能直接计算

```
在程序运行过程中其值能够改变的量成为变量

变量存在内存中	

变量定义格式： 
方式一：
var 变量名 数据类型         声明
var 变量名 数据类型 = 值    定义(申明并赋值)

方式二：
变量名:= 值                自动推导类型
```


### 2.1 多重赋值

```
a , b , c , d = 10 , 20 , 30 , 40
```



### 2.2 匿名赋值

```
_ , a = 10, 20 
```



```
ce: cheat engine 内存工具
```



## 3. 格式化输入输出

```

fmt.Println()//输出数据 自带换行
fmt.Print()  //输出数据 不带换行
fmt.Printf() //格式化输出数据 

%d 整型      (%5d)
%f 浮点型 

%c 字符类型
%b
%x / %X
%o

%v  相应值的默认格式
%+v 会添加字段名
%#v 相应值的 Go 语法表示

%p 内存地址

%s	字符串。输出字符串中的字符直至字符串中的空字符（字符串以'\0‘结尾，这个'\0'即空字符）
%t	以true或者false输出的布尔值
%T	使用Go语法输出的值的类型


fmt.Scan()  //输入数据  &变量  &-取地址符号
fmt.Scanf() //格式化输入数据

空格或者回车作为结束符

eg:
fmt.Scan(&age)
fmt.Scanf("%d",&age)
```


## 4. 变量命名规则

```

1、只能以字母或下划线开头
2、只能使用字母 数字 下划线
3、区分大小写
4、不能使用系统关键字
5、见名知义

```

## 5. 基本数据类型

```
类型	名称	  长度  零值	说明
bool  布尔类型	1	false	其值不为真即为假，不可以用数字代表true或false

int/uint 整型	4或8	0	有符号32位或无符号64位
int8	整型	1	0	-128 ~ 127, +
uint8	整型	1	0	0 ~ 255
int16 	整型	2	0	-32768 ~ 32767,
uint16	整型	2	0	0 ~ 65535
int32	整型	4	0	-2147483648 到 2147483647
uint32	整型	4	0	0 到 4294967295(42亿)
int64 	整型	8	0   0到18446744073709551615（1844京）
uint64	整型	8	0	-9223372036854775808到 9223372036854775807

float32	浮点型	4	0.0	小数位精确到7位
float64	浮点型	8	0.0	小数位精确到15位

complex64	复数类型	8		
complex128	复数类型	16		64 位实数和虚数

byte	字节型	     1	 0	 uint8别名
rune	字符类型	4	0	专用于存储unicode编码，等价于uint32
uintptr	整型	      4或8	  足以存储指针的uint32或uint64整数

string	字符串		""	utf-8字符串
```



## 6. 常量

### 6.1 常量的定义
```
const PI int = 3.14
```



### 6.2 字面常量

```
const PI int = 3.14
```



### 6.3 iota 枚举


```
常量声明可以使用iota常量生成器 初始化，它用于生成一组以相似规则初始化的常量，但是不用每行都写一遍初始化表达式。
注意：
	1.在一个const声明语句中，在第一个声明的常量所在的行，iota被置为0，然后在每一个有常量声明的行加一。
	2.写在同一行的值是相同的

const (
    a = iota
    b
    c
)

// a = 0, b = 1, c = 2
```



## 7. 运算符

### 7.1 算数运算符
```
+	加	10 + 5	15
-	减	10 - 5	5
*	乘	10 * 5	50
/	除	10 / 5	2      10 / 5.1   1.9607843137254901   / 结果既可以是整数，也可以是小数 
%	取模(取余)	10 % 3	1
++	后自增，没有前自增	a=0; a++	a=1
--	后自减，没有前自减	a=2; a--	a=1
```



### 7.2 类型转换

```
Go语言中不允许隐式转换，所有类型转换必须显式声明（强制转换），而且转换只能发生在两种相互兼容的类型之间
```



### 7.3 赋值运算符

```
=	普通赋值	c = a + b 将 a + b 表达式结果赋值给 c
+=	相加后再赋值	c += a 等价于 c = c + a
-=	相减后再赋值	c -= a 等价于 c = c - a
*=	相乘后再赋值	c *= a 等价于 c = c * a
/=	相除后再赋值	c /= a 等价于 c = c / a
%=	求余后再赋值	c %= a 等价于 c = c % a

```

### 7.4 关系运算符

```
==	相等于	4 == 3	false
!=	不等于	4 != 3	true
<	小于	4 < 3	false
>	大于	4 > 3	true
<=	小于等于	4 <= 3	false
>=	大于等于	4 >= 1	true

```

### 7.5 逻辑运算符

```
!	非	!a	如果a为假，则!a为真；如果a为真，则!a为假。
&&	与	a && b	如果a和b都为真，则结果为真，否则为假。
||	或	a || b 如果a和b有一个为真，则结果为真，二者都为假时，结果为假。

```

### 7.6 其他运算符

```

&	取地址运算符	&a	变量a的地址
*	取值运算符	*a	指针变量a所指向内存的值

```


### 7.6 运算符优先级

```
优先级	运算符
7	^    !   . 
6	*(乘法)    /    %    <<    >>    &      &^
5	+    -     |      ^
4	==   !=   <    <=    >=    >
3	<-
2	&&
1	||


1	逗号运算符	,	从左到右
2	赋值运算符	=、+=、-=、*=、/=、 %=、 >=、 <<=、&=、^=、|=	从右到左
3	逻辑或	||	从左到右
4	逻辑与	&&	从左到右
5	按位或	|	从左到右
6	按位异或	^	从左到右
7	按位与	&	从左到右
8	相等/不等	==、!=	从左到右
9	关系运算符	<、<=、>、>=	从左到右
10	位移运算符	<<、>>	从左到右
11	加法/减法	+、-	从左到右
12	乘法/除法/取余	*（乘号）、/、%	从左到右
13	单目运算符	!、*（指针）、& 、++、–、+（正号）、-（负号）	从右到左
14	后缀运算符	( )、[ ]、->	从左到右
```


## 8. 流程控制
### 8.1 if 

> 代码特点： 很多是没有小括号，分号， 冒号的 ( switch中是个例外)

基本语法如下：
```
if 条件判断 {
	要执行的代码段
}else if 条件判断 {
	要执行的代码段
}else if 条件判断 {
	要执行的代码段
}else if 条件判断 {
  	要执行的代码段
}else {
	
}
```

### 8.2 switch

> https://www.runoob.com/go/go-switch-statement.html

格式一：
```
switch 变量或者表达式的值 {
	case 值1:
		要执行的代码
	case 值2:
		要执行的代码
	case 值3:
		要执行的代码
	default:
		要执行的代码
}

e.g:
var marks int = 90
switch marks {
    case 90: grade = "A"
    case 80: grade = "B"
    case 50,60,70 : grade = "C"
    default: grade = "D"  
}
```


格式二：

```
switch score := 70 ; {
	case 表达式1:
		要执行的代码
	case 表达式1:
		要执行的代码
	case 表达式1:
		要执行的代码
	default:
		要执行的代码
}

等价于

var score int = 70
switch score {
	case 表达式1:
		要执行的代码
	case 表达式1:
		要执行的代码
	case 表达式1:
		要执行的代码
	default:
		要执行的代码
}

等价于 

switch {
      case grade == "A" :
         fmt.Printf("优秀!\n" )    
      case grade == "B", grade == "C" :
         fmt.Printf("良好\n" )      
      case grade == "D" :
         fmt.Printf("及格\n" )      
      case grade == "F":
         fmt.Printf("不及格\n" )
      default:
         fmt.Printf("差\n" );
   }
/*
某个case后面跟着的代码执行完毕后，不会再执行后面的case，而是跳出整个switch结构，相当于每个case后面都跟着break(终止)，但是如果我们想执行完成某个case后，强制执行后面的case,可以使用fallthrough。
*/

```

格式三：

```
var x interface{}

switch i := x.(type) {
case nil:  
   	fmt.Printf(" x 的类型 :%T",i)                
case int:  
     fmt.Printf("x 是 int 型")                      
case float64:
     fmt.Printf("x 是 float64 型")          
case func(int) float64:
     fmt.Printf("x 是 func(int) 型")                      
case bool, string:
     fmt.Printf("x 是 bool 或 string 型" )      
default:
     fmt.Printf("未知型")    
}  
```



### 8.3 for

基本语法结构如下：
```
for 表达式1;表达式2;表达式3 {
	循环体
}

```
说明：
```
在GO语言中，我们有专门实现这种循环的结构就是for结构（GO语言中只有for循环结构，没有while, 
do-while结构）
```

遍历：

```
for i, data := range arr{
    fmt.Println(data)
}
```



### 8.4 跳转

```
break, continue, goto
```



## 9. 函数
### 9.1 函数定义

```
func 函数名(){
  函数体
}
```



### 9.2 函数参数



### 9.3 函数不定参

```
func test(args ...int){
    // pass 
}

// 不定参在内存中是连续存储的
// 不定参内部再传递的时候，参数也要是不定的 ,  test(a[1:3]...)
```



### 9.4 函数返回值

>  建议return 的时候跟上变量名， 方便阅读

```
格式一： 单个返回值，int前可以不写参数名
func test() int {  
    return a + b
}

格式二：
func test() (sum int){  
    return  sum
}

格式三：
func test(a int, b int) (sum int) {
	sum = a + b
	return
}
```



### 9.5 函数类型(***)

> 规定函数的参数和返回值类型，和后面接口类似
>
> 函数类型本生是一个指针

格式一：
```
func  test(a int, b int )  (sum int) {
    fmt.Println("this is a demo of func type")
    return a + b
}

type FUNCType func(a int, b int) int

var f FUNCType
f = test
v := f(10,20)
fmt.Println(v)
```
格式二：自动推导

```
func  test(a int, b int )  (sum int){
    fmt.Println("this is a demo of func type")
    return a + b
}

f:= test
v := f(10,20)
fmt.Println(v)
```



格式三： 简化版

```
func  test(a int, b int )  (sum int){
    fmt.Println("this is a demo of func type")
    return a + b
}

var f fun(int, int) int
f = test
v := f(10,20)
fmt.Println(v)
```





### 9.6 匿名函数与闭包

匿名函数

格式一：
```
f : = func(a int , b int ) int{
    return a + b
}

f(10, 20)
```

格式二：

```
f : = func(a int, b int) int{
    return a + b
}(10, 20)

fmt.Println(f)  // 此时f是整形, 因为通过自动推导，拿到的是匿名函数的返回值
```

格式三：

```
{
    // pass  无参， 无返回值
}
```





闭包
> 可以实现函数在栈区的本地化操作(持久化操作)，它不关心这些捕获了的变量和常量是否已经超出了作用域，所以只有闭包还在使用它，这些变量就还会存在。
>
> 还是很容易写错的

```
func Test() func() int{
    var a int
    
    return func() int {
        a++
        return a
    } 
}
f := test()
fmt.Println(f())       # 1
fmt.Println(f())       # 2
fmt.Println(f())       # 3
fmt.Println(f())       # 4
fmt.Println(test()())  # 1
fmt.Println(test()())  # 2
fmt.Println(test()())  # 3
```



### 9.7 defer

> 延迟执行， 注意和匿名函数结合时的参数传递

```
package main

import "fmt"

func main() {
	a := 10
	b := 20
	//defer func() {
	//	fmt.Println("a:", a)
	//	fmt.Println("b:", b)
	//}()

	// 注意下面已经完成了参数的传递
	defer func(a int, b int) {
		fmt.Println("a1:", a)
		fmt.Println("b1:", b)
	}(a, b)
	a = 100
	b = 200

	fmt.Println("a:", a)
	fmt.Println("b:", b)
}
```



### 9.8 递归

```
package main

import "fmt"


func fib(a int) int {
	if a == 1 {
		return 1
	}
	return a * fib(a-1)
}

func main04() {
	fmt.Println(fib(5)) // 1*2*3*4*5
}
```




## 10. 工程管理

```
为了更好的管理项目中的文件，要求将文件都要放在相应的文件夹中。GO语言规定如下的文件夹如下：
（1）src目录：用于以代码包的形式组织并保存Go源码文件。（比如：.go .c .h .s等）
（2）pkg目录：用于存放经由go install命令构建安装后的代码包（包含Go库源码文件，.a存档文件），编译生成的包/库   
（3）bin目录：与pkg目录类似，在通过go install命令完成安装后，保存编译生成的可执行文件

```


```
同一目录:
   全局变量，方法  在src同级目录下可以直接使用

不同目录：
   func Xxx(){}  // 首字母大写, 对外提供需要


运行：
运行方式一：命令行中  切换到具体的代码目录  go run a.go b.go  或者 go run .
运行方式二：goland中  把Run kind 改为 Directory, 并直接运行，不要在具体文件中运行


e.g:
//demo5.go
package main

import "fmt"

func OutterGoPath() {
	fmt.Println("this is a test for outter go path  ")
}



// demo7.go
package inner

import "fmt"

func Inner_go_path() {
	fmt.Println("this is a test for inner go path  ")
}


//demo6.go  和 demo5.go 在同一目录
package main

import (
	"step1/D04/inner"
)

func main06() {
	OutterGoPath()
	inner.Inner_go_path()
}
```

gopath

```
配置环境变量(配置国内加速)
go env  -w  xxxx
```

import

```
// 推荐使用， 效率高
import (
    "fmt"
    "userinfo"
    "product"
)
```



## 11. 数组
定义：

```
所谓的数组：是指一系列同一数据类型的集合。

eg:
var a [10]int = [10]int{1,2,3}

arr := [10]int{1,2,3}

arr := [...]int{1, 2, 3, 4, 5}

eg:  
错误：
var a [...]int = [...]int{1,2,3}

正确
arr := [...]int{1,2,3}
```

遍历:

```
arr := [...]int{1,2,3}
方式一：
for i:=1 ; len(arr); i++ {
    fmt.Println(i)
}

方式二：_ 所在的位置是索引
for _ , data := range arr {
    fmt.Println(i)
}

```

数组排序：
```
最值

数组置换，反转

冒泡排序
```

数值作为函数参数和返回值：
>数组作为参数传递是值传递

```
e.g1:
func test(arr [10]int)  [10]int {
    // pass 
    return 
}
arr := [10]int{}
result = test(arr)

fmt.Println(result)


e.g2:
// 形参长度和实参的要一致
func test(arr [10]int) {
	fmt.Println(arr)
	fmt.Printf("%T\n", arr)
}
func main() {
	arr := [...]int{9, 1, 5, 6, 7, 3, 10, 2, 4, 8}
	test(arr)
}
```


随机数:

```
import (
"math/rand"
"time"
)

rand.Seed(time.Now().UnixNano()）

rand.Intn(123)
```

二维数组：
```
arr :=[3][4]int{{1,2,3},{2,3,4},{3,4,5}}
```



## 12. 切片

> 动态数组
> 切片长度可变
> 切片名本生就是地址
>
> 切片中数据类型一致,  make 中声明的时候就指定了类型
> 每次扩容，如果没有超过1024， 容量变为原来的2倍，超过了，每次增加1/4
> 切片存储在堆区


### 12.1 定义

```
// 格式一
var 切片名 []数据类型

// 格式二
s := make([]int, 5) 
s[0] =1
...
s[4] =5
//长度为5，只能初始化为5个

// 通过append 来添加新的数据
s = append(s, 6, 7, 8)

// 格式三：
var s []int = []int{1,2,3,4,5}


//遍历：
for index, v := range s{
    // pass
}

// 内存分配分析
//len(s) 使用长度
//cap(s) 整体的容量大小, 切片打印时只能打印有效长度的数据


没有超过1024, 每次扩展为上次的一倍，超过了，为1/4
```

### 12.2 切片的截取

```
eg1： // 包含起始下标，不包含结束
s:= []int{1,2,3,4,5}
slice:= s[2:]
// slice:= s[:2]
// slice:= s[2:5]
// slice:= s[0:2:5]   // 起始, 结束, 容量(大于等于len，小于等于caps)
fmt.Println(slice)


eg2: 切片截取的数据发生改变, 原始的切片数据也会发生改变, 因为切片名本生就是地址
s:=[]int{1,2,3,4,5}
slice:= s[0:2]
slice[1] = 123

fmt.Println(slice)  // [1,123]
fmt.Println(s)      // [1,123,3,4,5]
```



### 12.3 切片的追加和拷贝

```
切片存储在堆区

拷贝后是两个独立的空间，不会影响原有的数据

eg: copy
s1:=[]int{1,2,3,4,5}
s2:=make([]int,5)    //容量怎么定,只要有容量就行，但是决定后面拷贝最多能包含的容量上限

copy(s2, s1[1:])
fmt.Println(s2)

tips:
    append 切片首地址可能发生改变，如果容量扩充导致输出存储溢出，切片会指定寻找新的空间存储数据
```

### 12.4 切片作为函数参数，返回值

> 注意点： 传递的是地址，但最后结果却没有改变

```
// 切片作为参数传递是地址传递， 数组是值传递
// 栈中保存堆区的地址，   堆中才存放的是数据

func test(s []int) []int{
    s = append(s, 1, 2, 3)
    return s
}

func test1(s []int){
    s = append(s, 1, 2, 3)
}

func main(){
    s:=[]int{1,2,3,4,5}
    test(s)   // append首地址发生变化，开启新的空间，存放数据，使用完成后，释放; 
                 添加返回值，结果变成[1,2,3,4,5,1,2,3]
                 
    test1(s)  // [1,2,3,4,5]
}

```

## 13. map
> key:value 结构   key不能重复, 是基本数据类型
> 无序
> 自动扩容
> 访问或者删除不存在的元素，不会报错
> 作为参数传递是地址传递，内部做修改会更改map本身的值

```
map["name"] = "dh"
map[1] = "zhangshan"
```



### 13.1 定义及遍历

```
// map中的长度是自动扩容的, 数据是无序存储的
// 底层数据结构是树
m:= map[int]string{}

m:= make(map[int]string, 5)
	m[0] = "1"
    m[2] = "2"
    m[4] = "5"
    
m:= map[string]int{"k1":1, "k2":2, "k3":3}


// 遍历，只能通过该方式
for k, v := range m{
    fmt.Println(k)
    fmt.Println(v)
}

// ok 条件判断
value, ok := m[6]
if ok {
    fmt.Println()
} else {
    fmt.Println()
}

```

### 13.2 元素的删除

```
m:=map[int]string{101:"刘备", 105;"关羽"}
delete(m, 101)				 // 101 是key
delete(m, 101)                // 删除或者访问不存在的元素是不会报错的
fmt.Println(m)
```



### 13.3 map作为函数参数(***)

```
map作为参数传递是地址传递, 在函数内部更改数据会更改map本身的值 (跟切片不同，切片也是地址传递, 但是内容不会更改)

可以使用len(),  不可以使用caps

e.g.:

    package main

    import "fmt"
    
    func testMapFunc(m map[int]string) {
    	m[102] = "杨二郎"
    	m[103] = "唐老二"
    	fmt.Println(m)
    	delete(m, 102)
    	fmt.Println(m)
    }
    
    func main() {
    	m := make(map[int]string, 5)
    	m[101] = "孙悟空"
    	fmt.Println(len(m))
    	testMapFunc(m)
    	fmt.Println(m)
    }
```



### 13.4 指针作为函数参数

```
func Swap(a *int ,b *int){
    temp := *a
    *a = *b
    *b = temp
}

func main(){
    a := 10
    b := 20
    Swap(&a, &b)
    fmt.Println(a)
    fmt.Println(b)
    
}
```



## 14. 结构体(***)

> 可以存储不同的数据类型,  类似class,  但是不能在内部定义函数, 需要后续再单独定义方法

### 14.1 定义和使用

```
package main

import "fmt"

type student struct {
	id   int
	name string
	age  int
	addr string
}

func main() {
	// 方式一：
	//var s student = student{id: 1, name: "zhanshan", age: 18, addr: "beijing"}
	//fmt.Println(s)

	// 方式二：
	//var s student
	//s.id = 1
	//s.name = "zhanshan"
	//s.age = 18
	//s.addr = "beijing"
	//fmt.Println(s)

	// 方式三：
	s := student{id: 1, name: "zhanshan", age: 18, addr: "beijing"}
	fmt.Println(s)
}
```

### 14.2 赋值和比较

```
// 赋值
s:= Student{ age:30, id:101 }
// 更改后原有数据不改变, 对原有数据的拷贝
s1:= s
s1.age = 22

// 比较
==  两个结构体的判断


e.g:
package main

import "fmt"

type students struct {
	id   int
	name string
	age  int
	addr string
}

func main() {
	s := students{id: 1, name: "zhansan", age: 18, addr: "beijing"}
	// 结构体拷贝, 是独立的空间， 更改新的值，原有的结构体不会发生改变
	s1 := s
	s1.addr = "wuhan"
	fmt.Println(s1)
	fmt.Println(s)

	if s == s1 {
		fmt.Println("s1 和 s 是一样的")
	}

}
```

### 14.3 结构体数组和切片
结构体数组
```
type Student struct {
    id int
    name string
    age int
    address string
    gender bool
}

var arr [5]Student 
arr[0].id = 101

// 结构体数组中的数据/整体 可以相互交换

for k, v := range arr{
    // v 是一个结构体
}


e.g:
package main

import (
	"fmt"
)

type student03 struct {
	id    int
	name  string
	sex   string
	age   int
	score int
	addr  string
}

func main() {
	// 结构体数组
	var s [3]student03
	s[0] = student03{101, "zhanshan", "nan", 18, 80, "bj"}
	s[1] = student03{102, "zhanshan", "nan", 28, 70, "bj"}
	s[2] = student03{103, "zhanshan", "nan", 8, 90, "bj"}

	for k, v := range s {
		fmt.Println(k, v)
	}

	// 根据年龄排序(冒泡排序)
	for i := 0; i < len(s); i++ {
		for j := 0; j < len(s)-1-i; j++ {
			if s[j].age > s[j+1].age {
				s[j], s[j+1] = s[j+1], s[j]
			}
		}
	}
	fmt.Println(s)
}
```



结构体切片

```
arr := []Student{
    {101,"dh1"},
    {102,"dh2"}
}

arr = append(arr, Student{103,"dh3", ...})

e.g：
package main

import (
	"fmt"
)

type student03 struct {
	id    int
	name  string
	sex   string
	age   int
	score int
	addr  string
}

func main() {
	// 结构体切片
	s1 := make([]student03, 3)
	//s1 = append(s1,
	//	student03{101, "zhanshan", "nan", 18, 80, "bj"},
	//	student03{102, "zhanshan", "nan", 28, 70, "bj"},
	//	student03{103, "zhanshan", "nan", 8, 90, "bj"})

	s1[0] = student03{101, "zhanshan", "nan", 18, 80, "bj"}
	s1[1] = student03{102, "zhanshan", "nan", 28, 70, "bj"}
	s1[2] = student03{103, "zhanshan", "nan", 8, 90, "bj"}

	// 遍历
	for k, v := range s1 {
		// fmt.Printf("%T\n", v)
		fmt.Println(k, v)
	}
}

```

### 14.4 结构体作为map中的value

```
type Student struct{
    name string
    age int
    address string
    gender bool
}

//eg1: value是单个结构体，单条信息
m := make(map[int]Student)
m[101] = Student(101,"dh1")


//eg2: value是多个结构体(切片), 多条信息
m:= make(map[int][]Student)
m[101] = append(m[101], Student(101,"dh1"), Student(102,"dh2"))

for k, v := range m{
    for i, data := range v {
        fmt.Println(i, data)
    }
}


e.g:
package main

import "fmt"

type student04 struct {
	name  string
	age   int
	score int
}

func main() {
	// map 中value是单个结构体
	m := make(map[int]student04)
	m[101] = student04{"周瑜", 28, 101}
	m[102] = student04{"孙策", 32, 78}

	for k, v := range m {
		fmt.Println(k, v)
	}

	// map 中value是多个结构体，遍历
	m1 := make(map[int][]student04)
	m1[101] = append(m1[101], student04{"曹操", 50, 88}, student04{"张辽", 38, 98}, student04{})
	m1[102] = append(m1[102], student04{"刘备", 50, 88}, student04{"张飞", 38, 98})
	m1[103] = append(m1[103], student04{"孙权", 50, 88}, student04{"甘宁", 38, 98}, student04{"太史慈", 38, 98})

	for k, v := range m1 {
		for i, data := range v {
			if data.age >= 50 {
				fmt.Println(k, i, data)
			}

		}
	}
}

```

### 14.5 结构体作函数参数和返回值
> 结构体           作为参数是   值传递
> 结构体切片    作为参数是  地址传递
> 结构体数组    作为参数是  值传递

```
package main

import "fmt"

type person struct {
	id    int
	name  string
	score int
	sex   string
}

func test1Struct(p person) {
	p.name = "曹操"
}

func test2Struct(p [2]person) {
	p[0].name = "曹操"
	p[1].name = "曹操1"
}

func test3Struct(p []person) {
	p[0].name = "曹操"
	p[1].name = "曹操1"
}

func main() {
	// 结构体作为函数参数, 值传递
	p := person{101, "宋江", 9, "男"}
	test1Struct(p)
	fmt.Println(p)
	// 结构体数组作为函数参数, 值传递，不会变
	p1 := [2]person{{101, "宋江", 9, "男"}, {102, "宋江1", 9, "男"}}
	test2Struct(p1)
	fmt.Println(p1)
	// 结构体切片作为函数参数，地址传递，会变
	p2 := []person{{101, "宋江", 9, "男"}, {102, "宋江1", 9, "男"}}
	test3Struct(p2)
	fmt.Println(p2)
}
```



### 14.6 实际应用场景

```
可以实现类似数据库实体类之间的关联关系，这是map实现不了的

type skills struct {
    xxx
    xxx
    xxx
}

type role struct {
    xxx
    xxx
    xxx
    // skills
    // []skills 
}
```



## 15. 指针(难点)

### 15.1 定义和使用
```
// 格式一
var a int = 10
var p *int
p = &a

fmt.Println(*p) // 10
fmt.Println(p)  // 打印地址信息
fmt.Println(&a) // 打印地址信息
fmt.Println(a)  // 10



// 更改变量的值
*p = 100
fmt.Println(a)    // 100
fmt.Println(*p)   // 100   通过指针修改变量的值


// 格式二: 自动推导
a:= 10
p:= &a

// 错误方式
var p *int        // 空指针，不能直接赋值操作
*p = 123         //  panic, 空指针，(0-255为系统占用, 不允许使用)
fmt.Println(*p)   


e.g:
package main

import "fmt"

func main() {
	// 指针基本定义
	var a int = 5
	var p *int
	p = &a
	fmt.Println(p)
	fmt.Println(a)
	fmt.Println(*p)

	*p = 123
	fmt.Println(p)
	fmt.Println(a)
	fmt.Println(*p)

	// 自动推导指针
	p1 := &a
	fmt.Println(p1)
	fmt.Println(*p1)

	// 空指针
	// 申明指针的时候，如果没有指向某个变量，默认值为nil, 指向了内存地址为 0 的空间, 0-255为系统占用，会报错
	var p2 *int
	//*p2 = 123      // panic   nil pointer
	//*p2 = 300
	fmt.Println(*p2)
}
```
> 申明指针的时候，如果没有指向某个变量，默认值为nil, 指向了内存地址为 0 的空间, 0-255为系统占用，会报错



### 15.2 创建指针空间

```
var p *int

// 为指针变量创建一块内存空间，堆区创建空间，new创建的空间值为数据类型的默认值(比如 为int, 默认为0)
// new 返回的是有默认值的指针
p = new(int)  

fmt.Println(*p)   // 0


e.g:
package main

import "fmt"

func main() {
	//var a int
	//var p *int     //nil
	//fmt.Println(*p)  // 0
	//p = &a
	// fmt.Println(*p)
	 // new 返回的是有默认值的指针, 为数据类型的默认值： int --- 0
	p := new(int)
	//fmt.Println(a)
	fmt.Println(*p)
}
```


### 15.3 指针作为函数参数

```
func swap(a *int, b *int) {
	*a, *b = *b, *a
}

func main() {
	a := 1
	b := 2
	swap(&a, &b)
	fmt.Println(a)
	fmt.Println(b)
}

```


### 15.3 数组指针
> 指向数组的指针
> p[1]       ok   
>
> (*p)[1]  ok 
>
> *p[0]     error

```
// 方式一：
var arr [5]int = [5]int{1,2,3,4,5}
// 和上面的元素个数要求一样
var  p *[5]int
p = &arr

// 方式二： 自动推导 
p:= &arr  

fmt.Println(p)         // 地址
fmt.Println(*p)
fmt.Println(arr)
fmt.Println(*p[0])     // error 
fmt.Println((*p)[0])   // 等于   fmt.Println(p[0])   等于fmt.Println(&arr[0])
fmt.Println(p[0])

// 遍历
// len(p)  可以获取到元素的个数
for i :=0; i< len(p); i++ {
    fmt.Println(p[i])
}
```

### 15.4 切片指针
> 指向切片的指针
> p[1]      error    
>
> (*p)[1]  ok 

定义及使用
```
var slice []int = []int{1,2,3,4,5}  
p := &slice            
fmt.Println(p)      // 0xffee
fmt.Println(slice)  // 0xff00  切片名本生就是一个地址，上面和下面的地址可能不一样，一个是栈区，一个是堆区
fmt.Println(*p)     // 0xff00  p是一个二级指针


// 更改某个索引的值
(*p)[1] = 200
fmt.Println(*p)
fmt.Println(slice)     // 上面和下面的值都发生改变

fmt.Println(p[1])      // error
fmt.Println((*p)[1]) 

// 添加新的值
*p = append(*p, 6, 7, 8, 9, 10) 
```



切片指针作为函数参数，切片指针是地址传递，会改变原有的数据结构

```
// 切片指针作为函数参数
func Test(s *[]int) {
    *s = append(*s, 1,2,3)
}

func main() {
    s:= []int{1,2,3}
    // p:= &s
    // 切片指针是传地址 
    // Test(p)  
    Test(&s)
    fmt.Println(s)   // {1,2,3,1,2,3}
}
```


通过new创建切片指针
```
// var p *[]int     // 该行都可以省略
p = new([]int)      // 等价于 p = new(*[]int)
*p = append(*p, 1, 2, 3)
fmt.Println(*p)
```



### 15.5 指针数组，指针切片

指针数组(多个指针存在一个数组中)
```
var arr [3]*int
a:= 10
b:= 20
c:= 30

arr[0] = &a   // arr[i] 中存的是地址
arr[1] = &b  
arr[2] = &c 


e.g:
package main

import "fmt"

func main() {
	// 定义指针数组，打印
	var arr [3]*int
	a := 10
	b := 20
	c := 30
	arr[0] = &a
	arr[1] = &b
	arr[2] = &c

	fmt.Println(*arr[1])
	fmt.Println(arr[1])
	fmt.Println(len(arr))

	// 更改指针数组的值
	*arr[1] = 11
	fmt.Println(*arr[1])
	// 遍历
	//for i := 0; i < len(arr); i++ {
	//	fmt.Println(*arr[i])
	//}

	for idx, data := range arr {
		fmt.Println(idx, *data)
	}
}

```

指针切片

```
var arr []*int
a:= 10
b:= 20
c:= 30

arr= append(arr, &a, &b, &c)
```



### 15.6 结构体指针，结构体切片指针

结构体指针
```
type Student struct{
   
}

var s Student = Student{}
p:= &s

p.name = ""
p.age  = 18 

fmt.Println()
```



结构体切片指针

```
type Student struct{
    
}

stu := make([]Student)
p:= &stu

// 注意赋值方式 (*p)[0]
(*p)[0] = Student{101, "dh"}
*p = append(*p,  Student{101,"dh2"} ,  Student{102,"dh2"})


e.g:
package main

import "fmt"

type Student struct {
	name string
	id   int
	age  int
	sex  string
}

func main() {
	// 结构体指针，打印
	var stu Student = Student{id: 101, name: "多啦A梦", age: 100, sex: "男"}
	p := &stu
	fmt.Printf("%p\n", p)
	fmt.Printf("%p\n", &stu)
	fmt.Println(stu)
	fmt.Println((*p).name)
	fmt.Println(p.name)
	fmt.Println(&stu.name)
	fmt.Println(&stu.id)

	// 更改其中的值
	p.name = "多啦A梦1"
	fmt.Println(stu)

	// 结构体切片指针，赋值，append, 遍历
	var stu1 []Student = make([]Student, 3)
	p1 := &stu1
	(*p1)[0] = Student{"小猪佩奇", 1, 10, "女"}
	(*p1)[1] = Student{"小猪佩奇2", 2, 30, "女"}
	(*p1)[2] = Student{"小猪佩奇2", 3, 20, "女"}

	*p1 = append(*p1, Student{"小猪佩奇", 4, 40, "女"})

	fmt.Println(*p1)
	fmt.Println(stu1)

	for idx, data := range *p1 {
		fmt.Println(data)
		fmt.Println((*p1)[idx])
	}

}

```



### 15.7 多级指针

```
func main(){
    a := 10
    p := &a   //*int
    pp :=&p   //**int
    
    fmt.Printf("%T\n", a)  // int 
    fmt.Printf("%T\n", p)  // *int 
    fmt.Printf("%T\n", pp)  // **int 
    
    // 一级指针的地址
    fmt.Println(*pp)   // 地址   
    fmt.Println(p)     // 地址
    fmt.Println(&a)    // 地址
    
    
    // 变量 a 的值
    fmt.Println(**pp)
    fmt.Println(*p)
    fmt.Println(a)
}

```

### 15.8 内存模型
```
0-255 ： 系统占用
代码区： 存放计算机指令信息，只读
数据区： 常量区(const,常量区是不能显示内存地址的)，初始化区(全局变量)，未初始化区(结构体)
堆    ： 大块的内存区域, 分为：切片数据, new(), string的值
栈    ： 相对高区，      分为：切片地址，局部变量，函数信息
注册表： 最高地址段
```



## 16. 继承
> go中是没有继承的，通过匿名字段 (结构体名称作为另一个结构体字段) 来实现

### 16.1 匿名字段
```
type Person struct{
    name string
    age int
    sex string
}

type Student struct{
    Person         // 结构体名称作为另一个结构体字段
    id int
    score int
}

func main(){
    // 初始化方式一
    // var s Student = Student{person{}, id:101, score:100}
      
    // 初始化方式二
    var s Student
    s.id = 101
    s.score = 100
    //s.person.name = "dh"     // go 内部有优化
    s.name = "dh"
    s.age = 18
    s.sex = "男"
  
    fmt.Println(s)
}
```

### 16.2 同名字段

```
type person struct{
    name string
    age int
    sex string
}

type Student struct{
    person        // 结构体名称作为另一个结构体字段
    id int
    score int
    name string  //  就近原则，使用的子类的数据
}

// 初始化父类
s.person.name = "张三疯"

// 初始化子类
s.name = "张三疯之子"

```



### 16.3 指针匿名字段

> 为什么需要？？？ 直接用匿名字段不行么？？？  目的：可以嵌套自身，看下面多重继承 

```
type person struct{
    name string
    age int
    sex string
}

type Student struct{
    *person 
    id int
    score int
}

func main(){
    var stu Student
    stu.person = new(person)
    // 或者
    // var per Person = Person{}
    // stu.person = &per
    
    // 或者
    // var stu Student = Student{&person{}, 103, 80}

    stu.name = "郭襄"
    stu.person.name = "guoxiaojie"
}

```


### 16.4 多重继承

```
结构体内部不能嵌套本结构体(无限递归，内存无法确定大小), 可以嵌套本结构体指针类型(链表), 可以嵌套其他结构体

type TestA struct {
	name string
	id int
}
type TestB struct {
	TestA
	sex string
	age int
}
//注意结构体不能嵌套本结构体
//结构体可以嵌套本结构体指针类型  链表
type TestC struct {
    // TestC   err
	*TestC  ok
	TestB
	score int
}


应用场景：
     /*
        type skills struct{
        	名称
        	耗蓝
        	CD 冷却时间
        	范围
        	伤害
        }
        
        type role struct{
        
        	名称
        	等级 lv
        	经验 exp
        	钻石
        	金币
        	生命值 hp
        	攻击力
        	暴击
        	防御
        	蓝量mp
        	skills      //匿名字段
        	s []skills  //匿名字段期别名，结构体切片(多个匿名字段)
        }
     */
        
        
     /*
        type 信用卡 struct{
        	卡号
        	持卡人姓名
        	额度
        	有效期
        	密码
        	银行信息
        	消费记录         // 匿名字段
        	记录 []消费记录  // 结构体切片
        }
        
        type 消费记录 struct{
        	卡号
        	消费时间
        	消费id
        	流水号
        	消费金额
        	备注
        }
     */
     
Q: 结构体中定义匿名字段和 结构体切片的区别在哪里，适用场景有什么不同 ？
A: 结构体切片: 多个匿名字段
```



## 17. 方法(封装)

> 跟函数不是一个概念

疑问： 这不是搞麻烦了？？？
目的： 给指定结构体绑定方法


### 17.1 方法的定义和使用
> 方法的接收者 和 返回值不是一个概念， 方法的接收者更像是方法的所属，调用者,  要绑定的对象
> 方法是全局的，允许程序在所有的地方使用
> 方法可以和函数名同名

```
// eg1:
type Int int

// （方法接受者）方法名(参数列表) 返回值类型
//  方法的接收者 和返回值不是一个概念, 方法的接收者更像是方法的所属, 调用者, 绑定的对象
func (a Int) add(b Int) Int {
    return a + b
}

func main() {
    var a Int = 10
    value:= a.add(20)
    fmt.Println(value)
}


//eg2:  给结构体绑定方法(重点)
type Stu struct{
    name string
    age int
    sex string
}

func (s Stu) PrintInfo() {
    fmt.Println(s.name)
}

func main() {
    var s Stu = Stu{"dh","18","nan"}
    s.PrintInfo()
}


//eg3: 通过方法(指针)可以更改结构体数据
type Stu struct{
    name string
    age int
    sex string
}

func (s Stu)PrintInfo(){
    fmt.Println(s.name)
}

func (s *Stu)EditInfo(name string, age int, sex string){
    s.name = name
    s.age = age
    s.sex = sex
    // 方法内部可以调用其他的方法
    //s.PrintInfo()
}

func main() {
    // 方式一
    var s Stu = Stu{"dh","18","nan"}
    //(&s).EditInfo()  //ok
    s.EditInfo()       //ok   go内部做了优化
    
    //方式二
    var s *Stu
    s = new(Stu)       // 指针要初始化空间， 否则会报空指针
    s.EditInfo()
    s.PrintInfo()
}

tips:
    平时定义方法的时候建议都加上*(方法的接收者带 * ), 需要更改数据的时候可以直接更改
    方法名可以和函数名重名，直接调用就好
```



### 17.2 方法的继承

```
type person struct{
    name string
    age int
    sex string
}

type student struct{
    person
    // p person
    // p []person
    score int
}

func (p *person) SayHello(){
    // pass 
}

func main(){
    var stu student = student{}
    stu.SayHello()              // 子类允许使用父类的方法
}
```


### 17.3 方法的重写
```
type person4 struct{
	name string
	age int
	sex string
}

type student4 struct {
	person4

	score int
}

func (p person4)PrintInfo(){
	fmt.Printf("大家好，我是%s，我今年%d岁，我是%s生\n",p.name,p.age,p.sex)
}

//方法重写  在一个对象中不能出现相同的方法名, 加* 也不行，方法的接收者 带* 和不带* 表示一个相同的对象
func (s student4)PrintInfo(){
	fmt.Printf("大家好，我是%s，我今年%d岁，我是%s生,我的分数是%d分\n",s.name,s.age,s.sex,s.score)
}

func main() {
	s:=student4{person4{"张三",11,"男"},19}
	
	//默认使用子类的方法  采用就进原则
	//调用子类方法
	s.PrintInfo()
	
	//调用父类方法
	s.person4.PrintInfo()
}

```

### 17.4 方法类型和方法值

```
type Stu struct{
    name string
    age int
    sex string
}

func (s Stu)PrintInfo(){
    fmt.Println(s.name)
}

var s Stu = Stu{...}
以下等价于 type funcDemo func() int 
f:= s.PrintInfo
f()   // f(可以传参数)   
```


## 18. 接口(重点)
> 接口中只有方法的申明,  没有实现， 具体实现通过方法，实现接口中定义的方法，即实现了该接口
> 接口是否是指针呢 ？？？ 传递的是地址

### 18.1 接口的定义和使用
```
type student struct{
    name string
    age int
    sex string
}

type person interface{
    // SayHi(int)  int    // 前一个int是参数的类型，后一个int 是返回值类型
     SayHi()  int
}

// 接口中方法的实现
func (stu *student) SayHi() int{
    fmt.Println("hello")
    return 1
}

func main(){
    var stu student = student{}
    var p person
    p = &stu
    等价于
    //var p person
    //p = &student{...}
    等价于 
    // p:=&student{...}
    
    // 调用实现的接口中的方法
    p.SayHi()   
    // stu.SayHi()  可否
}

```

### 18.2 多态（重点）
> 跟18.1 的区别在哪里？？？
> 多态是将接口类型作为函数参数
> 多态实现了接口的同一处理
> 多态类似于工厂模式， 通过传入的子父类的不同，调用同一方法，实现不同操作

定义
```
type person struct{
    name string
    age int
    sex string
}

type student struct{
    person
    score
}

type teacher struct{
    person
    subject
}

// 接口定义
type Personer interface{
    SayHi()
}

// 接口实现
func (stu *student) SayHi() {
    fmt.Println("hello student")
}
// 接口实现
func (tea *teacher) SayHi() {
    fmt.Println("hello teacher")

}

// 多态实现
// 多态实现了接口的统一处理
func SayHi(p Personer){
    p.SayHi()
}


func main(){
    var p Personer
    
    var s Student = Student{}
    // p = &student{}
    p = &s
    
    //var t teacher = Teacher{}
    //p = &t
    
    SayHi(p)
    
}
    
```



### 18.3 接口继承和转换 （难点）

> 接口转换的时候， 超集转子集
> 接口转换可以用来判断类型(类型断言)，一个接口可以转换为另一个接口，一个接口可以转换为其他类型

http://c.biancheng.net/view/83.html
https://segmentfault.com/a/1190000022255009

``` 
package main

import "fmt"

type student3 struct {
	name string
	age  int
	sex  string
}

type Humaner2 interface {
	SayHi()
}

type Personer2 interface {
	Humaner2
	Sing()
}

func (s *student3) SayHi() {
	fmt.Println(" i am sayhi")
}

func (s *student3) Sing() {
	fmt.Println("i am sing")
}

func main03() {
	var h Humaner2
	var p Personer2

	var s student3 = student3{"dh1", 18, "nan"}
	h = &s
	h.SayHi()

	p = &s
	p.SayHi()
	p.Sing()

	// 接口转换  大转小
	h = p
	p.Sing()
	p.SayHi()

}

```

### 18.4 空接口
> 可以接受任意数据类型，万能指针
> 空接口切片 类似于python 中的list， 什么数据类型的都可以往里面扔

```
// 空接口, 万能指针
var i interface{}  
// 指向 整数
i = 10
fmt.Printf("%T\n", i)
fmt.Println(i)

// 指向数组
var arr [4]int = [4]int{1,2,3,4}
i = arr 

//空接口切片   类似于 python中的 list 什么数据类型的都可以往里面扔 ****
var i []interface{}
i = append(i,  1,  2,  "hello",  "你瞅啥", [3]int{1, 2, 3})

for idx, v := range i {
	fmt.Println(idx, v)
}

```


### 18.5 类型断言

```
arr := make([]interface{}, 3)
arr[0] = 123
arr[1] = 3.1415

for i, v := range arr{
    // 格式一
    // v.(int) 是类型断言，  类似python 中的 isinstance()
    data,  ok:= v.(int)     
    if ok {
        //pass 
    }
    
    //格式二
    if data, ok := v.(int); ok{
        //pass
    }else if data, ok := v.(float64); ok{
        //pass 
    }
    
}
```

### 18.5 面向对象实例(重点)
```
package main

import "fmt"

type Shuzi struct {
	num1 int
	num2 int
}

type JiafaLei struct {
	Shuzi
}

type JianfaLei struct {
	Shuzi
}

// 接口
type SuanShu interface {
	Operate() int
}

// 接口实现方法
func (j *JiafaLei) Operate() int {
	return j.num1 + j.num2
}

func (j *JianfaLei) Operate() int {
	return j.num1 - j.num2
}

// 多态
func Jisuan(suanshu SuanShu) int {
	value := suanshu.Operate()
	return value
}

// 工厂模式
type gongchang struct {
}

func (g *gongchang) Factory(num1 int, num2 int, ops string) (result int) {
	var suanshu SuanShu
	switch ops {
	case "+":
		var jiafa JiafaLei = JiafaLei{Shuzi{num1, num2}}
		suanshu = &jiafa
	case "-":
		var jianfa JianfaLei = JianfaLei{Shuzi{num1, num2}}
		suanshu = &jianfa
	}

	//suanshu.Operate()
	s := Jisuan(suanshu)
	return s
}

func main() {
	var g gongchang
	result := g.Factory(10, 20, "+")
	result1 := g.Factory(10, 20, "-")
	fmt.Println(result)
	fmt.Println(result1)

}
```



## 19. 异常
errors
> 一般性的错误

```
import "errors"

func test()(err error) {
    err = errors.New("xxxxx")
    return
}


func main() {
    value, err := test()
    if err != nil {
        // pass 
    }
}
```


panic
> 让程序崩溃的信息

```
// 返回的让程序崩溃的信息
panic("hello world")  // 直接终止执行

// 以下两个是对错误进行处理的，不建议在程序中打印的时候使用
print
println 

```


defer 延迟加载

```
func main(){
    fmt.Println("333333333333")
    defer fmt.Println("1111111")  
    defer fmt.Println("2222222")  
    fmt.Println("444444444")
}

333333333333
444444444
2222222
1111111

/*
defer 调用的函数并没有直接调用， 而是先加载到栈区内存中， 在函数结束的时候，从后向前运行

*/
e.g.:

a:=10
b:=20

defer func (){
    fmt.Println(a)
    fmt.Println(b)
}()  //100,200


defer func(a int, b int) {
    fmt.Println(a)
    fmt.Println(b)
}(a,b) //10, 20

a = 100
b = 200

fmt.Println(a)
fmt.Println(b)


/*
100
200
10
20
100
200
*/

```


recover  
> 拦截运行时， 只在defer中调用才有效, 可以从panic中获取控制权，有多个异常时只能捕获第一个

```
// 在错误出现前拦截，才可继续往下运行，有多个异常的时候只能捕获第一
// 以下代码放在最前面， 先将代码加载到内存中，才能在出现错误时拦截

package main

import "fmt"

func main() {
	// 写一defer 代码， 通过recover 获取 其中的错误， 代码中可以有多处错误
	defer func() {
		err := recover()
		if err != nil {
			fmt.Println(err)
		}
	}()

	var p *int
	*p = 123

	a := 10
	b := 0
	result := a / b
	fmt.Println(result)
}
```



## 20. 文件

### 20.1 文件的创建

```
import "os"
fp , err := os.Create("d:/a.txt")
if err != nil {
    // pass
}

defer fp.close()
```

### 20.2 文件的写入和读取
> go 一个中文占 3个字节

```
// 创建文件
import "os"
fp, err := os.Create("d:/a.txt")
if err != nil {
    // pass
}

// 关闭文件
defer fp.close()


// 写入操作
// 字符串可以和字符切片转换
str := "hello"
b:= []byte(str)
fp.Write(b)

//n,  _fp.WriteString("itcast")
// n 为长度
// fp.WriteAt([]bytes, offset)    // 会覆盖原有位置的内容


// 打开文件 & 获取光标的位置
// os.Open(0)      // open只有读的权限
// fp, err := os.OpenFile(filepath, mode, 权限)
// n = fp.Seek(offset, 0/1/2)     //将光标定位到某个位置， offset + 设定的位置， offset可以为负数


// 读取操作
b := make([]byte, 1024)
for {
    n, error = fp.Read(b)
    if error == io.EOF {
       break
    }
    fmt.Println(string(b[:n]))
}

// 缓冲区读
r := bufio.NewReader(fp)
for {
   data, err := r.ReadBytes("\n")
   if err == io.EOF {
       break
    }
   fmt.Println(string(data))
   //fmt.Println(data) // 打印的是ascii 
}

e.g1:
package main

import (
	"fmt"
	"os"
)

func main() {
	fp, err := os.Create("files.txt")
	if err != nil {
		fmt.Println("文件创建失败")
		return
	}
	defer fp.Close()

	//1. 写入英文，中文
	n, err := fp.WriteString("helloworld\r\n")
	fmt.Println(n)
	n1, err := fp.WriteString("美女\r\n")
	fmt.Println(n1)

	//2. 写入字符切片
	b := []byte{'h', 'e', 'l', 'l', 'o', 'g', 'o'}
	n2, err := fp.Write(b)
	fmt.Println(n2)

	str := "hello go go go "
	n3, err := fp.Write([]byte(str))
	fmt.Println(n3)

	//3. 打开文件，获取光标，在指定位置写入
	fp1, err := os.OpenFile("files.txt", os.O_RDWR, 666)
	result, err := fp1.Seek(0, 2)
	fmt.Println(result)

	at, err := fp1.WriteAt([]byte{'e', 'n', 'd'}, result)   // at 代表返回的是写入成功的字节数
	fmt.Println(at)
}

e.g2:
package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
)

func main() {
	fp, err := os.OpenFile("files.txt", os.O_RDWR, 666)
	if err != nil {
		return
	}

	defer fp.Close()

	//  方式一
	//b := make([]byte, 1024)
	//for {
	//	n, err := fp.Read(b)
	//	if err == io.EOF {
	//		break
	//	}
	//	fmt.Println(string(b[:n]))
	//}

	//方式二：
	reader := bufio.NewReader(fp)
	for {
		result, err := reader.ReadBytes('\n')
		if err == io.EOF {
			break
		}
		fmt.Println(string(result))
	}
}



总结：
    os.Create()
    os.Open()       // 只能读取
    os.OpenFile()   // 啥都能干
    
    fp.Write(b []byte)      先要os.Open()
    fp.writeFile()          fs.writeFile()也是对fs.write()方法的进一步封装
    fp.WriteString(s string)  writes the contents of string s rather than a slice of bytes.
    fp.Seek(offset, 0/1/2)
    fp.WriteAt([]bytes, offset)
    ioutils.writefile()
    
    b := make([]byte, 1024)
    fp.Read(b)
    bufio.NewReader().ReadBytes()
```



## 21. 字符串
### 21.1 常用方法
> strings 包

```
strings.Contains()
strings.Index()
strings.Repeat(str, count)  //将一个字符串重复count次

strings.Join()  
strings.Replace(s, old, new, n )  // 其中n是替换次数
strings.Split()  // 返回的是切片
strings.Trim(s string , curset string)  //将字符串首位包含curset的去掉,curset 就是规则，且没有前后区别   
    e.g.:
        trim := strings.Trim(" ====hell o===  ", "")
        //trim := strings.Trim(" ====hell o===  ", " ")
        //trim := strings.Trim(" ====hell o===  ", "=")
        //trim := strings.Trim(" ====hell o===  ", "= ")
        fmt.Println(trim)

strings.Fields(str)    // 去掉字符串中所有的空格，并按照空格分隔，返回slice



e.g:
package main

import (
	"fmt"
	"strings"
)

func main() {
	// contains
	contains := strings.Contains("helloworld", "rld")
	if contains {
		fmt.Println("包含")
	}

	// join
	a := []string{"hello", "world"}
	result := strings.Join(a, "---")
	fmt.Println(result)

	// index
	index := strings.Index("helloworld", "rld")
	fmt.Println(index)

	//repeat
	repeat := strings.Repeat("hello ", 3)
	fmt.Println(repeat)

	//replace
	replace := strings.Replace("hello", "l", "ll", 2)
	fmt.Println(replace)

	// split
	split := strings.Split("hello", "")
	fmt.Println(split)

	// trim  ???  将字符串首位包含curset 的去掉， curset 就是规则，且没有前后区别
	//trim := strings.Trim(" ====hell o===  ", "")
	//trim := strings.Trim(" ====hell o===  ", " ")
	//trim := strings.Trim(" ====hell o===  ", "=")
	trim := strings.Trim(" ====hell o===  ", "= ")
	fmt.Println(trim)

	// fields   按空格切， 返回切片
	fields := strings.Fields(" hell o  ")
	fmt.Println(fields)
}

```



### 21.2 字符串类型转换

> strconv包

```
//将其他类型转成字符串
strconv.FormatBool()
strconv.FormatInt(数据, 进制)
strconv.FormatFloat(数据，"f", 小数点位数，64/32（以float64或者float32处理）)

// 将字符串转成bool
strconv.ParseBool(数据)
// 将字符串转成int
strconv.ParseInt(数据)

// append   将其他类型转成字符串后，添加到现有的字节数组中
strconv.AppendBool()
strconv.AppendInt()
strconv.AppendFloat()
strconv.AppendQuote()  // 字符串

strconv.Itoa(i int)
strconv.Atoi(s string )



e.g:
// format
b := false
formatBool := strconv.FormatBool(b)
fmt.Printf("%T\n", formatBool)
fmt.Println(formatBool)
// parse
//parseInt, _ := strconv.ParseInt("123", 10, 0)
parseInt, _ := strconv.ParseInt("123", 10, 64)
fmt.Printf("%T\n", parseInt)
fmt.Println(parseInt)

// append 最终结果是一个字节切片 ， 作用是什么？
b1 := make([]byte, 0, 10)
//float := strconv.AppendFloat(b1, 1.234, 'f', 3, 64)
//fmt.Printf("%T\n", float)
//fmt.Println(float)

b1 = strconv.AppendBool(b1, false)
b1 = strconv.AppendInt(b1, 123, 10)
b1 = strconv.AppendFloat(b1, 1.234, 'f', 5, 64)
b1 = strconv.AppendQuote(b1, "hello")
fmt.Println(b1)
```



## todo

```
1. 指针匿名函数 和  匿名字段的区别 
	
2. 接口转换  转和没转没有区别
   https://blog.csdn.net/yjk13703623757/article/details/103094211
```

