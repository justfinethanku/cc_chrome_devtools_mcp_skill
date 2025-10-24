# Chrome DevTools MCP Workflows

This document details the key workflows supported by the chrome-devtools-mcp server, including step-by-step processes, tool combinations, and best practices.

*Documentation format inspired by Mike Dion's Markdown specification (.md)*

---

## 1. Performance Analysis Workflow

Measure and analyze page performance including Core Web Vitals (INP, LCP, CLS) and lab metrics (TBT).

### Tools Required

- `performance_start_trace` - Start Chrome DevTools performance tracing
- `performance_stop_trace` - Stop tracing and retrieve trace data
- `performance_analyze_insight` - Extract detailed performance insights

### Step-by-Step Process

#### Basic Performance Capture

```
1. Start performance trace
   - Tool: performance_start_trace
   - Parameters:
     - reload: true (to capture full page load)
     - autoStop: false (for manual control)

2. Wait for page to complete loading
   - Tool: wait_for
   - Wait for specific content or use timeout

3. Stop trace recording
   - Tool: performance_stop_trace
   - Returns: Trace data with Core Web Vitals

4. Analyze specific insights
   - Tool: performance_analyze_insight
   - Parameters: insightName (e.g., "LCPBreakdown", "DocumentLatency")
```

#### Advanced Performance Analysis

```
1. Navigate to target page
   - Tool: navigate_page
   - Ensure clean state before tracing

2. Start trace without reload
   - Tool: performance_start_trace
   - Parameters: reload: false, autoStop: true
   - Use when testing specific interactions

3. Perform user interactions
   - Tools: click, fill, scroll actions
   - Captures interaction-based metrics

4. Auto-stop or manual stop
   - Tool: performance_stop_trace (if manual)
   - Trace ends automatically if autoStop: true

5. Review multiple insights
   - Tool: performance_analyze_insight
   - Check: "LCPBreakdown", "DocumentLatency", "TBT"
```

### Core Web Vitals Interpretation

#### Interaction to Next Paint (INP)
- **Good:** ≤ 200ms
- **Needs Improvement:** 200-500ms
- **Poor:** > 500ms
- **Measures:** Input delay + processing time + presentation delay
- **Note:** Field metric only; requires real user interactions

#### Largest Contentful Paint (LCP)
- **Good:** ≤ 2.5 seconds
- **Needs Improvement:** 2.5-4 seconds
- **Poor:** > 4 seconds
- **Measures:** Render time of largest content element in viewport

#### Cumulative Layout Shift (CLS)
- **Good:** ≤ 0.1
- **Needs Improvement:** 0.1-0.25
- **Poor:** > 0.25
- **Measures:** Unexpected layout shifts during page lifecycle

#### Total Blocking Time (TBT)
- **Good:** < 200ms
- **Status:** Lab proxy for INP, NOT a Core Web Vital
- **Measures:** Time main thread blocked (>50ms) after First Contentful Paint

### Trace Configuration Options

**CDP Domains Used:** Tracing, Performance

**Trace Categories:**
- `devtools.timeline` - Standard performance timeline
- `disabled-by-default-devtools.screenshot` - Screenshots during trace
- Custom categories for specific analysis

**Export Formats:**
- JSON format (for Chrome DevTools Performance panel)
- Perfetto protocol buffer (for Perfetto UI)

### Performance Workflow Best Practices

1. **Always reload for baseline metrics** - Use `reload: true` for consistent page load measurements
2. **Clear cache between runs** - Use isolated mode or clear cache manually
3. **Multiple trace captures** - Run 3-5 times and use median values
4. **Analyze specific insights** - Use performance_analyze_insight for LCP breakdown and document latency
5. **Export traces** - Save trace data for offline analysis in Chrome DevTools

---

## 2. Network Monitoring Workflow

Capture, filter, and analyze HTTP traffic with HAR export capabilities.

### Tools Required

- `list_network_requests` - List all network requests since last navigation
- `get_network_request` - Get specific request/response details

### Step-by-Step Process

#### Basic Network Capture

