# Kubernetes

## 1. 基本认识

```
# 发展史
apache mesos
docker docker-swam
google k8s ( 用go基于borg开发出来 )

# 作用：资源管理器，容器集群化

# 特点：
轻量级，消耗资源小
开源
弹性伸缩
负载均衡(ipvs, 国人开发，负载能力第一)


# 实验机器规划：
k8s_master 2,4,100   centos7
k8s_node1  4,4,100   centos7
k8s_node2  4,4,100   centos7
k8s_harbor 2,2,100	 centos7
koolshare1 1,1,20    winpe

k8s版本：1.15.a
```



## 2. 知识图谱

> *** 视频中的思维导图，参考截图 ***

```
pod：最小的管理单位，可以管理多个容器

    资源清单(资源清单的书写，pod的编写)
    pod生命周期 ***
    控制器概念
    控制器类型  ***  k8s灵魂

    pod服务发现
    网络通讯模式(网络通讯，组件通讯)

服务发现：svc原理及其构建方式

存储：  掌握多种存储服务的特点，会根据不同场景选择对应的存储(pv, volume, secret, configmap)

调度器：掌握调度器原理，根据要求将pod放到相应的调度器

安全： 认证，鉴权，访问控制原理及其流程

helm: 类似yum， yaml包管理工具， helm原理及其模板自定义，部署常用的功能 ***

运维： kubeadm源码修改(证书的更新，默认只有一年), 高可搭建

还有后续2.0教程
```



## 3. 架构原理

![](imgs\002-k8s架构图.png)



```
master:
scheduler: 负责接收任务，选择合适的节点进行任务分配(将任务交给apisesrver, apiserver写入到etcd)
control manager: 维持副本期望数目(创建pod, 删除pod)
apiserver:       所有服务访问的统一入口(kubectl, webui, etcd ... 都需要跟它交互)
etcd:            分布式的键值对数据库，k8s持久化(当前使用的是v3, v2已经在v1.11中弃用，v3 db, v2 memory)

node:
kubelet:    直接跟容器引擎(CRI)交互，管理容器(pod)生命周期
kube-proxy: 负载均衡，负责写入规则到firewall, 最新版ipvs实现服务访问映射node(pod(container))

其他插件：
coredns:   为 svc 创建一个  域名-ip  对应的解析关系
dashboard: 提供一个b/s架构的访问体系

ingress controller: 实现7层代理
federation:         提供一个跨集群中心多k8s同一管理平台kube config/rancher/kuboard/kubesphere

prometheus: 提供k8s监控能力
elk:        日志管理
```



## 4. pod

### 4.1 pod分类

```
pod分为 自主式pod 和 控制器管理的pod
```



### 4.2 自主式pod

> 疑问：pause网络，存储？？？  
>
> pause 容器有时候也称为 `infra` 容器，最大的作用是维护 Pod 网络协议栈
>
> https://blog.csdn.net/alex_yangchuansheng/article/details/104234098
>
> Kubernetes 的 Pod 抽象基于 Linux 的 `namespace` 和 `cgroups`

```
特点：一旦死亡拉不起来，副本无法维持，无法管理.

其他：
	传统容器通过(namespace)名称空间进行隔离，每个都有自己的ip地址，都可以有自己的挂载卷；
	pod内的(pause，也叫infra)容器共享网络，localhost即可相互访问，port不能冲突。
```



### 4.3 控制器pod

```
当前主要是概念，后面资源清单后会有实操

# rc(replicationCOntrol):  用来确保容器应用的副本数始终保持在用户的副本数，即如果有容器异常退出，会自动创建新的pod来替代；而如果异常多出来的容器也会自动回收，新版本K8s，建议用rs替代rc
	
# rs(replicaset): 支持集合式的selector，打一堆标签，通过标签操作，rs支持，rc不支持
	
# deployment: 虽然rs可以独立使用，建议通过deployment来管理replicaset，避免一些兼容性问题，比如支持滚动更新(rolling-update). 为啥rs和deployment一起用：因为deployment并不负责pod创建，是通过rs创建
	
# HPA: horizontal pod autoscaling 平滑扩展， 仅适应于deployment 和 replicaset, 在v1版本中仅支持根据pod的cpu利用率扩容，在vl-alpha版本中，支持根据内存和自定义metric扩容



# statefulset:
        为了解决有状态服务的问题(deployment和rs 是无状态设计)

        稳定的持久化存储，基于pvc
        稳定的网络状态, podname 和  hostname不变，基于headless service(没有cluster ip的service)
        有序部署，有序扩展： pod是有顺序的，需要根据定义的顺序，0 到 n-1 有序创建（创建下一个之前，前一个pod是running 和 ready 的状态)，基于init containers
        有序收缩，有序删除： n-1 到 0
        

# daemonset:
        确保所有或部分node上运行一个pod的副本(打了污点的除外)，当有node加入到集群，也会为其新增pod, 当node从集群中移除，pod也会被回收，删除daemonset，将会删除他们创建的所有pod

        场景：
            在每个Node上运行集群存储 daemon, 例如： 在每个node上运行glusterd, ceph
            在每个Node上运行日志收集 daemon, 例如： fluentd,logstash
            在每个Node上运行监控系统 daemon, 例如： prometheus node_exporter
            
        问题：
        	daemonset如何运行多个pod, 将相同的地方提取出来，放到一个pod, 或者设置3个不同的daemonset

# Job和cronJob:
        job：	负责批处理任务，即仅可执行一次的任务, 保证任务的一个或者多个Pod成功或结束(pod不是正常退出，会重新执行，可以指定运行次数)
        cronjob：负责周期性反复执行任务
        
        场景：	
        	备份数据库
```



### 4.4 服务发现

> 注意总结:  服务发现和网络通讯方式 与 service 之间的关系

```
# 原理：
	客户端想访问一组pod, service通过标签选择(收集) (rc, rs, deployment创建的)pod, 选择后service会有自己的 ip + port, 客户端就能通过 ip + port 访问到service, 间接访问到pod， service访问pod，用的是rr
	
	如果service 下的pod被替换掉，也不会有问题
```

![](imgs\017-service简单应用.png)





### 4.5 网络通讯

> 还需要看后面有没有实操  todo

```
# 基本原理：
	k8s中假定所有的pod都在一个可以直接连通的扁平的网络空间(表面是直接通过ip直接到达)中，这在gce(google compute engine) 里面是现成的网络模型;  私有云里，需要自己实现，将不同容器中的docker网络连通，再运行k8s


# 场景1：同一个 pod 里面的容器之间	***
  io：共享同一个网络命名空间，共享同一个linux网络协议栈(pause),  通过localhost相互访问
	
# 场景2：pod 和 pod 之间	***
  overlay network
  见下面flannel解决方案(还有calico)

# 场景3：pod 和 service 之间	***
  目前基于性能考虑，各节点的 iptables 维护和转发(最新lvs, 上限更高)  kube-proxy

# 场景4： pod访问外网
  snat， pod向外网发送请求，查找路由表，转发数据包到宿主机的网卡，宿主网卡完成路由选择后，iptables执行masquerade, 把源ip更改为宿主机网卡的ip, 然后向外网服务器发送请求

# 场景5： 外网访问pod
  nodeport
```



flannel 解决方案：

![](imgs\004-flannel架构.png)

```
#1. flannel: coreos针对 k8s 设计的网络规划服务

#2. 作用：不同节点主机创建的docker容器具有全集群唯一的虚拟ip地址，而且还能在ip地址之间建立一个覆盖网络(overlay network)， 通过覆盖网络将数据包原封不动的传递到目标容器内
	
#3. 步骤：
		1. 主机上安装flanneld, 监听端口(用于后期转发数据包的服务端口)
		2. 开启网桥flannel0, 收集docker0 数据包
		3. docker0 分配ip到对应的pod上
		
		同一台主机上不同pod之间的访问，走的docker0的网桥
		
		不同台主机pod之间的访问，目标pod将地址，给到docker0, flannel0, flanneld, flanneld从etcd中找到目标主机的信息，进行解析(mac, outerIp, udp,  InnerIP, payload数据包实体等)
		outerip:
			source: 192.168.19.11
			des:    192.168.19.12 
			
		innerIP:
			source: 10.1.15.2
			des:	10.1.20.3

 目标机器flanneld, flannel0, docker0, 目标pod ,最终实现跨主机，还能直接通过ip访问到
	

# flannel中etcd的作用：
	 1.负责存储flannel可分配的ip地址段
	 2.负责监控每个pod的实际地址，并在内存中建立维护pod节点路由表
```



### 4.6 集群安装

```
# 安装方式：
	1. 源码, 挂掉无法启动, 暂不使用
	2. kubeadm
	
# 安装要求：linux 内核 4.4,  centos7

# 机器规划：
k8s_master 2,4,100   centos7   192.168.66.10
k8s_node1  4,4,100   centos7   192.168.66.20
k8s_node2  4,4,100   centos7   192.168.66.21
k8s_harbor 2,2,100	 centos7   192.168.66.40
koolshare1 1,1,20    winpe     192.168.1.1 ---> 192.168.66.1 

							   192.168.1.240
							   192.168.66.240

网络连接， 仅主机

# 安装版本：1.15.a
```



#### 4.6.1 软路由安装

```
# 安装参数： window10,  bios, 2, 4, ide,  20g

# 步骤：
	1. 编辑虚拟机，选择laomaotao
	2. 开启虚拟机，进入win10pe
	3. pe开机状态下，虚拟机中更换iso   2019_xxx.iso
	4. 进入此电脑，双击光驱，右键管理员 运行img写盘工具
	5. 浏览，选择 openwrt-koolshare压缩文件，点击开始
	6. 完成后，虚拟机中cd   关闭   已连接，启动时连接
	7. 关机，调系统资源， 1c, 1g, 20g,  添加网卡，选择nat模式(原有的网卡是仅主机)
	8. 开机
	
# 宿主机(windows)配置
	见下面截图
	
# 访问
	192.168.1.1
	koolshare
	
	网络/接口， 删除wan6, 留下lan, wan(为啥删不掉)
	编辑lan, 选择物理设置，去掉 桥接接口，让其直接使用物理网卡; 选择基本设置，ipv4地址改为192.168.66.1
	编辑wan, 查看确认是否是eth1(dhcp连接即可，当然也可以拨号连接)
	
	访问：192.168.66.1   网络/诊断  输入 www.baidu.com   点击ping(不成功的原因在于需要有线连接)
	
	访问国外，选择酷软，离线安装，选择kollss.tar.gz, 上传并安装，点进去，配置相关代理信息保存，开启
```

![](imgs\18-koolshare网络.png)



vmware  仅主机 注意去掉 勾选dhcp

![](imgs\19-软路由配置仅仅主机模式1.png)



windows vmnet1 配置

![](imgs\19-软路由配置仅仅主机模式.png)

重点:  绕过koolshare连接外网，同时和主机能交互

```
windows 根据网络连接方式，wlan2, 以太网2， 共享网络vnet1, 默认192.168.137.1 

windows vnet1 设置一个ip地址，例如： 192.168.66.240, 可以删除默认的

vmware 虚拟网络设置，仅主机，去掉dhcp, 将子网ip 更改为 192.168.66.0

vmware 虚拟机设置， 网络适配器，选择仅主机模式

vim /etc/sysconfig/network-scripts/ifcfg-ens33
bootprotocol=none

IP=192.168.66.40
HOST=xxx
HOSTNAME=xxx
BROADCAST=192.168.66.240   //指向koolshare地址
GATEWAY=192.168.66.240

vim /etc/hosts 

vim /etc/resolv.conf 

hostnamectl set-hostname 


ping 192.168.66.240
ping www.baidu.com 

# 报错：
	1. 修改后ip addr 没有地址
	chkconfig --level 123456 NetworkManager off
	chkconfig --level 345    network on
	reboot
```



#### 4.6.2 centos7安装

```
vim /etc/sysconfig/network-scripts/ifcfg-ens33

IP=192.168.66.40
HOST=hub.atguigu.com
HOSTNAME=hub.atguigu.com
BROADCAST=192.168.66.240   //指向koolshare地址， 不指向koolshare可以直接指向vnet1
GATEWAY=192.168.66.240

vim /etc/resolv.conf
nameserver 
```



#### 4.6.3 系统初始化

```
每台机器上运行 init_k8s.sh， 注意更改ip


sysctl -p /etc/sysctl.d/kubernetes.conf


# 编辑master
vim /etc/hosts
192.168.66.10 k8s_master01
192.168.66.20 k8s_node01
192.168.66.21 k8s_node02


# 升级内核为4.4
rpm -Uvh https://mirror.tuna.tsinghua.edu.cn/elrepo/kernel/el7/x86_64/RPMS/elrepo-release-7.0-5.el7.elrepo.noarch.rpm

yum --enablerepo=elrepo-kernel install -y kernel-lt

grub2-set-default 'CentOS Linux (4.4.241-1.el7.elrepo.x86_64) 7 (Core)'

reboot 

uname -r 
```



#### 4.6.4 开启ipvs

```
# kube-proxy开启ipvs的前置条件
# 执行  prepare_kube_proxy.sh 

mobprobe br_netfilter
lsmod |grep br_netfilter

cat > /etc/sysconfig/modules/ipvs.modules <<EOF
#!/bin/bash

modprobe -- ip_vs
modprobe -- ip_vs_rr
modprobe -- ip_vs_wrr
modprobe -- ip_vs_sh
modprobe -- nf_conntrack_ipv4
EOF

chmod 755 /etc/sysconfig/modules/ipvs.modules && bash /etc/sysconfig/modules/ipvs.modules && lsmod | grep -e ip_vs -e nf_conntrack_ipv4


报错：
	1. ipva rr no destination available
	ipvsadm -Ln
```



#### 4.6.5 安装docker

```

"registry-mirrors": ["http://hub-mirror.c.163.com"]

cat > /etc/docker/daemon.json <<EOF
{
	"exec-opts": ["native.cgroupdriver=systemd"],
	"log-driver": "json-file",
	"log-opts": {
		"max-size": "100m"
	},
	"insecure-registries": ["https://hub.atguigu.com"]
}
EOF


mkdir -p /etc/systemd/system/docker.service.d

systemctl daemon-reload && systemctl restart docker && systemctl enable docker 


报错：
	多半是配置文件的问题
```



#### 4.6.6 安装kubeadm

install_kubeadm.sh

```
#!/bin/bash

cat <<EOF > /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=kubernetes
baseurl=http://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=0
repo_gpgcheck=0
gpgkey=http://mirrors.aliyun.com/kubernetes/yum/doc/yum-key.gpg
http://mirrors.aliyun.com/kubernetes/yum/doc/rpm-package-key.gpg
EOF

yum install -y kubeadm-1.15.1 kubectl-1.15.1 kubelet-1.15.1

systemctl enable kubelet.service
```



tar -xvf  kubeadm-basic.images.tar.gz



load_kubeadm.sh

```
#!/bin/bash 

ls /root/kubeadm-basic.images >> /tmp/image_list.txt 
cd /root/kubeadm-basic.images
for i in $( cat /tmp/image_list.txt )
do	
	docker load -i $i
done

rm -rf /tmp/image_list.txt 



chmod 755 load_kubeadm.sh 
sh ./load_kubeadm.sh
```



#### 4.6.7 初始化主节点

```
kubeadm --help 

1. kubeadm config print init-defaults > kubeadm-config.yaml

2. vim kubeadm-config.yaml

advertiseAddress: 192.168.66.10
kubernetesVersion: v1.15.1

networking:
	podSubnet: 10.244.0.0/16       // 新增， flannel 默认网段
	serviceSubnet: 10.96.0.0/12    // 不修改
	

---
apiVersion: kubeproxy.config.k8s.io/v1alpha1
kind: KubeProxyConfiguration
featureGates:
  SupportIPVSProxyMode: true
mode: ipvs 


3. kubeadm init --config=kubeadm-config.yaml --experimental-upload-certs | tee kubeadm-init.log 

# 记得拷贝最终的执行结果，比如： 
kubeadm join 192.168.19.130:6443 --token abcdef.0123456789abcdef \
    --discovery-token-ca-cert-hash sha256:0b7a6dea89f0d5bf3c7b7897ae31ec019c311bbcb5c72cbc6368d372e1605503


*****************************************************************
*** init 信息如果错误, 导致再次启动，端口占用 ***
kubeadm reset 
rm -f $HOME/.kube/config

从节点上，各种文件，端口占用解除
lsof -i :10250|grep -v "PID"|awk '{print "kill -9",$2}'|sh
*****************************************************************

# cat kubeadm-init.log
make -vp ~/.kube     //保存连接配置  config, 缓存等
sudo cp -i /etc/kubernetes/admin.conf ~/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config


# docker images 
# kubectl get nodes  
# notready , 因为需要偏平化的网络，所以下面部署网络


***************************************************************************
# 在其他子节点运行，加入子节点
kubeadm join 192.168.66.10:6443 --token xxx  --discovery-token-ca-cert-hash yyy

# 主节点， 其他节点是无法看到的，当前状态还是notready, 需要部署网络
kubectl get node -n kube-system -o wide -w
kubectl get nodes 
```



