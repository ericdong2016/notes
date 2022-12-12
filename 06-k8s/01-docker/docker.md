## 01

### 1.架构图

![](imgs\001-docker架构图.png)



### 2.四大核心组件

```
container 
image 
network
volume
```



### 3.运行流程

>  docker registry:  docker仓库， 专门用于存储镜像环境的云服务环境
>
> docker hub 就是一个公有的存储镜像的地方，类似gitlab,  也可以搭建私库

![](imgs\002-docker组织图.png)



### 4.安装

```
#安装基本软件
$ sudo apt-get update
$ sudo apt-get install apt-transport-https ca-certificates curl software-
properties-common lrzsz -y

#使用阿里云的源{推荐}
$ sudo curl -fsSL https://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | sudo apt-
key add -
$ sudo add-apt-repository "deb [arch=amd64] https://mirrors.aliyun.com/docker-
ce/linux/ubuntu $(lsb_release -cs) stable"

#软件源升级
$ sudo apt-get update

#安装docker
$ sudo apt-get install docker-ce -y

# 可以指定版本安装docker：
# $ sudo apt-get install docker-ce=<VERSION> -y

#查看支持的docker版本
$ sudo apt-cache madison docker-ce

#测试docker
docker version
```



### 5.配置加速器

```
# vim /etc/docker/daemon.json
#docker cloud加速器的默认内容是少了一条配置，所以我们要编辑文件把后面的内容补全

{"registry-mirrors": ["http://e5d212cc.m.daocloud.io"], "insecure-registries": []}

# 重启docker
systemctl restart docker
```



### 6.启动和目录

```
# 命令
systemctl start/stop/status docker 

# 目录
/etc/docker/         #docker的认证目录
/var/lib/docker/     #docker的应用目录
```



### 7.docker执行加sudo

```
#如果还没有 docker group 就添加一个：
$ sudo groupadd docker

#将用户加入该 group 内。然后退出并重新登录就生效啦。
$ sudo gpasswd -a ${USER} docker

#重启 docker 服务
$ systemctl restart docker

#切换当前会话到新 group 或者重启 X 会话
#注意: 这一步必须的，否则因为 groups 命令获取到的是缓存的组信息，刚添加的组信息未能生效，
#所以 docker images 执行时同样有错。
$newgrp - docker
```



### 8.镜像

```
# 搜索镜像
docker search  xxx 

# 获取镜像
# 获取的镜像在哪里： /var/lib/docker   repositories.json中可以更改存放的位置
docker pull xxx 

# 查看镜像
docker image ls   / 镜像名称
docker images -a

# 镜像重命名（镜像名，tag变了，image_id没有变化）
docker tag   老的镜像名:版本号  新的镜像名:版本号

# 镜像删除
# 可以删除一个或者多个镜像
docker rmi [命令参数][镜像id]
docker rmi [命令参数][镜像名:tag]     # id一样，通过该方式
docker image rm [命令参数][镜像]

命令参数：
	-f     # 强制删除
	
e.g:
	docker rmi 3fa822599e10
	docker rmi mysql:latest
	docker rmi 3fa822599e10 3fa822599e11
	
# 导入和导出
docker save [命令参数][导出镜像名称][本地镜像镜像]

命令参数(OPTIONS)：
	-o, --output string  指定写入的文件名和路径
e.g:
	docker save -o nginx.tar nginx 
	
docker load < [被导入镜像压缩文件的名称]
e.g:
	docker load < nginx.tar
注意：
	如果导入的时候没有权限，需要通过chmod更改镜像的权限

# 查看镜像的详细信息
docker inspect [命令参数][镜像名称]:[镜像版本]
docker inspect [命令参数][镜像id]


# 了解
# 历史
docker history [镜像id]
docker history [镜像名称][镜像版本]

# 根据模板创建镜像
# https://download.openvz.org/template/precreated/
cat xxx | docker import - [自定义镜像名]

```



![](imgs\003-docker镜像.png)



### 9.容器

```
# 某种程度上是一个进程


# 查看容器
docker ps -a 
docker container ls -a 

# 创建待启动容器
docker create [options] image [容器内命令] [命令参数]

options；
	-t
	-i 
	--name 
	
容器内命令：
	ps, ls，/bin/sh  /bin/bash
命令参数：
	-a 
	
docker create -it --name nginx_v1 nginx ls -a 

#  启动容器
1. 待启动或者关闭
	docker start [options] [容器id]
	options:
		-a, --attach 将当前shell的 STDOUT/STDERR 连接到容器上
		-i, --interactive 将当前shell的 STDIN连接到容器上
		
	e.g.:
		docker start -a nginx_v1
		
2. 新建并启动
	docker run [命令参数] [镜像名称] [执行命令]
	命令参数：
		-t
		-d 
		-i
		--name 
		--rm   退出后删除容器
		
	e.g.:
		docker run -it --name nginx_v1 nginx /bin/bash    
		# docker run = docker create + docker start 
		
	
3. 守护进程启动docker 
	docker run -d ...
	
	
# 暂停和取消暂停，重启
docker pause 容器id
docker unpause 容器id

docker restart [options] 容器id    # 重启一个出于运行状态，暂停状态，关闭状态或新建状态的容器
options:
	-t  等待时间
e.g.:
	docker restart -t 120 xxx
	

# 关闭，终止，删除
docker stop 
docker kill 

删除：
1. 删除已关闭的
	docker rm 容器id 
2. 删除正在运行的
	docker rm -f 容器id
3. 删除全部的容器
	docker rm -f $(docker ps -a -q)



# 进入和退出
进入：
1. 创建容器并进入
	docker run -itd nginx /bin/bash 
2. 手工方式
	docker exec -it 容器id /bin/bash
3. 生产环境
vim docker_in.sh

#!/bin/bash
docker_in(){
 NAME_ID=$1
 PID=$(docker inspect --format {{.State.Pid}} $NAME_ID)
 nsenter --target $PID --mount --uts --ipc --net --pid
}
docker_in $1

chmod +x docker_in.sh         #执行可执行权限

./docker_in.sh b3fbcba852fd   #进入指定的容器，并测试

退出：
	#方法一：
		exit
	#方法二：
		Ctrl + D
		
tips:
	 sed -i 's/\r$//' docker_in.sh


# 日志
docker logs

# 查看详细信息中的网络信息
docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'
容器id

# 重命名
docker rename 

# 查看端口信息
docker port [容器id]

# 基于容器创建镜像  **********
方式一：
	docker commit -m '改动信息' -a "作者信息" [container_id][new_image:tag]
方式二：
	docker export [容器id] > 模板文件名.tar
	e.g.:
		#创建镜像:
        $ docker export ae63ab299a84 > nginx.tar
        #导入镜像:
        $ cat nginx.tar | docker import - panda-test
        
导出（export）导入（import）与保存（save）加载（load）的恩怨情仇
import与load的区别：
    import可以重新指定镜像的名字，docker load不可以
export 与 保存 save 的区别：
    1、export导出的镜像文件大小，小于save保存的镜像。
    2、export导出（import导入）是根据容器拿到的镜像，再导入时会丢失镜像所有的历史。
```



