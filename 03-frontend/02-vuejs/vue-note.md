# vue2.x

## 0. 参考文档

```
https://cn.vuejs.org/v2/api/

https://cn.vuejs.org/v2/guide/
```



## 1.  发展历程

```
2014.2   诞生
2015.10  vue1.0发布
2016.4   vue2.0发布预览版， 10月出正式版本
2020.4   vue3.0发布预览版   9.18正式版本
```



## 2. 概述

```
声明式渲染  --- 组件系统 --- 客户端路由 --- 集中式状态管理 --- 项目构建
```



## 3. 基本使用

```vue
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<script type="text/javascript" src="js/vue.js"></script>


<body>
    <div id="app">
        <div>{{ msg }}</div>
    </div>
    <script type="text/javascript">
        var vm = new Vue({
            el: "#app",
            data: {
                msg: "hello world"
            }
        })
    </script>

</body>

</html>
```



## 4. 指令

```
自定义属性就是指令，在vue中以 v- 开头
```



### 4.1 v-cloak

- 防止页面加载时出现闪烁问题(针对的是差值表达式，不断刷新出现渲染问题：有花括号)

```vue
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<style type="text/css">
    [v-cloak] {
        display: none;
    }
</style>
<script type="text/javascript" src="js/vue.js"></script>

<body>
    <div id="app">
        <div v-cloak>{{ msg }}</div>
    </div>
    
    <script type="text/javascript">
        var vm = new Vue({
            el: "#app",
            data: {
                msg: "hello world"
            }
        })
    </script>
</body>

</html>
```

- 背后原理：先隐藏，替换完成后，再显示



### 4.2 v-text

- 没有闪动问题
- 渲染文本

```vue
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>

<script type="text/javascript" src="../js/vue.js"></script>

<body>
    <div id="app">
        <div>{{ msg }}</div>
        <div v-text="msg"></div>
        <div v-html="msg1"></div>
        <span v-pre>{{msg2}}</span>  
    </div>

    <script type="text/javascript">
        var vm = new Vue({
            el: "#app",
            data: {
                msg: "hello world", 
                msg1: "<h1>html</h1>",
                msg2: "原始信息"
            }
        })
    </script>
</body>

</html>
```

### 4.3 v-html

- 渲染html
- 存在一定的xss 问题， 网站内部数据可以使用，第三方的的数据不建议使用



### 4.4 v-pre

- 填充原始数据，跳过编译过程



### 4.5 v-once

- 数据响应式，只编译一次，数据改变的时候，差值不发生变化

  ```vue
  <span v-once>{{ msg}}</span>    
  <script>
      new Vue({
          el: '#app',
          data: {
              msg: 'Hello Vue.js'
          }
      });
  </script>
  ```



### 4.6 v-model

- 当数据发生变化的时候，视图也就发生变化
- 当视图发生变化的时候，数据也会跟着同步变化
- v-model  =  属性绑定 + 事件绑定(v-bind + v-on)
- mvvm(model, view, view-model(vm, dom listeners, data bindings))
- **v-model**是一个指令，限制在 `<input>、<select>、<textarea>、components`中使用

```vue
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>

<script type="text/javascript" src="../js/vue.js"></script>

<body>
    <div id="app">
        <div>{{ msg }}</div> 
        <input type="text" name="" id=""  v-model="msg"></input>
    </div>

    <script type="text/javascript">
        var vm = new Vue({
            el: "#app",
            data: {
                msg: "hello world",
            },
            methods: {

            },
        })
    </script>
</body>

</html>
```



### 4.7 v-on

- v-on:click=""  可以简写为   @click=""
- 调用方式    @click="sayHi"   或者是  @click="sayHi()"

```vue
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>

<script type="text/javascript" src="../js/vue.js"></script>

<body>
    <div id="app">
        <div>{{ num }}</div>
        <input type="button" id="button1" value="点击1" v-on:click="num++"></input>
        <input type="button" id="button2" value="点击2" v-on:click="handle"></input>
        <input type="button" id="button3" value="点击3" @click="handle"></input>
    </div>

    <script type="text/javascript">
        var vm = new Vue({
            el: "#app",
            data: {
                num: 0
            },
            methods: {
                handle: function () {
                    this.num++
                }
            },
        })
    </script>
</body>
</html>
```



### 4.8 事件

- 事件函数参数传递： 普通参数 和 事件对象

- event默认会传递，所以可以在函数后直接加上   ***

  ```vue
  <!DOCTYPE html>
  <html lang="en">
  <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Document</title>
  </head>
  
  <script type="text/javascript" src="../js/vue.js"></script>
  
  <body>
      <div id="app">
          <div>{{ num }}</div>
          <input type="button" id="button2" value="点击2" v-on:click="handle1"></input>
          <input type="button" id="button3" value="点击3" @click="handle2(123, $event)"></input>
      </div>
  
      <script type="text/javascript">
          var vm = new Vue({
              el: "#app",
              data: {
                  num: 0
              },
              methods: {
                  handle1: function () {
                      this.num++
                  },
                  handle2: function (p1, event) {
                      console.log(p1)
                      console.log(event.target.tagName)
                      console.log(event.target.value)
                      console.log(event.keyCode)
                  },
              },
          })
      </script>
  </body>
  
  </html>
  ```
  
- 事件修饰符

  - 在事件处理程序中调用 `event.preventDefault()` 或 `event.stopPropagation()` 是非常常见的需求。
  - Vue 不推荐我们操作DOM    为了解决这个问题，Vue.js 为 `v-on` 提供了**事件修饰符**
    - 修饰符是由点开头的指令后缀来表示的

  ```
  <!-- 提交事件不再重载页面 或者 不再跳转 -->
  <form v-on:submit.prevent="onSubmit"></form>
  
  <!-- 阻止单击事件继续传播, 防止冒泡 -->
  <a v-on:click.stop="doThis"></a>
  
  <!-- 修饰符可以串联   即阻止冒泡也阻止默认跳转事件 -->
  <a v-on:click.stop.prevent="doThat"></a>
  
  <!-- 只当在 event.target 是当前元素自身时触发处理函数 -->
  <!-- 即事件不是从内部元素触发的 -->
  <div v-on:click.self="doThat">...</div>
  
  使用修饰符时，顺序很重要；相应的代码会以同样的顺序产生。因此，用 v-on:click.prevent.self 会阻止所有的点击，而 v-on:click.self.prevent 只会阻止对元素自身的点击。
  
  self 和 stop 的区别：
  https://blog.csdn.net/lolhuxiaotian/article/details/121244535
  ```

  ```vue
  <!DOCTYPE html>
  <html lang="en">
  
  <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Document</title>
  </head>
  
  <script type="text/javascript" src="../js/vue.js"></script>
  
  <body>
      <div id="app">
          <div>{{ num }}</div>
          <div v-on:click="handle1">
              <!-- 阻止冒泡1 -->
              <!-- <button v-on:click="handle2($event)"> 点击1</button> -->
  
              <!-- 阻止冒泡2 -->
              <button v-on:click.stop="handle2($event)"> 点击1</button>
          </div>
  
  
          <!-- 阻止跳转1 -->
          <!-- <a href="www.baidu.com" v-on:click="handle3">百度</a>   -->
          <!-- 阻止跳转2 -->
          <a href="www.baidu.com" v-on:click.prevent="handle3">百度</a>  
  
  
      </div>
  
      <script type="text/javascript">
          var vm = new Vue({
              el: "#app",
              data: {
                  num: 0
              },
              methods: {
                  handle1: function () {
                      this.num++
                  },
                  handle2: function (event) {
                      // 阻止冒泡1
                      // event.stopPropagation();
                  },
                  handle3: function (event) {
                      // 阻止跳转1
                      // event.preventDefault();
                  },
              },
          })
      </script>
  </body>
  
  </html>
  ```

- 按键修饰符

  ```vue
  <!-- 只有在 `keyCode` 是 13 时调用 `vm.submit()` -->
  <input v-on:keyup.13="submit">
  
  <!-- -当点击enter 时调用 `vm.submit()` -->
  <input v-on:keyup.enter="submit">
  
  <!--当点击enter或者space时  时调用 `vm.alertMe()`   -->
  <input type="text" v-on:keyup.enter.space="alertMe" >
  
  
  <script>
  	var vm = new Vue({
          el:"#app",
          methods: {
                submit:function(){},
                alertMe:function(){},
          }
      })
  </script>
  
  
  <!--常用的按键修饰符 --
  .enter =>    enter键
  .tab => 	 tab键
  .delete      (捕获“删除”和“退格”按键) =>  删除键
  .esc =>      取消键
  .space =>    空格键
  .up =>       上
  .down =>     下
  .left =>     左
  .right =>    右	
  ```
  
- 自定义按键修饰符(keyup是好用的，keydown有问题的，可能默认只支持keyup)

  ```vue
  <div id="app">
      预先定义了keycode 116（即F5）的别名为f5，因此在文字输入框中按下F5，会触发prompt方法
      <input type="text" v-on:keyup.f5="prompt()">   
  </div>
  
  <script>
  	<!-- vue.config.keycode 自定义按键修饰符 -->
      Vue.config.keyCodes.f5 = 116;
  
      let app = new Vue({
          el: '#app',
          methods: {
              prompt: function() {
                  alert('我是 F5！');
              }
          }
      });
  </script>
  ```





### 4.9 v-bind

- v-bind :href   
- :href

```vue
<!-- 绑定一个属性 -->
<img v-bind:src="imageSrc">

<!-- 缩写 -->
<img :src="imageSrc">
```



- 绑定对象

```vue
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<style type="text/css">
    .active {
        border: 1px solid red;
    }
</style>

<script type="text/javascript" src="../js/vue.js"></script>

<body>
    <div id="app">
        <!-- 绑定对象 -->
        <button v-bind:class=" {active:isActive} "> 绑定对象</button>
    </div>

    <script type="text/javascript">
        var vm = new Vue({
            el: "#app",
            data: {
                isActive: true
            },
        })
    </script>
</body>

</html>
```



- 绑定数组

```vue
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<style type="text/css">
    .textColor{
        color:#f00;
        background-color:#eef;
    }
    .textSize{
        font-size:30px;
        font-weight:bold;
    }
</style>

<script type="text/javascript" src="../js/vue.js"></script>

<body>
    <div id="app">
        <!-- 绑定数组 -->
        <button v-bind:class=" [ class1, class2 ] "> 绑定数组</button>
    </div>

    <script type="text/javascript">
        var vm = new Vue({
            el: "#app",
            data: {
                class1 : "textColor",
                class2 : "textSize",
            },
        })
    </script>
</body>

</html>
```



class绑定注意事项

```vue
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Document</title>
  <style type="text/css">
    .active {
      border: 1px solid red;
      width: 100px;
      height: 100px;
    }
    .error {
      background-color: orange;
    }
    .test {
      color: blue;
    }
    .base {
      font-size: 28px;
    }
  </style>
</head>
<body>
  <div id="app">
    <div v-bind:class='[activeClass, errorClass, {test: isTest}]'>测试样式</div>
    <div v-bind:class='arrClasses'></div>
    <div v-bind:class='objClasses'></div>
    <div class="base" v-bind:class='objClasses'></div>

    <button v-on:click='handle'>切换</button>
  </div>
  <script type="text/javascript" src="js/vue.js"></script>
  <script type="text/javascript">
    /*
      样式绑定相关语法细节：
      1、对象绑定和数组绑定可以结合使用
      2、class绑定的值可以简化操作
      3、默认的class如何处理？默认的class会保留, 默认的class和自定义的class可以混合使用
      
    */
    var vm = new Vue({
      el: '#app',
      data: {
        activeClass: 'active',
        errorClass: 'error',
        isTest: true,
        arrClasses: ['active','error'],
        objClasses: {
          active: true,
          error: true
        }
      },
      methods: {
        handle: function(){
          // this.isTest = false;
          this.objClasses.error = false;
        }
      }
    });
  </script>
</body>
</html>

```



- 绑定style

```vue
<!-- 绑定样式对象 -->
<div v-bind:style="styleObject">绑定样式对象</div>'
 
<!-- CSS 属性名可以用驼峰式 (camelCase) 或短横线分隔 (kebab-case，记得用单引号括起来)    -->
 <div v-bind:style="{ color: activeColor, fontSize: fontSize, background:'red' }">内联样式</div>

<!--绑定样式数组可以将多个样式对象应用到同一个元素 -->
<div v-bind:style="[styleObj1, styleObj2]"></div>


<script>
	new Vue({
      el: '#app',
      data: {
        styleObject: {
          color: 'green',
          fontSize: '30px',
          background:'red'
        }，
        activeColor: 'green',
   		fontSize: "30px",
        styleObj1: {
             color: 'red'
        },
        styleObj2: {
            fontSize: '30px'
        }, 
      },
</script>
```





### 4.10 v-if

```vue
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<script type="text/javascript" src="../js/vue.js"></script>

<body>
    <div id="app">
        <div v-if="score>=90"> 优秀啊</div>
        <div v-else-if=" score < 90 && score>=80 "> 良好</div>
        <div v-else="score>=60 && score < 80 "> 一般啊</div>
        <button v-show="open" v-on:click="change"> change</button>
    </div>

    <script type="text/javascript">
        var vm = new Vue({
            el: "#app",
            data: {
                score: 80,
                open: true
            },
            methods: {
                change: function () {
                    this.open = !this.open
                }
            },

        })
    </script>
</body>

</html>
```



### 4.11 v-show

- v-show本质就是标签display设置为none，控制隐藏
  - v-show只编译一次，后面其实就是控制css，而v-if不停的销毁和创建，故v-show性能更好一点。
- v-if是动态的向DOM树内添加或者删除DOM元素
  - v-if切换有一个局部编译/卸载的过程，切换过程中合适地销毁和重建内部的事件监听和子组件



### 4.12 v-for

- 用于循环的数组里面的值可以是对象，也可以是普通元素  

- **不推荐**同时使用 `v-if` 和 `v-for`
- 当 `v-if` 与 `v-for` 一起使用时，`v-for` 具有比 `v-if` 更高的优先级。
- key 的作用（很重要）
  - **key来给每个节点做一个唯一标识**
  - **key的作用主要是为了高效的更新虚拟DOM**

```vue
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<script type="text/javascript" src="../js/vue.js"></script>

<body>
    <div id="app">
        <!-- 普通数组 -->
        <li v-for="item in fruits">{{item}}</li>

        <!-- 带索引 -->
        <li v-for="(item, index) in fruits">{{item +"--"+index}}</li>

        <!-- 对象 -->
        <li v-for="item in obj">{{ item.name +"---"+item.age }}</li>

        <!-- 带key -->
        <li :key="index" v-for="(item,index) in obj">{{ item.name +"---"+item.age }}</li>

    </div>

    <script type="text/javascript">
        var vm = new Vue({
            el: "#app",
            data: {
                fruits: ["apple", "banana", "orange"],
                obj: [{
                        name: "1",
                        age: 10
                    },
                    {
                        name: "2",
                        age: 20
                    },

                    {
                        name: "3",
                        age: 30
                    },

                ]
            },

        })
    </script>
</body>

</html>
```



### 总结：

```
通用：
	v-xxx="变量名"
特殊：
	v-bind:xxx/class/style="[]/{}/变量名/三元表达式"
	
差值表达式：
	<div> {{ msg }}</div>
```





## 5. 常用特性

### 5.1 表单操作

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Document</title>
  <style type="text/css">
  
  form div {
    height: 40px;
    line-height: 40px;
  }
  form div:nth-child(4) {
    height: auto;
  }
  form div span:first-child {
    display: inline-block;
    width: 100px;
  }
  </style>
</head>
<body>
  <div id="app">
    <form action="http://itcast.cn">
      <div>
        <span>姓名：</span>
        <span>
          <input type="text" v-model='uname'>
        </span>
      </div>
      <div>
        <span>性别：</span>
        <span>
          <input type="radio" id="male" value="1" v-model='gender'>
          <label for="male">男</label>
          <input type="radio" id="female" value="2" v-model='gender'>
          <label for="female">女</label>
        </span>
      </div>
      <div>
        <span>爱好：</span>
       <!-- 
		1、 复选框需要同时通过v-model 双向绑定 一个值 
         2、 每一个复选框必须要有value属性  且value 值不能一样 
		3、 当某一个单选框选中的时候 v-model  会将当前的 value值 改变 data 中的数据hobby 的值就是选中的值，我们只需要实时监控他的值就可以了
		-->
        <input type="checkbox" id="ball" value="1" v-model='hobby'>
        <label for="ball">篮球</label>
        <input type="checkbox" id="sing" value="2" v-model='hobby'>
        <label for="sing">唱歌</label>
        <input type="checkbox" id="code" value="3" v-model='hobby'>
        <label for="code">写代码</label>
      </div>
      <div>
        <span>职业：</span>
        <select v-model='occupation' multiple>
          <option value="0">请选择职业...</option>
          <option value="1">教师</option>
          <option value="2">软件工程师</option>
          <option value="3">律师</option>
        </select>
      </div>
      <div>
        <span>个人简介：</span>
        <textarea v-model='desc'></textarea>
      </div>
      <div>
        <input type="submit" value="提交" @click.prevent='handle'>
      </div>
    </form>
  </div>
  <script type="text/javascript" src="js/vue.js"></script>
  <script type="text/javascript">
    /*
      表单基本操作
    */
    var vm = new Vue({
      el: '#app',
      data: {
        uname: 'lisi',
        gender: 2,
        hobby: ['2','3'],
        // occupation: 3
		// 需要是数组
        occupation: ['2','3'],
        desc: 'nihao'
      },
      methods: {
        handle: function(){
          // console.log(this.uname)
          // console.log(this.gender)
          // console.log(this.hobby.toString())
          // console.log(this.occupation)
          console.log(this.desc)

        }
      }
    });
  </script>
</body>
</html>
```



### 5.2 表单域修饰符

- .number  转换为数值
  - 当开始输入非数字的字符串时，因为Vue无法将字符串转换成数值
  - 所以属性值将实时更新成相同的字符串。即使后面输入数字，也将被视作字符串。
- .trim  自动过滤用户输入的首尾空白字符
- .lazy   将input事件切换成change事件
  - lazy 修饰符延迟了同步更新属性值的时机。即将原本绑定在 input 事件的同步逻辑转变为绑定在 change 事件上
  - 在失去焦点 或者 按下回车键时才更新

```vue 
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Document</title>
</head>
<body>
  <div id="app">
  
    <input type="text" v-model.number='age'>
    <input type="text" v-model.trim='info'>
    <input type="text" v-model.lazy='msg'>
	
    <div>{{msg}}</div>
    <button @click='handle'>点击</button>
  </div>
  <script type="text/javascript" src="js/vue.js"></script>
  <script type="text/javascript">
    /*
      表单域修饰符
    */
    var vm = new Vue({
      el: '#app',
      data: {
        age: '',
        info: '',
        msg: ''
      },
      methods: {
        handle: function(){
          // console.log(this.age + 13)
          // console.log(this.info.length)
        }
      }
    });
  </script>
</body>
</html>
```



### 5.3 自定义指令

   内置指令不能满足我们特殊的需求， Vue允许我们通过directive 自定义指令

- 注册全局指令

  ```vue
  <!DOCTYPE html>
  <html lang="en">
  <head>
    <meta charset="UTF-8">
    <title>Document</title>
  </head>
  <body>
    <div id="app">
      <input type="text" v-focus>
      <input type="text">
    </div>
    <script type="text/javascript" src="js/vue.js"></script>
    <script type="text/javascript">
      /*
        自定义指令
      */
      Vue.directive('focus', {
        inserted: function(el){
          // el表示指令所绑定的元素
          el.focus();
        }
      });
  	
      var vm = new Vue({
        el: '#app',
        data: {
          
        },
        methods: {
          handle: function(){
            
          }
        }
      });
    </script>
  </body>
  </html>
  ```
  
  

- 注册全局指令 带参数

  ```vue
  <!DOCTYPE html>
  <html lang="en">
  <head>
    <meta charset="UTF-8">
    <title>Document</title>
  </head>
  <body>
    <div id="app">
    
      <input type="text" v-color='msg'>
  	
    </div>
    <script type="text/javascript" src="js/vue.js"></script>
    <script type="text/javascript">
      /*
        自定义指令-带参数
      */
      Vue.directive('color', {
        bind: function(el, binding){
          // 根据指令的参数设置背景色
          // console.log(binding.value.color)
          el.style.backgroundColor = binding.value.color;
        }
  	  
      });
      var vm = new Vue({
        el: '#app',
        data: {
          msg: {
            color: 'blue'
          }
        },
        methods: {
          handle: function(){
            
          }
        }
      });
    </script>
  </body>
  </html>
  
  ```

  

- 注册局部指令

  ```vue
  <!DOCTYPE html>
  <html lang="en">
  <head>
    <meta charset="UTF-8">
    <title>Document</title>
  </head>
  <body>
    <div id="app">
      <input type="text" v-color='msg'>
      <input type="text" v-focus>
    </div>
    <script type="text/javascript" src="js/vue.js"></script>
    <script type="text/javascript">
      /*
        自定义指令-局部指令
      */
      var vm = new Vue({
        el: '#app',
        data: {
          msg: {
            color: 'red'
          }
        },
        methods: {
          handle: function(){
            
          }
        },
  	  
        directives: {
          color: {
            bind: function(el, binding){
              el.style.backgroundColor = binding.value.color;
            }
          },
  		
          focus: {
            inserted: function(el) {
              el.focus();
            }
          }
        }
      });
    </script>
  </body>
  </html>
  
  ```

  

### 5.4 计算属性

- 模板中放入太多的逻辑会让模板过重且难以维护  使用计算属性可以让模板更加的简洁
- computed 比较适合对多个变量或者对象进行处理后返回一个结果值，也就是数多个变量中的某一个值发生了变化则我们监控的这个值也就会发生变化
- **计算属性是基于它们的响应式依赖进行缓存的**
- 计算属性与方法的区别:   计算属性是基于依赖进行缓存的，而方法不缓存

```vue
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Document</title>
</head>
<body>
  <div id="app">
    <div>{{reverseString}}</div>
    <div>{{reverseString}}</div>
    <div>{{reverseMessage()}}</div>
    <div>{{reverseMessage()}}</div>
  </div>
  <script type="text/javascript" src="js/vue.js"></script>
  <script type="text/javascript">
    /*
      计算属性与方法的区别:计算属性是基于依赖进行缓存的，而方法不缓存
    */
    var vm = new Vue({
      el: '#app',
      data: {
        msg: 'Nihao',
        num: 100
      },
      methods: {
        reverseMessage: function(){
          console.log('methods')
          return this.msg.split('').reverse().join('');
        }
      },
      computed: {
        reverseString: function(){
          console.log('computed')
          // return this.msg.split('').reverse().join('');
          var total = 0;
          for(var i=0;i<=this.num;i++){
            total += i;
          }
          return total;
        }
      }
    });
  </script>
</body>
</html>
```



### 5.5 侦听器

- **一般用于异步或者开销较大的操作** , 这是侦听器和计算属性的区别
- watch 中的属性 **一定是 data 中 已经存在的数据** 
- 当需要监听一个**对象的改变**时，普通的watch方法无法监听到对象内部属性的改变，只有data中的数据才能够监听到变化，此时就需要deep属性对对象进行深度监听

侦听器 与 计算属性的对比

```vue
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Document</title>
</head>
<body>
  <div id="app">
    <div>
      <span>名：</span>
      <span>
        <input type="text" v-model='firstName'>
      </span>
    </div>
    <div>
      <span>姓：</span>
      <span>
        <input type="text" v-model='lastName'>
      </span>
    </div>
    <div>{{fullName}}</div>
  </div>
  <script type="text/javascript" src="js/vue.js"></script>
  <script type="text/javascript">
    /*
      侦听器 与 计算属性的对比
    */
    var vm = new Vue({
      el: '#app',
      data: {
        firstName: 'Jim',
        lastName: 'Green',
        // fullName: 'Jim Green'
      },
      computed: {
        fullName: function(){
          return this.firstName + ' ' + this.lastName;
        }
      },
      watch: {
        // firstName: function(val) {
        //   this.fullName = val + ' ' + this.lastName;
        // },
        // lastName: function(val) {
        //   this.fullName = this.firstName + ' ' + val;
        // }
      }
    });
  </script>
</body>
</html>

