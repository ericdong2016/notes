## 0. 准备

```
In the video, I said the exam is 3 hours. With the latest version of the exam, it is now only 2 hours. The contents of this course has been updated with the changes required for the latest version of the exam.

Below are some references:
Certified Kubernetes Administrator: https://www.cncf.io/certification/cka/
Exam Curriculum (Topics): https://github.com/cncf/curriculum
Candidate Handbook: https://www.cncf.io/certification/candidate-handbook
Exam Tips: http://training.linuxfoundation.org/go//Important-Tips-CKA-CKAD

Use the code - DEVOPS15 - while registering for the CKA or CKAD exams at Linux Foundation to get a 15% discount.


https://www.zhaohuabing.com/post/2022-02-08-how-to-prepare-cka/
```



## 1.  核心概念

> https://github.com/kodekloudhub/certified-kubernetes-administrator-course
>
> https://www.zhaohuabing.com/post/2022-02-08-how-to-prepare-cka/

### 1. master组件

```
etcd
scheduler
controller-manager: node-controller, replication-controller，。。。
apiserver
```



####  etcd

```
put key value 
get key
```





#### apiserver

```
作用:
1. 认证用户
2. 校验请求
3. 校验数据
4. 更新etcd
5. 调度
6. kubelet


cat /etc/kubernetes/manifests/kube-apiserver.yaml

cat /etc/systemd/system/kube-apiserver.service

ps -aux | grep kube-apiserver
```



#### controller-manager

```
1. watch status 
2. remediate situation

common controllers：
node
namespace
deployment
rc
rs
sa
pv
pvc
job
cronjob
stateful-set
daemonset



All controllers: 
attachdetach, bootstrapsigner, clusterrole-aggregation, cronjob, csrapproving,
csrcleaner, csrsigning, daemonset, deployment, disruption, endpoint, garbagecollector,
horizontalpodautoscaling, job, namespace, nodeipam, nodelifecycle, persistentvolume-binder,persistentvolume-expander, podgc, pv-protection, pvc-protection, replicaset, replicationcontroller,resourcequota, root-ca-cert-publisher, route, service, serviceaccount, serviceaccount-token, statefulset, tokencleaner, ttl


cat /etc/kubernetes/manifests/kube-controller-manager.yaml

cat /etc/systemd/system/kube-controller-manager.service

ps -aux | grep kube-controller-manager
```



#### scheduler

```
1. filter node
2. rank node
3. 资源请求和限制
4. 污点和容器
5. 节点选择和亲和度

cat /etc/kubernetes/manifests/kube-scheduler.yaml
ps -aux | grep kube-scheduler
```







### 2. worker组件

```
kubelet
kube-proxy
```



#### kubelet

```
1. 注册节点
2. 创建pod, 生命周期管理
```



#### kube-proxy

```
负载均衡
```









### 3. pod

```
node 下可以有多个pod
pod  下可以有多个container


kubectl run nginx --image nginx
kubectl get pods
```



### 4. yaml

```
apiVersion:
kind:
metadata:
  name:    xxx
  labels:
    app: xxx
    type: yyy
spec:
  containers:
  - name: nginx-container      // first item
    image: nginx


kind         version
Pod          v1
Service      v1
Replicaset   apps/v1
Deployment   apps/v1



kubectl get pods
kubectl describe pod my-app
```

### 5. 线上测试环境

```
Link: 
	https://kodekloud.com/courses/labs-certified-kubernetes-administrator-with-practice-tests/

先用邮箱注册
https://kodekloud.com/courses/labs-certified-kubernetes-administrator-with-practice-tests/?utm_source=udemy&utm_medium=labs&utm_campaign=kubernetes

然后点击右侧 enroll in this course, (Apply the coupon code)  udemystudent151113

练习:
	https://kodekloud.com/topic/practice-test-pods-2/
```



### 6. rs

#### 1. 基本概念

```
# rc.yaml
apiVersion: v1
kind: ReplicationController
metadata:
  name:   myapp-rc
  labels:
    app: myapp
    type: frontend
spec:
  template:
    metadata:
      name: myapp-rc
      labels:
        app: myapp
        type: frontend
    spec:
      containers:
      - name: nginx-container      // first item
        image: nginx
        
  replicas: 3
  
 

kubectl create -f rc.yaml
kubectl get rc
kubectl get pods



# rs.yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name:   myapp-rs
  labels:
    app: myapp
    type: frontend
spec:
  template:
    metadata:
      name:   myapp-rs
      labels:
        app: myapp
        type: frontend
    spec:
      containers:
      - name: nginx-container      // first item
        image: nginx
        
  replicas: 3
  selector:
    matchLabels:
      type: frontend
      
      
      
      
# label & selector

# scale
replicas: 6

kubectl replace -f rs-scale.yaml
kubectl scale --replicas=6 -f  rs-scale.yaml
kubectl scale --replicas=6  replicaset  myapp-replicaset   // type name
```

#### 2.  线上测试



#### 3. solution

```
题目是删除one of the four, 不要删除busybox rs, 否则后面就无法操作了

fix new-replica-set
	kubectl edit  rs xxx      --- busybox ---  删除原有的 kubectl delete pods -A 

Now scale the ReplicaSet up to 5 PODs.
	kubectl scale replicaset --replicaset=5 xxxrs
	
Now scale the ReplicaSet down to 2 PODs.
    kubectl scale replicaset --replicaset=2 xxxrs
    kubectl edit rs xxxrs
```



### 7. deployment

#### 1. 基本概念

```
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-rs
  labels:
    app: myapp
    type: frontend
spec:
  template:
    metadata:
      name: myapp-rs
      labels:
        app: myapp
        type: frontend
    spec:
      containers:
      - name: nginx-container      //first item
        image: nginx
        
  replicas: 3
  selector:
    matchLabels:
      type: frontend
      
kubectl get all
kubectl get deploy
kubectl get rs
kubectl get pods


Create an NGINX Pod
	kubectl run nginx --image=nginx

Generate POD Manifest YAML file (-o yaml). Don't create it(--dry-run)
	kubectl run nginx --image=nginx --dry-run=client -o yaml

Create a deployment
	kubectl create deployment nginx --image=nginx 

Generate Deployment YAML file (-o yaml). Don't create it(--dry-run)
	kubectl create deployment nginx --image=nginx  --dry-run=client -o yaml

Generate Deployment YAML file (-o yaml). Don't create it(--dry-run) with 4 Replicas (--replicas=4)
	kubectl create deployment --image=nginx nginx --dry-run=client -o yaml > nginx-deployment.yaml

Save it to a file, make necessary changes to the file (for example, adding more replicas) and then create the deployment.
	kubectl create -f nginx-deployment.yaml

OR

In k8s version 1.19+, we can specify the --replicas option to create a deployment with 4 replicas.

	kubectl create deployment  nginx --image=nginx  --replicas=4 --dry-run=client -o yaml > nginx-deployment.yaml
```

