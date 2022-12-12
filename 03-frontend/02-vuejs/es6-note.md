参考资料

```
https://www.bilibili.com/video/BV1Kt411w7MP?p=2
https://wangdoc.com/javascript/            //js基础
https://www.jianshu.com/p/ebfeb687eb70         //推荐看，快速熟悉新特性
https://www.bilibili.com/read/cv16013578       //推荐看，完整版
https://www.runoob.com/w3cnote/es6-setup.html  //推荐看，完整版
https://es6.ruanyifeng.com/                //工具书，比较深
```



## 1. call&apply&bind

```
53-59

// call 可以改变函数的指向, 可以实现继承
var o = {
	name: "andy"
}

function fn(a, b) {
	console.log(this)
	console.log(a + b )
}

fn.call(o, 1, 2)



function Father(uname, age, sex) {
	this.uname = uname;
	this.age = age;
	this.sex = sex;
}
function Son(uname, age, sex) {
	Father.call(this, uname, age, sex)
}

// apply, 和call类似，但是参数不一样, 传递的是数组
var o = {
	name: "andy"
}
function fn(arr) {
	console.log(this)
	console.log(arr)
}
fn.apply(o, [1, 2])

var arr = [1, 5, 3, 10]
Math.max.apply(Math, arr)


// bind, 不会调用函数， 返回的是原函数的拷贝
var o = {
	name: "andy"
}
function fn(arr) {
	console.log(this)
	console.log(arr)
}
var fn1 = fn.bind(o, [1, 2])
fn1() 


// bind的应用(应用最多, 在es6中通过箭头函数改变this指向)
定时器函数里面的this指向的window, btn 指向的是btn

btn.onclick = function(){
	this.disabled = true;
	setTimeout(function(){
		this.disabed = false;
	}.bind(this), 3000)
}

bind(this.xxx, this)
```



## 2. var&let&const

```
91-122

var   在全局范围内都有效， 变量可以在声明之前使用，值为undefined，存在变量提升 
let   声明的变量只在它所在的代码块有；不存在变量提升, 直接报错； 块级作用域
const 
	e.g:
		var a = 10; 
		let b = 20;
		const PI = 3.14;    // const有一个很好的应用场景，就是当我们引用第三方库的时声明的变量，用const来声明可以避免未来不小心重命名而导致出现bug
```



## 3.  class&extends&super

```
class, extends, super
// e.g.:
class Animal {
    constructor(){
        this.type = 'animal'
    }
    says(word){
        console.log(this.type + ' says ' + word)
    }
}

let animal = new Animal()
animal.says('hello')   //  animal says hello

class Cat extends Animal {
    constructor(){
        super()
        this.type = 'cat'
    }
}

let cat = new Cat()
cat.says('hello')    //cat says hello
```







## 4. 箭头函数

```
() => {}

//1.函数体只有一句代码，大括号省略, return省略
const sum = (n1, n2) => n1 + n2
//2. 参只有一个
const fn = v => alert(v)
//3. this, 不绑定this, 箭头函数定义在哪，this指向谁, 实际是继承

e.g.1:
	function(i){ return i + 1; } //ES5
	(i) => i + 1 //ES6
	
e.g.2:
	function(x, y) { 
        x++;
        y--;
        return x + y;
    }
    (x, y) => {x++; y--; return x+y}
    
e.g.3: this
	class Animal {
        constructor(){
            this.type = 'animal'
        }
        says(say){
            setTimeout(function(){
                console.log(this.type + ' says ' + say)
            }, 1000)
        }
    }

    var animal = new Animal()
    animal.says('hi')  //undefined says hi
    
    传统解决方案：
    	第一种是将this传给self,再用self来指代this
         says(say){
             var self = this;
             setTimeout(function(){
                 console.log(self.type + ' says ' + say)
             }, 1000)
             
         第二种方法是用bind(this),即
            says(say){
                setTimeout(function(){
                console.log(self.type + ' says ' + say)
            }.bind(this), 1000)

		第三种箭头函数:
			class Animal {
                constructor(){
                    this.type = 'animal'
                }
                says(say){
                    setTimeout( () => {
                        console.log(this.type + ' says ' + say)
                    }, 1000)
                }
            }
            var animal = new Animal()
            animal.says('hi')  //animal says hi
            
            函数体内的this对象，就是定义时所在的对象，而不是使用时所在的对象。并不是因为箭头函数内部有绑定this的机制，实际原因是箭头函数根本没有自己的this，它的this是继承外面的，因此内部的this就是外层代码块的this。
```







## 5. 模板字符串

