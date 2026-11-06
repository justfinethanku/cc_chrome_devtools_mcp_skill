# Chrome DevTools setup and configuration guide

This package supplies instructions to Claude Code. Install and configure the
external MCP server separately. Setup and tool discovery were checked with
Claude Code 2.1.318, Node.js 22.22.2, and `chrome-devtools-mcp@1.12.0` on Linux
on November 6, 2026. Browser startup and end-to-end page interactions were not
verified on that audit host, which has no Chrome executable on its command path.

## Quick start

Follow [the README prerequisites and setup](README.md#prerequisites) for the
maintained installation procedure. The README covers plugin and manual skill
installation, registration scope, and verification. Avoid installing the same
skill through both paths.

After setup, ask for a specific page and task. Start by listing pages, then use
the returned `pageId` for page-targeted tools. See [tool inputs](TOOLS.md#tool-inputs)
and [task workflows](WORKFLOWS.md). Available tools and arguments depend on the
server version and category flags; this reference targets the default v1.12.0
inventory, not upstream development HEAD.

## Configuration options

Run the installed version's help before changing its flags:

```bash
npx -y chrome-devtools-mcp@1.12.0 --help
```

The examples pin the version used for validation. To upgrade, choose a released
version, review its release/security notes, update the package argument, and
check tool discovery and the changed schemas again.

| Option | Purpose |
| --- | --- |
| `--isolated=true` | Use a temporary profile when the server launches Chrome. Does not isolate an attached browser. |
| `--headless=true` | Launch Chrome without a visible window. Chrome must still be installed. |
| `--executablePath=PATH` | Select a Chrome/Chromium executable on the server host. |
| `--channel=stable` | Choose stable, beta, dev, or canary. |
| `--viewport=1920x1080` | Set launch viewport dimensions. |
| `--userDataDir=PATH` | Choose a persistent launch profile using an absolute path on the server host; remove `--isolated=true` first. |
| `--browserUrl=URL` | Attach through an existing browser's HTTP debugging endpoint. |
| `--wsEndpoint=URL` | Attach through its WebSocket endpoint instead. |
| `--wsHeaders=JSON` | Pass headers to an already authenticated WebSocket endpoint. |
| `--proxyServer=URL` | Set a launch proxy. |
| `--logFile=PATH` | Write potentially sensitive debug logs. `NODE_DEBUG=*` enables verbose Node debugging. |
| `--no-usage-statistics` | Disable the server's usage statistics. |
| `--no-performance-crux` | Disable trace URL lookups against the CrUX API. |
| `--workspace=PATH` | Allow file tools to access a directory; repeat for multiple roots. |

The correct persistent-profile flag is `--userDataDir`; use the spelling in the
installed help. Choose the browser mode before combining options.

### Choose the browser mode

These modes describe the pinned v1.12.0 MCP server registered in the README.
The instruction plugin does not allocate profiles or own browser processes.

| Mode | Connection arguments | Browser and profile ownership |
| --- | --- | --- |
| Temporary launch (README default) | `--isolated=true`, without an attachment or `--userDataDir` | The server launches and closes Chrome; Puppeteer allocates the temporary profile and handles its cleanup. |
| Persistent launch | `--userDataDir=PATH`, without `--isolated=true` or an attachment | The server launches and closes Chrome; the chosen profile remains on disk. Replace `PATH` with a dedicated test profile. |
| HTTP attachment | `--browserUrl=URL` | You launch and close the external test browser and manage its profile. Disconnecting MCP leaves it running. |
| WebSocket attachment | `--wsEndpoint=URL` | Same external ownership as HTTP attachment; use the endpoint from that test browser. |

When switching from the README's temporary launch to a persistent launch,
replace `--isolated=true` with `--userDataDir=PATH`. Appending the profile flag
fails at startup with `Arguments userDataDir and isolated are mutually exclusive`.
The server also rejects `--userDataDir` with either attachment flag, both
attachment flags together, and an explicit `--channel` or `--executablePath`
with either attachment flag. Launch settings do not configure an external browser.

Isolation lasts for the launched browser's lifetime. Repeated tool calls through
one running server reuse its browser; `--isolated=true` does not reset cookies or
storage before each call. For a fresh browser profile, stop that server and start
a new isolated launch using [the recovery procedure](#recover-or-remove-a-browser-connection).

Without isolation or an explicit profile, the MCP server selects a persistent
profile under `~/.cache/chrome-devtools-mcp/chrome-profile` (with a suffix for a
non-stable channel). This path is shared by launches using the same home and
channel, including launches from different projects. Registration scope does
not give each project its own profile directory. For parallel independent tests,
use separate isolated launches or distinct dedicated persistent profile paths.
If Chrome reports that a profile is already running, close the test browser that
owns it or choose a separate profile; retain its data and lock files while it runs.

Mode conflicts and browser ownership were checked against the published v1.12.0
configuration and connection code. Launch, close, failure, and retry checks used
inert Puppeteer fixtures; they did not run Chrome, reproduce an OS profile lock,
or verify temporary-directory cleanup. See the [upstream configuration reference](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/configuration.md)
when changing versions.

### Keep a persistent profile stable across projects

For v1.12.0 launches, use an absolute `--userDataDir` path on the MCP server
host. Puppeteer resolves a relative value such as `./test-profile` from the
server process's working directory, not from the configuration file's directory.
The same user-scoped registration can therefore select different profile paths
when the server starts from different projects. MCP initialization and tool
discovery can succeed in both projects before any browser launches.

JSON argument strings do not run through a shell: `"--userDataDir=~/test-profile"`
passes a literal `~`. In the checked Linux launcher, that becomes a directory
named `~` under the server's working directory. Use the full absolute path in
JSON. In a POSIX shell command, `"--userDataDir=$PROFILE_DIR"` expands the shell
variable before Claude saves the argument.

To repair a user-scoped persistent launch while retaining its original profile:

1. Inspect `claude mcp get chrome-devtools` from each affected project. Record
   the scope and complete arguments. Stop the affected Claude sessions and their
   owned test browsers before changing the registration. If another scope is
   selected, use [the scope recovery procedure](#recover-the-intended-profile)
   to locate the entry you intend to change.
2. Identify the existing dedicated test profile you want to retain. Resolve it
   on the server host in a POSIX shell:

   ```bash
   PROFILE_DIR="$(cd -- "/ABSOLUTE/PATH/TO/EXISTING/TEST-PROFILE" && pwd -P)"
   printf '%s\n' "$PROFILE_DIR"
   ```

   Replace the placeholder with that existing directory. The command must
   succeed and print its absolute path. If a relative registration has already
   selected several directories, choose the intended one before proceeding;
   do not move, merge, or delete their contents as part of this repair.
3. Replace only the user entry. For the standard pinned server with no custom
   options, run in the same shell:

   ```bash
   claude mcp remove --scope user chrome-devtools
   claude mcp add --scope user chrome-devtools -- npx -y chrome-devtools-mcp@1.12.0 "--userDataDir=$PROFILE_DIR"
   claude mcp get chrome-devtools
   ```

   Preserve any recorded custom executable and other intended launch options
   when adapting the command. Leave out `--isolated=true` and attachment flags
   for this persistent launch. If registration fails after removal, retry the
   corrected add command; the profile directory remains separate from it.
4. Inspect the effective entry from each project again. It should show the
   same absolute profile path and intended scope. Restart the affected sessions,
   then verify the expected test tabs and profile before continuing browser work.
   Updating or uninstalling the instruction plugin does not rewrite this path.

This migration was checked on Linux with Claude Code 2.1.319 and the published
v1.12.0 server. A real MCP tool call reached Puppeteer's launcher with an
argument-recording executable: two working directories selected different
relative paths, while the repaired absolute path stayed the same. The original
synthetic profile file remained unchanged. The executable deliberately exited;
no Chrome session, cookies, profile lock, or browser-data migration was tested.
See the [upstream launch implementation](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/src/BrowserManager.ts)
and [Puppeteer launch options](https://pptr.dev/api/puppeteer.launchoptions).

## Configuration examples

These are MCP configuration objects. For Claude Code project scope, save one as
`.mcp.json` at the project root and approve it through Claude Code's normal MCP
flow. User and local scope are managed by `claude mcp add`; they are stored in
`~/.claude.json` (or the configured Claude config directory), not
`~/.claude/mcp_settings.json`. See [Claude Code's scope documentation](https://code.claude.com/docs/en/mcp#mcp-installation-scopes).

Launch an isolated headless test browser with a chosen viewport:

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@1.12.0", "--isolated=true", "--headless=true", "--viewport=1920x1080"]
    }
  }
}
```

For custom binaries, add an `--executablePath=PATH` argument using the actual
path on the MCP server host. The configuration can initialize even when Chrome
is missing because browser startup is lazy; tool discovery alone does not prove
a browser can launch.

Attach to a separately launched test browser only after following
[the external-browser setup](README.md#connect-to-existing-chrome-instance):

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@1.12.0", "--browserUrl=http://127.0.0.1:9222"]
    }
  }
}
```

## Recover or remove a browser connection

The instruction plugin, MCP registration, running MCP process, and browser have
separate lifecycles. Plugin update and uninstall leave a server registered with
`claude mcp add` unchanged. An existing Claude session can also retain its running
server until it stops or restarts. Removing a registration changes future
configuration; it does not terminate every client already using that server.

### Bound a stalled startup check

`claude mcp get` health-checks the selected registration and can start its stdio
command. Each invocation starts another check; repeating it against a command
that never answers initialization repeats the startup wait. Updating the
instruction plugin does not repair that separate command.

For an already installed stdio server that is stalled during startup, inspect
it from the affected project's root with a short diagnostic budget in a POSIX
shell:

```bash
MCP_TIMEOUT=2000 claude mcp get chrome-devtools
```

This sets the startup timeout to 2,000 milliseconds for this command only, plus
CLI overhead. It leaves the saved registration and normal Claude sessions
unchanged. Read the reported scope and arguments even if the status says
`Failed to connect`; the tested CLI exits zero for that status, so the exit code
alone does not establish a working connection. Keep the result while diagnosing
an unchanged entry, and check again after an actual configuration or server fix.

A first `npx` download or a healthy but slow startup can exceed this short budget.
After repairing the command, run `claude mcp get chrome-devtools` with enough
startup time to verify it normally. Do not save the short diagnostic budget as a
permanent setting. See [Claude Code's startup timeout setting](https://code.claude.com/docs/en/mcp#installing-mcp-servers).

This budget covers MCP initialization, not Chrome launch, CDP attachment, or tool
execution. A connected MCP server can still point at a stale browser endpoint
because Chrome connects on first browser tool use. For that failure, use the
profile and endpoint checks below instead of repeating successful health checks.
The timeout and recovery controls were checked with Claude Code 2.1.319 and
synthetic silent/healthy stdio peers, without launching a browser.

### Recover the intended profile

1. Run `claude mcp get chrome-devtools` from the affected project's root. Inspect
   the reported scope, command, package version, and arguments. For a stalled
   stdio startup, use [the bounded diagnostic command](#bound-a-stalled-startup-check).
   In Claude Code's
   CLI, local scope takes precedence over approved project scope, then user
   scope; entries replace one another in full, without merging isolation flags.
   Project entries still require the normal workspace trust and MCP approval flow. Other client
   surfaces or managed settings can have different precedence; see the
   [official scope hierarchy](https://code.claude.com/docs/en/mcp#scope-hierarchy-and-precedence).
2. Remove an obsolete entry only from the scope you intend to change. For
   example, remove an old private project attachment with:

   ```bash
   claude mcp remove --scope local chrome-devtools
   claude mcp get chrome-devtools
   ```

   The second command can reveal a project or user entry that was hidden by the
   local entry. Review it before using browser tools. To remove a shared project
   entry, use `--scope project` from that project's root; this edits `.mcp.json`
   for the team. Use `--scope user` for a user entry. Repeat inspection after each
   removal until the effective configuration is the intended one.
3. For a fresh launch, use [the user-scoped isolated registration](README.md#register-the-mcp-server)
   after removing an obsolete entry at that scope. For an attachment, verify the
   endpoint belongs to the test browser you launched and its expected profile.
   Close that owned browser when replacing it, then obtain the new endpoint.
4. Stop or restart each affected Claude session to apply the change. In the new
   session, list pages and confirm the expected test tabs before interacting.
   A connected MCP status alone does not establish browser or profile identity.

An HTTP `--browserUrl` rediscovers the WebSocket endpoint when connecting. If the
old browser exits and another process reuses its port, the next connection can
reach a different browser. Treat disconnects, timeouts, and browser restarts as
reasons to check identity again. An exact `--wsEndpoint` with the old browser ID
fails when the replacement exposes only a different ID, but neither that path
nor loopback is authentication: another local process can impersonate the peer.
Use a separately owned test browser and [the external-browser setup](README.md#connect-to-existing-chrome-instance).

### Remove the installation

1. Stop the Claude sessions using the connection. Uninstall the instruction
   plugin at its installed scope; for the README's default user install, run:

   ```bash
   claude plugin uninstall cc_chrome_devtools_mcp_skill@cc_chrome_devtools_mcp_skill-plugin-marketplace
   ```

2. Inspect `claude mcp get chrome-devtools` in each project where you used it.
   Remove each registration you intend to retire using its explicit scope, as
   in the recovery procedure. If the only entry is the README's user entry, run:

   ```bash
   claude mcp remove --scope user chrome-devtools
   claude mcp get chrome-devtools
   ```

   With no other entry, the last command exits nonzero and reports no server
   named `chrome-devtools`. If another entry appears, inspect its scope instead
   of assuming browser access has been removed.
3. Close any externally launched test browser you own. Disconnecting MCP from
   an attached browser leaves that browser and its debugging listener running.
   Remove only that test browser's recorded disposable profile after it exits,
   if you no longer need its data. Persistent profiles remain user data; plugin
   uninstall is not profile deletion. For a manual skill install, remove the
   copied skill separately when you intend to retire it.

Lifecycle checks used temporary Claude Code 2.1.319 configurations. Endpoint
replacement and attachment disconnect were checked with the real v1.12.0
connection code against a synthetic local CDP peer, without launching Chrome.
These checks do not verify real Chrome process termination or profile cleanup.

### Recover from an interrupted local update

With Claude Code 2.1.319, updating from a local marketplace checkout with a
truncated `.claude-plugin/plugin.json` can exit successfully while recording
version `unknown`. The skill then disappears from `plugin details`. Diagnose
the installed state instead of relying on the update command's exit status:

```bash
claude plugin list --json
claude plugin details cc_chrome_devtools_mcp_skill
```

Inspect the matching record's `errors`, `version`, and `readFromFolder`. For a
local marketplace, restore the checkout's complete manifest from a known-good
revision or saved copy, then validate that checkout before retrying:

```bash
claude plugin validate /PATH/TO/cc_chrome_devtools_mcp_skill --json
claude plugin update cc_chrome_devtools_mcp_skill@cc_chrome_devtools_mcp_skill-plugin-marketplace
claude plugin list --json
claude plugin details cc_chrome_devtools_mcp_skill
```

Replace `/PATH/TO/cc_chrome_devtools_mcp_skill` with the local marketplace
checkout. Continue only after validation succeeds, the installed record has
the expected release version and no errors, and details shows one skill and zero
bundled MCP servers.
Restart the affected session to load the repaired instruction package. These
steps were tested with a local checkout; they do not establish remote download
rollback behavior. Repairing the instruction files does not require removing the
separate MCP registration or profile.

An interrupted `.mcp.json` write is a separate failure. In the tested CLI,
`mcp get` can show a user entry while the malformed project entry is ignored;
project-scoped removal refuses to edit the malformed file. Restore its saved,
complete JSON and inspect the effective registration again before scoped removal.
Preserve other server entries and profile data while repairing configuration.

## Captures and filesystem access

Paths are resolved on the MCP server, except uploads whose paths must be
available to the browser. Without negotiated MCP roots or explicit workspaces,
v1.12.0 file tools default to the OS temporary directory. Use a directory allowed
by the current roots/workspace configuration; create its parent first. Prefer a
specific artifact directory over broad filesystem access. A valid input schema
does not establish path permission or file availability.

Request lists are not HAR files. Use Chrome DevTools for native HAR export.
Snapshots expose the accessibility tree; they cannot certify WCAG compliance.
See [tool constraints](TOOLS.md#important-constraints) and
[measurement interpretation](METRICS.md#field-and-lab-data).

## Security considerations

Read [the complete security guidance](SKILL.md#security-considerations), including
profile lifecycle, untrusted page content, artifact redaction, and outbound data
settings. Temporary profiles do not hide browser data from the MCP client.
Attached browsers retain their existing sessions. A loopback debugging port can
be controlled by other local processes.

## Troubleshooting

- **Server missing:** run `claude mcp get chrome-devtools` from the intended
  project. Check registration scope, project approvals, and restart the session
  after configuration changes.
- **Server exits before discovery:** run the pinned package's `--help`, check
  Node compatibility and package access, and inspect `/mcp` in Claude Code.
- **Chrome launch fails:** verify the executable and its version on the server
  host. Supply `--executablePath` if discovery cannot find it. Inspect the actual
  error before changing OS permissions or sandbox settings.
- **Tool or argument rejected:** inspect the connected server's schema. Old
  examples use tab indexes, scalar waits, and separate emulation tools that do
  not match this version. Do not infer schemas from another release.
- **Capture write rejected:** check the server's allowed roots/workspaces and
  parent directory. Use a permitted path rather than disabling all restrictions.

See the [official upstream configuration guide](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/configuration.md)
and [connection guide](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/advanced-usage.md)
for options beyond this package's tested setup.