#### 2. 线上测试



#### 3. solution

```
最后一题：
	kubectl create deployment  httpd-frontend --image=httpd:2.4-alpine
	kubectl scale --replicaset=3 deployment httpd-frontend
	
	或者cp  现有yaml文件，改改也可以
```



### 8. namespace

#### 1. 基本概念

``` 
apiVersion: apps/v1
kind: Deployment
metadata:
  name:   myapp-rs
  namespace: dev
  labels:
    app: myapp
    type: frontend
spec:
  template:
    metadata:
      name:   myapp-rs
      labels:
        app: myapp
        type: frontend
    spec:
      containers:
      - name: nginx-container      // first item
        image: nginx
        
  replicas: 3
  selector:
    matchLabels:
      type: frontend
      
      
      
# namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: dev


kubectl create namespace dev

kubectl -n dev get pods
kubectl get pods -ns=dev
kubectl get pods --namespace=dev
kubectl config set-context  $(kubectl config current-context) --namespace=dev

kubectl get pods --all-namespace / -A




#resourceQuota
apiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-quote
  namespace: dev
  
spec:
  hard:
    pods: "10"
    requests.cpu: "4"
    requests.memory: 5Gi
    limit.cpu: "10"
    limit.memory: 10Gi
```



#### 2. 线上测试





#### 3. solution

```
kubectl get ns --no-headers | wc -l
kubectl -n research get pods --no-headers
kubectl run redis --image=redis --dry-run=client -o yaml > ns.yaml

kubectl get pods --all-namespace | grep blue

ping  www.baidu.com  80

# marking
db-service:3306

# dev
db-service.dev.svc.cluster.local
```



### 9. service

####  1. 基础知识

```
ClusterIP
NodePort
LoadBalance
ExternalName


# nodePort.yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  type: NodePort
  ports:
  - targetPort: 80
    port: 80
    nodePort: 30008
  selector:
  	app: myapp       // 通过selector 选择label, 同一label能负载均衡
  	type: frontend
  	
 
# clusterIp
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  type: ClusterIP
  ports:
  - targetPort: 80
    port: 80
  selector:
  	app: myapp        // 通过selector 选择label, 同一label能负载均衡
  	type: frontend
  	
  	
kubectl get svc


# loadBalance.yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  type: LoadBalance
  ports:
  - targetPort: 80
    port: 80 
    nodePort: 30008
    
http://example-1.com
http://example-2.com

cloud
```



#### 2. 线上实验





#### 3. solution

```
kubectl expose deployment simple-webapp-deployment --name=webapp-service --target-port=8080 --type=NodePort --port=8080 --dry-run=client -o yaml > svc.yaml
```





### 10. 声明式和命令式

#### 1. 基础知识

```
命令式：
	仅需一步就对集群做了修改
	
	kubectl run/expose/edit/scale/set image/    create/replace/delete -f  xxx.yaml
	
	kubectl replace --force -f xx.yaml
	
声明式：
	核心思想是apply命令使用的是patch API，该API可以认为是一种update操作，先计算patch请求，发送patch请求，操作的范围是object的指定字段而不是整个object
	 
	kubectl apply -f xx.yaml
	
	live object configuration
	
	annotations: kubectl.kubernetes.io/last-applied-configuration: {"apiversion": ...}
		
```

#### 2. 线上测试

```
多用--help

Create a pod called httpd using the image httpd:alpine in the default namespace. Next, create a service of type ClusterIP by the same name (httpd). The target port for the service should be 80.

Try to do this with as few steps as possible.

'httpd' pod created with the correct image?
'httpd' service is of type 'ClusterIP'?
'httpd' service uses correct target port 80?
'httpd' service exposes the 'httpd' pod?
```



#### 3. solution

```
kubectl edit pod httpd      run:httpd   app:httpd

kubectl run httpd --image=httpd:alpine --port 80 --expose  // 最快
```







## 2. scheduler

### 1. manual schedule

> 将pod绑定到固定node,  也称固定节点调度

```
# 方式一
apiVersion: v1
kind: Binding
metadata:
  name: nginx
target:
  apiVersion: v1
  kind: Node
  name: node02
  
  
# 方式二：
apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  nodeName: node01
  containers:
  - name: nginx
    image: nginx
```

线上测试

```
要等结果出来后，自己验证没有问题再点击check
```

solution

```

```



### 2. label&selector

**label & selector**

```
selector:
  matchLabels:
    app: monitoring-agent
    
template:
  metadata:
    labels:
      app: monitoring-agent
```

**线上测试**

```
kubectl get all --show-labels | grep "env=prod"

kubectl get pods -l env=dev --no-headers | wc -l
```

**solution**





### 3. taints & tolerations

```
# taints node
kubectl taint nodes node-name key=value:taint-effect（NoSchedule/PreferNoSchedule/NoExecute）

# tolerations pod
kubectl taint nodes node1 app=blue:NoSchedule


apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  containers:
  - name: nginx
    image: nginx
  tolerations:
  - key: app
    operator: "Equal"
    value: blue
    effect: NoSchedule
    
    
# taints effect
NoSchedule
PreferNoSchedule
NoExecute

master default NoSchedule

kubectl describe node master | grep taint
```

线上测试

```
kubectl get nodes 



kubectl taint node node01 spray=mortein:NoSchedule


kubectl run bee --image=nginx -o yaml > new.yaml
	  tolerations:
      - key: app
        operator: "Equal"
        value: blue
        effect: NoSchedule


kubectl explain pod.spec  
kubectl explain pod --recursive | less 
kubectl explain pod --recursive | grep -A5 	tolerations



10. Remove the taint on controlplane, which currently has the taint effect of NoSchedule.
kubectl taint node controlplane node-role.kubernetes.io/master:NoSchedule-
```

solution

```

```



### 4. node selector