![](imgs\004-docker容器.png)



### 10.数据卷&数据卷容器&数据备份

> 数据卷和数据卷容器有什么区别？

```
# 数据需要持久化保存，数据和容器解耦
# 容器和宿主机中的目录可以同步

# 数据卷
docker run -itd --name nginx_v1 nginx -v [宿主机目录]:[容器目录]  [镜像名称]  

e.g.:  目录或者文件(不推荐)
	# 创建测试文件:
    $ echo "file1" > tmp/file1.txt
    
    #启动一个容器，挂载数据卷:
    #注意宿主机目录需要绝对路径
    $ docker run -itd --name test1 -v /home/itcast/tmp/:/test1/ nginx
    
    #测试效果
    $ docker exec -it a53c61c77 /bin/bash
    cat /test1/file1.txt
    file1
    

# 数据卷容器
需要在多个容器之间共享一些持续更新的数据，最简单的方式是使用数据卷容器。数据卷容器也是一个容器，但是它的目的是专门用来提供数据卷供其他容器挂载

数据卷容器就是为其他容器提供数据交互存储的容器

操作流程：
    1、创建数据卷容器
    	#命令格式：
        docker create -v [容器数据卷目录] --name [容器名字][镜像名称] [命令(可选)]
        
        #执行效果
        $ docker create -v /data --name v1-test1 nginx
        
    2、其他容器挂载数据卷容器
    	#命令格式：
        docker run --volumes-from [数据卷容器id/name] -tid --name [容器名字][镜像名称] [命令(可
        选)]
	
        #创建 vc-test1 容器:
        docker run --volumes-from 4693558c49e8 -tid --name vc-test1 nginx /bin/bash
        
        #创建 vc-test2 容器:
        docker run --volumes-from 4693558c49e8 -tid --name vc-test2 nginx /bin/bash
    		
    3.确认卷容器共享
        #进入vc-test1，操作数据卷容器:
        :~$ docker exec -it vc-test1 /bin/bash
        root@c408f4f14786:/# ls /data/
        root@c408f4f14786:/# echo 'v-test1' > /data/v-test1.txt
        root@c408f4f14786:/# exit
        
        #进入vc-test2，确认数据卷:
        :~$ docker exec -it vc-test2 /bin/bash
        root@7448eee82ab0:/# echo 'v-test2' > /data/v-test2.txt
        root@7448eee82ab0:/# ls /data/
        v-test1.txt
        root@7448eee82ab0:/# exit
        
        #回到vc-test1进行验证
        :~$ docker exec -it vc-test1 /bin/bash
        root@c408f4f14786:/# ls /data/
        v-test1.txt v-test2.txt
        root@c408f4f14786:/# cat /data/v-test2.txt
        v-test2

    
# 数据备份
步骤：
1 创建一个数据卷容器及本地备份目录
2 挂载宿主机本地目录到容器指定目录作为备份数据卷
3 将数据卷容器的内容 备份到 数据卷容器的指定目录，后续会被映射到 宿主机本地目录
4 完成备份操作后销毁刚创建的容器

#命令格式：
$ docker run --rm --volumes-from [数据卷容器id/name] -v [宿主机目录]:[容器目录]  [镜像名称]  [备份命令]



#创建数据卷容器
docker create -v /data  --name c1  nginx 

#宿主机本地创建备份目录:
$ mkdir /backup

#备份数据:
$ docker run --rm --volumes-from c1 -v /backup/或者$(pwd):/tmp  nginx 
  tar zcPf /tmp/data.tar.gz /data

#验证操作:
$ ls /backup
$ tar -xvf /backup/data.tar.gz
$ cd /backup/data && cat xxx
```



## 02

### 端口映射

> 查看当前宿主机开放了哪些端口： netstat -tnulp

```
# 1.随机端口映射
docker run -d -P 镜像名

# 2.指定主机的随机端口映射
docker run -d -p ip::容器端口

# 3.指定单个端口
docker run -d -p [ip]:宿主机端口:容器端口

# 4.指定多个端口
docker run -d -p [ip]:宿主机端口:容器端口  -p [ip]:宿主机端口:容器端口 ...  镜像名称
```



### 网络管理

#### 基本命令

```
docker network help 

docker network ls 
docker network inspect bridge 
docker inspect xxx
docker port 容器id
```