```



侦听器的使用案例

```vue
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Document</title>
</head>
<body>
  <div id="app">
    <div>
      <span>用户名：</span>
      <span>
        <input type="text" v-model.lazy='uname'>
      </span>
      <span>{{tip}}</span>
    </div>
  </div>
  <script type="text/javascript" src="js/vue.js"></script>
  <script type="text/javascript">
    /*      
      侦听器
      1、采用侦听器监听用户名的变化
      2、调用后台接口进行验证
      3、根据验证的结果调整提示信息
    */
    var vm = new Vue({
      el: '#app',
      data: {
        uname: '',
        tip: ''
      },
      methods: {
        checkName: function(uname) {
          // 调用接口，但是可以使用定时任务的方式模拟接口调用
          var that = this;
          setTimeout(function(){
            // 模拟接口调用
            if(uname == 'admin') {
              that.tip = '用户名已经存在，请更换一个';
            }else{
              that.tip = '用户名可以使用';
            }
          }, 2000);
            
          或者
   
          setTimeout(() => {
            // 模拟接口调用
            if(uname == 'admin') {
              that.tip = '用户名已经存在，请更换一个';
            }else{
              that.tip = '用户名可以使用';
            }
          }, 2000);
        }
      },
      watch: {
        uname: function(val){
          // 调用后台接口验证用户名的合法性
          this.checkName(val);
          // 修改提示信息
          this.tip = '正在验证...';
        }
      }
    });

  </script>
</body>
</html>
```



### 5.6 过滤器

- 基本过滤器

  ```vue
  <!DOCTYPE html>
  <html lang="en">
  <head>
    <meta charset="UTF-8">
    <title>Document</title>
  </head>
  <body>
    <div id="app">
      <input type="text" v-model='msg'>
      <div>{{msg | upper}}</div>
      <div>{{msg | upper | lower}}</div>
      <div :abc='msg | upper'>测试数据</div>
    </div>
    <script type="text/javascript" src="js/vue.js"></script>
    <script type="text/javascript">
      /*
        过滤器
        1、可以用与插值表达式和属性绑定
        2、支持级联操作
        3、val代表差值表达式中的传递的值
      */
      // Vue.filter('upper', function(val) {
      //   return val.charAt(0).toUpperCase() + val.slice(1);
      // });
      Vue.filter('lower', function(val) {
        return val.charAt(0).toLowerCase() + val.slice(1);
      });
  	
      var vm = new Vue({
        el: '#app',
        data: {
          msg: ''
        },
  	  
        filters: {
          upper: function(val) {
            return val.charAt(0).toUpperCase() + val.slice(1);
          }
        }
      });
    </script>
  </body>
  </html>
  ```



- 带参数的过滤器

  ```vue
  
  <!DOCTYPE html>
  <html lang="en">
  <head>
    <meta charset="UTF-8">
    <title>Document</title>
  </head>
  <body>
  
    <div id="app">
  -<div>{{date | format('yyyy-MM-dd hh:mm:ss')}}</div>
    </div>
    
    <script type="text/javascript" src="js/vue.js"></script>
    <script type="text/javascript">
      /*
        过滤器案例：格式化日期
        
      */
      // Vue.filter('format', function(value, arg) {
      //   if(arg == 'yyyy-MM-dd') {
      //     var ret = '';
      //     ret += value.getFullYear() + '-' + (value.getMonth() + 1) + '-' + value.getDate();
      //     return ret;
      //   }
      //   return value;
      // })
      Vue.filter('format', function(value, arg) {
        function dateFormat(date, format) {
            if (typeof date === "string") {
                var mts = date.match(/(\/Date\((\d+)\)\/)/);
                if (mts && mts.length >= 3) {
                    date = parseInt(mts[2]);
                }
            }
            date = new Date(date);
            if (!date || date.toUTCString() == "Invalid Date") {
                return "";
            }
            var map = {
                "M": date.getMonth() + 1, //月份 
                "d": date.getDate(), //日 
                "h": date.getHours(), //小时 
                "m": date.getMinutes(), //分 
                "s": date.getSeconds(), //秒 
                "q": Math.floor((date.getMonth() + 3) / 3), //季度 
                "S": date.getMilliseconds() //毫秒 
            };
  
            format = format.replace(/([yMdhmsqS])+/g, function(all, t) {
                var v = map[t];
                if (v !== undefined) {
                    if (all.length > 1) {
                        v = '0' + v;
                        v = v.substr(v.length - 2);
                    }
                    return v;
                } else if (t === 'y') {
                    return (date.getFullYear() + '').substr(4 - all.length);
                }
                return all;
            });
            return format;
        }
  	  
        return dateFormat(value, arg);
      })
  	
      var vm = new Vue({
        el: '#app',
        data: {
          date: new Date()
        }
      });
    </script>
  </body>
  </html>
  ```

  

### 5.7 生命周期

| beforeCreate  | 在实例初始化之后，数据观测和事件配置之前被调用 此时data 和 methods 以及页面的DOM结构都没有初始化   什么都做不了 |
| ------------- | ------------------------------------------------------------ |
| created       | 在实例创建完成后被立即调用此时data 和 methods已经可以使用  但是页面还没有渲染出来 |
| beforeMount   | 在挂载开始之前被调用   此时页面上还看不到真实数据 只是一个模板页面而已 |
| mounted       | el被新创建的vm.$el替换，并挂载到实例上去之后调用该钩子。  数据已经真实渲染到页面上  在这个钩子函数里面我们可以使用一些第三方的插件 |
| beforeUpdate  | 数据更新时调用，发生在虚拟DOM打补丁之前。   页面上数据还是旧的 |
| updated       | 由于数据更改导致的虚拟DOM重新渲染和打补丁，在这之后会调用该钩子。 页面上数据已经替换成最新的 |
| beforeDestroy | 实例销毁之前调用                                             |
| destroyed     | 实例销毁后调用                                               |



```vue

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Document</title>
</head>
<body>
  <div id="app">
    <div> {{msg}} </div>
    <button @click='update'>更新</button>
    <button @click='destroy'>销毁</button>
  </div>
    
  <script type="text/javascript" src="../js/vue.js"></script>
  <script type="text/javascript">
    /*
      写在methods 中 和 外面单独定义的区别：
          method 中的方法是在页面渲染后调用的；
          created 方法是在页面渲染时候调用的；	
    */
    var vm = new Vue({
      el: '#app',
      data: {
        msg: '生命周期'
      },
      methods: {
        update: function(){
          this.msg = 'hello';
        },
        destroy: function(){
          this.$destroy();
        }
      },
	  
      beforeCreate: function(){
        console.log('beforeCreate');
      },
      created: function(){
        console.log('created');
      },
      beforeMount: function(){
        console.log('beforeMount');
      },
      mounted: function(){
        console.log('mounted');
      },
      beforeUpdate: function(){
        console.log('beforeUpdate');
      },
      updated: function(){
        console.log('updated');
      },
      beforeDestroy: function(){
        console.log('beforeDestroy');
      },
      destroyed: function(){
        console.log('destroyed');
      }
    });
  </script>
</body>
</html>

```



### 5.8 变异方法和替换数组

在 Vue 中，直接修改**数组对象**属性的值无法触发响应式。当你直接修改了对象属性的值，你会发现，只有数据改了，但是页面内容并没有改变



变异方法

- 即保持数组方法原有功能不变的前提下对其进行功能拓展， 修改原有数据

| `push()`    | 往数组最后面添加一个元素，成功返回当前数组的长度             |
| ----------- | ------------------------------------------------------------ |
| `pop()`     | 删除数组的最后一个元素，成功返回删除元素的值                 |
| `shift()`   | 删除数组的第一个元素，成功返回删除元素的值                   |
| `unshift()` | 往数组最前面添加一个元素，成功返回当前数组的长度             |
| `splice()`  | 有三个参数，第一个是想要删除的元素的下标（必选），第二个是想要删除的个数（必选），第三个是删除 后想要在原位置替换的值 |
| `sort()`    | sort()  使数组按照字符编码默认从小到大排序,成功返回排序后的数组 |
| `reverse()` | reverse()  将数组倒序，成功返回倒序后的数组                  |



替换数组

- 不会改变原始数组，但总是返回一个新数组      

| filter | filter() 方法创建一个新的数组，新数组中的元素是通过检查指定数组中符合条件的所有元素。 |
| ------ | ------------------------------------------------------------ |
| map    | 方法返回一个新数组，数组中的元素为原始[数组元素](https://so.csdn.net/so/search?q=数组元素&spm=1001.2101.3001.7020)调用函数处理后的值 当数组为基础类型时原数组不变，当数组为引用类型时原数组发生改变,   避免原数组发生改变，扩展运算符   https://blog.csdn.net/Anna0115/article/details/103696124 |
| concat | concat() 方法用于连接两个或多个数组。该方法不会改变现有的数组 |
| slice  | slice() 方法可从已有的数组中返回选定的元素。该方法并不会修改数组，而是返回一个子数组 |



```vue
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Document</title>
</head>
<body>
  <div id="app">
    <div>
      <span>
        <input type="text" v-model='fname'>
        <button @click='add'>添加</button>
        <button @click='del'>删除</button>
        <button @click='change'>替换</button>
      </span>
    </div>
      
    <ul>
      <li :key='index' v-for='(item,index) in list'>{{item}}</li>
    </ul>
      
  </div>
  <script type="text/javascript" src="js/vue.js"></script>
  <script type="text/javascript">
    /*
      Vue数组操作
      1、变异方法：会影响数组的原始数据的变化。
      2、替换数组：不会影响原始的数组数据，而是形成一个新的数组。
    */
    var vm = new Vue({
      el: '#app',
      data: {
        fname: '',
        list: ['apple','orange','banana']
      },
	  
      methods: {
        add: function(){
          this.list.push(this.fname);
        },
        del: function(){
          this.list.pop();
        },
        change: function(){
          this.list = this.list.slice(0,2);
        }
      }
    });
  </script>
</body>
</html>
```



### 5.9 动态响应式数据处理

- Vue.set(a,b,c)    让触发视图重新更新一遍，数据做到响应式	
- vue.$set(a,b,c)
- a是要更改的对象名称 、b是要更改的对象的索引或者Key、c是要更改的对象具体的值

```vue

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Document</title>
</head>
<body>
  <div id="app">
    <ul>
      <li v-for='item in list'>{{item}}</li>
    </ul>
    <div>
      <div>{{info.name}}</div>
      <div>{{info.age}}</div>
      <div>{{info.gender}}</div>
    </div>
  </div>
  <script type="text/javascript" src="js/vue.js"></script>
  <script type="text/javascript">
    /*
      动态处理响应式数据
    */
    var vm = new Vue({
      el: '#app',
      data: {
        list: ['apple', 'orange', 'banana'],
        info: {
          name: 'lisi',
          age: 12
        }
      },
    });
    // vm.list[1] = 'lemon';
    // Vue.set(vm.list, 2, 'lemon');
    vm.$set(vm.list, 1, 'lemon');

    // vm.info.gender = 'male';
    vm.$set(vm.info, 'gender', 'female');
      
  </script>
</body>
</html>
```





## 6. 组件开发

### 6.1 组件注册

> 弄清楚哪个是父组件，子组件， 外层使用者是父组件，调用的内层组件是子组件， 在组件通信中有



#### 6.1.1 基本使用

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Document</title>
</head>
<body>

  <div id="app">
    <button-counter> </button-counter>
    <button-counter> </button-counter>
    <button-counter> </button-counter>
  </div>
  
  <script type="text/javascript" src="js/vue.js"></script>
  <script type="text/javascript">
    /*
      组件注册
    */
    Vue.component('button-counter', {
      data: function(){
        return {
          count: 0
        }
      },
      template: '<button @click="handle">点击了{{count}}次</button>',
      methods: {
        handle: function() {
          this.count += 2;
        }
      }
    })
	
    var vm = new Vue({
      el: '#app',
      data: {
        
      }
    });
  </script>
</body>
</html>
```



#### 6.1.2 全局注册

##### 注意事项

- 组件参数的data值必须是函数
- 组件模板必须是单个根元素
- 组件模板的内容可以是模板字符串(反引号里面写模板,  模板比较复杂，通过这可以比较直观)
- 如果使用驼峰式命名组件，那么在使用组件的时候，可以在字符串模板中用**驼峰的方式或者短中横线的方式**使用组件，但是
  在普通的标签模板中，必须使用**短中横线的方式**使用组件

```html
  <script type="text/javascript" src="js/vue.js"></script>
  <script type="text/javascript">
    /*
      组件注册注意事项
      1、组件参数的data值必须是函数
      2、组件模板必须是单个根元素
      3、组件模板的内容可以是模板字符串

    */
    // Vue.component('button-counter', {
    //   data: function(){
    //     return {
    //       count: 0
    //     }
    //   },
    //   template: '<div><button @click="handle">点击了{{count}}次</button><button>测试</button></div>',
    //   methods: {
    //     handle: function(){
    //       this.count += 2;
    //     }
    //   }
    // })
    // -----------------------------------
      
    // 全局定义子组件
    Vue.component('button-counter', {
      data: function(){
        return {
          count: 0
        }
      },
      template: `
        <div>
          <button @click="handle">点击了{{count}}次</button>
          <button>测试123</button>
        </div>
      `,
      methods: {
        handle: function(){
          this.count += 2;
        }
      }
    })
	
    var vm = new Vue({
      el: '#app',
      data: {
        
      }
    });
  </script>
```



##### 组件命名

- 如果使用驼峰式命名组件，那么在使用组件的时候，只能在模板字符串中用驼峰的方式使用组件(模板字符串可以用短横线的方式)，但是在普通的标签模板中，必须使用短横线的方式使用组件

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Document</title>
</head>
<body>
  <div id="app">
    <button-counter></button-counter>
    <hello-world></hello-world>
  </div>
  <script type="text/javascript" src="js/vue.js"></script>
  <script type="text/javascript">
    /*
      组件注册注意事项
      如果使用驼峰式命名组件，那么在使用组件的时候，只能在字符串模板中用驼峰的方式使用组件，但是
      在普通的标签模板中，必须使用短横线的方式使用组件
    */
    Vue.component('HelloWorld', {
      data: function(){
        return {
          msg: 'HelloWorld'
        }
      },
      template: '<div>{{msg}}</div>'
    });
	
    Vue.component('button-counter', {
      data: function(){
        return {
          count: 0
        }
      },
      template: `
        <div>
          <button @click="handle">点击了{{count}}次</button>
          <button>测试123</button>
          <HelloWorld></HelloWorld>
		  <hello-world></hello-world>
        </div>
      `,
      methods: {
        handle: function(){
          this.count += 2;
        }
      }
    })
    var vm = new Vue({
      el: '#app',
      data: {
        
      }
    });
  </script>
</body>
</html>

```





#### 6.1.3 局部注册

- 左侧是组件名，右侧是组件模板
- 局部组件只能在注册他的父组件(vue实例)中使用(**容易报错)

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Document</title>
</head>
<body>
  <div id="app">
    <hello-world></hello-world>
    <hello-tom></hello-tom>
    <hello-jerry></hello-jerry>
    <test-com></test-com>
  </div>
  <script type="text/javascript" src="js/vue.js"></script>
  <script type="text/javascript">
    
     /*
      	局部组件只能在注册他的父组件中使用, 下面会报错
    */
    Vue.component('test-com',{
      template: '<div>Test<hello-world></hello-world></div>'
    });
    
    // 局部定义子组件
    var HelloWorld = {
      data: function(){
        return {
          msg: 'HelloWorld'
        }
      },
      template: '<div>{{msg}}</div>'
    };
      
    var HelloTom = {
      data: function(){
        return {
          msg: 'HelloTom'
        }
      },
      template: '<div>{{msg}}</div>'
    };
      
    var HelloJerry = {
      data: function(){
        return {
          msg: 'HelloJerry'
        }
      },
      template: '<div>{{msg}}</div>'
    };
	
    var vm = new Vue({
      el: '#app',
      data: {
        
      },
      components: {
        'hello-world': HelloWorld,
        'hello-tom': HelloTom,
        'hello-jerry': HelloJerry
      }
    });
  </script>
</body>
</html>

```



### 6.2 组件通信

> 注意事项： 此处关注的是组件间传递数据
>
> data 和 props 的区别： 
>
> ​	子组件中的data数据，不是通过父组件传递的是子组件私有的，是可读可写的。
>
>    ​    子组件中的props数据，都是通过父组件传递给子组件的，是只读的。



#### 6.2.1 父传子

##### 方式一 

子组件内部通过props接收，并在template中使用

```html
// 父组件
<div id="app">
     
    <div>{{pmsg}}</div>
    <menu-item title='来自父组件的值'></menu-item>
     
  </div>
  
  <script type="text/javascript" src="js/vue.js"></script>
  <script type="text/javascript">
     
    /*
        父组件向子组件传值-基本使用
        子组件
    */
        Vue.component('menu-item', {
          props: ['title'],
          data: function() {
            return {
              msg: '子组件中数据'
            }
          },
          template: '<div>{{msg + "----" + title }}</div>'
        });

        var vm = new Vue({
          el: '#app',
          data: {
            pmsg: '父组件中内容'
          }
        });
      </script>
```



##### 方式二

父组件通过属性将值传递给子组件

```html
  <div id="app">
       
    <div>{{pmsg}}</div>
    <menu-item :title='ptitle' content='hello'></menu-item> 
       
  </div>
 
  <script type="text/javascript" src="js/vue.js"></script>
  <script type="text/javascript">
    /*
      父组件向子组件传值-基本使用
    */
    Vue.component('menu-item', {
      props: ['title', 'content'],
      data: function() {
        return {
          msg: '子组件本身的数据'
        }
      },
      template: '<div>{{msg + "----" + title + "-----" + content}}</div>'
    });
	
    var vm = new Vue({
      el: '#app',
      data: {
        pmsg: '父组件中内容',
        ptitle: '动态绑定属性'
      }
    });
  </script>
```



##### props命名规则

- 如果在props中使用驼峰形式，普通模板中需要使用短横线的形式

- 字符串模板中没有这个限制
- 没有遵循以上原则，不会报错，但是会有警告，效果显示不出来

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Document</title>
</head>
<body>
  <div id="app">
  
    <div>{{pmsg}}</div>
    <menu-item :menu-title='ptitle'></menu-item>
    <menu-item :menuTitle='ptitle'></menu-item>
	
  </div>
  <script type="text/javascript" src="js/vue.js"></script>
  <script type="text/javascript">
    /*
      父组件向子组件传值-props属性名规则
    */
    Vue.component('third-com', {
      props: ['testTile'],
      template: '<div>{{testTile}}</div>'
    });
	
    Vue.component('menu-item', {
      props: ['menuTitle'],
      template: `<div>{{menuTitle}} <third-com testTile="hello"></third-com> </div>`
    });
	
    var vm = new Vue({
      el: '#app',
      data: {
        pmsg: '父组件中内容',
        ptitle: '动态绑定属性'
      }
    });
  </script>
</body>
</html>

```



##### props值类型

- string
- number( :pnum='12'  和  pnum="12" 效果一样， 但是前面会转成Number, 支持运算，后面是字符串)
- boolean
- array
- object

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Document</title>
</head>
<body>
  <div id="app">
    <div>{{pmsg}}</div>
    <menu-item :pstr='pstr' :pnum='12' pboo='true' :parr='parr' :pobj='pobj'></menu-item>
  </div>
  <script type="text/javascript" src="js/vue.js"></script>
  <script type="text/javascript">
    /*
      父组件向子组件传值-props属性值类型
    */
    
    Vue.component('menu-item', {
      props: ['pstr','pnum','pboo','parr','pobj'],
      template: `
        <div>
          <div>{{pstr}}</div>
          <div>{{12 + pnum}}</div>
          <div>{{typeof pboo}}</div>
          <ul>
            <li :key='index' v-for='(item,index) in parr'>{{item}}</li>
          </ul>

          <span>{{pobj.name}}</span>
          <span>{{pobj.age}}</span>
        </div>
      `
    });
    var vm = new Vue({
      el: '#app',
      data: {
        pmsg: '父组件中内容',
        pstr: 'hello',
        parr: ['apple','orange','banana'],
        pobj: {
          name: 'lisi',
          age: 12
        }
      }
    });
  </script>
</body>
</html>
```



#### 6.2.2 子传父

props是单向数据流，只能从父组件流向子组件



步骤：

 1.  子组件通过自定义事件向父组件传递信息

     ```html
         Vue.component('menu-item', {
           props: ['parr'],
           template: `
             <div>
               <ul>
                 <li :key='index' v-for='(item,index) in parr'>{{item}}</li>
               </ul>
     		  
               <button @click='$emit("enlarge-text")'>扩大父组件中字体大小</button>
             </div>
           `
         });
     ```

     

 2.  父组件监听子组件的事件

     ```html
     <menu-item :parr='parr' @enlarge-text='handle'></menu-item>
     ```



example:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Document</title>
</head>
<body>
  <div id="app">
    <div :style='{fontSize: fontSize + "px"}'>{{pmsg}}</div>
    <menu-item :parr='parr' @enlarge-text='handle'></menu-item>
  </div>
  <script type="text/javascript" src="js/vue.js"></script>
  <script type="text/javascript">
    /*
      子组件向父组件传值-基本用法
      props传递数据原则：单向数据流
    */
    
    Vue.component('menu-item', {
      props: ['parr'],
      template: `
        <div>
          <ul>
            <li :key='index' v-for='(item,index) in parr'>{{item}}</li>
          </ul>
		  
          <button @click='$emit("enlarge-text")'>扩大父组件中字体大小</button>
        </div>
      `
    });
	
    var vm = new Vue({
      el: '#app',
      data: {
        pmsg: '父组件中内容',
        parr: ['apple','orange','banana'],
        fontSize: 10
      },
	  
      methods: {
        handle: function(){
          // 扩大字体大小
          this.fontSize += 5;
        }
      }
    });
  </script>
</body>
</html>
```



子组件给父组件传递数据

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Document</title>
</head>
<body>
  <div id="app">
    <div :style='{fontSize: fontSize + "px"}'>{{pmsg}}</div>
      
    <menu-item :parr='parr' @enlarge-text='handle($event)'></menu-item>
    
  </div>
  <script type="text/javascript" src="js/vue.js"></script>
  <script type="text/javascript">
    /*
      子组件向父组件传值-携带参数
    */
    
    Vue.component('menu-item', {
      props: ['parr'],
      template: `
        <div>
          <ul>
            <li :key='index' v-for='(item,index) in parr'>{{item}}</li>
          </ul>
          <button @click='$emit("enlarge-text", 5)'>扩大父组件中字体大小</button>
        </div>
      `
    });
	
    var vm = new Vue({
      el: '#app',
      data: {
        pmsg: '父组件中内容',
        parr: ['apple','orange','banana'],
        fontSize: 10
      },
      methods: {
        handle: function(val){
          // 扩大字体大小
          this.fontSize += val;
        }
      }
    });
  </script>
</body>
</html>
```



#### 6.2.3 兄弟之间

步骤：

 1.  创建单独的事件中心管理组件间的通信

     ```
     var hub = new Vue()
     ```

     

 2.   监听事件与销毁事件

      ```
      // 触发兄弟组件的事件
      hub.$emit('tom-event', 1);
      
      // 监听事件
      hub.$on('jerry-event', (val) => {
                this.num += val;
              });
      
      // 销毁事件
      hub.$off('tom-event');
      ```



example:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Document</title>
</head>
<body>

  <div id="app">
    <div>
      <button @click='handle'>销毁事件</button>
    </div>
	
    <test-tom></test-tom>
    <test-jerry></test-jerry>
	
  </div>
  
  
  <script type="text/javascript" src="js/vue.js"></script>
  <script type="text/javascript">
    /*
      兄弟组件之间数据传递
    */
	
    // 提供事件中心
    var hub = new Vue();

    Vue.component('test-tom', {
      data: function(){
        return {
          num: 0
        }
      },
      template: `
        <div>
          <div>TOM:{{num}}</div>
          <div>
            <button @click='handle'>点击</button>
          </div>
        </div>
      `,
      methods: {
        handle: function(){
          hub.$emit('jerry-event', 2);
        }
      },
      mounted: function() {
        // 监听事件
        hub.$on('tom-event', (val) => {
          this.num += val;
        });
      }
    });
	
    Vue.component('test-jerry', {
      data: function(){
        return {
          num: 0
        }
      },
      template: `
        <div>
          <div>JERRY:{{num}}</div>
          <div>
            <button @click='handle'>点击</button>
          </div>
        </div>
      `,
      methods: {
        handle: function(){
          // 触发兄弟组件的事件
          hub.$emit('tom-event', 1);
        }
      },
      mounted: function() {
        // 监听事件
        hub.$on('jerry-event', (val) => {
          this.num += val;
        });
      }
    });
	
    var vm = new Vue({
      el: '#app',
      data: {
        
      },
      methods: {
        handle: function(){
		 // 销毁事件
          hub.$off('tom-event');
          hub.$off('jerry-event');
        }
      }
    });
  </script>
