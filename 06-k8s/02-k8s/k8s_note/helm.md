# helm

> helm安装包： https://github.com/helm/helm
>
> helm 仓库：    https://hub.helm.sh/
>
> helm 镜像源：
>
> 	aliyun     https://kubernetes.oss-cn-hangzhou.aliyuncs.com/charts
> 		
> 	stable     http://mirror.azure.cn/kubernetes/charts
> 	#incubator http://mirror.azure.cn/kubernetes/charts-incubator
> 	#svc-cat   http://mirror.azure.cn/kubernetes/svc-catalog-charts
> 		
> 	https://kubernetes-charts.storage.googleapis.com/
> 	https://helm.elastic.co/
> 		
> 	e.g.:
> 	helm repo add aliyun https://kubernetes.oss-cn-hangzhou.aliyuncs.com/charts





## 1.基本概念

```
定义：包管理工具，不同yaml文件，更改属性，就可实现相应功能，通过打包的方式，支持发布的版本管理和控制，很大	程度上简化了k8s应用的管理和部署。比如：监控，日志

本质： 让K8s的应用管理可配置，动态生成(资源清单)

2个概念：
    chart：  应用信息的集合，包括配置模板, 配置参数, 依赖关系, 文档说明等
    release：chart运行实例, 代表一个运行的应用，chart能被多次安装到同一个集群，每次都是一个release

2个组件：
	helm client --- grpc ---> tiller服务器(默认在kube-system名称空间下) ---> kube api
```



## 2. 下载安装

> helm安装包:  https://get.helm.sh/helm-v2.13.1-linux-386.tar.gz

```
// 部署客户端
# wget https://get.helm.sh/helm-v2.13.1-linux-386.tar.gz

tar -xvf helm-v2.13.1-linux-386.tar.gz

cd linux-386 

cp helm /usr/local/bin 

chmod a+x  /usr/local/bin/helm


// 部署服务端
// 为了安装好服务端 tiller, 需要先在机器上 安装好 kubectl 和 kubeconfig 文件，确保kubectl 可以访问apiserver,  因为kube apiserver开启了rbac访问控制，所以需要创建tiller使用的service account:tiller并分配合适的角色给它。

# vim tiller-rbac.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: tiller
  namespace: kube-system
---
kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1beta1
metadata:
  name: tiller
roleRef:
  kind: ClusterRole
  name: cluster-admin
  apiGroup: rbac.authorization.k8s.io
subjects:
  - kind: ServiceAccount
    name: tiller
    namespace: kube-system


kubectl create -f tiller-rbac.yaml

// 如果有重复的，删除sa, clusterrolebinding

// 每个节点上加载该镜像
docker load helm-tiller.tar

// 创建一个deployment的tiller服务端, 该tiller-deployment注入到了kubernetes中
helm init --service-account tiller  --skip-refresh

kubectl get pod/deployment -n kube-system   # 可以看到tiller-deploy-xxx 在运行

helm version

Client: &version.Version{SemVer:"v2.13.1", GitCommit:"618447cbf203d147601b4b9bd7f8c37a5d39fbb4", GitTreeState:"clean"}
Server: &version.Version{SemVer:"v2.13.1", GitCommit:"618447cbf203d147601b4b9bd7f8c37a5d39fbb4", GitTreeState:"clean"}

```



## 3. 基本使用

> helm 仓库：  https://hub.helm.sh/

```
使用步骤： 
1.添加helm仓库 helm repo 
2.安装helm包   helm install

e.g.: 
helm install stable/xxx --version yyy
helm install stable/xxx --values values-prodution.yaml
```



## 4. 自定义模板