#### 网络模式

```
从1.7.0 将网络和存储剥离出来，以插件化的形式提供， 其中网络插件叫 libnetwork  

bridge: 	简单来说：就是穿马甲，打着宿主机的旗号，做自己的事情。 Docker的默认模式，它会在docker容
器启动时候，自动配置好自己的网络信息，同一宿主机的所有容器都在一个网络下，彼此间可以通信。类似于我们
vmware虚拟机的桥接模式。 利用宿主机的网卡进行通信，因为涉及到网络转换，所以会造成资源消耗，网络效率
会低

host： 		简单来说，就是鸠占鹊巢，用着宿主机的东西，干自己的事情。容器使用宿主机的ip地址进行通信。
特点：容器和宿主机共享网络

container：  新创建的容器间使用，使用已创建的容器网络，类似一个局域网。 特点：容器和容器共享网络

none： 		这种模式最纯粹，不会帮你做任何网络的配置，可以最大限度的定制化。 不提供网络服务，容器启动
后无网络连接

overlay：	容器彼此不再同一网络，而且能互相通行
```



#### 定制bridge 一

```
# 创建网络
docker network create --driver [网络类型] [网络名称]

docker network ls
docker network inspect 网络名称
ifconfig


# 自定义网段和网关
docker network create --driver [网络类型] [网络名称]  --gateway  xxx --subway xxx 

e.g.:
	docker network create --driver bridge --gateway 172.99.0.1 --subnet
172.99.0.0/16 bridge-test1


# 在自定义网络中启动容器
docker run -itd  --net=网络名称 --name 容器名 镜像名

# 连接容器和网络
docker network connect 网络名  容器名

# 断开网络 
docker network disconnect 网络名 容器名
```



#### 定制bridge 二

```
## 需求: 定制docker网桥
他是一种设备，根据设备的物理地址来划分网段，并传输数据的，docker0就是默认的网桥， 接下来我们自己定义一个br0网桥，然后启动的容器就用这个

## bridge-utils介绍
1、安装bridge-utils，利用brcrl创建网桥 
2、
配置/etc/default/docker文件 
编辑systemctl的配置文件使用该docker文件 
重载systemctl配置 
重启docker 
3、测试, 创建容器，查看容器信息即可

## 准备工作
sudo apt-get install bridge-utils -y

brctl show 

## 创建网桥
sudo brctl addbr br0
brctl show 

## 给网桥设置网段
sudo ifconfig br0 192.168.99.1 netmask 255.255.255.0
ifconfig

## docker配置网桥
  #配置docker文件
  sudo vim /etc/default/docker
  
  #最末尾添加
  DOCKER_OPTS="-b=br0"

## systemctl使用docker文件
    #创建服务依赖文件
    sudo mkdir -p /etc/systemd/system/docker.service.d
    sudo vim /etc/systemd/system/docker.service.d/Using_Environment_File.conf

    [Service]
    EnvironmentFile=-/etc/default/docker
    ExecStart=
    ExecStart=/usr/bin/dockerd -H fd:// $DOCKER_OPTS

    #重载服务配置文件
    systemctl daemon-reload
 
## 重启docker
    #重启前效果
    :~$ ps aux |grep docker
    root    32949  0.1  1.4 783160 59632 ?    Ssl  2月24  1:01 /usr/bin/dockerd -
    H fd://

    #重启
    :~$ systemctl restart docker

    #重启后效果
    :~$ ps aux |grep docker
    root  45737 4.3  1.2 527600 50572 ? Ssl 09:32 0:00 /usr/bin/dockerd -H fd:// -
    b=br0

## 测试

```



### host模式

```
# 容器使用宿主机 ip 
# 使用场景;
host模型比较适合于，一台宿主机跑一个固定的容器，比较稳定，或者一个宿主机跑多个占用不同端
口的应用的场景，他的网络性能是很高的。 host模型启动的容器不会有任何地址，他其实是使用了宿主机的所有
信息

docker run --net=host -itd --name nginx_v1 nginx 

docker network inspect xx 
docker inspect xx 
netstat -tnulp
```



### none模式

#### 简单使用

```
docker run --net=none -itd --name nginx_v1 nginx 
```



#### 自定义网络