</body>
</html>
```







### 6.3 组件插槽

- 组件的最大特性就是复用性，而用好插槽能大大提高组件的可复用能力
- 插槽就是Vue实现的一套内容分发的API，将<slot></slot>元素作为承载分发内容的出口。
- 仔细比较 组件插槽 和 组件嵌套的区别
  - 组件插槽  关注的重点是有了组件后更改差值表达式位置(局部)的**内容**
  - 组件嵌套  关注的重点是没有组件前整体的结构
- 主要作用： **父组件向子组件传递内容(模板)**
- 参考文档： https://www.jianshu.com/p/8f73d52edb54    
- 参考文档： https://www.jianshu.com/p/865293d60c98
- 参考文档： https://www.cnblogs.com/chinabin1993/p/9115396.html   推荐看



#### 6.3.1 匿名插槽

> 插槽就是Vue实现的一套内容分发的API，将<slot></slot>元素作为承载分发内容的出口

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Document</title>
</head>
<body>
    
  <div id="app">

    <alert-box></alert-box>
    <alert-box>有bug发生</alert-box>
    <alert-box>有一个警告</alert-box>
  </div>
    
  <script type="text/javascript" src="js/vue.js"></script>
  <script type="text/javascript">
    /*
      组件插槽：父组件向子组件传递内容
    */
    Vue.component('alert-box', {
      template: `
        <div>
          <strong>ERROR:</strong>
          <slot></slot>
        </div>
      `
    });
    var vm = new Vue({
      el: '#app',
      data: {
        
      }
    });
  </script>
</body>
</html>

```



#### 6.3.2 具名插槽

- 具有名字的插槽 
- 给 <slot> 中的 "name" 属性绑定元素
- template 类似一个容器,  可以填充多个具名插槽



示例1：  好像已经废弃了

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Document</title>
</head>
<body>
  <div id="app">
    <base-layout>
      <p slot='header'>标题信息</p>
      <p>主要内容1</p>
      <p>主要内容2</p>
      <p slot='footer'>底部信息信息</p>
    </base-layout>

	
	
    <base-layout>
	  // 为啥可以在其中用<p></p>  也可以用   <template slot='footer'> </template>
	  // template 只是临时包裹一下内容
      <template slot='header'>
        <p>标题信息1</p>
        <p>标题信息2</p>
      </template>
      <p>主要内容1</p>
      <p>主要内容2</p>
      <template slot='footer'>
        <p>底部信息信息1</p>
        <p>底部信息信息2</p>
      </template>
    </base-layout>
  </div>
  <script type="text/javascript" src="js/vue.js"></script>
  <script type="text/javascript">
    /*
      具名插槽
    */
    Vue.component('base-layout', {
      template: `
        <div>
          <header>
            <slot name='header'></slot>
          </header>
		  
          <main>
            <slot></slot>
          </main>
		  
          <footer>
            <slot name='footer'></slot>
          </footer>
        </div>
      `
    });
	
    var vm = new Vue({
      el: '#app',
      data: {
        
      }
    });
  </script>
</body>
</html>

```



示例2：现在推荐使用

```html
    <body>
        <div id='app'>
            <base-layout>
                <template v-slot:header>
                    <h1>标题</h1>
                </template>
                <template v-slot:default>
                    <p>A paragraph for the main content</p>
                    <p>And another one</p>
                </template>
                <template v-slot:footer>
                    <p>结尾</p>
                </template>
            </base-layout>
        </div>
        <script>
            var baseLayout = {
                template:`<div class="container">
                        <header>
                            <slot name="header"></slot>
                        </header>
                        <main>
                            <slot></slot>
                        </main>
                        <footer>
                            <slot name="footer"></slot>
                        </footer>
                        </div>`
            }
            var vm = new Vue({
                el:'#app',
                components:{
                    'base-layout':baseLayout
                }
            })
        </script>
    </body>
```



#### 6.3.3 作用域插槽

- 父组件对子组件进行加工处理， 在组件上的属性，可以在组件元素内使用
-  Vue2.6.0    v-slot  替换  slot-scope (v-slot:header="slotProps")

示例1： 

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Document</title>
</head>
<style type="text/css">
  .current {
    color: orange;
  }
</style>
    
    
<body>
  <div id="app">
    // 属性
    <fruit-list :list='list'>
      // 属性传递到组件内部，可以直接使用，slotProps 名字任意
      <template slot-scope='slotProps'>
        <strong v-if='slotProps.info.id==3' class="current">{{slotProps.info.name}}</strong>
        <span v-else>{{slotProps.info.name}}</span>
      </template>
    </fruit-list>
  </div>
  
  <script type="text/javascript" src="js/vue.js"></script>
  <script type="text/javascript">
    /*
      作用域插槽
    */
    Vue.component('fruit-list', {
      props: ['list'],
      template: `
        <div>
          <li :key='item.id' v-for='item in list'>
            <slot :info='item'>{{item.name}}</slot>
          </li>
        </div>
      `
    });
	
    var vm = new Vue({
      el: '#app',
      data: {
        list: [{
          id: 1,
          name: 'apple'
        },{
          id: 2,
          name: 'orange'
        },{
          id: 3,
          name: 'banana'
        }]
      }
    });
  </script>
  
</body>
</html>

```

示例2：

```
<div id="app">
    <child :lists="nameList">
        <template slot-scope="a">
            {{a}}
        </template>
    </child>
</div>
<script>
    Vue.component('child',{
        props:['lists'],
        template:`
            <div>
                <ul>
                    <li v-for="list in lists">
                        <slot :bbbbb="list"></slot>
                    </li>
                </ul>
            </div>
        `
    })

    let vm = new Vue({
        el:'#app',
        data:{
            nameList:[
            {id:1,name:'孙悟空'},
            {id:2,name:'猪八戒'},
            {id:3,name:'沙和尚'},
            {id:4,name:'唐僧'},
            {id:5,name:'小白龙'},
            ]
        }
    })
</script>


//result
{"bbbb"：{id:1,name:'孙悟空'},
 "bbbb"：{id:2,name:'猪八戒'},
 "bbbb"：{id:3,name:'沙和尚'},
 "bbbb"：{id:4,name:'唐僧'},
 "bbbb"：{id:5,name:'小白龙'}}
 
 
 
<child :lists="nameList">
        <template slot-scope="a">
            <div v-if='a.bbbbb.id==1'>你好：<span>{{a.bbbbb.name}}</span></div>
            <div v-else>{{a.bbbbb.name}}</div>
        </template>
</child>
```



示例3 ：

```html
    <body>
        <div id='app'>
            // 没有props
            <child>
                <template v-slot:header="slotProps">
                    // data中的数据
                    <p>{{slotProps.title}}</p>
                    <p>{{slotProps.summary}}</p>
                </template>
            </child>
        </div>
        <script>
            var child = {
                data(){
                    return {
                        title:'hello world',
                        summary:'学习作用域插槽'
                    }
                }, 
                template:`<div>
                     <header>
					   // 在插槽上暴露数据title和summary
                       <slot name="header" :title="title" :summary="summary"></slot>
                     </header>
                 </div>`

            }
            var vm = new Vue({
                el:'#app',
                components:{
                    child
                }
            })
        </script>
    </body>
```





## 7. 前端交互

### 7.1 异步编程

- ajax异步编程无法拿到想要的结果
- 多次异步请求，顺序无法保证
- 多次异步请求，有顺序要求，嵌套

```html

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Document</title>
</head>
<body>
  <div>前后端交互</div>
  <script type="text/javascript" src="js/jquery.js"></script>
  <script type="text/javascript">
    /*
      前后端交互-异步编程与Promise概述
    */
    // var ret = '---';
    // $.ajax({
    //   url: 'http://localhost:3000/data',
    //   success: function(data) {
    //     ret = data;
    //     console.log(ret)
    //   }
    // });
    // console.log(ret)

    // ----------------------------
    // $.ajax({
    //   url: 'http://localhost:3000/data',
    //   success: function(data) {
    //     console.log(data)
    //   }
    // });
    // $.ajax({
    //   url: 'http://localhost:3000/data1',
    //   success: function(data) {
    //     console.log(data)
    //   }
    // });
    // $.ajax({
    //   url: 'http://localhost:3000/data2',
    //   success: function(data) {
    //     console.log(data)
    //   }
    // });
    // -----------------------------------
    $.ajax({
      url: 'http://localhost:3000/data',
      success: function(data) {
        console.log(data)
        $.ajax({
          url: 'http://localhost:3000/data1',
          success: function(data) {
            console.log(data)
            $.ajax({
              url: 'http://localhost:3000/data2',
              success: function(data) {
                console.log(data)
              }
            });
          }
        });
      }
    });
  </script>
</body>
</html>
```



### 7.2 promise

promise是异步编程的解决方案



好处：

- 主要解决异步深层嵌套的问题(回调地狱)
- promise 提供了简洁的API  使得异步操作更加容易



#### 7.2.1 基本用法

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Document</title>
</head>
<body>
  
  <script type="text/javascript">
    /*
      Promise基本使用
    */
    // console.log(typeof Promise)
    // console.dir(Promise);

    var p = new Promise(function(resolve, reject){
      // 这里用于实现异步任务
      setTimeout(function(){
        var flag = false;
        
        if(flag) {
          // 正常情况
          resolve('hello');
        }else{
          // 异常情况
          reject('出错了');
        }
        
      }, 100);
    });
    p.then(function(data){
      console.log(data)
    },function(info){
      console.log(info)
    });
  </script>
</body>
</html>
```



#### 7.2.2 发送ajax请求

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Document</title>
</head>
<body>
  
  <script type="text/javascript">
    /*
      基于Promise发送Ajax请求
    */
    function queryData(url) {
      var p = new Promise(function(resolve, reject){
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function(){
          if(xhr.readyState != 4) return;
          if(xhr.readyState == 4 && xhr.status == 200) {
            // 处理正常的情况
            resolve(xhr.responseText);
          }else{
            // 处理异常情况
            reject('服务器错误');
          }
        };
        xhr.open('get', url);
        xhr.send(null);
      });
      return p;
    }
     
    // 发送单个ajax请求
    // queryData('http://localhost:3000/data')
    //   .then(function(data){
    //     console.log(data);
    //   },function(info){
    //     console.log(info)
    //   });

      
    // 发送多个ajax请求并且保证顺序
    queryData('http://localhost:3000/data')
      .then(function(data){
        console.log(data)
        return 	queryData('http://localhost:3000/data1');
      })
      .then(function(data){
        console.log(data);
        return queryData('http://localhost:3000/data2');
      })
      .then(function(data){
        console.log(data)
      });
      
  </script>
</body>
</html>
```

then中的返回值

```html
/*
   then参数中的函数返回值:
	1.返回promise实例对象(返回的实例对象会调用下一个then)
	2.返回普通值(返回的普通值会传递给下一个then,通过then参数中函数的参数接收该值， 会产生新的promise对象，保证链式调用)

	简言之：返回的对象对传给下一个then去调用, 返回的值会传给下个then做为参数
*/


  <script type="text/javascript">
    /*
      then参数中的函数返回值
    */
    function queryData(url) {
      return new Promise(function(resolve, reject){
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function(){
          if(xhr.readyState != 4) return;
          if(xhr.readyState == 4 && xhr.status == 200) {
            // 处理正常的情况
            resolve(xhr.responseText);
          }else{
            // 处理异常情况
            reject('服务器错误');
          }
        };
        xhr.open('get', url);
        xhr.send(null);
      });
    }
    queryData('http://localhost:3000/data')
      .then(function(data){
        return queryData('http://localhost:3000/data1');
      })
      .then(function(data){
        return new Promise(function(resolve, reject){
          setTimeout(function(){
            resolve(123);
          },1000)
        });
      })
      .then(function(data){
        return 'hello';
      })
      .then(function(data){
        console.log(data)
      })

  </script>
```





#### 7.2.3 实例方法

- then()
  - 得到异步任务正确的结果
- catch()
  - 获取异常信息
- finally()
  - 成功与否都会执行（不是正式标准） 

```html
  <script type="text/javascript">
    /*
      Promise常用API-实例方法
    */
    // console.dir(Promise);
    function foo() {
      return new Promise(function(resolve, reject){
        setTimeout(function(){
          // resolve(123);
          reject('error');
        }, 100);
      })
    }
    // foo()
    //   .then(function(data){
    //     console.log(data)
    //   })
    //   .catch(function(data){
    //     console.log(data)
    //   })
    //   .finally(function(){
    //     console.log('finished')
    //   });


    // 两种写法是等效的
    foo()
      .then(function(data){
        console.log(data)
      },function(data){
        console.log(data)
      })
      .finally(function(){
        console.log('finished')
      });
  </script>
```



#### 7.2.4 对象方法

- all()

  - 并发的处理多个异步任务，所有任务执行完成才能得到结果

  - Promise.all`方法接受一个数组作参数，数组中的对象（p1、p2、p3）均为promise实例（如果不是一个promise，该项会被用`Promise.resolve`转换为一个promise)。它的状态由这三个promise实例决定

- race()

  - 并发的处理多个异步任务，只要有一个任务执行完成就能得到结果

  - `Promise.race`方法同样接受一个数组作参数。当p1, p2, p3中有一个实例的状态发生改变（变为`fulfilled`或`rejected`），p的状态就跟着改变。并把第一个改变状态的promise的返回值，传给p的回调函数

```html
  <script type="text/javascript">
    /*
      Promise常用API-对象方法
    */
    // console.dir(Promise)
    function queryData(url) {
      return new Promise(function(resolve, reject){
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function(){
          if(xhr.readyState != 4) return;
          if(xhr.readyState == 4 && xhr.status == 200) {
            // 处理正常的情况
            resolve(xhr.responseText);
          }else{
            // 处理异常情况
            reject('服务器错误');
          }
        };
        xhr.open('get', url);
        xhr.send(null);
      });
    }

    var p1 = queryData('http://localhost:3000/a1');
    var p2 = queryData('http://localhost:3000/a2');
    var p3 = queryData('http://localhost:3000/a3');
    // Promise.all([p1,p2,p3]).then(function(result){
    //   console.log(result)
    // })
    Promise.race([p1,p2,p3]).then(function(result){
      console.log(result)
    })
  </script>
```



### 7.3 fetch

- 基于promise, 更加简单的数据获取方式，功能更加强大，更灵活，可以看做是xhr的升级版
- Fetch API是新的ajax解决方案，Fetch会返回Promise
- **fetch不是ajax的进一步封装，而是原生js，没有使用XMLHttpRequest对象**。

   

#### 7.3.1 基本使用

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Document</title>
</head>
<body>
  
  <script type="text/javascript">
    /*
      Fetch API 基本用法
    */
    fetch('http://localhost:3000/fdata').then(function(data){
      // text()方法属于fetchAPI的一部分，它返回一个Promise实例对象，用于获取后台返回的数据
      return data.text();
        
    }).then(function(data){
      //注意：这里才是最终数据， 因为上面返回的是一个promise对象
      console.log(data);
    })
  </script>
</body>
</html>
```

​	

#### 7.3.2 请求

常见配置选项：

- method(string): http请求方法，默认为get
- body(string): http的请求参数
- headers(string): http请求头，默认为0

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Document</title>
</head>
<body>
  <script type="text/javascript">
    /*
      Fetch API 调用接口传递参数
    */

    // GET参数传递-传统URL
    // fetch('http://localhost:3000/books?id=123', {
    //   method: 'get'
    // })
    //   .then(function(data){
    //     return data.text();
    //   }).then(function(data){
    //    注意： 这里才是最终数据
    //     console.log(data)
    //   });

    // GET参数传递-restful形式的URL
    // fetch('http://localhost:3000/books/456', {
    //   method: 'get'
    // })
    //   .then(function(data){
    //     return data.text();
    //   }).then(function(data){
    //    注意： 这里才是最终数据
    //     console.log(data)
    //   });

    // DELETE请求方式参数传递
    // fetch('http://localhost:3000/books/789', {
    //   method: 'delete'
    // })
    //   .then(function(data){
    //     return data.text();
    //   }).then(function(data){
    //     console.log(data)
    //   });

    // POST请求传参
    // fetch('http://localhost:3000/books', {
    //   method: 'post',
    //   body: 'uname=lisi&pwd=123',
    //   headers: {
    //     'Content-Type': 'application/x-www-form-urlencoded'
    //   }
    // })
    //   .then(function(data){
    //     return data.text();
    //   }).then(function(data){
    //     console.log(data)
    //   });

    // POST请求传参
    // fetch('http://localhost:3000/books', {
    //   method: 'post',
    //   body: JSON.stringify({
    //     uname: '张三',
    //     pwd: '456'
    //   }),
    //   headers: {
    //     'Content-Type': 'application/json'
    //   }
    // })
    //   .then(function(data){
    //     return data.text();
    //   }).then(function(data){
    //     console.log(data)
    //   });

    // PUT请求传参
    fetch('http://localhost:3000/books/123', {
      method: 'put',
      body: JSON.stringify({
        uname: '张三',
        pwd: '789'
      }),
      headers: {
        'Content-Type': 'application/json'
      }
    })
      .then(function(data){
        return data.text();
      }).then(function(data){
        console.log(data)
      });
  </script>
</body>
</html>
```



#### 7.3.3 响应

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Document</title>
</head>
<body>
  
  <script type="text/javascript">
    /*
      Fetch响应结果的数据格式：
      如果响应正常返回，我们首先看到的是一个response对象，其中包括返回的一堆原始字节，这些字节需要在收到后，需要我们通过调用方法将其转换为相应格式的数据，比如JSON，BLOB或者TEXT等等
    */
    fetch('http://localhost:3000/json').then(function(data){
      // return data.json();
      return data.text();
    }).then(function(data){
      // console.log(data.uname)
      // console.log(typeof data)
      var obj = JSON.parse(data);
      console.log(obj.uname,obj.age,obj.gender)
    })
  </script>
</body>
</html>
```



### 7.4 axios

- 基于promise用于浏览器和node.js的http客户端
- 能拦截请求和响应
- 自动转换JSON数据
- https://www.w3cschool.cn/jquti/jquti-rksl35xd.html



#### 7.4.1 基本用法

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Document</title>
</head>
<body>
  
  <script type="text/javascript" src="js/axios.js"></script>
  <script type="text/javascript">
    axios.get('http://localhost:3000/adata').then(function(ret){
      // 注意data属性是固定的用法，用于获取后台的实际数据
      // console.log(ret)
      console.log(ret.data)
    })
  </script>
</body>
</html>
```

#### 7.4.2 常用api

- get
- post
- put
- delete

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Document</title>
</head>
<body>
  
  <script type="text/javascript" src="js/axios.js"></script>
  <script type="text/javascript">
    /*
      axios请求参数传递
    */
    // axios get请求传参
    // axios.get('http://localhost:3000/axios?id=123').then(function(ret){
    //   console.log(ret.data)
    // })
      
    // axios.get('http://localhost:3000/axios/123').then(function(ret){
    //   console.log(ret.data)
    // })
    // axios.get('http://localhost:3000/axios', {
    //   params: {
    //     id: 789
    //   }
    // }).then(function(ret){
    //   console.log(ret.data)
    // })

    // axios delete 请求传参
    // axios.delete('http://localhost:3000/axios', {
    //   params: {
    //     id: 111
    //   }
    // }).then(function(ret){
    //   console.log(ret.data)
    // })

    // axios.post('http://localhost:3000/axios', {
    //   uname: 'lisi',
    //   pwd: 123
    // }).then(function(ret){
    //   console.log(ret.data)
    // })
      
    // var params = new URLSearchParams();
    // params.append('uname', 'zhangsan');
    // params.append('pwd', '111');
    // axios.post('http://localhost:3000/axios', params).then(function(ret){
    //   console.log(ret.data)
    // })

    // axios put 请求传参
    axios.put('http://localhost:3000/axios/123', {
      uname: 'lisi',
      pwd: 123
    }).then(function(ret){
      console.log(ret.data)
      console.log(ret.data.uname)
    })

  </script>
</body>
</html>
```



#### 7.4.3 全局配置

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Document</title>
</head>
<body>
  
  <script type="text/javascript" src="js/axios.js"></script>
  <script type="text/javascript">
    /*
      axios 响应结果与全局配置
    */
    // axios.get('http://localhost:3000/axios-json').then(function(ret){
    //   console.log(ret.data.uname)
    // })

    // 配置请求的基准URL地址
    axios.defaults.baseURL = 'http://localhost:3000/';
    // 配置请求头信息
    axios.defaults.headers['mytoken'] = 'hello';
    // 配置 超时时间
    axios.defaults.timeout = 2500;
    // 配置公共的请求头
    axios.defaults.headers.common['Authorization'] = AUTH_TOKEN;
    // 配置公共的 post 的 Content-Type
    axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
    
    
    axios.get('axios-json').then(function(ret){
      console.log(ret.data.uname)
    })
  </script>
</body>
</html>
```



#### 7.4.4 拦截器

- 请求拦截器
  - 请求拦截器的作用是在请求发送前进行一些操作,  例如在每个请求体里加上token，统一做了处理如果以后要改也非常容易
- 响应拦截器
  - 响应拦截器的作用是在接收到响应后进行一些操作, 例如在服务器返回登录状态失效，需要重新登录的时候，跳转到登录页

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Document</title>
</head>
<body>
  
  <script type="text/javascript" src="js/axios.js"></script>
  <script type="text/javascript">
    /*
      axios拦截器
    */
    // 拦截请求
    axios.interceptors.request.use(function(config) {
      console.log(config.url)
      config.headers.mytoken = 'nihao';
      return config;
    }, function(err){
      console.log(err)
    })
	// 拦截响应
    axios.interceptors.response.use(function(res) {
      // console.log(res)
      var data = res.data;
      return data;
    }, function(err){
      console.log(err)
    })
      
    axios.get('http://localhost:3000/adata').then(function(data){
      console.log(data)
    })
  </script>
</body>
</html>
```



### 7.5 async&await

- es7 引入的新语法，可以更加方便的进行一步操作

- async作为一个关键字放到函数前面
  - 任何一个`async`函数都会隐式返回一个`promise`
- `await`关键字只能在使用`async`定义的函数中使用
  -  await后面可以直接跟一个 Promise实例对象
  -  await函数不能单独使用
- **async/await 让异步代码看起来、表现起来更像同步代码**



```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Document</title>
</head>
<body>
  
  <script type="text/javascript" src="js/axios.js"></script>
  <script type="text/javascript">
    /*
      async/await处理多个异步任务
    */
    axios.defaults.baseURL = 'http://localhost:3000';

    async function queryData() {
      var info = await axios.get('async1');
      var ret = await axios.get('async2?info=' + info.data);
      return ret.data;
    }

    queryData().then(function(data){
      console.log(data)
    })
  </script>
</body>
</html>
```



## 8. 前端路由

vue中的路由指的是组件路由，即通过路由负责事件监听，触发事件后渲染不同的内容

spa:  整个网址只有一个页面，内容ajax局部更新，同时支持浏览器地址栏的前进和后退操作。（实现原理：基于url地址的Hash）

vue-router



### 8.1 简单实现

- 动态组件  <component :is="comName"></component>

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta http-equiv="X-UA-Compatible" content="ie=edge" />
    <title>Document</title>
    <!-- 导入 vue 文件 -->
    <script src="./lib/vue_2.5.22.js"></script>
  </head>
  <body>
    <!-- 被 vue 实例控制的 div 区域 -->
    <div id="app">
      <!-- 切换组件的超链接 -->
      <a href="#/zhuye">主页</a> 
      <a href="#/keji">科技</a> 
      <a href="#/caijing">财经</a>
      <a href="#/yule">娱乐</a>

      <!-- 根据 :is 属性指定的组件名称，把对应的组件渲染到 component 标签所在的位置 -->
      <!-- 可以把 component 标签当做是【组件的占位符】 -->
      <component :is="comName"></component>
    </div>

    <script>
      // #region 定义需要被切换的 4 个组件
      // 主页组件
      const zhuye = {
        template: '<h1>主页信息</h1>'
      }

      // 科技组件
      const keji = {
        template: '<h1>科技信息</h1>'
      }

      // 财经组件
      const caijing = {
        template: '<h1>财经信息</h1>'
      }

      // 娱乐组件
      const yule = {
        template: '<h1>娱乐信息</h1>'
      }
      // #endregion

      // #region vue 实例对象
      const vm = new Vue({
        el: '#app',
        data: {
          comName: 'zhuye'
        },
        // 注册私有组件
        components: {
          zhuye,
          keji,
          caijing,
          yule
        }
      })
      // #endregion

      // 监听 window 的 onhashchange 事件，根据获取到的最新的 hash 值，切换要显示的组件的名称
      window.onhashchange = function() {
        // 通过 location.hash 获取到最新的 hash 值
        console.log(location.hash);
        switch(location.hash.slice(1)){
          case '/zhuye':
            vm.comName = 'zhuye'
          break
          case '/keji':
            vm.comName = 'keji'
          break
          case '/caijing':
            vm.comName = 'caijing'
          break
          case '/yule':
            vm.comName = 'yule'
          break
        }
      }
    </script>
  </body>
</html>