#### 4.6.8 部署网络

>  只在主节点上部署么？？？  是的

```
# kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml

kubectl apply -f kube-flannel.yml

kubectl get pod -n kube-system -w     //看服务的状态

kubectl get nodes

ifconfig

```



#### 4.6.9 部署harbor

> 配置不能太低，会访问的很慢，甚至失败

```
# step1:
vim /etc/docker/daemon.json
{

	"insecure-registries": ["https://hub.atguigu.com"]
}

systemctl restart docker 


# step2:
上传docker-compose, harbor-offline-installer-v1.2.0.tgz   (docker-compose没有用到？？？ 暂时没有用到, install.sh中有使用)

mv docker-compose /usr/local/bin/
chmod a+x /usr/local/bin/docker-compose

tar -zxvf harbor-offline-installer-v1.2.0.tgz 

cd harbor
// vim harbor.cfg 
hostname = hub.atguigu.com 
ui_url_protocol = https


mkdir -p /data/cert

cd /data/cert

# step3:
	创建证书
	
	openssl genrsa -des3 -out server.key 2048          //设置密码  123456
	
	openssl req -new -key server.key -out server.csr   //输入上面的密码，common Name: hub.atguigu.com, 最后一个提示改密码，直接回车
	
	cp server.key server.key.org 
	
	openssl rsa -in server.key.org -out server.key    //去掉密码，不然会失败(需要输入密码)
	
	openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt
	
	chmod 755 *    // 目录在cert 
	
	
	cd - 
	
	./install.sh 
	
	
# step4:
	添加harbor 到每台主机的hosts
	
	echo "192.168.66.40 hub.atguigu.com" >> /etc/hosts
	
	
# step5:
	windows hosts中添加
	
	192.168.66.40   hub.atguigu.com
	
	
# step6:
	浏览器访问
		https://hub.atguigu.com
        admin
        Harbor12345     // cat  harbor.cfg  harbor_admin_password=Harbor12345
	
	docker访问及推送镜像：
		docker login https://hub.atguigu.com
		
		admin
		Harbor12345
		
		docker pull nginx
		
		docker tag nginx:latest   hub.atguigu.com/library/nginx:v1
		
		docker push hub.atguigu.com/library/nginx:v1
		
	k8s集群使用harbor仓库:
		# 临时使用
		kubectl run --help 
		kubectl run nginx-deployment --image=hub.atguigu.com/library/nginx:v1 --port=80 --replicas=1
		
		kubectl get deployment
		
		kubectl get rs
		
		kubectl get pod -o wide
		
		curl ip  //发现能访问
		
# step7:  先了解即可
	# 基本使用
	
	kubectl delete pod nginx-de
	
	kubectl scale --replicas=3 deployment/nginx-deploy
	
	kubectl get pod
	
	
	# 访问pod内部的网络
	kubectl expose deployment xxx --port=30000 --target-port=80
	kubectl get svc 
	
	curl ip:port
	
	# 外部网络访问内部pod, 所有节点都暴露(是否有安全问题)
	kubectl edit svc nginx
	type: NodePort

```






### 4.7 资源清单

#### 4.7.1 资源分类

```
资源定义：所有的内容都抽象为资源，资源实例化后，叫做对象

资源分类：
    名称空间：仅在此名称空间下生效
            kubectl  get pod -n kube-system      // 不加 -n 指定，默认为default

            工作负载型(workload): pod, rs, deployment, statefulset, daemonset, job, cronjob
            服务发现与负载均衡：   service, ingress
            配置与存储：  volume, csi(容器存储接口，可以扩展各种第三方的存储卷)
            特殊的存储卷：configmap, secret, downwardAPI(把外部环境中的信息输出给容器)

    集群级别：在全集群中所有空间都可见
            Namespace, Node, Role, ClusterRole, RoleBinding, ClusterRoleBinding

    元数据： 
            HPA, PodTemplate, limitRange
```



#### 4.7.2 基本语法

```
基本语法：
	1. 不允许使用tab, 只能使用空格
	2. 缩进的空格数量不重要，只要相同层级的元素左对齐即可
	3. # 用来注释
	
数据结构：
	1. 对象: 键值对的集合，也叫映射(mapping)，类似于 哈希(hash)，字典(dict)
        example:
            name: "dh"
            hash: { name: "steve", age: 18}
            
	2. 数组：也叫序列， 列表(list)
        example:
            animal:
            - Cat
            - Dog
		    等价于
    		animal: [Cat, Dog]

	3. 纯量
		字符串: 
			默认不要使用引号，
			包含空格或者特殊字符需要放在引号之中，
			双引号不会转义，
			单引号之中还有单引号，连续使用两个单引号，
			多行字符串可以使用，|保留换行，>折叠换行, +表示保留文字块末尾的换行，-表示删除字符串末尾的换行
				e.g.:
				  this: |
                    Foo
                    Bar
                    
                    that: >
                    Foo
                    Bar
                    
                    s2: |+
                      Foo

                    s3: |-
                      Foo
                      
		布尔值
		整数
		浮点数
		null(~)
		时间(iso8601)
		日期(date)
		
		允许使用两个感叹号，强制转换数据类型
		e: !!str 123
		f: !!str true
```



#### 4.7.3 常用字段

> tips：     **kubectl  explain  pod / srv     kubectl explain pod.apiVersion**
>
> 参考文档： 上面的命令行中可以看到官方的文档  https://github.com/kubernetes/community
>
> vscode plugin： kubernetes support



```
apiVersion: 					string, kubectl api-versions
kind:							string, 资源类型和角色， 比如：Pod(注意是大写)
metadata:						Object
metadata.name:					string, 比如pod的名字
metadata.namespace:				string, 名称空间
metadata.labels:				<map[string]string>, 下面的名字可以自定义


Spec:							Object
spec.containers[]				list, spec对应的容器列表
spec.containers[].name			string,定义容器的名字
spec.containers[].image			string,定义镜像的名字
spec.containers[].imagePullPolicy string,镜像拉取策略Always,Never,IfNotPresent, 默认Always
spec.containers[].commands[]    list, 指定容器启动命令，不指定使用镜像打包时的命令
spec.containers[].args[]	    list, 指定容器启动参数
spec.containers[].workingDir    string, 指定容器的工作目录

spec.containers[].ports[]     	list
spec.containers[].ports[].name  string
spec.containers[].ports[].containerPort  string
spec.containers[].ports[].hostPort  string
spec.containers[].ports[].protocol  string, tcp, udp

spec.containers[].env[]			list, 环境变量列表
spec.containers[].env[].name    string
spec.containers[].env[].value   string

spec.containers[].resources	    		Object, 指定资源限制和资源请求的值
spec.containers[].resources.limits	    Object， 设定容器运行时的资源的运行上限
spec.containers[].resources.limits.cpu	string , cpu核数
spec.containers[].resources.limits.memory	string , 默认gb, mb

spec.containers[].resources.requests    Object, 指定容器启动和调度时的资源设置
spec.containers[].resources.requests.cpu
spec.containers[].resources.requests.memory 

spec.restartPolicy                 string, 定义pod的重启策略，Always(默认), OnFailure, Never
spec.nodeSelector				   Object, 定义Node的标签过滤，key: value
spec.imagePullSecrects			   Object, 定义pull镜像时使用secret名称，name: secretKey
spec.hostNetwork			       bool,   是否使用桥接网络，默认false, 设置为true表示使用宿主机									网络，不适用docker0, 同时注意无法在同一台宿主机上启动第二个副本

```

![](imgs\20-pod常用属性1.png)



![](imgs\20-pod常用属性2.png)



![](imgs\20-pod常用属性3.png)



![](imgs\20-pod常用属性4.png)



![](imgs\20-pod常用属性5.png)



#### 4.7.4 简单使用

```
vim pod.yaml

apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
  namespace: default
  labels:
  	app: myapp
  	version: v1
spec: 
  containers:
  - name: app
  	image: hub.atguigu.com/library/nginx:v1
  
  - name: test
  	image: hub.atguigu.com/library/nginx:v2
  	command:
  	- "/bin/sh"
  	- "-c"
  	- "sleep 3600"
  



kubectl create -f xxx.yaml 
kubectl get pod [ -o wide -w ] 
kubectl describe pod myapp-pod 
kubectl logs myapp-pod -c test    //指定pod名， 指定容器名

curl ip

kubectl delete pod myapp-pod
```





```
kubernetes yaml 有的前面加中划线，有的不加, 为什么不是都不加或者都加https://www.cnblogs.com/lgeng/p/11053063.html

spec:
  containers:
    - name: front-end
      image: nginx
      ports:
        - containerPort: 80
    - name: flaskapp-demo
      image: jcdemo/flaskapp
      ports: 
	    - containerPort: 8080
	
等价于：
"spec": {
        "containers": 
			[{
				"name": "front-end",
				"image": "nginx",
				"ports": [{
					"containerPort": "80"
				}]
			}, 
			{
				"name": "flaskapp-demo",
				"image": "jcdemo/flaskapp",
				"ports": [{
					"containerPort": "5000"
				}]
			}]
		}
```



### 4.8 pod生命周期(***)



![](imgs\007-pod生命周期.png)



```
(kubelet)
cri容器环境初始化
init c: 初始化完成后，就死亡了，顺序的不能并行
main c: start,stop启动和退出操作
readiness: 就绪检测 判断容器能不能被使用(可用改为running,能不能被外网访问)
liveness:  生存检测 解决僵尸进程, 伴随整个main c
```



#### 4.8.1 init c

```
pod能够运行多个容器，应用运行在容器里面，但是它也可能有一个或多个先于应用容器启动的init容器

init容器和普通容器的区别： *****
	1. init容器总是运行到成功完成为止(如果pod的init容器失败，会不断重启，直到成功，如果restartPolicy为Never, 它会不启动)
	2. 每个init容器总是在下一个init容器完成之前完成
	3. init C能访问secret的权限, 而应用容器则不能, 可用来做权限控制  ***
	4. init C必须在应用容器启动之前完成，所以，init容器提供了一种简单的阻塞或延迟应用容器启动的方法，直到条件满足，再启动应用容器
	
注意事项：
	1. init容器会在网络和数据卷初始化(pause)之后完成
	2. pod重启，所有init容器必须重新运行
	3. 对init容器的spec字段被限制在容器image字段，修改其他字段都不会生效，更改init容器的image字段，等价于重启该pod  ***
	4. init容器具有应用容器的所有字段，除了readinessProbe, 因为init容器无法定义完成和就绪之外的其他状态
	5. 在pod中每个app和init容器的名称必须唯一，与任何其他容器共享一个名称，否则会在验证时报错

example: 
	# 先在vscode中写，拷贝过来直接运行
	# 使用了 nslookup 来检查相应服务是否运行
	
	# vim  init_pod.yaml
    apiVersion: v1
    kind: Pod
    metadata:
      name: myapp-pod
      labels:
        name: myapp
    spec:
      containers:
        - name: myapp-container
          image: busybox
          command: ["sh","-c", "echo the app is runing && sleep 3600"]

      initContainers:
        - name:  init-myservice
          image: busybox
          command:
            [ 
              "sh",
              "-c",
              "until nslookup myservice; do echo waiting for myservice; sleep 2; done",
            ]

        - name: init-mydb
          image: busybox
          command:
            [
              "sh",
              "-c",
              "until nslookup mydb; do echo waiting for mydb; sleep 2; done",
            ]


	# vim  init_myservice_svc.yaml
	kind: Service
    apiVersion: v1
    metadata:
      name:  myservice
    spec:
      ports:
      - protocol:  TCP
        port:  80
        targetPort:  9376
    
    # vim  init_mydb_svc.yaml
    kind: Service
    apiVersion: v1
    metadata:
      name:  mydb
    spec:
      ports:
      - protocol:  TCP
        port:  80
        targetPort:  9377
        
        
kubectl create -f init_pod.yml
or 
kubectl apply  -f init_pod.yml   

kubectl get pod -o wide -w
kubectl get svc 
kubectl get pod -n kube-system
kubectl describe pod xxx 

# 启动myservice 和 mydb 两个相应服务
kubectl create -f init_mydb_svc.yaml
kubectl create -f init_myservice_svc.yaml
kubectl get pod -o wide -w

kubectl delete pod --all
kubectl delete svc xxx xxx 

kubectl edit pod xxx
```



kubectl apply 和 kubectl create 区别：

| 序号 | kubectl apply                                                | kubectl create                                               |
| ---- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 1    | 根据yaml文件中包含的字段（yaml文件可以只写需要改动的字段），直接升级集群中的现有资源对象 | 首先删除集群中现有的所有资源，然后重新根据yaml文件（必须是完整的配置信息）生成新的资源对象 |
| 2    | yaml文件可以不完整，只写需要的字段                           | yaml文件必须是完整的配置字段内容                             |
| 3    | kubectl apply只工作在yaml文件中的某些改动过的字段            | kubectl create工作在yaml文件中的所有字段                     |
| 4    | 在只改动了yaml文件中的某些声明时，而不是全部改动，你可以使用kubectl apply | 在没有改动yaml文件时，使用同一个yaml文件执行命令kubectl replace，将不会成功（fail掉），因为缺少相关改动信息 |

总结： kubectl create首先删除集群中现有的所有资源，然后重新根据yaml文件（必须是完整的配置信息）生成新的资源对象，没有改动重复运行该命令，则会抛出错误；kubectl apply，在只改动了yaml文件中的部分声明时，而不是全部改动；新的资源 kubectl create,  后续改动kubectl apply



#### 4.8.2 readiness&liveness

```
探针是由容器kubelet对容器的定期检测

三种类型：
	exec:        退出码为0，    成功
	tcpsockets： 端口打开，     成功
	httpGet：	状态码为200，  成功
	
三种结果：
	成功： 容器通过了诊断
	失败： 容器未通过诊断
	未知： 诊断失败，不采取任何行动
	
探测方案：
	livenessprobe：  指示容器是否在运行，如果存活检测失败，则kubelet会杀死容器，并且受到重启策略的影响；如果容器不提供存活探针，则默认为success
	readlinessprobe：反应容器时候准备好接受请求，如果检测失败，状态不是ready, 端点控制器将从与pod匹配的所有service端点中删除pod的ip地址
	

检测探针-就绪检测-httpGet
# vim readiness-httpget.yaml

apiVersion: v1
kind: Pod
metadata:
  name: readiness-httpget-pod
  namespace: default
  labels:
    name: myapp
spec:
  containers:
    - name: readiness-httpget-container
      image: hub.atguigu.com/library/nginx:v1
      imagePullPolicy: IfNotPresent

      readinessProbe:
        httpGet:
          port: 80
          path: /index.html
        initialDelaySeconds: 1
        periodSeconds: 3

kubectl exec xxx  -c  yyy  -it  -- /bin/sh

cd /usr/share/nginx/html
echo "hello" >>index.html


kubectl get pod -o wide 
curl ip    # 结果在最下面
	


检测探针-存活检测-exec
# vim liveness-exec.yaml
apiVersion: v1
kind: Pod
metadata:
  name: liveness-exec-pod
spec:
  containers:
    - name: liveness-exec-container
      image: hub.atguigu.com/library/nginx:v1
      imagePullPolicy: IfNotPresent
      command:
        [
          "/bin/bash",
          "-c",
          "touch /tmp/live; sleep 60; rm -rf /tmp/live; sleep 3600",
        ]

      livenessProbe:
        exec:
          command: ["test", "-e", "/tmp/live"]
        initialDelaySeconds: 1
        periodSeconds: 3
        
        
kubectl exec liveness-exec-pod -c liveness-exec-container -it -- /bin/sh
cd /tmp/
ls 



检测探针-存活检测-httpGet
# vim liveness-httpget.yaml 

apiVersion: v1
kind: Pod
metadata:
  name: liveness-httpget-pod
spec:
  containers:
    - name: liveness-httpget-container
      image: hub.atguigu.com/library/nginx:v1
      imagePullPolicy: IfNotPresent
      command:
        [
          "/bin/bash",
          "-c",
          "touch /tmp/live; sleep 60; rm -rf /tmp/live; sleep 3600",
        ]

      ports:
        - name: http
          containerPort: 80

      livenessProbe:
        httpGet:
          port: http
          path: /index.html
        initialDelaySeconds: 1
        periodSeconds: 3
        timeoutSeconds: 10


检测探针-存活检测-tcpSocket
# vim liveness-tcp.yaml

apiVersion: v1
kind: Pod
metadata:
  name: liveness-tcp-pod
spec:
  containers:
    - name: liveness-tcp-container
      image: hub.atguigu.com/library/nginx:v1

      livenessProbe:
        initialDelaySeconds: 1
        periodSeconds: 3
        timeoutSeconds: 10
        tcpSocket:
          port: 80


检测探针-存活检测&就绪检测
# vim readiness_liveness.yaml
apiVersion: v1
kind: Pod
metadata:
  name: liveness-httpget-pod
spec:
  containers:
    - name: liveness-httpget-container
      image: hub.atguigu.com/library/nginx:v1
      imagePullPolicy: IfNotPresent
      command:
        [
          "/bin/bash",
          "-c",
          "touch /tmp/live; sleep 60; rm -rf /tmp/live; sleep 3600",
        ]

      ports:
        - name: http
          containerPort: 80

      readinessProbe:
        httpGet:
          port: 80
          path: /index.html
        initialDelaySeconds: 1
        periodSeconds: 3

      livenessProbe:
        httpGet:
          port: http
          path: /index.html
        initialDelaySeconds: 1
        periodSeconds: 3
        timeoutSeconds: 10

```