```
apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  containers:
  - name: nginx
    image: nginx
  nodeSelector:
    size: large
    
    
kubectl label node node_name key=value
```



### 5. node affinity

```
apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  containers:
  - name: nginx
    image: nginx
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
      // preferredDuringSchedulingIgnoredDuringExecution
      // requiredDuringSchedulingRequiredDuringExecution
        nodeSelectorTerms:
        - matchExpressions:
          - key: size
            operator: NotIn/In/Exists(没有下面的values)
            values: 
            - Large
            - Medium
            
```



线上测试

```
Which nodes can the pods for the blue deployment be placed on?
Make sure to check taints on both nodes!
	answer:
	 	kubectl describe node controlplane | grep -i taint
	 	发现都没有taints
	 	
Set Node Affinity to the deployment to place the pods on node01 only.
	answer:
		kubectl create deployment blue --image=nginx --replicas=3 --dry-run=client  -o yaml > deploy.yaml


apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: blue
  name: blue
spec:
  replicas: 3
  selector:
    matchLabels:
      app: blue
  template:
    metadata:
      labels:
        app: blue
    spec:
      containers:
      - image: nginx
        name: nginx
        resources: {}
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
            - matchExpressions:
              - key: color
                operator: In
                values:
                - blue

kubectl get deployments.apps blue -o yaml > blue.yaml

vim blue.yaml
```



### 6. resource limits

```
apiVersion: apps/v1
kind: Pod
metadata:
  labels:
    app: blue
  name: blue
spec:
  containers:
  - image: nginx
    name: nginx
    resources:
      requests:
        memory: "1Gi/256Mi"
        cpu: 1/100m(0.1)
      limits:
        memory: "2Gi"
        cpu: 2
```



### 7.  daemonsets

```
kube-proxy
networking


apiVersion: apps/v1
kind: DaemonSet
metadata:
  labels:
    app: blue
  name: blue
spec:
  selector:
    matchLabels:
      app: blue
  template:
    metadata:
      labels:
        app: blue
    spec:
      containers:
      - image: nginx
        name: nginx
        
        
 kubectl get daemonset/ds
```



线上测试

```
1. kubectl -n kube-proxy get pods | grep proxy


2. kubectl create deployment elastic --image=xxx --namespace=xxx -o yaml> deploy.yaml

vim deploy.yaml   
	
	kind: DaemonSet
```



### 8. static pods

```
/etc/kubernetes/manifests

自动重启，无法删除，更新，只读

created by the kubelet
deploy control plane components as static pods
```



线上测试

```
How many static pods exist in this cluster in all namespaces?
ls /etc/kubernetes/manifests


2. 
kubernetes run static-busybox --image=busybox --dry-run=client -o yaml > busybox.yaml

// busybox.yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: static-busybox
  name: static-busybox
spec:
  containers:
  - image: busybox
    name: static-busybox
    command: ["bin/sh", "-c", "sleep 1000"]
    resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Always
status: {}

cp busybox.yaml /etc/kubernetes/manifests


3. 
kubectl get node node01 -o wide 
ssh node01

ps -ef | grep kubelet

grep -i static /var/lib/xxx


cd /etc/just
rm -f xxx.yaml
```



### 9. multi scheduler(todo)

```
apiVersion: v1
kind: Pod
metadata:
  labels:
    run: static-busybox
  name: my-scheduler
spec:
  containers:
  - image: busybox
    name: static-busybox
  - command:
    - kube-scheduler
    - --address=
    - --scheduler-name=my-custom-scheduler
    - --leader-elect=false

status: {}



# pod.yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: static-busybox
  name: static-busybox
spec:
  containers:
  - image: busybox
    name: static-busybox
  schedulerName: my-custom-scheduler
  
  
kubectl get events

kubectl logs my-custom-scheduler -n kube-system
```



线上测试

```
1. Deploy an additional scheduler to the cluster following the given specification.

Use the manifest file used by kubeadm tool. Use a different port than the one used by the current one.

    CheckCompleteIncomplete
    Namespace: kube-system
    Name: my-scheduler
    Status: Running
    Custom Scheduler Name
    
 answer:
 	未成功
 

```

### 10. config scheduler





## 3. logging&monitor



```
// 查看cpu, mem
kubectl top node/pod 


// 查看日志
kubectl logs -f xxpod1xx  xxxpod2xxx

kubectl logs -f  xxpodxx -c  container
```



## 4. lifecycle

### 1. update & rollback

```
kubectl rollout status/history   deployment/xx-deployment

replicas

kubectl set image deployment/myapp-deployment nginx=nginx:1.9.1

kubectl rollout undo deployment/xxx-deployment

kubectl get rs


strategy:
  type: Recreate / RollingUpdate
```

### 2. comands & arguments

```
apiVersion: v1
kind: Pod
metadata:
  labels:
    run: static-busybox
  name: static-busybox
spec:
  containers:
  - image: busybox
    name: static-busybox
    command:
    - "bin/sh"
    - "-c"
    - "sleep"
    args: ["1"]
```

线上测试

```
Create a pod with the given specifications. By default it displays a blue background. Set the given command line arguments to change it to green

CheckCompleteIncomplete
Pod Name: webapp-green
Image: kodekloud/webapp-color
Command line arguments: --color=green


args: ["--color=green"]
```





### 3. env 

```
# 使用一
env:
  - name: APP_COLOR
    value: pink

# 使用二， configmap
env:
  - name: APP_COLOR
    valueFrom:
      configMapKeyRef:
        xxx
        
# 使用三，secret
env:
  - name: APP_COLOR
    valueFrom: 
      secretKeyRef:
        xxx
```



### 4. configmap

```
// 声明式
apiVersion: v1
data:
  APP_COLOR: darkblue
kind: ConfigMap
metadata:
  name: webapp-config-map
  namespace: default
  

// 交互式
kubectl create cm xxx --from_literal=key=value
kubectl create cm xxx --from_file=app_config.properties


kubectl get cm 
kubectl describe cm



# 完整使用
       container:
         # 方式一
         env    <[]Object>
            name        <string>
            value       <string>
            valueFrom   <Object>
               configMapKeyRef  <Object>
                  key   <string>
                  name  <string>
                  optional      <boolean>
               fieldRef <Object>
                  apiVersion    <string>
                  fieldPath     <string>
               resourceFieldRef <Object>
                  containerName <string>
                  divisor       <string>
                  resource      <string>
               secretKeyRef     <Object>
                  key   <string>
                  name  <string>
                  optional      <boolean>
                  
         # 方式二       
         - envFrom        <[]Object>   前面的 - 如果检测过不了，往下移动去掉前面的 - 就好了
           - configMapRef        <Object>
               name     <string>
               optional <boolean>
           - secretRef   <Object>
               name     <string>
               optional <boolean>     
```



