## 01

### 1.  指针

```
内存布局:
	代码区 只读数据区(常量区) 初始化数据区 未初始化数据区  heap(存储的是new出来)  stack 

栈帧：用来给函数运行提供内存空间
	局部变量
	形参
	内存地址描述符
	
	栈顶指针
	栈基指针
	
空指针&野指针：
	go 语言中保留了指针，但是和c语言有不同
	1. 默认值nil
	2. & 和 *
	3. 不支持指针运算，不支持 ' -> ', 直接用'.' 访问目标成员
	
	空指针： 未被初始化的指针
		e.g:
			var p *int
			*p =123
	野指针： 被一片无效的地址空间初始化
		e.g:
			var p *int = 0xff00
	
new:  在堆上申请一片内存地址空间
	e.g.:  
		var p *int
		p = new(int)
		fmt.Printf("%q\n", *p)  //打印go语言格式的字符串
		

指针作为函数参数：
	nil 被回收
	new出来的地址在堆，其他地址在栈，不在一块空间，所以可以传地址(引用)
	
	指针传地址/引用   e.g.: 交换a, b的值   在A栈帧内部，修改b栈帧中的变量值
```

### 2. 切片

```
为什么用切片，不用数组：
	1. 数组的容量固定，不能自动扩展
	2. 数组是值传递，不方便修改值

切片不是数组或数组指针，底层操作数组内部元素(runtime/slice.go )

截取数组：
	arr := s[2:5]
	
切片的创建：
	var a []int = []int{}
	a:=[]int{}
	a:=make([]int, 长度，容量)
	a:=make([]int, 长度)  // 容量 == 长度
	
	注意： make 只能用于创建 slice, map, channel ， 返回一个有初始值的对象
	
append:
	s = append(s , 1)
	
	容量增长，1024以下，一倍，超过，1/4
	

空切片：
	a :=make([]string, 0) 
	a := data[:0]
	
copy:
	2个切片之间复制数据
	copy(dest, source)
```

### 3. map

```
字典， 映射  key-value
key： 唯一， 无序(不能是引用)

创建：
	var m map[int]string 
	
	m:=map[int]string{}
	
	m:=make(map[int]string)
	
	m:=make(map[int]string, 10)

	不能使用cap,  支持cap的有： array, slice, pointer, channel
	

初始化：
	1.定义的同时初始化
	2.m[1] ="hello"
	
遍历：
	for k,v:= range arr{
		
	}

判断map中key是否存在：
	if v, ok:= m[1]; ok{
		
	}
	
	
删除元素：
	delete(m, idx)
```



## 02

### 1. 结构体

```
结构体定义

结构体赋值

结构体比较：
	== 
	!=

结构体作为函数参数是 值传递。 结构体传参几乎不用，内存消耗大

结构体指针：
	var p *Person = &Person{}
	
结构体指针作为函数参数是 地址传递，使用频率高 
```



### 2. 字符串

```
split
splitN  // 按照空格

Fields 

hasPrefix
hasSuffix
```



### 3. 文件操作

```
打开
关闭
写入
读取

e.g: 文件拷贝
	buf := make([]byte, 1024) //切片缓冲区
	
    for {
        //从源文件读取内容，n为读取文件内容的长度
        n, err := srcFile.Read(buf)
        
        if err != nil && err != io.EOF {
            fmt.Println(err)
            break
        }

        if n == 0 {
            fmt.Println("文件处理完毕")
            break
        }
        
        //把读取的内容写入到目的文件
        dstFile.Write( buf[:n])
    }

```

### 4. 目录操作

```
OpenFile()
ReadDir()
Chdir()
Isdir()
Getwd()
```



## 03(***)

### 1. 并发和并行

```
并行：多核cpu
并发：多线程, cpu时间轮片

进程状态：
	初始态
	就绪态
	运行态
	挂起态
	终止态

孤儿进程

僵尸进程
```



### 2.  线程和进程

```
进程并发：

线程并发：
	lwp     轻量级进程， 最小的执行单位(进程是最小的资源分配单位)
	线程并发 没有共有的地址空间
	
生产线 --- 进程
工人  ---  线程
1条生产线 50个工人  单进程多线程
10条生产线 500个工人 多进程多线程

```



### 3. 32位和64位

```
2^32   4g
2^64   
```



### 4. 同步

```
线程同步
进程同步

定义：   同一时间访问同一资源，需要同步机制

互斥锁： 同一时刻，只能有一个线程持有该锁， 对读写都有效

读写锁： 写独占，读共享
```



### 5. 协程

```
协程：   coroutine, 也叫轻量级线程

go协程： goroutine 

Go语言标准库提供的所有系统调用操作（包括所有同步IO操作），都会出让CPU给其他goroutine。这让轻量级线程的切换管理不依赖于系统的线程和进程，也不需要依赖于CPU的核心数量, Go从语言层面就支持并行。并发程序的内存管理有时候是非常复杂的，而Go语言提供了自动垃圾回收机制。

Go语言为并发编程而内置的上层API基于 顺序通信进程模型CSP(communicating sequential processes), 这就意味着显式锁都是可以避免的，因为Go通过相对安全的通道发送和接受数据以实现同步，大大地简化了并发程序的编写。

Go语言中的并发程序主要使用两种手段来实现: goroutine 和 channel
```



### 6.  goroutine

#### 6.1 简介

```
	goroutine是Go并行设计的核心。 goroutine说到底其实就是协程，它比线程更小，十几个goroutine可能体现在底层就是五六个线程，Go语言内部帮你实现了这些goroutine之间的内存共享。执行goroutine只需极少的栈内存(大概是4~5KB)，当然会根据相应的数据伸缩。也正因为如此，可同时运行成千上万个并发任务。goroutine比thread更易用、更高效、更轻便. 一般情况下，一个普通计算机跑几十个线程就有点负载过大了，但是同样的机器却可以轻松地让成百上千个goroutine进行资源竞争。
```



