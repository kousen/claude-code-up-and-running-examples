---
name: osquery
description: |
  System diagnostics using osquery. Use when asked about CPU usage, memory
  consumption, network connections, running processes, disk I/O, fan speeds,
  temperatures, or system security. Triggers: "why is my computer slow",
  "what's using memory", "what's using CPU", "network connections",
  "suspicious processes", "system health", "fan running", "overheating",
  "disk activity", "what processes are running", "file changes", "browser
  extensions", "Docker containers", "startup programs", "file hash",
  "installed apps", "what runs at boot".
allowed-tools: Bash
---

# Osquery System Diagnostics Skill

Use osquery to answer system diagnostic questions through natural language.

## How to Execute Queries

Run osquery with JSON output for structured data:

```bash
osqueryi --json "YOUR SQL QUERY HERE"
```

**Important**: Always use `--json` flag for parseable output.

## Quick Reference: Common Diagnostics

| User Question | Use This Query |
|---------------|----------------|
| "Why is my computer slow?" | High CPU or High Memory query |
| "What's using all my RAM?" | High Memory query |
| "What's using my network?" | Network Connections query |
| "Is my fan running hot?" | Temperature Info query |
| "Is my system compromised?" | Suspicious Processes query |
| "What's causing disk slowdown?" | High Disk I/O query |
| "Give me a system overview" | System Health Summary |

### Advanced Queries (see Advanced Scenarios section)

| User Question | Use This Query |
|---------------|----------------|
| "What files changed recently?" | File Integrity / `file` table |
| "Verify this file's hash" | Hash Verification query |
| "Show my browser extensions" | Browser and Application Data |
| "What runs at startup?" | Startup Items and Persistence |
| "Show Docker containers" | Container queries |
| "What apps are installed?" | Applications query |

## Predefined Queries

See [queries.md](queries.md) for complete SQL templates with explanations.

## Interpreting Results

### CPU Usage
- **cpu_percent > 50%** for a single process is high
- System processes like `kernel_task`, `WindowServer` are normal consumers
- Browser processes (`Google Chrome Helper`) often top the list - normal

### Memory Usage
- **resident_mb > 1000** (1GB) is significant
- Compare to total system RAM (check with `SELECT physical_memory FROM system_info`)
- Multiple instances of same app (e.g., Chrome tabs) add up

### Network Connections
- `ESTABLISHED` = active connection
- `LISTEN` = waiting for connections (servers)
- Unexpected connections to unknown IPs warrant investigation

### Temperature (macOS)
- CPU temps **under 80C** are normal under load
- **Above 90C** sustained indicates cooling issues
- Fan speeds increase automatically with temperature

### Suspicious Processes
Flagged processes aren't necessarily malware. Common false positives:
- **"No parent process"**: Daemons that outlive their parent are normal
- **"Running from temp"**: Installers and updaters often run from /tmp
- Investigate further with: `SELECT * FROM processes WHERE pid = <pid>`

## Platform Notes

**macOS-specific tables**:
- `temperature_sensors`, `fan_speed_sensors` - Only on macOS
- `launchd` - macOS service manager

**Linux alternatives**:
- Use `/proc` filesystem tables
- `systemd_units` instead of `launchd`

## Error Handling

If you see "no such table", the table may not exist on this platform:
```bash
# List available tables
osqueryi --json "SELECT name FROM osquery_registry WHERE active = 1"
```

## Follow-up Suggestions

After showing results, consider suggesting:
- "Would you like me to investigate any specific process?"
- "Should I check what files this process has open?"
- "Want me to look at the network activity for this process?"

## Advanced Scenarios

For security investigations and specialized queries beyond the common diagnostics above, osquery offers powerful capabilities documented at https://osquery.readthedocs.io/en/stable/

### File Integrity Monitoring

**Triggers**: "file changes", "modified files", "file monitoring", "who changed this file"

