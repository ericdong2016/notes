参考资料

```
https://www.bilibili.com/video/BV1KJ411Y7Zz?p=11                                   //入门
https://www.bilibili.com/video/BV1bK411H7YU?from=search&seid=1507236772512004325   //精简
https://www.bilibili.com/video/BV1KE411b7RQ?p=25								//大全

https://www.sass.hk/guide/													//快速入门
https://www.sass.hk/docs/													//完整教程

个人理解： 
	sass 自顶向下，css自底向上
```



## 1. 安装sass 

```
https://www.runoob.com/ruby/ruby-installation-windows.html
安装ruby
添加环境变量
ruby -v 

gem install sass 

sass -v
```



## 2. 编译

```
// scss编译成css
sass sass/xx.scss:css/xx.css

// 自动编译
sass --watch sass:css

// 修改编译输出的css格式
nested: 嵌套
compact: 紧凑
expanded: 扩展
compressed: 压缩

sass --watch sass:css --style expanded
```



## 3. sass和scss区别

> https://blog.csdn.net/jiaojsun/article/details/95093505

```
scss 符合现在的使用习惯，css3.0后出现, 兼容css3.0, scss的功能比sass更多， scss需要分号和花括号，对空白符号不敏感。

sass 文件的后缀是.scss
```



## 6. 变量

```
/* 
sass让人们受益的一个重要特性就是它为css引入了变量。你可以把反复使用的css属性值 定义成变量，然后通过变量名来引用它们，而无需重复书写这一属性值
sass使用$符号来标识变量
*/

// 1. 变量的声明, 单值，多值
$highlight-color: rgb(255, 145, 0);
$basic-border: 1px solid black;
$nav-color: #f90;
nav {
    $width: 100px;
    width : $width;
    color :$nav-color
}

/* 
//编译后
nav {
    width: 100px;
    color: #F90;
}
*/


// 2. 变量引用
.selected {
    border: 1px solid $highlight-color;
}

/* 
//编译后
.selected {
    border: 1px solid #F90;
}
*/

// 3.声明变量时也可以引用其他变量
$highlight-border: 1px solid $highlight-color;
.selected1 {
    border: $highlight-border
}

/* //编译后

.selected {
    border: 1px solid #F90;
}
 */

// 4.变量命名
$link_color: blue;
a {
    color: $link-color;
}


tips: 
    1.定义变量的时候可以使用下划线或者连字符，两者是一样的(对混合器和Sass函数的命名也适用)
    2.一个变量的多个值之间可以用空格分隔，也可以用逗号分隔
    3.变量分局部变量和全局变量
```



## 7. 嵌套

```
//1. 基本嵌套
.nav {
	height: 100px
	
}
.nav ul {
	mergin: 0
}

.nav ul li {
	float: left
	list-style: none
	padding: 5px
}


等价于

.nav {
	height: 100px
	ul {
		mergin: 0
		li {
            float: left
            list-style: none
            padding: 5px
        }
	}
	
}


//2. 调用父选择器(&)，通常在伪类选择器
.nav {
	height: 100px;
	ul {
		mergin: 0;
		li {
            float: left;
            list-style: none;
            padding: 5px;
        }
	}
	a {
		display: none; 
		color: #000;
		padding: 5px;
		&:hover {
			backgroud-color: red;
			color: #fff
		}
		// 另一种写法:
		举例来说，当用户在使用IE浏览器时，你会通过JavaScript在<body>标签上添加一个ie的类名
		body.ie & { color: green }
		
	}
	& &-text {
		color: blue
	}
}

//3. 群组选择器的嵌套
.container {
  h1, h2, h3 {margin-bottom: .8em}
}

==>  .container h1, .container h2, .container h3 { margin-bottom: .8em }

nav, aside {
  a {color: blue}
}

==>  nav a, aside a {color: blue}


//4. 子组合选择器和同层组合选择器：>、+和~;
article section { margin: 5px }
article > section { border: 1px solid #ccc }
你可以用子组合选择器>  选择一个元素的直接子元素。
第一个选择器会选择article下的所有命中section选择器的元素。
第二个选择器只会选择article下紧跟着的子元素中命中section选择器的元素。

你可以用同层相邻组合选择器+  选择header元素后紧跟的p元素：
header + p { font-size: 1.1em }

你也可以用同层全体组合选择器~，选择所有跟在article后的同层article元素，不管它们之间隔了多少其他元素：
article ~ article { border-top: 1px dashed #ccc }


//5. 嵌套属性
body {
	font-family: sans-serif;
	font-size: 15px;
	font-weight: normal;
	
	等价于
	
	font: {
		family: sans-serif;
		size: 15px;
		weight: normal;
	}
}


nav {
  border-style: solid;
  border-width: 1px;
  border-color: #ccc;
}
等价于
.nav {
	border: 1px solid #000 {
		left: 0;
		right: 0;
	}
}
```