#### 6.2 创建

```
// 只需在函数调⽤语句前添加 go 关键字，就可创建并发执⾏单元。开发⼈员无需了解任何执⾏细节，调度器会自动将其安排到合适的系统线程上执行	

package main

import (
	"fmt"
	"time"
)

func sing() {
	fmt.Println("i am singing")
}

func dance() {
	fmt.Println("i am dancing")
}

func main() {
	for {
		go sing()
		time.Sleep(time.Second * 1)
		go dance()
	}
}
```



#### 6.3 特性

> 主go程退出， 子go程退出

```
package main

import (
	"fmt"
	"time"
)

func test() {
	fmt.Println("i am test ")
}

func main() {
	go test()
	// fmt.Println(" i am main go ")   // 主go程执行完毕，子go程自动退出, 子go程还没有来得及执行已经退出
	for i := 0; i < 5; i++ {
		fmt.Println(" i am main go ") // 主go程执行完毕， 子go程自动退出
		time.Sleep(time.Second * 1)
	}
}
```



#### 6.4 runtime包

> 尽管 Go 编译器产生的是本地可执行代码，这些代码仍旧运行在 Go 的 runtime（这部分的代码可以在 runtime 包中找到）当中。这个 runtime 类似 Java 和 .NET 语言所用到的虚拟机，它负责管理包括内存分配、垃圾回收、栈处理、goroutine、channel、slice、map 和反射（reflection）等等。    
>
>  (性能调优)
>
> gosched
>
> goexit
>
> gomaxprocs

```
Gosched: 让出cpu时间片，让出当前的执行权限，下次当前go程再获取到cpu时间片，从当前的下一步开始执行

gosched与time区别： time后台启动的是定时器，后续恢复后，依然要竞争cpu时间轮片

        package main

        import (
            "fmt"
            "runtime"
        )

        func main() {
            // 创建一个goroutine
            go func(s string) {
                for i := 0; i < 2; i++ {
                    fmt.Println(s)
                }
            }("world")

            for i := 0; i < 2; i++ {
                runtime.Gosched()  
                /*
                    没有runtime.Gosched()运行结果如下：
                        hello
                        hello

                    有runtime.Gosched()运行结果如下：
                        world
                        world
                        hello
                        hello
                */
                fmt.Println("hello")
            }
        }


Goexit: 立即终止当前goroutine 
	return: 返回当前函数调用， return之前的defer有效
	goexit: 结束当前go程，     goexit之前的defer有效
	
	e.g:
	    package main

        import (
        "fmt"
        "runtime"
        )

        func main() {
            go func() {
                defer fmt.Println("aaaaa")
			   func(){
                    defer fmt.Println("ccccc")
                    runtime.Goexit()					// ccc, aaa 
                    //return                              // ccc, bbb, aaa
                    fmt.Println("dddddd")                 // 不会执行
				}
                fmt.Println("bbbbb") 
            }() 

            //死循环，目的不让 主goroutine 结束
            for {
            }
        }


GOMAXPROCS: 用来设置可以并行计算的CPU核数的最大值，并返回之前cpu的值. 能实现主go程和其他go程同时竞争执行，否则当cpu时间轮片时间到了，才会切换到其他go程

	e.g:
	    package main

        import (
            "fmt"
        )

        func main() {
            //n := runtime.GOMAXPROCS(1) 	   // 第一次 测试
            //打印结果：111111111111111111110000000000000000000011111...

            n := runtime.GOMAXPROCS(2)         // 第二次 测试
            //打印结果：010101010101010101011001100101011010010100110...

            for {
                    go fmt.Print(0)
                    fmt.Print(1)
                }
            }

其他包：
	runtime.NumCPU(): 返回当前系统的 CPU 核数量
	runtime.GC():    会让运行时系统进行一次强制性的垃圾收集
		强制的垃圾回收：不管怎样，都要进行的垃圾回收。
		非强制的垃圾回收：只会在一定条件下进行的垃圾回收（即运行时，系统自上次垃圾回收之后新申请的堆内存的单元（也成为单元增量）达到指定的数值）。
	runtime.NumGoroutine()：返回正在执行和排队的任务总数，runtime.NumGoroutine函数在被调用后，会返回系统中的处于特定状态的Goroutine的数量。这里的特指是指Grunnable\Gruning\Gsyscall\Gwaition。处于这些状态的Groutine即被看做是活跃的或者说正在被调度。
		注意：垃圾回收所在Groutine的状态也处于这个范围内的话，也会被纳入该计数器。
		
	runtime.GOOS():         查看目标操作系统
```



#### 6.5 sync包