#### 4.8.3 start&stop

```
main c     postStart, preStop 启动， 退出操作

# vim start_stop.yaml

apiVersion: v1
kind: Pod
metadata:
  name: lifecycle-port

spec:
  containers:
    - name: lifecycle-container
      image: hub.atguigu.com/library/nginx:v1

      lifecycle:
        postStart:
          exec:
            command: ["/bin/bash", "-c", "echo hello from the poststart handler"]
        preStop:
          exec:
            command: ["/bin/bash", "-c", "echo hello from the prestop handler"]

```



#### 4.8.4 状态

```
pending:   pod已被k8s接受，当有一个或者多个容器未被创建
running：  pod已经被绑定一个节点上，pod中所有容器已经创建，至少有一个容器在运行，或者正处于启动或者重启
successed: pod中的所有容器已经成功创建
failed：   至少一个容器因为失败终止
unknown：  无法获取pod的状态，通信失败
```





### 4.9 控制器使用(***)

#### 4.9.1 review

```
rc

rs: 集合式的selector，标签来选择

deployment: 
	声明式  apply 	 deployment
	命令式  create  rs 
	
	通过rs创建pod
	滚动升级和回滚应用(rs副本)  根据版本，数量变少，或者为0
	扩容，缩容
	暂停和继续      
	
HPA:	
	水平自动扩展
	
Daemontset:
	确保全部或者一些Node上运行一个Pod的副本, 注入agent/exporter
	典型用法：
		运行存储daemon. 例如每个Node上运行ceph
		运行日志收集daemon
		运行监控daemon
		
Job&cronjob
	有纠错能力
	
statefulset:
	有状态服务的问题
	场景：
        稳定的网络存储	  pvc
        稳定的网络标识   podname hostname  没有clusterIP的service
        有序部署，有序扩展
        有序收缩，有序删除
```



#### 4.9.2 rs

```
# vim rs.yaml
apiVersion: extensions/v1beta1
kind: ReplicaSet
metadata:
  name: frontend
spec:
  replicas: 3
  selector:
    matchLabels:
      tier: frontend
  template:
    metadata:
      labels:
        tier: frontend
    spec:
      containers:
        - name: nginx-v1
          image: hub.atguigu.com/library/nginx:v1
          ports:
            - containerPort: 80

kubectl get pod --show-labels

// 给pod打标签，更改后发现是先新增，后删除原有的
kubectl label pod frontend-klxcb tier=frontend1  --overwrite=True  
kubectl get pod -o wide -w

kubectl delete rs --all 
```



#### 4.9.3 deployment

```
# vim deployment.yaml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 3
  template:
    metadata:
      labels:
        name: nginx
    spec:
      containers:
        - image: hub.atguigu.com/library/nginx:v1
          name: nginx
          ports:
            - containerPort: 80


kubectl create -f deployment.yaml --record //--record可以记录命令可以很方便的查看每revision变化
kubectl get deployment / rs

# 扩容
kubectl scale deployment nginx-deployment --replicas=5
kubectl get pod 
kubectl get rs          //模板并未变化

# hpa 
kubectl autoscale deployment nginx-deployment --min=10 --max=15 --cpu-percent=80

# 更新镜像, harbor记得打开
kubectl set image deployment/nginx_deploy 容器名=镜像地址:版本
kubectl set image deployment/nginx_deploy nginx=hub.atguigu.com/library/nginx:v2
kubectl get rs        // 镜像修改触发rs模板创建

# 回滚
# 回滚到指定版本
kubectl rollout undo deployment/nginx_deployment --to-revision=2

kubectl describe deployment
kubectl rollout status deployment/nginx-deployment   // 查看更新状态echo $?  退出值是否为0，判断是否成功
kubectl rollout history deployment/nginx-deployment  // 查看历史记录
kubectl rollout pause   deployment/nginx-deployment  // 暂停


# deployment更新策略
1 - 1  到 先创建25%, 删除25%  可通过资源清单相关属性修改
rollover(多个rollout并行): 如果用老版本创建的过程中，使用了新的镜像，会立即删除老的，用新的

# deployment保留历史策略
  spec.revisionHistoryLimit 来指定保留多少revision历史，默认保留所有，设置为0，不允许回退
```



#### 4.9.3 daemonset

> 至少维持一个副本

```
# vim daemonset.yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: daemonset-example
  labels:
    app: daemonset
spec:
  selector:
    matchLabels:
      name: daemonset-example
  template:
    metadata:
      labels:
        name: daemonset-example
    spec:
      containers:
        - name: daemonset-example
          image: hub.atguigu.com/library/nginx:v1
          

kubectl get daemonset
kubectl get pod -o wide -w
```



#### 4.9.4 job&cronjob

```
job 
# vim job.yaml

apiVersion: batch/v1
kind: Job
metadata:
  name: pi
spec:
  template:
    metadata:
      name: pi
    spec:
      containers:
        - name: pi
          image: hub.atguigu.com/library/perl:v1
          command: ["perl", "-Mbignum=bpi", "-wle", "print bpi(2000)"]
      restartPolicy: Never



rz perl.tar.gz 
docker load -i perl.tar    // 每个节点运行或者导入到harbor, 报错

docker pull perl


kubectl create -f job.yaml
kubectl get job

kubectl get pod 
kubectl logs pi-4jr9r
kubectl delete job pi




cronjob.spec:
	.restartPolicy 仅支持 Never 或者 onFailure
	.schedule      指定运行周期， 同cron
	.completions   标识job结束需要成功运行的pod个数，默认为1
	.activeDeadlineSeconds: 最大重试时间
	.jobTemplate

# vim cronjob.yaml
apiVersion: batch/v1beta1
kind: CronJob
metadata:
  name: hello
spec:
  schedule: "*/1 * * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
            - name: hello
              image: busybox
              args:
                - /bin/bash
                - -c
                - date; echo hello from the k8s cluster
          restartPolicy: OnFailure


kubectl get cronjob 
kubectl get jobs 

pods=$(kubectl get pods --selector=job-name=hello-1596430800 --output=jsonpath={.items..metadata.name})

kubectl logs $pods

kubectl delete cronjob xxx

幂等，cronjob 无法获取job成功与否
```





## 5. service(***)

```
# 作用: 
	负责检测pod状态，使pod能够被svc(service)发现，下层的扩容更新不会对上层应用有影响； 通过label selector 对一组pod做服务发现，采用的是rr算法

# 特点:
	能够提供4层负载均衡(ip + port)，没有7层能力，不能通过主机名和域名的方式来负载均衡，可通过ingress来实现7层.

# 四种类型:
clusterIP: 自动分配一个仅clusterIP内部可以访问的ip

NodePort:  在clusterIP的基础上绑定一个端口，这样可以通过NodeIP:NodePort来访问, 暴露内部服务(外部还会加负载均衡保证高可用)

LoadBalancer: 在nodeport的基础上，加上cloud provider(云供应商)， 不需要外部加负载均衡，就可以将请求转发到指定的节点的ip+port上

externalName: 把集群外部的服务引入到内部来，kube 1.7 或者更高版本的kube-dns才支持，通过在集群内部创建svc, 记录外部的ip+port, 集群内部的pod直接通过ip+port就可访问外部服务
```



svc原理：



![](imgs\010-kube-proxy.png)

```
apiserver(watch svc, write info into etcd ) --- kube-proxy(open proxy port) --- iptables

client --- iptables --- kube-proxy(rr) --- pod 
```



### 5.1 代理模式

> node中 包含userspace和kernel space ,  userspace中包含pod 和 kube-proxy

```
# kube-proxy的作用: k8s集群中, 每个node运行一个kube-proxy进程, kube-proxy负责为service实现一种vip(虚拟ip), 而不是externalName.

# kube-proxy发展: userspace(1.0) --- iptables(1.2 默认)--- ipvs(1.14 默认)

# 为什么不用round-robin dns?
  dns会进行缓存，负载均衡达不到效果
```

#### 5.1.1 userspace 

> 问题： 很多请求会经过kube-proxy , 压力大

![](imgs\011-userspace代理模式.png)



#### 5.1.2  iptables

> 请求直接经过iptables转发，Kube-proxy 负责开放代理端口，写入规则



![](imgs\012-iptables代理模式.png)



#### 5.1.3 ipvs

> iptables 换成ipvs, 更多的算法选择
>
> 要求先安装ipvs,  开启相应的算法， 如果没有会回退为iptables 
>
> 查看ipvs： ipvsadm -Ln   



![](imgs\013-ipvs代理模式.png)





### 5.2 ClusterIP

> 包括无头服务headless service    statefulset的基础

```
# 熟悉svc流程， 见上面service原理

    # vim clusterip_deployment.yaml
    # set paste 
    
    	apiVersion: apps/v1
        kind: Deployment
        metadata:
          name: myapp-deployment
          namespace: default
        spec:
          replicas: 3
          selector:
            matchLabels:
              app: myapp
              release: stabel
          template:
            metadata:
              labels:
                app: myapp
                release: stabel
                env: test
            spec:
              containers:
                - image: hub.atguigu.com/library/nginx:v1
                  imagePullPolicy: IfNotPresent
                  name: myapp
                  ports:
                    - name: http
                      containerPort: 80
              



    # vim clusterip.yaml 
    # service 通过label selector 来访问pod, 所以标签需要对应
    
        kind: Service
        apiVersion: v1
        metadata:
          name: myservice
          namespace: default
        spec:
          selector:
            app: myapp
            release: stabel
          type: ClusterIP
          ports:
            - name: http
              port: 80
              targetPort: 80
    
    kubectl get svc 
    
    curl ip 

    kubectl delete -f clusterip.yaml 
    

# headless service   statefulset的基础, 特殊的clusterIP
# 作用：不需要或者不想要负载均衡，以及单独的service ip, 可以通过  clusterIP: "None", 这类service并不会分配clusterIP, kube-proxy不会处理他们, 但是依然能通过访问域名(ip)的方式访问到相应的pod

# vim headless-service.yaml 
    	kind: Service
        apiVersion: v1
        metadata:
          name: myservice-headless
          namespace: default
        spec:
          selector:
            app: myapp

          clusterIP: "None"
          ports:
            - port: 80
              targetPort: 8080
	
	// svc创建后会写入到 coredns
	// 拿到ip, 方便下面dig 
    kubectl get pod -n kube-system -o wide     

    yum install -y bind-utils 
    # dig -t A podname.namespace.svc.cluster.local. @ip
    dig -t A myservice-headless.default.svc.cluster.local. @10.244.0.2
```



### 5.3 NodePort(***)

```
node上开了一个端口, 内部服务暴露给外部, 所有节点都会开启这个端口，netlink

# vim nodeport.yaml 
kind: Service
apiVersion: v1
metadata:
  name: myservice-nodeport
  namespace: default
spec:
  selector:
    app: myapp
    release: stabel
  type: NodePort
  ports:
    - name: http
      port: 80
      targetPort: 80
      nodePort: 8080    // 指定端口, 也可不指定, 不指定就是随机端口

# 查询
kubectl get svc 
192.168.66.10:30478

netstat -anpt | grep :30478
iptables -t nat -nvL
```



### 5.4 LoadBalancer

> https://www.jianshu.com/p/4595ca7e29c8

```
跟 nodeport 一样, 只是外部负载均衡用的是 cloud provider， 云厂商的
```



### 5.5 ExternalName

```
说明:
这个类型的service 通过返回dns cname和它的值，将服务转发到制定域名（映射到externalName中的字段值)例如：hub.atguigu.com)

没有selector, 也不需要定义任何的端口和 endpoint，对于集群外部服务，它是通过访问外部服务别名
外部流量引入到集群内部, svc负责记录集群外 ip + port

# vim externalName.yaml
kind: Service
apiVersion: v1
metadata:
  name: myservice-externalname
  namespace: default
spec:
  type: ExternalName
  externalName: hub.atguigu.com



访问  myservice-externalname.default.svc.cluster.local 时，集群的dns服务将返回 hub.atguigu.com, 唯一不同的是重定向发生在dns层，不会进行代理和转发

kubectl get svc 

kubectl get pod -o wide -n kube-system     //查看coredns的ip

dig -t A myservice-externalname.default.svc.cluster.local. @10.244.0.2
```



### 5.6 ingress(***)

> 1.11 新增
>
> https://kubernetes.github.io/ingress-nginx



flannel 解决方案：

![](imgs\004-flannel架构.png)

```
# 场景： 
	client -- ngnix(https开启认证即可, 内部走http,  私有网络) -- apache -- mysql 

# 作用： 
    7层代理，常见的有ingress-nginx, ingress-haproxy 等等
    借助ingress，不需要进入nginx，通过定义ingress配置，由ingress写入到nginx的配置文件中
    
# 部署ingress-nginx：镜像需要挂代理提前下载, yaml文件可以利用edge下载
    wget https://github.com/kubernetes/ingress-nginx/tree/nginx-0.24.1/deploy/mandatory.yaml
   
    wget https://github.com/kubernetes/ingress-nginx/tree/nginx-0.24.1/deploy/provider/baremetal/service-nodeport.yaml
    
    // 上述下载可能报错，可以在github中找到相应的文件，raw下载
    cat mandatory |  grep image
    # image: quay.io/kubernetes-ingress-controller/nginx-ingress-controller:0.24.1
    # docker pull quay.io/kubernetes-ingress-controller/nginx-ingress-controller:0.24.1
    
    tar -xvf ingree.contro.tar.gz
   
   	# 每个节点上上传
    docker load -i ingree.contro.tar
	
    kubectl apply -f mandatory.yaml
    
    kubectl apply -f service-nodeport.yaml
	
    kubectl get pod -n ingress-nginx 
    kubectl get svc -n ingress-nginx


# 使用1：ingress http代理（可以在一个文件中既写入deployment, 又写入service)
# vim ingress-deployment.yaml

apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: nginx-deploy
spec:
  replicas: 2
  template:
    metadata:
      labels:
        name: nginx
    spec:
      containers:
        - image: hub.atguigu.com/library/nginx:v1
          name: nginx
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 80
---
kind: Service
apiVersion: v1
metadata:
  name: nginx-svc
spec:
  selector:
    name: nginx
  ports:
    - port: 80
      targetPort: 80
      protocol: TCP



# vim  ingress-http.yaml

kind: Ingress
apiVersion: extensions/v1beta1
metadata:
  name: nginx-http
spec:
  rules:
    - host: www1.atguigu.com
      http:
        paths:
          - path: /
            backend:
              serviceName: nginx-svc
              servicePort: 80


kubectl get svc
curl ip    // 先判断nginx service是否启动起来

kubectl get svc -n ingress-nginx      // 查看svc随机端口

需要配置hosts文件

浏览器访问：www1.atguigu.com:30315     // 为啥是30315?  是个随机端口，由上面查看得到



# 使用1.1 ingress实现service的pod升级(高可用) 
kubectl get ingress 


# 使用2：ingress https代理
openssl req -x509 -sha256 -nodes -days 365 -newkey rsa:2048 -keyout tls.key -out tls.crt  -subj "/CN=nginxsvc/O=nginxsvc"

kubectl create secret tls tls-secret --key tls.key --cert tls.crt
    
# vim ingress-https.yaml 
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: nginx-https
spec:
  tls:
    - hosts:
        - www2.atguigu.com
      secretName: tls-secret

  rules:
    - host: www2.atguigu.com
      http:
        paths:
          - path: /
            backend:
              serviceName: nginx-svc
              servicePort: 80
	
kubectl get svc -n ingress-nginx     //获取443对应的随机端口
https://www2.atguigu.com:30082/      //后面是上面得到的随机端口


# 使用3：ingress 对nginx进行basicAuth(输入用户名，密码)
yum install -y httpd  
htpasswd -c auth foo      //123456  将来界面上登录用，  foo 123456
kubectl create secret generic basic-auth  --from-file=auth
 
# vim ingress-basic-auth.yaml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: nginx-basic-auth
  annotations:
    nginx.ingress.kubernetes.io/auth-type: basic
    nginx.ingress.kubernetes.io/auth-secret: basic-auth
    nginx.ingress.kubernetes.io/auth-realm: "Authentication Required - foo"
spec:
  rules:
    - host: www3.atguigu.com
      http:
        paths:
          - path: /
            backend:
              serviceName: nginx-svc
              servicePort: 80
              
kubectl get svc -n ingress-nginx              
www3.atguigu.com:30315  


# 使用4：ingrees 对nginx进行重写
# vim ingress-rewrite.yaml

apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: nginx-rewrite
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: https://www2.atguigu.com:30082
    # nginx.ingress.kubernetes.io/ssl-redirect: true
    # nginx.ingress.kubernetes.io/force-ssl-redirect: true
    # nginx.ingress.kubernetes.io/app-root: /
    # nginx.ingress.kubernetes.io/use-regex: true

spec:
  rules:
    - host: www4.atguigu.com
      http:
        paths:
          - path: /
            backend:
              serviceName: nginx-svc
              servicePort: 80


www4.atguigu.com:30315   --> www2.atguigu.com:30082
```