```



### 8.2 基本使用

router-link

- <router-link>是路由中提供的标签，默认会被渲染为a标签

- to属性默认被渲染为href属性

- to属性的值会被渲染为#开头的hash地址

  

vue-router使用步骤：

1. 导入vue文件
2. 添加路由链接 router-link
3. 添加路由占位符
4. 定义组件
5. 创建路由实例对象并配置路由
6. 挂载路由实例到vue中

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta http-equiv="X-UA-Compatible" content="ie=edge" />
    <title>Document</title>
    <!-- 1.导入 vue 文件 -->
    <script src="./lib/vue_2.5.22.js"></script>
    <script src="./lib/vue-router_3.0.2.js"></script>
  </head>
  <body>

    <div id="app">
     <!-- 2. <router-link>是路由中提供的标签，默认会被渲染为a标签，to属性默认被渲染为href属性，to属				性的值会被渲染为#开头的hash地址
	-->
      <router-link to="/user">User</router-link>
      <router-link to="/register">Register</router-link>

      <!-- 3.路由占位符 
		    将来通过路由规则匹配到的组件，将会渲染到router-view所在的位置
	  -->
      <router-view></router-view>
    </div>

    <script>
      // 4. 定义组件
      const User = {
        template: '<h1>User 组件</h1>'
      }

      const Register = {
        template: '<h1>Register 组件</h1>'
      }

      // 5.创建路由实例对象并配置路由规则
      const router = new VueRouter({
      // 所有的路由规则
        routes: [
          { path: '/user', component: User },
          { path: '/register', component: Register }
        ]
      })

      // 创建 vm 实例对象
      const vm = new Vue({
        // 指定控制的区域
        el: '#app',
        data: {},
        // 6.挂载路由实例对象
        // router: router
        router
      })
    </script>
  </body>
</html>
```

补充：路由重定向(可以通过路由重定向为页面设置默认展示的组件)

```
var myRouter = new VueRouter({
    routes: [
        // path设置为/表示页面最初始的地址/ ,  redirect表示要被重定向的新地址，设置为一个路由即可
        { path:"/", redirect:"/user"},
        { path: "/user", component: User },
        { path: "/login", component: Login }
    ]
})
```



### 8.3 嵌套路由

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta http-equiv="X-UA-Compatible" content="ie=edge" />
    <title>Document</title>
    <!-- 导入 vue 文件 -->
    <script src="./lib/vue_2.5.22.js"></script>
    <script src="./lib/vue-router_3.0.2.js"></script>
  </head>
  <body>
    <!-- 被 vm 实例所控制的区域 
	     嵌套路由最关键的代码在于理解子级路由的概念：
		 比如: 我们有一个 /login的路由, 那么/login下面还可以添加子级路由，如:
		      /login/account
	          /login/phone
	-->
    <div id="app">
      <router-link to="/user">User</router-link>
      <router-link to="/register">Register</router-link>

      <!-- 路由占位符 -->
      <router-view></router-view>
    </div>

    <script>
      const User = {
        template: '<h1>User 组件</h1>'
      }

      const Register = {
        template: `<div>
          <h1>Register 组件</h1>
          <hr/>

          <!-- 子路由链接 -->
          <router-link to="/register/tab1">tab1</router-link>
          <router-link to="/register/tab2">tab2</router-link>

          <!-- 子路由的占位符 -->
          <router-view />
        <div>`
      }

      const Tab1 = {
        template: '<h3>tab1 子组件</h3>'
      }

      const Tab2 = {
        template: '<h3>tab2 子组件</h3>'
      }

      // 创建路由实例对象
      const router = new VueRouter({
        // 所有的路由规则
        routes: [
          { path: '/', redirect: '/user'},
          { path: '/user', component: User },
          // children 数组表示子路由规则
          { 
			  path: '/register', 
			  component: Register, 
			  children: [
				{ path: '/register/tab1', component: Tab1 },
				{ path: '/register/tab2', component: Tab2 }
			  ] 
		  }
        ]
      })

      // 创建 vm 实例对象
      const vm = new Vue({
        // 指定控制的区域
        el: '#app',
        data: {},
        // 挂载路由实例对象
        // router: router
        router
      })
    </script>
  </body>
</html>

```



### 8.4 动态路由

#### 8.4.1 动态路径参数(url传参)

```
// 设置动态路径参数
var myRouter = new VueRouter({
    routes: [
        // 动态路径参数
        { path: "/user/:id", component: User },
        ]
	}]

// 获取动态路径参数
const User = {
        template: '<h1>User 组件 -- 用户id为: {{$route.params.id}}</h1>'
      }
```

example: 	

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta http-equiv="X-UA-Compatible" content="ie=edge" />
    <title>Document</title>
    <!-- 导入 vue 文件 -->
    <script src="./lib/vue_2.5.22.js"></script>
    <script src="./lib/vue-router_3.0.2.js"></script>
  </head>
  <body>
    <!-- 被 vm 实例所控制的区域 -->
    <div id="app">
      <router-link to="/user/1">User1</router-link>
      <router-link to="/user/2">User2</router-link>
      <router-link to="/user/3">User3</router-link>
      <router-link to="/register">Register</router-link>

      <!-- 路由占位符 -->
      <router-view></router-view>
    </div>

    <script>
      const User = {
        template: '<h1>User 组件 -- 用户id为: {{$route.params.id}}</h1>'
      }

      const Register = {
        template: '<h1>Register 组件</h1>'
      }

      // 创建路由实例对象
      const router = new VueRouter({
        // 所有的路由规则
        routes: [
          { path: '/', redirect: '/user'},
          { path: '/user/:id', component: User },
          { path: '/register', component: Register }
        ]
      })

      // 创建 vm 实例对象
      const vm = new Vue({
        // 指定控制的区域
        el: '#app',
        data: {},
        // 挂载路由实例对象
        // router: router
        router
      })
    </script>
  </body>
</html>

```

#### 8.4.2 路由组件参数

- 方式一： props值为bool

  ```html
  <!DOCTYPE html>
  <html lang="en">
    <head>
      <meta charset="UTF-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      <meta http-equiv="X-UA-Compatible" content="ie=edge" />
      <title>Document</title>
      <!-- 导入 vue 文件 -->
      <script src="./lib/vue_2.5.22.js"></script>
      <script src="./lib/vue-router_3.0.2.js"></script>
    </head>
    <body>
      <!-- 被 vm 实例所控制的区域 -->
      <div id="app">
        <router-link to="/user/1">User1</router-link>
        <router-link to="/user/2">User2</router-link>
        <router-link to="/user/3">User3</router-link>
        <router-link to="/register">Register</router-link>
  
        <!-- 路由占位符 -->
        <router-view></router-view>
      </div>
  
      <script>
        const User = {
          props: ['id'],
          template: '<h1>User 组件 -- 用户id为: {{id}}</h1>'
        }
  
        const Register = {
          template: '<h1>Register 组件</h1>'
        }
  
        // 创建路由实例对象
        const router = new VueRouter({
          // 所有的路由规则
          routes: [
            { path: '/', redirect: '/user'},
            { path: '/user/:id', component: User, props: true },
            { path: '/register', component: Register }
          ]
        })
  
        // 创建 vm 实例对象
        const vm = new Vue({
          // 指定控制的区域
          el: '#app',
          data: {},
          // 挂载路由实例对象
          // router: router
          router
        })
      </script>
    </body>
  </html>
  ```

  

- 方式二： props值为对象(此时接收不到id值， 对象传递了哪些，就能就收哪些)

  ```html
  <!DOCTYPE html>
  <html lang="en">
    <head>
      <meta charset="UTF-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      <meta http-equiv="X-UA-Compatible" content="ie=edge" />
      <title>Document</title>
      <!-- 导入 vue 文件 -->
      <script src="./lib/vue_2.5.22.js"></script>
      <script src="./lib/vue-router_3.0.2.js"></script>
    </head>
    <body>
      <!-- 被 vm 实例所控制的区域 -->
      <div id="app">
        <router-link to="/user/1">User1</router-link>
        <router-link to="/user/2">User2</router-link>
        <router-link to="/user/3">User3</router-link>
        <router-link to="/register">Register</router-link>
  
        <!-- 路由占位符 -->
        <router-view></router-view>
      </div>
  
      <script>
        const User = {
          props: ['id', 'uname', 'age'],
          template: '<h1>User 组件 -- 用户id为: {{id}} -- 姓名为:{{uname}} -- 年龄为：{{age}}</h1>'
        }
  
        const Register = {
          template: '<h1>Register 组件</h1>'
        }
  
        // 创建路由实例对象
        const router = new VueRouter({
          // 所有的路由规则
          routes: [
            { path: '/', redirect: '/user'},
            { path: '/user/:id', component: User, props: { uname: 'lisi', age: 20 } },
            { path: '/register', component: Register }
          ]
        })
  
        // 创建 vm 实例对象
        const vm = new Vue({
          // 指定控制的区域
          el: '#app',
          data: {},
          // 挂载路由实例对象
          // router: router
          router
        })
      </script>
    </body>
  </html>
  
  ```

  

- 方式三： props值为函数形式(想要获取传递的参数值还想要获取传递的对象数据(比如id))

  ```html
  <!DOCTYPE html>
  <html lang="en">
    <head>
      <meta charset="UTF-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      <meta http-equiv="X-UA-Compatible" content="ie=edge" />
      <title>Document</title>
      <!-- 导入 vue 文件 -->
      <script src="./lib/vue_2.5.22.js"></script>
      <script src="./lib/vue-router_3.0.2.js"></script>
    </head>
    <body>
      <!-- 被 vm 实例所控制的区域 -->
      <div id="app">
        <router-link to="/user/1">User1</router-link>
        <router-link to="/user/2">User2</router-link>
        <router-link to="/user/3">User3</router-link>
        <router-link to="/register">Register</router-link>
  
        <!-- 路由占位符 -->
        <router-view></router-view>
      </div>
  
      <script>
        const User = {
          props: ['id', 'uname', 'age'],
          template: '<h1>User 组件 -- 用户id为: {{id}} -- 姓名为:{{uname}} -- 年龄为：{{age}}</h1>'
        }
  
        const Register = {
          template: '<h1>Register 组件</h1>'
        }
  
        // 创建路由实例对象
        const router = new VueRouter({
          // 所有的路由规则
          routes: [
            { path: '/', redirect: '/user' },
            {
              path: '/user/:id',
              component: User,
              props: route => ({ uname: 'zs', age: 20, id: $route.params.id })
            },
            { path: '/register', component: Register }
          ]
        })
  
        // 创建 vm 实例对象
        const vm = new Vue({
          // 指定控制的区域
          el: '#app',
          data: {},
          // 挂载路由实例对象
          // router: router
          router
        })
      </script>
    </body>
  </html>
  ```

  



### 8.5 命名路由

> 命名路由： 给路由取别名
>
> <router-link :to="{ name: 'user', params: {id: 3} }">User3</router-link>
>  <router-link :to="{ path: '/news', query: { userId: 1111}}">user4</router-link>

```
  // 创建路由实例对象
      const router = new VueRouter({
      	// 所有的路由规则
        routes: [
          {
            // 命名路由, 给路由起个别名
            name: 'user',
            path: '/user/:id',
            component: User,
            props: route => ({ uname: 'zs', age: 20, id: route.params.id })
          },
        ]
      })
```

example: 

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta http-equiv="X-UA-Compatible" content="ie=edge" />
    <title>Document</title>
    <!-- 导入 vue 文件 -->
    <script src="./lib/vue_2.5.22.js"></script>
    <script src="./lib/vue-router_3.0.2.js"></script>
  </head>
  <body>
    <!-- 被 vm 实例所控制的区域 -->
    <div id="app">
      <router-link to="/user/1">User1</router-link>
      <router-link to="/user/2">User2</router-link>
       <!-- 方式1 命名路由  get-->
      <router-link :to="{ name: 'user', params: {id: 3} }">User3</router-link>
        <!--方式2 普通路由  post -->
      <router-link :to="{ path: '/news', query: { userId: 1111}}">user4</router-link>
        
        <template>
          <div>
            this is the news page.the transform param is {{this.$route.query.userId}}
          </div>
        </template>
      <router-link to="/register">Register</router-link>

      <!-- 路由占位符 -->
      <router-view></router-view>
    </div>

    <script>
      const User = {
        props: ['id', 'uname', 'age'],
        template: '<h1>User 组件 -- 用户id为: {{id}} -- 姓名为:{{uname}} -- 年龄为：{{age}}</h1>'
      }

      const Register = {
        template: '<h1>Register 组件</h1>'
      }

      // 创建路由实例对象
      const router = new VueRouter({
        routes: [
          { path: '/', redirect: '/user' },
          {
            // 命名路由, 给路由起个名字
            name: 'user',
            path: '/user/:id',
            component: User,
            props: route => ({ uname: 'zs', age: 20, id: route.params.id })
          },
          { path: '/register', component: Register }
        ]
      })

      // 创建 vm 实例对象
      const vm = new Vue({
        // 指定控制的区域
        el: '#app',
        data: {},
        // 挂载路由实例对象
        // router: router
        router
      })
    </script>
  </body>
</html>

```



### 8.6 编程式导航

声明式导航：通过点击链接的方式实现的导航

编程式导航：调用js的api方法实现导航

```
Vue-Router中常见的导航方式：
// router.push() 格式
this.$router.push("hash地址");
// 字符串
this.$router.push("/login");
// 命名的路由(传递参数)， /user/123
this.$router.push({ name:'user' , params: {id:123} });
// 查询参数， /user?username=jack
this.$router.push({ path:"/login", query:{username:"jack"} });

// router.go() 格式
this.$router.go( n );//n为数字
this.$router.go( -1 );



$route和$router的区别：
	https://www.jianshu.com/p/758bde4d9c2e
    https://blog.csdn.net/benben513624/article/details/86657492
    https://www.cnblogs.com/czy960731/p/9288830.html
    https://segmentfault.com/a/1190000022666268

    $router是全局的路由实例，任何页面都可以调用push(),replace(),go()等方法， 
    $route是当前的路由信息，可以获取到当前的path, name, params, query等，
    在我们进行路由跳转的时候，我们就会用到 router, 当我们去取路径的参数值时。我们就用route
```



example:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta http-equiv="X-UA-Compatible" content="ie=edge" />
    <title>Document</title>
    <!-- 导入 vue 文件 -->
    <script src="./lib/vue_2.5.22.js"></script>
    <script src="./lib/vue-router_3.0.2.js"></script>
  </head>
  <body>
    <!-- 被 vm 实例所控制的区域 -->
    <div id="app">
      <router-link to="/user/1">User1</router-link>
      <router-link to="/user/2">User2</router-link>
      <router-link :to="{ name: 'user', params: {id: 3} }">User3</router-link>
      <router-link to="/register">Register</router-link>

      <!-- 路由占位符 -->
      <router-view></router-view>
    </div>

    <script>
      const User = {
        props: ['id', 'uname', 'age'],
        template: `<div>
          <h1>User 组件 -- 用户id为: {{id}} -- 姓名为:{{uname}} -- 年龄为：{{age}}</h1>
          <button @click="goRegister">跳转到注册页面</button>
        </div>`,
        methods: {
          goRegister() {
             // 编程式导航
            this.$router.push('/register')
          }
        },
      }

      const Register = {
        template: `<div>
          <h1>Register 组件</h1>
          <button @click="goBack">后退</button>
        </div>`,
        methods: {
          goBack() {
            // 编程式导航
            this.$router.go(-1)
          }
        }
      }

      // 创建路由实例对象
      const router = new VueRouter({
        // 所有的路由规则
        routes: [
          { path: '/', redirect: '/user' },
          {
            // 命名路由
            name: 'user',
            path: '/user/:id',
            component: User,
            props: route => ({ uname: 'zs', age: 20, id: route.params.id })
          },
          { path: '/register', component: Register }
        ]
      })

      // 创建 vm 实例对象
      const vm = new Vue({
        // 指定控制的区域
        el: '#app',
        data: {},
        // 挂载路由实例对象
        // router: router
        router
      })
    </script>
  </body>
</html>

```



### 8.7 钩子函数

```
1. 参考文档： https://www.cnblogs.com/qdlhj/p/9838426.html

2. beforeEach
router.beforeEach((to, from, next) => {
  if (to.name) {
    next()
  } else {
    next(false)
  }
  
  
    // 如果用户访问的登录页，直接放行
    if (to.path === '/login') return next()
    // 从 sessionStorage 中获取到 保存的 token 值
    const tokenStr = window.sessionStorage.getItem('token')
    // 没有token，强制跳转到登录页
    if (!tokenStr) return next('/login')
        next()
    })
    
})

to:   Route: 即将要进入的目标路由对象
from: Route: 当前导航正要离开的路由
next: Function: 一定要调用该方法来 resolve 这个钩子。执行效果依赖 next 方法的调用参数。

场景： 一般用来做一些进入页面的限制， 和 meta 结合
案例： https://www.cnblogs.com/Rivend/p/11984321.html	
```





## 9. 前端工程化

### 9.1 模块化分类

```
推荐使用ES6模块化，因为AMD，CMD局限使用与浏览器端，而CommonJS在服务器端使用。ES6模块化是浏览器端和服务器端通用的规范.

ES6模块化规范中定义：
    1).每一个js文件都是独立的模块
    2).导入模块成员使用import关键字
    3).暴露模块成员使用export关键字
```



### 9.2 安装babel

```
npm install --save-dev @babel/core @babel/cli @babel/preset-env @babel/node
npm install --save @babel/polyfill

// 创建babel.config.js
const presets = [
        ["@babel/env",{
            targets:{
                edge:"17",
                firefox:"60",
                chrome:"67",
                safari:"11.1"
            }
        }]
    ]
module.exports = { presets }

// 创建index.js文件
console.log("ok");

//运行index.js
npx babel-node ./index.js
```



### 9.3  默认导入导出

```
//格式： export default {
    成员A,
    成员B,
}

let num = 100;
export default{
    num
}


//格式： import 接收名称 from "模块标识符"
import test from "./test.js"



注意： 
	在一个模块中，只允许使用export default向外默认暴露一次成员，千万不要写多个export default;
    如果在一个模块中没有向外暴露成员(没有使用export)，其他模块引入该模块时将会得到一个空对象 
```



### 9.4 按需导入导出

> 按需导入导出和默认导入导出不会冲突

```
export let num = 998;
export let myName = "jack";
export function fn = function(){ console.log("fn") }

// 按需导入起别名
import { num, fn as printFn, myName } from "./test.js"
// 同时导入默认导出的成员以及按需导入的成员
import test,{ num, fn as printFn, myName } from "./test.js"
```



### 9.5 直接导入并执行

```
import "./test2.js";
```



### 9.6 webpack

#### 9.6.1 概述

```
webpack是一个流行的前端项目构建工具，可以解决目前web开发的困境。
webpack提供了模块化支持，代码压缩混淆，解决js兼容问题，性能优化等特性，提高了开发效率和项目的可维护性
```

#### 9.6.2 基本使用

1. 创建项目目录并初始化
2. 创建src，并创建index.html， index.js
3. 安装jQuery
4. 导入jquery
5. 安装webpack

```
npm init -y

src/index.html
src/index.js

npm install jQuery -S

// 打开index.js文件，编写代码导入jQuery并实现功能：
import $ from "jquery";
$(function(){
    $("li:odd").css("background","cyan");
    $("li:odd").css("background","pink");
})

// 注意：此时项目运行会有错误，因为import $ from "jquery";这句代码属于ES6的新语法代码，在浏览器中可能会存在兼容性问题, 所以我们需要webpack来帮助我们解决这个问题。


// 安装webpack
1)打开项目目录终端，输入命令:

npm install webpack webpack-cli -D

2)然后在项目根目录中，创建一个 webpack.config.js 的配置文件用来配置webpack
在 webpack.config.js 文件中编写代码进行webpack配置，如下：

module.exports = {
    mode:"development"   
}

补充：mode设置的是项目的编译模式。
如果设置为development则表示项目处于开发阶段，不会进行压缩和混淆，打包速度会快一些
如果设置为production则表示项目处于上线发布阶段，会进行压缩和混淆，打包速度会慢一些

3)修改项目中的package.json文件 添加运行脚本dev ，如下：

"scripts":{
    "dev":"webpack"
}

注意：scripts节点下的脚本，可以通过npm run 运行, 并打包，比如：npm run dev

4)运行dev命令进行项目打包，并在页面中引入项目打包生成的js文件

npm run dev

等待webpack打包完毕之后，找到默认的dist路径中生成的main.js文件，将其引入到html页面中。
浏览页面查看效果。
```



#### 9.6.3 配置打包入口和出口

```
在webpack 4.x中，默认会将src/index.js 作为默认的打包入口js文件
                默认会将dist/main.js 作为默认的打包输出js文件
如果不想使用默认的入口/出口js文件，我们可以通过改变 webpack.config.js 来设置入口/出口的js文件，如下：

const path = require("path");
module.exports = {
    mode:"development",
    //设置入口文件路径
    entry: path.join(__dirname,"./src/xx.js"),
    //设置出口文件
    output:{
        //设置路径
        path:path.join(__dirname,"./dist"),
        //设置文件名
        filename:"res.js"
    }
}
```



#### 9.6.4 配置自动打包

```
默认情况下，我们更改入口js文件的代码，需要重新运行命令打包webpack，才能生成出口的js文件
那么每次都要重新执行命令打包，这是一个非常繁琐的事情，那么，自动打包可以解决这样繁琐的操作。

实现自动打包功能的步骤如下：
    A.安装自动打包功能的包:webpack-dev-server
        npm install webpack-dev-server -D
        
    B.修改package.json中的dev指令如下：
        "scripts":{
            "dev":"webpack-dev-server"
        }
        
    C.将引入的js文件路径更改为：<script src="/bundle.js"></script>
    D.运行npm run dev，进行打包
    E.打开网址查看效果：http://localhost:8080


注意：webpack-dev-server自动打包的输出文件，默认放到了服务器的根目录中.  放在内存中，看不到
补充：在自动打包完毕之后，默认打开服务器网页，实现方式就是打开package.json文件，修改dev命令：
	"scripts":{
            "dev": "webpack-dev-server --open --host 127.0.0.1 --port 9999"
        }
```

#### 9.6.5 配置预览页面

```
使用html-webpack-plugin 可以生成一个预览页面。
因为当我们访问默认的 http://localhost:8080/的时候，看到的是一些文件和文件夹，想要查看我们的页面
还需要点击文件夹点击文件才能查看，那么我们希望默认就能看到一个页面，而不是看到文件夹或者目录。

实现默认预览页面功能的步骤如下：
    A.安装默认预览功能的包:html-webpack-plugin
    
        npm install html-webpack-plugin -D
        
    B.修改webpack.config.js文件，如下：
        //导入包
        const HtmlWebpackPlugin = require("html-webpack-plugin");
        
        //创建对象
        const htmlPlugin = new HtmlWebpackPlugin({
            //设置生成预览页面的模板文件
            template:"./src/index.html",
            //设置生成的预览页面名称
            filename:"index.html"
        })
        
    C.继续修改webpack.config.js文件，添加plugins信息：
        module.exports = {
            plugins:[ htmlPlugin ]
        }
```



#### 9.6.6 loader(**)