```
// 同步等待组
sync.waitgroup
	在类型上，它是一个结构体。一个WaitGroup的用途是等待一个goroutine的集合执行完成。主goroutine调用了Add()方法来设置要等待的goroutine的数量。然后，每个goroutine都会执行并且执行完成后调用Done()这个方法。与此同时，可以使用Wait()方法来阻塞，直到所有的goroutine都执行完成。

var wg sync.WaitGroup
wg.Add()    
wg.Wait()  //表示让当前的goroutine等待，进入阻塞状态。直到WaitGroup的计数器为零。才能解除阻塞，这个goroutine才能继续执行。
wg.done()  //就是当WaitGroup同步等待组中的某个goroutine执行完毕后，设置这个WaitGroup的counter数值减1。其实Done()的底层代码就是调用了Add(-1)


e.g:
package main

import (
	"fmt"
	"sync"
)

var wg sync.WaitGroup // 创建同步等待组对象
func main() {
	/*
	   WaitGroup：同步等待组
	       可以使用Add(),设置等待组中要 执行的子goroutine的数量，

	       在main 函数中，使用wait(), 让主程序处于等待状态。直到等待组中子程序执行完毕。解除阻塞

	       子gorotuine对应的函数中。wg.Done()，用于让等待组中的子程序的数量减1
	*/
	//设置等待组中，要执行的goroutine的数量
	wg.Add(2)
	go fun1()
	go fun2()
	fmt.Println("main进入阻塞状态")
	wg.Wait() //表示main goroutine进入等待，意味着阻塞, 等待组中指定数量的goroutine执行完毕才会解除
	fmt.Println("main解除阻塞状态")

}
func fun1() {
	for i := 1; i <= 10; i++ {
		fmt.Println("fun1:", i)
	}
	wg.Done() //给wg等待中的执行的goroutine数量减1. 同Add(-1)
}
func fun2() {
	defer wg.Done()
	for j := 1; j <= 10; j++ {
		fmt.Println("fun2,", j)
	}
}



//互斥锁
sync.Mutex


//读写锁
sync.RWMutex


sync.Once()
func (o *Once) Do(f func()) {}

sync.Map()
var syncMap sync.Map
//新增
syncMap.Store(key, n)
//删除
syncMap.Delete(key)
//改
syncMap.LoadOrStore（key）
//遍历
syncMap.Range(walk)
```



#### 6.6 csp

```
https://www.qfgolang.com/?special=bingfagoroutinechannel&pid=2067

在Go的并发编程中有一句很经典的话：不要以共享内存的方式去通信，而要以通信的方式去共享内存。

在Go语言中并不鼓励用锁保护共享状态的方式在不同的Goroutine中分享信息(以共享内存的方式去通信)。而是鼓励通过channel将共享状态或共享状态的变化在各个Goroutine之间传递（以通信的方式去共享内存），这样同样能像用锁一样保证在同一的时间只有一个Goroutine访问共享状态.
```



### 7. channel(***)

#### 7.1 简介

> 主要用来解决协程的同步问题 以及 协程之间数据共享（数据传递）的问题
>
> 以后 goroutine 之间的通讯通过 channel 来实现， 内部实现了同步，确保并发安全
>
> goroutine 奉行 通过通信来共享内存，而不是共享内存来通信

```
channel是go语言中的一个核心类型，可以看成管道（底层数据结构其实就是队列）。并发核心单元通过它就可以发送或者接收数据进行通讯，这在一定程度上又进一步降低了编程的难度。

主要用来解决协程的同步问题以及协程之间数据共享（数据传递）的问题。

goroutine 运行在相同的地址空间，因此访问共享内存必须做好同步。goroutine奉行通过通信来共享内存，而不是共享内存来通信。

引⽤类型 channel 可用于多个 goroutine 通讯。其内部实现了同步，确保并发安全(以后goroutine之间的通讯通过channel来实现)。
```



#### 7.2 使用

```
// 创建
// cap为零, 代表无缓冲阻塞读写, 不为0, 代表有缓冲非阻塞
c := make(chan Type, cap)   

c <- value        // 将value的数据写入(存放)到channel中
a :=  <- c        // 将channel中的数据读取出来到a中
a, ok := <- c     // 将channel中的数据读取出来到a中, 同时判断通道是否关闭或者是否为nil

e.g:
	package main

    import (
        "fmt"
        "time"
        "runtime"
    )
    
    // 全局定义channel， 用来完成数据同步
    var channel = make(chan int)

    // 定义一台打印机
    func printer(s string)  {
        for _ , ch := range s {
            fmt.Printf("%c", ch)					// 屏幕stdout会有延时
            time.Sleep(1000 * time.Millisecond)
        }
    }

    // 定义两个人使用打印机
    func person1()  {				// person1 先执行
        printer("hello")
        channel <- 8
    }
    
    func person2()  {				// person2 后执行
        <- channel
        printer("wrold")
    }

    func main()  {
        go person1()
        go person2()
        runtime.Goexit()
    }


// channel同步
e.g:  
func main() {
	ch := make(chan string)

	go func() {
		for i := 0; i < 3; i++ {
			fmt.Println("子go程：",i)
		}
		ch <- "子go执行完毕"
	}()

	// 主go程获取
	str := <- ch
	fmt.Println("主go程读取：", str)
}
```



#### 7.3 无缓冲

```
无缓冲阻塞    同步
参考示意图

e.g:
package main

import (
	"fmt"
)

func main08() {
	ch := make(chan int)

	go func() {
		for i := 0; i < 5; i++ {
			fmt.Println("子 go:", i)
			ch <- i
		}
	}()

	for i := 0; i < 5; i++ {
		num := <- ch
		fmt.Println("main go:", num)
	}
}
```

#### 7.4 有缓冲

```
有缓冲非阻塞   达到缓冲区上限，阻塞，具备异步能力(那如何保证数据安全)

e.g:
package main

import (
	"fmt"
)

func main09() {
	ch := make(chan int, 5)   // 缓冲个数并不是那么精准

	go func() {
		for i := 0; i < 10; i++ {
			fmt.Println("子 go i:", i)
			ch <- i
		}
	}()

	for i := 0; i < 10; i++ {
		num := <- ch
		fmt.Println("main go i:", num)
	}
}

```

#### 7.5 关闭

> close(ch)