### 5. secrets

```
// 交互式
kubectl create secret generic xxx  --from-literal=key1=value1  --from-literal=key2=value2
kubectl create secret generic xxx --from_file = xxx

// 声明式
apiVersion: v1
kind: Secret
metadata:
  name:
data:
  xxx: hash  // echo -n "xx" | base64  [--decode]

kubectl get secret [xx -o yaml]
kubectl describe secret

// 使用
- envFrom       <[]Object>   前面的 - 如果检测过不了，往下移动去掉前面的 - 就好了
  - secretRef   <Object>
      name      <string>
  
env: 
- name        <string>
  valueFrom   <Object>
    secretKeyRef     <Object>
      key   <string>
      name  <string>
      
// volume
volumes:
- name: app-secret-volume
  secret:
    secretName: app-sec
```



### 6. multi container pods

```
apiVersion: v1
kind: Pod
metadata:
  labels:
    run: static-busybox
  name: static-busybox
spec:
  containers:
  - image: busybox
    name: static-busybox
    
  - image: xxx
    name: xxx1
```

### 7. init pod

```
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
  labels:
    app: myapp
spec:
  containers:
  - name: myapp-container
    image: busybox:1.28
    command: ['sh', '-c', 'echo The app is running! && sleep 3600']
  initContainers:
  - name: init-myservice
    image: busybox
    command: ['sh', '-c', 'git clone xx; done;']



If any of the initContainers fail to complete, Kubernetes restarts the Pod repeatedly until the Init Container succeeds.

apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
  labels:
    app: myapp
spec:
  containers:
  - name: myapp-container
    image: busybox:1.28
    command: ['sh', '-c', 'echo The app is running! && sleep 3600']
  initContainers:
  - name: init-myservice
    image: busybox:1.28
    command: ['sh', '-c', 'until nslookup myservice; do echo waiting for myservice; sleep 2; done;']
  - name: init-mydb
    image: busybox:1.28
    command: ['sh', '-c', 'until nslookup mydb; do echo waiting for mydb; sleep 2; done;']


```

线上测试

```
Edit the pod to add a sidecar container to send logs to Elastic Search. Mount the log volume to the sidecar container.

Only add a new container. Do not modify anything else. Use the spec provided below.

Name: app
Container Name: sidecar
Container Image: kodekloud/filebeat-configured
Volume Mount: log-volume
Mount Path: /var/log/event-simulator/

Existing Container Name: app
Existing Container Image: kodekloud/event-simulator



// 
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
  labels:
    app: myapp
spec:
  containers:
  - name: myapp-container
    image: busybox:1.28
    command: ['sh', '-c', 'echo The app is running! && sleep 3600']
    
  - image: kodekloud/filebeat-configured
    name: sidecar
    volumeMounts:
    - mountPath: /var/log/event-simulator/
      name: log-volume
```



## 5. cluster maintenance

### 1. os update

> https://v1-20.docs.kubernetes.io/zh/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/

```
// 驱逐
kubectl drain node-1
// 不可调度
kubectl cordon node-2
// 可调度
kubectl uncordon node-1


--------------------------
kubeadm upgrade plan
master:
kubectl cordon master
apt-mark unhold kubeadm && \
apt-get update && apt-get install -y kubeadm=1.20.0-00 && \
apt-mark hold kubeadm

kubeadm upgrade plan

kubeadm upgrade apply v1.20.0

 apt-mark unhold kubelet kubectl && \
  apt-get update && apt-get install -y kubelet=1.20.0-00 kubectl=1.20.0-00 && \
  apt-mark hold kubelet kubectl
  
sudo systemctl daemon-reload
sudo systemctl restart kubelet

kubectl uncordon master
kubectl get nodes




node:
kubectl drain node-1

apt-get upgrade -y kubeadm=1.20.0-00
kubeadm upgrade node config --kubelet-version v1.20.0
apt-get upgrade -y kubelet=1.20.0-00  kubectl=1.20.0-00
sudo systemctl daemon-reload
sudo systemctl restart kubelet
kubectl get nodes

kubectl uncordon node-1

--------------------------
kubectl drain node-2
。。。
kubectl uncordon node-2
--------------------------
kubectl drain node-3
。。。
kubectl uncordon node-3





// cannot delete Pods not managed by ReplicationController, ReplicaSet, Job, DaemonSet or StatefulSet (use --force to override): default/hr-app

 kubectl drain node01 --ignore-daemonsets --force
```



### 2. backup & restore（todo）

```
# backup
// resource configuration
kubectl get all --all-namespaces -o yaml > all.yaml

// etcd
kubectl describe pod -n kube-system | grep etcd 找到配置

ETCDCTL_API=3 etcdctl snapshot save snapshot.db --endpoints=https://127.0.0.1:2379 \
--cacert=/etc/kubernetes/pki/etcd/ca.crt \
--cert=/etc/kubernetes/pki/etcd/server.crt \
--key=/etc/kubernetes/pki/etcd/server.key

ETCDCTL_API=3 etcdctl \
snapshot status snapshot.db

// pv



# restore
// etcd 
service kube-apiserver stop

ETCDCTL_API=3 etcdctl \
snapshot restore snapshot.db --data-dir=/var/lib/etcd-from-backup

ls /var/lib/etcd-from-backup

cd /etc/kubernetes/manifests

vim etcd.yaml 
	volumes:
	- hostpath:
	    path: /var/lib/etcd-from-backup
	    type: xxx

systemctl daemon-reload
service etcd restart
 
service kube-apiserver start


kubectl get pods,deploy,svc
```



线上测试：

```
Where is the ETCD server certificate file located?
Note this path down as you will need to use it later

/etc/kubernetes/pki/server.crt
/etc/kubernetes/pki/etcd/peer.crt
/etc/kubernetes/pki/etcd/ca.crt
/etc/kubernetes/pki/etcd/server.crt    ****
```





## 6. security(todo)

### 1.  authentication

