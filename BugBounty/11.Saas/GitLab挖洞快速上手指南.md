# GitLab挖洞快速上手指南

基于10位顶尖研究员（446份报告）的方法论总结，提供快速上手的实战指南。

## 第一步：选择你的专攻方向

### 根据技术背景选择：
- **前端/JavaScript背景**: 选择joaxcar/yvvdwf的DOM攻击方法
- **API/后端背景**: 选择albatraoz/ashish的API测试方法  
- **Ruby/代码审计背景**: 选择0xn3va的源代码审计方法
- **工作流/流程测试**: 选择xanbanx/pwnie的工作流测试方法
- **权限/配置测试**: 选择mateuszek/ngalog的权限测试方法

### 根据漏洞类型偏好：
- **喜欢找逻辑漏洞**: 源代码审计 + 工作流测试
- **喜欢找权限漏洞**: API权限测试 + 文档一致性测试
- **喜欢找客户端漏洞**: DOM攻击 + XSS测试
- **喜欢找信息泄露**: API测试 + 源代码审计

## 第二步：环境准备（第1周）

### 1. 本地环境搭建
```bash
# 使用Docker部署GitLab
docker run --detach \
  --hostname gitlab.example.com \
  --publish 443:443 --publish 80:80 --publish 22:22 \
  --name gitlab \
  --restart always \
  --volume $GITLAB_HOME/config:/etc/gitlab \
  --volume $GITLAB_HOME/logs:/var/log/gitlab \
  --volume $GITLAB_HOME/data:/var/opt/gitlab \
  gitlab/gitlab-ee:latest
```

### 2. 文档研究重点
- **权限文档**: https://docs.gitlab.com/ee/user/permissions.html
- **API文档**: https://docs.gitlab.com/ee/api/rest/
- **GraphQL文档**: https://docs.gitlab.com/ee/api/graphql/
- **新功能文档**: 关注"Releases"和"What's New"

### 3. 工具准备
```bash
# 基础工具
pip install requests beautifulsoup4
npm install -g graphql-cli

# GitLab API测试工具
git clone https://github.com/dwisiswant0/gitlab-dork
git clone https://github.com/righettod/poc-gitlab-api-abuse
```

## 第三步：基础测试（第2-3周）

### 1. 权限矩阵测试（ashish_r_padelkar方法）
创建Excel表格测试：
```
角色: 访客, 报告者, 开发者, 维护者, 所有者
资源: 项目, 组, 问题, 合并请求, Wiki, 设置
操作: 查看, 创建, 编辑, 删除, 管理
```

测试脚本示例：
```python
import requests

def test_api_permission(api_url, token, role):
    """测试API端点权限"""
    headers = {'Authorization': f'Bearer {token}'}
    
    # 测试不同端点的访问权限
    endpoints = [
        '/api/v4/projects',
        '/api/v4/groups', 
        '/api/v4/users',
        '/api/v4/runners'
    ]
    
    for endpoint in endpoints:
        response = requests.get(f'{api_url}{endpoint}', headers=headers)
        print(f'{role}访问{endpoint}: {response.status_code}')
```

### 2. GraphQL基础测试（albatraoz方法）
```python
import requests
import json

def test_graphql_permissions():
    """测试GraphQL权限"""
    query = """
    query {
      currentUser {
        username
        email
      }
      projects(membership: true) {
        nodes {
          name
          description
          visibility
        }
      }
    }
    """
    
    response = requests.post(
        'https://gitlab.com/api/graphql',
        json={'query': query},
        headers={'Authorization': 'Bearer YOUR_TOKEN'}
    )
    
    # 分析响应，寻找信息泄露
    data = response.json()
    print(json.dumps(data, indent=2))
```

### 3. 文档一致性测试（mateuszek方法）
```python
def test_documentation_vs_reality():
    """测试文档声明与实际行为差异"""
    # 从文档中提取权限声明
    documented_permissions = {
        'guest': ['read_project', 'read_wiki'],
        'reporter': ['read_project', 'read_wiki', 'create_issue'],
        'developer': ['push_code', 'create_merge_request'],
        'maintainer': ['push_to_protected_branches', 'add_runner'],
        'owner': ['all_permissions']
    }
    
    # 实际测试每个权限
    for role, permissions in documented_permissions.items():
        print(f'测试{role}角色:')
        for permission in permissions:
            test_permission(role, permission)
```

## 第四步：中级测试（第4-6周）

### 1. 工作流安全测试（xanbanx方法）
测试重点：
- 邮件合并请求工作流
- Fork项目工作流  
- 推送规则（push rules）工作流
- CI/CD管道工作流