```
模板字符串: 用反引号（` 和 `）来标识起始和结束，用${}来引用变量，而且所有的空格和缩进都会被保留在输出之中

let basket = {
	count: 1 ; 
	onSale: false;
}

$("#result").append(`
  There are <b>${basket.count}</b> items
   in your basket, <em>${basket.onSale}</em>，
    <em>${fn()}</em>
   are on sale!
`);

特点：
//1.可以调用函数
//2.可以换行
//3.解析变量
```



## 6. 解构赋值

> ES6允许按照一定模式，从数组和对象中提取值，对变量进行赋值，这被称为解构（Destructuring）。

```
// 数组解构
let arr = [1,2,3]
let [a, b, c, d] = arr

// 对象解构
let person = {name: "dh", age: 20};
let {name, age} = person;
console.log(name, age)

// 别名 
let {name: myname, age: myage} = person
```



## 5. 不定参数和默认值

```
//1. 基本使用
const sum = (...args) => {
	let total =0
	args.forEach(item => {
		total +=item
	})
	return total
}
console.log(sum(10,20))
console.log(sum(10,20,30))

//2. 不定参数和解构结合使用
let arr1 = ["张三", "李四"，"王五"]
let [s1, ...s2] = arr1

//3. 默认值
function animal(type = 'cat'){
    console.log(type)
}
animal()
```



## 6. 扩展运算符

```
扩展运算符，也叫展开语法，可以将数组或者对象转为逗号分隔的参数序列

1. 数组扩展
// 基本使用
let arr = [1,2,3]
console.log(...arr)  //1,2,3

// 合并数组
let arr1 = [1,2,3]
let arr2 = [4,5,6]
let arr3 = [...arr1, ...arr2]
或者 
arr1.push(...arr2)
或者
let arr = arr1.concat(arr2);

// 将伪数组转换成真正的数组
let oDivs = documents.getElementByTagName("div");
oDivs = [...oDivs]
oDivs.push("a")
console.log(oDivs)


// Array.from()  //将伪数组或者类数组变成真数组，第二个参数，作用类似于数组的map
// Array.find()  找到了就返回符合条件的成员, 找不着就返回undefined
// Array.findIndex()
// Array.includes()
	e.g.1:
        let itemList = document.querySelectorAll('.item');
        Array.isArray(itemList);  // false
        let list = Array.from(Array);
        Array.isArray(list);  // true

        // arguments对象,函数调用时都会产生的一个对象, 用来存放所有实体参数
        function say() {
            console.log(Array.isArray(arguments)); //false arguments是个伪数组
            let args = Array.from(arguments);
            console.log(Array.isArray(args));  // true
        }
        say('a','b','c');
    
    e.g.2:
    	let list = [
          { username: "zs", age: 21 },
          { username: "lisi", age: 20 },
          { username: "ww", age: 22 },
          { username: "lisi", age: 100 },
        ];

        let res1 = list.find(function(item) {
            return item.username === 'lisi';
        })
        console.log('res1',res1);

        let res2 = list.find(function(item) {
            return item.username === 'lisan';
        })
        console.log('res2',res2); 
    
    
2. 对象扩展
    let username = '张三';
    let age = 20;
    // es5对象的写法
    const obj = {
        username: username,
        age: age,
        say: function() {
            console.log(this.username);
        }
    }
    // es6对象属性和对象的简洁表示方式
    const obj2 = {
        // 如果属性和值相同,只写一个
        username,
        age,
        say() {
            console.log(this.username);
        }
    } 


    // 合并对象
    let obj1 = {
        name: 'zs',
        age: 20
    }
    let obj2 = {
        name: '李四',
        age: 20,
        addr: '广东深圳'
    }
    const obj = Object.assign(obj1,obj2);
    console.log(obj);



3. 函数扩展
	箭头函数及箭头指向
	
	//1. 箭头函数
        const add = (a,b)=> {
            return a+b;
        }
        add(2,3);


        //函数体只有一行代码的时候可以简写成
        const add = (a, b) => a + b;
        add(2, 3);

        const arr = [1, 2, 3, 41, 2, 34, 4, 12];
        // es5写法
        arr.filter(function (item) {
          return item > 20;
        });
        // 箭头函数的写法
        arr.filter((item) => item > 20);

      //2. 箭头函数的this指向
      // 箭头函数自己是没有this的, 它会捕获它的上下文(作用域), 作为它自己的this
        const obj = {
            say() {
                // this指向obj
                console.log('1',this);
                setTimeout(function(){
                    // 匿名函数,this指向window
                    console.log('2',this);
                },1000)

                setTimeout(()=>{
                    // 匿名函数,this指向window
                    console.log('3',this);
                },2000)
            }
        }
        obj.say(); 

4. 扩展运算符
//1.在对象中使用
const obj1 = {
    a:2,
    c:5
}
const obj2 = {
    a:3,
    b:4
}

// 合并两个对象
const obj = {
    ...obj1,
    ...obj2,
}

// 合并对象
let obj = Object.assign(obj1,obj2);
console.log(obj);

// 复制一个对象的同时修改或新增属性
const obj1 = {
    name: 'zs',
    age: 20
}

const obj2 = {
    ...obj1,
    // 修改原来属性
    age: 30,
    // 新增属性
    addr: '深圳'
}
console.log(obj2);

//2.在数组中使用
const arr1 = [1,2,3];
const arr2 = [
    ...arr1,
    2,
    4
]
console.log('arr2',arr2);

// 合并两个数组
const arr = [
    ...arr1,
    ...arr2
]
console.log('arr',arr)

//3.在函数中使用
const say = (a,b, ...c)=> {
    console.log(a,b,c)
}
say(1,2,3,4,5,6,7); 
```