```
1. Navigate to target page
   - Tool: navigate_page
   - Clears previous network requests

2. List all requests
   - Tool: list_network_requests
   - Returns: Array of requests with reqid identifiers

3. Get specific request details
   - Tool: get_network_request
   - Parameter: reqid from list_network_requests
   - Returns: Full request/response with headers, body, timing
```

#### Filtered Network Analysis

```
1. Navigate and wait
   - Tool: navigate_page
   - Tool: wait_for (specific content)

2. Filter by resource type
   - Tool: list_network_requests
   - Parameters: resourceTypes array
   - Options: ["document", "stylesheet", "image", "script", "xhr", "fetch"]

3. Paginated request listing
   - Tool: list_network_requests
   - Parameters: pageSize (limit), pageIdx (0-based)
   - Use for large request volumes

4. Include preserved requests
   - Tool: list_network_requests
   - Parameters: includePreservedRequests: true
   - Returns: Requests from last 3 navigations
```

### HAR Export Capabilities

The `list_network_requests` tool returns data compatible with HTTP Archive (HAR) format v1.2:

**HAR Structure:**
```json
{
  "log": {
    "version": "1.2",
    "creator": {...},
    "pages": [...],
    "entries": [
      {
        "request": {
          "method": "GET",
          "url": "https://example.com",
          "headers": [...],
          "queryString": [...]
        },
        "response": {
          "status": 200,
          "headers": [...],
          "content": {...}
        },
        "timings": {
          "dns": 10,
          "connect": 20,
          "ssl": 15,
          "send": 5,
          "wait": 100,
          "receive": 50
        }
      }
    ]
  }
}
```

### Resource Type Filtering

**Available Resource Types:**
- `document` - HTML documents
- `stylesheet` - CSS files
- `image` - Images (PNG, JPEG, GIF, WebP, SVG)
- `media` - Video/audio files
- `font` - Web fonts
- `script` - JavaScript files
- `texttrack` - Video text tracks
- `xhr` - XMLHttpRequest
- `fetch` - Fetch API requests
- `prefetch` - Prefetch resources
- `eventsource` - Server-Sent Events
- `websocket` - WebSocket connections
- `manifest` - Web app manifests
- `signedexchange` - Signed HTTP Exchanges
- `ping` - Beacon/ping requests
- `cspviolationreport` - CSP violation reports
- `preflight` - CORS preflight requests
- `other` - Uncategorized resources

### Network Timing Details

Each request includes detailed timing breakdown:
- **DNS lookup time** - Domain name resolution
- **Connection time** - TCP connection establishment
- **SSL time** - TLS/SSL handshake
- **Send time** - Request transmission
- **Wait time** - Server processing (TTFB)
- **Receive time** - Response download

### Network Workflow Best Practices

1. **Filter early** - Use resourceTypes parameter to reduce data volume
2. **Paginate large captures** - Use pageSize/pageIdx for pages with hundreds of requests
3. **Preserve across navigations** - Set includePreservedRequests: true for multi-page flows
4. **Combine with emulation** - Use emulate_network to test different connection speeds
5. **Security details** - Check protocol, cipher suite in response data
6. **Cookie tracking** - Request data includes cookie information

---

## 3. Accessibility Testing Workflow

Validate semantic structure and screen reader compatibility using the accessibility tree.

### Tool Required

- `take_snapshot` - Get text representation based on accessibility tree

### Step-by-Step Process

#### Basic Accessibility Snapshot

```
1. Navigate to target page
   - Tool: navigate_page

2. Take standard snapshot
   - Tool: take_snapshot
   - Parameter: verbose: false (default)
   - Returns: Text representation with element UIDs

3. Analyze snapshot for:
   - ARIA roles and attributes
   - Semantic HTML usage
   - Accessible names and descriptions
   - Focusable elements
   - Form label associations
```

#### Verbose Accessibility Analysis

```
1. Take verbose snapshot
   - Tool: take_snapshot
   - Parameter: verbose: true
   - Returns: Full accessibility tree with all properties

2. Review detailed properties:
   - nodeId, role, name, description, value
   - States (busy, disabled, focusable, focused, etc.)
   - Relationships (labelledby, describedby, controls)
   - ARIA attributes
   - Computed roles
```