```
mkdir hello_helm
cd hello_helm

// 创建自描述文件  Chart.yaml, 这个文件必须有name 和 version定义
cat <<'EOF' > ./Chart.yaml
name: hello-helm
version: 0.1
EOF

// 创建模板文件， 用于生成k8s资源清单, templates文件夹和chart.yaml在同一级目录
mkdir ./templates

cat <<'EOF' >  ./templates/deployment.yaml 
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: hello-helm
  labels:
    name: hello-helm
spec:
  replicas: 1
  template:
    metadata:
      labels:
        name: hello-helm
    spec:
      containers:
        - image: hub.atguigu.com/library/nginx:v1
          name: hello-helm
          ports:
            - containerPort: 80
              protocol: TCP
EOF


cat <<'EOF' >  ./templates/service.yaml
kind: Service
apiVersion: v1
metadata:
  name: hello-helm
spec:
  selector:
    app: hello-helm
  type: NodePort
  ports:
    - port: 80
      targetPort: 80
      protocol: TCP
EOF




// 创建values.yaml 文件， 用于更改镜像
cat <<'EOF' >  ./values.yaml
image:
  repository: hub.atguigu.com/library/nginx
  tag: "v1"
EOF


// 通过模板语法更改template文件夹下的文件中的内容
./templates/deployment.yaml
image:
  {{ .Values.image.repository }}:{{ .Values.image.tag }}


// 创建release 
helm install . [ --name hello-helm ]     //创建release, 可以指定名称，方便后续操作
```



## 5.  模板语法

```
# 模板语法
https://www.cnblogs.com/klvchen/p/13606311.html
https://blog.csdn.net/winterfeng123/article/details/107843282
https://juejin.cn/post/6844904199818313735#heading-9

https://helm.sh/docs/chart_template_guide/function_list/         //官方文档中方法的完整列表
https://helm.sh/docs/chart_template_guide/builtin_objects/       //官方文档中方法的内置对象
https://helm.sh/docs/chart_template_guide/accessing_files/       //文件相关的
https://github.com/Masterminds/sprig

Helm template由go template编写，所以我们先需要掌握gotemplate的基础语法
```



### 5.1 横杠（-）

```
1. 横杠（-）表示去掉表达式输出结果前面和后面的空格，去掉前面空格可以这么写{{- 模版表达式 }}, 去掉后面空格 {{ 模版表达式 -}}

    # 去除test模版头部的第一个空行, 用于yaml文件前置空格的语法
    {{- template "test" }}
    

    # 这种方式定义的模版，会去除test模版头部和尾部所有的空行
    {{- define "test" -}}
    模版内容
    {{- end -}}
```



### 5.2 变量&作用域&内置对象

