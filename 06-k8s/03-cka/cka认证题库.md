## 00. 考题涉及的k8s文档

```
01-rbac  https://kubernetes.io/docs/reference/access-authn-authz/rbac/
02-drain https://kubernetes.io/zh/docs/tasks/administer-cluster/safely-drain-node/
03-kubeadm 
https://kubernetes.io/zh/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/

04-etcd 
https://kubernetes.io/zh/docs/tasks/administer-cluster/configure-upgrade-etcd/

05-networkpolicy 
https://kubernetes.io/zh/docs/concepts/services-networking/network-policies/

06-service 
https://kubernetes.io/docs/concepts/services-networking/service/

07-ingress 
https://kubernetes.io/zh/docs/concepts/services-networking/ingress/

08-deploy
https://kubernetes.io/zh/docs/concepts/workloads/controllers/deployment/#scaling-a-deployment

09-pod 
https://kubernetes.io/zh/docs/concepts/scheduling-eviction/assign-pod-node/

11-多容器pod
https://kubernetes.io/zh/docs/concepts/workloads/pods/#pod-%E6%80%8E%E6%A0%B7%E7%AE%A1%E7%90%86%E5%A4%9A%E4%B8%AA%E5%AE%B9%E5%99%A8

12-pv
https://kubernetes.io/zh/docs/tasks/configure-pod-container/configure-persistent-volume-storage/#create-a-persistentvolume


13-pvc
https://kubernetes.io/zh/docs/concepts/storage/persistent-volumes/

15-监控sidercar日志
https://kubernetes.io/zh/docs/concepts/cluster-administration/logging/
```



## 01. 权限控制RBAC

> https://kubernetes.io/docs/reference/access-authn-authz/rbac/

```
// question
1. 创建名称 deployment-clusterrole 的 ClusterRole，该⻆⾊具备 创建 
Deployment,Statefulset,Daemonset 的权限
2. 在命名空间 app-team1 中创建名称为 cicd-token 的 ServiceAccount，
3. 绑定 ClusterRole 到 ServiceAccount，且限定命名空间为 app-team1

// answer
kubectl config use-context k8s
kubectl create ns app-team1
kubectl create serviceaccount cicd-token
kubectl create clusterrole  deployment-clusterrole  --verb=create --resource=Deployment,Statefulset,Daemonset

kubectl -n app-team1 create rolebinding deploy-rolebinding --clusterrole=deployment-clusterrole  --serviceaccount=app-team1:cicd-token
```



## 02. 设置节点不可用

> https://kubernetes.io/zh/docs/tasks/administer-cluster/safely-drain-node/

```
// question
设置 ek8s-node-1 节点为不可⽤、重新调度该节点上的所有 pod

// answer
kubectl config use-context k8s
kubectl cordon ek8s-node-1
kubectl drain  ek8s-node-1 --ignore-daemonsets --delete-emptydir-data --
force
完成后⼀定要通过 get nodes 确认status 状态
```



## 03. 升级kubeadm

> https://kubernetes.io/zh/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/

```
// question
升级 master 节点为1.22.2，升级前确保drain master节点，不要升级worker node 、容器
manager、 etcd、 CNI插件、DNS 等内容；

⾸先 cordon、drain master节点，
其次升级 kubeadm 并 apply 到1.22.2版本，
升级 kubelet 和kubectl


// answer, 以ubuntu 系统为例
kubectl config use-context k8s
kubectl get nodes
ssh mk8s-master-0
kubectl cordon mk8s-master-0
kubectl drain mk8s-master-0 --ignore-daemonsets --force

apt-mark unhold kubeadm && \
apt-get update && apt-get install -y kubeadm=1.22.2 && \
apt-mark hold kubeadm
kubeadm version
kubeadm upgrade plan
kubeadm upgrade apply v1.22.2  --etcd-upgrade=false

apt-mark unhold kubelet kubectl && \
apt-get update && apt-get install -y kubelet=1.2.2 kubectl=1.22.2 && \
apt-mark hold kubelet kubectl
  
sudo systemctl daemon-reload
sudo systemctl restart kubelet


kubectl -n kube-system rollout undo deployment coredns  //很重要
kubectl uncordon mk8s-master-0
```



## 04. 备份还原 etcd

> https://kubernetes.io/zh/docs/tasks/administer-cluster/configure-upgrade-etcd/