```
kubectl create user user1
kubectl list user

kubectl create sa sa1
kubectl get sa


// static password
command:
- kube-apiserver
- --basic-auth-file=

// static token
command:
- kube-apiserver
- --token-auth-file=
```

### 2. tls

```
ssh-keygen
cat ~/.ssh/authorized_keys

// tls in kubernetes
ca

server:
apiserver: apiserver.crt, apiserver.key  下面的都和apiserver打交道
etcd:      etcd.crt, etcd.key
kubelet:   kubelet.crt, kubelet.key

client:
kube-scheduler:  scheduler.key  scheduler.crt
kube-proxy
kube-controller-manager
admin



// ca
openssl genrsa  -out ca.key 2048      //设置密码  123456

openssl req -new -key ca.key -out ca.csr   //输入上面的密码，common Name: hub.atguigu.com, 最后一个提示改密码，直接回车


cp ca.key ca.key.org 
openssl rsa -in ca.key.org -out ca.key    //去掉密码，不然会失败(需要输入密码)

openssl x509 -req -in ca.csr -signkey ca.key -out ca.crt

// admin
openssl genrsa  -out admin.key 2048   
openssl req -new -key admin.key -subj "/CN=kube-admin" -out admin.csr 
openssl x509 -req -in admin.csr -CA ca.crt -CAkey ca.key -out admin.crt

...


curl https://kube-apiserver:6443/api/v1/pod --key admin.key -cert admin.crt --cacert ca.crt

clusters:
- cluster:
  	certificate-authority: ca.crt
  	server: https://kube-apiserver:6443
  
  name: kubernetes



// view ca details
cat /etc/systemd/system/kube-apiserver.service 
cat /etc/kubernetes/manifests/kube-apiserver.yaml

# apiserver

/etc/kubernetes/pki


openssl x509 -in /etc/kubernetes/pki/apiserver.crt -text -noout

	 Issuer: CN = etcd-ca
	 
     subject:
     
     Validity
     Not Before: Feb  4 15:07:34 2022 GMT
     Not After : Feb  4 15:07:34 2023 GMT
     
     X509v3 Subject Alternative Name: 
     DNS:controlplane, DNS:kubernetes, DNS:kubernetes.default, DNS:kubernetes.default.svc, DNS:kubernetes.default.svc.cluster.local, IP Address:10.96.0.1, IP Address:10.37.158.9

# inspect servive logs
journalctl -u etcd.service -l

# view logs
kubectl logs -f etcd

docker ps -a | grep api
docker logs xxx
```



### 3. certificates api(todo)

> https://kubernetes.io/zh/docs/reference/access-authn-authz/certificate-signing-requests/

```
openssl genrsa -out jane.key 2048

openssl req -new -key jane.key -subj "/CN=jane" -out jane.csr

cat jane.csr | base64



apiVersion: certificates.k8s.io/v1beta1
kind: CertificateSigningRequest
metadata:
  name: jane
spec:
  groups:
  - system:nodes
  - system:authenticated
  usages:
  - digital signature
  - key encipherment
  - client auth
  request:
    cat jane.csr | base64     // 此处要先在文本文件上手动处理下，否则会报错
    
    
kubectl get csr 

kubectl certificate approve jane

kubectl certificate deny  agent-smith

kubectl get csr jane -o yaml

cat /etc/kubernetes/manifests/kube-controller-manager.yaml 
    --cluster-signing-cert-file    = pki/ca.crt
    --cluster-signing-key-file     = pki/ca.key
```





### 4. kube config(todo)

> 

```
#HOME/.kube/config

curl https://xxx:6443/api/v1/pods --key=admin.key --cert admin.crt --cacert ca.crt

kubectl  get pods --server  --client-key --client-certificate --certificate-authority
=
kubectl get pods --kubeconfig config



apiVersion: v1
kind: Config
current-context: user@cluster

clusters:
- name: my-cluster
  cluster:
    certificate-authority-data: /etc/kubernetes/pki/ca.crt
    server:
    
   // cat ca.crt | base64
   // echo "" | base64 --decode

contexts:
- name: use@cluster
  context:
    cluster: my-cluster
    user: my-user
    namespace: xxx

users:
- name: my-user
  user:
    client-certificate-data: /etc/kubernetes/pki/user/xxx.crt
    client-key-data: /etc/kubernetes/pki/user/xxx.key
    

// 将集群详细信息添加到配置文件中：
kubectl config --kubeconfig=my-kube-config set-cluster test-cluster-1 --server=https://controlplane:6443 --certificate-authority=/etc/kubernetes/pki/ca.crt

// 
kubectl config --kubeconfig=my-kube-config set-credentials dev-user --client-certificate=fake-cert-file --client-key=fake-key-seefile


// 查看context
kubectl config view  --kubeconfig=my-config
// 改变context
kubectl config use-context 	prod-user@cluster

kubectl config -h
```

线上测试（todo）

```
1. I would like to use the dev-user to access test-cluster-1. Set the current context to the right one so I can do that.

Once the right context is identified, use the kubectl config use-context command.



2. We don't want to have to specify the kubeconfig file option on each command. Make the my-kube-config file the default kubeconfig.
CheckCompleteIncomplete
Default kubeconfig file configured


3. 
```



### 5. api groups(todo)

```
curl http://localhost:6433/api/v1/version
curl http://localhost:6443 -k  | grep "name"


core:
	api
	v1
namespace pods rc


named:
	              apis
/apps  /extensions /networking.k8s.io  /storage
v1
（resources） (verbs)
deployments   list
rs            get 
statefulsets  create


kubectl proxy
curl http://localhost:8001 -k
```



### 6. auth

**node**

```
kube api  --> kubelt 
              read 
              	services
              	endpoints
              	nodes
              	pods
              write
                node status
                pod  status
                events
```

**abac**

```

```

**rbac**

```
role     permission
```

**webhook**

```
user --> kube api --> open policy agent
```





```
cat /etc/kubenetes/manifests/kube-apiserver.yaml 

--authorization-mode=Node,RBAC【Webhook】




kubectl describe role kube-proxy -n kube-system

PolicyRule:
  Resources   Non-Resource URLs  Resource Names  Verbs
  ---------   -----------------  --------------  -----
  configmaps  []                 [kube-proxy]    [get]
  
  
1. Which account is the kube-proxy role assigned to it?
   kubectl get rolebindings.rbac.authorization.k8s.io  -A
   
   kubeadm
   
2. 
```