```
if num, ok := <- ch; ok{
	// 未关闭
} else {
	// 已关闭
	break
}

关闭channel后, 无法向channel再发送数据(引发 panic 错误后导致接收立即返回零值，获取不到值)
关闭channel后, 可以继续从channel接收数据, 其中有缓冲的, 先把缓冲区中的读取完毕, 再读取默认值； 对于无缓冲区的，直接读取默认值。

e.g:
package main

import "fmt"

func main() {
	//ch := make(chan int)
	ch := make(chan int, 10)

	go func() {
		for i := 0; i < 5; i++ {
			ch <- i
		}

		close(ch)
		// 关闭后不建议再发送数据
		//ch <- 89
		//fmt.Println("close ")
	}()

	//for {
	//	if num, ok := <-ch; ok {
	//		// 未关闭
	//		fmt.Println("main 接收到:", num)
	//	} else {
	//		num2 := <- ch
	//		fmt.Println("已关闭：", num2)
	//		break
	//	}
	//}
	for num := range ch {
		fmt.Println(num)
	}
}
```



#### 7.6  单向channel

> 有什么卵用 ？？？   做函数参数

```
单向写：   writeCh := make(chan<- int ) // 不能从其中读取数据
单向读：   readCh  := make(<-chan int)  

转换：
	双向的channel可以任意转换成单向的channel
		senCh = ch   // ok
	单向的channel不能转换成双向channel
		ch = senCh   // error

传参： 传引用
	
	
e.g.:
	//   chan<-  //只支持写
    func send(in chan<- int) {
        in <- 89
        close(out)
    }

    //   <-chan  //只支持读
    func recv(out <-chan int) {
       num:= <- out
       fmt.Println(num)
    }

    func main() {
        c := make(chan int) //  chan 读写，通过它在 只读 和  只写之间建立通道
        go send(c) 
        recv(c)    
        fmt.Println("done")
    }
```



## 04(***)

### 1. 生产者消费者模型

> 单向channel 基础上来的

```
package main

import (
	"fmt"
	"time"
)

func producer(in chan<- int) {
	for i := 0; i < 10; i++ {
		fmt.Println("生产：", i*i)
		in <- i * i
	}
	close(in)
}

func consumer(out <-chan int) {
	for num := range out {
		fmt.Println("消费者拿到：", num)
	}
}

func main() {
	ch := make(chan int, 6)
	go producer(ch) // 子go程 生产者
	consumer(ch)    // 主go程 消费
	time.Sleep(time.Second)
}

```

### 2. 定时器

```
# timer
timer有3个要素：
定时时间：就是那个d
触发动作：就是那个f
时间channel： 也就是 t.C

t :=  time.NewTimer(d) 
c :=  t.C     			 // c 是时间channel
end_time := <- t.C

t.Reset(time.Second)
ok := time.Stop()

t :=  time.AfterFunc(d, f)
c :=  time.After(d)      // c 是时间channel
t := <- time.After(d)    // t 能拿到具体的时间

e.g:
package main

import (
	"fmt"
	"time"
)


func main02() {
	// 定时器的三种方法
	fmt.Println("当前时间：", time.Now())
	//time.Sleep(time.Second)

	// time.NewTimer()
	//timer := time.NewTimer(time.Second)
	//end_time := <- timer.C
	//fmt.Println("end_time:", end_time)

	// time.After()
	// after := <- time.After(time.Second)
	// fmt.Println("after_time:", after)
	
    //// time.AfterFunc()
	//time.AfterFunc(time.Second, func() {
	//	fmt.Println("afterfun exec!!!")
	//})

	// 定时器停止, 重置
	timer := time.NewTimer(time.Second * 3)
	// 将原有定时器时间重置为 1s
	timer.Reset(time.Second)
	go func() {
		for {
			end_time := <- timer.C
			fmt.Println("end_time:", end_time)
		}
	}()
	// 停止原有的定时器
	//timer.Stop()
	for {
		;
	}
}



# ticker
ticker := time.NewTicker(time.Second)
num := <- ticker.C    					// ticker.C 是时间channel


e.g:
package main

import (
	"fmt"
	"time"
)

func main() {
	quite := make(chan bool)
	ticker := time.NewTicker(time.Second)

	i := 0
	go func() {
		for {
			num := <- ticker.C
			i++
			fmt.Println(num)

			if i >= 3 {
				quite <- true
				break
			}
		}
	}()
	// 在没有接受到数据前，一直是阻塞状态
	<- quite
}
```



### 3. select

```
	select 是 Go 中的一个控制结构。select语句类似于switch 语句，但是select会随机执行一个可运行的case。如果没有case可运行，它将阻塞，直到有case可运行。每个case中都是io操作: 

	作用：监听channel上的数据流动

e.g:
    select {
        case <- chan1:
        // 如果chan1成功读到数据，则进行该case处理语句
        case chan2 <- 1:
        // 如果成功向chan2写入数据，则进行该case处理语句
        default:
        // 如果上面都没有成功，则进入default处理流程
        // 一般不写default, 阻塞状态，出让cpu，直到有一个通信可以进行下去
    }
    
    /*
	如果其中的任意一语句可以继续执行(即没有被阻塞)，那么就从那些可以执行的语句中任意选择一条来使用
	如果没有任意一条语句可以执行(即所有的通道都被阻塞)，那么有两种可能的情况
        1.如果给出了default语句，那么就会执行default语句，同时程序的执行会从select语句后的语句中恢复
        2.如果没有default语句，那么select语句将被阻塞，直到至少有一个通信可以进行下去
    */


e.g:
package main

import (
	"fmt"
	"time"
)

func main() {
	ch := make(chan int)
	quite := make(chan bool)

	go func() {
		for i := 0; i < 5; i++ {
			ch <- i
			fmt.Println("写入:", i)
			time.Sleep(time.Second * 2)
		}
		close(ch)
		quite <- true
	}()

	for {
		select {
		case num := <-ch:
			fmt.Println("读取:", num)
		case <- quite:
			//break             // 会一直读取默认值
			//runtime.Goexit()  // 终止主go程, 后续会报错  fatal error: no goroutines (main called runtime.Goexit) - deadlock!
			return              // 终止线程
		}
		fmt.Println("++++++++++++")
	}
}



超时：	
package main

import (
	"fmt"
	"time"
)

func main() {
	ch := make(chan int)

	go func() {
		for i := 0; i < 5; i++ {
			ch <- i
			time.Sleep(time.Second)
		}
	}()

	for {
		select {
		case num := <-ch:
			fmt.Println(num)
		case <- time.After(time.Second * 3):
			goto label
		}
	}
label:
	fmt.Println("超时了！！！")
}

```