![](imgs\21-ingress使用2.png)





## 6. 存储

> 难点在于区分使用场景

```
分类：
	configmap 			  配置文件
	secret                 加密的信息
	volume	               共享存储卷(数据可能会丢失)
	pvc                    持久卷容器
	pv(persistent volume)  持久卷
```



### 6.1 configmap(***)

> 注意: configmap 能热更新，但是pod需要重启，才能实现热更新

```
简介：提供了容器中注入配置信息的机制，可以是单个属性，也可以是整个配置文件，或者json二进制文件。(生产环境中可用作配置文件、注册中心)

案例: configmap中有nginx.conf, 创建Pod的时候将配置注入到容器中

注意: configmap能热更新，但是pod需要重启，才能实现热更新

创建的三种方式：
    1. 目录
    2. 文件
    3. 字面值(键值)
```



#### 6.1.1 使用目录创建

> 创建的时候指定的是目录

```
mkdir configMap_dir
# vim game.properties
enemies=aliens
lives=3
enemies.cheat=true


# vim ui.properties
color.good=purple
color.bad=yellow


kubectl create configmap game-config --from-file=./configMap_dir
kubectl get cm [ game-config -o yaml ]
kubectl describe cm 
```



#### 6.1.2 使用文件创建

> 创建的时候指定的是目录下具体的文件

```
kubectl create configmap game-config2 --from-file=./configMap_dir/game.properties

kubectl get cm  game-config2 [-o yaml]
```



#### 6.1.3 使用字面量创建

```
kubectl create configmap special-config --from-literal=special.how=very --from-literal=special.type=charm

kubectl  get cm special-config -o yaml 
```



#### 6.1.4 使用场景

```
场景1： 在配置中使用envFrom和env替代环境变量
# vim configmap_special_config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: special-config
data:
  special.how: very
  special.type: charm


# vim configmap_env_config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: env-config
data:
  log_level: INFO

# vim configmap_env_pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: configmap-env
  labels:
    name: configmap-env
spec:
  containers:
    - name: configmap-env-container
      image: hub.atguigu.com/library/nginx:v1
      command: ["/bin/bash", "-c", "env"]
      env:
        - name: SPECIAL_LEVEL_KEY
          valueFrom:
            configMapKeyRef:
              name: special-config
              key: special.how

        - name: SPECIAL_TYPE_KEY
          valueFrom:
            configMapKeyRef:
              name: special-config
              key: special.type
      envFrom:
        - configMapRef:
            name: env-config
  restartPolicy: Never


kubectl create -f configmap_special_config.yaml
kubectl create -f configmap_env_config.yaml
kubectl create -f confimap_env.yaml

kubectl logs configmap-env  | grep TYPE
kubectl logs configmap-env  | grep LEVEL


场景2： 设置命令行参数 
# vim configmap_cli.yaml
apiVersion: v1
kind: Pod
metadata:
  name: configmap-cli
  labels:
    name: configmap-cli
spec:
  containers:
    - name: configmap-cli-container
      image: hub.atguigu.com/library/nginx:v1
      command: ["/bin/bash", "-c", "echo  $(SPECIAL_LEVEL_KEY) $(SPECIAL_TYPE_KEY) "]
      env:
        - name: SPECIAL_LEVEL_KEY
          valueFrom:
            configMapKeyRef:
              name: special-config
              key: special.how

        - name: SPECIAL_TYPE_KEY
          valueFrom:
            configMapKeyRef:
              name: special-config
              key: special.type
  restartPolicy: Never

kubectl create -f confimap_cli.yaml
kubectl logs configmap-cli



场景3： 数据卷插件使用configMap(***), 将configmap挂载到数据卷下
# vim configmap_volume.yaml
apiVersion: v1
kind: Pod
metadata:
  name: configmap-volume
  labels:
    name: configmap-volume
spec:
  containers:
    - name: configmap-volume-container
      image: hub.atguigu.com/library/nginx:v1
      command: ["/bin/bash", "-c", "sleep 200"]
      volumeMounts:
        - name: config-volume
          mountPath: /etc/config
  volumes:
    - name: config-volume
      configMap:
        name: special-config
  restartPolicy: Never


kubectl create -f configmap_volume.yaml
kubectl exec configmap-volume -it -- bash

#结果
# cd /etc/config
# ls 
special.how special.type


场景4： 使用configMap挂载nginx配置文件 nginx.conf到指定目录下(前提是现有nginx.conf)
kubectl create configmap nginx-config --from-file=./nginx.conf

# vim configmap_volume_nginx.yaml
apiVersion: v1
kind: Pod
metadata:
  name: configmap-volume-nginx
  labels:
    name: configmap-volume-nginx
spec:
  containers:
    - name: configmap-volume-nginx-container
      image: hub.atguigu.com/library/nginx:v1
      command: ["/bin/bash", "-c", "sleep 200"]
      volumeMounts:
        - name: config-volume2
          mountPath: /etc/config
  volumes:
    - name: config-volume2
      configMap:
        name: nginx-config
  restartPolicy: Never

kubectl create -f configmap_volume_nginx.yaml
kubectl exec configmap-volume -it -- bash

ls
# nginx.conf
```



#### 6.1.5 热更新

> 1. 解决configmap更新后，pod需要重启才能更新的方式： 通过给annocation添加 version/config, 每次修改完值即可滚动更新
>2. configmap挂载的env不会同步更新
> 3. configmap挂载的volume中的数据需要一段时间才能同步  
> 4. traefik



```
# vim configmap_hot_update.yaml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: configmap-hot-update
spec:
  replicas: 1
  template:
    metadata:
      labels:
        name: configmap-hot-update
    spec:
      containers:
        - image: hub.atguigu.com/library/nginx:v1
          name: configmap-hot-update-container
          volumeMounts:
            - name: config-volume
              mountPath: /etc/config

      volumes:
        - name: config-volume
          configMap:
            name: env-config



kubectl create -f configmap_hot_update.yaml

# kubectl exec configmap-hot-update-xxx -it -- sh

  kubectl exec `kubectl get pods -l name=configmap-hot-update -o=name | cut -d "/" -f2` -it  -- cat /etc/config/log_level

  kubectl edit configmap env-config    # 改为debug
    
  大概10s后再次查看环境变量(因为挂载的volume)
  kubectl exec `kubectl get pods -l name=configmap-hot-update -o=name | cut -d "/" -f2` -it  -- cat /etc/config/log_level


    
注意：
	1. configmap挂载的env不会同步更新
    2. configmap挂载的volume中的数据需要一段时间才能同步(如果是nginx配置文件，此时可以热更新) 
    3. configmap能热更新，但是pod需要重启才能更新, 怎么在configmap更新后强制pod滚动更新？？？
    通过给annocation添加 version/config, 每次修改改值即可滚动更新

// 该方式不生效
kubectl patch deployment configmap-hot-update --patch '{"spec":{"template":{"metadata":{"annocation":{"version/config":"202008041607"}}}}}'

// 下面的生效  https://www.jianshu.com/p/3aedd9464895
kubectl patch deployment configmap-hot-update --patch '{"spec": {"template": {"metadata": {"annotations": {"update": "202008041607" }}}}}'

// 可看到pod的更新更新过程
kubectl get deployment -o wide -w
```





### 6.2 secret(***)

```
作用： 解决密码，token等敏感数据的配置问题，而不是将这些数据暴露在pod.spec中， secret可以以volume或者环境变量的方式使用

分类：
	service account(sa): 用来访问kubenetes api, 由kubenetes创建, 挂载到指定目录
	opaque:              用来存储密码，秘钥，存放的是base64编码后的值，使用时自解密
    dockerconfigjson:    用来存储docker registry的认证信息
```



#### 6.2.1 sa

```
用来访问kubernetes api, 由kubenetes创建，挂载到/var/run/secrets/kubernetes.io/serviceaccount

kubectl run nginx --image hub.atguigu.com/library/nginx:v1

kubectl exec `kubectl get pods -l run=nginx -o=name | cut -d "/" -f2` ls /var/run/secrets/kubernetes.io/serviceaccount


kubectl exec -it `kubectl get pods -l run=nginx -o=name | cut -d "/" -f2` ls /var/run/secrets/kubernetes.io/serviceaccount

"""
ca.crt
namespace
token
"""

kubectl create sa dashboard-sa
kubectl get sa
kubectl describe sa dashboard-sa
```



#### 6.2.2 opaque

```
用来存储密码，秘钥，存放的是base64编码后的值，使用的时候自己会解密

echo -n "admin" | base64
echo -n "123456"| base64

# 准备Opaque的secret(mysecret)
# vim secrets.yaml 
apiVersion: v1
kind: Secret
metadata:
  name: mysecret
type: Opaque
data:
  username: YWRtaW4=
  password: MTIzNDU2

kubectl create -f secrets.yaml 
kubectl get secret 

# 使用方式1： secret挂载到volume
# vim secret_Opaque_volume.yaml
apiVersion: v1
kind: Pod
metadata:
  name: secret-opaque-volume-pod
  labels:
    name: secret-opaque-volume-pod
spec:
  containers:
    - name: secret-opaque-volume-container
      image: hub.atguigu.com/library/nginx:v1
      volumeMounts:
        - name: secrets
          mountPath: /tmp/
          readOnly: true

  volumes:
    - name: secrets
      secret:
        # 下面的mysecret是上面创建的secret
        secretName: mysecret 


kubectl create -f secret_Opaque_volume.yaml

# 打了labels才能识别出来
# 在/tmp下会有  username 和 password
kubectl exec `kubectl get pods -l name=secret-opaque-volume-pod  -o=name | cut -d "/" -f2` cat /tmp/username


# 使用方式2： secret导出到环境变量中
# vim secret_Opaque_env.yaml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: secret-opaque-env
spec:
  replicas: 1
  template:
    metadata:
      labels:
        name: secret-opaque-env
    spec:
      containers:
        - image: hub.atguigu.com/library/nginx:v1
          name: secret-opaque-env
          ports:
            - containerPort: 80
          env:
            # 此处的TEST_USER相当于 username 的别名
            - name: TEST_USER
              valueFrom:
                secretKeyRef:
                  #下面的mysecret是上面创建的secret
                  name: mysecret
                  key: username

            - name: TEST_PASSWORD
              valueFrom:
                secretKeyRef:
                  #下面的mysecret是上面创建的secret
                  name: mysecret
                  key: password


kubectl create -f secret_Opaque_env.yaml

# 打了labels才能识别出来
kubectl exec `kubectl get pods -l name=secret-opaque-env -o=name | cut -d "/" -f2` env | grep TEST_USER 
```



#### 6.2.3 dockerconfigjson

> harbor 地址： 
>
> https://hub.atguigu.com
>
> admin
> Harbor12345

```
完成harbor中的认证, 在harbor创建私有仓库mysql, docker logout, 推mysql到仓库中


docker tag nginx:latest hub.atguigu.com/mylibrary/nginx:v1
docker push hub.atguigu.com/mylibrary/nginx:v1

docker logout  hub.atguigu.com
docker rmi 
docker pull hub.atguigu.com/mylibrary/nginx:v1



kubectl create secret docker-registry myregistrykey --docker-server=hub.atguigu.com --docker-username=admin --docker-password=Harbor12345 --docker-email="123@qq.com"
		
# vim secret-dockerconfig.yaml
apiVersion: v1
kind: Pod
metadata:
  name: foo
spec:
  containers:
    - name: foo
      image: hub.atguigu.com/mylibrary/nginx:v1

  imagePullSecrets:
    - name: myregistrykey
    

kubectl create -f secret-dockerconfig.yaml
kubectl get pod foo    # 发现能正常运行
```





### 6.3 volume

> 解决的问题： 常用于容器间共享文件
>
> 生命周期：    与封装它的pod相同
>
> 问题： pod删除后，hostpath 数据不会丢失，如果再次挂载里面时间还在么？ 在，数据不会丢失，存储卷在Pod迁移到其它节点后数据就会丢失，所以只能用于存储临时数据或用于在同一个Pod里的容器之间共享数据。

```
通常容器崩溃时， kubelet会重启它， 但是文件会丢失，容器以干净的状态(镜像最初的状态)重新启动，需要能有持久化存储；其次，在pod中同时运行多个容器时，这些容器之间通常需要共享文件，volume 抽象很好的解决了这一问题。
	
卷的寿命：与封装它的pod相同。

最基础的pod构成：
    c1	   c2
      pause(共享存储卷)
      volume

kubernetes支持的卷：
	emptydir
	hostpath 
	nfs
	azuredisk
	...
```



#### 6.3.1 emptydir

```
当pod分配给节点的时候，首先创建emptydir卷，与pause绑定, 并且只要该pod在该节点上运行，该卷就会存在，pod中容器可以写入和读取emptydir中的相同文件，可以挂载到每个容器相同或者不同路径上，从节点中删除pod, emptydir中的数据将被永久删除，崩溃不会删除，因为崩溃不会从节点中删除pod

用法：
    1.暂存空间, 例如用于基于磁盘的合并排序
    2.用作长时间计算崩溃恢复时的检查点
    3.web服务器提供数据时，保存内容管理器容器提取的文件
    
节点下的容器都可以往不同的挂载点写入数据，对其他的容器中可见

# 跟configmap的 yaml 文件很像
# 注意：有多个container, busybox需要让容器运行起来，mysql需要输入密码，两者都有些问题，因此选择了nginx
# 下面的例子是作为共享卷测试

# vim volume-emptydir.yaml
apiVersion: v1
kind: Pod
metadata:
  name: volume-emptydir-pod
  labels:
    name: volume-emptydir-pod
spec:
  containers:
    - name: container1
      image: hub.atguigu.com/library/nginx:v1
      volumeMounts:
        - name: cache-volume
          mountPath: /cache

    - name: container2
      image: hub.atguigu.com/library/nginx:v1
      command: ["/bin/sh" ,"-c", "sleep 200s"]
      volumeMounts:
        - name: cache-volume
          mountPath: /test

  volumes:
    - name: cache-volume
      emptyDir: {}

kubectl exec volume-emptydir-pod -c container1 -it -- sh 
cd /cache 
date > index.html 
cat index.html


kubectl exec volume-emptydir-pod -c container2 -it -- sh
cd /test 
ls
cat index.html
```



#### 6.3.2 hostpath

> 很灵活， 可以跟任何存储对接,  特殊的pv

