> java 编写POC的优势
> 反序列化漏洞
> 1. 其余语言无法动态生成字节码
> 2. 长亭科技自己用golang动态生成字节码
> 3. maven -- 第三方依赖管理


## POC编写

1. Verif 漏洞验证模块
2. Exp  漏洞利用模块 -- java spel command--whoami
3. info  信息探测模块
	1. 目标探测：无害包 / OA版本
	2. 精准检测：dnslog  /  echo
4. tools 工具辅助模块 -- 快速生成常用命令 / 编码解码


## [woodpecker](https://github.com/woodpecker-framework/woodpecker-framework-release)

### 编写插件流程
1. Idea 新建项目
2. Name-vuldb
3. groupid：me.gv7.woodpecker.plugin ![](media/Pasted%20image%2020240518140245.png)
4. 配置maven , 云仓库 / 本地仓库
5. 导入一个[woodpecker依赖](https://github.com/woodpecker-framework/woodpecker-sdk)
```java
<dependency>
  <groupId>me.gv7.woodpecker</groupId>
  <artifactId>woodpecker-sdk</artifactId>
  <version>0.1.0.beta4</version>
</dependency>
```
6. 导入[请求依赖](https://github.com/woodpecker-framework/woodpecker-requests)
```java
<dependency>
    <groupId>me.gv7.woodpecker</groupId>
    <artifactId>woodpecker-requests</artifactId>
    <version>0.1.0</version>
</dependency>
```
7. 导入序列化依赖 / fastjson 解决字符串
8. 创建相关类![](media/Pasted%20image%2020240518143718.png)  ![](media/Pasted%20image%2020240518143807.png)  
9. exploit / Pocs


给出[框架代码](media/All-vuldb.zip)