### Accessibility Tree Usage

The accessibility tree is a parallel tree structure to the DOM that represents how assistive technologies (screen readers) interpret the page.

**AXNode Properties:**
- `nodeId` - Unique identifier for accessibility node
- `ignored` - Whether node is ignored by assistive tech
- `role` - ARIA role (button, link, heading, etc.)
- `name` - Accessible name (visible label)
- `description` - Accessible description (additional context)
- `value` - Current value (for inputs, sliders)
- `states` - Object with boolean flags:
  - `busy`, `disabled`, `editable`, `focusable`, `focused`
  - `hidden`, `hiddenRoot`, `invalid`, `modal`, `multiline`
  - `multiselectable`, `readonly`, `required`, `selected`
- `relationships` - ARIA relationships:
  - `labelledby`, `describedby`, `controls`, `owns`
  - `activeDescendant`, `flowTo`, `details`

### Element UID Extraction

The `take_snapshot` tool returns unique identifiers (UIDs) for each interactive element:

**Example Snapshot Output:**
```
[1] button "Submit Form"
[2] textbox "Email Address"
[3] link "Privacy Policy"
[4] heading "Welcome to Our Site" level=1
[5] checkbox "Remember me" checked
```

**Using UIDs for interaction:**
```
1. Take snapshot to get UIDs
   - Tool: take_snapshot

2. Identify target element UID
   - Example: [2] for email textbox

3. Interact using UID
   - Tool: fill
   - Parameters: uid: "2", value: "user@example.com"
```

### Accessibility Testing Patterns

#### 1. Form Accessibility Check
```
1. Take snapshot
2. Verify each input has accessible name
3. Check label associations
4. Validate error message accessibility
5. Test keyboard navigation (tab order)
```

#### 2. Heading Structure Validation
```
1. Take verbose snapshot
2. Filter for role: "heading"
3. Verify logical hierarchy (h1 → h2 → h3)
4. Check no heading levels skipped
```

#### 3. Interactive Element Audit
```
1. Take snapshot
2. Identify all focusable elements
3. Verify accessible names for buttons/links
4. Check ARIA roles match functionality
5. Validate state attributes (disabled, checked, etc.)
```

#### 4. Screen Reader Simulation
```
1. Take verbose snapshot
2. Review accessible name + description for each element
3. Verify information available without visual context
4. Check landmarks (navigation, main, complementary)
5. Validate skip links and focus management
```

### Accessibility Workflow Best Practices

1. **Use standard snapshot first** - Verbose mode only when detailed analysis needed
2. **Combine with visual testing** - Take screenshot + snapshot for complete picture
3. **Test dynamic content** - Re-snapshot after interactions to verify state changes
4. **Validate forms thoroughly** - Check labels, error messages, required indicators
5. **Review ignored nodes** - Verbose mode shows why elements are ignored
6. **Check relationships** - Verify aria-labelledby and aria-describedby connections

---

## 4. Browser Automation Workflow

Automate user interactions with reliable element targeting via accessibility UIDs.

### Tools Required

- `click` - Click or double-click elements
- `fill` - Fill single form field
- `fill_form` - Fill multiple form fields simultaneously
- `hover` - Hover over elements
- `drag` - Drag element onto another element
- `handle_dialog` - Handle browser dialogs (alerts, confirms, prompts)
- `upload_file` - Upload files to input elements
- `wait_for` - Wait for text to appear

### Automation Pattern: Snapshot → Identify → Interact → Wait

This is the fundamental pattern for all browser automation:

```
1. SNAPSHOT: Get current page state
   - Tool: take_snapshot
   - Returns: Element UIDs for interaction

2. IDENTIFY: Find target element UID
   - Parse snapshot output
   - Locate element by role, name, or text

3. INTERACT: Perform action using UID
   - Tool: click, fill, hover, drag, etc.
   - Parameter: uid from snapshot

4. WAIT: Confirm action result
   - Tool: wait_for
   - Wait for expected text/state change
```

### Step-by-Step Automation Examples

#### Example 1: Form Submission