## 8. 导入

```
css有一个特别不常用的特性，即@import规则，它允许在一个css文件中导入其他css文件。然而，后果是只有执行到@import时，浏览器才会去下载其他css文件，这导致页面加载起来特别慢。  注意

sass也有一个@import规则，但不同的是，sass的@import规则在生成css文件时就把相关文件导入进来。这意味着所有相关的样式被归纳到了同一个css文件中，而无需发起额外的下载请求。另外，所有在被导入文件中定义的变量和混合器（参见2.5节）均可在导入文件中使用。

使用sass的@import规则并不需要指明被导入文件的全名。你可以省略.sass或.scss文件后缀（见下图）。这样，在不修改样式表的前提下，你完全可以随意修改你或别人写的被导入的sass样式文件语法，在sass和scss语法之间随意切换

//1. 将样式分割成小部分，小部分叫做partials
sass局部文件的文件名以下划线开头。这样，sass就不会在编译时单独编译这个文件输出css，而只把这个文件用作导入。当你@import一个局部文件时，还可以不写文件的全名，即省略文件名开头的下划线。举例来说，你想导入themes/_night-sky.scss这个局部文件里的变量，你只需在样式表中写@import "themes/night-sky";

_base.scss   // 该文件不会被编译
    body {
        color: #red;
    }

style.scss
    @import "base";  // 注意格式
    .alert {
    }


//2. 默认值，在这种情况下，有时需要在你的样式表中对导入的样式稍作修改，sass有一个功能刚好可以解决这个问题，即默认变量值。 如果这个变量被声明赋值了，那就用它声明的值，否则就用这个默认值。

$fancybox-width: 400px !default;
.fancybox {
	width: $fancybox-width;
}

在上例中，如果用户在导入你的sass局部文件之前声明了一个$fancybox-width变量，那么你的局部文件中对$fancybox-width赋值400px的操作就无效。如果用户没有做这样的声明，则$fancybox-width将默认为400px。


//3. 嵌套导入
跟原生的css不同，sass允许@import命令写在css规则内。这种导入方式下，生成对应的css文件时，局部文件会被直接插入到css规则内导入它的地方。举例说明，有一个名为_blue-theme.scss的局部文件，内容如下：
aside {
  background: blue;
  color: white;
}

然后把它导入到一个CSS规则内，如下所示：
.blue-theme {
	@import "blue-theme"
}

生成的结果跟你直接在.blue-theme选择器内写_blue-theme.scss文件的内容完全一样。
.blue-theme {
  aside {
    background: blue;
    color: #fff;
  }
}


//4. 原生的css  你可以把原始的css文件改名为.scss后缀，即可直接导入了
有时，可用css原生的@import机制，在浏览器中下载必需的css文件.
由于sass兼容原生的css，所以它也支持原生的CSS@import. 尽管通常在sass中使用@import时，sass会尝试找到对应的sass文件并导入进来，但在下列三种情况下会生成原生的CSS@import，尽管这会造成浏览器解析css时的额外下载：
被导入文件的名字以.css结尾；
被导入文件的名字是一个URL地址，由此可用谷歌字体API提供的相应服务；
被导入文件的名字是CSS的url()值。

这就是说，你不能用sass的@import直接导入一个原始的css文件，因为sass会认为你想用css原生的@import。
但是，因为sass的语法完全兼容css，所以你可以把原始的css文件改名为.scss后缀，即可直接导入了。  重点
```