```
# 需求：为了使本地网络和Docker容器更方便的通信(实现宿主机和容器的通信)，我们经常会有将Docker容器配置到和主机同一网段，而且还要指定容器的ip地址（pipwork工具实现定制docker容器ip地址）

#1、网络环境部署
#1.1 网卡环境部署
    #1.1.1 网桥软件部署
        sudo apt-get install bridge-utils -y
        brctl show 

    #1.1.2 桥接网卡配置
        #编辑网卡信息编辑Ubuntu的网卡信息文件
        #对源文件进行备份
        sudo cp /etc/network/interfaces /etc/network/interfaces-old
        sudo vim /etc/network/interfaces

        #与源文件内容进行1行的空行
        auto br0
        iface br0 inet static
        address 192.168.110.14
        netmask 255.255.255.0
        gateway 192.168.110.2
        dns-nameservers 192.168.110.2
        bridge_ports ens33

        #重启
        service networking restart

#1.2  docker服务配置
  #1.2.1 配置docker文件
 	sudo vim /etc/default/docker
    #最末尾添加
    DOCKER_OPTS="-b=br0"
 
  #1.2.2 systemctl使用docker文件
  #创建服务依赖文件
 	sudo mkdir -p /etc/systemd/system/docker.service.d
 	sudo vim /etc/systemd/system/docker.service.d/Using_Environment_File.conf
  #内容如下：
    [Service]
    EnvironmentFile=-/etc/default/docker
    ExecStart=
    ExecStart=/usr/bin/dockerd -H fd:// $DOCKER_OPTS
    
  #重载服务配置文件
 	systemctl daemon-reload
 	
  #1.2.3 重启docker 
  	# 第一次配置的时候需要重启linux虚拟机：reboot
  	systemctl restart docker
  	
    #注意查看网卡信息
     brctl show
     
     bridge   name  bridge id      STP enabled   interfaces
     br0         8000.000c2960060c  no       ens33
     docker0       8000.02427c11f899  no 

     br0    Link encap:以太网 硬件地址 00:0c:29:60:06:0c 
        inet 地址:192.168.110.14 广播:192.168.110.255 掩码:255.255.255.0
        inet6 地址: fe80::20c:29ff:fe60:60c/64 Scope:Link
        UP BROADCAST RUNNING MULTICAST MTU:1500 跃点数:1

     ens33   Link encap:以太网 硬件地址 00:0c:29:60:06:0c 
      UP BROADCAST RUNNING MULTICAST MTU:1500 跃点数:1
    #广播运行多播

    #验证dns解析是否正常
      ping www.baidu.com 

    #网络可能会没有dns解析所以我们需要进行dns的配置
    #16.04：
    sudo vim/etc/resolvconf/resolv.conf.d/base
    #18.04：
    sudo vim/etc/resolv.conf
    
    #增加内容
    nameserver 223.5.5.5
    nameserver 114.114.114.114
    nameserver 8.8.8.8

    #注意如果重启后网络并未生效则
    sudo /etc/init.d/networking restart
  
#1.3 容器创建
  #基于ubuntu镜像创建一个容器，网络模式使用none ，启动容器时,挂载本地Linux系统的etc/apt文件
 	docker run -itd --net=none --name ubuntu-test1 -v /etc/apt/:/home/etc 
ubuntu /bin/bash
 
 	docker ps
         CONTAINER ID IMAGE   COMMAND   CREATED       STATUS     PORTS
         NAMES
         5f7b976ddfdf ubuntu   "/bin/bash"  5 seconds ago    Up 4 seconds    
         ubuntu-test1
   
#2、定制容器ip
  #2.1 pipwork软件部署
      #安装pipwork
      #方法1：
        git clone https://github.com/jpetazzo/pipework

      #方法2：将软件直接拖入ubuntu虚拟机
        unzip pipework-master.zip
        sudo cp pipework-master/pipework /usr/local/bin/
 
  #2.2 定制容器ip
 	sudo pipework br0 ubuntu-test1 192.168.110.129/24@192.168.110.2
 
  #2.3 测试效果
  #进入容器查看ip地址信息
 	docker exec -it ubuntu-test1 /bin/bash
 
  #删除容器下的sources.lis
  	rm /etc/apt/sources.list
  #将本地sources.list 复制过来
 	cp /home/etc/sources.list /etc/apt/
  #进行软件源更新
 	apt-get update
  #安装ping命令
 	apt-get install inetutils-ping -y
  #安装ifconfig命令
 	apt-get install net-tools -y
  #宿主机ping命令测试
 	ping 192.168.110.14

```



#### 跨主机互联

> 优点： 配置简单，不依赖第三方软件 
> 缺点： 容器依赖于主机间的网络 容器与主机在同网段，注意ip地址分配 生产中不容易实现、不好管理
>
> 
>
> tips:
>
> 1.下面更改网段的方式是通过docker的配置文件，可也以通过usr/ lib/systemd/system/docker.service 更
>
> 2.容器和宿主机之间可以通过添加路由的方式实现互通：route add -net 192.168.x.x/24  gw ens33地址
>
> 
>
> 如何解决： 搭建dns 服务器， k8s ,  如果docker挂了，重启后ip如何分配

```
#1、ubuntu桥接网卡配置
  #1.1 软件安装
 	apt-get install bridge-utils -y
  #1.2 编辑网卡
    sudo vim /etc/network/interfaces
  #与文件源内容进行1行的空行
  #主机1
    auto br0
    iface br0 inet static
    address 192.168.110.14
    netmask 255.255.255.0
    gateway 192.168.110.2
    dns-nameservers 192.168.110.2
    bridge_ports ens33
    
  #主机2
     auto br0
     iface br0 inet static
     address 192.168.110.15
     netmask 255.255.255.0
     gateway 192.168.110.2
     dns-nameservers 192.168.110.2
     bridge_ports ens33
 
#2、docker配置网桥
  #2.1 配置docker文件
  #修改docker的守护进程文件
  vim /etc/default/docker
  #末尾添加:
  #主机1
  DOCKER_OPTS="-b=br0 --fixed-cidr=192.168.110.99/26"
  #主机2
  DOCKER_OPTS="-b=br0 --fixed-cidr=192.168.110.170/26"  
  #注释：
  #-b 用来指定容器连接的网桥名字
  #--fixed-cidr用来限定为容器分配的IP地址范围
  #192.168.110.99/26地址范围：192.168.110.64~192.168.110.127
  #192.168.110.170/26地址范围：192.168.110.128~192.168.110.191
  #网段的计算可以参考网址：http://help.bitscn.com/ip/


 #2.2 systemctl使用docker文件
 创建服务依赖文件
 	sudo mkdir -p /etc/systemd/system/docker.service.d
 	sudo vim /etc/systemd/system/docker.service.d/Using_Environment_File.conf
 内容如下：
    [Service]
    EnvironmentFile=-/etc/default/docker
    ExecStart=
    ExecStart=/usr/bin/dockerd -H fd:// $DOCKER_OPTS
  #重载服务配置文件
 	systemctl daemon-reload
  #2.3 重启主机
 	reboot
  #注意如果重启后网络并未生效则
  	sudo /etc/init.d/networking restart
  #注意查看网卡信息
 	brctl show

  #验证dns解析是否正常
     ping www.baidu.com
     
   #网络可能会没有dns解析所以我们需要进行dns的配置
    #16.04：
    	sudo vim/etc/resolvconf/resolv.conf.d/base
    #18.04：
    	sudo vim/etc/resolv.conf
    #增加内容
    nameserver 223.5.5.5
    nameserver 114.114.114.114
    nameserver 8.8.8.8
    #注意如果重启后网络并未生效则
      sudo /etc/init.d/networking restart
      
#3、容器测试
  #3.1 创建容器
  #主机1：
	docker run -itd --name ubuntu-test1 -v /etc/apt/:/home/etc ubuntu
/bin/bash
 	docker run -itd --name ubuntu-test2 -v /etc/apt/:/home/etc ubuntu
/bin/bash
  #主机2                                   
 	docker run -itd --name ubuntu-test3 -v /etc/apt/:/home/etc ubuntu
/bin/bash
 	docker run -itd --name ubuntu-test4 -v /etc/apt/:/home/etc ubuntu
/bin/bash
  #3.2 容器间测试
 	进入容器
   #主机1
 	docker exec -it ubuntu-test1 /bin/bash
 	docker exec -it ubuntu-test2 /bin/bash
  #主机2
 	docker exec -it ubuntu-test3 /bin/bash
 	docker exec -it ubuntu-test4 /bin/bash
 	
	rm /etc/apt/sources.list
    #容器内部将本地sources.list 复制过来
        cp /home/etc/sources.list /etc/apt/
    #容器内部进行软件源更新
    	apt-get update
    #容器内部安装ping命令
    	apt-get install inetutils-ping -y
    #容器内部安装ifconfig命令
    	apt-get install net-tools -y
    	
	#四个容器之间相互ping通
    宿主机ping命令测试
        ping 192.168.110.14
        ping 192.168.110.15
```