```
通过loader打包非js模块：默认情况下，webpack只能打包js文件，如果想要打包非js文件，需要调用loader加载器才能打包
    loader加载器包含：
        1).less-loader
        2).sass-loader
        3).url-loader:打包处理css中与url路径有关的文件
        4).babel-loader:处理高级js语法的加载器
        5).postcss-loader
        6).css-loader,style-loader

注意：指定多个loader时的顺序是固定的，而调用loader的顺序是从后向前进行调用


//1. 安装style-loader,css-loader来处理css文件打包
	1).安装包
	
      npm install style-loader css-loader -D
      
    2).配置规则：更改webpack.config.js的module中的rules数组
    module.exports = {
        plugins:[ htmlPlugin],
        module : {
            rules:[
                {
                    //test设置需要匹配的文件类型，支持正则
                    test:/\.css$/,
                    //use表示该文件类型需要调用的loader
                    //use数组中指定的Loader顺序是固定的
                    //多个loader的调用顺序是：从后往前调用
                    use:['style-loader','css-loader']
                }
            ]
        }
    }

//2. 安装less,less-loader处理less文件
	1).安装包
        npm install less-loader less -D
    2).配置规则：更改webpack.config.js的module中的rules数组
    module.exports = {
        plugins:[ htmlPlugin ],
        module : {
            rules:[
                {
                    //test设置需要匹配的文件类型，支持正则
                    test:/\.css$/,
                    //use表示该文件类型需要调用的loader
                    use:['style-loader','css-loader']
                },
                {
                    test:/\.less$/,
                    use:['style-loader','css-loader','less-loader']
                }
            ]
        }
    }
    
    
    
//3. 安装sass-loader,node-sass处理less文件
    1).安装包
        npm install sass-loader node-sass -D
    2).配置规则：更改webpack.config.js的module中的rules数组
    module.exports = {
        ......
        plugins:[ htmlPlugin ],
        module : {
            rules:[
                {
                    //test设置需要匹配的文件类型，支持正则
                    test:/\.css$/,
                    //use表示该文件类型需要调用的loader
                    use:['style-loader','css-loader']
                },
                {
                    test:/\.less$/,
                    use:['style-loader','css-loader','less-loader']
                },
                {
                    test:/\.scss$/,
                    use:['style-loader','css-loader','sass-loader']
                }
            ]
        }
    }

    补充：安装sass-loader失败时，大部分情况是因为网络原因，详情参考：
    https://segmentfault.com/a/1190000010984731?utm_source=tag-newest
    

//4. 安装post-css自动添加css的兼容性前缀（-ie-,-webkit-）   很重要
    1).安装包
        npm install postcss-loader autoprefixer -D
        
    2).在项目根目录创建并配置 postcss.config.js 文件
    
    const autoprefixer = require("autoprefixer");
    module.exports = {
        plugins:[ autoprefixer ]
    }
    
    3).配置规则：更改webpack.config.js的module中的rules数组
    module.exports = {

        plugins:[ htmlPlugin ],
        module : {
            rules:[
                {
                    //test设置需要匹配的文件类型，支持正则
                    test:/\.css$/,
                    //use表示该文件类型需要调用的loader
                    use:['style-loader','css-loader','postcss-loader']
                },
                {
                    test:/\.less$/,
                    use:['style-loader','css-loader','less-loader']
                },
                {
                    test:/\.scss$/,
                    use:['style-loader','css-loader','sass-loader']
                }
            ]
        }
    }
    
    
//5. 打包样式表中的图片以及字体文件
	在样式表css中有时候会设置背景图片和设置字体文件，一样需要loader进行处理
	使用url-loader和file-loader来处理打包图片文件以及字体文件

    1).安装包
    
        npm install url-loader file-loader -D
        
    2).配置规则：更改webpack.config.js的module中的rules数组
    module.exports = {
        plugins:[ htmlPlugin],
        module : {
            rules:[
                {
                    //test设置需要匹配的文件类型，支持正则
                    test:/\.css$/,
                    //use表示该文件类型需要调用的loader
                    use:['style-loader','css-loader','postcss-loader']
                },
                {
                    test:/\.less$/,
                    use:['style-loader','css-loader','less-loader']
                },
                {
                    test:/\.scss$/,
                    use:['style-loader','css-loader','sass-loader']
                },
                
                {
                    test:/\.jpg|png|gif|bmp|ttf|eot|svg|woff|woff2$/,
                    //limit用来设置字节数，只有小于limit值的图片，才会转换
                    //为base64图片
                    use:"url-loader?limit=16940"
                }
            ]
        }
    }
    
//6.打包js文件中的高级语法：
	在编写js的时候，有时候我们会使用高版本的js语法, 有可能这些高版本的语法不被兼容，我们需要将之打包为兼容性的js代码.
	
	我们需要安装babel系列的包
    A.安装babel转换器
    
        npm install babel-loader @babel/core @babel/runtime -D
        
    B.安装babel语法插件包
    
        npm install @babel/preset-env @babel/plugin-transform-runtime @babel/plugin-proposal-class-properties -D
        
    C.在项目根目录创建并配置babel.config.js文件

        module.exports = {
            presets:["@babel/preset-env"],
            plugins:[ "@babel/plugin-transform-runtime", "@babel/plugin-proposal-class-properties" ]
        }
        
    D.配置规则：更改webpack.config.js的module中的rules数组
    module.exports = {
        plugins:[ htmlPlugin],
        module : {
            rules:[
                {
                    //test设置需要匹配的文件类型，支持正则
                    test:/\.css$/,
                    //use表示该文件类型需要调用的loader
                    use:['style-loader','css-loader']
                },
                {
                    test:/\.less$/,
                    use:['style-loader','css-loader','less-loader']
                },
                {
                    test:/\.scss$/,
                    use:['style-loader','css-loader','sass-loader']
                },
                {
                    test:/\.jpg|png|gif|bmp|ttf|eot|svg|woff|woff2$/,
                    //limit用来设置字节数，只有小于limit值的图片，才会转换
                    //为base64图片
                    use:"url-loader?limit=16940"
                },
                {
                    test:/\.js$/,
                    use:"babel-loader",
                    //exclude为排除项，意思是不要处理node_modules中的js文件
                    exclude:/node_modules/
                }
            ]
        }
    }
    
    
//7. .pretterrc 
配置单引号和不加分号

{
"semi": false,
"singleQuote": true
}

最后在所有界面ctl +s 


//8. .eslintrc.js
module.exports = {
  root: true,
  env: {
    node: true
  },
  'extends': [
    'plugin:vue/essential',
    '@vue/standard'
  ],
  rules: {
    'no-console': process.env.NODE_ENV === 'production' ? 'error' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'error' : 'off',
    'space-before-function-paren': 0
  },
  parserOptions: {
    parser: 'babel-eslint'
  }
}
```



#### 9.6.7 vue单文件

```
传统Vue组件的缺陷：
    1.全局定义的组件不能重名，
    2.字符串模板缺乏语法高亮，
    3.不支持css(当html和js组件化时，css没有参与其中)
    4.没有构建步骤限制，只能使用H5和ES5，
    5.不能使用预处理器（babel）
解决方案：
    使用Vue单文件组件，每个单文件组件的后缀名都是.vue
    每一个Vue单文件组件都由三部分组成
        1).template组件组成的模板区域
        2).script组成的业务逻辑区域
        3).style样式区域
```



##### 代码结构

```
<template>
    组件代码区域
</template>

<script>
    js代码区域
</script>

// 私有的样式
<style scoped>
    样式代码区域
</style>
```



#### 9.6.8 配置vue加载器

```
1.安装vue组件的加载器

    npm install vue-loader vue-template-compiler -D
    
2.配置规则：更改webpack.config.js的module中的rules数组
    const VueLoaderPlugin = require("vue-loader/lib/plugin");
    const vuePlugin = new VueLoaderPlugin();
    module.exports = {
        plugins:[ htmlPlugin, vuePlugin  ],
        module : {
            rules:[
                ...//其他规则
                { 
                    test:/.vue$/,
                    loader:"vue-loader",
                }
        ]
    }
}
```



#### 9.6.9 使用vue

```
	我们安装处理了vue单文件组件的加载器，想要让vue单文件组件能够使用，我们必须要安装vue, 并使用vue来引用vue单文件组件。

1.安装Vue
    npm install vue -S
    
2.在index.js中引入vue：
	import Vue from "vue"

3.创建Vue实例对象并指定el，最后使用render函数渲染单文件组件
    const vm = new Vue({
        el:"#app",
        render:h=>h(app)
    })
```



#### 9.6.10 打包发布项目

```
在项目上线之前，我们需要将整个项目打包并发布。

1.配置package.json
    "scripts":{
        "dev":"webpack-dev-server",
        "build":"webpack -p"
    }
    
2.在项目打包之前，可以将dist目录删除，生成全新的dist目录
	npm run build
```



### 9.7 vue脚手架

#### 9.7.1 安装并创建项目

```
1.安装3.x版本的Vue脚手架：

    npm install -g @vue/cli 
    
    vue -V
    
2.基于3.x版本的脚手架创建Vue项目：
    方式一：使用命令创建Vue项目
  
        vue create my-project
        
        选择Manually select features(选择特性以创建项目)
        勾选特性可以用空格进行勾选。
        是否选用历史模式的路由：n
        ESLint选择：ESLint + Standard config
        何时进行ESLint语法校验：Lint on save
        babel，postcss等配置文件如何放置：In dedicated config files(单独使用文件进行配置)
        是否保存为模板：n
        使用哪个工具安装包：npm
        
    方式二：基于ui界面创建Vue项目
        命令：vue ui
        在自动打开的创建项目网页中配置项目信息。
        
    补充：基于2.x的旧模板，创建Vue项目
        npm install -g @vue/cli-init    /  npm install -g vue-cli
        vue init webpack my-project
        
        runtime-only 
        standed
        npm

3.分析Vue3.x脚手架生成的项目结构
    node_modules:依赖包目录
    public：静态资源目录
    src：源码目录
    src/assets:资源目录
    src/components：组件目录
    src/views:视图组件目录
    src/App.vue:根组件
    src/main.js:入口js
    src/router.js:路由js
    *****************************************************
    vue.config.js:   额外的配置信息，跟package.json分割开
    babel.config.js: babel配置文件， js语法编译
    package.json:    npm的配置文件，里面设定了脚本以及项目依赖的库
    .eslintrc.js:    
    	eslint是用来管理和检测js代码风格的工具，可以和编辑器搭配使用，如vscode的eslint插件
		当有不符合配置文件内容的代码出现就会报错或者警告
		
		module.exports = {
          root: true,
          env: {
            node: true
          },
          extends: [
            'plugin:vue/essential',
            '@vue/standard'
          ],
          parserOptions: {
            parser: 'babel-eslint'
          },
          rules: {
            'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
            'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off'
          }
        }
	
    
	.editorconfig:   代码风格（vscode的editorconfig）
	
    postcss.config.js: css预处理配置
    
    .browserslistrc
        > 1%,
        last 2 versions,
        not ie <= 8,
        safari >= 7
        
        设置浏览器的兼容
        对于部分配置参数做一些解释:
        " >1%" :代表着全球超过1%人使用的浏览器
        “last 2 versions” : 表示所有浏览器兼容到最后两个版本
        “not ie <=8” :表示IE浏览器版本大于8（实则用npx browserslist 跑出来不包含IE9 ）
        “safari >=7”:表示safari浏览器版本大于等于7
        
    .env.pre-release       # 预发布环境    
    .env.production        # 生产环境       
    .env.test              # 测试环境  
    
    
   
    *****************************************************
    
4.tips:
    1. npm run lint --fix
    2. vscode 中更改settings.json配置
    
```

#### 9.7.2 基本配置

```
方式一： 通过 package.json 进行配置 [不推荐使用]
    "vue":{
        "devServer":{
            "port":"9990",
            "open":true
        }
        
方式二：通过单独的配置文件进行配置，创建vue.config.js
    module.exports = {
        devServer:{
            port:8888,
            open:true
        }
    }
```



#### 9.7.3 element-ui

```
Element-UI: 一套基于2.0的桌面端组件库,  https://element.eleme.cn/#/zh-CN/component/layout

1.安装：
    npm install element-ui -S
    
2.导入使用：
    import ElementUI from 'element-ui';
    import 'element-ui/lib/theme-chalk/index.css';
    
    Vue.use(ElementUI)
```



#### 9.7.4 运行流程

```
main.js ---App.vue --- router/index.js ---> view/xxx.vue（component,widget）---> service/xxx.js 获取数据
```





## 10. Vuex

### 10.1 概述

```
Vuex是实现组件全局状态（数据）管理的一种机制，可以方便的实现组件之间的数据共享

使用Vuex管理数据的好处：
    A.能够在vuex中集中管理共享的数据，便于开发和后期进行维护
    B.能够高效的实现组件之间的数据共享，提高开发效率
    C.存储在vuex中的数据是响应式的，当数据发生改变时，页面中的数据也会同步更新

哪些数据适合vuex:
	组件之间共享的数据，私有数据是不需要的，依旧存储在data中
```



### 10.2 基本使用

```
1. 安装vuex
npm install vuex --save 

2. 导入vuex包
import Vuex from 'vuex'
Vue.use(Vuex)

3. 创建store对象
const store = new Vuex.Store({
	state: {
		count: 0
	},
	modules: {},
	plugins: {}
})

export default store

4. 将store对象挂载到vue实例中
window.gApp = new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
```

### 10.3 计数器搭建

- 找到src目录中的App.vue组件，将代码重新编写如下：

  ```vue
  <template>
    <div>
      <p>---------------加----------------</p>
      <my-addition></my-addition>
  
      <p>---------------减----------------</p>
      <my-subtraction></my-subtraction>
    </div>
  </template>
  
  <script>
  import Addition from './components/Addition.vue'
  import Subtraction from './components/Subtraction.vue'
  
  export default {
    data() {
      return {}
    },
    components: {
      'my-subtraction': Subtraction,
      'my-addition': Addition
    }
  }
  </script>
  
  <style>
  </style>
  ```



- 在components文件夹中创建Addition.vue组件，代码如下：

  ```vue
  <template>
      <div>
          <h3>当前最新的count值为：</h3>
          <button>+1</button>
      </div>
  </template>
  
  <script>
  export default {
    data() {
      return {}
    }
  }
  </script>
  
  <style>
  </style>
  ```

- 在components文件夹中创建Subtraction.vue组件，代码如下：

  ```vue
  <template>
      <div>
          <h3>当前最新的count值为：</h3>
          <button>-1</button>
      </div>
  </template>
  
  <script>
  export default {
    data() {
      return {}
    }
  }
  </script>
  
  <style>
  </style>
  ```

  

- 在项目根目录(与src平级)中创建 .prettierrc 文件，编写代码如下：

```
{	
	// 是否必须加分号
    "semi":false,
    // 单引号
    "singleQuote":true
}
```



### 10.4 State

> State提供唯一的公共数据源

```
State提供唯一的公共数据源，所有共享的数据都要统一放到Store中的State中存储

例如，打开项目中的store.js文件，在State对象中可以添加我们要共享的数据，

export default new Vuex.Store({
  state: {
    count: 0
  },
  mutations: {
  },
  actions: {
  },
  
  getters: {},
  modules: {},
  plugins: []      // 参见 yv-appmgt 中 index.js 的用法
})

在组件中访问State的方式：
   方式1： $store.state.全局数据名称 如：$store.state.count
   
   方式2： 先按需导入mapState函数:
           import { mapState } from 'vuex'
           
           然后数据映射为计算属性:
           computed: { 
             ...mapState( ['全局数据名称'] ) 
           }

eg:
	<template>
        <div>
            <h3>方式一：当前最新的count值为：{{$store.state.count}}	</h3>
            <h3>方式二：当前最新的count值为：{{count}}</h3>
            <button>+1</button>
        </div>
    </template>

    <script>
        import { mapState } from 'vuex'
        export default {
          data: function () {
            return {
            }
          },
          computed: {
            ...mapState(['count'])
          }
        }
    </script>

    <style>
    </style>
```



### 10.5 Mutation

```
Mutation用于修改变更$store中的数据，不允许通过this.$store.state.count直接修改

1. store.js文件，添加代码如下
mutations: {
    add(state, args){
      //第一个形参永远都是state也就是$state对象
      //第二个形参是调用add时传递的参数
      state.count+=args;
    }
  }
  
2. Addition.vue中给按钮添加事件代码如下： ***都可以传参***
<button @click="Add">+1</button>

方式一：
methods:{
  Add(){
    //使用commit函数调用mutations中的对应函数，
    //第一个参数就是我们要调用的mutations中的函数名
    //第二个参数就是传递给add函数的参数
    this.$store.commit('add',10)
  }
}

方式二：
import { mapMutations } from 'vuex'

methods:{
      //获得mapMutations映射的sub函数
      ...mapMutations(['sub']),
      
      //当点击按钮时触发Sub函数么，也可以不封装，直接用
      Sub(){
          //调用sub函数完成对数据的操作
          this.sub(10);
      }
}
```



### 10.6 Action

```
在mutations中不能编写异步的代码，会导致vue调试器的显示出错。在vuex中我们可以使用Action来执行异步操作

1. 打开store.js文件，修改Action，如下：
actions: {
  addAsync(context, step){
    setTimeout(()=>{
      context.commit('add', step);
    },2000)
  }
}

或者

const actions = {
  toggleSideBar({ commit }) {
    commit('TOGGLE_SIDEBAR')
  },
  closeSideBar({ commit }, { withoutAnimation }) {
    commit('CLOSE_SIDEBAR', withoutAnimation)
  },
  toggleDevice({ commit }, device) {
    commit('TOGGLE_DEVICE', device)
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}



2. 然后在Addition.vue中给按钮添加事件代码如下：
<button @click="AddAsync">...+1</button>


方式一：
methods:{
  AddAsync(){
    this.$store.dispatch('addAsync', 5)
  }
}


方式二：
import { mapActions } from 'vuex'

methods:{
   //获得mapActions映射的addAsync函数
      ...mapActions(['subAsync']),
      asyncSub(){
          this.subAsync(5);
      }
}

方式三：
	<button @click="AddAsync(5)">...+1</button>
	
	import { mapActions } from 'vuex'

    methods:{
       //获得mapActions映射的addAsync函数
          ...mapActions(['subAsync']),
    }

```



### 10.7 Getter

```
Getter用于对Store中的数据进行加工处理形成新的数据，类似计算属性
它只会包装Store中保存的数据，并不会修改Store中保存的数据，当Store中的数据发生变化时，Getter生成的内容也会随之变化。  副本


1. 打开store.js文件，添加getters，如下：
export default new Vuex.Store({
  getters:{
    //添加了一个showNum的属性
    showNum : state => {
       return '最新的count值为：'+state.count;
    }
  }
})


2. 
方式一：打开Addition.vue中，添加插值表达式使用getters
<h3>{{ $store.getters.showNum }}</h3>
	
方式二： Subtraction.vue
<h3>{{showNum}}</h3>

import { mapGetters } from 'vuex'
computed:{
  ...mapGetters(['showNum'])
}
```





### 10.8 mapXxx

```
mapState
mapActions
mapMutation
mapGetters

按需导入，辅助函数

参考：
   https://www.cnblogs.com/m2maomao/p/9954640.html
   https://www.toutiao.com/a6751937823827296782/?tt_from=android_share&utm_campaign=client_share&timestamp=1572178352&app=news_article&utm_medium=toutiao_android&req_id=2019102720123201001404813727D2F874&group_id=6751937823827296782




```



### 10.9 modules

index.js

```
import Vue from 'vue'
import Vuex from 'vuex'
import getters from './getters'
import app from './modules/app'
import settings from './modules/settings'
import user from './modules/user'

Vue.use(Vuex)

const store = new Vuex.Store({
  modules: {
    app,
    settings,
    user
  },
  getters
})

export default store
```

getters.js

```
const getters = {
  sidebar: state => state.app.sidebar,
  device: state => state.app.device,
  token: state => state.user.token,
  avatar: state => state.user.avatar,
  name: state => state.user.name
}
export default getters
```

user.js

settings.js

app.js



### 10.10 更新

```
import Vue from 'vue'
import Vuex from 'vuex'
import EventBus from '../common/event-bus'
import configModule from './config'

Vue.use(Vuex)

function initialState (modules) {
  const storageState = JSON.parse(window.localStorage.getItem('vuex'))
  if (!storageState) {
    return modules
  }
  Object.keys(modules).forEach(name => {
    const module = modules[name]
    if (storageState.hasOwnProperty(name)) {
      module.state = {
        ...module.state,
        ...storageState[name]
      }
    }
  })
  return modules
}

function persistedState (store) {
  window.store = store
  const state = store.state
  window.localStorage.setItem('vuex', JSON.stringify(state))
  store.subscribe((mutation, state) => {
    window.localStorage.setItem('vuex', JSON.stringify(state))
  })
}

function resetLocaleMap (store) {
  store.subscribe((mutation, state) => {
    if (mutation.type === 'configModule/changeLang') {
      EventBus.$emit('changeLang', state.configModule.language)
    }
  })
}

export default new Vuex.Store({
  modules: {
    ...initialState({
      configModule
    })
  },
  plugins: [persistedState, resetLocaleMap]
})

```





## 11. 其他

### 11.1 nextTick

```
原理：
	Vue 实现响应式并不是数据发生变化之后 DOM 立即变化，而是按一定的策略进行 DOM 的更新。
	$nextTick 是在下次 DOM 更新循环结束之后执行延迟回调，在修改数据之后使用 $nextTick，则可以在回调中获取更新后的 DOM
	
	不这样做可能一些执行的操作无效，为啥有的加这个，有的不加呢？   ***
	
场景：
　　1.在Vue生命周期的created()钩子函数进行的DOM操作一定要放在Vue.nextTick()的回调函数中。
　　2.在created()钩子函数执行的时候DOM 其实并未进行任何渲染，而此时进行DOM操作无异于徒劳，所以此处一定要将DOM操作的js代码放进Vue.nextTick()的回调函数中。与之对应的就是mounted()钩子函数，因为该钩子函数执行时所有的DOM挂载和渲染都已完成，此时在该钩子函数中进行任何DOM操作都不会有问题 。
　　3.在数据变化后要执行的某个操作，而这个操作需要使用随数据改变而改变的DOM结构的时候，这个操作都应该放进Vue.nextTick()的回调函数中。
　　
　
代码： yv_appmgt  

https://blog.csdn.net/zhouzuoluo/article/details/84752280
```



### 11.2 ref

```
比较方便取DOM，方便操作DOM, 减少获取dom节点的消耗

注意事项：
	$refs 是非响应式的，需要组件填充完后才能获取到（避免在模板或者计算属性中使用）
	ref 和  v-for 一起使用的时候，获取到的引用是一个数组，包含和循环数组对应的子组件；li里的ref的无法读取item里面的值，即item.name或被直接读取为字符串“item.name”
```



### 11.3 展开表达式

```
https://www.jianshu.com/p/3935a80342a0

1.替代apply
function f(a,b,c){
  console.log(a,b,c)
}
let args = [1,2,3];
// 以下三种方法结果相同
f.apply(null,args)
f(...args)
f(1,2,3)

function f2(...args){
  console.log(args)
}
f2(1,2,3) // [1,2,3]

2.合并数组、构造数据
let a = [1,2,3];
let b = [4,5,6];
let c = [...a, ...b]; // [1,2,3,4,5,6]

let x = {
	name: 'autumn'
}
let y = {
	age: 18
}
let z = {...x,...y}
console.log(z)


3.解构赋值
let a = [1,2,3,4,5,6]
//展开运算符必须放在最后一位
let [c, ...d] = a
console.log(c); // 1
console.log(d); // [2,3,4,5,6]

4.字符串转为数组
[...'siva'] // ['s','i','v','a']

5.具有 Iterator 接口的对象,转换成数组
var nodelist = document.querySelectorAll('div');
console.log([...nodelist]) // 转化成数组

var map = new Map([[1,11],[2,22],[3,33]]);
console.log([...map.keys()]); // [1,2,3]


6. 浅拷贝    https://blog.csdn.net/zomixi/article/details/84064255
//数组
var a = [1,2,4]
var b = [...a]
a.push(6)
console.log(b) // [1,2,4]

//对象
var a = {a:1}
var b = {...a}
a.a = 5
console.log(b.a) // 1
```



### 11.4 vue.use

```
https://www.cnblogs.com/fps2tao/p/10830804.html

https://segmentfault.com/a/1190000012296163

编写插件的两种方式：
	1. 将这个插件的逻辑封装成一个对象，最后在install中编写业务代码暴露给vue对象，好处在于可以添加任意参数，可扩展性高
	2. 所有逻辑都编写成一个函数暴露给vue
```



### 11.5 mixin&extend

> 威力太大，用的少

```
https://segmentfault.com/a/1190000015608340
https://www.cnblogs.com/xzybk/p/12786680.html

区别：
	mixin是对Vue类的options进行混入。所有Vue的实例对象都会具备混入进来的配置行为。
	extend是产生一个继承自Vue类的子类，只会影响这个子类的实例对象，不会对Vue类本身以及Vue类的实例对象产生影响。

优先级：
	extend > extends > mixins，但他们都会在  Vue.extend 与  Vue.mixin之后  执行
	

// 给vue增加一些类似全局的方法
Vue.mixin(AuthorityMixin)
vue.extends
vue.extend


//vue extend 扩展实例构造器
var ex = Vue.extend({
    template:`{{a}}`,
    props: ["a"]
    data: function(){
        return {
        }
    },
})
new ex({propsData:{a:11}}).$mount("")


//vue.extends 单次扩展一个组件

//vue mixin（跟上面很像）
全局注册一个混入，影响注册之后所有创建的每个 Vue 实例， 可扩展多个组件
    方式一：
    var addConsole={
        updated: function(){
            console.log(this.num)
        }
    }
    var vm = new Vue({
        el:"#app",
        data:{
            num: 1
        },
        methods:{
            add:function(){
                    this.num++;
                },
                
        mixins:[addConsole]
    }
    
    方式二：
    var vm = new Vue({
        el:"#app",
        data:{
            num: 1
        },
        updated:function(){
            
        },
        methods:{
            add:function(){
                    this.num++;
                },
    }
    
    
    方式三：
    全局api
    Vue.mixin({
        updated:function(){
            
        }
    })
    
    
example:
	export default {
      methods: {
        validPermission (code) {
          const permissions = this.$store.state.configModule.authority
          return permissions.includes(code)
        }
      }
    }
    
    Vue.mixin(AuthorityMixin)
```