```
默认情况最左面的点( . ), 代表全局作用域，用于引用全局对象，中间的点，很像是js中对json对象中属性的引用方式。
	#这里引用了全局作用域下的Values对象中的key属性。 最左边的点就是全局，中间的点代表是从Values对象中取key属性.
	{{ .Values.key }}
	
	
	helm中的内置对象：
	   Build-in Objects: https://helm.sh/docs/chart_template_guide/builtin_objects/

        Release：代表Release对象，属性包含：Release.Name、 Release.Namespace、Release.Revision等
        Values： 表示 values.yaml 文件数据
        Chart：  表示 Chart.yaml 数据，例：{{ .Chart.Name }}-{{ .Chart.Version}}
        Files：  用于访问 chart 中非标准文件
                提供文件访问方法：
                Files.Get      获取指定文件名称的文件内容, eg: {{.Files.Get "conf/evo.conf" | printf "%s" | indent 4 }}	
                Files.GetBytes 返回文件的二进制数组，读二进制文件时使用（例如图片）。
                Files.Glob     返回符合给定shell glob pattern的文件数组，例:{{ .Files.Glob "*.yaml" }}
                Files.Lines     按行遍历读取文件
                Files.AsSecrets 返回文件内容的Base 64编码
                Files.AsConfig  返回文件内容对应的YAML map
                
                Files.AsConfig和Files.AsSecrets就是用来把配置文件转换成ConfigMap和Secret的

        Capabilities： 用于获取 k8s 集群的一些信息
           	Capabilities.APIVersions：     集群支持的api version列表。
            Capabilities.APIVersions.Has： $version 指出当前集群是否支持当前API版本 (e.g., batch/v1)或资源 (e.g., apps/v1/Deployment)
            Capabilities.KubeVersion / Capabilities.KubeVersion.Version： Kubernetes版本号
            Capabilities.KubeVersion.Major： Kubernetes主版本号
            Capabilities.KubeVersion.Minor： Kubernetes子版本号

        Template： 表示当前被执行的模板
           - Name：表示模板名，  如：mychart/templates/mytemplate.yaml
           - BasePath：表示路径，如：mychart/templates
           
    helm全局作用域中有两个重要的全局对象：Values和Release
    
	
2.1 Values
	Values代表的就是values.yaml定义的参数，通过.Values可以引用values中的任意参数（可以多级引用）。

    例子：
    #引用某个属性
    {{ .Values.replicaCount }}

    #引用嵌套对象例子，跟引用json嵌套对象类似
    {{ .Values.image.repository }}
    
    .Values.nameOverride
	.Values.fullnameOverride
    
    
    数据来源：
        1.chart 包中的 values.yaml 文件
        2.父 chart 包的 values.yaml 文件
        3.使用 helm install 或者 helm upgrade 的 -f 或者 --values 参数传入的自定义的 yaml 文件
        4.通过 --set 参数传入的值
     *********************************************************************************** 
    	# cat global.yaml 
        course: k8s

        # cat mychart/templates/configmap.yaml 
        apiVersion: v1
        kind: ConfigMap
        metadata:
          name: {{ .Release.Name }}-configmap
        data:
          myvalue: "Hello World"
          course:  {{ .Values.course }}

        helm install --name mychart --dry-run --debug -f global.yaml ./mychart/
	***********************************************************************************
	    helm install --name mychart --dry-run --debug --set course="k8s" ./mychart/
		
	    部署成功后，使用helm get manifest xxx 命令可以看到被部署的yaml文件
	    
        # 运行部分结果:
        # Source: mychart/templates/configmap.yaml
        apiVersion: v1
        kind: ConfigMap
        metadata:
          name: mychart-configmap
        data:
          myvalue: "Hello World"
          course:  k8s
     ***********************************************************************************
        # 编辑 mychart/values.yaml，在最后加入
        course:
          k8s: klvchen
          python: lily

        # cat mychart/templates/configmap.yaml 
        apiVersion: v1
        kind: ConfigMap
        metadata:
          name: {{ .Release.Name }}-configmap
        data:
          myvalue: "Hello World"
          k8s:  {{ quote .Values.course.k8s }}      # quote叫双引号
          python:  {{ .Values.course.python }}


        helm install --name mychart --dry-run --debug ./mychart/
        
        部署成功后，使用helm get manifest xxx 命令可以看到被部署的yaml文件
        
        # 运行结果：
        # Source: mychart/templates/configmap.yaml
        apiVersion: v1
        kind: ConfigMap
        metadata:
          name: mychart-configmap
        data:
          myvalue: "Hello World"
          k8s:     "klvchen"
          python:  lily
    
	
2.2 Release
	Release代表一次应用发布时带有的属性（介绍信息），注意这里和Values中的模板区分开,模板替换还是用Values，下面是Release对象包含的属性字段：
	Release.Name        - release的名字，一般通过Chart.yaml定义，或者通过helm命令在安装应用的时候指定。
    Release.Time        - release安装时间
    Release.Namespace   - k8s命名空间
    Release.Revision    - release版本号，是一个递增值，每次更新都会加一
    Release.IsUpgrade   - true代表，当前release是一次更新.
    Release.IsInstall   - true代表，当前release是一次安装
    Release.Service	    - 总是"Helm"
	
	例子:
	// deployment.yaml
    {{ .Release.Name }}
    
    // Chart.yaml
    apiVersion: v2
    name: mychart
	
2.3 自定义模板变量
	定义：变量名以$开始命名，赋值运算符是 := (冒号等号)，这是go语言中的赋值方式。
	{{- $relname := .Release.Name -}}
	
	引用:
	{{ $relname }}   // 不需要使用符号 . 来引用
```



### 5.3 函数&管道运算符

```

3.1 调用函数
    语法和shell中类似：{{ functionName arg1 arg2… }}

    例子: 调用quote函数，将结果用“”引号包括起来。
    {{ quote .Values.favorite.food }}
    
3.2 管道（pipelines）运算符 |
	#将.Values.favorite.food传递给quote函数处理，然后在输出结果。
    {{ .Values.favorite.food | quote  }}

    #先将.Values.favorite.food的值传递给upper函数将字符转换成大写，然后专递给quote加上引号包括起来。
    {{ .Values.favorite.food | upper | quote }}

    #如果.Values.favorite.food为空，则使用default定义的默认值
    {{ .Values.favorite.food | default "默认值" }}

    #将.Values.favorite.food输出5次
    {{ .Values.favorite.food | repeat 5 }}

    #对输出结果缩进2个空格
    {{ .Values.favorite.food | nindent 2 }}
    
    
3.3 关系运算函数
常用的关系运算符>、 >=、 <、!=、与或非, 在helm模版中都以 函数 的形式实现。

关系运算函数定义：

eq 相当于 =
ne 相当于 !=
lt 相当于 <=
gt 相当于 >=
and 相当于 &&
or 相当于 ||
not 相当于 !
contains 

例子:
// 相当于 if (.Values.fooString && (.Values.fooString == "foo"))
{{ if and .Values.fooString (eq .Values.fooString "foo") }}
    {{ ... }}
{{ end }}
```