## 9. 注释

```
//     这种注释内容不会出现在生成的css文件中

/**/   这种注释内容不会出现在生成的css文件中

/*!
	强制注释， 会出现在代码中
*/
```



## 10. mixin

> 变量的升级版， 代码块，也可使用import

```
混合器, 复用代码，如果你的整个网站中有几处小小的样式类似（例如一致的颜色和字体），那么使用变量来统一处理这种情况是非常不错的选择。但是当你的样式变得越来越复杂，你需要大段大段的重用样式的代码，独立的变量就没办法应付这种情况了。你可以通过sass的混合器实现大段样式的重用。

@mixin 名字(参数1，参数2...)
可以嵌套


// 定义
@mixin rounded-corners {
  -moz-border-radius: 5px;
  -webkit-border-radius: 5px;
  border-radius: 5px;
}
// 使用
.alert-warnging {
	@include rounded-corners;
}

// 传递参数
@mixin alert($text-color, $background) {
	color: $text-color;
	background-color: $background;
	a {
		color: darken($text-color, 10%)
	}
}

.alert-warninng {
	@include alert(#red, #blue)
}

.alert-info {
	@include alert($text-color:#red, $background:#blue)
}

// 默认参数
为了在@include混合器时不必传入所有的参数，我们可以给参数指定一个默认值。参数默认值使用$name: default-value的声明形式，默认值可以是任何有效的css属性值，甚至是其他参数的引用，如下代码：

@mixin link-colors($normal, $hover: $normal, $visited: $normal) {
  color: $normal;
  &:hover { color: $hover; }
  &:visited { color: $visited; }
}

@include link-colors(red)  

$hover和$visited也会被自动赋值为red
```



## 11. 继承

> 选择器继承来精简css
>
> 不建议使用

```
继承当前 及 当前有关的组合选择器的格式
// e.g.1:
.alert {
	pardding: 15px
}

.alert a {
	font-weight: bold;
}

.alert-info {
	@extend .alert;
	background-color: #red;
}

// e.g.2:
.seriousError不仅会继承.error自身的所有样式，任何跟.error有关的组合选择器样式也会被.seriousError以组合选择器的形式继承，如下代码:

//.seriousError从.error继承样式
.error a{  // 应用到.seriousError a
  color: red;
  font-weight: 100;
}
h1.error { // 应用到hl.seriousError
  font-size: 1.2rem;
}


// 高级用法： 
接下来的这段代码定义了一个名为disabled的类，样式修饰使它看上去像一个灰掉的超链接。通过继承a这一超链接元素来实现：

.disabled {
  color: gray;
  @extend a;
}

假如一条样式规则继承了一个复杂的选择器，那么它只会继承这个复杂选择器命中的元素所应用的样式。举例来说， 如果.seriousError@extend.important.error ， 那么.important.error 和h1.important.error 的样式都会被.seriousError继承， 但是.important或者.error下的样式则不会被继承。这种情况下你很可能希望.seriousError能够分别继承.important或者.error下的样式。

如果一个选择器序列（#main .seriousError）@extend另一个选择器（.error），那么只有完全匹配#main .seriousError这个选择器的元素才会继承.error的样式，就像单个类 名继承那样。拥有class="seriousError"的#main元素之外的元素不会受到影响。


// 细节：
@extend有两个要点你应该知道。

1.跟混合器相比，继承生成的css代码相对更少。因为继承仅仅是重复选择器，而不会重复属性，所以使用继承往往比混合器生成的css体积更小。如果你非常关心你站点的速度，请牢记这一点。
2.继承遵从css层叠的规则。当两个不同的css规则应用到同一个html元素上时，并且这两个不同的css规则对同一属性的修饰存在不同的值，css层叠规则会决定应用哪个样式。相当直观：通常权重更高的选择器胜出，如果权重相同，定义在后边的规则胜出。

混合器本身不会引起css层叠的问题，因为混合器把样式直接放到了css规则中，而继承存在样式层叠的问题。被继承的样式会保持原有定义位置和选择器权重不变

// 最佳实践
避免这种情况出现的最好方法就是不要在css规则中使用后代选择器（比如.foo .bar）去继承css规则。

```



