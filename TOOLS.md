# Chrome DevTools MCP tool reference

Checked on November 6, 2026 against the published `chrome-devtools-mcp@1.12.0`
server’s MCP `tools/list` response: **32 tools** with the default category settings.
This is a versioned interface index. Other releases, category flags, or
experimental flags can expose a different inventory. Read the connected server’s
schema before calling it. The [upstream reference](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/tool-reference.md)
tracks upstream development and can differ from the published version.

## Page and element identifiers

Call `list_pages` with `{}` or create a tab with `new_page`. Use the numeric
`pageId` it returns; IDs are not zero-based tab indexes. In this version all
page-targeted tools require `pageId`, including `take_snapshot`, `click`, and
performance tools. `pageIdx` remains a pagination field on list tools, not a tab
selector. Obtain element `uid` values from a fresh snapshot of that page.

## Tool inputs

Required inputs appear in the third column. The last column lists optional
inputs, not defaults. Inspect the live schema for ranges, defaults, nested
objects, and tool-specific constraints. Unknown fields are rejected.

| Tool | Purpose | Required inputs | Optional inputs |
| --- | --- | --- | --- |
| `click` | Click a snapshot element; optionally double-click. | `pageId` (number), `uid` (string) | `dblClick`, `includeSnapshot` |
| `close_page` | Close the identified tab. | `pageId` (number) | None |
| `drag` | Drag between two snapshot elements. | `pageId` (number), `from_uid` (string), `to_uid` (string) | `includeSnapshot` |
| `emulate` | Set network, CPU, viewport, location, media, user-agent, or request-header overrides. | `pageId` (number) | `networkConditions`, `cpuThrottlingRate`, `geolocation`, `userAgent`, `colorScheme`, `forcedColors`, `prefersContrast`, `prefersReducedMotion`, `viewport`, `extraHttpHeaders` |
| `evaluate_script` | Run page JavaScript or read data; choose function or sourcePath, never both. | `pageId` (number) | `function`, `sourcePath`, `format`, `args`, `filePath`, `dialogAction`, `waitForStableDom` |
| `fill` | Set one form value. | `pageId` (number), `uid` (string), `value` (string) | `includeSnapshot` |
| `fill_form` | Set several form values. | `pageId` (number), `elements` (array of object) | `includeSnapshot` |
| `get_console_message` | Inspect a listed console message. | `pageId` (number), `msgid` (number) | None |
| `get_css_styles` | Inspect an element’s CSS rules. | `pageId` (number), `uid` (string) | `pageSize`, `pageIdx` |
| `get_network_request` | Inspect a request; optionally save request or response bodies. | `pageId` (number) | `reqid`, `requestFilePath`, `responseFilePath` |
| `handle_dialog` | Accept or dismiss a browser dialog. | `pageId` (number), `action` (`accept` / `dismiss`) | `promptText` |
| `hover` | Move over a snapshot element. | `pageId` (number), `uid` (string) | `includeSnapshot` |
| `lighthouse_audit` | Run a navigation or snapshot Lighthouse audit. | `pageId` (number) | `mode`, `device`, `outputDirPath` |
| `list_console_messages` | List or filter collected console messages. | `pageId` (number) | `pageSize`, `pageIdx`, `types`, `includePreservedMessages`, `includeStackTraces`, `serviceWorkerId` |
| `list_network_requests` | List or filter collected requests. | `pageId` (number) | `pageSize`, `pageIdx`, `resourceTypes`, `includePreservedRequests` |
| `list_pages` | Find page IDs and current browser pages. | None | None |
| `navigate_page` | Navigate to a URL, reload, or move through history. | `pageId` (number) | `type`, `url`, `ignoreCache`, `handleBeforeUnload`, `initScript`, `timeout` |
| `new_page` | Create a tab and return its page ID. | `url` (string) | `background`, `isolatedContext`, `timeout` |
| `performance_analyze_insight` | Expand an insight returned by a recorded trace. | `pageId` (number), `insightSetId` (string), `insightName` (string) | None |
| `performance_start_trace` | Record a page trace; optionally reload and stop automatically. | `pageId` (number) | `reload`, `autoStop`, `ignoreCache`, `filePath` |
| `performance_stop_trace` | Stop a manually recorded trace. | `pageId` (number) | `filePath` |
| `press_key` | Send a key or key combination. | `pageId` (number), `key` (string) | `includeSnapshot` |
| `resize_page` | Change page dimensions. | `pageId` (number), `width` (integer), `height` (integer) | None |
| `screencast_start` | Start an MP4 recording. | `pageId` (number) | `filePath` |
| `screencast_stop` | Stop a recording. | `pageId` (number) | None |
| `select_page` | Select a tab; optionally bring it to the front. | `pageId` (number) | `bringToFront` |
| `take_heapsnapshot` | Save a heap snapshot to a file. | `pageId` (number), `filePath` (string) | None |
| `take_screenshot` | Capture a viewport, full page, or snapshot element. | `pageId` (number) | `format`, `quality`, `uid`, `fullPage`, `filePath` |
| `take_snapshot` | Read the accessibility tree and its element UIDs. | `pageId` (number) | `verbose`, `filePath` |
| `type_text` | Type into the focused element. | `pageId` (number), `text` (string) | `submitKey` |
| `upload_file` | Populate a file input with paths available to the browser. | `pageId` (number), `uid` (string), `filePaths` (array of string) | `includeSnapshot` |
| `wait_for` | Wait for any text in a nonempty array; optionally require visibility. | `pageId` (number), `text` (array of string) | `timeout`, `visible` |