```
1. Navigate to form page
   - Tool: navigate_page
   - URL: https://example.com/contact

2. Take snapshot
   - Tool: take_snapshot
   - Identify: [2] textbox "Name", [3] textbox "Email", [4] button "Submit"

3. Fill form fields
   - Tool: fill_form
   - Parameters: [
       {uid: "2", value: "John Doe"},
       {uid: "3", value: "john@example.com"}
     ]

4. Click submit button
   - Tool: click
   - Parameter: uid: "4"

5. Wait for confirmation
   - Tool: wait_for
   - Parameter: text: "Thank you for your submission"
```

#### Example 2: File Upload

```
1. Take snapshot
   - Tool: take_snapshot
   - Identify: [5] "Choose File" button (file input)

2. Upload file
   - Tool: upload_file
   - Parameters: uid: "5", filePath: "/path/to/document.pdf"

3. Wait for upload confirmation
   - Tool: wait_for
   - Parameter: text: "Upload complete"
```

#### Example 3: Drag and Drop

```
1. Take snapshot
   - Tool: take_snapshot
   - Identify: [10] draggable item, [11] drop target

2. Drag element
   - Tool: drag
   - Parameters: from_uid: "10", to_uid: "11"

3. Wait for drop confirmation
   - Tool: wait_for
   - Parameter: text: "Item moved successfully"
```

#### Example 4: Dialog Handling

```
1. Click element that triggers dialog
   - Tool: click
   - Parameter: uid: "7"

2. Handle dialog
   - Tool: handle_dialog
   - Parameters: action: "accept" (or "dismiss")
   - Optional: promptText: "User input" (for prompt dialogs)
```

#### Example 5: Hover Interactions

```
1. Take snapshot
   - Tool: take_snapshot
   - Identify: [15] element with hover state

2. Hover over element
   - Tool: hover
   - Parameter: uid: "15"

3. Take new snapshot to verify hover state
   - Tool: take_snapshot
   - Check for newly visible elements (tooltips, dropdowns)
```

#### Example 6: Double-Click

```
1. Take snapshot
   - Tool: take_snapshot
   - Identify: [20] element requiring double-click

2. Double-click element
   - Tool: click
   - Parameters: uid: "20", dblClick: true
```

### Complex Automation Workflows

#### Multi-Step Form with Validation

```
1. Navigate to form
2. Take snapshot → identify all fields
3. Fill first field → wait for validation
4. Take new snapshot (validation may show/hide elements)
5. Fill remaining fields
6. Click submit → handle any confirmation dialog
7. Wait for success message
```

#### Dynamic Content Interaction

```
1. Navigate to page
2. Take snapshot → identify load-more button
3. Click load-more → wait for new content text
4. Take new snapshot (new UIDs for new elements)
5. Interact with newly loaded elements
6. Repeat as needed
```

#### Dropdown Navigation

```
1. Take snapshot → identify dropdown trigger
2. Hover over trigger → wait for dropdown appearance
3. Take new snapshot → identify dropdown options
4. Click option → wait for navigation
```

### Automation Workflow Best Practices

1. **Always snapshot before interaction** - Element UIDs change on page updates
2. **Use fill_form for multiple fields** - More efficient than multiple fill calls
3. **Wait after actions** - Use wait_for to ensure action completed
4. **Re-snapshot after dynamic changes** - New elements get new UIDs
5. **Handle dialogs immediately** - Automation blocks until dialog handled
6. **Combine with screenshots** - Visual verification of automation steps
7. **Timeout configuration** - Set appropriate timeout values for wait_for

---

## 5. Multi-Tab Management Workflow

Manage multiple browser tabs/pages with context switching.

### Tools Required

- `list_pages` - List all open pages/tabs
- `new_page` - Open new page/tab
- `select_page` - Switch active page context
- `close_page` - Close page/tab (cannot close last page)

### Step-by-Step Process

#### Basic Tab Management

```
1. List current pages
   - Tool: list_pages
   - Returns: Array of pages with pageIdx identifiers

2. Create new page
   - Tool: new_page
   - Parameters: url (optional), timeout (optional)
   - Returns: New page created and becomes active

3. Switch between pages
   - Tool: select_page
   - Parameter: pageIdx (from list_pages)

4. Close page
   - Tool: close_page
   - Parameter: pageIdx
   - Note: Cannot close last remaining page
```

