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
claude mcp add chrome-devtools -- npx -y chrome-devtools-mcp@latest --isolated=true
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

**Security note:** When MCP launches Chrome, `--isolated=true` creates a temporary profile that is cleaned up after the browser closes. It does not redact data exposed to MCP clients or isolate an existing browser attached through `--browserUrl` or `--wsEndpoint`. See [Security considerations](SKILL.md#security-considerations) before testing authenticated pages or exporting captures.

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
✅ Use `--isolated=true` when MCP launches Chrome to keep test profiles separate
✅ Test on multiple viewport sizes (mobile-first matters, even Mike Dion knows this)
✅ Measure Core Web Vitals on every major change
✅ Capture network HAR files before optimization work
✅ Validate accessibility early and often
✅ Automate repetitive testing workflows
✅ Take screenshots for visual regression testing

### DON'T:
❌ Assume isolated mode hides credentials, page content, or network captures from MCP clients
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
claude mcp add chrome-devtools -- npx -y chrome-devtools-mcp@latest --isolated=true
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
        "--executablePath=/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary",
        "--isolated=true"
      ]
    }
  }
}
```

### Connect to Existing Chrome Instance

Attachment gives MCP access to that browser's existing tabs, cookies, and sessions.
`--isolated=true` does not create a temporary profile when attaching. For a separate
test browser on Linux, create a fresh profile before enabling remote debugging:

```bash
CHROME_TEST_PROFILE="$(mktemp -d "${TMPDIR:-/tmp}/chrome-devtools-test.XXXXXX")"
printf 'Test profile: %s\n' "$CHROME_TEST_PROFILE"
google-chrome --remote-debugging-address=127.0.0.1 --remote-debugging-port=9222 --user-data-dir="$CHROME_TEST_PROFILE"
```

Chrome 136 and later require a non-default user data directory for these debugging
switches. The local debugging port lets other applications on your machine control
this test browser. Keep it on loopback and use test accounts. After closing the test
browser, remove the printed test profile directory if you no longer need it; MCP
does not clean up profiles belonging to an externally launched browser.

Configure MCP to attach to that test browser:

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": [
        "-y",
        "chrome-devtools-mcp@latest",
        "--browserUrl=http://127.0.0.1:9222"
      ]
    }
  }
}
```

See the [official connection guide](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/advanced-usage.md#connecting-to-a-running-chrome-instance)
and [Chrome's remote debugging requirements](https://developer.chrome.com/blog/remote-debugging-port).

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

- **[SKILL.md](SKILL.md)**: Task entrypoint and essential security guidance
- **[GUIDE.md](GUIDE.md)**: Setup, configuration examples, constraints, and background
- **WORKFLOWS.md**: Detailed workflows for common testing scenarios
- **METRICS.md**: Core Web Vitals reference and thresholds
- **TOOLS.md**: Complete reference for all 27 Chrome DevTools tools

## Plugin structure and validation

This repository ships one instruction skill. Claude Code loads the root
[SKILL.md](SKILL.md); its supporting Markdown files stay beside it so both
marketplace and manual skill installs use the same content.

The entrypoint links to supporting documents for conditional reading, so routine
browser tasks do not load the full setup and example guide. This follows
[Claude Code's supporting-file guidance](https://code.claude.com/docs/en/skills#add-supporting-files).
Reading every reference still loads its full content; this changes the default
instruction payload, not the external MCP server or browser speed.

[plugin.json](.claude-plugin/plugin.json) owns plugin metadata and the release
version. [marketplace.json](.claude-plugin/marketplace.json) maps the published
plugin name to this repository root and reads its metadata from that manifest.
Bump the version in `plugin.json` when releasing an update.

Configure the MCP server separately. The external `chrome-devtools-mcp` process
supplies tools and manages the Chrome connection,
as described in [Prerequisites](#prerequisites).

For local packaging checks, run these from the repository root:

```bash
claude plugin validate .
claude --plugin-dir . plugin details cc_chrome_devtools_mcp_skill
```

The details should show one skill, `cc_chrome_devtools_mcp_skill`, and zero bundled
MCP servers. See the official [manifest reference](https://code.claude.com/docs/en/plugins/manifest-reference)
and [component loading rules](https://code.claude.com/docs/en/plugins/components#skills).

### Automated package tests

With Python 3.9+ and Claude Code installed, run from the repository root:

```bash
python3 -m unittest discover -s tests -v
```

The suite checks direct loading from an arbitrarily named checkout, local
marketplace discovery and installation, the installed skill inventory and file
contents, manual-copy reference availability, and rejection of invalid metadata.
It creates temporary home and Claude configuration directories and removes them
after each test. It runs plugin management commands only; no model calls, MCP
server or Chrome session are started. A missing Claude CLI fails the installation
tests; set `CLAUDE_BIN` if its executable has a different name or path.

These checks cover this instruction package. They do not verify the external
MCP server's tools, browser behavior or the accuracy of every workflow example.

## Contributing

Issues and PRs welcome at: https://github.com/justfinethanku/cc_chrome_devtools_mcp_skill

## License

MIT License - See LICENSE file for details

## Author

**Jonathan Edwards**
https://github.com/justfinethanku

---

**Why this matters**: Frontend debugging without visibility is guesswork. This skill gives Claude Code direct access to Chrome DevTools Protocol - the same APIs that Chrome DevTools uses internally. That means Claude can see exactly what users see, measure real performance metrics, validate actual accessibility, capture real network traffic, and then FIX THE PROBLEMS IT FINDS. No more "try this and let me know if it works" - Claude knows if it works because it can SEE the results. That's the difference between guessing and knowing. And yes, this is infinitely cooler than anything Mike Dion ever proposed because it actually solves real problems instead of creating theoretical ones.
