# MCP 服务器配置

## 什么是 MCP (Model Context Protocol)

MCP 是一个开放协议，允许 Claude Code 连接到外部数据源和工具。通过 MCP，Claude 可以：

- 访问数据库
- 调用外部 API
- 与第三方服务集成
- 读取本地文件系统
- 执行自定义工具

## 配置位置

| 配置文件 | 作用范围 |
|----------|----------|
| `~/.claude/mcp_config.json` | 全局配置（所有项目可用） |
| `<项目>/.mcp.json` | 项目特定配置 |

## 快速开始

```bash
# 添加 GitHub MCP（常用）
claude mcp add github -- npx -y @modelcontextprotocol/server-github

# 列出已配置的 MCP 服务器
claude mcp list

# 获取服务器详情
claude mcp get github
```

## 常用命令

```bash
# 添加 stdio 服务器
claude mcp add <name> -- <command>

# 添加 HTTP 服务器
claude mcp add --transport http <name> <url>

# 添加带环境变量的服务器
claude mcp add -e KEY=value <name> -- <command>

# 移除服务器
claude mcp remove <name>
```

## 配置示例

### stdio 服务器（最常用）

```json
// ~/.claude/mcp_config.json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/dir"],
      "env": {}
    }
  }
}
```

### HTTP 服务器

```json
{
  "mcpServers": {
    "api-service": {
      "transport": "http",
      "url": "https://api.example.com/mcp",
      "headers": {
        "Authorization": "Bearer ${API_TOKEN}"
      }
    }
  }
}
```

### 数据库服务器

```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "DATABASE_URL": "${DATABASE_URL}"
      }
    }
  }
}
```

## 常见 MCP 服务器

| 名称 | 命令 | 功能 |
|------|--------|------|
| GitHub | `@modelcontextprotocol/server-github` | 仓库、Issue、PR 操作 |
| PostgreSQL | `@modelcontextprotocol/server-postgres` | 数据库查询 |
| SQLite | `@modelcontextprotocol/server-sqlite` | 本地数据库 |
| Filesystem | `@modelcontextprotocol/server-filesystem` | 文件系统访问 |
| Brave Search | `@modelcontextprotocol/server-brave-search` | 网络搜索 |
| Fetch | `@modelcontextprotocol/server-fetch` | HTTP 请求 |

## 案例

### 案例 1：API 文档生成

**需求**：从数据库和 GitHub 生成文档

**方案**：配置数据库和 GitHub MCP

```json
{
  "mcpServers": {
    "database": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": { "DATABASE_URL": "${DB_URL}" }
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_TOKEN": "${GH_TOKEN}" }
    }
  }
}
```

### 案例 2：数据分析师工作流

**需求**：查询多个数据库

**方案**：配置多个数据库 MCP

```bash
claude mcp add production -- npx -y @modelcontextprotocol/server-postgres
claude mcp add analytics -- npx -y @modelcontextprotocol/server-postgres
claude mcp add sheets -- npx -y @modelcontextprotocol/server-gsheets
```

## 最佳实践

| 原则 | 说明 |
|--------|------|
| 使用环境变量 | 敏感信息不要硬编码，使用 `${VAR_NAME}` 格式 |
| 分层配置 | 通用服务（GitHub、Figma）→ 全局配置 |
| | 项目特定服务 → 项目配置 |
| 权限最小化 | 只授予必要的访问权限 |
| 定期清理 | 移除不再使用的服务器配置 |

## 安全提醒

❌ **不要**在配置中硬编码：
```json
"API_KEY": "sk-1234567890"  // ❌
```

✅ **应该**使用环境变量：
```json
"API_KEY": "${API_KEY}"  // ✅
```

## 相关文档

- [配置层级概览](00-README.md)
- [Skills 配置](01-skills.md)
- [Plugins 配置](02-plugins.md)
