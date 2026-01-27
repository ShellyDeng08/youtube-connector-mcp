# Plugins 插件配置

## 推荐插件：Superpowers

### 为什么推荐 Superpowers

Superpowers 是一个**完整的软件开发工作流**，专门为 Claude Code 优化。它包含 13 个可组合的技能，自动引导智能体完成高质量的开发工作。

### 核心优势

| 优势 | 说明 |
|--------|------|
| **自动化工作流** | 技能自动触发，无需手动指定 |
| **系统化方法** | 明确的步骤和检查点 |
| **强制最佳实践** | RED-GREEN-REFACTOR TDD、YAGNI、DRY 原则 |
| **多智能体协作** | 可自主工作数小时不偏离计划 |
| **设计先行** | 写代码前先梳理需求，避免返工 |

### 包含的技能

| 技能 | 用途 |
|--------|------|
| `brainstorming` | 交互式设计优化 |
| `using-git-worktrees` | 创建隔离工作空间 |
| `writing-plans` | 将工作分解为 2-5 分钟任务 |
| `subagent-driven-development` | 多智能体协作开发 |
| `test-driven-development` | 强制 RED-GREEN-REFACTOR |
| `systematic-debugging` | 系统化调试流程 |
| `receiving-code-review` | 接收代码审查 |
| `requesting-code-review` | 请求代码审查 |
| `verification-before-completion` | 完成前验证 |

### 工作流程

```
用户请求 → [brainstorming] → [using-git-worktrees]
         ↓
   [writing-plans] → [subagent-driven-development]
         ↓
   [test-driven-development] ←→ [systematic-debugging]
         ↓
   [verification-before-completion] → [finishing-a-development-branch]
```

### 适用场景

- ✅ 新功能开发
- ✅ Bug 修复
- ✅ 代码重构
- ✅ 复杂架构设计

### 热门度

| 平台 | Stars | 说明 |
|------|-------|------|
| GitHub | ~6k+ | 社区活跃，持续更新 |
| Claude Code Marketplace | 广泛使用 | 首选开发插件 |

### 安装 Superpowers

```bash
# 推荐安装为 user 作用域（全局可用）
claude plugin install superpowers --scope user

# 验证安装
claude plugin list
```

### 新增命令

安装后，你将获得以下斜杠命令：

```
/superpowers:brainstorm    # 交互式设计优化
/superpowers:write-plan    # 创建实现计划
/superpowers:execute-plan  # 分批执行计划
```

---

## 什么是 Plugins

Plugins 是 Claude Code 的扩展包，可包含 Skills、Agents、Commands、Hooks 等组件。通过 Marketplace 分发和管理。

## 目录结构

```
my-plugin/
├── .claude-plugin/
│   └── manifest.json        # 必需：插件清单
├── skills/                  # 可选：包含的技能
│   └── skill-name/
│       └── SKILL.md
├── agents/                  # 可选：智能体
├── commands/                # 可选：命令
├── hooks/                   # 可选：钩子
└── README.md               # 可选：说明
```

## manifest.json

```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "插件描述",
  "author": "作者",
  "skills": ["skills/my-skill"],
  "agents": [],
  "commands": [],
  "hooks": []
}
```

## Plugin vs Skills

| 特性 | Plugin | Skill |
|------|--------|-------|
| 分发 | 是，通过 Marketplace | 否，通过 Plugin 或复制 |
| 内容 | 多个组件 | 单个技能 |
| 安装 | `claude plugin install` | 复制文件 |
| 版本 | 支持版本控制 | 无独立版本 |
| 作用域 | user 或 project | 跟随 Plugin |

## Marketplace 管理

```bash
# 列出已配置的 marketplace
claude plugin marketplace list

# 添加 marketplace
claude plugin marketplace add https://github.com/user/repo

# 移除 marketplace
claude plugin marketplace remove <name>
```

## Plugin 管理命令