### 4. 死锁

```
出现的可能：
	1. 单go程自己死锁
		读写在至少两个以上的go程中通信
	2. go程间channel访问顺序导致死锁
		main中先出现了读
	3. 多go程，多channel交叉死锁
		最常见的， 跟其他语言比较类似
```



### 5. 互斥锁

```
用来保证在任意时刻，只能有一个协程（线程）访问该资源。其它的协程只能等待

	互斥锁是传统并发编程对共享资源进行访问控制的主要手段，它由标准库sync中的Mutex结构体类型表示。sync.Mutex类型只有两个公开的指针方法，Lock和Unlock。 Lock锁定当前的共享资源，Unlock进行解锁。
在使用互斥锁时，一定要注意：对资源操作完成后，一定要解锁，否则会出现流程执行异常，死锁等问题。通常借助defer。锁定后，立即使用defer语句保证互斥锁及时解锁

e.g:
	var mutex sync.Mutex		// 定义互斥锁变量 mutex

    func write(){
       mutex.Lock( )
       defer mutex.Unlock( )
    }





e.g:
package main

import (
   "fmt"
   "time"
   "sync"
)

var mutex sync.Mutex

func printer(str string)  {
   mutex.Lock()               	    // 添加互斥锁
   defer mutex.Unlock()         	// 使用结束时解锁

   for _, data := range str {    	// 迭代器
      fmt.Printf("%c", data)
      time.Sleep(time.Second)       // 放大协程竞争效果
   }		
}

func person1(s1 string)  {
   printer(s1)
}

func person2(s1 string)  {
   printer(s1)    		    // 调函数时传参
}

func main()  {
   go person1("hello")   		// main 中传参
   go person2("world")
   for {
      ;
   }
}


```



### 6. 读写锁

```
	互斥锁的本质是当一个goroutine访问的时候，其他goroutine都不能访问。这样在资源同步，避免竞争的同时也降低了程序的并发性能。程序由原来的并行执行变成了串行执行。其实，当我们对一个不会变化的数据只做“读”操作的话，是不存在资源竞争的问题的。因为数据是不变的，不管怎么读取，多少goroutine同时读取，都是可以的。所以问题不是出在“读”上，主要是修改，也就是“写”。修改的数据要同步，这样其他goroutine才可以感知到。所以真正的互斥应该是读取和修改、修改和修改之间，读和读是没有互斥操作的必要的, 因此，衍生出另外一种锁，叫做读写锁


GO中的读写锁由结构体类型sync.RWMutex表示。此类型的方法集合中包含两对方法：
    一组是对 写操作的锁定和解锁，简称"写锁定"和"写解锁"：
        func (*RWMutex) Lock()
        func (*RWMutex) Unlock()
        
    一组表示对 读操作的锁定和解锁，简称为"读锁定"与"读解锁"：
        func (*RWMutex) RLock()
        func (*RWMutex) RUlock()
        
从互斥锁和读写锁的源码可以看出，它们是同源的。读写锁的内部用互斥锁来实现写锁定操作之间的互斥。可以把读写锁看作是互斥锁的一种扩展。

e.g:
	package main

    import (
       "sync"
       "fmt"
       "math/rand"
    )

    var count int           		// 全局变量count
    var rwlock sync.RWMutex       	// 全局读写锁 rwlock

    func read(n int)  {
       rwlock.RLock()
       fmt.Printf("读 goroutine %d 正在读取数据...\n", n)
       num := count
       fmt.Printf("读 goroutine %d 读取数据结束，读到 %d\n", n, num)
       defer rwlock.RUnlock()
    }
    
    func write(n int)  {
       rwlock.Lock()
       fmt.Printf("写 goroutine %d 正在写数据...\n", n)
       num := rand.Intn(1000)
       count = num
       fmt.Printf("写 goroutine %d 写数据结束，写入新值 %d\n", n, num)
       defer rwlock.Unlock()
    }

    func main()  {
       for i:=0; i<5; i++ {
          go read(i+1)
       }
       for i:=0; i<5; i++ {
          go write(i+1)
       }
       for {
          ;
       }
    }
    
 注意事项：channel 和  读写锁 不能同时使用
```



### 7. 条件变量