```
简介： 将主机节点的文件系统中的文件或者目录挂载到集群中（configmap也可以实现类似的功能）

用途：
	1.运行中本地需要访问docker容器，使用 /var/lib/docker的hostpath
	2.在容器中运行cAdvisor，       使用 /dev/cgroups   的hostpath
	
除了所需的path属性外，还可以指定type:
    空               
    DirectoryOrCreate    给定的目录不存在，就创建
    Directory            给定的目录必须存在
    FileOrCreate         文件不存在，就创建
    File                 文件必须存在
    Socket				 unix套接字必须存在
    CharDevice			 字符设备
    BlockDevice			 块设备
    
    
    e.g:
    	  volumes:
            - name: test-volume
              hostPath:
                path: /data
                type: Directory
    
    
注意事项：
	1. 每个节点上文件的不同，具有相同配置的pod在不同节点上的行为可能有所不同(所以所有节点挂载的要相同)
	2. k8s按照计划添加资源感知调度时，无法考虑hostpath使用的资源
	3. 特定容器中以root身份运行，或者修改主机上的文件权限以便写入 hostpath 卷
	
# vim volume-hostpath.yaml 
apiVersion: v1
kind: Pod
metadata:
  name: test-pod
  labels:
    name: test-pod
spec:
  containers:
    - name: test-container
      image: hub.atguigu.com/library/nginx:v1
      imagePullPolicy: IfNotPresent
      volumeMounts:
        - name: test-volume
          mountPath: /hostpath

  volumes:
    - name: test-volume
      hostPath:
        path: /data
        type: Directory


# 注意docker需要是root权限
ps aux | grep docker

# 每个节点下都要创建data文件夹， 因为不知道分配到哪个节点
mkdir /data

# 创建Pod
kubectl create -f volume-hostpath.yaml

# 可查看分配到哪个节点上，去对应的节点上看才会有, 比如：node1
kubectl get pod -o wide
kubectl exec test-pod -it -- sh
cd /hostpath
date > index.html


cd /data 
ls
cat index.html 
date >> index.html


kubectl exec test-pod -it -- sh
cd /hostpath
cat index.html
```

#### 6.3.3 区别

```
https://blog.csdn.net/qq_33591903/article/details/103529274

emptydir:
	1. pod删除时，其emptyDir中的数据也会被删除
	2. pod分配到node上时被创建，在node上自动分配一个目录，因此无需指定宿主机node上对应的目录文件
	3. 主要用于某些应用程序无需永久保存的临时目录，多个容器的共享目录
hostpath:
	1. pod删除原先Node上的存储卷还在
	2. 下次调度到另一个节点上启动时，就无法使用在之前节点上存储的文件
```



### 6.4 pv&pvc(***)

#### 6.4.1 基本认识

> pv与pod是独立的，pvc 管理pv，消耗pv资源，pvc 和 pv 是一一对应的，绑定后具有排他性

```
pv独立于pod的生命周期之外(pod被删除，pv依然在), pv类似一个抽象层，包含存储实现的细节，可以对接其他的存储
pvc: 用户存储的请求，与pod相似，pod消耗节点资源，pvc消耗pv资源。pod可以请求特定级别的资源(cpu和内存)，声明可以请求特定的大小和访问模式(例如可以读或者写或者只读)； 通常创建pod的时候， 创建一个pvc, 寻找合适(比如最小)的pv

静态pv: 管理的存储细节
动态pv: 云存储的细节，暂时了解
绑定：  pvc与pv是一一对应的， 绑定后是排他性的

原理见下图

持久卷访问保护：
	防止pod被删除，数据丢失；如果用户删除了一个pod正在使用的pvc, 则pvc不会被立即删除，pvc删除将被推迟，直到pvc不再被任何pod使用
	
持久化卷类型：
	persistentVolume类型以插件的形式实现，目前支持以下插件：
        gce
        flexvolume
        cinder
        hostpath(特殊的pv)
        ceph
	
访问模式：
	ReadWriteOnce  -- RWO    单节点读写，命令行中的缩写
	ReadOnlyMany   -- ROX    多节点只读
	ReadWriteMany  -- RWX    多节点读写
	
	插件对上述访问模式支持不同，参加的见下图

回收策略：
	Retain(保留)    手动回收
	Recycle(回收)   基本擦除, 在最新版本中已经被废弃
	Delete(删除) 	  关联的存储资产将被直接删除(aws ebs, gce pd, cinder)
	
	nfs 和 hostpath 支持回收策略(Recycle), aws ebs, gce pd, cinder 支持删除策略
	
状态：
	Available(可用)：  一块资源还没有被任何声明绑定
	Bound(已绑定)  
	Released
	Failed
```



![](imgs\22-1pv原理.png)





![](imgs\22-volume插件支持模式.png)





#### 6.4.2 简单使用

1. 部署nfs


```
# 192.168.66.40
yum install -y nfs-common nfs-utils rpcbind

mkdir /nfsdata
chmod 777 /nfsdata
chown nfsnobody /nfsdata
vim  /etc/exports
	/nfsdata *(insecure, rw, no_root_squash, no_all_squash, sync)
	
exportfs -rv
systemctl start rpcbind
systemctl start nfs

# 每个节点下都需要安装nfs-tools, rpc
yum install -y  nfs-utils rpcbind
systemctl start rpcbind
systemctl start nfs

# 简单测试, 其他节点
# https://blog.csdn.net/AZXHNLS81/article/details/103859756
# http://www.hmjblog.com/system/linux/2998.html
# https://www.cnblogs.com/feiyun126/p/11344831.html       有用
# exportfs -rv


mkdir /test

showmount -e 192.168.66.40  
//很重要看有没有结果

mount -t nfs 192.168.66.40:/nfsdata /test/   //将/nfsdata挂载至/test目录下，不报错，说明成功
cd /test/
vim 1.txt 

umount /test
rm -rf /test


报错：
	1. device is busy 
	yum install -y psmisc
	fuser -m -v /test/
	kill
```

 

2. 部署pv

```
# vim pv.yaml 
apiVersion: v1
kind: PersistentVolume
metadata:
  name: nfspv1
  namespace: default
  labels:
    app: nfspv1
spec:
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteOnce

  persistentVolumeReclaimPolicy: Retain
  storageClassName: nfs
  nfs:
    path: /nfsdata
    server: 192.168.66.40


kubectl create -f pv.yaml
kubectl get pv


# 192.168.66.40 上多创建几个挂载目录 mkdir /nfsdata1 /nfsdata2  /nfsdata3
vim  /etc/exports
	/nfsdata *(insecure, rw, no_root_squash, no_all_squash, sync)
	/nfsdata1 *(insecure,rw, no_root_squash, no_all_squash, sync)
	/nfsdata2 *(insecure,rw, no_root_squash, no_all_squash, sync)
	/nfsdata3 *(insecure,rw, no_root_squash, no_all_squash, sync)



mkdir /nfsdata{1..3}

chmod 777 /nfsdata1/  /nfsdata2/ /nfsdata3/
chown nfsnobody /nfsdata1/  /nfsdata2/  /nfsdata3/

systemctl restart rpcbind 
systemctl restart nfs
exportfs -rv



# vim pv.yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: nfspv1
  namespace: default
  labels:
    app: nfspv1
spec:
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteOnce

  persistentVolumeReclaimPolicy: Retain
  storageClassName: nfs
  nfs:
    path: /nfsdata
    server: 192.168.66.40
---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: nfspv2
  namespace: default
  labels:
    app: nfspv2
spec:
  capacity:
    storage: 5Gi
  accessModes:
    - ReadOnlyMany

  persistentVolumeReclaimPolicy: Retain
  storageClassName: nfs
  nfs:
    path: /nfsdata1
    server: 192.168.66.40
---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: nfspv3
  namespace: default
  labels:
    app: nfspv3
spec:
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteMany

  persistentVolumeReclaimPolicy: Retain
  storageClassName: slow
  nfs:
    path: /nfsdata2
    server: 192.168.66.40
---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: nfspv4
  namespace: default
  labels:
    app: nfspv4
spec:
  capacity:
    storage: 1Gi
  accessModes:
    - ReadOnlyMany

  persistentVolumeReclaimPolicy: Retain
  storageClassName: nfs
  nfs:
    path: /nfsdata3
    server: 192.168.66.40



kubectl delete pv nfspv3
kubectl apply -f pv.yaml
kubectl get pv 


```

3. 使用pvc

```
# vim pvc.yaml

kind: Service
apiVersion: v1
metadata:
  name: nginx
spec:
  selector:
    app: nginx
  clusterIP: None
  ports:
    - name: www
      port: 80

---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: web
  namespace: default
spec:
  selector:
    matchLabels:
      app: nginx               # has to match .spec.template.metadata.labels
  serviceName: "nginx"
  replicas: 3                  # by default is 1
  template:
    metadata:
      labels:
        app: nginx            # has to match .spec.selector.matchLabels
    spec:
      terminationGracePeriodSeconds: 10
      containers:
      - name: nginx
        image: hub.atguigu.com/library/nginx:v1
        ports:
        - containerPort: 80
          name: web
        volumeMounts:
        - name: www
          mountPath: /usr/share/nginx/html
  volumeClaimTemplates:
  - metadata:
      name: www
    spec:
      accessModes: [ "ReadWriteOnce" ]
      storageClassName: "nfs"
      resources:
        requests:
          storage: 1Gi


kubectl create -f pvc.yaml
kubectl get pv 
kubectl get pvc 
kubectl get pod -w  
kubectl describe pod web-1   # // web-0 能绑定，其他绑定不了，排他性， web-1不成功，web-2看不见(有序)


# 更改原有使其满足要求, nfs, 1g, ReadWriteOnce
kubectl delete pv nfspv3
kubectl delete pv nfspv4


vim pv.yaml  

kubectl get pod -w
kubectl get pv 
kubectl get pvc 
kubectl describe pv nfspv1



#192.168.66.40 
vim /nfsdata/index.html
111111111

chmod 777 /nfsdata/index.html

#192.168.66.10
kubectl get pod -o wide   // 查看web-0 的IP， nfsdata 是和nfspv1, web-0 关联的
curl ip
1111111111


# 删除节点，会创建副本，ip会变， 但是访问名称(hostname和podname)不变
```



![](imgs\23-pv，pvc, statefulset关系.png)



#### 6.4.3 动态pv

```
https://blog.csdn.net/hszxd479946/article/details/108696665
https://blog.csdn.net/liukuan73/article/details/60089305

https://www.cnblogs.com/leozhanggg/p/13611982.html
https://blog.csdn.net/networken/article/details/86697018
https://www.cnblogs.com/wuchangblog/p/13304928.html

image: quay.io/external_storage/nfs-client-provisioner:latest
image: registry.cn-shanghai.aliyuncs.com/leozhanggg/storage/nfs-client-provisioner:latest


# 1.部署nfs 
# 192.168.66.40
yum install -y nfs-common nfs-utils rpcbind

mkdir /nfsdata
chmod 777 /nfsdata
chown nfsnobody /nfsdata
vim  /etc/exports
	/nfsdata *(insecure, rw, no_root_squash, no_all_squash, sync)
	
exportfs -rv
systemctl start rpcbind
systemctl start nfs

# 每个节点下都需要安装nfs-tools, rpc
yum install -y  nfs-utils rpcbind
systemctl start rpcbind
systemctl start nfs



# 2.创建rbac
# vim dynamic_rbac.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: nfs-client-provisioner             #需要记录该名字，后面会用到
  namespace: scm-tools                     #注意修改namespace
---
kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: nfs-client-provisioner-runner
rules:
  - apiGroups: [""]
    resources: ["persistentvolumes"]
    verbs: ["get", "list", "watch", "create", "delete"]
  - apiGroups: [""]
    resources: ["persistentvolumeclaims"]
    verbs: ["get", "list", "watch", "update"]
  - apiGroups: ["storage.k8s.io"]
    resources: ["storageclasses"]
    verbs: ["get", "list", "watch"]
  - apiGroups: [""]
    resources: ["events"]
    verbs: ["create", "update", "patch"]
---
kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: run-nfs-client-provisioner
subjects:
  - kind: ServiceAccount
    name: nfs-client-provisioner
    namespace: scm-tools                #注意修改namespace
roleRef:
  kind: ClusterRole
  name: nfs-client-provisioner-runner
  apiGroup: rbac.authorization.k8s.io
---
kind: Role
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: leader-locking-nfs-client-provisioner
  namespace: scm-tools                  #注意修改namespace
rules:
  - apiGroups: [""]
    resources: ["endpoints"]
    verbs: ["get", "list", "watch", "create", "update", "patch"]
---
kind: RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: leader-locking-nfs-client-provisioner
  namespace: scm-tools                  #注意修改namespace
subjects:
  - kind: ServiceAccount
    name: nfs-client-provisioner
    namespace: scm-tools                #注意修改namespace
roleRef:
  kind: Role
  name: leader-locking-nfs-client-provisioner
  apiGroup: rbac.authorization.k8s.io


kubectl create -f dynamic_rbac.yaml


#3.创建provisioner
#vim dynamic_provisioner.yaml
apiVersion: apps/v1
kind: Deployment                     # provisioner的类型是一个deployment
metadata:
  name: nfs-client-provisioner
  labels:
    app: nfs-client-provisioner
  namespace: scm-tools               # 指定provisioner所属的namespace，改成你自己的namespace
spec:
  replicas: 1
  strategy:
    type: Recreate
  selector:
    matchLabels:
      app: nfs-client-provisioner
  template:
    metadata:
      labels:
        app: nfs-client-provisioner
    spec:
      serviceAccountName: nfs-client-provisioner   # 指定provisioner使用的sa，在上面
      containers:
        - name: nfs-client-provisioner
          image: registry.cn-shanghai.aliyuncs.com/leozhanggg/storage/nfs-client-provisioner:latest
          volumeMounts:
            - name: nfs-client-root
              mountPath: /persistentvolumes       # 固定写法
          env:
            - name: PROVISIONER_NAME
              value: test-storage-class           # 指定分配器的名称，创建storageclass会用到
            - name: NFS_SERVER
              value: 192.168.66.40                # 指定使用哪一块存储，这里用的是nfs，此处填写nfs的地址
            - name: NFS_PATH
              value: /nfsdata                     # 使用nfs哪一块盘符
      volumes:
        - name: nfs-client-root
          nfs:
            server: 192.168.66.40                 # 和上面指定的nfs地址保持一致
            path: /nfsdata                        # 和上面指定的盘符保持一致


kubectl create -f provisioner.yaml
kubectl get deploy -n scm-tools


#4.创建storageclass
# vim dynamic_sc.yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: test-storage                         # storageclass的名字
provisioner: test-storage-class              # 必须与provisioner.yaml中PROVISIONER_NAME的值一致
parameters:
  archiveOnDelete: "false"
  
  
kubectl create -f dynamic_sc.yaml
kubectl get sc


#5.创建一个pvc进行测试
#vim dynamic_pvc.yaml
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  name: scm-pvc
  namespace: scm-tools
spec:
  storageClassName: test-storage           # 需要与上面创建的storageclass的名称一致
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
      
kubectl create -f dynamic-pvc.yaml
kubectl get pvc -n scm-tools
kubectl describe pvc scm-pvc -n scm-tools
```



#### 6.4.4 statefulset(难点)

```
statefulset  无头服务 headless service     clusterIP: none


注意：
	1.匹配pod name(网络标识)的模式为：statefulset-序号, 比如: web-0, web-1, web-2
	2.statefulset为每个pod副本创建了一个dns域名，格式为： pod_name.headness_service_name(比如: web-0.nginx), 这意味着服务间通过pod域名来通信，而非ip, pod发生故障时，pod会漂移到其他node上，pod ip会变化，但是域名不变(coredns)
    3.statefulset使用 headless service来控制pod域名，域名格式为：service_name.namespace.svc.cluster.local(其中cluster.local 指的是集群的域名，比如： nginx.default.svc.cluster.local)
    4.删除pod	不会删除pvc, 手动删除pvc将自动释放pv
    5.根据volumeClaimTemplate, 为每个pod创建一个pvc,	格式为 volumeClaimTemplate_name-pod name-[序号]   wwww-web-0, www-web-1, www-web-2
    
   
   	# 测试上面的结论：
    kubectl exec test-pod -it -- /bin/sh                //test-pod是封装了busybox的pod
	ping web-0.nginx                                   // 即便删除依然可以通过这种方式访问， dns域名
	
	kubectl get pod -n kube-system -o wide            // 查找coredns的IP
	
	dig -t A nginx.default.svc.cluster.local. @10.244.0.2
	
statefulset启停顺序：
	有序部署  
	有序删除 
	有序扩展
	
	# 演示
	kubectl delete statefulset --all
	kubectl delete svc nginx 
	kubectl get pod -o wide -w 
	
	kubectl create -f pvc.yaml
	kubectl get pod -o wide -w 
	
	kubectl delete statefulset --all
	kubectl get pod -o wide -w 


statefulset使用场景：
	参考clusterIP中的使用场景
	稳定的网络标识， podname和hostname不变，不是ip不变

删除最终的数据： 
		kubectl delete -f xxx.yml 
	 	kubectl delete pvc --all   // 手动删除pvc
	 	kubectl get pv             // 资源释放
	    kubectl edit pv nfspvxxx   // 删除claimRef下的内容
	    
	    kubectl get pv           // 资源可用
	    
	    
最终原理图，见下图
```

![](imgs\23-pv，pvc, statefulset关系.png)





#### 6.4.5 volume和pvc区别

```
PV是类似于Volumes的卷插件，但是其生命周期独立于Pod，而 volume 和 pod是静态的绑定关系，生命周期是一致的，volume更多的是做共享，pv做持久化.
```