## 03

> 基于 ubuntu16_new



### 基本使用

> 命令越少，构建出来的通常越小  &&

```
vim Dockerfile
docker build -t 镜像名：版本号  目录
docker history 镜像id  				# 查看执行步骤, 优化 
docker inspect 镜像id  				# 查看镜像大小
```



### FROM

```
FROM
#格式：
 FROM <image>
 FROM <image>:<tag>
#解释：
  #FROM 是 Dockerfile 里的第一条而且只能是除了首行注释之外的第一条指令
  #可以有多个FROM语句，来创建多个image
  #FROM 后面是有效的镜像名称，如果该镜像没有在你的本地仓库，那么就会从远程仓库Pull取，如果远程也
没有，就报错失败
  #下面所有的 系统可执行指令 在 FROM 的镜像中执行。
```

### MAINTAINER

```
MAINTAINER
#格式：
 MAINTAINER <name>
#解释：
  #指定该dockerfile文件的维护者信息。类似我们在docker commit 时候使用-a参数指定的信息
```

### RUN

```
RUN
#格式：
 RUN <command>                  			(shell模式)
 RUN["executable", "param1", "param2"]      (exec 模式)
#解释：
  #表示当前镜像构建时候运行的命令，如果有确认输入的话，一定要在命令中添加 -y
  #如果命令较长，那么可以在命令结尾使用 \ 来换行
  #生产中，推荐使用上面数组的格式
#注释：
  #shell模式：类似于 /bin/bash -c  command
  #举例： RUN echo hello
  
  #exec模式：类似于 RUN["/bin/bash", "-c", "command"]
  #举例： RUN["echo", "hello"]
```



### EXPOSE

```
EXPOSE
#格式：
 EXPOSE <port> [<port>...]
#解释：
 设置Docker容器对外暴露的端口号，Docker为了安全，不会自动对外打开端口，如果需要外部提供访问，
 还需要启动容器时增加-p或者-P参数对容器的端口进行分配。
```

### CMD

```
CMD
#格式：
 CMD ["executable","param1","param2"]     (exec 模式)推荐
 CMD command param1 param2                (shell模式)
 CMD ["param1","param2"]                  提供给ENTRYPOINT的默认参数；
#解释：
  #CMD指定容器启动时默认执行的命令
  #每个Dockerfile只能有一条CMD命令，如果指定了多条，只有最后一条会被执行
  #如果你在启动容器的时候使用docker run 指定的运行命令，那么会覆盖CMD命令。
  #举例： CMD ["/usr/sbin/nginx","-g","daemon off；"]
  "/usr/sbin/nginx"  nginx命令
  "-g" 设置配置文件外的全局指令
  "daemon off；" 后台守护程序开启方式 关闭
  
  
# 示例
#修改Dockerfile文件内容：
  #在上一个Dockerfile文件内容基础上，末尾增加下面一句话：
 	CMD ["/usr/sbin/nginx","-g","daemon off;"]
  #构建镜像
 :~/docker/images/nginx$ docker build  -t ubuntu-nginx:v0.3 .

  #根据镜像创建容器,创建时候，不添加执行命令
 :~/docker/images/nginx$ docker run --name nginx-1 -itd ubuntu-nginx:v0.3
 
  #根据镜像创建容器,创建时候，添加执行命令/bin/bash
 :~/docker/images/nginx$ docker run  --name nginx-2 -itd ubuntu-nginx:v0.3
/bin/bash

 docker ps
 
  #发现两个容器的命令行是不一样的
 itcast@itcast-virtual-machine:~/docker/images/nginx$ docker ps -a
 CONTAINER ID IMAGE       COMMAND         CREATED      NAMES
 921d00c3689f ubuntu-nginx:v0.3 "/bin/bash"       5 seconds ago  nginx-
2
 e6c39be8e696 ubuntu-nginx:v0.3 "/usr/sbin/nginx -g …"  14 seconds ago  nginx-
1
```

