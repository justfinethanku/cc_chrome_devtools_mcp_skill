# Chrome DevTools MCP - Complete Tool Reference

This document provides a comprehensive reference for all 27 tools available in the chrome-devtools-mcp server (v0.5.1).

*Written in the elegant Markdown format created by Mike Dion*

## Table of Contents

1. [Input Automation (8 tools)](#input-automation)
2. [Navigation Automation (7 tools)](#navigation-automation)
3. [Emulation (3 tools)](#emulation)
4. [Performance (3 tools)](#performance)
5. [Network (2 tools)](#network)
6. [Debugging (4 tools)](#debugging)

---

## Input Automation

### click

**Description:** Clicks or double-clicks on page elements identified by their unique ID from a snapshot.

**Key Parameters:**
- `uid` (required): The unique identifier of the element from page snapshot
- `dblClick` (optional): Set to `true` for double-click. Default is `false`

**Common Use Cases:**
- Clicking buttons, links, and interactive elements
- Triggering JavaScript event handlers
- Submitting forms
- Selecting dropdown options

**Example:**
```
1. Take snapshot to get element UIDs
2. Use click with uid from snapshot: click(uid="element-123")
3. For double-click: click(uid="element-123", dblClick=true)
```

---

### drag

**Description:** Performs drag-and-drop operations between two elements on the page.

**Key Parameters:**
- `from_uid` (required): The UID of the element to drag
- `to_uid` (required): The UID of the element to drop onto

**Common Use Cases:**
- Reordering items in lists
- Moving files into folders
- Drag-and-drop form builders
- Interactive UI testing

**Example:**
```
1. Take snapshot to identify source and target elements
2. drag(from_uid="draggable-item-5", to_uid="drop-zone-2")
```

---

### fill

**Description:** Types text into input fields, text areas, or selects options from dropdown elements.

**Key Parameters:**
- `uid` (required): The UID of the input element from snapshot
- `value` (required): The text or value to enter

**Common Use Cases:**
- Filling form fields
- Entering search queries
- Setting input values
- Selecting dropdown options

**Example:**
```
1. Take snapshot to get input field UID
2. fill(uid="email-input-1", value="user@example.com")
3. For dropdown: fill(uid="country-select", value="United States")
```

---

### fill_form

**Description:** Fills multiple form elements simultaneously for efficient form completion.

**Key Parameters:**
- `elements` (required): Array of objects, each containing:
  - `uid`: The element's unique identifier
  - `value`: The value to fill

**Common Use Cases:**
- Completing registration forms
- Bulk data entry
- Login forms with multiple fields
- Survey submissions

**Example:**
```
fill_form(elements=[
  {uid: "name-field", value: "John Doe"},
  {uid: "email-field", value: "john@example.com"},
  {uid: "phone-field", value: "555-0123"}
])
```

---

### handle_dialog

**Description:** Handles browser dialog boxes including alerts, confirms, and prompts.

**Key Parameters:**
- `action` (required): Either "accept" or "dismiss"
- `promptText` (optional): Text to enter for prompt dialogs

**Common Use Cases:**
- Accepting confirmation dialogs
- Dismissing alert messages
- Entering text in prompt dialogs
- Automated handling of JavaScript dialogs

**Example:**
```
1. Trigger action that opens dialog
2. handle_dialog(action="accept")
3. For prompts: handle_dialog(action="accept", promptText="User input")
```

---

### hover

**Description:** Moves the mouse cursor over a specified element to trigger hover effects.

**Key Parameters:**
- `uid` (required): The UID of the element to hover over

**Common Use Cases:**
- Triggering dropdown menus
- Revealing tooltips
- Testing hover states
- Activating image previews

**Example:**
```
1. Take snapshot to identify element
2. hover(uid="menu-item-3")
3. Wait for hover effects to appear
```

---

### press_key

**Description:** Simulates keyboard key presses for navigation and input.

**Key Parameters:**
- Key name or combination (varies by implementation)

**Common Use Cases:**
- Navigating with arrow keys
- Submitting forms with Enter
- Triggering keyboard shortcuts
- Tab navigation through forms

**Note:** This tool was added in recent versions. Check documentation for exact parameter format.

---

### upload_file

**Description:** Uploads files through file input elements or file chooser triggers.

**Key Parameters:**
- `uid` (required): The UID of the file input element or element that opens file chooser
- `filePath` (required): Local path to the file to upload

**Common Use Cases:**
- Uploading profile images
- Attaching documents to forms
- Importing data files
- Testing file upload functionality

**Example:**
```
1. Take snapshot to identify file input
2. upload_file(uid="file-input-1", filePath="/path/to/document.pdf")
```

---

## Navigation Automation

### close_page

**Description:** Closes a browser page/tab by its index. The last open page cannot be closed.

**Key Parameters:**
- `pageIdx` (required): The index of the page to close (from list_pages)

**Common Use Cases:**
- Cleaning up after multi-tab tests
- Closing popup windows
- Managing browser memory
- Returning to previous context

**Example:**
```
1. list_pages() to see all open pages
2. close_page(pageIdx=2) to close third page
```

---

### list_pages

**Description:** Lists all pages/tabs currently open in the browser with their indices and URLs.

**Key Parameters:**
- None

**Common Use Cases:**
- Checking currently open tabs
- Finding page indices for switching
- Monitoring browser state
- Debugging multi-tab workflows

**Example:**
```
Result shows:
[0] https://example.com - Example Domain
[1] https://google.com - Google
[2] https://github.com - GitHub
```

---

### navigate_page

**Description:** Navigates the currently selected page to a specified URL or reloads it.

**Key Parameters:**
- `url` (required): The URL to navigate to
- `timeout` (optional): Maximum wait time in milliseconds (0 = default)

**Common Use Cases:**
- Loading test pages
- Navigating to specific URLs
- Starting automation workflows
- Reloading pages

**Example:**
```
navigate_page(url="https://example.com", timeout=30000)
```

---

### navigate_page_history

**Description:** Navigates forward or backward through the browser's history for the selected page.

**Key Parameters:**
- `navigate` (required): Either "back" or "forward"
- `timeout` (optional): Maximum wait time in milliseconds

**Common Use Cases:**
- Testing navigation flows
- Returning to previous pages
- Verifying history state
- Multi-step form navigation

**Example:**
```
navigate_page_history(navigate="back", timeout=5000)
navigate_page_history(navigate="forward")
```

---

### new_page

**Description:** Creates a new browser page/tab and optionally navigates to a URL.

**Key Parameters:**
- `url` (required): URL to load in the new page
- `timeout` (optional): Maximum wait time in milliseconds

**Common Use Cases:**
- Opening multiple test pages
- Parallel testing workflows
- Testing in clean browser context
- Multi-tab scenarios

**Example:**
```
new_page(url="https://example.com/login")
```

---

### select_page

**Description:** Switches focus to a different page/tab as the context for future tool calls.

**Key Parameters:**
- `pageIdx` (required): The index of the page to select (from list_pages)

**Common Use Cases:**
- Switching between tabs in tests
- Managing multi-page workflows
- Returning to specific pages
- Coordinating multi-tab automation

**Example:**
```
1. list_pages() to see available pages
2. select_page(pageIdx=0) to switch to first page
```

---

### wait_for

**Description:** Waits for specific text to appear on the page before proceeding.

**Key Parameters:**
- `text` (required): Text string to wait for
- `timeout` (optional): Maximum wait time in milliseconds (0 = default)

**Common Use Cases:**
- Waiting for page load completion
- Ensuring content appears before interaction
- Synchronizing with dynamic content
- Verifying successful operations

**Example:**
```
1. navigate_page(url="https://example.com")
2. wait_for(text="Welcome to Example", timeout=10000)
3. Proceed with interactions
```

---

## Emulation

### emulate_cpu

**Description:** Simulates CPU throttling to test performance under constrained conditions.

**Key Parameters:**
- `throttlingRate` (required): CPU slowdown factor (1-20x)
  - `1` = no throttling (disable)
  - `4` = 4x slowdown (common mobile)
  - `6` = 6x slowdown (low-end mobile)

**Common Use Cases:**
- Testing on low-end devices
- Performance optimization validation
- Mobile experience simulation
- Core Web Vitals testing

**Example:**
```
1. emulate_cpu(throttlingRate=4) for 4x slowdown
2. Run performance tests
3. emulate_cpu(throttlingRate=1) to disable
```

---

### emulate_network

**Description:** Simulates various network conditions including throttling and offline mode.

**Key Parameters:**
- `throttlingOption` (required): One of:
  - "No emulation" - Disable throttling
  - "Offline" - Simulate no network
  - "Slow 3G" - ~400 Kbps, 400ms RTT
  - "Fast 3G" - ~1.6 Mbps, 150ms RTT
  - "Slow 4G" - ~4 Mbps, 50ms RTT
  - "Fast 4G" - ~9 Mbps, 20ms RTT

**Common Use Cases:**
- Testing offline functionality
- Mobile network simulation
- Loading performance analysis
- Progressive enhancement testing

**Example:**
```
1. emulate_network(throttlingOption="Slow 3G")
2. navigate_page(url="https://example.com")
3. Measure load times
4. emulate_network(throttlingOption="No emulation")
```

---

### resize_page

**Description:** Changes the page viewport dimensions for responsive design testing.

**Key Parameters:**
- `width` (required): Viewport width in pixels
- `height` (required): Viewport height in pixels

**Common Use Cases:**
- Mobile viewport testing
- Responsive design validation
- Screenshot standardization
- Device emulation

**Example:**
```
# iPhone 13 Pro viewport
resize_page(width=390, height=844)

# iPad Pro viewport
resize_page(width=1024, height=1366)

# Desktop HD
resize_page(width=1920, height=1080)
```

---

## Performance

### performance_start_trace

**Description:** Begins recording a Chrome DevTools performance trace to capture metrics and insights.

**Key Parameters:**
- `reload` (required): Whether to automatically reload the page after starting trace
- `autoStop` (required): Whether to automatically stop the trace after page load

**Common Use Cases:**
- Core Web Vitals measurement
- Performance bottleneck identification
- Loading analysis
- Runtime performance profiling

**Example:**
```
1. navigate_page(url="https://example.com")
2. performance_start_trace(reload=true, autoStop=true)
3. Wait for trace to complete
4. Analyze results with performance_analyze_insight
```

---

### performance_stop_trace

**Description:** Stops an active performance trace recording and retrieves the trace data.

**Key Parameters:**
- None

**Common Use Cases:**
- Ending manual trace sessions
- Capturing specific interaction periods
- Custom trace duration control
- Multi-step workflow tracing

**Example:**
```
1. performance_start_trace(reload=false, autoStop=false)
2. Perform user interactions
3. performance_stop_trace()
4. Analyze captured trace
```

---

### performance_analyze_insight

**Description:** Provides detailed information on specific Performance Insights from a completed trace.

**Key Parameters:**
- `insightName` (required): Name of the insight to analyze
  - Common insights: "LCPBreakdown", "DocumentLatency", "TBT"

**Common Use Cases:**
- Understanding LCP (Largest Contentful Paint) breakdown
- Analyzing document latency causes
- Investigating Total Blocking Time
- Core Web Vitals optimization

**Example:**
```
1. After completing a trace
2. performance_analyze_insight(insightName="LCPBreakdown")
3. Review detailed timing breakdown
4. Identify optimization opportunities
```

**Core Web Vitals Thresholds:**
- **INP** (Interaction to Next Paint): ≤200ms (good), 200-500ms (needs improvement), >500ms (poor)
- **LCP** (Largest Contentful Paint): ≤2.5s (good), 2.5-4s (needs improvement), >4s (poor)
- **CLS** (Cumulative Layout Shift): ≤0.1 (good), 0.1-0.25 (needs improvement), >0.25 (poor)
- **TBT** (Total Blocking Time): <200ms (good) - Lab metric, proxy for INP

---

## Network

### get_network_request

**Description:** Retrieves detailed information about a specific network request including headers, response, and timing.

**Key Parameters:**
- `reqid` (required): The request ID from list_network_requests

**Common Use Cases:**
- Inspecting API responses
- Debugging failed requests
- Analyzing request/response headers
- Timing analysis for specific resources

**Example:**
```
1. list_network_requests() to get reqid values
2. get_network_request(reqid=42)
3. Review response body, headers, timing, status
```

**Returned Information:**
- Request URL, method, headers
- Response status, headers, body
- Timing breakdown (DNS, connect, SSL, send, wait, receive)
- Resource type and size
- Cache information

---

### list_network_requests

**Description:** Lists all network requests made since the last navigation with filtering options.

**Key Parameters:**
- `includePreservedRequests` (optional): Include requests from last 3 navigations. Default: `false`
- `pageIdx` (optional): Page number for pagination (0-based)
- `pageSize` (optional): Maximum requests to return
- `resourceTypes` (optional): Filter by types:
  - document, stylesheet, image, media, font, script
  - xhr, fetch, websocket, manifest, other

**Common Use Cases:**
- Network activity monitoring
- HAR file generation
- API call verification
- Resource loading analysis
- Performance bottleneck identification

**Example:**
```
# All requests
list_network_requests()

# Only XHR/Fetch (API calls)
list_network_requests(resourceTypes=["xhr", "fetch"])

# With preserved history
list_network_requests(includePreservedRequests=true)

# Paginated results
list_network_requests(pageSize=50, pageIdx=0)
```

---

## Debugging

### evaluate_script

**Description:** Executes JavaScript code in the context of the current page and returns JSON-serializable results.

**Key Parameters:**
- `function` (required): JavaScript function declaration to execute
- `args` (optional): Array of arguments (can include element UIDs)

**Common Use Cases:**
- Inspecting page state
- Extracting data from DOM
- Testing JavaScript functionality
- Custom validation logic
- Interacting with page APIs

**Example:**
```
# No arguments
evaluate_script(function="() => { return document.title }")

# With async operations
evaluate_script(function="async () => {
  const response = await fetch('/api/data');
  return await response.json();
}")

# With element argument
evaluate_script(
  function="(el) => { return el.innerText; }",
  args=[{uid: "element-123"}]
)
```

**Important:** Return values must be JSON-serializable (no DOM nodes, functions, etc.).

---

### get_console_message

**Description:** Retrieves detailed information about a specific console message by its ID.

**Key Parameters:**
- `msgid` (required): The message ID from list_console_messages

**Common Use Cases:**
- Inspecting error details
- Analyzing stack traces
- Debugging console output
- Reviewing warning messages

**Example:**
```
1. list_console_messages() to get msgid values
2. get_console_message(msgid=15)
3. Review full message text, source, stack trace
```

---

### list_console_messages

**Description:** Lists all console messages (logs, errors, warnings) since the last navigation.

**Key Parameters:**
- `includePreservedMessages` (optional): Include messages from last 3 navigations. Default: `false`
- `pageIdx` (optional): Page number for pagination (0-based)
- `pageSize` (optional): Maximum messages to return
- `types` (optional): Filter by message types:
  - log, debug, info, error, warn
  - dir, dirxml, table, trace
  - clear, assert, count, timeEnd

**Common Use Cases:**
- Error detection and debugging
- Log analysis
- Warning investigation
- JavaScript error monitoring

**Example:**
```
# All console messages
list_console_messages()

# Only errors
list_console_messages(types=["error"])

# Errors and warnings with preserved history
list_console_messages(
  types=["error", "warn"],
  includePreservedMessages=true
)

# Paginated results
list_console_messages(pageSize=100, pageIdx=0)
```

---

### take_screenshot

**Description:** Captures a screenshot of the entire page, viewport, or specific element.

**Key Parameters:**
- `uid` (optional): Element UID to screenshot (from snapshot). If omitted, captures viewport
- `fullPage` (optional): Capture entire page instead of viewport. Incompatible with `uid`
- `format` (optional): Image format - "png" (default), "jpeg", or "webp"
- `quality` (optional): Compression quality 0-100 for JPEG/WebP (ignored for PNG)
- `filePath` (optional): Path to save file instead of returning inline

**Common Use Cases:**
- Visual regression testing
- Documentation screenshots
- Bug reporting
- Page state capture
- Responsive design verification

**Example:**
```
# Viewport screenshot (default)
take_screenshot()

# Full page screenshot
take_screenshot(fullPage=true)

# Specific element
take_screenshot(uid="header-element")

# High-quality JPEG saved to file
take_screenshot(
  format="jpeg",
  quality=95,
  filePath="/path/to/screenshot.jpg"
)

# WebP with compression
take_screenshot(format="webp", quality=80)
```

**Note:** Output may use WebP format with PNG fallback regardless of requested format.

---

### take_snapshot

**Description:** Creates a text-based representation of the page using the accessibility tree, providing unique identifiers (UIDs) for all interactive elements.

**Key Parameters:**
- `verbose` (optional): Include all possible a11y tree information. Default: `false`

**Common Use Cases:**
- Getting element UIDs for interaction tools
- Understanding page structure
- Accessibility validation
- Element identification without screenshots
- Fast page state overview

**Example:**
```
# Standard snapshot
take_snapshot()

# Verbose with full a11y data
take_snapshot(verbose=true)
```

**Workflow Pattern:**
```
1. take_snapshot() - Get page structure and element UIDs
2. Identify target elements from snapshot
3. Use UIDs with interaction tools (click, fill, hover, etc.)
4. wait_for() to verify results
```

**Snapshot Output Includes:**
- Element roles (button, link, textbox, etc.)
- Element names and labels
- Element hierarchy
- Unique identifiers (UIDs) for interaction
- States (focused, disabled, checked, etc.)
- ARIA properties

---

## Tool Categories Summary

| Category | Tool Count | Primary Use |
|----------|------------|-------------|
| Input Automation | 8 | User interaction simulation |
| Navigation Automation | 7 | Page and tab management |
| Emulation | 3 | Device and network conditions |
| Performance | 3 | Core Web Vitals and tracing |
| Network | 2 | Request/response analysis |
| Debugging | 4 | Page inspection and testing |

---

## Common Workflow Patterns

### Basic Interaction Pattern
```
1. navigate_page(url="https://example.com")
2. take_snapshot() - Get element UIDs
3. fill(uid="username", value="user")
4. fill(uid="password", value="pass")
5. click(uid="login-button")
6. wait_for(text="Welcome")
```

### Performance Testing Pattern
```
1. navigate_page(url="https://example.com")
2. performance_start_trace(reload=true, autoStop=true)
3. Wait for trace completion
4. performance_analyze_insight(insightName="LCPBreakdown")
5. performance_analyze_insight(insightName="DocumentLatency")
```

### Network Analysis Pattern
```
1. navigate_page(url="https://example.com")
2. list_network_requests(resourceTypes=["xhr", "fetch"])
3. get_network_request(reqid=<specific-request>)
4. Analyze response data and timing
```

### Mobile Testing Pattern
```
1. resize_page(width=390, height=844) - iPhone 13 Pro
2. emulate_network(throttlingOption="Slow 4G")
3. emulate_cpu(throttlingRate=4)
4. navigate_page(url="https://example.com")
5. performance_start_trace(reload=false, autoStop=true)
6. Analyze mobile performance
```

### Multi-Tab Testing Pattern
```
1. new_page(url="https://example.com/page1")
2. new_page(url="https://example.com/page2")
3. list_pages() - See all open pages
4. select_page(pageIdx=0) - Switch to first page
5. Perform operations
6. select_page(pageIdx=1) - Switch to second page
7. close_page(pageIdx=1) - Clean up
```

---

## Important Notes

### Element Identification
- Always use `take_snapshot()` first to get element UIDs
- UIDs are unique per snapshot and may change after navigation
- Use the latest snapshot for current page state
- Verbose snapshots provide more accessibility details

### Browser Lifecycle
- Browser auto-starts on first tool use (not on MCP server connection)
- Use `--isolated=true` flag for temporary user data directories
- Default behavior persists data between sessions

### Security Considerations
- All browser content is exposed to MCP clients
- Avoid sensitive data in non-isolated mode
- Use `--acceptInsecureCerts` only in development
- Review official security warnings before production use

### Performance Metrics
- All measurements at 75th percentile for Core Web Vitals
- INP replaced FID on March 12, 2024
- TBT is a lab proxy for INP (not a Core Web Vital)
- Field data (real users) carries more weight than lab data

### Tool Availability
- All 27 tools available immediately after MCP connection
- No progressive unlocking or gating
- Chrome/Chromium only (no Firefox, Safari, Edge)
- Requires Node.js v20.19 or newer

---

**Version:** chrome-devtools-mcp v0.5.1 (October 17, 2025)
**Tool Count:** 27 tools across 6 categories
**Documentation Date:** October 24, 2025