#### Multi-Tab Workflow Example

```
1. List existing pages
   - Tool: list_pages
   - Example output: [
       {pageIdx: 0, url: "https://example.com", title: "Example"},
       {pageIdx: 1, url: "https://test.com", title: "Test"}
     ]

2. Open new page
   - Tool: new_page
   - Parameters: url: "https://newpage.com", timeout: 30000
   - New page automatically selected

3. Perform actions on new page
   - Tools: take_snapshot, click, fill, etc.
   - All tools operate on currently selected page

4. Switch to existing page
   - Tool: select_page
   - Parameter: pageIdx: 0

5. Perform actions on original page
   - Context now on pageIdx: 0

6. Close page when done
   - Tool: close_page
   - Parameter: pageIdx: 1
```

### Tab Switching Strategies

#### Strategy 1: Sequential Processing
Process multiple pages one at a time:
```
1. List all pages
2. For each page:
   a. Select page (select_page)
   b. Take snapshot
   c. Perform analysis/interaction
   d. Store results
3. Close completed pages
```

#### Strategy 2: Background Tab Loading
Open multiple tabs, then process:
```
1. Open multiple pages in background
   - new_page (URL 1)
   - new_page (URL 2)
   - new_page (URL 3)
2. List pages to get all pageIdx values
3. Process each page:
   - select_page → analyze → next page
```

#### Strategy 3: Comparison Testing
Compare same action across multiple pages:
```
1. Open pages for comparison
   - new_page (Version A)
   - new_page (Version B)
2. For each page:
   a. Select page
   b. Take performance trace
   c. Store metrics
3. Compare results across pages
```

#### Strategy 4: Frame Handling
Work with pages containing iframes:
```
1. Navigate to page with frames
2. take_snapshot shows frame structure
3. Interact with main page elements
4. CDP Target domain handles frame attachment automatically
```

### Page Selection Best Practices

1. **Always list before selecting** - Page indices may change after close operations
2. **Track page context** - Remember which pageIdx corresponds to which task
3. **Cannot close last page** - Keep at least one page open at all times
4. **New pages auto-select** - After new_page, it becomes active context
5. **Timeout for slow loads** - Set appropriate timeout for new_page operations
6. **Session persistence** - Pages persist across navigation within same session

### Multi-Tab Use Cases

#### Use Case 1: Cross-Browser Testing
```
1. Open same URL in multiple pages
2. Each page with different emulation settings
3. Compare snapshots/screenshots across pages
```

#### Use Case 2: Multi-Step User Flows
```
1. Page 1: Login
2. Page 2: Dashboard
3. Page 3: Settings
4. Switch between pages to verify state persistence
```

#### Use Case 3: Performance Comparison
```
1. Page 1: Production site
2. Page 2: Staging site
3. Run identical performance traces on both
4. Compare Core Web Vitals
```

#### Use Case 4: Data Extraction
```
1. Open multiple product pages
2. For each page:
   - Select page
   - Take snapshot
   - Extract product data
   - Store results
3. Close pages when done
```

---

## 6. Device Emulation Workflow

Simulate different devices, network conditions, and performance constraints.

### Tools Required

- `emulate_network` - Simulate network conditions
- `emulate_cpu` - Simulate CPU throttling
- `resize_page` - Change viewport dimensions

### Step-by-Step Process

#### Basic Device Emulation

```
1. Set viewport size
   - Tool: resize_page
   - Parameters: width (pixels), height (pixels)
   - Example: width: 375, height: 812 (iPhone X)

2. Configure network emulation
   - Tool: emulate_network
   - Parameter: throttlingOption
   - Options: "No emulation", "Offline", "Slow 3G", "Fast 3G", "Slow 4G", "Fast 4G"

3. Configure CPU throttling
   - Tool: emulate_cpu
   - Parameter: throttlingRate (1-20x)
   - Example: 4 (4x slowdown, simulates low-end device)

4. Navigate to page under test
   - Tool: navigate_page
   - Page loads with emulation applied

5. Run performance tests
   - Tools: performance_start_trace, performance_stop_trace
   - Metrics reflect emulated conditions
```