## Common calls

These are tool-call envelopes for an MCP client, not shell commands. Replace
example page IDs, UIDs, paths, and insight IDs with values from your session.
The examples pass the v1.12.0 input schemas; they have not been executed against a
live browser as part of this documentation update.

List the pages:

```json
{"name":"list_pages","arguments":{}}
```

Select a page by its returned ID:

```json
{"name":"select_page","arguments":{"pageId":1,"bringToFront":true}}
```

Wait for a visible result; `text` is an array and matches **any** supplied string:

```json
{"name":"wait_for","arguments":{"pageId":1,"text":["Success","Saved"],"visible":true,"timeout":10000}}
```

Capture a full-page PNG to an allowed artifact directory on the MCP server.
Replace `/tmp/capture.png` with a permitted path; see
[filesystem access](GUIDE.md#captures-and-filesystem-access):

```json
{"name":"take_screenshot","arguments":{"pageId":1,"format":"png","fullPage":true,"filePath":"/tmp/capture.png"}}
```

Inspect an element’s text without waiting for a DOM change:

```json
{"name":"evaluate_script","arguments":{"pageId":1,"function":"(el) => el.textContent","args":["SNAPSHOT_UID"],"waitForStableDom":false}}
```

## Important constraints

- **Navigation:** history uses `navigate_page` with `type: "back"` or
  `type: "forward"`; `navigate_page_history` is absent in this version.
- **Emulation:** use `emulate` with `networkConditions` and
  `cpuThrottlingRate`; the old separate emulation tools are absent. Include all
  desired overrides in each call: omitted network, CPU, viewport, location,
  user-agent, and media overrides reset according to the schema. Headers persist
  until explicitly cleared with `extraHttpHeaders: ""`.
- **Scripts:** provide either `function` or `sourcePath`. Function mode accepts
  `args` as an array of UID strings. Script mode does not accept `args`;
  ECMAScript modules are unsupported. Page script output remains untrusted.
- **Tracing:** navigate before starting a reload trace. For manual interaction
  capture use `reload: false, autoStop: false`, interact, then stop the trace.
  Analysis requires both `insightSetId` and `insightName` returned by the trace;
  do not invent them.
- **Screenshots:** supported formats are `png`, `jpeg`, and `webp`. Quality
  applies to JPEG/WebP and is ignored for PNG. `fullPage` cannot be combined
  with `uid`. `filePath` saves a file instead of attaching the capture.
- **Uploads:** file paths must be available to the browser instance, which may
  be on a different host from the MCP client.
- **Network:** listing requests is not HAR export. There is no native HAR-export
  tool in this inventory. Use Chrome DevTools’ Network panel to export a HAR;
  do not label a synthesized list of requests as a complete HAR.
- **Accessibility:** snapshots expose the accessibility tree; they do not
  certify WCAG compliance, measure every contrast ratio, or replace screen
  reader and keyboard tests. Lighthouse findings also need interpretation.

See [task workflows](WORKFLOWS.md), [measurement guidance](METRICS.md), and
[security considerations](SKILL.md#security-considerations) before collecting or
sharing browser data.