### 11.6 form-render

```
https://github.com/Nikozhang996/vue-form-renderer/
```





## 12. 组件库制作

> 参考: element-ui 相关基本组件

```
要求：自己封装组件，并使用
参考: element-ui 相关基本组件

https://www.bilibili.com/video/BV1nJ411V75n?p=8
https://github.com/weizhuren/one-ui
https://blog.csdn.net/weixiaowei_2016
https://github.com/hucongcong/heima-uui
```



### 12.1 button

> :diasbled = disabled  是必须，如果不设置，父组件上的click事件还是能触发，事件冒泡\
>
> $slots 相关用法  https://blog.csdn.net/guzhao593/article/details/89219229

- 前置知识

  ```
  组件通讯
  props校验
  插槽  	  预留<slot></slot>元素作为后续内容更改的出口
  scss
  ```

- 参数支持

  | 参数名   | 参数描述                                        | 参数类型 | 默认值  |
  | :------- | :---------------------------------------------- | :------- | :------ |
  | type     | 按钮类型（primary/success/warning/danger/info） | string   | default |
  | plain    | 是否是朴素按钮                                  | boolean  | false   |
  | round    | 是否是圆角按钮                                  | boolean  | false   |
  | circle   | 是否是圆形按钮                                  | boolean  | false   |
  | disabled | 是否禁用按钮                                    | boolean  | false   |
  | icon     | 图标类名                                        | string   | 无      |

- 事件

  ```
  click	点击事件
  ```

- step1: 初始化

  ```
  // 在componet下创建一个button.vue的文件，放置button组件代码。创建一个组建的button组件，，并且指定name为oneButton。
  
  <template>
    <button class="one-button">
     按钮组件
    </button>
  </template>
   
  <script>
  export default {
    name: 'oneButton'
  }
  </script>
   
  <style lang="scss">
  </style>
  
  // 创建组件完成后，不能在项目中直接使用，需要到main.js中注册才可以使用。
  
  import Vue from 'vue'
  import App from './App.vue'
  
  import OneButton from './components/button.vue'
   
  Vue.config.productionTip = false
   
  Vue.component(OneButton.name, OneButton)
   
  new Vue({
    render: h => h(App)
  }).$mount('#app')
  
  
  // 注册完成后，组件就可以在app.vue中使用了。
  <template>
    <div>
      <one-button></one-button>
    </div>
  </template>
  ```

- step2: 增加插槽

  ```
  凡是希望组件中内容可以灵活设置的地方，都需要用到slot插槽来自定义内容。
  
  //在button.vue 使用slot来定义按钮上的文本内容：
  
  <template>
    <button class="one-button">
     <span><slot></slot></span>
    </button>
  </template>
  
  <script>
  export default {
    name: 'oneButton'
  }
  </script>
  
  //button基本样式
  <style lang="scss">
    .one-button{
      display: inline-block;
      line-height: 1;
      white-space: nowrap;
      cursor: pointer;
      background: #ffffff;
      border: 1px solid #dcdfe6;
      color: #606266;
      -webkit-appearance: none;
      text-align: center;
      box-sizing: border-box;
      outline: none;
      margin: 0;
      transition: 0.1s;
      font-weight: 500;
      //禁止元素的文字被选中
      -moz-user-select: none;
      -webkit-user-select: none;
      -moz-user-select: none;
      -ms-user-select: none;
      padding: 12px 20px;
      font-size: 14px;
      border-radius: 4px;
      &:hover,
      &:hover{
        color: #409eff;
        border-color: #c6e2ff;
        background-color: #ecf5ff;
      }
    }
  </style>
  
  
  
  //在app.vue使用时就可以直接输入文本，定义按钮文本内容了：
  <template>
    <div>
      <one-button>登录</one-button>
      <one-button>删除</one-button>
      <one-button>取消</one-button>
    </div>
  </template>
  
  ```

- step3: 增加type样式

  ```
  // 子组件接收父组件传递的数据
  export default {
    name: 'oneButton',
    // 此时对props进行校验，值接收string类型的type值
    props: {
      type:{
        type: String，
        // 设置默认值：如果不传值，那么使用default
        default: 'default'
      }
    },
    created () {
      console.log(this.type) //defalut primary success info danger warning
    }
  }
  
  // 通过绑定类名的方法由父类动态控制样式
  <template>
    <button class="one-button" :class="`one-button-${type}`">
     <span><slot></slot></span>
    </button>
  </template>
  
  
  // 设置不同类型的样式
  .one-button-primary{
    color:#fff;
    background-color: #409eff;
    border-color: #409eff;
    &:hover,
    &:focus{
      background: #66b1ff;
      background-color: #66b1ff;
      color: #fff;
      }
    }
    .one-button-success{
    color:#fff;
    background-color: #67c23a;
    border-color: #67c23a;
    &:hover,
    &:focus{
      background: #85ce61;
      background-color: #85ce61;
      color: #fff;
      }
    }
    .one-button-info{
    color:#fff;
    background-color: #909399;
    border-color: #909399;
    &:hover,
    &:focus{
      background: #a6a9ad;
      background-color: #a6a9ad;
      color: #fff;
      }
    }
    .one-button-warning{
    color:#fff;
    background-color: #e6a23c;
    border-color: #e6a23c;
    &:hover,
    &:focus{
      background: #ebb563;
      background-color: #ebb563;
      color: #fff;
      }
    }
    .one-button-danger{
    color:#fff;
    background-color: #f56c6c;
    border-color: #f56c6c;
    &:hover,
    &:focus{
      background: #f78989;
      background-color: #f78989;
      color: #fff;
      }
    }
    
  // 父组件组件传递type属性
  <template>
    <div id="app">
      <div class="row">
      <one-button>按钮</one-button>
      <one-button type="primary">primary按钮</one-button>
      <one-button type="success">success按钮</one-button>
      <one-button type="info">info按钮</one-button>
      <one-button type="danger">danger按钮</one-button>
      <one-button type="warning">warning按钮</one-button>
      </div>
    </div>
  </template>
  
  
  // 效果
  ```

- step4: 增加plain，round， circle属性

  ```
  第一步:父组件组件传递plain值
  
  <template>
    <div id="app">
      <div class="row">
      <one-button plain>按钮</one-button>
      <one-button plain type="primary">primary按钮</one-button>
      <one-button plain type="success">success按钮</one-button>
      <one-button plain type="info">info按钮</one-button>
      <one-button plain type="danger">danger按钮</one-button>
      <one-button plain type="warning">warning按钮</one-button>
      </div>
      
      <div class="row">
      <one-button round>按钮</one-button>
      <one-button round type="primary">primary按钮</one-button>
      <one-button round type="success">success按钮</one-button>
      <one-button round type="info">info按钮</one-button>
      <one-button round type="danger">danger按钮</one-button>
      <one-button round type="warning">warning按钮</one-button>
      </div>
      
      <div class="row">
      <one-button circle>按钮</one-button>
      <one-button circle type="primary">primary按钮</one-button>
      <one-button circle type="success">success按钮</one-button>
      <one-button circle type="info">info按钮</one-button>
      <one-button circle type="danger">danger按钮</one-button>
      <one-button circle type="warning">warning按钮</one-button>
      </div>
    </div>
  </template>
  
  
  第二步：子组件接收负组件传递的数据，同样进行props校验，并且设置默认值为false
    props: {
      plain: {
        type: Boolean,
        default: false
      },
      round: {
        type: Boolean,
        default: false
      },
      circle: {
        type: Boolean,
        default: false
      }
    }
    
  第三步:通过绑定类名的方法动态控制样式，由于plain类型是布尔值，所以在类型中我们使用对象的形式来控制样式
  <template>
    <button class="one-button" :class="[`one-button-${type}`,{
      'is-plain':plain,
      'is-round':round,
      'is-circle':circle
    }]">
     <span><slot></slot></span>
    </button>
  </template>
  
  
  第四步：设置不同类型的样式，由于plain类型是以对象的形式在类中定义的，所以使用获取属性的方法定义样式
  // 朴素按钮样式
  .one-button.is-plain{
    &:hover,
    &:focus{
      background: #fff;
      border-color: #489eff;
      color: #409eff;
    }
  }
  .one-button-primary.is-plain{
    color: #409eff;
    background: #ecf5ff;
    &:hover,
    &:focus{
      background: #409eff;
      border-color: #409eff;
      color: #fff;
    }
  }
  .one-button-success.is-plain{
    color: #67c23a;
    background: #c2e7b0;
    &:hover,
    &:focus{
      background: #67c23a;
      border-color: #67c23a;
      color: #fff;
    }
  }
  .one-button-info.is-plain{
    color: #909399;
    background: #d3d4d6;
    &:hover,
    &:focus{
      background: #909399;
      border-color: #909399;
      color: #fff;
    }
  }
  .one-button-warning.is-plain{
    color: #e6a23c;
    background: #f5dab1;
    &:hover,
    &:focus{
      background: #e6a23c;
      border-color: #e6a23c;
      color: #fff;
    }
  }
  .one-button-danger.is-plain{
    color: #f56c6c;
    background: #fbc4c4;
    &:hover,
    &:focus{
      background: #f56c6c;
      border-color: #f56c6c;
      color: #fff;
    }
  }
  
  .one-button.is-round{
    border-radius: 20px;
    padding: 12px 23px;
  }
  
  .one-button.is-circle{
    border-radius: 50%;
    padding: 12px;
  }
  ```

- step5：增加字体图标

  ```
  在项目中使用字体图标，首先需要有字体图标，我们可以去阿里巴巴矢量图标库下载。(需要先注册，选择图标，添加到购物车，下载代码)
  
  下载完成后，在asset目录下新建一个fonts目录，存放我们下载到的字体图标。
  
  做完准备工作后，我们就可以开始把字体图标运用到项目中了。
  
  第一步：在main.js中引入字体图标
  import './assets/fonts/iconfont.css'
  
  第二步：将下载的字体图标css文件 iconfont.css 中的类名做修改，我将icon全部改为了one-icon，并且将初始的iconfont类改为了[class*='one-icon']，当类名中有one-icon时使用，如下:
  
  [class*='one-icon'] {
    font-family: "iconfont" !important;
    font-size: 16px;
    font-style: normal;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }
  .one-icon-bluetoothoff:before {
    content: "\e697";
  }
  
  第三步：父组件传递图标名，子组件接收并且放到图标中
  父组件传值：
      <div class="row">
        <one-button icon="bluetoothon"></one-button>
        <one-button type="primary" icon="camera">照相机</one-button>
        <one-button type="success" icon="course"></one-button>
        <one-button type="info" icon="bluetooth_link"></one-button>
        <one-button type="danger" icon="addto"></one-button>
        <one-button type="warning" icon="audio"></one-button>
      </div>
      
  子组件接收：
      icon: {
        type: String,
        default: ''
      }
      
  使用接收到的字体图标。在没有传入icon时隐藏<i>标签，在slot插槽没有传入值时，不显示<span>标签
  <template>
    <button class="one-button" :class="[`one-button-${type}`,{
      'is-plain':plain,
      'is-round':round,
      'is-circle':circle,
    }]">
    <i v-if="icon" :class="`one-icon-${icon}`"></i>
    <!-- 如果没传入文本插槽，则不显示span内容 -->
     <span v-if="$slots.default"><slot></slot></span>
    </button>
  </template>
  
  
  第四步：设置icon配套样式，使图标和文字之间有一定间隔
  .one-button [class*=one-icon-]+span{
    margin-left: 5px;
  }
  
  第五步：查看效果
  ```
  
- step6: 点击事件

  ```
  我们在使用组件时，直接给组件定义事件是不会被触发的。我们需要在组件中定义一个点击事件，这个点击事件不进行其他操作，只出发父组件中的点击事件。
  
  组件中的定义点击事件：
  
  <template>
    <button class="one-button" :class="[`one-button-${type}`,{
      'is-plain':plain,
      'is-round':round,
      'is-circle':circle,
    }]"
    @click="handleClick"
    >
    <i v-if="icon" :class="`one-icon-${icon}`"></i>
    <!-- 如果没传入文本插槽，则不显示span内容 -->
     <span v-if="$slots.default"><slot></slot></span>
    </button>
  </template>
   定义一个点击事件，这个点击事件的作用是调用父组件中的点击事件，并且回调 
  
    methods: {
      handleClick (e) {
         
      }
    }
  父组件在使用时定义自己的点击事件，其本质是子组件中的点击事件触发父组件中的点击事件。
  
  <div class="row">
    <one-button @click="getInfo">按钮</one-button>
  </div>
    methods: {
      getInfo () {
        console.log('获取信息！！')//获取信息！！
      }
    }
  ```

- step7: disabled属性

  ```
  和之前相似，只要父子组件传值并且动态获取这个值并且赋给disabled属性,并且设置一个disabled样式即可。
  
  <div class="row">
    <one-button @click="getInfo" disabled>按钮</one-button>
  </div>
  
  // 注意一个是禁用事件，二是样式
  <template>
    <button class="one-button" :class="[`one-button-${type}`,{
      'is-plain':plain,
      'is-round':round,
      'is-circle':circle,
      'is-disabled':disabled
    }]"
    @click="handleClick"
    //:disabled="disabled"
    >
    <i v-if="icon" :class="`one-icon-${icon}`"></i>
     <span v-if="$slots.default"><slot></slot></span>
    </button>
  </template>
  
  // props中增加属性
  disabled: {
      type: Boolean,
      default: false
  }
  
  // disabled样式
  .one-button.is-disabled{
     cursor: no-drop;
  }
  ```



### 12.2 dialog

- 前置知识

  ```
  vue过渡与动画
  sync修饰符    <h-dialog title="提示" width="30%" top="50px" :visible.sync='visible'>
  具名插槽与v-slot
  ```

- 参数支持：

| 参数名  | 参数描述                         | 参数类型 | 默认值 |
| :------ | :------------------------------- | :------- | :----- |
| title   | 对话框标题                       | string   | 提示   |
| width   | 宽度                             | string   | 50%    |
| top     | 与顶部的距离                     | string   | 15vh   |
| visible | 是否显示dialog（支持sync修饰符） | boolean  | false  |

- 事件支持：

| 事件名 | 事件描述       |
| :----- | :------------- |
| opened | 模态框显示事件 |
| closed | 模态框关闭事件 |

- 插槽说明：

| 插槽名称 | 插槽描述           |
| :------- | :----------------- |
| default  | dialog的内容       |
| title    | dialog的标题       |
| footer   | dialog的底部操作区 |



.sync

> https://blog.csdn.net/YuShiYue/article/details/119830279      2.x   3.x
>
> https://blog.csdn.net/u010671652/article/details/106466398 

```
从 2.3.0 Vue重新引入了 .sync 修饰符，但是这次它只是作为一个编译时的语法糖存在。它会被扩展为一个自动更新父组件属性的 v-on 监听器。

示例代码如下：（父组件.vue）

<comp :foo.sync="bar"></comp>
会被扩展为：
<comp :foo="bar" @update:foo="val => bar = val"></comp>

当子组件需要更新 foo 的值时，它需要显式地触发一个更新事件：
this.$emit('update:foo', newValue)
```





- step1: 基本样式

  ```
  <template>
   <div class="one-dialog_wrapper">
     <div class="one-dialog">
       <div class="one-dialog_header">
         <span class="one-dialog_title">提示</span>
         <button class="one-dialog_headerbtn">
           <i class="one-icon-close"></i>
         </button>
       </div>
       <div class="one-dialog_body">
         <span>这是一段信息</span>
       </div>
       <div class="one-dialog_footer">
         <one-button>取消</one-button>
         <one-button type="primary">确定</one-button>
       </div>
     </div>
   </div>
  </template>
  
  <style lang="scss" scoped>
  .one-dialog_wrapper{
    position: fixed;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    overflow: auto;
    margin: 0;
    z-index: 2001;
    background-color: rgba(0,0,0,0.5);
    .one-dialog{
      position: relative;
      margin: 15vh auto 50px;
      background: #fff;
      border-radius: 2px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.3);
      box-sizing: border-box;
      width: 30%;
      &_header{
        padding: 20px 20px 10px;
        .one-dialog_title{
          line-height: 24px;
          font-size: 18px;
          color: #303133;
        }
        .one-dialog_headerbtn{
          position: absolute;
          top: 20px;
          right: 20px;
          padding: 0;
          background: transparent;
          border: none;
          outline: none;
          cursor: pointer;
          font-size: 16px;
          .one-icon-close{
            color:909399
          }
        }
      }
      &_body{
        padding: 30px 20px;
        color: #606266;
        font-size: 14px;
        word-break: break-all;
      }
      &_footer{
        padding: 10px 20px 20px;
        text-align: right;
        box-sizing: border-box;
        ::v-deep .one-button:first-child{
          margin-right: 20px;
        }
      }
    }
  }
  </style>
  
  
  //main.js中引入
  
  //app.vue中使用
  ```

- step2: 自定义title内容

  ```
  title标题部分除了普通的标题内容外，也应该可以设置标题的样式，比如设置为h1红色的自定义标题内容，所以在这里我们就使用到了插槽，可以在使用时按照需求自定义标题内容和样式。
  
  4.2.0父子组件传值以及props验证不再赘述，之前内容已经介绍。
  
  4.2.1将标题span标签放到slot插槽下，这样便于控制span的内容和样式。
  
  <template>
   <div class="one-dialog_wrapper">
     <div class="one-dialog">
       <div class="one-dialog_header">
         <slot name="title">
           <!-- 将span放到slot内，这样不仅可以定义title文本，还可以定义样式等 -->
              <span class="one-dialog_title">
                {{title}}
              </span>
         </slot>
         <button class="one-dialog_headerbtn">
           <i class="one-icon-close"></i>
         </button>
       </div>
       <div class="one-dialog_body">
         <span>这是一段信息</span>
       </div>
       <div class="one-dialog_footer">
         <one-button>取消</one-button>
         <one-button type="primary">确定</one-button>
       </div>
     </div>
   </div>
  </template>
  
  
  4.2.2通过父子组件之间得传值以及slot指定组件自定义title内容和样式。
   <one-dialog title="温馨提示">
          <!-- 使用v-slot指定插槽进行编辑 -->
          <template v-slot:title>
            <h3 style="color:red">我是标题</h3>
          </template>
        </one-dialog>
  ```

- step3: 宽度与高度，body,  footer

  ```
  // 高度与宽度
  父组件传值：
  <one-dialog width="80%" top="200px"></one-dialog>
  
  子组件使用：
  <template>
   <div class="one-dialog_wrapper">
     <div class="one-dialog" :style="{width:width,marginTop:top}">
     </div>
   </div>
  </template>
  
  <script>
  export default {
    name: 'oneDialog',
    components: {
    },
    props: {
      title: {
        type: String,
        default: '提示'
      },
      width: {
        type: String,
        default: '50%'
      },
      top: {
        type: String,
        default: '15vh'
      }
    },
  
  }
  </script>
  
  
  
  //body
  body内容可能是除span以外的其他内容，比如列表等，所以在这里使用插，并且在这里使用匿名插槽，使用匿名插槽的好处就是在使用时不需要使用template标签指定内容，直接在组件标签下编写内容即可。
  4.4.1在body中使用匿名组件
       <div class="one-dialog_body">
         <slot></slot>
       </div>
       
  4.4.2在父组件中，只需要在标签下直接编辑内容即可，不需要再使用template标签绑定插槽或者父子组件传值了
  
  <one-dialog>
      <ul>
          <li>1</li>
          <li>2</li>
          <li>3</li>
      </ul>
  </one-dialog>
  
  
  //footer
  footer中使用slot插槽，在父组件中的定义底部内容。
  4.5.1设置footer插槽，如果没有指定footer插槽，则不显示
       <div class="one-dialog_footer">
         <!-- 如果footer不传递内容，则不显示footer -->
         <slot name="footer" v-if="$slots.footer"></slot>
       </div>
  4.5.2父组件中的定义footer插槽内容
          <template v-slot:footer>
            <one-button>取消</one-button>
            <one-button type="primary">确定</one-button>
          </template>
  ```

- step4: 显示与隐藏， sync

  ```
  打个比方，如下代码需要两部才能实现上述功能：1.向子组件传值；2.接收子组件回调的值
  
  //父组件传值 
  <demo :money="money" @update:money="fn1"></demo>
  
  //子组件回调
    methods: {
      fn () {
       this.$emit('update:monoy', 200)
      }
    }
    
  使用sync语法糖后，父组件不需要单独声明一个方法，只需要在回调时声明一个update绑定的回调函数（这个绑定值是传值自身）这样在父组件中就不需要再次定义回调函数进行接收了。
  
  //父组件中的使用sync语法糖，传递和接收参数
    <demo :visible.sync="visible" :money.sync="money"></demo>
    
  //子组件中使用update绑定参数的方法进行回调
    methods: {
      fn () {
        this.$emit('update:money', 200)
        this.$emit('update:visible', true)
      }
    }
    
  **************************************
  子组件控制dialog的显示和隐藏，不能直接修改父组件传递过来的值，需要使用回调触发父组件中的值进行修改，这里就使用到了上面介绍的sync语法糖。
  
  
  code:
  我们首先在子组件中使用v-show对于组建的显示与隐藏进行控制。
  <!-- @click.self避免冒泡，只有点击自己时才能触发   -->
  <div class="one-dialog_wrapper" v-show="visible" @click.self="handleClose">
  </div>
  
   methods: {
      handleClose () {
        this.$emit('update:visible', false)
      }
    }
  
  父组件中的直接通过传递一个参数visible，使用点击方法控制这个参数的布尔值即可。
        <one-dialog :visible.sync="visible">
          <ul>
            <li>1</li>
            <li>2</li>
            <li>3</li>
          </ul>
          <template v-slot:footer>
            <one-button @click="switchDialog">取消</one-button>
            <one-button type="primary">确定</one-button>
          </template>
        </one-dialog>
  ```

- step5: 动画

  ```
  使用transition包裹一个元素后，这个元素就会被自动添加类名，这部分vuejs文档都有介绍。
  
  4.7.1使用transition包裹整个dialog框架
  <template>
    <transition name="dialog-fade">
      <div class="one-dialog_wrapper" v-show="visible" @click.self="handleClose">
       
      </div>
    </transition>
  </template>
  
  4.7.2使用vue动画进行处理
  这里先定义了fade动画，然后在dialog组件显示和隐藏的时候调用（反向调用）这个动画。
  // 定义的格式是：name-enter-xxx
  .dialog-fade-enter-active{
    animation: fade .3s;
  }
  .dialog-fade-leave-active{
    animation: fade .3s reverse;
  }
  @keyframes fade{
    0% {
      opacity: 0;
      transform: translateY(-20px);
    }
    100% {
      opacity: 1;
      transform: translateY(0);
    }
  }
  ```

- step6: 深度选择器

  ```
   // 对于外界传进来的组件加上scope就不会有影响了
   // vue-loader
   
   &_footer{
        padding: 10px 20px 20px;
        text-align: right;
        box-sizing: border-box;
        ::v-deep .one-button:first-child{
          margin-right: 20px;
        }
      }
  ```
  
  

### 12.3 input

- 参数支持：

  | 参数名称      | 参数描述                    | 参数类型 | 默认值     |
  | :------------ | :-------------------------- | :------- | :--------- |
  | placeholder   | 占位符                      | string   | “”         |
  | type          | 文本框类型（text/password） | string   | “text”     |
  | disabled      | 禁用                        | boolean  | false      |
  | clearable     | 是否显示清空按钮            | boolean  | false      |
  | show-password | 是否显示密码切换按钮        | boolean  | false      |
  | name          | name属性                    | string   | 无事件支持 |