### ENTRYPOINT

```
ENTRYPOINT
#格式：
 ENTRYPOINT ["executable", "param1","param2"] (exec 模式)
 ENTRYPOINT command param1 param2 (shell 模式)
#解释：
  #和CMD 类似都是配置容器启动后执行的命令，并且不会被docker run 提供的参数覆盖。
  #每个Dockerfile 中只能有一个ENTRYPOINT，当指定多个时，只有最后一个起效。
  #生产中我们可以同时使用ENTRYPOINT 和CMD，
  #想要在docker run 时被覆盖，可以使用"docker run --entrypoint"
 
#ENTRYPOINT指令实践：
  #修改Dockerfile文件内容：
  #在上一个Dockerfile 文件内容基础上，修改末尾的CMD 为ENTRYPOINT：
 ENTRYPOINT ["/usr/sbin/nginx","-g","daemon off;"]
 
  #构建镜像
 :~/docker/images/nginx$ docker build -t ubuntu-nginx:v0.4 .
 
  #根据镜像创建容器,创建时候，不添加执行命令
 :~/docker/images/nginx$ docker run  --name nginx-3 -itd ubuntu-nginx:v0.4
 
  #根据镜像创建容器,创建时候，添加执行命令/bin/bash
 :~/docker/images/nginx$ docker run  --name nginx-4 -itd ubuntu-nginx:v0.4
/bin/bash
 
  #查看ENTRYPOINT是否被覆盖
  :~/docker/images/nginx$ docker ps -a
 CONTAINER ID IMAGE        COMMAND         CREATED      
NAMES
 e7a2f0d0924e ubuntu-nginx:v0.4  "/usr/sbin/nginx -g …"  59 seconds ago   
nginx-4
 c92b2505e28e ubuntu-nginx:v0.4  "/usr/sbin/nginx -g …"  About a minute ago 
nginx-3
 
  #根据镜像创建容器,创建时候，使用--entrypoint参数，添加执行命令/bin/bash
 docker run  --entrypoint "/bin/bash" --name nginx-5 -itd ubuntu-nginx:v0.4
 
  #查看ENTRYPOINT是否被覆盖
 :~/docker/images/nginx$ docker ps
 CONTAINER ID IMAGE        COMMAND         CREATED      
NAMES
 6c54726b2d96 ubuntu-nginx:v0.4  "/bin/bash"        3 seconds ago   
nginx-5
 
```



### ADD

```
#ADD
#格式：
  ADD <src>... <dest>
  ADD ["<src>",... "<dest>"]
#解释：
  #将指定的<src> 文件复制到容器文件系统中的<dest>
  #src指的是宿主机，dest指的是容器
  #所有拷贝到container 中的文件和文件夹权限为0755, uid 和gid 为 0
  #如果文件是可识别的压缩格式，则docker 会帮忙解压缩
  #注意：
  #1、如果源路径是个文件，且目标路径是以/ 结尾， 则docker 会把目标路径当作一个目录，会把源文件
拷贝到该目录下;
	#如果目标路径不存在，则会自动创建目标路径。
  #2、如果源路径是个文件，且目标路径是不是以/ 结尾，则docker 会把目标路径当作一个文件。
      #如果目标路径不存在，会以目标路径为名创建一个文件，内容同源文件；
      #如果目标文件是个存在的文件，会用源文件覆盖它，当然只是内容覆盖，文件名还是目标文件名。
      #如果目标文件实际是个存在的目录，则会源文件拷贝到该目录下。注意，这种情况下，最好显示的以/ 结尾，以
    避免混淆。
  #3、如果源路径是个目录，且目标路径不存在，则docker 会自动以目标路径创建一个目录，把源路径目录
下的文件拷贝进来。
	#如果目标路径是个已经存在的目录，则docker 会把源路径目录下的文件拷贝到该目录下。
  #4、如果源文件是个压缩文件，则docker 会自动帮解压到指定的容器目录中。
 
#ADD实践：
  #拷贝普通文件
  	~/docker/images/nginx$ vim Dockerfile
 
  #Dockerfile文件内容
  # 构建一个基于ubuntu的docker定制镜像
  # 基础镜像
 FROM ubuntu
  # 镜像作者
 MAINTAINER panda kstwoak47@163.com
  # 执行命令
  ADD ["sources.list","/etc/apt/sources.list"]
 RUN apt-get clean
 RUN apt-get update
 RUN apt-get install nginx -y
  # 对外端口
 EXPOSE 80
 
  #构建镜像
 docker build -t ubuntu-nginx:v0.6 .
 
  #根据镜像创建容器,创建时候，不添加执行命令进入容器查看效果
 docker run  --name nginx-8 -it ubuntu-nginx:v0.6
 
  #拷贝压缩文件
 tar zcvf this.tar.gz ./*
 
  #Dockerfile文件内容
 ...
  # 执行命令
 ...
  # 增加文件
 ADD ["linshi.tar.gz","/nihao/"]


  #构建镜像
 :~/docker/images/nginx$ docker build -t ubuntu-nginx:v0.7 .
 
  #根据镜像创建容器,创建时候，不添加执行命令进入容器查看效果
  docker run --name nginx-9 -it ubuntu-nginx:v0.7
  
```

### COPY