### 5.4 流程控制

```

4.1 if/else
    语法:
    {{ if 条件表达式 }}
    #Do something
    {{ else if 条件表达式 }}
    #Do something else
    {{ else }}
    #Default case
    {{ end }}


    例子:
    apiVersion: v1
    kind: ConfigMap
    metadata:
      name: {{ .Release.Name }}-configmap
    data:
      myvalue: "Hello World"
      drink: {{ .Values.favorite.drink | default "tea" | quote }}
      food: {{ .Values.favorite.food | upper | quote }}
      {{if eq .Values.favorite.drink "coffee"}}
        mug: true
      {{end}}
      
4.2 with
	with主要就是用来修改 . 作用域的，默认 . 代表全局作用域，with语句可以修改.的含义.

    语法:
    {{ with 引用的对象 }}
    这里可以使用 . (点)， 直接引用with指定的对象
    {{ end }}

    例子: .Values.favorite是一个object类型
    {{- with .Values.favorite }}
    drink: {{ .drink | default "tea" | quote }}   // 相当于.Values.favorite.drink
    food: {{ .food | upper | quote }}
    {{- end }}

 
    注意:   这里面 . 相当于已经被重定义了。所以不能在with作用域内使用 . 引用全局对象。
            如果非要在with里面引用全局对象，可以先在with外面将全局对象复制给一个变量，
            然后在with内部使用这个变量引用全局对象。如下：

            {{- $release:= .Release.Name -}}              #先将值保存起来

            {{- with .Values.favorite }}
            drink: {{ .drink | default "tea" | quote }}   #相当于.Values.favorite.drink
            food: {{ .food | upper | quote }}

            release: {{ $release }}                       #间接引用全局对象的值
            {{- end }}


4.3 range
    range主要用于循环遍历数组类型。

    语法1:
    #遍历map类型，用于遍历键值对象
    #变量key代表对象的属性名，val代表属性值

    {{- range key,val := 键值对象 }}
    {{ $key }}: {{ $val | quote }}
    {{- end}}

    语法2：
    # 遍历数组
    {{- range 数组 }}
    {{ . | title | quote }} # . (点)引用数组元素值。
    {{- end }}
	
	
    例子:
    #values.yaml

    ##map类型
    favorite:
      drink: coffee
      food: pizza

    map类型遍历例子:
    {{- range $key, $val := .Values.favorite }}
    {{ $key }}: {{ $val | quote }}
    {{- end}} 

    ##数组类型
    pizzaToppings:
      - mushrooms
      - cheese
      - peppers
      - onions

    数组类型遍历例子:
    {{- range .Values.pizzaToppings}}
    {{ . | quote }}
    {{- end}}

```



### 5.5 子模板

```

    在chart中以 "下划线" 开头的文件，称为”子模版”, 保存一些可复用的模板，  _helpers.tpl
    
    
    定义子模块：
    	在 _helper.tpl 中定义子模块，格式：{{- define "模版名字" -}} 模版内容 {{- end -}}
        若 .Values.nameOverride 为空，则默认值为 .Chart.Name
        {{- define "nginx.name" -}}
        {{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
        {{- end -}}

    引用模板：
    	格式：{{ include "模版名字" 作用域}}
        apiVersion: apps/v1
        kind: Deployment
        metadata:
          name: {{ include "nginx.fullname" . }}
      
    
    include 是一个函数，所以他的输出结果是可以传给其他函数的
    # 例子1：
    env:
      {{- include "xiaomage" . }}

    # 结果：
    env:
        - name: name
          value: xiaomage
        - name: age
          value: secret
        - name: favourite
          value: "Cloud Native DevSecOps"
        - name: wechat
          value: majinghe11

    # 例子2：可以在模版每一行的头部增加8个空格，用于yaml文件的对齐， 不要在定义时加空格
    env:
      {{- include "xiaomage" . | indent 8}}

    # 结果：
              env:
                - name: name
                  value: xiaomage
                - name: age
                  value: secret
                - name: favourite
                  value: "Cloud Native DevSecOps"
                - name: wechat
                  value: majinghe11
                  

```