- 事件支持：

  | 事件名称 | 事件描述     |
  | :------- | :----------- |
  | blur     | 失去焦点事件 |
  | change   | 内容改变事件 |
  | focus    | 获取焦点事件 |

  

  step1: 基本框架和样式以及处理placeholder、type、name、disabled

  ```
  <template>
   <div class="one-input">
     <input
     class="one-input_inner"
     :class="{'is-disabled': disabled}"
     :placeholder="placeholder"
     :type="type"
     :name="name"
     :disabled="disabled"/>
   </div>
  </template>
  <script>
  export default {
    name: 'oneInput',
    props: {
      placeholder: {
        type: String,
        default: ''
      },
      type: {
        type: String,
        default: 'text'
      },
      name: {
        type: String,
        default: ''
      },
      disabled: {
        type: Boolean,
        default: false
      }
    },
    data () {
      return {}
    },
    methods: {}
  }
  </script>
  <style lang="scss" scoped>
    .one-input{
      width: 100%;
      position: relative;
      font-size: 14px;
      display: inline-block;
      .one-input_inner{
        -webkit-appearance: none;
        background-color: #fff;
        background-image: none;
        border: 1px solid #dcdfe6;
        border-radius: 4px;
        box-sizing: border-box;
        color: #606266;
        display: inline-block;
        font-size: inherit;
        height: 40px;
        line-height: 40px;
        outline: none;
        padding: 0 15px;
        transition: border-color .2s cubic-bezier(.645,045,.355,1);
        width: 100%;
   
        &:focus{
          outline: none;
          border-color: #409eff;
        }
        
        // input禁用样式
        &.is-disabled{
          background-color: #f5f7fa;
          border-color: #e4e7ed;
          color: #c0c4cc;
          cursor:not-allowed;
        }
      }
    }
  </style>
  
  
  父组件中传值也是与之前一样的：
  <one-input placeholder="请输入密码" type="password" name="name" disabled=true></one-input>
  ```

  step2: v-model语法糖

  ```
  当我们给一个input标签进行双向数据绑定时，我们需要使用value绑定数据，再使用input事件监听标签内数据的变动，每当输入框内容发生变化，就会触发 input ，把最新的value传递给 mes。从而实现了v-model：
  <input :value="username" @input="username=$event.target.value"/>
  	
  在封装input组件时，这样显然是不合适的，所以这里我们需要使用到v-model语法糖。
  
  显然，我们是不能给我们封装的input组件直接使用v-model绑定数据的，但是由于v-model的特性，他将value值绑定在了组件上，所以，我们组件内部通过接收value值的方式，就可以接收到传入的数据；并且v-model也实现了input事件，在组件内部绑定的input事件作为回调，把value值返回给父组件，这样就实现了input组件的双向绑定了。
  
  父组件中的使用v-model绑定：
  <one-input v-model="username"></one-input>
  
  组件内部绑定value值以及实现回调：
   //绑定value值和input事件
   <input
     class="one-input_inner"
     :class="{'is-disabled': disabled}"
     :placeholder="placeholder"
     :type="type"
     :name="name"
     :value="value"
     @input="handleInput"
     :disabled=disabled />
     
    //绑定input事件进行回调
    handleInput (e) {
   	 this.$emit('input', e.target.value)
    }
  ```
  
  step3:  clearable,  password

  ```
当我们在组件中键入clearable属性时，我们希望组件可以有一个一键删除数据得功能。
  
  当input组件的type属性是password时，我们希望在给与show-password属性时，可以有一个显示和隐藏密码的按钮。
  
  实现这个两个功能，除了基本的父子组件传值外，还要添加i标签的icon字体图标，以及实现功能。
   <div class="one-input" :class="{'one-input_suffix':showSuffix}">
     <input
     class="one-input_inner"
     :class="{'is-disabled': disabled}"
     :placeholder="placeholder"
     :type="type"
     :name="name"
     :value="value"
     @input="handleInput"
     :disabled=disabled>
     
    <span class="one-input_suffix">
     <i class="on-input_icon one-icon-cancel" v-if="clearable && value" @click="clear"></i>
     <i class="on-input_icon one-icon-visible" v-if="showPassword && type=='password'" @click="handlePassword"></i>
   </span>
   
   </div>
   
   
  样式：
    .one-input_suffix{
      .one-input_inner{
        padding-right: 30px;
      }
      .one-input_suffix{
        position: absolute;
        right: 10px;
        height: 100%;
        top: 0;
        line-height: 40px;
        text-align: center;
        color: #c0c4cc;
        transition: all .3s;
        z-index: 900;
        i {
          color: #c0c4cc;
          font-size: 14px;
          cursor: pointer;
          transition: color .2s cubic-bezier(.645,.045,.355,1);
        }
      }
    }
    
  5.3.1实现clearable功能
  首先获取父组件传递的clearable值，然后给i标签绑定一个点击事件，这个事件触发input事件回调，当点击叉号字体图标时，将父组件的value清空：
  
      clear () {
        this.$emit('input', '')
      }
      
  5.3.2实现showPassword功能
  实现showPassword功能的思路很简单，就是改变input的type类型即可。但是，我们不能直接改变父组件传递过来的type值，但是我们可以使用判断type值的方式，实现type的改变。
  
  首先设置一个布尔类型的变量，并且设置点击事件改变这个变量：
  
   data () {
      return {
        // 显示是否显示密码框
        passwordVisible: false
      }
    },
    
  methods: {
      handlePassword () {
        this.passwordVisible = !this.passwordVisible
      }
    }
    
  然后我们在组件中需要在绑定type值时，进行两重判断。
  第一步、判断showPassword是否为真；第二步、如果为真则通过passwordVisible去判断type为text还是password，以此来控制隐藏和现实，否则type值就为传入的type值即可：
  
  :type="showPassword ? (passwordVisible ? 'text' : 'password') : type"
  ```



### 12.4 switch

- 参数支持：

  | 参数名        | 参数描述           | 参数类型 | 默认值  |
  | :------------ | :----------------- | :------- | :------ |
  | v-model       | 双向绑定           | 布尔类型 | false   |
  | name          | name属性           | string   | text    |
  | activeColor   | 自定义的激活颜色   | string   | #1ec63b |
  | inactiveColor | 自定义的不激活颜色 | string   | #dd001b |

- 事件支持：

  | 事件名称 | 事件描述           |
  | :------- | :----------------- |
  | change   | change时触发的事件 |

- step1: 基本框架和样式

  ```
  switch组件基本框架：
  <template>
    <div class="one-switch">
      <span class="on-switch_core">
        <span class="one-switch_button"></span>
      </span>
    </div>
  </template>
  
  
  switch组件样式：
  <style lang="scss" scoped>
    .one-switch{
      display: inline-block;
      align-items: center;
      position: relative;
      font-size: 14px;
      line-height: 20px;
      vertical-align: middle;
      .one-switch_core{
      margin: 0;
      display: inline-block;
      position: relative;
      width: 40px;
      height: 20px;
      border: 1px solid #dcdfe6;
      outline: none;
      border-radius: 10px;
      box-sizing: border-box;
      background: #dcdfe6;
      cursor: pointer;
      transition: border-color .3s,background-color .3s;
      vertical-align: middle;
      .one-switch_button{
        position:absolute;
        top: 1px;
        left: 1px;
        border-radius: 100%;
        transition: all .3s;
        width: 16px;
        height: 16px;
        background-color: #fff;
        }
      }
    }
  </style>
  ```

- step2: 双向绑定

  ```
  实现switch组件数据双向绑定和input组件相同，使用v-model语法糖即可。
  
  在父组件种通过v-model绑定数据，在组件内部获取value属性，并且定义一个回调函数与父组件通信，改变父组件中的绑定值即可。
  
  父组件：
  <one-switch v-model="active" ></one-switch>
  
  子组件，点击时改变is-checked类状态，触发滑块滑动：
  <div class="one-switch" :class="{'is-checked':value}" @click="handleClick">
    <span class="one-switch_core">
      <span class="one-switch_button"></span>
    </span>
  </div>
   
   methods: {
       handleClick () {
       	this.$emit('input', !this.value)
       }
   }
    
  滑动样式：
    // 选中样式
    .is-checked {
      .one-switch_core{
        border-color: #409eff;
        background-color: #409eff;
        .one-switch_button {
          transform: translateX(20px);
        }
      }
    }
  ```

- step3: 颜色自定义

  ```
  颜色自定义
  自定义switch组件的颜色，首先需要传入颜色的值，在子组件中获取后，使用ref获取节点，将背景颜色改变为对应颜色即可。
  
  父组件传递色彩参数：
       <one-switch
       v-model="active"
       active-color="#13ce66"
       inactive-color="#ff4949"
       ></one-switch>
       
       
  子组件中定义ref="core"以确定节点：
   <div class="one-switch" :class="{'is-checked':value}" @click="handleClick">
      <span class="one-switch_core" ref="core">
        <span class="one-switch_button"></span>
      </span>
    </div>
    
    
  通过mouted钩子和watch监听，在刚进入页面以及value改变时对颜色进行改变：
  
    mounted () {
      // 修改开关颜色
      if (this.activeColor || this.inactiveColor) {
        var color = !this.value ? this.activeColor : this.inactiveColor
        this.$refs.core.style.borderColor = color
        this.$refs.core.style.backgroundColor = color
      }
    },
    watch: {
      'value' (e) {
        // 修改开关颜色
        if (this.activeColor || this.inactiveColor) {
          var color = !e ? this.activeColor : this.inactiveColor
          this.$refs.core.style.borderColor = color
          this.$refs.core.style.backgroundColor = color
        }
      }
    }
  ```

- step4: name属性

  ```
  用户在使用switch组件的时候，实质上是当成表单元素来使用的。因此可能会用到组件的name属性。所以需要在switch组件中添加一个checkbox，并且当值改变的时候，也需要设置checkbox的value值。
  
  加入input标签：注意包围用div, 用label的话会点击到input上去
  <template>
    <div class="one-switch" :class="{'is-checked':value}" @click="handleClick">
      <span class="one-switch_core" ref="core">
        <span class="one-switch_button"></span>
      </span>
      <input type="checkbox" class="one-switch_input" :name="name" ref="input">
    </div>
  </template>
  
  1.设置标签样式，因为input标签只作为name绑定使用，所以将其隐藏起来：
    // 隐藏input标签
    .one-switch_input{
      position:absolute;
      width: 0;
      height: 0;
      opacity: 0;
      margin: 0;
    }
    
  2.我们在页面加载和点击时修改input的checked值，保证可以和value值同步：
    mounted () {
      // 修改开关颜色
      if (this.activeColor || this.inactiveColor) {
        var color = !this.value ? this.activeColor : this.inactiveColor
        this.$refs.core.style.borderColor = color
        this.$refs.core.style.backgroundColor = color
      }
      // 控制checkbox的值, input值同步value值
      this.$refs.input.checked = this.value
    },
    methods: {
      handleClick () {
        this.$emit('input', !this.value)
        // 控制checkbox的值,  input值同步value值
        this.$refs.input.checked = this.value
      }
    }
  ```
  
  

### 12.5 radio

> 很重要
>
> radio 和 checkbox 差不多
>
> form-item , form 也是用到了  providor 和 inject  祖孙间通讯

```
<template>
  <!-- label === value 是不行的，被group包裹后拿到的是还是自身的value, 此时是没有值的-->
  <label class="one-radio" :class="{'is-checked': label == model}">
    <span class="one-radio_input">
      <span class="one-radio_inner"></span>
      <input
          type="radio"
          class="one-radio_original"
          :value="label"
          v-model="model"
      >
    </span>
    <span class="one-radio_label">
      <slot></slot>
      <!-- 如果没有传值，就把label作为文本显示 -->
      <template v-if="!$slots.default">{{label}}</template>
    </span>
  </label>
</template>
<script>
export default {
  name: 'oneRadio',
  props: {
    label: {
      type: [String, Number, Boolean],
      defualt: ''
    },
    value: null,
    name: {
      type: String,
      defualt: ''
    }
  },
  inject: {
    RadioGroup: {
      default: ''
    }
  },
  computed: {
    model: {
      get () {
        return this.isGroup ? this.RadioGroup.value : this.value
      },
      set (value) {
        // 触发父组件的input事件
        this.isGroup ? this.RadioGroup.$emit('input', value) : this.$emit('input', value)
      }
    },
    // 用于判断radio是否被radioGroup包裹
    isGroup () {
      return !!this.RadioGroup
    }
  },
  data () {
    return {}
  },
  methods: {}
}
</script>
<style lang="scss" scoped>
  .one-radio{
    color: #606266;
    font-weight: 500;
    line-height: 1;
    position: relative;
    cursor: pointer;
    display: inline-block;
    white-space: nowrap;
    outline: none;
    font-size: 14px;
    margin-right: 30px;
    -moz-user-select: none;
    -webkit-user-select: none;
    -moz-user-select: none;
    .one-radio_input{
      white-space: nowrap;
      cursor: pointer;
      outline: none;
      display: inline-block;
      line-height: 1;
      position: relative;
      vertical-align: middle;
      .one-radio_inner{
        border: 1px solid #dcdfe6;
        border-radius: 100%;
        width: 14px;
        height: 14px;
        background-color: #fff;
        position: relative;
        cursor: pointer;
        display: inline-block;
        box-sizing: border-box;
        &:after{
          width: 4px;
          height: 4px;
          border-radius: 100%;
          background-color: #fff;
          content: "";
          position: absolute;
          left: 50%;
          top: 50%;
          transform: translate(-50%,-50%) scale(0);
          transition: transform .15s ease-in;
        }
      }
      .one-radio_original{
        opacity: 0;
        outline: none;
        position: absolute;
        z-index: -1;
        top: 0;
        left: 0px;
        right: 0;
        bottom: 0;
        margin: 0;
      }
    }
    .one-radio_label{
      font-size: 14px;
      padding-left: 10px;;
    }
  }
  
  // 选中的样式
  .one-radio.is-checked{
    .one-radio_input{
      .one-radio_inner{
        border-color: #409eff;
        background-color: #409eff;
        &:after{
          transform: translate(-50%,-50%) scale(1);
        }
      }
    }
    .one-radio_label{
      color:#409eff;
    }
  }
</style>


附radio-group组件代码：
<template>
  <div class="one-radio-group">
    <slot></slot>
  </div>
</template>
<script>
export default {
  name: 'oneRadioGroup',
  provide () {
    return {
      RadioGroup: this
    }
  },
  props: {
    // 组件接收到了value值，我们需要触发这个组件的input事件
    // provide 与 inject  用来做祖孙之间得组件通讯
    value: null
  }
}
</script>
<style lang="scss" scoped>
</style>

// 使用
```



### 12.6 checkbox

> isChecked () {
>       // 如果十group包裹，判断label是否在model中         
>       // 如果没有group包裹,直接使用model
>       return  this.isGroup ? this.model.includes(this.label) : this.model
>     }
>
>    value: {
>       type: Boolean,
>       default: false
>     },





```
<template>
  <label class="one-checkbox" :class="{' is-checked': isChecked}">
    <span class="one-checkbox_input">
      <span class="one-checkbox_inner"></span>
      <input type="checkbox"
          class="one-checkbox_original"
          :name="name"
          v-model="model"
          :value="label"
      >
    </span>
    <span class="one-checkbox_label">
      <slot></slot>
      <template v-if="!$slots.default">
        {{label}}
      </template>
    </span>
  </label>
</template>
<script>
export default {
  name: 'oneCheckbox',
  inject: {
    CheckboxGroup: {
      default: ''
    }
  },
  props: {
    value: {
      type: Boolean,
      default: false
    },
    label: {
      type: String,
      default: ''
    },
    name: {
      type: String,
      default: ''
    }
  },
  computed: {
    model: {
      get () {
        return this.isGroup ? this.CheckboxGroup.value : this.value
      },
      set (value) {
        this.isGroup ? this.CheckboxGroup.$emit('input', value) : this.$emit('input', value)
        console.log(value)
      }
    },
    isGroup () {
      return !!this.CheckboxGroup
    },
    isChecked () {
      // 如果十group包裹，判断label是否在model中         
      // 如果没有group包裹,直接使用model
      return  this.isGroup ? this.model.includes(this.label) : this.model
    }
  }
}
</script>
 
<style lang="scss" scoped>
  .one-checkbox{
    color: #606266;
    font-weight: 500;
    font-size: 14px;
    position: relative;
    cursor: pointer;
    display: inline-block;
    white-space: nowrap;
    user-select: none;
    margin-right: 30px;
    .one-checkbox_input{
      white-space: nowrap;
      cursor: pointer;
      outline: none;
      display: inline-block;
      line-height: 1;
      position: relative;
      vertical-align: middle;
      .one-checkbox_inner{
        display: inline-block;
        position: relative;
        border: 1px solid #dcdfe6;
        border-radius: 2px;
        box-sizing: border-box;
        width: 14px;
        height: 14px;
        background-color: #fff;
        z-index: 1;
        transition: border-color .25s cubic-bezier(.71,-.46,.29,1.46),background-color .25s,cubic-bezier(.71,-.46,.29,1.46);
        &:after{
          box-sizing: content-box;
          content: '';
          border: 1px solid #ffffff;
          border-left: 0;
          border-top: 0;
          height: 7px;
          left: 4px;
          position: absolute;
          top: 1px;
          transform: rotate(45deg) scaleY(0);
          width: 3px;
          transition: transform .15s ease-in .05s;
          transform-origin: center;
        }
      }
      .one-checkbox_original{
        opacity: 0;
        outline: none;
        position: absolute;
        left: 10px;
        margin: 0;
        width: 0;
        height: 0;
        z-index: -1;
      }
    }
    .one-checkbox_label{
      display: inline-block;
      padding-left: 10px;
      line-height: 19px;
      font-size: 14px;
    }
  }
  // 选中的样式
  .one-checkbox.is-checked{
    .one-checkbox_input{
      .one-checkbox_inner{
        background-color: #409eff;
        border-color: #409eff;
      }
      &:after{
        transform: rotate(45deg) scaleY(1);
      }
    }
    .one-checkbox_label{
      color: #409eff;
    }
  }
</style>


// checkbox-group组件和radio-group组件相似，这里不过多介绍了。

<template>
  <div class="one-checkbox-group">
    <slot></slot>
  </div>
</template>
<script>
export default {
  name: 'oneCheckboxGroup',
  provide () {
    return {
      CheckboxGroup: this
    }
  },
  props: {
    value: {
      type: Array
    }
  }
}
</script>
```



### 12.7 form

```
// form
<template>
  <div class="one-form">
    <slot></slot>
  </div>
</template>
<script>
export default {
  name: 'oneForm',
  provide () {
    return {
      Form: this
    }
  },
  props: {
    model: {
      type: Object,
      required: true
    },
    labelWidth: {
      type: String,
      default: '80px'
    }
  }
}
</script>


//form-item组件
<template>
  <div class="one-form-item">
    <label :style="labelStyle" class="one-form-item_label">{{label}}</label>
    <div class="one-form-item_content">
      <slot></slot>
    </div>
  </div>
</template>

<script>
export default {
  name: 'oneFormItem',
  props: {
    label: {
      type: String,
      default: ''
    }
  },
  inject: ['Form'],
  computed: {
    labelStyle () {
      return {
        width: this.Form.labelWidth
      }
    }
  }
}
</script>
 
<style lang="scss" scoped>
  .one-form-item{
    margin-bottom: 25px;
    .one-form-item_label{
      text-align: right;
      vertical-align: middle;
      float: left;
      font-size: 14px;
      color: #606266;
      line-height: 40px;
      padding: 0 12px 0 0;
      box-sizing: border-box;
    }
    .one-form-item_content{
      line-height: 40px;
      position: relative;
      font-size: 14px;
      overflow: hidde;
    }
  }
</style>
 
```

### 12.8 打包发布





# vue3.x

## 0. changelog

> https://juejin.cn/post/7030992475271495711#heading-0

```
1. vite
	//要构建一个 Vite + Vue 项目，运行，使用 NPM:
    npm init @vitejs/app 项目名
    
    //使用 Yarn:
    yarn create @vitejs/app 项目名
    
    //你会觉得非常快速的创建了项目，然而它并没有给你下载依赖，你还有进入文件然后
    npm install (or yarn)
    
2. 按需导入
	main.js 
		import { createApp } from "vue";
		import App from "./App.vue"
		createApp(App).use(store).use(router).mount("#app")
		
3. template
	没有了根标签
	
4. Composition API
	setup 入口，一定要有return, 没有this, 兼容vue2的写法如：data，methods；beforeCreate和created这两个生命周期还要快； setup可以接受两个参数，第一个参数是props,也就是组件传值，第二个参数是context,上下文对象，context里面还有三个很重要的东西attrs，slots,emit，它们就相当于vue2里面的 this.$attrs, this.$slots, this.$emit。

		<script>
             export default {
              name: 'App',
              setup(){
               let name = '流星'
               let age = 18
       
               function say(){
                console.log(`我叫${name},今年${age}岁`)
               }

               return {
                    name,
                    age,
                    say
               }
              }
             }
            </script>

5. 不能使用 slot="XXX",要使用v-slot，不然会报错
    <template>
      <div class="home">
        <HelloWorld wish="不掉发" wishes="变瘦" @carried="carried">
          <h3>实现插槽1</h3>
          <template v-slot:dome>
            <h4>实现插槽2</h4>
          </template>
        </HelloWorld>
      </div>
    </template>

6. 响应式 ref & reactive
	ref:
	我们写的不是响应式数据，我们写的只是字符串和数字，那怎么变成响应式数据呢，那就呀引入ref，但是如果我们直接在代码里面修改是修改不了的,不如打印一下name和age，你会发现ref把它们变成了对象 并且还是RefImpl的实例对象
	
<template>
  <div class="home">
    <h1>姓名：{{name}}</h1>
    <h1>年龄：{{age}}</h1>
    <button @click="say">修改</button>
  </div>
</template>

<script>
import {ref} from 'vue'
export default {
  name: 'Home',
  setup(){
    let name = ref('燕儿')
    let age = ref(18)
    console.log(name)
    console.log(age)
    //方法
    function say(){
      name='苒苒'
      age=20
      // name.value='苒苒'
  	  // age.value=20
    }
    return {
      name,
      age,
      say
    }
  }
}
</script>

那么要是我定义的ref是个对象呢，因为我们知道尽管ref后会变成RefImpl的实例对象，所以我们就用XX.value.xx进行修改

<template>
  <div class="home">
    <h1>姓名：{{name}}</h1>
    <h1>年龄：{{age}}</h1>
    <h2>职业：{{job.occupation}}</h2>
    <h2>薪资：{{job.salary}}</h2>
    <button @click="say">修改</button>
  </div>
</template>

<script>
import {ref} from 'vue'
export default {
  name: 'Home',
  setup(){
    let name = ref('燕儿')
    let age = ref(18)
    let job=ref({
      occupation:'程序员',
      salary:'10k'
    })
    console.log(name)
    console.log(age)
    //方法
    function say(){
      job.value.salary='12k'
    }
    return {
      name,
      age,
      job,
      say
    }
  }
}
</script>
job.value,你会发现，它不再是RefImpl实例对象，变成了Proxy实例对象; ref中是对象，自动会调用reactive。

	reactive:
		<template>
          <div class="home">
            <h1>姓名：{{name}}</h1>
            <h1>年龄：{{age}}</h1>
            <h2>职业：{{job.occupation}}<br>薪资：{{job.salary}}</h2>
            <h3>爱好：{{hobby[0]}},{{hobby[1]}},{{ hobby[2] }}</h3>
            <button @click="say">修改</button>
          </div>
        </template>

        <script>
        import {ref,reactive} from 'vue'
        export default {
          name: 'Home',
          setup(){
            let name = ref('燕儿')
            let age = ref(18)
            let job=reactive({
              occupation:'程序员',
              salary:'10k'
            })
            let hobby=reactive(['刷剧','吃鸡','睡觉'])
            console.log(name)
            console.log(age)
            //方法
            function say(){
              job.salary='12k'
              hobby[0]='学习'
            }
            return {
              name,
              age,
              job,
              say,
              hobby
            }
          }
        }
        </script>
 
ref与reactive的区别
    ref用来定义：基本类型数据。
    ref通过Object.defineProperty()的get与set来实现响应式（数据劫持）。
    ref定义的数据：操作数据需要.value，读取数据时模板中直接读取不需要.value。
    
    reactive用来定义：对象或数组类型数据。
    reactive通过使用Proxy来实现响应式（数据劫持）, 并通过Reflect操作源代码内部的数据。
    reactive定义的数据：操作数据与读取数据：均不需要.value。
    当然，我之前就说过，ref可以定义对象或数组的，它只是内部自动调用了reactive来转换。


	
7. 响应式原理
	Proxy
	
	const p=new Proxy(data, {
    // 读取属性时调用
        get (target, propName) {
            return Reflect.get(target, propName)
        },
    //修改属性或添加属性时调用
        set (target, propName, value) {
            return Reflect.set(target, propName, value)
        },
    //删除属性时调用
        deleteProperty (target, propName) {
            return Reflect.deleteProperty(target, propName)
        }
    }) 
    
8. computed, watch, watchEffect
// computed
<template>
  <div class="home">
    姓：<input type="text" v-model="names.familyName"><br>
    名：<input type="text" v-model="names.lastName"><br>
    姓名：<input type="text" v-model="names.fullName"><br>
  </div>
</template>

<script>
import {reactive,computed} from 'vue'
export default {
  name: 'Home',
  setup(){
    let names=reactive({
      familyName:'阿',
      lastName:'斌'
    })
    names.fullName=computed({
      get(){
        return names.familyName+'.'+names.lastName
      },
      set(value){
        let  nameList=value.split('.')
        names.familyName=nameList[0]
        names.lastName=nameList[1]
      }
    })
    return {
      names
    }
  }
}
</script>



// watch 
<template>
  <div class="home">
    <h1>当前数字为:{{num}}</h1>
    <button @click="num++">点击数字加一</button>
  </div>
</template>

<script>
import {ref, watch} from 'vue'
export default {
  name: 'Home',
  setup(){
    let num=ref('0')
    watch(num,(newValue,oldValue)=>{
      console.log(`当前数字增加了,${newValue},${oldValue}`)
    })
    return {
      num
    }
  }
}
</script>
当然这是监听ref定义出来的单个响应式数据，要是监听多个数据应该怎么办呢？其实可以用多个watch去进行监听，当然这不是最好的方法，最好的办法其实是监视数组

 watch([num,msg],(newValue,oldValue)=>{
      console.log('当前改变了',newValue,oldValue)
 })
 

我们现在监听的是监听ref定义出来数据，那么要是我们监听的是reactive
<template>
  <div class="home">
    <h1>当前姓名:{{names.familyName}}</h1>
    <h1>当前年龄:{{names.age}}</h1>
    <h1>当前薪水:{{names.job.salary}}K</h1>
    <button @click="names.familyName+='!'">点击加!</button>
    <button @click="names.age++">点击加一</button>
    <button @click="names.job.salary++">点击薪水加一</button>
  </div>
</template>

<script>
import {reactive,watch} from 'vue'
export default {
  name: 'Home',
  setup(){
    let names=reactive({
      familyName: '鳌',
      age:23,
      job:{
        salary:10
      }
    })
    
   watch(()=>names.age,(newValue,oldValue)=>{
      console.log('names改变了',newValue,oldValue)
    })
    
   // 多个数据
   watch([()=>names.age,()=>names.familyName],(newValue,oldValue)=>{
      console.log('names改变了',newValue,oldValue)
    })
    
   // ok，要是我们监听的是深度的属性那要怎么办呢？你会发现我要是只监听第一层是监听不到的，那么我们有两种写法
   //第一种
    watch(()=> names.job.salary,(newValue,oldValue)=>{
      console.log('names改变了',newValue,oldValue)
    })
    //第二种
    watch(()=> names.job,(newValue,oldValue)=>{
      console.log('names改变了',newValue,oldValue)
    },{deep:true}) 
  }
}
</script>
    

// watchEffect


9. 生命周期
setup里面应该这样写

beforeCreate===>Not needed*
created=======>Not needed*
beforeMount ===>onBeforeMount
mounted=======>onMounted
beforeUpdate===>onBeforeUpdate
updated =======>onUpdated
beforeUnmount ==>onBeforeUnmount
unmounted =====>onUnmounted

10. hooks
Vue3 的 hook函数 相当于 vue2 的 mixin, 不同在与 hooks 是函数
Vue3 的 hook函数 可以帮助我们提高代码的复用性, 让我们能在不同的组件中都利用 hooks 函数
可以用到外部的数据，生命钩子函数

11. toRefs 和 toRef
	toRef翻译过来其实就是把什么变成ref类型的数据，可能大家会觉得没有什么用，毕竟我们之前定义时就已经定义成ref, 那就是把name.xx变为响应式，然后操作它时会自动的去修改name里面的数据
return {
  name:toRef(names,'name'),
  age:toRef(names,'age'),
  salary:toRef(names.job,'salary')
}


12. provider, inject
都知道组件传值吧，在vue2中，如果要在后代组件中使用父组件的数据，那么要一层一层的父子组件传值或者用到vuex，但是现在，无论组件层次结构有多深，父组件都可以作为其所有子组件的依赖提供者。这个特性有两个部分：父组件有一个 provide 选项来提供数据，子组件有一个 inject 选项来开始使用这些数据。

// 父
import { provide } from 'vue'
    setup(){
         let fullname = reactive({name:'阿月',salary:'15k'})
         provide('fullname',fullname) // 给自己的后代组件传递数据
         return {...toRefs(fullname)}
    }
    
// 后代
import {inject} from 'vue'
    setup() {
         let fullname = inject('fullname')
         return {fullname}
    }

	
	
13. router
可能大家会想到路由跳转的问题，可能大家会以为还是用this.$router.push来进行跳转，但是哦，在vue3中，这些东西是没有的，它是定义了一个vue-router然后引入的useRoute,useRouter 相当于vue2的 this.$route，this.$router,然后其他之前vue2的操作都可以进行

import {useRouter,useRoute} from "vue-router";
setup(){
  const router= useRouter()
  const route= useRoute()
  function fn(){
    this.$router.push('/about')
  }
  onMounted(()=>{
    console.log(route.query.code)
  })
  return{
    fn
  }
}

14. 全局api的转移
app.config.xxxx
app.component
app.directive
app.mixin
app.use
app.config.globalProperties


15. 其他改变
移除keyCode作为 v-on 的修饰符，同时也不再支持config.keyCodes
移除v-on.native修饰符
移除过滤器（filter）

响应式判断
import {ref, reactive, readonly, isRef, isReactive, isReadonly, isProxy } from 'vue'

export default {
  name:'App',
  setup(){
    let fullName = reactive({name:'小唐',price:'20k'})
    let num = ref(0)
    let fullNames = readonly(fullName)
    console.log(isRef(num))
    console.log(isReactive(fullName))
    console.log(isReadonly(fullNames))
    console.log(isProxy(fullName))
    console.log(isProxy(fullNames))
    console.log(isProxy(num))
    return {}
  }
}
```