```
#COPY
  #格式：
 COPY <src>... <dest>
 COPY ["<src>",... "<dest>"]
  #解释：
  #COPY 指令和ADD 指令功能和使用方式类似。只是COPY 指令不会做自动解压工作。
  #单纯复制文件场景，Docker 推荐使用COPY
#COPY实践
  #修改Dockerfile文件内容:
  # 构建一个基于ubuntu的docker定制镜像
  # 基础镜像
     FROM ubuntu
      # 镜像作者
     MAINTAINER panda kstwoak47@163.com
      # 执行命令
    ADD ["sources.list","/etc/apt/sources.list"]

    RUN apt-get clean
    RUN apt-get update
    RUN apt-get install nginx -y
    COPY ["index.html","/var/www/html/"]
    # 对外端口
    EXPOSE 80
    #运行时默认命令
    ENTRYPOINT ["/usr/sbin/nginx","-g","daemon off;"]
    
index.html 文件内容：
<h1>hello world </h1>
<h1>hello docker </h1>
<h1>hello nginx</h1>

#构建镜像
:~/docker/images/nginx$ docker build -t ubuntu-nginx:v0.8 .
#根据镜像创建容器,创建时候，不添加执行命令
:~/docker/images/nginx$ docker run  --name nginx-10 -itd ubuntu-nginx:v0.8
#查看nginx-10信息
:~/docker/images/nginx$docker inspect nginx-10
#浏览器访问nginx查看效果
```



### VOLUME

```
#VOLUME
  #格式：
 VOLUME ["/data"]
  #解释：
  #VOLUME 指令可以在镜像中创建挂载点，这样只要通过该镜像创建的容器都有了挂载点
  #通过VOLUME 指令创建的挂载点，无法指定主机上对应的目录，是自动生成的。
 
#VOLUME实践
#修改Dockerfile文件内容：
#将COPY替换成为VOLUME
:~/docker/images/nginx$vim Dockerfile
VOLUME ["/helloworld/"]
...
#构建镜像
:~/docker/images/nginx$docker build -t ubuntu-nginx:v0.9 .

#创建数据卷容器
:~/docker/images/nginx$docker run -itd --name nginx-11 ubuntu-nginx:v0.9
#查看镜像信息
:~/docker/images/nginx$docker inspect nginx-11
#验证操作
:~/docker/images/nginx$docker run -itd --name vc-nginx-1 --volumes-from nginx-11
nginx
:~/docker/images/nginx$docker run -itd --name vc-nginx-2 --volumes-from nginx-11
nginx
#进入容器1
:~/docker/images/nginx$docker exec -it vc-nginx-1 /bin/bash
:/# echo 'nihao itcast' > helloworld/nihao.txt
#进入容器2
:~/docker/images/nginx$ docker exec -it vc-nginx-2 /bin/bash
:/# cat helloworld/nihao.txt
```



### ENV

```
#ENV
#格式：
 ENV <key> <value>          （一次设置一个环节变量）
 ENV <key>=<value> ...      （一次设置一个或多个环节变量）
 
#解释：
#设置环境变量，可以在RUN 之前使用，然后RUN 命令时调用，容器启动时这些环境变量都会被指定

#ENV实践：
  #命令行创建ENV的容器
 	docker run -e NIHAO="helloworld" -itd --name ubuntu-111 ubuntu /bin/bash
 	
  #进入容器ubuntu-111
 	docker exec -it ubuntu-111 /bin/bash
 	echo $NIHAO
 
  #修改Dockerfile文件内容：
  #在上一个Dockerfile 文件内容基础上，在RUN 下面增加一个ENV
 	ENV NIHAO=helloworld
 
  #构建镜像
 	docker build -t ubuntu-nginx:v0.10 .
 
  #根据镜像创建容器,创建时候，不添加执行命令
 docker run  --name nginx-12 -itd ubuntu-nginx:v0.10
 docker exec -it nginx-12 /bin/bash
 echo $NIHAO

```



### WORKDIR

```
#WORKDIR
  #格式：
 WORKDIR /path/to/workdir (shell 模式)
  #解释：
  #切换目录，为后续的RUN、CMD、ENTRYPOINT 指令配置工作目录。相当于cd
  #可以多次切换(相当于cd 命令)，
  #也可以使用多个WORKDIR 指令，后续命令如果参数是相对路径，则会基于之前命令指定的路径。例如
  #举例：
 WORKDIR /a
 WORKDIR b
 WORKDIR c
 RUN pwd
 #则最终路径为/a/b/c
 
#WORKDIR实践：
#修改Dockerfile文件内容：
# 在上一个Dockerfile 文件内容基础上，在RUN 下面增加一个WORKDIR
 WORKDIR /nihao/itcast/
 RUN ["touch","itcast1.txt"]
 WORKDIR /nihao
 RUN ["touch","itcast2.txt"]
 WORKDIR itcast
 RUN ["touch","itcast3.txt"]
 ...
  #构建镜像
 :~/docker/images/nginx$ docker build -t ubuntu-nginx:v0.11 .
 
  #根据镜像创建容器,创建时候，不添加执行命令
 docker run  --name nginx-13 -itd ubuntu-nginx:v0.11
 
  #进入镜像
 docker exec -it nginx-13 /bin/bash
```



### 构建缓存

```
#取消缓存：
docker build --no-cache -t [镜像名]:[镜像版本][Dockerfile位置]
```



### Dockerfile构建beego