## 7. 调度

### 7.1 简介

```
scheduler： 主要的任务是把定义的pod分配到集群的节点上

scheduler是单独的程序运行的，启动之后会一直监听api server, 获取podspec.NodeName为空的pod，对每个pod都会创建一个binding, 表明该pod应该在哪个节点上

调度过程：
	1.predicate, 预选， 过滤掉不满足条件的节点
	2.priority,  优选， 按照优先级排序
	3.选择优先级最高的节点
	如果当中有错误，直接返回错误
	
predicate预选算法：
	PodFitsResources:  节点上剩余的资源是否大于pod请求的资源
	PodFitsHost:       如果pod指定了NodeName, 检查节点名称是否和NodeName匹配
	PodFitsHostPorts:  节点上使用的port是否和pod申请打的port冲突
	PodSelectorMatches: 过滤掉和pod指定的label不匹配的点
	NoDiskConfict:      已经mount的volume 和 pod指定的volume不冲突，除非他们是只读
	
	如果没有合适的节点，pod会一直pending
	
priority优先级：
	LeastRequestedPriority:     cpu和memory使用率来决定权重, 使用率越低，权重越高
	BalancedResourceAllocation: cpu和memory使用率越接近，权重越高， 通常和上面一起使用
	ImageLocalityPriority:      倾向于已经要使用的镜像的大小，大小越大，权重越高
	
自定义调度器：
	spec.schedulername 来指定名字, 而不是默认的default-scheduler
```



### 7.2 亲和性

```
# node亲和性
    pod.spec.nodeAffinity:
        preferredDuringSchedulingIgnoredDuringExecution: 软亲和, 可以指定权重, 权重大的先运行
        requiredDuringSchedulingIgnoredDuringExecution : 硬亲和, 满足运行，不满足不运行

        
        键值关系：
            In 
            NotIn
            Gt
            Lt
            Exists
            DoesNotExists


可单独使用也可合并使用
# 注意：value中的值要 和 机器的hostname一致
# vim node-affinity.yaml
apiVersion: v1
kind: Pod
metadata:
  name: node-affinity-pod
  namespace: default
  labels:
    app: node-affinity-pod
spec:
  containers:
    - name: node-affinity-container
      image: hub.atguigu.com/library/nginx:v1
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
          - matchExpressions:
              - key: kubernetes.io/hostname
                operator: NotIn
                values:
                  - node2

---
apiVersion: v1
kind: Pod
metadata:
  name: node-affinity-pod
  namespace: default
  labels:
    app: node-affinity-pod
spec:
  containers:
    - name: node-affinity-container
      image: hub.atguigu.com/library/nginx:v1
  affinity:
    nodeAffinity:
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 1
        preference:
          matchExpressions:
          - key: kubernetes.io/hostname
            operator: In
            values:
              - node2

---
apiVersion: v1
kind: Pod
metadata:
  name: node-affinity-pod
  namespace: default
  labels:
    app: node-affinity-pod
spec:
  containers:
    - name: node-affinity-container
      image: hub.atguigu.com/library/nginx:v1
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
          - matchExpressions:
              - key: kubernetes.io/hostname
                operator: NotIn
                values:
                  - node2

      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 1
        preference:
          matchExpressions:
          - key: kubernetes.io/hostname
            operator: In
            values:
              - node2


# pod亲和性
    pod.spec.affinity.podAffinity/podAntiAffinity  
        preferred: 软亲和   可以，不是一定
        required:  硬亲和   一定

        可单独使用也可合并使用
        

# 需要先建立pod-01, pod-02 
# vim pod-affinity.yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-03
  namespace: default
  labels:
    app: pod-03
spec:
  containers:
    - name: node-affinity-container
      image: hub.atguigu.com/library/nginx:v1
  affinity:
    # 匹配pod, pod和指定pod在同一拓扑
    podAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
      - labelSelector:
          matchExpressions:
          - key: app
            operator: NotIn
            values:
              - pod-01
        topologyKey: kubernetes.io/hostname
    # 匹配pod, pod和指定pod不在同一拓扑
    podAntiAffinity:
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 1
        podAffinityTerm:
          topologyKey: kubernetes.io/hostname
          labelSelector:
            matchExpressions:
            - key: app
              operator: NotIn
              values:
                - pod-02

        
       	
kubectl get pod --show-labels

# nodeAffinity 和 podaffinity 和  podAntiAffinity 对比

    nodeAffinity 		匹配主机              In, NotIn, Exists, DoesNotExists, Gt, Lt
    podaffinity  		匹配pod, pod和指定pod在同一拓扑  In, NotIn, Exists, DoesNotExists
    podAntiAffinity 	匹配pod, pod和指定pod不在同一拓扑 In, NotIn, Exists, DoesNotExists

    kubectl create -f xxx.yaml && kubectl get pod -o wide -w && kubectl get pod --show-labels
```



### 7.3 污点和容忍

> 系统升级的时候可以打上污点，这样就不会被调度到该节点
>
> 	kubectl taint nodes node1 key1=value1:NoExecute
> 	    										
> 	kubectl taint nodes node1 key1=value1:NoExecute-
> 规则比较多

```
简介：
	和亲和性不一样的在于，taint 使节点能够排斥一类特定的pod

	taint 和 toleration 相互配合，可以用来避免pod被分配到不合适的节点上

    有污点，能容忍的，可能被分配到相应节点
    有污点，不能容忍，不可能被分配到相应节点

# 污点(taint)：
	污点的组成： key=value:effect ，其中value可以为空，effect描述污点的作用
	
 		effect 选项：
            NoSchedule:        不会将pod调度到该Node，master节点天生有污点
            PreferNoScheduler: 尽量避免将pod调度到该Node
            NoExecute:         不会将pod调度到该Node, 同时将node上已经存在的pod驱逐出去
            
        kubectl describe node k8s-master01   // 可以看到master的污点， taints: NoSchedule

    污点的设置，查看和除去：
        # 设置
        kubectl taint nodes node1 key1=value1:NoSchedule

        # 查看
        kubectl describe pod pod_name

        # 去除
        kubectl taint nodes node1 key1:NoSchedule-


	
# 容忍(toleration)：
	key, value, effect 要与Node上 taint 保持一致
	operator:           值为exists将会忽略value的值
	tolerationSeconds： 表示能容忍的时间
	
	example:
        pod.spec
            tolerations:
              - key: "key1"
                operator: "Exists"
                value: "value1"
                effect: "NoSchedule"
                tolerationSeconds: 3600
              - key: "key2"
                operator: "Equal"
                value: "value1"
                effect: "NoSchedule"
	
	不指定key时，   表示容忍所有的污点key    不是跟没指定一样
        tolerations:
          operator: "Exists"
	  
	不指定effect时，表示容忍所有的污点作用   不是跟没有指定一样
        tolerations:
          - key: "key"
            operator: "Exists"
	
	多个master存在时，防止资源竞争，可以做如下设置：
	kubectl taint nodes node_name node_role.kubernates.io/master=:PreferNoSchedule
	
	tips:
		# 维护时，将某个节点上打污点，维护完成再删除 
        kubectl taint nodes node1 key1=value1:NoExecute
        kubectl taint nodes node1 key1=value1:NoExecute-
        
        # 驱逐和禁用
        1. 设置节点不可调度, 新的不会被分配
        kubectl cordon k8s-node3
        kubectl get pods

        2. 驱逐已有的节点
        kubectl drain k8s-node3 --ignore-daemonsets

        3. 删除已有的节点
        kubectl delete node k8s-node3
```



### 7.4 固定节点

> nodeName
>
> nodeSelector

```
方式1：nodeName
pod.spec.nodeName:  将pod直接调度到node上, 跳过scheduler, 该规则是强制匹配
	spec:
	  nodeName: k8s-node01
	  
	  
# vim schedule-fix-node-nodename.yaml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: myweb
  labels:
    name: myweb
spec:
  replicas: 1
  template:
    metadata:
      labels:
        name: myweb
    spec:
      # 调度到指定节点， 注意节点名称
      nodeName: node1
      containers:
        - image: hub.atguigu.com/library/nginx:v1
          name: myweb

          ports:
            - containerPort: 80


方式二：nodeSelector
pod.spec.nodeSelector: 由k8s的label_selector机制选择节点, 改规则属于强制约束
      spec:
        nodeSelector:
          disk: ssd

# vim schedule-fix-node-nodeselector.yaml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: myweb1
  labels:
    name: myweb1
spec:
  replicas: 1
  template:
    metadata:
      labels:
        name: myweb1
    spec:
      # 调度到包含disk=ssd标签的节点
      nodeSelector:
        disk: ssd
      containers:
        - image: hub.atguigu.com/library/nginx:v1
          name: myweb1

          ports:
            - containerPort: 80


# kubectl label node k8s-node02 disk=ssd
kubectl label node node2 disk=ssd
```





## 8. 安全

```
 apiserver  集群内部各个组件通信的中介，也是外部控制的入口
 
 认证
 鉴权
 准入
```



### 8.1 认证

>  只有原理，没有示例， todo 
>
> 手动签发怎么签发？？？

```
http认证
1. http base
	用户名 + 密码
	Authorization: Basic xxx
	WWW-Authenticate： Basic realm="WallyWorld"
	Proxy_Authorization

2. http token
	digest   WWW-Authenticate: Digest realm="testrealm@host.com"   
	Bearer   WWW-Authenticate: Bearer realm="testrealm@host.com"
	oauth
	jwt

3. https
	ca证书认证
	
	双向认证
	
4. form  
	cookie, sesseion
	
安全性说明：
	controllerManager和scheduler 跟 apiserver在同一台机器上, 是内部访问，所以用本地回环，http即可
	kubectl, kube-proxy 和 kubelet 访问apiserver是远程访问， https访问
	
证书签发：
	手动：k8s集群和ca证书进行签发
	自动：首次访问api-server 的时候，签发token, 通过后，controllerManager会为kubelet生成一个证书，以后通过证书访问(kubeadm 自动签发)
	

kubeconfig:
	包含集群参数(api server地址， ca证书) ，客户端参数(证书和私钥)，集群context信息(集群名称，用户名)，k8s通过指定不同的kubeconfig可以切换到不同集群
	
	# cd ~/.kube 
	# cat config
	
serviceAccount:（sa）
	pod的创建和销毁是动态的，手动生成不可行，解决Pod访问api-server的认证问题
	
sa 和 secret 的关系：
	secret 包含 sa 和 保存用户自定义保密信息的opaque， dockerconfigjson
	sa:    
	   默认情况下每个namespace都会有serviceAccount, 默认目录 /var/run/secrets/kubernetes.io/serviceaccount
	   
		namespace（表示service-account-token的作用域空间）
		ca.crt    (客户端校验api-server发送的证书)
		token    （api server私钥签发的jwt, server端校验）
	
	
	kubectl exec `kubectl get pods -l run=nginx -o=name | cut -d "/" -f2` ls /run/secrets/kubernetes.io/serviceaccount
	
    kubectl get secret --all-namespaces 
    kubectl describe secret xxx --namespace=kube-system

***************************************************************************************
总结：
 k8s认证 --  pod -- sa -- sa token	    ------------------------------- api-server
		--	组件 /kubectl,kube-proxy  手动签发  -- 证书 -- kubeconfig------ api-server
				/ kubelet   tls	
		
 pod通过 secret 下的sa 拿到 token, 进而完成apiserver的认证
 
```

![](imgs\24-sa.png)





### 8.2 鉴权

#### 8.2.1  基本认识

```
api server授权策略：--authorization-mode
	AlwaysDeny:
	AlwaysAllow:
	ABAC:  基于属性
	RBAC:  基于角色  无需重启api-server
	Webhook: 外部的rest 服务对用户进行授权   

RBAC授权模式：
	1.5
	整个rbac完全用几个api对象完成，可以用api或者kubelet操作
	无需重启api server
	
RBAC资源对象：
    Role       (角色，它其实是一组规则，定义了一组对 Kubernetes API 对象的操作权限)
    RoleBinding(规则绑定)
    ClusterRole(类似group, 集群级别, 跨名称空间), 也可以对应RoleBinding
    ClusterRoleBinding(超管)
    
    都可以通过kubectl 与 api操作
    
    tips:
    
    k8s中并不提供用户管理，没有创建role的命令, 那么user, group, sa指定的用户从何而来，是在申请ca证书的时候定义的, 其中: 
        CN: "admin"	 
        "name":  [
               {
                "O": "system:masters"
               }
           ]	
         CN     对应 user
		name.O 对应 group
		
		k8s api server 会为token绑定一个默认的user和group, pod使用sa认证时，基于jwt的 sa token  就能保存到 user 信息，有了用户信息，再创建一对role, rolebinding等, 就可以完成权限绑定了
		
	 
	 总结： 先有用户，用户组，再去定义role, 最后 rolebinding  给某些用户，用户组，sa
```

![](imgs\25-role和rolebinding.png)





#### 8.2.2 Role

> tips:  定义通用的clusterRole,  绑定给roleBinding

```
role 和 clusterRole, 只能累加，不能修改
role可以定义在一个namespace中， 默认名称空间: default,  如果要跨名称空间 可以创建clusterRole

clusterRole:
	1. 集群级别的资源控制(例如访问node的能力)
	2. 非资源型的访问能力(例如：/healthz )
	3. 所有命名空间的访问能力，例如 pods
	
	tips:
		定义通用的clusterRole, 绑定给roleBinding

# role 
kind: Role
apiVersion: rbac.authorization.k8s.io/v1beta1
metadata:
  namespace: default
  name: pod-reader
rules:
  - apiGroups: [""]           # "" indicates the core api group
    resources: ["pods"]
    verbs: ["get", "watch", "list"]
	
	
# clusterRole
# 当前demo指定的是
kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1beta1
metadata:
  name: secret-reader
rules:
  - apiGroups: [""]           # "" indicates the core api group
    resources: ["secrets"]
    verbs: ["get", "watch", "list"]

```



#### 8.2.3 RoleBinding

```
rolebinding:
	rolebinding 包含一组权限列表，权限列表包含不同形式的待授予权限的资源，rolebinding适用于某个名称空间下的授权, rolebinding 可以使用clusterRole对某个namespace内的用户，用户组，sa 授权
	

clusterRoleBinding:
	clusterRoleBinding适用于 某个名称空间 下对clusterRole的授权
	
	
example:
# 将default命名空间的 pod-reader 这个role(上面有定义) 授权给用户jane
kind: RoleBinding
apiVersion: rbac.authorization.k8s.io/v1beta1
metadata:
  name: read-pods
  namespace: default

subjects:
  - kind: User
    name: jane
    apiGroup: rbac.authorization.k8s.io

roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io


# 将 dave 授权 具有 develoyment 名称空间下 secrets 的 "get", "watch", "list"访问权限
kind: RoleBinding
apiVersion: rbac.authorization.k8s.io/v1beta1
metadata:
  name: read-secret
  namespace: development

subjects:
  - kind: User
    name: dave
    apiGroup: rbac.authorization.k8s.io

roleRef:
  kind: ClusterRole
  name: secret-reader
  apiGroup: rbac.authorization.k8s.io
  
  




# manager 组里面的所有用户 对所有名称空间下(不是deployment，clusterrole 对 所用的名称空间有效)的 secret 具有访问权限

kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1beta1
metadata:
  name: read-secret-global
  namespace: deployment

subjects:
  - kind: Group
    name: manager
    apiGroup: rbac.authorization.k8s.io

roleRef:
  kind: ClusterRole
  name: secret-reader
  apiGroup: rbac.authorization.k8s.io
```



#### 8.2.4  resources

> 资源和非资源

```
GET /api/v1/namespaces/{namespace}/pod/{podname}/logs

子资源的访问通常用  /  

resources: ["pods/logs"]
resources: ["pods"]
resources: ["pod", "pods/logs"]
```



#### 8.2.5 subjects

> 使用者

```
subjects 包括： user, group, sa

users, group可以用字符串表示，也可以是... ,  但是前缀 system: 是系统保留的, 集群管理员应该确定普通用户不会使用这个前缀格式
```



#### 8.2.6 案例

