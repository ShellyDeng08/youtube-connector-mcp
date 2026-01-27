# Skills 技能配置

## 什么是 Skills

Skills 是模块化的包，提供专业知识、工作流程和工具来扩展 Claude 的能力。将 Claude 从通用智能体转变为具备特定知识的专用智能体。

## 目录结构

```
.claude/skills/
└── my-skill/
    ├── SKILL.md           # 必需：技能定义
    ├── scripts/           # 可选：可执行脚本
    ├── references/        # 可选：参考文档
    └── assets/            # 可选：输出资源
```

## SKILL.md 格式

```markdown
---
name: skill-name
description: 技能描述，说明何时使用
---

# 技能内容

这里是使用说明...
```

**必需字段**：
- `name`: 技能名称
- `description`: 技能描述和触发条件

## 可选资源

| 资源类型 | 用途 | 示例 |
|----------|------|------|
| `scripts/` | 可执行代码 | `rotate_pdf.py` |
| `references/` | 参考文档 | `api_docs.md` |
| `assets/` | 输出资源 | `logo.png`、`template.html` |

## 核心原则

### 1. 简洁
- SKILL.md 保持在 500 行以内
- 只添加 Claude 没有的上下文
- 优先用简洁示例

### 2. 适当自由度

| 自由度 | 使用场景 |
|--------|----------|
| 高自由度（文本） | 多种方法都有效 |
| 中等自由度（脚本） | 有首选模式 |
| 低自由度（固定脚本） | 操作必须严格遵循 |

## 共享 Skills

### 方法一：复制文件夹

```bash
cp -r source-project/.claude/skills/ destination-project/.claude/skills/
```

### 方法二：通过 Plugin（推荐）

将 Skills 打包成 Plugin 后通过 Marketplace 分发。详见 [Plugins 配置](02-plugins.md)。

## 案例：代码审查 Skill

**需求**：团队统一代码审查标准

**方案**：创建 `code-review-skill`

```
.claude/skills/code-review/
├── SKILL.md           # 审查流程
└── references/
    ├── checklist.md     # 检查清单
    └── standards.md    # 团队标准
```

**共享**：
```bash
cp -r team-skills/code-review/ project-a/.claude/skills/
cp -r team-skills/code-review/ project-b/.claude/skills/
```

## 相关文档

- [配置层级概览](00-README.md)
- [Plugins 配置](02-plugins.md)
- [MCP 配置](03-mcp.md)
