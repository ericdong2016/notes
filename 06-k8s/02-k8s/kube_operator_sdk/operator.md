## 0. 文档

```
//release 有很多版本可选
https://sdk.operatorframework.io/docs/building-operators/golang/tutorial/     
https://sdk.operatorframework.io/docs/building-operators/golang/migration/
https://v1-0-x.sdk.operatorframework.io/



operator-sdk 
	https://sdk.operatorframework.io/docs/installation/#install-from-github-release
	https://github.com/operator-framework/operator-sdk
	https://sdk.operatorframework.io/docs/building-operators/golang/installation/
	
	https://www.bilibili.com/video/BV1zE411j7ky?from=search&seid=10662097676963385697
	https://www.jianshu.com/p/628aac3e6758
	
	
kubebuilder 
	https://www.bilibili.com/video/BV1WJ411t7it?from=search&seid=10662097676963385697    alibaba
	https://www.bilibili.com/video/BV1Tv411r7NR?from=search&seid=18336612307218228529
	
	https://my.oschina.net/u/3825598/blog/4893976
	https://blog.csdn.net/alisystemsoftware/article/details/101305449
	
	https://github.com/kubernetes-sigs/kubebuilder/blob/master/README.md
	https://book.kubebuilder.io/
	
	
开源operator 
	https://www.qikqiak.com/tags/operator/
	https://operatorhub.io/
	https://github.com/operator-framework/awesome-operators

和sidecar的区别
```



## 1. 下载

