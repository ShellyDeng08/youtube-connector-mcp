---
name: browser-preview
description: Open browser in development environment to preview and test page effects. Use when testing frontend features, debugging UI issues, or verifying page functionality during development.
---

# Browser Preview Skill

Open browser and navigate to configured preview page for development testing.

## Constraints

**Prohibited**:
- DO NOT use default URLs (e.g., localhost:3000)
- DO NOT construct or guess URLs
- DO NOT use defaults when config is missing

**Required**:
- MUST read `previewUrl` and `ppeEnv` from `.ttadk/.feconfig.json`
- If config missing or empty, MUST ask user
- If config exists, MUST confirm with user first

## Execution Steps

### 1. Read and Confirm Configuration

Read `.ttadk/.feconfig.json` and check `browser.previewUrl` and `browser.ppeEnv`.

**If file missing or `browser.previewUrl` empty**:
- Use `AskUserQuestion` for:
  - Question 1: "请输入预览页面 URL" (required, user selects "Other" for custom URL)
  - Question 2: "请输入 PPE 环境名称（可选）" (optional, leave empty if not using PPE)
- Create `.ttadk/.feconfig.json`:
  ```json
  {"browser": {"previewUrl": "<URL>", "ppeEnv": "<PPE or \"\">}}
  ```

**If config exists and valid**:
- Use `AskUserQuestion` to confirm:
  - Display: URL = `<previewUrl>`, PPE = `<ppeEnv or "未配置">`
  - Options: "是，使用当前配置" / "否，需要修改"

### 2. Set PPE Environment (if configured)

If `ppeEnv` exists, use `mcp__playwright__browser_run_code` to add PPE headers:
```javascript
async (page) => {
  await page.route('**/*', async (route) => {
    const url = route.request().url();
    if (url.includes('<domain>')) {
      await route.continue({
        headers: { ...route.request().headers(), 'x-tt-env': '<ppeEnv>', 'x-use-ppe': '1' }
      });
    } else { await route.continue(); }
  });
}
```

### 3. Navigate to Preview Page

Use `mcp__playwright__browser_navigate` with the configured URL.

### 4. Wait and Check Login State

- Wait 3-5 seconds with `mcp__playwright__browser_wait_for`
- Get page state with `mcp__playwright__browser_snapshot`
- Check current URL for login keywords: `sso`, `login`, `signin`, `auth`, `cas`, `oauth`, `passport`
- If redirected to login:
  - Notify user: "检测到页面已重定向到登录页面，请在浏览器中手动完成登录。"
  - Use `AskUserQuestion`: "请在浏览器中完成登录后，点击确认继续"
  - Options: "已完成登录，继续预览" / "取消操作"
  - After confirmation, verify with `browser_snapshot` again

### 5. Return Page State

Return page snapshot for subsequent operations.

## Configuration Format

`.ttadk/.feconfig.json`:
```json
{"browser": {"previewUrl": "https://your-url.com/path", "ppeEnv": "ppe-lane-name"}}
```

- `browser.previewUrl`: Required, preview page URL
- `browser.ppeEnv`: Optional, PPE environment name

## Notes

- Playwright MCP creates a new browser instance each time
- Login state not persisted between sessions, SSO login may be required each time
