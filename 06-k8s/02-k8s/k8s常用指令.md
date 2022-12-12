
```

https://m.toutiaocdn.com/i6981622551407575566/?app=news_article×tamp=1625618245&use_new_style=1&req_id=202107070837250102122020965C10616B&group_id=6981622551407575566&tt_from=android_share&utm_medium=toutiao_android&utm_campaign=client_share&share_token=e543144c-c034-4383-a55d-c5c64cd83512


kubectl 插件：  https://krew.sigs.k8s.io/plugins

# 创建
kubectl create -f xxx.yml [--record] //--record可以记录命令可以很方便的查看每revision变化
kubectl apply  -f xxx.yml 


# 查看 pod 状态， 可以获取到ip等信息
kubectl get svc/deployment/rs/pod   all/-n kube-system  -o wide -w (一直刷新, 也可以在最前面加上watch)
    -o=json	以JSON格式显示结果
    -o=jsonpath=<template>	输出jsonpath表达式定义的字段信息
    -o=jsonpath-file=<filename>	输出jsonpath表达式定义的字段信息，来源于文件
    -o=name	仅输出资源对象的名称
    -o=wide	输出额外信息。对于Pod，将输出Pod所在的Node名  *****
    -o=yaml	以yaml格式显示结果   *****

# 查看 pod 标签
kubectl get pod --show-labels

kubectl edit pod/cm/pv  xxx

kubectl describe pod/deployment/rs/svc/cm/pv/node xxx 

kubectl explain pod.spec.xxx
kubectl explain pod --recursive | less      very useful
kubectl explain pod --recursive | grep -A5 	tolerations


# 查看pod日志
kubectl logs pod名 -c 容器名 -n namespace  // -c 指定容器名

pods=$(kubectl get pods --selector=job-name=hello-1596430800 --output=jsonpath={.items..metadata.name})

kubectl logs $pods



 kubectl exec `kubectl get pods -l name=configmap-hot-update -o=name | cut -d "/" -f2` -it  -- cat /etc/config/log_level


# 删除
kubectl delete -f clusterip.yaml
kubectl delete pod/rs/svc --all
kubectl delete deployment/svc/pod xxx


# 扩容
kubectl scale deployment nginx-deployment --replicas=5
kubectl get pod 
kubectl get rs          // 模板并未变化

# hpa 
kubectl autoscale deployment nginx-deployment --min=10 --max=15 --cpu-percent=80

# 回滚到指定版本
// 查看历史记录
kubectl rollout history deployment/nginx-deployment  
// 查看单个revision 的详细信息
kubectl rollout history deployment alpine-fbgweb --revision=1
// 回退到指定版本
kubectl rollout undo deployment/nginx_deployment --to-revision=2 
// 查看回滚状态
kubectl rollout status deployment/nginx-deployment   // 查看更新状态  echo $? 退出值是否为0，判断是否成功

kubectl rollout pause   deployment/nginx-deployment  // 暂停


# 更新镜像, harbor记得打开
kubectl set image deployment/nginx_deployment 容器名=镜像名:版本 -n namespace

kubectl set image deployment/nginx_deployment nginx=hub.atguigu.com/library/nginx:v2  

kubectl get rs        // 镜像修改触发rs模板创建


# 查看 pod 标签
kubectl get pod --show-labels

# 更新 pod 标签, 更改发现pod是新增的
kubectl label pod frontend-klxcb tier=frontend1  --overwrite=True


# daemonset
kubectl get daemonset

# job
kubectl get job
kubectl logs pi-4jr9r
kubectl delete job xxx

# cronjob
kubectl get cronjob 
kubectl get jobs 
kubectl delete cronjob xxx
幂等，cronjob 无法获取job成功与否




# service
# 查看ipvs： 
ipvsadm -Ln

ipvs算法：
rr
lc 
dh 
sh 
sed
nq


yum install -y bind-utils 
# dig -t A podname.namespace.svc.cluster.local. @ip
dig -t A myservice-headless.default.svc.cluster.local. @10.244.0.2
    

netstat -anpt | grep :30478
iptables -t nat -nvL


kubectl get svc 
kubectl get pod -o wide -n kube-system
dig -t A myservice-externalname.default.svc.cluster.local. @10.244.0.2


# ingress
借助ingress，不需要进入nginx，通过定义ingress配置，由ingress写入到nginx的配置文件中

kubectl apply -f mandatory.yaml

kubectl apply -f service-nodeport.yaml

kubectl get pod -n ingress-nginx 
kubectl get svc -n ingress-nginx

kubectl get ingress 


# configmap
## 目录
kubectl create configmap game-config --from-file=./configMap_dir
## 文件
kubectl create configmap game-config2 --from-file=./configMap_dir/game.properties

kubectl create configmap nginx-config --from-file=./nginx.conf

## 字面量
kubectl create configmap special-config --from-literal=special.how=very --from-literal=special.type=charm

kubectl get cm [ game-config -o yaml ]
kubectl describe cm 


kubectl logs configmap-env  | grep TYPE

kubectl exec `kubectl get pods -l name=configmap-hot-update -o=name | cut -d "/" -f2` -it  -- cat /etc/config/log_level


热更新：
kubectl patch deployment configmap-hot-update --patch '{"spec":{"template":{"metadata":{"annocation":{"version/config":"20201101"}}}}}' 


# secret 
kubectl get secret 

kubectl create secret docker-registry myregistrykey --docker-server=hub.atguigu.com --docker-username=admin --docker-password=Harbor12345 --docker-email="123@qq.com"


kubectl create secret tls tls-secret --key tls.key --cert tls.crt

kubectl create secret generic basic-auth  --from-file=auth


# volume


# pv & pvc
kubectl delete statefullset --all
kubectl get pv
kubectl get pvc
kubectl describe pv nfspv1

kubectl edit pv xxx


# pvc 和 volume区别
PV是类似于Volumes的卷插件，但是其生命周期独立于Pod，而 volume 和 pod是静态的绑定关系，生命周期是一致的，volume更多的是做共享，pv做持久化.




# others 
    # 查看adm版本
    kubeadm version
    
    # 获取现有的namespace
    kubectl get namespaces
    
    
    kubectl exec xxx -c yyy  -it -- /bin/sh
    
    kubectl run/create xxx --image=xxx  --replicas=10 --requests="cpu=1,memory=256Mi"
    
    kubectl get csr    // 如果没有，说明部署的有问题
    systemctl restart kubelet
    
    kubectl certificate approve xxxx 
    
    
    
    kubectl get node    // 部署完flannel 才会就绪ready
    
    kubectl top node
    
    kubectl describe node k8s-node3   // 查看k8s-node3上资源分配的情况
    
    
    设置名称空间偏好
    #可以通过 set-context 命令改变当前 kubectl 上下文 的名称空间，后续所有命令都默认在此名称空间下执行。
    
    kubectl config set-context --current --namespace=<您的名称空间>
    
    # 验证结果
    kubectl config view --minify | grep namespace
    
    # 检查上下文
    kubectl config view
    
    
    #切换到 development 名称空间：
    kubectl config use-context dev
     
    #验证
    kubectl config current-context
    dev
    
    
    并非所有对象都在名称空间里
    大部分的 Kubernetes 对象（例如，Pod、Service、Deployment、StatefulSet等）都必须在名称空间里。但是某些更低层级的对象，是不在任何名称空间中的，例如 nodes、persistentVolumes、storageClass 等
    
    执行一下命令可查看哪些 Kubernetes 对象在名称空间里，哪些不在：
    
    # 在名称空间里
    kubectl api-resources --namespaced=true
    
    # 不在名称空间里
    kubectl api-resources --namespaced=false


# 驱逐和禁用
    1. 设置节点不可调度, 新的不会被分配
    kubectl cordon k8s-node3
    kubectl get pods 
    
    2. 驱逐已有的节点
    kubectl drain k8s-node3 --ignore-daemonsets --force
    
    3. 删除已有的节点
    kubectl delete node k8s-node3
    
    关机也可以，大概5分钟
    
    
    
    # 维护时，将某个节点上打污点，维护完成再删除 
    kubectl taint nodes node1 key1=value1:NoExecute
    kubectl taint nodes node1 key1=value1:NoExecute-
    
    # 给节点打标签
    kubectl label node node2 disk=ssd
    
    
    // 发送原始请求并解析成json
    kubectl get --raw "/apis/custom.metrics.k8s.io/v1beta1"  | jq




# metrics server
kubectl get --raw /apis/metrics.k8s.io/v1beta1/nodes
kubectl top node/pods --all-namespaces          // 查看有没有 cpu, memory等指标
kubectl get pods -n kube-system                 // 查看有没有metrics server 

kubectl logs xxx -n kube-system                 // 查看有没有错误日志，有没有正常工作

kubectl get apiservers                          // 查看聚合成有么有成功注册




# helm 
https://blog.csdn.net/bbwangj/article/details/81087911#helm%E7%AE%80%E4%BB%8B
https://www.jianshu.com/p/ab26b5762cf5

// 使用如下命令可以看到实际的模板被渲染过后的资源文件， 跟debug效果是一样的
helm get manifest web

// 检查语法
helm lint mycharts

// 调试信息
helm install web2 --dry-run /root/mychart

// 获取service 的endpoint信息
kubectl get ep




helm --help

//安装本地
helm install . [ --name hello-helm ] 

//安装线上的
helm install stable/xxx --version yyy
helm install stable/xxx --values values-prodution.yaml

helm install  stable/metrics-server \
 -n metrics-server \
 --namespace kube-system \
 -f metrics-server.yaml

//通过 tar 包安装
helm install ./nginx-1.2.3.tgz

//通过 URL 安装
helm install https://example.com/charts/nginx-1.2.3.tgz


// 常用命令
helm repo list
helm repo remove stable  /  xxx 
helm repo add stable https://kubernetes.oss-cn-hangzhou.aliyuncs.com/charts

helm search stable/kubernetes-dashboard
helm fetch  stable/kubernetes-dashboard      //为啥我的fetch没有作用 ？？？ 网络问题
helm init --service-account tiller  --skip-refresh
helm version


helm list/ls  --deleted                  // 列出当前的helm chart, 包括删除的, 可以看到版本信息等
helm history  release_name               // 查看release的历史信息
helm status   release_name               // 查看release的状态
heml delete [ --purge ]  release_name    // (完整)删除

helm (repo) upgrade release_name .  --set image.tag="v3"    //更新release
helm (repo) upgrade release_name . -f values.yaml

// 回滚
helm rollback release_name release_version     // 非完整删除下可以回滚, 会生成新的revision
helm rollback db-mysql 1

// debug , 能看到所有模板渲染后的yaml文件，但是不会执行
helm install .  --dry-run --debug --set image.tag=latest --name test
helm install --name mychart --dry-run --debug -f global.yaml ./mychart/
helm install --name mychart --dry-run --debug --set course="k8s" ./mychart/
helm install --name mychart --dry-run --debug ./mychart/

// 检查语法
helm lint mycharts



# k8s文档
https://kubernetes.io/docs/home/
https://kubernetes.io/zh/docs/home/
http://docs.kubernetes.org.cn/230.html

```
