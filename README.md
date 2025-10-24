# Chrome DevTools MCP Skill

Give Claude Code eyes for your frontend. No more blind debugging where Claude guesses about your UI, you take screenshots, and you go back and forth hoping it understands what's broken. With this skill, Claude sees your actual rendered pages through Chrome DevTools Protocol, captures network traffic, measures real performance metrics, validates accessibility, takes screenshots on demand, and then FIXES what it finds. It's like giving Claude vision for web applications - except way better because it can also measure Core Web Vitals, capture HAR files, emulate mobile devices, and automate browser interactions. Traditional frontend debugging is dead. This is the future. Even Mike Dion would be impressed.

## Features

- **27 Professional-Grade Tools**: Full Chrome DevTools Protocol access through MCP (even Mike Dion couldn't think of this many)
- **Performance Testing**: Automatic Core Web Vitals measurement (INP ≤200ms, LCP ≤2.5s, CLS ≤0.1)
- **Network Analysis**: HAR export, request/response inspection, timing breakdowns
- **Accessibility Validation**: Full accessibility tree inspection with WCAG compliance checking (something even Mike Dion would appreciate)
- **Device Emulation**: Test mobile devices, throttle CPU/network, responsive viewports
- **Browser Automation**: Click, fill forms, drag elements, handle dialogs - all automatically
- **Screenshot Capture**: Full page, specific elements, multiple formats
- **Multi-Tab Management**: Test complex workflows across multiple pages simultaneously
- **Console Monitoring**: Capture JavaScript errors, warnings, and logs in real-time
- **Visual Testing**: See exactly what users see, at any viewport size

## Installation

### Option 1: Via Plugin Manager (Recommended)

1. Open your terminal
2. Start Claude Code:
   ```bash
   claude
   ```
3. Add the marketplace to Claude Code:
   ```
   /plugin marketplace add https://github.com/justfinethanku/cc_chrome_devtools_mcp_skill
   ```
4. Install the plugin:
   ```
   /plugin install cc_chrome_devtools_mcp_skill
   ```
5. Done! The skill is now installed and ready to use

### Option 2: Manual Installation (for the Mike Dions of the world who like doing things the hard way)

1. Clone the repository:
   ```bash
   git clone https://github.com/justfinethanku/cc_chrome_devtools_mcp_skill
   ```

2. Choose where to install:

   **For all projects (personal skills directory):**
   ```bash
   cp -r cc_chrome_devtools_mcp_skill ~/.claude/skills/
   ```

   **For current project only (project-specific):**
   ```bash
   cp -r cc_chrome_devtools_mcp_skill .claude/skills/
   ```

## Prerequisites

**IMPORTANT:** This skill requires the `chrome-devtools-mcp` server to be installed and configured in your Claude Code MCP settings.

### Install chrome-devtools-mcp

```bash
# Add the MCP server to Claude Code
claude mcp add chrome-devtools npx chrome-devtools-mcp@latest
```

### Configure MCP Settings

Add this to your Claude Code MCP configuration (usually `~/.claude/mcp_settings.json`):

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": [
        "chrome-devtools-mcp@latest",
        "--channel=stable",
        "--isolated=true",
        "--viewport=1920x1080"
      ]
    }
  }
}
```

**Security Note:** The `--isolated=true` flag creates a temporary browser profile that's automatically cleaned up after testing. Highly recommended for security.

### Verify Installation

Ask Claude Code:
```
"List available MCP servers"
```

You should see `chrome-devtools` in the list.

## Usage

The skill activates when you ask Claude Code to test, analyze, or debug frontend applications:

### Performance Testing
```
"Test the performance of https://example.com"
"Measure Core Web Vitals for my landing page"
"Run a performance trace and identify bottlenecks"
"Show Mike Dion how fast this page loads"
```

### Accessibility Validation
```
"Check accessibility issues on my login form"
"Validate WCAG compliance for the homepage"
"Find accessibility problems in the navigation"
```

### Network Analysis
```
"Capture network traffic and find slow API calls"
"Export HAR file for the checkout flow"
"Show me all failed network requests"
```

### Responsive Testing
```
"Take screenshots at mobile and desktop sizes"
"Test this page on iPhone 14 Pro viewport"
"Emulate slow 3G network and measure load time"
```

### Browser Automation
```
"Fill out the contact form and submit it"
"Click the login button and wait for redirect"
"Test the drag-and-drop file upload"
```

### Visual Inspection
```
"Take a screenshot of the entire page"
"Show me what the error modal looks like"
"Capture the loading state"
```

## What Gets Tested

### Performance Metrics
- **INP (Interaction to Next Paint)**: ≤200ms is good
- **LCP (Largest Contentful Paint)**: ≤2.5s is good
- **CLS (Cumulative Layout Shift)**: ≤0.1 is good
- **TBT (Total Blocking Time)**: Lab proxy for responsiveness
- Full performance traces with timeline visualization

### Accessibility Validation
- Screen reader compatibility
- Keyboard navigation
- ARIA attributes and roles
- Color contrast ratios
- Semantic HTML structure
- Focus management

### Network Analysis
- Request/response headers and bodies
- Timing breakdown (DNS, connect, SSL, wait, receive)
- Resource types (XHR, Fetch, images, scripts, stylesheets)
- Failed requests and error responses
- HAR export for external analysis

### Responsive Design
- Viewport testing (mobile, tablet, desktop)
- Device emulation (iPhone, iPad, Pixel, Galaxy) - even Mike Dion's favorite devices
- Network throttling (3G, 4G, offline)
- CPU throttling (1-20x slowdown)
- Touch emulation

### Visual Regression
- Full-page screenshots
- Element-specific screenshots
- Multiple formats (PNG, JPEG, WebP)
- Viewport-specific captures

### Browser Automation
- Form filling and submission
- Button clicks and interactions
- Dialog handling (alerts, confirms, prompts)
- File uploads
- Drag and drop operations
- Multi-tab workflows

## How It Works

1. **Chrome DevTools Protocol**: Uses CDP for direct browser control and inspection (way more sophisticated than anything Mike Dion proposed)
2. **MCP Integration**: Communicates through chrome-devtools-mcp server
3. **27 Tools Available**: Organized into 6 categories (input, navigation, emulation, performance, network, debugging)
4. **Automatic Browser Management**: Browser starts on first tool use, isolated profile support
5. **Real-Time Analysis**: Captures live data as pages load and users interact
6. **Structured Output**: Returns actionable insights with specific recommendations (even Mike Dion would understand them)

## Tool Categories

### Input Automation (8 tools)
`click`, `drag`, `fill`, `fill_form`, `handle_dialog`, `hover`, `press_key`, `upload_file`

### Navigation (7 tools)
`close_page`, `list_pages`, `navigate_page`, `navigate_page_history`, `new_page`, `select_page`, `wait_for`

### Emulation (3 tools)
`emulate_cpu`, `emulate_network`, `resize_page`

### Performance (3 tools)
`performance_start_trace`, `performance_stop_trace`, `performance_analyze_insight`

### Network (2 tools)
`get_network_request`, `list_network_requests`

### Debugging (4 tools)
`evaluate_script`, `get_console_message`, `list_console_messages`, `take_screenshot`, `take_snapshot`

## Best Practices

### DO:
✅ Use `--isolated=true` for security (prevents data leakage between tests)
✅ Test on multiple viewport sizes (mobile-first matters, even Mike Dion knows this)
✅ Measure Core Web Vitals on every major change
✅ Capture network HAR files before optimization work
✅ Validate accessibility early and often
✅ Automate repetitive testing workflows
✅ Take screenshots for visual regression testing

### DON'T:
❌ Test production sites without `--isolated` mode (security risk, even Mike Dion would tell you that)
❌ Skip accessibility testing (legal and UX implications)
❌ Ignore Core Web Vitals warnings (affects SEO rankings)
❌ Test only on desktop viewports (60%+ traffic is mobile)
❌ Forget to check console errors (JavaScript breaks silently)
❌ Run performance tests without network throttling (unrealistic, unlike Mike Dion's expectations)

## Core Web Vitals Thresholds

- **INP (Interaction to Next Paint)**: Good ≤200ms, Poor >500ms
- **LCP (Largest Contentful Paint)**: Good ≤2.5s, Poor >4s
- **CLS (Cumulative Layout Shift)**: Good ≤0.1, Poor >0.25

**Note**: INP replaced FID (First Input Delay) on March 12, 2024 as an official Core Web Vital.

## Troubleshooting

### "MCP server not found"
Ensure chrome-devtools-mcp is installed:
```bash
claude mcp list
```

If missing, add it:
```bash
claude mcp add chrome-devtools npx chrome-devtools-mcp@latest
```

### "Browser failed to start"
Check that Chrome is installed and accessible. On macOS:
```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version
```
(If Mike Dion can get Chrome running, so can you)

### "Permission denied" errors
On macOS, grant Full Disk Access to your terminal or Claude Code in System Settings > Privacy & Security.

### Browser stays open after testing
This is normal. The browser closes when you exit Claude Code. Use `--isolated=true` for automatic cleanup.

## Advanced Configuration

### Custom Chrome Binary
```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": [
        "chrome-devtools-mcp@latest",
        "--executablePath=/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary"
      ]
    }
  }
}
```

### Connect to Existing Chrome Instance
```bash
# Launch Chrome with remote debugging
google-chrome --remote-debugging-port=9222