## 1. 参考

```
https://www.bilibili.com/video/BV175411h7TN?from=search&seid=535398711802368847
https://www.bilibili.com/video/BV1JJ41137jb?from=search&seid=535398711802368847
http://www.liulongbin.top:8085
https://gitee.com/vsdeveloper/vue3-compositionAPI-study


https://www.bilibili.com/video/BV1LC4y1h7BF?from=search&seid=535398711802368847
https://www.bilibili.com/video/BV19C4y187Xz?from=search&seid=535398711802368847
****************************************************************************************
尤雨溪直播
https://www.bilibili.com/video/BV1Tg4y1z7FH?from=search&seid=535398711802368847
https://www.bilibili.com/video/BV1iA411J7cA?from=search&seid=535398711802368847
****************************************************************************************
源码
https://github.com/vuejs/vue-next
```



## 2. 安装

```
npm install -g @vue/cli

vue create my-project

npm install @vue/composition-api --save

import VueCompositionApi from '@vue/composition-api'

Vue.use(VueCompositionApi)


# 按需导入
const app = createApp(App)
app.use()
app.mixin()
app.component()
app.directive()

因此Vue2.x的以下全局API也需要改为ES6模块化引入：
Vue.nextTick()
Vue.observable不再支持，改为reactive
Vue.version
Vue.compile (仅全构建)
Vue.set (仅兼容构建)
Vue.delete (仅兼容构建)

除此之外，vuex和vue-router也都使用了Tree-Shaking进行了改进，不过api的语法改动不大
//src/store/index.js
import { createStore } from "vuex";

export default createStore({
  state: {},
  mutations: {},
  actions: {},
  modules: {},
});
//src/router/index.js
import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});
```



## 3. setup

> setup() 函数是 vue3 中，专门为组件提供的新属性。它为我们使用 vue3 的 Composition API (组合式api)新特性提供了统一的入口。

### 3.1 执行时机

```
setup 函数会在 beforeCreate 之后、created 之前执行
```



### 3.2 props

```
// 在props中定义当前组件允许外界传递过来的参数名称：
props: {
  p1: String
}

// 通过setup函数的第一个形参，接收 props 数据: 
setup(props, context) {
    console.log(props.p1)
}
```



### 3.3 context

```
setup 函数的第二个形参是一个上下文对象，这个上下文对象中包含了一些有用的属性，这些属性在vue 2.x中需要通过 this才能访问到，在vue 3.x中，它们的访问方式如下：

const MyComponent = {
  setup(props, context) {
    context.attrs
    context.slots
    context.parent
    context.root
    context.emit
    context.refs
  }
}

注意：在 setup()函数中无法访问到 this
```



## 4. reactive

> 定义：reactive() 函数接收一个**普通对象**，返回一个响应式的数据对象。
>
> 注意： 一旦return出去，后面的数据就不是响应式的了

### 4.1 基本语法

```
等价于 vue 2.x 中的 Vue.observable() 函数，vue 3.x 中提供了 reactive() 函数，用来创建响应式的数据对象，基本代码示例如下：

import { reactive } from '@vue/composition-api'

// 创建响应式数据对象，得到的state类似于 vue 2.x 中 data() 返回的响应式对象
const state = reactive({ count: 0 })
```



### 4.2 在template中访问

```
// 按需导入reactive函数：
import { reactive } from '@vue/composition-api'


//在setup()函数中调用reactive()函数，创建响应式数据对象：
setup() {
     // 创建响应式数据对象
    const state = reactive({count: 0})

     // setup函数中将响应式数据对象 return 出去，供template使用，一旦return出去，后面的数据就不是响应式的了
    return state
}

//在template中访问响应式数据：
<p>当前的 count 值为：{{count}}</p>
```



## 5. ref

> **给定的值**， ref本身也是能处理对象和数组的
>
> 和 reactive 区别

### 5.1 基本语法

```
ref() 函数用来根据给定的值创建一个响应式的数据对象，ref() 函数调用的返回值是一个对象，这个对象上只包含一个 .value 属性：

import { ref } from '@vue/composition-api'

// 创建响应式数据对象 count，初始值为 0
const count = ref(0)

// 如果要访问 ref() 创建出来的响应式数据对象的值，必须通过 .value 属性才可以
console.log(count.value) // 输出 0

// 让count的值 +1
count.value++

// 再次打印count的值
console.log(count.value) // 输出 1
```



### 5.2 在 template 中访问 ref 创建的响应式数据

```
// 在setup() 中创建响应式数据：
import { ref } from '@vue/composition-api'

setup() {
    const count = ref(0)

     return {
         count,
         name: ref('zs')
     }
}

// 在template中访问响应式数据：
<template>
  <p>{{count}} --- {{name}}</p>
</template>
```



### 5.3 在 reactive 对象中访问 ref 创建的响应式数据

```
当把 ref() 创建出来的响应式数据对象，挂载到 reactive() 上时，会自动把响应式数据对象展开为原始的值，不需通过 .value 就可以直接被访问，例如：

const count = ref(0)
const state = reactive({
  count
})

console.log(state.count) // 输出 0
state.count++ // 此处不需要通过 .value 就能直接访问原始值
console.log(count) // 输出 1



注意：新的ref 会覆盖 旧的ref，示例代码如下：
// 创建 ref 并挂载到 reactive 中
const c1 = ref(0)
const state = reactive({
  c1
})

// 再次创建ref，命名为c2
const c2 = ref(9)
// 将 旧ref c1 替换为 新ref c2
state.c1 = c2
state.c1++

console.log(state.c1) // 输出 10
console.log(c2.value) // 输出 10
console.log(c1.value) // 输出 0
```



## 6. isRef

```
isRef() 用来判断某个值是否为 ref() 创建出来的对象；应用场景：当需要展开某个可能为 ref() 创建出来的值的时候，例如：

import { isRef } from '@vue/composition-api'
const unwrapped = isRef(foo) ? foo.value : foo
```



## 7. toRefs

```
toRefs()函数可以将reactive()创建出来的响应式对象，转换为普通的对象，只不过，这个对象上的每个属性节点，都是 ref() 类型的响应式数据，最常见的应用场景如下：

import { toRefs } from '@vue/composition-api'
setup() {
    // 定义响应式数据对象
    const state = reactive({
      count: 0
    })

    // 定义页面上可用的事件处理函数
    const increment = () => {
      state.count++
    }

    // 在 setup 中返回一个对象供页面使用
    // 这个对象中可以包含响应式的数据，也可以包含事件处理函数
    return {
      // 将 state 上的每个属性，都转化为 ref 形式的响应式数据
      ...toRefs(state),
      // 自增的事件处理函数
      increment
    }
}

页面上可以直接访问 setup() 中 return 出来的响应式数据：
<template>
  <div>
    <p>当前的count值为：{{count}}</p>
    <button @click="increment">+1</button>
  </div>
</template>
```



## 8. computed

```
computed() 用来创建计算属性，computed() 函数的返回值是一个 ref 的实例。使用 computed 之前需要按需导入：

import { computed } from '@vue/composition-api'
```

### 8.1 创建只读的计算属性

```
在调用 computed() 函数期间，传入一个 function 函数，可以得到一个只读的计算属性，示例代码如下：

// 创建一个 ref 响应式数据
const count = ref(1)

// 根据 count 的值，创建一个响应式的计算属性 plusOne
// 它会根据依赖的 ref 自动计算并返回一个新的 ref
const plusOne = computed(() => count.value + 1)

console.log(plusOne.value) // 输出 2
plusOne.value++ // error
```



### 8.2 创建可读可写的计算属性

```
在调用 computed() 函数期间，传入一个包含 get 和 set 函数的对象，可以得到一个可读可写的计算属性，示例代码如下：

// 创建一个 ref 响应式数据
const count = ref(1)

// 创建一个 computed 计算属性
const plusOne = computed({
  // 取值函数
  get: () => count.value + 1,
  // 赋值函数
  set: val => {
    count.value = val - 1
  }
})

// 为计算属性赋值的操作，会触发 set 函数
plusOne.value = 9
// 触发 set 函数后，count 的值会被更新
console.log(count.value) // 输出 8
```



## 9. watch

> 侦听一个深度嵌套的对象属性变化时，需要设置`deep:true`
>
> 这是因为侦听一个响应式对象始终返回该对象的引用，因此我们需要对值进行深拷贝： () => _.cloneDeep(deepObj)

### 9.1 基本使用

```
watch() 函数用来监视某些数据项的变化，从而触发某些特定的操作，使用之前需要按需导入：

import { watch } from '@vue/composition-api'
const count = ref(0)

// 定义 watch，只要 count 值变化，就会触发 watch 回调
// watch 会在创建时会自动调用一次
watch(() => console.log(count.value))
// 输出 0

setTimeout(() => {
  count.value++
  // 触发watch回调，输出1
}, 1000)
```



### 9.2 监视指定的数据源

监视 `reactive` 类型的数据源：

```js
// 定义数据源
const state = reactive({ count: 0 })
// 监视 state.count 这个数据节点的变化
watch(() => state.count,
  (count, prevCount) => {
    /* ... */
  }
)
```

监视 `ref` 类型的数据源：

```js
// 定义数据源
const count = ref(0)
// 指定要监视的数据源
watch(count, (count, prevCount) => {
  /* ... */
})
```

### 9.3 监视多个数据源

监视 `reactive` 类型的数据源：

```js
const state = reactive({ count: 0, name: 'zs' })

watch(
  [() => state.count, () => state.name], // Object.values(toRefs(state)),
  ([count, name], [prevCount, prevName]) => {
    console.log(count) // 新的 count 值
    console.log(name) // 新的 name 值
    console.log('------------')
    console.log(prevCount) // 旧的 count 值
    console.log(prevName) // 新的 name 值
  },
  {
    lazy: true // 在 watch 被创建的时候，不执行回调函数中的代码
  }
)

setTimeout(() => {
  state.count++
  state.name = 'ls'
}, 1000)
```

监视 `ref` 类型的数据源：

```js
const count = ref(0)
const name = ref('zs')

watch(
  [count, name], // 需要被监视的多个 ref 数据源
  ([count, name], [prevCount, prevName]) => {
    console.log(count)
    console.log(name)
    console.log('-------------')
    console.log(prevCount)
    console.log(prevName)
  },
  {
    lazy: true
  }
)

setTimeout(() => {
  count.value++
  name.value = 'xiaomaolv'
}, 1000)
```

### 9.4 清除监视源

在 `setup()` 函数内创建的 `watch` 监视，会在当前组件被销毁的时候自动停止。如果想要明确地停止某个监视，可以调用 `watch()` 函数的返回值即可，语法如下：

```js
// 创建监视，并得到 停止函数
const stop = watch(() => {
  /* ... */
})

// 调用停止函数，清除对应的监视
stop()
```



### 9.5 清楚无效的异步任务

有时候，当被 `watch` 监视的值发生变化时，或 `watch` 本身被 `stop` 之后，我们期望能够清除那些无效的异步任务，此时，`watch` 回调函数中提供了一个 `cleanup registrator function` 来执行清除的工作。这个清除函数会在如下情况下被调用：

- watch 被重复执行了
- watch 被强制 `stop` 了

**Template 中的代码示例如下**：

```html
/* template 中的代码 */ <input type="text" v-model="keywords" />
```

**Script 中的代码示例如下**：

```js
// 定义响应式数据 keywords
const keywords = ref('')

// 异步任务：打印用户输入的关键词
const asyncPrint = val => {
  // 延时 1 秒后打印
  return setTimeout(() => {
    console.log(val)
  }, 1000)
}

// 定义 watch 监听
watch(
  keywords,
  (keywords, prevKeywords, onCleanup) => {
    // 执行异步任务，并得到关闭异步任务的 timerId
    const timerId = asyncPrint(keywords)

    // 如果 watch 监听被重复执行了，则会先清除上次未完成的异步任务
    onCleanup(() => clearTimeout(timerId))
  },
  // watch 刚被创建的时候不执行
  { lazy: true }
)

// 把 template 中需要的数据 return 出去
return {
  keywords
}
```



## 10. 生命周期钩子

新版的生命周期函数，可以按需导入到组件中，且只能在 `setup()` 函数中使用，代码示例如下：

```js
import { onMounted, onUpdated, onUnmounted } from '@vue/composition-api'

const MyComponent = {
  setup() {
    onMounted(() => {
      console.log('mounted!')
    })
    onUpdated(() => {
      console.log('updated!')
    })
    onUnmounted(() => {
      console.log('unmounted!')
    })
  }
}
```

下面的列表，是 vue 2.x 的生命周期函数与新版 Composition API 之间的映射关系：

- ~~`beforeCreate`~~ -> use `setup()`
- ~~`created`~~ -> use `setup()`
- `beforeMount` -> `onBeforeMount`
- `mounted` -> `onMounted`
- `beforeUpdate` -> `onBeforeUpdate`
- `updated` -> `onUpdated`
- `beforeDestroy` -> `onBeforeUnmount`
- `destroyed` -> `onUnmounted`
- `errorCaptured` -> `onErrorCaptured`



## 11. provide & inject

### 11.1 共享普通数据

`App.vue` 根组件：

```jsx
<template>
  <div id="app">
    <h1>App 根组件</h1>
    <hr />
    <LevelOne />
  </div>
</template>

<script>
import LevelOne from './components/LevelOne'
// 1. 按需导入 provide
import { provide } from '@vue/composition-api'

export default {
  name: 'app',
  setup() {
    // 2. App 根组件作为父级组件，通过 provide 函数向子级组件共享数据（不限层级）
    //    provide('要共享的数据名称', 被共享的数据)
    provide('globalColor', 'red')
  },
  components: {
    LevelOne
  }
}
</script>
```

`LevelOne.vue` 组件：

```jsx
<template>
  <div>
    <!-- 4. 通过属性绑定，为标签设置字体颜色 -->
    <h3 :style="{color: themeColor}">Level One</h3>
    <hr />
    <LevelTwo />
  </div>
</template>

<script>
import LevelTwo from './LevelTwo'
// 1. 按需导入 inject
import { inject } from '@vue/composition-api'

export default {
  setup() {
    // 2. 调用 inject 函数时，通过指定的数据名称，获取到父级共享的数据
    const themeColor = inject('globalColor')

    // 3. 把接收到的共享数据 return 给 Template 使用
    return {
      themeColor
    }
  },
  components: {
    LevelTwo
  }
}
</script>
```

`LevelTwo.vue` 组件：

```jsx
<template>
  <div>
    <!-- 4. 通过属性绑定，为标签设置字体颜色 -->
    <h5 :style="{color: themeColor}">Level Two</h5>
  </div>
</template>

<script>
// 1. 按需导入 inject
import { inject } from '@vue/composition-api'

export default {
  setup() {
    // 2. 调用 inject 函数时，通过指定的数据名称，获取到父级共享的数据
    const themeColor = inject('globalColor')

    // 3. 把接收到的共享数据 return 给 Template 使用
    return {
      themeColor
    }
  }
}
</script>
```



### 11.2 共享ref响应式数据

如下代码实现了点按钮切换主题颜色的功能，主要修改了 `App.vue` 组件中的代码，`LevelOne.vue` 和 `LevelTwo.vue` 中的代码不受任何改变：

```jsx
<template>
  <div id="app">
    <h1>App 根组件</h1>

    <!-- 点击 App.vue 中的按钮，切换子组件中文字的颜色 -->
    <button @click="themeColor='red'">红色</button>
    <button @click="themeColor='blue'">蓝色</button>
    <button @click="themeColor='orange'">橘黄色</button>

    <hr />
    <LevelOne />
  </div>
</template>

<script>
import LevelOne from './components/LevelOne'
import { provide, ref } from '@vue/composition-api'

export default {
  name: 'app',
  setup() {
    // 定义 ref 响应式数据
    const themeColor = ref('red')

    // 把 ref 数据通过 provide 提供的子组件使用
    provide('globalColor', themeColor)

    // setup 中 return 数据供当前组件的 Template 使用
    return {
      themeColor
    }
  },
  components: {
    LevelOne
  }
}
</script>
```



## 12. template refs

### 12.1 元素引用

示例代码如下：

```jsx
<template>
  <div>
    <h3 ref="h3Ref">TemplateRefOne</h3>
  </div>
</template>

<script>
import { ref, onMounted } from '@vue/composition-api'

export default {
  setup() {
    // 创建一个 DOM 引用
    const h3Ref = ref(null)

    // 在 DOM 首次加载完毕之后，才能获取到元素的引用
    onMounted(() => {
      // 为 dom 元素设置字体颜色
      // h3Ref.value 是原生DOM对象
      h3Ref.value.style.color = 'red'
    })

    // 把创建的引用 return 出去
    return {
      h3Ref
    }
  }
}
</script>
```



### 12.2 组件引用

`TemplateRefOne.vue` 中的示例代码如下：

```jsx
<template>
  <div>
    <h3>TemplateRefOne</h3>

    <!-- 4. 点击按钮展示子组件的 count 值 -->
    <button @click="showNumber">获取TemplateRefTwo中的count值</button>

    <hr />
    <!-- 3. 为组件添加 ref 引用 -->
    <TemplateRefTwo ref="comRef" />
  </div>
</template>

<script>
import { ref } from '@vue/composition-api'
import TemplateRefTwo from './TemplateRefTwo'

export default {
  setup() {
    // 1. 创建一个组件的 ref 引用
    const comRef = ref(null)

    // 5. 展示子组件中 count 的值
    const showNumber = () => {
      console.log(comRef.value.count)
    }

    // 2. 把创建的引用 return 出去
    return {
      comRef,
      showNumber
    }
  },
  components: {
    TemplateRefTwo
  }
}
</script>
```

`TemplateRefTwo.vue` 中的示例代码：

```jsx
<template>
  <div>
    <h5>TemplateRefTwo --- {{count}}</h5>
    <!-- 3. 点击按钮，让 count 值自增 +1 -->
    <button @click="count+=1">+1</button>
  </div>
</template>

<script>
import { ref } from '@vue/composition-api'

export default {
  setup() {
    // 1. 定义响应式的数据
    const count = ref(0)

    // 2. 把响应式数据 return 给 Template 使用
    return {
      count
    }
  }
}
</script>
```



## 13. 优化

```
1. 更快
    1.1 重构了 virtual dom
        标记静态内容，并区分动态内容
        更新时只diff动态的部分

    1.2 事件缓存
        cachehandles, 变成静态节点

    1.3 proxy的响应式对象
        实例化，添加，删除，修改属性等，都需要通过该代理器

        vue2.x object.defineProperty 来实现响应式对象

        vue3.x reactive, ref

2. 更小
    2.1 tree shaking 
        将无用的代码都摇掉，原生的，比如按需导入, 所有的API都通过ES6模块化的方式引入，这样就能让webpack或rollup等打包工具在打包时对没有用到API进行剔除，最小化bundle体积
	
3. 更易于维护
    3.1 从 flow 迁移到 typescript 
        类型检测，null引用，自动类型转换

    3.2 代码目录结构遵循monorepo
        将代码从src 分隔到一个个小的模块中，专注自己的几个模板
```



## 14. 新的内置组件

```
fragments 
	template中内容必须由一个div包裹，直接可以省略，不会报错
	
teleport
	内置标签，模态功能，遮罩
	<teleport> 
		...
    </teleport>
    
suspense
	呈现回退内容，占位逻辑或者加载异常逻辑， 异步组件
```



## 15. 新的构建工具vite

```
特点：
	1.快速的冷启动
	2.即时的模块热更新
	3.真正的按需编译

esm, 生产环境用rollup打包（tree shaking, 基于es modules）

npm init vite-app xxx
npm install 
npm run dev
```

