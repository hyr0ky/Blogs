
## Develop an ERC20 Cryptocurrency

### ERC20 基础
- [eips.ethereum.org](https://eips.ethereum.org)
#### 核心概念​​

1. ​**​EIP（以太坊改进提案）​**​
    - 定义：社区提出的以太坊协议改进方案，用于推动生态发展。
    - 流程：提议 → 社区讨论 → 标准化（通过后成为 ERC）。
2. ​**​ERC（以太坊请求注释）​**​
    - 定义：被广泛采纳的 EIP，成为以太坊生态标准规范。
    - 编号规则：按时间顺序（如 ERC20 是第 20 号提案）。
    - ​**​ERC20​**​：最主流的​**​可互换代币标准​**​，定义代币的通用接口。

#### ​​EIP 状态流转​​

EIP 生命周期包含以下阶段：

|​**​状态​**​|​**​描述​**​|
|---|---|
|​**​Idea​**​|草案前概念阶段，未进入正式跟踪。|
|​**​Draft​**​|正式开发阶段，格式合规后被合并至 EIP 仓库。|
|​**​Review​**​|作者标记为"准备就绪"，请求同行评审。|
|​**​Last Call​**​|最终审查期（通常 14 天），若需修改则退回 Review。|
|​**​Final​**​|成为最终标准，仅允许修正错误或非规范性补充。|
|​**​Stagnant​**​|草案/评审阶段超过 6 个月无更新，可被复活为 Draft。|
|​**​Withdrawn​**​|作者主动撤回，该编号永久失效。|
|​**​Living​**​|持续更新的活跃标准（如 EIP-1）。|

#### ​ERC20 标准详解​​

1. ​**​本质​**​
    - 基于智能合约在链上记录价值余额的协议。
    - 合约自动追踪代币所有权和交易。
2. ​**​核心用途​**​
    - ✅ 治理代币（DAO 投票权）
    - ✅ 网络安全性保障（如质押代币）
    - ✅ 合成资产（锚定现实资产）
    - ✅ 稳定币（如 DAI、USDC）
    - ✅ 实用代币（生态系统内流通）
3. ​**​必须实现的函数接口​**​
    
 ```bash
    // 基础信息
    function name() external view returns (string memory)  // 代币名称
    function symbol() external view returns (string memory)  // 代币符号
    function decimals() external view returns (uint8)  // 精度（默认 18）
    
    // 核心功能
    function balanceOf(address account) external view returns (uint256)  // 查询余额
    function transfer(address to, uint256 amount) external returns (bool)  // 转账
    function approve(address spender, uint256 amount) external returns (bool)  // 授权
    function allowance(address owner, address spender) external view returns (uint256)  // 查询授权额度
    function transferFrom(address from, address to, uint256 amount) external returns (bool)  // 从授权地址转账
```
    

#### ​开发与部署​​

1. ​**​核心步骤​**​
    - 编写符合 ERC20 标准的 Solidity 合约。
    - 实现所有必需函数（可复用 OpenZeppelin 库）。
    - 通过测试网/主网部署合约。
2. ​**​核心优势​**​
    - ​**​互操作性​**​：所有支持 ERC20 的钱包/交易所可无缝集成。
    - ​**​可组合性​**​：轻松对接 DeFi 协议（如 DEX、借贷平台）。

### 手动创建 ERC20 代币

#### ​基础合约框架​

```go
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.18;

contract ManualToken {
    // 代币基础信息
    function name() public pure returns(string memory) {
        return "Manual Token";
    }
    
    function decimals() public pure returns(uint8) {
        return 18;
    }
    
    function totalSupply() public pure returns(uint256) {
        return 100 ether; // 等价于 100 * 10**18
    }
}
```

#### ​核心功能实现​​

1. ​**​余额存储与查询​**​
    
    ```go
    mapping(address => uint256) private s_balances;
    
    function balanceOf(address _owner) public view returns(uint256) {
        return s_balances[_owner];
    }
    ```
    
    - 使用 `mapping` 存储地址到余额的映射
    - 代币余额本质是合约内部的记账系统
2. ​**​转账功能​**​
    
    ```go
    function transfer(address _to, uint256 _amount) public {
        // 1. 记录转账前总余额（防错验证）
        uint256 previousBalance = balanceOf(msg.sender) + balanceOf(_to);
        
        // 2. 更新余额
        s_balances[msg.sender] -= _amount;
        s_balances[_to] += _amount;
        
        // 3. 验证守恒（防止算术错误）
        require(
            balanceOf(msg.sender) + balanceOf(_to) == previousBalance,
            "Balance conservation failed"
        );
    }
    ```
    
    - 先扣减发送方余额，再增加接收方余额
    - 通过 `require` 验证转账前后总余额守恒


### OpenZeppelin 实现 ERC20 代币

#### ​**​OpenZeppelin 核心优势​**​
- https://docs.openzeppelin.com/contracts/5.x/
1. ​**​安全可靠​**​：提供经过审计的标准合约实现
2. ​**​开发高效​**​：避免重复造轮子，大幅减少开发时间
3. ​**​功能完整​**​：全面实现 ERC20 标准功能（转账/授权/事件等）

#### ​**环境配置**​

1. ​**​安装 OpenZeppelin 库​**​
    
    ```
    forge install OpenZeppelin/openzeppelin-contracts --no-commit
    ```
    
2. ​**​配置路径映射​**​（在 `foundry.toml` 中添加）
    
    ```
    remappings = ["@openzeppelin=lib/openzeppelin-contracts"]
    ```
    

#### ​代币合约实现

```go
// SPDX-License-Identifier: MIT

pragma solidity ^0.8.18;
// 导入 OpenZeppelin 的 ERC20 实现
import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
contract MyToken is ERC20 {
    /**
     * @dev 构造函数初始化代币
     * @param initialSupply 初始供应量（包含精度）
     */
    constructor(uint256 initialSupply) ERC20("MyToken", "MTK") {
        // 向部署者地址铸造初始供应量
        _mint(msg.sender, initialSupply);
    }
}
```

#### ​关键组件解析​

1. ​**​构造函数参数​**​：
    
    - `ERC20("OurToken", "OT")`：设置代币名称和符号
    - `initialSupply`：初始供应量（需包含精度，如 1000 * 10¹⁸）
2. ​**​核心函数继承​**​：
    
    |​**​函数​**​|​**​功能​**​|​**​是否实现​**​|
    |---|---|---|
    |`name()`|获取代币名称|✅|
    |`symbol()`|获取代币符号|✅|
    |`decimals()`|获取代币精度|✅|
    |`totalSupply()`|获取总供应量|✅|
    |`balanceOf()`|查询地址余额|✅|
    |`transfer()`|代币转账|✅|
    |`approve()`|授权额度|✅|
    |`allowance()`|查询授权额度|✅|
    |`transferFrom()`|从授权地址转账|✅|
    
3. ​**​铸造机制​**​：
    
    - 使用 `_mint(msg.sender, initialSupply)` 向部署者分配初始代币
    - 可根据需求修改铸造地址（如 DAO 多签钱包）

