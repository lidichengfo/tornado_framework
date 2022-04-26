# tornado部署框架

## 1. 简述
>- 语言：python
>- 部署框架：tornado
>- 功能：使用tornado来进行部署,这里值列了两个功能：post和put，post用来操作，put用来更新。
>- 效果：能实现多线程多协程非阻塞微服务

## 2. 操作
>- 对于整个操作，第一、需要设置好port和luyou；第二、完善handle模块和update模块，其他的不需要变动
>- 其他废话也不多说，大家用用吧

## 3. 结构
>- tornado_framework.py 是整个tornado微服务部署的框架
>- example.py 是一个简单的实例，大家看一下即可