```
// question
备份 https://127.0.0.1:2379 上的 etcd 数据到 /var/lib/backup/etcd-snapshot.db，使⽤之前的⽂件 /data/backup/etcd-snapshot-previous.db 还原 etcd，使⽤指定的 ca.crt 、 etcd-client.crt 、etcd-client.key

// answer
方式一：
# 备份
ETCDCTL_API=3 etcdctl --endpoints=https://127.0.0.1:2379 \
  --cacert=/opt/KUIN00601/ca.crt --cert=/opt/KUIN00601/etcd-client.crt \
  --key=/opt/KUIN00601/etcd-client.key \
  snapshot save /var/lib/backup/etcd-snapshot.db
  
  
# 还原
ETCDCTL_API=3 etcdctl --endpoints=https://127.0.0.1:2379  \
--cacert=/opt/KUIN00601/ca.crt --cert=/opt/KUIN00601/etcd-client.crt \
--key=/opt/KUIN00601/etcd-client.key \
snapshot restore /data/backup/etcd-snapshot-previous.db

kubectl get nodes



方式二：
1.⾸先先将etcd、api停⽌了，移动静态pod⽂件后，过了⼀会容器会⾃动停⽌，
mv /etc/kubernetes/manifests /etc/kubernetes/manifests.bak

2.备份⼀下原来etcd的⽂件夹
mv /var/lib/etcd /var/lib/etcd.bak

3.恢复数据
ETCDCTL_API=3 etcdctl --endpoints=https://127.0.0.1:2379 snapshot restore
/data/backup/etcd-snapshot-previous.db --data-dir=/var/lib/etcd

4.启动etcd、api容器，把静态pod⽂件夹移回来 过⼀会就可以启动了
mv /etc/kubernetes/manifests.bak /etc/kubernetes/manifests

5.验证集群、pod资源状态
kubectl get nodes
kubectl get pods
```



## 05. NetworkPolicy

> https://kubernetes.io/zh/docs/concepts/services-networking/network-policies/

```
// question
在命名空间 fubar 中创建⽹络策略 allow-port-from-namespace，只允许命名空间 my-app 中的 pod 连上 fubar 中 pod 的 80 端⼝，注意:这⾥有 2 个 ns ，⼀个为 fubar(⽬标pod的ns)，另外⼀个为 my-app(访问源pod的ns)

// answer


kubectl -n my-app get pods --show-labels 


apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-port-from-namespace
  namespace: fubar
spec:
  podSelector:
    matchLabels: {}
  policyTypes:
  - Ingress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          kubernetes.io/metadata.name: my-app
      podSelector:
        matchLabels: {}
    ports:
    - protocol: TCP
      port: 80
```

## 06. 创建service

> https://kubernetes.io/docs/concepts/services-networking/service/

```
// question
重新配置已有的 deployment front-end，添加⼀个名称为 http 的端⼝，暴露80/TCP，创建名
称为 front-end-svc 的 service，暴露容器的 http 端⼝，配置service 的类别为NodePort

// answer
kubectl edit deployment front-end
ports:
- name: http
  protocol: TCP
  containerPort: 80
  
  
kubectl expose deployment front-end --port=80 --target-port=80 --protocol=http --name=front-end-svc
```



## 07. 创建 Ingress

> https://kubernetes.io/zh/docs/concepts/services-networking/ingress/

```
// question
创建⼀个新的 Ingress 资源，名称 ping，命名空间 ing-internal，使⽤ /hello 路径暴露服务
hello 的 5678 端⼝

// answer
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ping
  namespace: ing-internal
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - http:
      paths:
      - path: /hello
        pathType: Prefix
        backend:
          service:
            name: hello
            port:
              number: 5678
              
              
kubectl get ingress -n ing-internal

curl -kl 192.168.123.151/hello
```



## 08. 扩容Deployment

> https://kubernetes.io/zh/docs/concepts/workloads/controllers/deployment/#scaling-a-deployment

```
// question
扩容 deployment guestbook 为 6个pod

// answer
kubectl scale deployment/guestbook --replicas=6
```



## 09. 调度 pod 到指定节点

> https://kubernetes.io/zh/docs/concepts/scheduling-eviction/assign-pod-node/

```
// question
创建pod名称nginx-kusc0041，镜像nginx，调度该pod到disk=ssd的节点上

// answer
apiVersion: v1
kind: Pod
metadata:
  name: nginx-kusc0041
spec:
  containers:
  - name: nginx
    image: nginx
    imagePullPolicy: IfNotPresent
  nodeSelector:
    disk: ssd
```



## 10. 统计ready 状态节点数量