```
不是锁， 总是与锁结合使用

判断条件变量：
        1. 加锁
        2. 访问缓冲区
        3. 解锁
        4. 唤醒阻塞在条件变量上的对端
	
	如果仓库队列满了，我们可以使用条件变量让生产者对应的goroutine暂停（阻塞），但是当消费者消费了某个产品后，仓库就不再满了，应该唤醒（发送通知给）阻塞的生产者goroutine继续生产产品。 
	
	GO标准库中的sys.Cond类型代表了条件变量。条件变量要与锁（互斥锁，或者读写锁）一起使用。成员变量L代表与条件变量搭配使用的锁
	
    type Cond struct {
       noCopy noCopy
       L Locker
       notify  notifyList
       checker copyChecker
    }


对应的有3个常用方法: Wait, Signal, Broadcast
1)	func (c *Cond) Wait() 
	该函数的作用可归纳为如下三点：
    a)	阻塞等待条件变量满足	
    b)	释放已掌握的互斥锁相当于cond.L.Unlock()。 注意：两步为一个原子操作。
    c)	当被唤醒，Wait()函数返回时，解除阻塞并重新获取互斥锁。相当于cond.L.Lock()

2)	func (c *Cond) Signal()
	单发通知，给一个正等待（阻塞）在该条件变量上的goroutine（线程）发送通知。

3)	func (c *Cond) Broadcast()
	广播通知，给正在等待（阻塞）在该条件变量上的所有goroutine（线程）发送通知。


大致执行过程：
	var cond sync.Cond
	cond.L = new(sync.Mutex())
	
	cond.L.lock()
	for len(ch) == xxx {
		cond.wait()     // 1.阻塞  2. cond.L.unlock() 3. cond.L.lock()
 	}
 	cond.L.unlock()
 	cond.Signal()


e.g:
	package main
    import "fmt"
    import "sync"
    import "math/rand"
    import "time"

    var cond sync.Cond             // 创建全局条件变量

    // 生产者
    func producer(out chan<- int, idx int) {
       for {
          cond.L.Lock()           	    // 条件变量对应互斥锁加锁
          for len(out) == 3 {          	// 产品区满 等待消费者消费,注意是for
             cond.Wait()             	// 挂起当前协程，等待条件变量满足，被消费者唤醒
          }
          num := rand.Intn(1000) 	    // 产生一个随机数
          out <- num             	    // 写入到 channel 中 （生产）
          fmt.Printf("%dth 生产者，产生数据 %3d, 公共区剩余%d个数据\n", idx, num, len(out))
          cond.L.Unlock()             	// 生产结束，解锁互斥锁
          cond.Signal()           	    // 唤醒 阻塞的 消费者
          time.Sleep(time.Second)       // 生产完休息一会，给其他协程执行机会，也可以将该部分注释掉看效果
       }
    }
    
    //消费者
    func consumer(in <-chan int, idx int) {
       for {
          cond.L.Lock()           		// 条件变量对应互斥锁加锁（与生产者是同一个）
          for len(in) == 0 {      		// 产品区为空 等待生产者生产， 注意是for
             cond.Wait()             	// 挂起当前协程， 等待条件变量满足，被生产者唤醒
          }
          num := <- in                	// 将 channel 中的数据读走 （消费）
          fmt.Printf("---- %dth 消费者, 消费数据 %3d,公共区剩余%d个数据\n", idx, num, len(in))
          cond.L.Unlock()             	// 消费结束，解锁互斥锁
          cond.Signal()           		// 唤醒 阻塞的 生产者
          time.Sleep(time.Millisecond * 500)  //消费完休息一会，给其他协程执行机会，也可以将该部分注释掉看效果
       }
    }
    
    func main() {
       rand.Seed(time.Now().UnixNano())  // 设置随机数种子
       quit := make(chan bool)           // 创建用于结束通信的 channel
       ch := make(chan int, 3)           // 使用channel 模拟
       
       
       // 很重要，否则会空指针异常
       cond.L = new(sync.Mutex)          // 创建互斥锁和条件变量

       for i := 0; i < 5; i++ {          // 5个消费者
          go producer(ch, i+1)
       }
       for i := 0; i < 3; i++ {          // 3个生产者
          go consumer(ch, i+1)
       }
       <-quit                         	 // 主协程阻塞 不结束
    }
```





## 09

### 1. web工作方式

```
域名---dns服务器---IP---http服务器
```



### 2. 错误处理函数

```
func error(err error, info string){
	if err != nil {
		fmt.Println(err, info)
		// os.Exit(1)
		return
	}
}
```



### 3. http协议

```
请求行
请求头
\r\n  代表请求头结束
请求体

e.g.:

func errFunc(err error, info string) {
	if err != nil {
		fmt.Println(info, err)
		//return					// 返回当前函数调用
		//runtime.Goexit()			// 结束当前go程
		os.Exit(1) 				   // 将当前进程结束
	}
}

func main() {

	listener, err := net.Listen("tcp", "127.0.0.1:8000")
	errFunc(err, "net.Listen err:")
	defer listener.Close()

	conn, err := listener.Accept()
	errFunc(err, "Accpet err:")
	defer conn.Close()

	buf := make([]byte, 4096)
	n, err := conn.Read(buf)
	if n == 0 {
		return
	}
	errFunc(err, "conn.Read")

	fmt.Printf("|%s|\n", string(buf[:n]))
}
```



### 4. net

> 什么时候用net, 什么时候用http???

```
package main

import (
	"fmt"
	"net"
	"os"
)

func ErrorFunc(err error, info string) {
	if err != nil {
		fmt.Println(info, err)
		os.Exit(1)
	}

}

func main() {
	listen, err := net.Listen("tcp", "127.0.0.1:8000")
	ErrorFunc(err, "listen error")

	defer listen.Close()

	accept, err := listen.Accept()
	ErrorFunc(err, "accept erro")

	defer accept.Close()

	b := make([]byte, 1024)
	n, _ := accept.Read(b)

	if n == 0 {
		return
	}
	fmt.Println(string(b[:n]))

	//GET /1111 HTTP/1.1
	//Host: 127.0.0.1:8000
	//Connection: keep-alive
	//Upgrade-Insecure-Requests: 1
	//User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36
	//Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
	//Sec-Fetch-Site: none
	//Sec-Fetch-Mode: navigate
	//Sec-Fetch-User: ?1
	//Sec-Fetch-Dest: document
	//Accept-Encoding: gzip, deflate, br
	//Accept-Language: zh-CN,zh;q=0.9,en;q=0.8
}


回调函数，本质是函数指针。 在程序中，定义一个函数，但不显示调用，但某一特定条件满足时，该函数由操作系统自动调用
```