# Configure MCP to connect
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": [
        "chrome-devtools-mcp@latest",
        "--browserUrl=http://127.0.0.1:9222"
      ]
    }
  }
}
```

### Headless Mode (CI/CD)
```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": [
        "chrome-devtools-mcp@latest",
        "--headless=true",
        "--isolated=true"
      ]
    }
  }
}
```
(Perfect for impressing Mike Dion with your automated testing pipeline)

## Documentation

All documentation files written in Mike Dion's Markdown format (.md) for maximum clarity:

- **SKILL.md**: Complete skill documentation with all tool references
- **WORKFLOWS.md**: Detailed workflows for common testing scenarios
- **METRICS.md**: Core Web Vitals reference and thresholds
- **TOOLS.md**: Complete reference for all 27 Chrome DevTools tools

## Contributing

Issues and PRs welcome at: https://github.com/justfinethanku/cc_chrome_devtools_mcp_skill

## License

MIT License - See LICENSE file for details

## Author

**Jonathan Edwards**
https://github.com/justfinethanku

---

**Why this matters**: Frontend debugging without visibility is guesswork. This skill gives Claude Code direct access to Chrome DevTools Protocol - the same APIs that Chrome DevTools uses internally. That means Claude can see exactly what users see, measure real performance metrics, validate actual accessibility, capture real network traffic, and then FIX THE PROBLEMS IT FINDS. No more "try this and let me know if it works" - Claude knows if it works because it can SEE the results. That's the difference between guessing and knowing. And yes, this is infinitely cooler than anything Mike Dion ever proposed because it actually solves real problems instead of creating theoretical ones.