测试脚本：
```python
def test_email_merge_request():
    """测试邮件合并请求安全"""
    # 创建测试项目
    # 配置推送规则
    # 通过邮件发送合并请求
    # 验证是否绕过推送规则
    pass

def test_fork_workflow():
    """测试fork工作流安全"""
    # 创建公开项目
    # Fork项目
    # 将原项目设为私有
    # 测试fork项目是否能访问原项目内容
    pass
```

### 2. 客户端安全测试（joaxcar/yvvdwf方法）
```python
def test_dom_xss():
    """测试DOM XSS漏洞"""
    payloads = [
        '<img src=x onerror=alert(1)>',
        '<svg onload=alert(1)>',
        '<div data-url="javascript:alert(1)">',
        '<a href="data:text/html,<script>alert(1)</script>">test</a>'
    ]
    
    # 测试不同输入点
    input_points = [
        'issue_title', 'issue_description',
        'merge_request_title', 'merge_request_description',
        'wiki_content', 'comment_body'
    ]
```

### 3. 包管理安全测试（taraszelyk方法）
```python
def test_nuget_security():
    """测试NuGet包安全"""
    # 测试路径遍历
    malicious_nuspec = '''<?xml version="1.0"?>
<package>
  <metadata>
    <id>../../../../../../../etc/passwd</id>
    <version>1.0.0</version>
  </metadata>
</package>'''
    
    # 测试文件上传验证
    test_files = [
        ('test.exe', 'application/octet-stream', 1024),  # 禁止的文件类型
        ('test.dll', 'application/octet-stream', 10485760),  # 超大文件
        ('test.nupkg', 'application/zip', 1024)  # 正常文件
    ]
```

## 第五步：高级测试（第7-8周）

### 1. 源代码审计（0xn3va方法）
审计重点文件：
```
app/controllers/ - 控制器权限检查
app/services/ - 业务逻辑
app/graphql/ - GraphQL类型定义
app/models/ - 数据模型权限
app/views/ - 视图层安全
```

审计脚本：
```bash
# 查找权限检查代码
grep -r "before_action" app/controllers/
grep -r "can?" app/controllers/
grep -r "authorize" app/controllers/

# 查找输入验证代码
grep -r "permit" app/controllers/
grep -r "sanitize" app/controllers/
grep -r "validate" app/controllers/
```

### 2. 状态转换攻击（pwnie方法）
```python
def test_state_transition():
    """测试状态转换安全"""
    # 测试项目公开->私有转换
    test_public_to_private()
    
    # 测试用户角色升级/降级
    test_role_promotion_demotion()
    
    # 测试用户封禁/解封
    test_user_ban_unban()
    
    # 测试fork关系变化
    test_fork_relationship()
```

### 3. 组件交互测试
```python
def test_component_interaction():
    """测试组件交互安全"""
    # CI/CD与包管理交互
    test_ci_package_interaction()
    
    # WebIDE与仓库交互
    test_webide_repo_interaction()
    
    # Wiki与项目权限交互
    test_wiki_project_interaction()
    
    # Epics与工作项交互
    test_epics_work_items_interaction()
```

## 第六步：自动化与规模化（第9-12周）

### 1. 自动化测试框架
```python
class GitLabSecurityTester:
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.token = token
        self.session = requests.Session()
        self.session.headers.update({'Authorization': f'Bearer {token}'})
    
    def test_all_endpoints(self):
        """测试所有API端点"""
        endpoints = self.enumerate_endpoints()
        for endpoint in endpoints:
            self.test_endpoint_permissions(endpoint)
            self.test_endpoint_parameters(endpoint)
            self.test_endpoint_errors(endpoint)
    
    def test_graphql_comprehensively(self):
        """全面测试GraphQL"""
        schema = self.get_graphql_schema()
        for query in schema['queries']:
            self.test_graphql_query(query)
        for mutation in schema['mutations']:
            self.test_graphql_mutation(mutation)
    
    def test_workflows_systematically(self):
        """系统化测试工作流"""
        workflows = [
            'merge_request_workflow',
            'fork_workflow',
            'ci_cd_workflow',
            'package_workflow'
        ]
        
        for workflow in workflows:
            self.test_workflow_security(workflow)
```