### 7. rbac

```
# role
apiVersion: rbac.authorization.k8s.io/v1beta1
kind: Role
metadata:
  namespace: default
  name: dev
rules:
  - apiGroups: [""]    // core api
    resources: ["pods"]
    verbs: ["get", "watch", "list"]
    
 - apiGroups: [""]    // core api
   resources: ["configMap"]
   verbs: ["create"]
   
   
   
   
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  creationTimestamp: "2022-02-06T07:48:49Z"
  name: developer
  namespace: blue
  resourceVersion: "870"
  uid: 1e34b0a5-6b68-475c-8510-ca17258a3b51
rules:
- apiGroups:
  - ""
  resourceNames:
  - blue-app
  resources:
  - pods
  verbs:
  - get
  - watch
  - create
  - delete
  - list
    


# roleBinding
apiVersion: rbac.authorization.k8s.io/v1beta1
kind: RoleBinding
metadata:
  name: dev-binding
  namespace: default

subjects:
  - kind: User
    name: jane
    apiGroup: rbac.authorization.k8s.io

roleRef:
  kind: Role
  name: dev
  apiGroup: rbac.authorization.k8s.io
  
  
kubectl get roles/rolebindings
kubectl describe role dev
kubectl describe rolebinding dev-binding

kubectl auth can-i create deployments --as dev
kubectl auth can-i create/list pods --as dev -n xxx
kubectl auth can-i delete nodes





# clusterRole  跨namespace
kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1beta1
metadata:
  name: secret-reader
rules:
  - apiGroups: [""]         
    resources:["secrets/nodes/ns/user/group"]
    verbs: ["get", "watch", "list"]
    

# clusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1beta1
kind: ClusterRoleBinding
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

线上测试

```
1. Grant the dev-user permissions to create deployments in the blue namespace.
Remember to add both groups "apps" and "extensions".
Create Deployments


rules:
- apiGroups:
  - ""
  resourceNames:
  - dark-blue-app
  resources:
  - pods
  verbs:
  - get
  - watch
  - create
  - delete
  - list
- apiGroups: ["extensions"，"apps"]
  resources:
  - deployments
  verbs: ["create"]
  
  
  
2. What namespace is the cluster-admin clusterrole part of?
cluster roles are cluster wide and not part of any namespaces
```



### 8. sa

```
用来访问kubernetes api, 由kubenetes创建，挂载到/var/run/secrets/kubernetes.io/serviceaccount

kubectl run nginx --image=hub.atguigu.com/library/nginx:v1

kubectl exec -it `kubectl get pods -l run=nginx -o=name | cut -d "/" -f2` ls /var/run/secrets/kubernetes.io/serviceaccount


kubectl exec -it `kubectl get pods -l run=nginx -o=name | cut -d "/" -f2` cat /var/run/secrets/kubernetes.io/serviceaccount/token


"""
ca.crt
namespace
token
"""


kubectl create sa dashboard-sa
kubectl get sa
kubectl describe sa dashboard-sa



apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
  labels:
    app: myapp
spec:
  containers:
  - name: myapp-container
    image: busybox:1.28
    
  serviceAccountName: dashboard-sa
  serviceAccount: xxxx
  automountServiceAccountName: false
```



### 9. image security

```
docker tag nginx:latest hub.atguigu.com/mylibrary/nginx:v1
docker push hub.atguigu.com/mylibrary/nginx:v1

docker logout  hub.atguigu.com
docker rmi 
docker pull hub.atguigu.com/mylibrary/nginx:v1




		
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
kubectl get pod foo    # 发现不能正常运行

kubectl create secret docker-registry myregistrykey --docker-server=hub.atguigu.com --docker-username=admin --docker-password=Harbor12345 --docker-email="123@qq.com"

kubectl get pod foo    # 发现能正常运行
```



### 10. security context（***）

>  可用来给为 Container 设置linux权能 
>
> https://kubernetes.io/zh/docs/tasks/configure-pod-container/security-context/

```
apiVersion: v1
kind: Pod
metadata:
  name: foo
spec:
  containers:
    - name: foo
      image: hub.atguigu.com/mylibrary/nginx:v1
      securityContext:
        runAsUser: 1000
        capabilities:
          add: ["mac_admin", "NET_ADMIN", "SYS_TIME"]
```



### 11. network policy

```
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: db-policy
spec:
  podSelector:
    matchLabels:
      role: db
  policyTypes:
  - Ingress
  - Engress
  
  ingress:
  - from:
    - podSelector:
        matchLabels:
          name: api-pod
    - namespaceSelector:
        matchLabels:
          name: api-pod
    - ipBlock:
        cidr: 192.168.1.1/20
          
    ports:
    - protocol: TCP
      port: 3306
      
  egress:
  - to:
    - ipBlock:
    	cidr: 192.168.19.1/32
    ports:
    - protocol: TCP
      port: 80
      
      
kubectl get networkpolicies
```



线上测试

```
11. Create a network policy to allow traffic from the Internal application only to the payroll-service and db-service.

Use the spec given on the below. You might want to enable ingress traffic to the pod to test your rules in the UI.

CheckCompleteIncomplete
Policy Name: internal-policy
Policy Type: Egress
Egress Allow: payroll
Payroll Port: 8080
Egress Allow: mysql
MySQL Port: 3306



apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: internal-policy
  namespace: default
spec:
  podSelector:
    matchLabels:
      name: internal
  policyTypes:
  - Egress
  - Ingress
  ingress:
    - {}
  egress:
  - to:
    - podSelector:
        matchLabels:
          name: mysql
    ports:
    - protocol: TCP
      port: 3306

  - to:
    - podSelector:
        matchLabels:
          name: payroll
    ports:
    - protocol: TCP
      port: 8080

  - ports:
    - port: 53
      protocol: UDP
    - port: 53
      protocol: TCP
```





## 7. storage

### 1. storage in docker

```
/var/lib/docker
aufs
containers
image
volumes
	data_volumes


// image & container
镜像分层
copy on write

container layer  read write
image layer      read only


// volumes
-v  read --- read write

docker run -v data_volumes:/var/lib/mysql mysql
```

### 2. drivers

```
// storage drivers
zfs/overlay

// volume drivers
local/gfs/...

docker run -it --name mysql --volume-driver rexray/ebs --mount src=ebs-vol,target=/var/lib/mysql mysql
```



### 3. csi

```
rkt, cri-o