### 5. http

```
// http 客户端
package main

import (
	"fmt"
	"net"
	"os"
)

func errFunc2(err error, info string) {
	if err != nil {
		fmt.Println(info, err)
		//return					// 返回当前函数调用
		//runtime.Goexit()			 // 结束当前go程
		os.Exit(1) 					// 将当前进程结束
	}
}
func main() {
	dial, err := net.Dial("tcp", "127.0.0.1:8000")
	errFunc2(err, "dail error")
	defer dial.Close()

	// 写
	// 先模拟浏览器 访问服务器
	//注意  get  http host 的大小写
	httpRequest := "GET /xxx HTTP/1.1\r\nHost:127.0.0.1:8000\r\n\r\n"
	_, err = dial.Write([]byte(httpRequest))
	errFunc2(err, "write error")

	// 读
	b := make([]byte, 1024)
	n, err := dial.Read(b)
	if n == 0 {
		return
	}
	errFunc2(err, "read error")
	fmt.Println(string(b[:n]))
}


// http 服务端
package main

import "net/http"

func handler(resp http.ResponseWriter, req *http.Request) {
	resp.Write([]byte("hello world"))
}

func main() {
	http.HandleFunc("/xxx", handler)

	http.ListenAndServe("127.0.0.1:8000", nil)
}



// http get 
package main

import (
	"net/http"
	"fmt"
	"io"
)

func main()  {
	// 使用Get方法获取服务器响应包数据
	//resp, err := http.Get("http://www.baidu.com")
	resp, err := http.Get("http://127.0.0.1:8000/hello")
	if err != nil {
		fmt.Println("Get err:", err)
		return
	}
	defer resp.Body.Close()

	// 获取服务器端读到的数据
	fmt.Println("Status = ", resp.Status)           // 状态
	fmt.Println("StatusCode = ", resp.StatusCode)   // 状态码
	fmt.Println("Header = ", resp.Header)           // 响应头部
	fmt.Println("Body = ", resp.Body)               // 响应包体

	buf := make([]byte, 4096)         // 定义切片缓冲区，存读到的内容
	var result string
	// 获取服务器发送的数据包内容
	for {
		n, err := resp.Body.Read(buf)  // 读body中的内容
		if n == 0 {
			fmt.Println("--Read finish!")
			break
		}
		if err != nil && err != io.EOF {
			fmt.Println("resp.Body.Read err:", err)
			return
		}

		result += string(buf[:n])     // 累加读到的数据内容
	}
	// 打印从body中读到的所有内容
	fmt.Println("result = ", result)
}
```



## 10

### 反射

> https://www.qfgolang.com/?special=fanshejizhi&pid=2594
>
> https://www.cnblogs.com/itbsl/p/10551880.html       推荐看

