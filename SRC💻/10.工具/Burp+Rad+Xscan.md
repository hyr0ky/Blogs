
1. xsacn终端和Rad终端：`set http_proxy=http://127.0.0.1:7890 & set https_proxy=http://127.0.0.1:7890`
2. `xscan.exe  proxy --port 9999`![](media/Pasted%20image%2020250529144622.png)  
3. Burp设置代理![](media/Pasted%20image%2020250529144659.png)![](media/Pasted%20image%2020250529144737.png)  
4. Subfinder / ffuf 搜集站点 子域名等 写入url.txt中
5. Rad爬取`rad --url-file sui.txt --http-proxy 127.0.0.1:8080 -text-output result.txt` ![](media/Pasted%20image%2020250529144955.png)
