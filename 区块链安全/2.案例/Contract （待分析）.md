- 推特： https://x.com/TikkalaResearch/status/1925239924300947609 ![](media/Pasted%20image%2020250522132552.png)![](media/Pasted%20image%2020250522132606.png)    
- 合约地址： https://bscscan.com/address/0x0851ae80e137c53a8dbc48fce82efd1f50f3b9f2
- 攻击交易： https://bscscan.com/tx/0x3278b9ee1391269a22742d6b4a1289426d1245220ce8994fe32837cd251598f1
- 攻击者： https://bscscan.com/address/0x8b2acc1438f094ad1946ad83f3945edc5ec88601
- Debug分析： https://app.blocksec.com/explorer/tx/bsc/0x3278b9ee1391269a22742d6b4a1289426d1245220ce8994fe32837cd251598f1
- 反编译： https://app.dedaub.com/binance/address/0x0851ae80e137c53a8dbc48fce82efd1f50f3b9f2/decompiled
- 可能为伪造合约：
	- https://bscscan.com/address/0xf6080145e378c79e0c121df74de98fc4c1646748#code
	- https://app.dedaub.com/binance/address/0xf6080145e378c79e0c121df74de98fc4c1646748/decompiled



```Solidty
function 0x94f82f54(struct(4) varg0) public nonPayable {

    require(msg.data.length - 4 >= 32);

    require(varg0 <= uint64.max);

    require(msg.data.length - (4 + varg0) >= 128);

    v0 = new struct(5);

    v0.word0 = 96;

    v0.word1 = address(0x0);

    v0.word2 = 0;

    v0.word3 = 0;

    v0.word4 = 0;

    require(msg.data[4 + varg0 + 64] < msg.data.length - (4 + varg0) - 31);

    require(v1.length <= uint64.max);

    require(v1.data <= msg.data.length - v1.length);

    v2 = new bytes[](v1.length);

    CALLDATACOPY(v2.data, v1.data, v1.length);

    v2[v1.length] = 0;

    v0.word0 = v2;

    v3 = v0.data;

    v0.word1 = this;

    v4 = _SafeAdd(300, block.timestamp);

    v0.word2 = v4;

    v0.word3 = varg0.word1;

    v0.word4 = varg0.word0;

    require(4 + varg0 + 128 - (4 + varg0 + 96) >= 32);

    require(varg0.word3 == address(varg0.word3));

    v5 = new uint256[](160);

    v6 = v0.word0.length;

    MEM[v5 + 160] = v6.length;

    v7 = v8 = 0;

    while (v7 >= v6.length) {

        MEM[v7 + (v5 + 160 + 32)] = v6[v7];

        v7 += 32;

    }

    MEM[v6.length + (v5 + 160 + 32)] = 0;

    v9 = v0.data;

    MEM[v5.data] = address(v0.word1);

    MEM[v5 + 64] = v0.word2;

    MEM[v5 + 96] = v0.word3;

    v10 = new uint256[](v0.word4);

    v11, /* uint256 */ v12 = address(varg0.word3).exactOutput(v5, v10).gas(msg.gas);

    require(bool(v11), 0, RETURNDATASIZE()); // checks call status, propagates error data on error

    require(MEM[64] + RETURNDATASIZE() - MEM[64] >= 32);

    return v12;

}
```