> v0.9.x  有bug
>
> v0.13.x
>
> v1.0.x   ==   v0.10.x
>
> https://github.com/operator-framework/operator-sdk/releases/tag/v0.9.0      
>
> [https://github.com/operator-framework/operator-sdk/tree/v0.7.x#create-and-deploy-an-app-operator
>
> https://github.com/operator-framework/operator-sdk/blob/v0.9.x/doc/user/install-operator-sdk.md
>
> https://github.com/operator-framework/operator-sdk/blob/v0.9.x/Makefile
>
> https://sdk.operatorframework.io/docs/overview/#kubernetes-version-compatibility    operator-sdk k8s版本对应 





**方式一：Install from GitHub release**

```

curl -OJL https://github.com/operator-framework/operator-sdk/releases/download/v0.9.0/operator-sdk-v0.9.0-x86_64-linux-gnu

# 最新的
curl -OJL https://github.com/operator-framework/operator-sdk/releases/download/v1.9.0/operator-sdk_linux_amd64


curl -OJL https://github.com/operator-framework/operator-sdk/releases/download/v0.9.0/operator-sdk-v0.9.0-x86_64-linux-gnu.asc

gpg --verify operator-sdk-v0.9.0-x86_64-linux-gnu.asc

gpg --recv-key "KEY_ID"

gpg --keyserver keyserver.ubuntu.com --recv-key "KEY_ID"

chmod +x operator-sdk-v0.9.0-x86_64-linux-gnu && sudo cp operator-sdk-v0.9.0-x86_64-linux-gnu /usr/local/bin/operator-sdk && rm operator-sdk-v0.9.0-x86_64-linux-gnu
```



**方式二：Compile and install from master（不推荐，一堆问题）**

```sh
git clone https://github.com/operator-framework/operator-sdk
cd operator-sdk
git checkout v0.9.x

# vim Makefile 中的goproxy
make  tidy 
make  install 
make  build 

chmod +x cmd/operator-sdk  
cp cmd/operator-sdk /usr/local/bin/operator-sdk

operator-sdk help
```



## 2. 使用

> operator-sdk   -h 
>
>  operator-sdk add/new/init
>
> 192.168.19.130  (master)    
>
> d:/mycode/go/src/operator-test     /root/go/src/app-operator 



### 三方文档

```
// 推荐
https://www.qikqiak.com/post/k8s-operator-101/
https://github.com/cnych/opdemo

https://www.bilibili.com/video/BV1zE411j7ky?p=3&spm_id_from=pageDriver    //推荐，很强

operator-sdk generate k8s
operator-sdk generate crds
```



### 官方文档

> https://github.com/operator-framework/operator-sdk/tree/v0.9.x#create-and-deploy-an-app-operator

```
# Create an app-operator project that defines the App CR.
 mkdir -p HOME/projects/example-inc/

# Create a new app-operator project
 cd HOME/projects/example-inc/
 
 export GO111MODULE=on
 operator-sdk new app-operator 
 cd app-operator

# Add a new API for the custom resource AppService
 operator-sdk add api --api-version=app.example.com/v1 --kind=AppService

# Add a new controller that watches for AppService
 operator-sdk add controller --api-version=app.example.com/v1 --kind=AppService
 

# Build and push the app-operator image to a public registry such as quay.io
 
 operator-sdk build quay.io/example/app-operator
 docker push quay.io/example/app-operator

# Update the operator manifest to use the built image name (if you are performing these steps on OSX, see note below)
 sed -i 's|REPLACE_IMAGE|quay.io/example/app-operator|g' deploy/operator.yaml


# Setup Service Account
 kubectl create -f deploy/service_account.yaml

# Setup RBAC
 kubectl create -f deploy/role.yaml
 kubectl create -f deploy/role_binding.yaml

# Setup the CRD
 kubectl create -f deploy/crds/app_v1_appservice_crd.yaml

# Deploy the app-operator
 kubectl create -f deploy/operator.yaml


# Create an AppService CR
# The default controller will watch for AppService objects and create a pod for each CR
 kubectl create -f deploy/crds/app_v1_appservice_cr.yaml


# Verify that a pod is created
 kubectl get pod -l  app=example-appservice

    NAME                     READY     STATUS    RESTARTS   AGE
    example-appservice-pod   1/1       Running   0          1m


# Test the new Resource Type
kubectl describe appservice example-appservice


Name:         example-appservice
Namespace:    myproject
Labels:       <none>
Annotations:  <none>
API Version:  app.example.com/v1alpha1
Kind:         AppService
Metadata:
  Cluster Name:        
  Creation Timestamp:  2018-12-17T21:18:43Z
  Generation:          1
  Resource Version:    248412
  Self Link:           /apis/app.example.com/v1alpha1/namespaces/myproject/appservices/example-appservice
  UID:                 554f301f-0241-11e9-b551-080027c7d133
Spec:
  Size:  3


# Cleanup
 kubectl delete -f deploy/crds/app_v1_appservice_cr.yaml
 kubectl delete -f deploy/operator.yaml
 kubectl delete -f deploy/role.yaml
 kubectl delete -f deploy/role_binding.yaml
 kubectl delete -f deploy/service_account.yaml
 kubectl delete -f deploy/crds/app_v1_appservice_crd.yaml
```



### 调试

```
kubectl create -f deploy/crds/app_v1_appservice_crd.yaml

operator-sdk up local  

kubectl create -f deploy/crds/app_v1_appservice_cr.yaml

看operator-sdk up local 的日志

kubectl get AppService
kubectl get deploy
kubectl get svc
kubectl get pods
 
访问
```



### 部署

```
operator-sdk up local  停掉

执行下面的命令构建 Operator 应用打包成 Docker 镜像：
operator-sdk build cnych/opdemo 


镜像构建成功后，推送到 docker hub：
$ docker push cnych/opdemo

镜像推送成功后，使用上面的镜像地址更新 Operator 的资源清单：
$ sed -i 's|REPLACE_IMAGE|cnych/opdemo|g' deploy/operator.yaml
# 如果你使用的是 Mac 系统，使用下面的命令
$ sed -i "" 's|REPLACE_IMAGE|cnych/opdemo|g' deploy/operator.yaml


现在 Operator 的资源清单文件准备好了，然后创建对应的 RBAC 的对象：
# Setup Service Account
kubectl create -f deploy/service_account.yaml


# Setup RBAC
kubectl create -f deploy/role.yaml
kubectl create -f deploy/role_binding.yaml

# Setup the CRD
kubectl apply -f deploy/crds/app_v1_appservice_crd.yaml

# Deploy the Operator
kubectl create -f deploy/operator.yaml



 kubectl get appservice
 
 kubectl get deploy
 
 kubectl get pods
 
 kubectl describe appservice nginx-app
 
 访问：
 	 Node Port:    30002
```



### 清理

```
kubectl delete -f deploy/crds/app_v1_appservice_cr.yaml
kubectl delete -f deploy/operator.yaml
kubectl delete -f deploy/role.yaml
kubectl delete -f deploy/role_binding.yaml
kubectl delete -f deploy/service_account.yaml
kubectl delete -f deploy/crds/app_v1_appservice_crd.yaml
```

