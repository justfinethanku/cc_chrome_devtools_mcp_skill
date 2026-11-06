# Chrome DevTools testing workflows

These workflows target `chrome-devtools-mcp@1.12.0` with default tools and
`pageId` routing enabled. JSON blocks are tool-call envelopes for an MCP client.
They passed input-schema validation; browser outcomes depend on your application
and were not exercised in this documentation audit. Replace example page IDs,
UIDs, text, and insight IDs with values returned by your session.

Use [setup instructions](README.md#prerequisites) first. Read
[security considerations](SKILL.md#security-considerations) before using accounts
or saving captures. Only perform interactions authorized by the user's task.

## Performance analysis workflow

1. Open the target page before starting a reload trace:

   ```json
   {"name":"new_page","arguments":{"url":"https://example.com"}}
   ```

2. Record the returned page ID. The following examples use `1`. Set test
   conditions before tracing:

   ```json
   {"name":"emulate","arguments":{"pageId":1,"networkConditions":"Fast 4G","cpuThrottlingRate":4}}
   ```

3. Capture a reload trace that stops automatically:

   ```json
   {"name":"performance_start_trace","arguments":{"pageId":1,"reload":true,"autoStop":true}}
   ```

4. Read the available insight sets and metrics from the result. To expand an
   insight, use its exact returned set ID and name:

   ```json
   {"name":"performance_analyze_insight","arguments":{"pageId":1,"insightSetId":"RETURNED_INSIGHT_SET_ID","insightName":"LCPBreakdown"}}
   ```

5. Record URL, server and browser versions, viewport, CPU/network conditions,
   cache state, interactions, and repeated samples. Report available metrics;
   do not invent an INP result for a trace with no qualifying interactions.
   See [lab and field interpretation](METRICS.md#field-and-lab-data).

For an interaction trace, start with `reload: false, autoStop: false`, perform
the requested user flow, then call `performance_stop_trace` with the same
`pageId`. Do not stop a trace that already stopped automatically. Keep the same
conditions for before/after comparisons.

## Network monitoring workflow

1. Navigate the target page and wait for the specific content needed by the test:

   ```json
   {"name":"navigate_page","arguments":{"pageId":1,"type":"url","url":"https://example.com"}}
   ```

2. List the relevant requests:

   ```json
   {"name":"list_network_requests","arguments":{"pageId":1,"resourceTypes":["xhr","fetch","document"],"pageSize":50,"pageIdx":0}}
   ```

3. Use a returned `reqid` to inspect the request:

   ```json
   {"name":"get_network_request","arguments":{"pageId":1,"reqid":123}}
   ```

4. Inspect failures and the returned data before drawing conclusions. Request
   and console retention is bounded; older response bodies may be unavailable.
   `includePreservedRequests` includes retained navigations, not unlimited history.

`list_network_requests` does not export HAR. For a HAR file, use the Chrome
DevTools Network panel's export function and review the file before sharing.
See [Chrome's network export guide](https://developer.chrome.com/docs/devtools/network/reference#save-as-har).

## Accessibility testing workflow

1. Take a snapshot of the target page:

   ```json
   {"name":"take_snapshot","arguments":{"pageId":1,"verbose":true}}
   ```

2. Inspect roles, names, heading structure, and form labels. Obtain fresh UIDs
   after navigation or application state changes.
3. Test keyboard behavior, observing focus and the expected effect after each
   action:

   ```json
   {"name":"press_key","arguments":{"pageId":1,"key":"Tab","includeSnapshot":true}}
   ```

4. Inspect a screenshot for focus visibility and visual issues. A snapshot
   alone cannot establish color contrast or screen reader compatibility.
5. Report specific observed problems and the checks performed. Use dedicated
   contrast measurement and actual assistive technology where required. Neither
   a snapshot nor a Lighthouse report certifies WCAG compliance.

## Browser automation workflow

Use the pattern **snapshot → identify → interact → wait → verify** on a test
account or fixture.

1. Take a snapshot and identify the form UIDs:

   ```json
   {"name":"take_snapshot","arguments":{"pageId":1}}
   ```

2. Fill the fields identified by that snapshot:

   ```json
   {"name":"fill_form","arguments":{"pageId":1,"elements":[{"uid":"EMAIL_UID","value":"test@example.com"},{"uid":"NAME_UID","value":"Test User"}]}}
   ```

3. Click the intended submit control:

   ```json
   {"name":"click","arguments":{"pageId":1,"uid":"SUBMIT_UID"}}
   ```

4. Wait for the application's visible confirmation:

   ```json
   {"name":"wait_for","arguments":{"pageId":1,"text":["Saved"],"visible":true,"timeout":10000}}
   ```

5. Verify the resulting state. Visible text is evidence of UI behavior; it does
   not independently prove a server-side write succeeded. Inspect the relevant
   response or persisted result when the task requires that boundary.

Use `upload_file` only with files accessible to the browser instance. Use
`handle_dialog` for an expected dialog; inspect its meaning before accepting.

## Multi-tab management workflow

1. Call `list_pages` with `{}`. Keep each returned page ID with its task.
2. Use `new_page` to create a page; `background: true` avoids foreground focus.
3. Pass `pageId` explicitly on every page-targeted call. Selecting a tab does
   not remove that requirement in the default v1.12.0 configuration:

   ```json
   {"name":"select_page","arguments":{"pageId":1,"bringToFront":true}}
   ```

4. Navigate history with the same navigation tool:

   ```json
   {"name":"navigate_page","arguments":{"pageId":1,"type":"back"}}
   ```

5. Close only pages that belong to the task and are no longer needed:

   ```json
   {"name":"close_page","arguments":{"pageId":1}}
   ```

Tabs in the same browser context share cookies and storage. For separate account
fixtures, `new_page` supports named `isolatedContext` values. This is separate
from the server's temporary-profile flag and does not redact returned data.

## Device emulation workflow

1. Emulate a mobile viewport, touch input, CPU, and network together:

   ```json
   {"name":"emulate","arguments":{"pageId":1,"viewport":"390x844x3,mobile,touch","networkConditions":"Fast 4G","cpuThrottlingRate":4}}
   ```

2. Run the requested flow. Capture screenshots and inspect the resulting
   accessibility tree at the relevant states.
3. To change one setting, include the other desired overrides again. Omitted
   overrides reset according to the schema; request headers persist until
   explicitly cleared.
4. Restore defaults and clear extra request headers when finished:

   ```json
   {"name":"emulate","arguments":{"pageId":1,"extraHttpHeaders":""}}
   ```

For layout-only testing, `resize_page` accepts `pageId`, `width`, and `height`.
A viewport size does not emulate an entire named physical device, and Chrome
emulation does not test Safari or Firefox. Record these limits in your result.