#### Mobile Device Testing

```
1. Configure mobile viewport
   - Tool: resize_page
   - Common sizes:
     - iPhone 14 Pro: 393 x 852
     - iPhone SE: 375 x 667
     - Pixel 7: 412 x 915
     - Galaxy S22: 360 x 800

2. Set mobile network
   - Tool: emulate_network
   - Parameter: throttlingOption: "Fast 4G"
   - Simulates typical mobile connection

3. Set CPU throttling
   - Tool: emulate_cpu
   - Parameter: throttlingRate: 4
   - Simulates mid-range mobile device

4. Take snapshot/screenshot
   - Tools: take_snapshot, take_screenshot
   - Verify mobile layout

5. Test mobile interactions
   - Tools: click, fill, drag
   - Interactions work identically on emulated mobile
```

#### Tablet Device Testing

```
1. Configure tablet viewport
   - Tool: resize_page
   - Common sizes:
     - iPad Pro 12.9": 1024 x 1366
     - iPad Air: 820 x 1180
     - Surface Pro: 912 x 1368

2. Set network conditions
   - Tool: emulate_network
   - Parameter: throttlingOption: "Fast 4G" or "No emulation" (WiFi)

3. Test responsive breakpoints
   - Resize between tablet/desktop sizes
   - Verify layout changes
```

### Network Emulation Options

**Available Throttling Profiles:**

1. **No emulation** (default)
   - Full network speed
   - No artificial latency

2. **Offline**
   - Simulates no network connection
   - Tests offline functionality, service workers

3. **Slow 3G**
   - Download: ~400 Kbps
   - Upload: ~400 Kbps
   - Latency: ~2000ms
   - Use for: Extreme mobile testing

4. **Fast 3G**
   - Download: ~1.6 Mbps
   - Upload: ~750 Kbps
   - Latency: ~562ms
   - Use for: Typical 3G mobile

5. **Slow 4G**
   - Download: ~4 Mbps
   - Upload: ~3 Mbps
   - Latency: ~150ms
   - Use for: Poor LTE conditions

6. **Fast 4G**
   - Download: ~10 Mbps
   - Upload: ~5 Mbps
   - Latency: ~40ms
   - Use for: Good LTE conditions

### CPU Throttling Configuration

**Throttling Rate Scale:** 1-20x

- **1x** - No throttling (default)
- **4x** - Mid-range mobile device
- **6x** - Low-end mobile device
- **10x+** - Extreme performance constraints

**Use Cases:**
- Test Time to Interactive (TTI) on slow devices
- Identify JavaScript performance bottlenecks
- Measure TBT under constrained conditions
- Validate progressive enhancement

### Viewport Resize Patterns

#### Common Device Dimensions

**Smartphones (Portrait):**
- iPhone 14 Pro Max: 430 x 932
- iPhone 14 Pro: 393 x 852
- iPhone 14: 390 x 844
- iPhone SE: 375 x 667
- Pixel 7 Pro: 412 x 915
- Pixel 7: 412 x 915
- Galaxy S22 Ultra: 384 x 854
- Galaxy S22: 360 x 800

**Tablets:**
- iPad Pro 12.9": 1024 x 1366
- iPad Pro 11": 834 x 1194
- iPad Air: 820 x 1180
- iPad Mini: 744 x 1133
- Surface Pro 8: 912 x 1368

**Desktop:**
- MacBook Air 13": 1280 x 832
- MacBook Pro 14": 1512 x 982
- Desktop 1080p: 1920 x 1080
- Desktop 4K: 3840 x 2160

### Emulation Workflow Examples

#### Example 1: Mobile Performance Audit

```
1. Resize to mobile
   - resize_page: width: 375, height: 812

2. Set mobile network
   - emulate_network: throttlingOption: "Fast 4G"

3. Set CPU throttling
   - emulate_cpu: throttlingRate: 4

4. Start performance trace
   - performance_start_trace: reload: true, autoStop: true

5. Analyze results
   - performance_stop_trace
   - Check INP, LCP, CLS under mobile conditions
```

