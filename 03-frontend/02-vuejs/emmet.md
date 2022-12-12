## 0. 参考文档

```
https://blog.csdn.net/weixin_42160117/article/details/114800988
https://www.jianshu.com/p/710b15281d56
```



## 1. HTML 初始化

```
! + Tab   快速生成Html文档常用结构代码,当然你可以去VS code安装包修改这个模板。

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="X-UA-Compatible" content="ie=edge">
  <title>Document</title>
</head>
<body>
  
</body>
</html>
```



## 2. 隐式标签

```
标签名 + Tab

不嵌套的直接键入内容指代div
其他常见的隐式指代如：ul,ol,table,em等

示例
<!-- 标签名Tab -->
<p></p>
```



## 3. 子代

```
> + Tab 

示例
<!-- div>p>span -->
<div>
    <p><span></span></p>
</div>
```



## 4. 同级

```
+号  +  Tab
示例
<!--多个dom元素之间用+号连接即可-->
<!--div+p+span-->
<div></div>
<p></p>
<span></span>
```



## 5. 到上级

> E^N 代表N是E的上级元素，其实是叔叔元素，如果没有上级元素，那么效果和E+N一样,E^^N是爷爷元素，以此类推

```
^号 + Tab
示例
<!--多个dom元素之间用+号连接即可-->
<!--div>p^span-->
<div><p></p></div>
<span></span>


<!--div>p+span-->
<div></div>
  <p></p>
  <spa></spa>
</div>
```

## 6.  分组

```
div>(ul>li+span)>a

<div>
    <ul>
        <li></li>
        <span></span>
    </ul>
    <a href=""></a>
</div>
```



## 7. 多个

```
标签名*number + tab

<!--div>ul>li*5-->
<div>
    <ul>
        <li></li>
        <li></li>
        <li></li>
        <li></li>
        <li></li>
    </ul>
</div>
```



## 8. 元素属性

```
键入 #id名 + tab
键入 .类名 + tab
生成普通属性[] + tab
生成元素内容 {} + tab


示例
<!--.nav-->
<div class="nav"></div>

<!--#id-->
<div id="itme"></div>

<!--一次添加多个属性 div#header.container[title="我是一个容器"]-->
<div id="header" class="container" title="我是一个容器"></div>

<!--div{我是文字内容}-->
<div>我是文字内容</div>
```



## 9. 添加序号

```
键入占位符｛$$｝ 或者 {$} 或者 {$排序}

<!--div.container#header>p{$$排序}*5-->
<div class="container" id="header">
    <p>01排序</p>
    <p>02排序</p>
    <p>03排序</p>
    <p>04排序</p>
    <p>05排序</p>
</div>
```



