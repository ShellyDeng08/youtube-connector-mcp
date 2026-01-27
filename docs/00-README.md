# Claude Code 配置指南

本指南介绍 Skills、Plugins 和 MCP 的配置和使用方法，适用于团队技术分享。

## 快速导航

| 文档 | 内容 |
|------|------|
| [01-skills.md](01-skills.md) | Skills - 工作流程和领域知识 |
| [02-plugins.md](02-plugins.md) | Plugins - 安装、管理和创建 |
| [03-mcp.md](03-mcp.md) | MCP - 外部数据源和工具 |
| [04-examples.md](04-examples.md) | 案例 - 6 个实际应用场景 |
| [05-best-practices.md](05-best-practices.md) | 最佳实践 - 安全和高效配置 |

## 一图胜千言

```
┌─────────────────────────────────────────────────────────────┐
│                     Claude Code                        │
├─────────────────────────────────────────────────────────────┤
│                                                        │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐ │
│  │  Skills  │    │ Plugins  │    │   MCP    │ │
│  │  工作流程  │◄───│  分发    │◄───│  数据源   │ │
│  │  领域知识  │    │  管理    │    │  外部API  │ │
│  └──────────┘    └──────────┘    └──────────┘ │
│         │                                    │       │
│         └────────────┬─────────────────────┘       │
│                      │                             │
│              根据需求选择合适的工具              │
│                                                        │
└─────────────────────────────────────────────────────────────┘
```

## 三者对比

| 特性 | Skills | Plugins | MCP |
|------|--------|----------|-----|
| **用途** | 工作流程、领域知识 | 分发和管理 | 数据访问、外部 API |
| **分发** | 复制或通过 Plugin | Marketplace 安装 | 手动配置 |
| **内容** | 单个技能 | 多个组件 | 数据源配置 |
| **作用域** | 项目或跟随 Plugin | user 或 project | 全局或项目 |
| **版本** | 无 | 支持版本 | 无 |

## 快速开始

```bash
# 1. 安装 Plugin（全局）
claude plugin install plugin-name --scope user

# 2. 配置 MCP
claude mcp add github -- npx -y @modelcontextprotocol/server-github

# 3. 列出已配置
claude plugin list
claude mcp list
```

## 配置层级

| 位置 | 作用范围 | 用途 |
|------|----------|------|
| `~/.claude/settings.json` | 全局 | Plugin 作用域 |
| `<项目>/.claude/settings.json` | 项目 | 项目特定设置 |
| `<项目>/.claude/skills/` | 项目 | 本地 Skills |
| `~/.claude/mcp_config.json` | 全局 | 通用 MCP 服务器 |
| `<项目>/.mcp.json` | 项目 | 项目特定 MCP 服务器 |

## 选择建议

| 场景 | 推荐方案 |
|------|----------|
| 团队共享工作流程 | [Plugin + Skills](02-plugins.md) |
| 访问外部数据 | [MCP](03-mcp.md) |
| 项目特定需求 | [.mcp.json + Skills](04-examples.md) |
| 通用工具集 | [Plugin user scope](02-plugins.md) |

## 安全提醒

❌ **不要**在文档中硬编码：
- API keys
- Tokens
- 密码
- 任何敏感情感

✅ **应该**使用：
- 环境变量 `${VAR_NAME}`
- `.env` 文件（不提交到 git）
- 配置管理工具

```json
// 错误示例
"API_KEY": "sk-1234567890"

// 正确示例
"API_KEY": "${API_KEY}"
```

## 相关资源

- [Claude Code 文档](https://docs.anthropic.com)
- [MCP 协议规范](https://modelcontextprotocol.io)
- [Claude Code GitHub](https://github.com/anthropics/claude-code)
