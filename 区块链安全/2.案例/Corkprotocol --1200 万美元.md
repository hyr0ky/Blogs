>Corkprotocol 遭受攻击，损失 3,762 wstETH（价值约 1200 万美元）。
![](media/Pasted%20image%2020250528222543.png)  

- 分析： https://x.com/hklst4r/status/1927743793325121665
- https://app.blocksec.com/explorer/tx/eth/0xfd89cdd0be468a564dd525b222b728386d7c6780cf7b2f90d2b54493be09f64d
- 推特： https://x.com/officer_cia/status/1927709439190020443
- 攻击者地址：0xEA6f30e360192bae715599E15e2F765B49E4da98 ![](media/Pasted%20image%2020250528222426.png)  
 >根本原因似乎是汇率计算方式存在问题。攻击者通过部署虚假代币来操纵汇率——该协议包含恢复默认值的逻辑 

 ![](media/Pasted%20image%2020250528222505.png)  

## 更新代码
- 资产工厂： https://contract-diff.swiss-knife.xyz/?contractOld=0x1dc70bd6b9b939cda32ab947459c093bba29e3a7&contractNew=0x0be656b3b8c8efee9d00535debf21cbd6c92824a&chainIdOld=1&chainIdNew=1
- 模块核心： https://contract-diff.swiss-knife.xyz/?contractOld=0x5db3624a38f52d40947c5eefd59791a6ef8d9fb5&contractNew=0xc30d089b8af46190efd6da5652410a6516f19b4b&chainIdOld=1&chainIdNew=1


## 可能
![](media/Pasted%20image%2020250528222937.png)  



## S7iter 

LP  --  两种币相互兑换
![](media/Pasted%20image%2020250528231815.png)  