Track file modifications in real-time (requires osqueryd daemon, not just osqueryi):
- **macOS**: `file_events` table (FSEvents-based)
- **Linux**: `file_events` (inotify) or `process_file_events` (Audit)
- **Windows**: `ntfs_journal_events` (NTFS Journal)

```sql
-- Check recently modified files in a directory (point-in-time, works with osqueryi)
SELECT path, mtime, size, uid FROM file
WHERE path LIKE '/etc/%' AND mtime > (strftime('%s', 'now') - 3600)
```

**Documentation**: https://osquery.readthedocs.io/en/stable/deployment/file-integrity-monitoring/

### Hash Verification

**Triggers**: "file hash", "verify file", "checksum", "file integrity"

```sql
-- Get hashes for a specific file
SELECT path, md5, sha1, sha256 FROM hash WHERE path = '/usr/bin/ssh'

-- Check hashes of all files in a directory
SELECT path, sha256 FROM hash WHERE directory = '/usr/local/bin'
```

### Advanced SQL Functions

Osquery extends SQLite with useful functions:

| Function | Purpose | Example |
|----------|---------|---------|
| `regex_match(pattern, string, index)` | Pattern matching | `WHERE regex_match('^192\.168\.', remote_address, 0) IS NOT NULL` |
| `in_cidr_block(ip, cidr)` | IP range checking | `WHERE in_cidr_block(remote_address, '10.0.0.0/8')` |
| `split(string, delimiter, index)` | String parsing | `split(cmdline, ' ', 0)` for first argument |
| `version_compare(v1, v2)` | Version comparison | `WHERE version_compare(version, '2.0.0') < 0` |

**Documentation**: https://osquery.readthedocs.io/en/stable/introduction/sql/

### Browser and Application Data

**Triggers**: "browser extensions", "Chrome extensions", "Firefox addons", "installed apps"

```sql
-- Chrome extensions (macOS/Linux)
SELECT name, identifier, version, path FROM chrome_extensions

-- Firefox addons
SELECT name, identifier, version, active FROM firefox_addons

-- Safari extensions (macOS)
SELECT name, identifier, version FROM safari_extensions

-- Installed applications (macOS)
SELECT name, bundle_identifier, bundle_version FROM apps
```

### Startup Items and Persistence

**Triggers**: "startup programs", "auto-start", "persistence", "what runs at boot"

```sql
-- macOS launch agents/daemons
SELECT name, program, run_at_load FROM launchd WHERE run_at_load = '1'

-- Linux systemd services
SELECT id, description, active_state, sub_state FROM systemd_units WHERE active_state = 'active'

-- Cron jobs
SELECT command, path FROM crontab

-- Scheduled tasks (Windows)
SELECT name, action, path, enabled FROM scheduled_tasks WHERE enabled = 1
```

### Container and Virtualization

**Triggers**: "Docker containers", "running containers", "virtual machines"

```sql
-- Docker containers
SELECT id, name, image, state, status FROM docker_containers

-- Docker images
SELECT id, tags, size FROM docker_images

-- Docker networks
SELECT id, name, driver FROM docker_networks
```

### Discovering More Tables

When you need capabilities beyond the predefined queries:

```sql
-- List all available tables on this system
SELECT name FROM osquery_registry WHERE registry = 'table' ORDER BY name

-- Get schema for any table
PRAGMA table_info(table_name_here)

-- Search for tables by keyword
SELECT name FROM osquery_registry WHERE registry = 'table' AND name LIKE '%network%'
```

**Complete schema reference**: https://osquery.io/schema/

### Performance Considerations

Some tables are expensive to query:
- `file` and `hash` tables traverse the filesystem - always constrain with `WHERE path` or `WHERE directory`
- `process_open_files` and `process_open_sockets` are heavier than `processes`
- Event-based tables (`*_events`) require the osqueryd daemon

**Documentation**: https://osquery.readthedocs.io/en/stable/deployment/performance-safety/