## 12. 数据类型

```
sass -i

type-of(5)
type-of(5px)
type-of(hello)
type-of(1px red)


数字：1，2，10px
	2 + 8
	2 * 8
   （8 / 2）
    5px + 2px
    5px * 2 
    ( 5px / 2 ) 
    
    常用的数字函数：
        abs(10)
        abs(-10px)
        round(3.5)
        round(3.2)
        cell(3.1)
        floor(3.6)
        min(1,2,3)
        max(1,2,3)
	
字符串：
	“ning” + hao 
	"ning" + 8080 
	"ning" - hao   // "ning-hao"
	
    字符串函数：
        $greeting: "hello"
        $greeting

        to-upper-case($greeting)
        str-length($greeting)
        str-index($greeting, "hello")  // 索引从1开始
        str-insert($greeting, ".net", 14)
	
颜色：
   RGB(255,0,0)
   red
   #FF0000
   hls(0, 100%, 50%)
   
   rgb()
   rgba(255，0，0 ，0.8 )    // 带透明度 0-1 之间
   hsl(0，100%， 50%)        // 色相，饱和度，明度
   hsla()
   
   adjust-hue 					 // 调节
   lighten($base_color, 80%)      // 更亮，明度
   darken($base_color, 20%)      //  更黯， 明度
   saturate($base_color,50%)    // 增加纯度，饱和度
   desaturate    // 减少纯度
   
   transparentize()
   opacify($base_color, 0.3)      // 增加alpha/透明度
   
   
列表: 数组， 用空格或逗号作分隔符
	padding: 5px 10px, 5px 0 
	border: 
	
    列表函数：
        length(5px 10px)
        nth(5px 10px, 1)   //5px
        index(1px solid red, red)
        append(5px 10px 5px)
        join(5px 10px, 5px 0, comma)  // 逗号分隔
	
map: (key1: value1, key2: value2)
	$map: (k1:v1, k2:v2)
	e.g: $colors: (light: #ffffff, dark: #000000)
	
	map-get($colors, light)
	
	map-keys($colors)
	
	map-values($colors)
	
	map-has-key()
	
	map-merge($colors, (xx:yyy))
	
	map-remove($colors, light)
	
	
布尔值：true, false
	5px > 3px
	() and ()
	() or ()
	not()
	
空值: null
```



## 13. 差值语句

>  interpolation    #{}

```
$name: foo;
$attr: border;
p.#{$name} {
  #{$attr}-color: blue;
}
编译为
p.foo {
  border-color: blue; 
}




p {
  $font-size: 12px;
  $line-height: 30px;
  font: #{$font-size}/#{$line-height};
}
编译为
p {
  font: 12px/30px; }
```



## 14. 各种语句

```
body {
	@if $use_prefix {
		-webkit-border-radius: 5px;
	}@else if xxx {
		
	}@else {
		
	}
}


@for $val    from  开始值   through/to   结束值     {}

@for $i from 1 through $columns {
	.col-#{$i} {
		width: 100% / $columns * $i 
	}
}


@each $icon in $icons {
	.icon-#{$icon} {
		background-image: url(../images/icons/#{$icon}.png)
	}
}


@while $i > 0 {
	.item-#{$i} {
		width: 5px * $i;
	}
	$i: $i - 2 
}
```



## 15. 自定义函数

```
@function 名称(参数1，参数2) {
	@return xxx
}


$colors: (ligth: #000000, dark: #ffffff)

@function color($key) { 
	@return map-get($colors, $key)
}

body {
	background-color: color($colors)
}
```