```bash
# 安装插件（默认 project 作用域）
claude plugin install plugin-name

# 安装为全局（推荐用于通用工具）
claude plugin install plugin-name --scope user

# 从特定 marketplace 安装
claude plugin install plugin-name@marketplace

# 列出已安装插件
claude plugin list

# 启用/禁用
claude plugin enable plugin-name
claude plugin disable plugin-name

# 更新
claude plugin update plugin-name

# 卸载
claude plugin uninstall plugin-name
```

## 作用域选择

| 场景 | 作用域 |
|--------|--------|
| 通用工具，所有项目都用 | `--scope user` |
| 项目特定工具 | `--scope project` |

## 案例：团队工具集 Plugin

**需求**：团队共享开发工具

**方案**：创建团队 Plugin

```
team-plugin/
├── .claude-plugin/manifest.json
├── skills/
│   ├── code-style/
│   ├── api-patterns/
│   └── testing/
└── commands/
    └── deploy/
```

**发布流程**：
```bash
# 1. 发布到 GitHub
git push origin team-plugin

# 2. 成员添加 marketplace
claude plugin marketplace add https://github.com/team/team-plugin

# 3. 全局安装
claude plugin install team-plugin@team --scope user
```

### 新增命令

安装后，你将获得以下斜杠命令：

```
/superpowers:brainstorm    # 交互式设计优化
/superpowers:write-plan    # 创建实现计划
/superpowers:execute-plan  # 分批执行计划
```

### 如何使用 Superpowers

**方式一：完全自动化（推荐）**

直接请求开发任务，superpowers 会自动触发工作流：

```
用户：帮我实现一个用户认证功能
Claude：[自动执行 brainstorming → write-plan → execute-plan]
```

**方式二：逐步控制**

使用斜杠命令手动控制流程：

```
# 1. 先头脑风暴
用户：/superpowers:brainstorm 我需要设计一个用户认证系统

# 2. 查看计划
用户：/superpowers:write-plan

# 3. 执行计划
用户：/superpowers:execute-plan
```

**方式三：项目特定工作流**

某些任务如代码审查、部署，会自动触发相应技能。

### 工作流说明

| 阶段 | 说明 | 自动触发？ |
|--------|------|-----------|
| brainstorming | 通过问题优化设计 | 否，需主动使用 |
| using-git-worktrees | 创建隔离工作空间 | 否，需主动使用 |
| writing-plans | 将工作分解为任务 | 写代码时自动 |
| subagent-driven-development | 多智能体协作开发 | 写代码时自动 |
| test-driven-development | RED-GREEN-REFACTOR TDD | 写代码时自动 |
| receiving-code-review | 接收代码审查反馈 | 代码审查时自动 |
| requesting-code-review | 请求代码审查 | 完成任务时自动 |

### 核心理念

- **RED-GREEN-REFACTOR TDD**：先写失败测试，通过测试，再重构
- **YAGNI**：You Aren't Gonna Need It - 不做不必要的事
- **DRY**：Don't Repeat Yourself - 避免重复代码
- **验证优于声明**：修复后验证，而不是口头声明完成

## 安装示例：Superpowers Plugin

**场景**：将 superpowers 插件安装到 user 作用域（全局可用）

```bash
# 1. 安装插件到 user 作用域
claude plugin install superpowers --scope user

# 2. 验证安装结果
claude plugin list
```

**预期输出**：
```
Installed plugins:

  ❯ superpowers@superpowers-marketplace
    Version: 4.1.1
    Scope: user
    Status: ✔ enabled

  ❯ ui-ux-pro-max@ui-ux-pro-max-skill
    Version: 2.0.1
    Scope: user
    Status: ✔ enabled
```

## 最佳实践

| 原则 | 说明 |
|--------|------|
| 单一职责 | 每个 plugin 专注一个领域 |
| 版本管理 | 遵循 SemVer，记录变化 |
| 文档完善 | README + 使用示例 |
| 定期清理 | 禁用/卸载不用的插件 |

## 相关文档

- [配置层级概览](00-README.md)
- [Skills 配置](01-skills.md)
- [MCP 配置](03-mcp.md)
