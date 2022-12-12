```
vue-css 按需选择相关的属性
https://blog.csdn.net/zhangxia_/article/details/125515747
https://www.runoob.com/css/css-align.html
	
https://www.bilibili.com/video/BV14J4114768?p=107    全
https://www.bilibili.com/video/BV1XJ411X7Ud?spm_id_from=333.337.search-card.all.click   简单
	
    选择器
    
    属性
    
	盒子模型  margin, border, padding （margin塌陷，bfc，after伪类）
	
	position（top, left, right, bottom, z-index）
		static
		relative
		fixed
		absolute
		sticky
		
	overflow  内容溢出时使用
		visible
		hidden
		scroll
		auto
		inherit
		
	float
		会使元素向左或向右移动，其周围的元素也会重新排列
		
		元素的水平方向浮动，意味着元素只能左右移动而不能上下移动。
		一个浮动元素会尽量向左或向右移动，直到它的外边缘碰到包含框或另一个浮动框的边框为止。
		浮动元素之前的元素将不会受到影响，浮动元素之后的元素将围绕它。

		left
		right
		none
		
		clear: none/right/left/both
		

	display(块元素，行内元素，行内块元素)
		none
		block
		inline-block
		box
		inline-box
		inline
		
	对齐
		https://www.runoob.com/css/css-align.html
	
	尺寸
		height
		width
		line-height
		max-height
		min-height
		
	
	疑难杂症：
		https://www.cnblogs.com/cobby/archive/2012/05/13/2498414.html
		https://blog.csdn.net/m0_63872974/article/details/123333901
		https://blog.csdn.net/qq_26327971/article/details/60583743
		https://juejin.cn/post/6997564962952445982
		https://juejin.cn/post/6940111892459618340
		https://juejin.cn/post/6985361507814998046
		https://blog.csdn.net/qq449245884/article/details/123268101
		https://zhuanlan.zhihu.com/p/413274882
		https://www.cnblogs.com/liutie1030/p/7813448.html
	
	像素和百分比
	flex
	em, rem(过时了, font-size)
    vw,vh, 按比例计算，vm适配，px转vw的小插件  px2vw
    页面(网页)适配，达到大小屏上显示完整
    
    style是设置的样式，computed是生效的样式，网页最小是12px, 小于12的，自动设置成12px,所以要扩大倍数， 比如40倍
    
    html{
    	font-size: 5.333vw
    }
    .box1{
    	width: 18.75rem
    	height: 0.875rem
    }
    
    过渡，动画，关键帧
	less
    sass
```