### 5.6  其他

```
6. 其他
6.1 toYaml：将数据转为yaml格式
# deployment.yaml
spec:
  strategy:
{{ toYaml .Values.strategy | indent 4 }}


#values.yaml
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxUnavailable: 0

------------------------------------------------------------------
渲染效果：
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 0
  
  

6.2 include 和 template 区别
https://blog.csdn.net/qq_26884501/article/details/108150545

app: {{ template "nginx-evo.name" . }}
chart: {{ template "nginx-evo.chart" . }}

{{ include (print .Template.BasePath "/configmap.yaml") . | sha256sum }}

相同与不同点:
1、本质上 template和include都是操作而不是函数，数据只是进行了内联插入这个操作。
2、无法将template调用的输出传递给其他函数。
3、include调用的输出可以通过管道符传递给其他函数。

结论：
	建议用 include
```



## 6. 常用命令

```
helm --help

helm repo update
helm repo list
helm repo remove stable  /  xxx 
helm repo add stable https://kubernetes.oss-cn-hangzhou.aliyuncs.com/charts

helm search stable/kubernetes-dashboard
helm fetch  stable/kubernetes-dashboard      //为啥我的fetch没有作用 ？？？ 网络问题

helm list/ls  --deleted                  // 列出当前的helm chart, 包括删除的, 可以看到版本信息等
helm history  release_name               // 查看release的历史信息
helm status   release_name               // 查看release的状态
heml delete [ --purge ]  release_name    // (完整)删除


// 更新release, 即将过时，推荐使用 repo update
vim xx.yaml
helm update  release_name .
helm upgrade release_name .  --set image.tag="v3"
helm upgrade release_name . -f values.yaml
或者
helm (repo) upgrade release_name .  --set image.tag="v3"    //更新release
helm (repo) upgrade release_name . -f values.yaml

// 回滚
# helm rollback release_name release_version     // 非完整删除下可以回滚, 会生成新的revision
helm rollback db-mysql 1

// debug
helm install .  --dry-run --debug --set image.tag=latest --name test //尝试运行清单文件，而不执行部署, 主要看报不报错

// 检查语法
helm lint mychart


*****************************************************************************************
// 其他 
# 依赖管理
方式1.直接把依赖的 package 放在 charts/ 目录中
方式2.使用 requirements.yaml 并用 helm dep up foochart 来自动下载依赖的 packages

dependencies:
  - name: apache
    version: 1.2.3
    repository: http://example.com/charts
  - name: mysql
    version: 3.2.1
    repository: http://another.example.com/charts


# 插件管理
$(helm home)/plugins/
  |- keybase/
      |
      |- plugin.yaml
      |- keybase.sh
      
vim plugin.yaml

name: "keybase"
version: "0.1.0"
usage: "Integreate Keybase.io tools with Helm"
description: |-
  This plugin provides Keybase services to Helm.
ignoreFlags: false
useTunnel: false
command: "$HELM_PLUGIN_DIR/keybase.sh"

helm keybase   // 使用插件


# 搭建本地helm仓库
## 生成 repo 索引（用于搭建 helm repository）
helm repo index
## 打包 chart 到 tgz
helm package hello-chart
## 查询 package 详细信息
helm inspect stable/mysql

helm repo update 
helm repo list
helm repo remove stable  /  xxx 
helm repo add stable https://kubernetes.oss-cn-hangzhou.aliyuncs.com/charts

helm search stable/kubernetes-dashboard
helm fetch  stable/kubernetes-dashboard      //为啥我的fetch没有作用 ？？？ 网络问题


# 三方资源
## Prometheus Operator
https://github.com/coreos/prometheus-operator/tree/master/helm
 
## Bitnami Library for Kubernetes
https://github.com/bitnami/charts

## Openstack-Helm
https://github.com/att-comdev/openstack-helm
https://github.com/sapcc/openstack-helm

## Tick-Charts
https://github.com/jackzampolin/tick-charts
```