```
创建一个用户只能管理dev空间

# 用户创建
useradd devuser
passwd devuser  // dev123456

开新的终端，devuser 连接 
192.168.66.10
devuser
dev123456

kubectl get pod   // 啥都没有

// 回到root
mkdir cert 
cd cert 

vim devuser-csr.json
{
  "CN": "devuser",
  "hosts": [],
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "name": [
    {
      "C": "CN",
      "ST": "shanghai",
      "L": "shanghai",
      "O": "k8s",
      "OU": "System"
    }
  ]
}

上传cfssl文件 到 /usr/local/bin/

chmod 777 /usr/local/bin/*

cd /etc/kubernetes/pki 

cfssl gencert -ca=ca.crt -ca-key=ca.key -profile=kubenetes /root/auth-yaml/cert/devuser-csr.json | cfssljson -bare devuser

ls 
"""
devuser.csr
devuser-key.pem
devuser.pem
"""

# 设置集群参数
export KUBE_APISERVER="https://192.168.66.10:6443"

kubectl config set-cluster kubernetes --certificate-authority=/etc/kubernetes/pki/ca.crt
--embed-certs=true --server=${KUBE_APISERVER} --kubeconfig=devuser.kubeconfig

# 设置客户端认证参数
kubectl config set-credentials devuser --client-certificate=/etc/kubernetes/pki/devuser.pem --client-key=/etc/kubernetes/pki/devuser-key.pem --embed-certs=true  --kubeconfig=devuser.kubeconfig

# 设置上下文参数
kubectl create namespace dev 

kubectl config set-context kubernetes --cluster=kubernetes --user=devuser --namespace=dev  --kubeconfig=devuser.kubeconfig

*********************************************************
# 很粗糙的创建了一个rolebinding, 实际可以定义yaml文件
kubectl create rolebinding devuser-admin-binding --clusterrole=admin --user=devuser --namespace=dev
*********************************************************

//在devuser登录的账号下
mkdir .kube


cp -f ./devuser.kubeconfig /home/devuser/.kube/
chown devuser:devuser /home/devuser/.kube/devuser.kubeconfig

# 设置默认上下文
# 在devuser中
cd .kube
mv devuser.kubeconfig  config     
kubectl config use-context kubernetes --kubeconfig=config


# 测试
//分别在devuser， root登录的账号下
kubectl get pod                // 不会报错

kubectl get pod -n default   // 报错
kubectl get pod -n dev      // 不会报错


cat devuser.kubeconfig
rm 
kubectl config set-cluster kubernetes --certificate-authority=/etc/kubernetes/pki/ca.crt


报错：
	1. 8080 refuse
    mv devuser.kubeconfig  config   
```



### 8.3 准入(***)

```
认证插件和授权插件完成身份认证和权限检查之后，准入控制器将拦截那些创建、更新和删除的相关操作请求以强制实现控制器中实现的功能。

通过插件来实现，不同插件，不同功能， 主要的功能是通过adminssion controller实现，比如: SA

推荐插件列表：
	namespaceLifecycle: 防止在不存在的namespace上创建资源，防止删除系统预置namespace
	limitRanger       : 确保请求的资源不会超过namespace limitranger规定的值
	serviceAccount    : 实现了自动化添加sa
	ResourceQuota     : 确保请求的资源不会操作resourceQuota 限制
	...
	
建议采用官方的准入控制
```


#### 8.3.1 资源限制(***)

> https://kubernetes.io/zh/docs/reference/access-authn-authz/admission-controllers/

```
*****************************************************************************************
// 资源限制-pod(可以二次更改limits中的值，没有设置的化，用默认的，要看limits在哪个命名空间)
防止oom

resources:
	requests要分配的资源
	limits是最高分配的值，可以理解为初始值和最大值

apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name:  my-name
  labels:
    name:  my-name
spec:
  template:
    metadata:
      labels:
        name:  my-name
    spec:
      containers:
      - image:  ipedrazas/docmock
        name:  my-name
        resources:
          limits:
            cpu: "4"
            memory: "10Gi"
          requests:
            cpu: "20m"
            memory: "55M"
            
// 资源限制-container(limitRange)
# 配置cpu和内存
## default         即为limit的值
## defaultRequest  即为request的值

kind: LimitRange
apiVersion: v1
metadata:
  name:  mem-limit-range
spec:
  limits:
    - type: Container
      default:
        memory: 50Gi
        cpu: 5
      defaultRequest:
        memory: 1Gi
        cpu: 1
        
  - type: Container       #限制的资源类型
    max:
      cpu: "2"            #限制单个容器的最大CPU
      memory: "2Gi"       #限制单个容器的最大内存
    min:
      cpu: "500m"         #限制单个容器的最小CPU
      memory: "512Mi"     #限制单个容器的最小内存
    default:
      cpu: "500m"         #默认单个容器的CPU限制
      memory: "512Mi"     #默认单个容器的内存限制
    defaultRequest:
      cpu: "500m"         #默认单个容器的CPU创建请求
      memory: "512Mi"     #默认单个容器的内存创建请求
    maxLimitRequestRatio:
      cpu: 2              #限制CPU limit/request比值最大为2
      memory: 2         #限制内存limit/request比值最大为1.5
      
  - type: Pod
    max:
      cpu: "4"            #限制单个Pod的最大CPU
      memory: "4Gi"       #限制单个Pod最大内存
      
  - type: PersistentVolumeClaim
    max:
      storage: 50Gi        #限制PVC最大的requests.storage
    min:
      storage: 30Gi        #限制PVC最小的requests.storage


// 资源限制-名称空间
用 ResourceQuota 限制命名空间中所有 Pod 的内存请求总量。 同样你也可以限制内存限制总量、CPU 请求总量、CPU 限制总量

除了可以管理命名空间资源使用的总和，如果你想限制单个 Pod，或者限制这些 Pod 中的容器资源， 可以使用 LimitRange 实现这类的功能。

1.计算资源配额限制
kind: ResourceQuota
apiVersion: v1
metadata:
  name:  compute-resource
  namespace: spark-cluster
spec:
  hard:
    pods: "20"
    requests.cpu: "20"
    requests.memory: 100Gi
    limits.cpu: "40"
    limits.memory: 200Gi

2.对象数量配额限制
kind: ResourceQuota
apiVersion: v1
metadata:
  name:  compute-resource
  namespace: spark-cluster
spec:
  hard:
    configmaps: "10"
    persistentvolumeclaims: "4"
    replicationcontrollers: "20"
    secrets: "10"
    services: "10"
    services.loadbalancers: "2"

```





## 9. helm

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



### 9.1 基础(***)

#### 9.1.1 基本概念

```
定义：包管理工具，不同yaml文件，更改属性，就可实现相应功能，通过打包的方式，支持发布的版本管理和控制，很大	程度上简化了k8s应用的管理和部署。比如：监控，日志

本质： 让K8s的应用管理可配置，动态生成(资源清单)

2个概念：
    chart：  应用信息的集合，包括配置模板, 配置参数, 依赖关系, 文档说明等
    release：chart运行实例, 代表一个运行的应用，chart能被多次安装到同一个集群，每次都是一个release

2个组件：
	helm client --- grpc ---> tiller服务器(默认在kube-system名称空间下) ---> kube api
```



#### 9.1.2 下载安装

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



#### 9.1.3 基本使用

> helm 仓库：  https://hub.helm.sh/

```
使用步骤： 
1.添加helm仓库 helm repo 
2.安装helm包   helm install

e.g.: 
helm install stable/xxx --version yyy
helm install stable/xxx --values values-prodution.yaml
```



#### 9.1.4 自定义模板

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




# 模板语法
https://www.cnblogs.com/klvchen/p/13606311.html
https://blog.csdn.net/winterfeng123/article/details/107843282
https://juejin.cn/post/6844904199818313735#heading-9

https://helm.sh/docs/chart_template_guide/function_list/         //官方文档中方法的完整列表
https://helm.sh/docs/chart_template_guide/builtin_objects/       //官方文档中方法的内置对象
https://helm.sh/docs/chart_template_guide/accessing_files/       // 文件相关的
https://github.com/Masterminds/sprig

Helm template由go template编写，所以我们先需要掌握gotemplate的基础语法


1. 横杠（-）表示去掉表达式输出结果前面和后面的空格，去掉前面空格可以这么写{{- 模版表达式 }}, 去掉后面空格 {{ 模版表达式 -}}

    # 去除test模版头部的第一个空行, 用于yaml文件前置空格的语法
    {{- template "test" }}
    

    # 这种方式定义的模版，会去除test模版头部和尾部所有的空行
    {{- define "test" -}}
    模版内容
    {{- end -}}

2. 变量和作用域，内置对象
	默认情况最左面的点( . ), 代表全局作用域，用于引用全局对象，中间的点，很像是js中对json对象中属性的引用方式。
	#这里引用了全局作用域下的Values对象中的key属性。 最左边的点就是全局，中间的点代表是从Values对象中取key属性。	
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
	定义：变量名以$开始命名， 赋值运算符是 := (冒号等号)，这是go语言中的赋值方式。
	{{- $relname := .Release.Name -}}
	
	引用:
	{{ $relname }}   // 不需要使用符号 . 来引用
	
3. 函数和管道运算符
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


4. 流程控制语句
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

	
5. 子模板
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

相同与不同点
1、本质上 template和include都是操作而不是函数，数据只是进行了内联插入这个操作。
2、无法将template调用的输出传递给其他函数。
3、include调用的输出可以通过管道符传递给其他函数。

结论：
	建议用 include
```



#### 9.1.5 常用命令

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



### 9.2 部署dashboard

```
# helm repo add k8s-dashboard https://kubernetes.github.io/dashboard
# helm install k8s-dashboard/kubernetes-dashboard --version 2.3.0 --name kubernetes-dashboard

helm repo update 
helm repo list
helm repo remove stable  /  xxx 
helm repo add stable https://kubernetes.oss-cn-hangzhou.aliyuncs.com/charts

helm search stable/kubernetes-dashboard
helm fetch  stable/kubernetes-dashboard      //为啥我的fetch没有作用 ？？？ 网络问题
tar -xvf kubernetes-dashboard-0.6.0.tgz

cd ./kubernetes-dashboard

# vim kubernetes-dashboard.yaml    //类似values.yaml文件
image:
  repository: registry.cn-hangzhou.aliyuncs.com/google_containers/kubernetes-dashboard-amd64
  tag: v1.8.3
ingress:
  enabled: true
  hosts:
    - k8s.frognew.com
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/backend-protocol: "HTTPS"
  tls:
    - secretname: frognew-com-tls-secret
      hosts:
        - k8s.frognew.com
rbac:
  clusterAdminRole: true


helm install stable/kubernetes-dashboard \
	-n kubernetes-dashboard \
	--namespace kube-system \
	-f kubernetes-dashboard.yaml
	
// 上面会用到dashborad镜像， 需要提前上传其他节点，docker load -i
// 以上这些，其实可以在template.yaml文件中提前 grep image， 然后docker pull ，load

kubectl get svc -n kube-system 

kubectl edit svc kubernetes-dashboard -n kube-system
// type: NodePort

kubectl get svc -n kube-system  

// 查看上面的端口， 浏览器访问， google会直接拦截，建议用火狐
https://192.168.66.10:31932

// kubeconfig 获取 token 登录
kubectl get secret -n kube-system | grep kubernetes-dashboard-token

kubectl describe secret -n kube-system  kubernetes-dashboard-token-xxx

// dashboard试用
尝试部署新的应用， (可能会有bug存在，建议通过命令行)
创建 --- 输入yaml文件内容，上传yaml文件，创建应用
```



### 9.3 部署metrics-server

> prometheus中已经集成了，这里不再单独部署

```
heapster 从1.12已经移除，现在推荐 metrics-server

# vim metrics-server.yaml
args:
  - --logtostderr
  - --kubelet-insecure-tls
  - --kubelet-prefferred-address-types-InternalIP
  
 
helm install  stable/metrics-server \
 -n metrics-server \
 --namespace kube-system \
 -f metrics-server.yaml
 
 
kubectl top node 
 
kubectl top node --all-namespaces
 
```



### 9.4 部署prometheus

#### 9.4.1 prometheus

```
//用下发的源码包，否则变化可能很大, release 0.1 /0.2
git clone https://github.com/coreos/kube-prometheus.git  

git clone https://github.com/AliyunContainerService/prometheus-operator



tar -xzf  kube-prometheus.tar.gz
cd /kube-prometheus/manifests


example:
spec:
  type: NodePort
  ports:  
  - name: http
    port: 80
    targetPort: 80
    nodePort: 30036
    protocol: TCP
    
    
# vim grafana-service.yaml 
spec:
  type: NodePort

  ports:
  	nodePort: 30200
  
# vim prometheus-service.yaml 
spec:
  type: NodePort
  
  ports:
  	nodePort: 30100
  	
# vim alertmanager-service.yaml
spec:
  type: NodePort
  
  ports:
  	nodePort: 30300

//下载解压，加载镜像, 并在每个节点上传镜像，加载镜像
tar -xzf prometheus.tar.gz
mv prometheus load-images.sh /root/
cd /root/
chmod a+x  load-images.sh
./load-images.sh 

scp -r load-images.sh prometheus root@192.168.66.20:/root/
scp -r load-images.sh prometheus root@192.168.66.21:/root/

// 其他节点
chmod a+x  load-images.sh
./load-images.sh 


kubectl create namespace monitoring

kubectl apply -f ../manifests/          //如果报错，可以多导入几次， 解决不了问题

报错：
"""
unable to recognize "manifests/alertmanager-alertmanager.yaml": no matches for kind "Alertmanager" in version "monitoring.coreos.com/v1"
unable to recognize "manifests/alertmanager-serviceMonitor.yaml": no matches for kind "ServiceMonitor" in version "monitoring.coreos.com/v1"
unable to recognize "manifests/grafana-serviceMonitor.yaml": no matches for kind "ServiceMonitor" in version "monitoring.coreos.com/v1"
unable to recognize "manifests/kube-state-metrics-serviceMonitor.yaml": no matches for kind "ServiceMonitor" in version "monitoring.coreos.com/v1"
unable to recognize "manifests/node-exporter-serviceMonitor.yaml": no matches for kind "ServiceMonitor" in version "monitoring.coreos.com/v1"
unable to recognize "manifests/prometheus-adapter-serviceMonitor.yaml": no matches for kind "ServiceMonitor" in version "monitoring.coreos.com/v1"
unable to recognize "manifests/prometheus-operator-serviceMonitor.yaml": no matches for kind "ServiceMonitor" in version "monitoring.coreos.com/v1"
unable to recognize "manifests/prometheus-prometheus.yaml": no matches for kind "Prometheus" in version "monitoring.coreos.com/v1"
unable to recognize "manifests/prometheus-rules.yaml": no matches for kind "PrometheusRule" in version "monitoring.coreos.com/v1"
unable to recognize "manifests/prometheus-serviceMonitor.yaml": no matches for kind "ServiceMonitor" in version "monitoring.coreos.com/v1"
unable to recognize "manifests/prometheus-serviceMonitorApiserver.yaml": no matches for kind "ServiceMonitor" in version "monitoring.coreos.com/v1"
unable to recognize "manifests/prometheus-serviceMonitorCoreDNS.yaml": no matches for kind "ServiceMonitor" in version "monitoring.coreos.com/v1"
unable to recognize "manifests/prometheus-serviceMonitorKubeControllerManager.yaml": no matches for kind "ServiceMonitor" in version "monitoring.coreos.com/v1"
unable to recognize "manifests/prometheus-serviceMonitorKubeScheduler.yaml": no matches for kind "ServiceMonitor" in version "monitoring.coreos.com/v1"
unable to recognize "manifests/prometheus-serviceMonitorKubelet.yaml": no matches for kind "ServiceMonitor" in version "monitoring.coreos.com/v1"

"""