#### Example 2: Offline Mode Testing

```
1. Set offline mode
   - emulate_network: throttlingOption: "Offline"

2. Navigate to page
   - navigate_page
   - Should trigger offline fallback

3. Verify service worker
   - take_snapshot
   - Check offline content displayed

4. Restore network
   - emulate_network: throttlingOption: "No emulation"
```

#### Example 3: Responsive Design Testing

```
1. Test mobile breakpoint
   - resize_page: width: 375, height: 667
   - take_screenshot (mobile layout)

2. Test tablet breakpoint
   - resize_page: width: 768, height: 1024
   - take_screenshot (tablet layout)

3. Test desktop breakpoint
   - resize_page: width: 1920, height: 1080
   - take_screenshot (desktop layout)

4. Compare screenshots for layout consistency
```

#### Example 4: Network Speed Comparison

```
1. Baseline (no throttling)
   - emulate_network: "No emulation"
   - Run performance trace
   - Record load time

2. Fast 4G
   - emulate_network: "Fast 4G"
   - Run performance trace
   - Compare load time

3. Slow 3G
   - emulate_network: "Slow 3G"
   - Run performance trace
   - Compare load time

4. Analyze network waterfall for bottlenecks
```

### Emulation Best Practices

1. **Reset emulation between tests** - Set to "No emulation" and throttlingRate: 1
2. **Combine emulation types** - Use network + CPU + viewport together
3. **Match real-world conditions** - Fast 4G + 4x CPU = typical mobile experience
4. **Test offline gracefully** - Verify service worker, error messages, fallback content
5. **Validate responsive breakpoints** - Test at exact breakpoint boundaries
6. **Document test conditions** - Record emulation settings with results
7. **Compare against field data** - Lab emulation should match real user metrics from CrUX

### Mobile Device Testing Workflow

Complete mobile testing checklist:

```
1. Set device viewport (resize_page)
2. Configure network (emulate_network: "Fast 4G")
3. Configure CPU (emulate_cpu: 4)
4. Navigate to page
5. Take accessibility snapshot (take_snapshot)
6. Run performance trace (performance_start_trace/stop)
7. Test touch interactions (click, drag)
8. Verify mobile-specific features (hamburger menu, gestures)
9. Take screenshots for visual verification
10. Reset emulation for next test
```

---

## Workflow Combination Strategies

Many real-world testing scenarios combine multiple workflows:

### Strategy 1: Complete Performance Audit

```
1. Device Emulation Setup
   - Mobile viewport, Fast 4G, 4x CPU

2. Performance Analysis
   - Start trace with reload
   - Stop trace and analyze Core Web Vitals

3. Network Monitoring
   - List network requests
   - Filter for large resources
   - Check total payload size

4. Accessibility Testing
   - Take verbose snapshot
   - Verify mobile accessibility
```

### Strategy 2: Cross-Device Comparison

```
1. Multi-Tab Setup
   - Page 1: Mobile (375x667)
   - Page 2: Tablet (768x1024)
   - Page 3: Desktop (1920x1080)

2. For each page:
   - Select page
   - Run performance trace
   - Take screenshot
   - Export results

3. Compare metrics across devices
```

### Strategy 3: End-to-End User Flow

```
1. Browser Automation
   - Navigate through multi-step flow
   - Fill forms, click buttons

2. Performance Monitoring
   - Trace each step
   - Measure interaction latency

3. Network Analysis
   - Track requests at each step
   - Identify slow API calls

4. Accessibility Validation
   - Snapshot at each step
   - Verify keyboard navigation
```

---

## CDP Domain Reference

Each workflow leverages specific Chrome DevTools Protocol domains:

- **Performance Analysis:** Tracing, Performance
- **Network Monitoring:** Network
- **Accessibility Testing:** Accessibility (Experimental)
- **Browser Automation:** Input, Runtime, DOM
- **Multi-Tab Management:** Target, Page
- **Device Emulation:** Emulation

For complete CDP documentation, see: https://chromedevtools.github.io/devtools-protocol/

---

**Document Version:** 1.0
**Last Updated:** October 24, 2025
**Based on:** chrome-devtools-mcp v0.5.1
