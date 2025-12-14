#docker
## **TLS 证书验证失败**
- tls: failed to verify certificate: x509

```bash
Pulling mongodb (mongo:4.0.27)... ERROR: Get "https://registry-1.docker.io/v2/": tls: failed to verify certificate: x509: certificate is valid for *.ntdtv.com, ntdtv.com, not registry-1.docker.io
```
![](media/Pasted%20image%2020251207192735.png)  

```bash
# Linux: 修改 /etc/resolv.conf 
nameserver 8.8.8.8
nameserver 1.1.1.1
```