cni: flannel, cilium, weaveworks

csi: dell emc, glusterfs
```



### 4. volumes

```
apiVersion: v1
kind: Pod
metadata:
  name: foo
spec:
  containers:
    - name: foo
      image: hub.atguigu.com/mylibrary/nginx:v1
      volumeMounts:
      - mountPath: /opt
        name: data-volumes
  volumes:
  - name: data_volumes
    hostpath: 
      path: /data
      type: Directory
      
      
// volumes types
hostpath
awsElasticBlockStore
  volumeId:
  fsType: ext4
```



### 3. pv

```
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-voll
spec:
  accessMode:
  - ReadWriteOnce
  capacity:
    storage: 1Gi
    
  hostpath:
    path: /tmp/data
    
  awsElasticBlockStore:
    volumeId: xxx
    fsType: ext4
    
kubectl get pv
```



### 4. pvc

```
// pv
labels:
  name: pv
  
// pvc
selector:
  matchLabels:
    name: my-pv
    


// pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: myclaim
spec:
  accessModes:
    - ReadWriteOnce
  volumeMode: Filesystem
  resources:
    requests:
      storage: 500Mi

  storageClassName: slow
  selector:
    matchLabels:
      release: "stable"
    matchExpressions:
      - {key: environment, operator: In, values: [dev]}


kubectl get pvc


// pv.yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-voll
spec:
  accessMode:
  - ReadWriteOnce
  capacity:
    storage: 1Gi
  persistentVolumeReclaimPolicy: Retain/Delete/Recycle
  awsElasticBlockStore:
    volumeId: xxx
    fsType: ext4



// pod.yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    run: static-busybox
  name: static-busybox
spec:
  containers:
  - image: busybox
    name: static-busybox
    command:
    - "bin/sh"
    - "-c"
    - "sleep"
    args: ["1"] 
    
    volumeMounts:
    - mountPath: /opt
      name: data-volume
      
  volumes:
  - name: data-volume
    persistentVolumeClaim:
      claimName: myclaim
```



### 5. storage class(***)

```
// static provision

// dynamic provision
// sc.yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: google-storage
provisioner: kubernetes.io/gce-pd
parameters:
  resturl: "http://192.168.10.100:8080"
  restuser: ""
  secretNamespace: ""
  secretName: ""
  
  or
  
  type: pd-standard | pd-ssd
  replication-type: none
  
reclaimPolicy: Retain
allowVolumeExpansion: true
mountOptions:
  - debug
volumeBindingMode: Immediate





// pv.yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-voll
spec:
  accessMode:
  - ReadWriteOnce
  capacity:
    storage: 1Gi
  gcePersistentDisk:
    pdName: pd-disk
    fsType: ext4
    

// pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: myclaim
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 500Mi
      
  storageClassName: google-storage
      
// pod.yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    run: static-busybox
  name: static-busybox
spec:
  containers:
  - image: busybox
    name: static-busybox
    command:
    - "bin/sh"
    - "-c"
    - "sleep"
    args: ["1"] 
    
    volumeMounts:
    - mountPath: /opt
      name: data-volume
      
  volumes:
  - name: data-volume
    persistentVolumeClaim:
      claimName: myclaim
```





## 8. network

### 1. basic

```
1. switch and routing
   // switch  同网段
	ip link
	ip addr add 192.168.1.10/24 dev eth0
	ip addr add 192.168.1.11/24 dev eth0
	
	ping 192.168.1.1
	
  // routing  跨网段
  192.168.1.1  192.168.2.1  交换机上的一个端口
  route
  
  ip route add 192.168.2.0/24 via 192.168.1.1
  
  同理
  ip route add 192.168.1.0/24 via 192.168.2.1
  
  
  // gateway 
  ip route add default via 192.168.2.1
  
  
  cat /proc/sys/net/ipv4/ip_forward
  0
  
  echo 1 > /proc/sys/net/ipv4/ip_forward


dns
	ping 192.168.1.11
	ping db 
	
	//dns server 192.168.1.100
	cat /etc/hosts    
	192.168.1.11 db
	192.168.1.11 www.xxx.com
	
	// sub server
	cat /etc/resolv.conf
	nameserver 192.168.1.100
	nameserver 8.8.8.8
	
	// 优先级调整
	cat /etc/nsswitch.conf
	hosts: files  dns
	
	
	
	domain names
	   www           baidu                   .com
	   subdomain    top level domain name     root
	   
	   
	apps.google.com 
		org dns -> root dns -> .com dns -> google dns -> ip -> cache
		
		
	root dns:
		192.168.1.10    web.mycompany.com
		
 	 cat /etc/resolv.conf
 	 nameserver 192.168.1.100
 	 search mycompany.com   prod.mycompany.com
 	 
 	 
 	 
 	 cname:
 	 	foot.web-server   eat.web-server / hungry.web-server mapping
 	 
 	 nslookup www.baidu.com
 	 	name: www.google.com
 	 	address: 172.217.0.132
      
      dig www.google.com
      

network namespace:
	ps aux
	
	ip netns add red
	ip netns
	
	ip link
	ip netns exec red ip link
	ip -n red link 
	
	
	
	arp node01
	ip netns exec red arp
	
	
	route 
	ip netns exec red route
	
	ip link add veth-red  type veth peer name  veth-blue
	ip link set veth-red netns red
	ip link set veth-blue netns blue
	
	ip -n red addr add 192.168.15.1 dev veth-red
	ip -n blue addr add 192.168.15.2 dev veth-blue
	
	ip -n red link set veth-red up
	ip -n blue link set veth-blue up
	
	
	linux bridge:
		ip addr add 192.168.15.5/24 dev v-net-0
		
		namespace 192.158.15.5  --> 192.168.1.3
		ip netns exec blue ping 192.168.13
		ip netns exec blue route
		ip netns exec blue ip route add 192.168.1.0/24 via 192.168.15.5
		
		iptables -t nat -A POSTROUTING -s 192.168.15.0/24 -j MASQUERADE
	
	    ip netns exec blue ping 8.8.8.8
	    ip netns exec blue route
	    ip netns exec blue ip route add default via 192.168.15.5
	    
	    ip netns exec blue ping 8.8.8.8
	    
	    
	    
		
	
	