## 16. 警告

```
@if not map-has-key($colors, $key) {
	@warn ""
}
```



## 17. !default

```
可以在变量的结尾添加 !default 给一个未通过 !default 声明赋值的变量赋值，此时，如果变量已经被赋值，不会再被重新赋值，但是如果变量还没有被赋值，则会被赋予新的值。

$content: "First content";
$content: "Second content?" !default;
$new_content: "First time reference" !default;

#main {
  content: $content;
  new-content: $new_content;
}
编译为
#main {
  content: "First content";
  new-content: "First time reference"; }
  
  
变量是 null 空值时将视为未被 !default 赋值。
$content: null;
$content: "Non-null content" !default;

#main {
  content: $content;
}
编译为
#main {
  content: "Non-null content"; }
```



## 18. media

```
media screen适应分辨率变化

Sass中 @media 指令与 CSS 中用法一样，只是增加了一点额外的功能：允许其在 CSS 规则中嵌套。如果 @media 嵌套在 CSS 规则内，编译时，@media 将被编译到文件的最外层，包含嵌套的父选择器。这个功能让 @media 用起来更方便，不需要重复使用选择器，也不会打乱 CSS 的书写流程。  

.sidebar {
  width: 300px;
  @media screen and (orientation: landscape) {
    width: 500px;
  }
}

编译为
.sidebar {
  width: 300px; }
  @media screen and (orientation: landscape) {
    .sidebar {
      width: 500px; 
    } 
  }
	  
	  
@media 的 queries 允许互相嵌套使用，编译时，Sass自动添加 and
@media screen {
  .sidebar {
    @media (orientation: landscape) {
      width: 500px;
    }
  }
}
编译为
@media screen and (orientation: landscape) {
  .sidebar {
    width: 500px;
  } 
}





e.g:
@charset "UTF-8";
 
//背景颜色
$all-bgColor:#5b9bd5;
 
//封装方法(传入4个参数，方法必须写前面)
@mixin allSize-PX($oneBtn-width,$oneBtn-height,$font-size,$date-width) {
  /*中间按钮*/
  .oneBtn{
    margin: 0 auto;
    width: $oneBtn-width;
    height: $oneBtn-height;
  }
  
  /*时间选择*/
  .date {
    border: none;
    width: $date-width;
    height: 30px;
    background-color: $all-bgColor;
    padding-top: 2px;
    font-size: $font-size;
  }
}
 
/* css注释：设置了浏览器宽度不小于1401px时 abc 显示1200px宽度 */
@media screen and (min-width: 1401px) {
  @include allSize-PX(
          $oneBtn-width:250px,
          $oneBtn-height:100px,
          $font-size:18px,
          $date-width:110px
  );
}
 
/* 设置了浏览器宽度不大于1400px时 */
@media screen and (max-width: 1400px) {
  @include allSize-PX(
          $oneBtn-width:220px,
          $oneBtn-height:80px,
          $font-size:16px,
          $date-width:100px
  );
}
 
@media screen and (max-width: 1200px){
  @include allSize-PX(
          $oneBtn-width:190px,
          $oneBtn-height:70px,
          $font-size:15px,
          $date-width:90px
  );
}
 
/* 设置了浏览器宽度不大于900px时 abc 显示900px宽度 */
@media screen and (max-width: 900px) {
  @include allSize-PX (
          $oneBtn-width:170px,
          $oneBtn-height:65px,
          $font-size:14px,
          $date-width:80px
   ); 
}
```



## 19. 前端切图

```
photoshop, 更改缓存盘，更改默认单位

预设： 标尺，段落，图层(分组，很重要，自动选择)，信息，工具(吸管(颜色)，裁切)

将图片放到一张图片上的，需要的时候加载出来，定好位置就行

切图优化：3s
	1. 颜色代替图片
	2. 雪碧图的使用
	3. 字体图标的使用

markdown
tinyPNG
前端自动化  gup等一键生成雪碧图等

pxcook
avocook 
蓝湖等，自动切图，生成css代码
```