```
1. 反射使用的2个常见场景：

    场景1：有时你需要编写一个函数，但是并不知道传给你的参数类型是什么，可能是没约定好；也可能是传入的类型很多，这些类型并不能统一表示。这时反射就会用的上了。
    
    场景2：有时候需要根据某些条件决定调用哪个函数，比如根据用户的输入来决定。这时就需要对函数和函数的参数进行反射，在运行期间动态地执行函数。

2. 不太建议使用反射的理由

	与反射相关的代码，经常是难以阅读的。在软件工程中，代码可读性也是一个非常重要的指标。
	
	Go 语言作为一门静态语言，编码过程中，编译器能提前发现一些类型错误，但是对于反射代码是无能为力的。所以包含反射相关的代码，很可能会运行很久，才会出错，这时候经常是直接 panic，可能会造成严重的后果。
	
	反射对性能影响还是比较大的，比正常代码运行速度慢一到两个数量级。所以，对于一个项目中处于运行效率关键位置的代码，尽量避免使用反射特性。	
	
3. 反射基本概念
反射是建立在类型之上的，主要与Golang的interface类型相关（它的type是concrete type），只有interface类型才有反射一说。

理解了pair，就更容易理解反射。反射就是用来检测存储在接口变量内部(值value；类型concrete type) pair对的一种机制。

所以我们要理解两个基本概念 Type 和 Value，它们也是 Go语言包中 reflect 空间里最重要的两个类型。


它提供了两种类型（或者说两个方法）让我们可以很容易的访问接口变量内容，分别是reflect.ValueOf() (获取值)和 reflect.TypeOf() (获取类型)


package main

import (
    "fmt"
    "reflect"
)

func main() {
    //反射操作：通过反射，可以获取一个接口类型变量的 类型和数值
    var x float64 =3.4

    fmt.Println("type:",reflect.TypeOf(x)) //type: float64
    fmt.Println("value:",reflect.ValueOf(x)) //value: 3.4

    fmt.Println("-------------------")
    //根据反射的值，来获取对应的类型和数值
    v := reflect.ValueOf(x)
    fmt.Println("kind is float64: ",v.Kind() == reflect.Float64)
    fmt.Println("type : ",v.Type())
    fmt.Println("value : ",v.Float())
}


4. 反射获取接口变量信息
4.1 通过实例获取Value对象
func ValueOf(i interface {}) Value 

4.2 通过实例获取 Type
func TypeOf(i interface{}) Type

4.3 (type --- value)Type 里面只有类型信息，所以直接从一个 Type 接口变量里面是无法获得实例的 Value 的，但可以通过该 Type 构建一个新实例的 Value
	//New 返回的是一个 Value，该 Value 的 type 为 PtrTo(typ)，即 Value 的 Type 是指定 typ 的指针
	func New(typ Type) Value
	
	//Zero 返回的是一个 typ 类型的零佳，注意返回的 Value 不能寻址，位不可改变
	func Zero(typ Type) Value
	
	//如果知道一个类型值的底层存放地址，则还有一个函数是可以依据 type 和该地址值恢复出 Value 的。例如：
	func NewAt(typ Type, p unsafe.Pointer) Value
	
4.4 从 Value 到 Type, 从反射对象 Value 到 Type 可以直接调用 Type 的方法，因为 Value 内部存放着到 Type 类型的指针。例如：
func (v Value) Type() Type


4.5 从 Value 到实例
    //该方法最通用，用来将 Value 转换为空接口，该空接口内部存放具体类型实例
    //可以使用接口类型查询去还原为具体的类型
    func (v Value) Interface() （i interface{})

    //Value 自身也提供丰富的方法，直接将 Value 转换为简单类型实例，如果类型不匹配，则直接引起 panic
    func (v Value) Bool () bool
    func (v Value) Float() float64
    func (v Value) Int() int64
    func (v Value) Uint() uint64
   
4.6 从 Value 的指针到值
      //如果 v 类型是接口，则 Elem() 返回接口绑定的实例的 Value，如采 v 类型是指针，则返回指针值的 		Value，否则引起 panic
    	func (v Value) Elem() Value
    	
       //如果 v 是指针，则返回指针值的 Value，否则返回 v 自身，该函数不会引起 panic
    	func Indirect(v Value) Value
   
4.7 Type指针和值的相互转换
    指针类型 Type 到值类型 Type。例如：

    //t 必须是 Array、Chan、Map、Ptr、Slice，否则会引起 panic
    //Elem 返回的是其内部元素的 Type
    t.Elem() TypeCOPY
    
    
    值类型 Type 到指针类型 Type。例如：
    //PtrTo 返回的是指向 t 的指针型 Type
    func PtrTo(t Type) Type

4.8 Value 值的可修改性
//通过 CanSet 判断是否能修改
func (v Value ) CanSet() bool
//通过 Set 进行修改
func (v Value ) Set(x Value)


4.9 使用
已知原有类型
已知类型后转换为其对应的类型的做法如下，直接通过Interface方法然后强制转换，如下：
realValue := value.Interface().(已知的类型)
e.g:
	convertPointer := pointer.Interface().(*float64)
    convertValue := value.Interface().(float64)
  
未知原有类型
package main

import (
    "fmt"
    "reflect"
)

type Person struct {
    Name string
    Age int
    Sex string
}

func (p Person)Say(msg string)  {
    fmt.Println("hello，",msg)
}
func (p Person)PrintInfo()  {
    fmt.Printf("姓名：%s,年龄：%d，性别：%s\n",p.Name,p.Age,p.Sex)
}

func main() {
    p1 := Person{"王二狗",30,"男"}
    DoFiledAndMethod(p1)
}

// 通过接口来获取任意参数
func DoFiledAndMethod(input interface{}) {

    getType := reflect.TypeOf(input) //先获取input的类型
    fmt.Println("get Type is :", getType.Name()) // Person
    fmt.Println("get Kind is : ", getType.Kind()) // struct

    getValue := reflect.ValueOf(input)
    fmt.Println("get all Fields is:", getValue) //{王二狗 30 男}

    // 获取方法字段
    // 1. 先获取interface的reflect.Type，然后通过NumField进行遍历
    // 2. 再通过reflect.Type的Field获取其Field
    // 3. 最后通过Field的Interface()得到对应的value
    for i := 0; i < getType.NumField(); i++ {
        field := getType.Field(i)
        value := getValue.Field(i).Interface() //获取第i个值
        fmt.Printf("字段名称:%s, 字段类型:%s, 字段数值:%v \n", field.Name, field.Type, value)
    }

    // 通过反射，操作方法
    // 1. 先获取interface的reflect.Type，然后通过.NumMethod进行遍历
    // 2. 再公国reflect.Type的Method获取其Method
    for i := 0; i < getType.NumMethod(); i++ {
        method := getType.Method(i)
        fmt.Printf("方法名称:%s, 方法类型:%v \n", method.Name, method.Type)
    }
}

    

5. 设置实际变量的值
通过refPtrVal := reflect.Valueof( &var )的方式获取指针类型，你使用refPtrVal.elem( ).set（一个新的reflect.Value）来进行更改，传递给set()的值也必须是一个reflect.value。

 	pointer := reflect.ValueOf(&num)
    newValue := pointer.Elem()

    fmt.Println("类型 :",       newValue.Type()) //float64
    fmt.Println("是否可以修改:", newValue.CanSet())

    // 重新赋值
    newValue.SetFloat(77)
    fmt.Println("新的数值:", num)


6. 方法调用
reflect.Valueof() 拿到反射对象 --> MethodByName(), call() 
	 //一定要指定参数为正确的方法名
    // 先看看没有参数的调用方法
    methodValue1 := getValue.MethodByName("PrintInfo")
    fmt.Printf("Kind : %s, Type : %s\n",methodValue1.Kind(), methodValue1.Type())
    methodValue1.Call(nil) //没有参数，直接写nil

    args1 := make([]reflect.Value, 0) //或者创建一个空的切片也可以
    methodValue1.Call(args1)

    // 有参数的方法调用
    methodValue2 := getValue.MethodByName("Say")
    fmt.Printf("Kind : %s, Type : %s\n",methodValue2.Kind(),methodValue2.Type())
    args2 := []reflect.Value{reflect.ValueOf(100),reflect.ValueOf("hello")}
    methodValue2.Call(args2)
```