```
// question
统计ready状态节点 要求不包括NoSchedule的节点

// answer
kubectl describe nodes | grep -i taint | grep -v "NoSchedule" | wc -l
```





## 11. 创建多容器的pod

> https://kubernetes.io/zh/docs/concepts/workloads/pods/#pod-%E6%80%8E%E6%A0%B7%E7%AE%A1%E7%90%86%E5%A4%9A%E4%B8%AA%E5%AE%B9%E5%99%A8

```
// question
创建名称为kucc1的pod，pod中运⾏nginx和redis两个容器

// answer
kubectl run kucc1 --image=nginx --dry-run=client -o yaml > pod.yaml 


apiVersion: batch/v1
kind: Pod
metadata:
  name: kucc1
spec:
  containers:
  - name: nginx
    image: nginx
  - name: redis
    image: redis
```



## 12. 创建PV

> https://kubernetes.io/zh/docs/tasks/configure-pod-container/configure-persistent-volume-storage/#create-a-persistentvolume

```
// question
创建⼀个名为app-config的PV，PV的容量为2Gi，访问模式为ReadWriteMany，volume的类型
为hostPath，pv映射的hostPath为/srv/app-config⽬录

// answer
apiVersion: v1
kind: PersistentVolume
metadata:
  name: app-config
spec:
  capacity:
    storage: 2Gi
  accessModes:
    - ReadWriteMany
  hostPath:
    path: "/srv/app-config"
```



## 13. 创建pvc

> https://kubernetes.io/zh/docs/concepts/storage/persistent-volumes/

```
// question
使⽤指定storageclass csi-hostpath-sc创建⼀个名称为pv-volume的 pvc，容量为10Mi,
创建名称为web-server的pod，将nginx 容器的/usr/share/nginx/html⽬录使⽤该pvc挂载,
将上述pvc的⼤⼩从10Mi更新为70Mi，并记录本次变更


// answer


apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pv-volume
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Mi
  storageClassName: csi-hostpath-sc
  
  


apiVersion: v1
kind: Pod
metadata:
  name: web-server
spec:
  containers:
    - name: nginx
      image: nginx
      volumeMounts:
      - mountPath: /usr/share/nginx/html
        name: mypd
  volumes:
    - name: mypd
      persistentVolumeClaim:
        claimName: pv-volume
        
  
 kubectl edit pvc  pv-volume   
```



## 14. 监控pod的⽇志

```
// question
监控foobar pod中的⽇志
获取包含unable-to-access-website的⽇志，并将⽇志写⼊到/opt/KUTR00101/foobar


// answer
kubectl logs foobar | grep unable-to-access-website >
/opt/KUTR00101/foobar
```



## 15. 添加 sidecar 容器并输出⽇志

> https://kubernetes.io/zh/docs/concepts/cluster-administration/logging/

```
// question
添加⼀个sidecar容器(使⽤busybox 镜像)到已有的pod 11-factor-app中，确保sidecar容器能
够输出/var/log/11-factor-app.log的信息，使⽤volume挂载/var/log⽬录，确保sidecar能访问
11-factor-app.log ⽂件


// answer
kubectl get pod -o yaml > new-pod.yaml


apiVersion: v1
kind: Pod
metadata:
  name: counter
spec:
  containers:
  - name: count
    image: busybox
    
    volumeMounts:
    - name: varlog
      mountPath: /var/log
      
  - name: sidercar
    image: busybox
    args: [/bin/sh, -c, "tail -n+1 -f /var/log/11-factor-app.log"]
    volumeMounts:
    - name: varlog
      mountPath: /var/log
   
  volumes:
  - name: varlog
    emptyDir: {}
    

kubectl get pod 11-factor-app
kubectl logs 11-factor-app -c sidecar
```



## 16. 查看 cpu 使用率最高的 pod

```
// question
查找label为name=cpu-loader的pod，筛选出cpu负载最⾼的那个pod，并将名称追加
到/opt/KUTR00401/KUTR00401.txt


// answer
kubectl top pod -l name=cpu-loader -A --sort-by='cpu'
echo podName >> /opt/KUTR00401/KUTR00401.txt
```



## 17. 排查集群中故障节点

```
// question 
节点wk8s-node-0状态为NotReady，查看原因并恢复其状态为Ready
确保操作为持久的

// answer
kubectl get nodes
ssh wk8s-node-0
sudo -i

systemctl status kubelet
systemctl enable kubelet
systemctl restart kubelet
systemctl status kubelet

再次 get nodes， 确保节点恢复 Ready 状态
```