```
# 构建一个基于ubuntu 的docker 定制镜像
# 基础镜像
FROM ubuntu

# 镜像作者
MAINTAINER panda kstwoak47@163.com

# 增加国内源
#COPY sources.list /etc/apt/
RUN sed -i 's/archive.ubuntu.com/mirrors.ustc.edu.cn/g' /etc/apt/sources.list
RUN sed -i 's/security.ubuntu.com/mirrors.ustc.edu.cn/g' /etc/apt/sources.list

# 执行命令
RUN apt-get update
RUN apt-get install gcc libc6-dev git lrzsz -y

#将go复制解压到容器中
ADD go1.10.linux-amd64.tar.gz /usr/local/

# 定制环境变量
ENV GOROOT=/usr/local/go        
ENV PATH=$PATH:/usr/local/go/bin 
ENV GOPATH=/root/go
ENV PATH=$GOPATH/bin/:$PATH

# 下载项目
# 该命令可能比较慢，可以下载安装包，用add命令 解压
RUN go get github.com/astaxie/beego

# 增加文件
COPY test.go /root/go/src/myTest/

# 定制工作目录
WORKDIR /root/go/src/myTest/

# 对外端口
EXPOSE 8080

# 运行项目
ENTRYPOINT ["go","run","test.go"]

#把sources.list和test.go文件放到这个目录中
#构建镜像
docker build -t go-test:v0.1 .

#运行镜像
docker run -p 8080:8080 -itd go-test:v0.1
#访问镜像，查看效果
```



### docker-compose

> image 和 depends-on 中 depends-on 可以去掉么？

```
文档： https://docs.docker.com/compose/
单机版： docker-compose
集群版： docker-swam  mesos  k8s

# docker-compose基本使用
# vim docker-compose.yml

version: '2'
services:
web1:
 image: nginx
 ports:
  - "9999:80"
 container_name: nginx-web1
web2:
 image: nginx
 ports:
  - "8888:80"
 container_name: nginx-web2
 
 
# compose常见属性
#镜像：
 格式：
   image: 镜像名称:版本号
 举例：
   image: nginx:latest
   
#容器命名：
 格式：
   container_name: 自定义容器命名
 举例：
   container_name: nginx-web1
  
#端口：
 格式：
   ports:
     - "宿主机端口:容器端口"
 举例：
   ports:
     - "9999:80"
     
#镜像构建：
 格式：
   build: Dockerfile 的路径
 举例：
   build: .
   build: ./dockerfile_dir/
   build: /root/dockerfile_dir/
   
#数据卷：
 格式：
   volumes:
     - 宿主机文件:容器文件
 举例：
   volumes:
     - ./linshi.conf:/nihao/haha.sh
     
# 网络：
network:
  web:
  	driver: "bridge"
  	
  
...
network:
  - web 
...
  	  
  	  
   
#镜像依赖：
 格式：
   depends_on:
     - 本镜像依赖于哪个服务
 举例：
   depends_on:
     - web1   
 
 
 
 
# docker-compose 常用命令
#后台启动：
docker-compose up -d

#注意：
  #如果不加-d，那么界面就会卡在前台
  
#查看运行效果
docker-compose ps

#删除服务
docker-compose down


#启动一个服务
docker-compose start <服务名>
#注意：
  #如果后面不加服务名，会启动所有的服务
  
#停止一个服务
docker-compose stop <服务名>
#注意：
  #如果后面不加服务名，会停止所有的服务
  
#删除服务
docker-compose rm
#注意：
  #这个docker-compose rm不会删除应用的网络和数据卷。工作中尽量不要用rm进行删除

#查看服务运行的日志
docker-compose logs -f
#注意：
  #加上-f 选项，可以持续跟踪服务产生的日志
  
#查看服务依赖的镜像
docke-compose images

#进入服务容器
docker-compose exec <服务名> <执行命令>

#查看服务网络
docker network ls



# 示例
version: '2'
services:
web1:
 image: nginx
 ports:
  - "9999:80"
 volumes:
  - ./nginx/nginx-beego.conf:/etc/nginx/conf.d/default.conf
   #将配置文件映射到nginx的配置文件位置
 container_name: nginx-web1
go-base:
 build: ./go-base/
 image: go-base:v0.1
beego-web1:
 image: go-base:v0.1
 volumes:
  - ./beego1/test.go:/root/go/src/myTest/test.go
 ports:
  - "10086:8080"
 container_name: beego-web1
 depends_on:
 - go-base
beego-web2:
 image: go-base:v0.1
 volumes:
  - ./beego2/test.go:/root/go/src/myTest/test.go
 ports:
  - "10087:8080"
 container_name: beego-web2
 depends_on:
  - go-base


# 测试
#构建镜像
$docker-compose build

#启动任务
$docker-compose up -d

#查看效果
$docker-compose ps

#浏览器访问
192.168.110.5:9999
```



## 04 

### 1. 镜像分层原理

```
https://www.cnblogs.com/woshimrf/p/docker-container-lawyer.html

启动镜像的时候，一个新的可写层会加载到镜像的顶部。这一层通常称为“容器层”， 之下是“镜像层”。

容器层可以读写，容器所有发生文件变更写都发生在这一层。镜像层read-only,只允许读取。

由此可以看出，每个步骤都将创建一个imgid, 一直追溯到1e1148e4cc2c正好是我们的base镜像的id

copy-on-write (CoW) 的策略来保证base镜像的安全性，以及更高的性能和空间利用率


启动容器的时候，最上层容器层是可写层，之下的都是镜像层，只读层。

当容器需要读取文件的时候

从最上层镜像开始查找，往下找，找到文件后读取并放入内存，若已经在内存中了，直接使用。(即，同一台机器上运行的docker容器共享运行时相同的文件)。

当容器需要添加文件的时候

直接在最上面的容器层可写层添加文件，不会影响镜像层。

当容器需要修改文件的时候

从上往下层寻找文件，找到后，复制到容器可写层，然后，对容器来说，可以看到的是容器层的这个文件，看不到镜像层里的文件。容器在容器层修改这个文件。

当容器需要删除文件的时候

从上往下层寻找文件，找到后在容器中记录删除。即，并不会真正的删除文件，而是软删除。这将导致镜像体积只会增加，不会减少。

综上，Docker镜像通过分层实现了资源共享，通过copy-on-write实现了文件隔离。

对于文件只增加不减少问题，我们应当在同一层做增删操作，从而减少镜像体积
```