## 7. promise

```
1. Promise 的定义
2. promise有三种状态:
    pending 正在进行中
    resolved 成功
    rejected 失败

3. 状态一旦改变，就无法再次改变状态，这也是它名字 promise-承诺 的由来，一个promise对象状态只能改变一次
4. 我们可以使用promise来保存将来的数据


使用步骤
    1.创建promise对象
    2.存储成功或失败的数据
    3.获取promise对象的数据


<!--promise-->
<!DOCTYPE html>
<html lang="en">
<body>
    <script type="module">
      let num = window.prompt("请输入数字");

      // 1.创建promise对象
      const obj = new Promise((resolve, reject) => {
        // num > 10定位成功, 否则失败
        if (num > 10) {
          // 2.成功时用resolve保存数据
          resolve({msg:'sucess',num});
        } else {
          // 3.失败时用reject保存数据
          reject({ msg: 'error', num });
        }
      });

      // 3.获取数据 then()获取成功的数据, catch()获取失败的数据
      obj.then((res)=> {
        console.log('成功', res);
      }).catch(err=> {
          console.log('失败',err);
      })
    </script>
</body>
</html>


<!--axois和promise的关系-->
<!DOCTYPE html>
<html lang="en">
<body>
    <script src="https://cdn.bootcdn.net/ajax/libs/axios/0.26.0/axios.min.js"></script>
    <script>
      const xhr = axios.get('xxxxx');
      // axios.get()和axios.post()  都是返回一个Promise的实例对象
      console.log(xhr instanceof Promise);
      xhr.then(res=> {
          console.log(res);
      }).catch(err=> {
        console.log(err);
      })
    </script>
</body>
</html>



<!--axios await 异步编程变为同步编程-->
<!DOCTYPE html>
<html lang="en">
<body>
    <script src="https://cdn.bootcdn.net/ajax/libs/axios/0.26.0/axios.min.js"></script>
    <script>
        const getData = async () => {
            try {
                const res = await axios.get('http://huruqing.cn:3003/category/all2');
                console.log(res.data);
            } catch (error) {
                console.log('错误信息',error);
            }
        }
        getData();
    </script>
</body>
</html>
```



## 8. 模块

```
export 与 import 基本用法：
模块导入导出各种类型的变量，如字符串，数值，函数，类。
    1.导出的函数声明与类声明必须要有名称（export default 命令另外考虑）。 
    2.不仅能导出声明还能导出引用（例如函数）。
    3.export 命令可以出现在模块的任何位置，但必需处于模块顶层。
    4.import 命令会提升到整个模块的头部，首先执行。

// export
let myName = "Tom";
let myAge = 20;
let myfn = function(){
    return "My name is" + myName + "! I'm '" + myAge + "years old."
}
let myClass =  class myClass {
    static a = "yeah!";
}
export { myName, myAge, myfn, myClass }

// import
import { myName, myAge, myfn, myClass } from "./test.js";
console.log(myfn());      // My name is Tom! I'm 20 years old.
console.log(myAge);       // 20
console.log(myName);      // Tom
console.log(myClass.a );  // yeah!



export default 用法：
    1. 在一个文件或模块中，export、import 可以有多个，export default 仅有一个。
    2. export default 中的 default 是对应的导出接口变量。
    3. 通过 export 方式导出，在导入时要加{ }，export default 则不需要。
    4. export default 向外暴露的成员，可以使用任意变量来接收。
    
    var a = "My name is Tom!";
    export default a;               // 仅有一个
    export default var c = "error"; // error，default 已经是对应的导出变量，不能跟着变量声明语句

    import b from "./xxx.js";       // 不需要加{}， 使用任意变量接收
```



## 9. map&set&proxy&reflect

> https://www.runoob.com/w3cnote/es6-map-set.html
>
> https://www.runoob.com/w3cnote/es6-reflect-proxy.html