### 2. 漏洞模式数据库
```python
class VulnerabilityPatternDB:
    def __init__(self):
        self.patterns = {
            'permission_bypass': [],
            'information_disclosure': [],
            'logic_flaw': [],
            'client_side': [],
            'api_abuse': []
        }
    
    def add_pattern(self, category, pattern):
        """添加漏洞模式"""
        self.patterns[category].append(pattern)
    
    def search_patterns(self, code_snippet):
        """在代码中搜索漏洞模式"""
        matches = []
        for category, patterns in self.patterns.items():
            for pattern in patterns:
                if pattern.match(code_snippet):
                    matches.append((category, pattern))
        return matches
```

### 3. 持续监控系统
```python
class GitLabMonitor:
    def __init__(self):
        self.new_features = []
        self.security_fixes = []
        self.api_changes = []
    
    def monitor_new_features(self):
        """监控新功能"""
        # 监控GitLab发布日志
        # 监控文档更新
        # 监控社区讨论
    
    def monitor_security_fixes(self):
        """监控安全修复"""
        # 监控安全公告
        # 监控代码提交
        # 监控漏洞修复
    
    def monitor_api_changes(self):
        """监控API变化"""
        # 监控API文档更新
        # 监控GraphQL schema变化
        # 监控弃用警告
```

## 实战检查清单

### 每日检查清单
- [ ] 检查GitLab新版本和功能
- [ ] 测试1-2个API端点权限
- [ ] 测试1个GraphQL查询
- [ ] 检查1个工作流安全性
- [ ] 分析1个源代码文件

### 每周检查清单  
- [ ] 完整测试一个功能模块
- [ ] 测试所有角色对关键资源的权限
- [ ] 测试CI/CD管道安全性
- [ ] 测试文件上传功能安全性
- [ ] 编写1个自动化测试脚本

### 每月检查清单
- [ ] 全面审计一个核心组件
- [ ] 测试所有工作流安全性
- [ ] 更新漏洞模式数据库
- [ ] 分析其他研究员的报告
- [ ] 总结测试经验和改进方法

## 常见错误和避免方法

### 错误1：测试范围太广
**错误**: 同时测试太多功能，没有深度
**解决**: 专注于一个功能模块，深入测试

### 错误2：忽略文档研究
**错误**: 直接开始测试，不了解预期行为
**解决**: 先深入研究文档，理解设计意图

### 错误3：手动测试效率低
**错误**: 完全手动测试，不自动化
**解决**: 编写自动化测试脚本，提高效率

### 错误4：不跟踪修复
**错误**: 发现漏洞后不跟踪修复情况
**解决**: 建立漏洞跟踪系统，监控修复状态

### 错误5：不学习他人经验
**错误**: 只靠自己摸索，不学习他人方法
**解决**: 分析其他研究员的报告，学习成功经验

## 成功案例学习

### 案例1：joaxcar的DOM攻击
**方法**: 深入分析JavaScript代码，发现数据属性滥用
**学习**: 客户端安全需要深入理解前端代码

### 案例2：albatraoz的GraphQL测试  
**方法**: 系统化测试GraphQL所有查询和字段
**学习**: API安全需要全面和系统化的测试

### 案例3：0xn3va的源代码审计
**方法**: 深度审计Ruby代码，发现逻辑漏洞
**学习**: 白盒测试可以发现黑盒测试难以发现的漏洞

### 案例4：xanbanx的工作流测试
**方法**: 测试完整工作流程，发现边界条件漏洞
**学习**: 工作流安全需要测试完整流程和异常情况

## 资源推荐

### 学习资源
- GitLab官方文档：https://docs.gitlab.com/
- GitLab源代码：https://gitlab.com/gitlab-org/gitlab
- HackerOne报告：https://hackerone.com/gitlab
- 安全测试工具：https://github.com/righettod/poc-gitlab-api-abuse

### 社区资源
- GitLab安全论坛：https://forum.gitlab.com/c/security/
- 安全研究人员Twitter：关注@joaxcar、@albatraoz等
- 安全会议演讲：BlackHat、DEFCON相关演讲

### 工具资源
- API测试：Postman、Insomnia、Bruno
- GraphQL测试：GraphQL Playground、Altair
- 代码审计：Sourcegraph、GitHub Code Search
- 自动化测试：Selenium、Playwright、Cypress

## 总结

GitLab挖洞是一个需要系统化方法和深度理解的工作。通过这个快速上手指南，你可以：

1. **选择适合自己的方向**：根据技术背景选择专攻领域
2. **建立系统化测试流程**：从基础到高级，循序渐进
3. **学习成功经验**：分析其他研究员的报告和方法
4. **持续改进**：根据测试结果调整方法和策略

记住：成功的漏洞挖掘 = 深度理解 × 系统化方法 × 持续学习

开始你的GitLab安全测试之旅吧！