docker network
	host 
	bridge
		docker network ls
		ip link   
		ip addr
		ip netns
		docker inspect xxx
		
		
		ip link                  能看到vethxxx   bridge   接口
		ip -n (ip netns) link    能看到eth0      container接口
		
		ip -n (ip netns)  addr   能看到IP        container
		ip addr                  能看到ip        bridge 上的docker0
		
		docker run -p 8080:80 nginx 
		iptables -t nat -A PREROUTING -j DNAT --dport 80 --to-destination 8080
		iptables -nvl -t nat
		
		
		cni:
			bridge  add <cid> <namespace>
			bridge add 2exx /var/run/netns/2exx
```

### 2. pod network

```
同一 node 下的pod
不同 node 下的pod
   ip addr add 10.244.1.1/24 dev v-net-0
   ip addr add 10.244.2.1/24 dev v-net-0
   ip addr add 10.244.3.1/24 dev v-net-0
   
   ip addr set 
   ip -n xxx addr add
   ip -n xxx route add
   ip -n xxx link set
   ip link set
   
   
   *****************************************************
   kubelet --cni-conf-dir=/etc/cni/net.d
           --cni-bin-dir=/etc/cni/bin
           --network-plugin=cni
           
   ps -ef | grep kubelet
   
   ls /opt/cni/bin     //二进制文件，默认
   
   ls /etc/cni/net.d   //配置文件， 默认
   
   
   cat /etc/kubernetes/manifests/kube-apiserver.yaml | grep cluster-ip-range
   
   
   *****************************************************
   
   通过weaves 实现 10.244.1.2  to  10.244.2.2
   
   kubectl 	exec busybox ip route
```



### 3. ipam

```
ip address manager

ip = get_free_ip_from_host_local()
ip -n <namespace> addr add
ip -n <namespace> route add

cat /etc/cni/net.d/net-script.conf
```



### 4. service network

```
clusterip
nodeport
loadbalancer
external


kube-proxy --proxy-mode [ userspace | iptables | ipvs ]
ps aux | grep kube-api-server

iptabels -L -t nat | grep db-service

cat /var/log/kube-proxy.log
kubectl -n kube-system  logs  kube-proxy-log
```



### 5. coredns

```
default                         dns                         apps
10.244.1.5            web-service 10.107.37.188       10.107.37.188
test                                                  web-service


curl http://web-service.apps.svc/pod.cluster.local             (servicename/hostname.namespace.types.Root)


pod                                   dns
cat /etc/hosts                     web  xxx.xx.xx.xx
cat /etc/resolv.conf               test xxx.xx.xx.xx


coredns --- rs
cat /etc/coredns/Corefile


kubectl get cm -n kube-system
kubectl get service -n kube-system


host web-service
cat /etc/resolv.conf   // search default.svc.cluster.local svc.cluster.local  cluster.local

```

线上测试

```
Set the DB_Host environment variable to use mysql.payroll.
kubectl edit deploy webapp  DB_Host
```



### 6. ingress

```
google cloud platform
38080

ingress 

wear-service   video-service
wear wear wear video video video


apiVersion: v1
kind: Deployment
metadata:
  labels:
    run: static-busybox
  name: static-busybox
spec:
  replicas: 1
  selector:
    matchLabels:
      name: nginx-ingress
      
  template:
    metadata:
      labels:
        name: nginx-ingress
    spec:
      containers:
      - image: busybox
        name: static-busybox
        
      args:
      
      env:
      
      
      ports:
      - name: http
        containerPort: 80
      - name: https
        containerPort: 443
        
     
apiVersion: v1
kind: Service
metadata:
  name: nginx-ingress
spec:
  type: NodePort
  ports:
  - port: 90
    targetPort: 80
    protocol: TCP
  - port: 443
    targetPort: 443
    protocol: TCP
    name: https
    
  selector:
  	name: nginx-ingress
  	
  	

kind: ConfigMap
apiVersion: v1
metadata:
  name: nginx-configuration
  
 
kind: ServiceAccount
apiVersion: v1
metadata:
  name: nginx-ingress-sa
  
  
  
kind: Ingress
apiVersion: extentions/v1beta1
metadata:
  name: ingress-wear
spec:
  方式一：
  backend:
    serviceName: wear-service
    servicePort: 80
  
  方式二：
  rules:
  - http:
      paths: 
      - path: /wear
      	backend:
          serviceName: wear-service
          servicePort: 80
      - path: /watch
        backend:
          serviceName: watch-service
          servicePort: 80
          
  方式三：
  rules:
  - host: wear.my-online-store.com
    http:
      paths: 
      - backend:
          serviceName: wear-service
          servicePort: 80
   - host: watch.my-online-store.com
     http:
       paths: 
       - backend:
           serviceName: watch-service
           servicePort: 80
```



## 9. others

### 1. ha

```
cluster:
        nginx/haproxy

    master  master  master


etcd:
	etcd cluster
```



### 2. trouble shooting

```
// application failed
    # check service status

    curl http://web-service-ip:node-port
    kubectl describe service web-service  // endpoint, selector


    # check pod
    kubectl get pod
    kubectl describe pod xxx
    kubectl logs -f podxxx


    # check dependent applications


// control plane failed
    # check node status
    kubectl get nodes
    kubectl get pods

    # check controlplane pods
    kubectl get pods -n kube-system

    # check controlplane services
    service kube-apiserver status 
    service kube-controller-manager status
    service kube-scheduler status

    service kubelet status
    service kube-proxy status

    # check service log
    kubectl logs kube-apiserver-master -n kube-system
    sudo journalctl -u kube-apiserver


// work node failed
    # check node status
    kubectl get nodes
    kubectl describe node work-1

    # check node
    top 
    df -h

    # check kubelet status
    service kubelet status
    sudo journalctl –u kubelet


//  Check Certificates
openssl x509 -in /var/lib/kubelet/worker-1.crt -text


//  network failure


// etcd failure
```



### 3. advanced command

```
kubectl get nodes -o json    // 大量节点的时候使用
kubectl get pods -o=jsonpath='{ .items[0].spec.containers[0].image }'
                             '{ range .items[*] }'
                             '{.metadata.name}{"\t"}{.status.capacity.cpu}{"\n"}'


kubectl get nodes -o=custom-columns=<colume-name>:<json-path>,<colume-name>:<json-path>

kubectl get nodes -o=custom-columns=node:.metadata.name, cpu:.status.capacity.cpu

kubectl get nodes --sort-by=.status.capacity.cpu
```