解决：
  1. Pod 一直处于创建状态
  	kubectl describe pod xxx 
	grep image directxman12/k8s-prometheus-adapter:v0.7.0 ./*
	vim xxx 
	image quay.io/coreos/k8s-prometheus-adapter-amd64:v0.4.1
	
  2. xxx.yaml no matches for kind "ServiceMonitor" in version "monitoring.coreos.com/v1"
	 cat  alertmanager-alertmanager.yaml | grep apiVersion
	 
	 运行两次
	 
kubectl get pod -n monitoring   //看看服务是否起来没有

kubectl top node    			// 看看有灭有cpu, 内存啥的                

kubectl get svc --all-namespaces 

访问prometheus
192.168.66.10:30100

target
rules
service discory

sum by(pod_name)( rate(container_cpu_usage_seconds_total{image!="", pod_name!=""}[1m]) )


访问grafana:
192.168.66.10:30200
admin
admin

添加数据源
```



#### 9.4.2 hpa

```
*****************************************************************************************
// hpa
上传 hpa example , 该项目主要是通过占用资源来演示 hpa
docker load -i hpa-example.tar

// 通过kubectl run 创建一个deployment 进而创建pod
vim hpa.yaml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name:  php-apache
  labels:
    name:  php-apache
spec:
  template:
    metadata:
      labels:
        name:  php-apache
    spec:
      containers:
      - image:  gcr.io/google_containers/hpa-example:v1
        name:  php-apache
        ports:
        - containerPort:  80
        
# 正常情况下 run 创建的是一个 deployment, 
# kubectl run php-apache --image gcr.io/google_containers/hpa-example:v1 --requests=cpu=200m --expose --port=80    

kubectl create -f hpa.yaml

kubectl get pod 

kubectl autoscale deployment php-apache --cpu-percent=50 --min=1 --max=10

kubectl get hpa

// 一个不行，开两个
kubectl run -i --tty load-generator --image=busybox /bin/sh

while true; do echo ok-; done

kubectl get hpa  -w                     // 新窗口中
kubectl get pod	-w                     // 新窗口中
```






### 9.5 部署elk

>  oss 连接时不需要校验

```
 // 添加google 仓库
// helm repo add incubator http://storage.googleapis.com/kubernetes-charts-incubator

helm repo add incubator http://mirror.azure.cn/kubernetes/charts-incubator

helm repo list 
 
 // es
 kubectl create namespace efk
 helm fetch incubator/elasticsearch 
 
 tar 
 
 vim values.yaml 
 repository: "docker.elastic.co/elasticsearch/elasticsearch-oss"
 MINIMUM_MASTER_NODES: "1"
 replicas: 1               // 好几处
 
 master:
 	persistence:
 	  enabled: false
 
 
 helm install --name es1 --namespace=efk -f values.yaml incubator/elasticsearch
 
 kubectl get pod -n efk -o wide 
 
 kubectl run cirror-$RANDOM --rm -it --image=cirros -- /bin/sh
 	
 curl 10.98.224.240:9200/_cat/nodes
 	
 
 // fluentd
 helm  fetch stable-azure/fluentd-elasticsearch 
 
 kubectl get svc -n efk
 
vim values.yaml
 elasticsearch:
   host: "xxx"
   	

helm install --name fluentd1 --namespace=efk -f values.yaml stable-azure/fluentd-elasticsearch
 
 kubectl get pod -n efk
 
// kibana
helm search stable/kibana --version 0.14.0
helm fetch stable/kibana --version 0.14.0


helm fetch elastic/kibana --version 6.4.2

# docker pull docker.elastic.co/kibana/kibana-oss:6.4.2
# docker pull kibana:6.4.2
# 阿里云镜像仓库找到 registry.cn-hangzhou.aliyuncs.com/top_k8s/kibana-oss:6.4.2

# vim values.yaml
elasticsearch.url: http://xx:9200
elasticsearchURL: "http://10.99.156.8:9200"
image: registry.cn-hangzhou.aliyuncs.com/top_k8s/kibana-oss


# vim deployment.yaml 
注释掉readiness 相关的，否则无法启动，或者启动很慢

helm install --name kibana1 --namespace=efk -f values.yaml elastic/kibana --version 6.4.2
 
kubectl get svc -n efk 

kubectl get pod -n efk 

kubectl edit svc  kibana1-kibana -n efk
# type: NodePort

logstach-2020.08.06
timestamp

日志位置： /var/log/containers   (没有在哪里设置过这个地址，还是文件里默认就是这里？？？)


报错：
	1。It appears you're running the oss-only distribution of Elasticsearch.
	 To use the full set of free features in this distribution of Kibana, please update Elasticsearch to the default distribution. 
	
	Kibana 的版本号不能比 ElasticSerach 的版本号高，否则不支持。大版本号相同的情况下，中版本号可以比 ElasticSearch 低，但是会有警告。版本尽量保持一致即可避免这个问题。
```




## 10. 更改证书有效期

```
# 切换到kube证书目录
cd /etc/kubernetes/pki

# 查看有效期
openssl x509 -in apiserver.crt -text -noout 

validity:
	before:
	after:

# 查看kubeadm版本
kubeadm version 


目的：维持集群的最新更新策略
需求：更改kubaadm源码
// 安装go
wget https://studygolang.com/dl/golang/go1.14.6.linux-amd64.tar.gz

tar -xvf go1.14.6.linux-amd64.tar.gz -C /usr/local/

vim /etc/profile
export PATH=$PATH:/usr/local/go/bin

source /etc/profile

go version

// 配置go proxy
go env -w GO111MODULE=on
go env -w GOPROXY=https://goproxy.cn,direct


// 下载源码
git clone https://github.com/kubernetes/kubernetes.git
# 千万别使用下面的地址
# git clone --depth=1 https://github.com.cnpmjs.org/kubernetes/kubernetes.git
cd kubernetes
git checkout -b remotes/origin/release-1.15.1 v1.15.1

// 修改源码，更改时时间，编辑第591行
vim  ./cmd/kubeadm/app/util/pkiutil/pki_helpers.go +564

const duration365d = time.Hour * 24 * 365 * 10 
NotAfter: time.now().Add(duration365d)

# 方式一
# 先配置go proxy, 否则下载的很慢, 不推荐直接使用
# make WHAT=cmd/kubeadm GOFLASS=-v 
# cp _output/bin/kubeadm /root/kubeadm-new

# 方式二
# 拉取镜像
docker pull mirrorgooglecontainers/kube-cross:v1.12.10-1

#例如, 我的源代码放到了/root/kubernetes下
docker run --rm -it -v /root/kubernetes:/go/src/k8s.io/kubernetes \
mirrorgooglecontainers/kube-cross:v1.12.10-1 bash

# cd到容器内部的挂载路径，可以ls -al查看一下里面的文件是不是主机挂载目录的源码文件
cd /go/src/k8s.io/kubernetes

# 编译kubeadm, 这里主要编译kubeadm 即可
make all WHAT=cmd/kubeadm GOFLAGS=-v

# 编译完路径
路径./_output/local/bin/linux/amd64/kubeadm
#  /root/kubernetes/_output/local/bin/linux/amd64/kubeadm

# 退出容器

// 更新kubeadm
cp /usr/bin/kubeadm /usr/bin/kubeadm.bak
cp _output/local/bin/linux/amd64/kubeadm /usr/bin/kubeadm
chmod a+x /usr/bin/kubeadm

// 更新各节点证书至master节点
cp -r /etc/kubernetes/pki /etc/kubernetes/pki.old
cd /etc/kubernetes/pki
kubeadm alpha certs renew all --config=/root/kubeadm-config.yaml

// 查看证书有效期
openssl x509 -in apiserver.crt -text -noout | grep Not



// ha集群其余节点master证书更新
#!/bin/bash

masterNode="192.168.66.20 192.168.66.21"
for host in ${CONTROL_PLANE_IPS};
do 
	scp /etc/kubernetes/pki/{ca.crt,ca.key,sa.key,sa.pub,front-proxy-ca.crt,front-proxy-ca.key} "${USER}"@$HOST:/root/pki/
	
	scp /etc/kubernetes/pki/etcd/{ca.crt,ca.key} "root"@$HOST:/root/etcd/
	
	scp /etc/kubernetes/admin.conf "root"@$HOST:/root/kubernetes/
	
done
```





## 11. 高可用搭建

```
# 先创建一个目录，用来存放高可用集群搭建所需的各种文件
mkdir -p /usr/local/kubernetes/install

1. 设置hostname
# 每个主节点上都运行
hostnamectl set-hostname k8s-master01

2. 安装基本的环境
# 每个主节点上都运行
install_k8s_cluster.sh

# 升级内核后需要reboot 
# 查看内核是否更改过来
uname -r 


3. 关闭numa
# 每个主节点上都运行
# 关闭Numa后 reboot

cp /etc/default/grub{,.bak}
vim /etc/default/grub 
# 在 GRUB_CMDLINE_LINUX 最后添加 numa=off 

cp /boot/grub2/grub.cfg{,.bak}
grub2-mkconfig -o /boot/grub2/grub.cfg

reboot

4. kube-proxy开启ipvs的前置条件
# 每个主节点上都运行
prepare_kube_proxy.sh

5. 安装docker
# 每个主节点上都运行
install_docker4k8s.sh 

# 安装docker 过程中会更新 yum, 需要重新设置下内核并reboot 

grub2-set-default 'CentOS Linux (4.4.232-1.el7.elrepo.x86_64) 7 (Core)'

reboot 

uname -r


6. haproxy, keepalived
# 每个主节点上都运行，先在一个节点上执行成功后，将相关配置拷贝到其他节点上

tar -xvf kubeadm-basic.images.tar.gz

chmod 777 load_images.sh 

./load_images.sh


docker load -i haproxy.tar
docker load -i keepalived.tar

tar -xvf start.keep.tar.gz

mv data/  / 

cd /data/lb

vim etc/haproxy.cfg 
# 先只保留一个server
backend be_k8s_6443 
	server  xxx
	
vim start-haproxy.sh
MasterIP1=
MasterIP2=
MasterIP3=

./start-haproxy.sh 

netstat -anpt | grep :6444


vim start-keepalived.sh
vip 
interface  

./start-keepalived.sh

# ifconfig查看不到
ip addr


7. 安装kubeadm及初始化主节点
# 每个主节点上都要执行
install_kubeadm.sh

# kubeadm config print init-defaults > kubeadm-config.yaml

上传kubeadm-config.yaml, 并更改配置
loadAPIEndpoint:
  advertiseAddress: ip
	

controlPlaneEndpoint: "192.168.66.100:6444"
controllerManager:  xxx

# 第一个主节点运行
kubeadm init --config=kubeadm-config.yaml --experimental-upload-certs | tee kubeadm-init.log

执行安装日志中的命令， 比如 mkdir .kube  ...

# 前提： 192.168.66.100 能设置成功
# 其他两个主节点上执行 
kubeadm join 

执行安装日志中的命令， 比如 mkdir .kube 。。。


# init/join 报错, 文件已存在，端口占用
swapoff -a
kubeadm reset
rm -f $HOME/.kube/config
systemctl daemon-reload
systemctl restart kubelet
iptables -F && iptables -t nat -F && iptables -t mangle -F && iptables -X

端口占用解除
lsof -i :10250|grep -v "PID"|awk '{print "kill -9",$2}'|sh


tips:
	如果卡在join, 注意检查新节点的 /etc/kubernetes 下的内容， 最好从已有的节点上拷贝过来
admin.conf   pki



8. 修改haproxy.cfg 添加其他几个 server
docker rm -f HAProxy-K8S   && bash /data/lb/start-haproxy.sh

将配置信息拷贝到其他几个节点，执行相同的操作

9. 部署flannel
# 只要一个主节点上部署即可，部署完成，节点变成ready状态
kubectl get pod -n kube-system

kubectl get nodes

10. 更改vim /root/.kube/config 中server ip为机器ip 否则会卡死

11. etcd集群状态查看
kubectl get endpoint kube-controller-manager --namespace=kube-system -o yaml 

kubectl get endpoint kube-scheduler --namespace=kube-system -o yaml


kubectl -n kube-system exec etcd-k8s-master01 --etcdctl \ 
--endpoints=https://192.168.66.10:2379 \
--ca-file=/etc/kubernetes/pki/etcd/ca.cert \
--cert-file=/etc/kubernetes/pki/etcd/server.crt  \ 
--key-file=/etc/kubernetes/pki/etcd/server.key cluster-health
```



## 12. api接口

```
deprecate:
	https://blog.csdn.net/hxpjava1/article/details/79323236
	https://blog.csdn.net/xili2532/article/details/104562184
now:
	// 自己生成
	https://kubernetes.io/zh/docs/contribute/generate-ref-docs/kubernetes-api/  
	
	https://kubernetes.io/zh/docs/concepts/overview/kubernetes-api/
	https://www.cnblogs.com/faberbeta/p/13359813.html
	https://kubernetes.io/docs/reference/
	https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.18/#deployment-v1-apps
	
	// *****    go/python  sdk   important  *****
	
	kubectl explain pod.spec

    https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/

    https://kubernetes.io/zh/docs/concepts/workloads/pods/pod-lifecycle/
    
	https://github.com/kubernetes/client-go/
	https://github.com/kubernetes-client/python
	
	# 打不开解决方案 https://www.cnblogs.com/jeshy/p/12353188.html
	
	199.232.68.133 raw.githubusercontent.com
	
	
	
	https://github.com/kubernetes-client/python/blob/master/kubernetes/README.md
	
	https://raw.githubusercontent.com/kubernetes-client/python/master/kubernetes/client/api/core_v1_api.py
	
	
	# python文档搭建
	https://github.com/kubernetes-client/python/tree/master/doc
	
	
	##1. git clone 代码
	
	##2. pip install -r test_requirements.txt
	
	##3. make html 
	
	##4. vim nginx.conf 
	
	#user  nobody;
    worker_processes  1;
    
    events {
        worker_connections  1024;
    }
    
    
    http {
        include       mime.types;
        default_type  application/octet-stream;
    
        #log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
        #                  '$status $body_bytes_sent "$http_referer" '
        #                  '"$http_user_agent" "$http_x_forwarded_for"';
    
    
        sendfile        on;
    
        keepalive_timeout  65;
    
    
        server {
            listen       80;
            server_name  localhost;
    
            location / {
                root  /tmp/k8s-python/doc/build/html;
                index  index.html index.htm;
            }
    
    
            error_page   500 502 503 504  /50x.html;
            location = /50x.html {
                root   html;
             }
        }
    }

	##5. docker run -itd --name nginx-test -p 80:80 -v /tmp/nginx.conf:/etc/nginx/nginx.conf -v /tmp/k8s-python/doc/build/html:/tmp/k8s-python/doc/build/html  nginx
	
	##6. 访问
	
	

curl https://192.168.66.10:6443/api/v1/nodes \
    --cacert /etc/kubernetes/pki/ca.crt \
    --cert /etc/kubernetes/pki/apiserver-kubelet-client.crt \
    --key /etc/kubernetes/pki/apiserver-kubelet-client.key
    
    
    
    
# gitlab, harbor, helm, k8s 
## harbor
https://github.com/search?l=Python&q=harbor&type=Repositories

## gitlab
https://pypi.org/project/python-gitlab/
https://github.com/python-gitlab/python-gitlab


## helm
https://github.com/flaper87/pyhelm
https://github.com/andriisoldatenko/pyhelm#how-to-use-pyhelm

## k8s
https://github.com/kubernetes-client/python

https://github.com/kubernetes-client/python/blob/master/kubernetes/README.md

https://raw.githubusercontent.com/kubernetes-client/python/master/kubernetes/client/api/core_v1_api.py

```



## 13. 可视化

```
rancher 

openshift
```





## 14. 总结

```
Pod:
kubectl create -f xxx.yaml 
kubectl get pod [ -o wide -w ]   -o  yaml/json
kubectl logs myapp-pod  -c test    //指定pod名， 指定容器名

kubectl get pod -n kube-system
kubectl get pod --show-labels
kubectl describe pod xxx 

kubectl delete pod myapp-pod
kubectl delete depoyment xxx
kubectl delete pod --all
kubectl delete svc xxx xxx 

kubectl edit pod xxx 

rs:
kubectl label pod xxx tier=yyy --overwrite=True
kubectl label pod node01 app=node02 --overwrite=True

deployment:
kubectl create -f xxx --record

kubectl scale deployment xxx --replicas 3

kubectl autoscale deployment xxx --min=10 --max=15 --cpu-percent=80

kubectl set image deployment/nginx_deployment nginx=镜像地址:版本

kubectl rollout undo deployment/nginx_deployment

kubectl rollout undo deployment/nginx_deployment --to-revision=2

kubectl rollout status xxx
kubectl rollout history xxx
kubectl rollout pause 



kubectl get job/jobs

kubectl logs $pods
kubectl delete job /cronjob xxx
kubectl get crobjob 


kubectl delete -f xx.yaml


service:
kubectl get svc 


storage:
kubectl get pv 
kubectl get pvc 
kubectl get pod -w




kubectl get node 

kubectl exec xxx -c yyy -it -- /bin/sh
kubectl exec xxx -c yyy -it -- rm -rf /usr/share/nginx/html/index.html
kubectl exec `kubectl get pods -l name=configmap-hot-update -o=name | cut -d "/" -f2` -it  -- cat /etc/config/log_level



***********************************************************************************
vscode plugin： kubernetes support， kubernetes template

Harbor12345

hub.atguigu.com/library/nginx:v1
hub.atguigu.com/mysql/mysql:v1
hub.atguigu.com/library/nginx-ingress-controller:0.25.0

ntpdate ntp1.aliyun.com

tips:
	按住ctrl + backspace 可以删除
	
```



## 15. todo

```
1.apiversion的值 有规定么？

# kubelet 
在kubernetes集群中，每个Node节点都会启动kubelet进程，用来处理Master节点下发到本节点的任务，管理Pod和其中的容器。kubelet会在API Server上注册节点信息，定期向Master汇报节点资源使用情况，并通过cAdvisor监控容器和节点资源。可以把kubelet理解成【Server-Agent】架构中的agent，是Node上的pod管家。


2.service 中 ingress 和  flannel 的区别？？？
3.volume 和 pv 区别
4.pv和pvc区别？？？
```

