# Osquery Query Templates

## High CPU Processes

**Triggers**: "slow computer", "CPU usage", "what's using CPU", "laggy"

```sql
SELECT name, pid, uid, (user_time + system_time) AS cpu_time,
ROUND(((user_time + system_time) * 100.0 / (SELECT SUM(user_time + system_time) FROM processes)), 2) AS cpu_percent
FROM processes ORDER BY cpu_time DESC LIMIT 10
```

**Baseline guidance**:
- Single process > 50% CPU sustained = investigate
- `kernel_task`, `WindowServer` (macOS) normally high
- Browser helpers consuming CPU often = too many tabs or heavy pages
- `mds`, `mdworker` (Spotlight indexing) spikes are temporary

---

## High Memory Processes

**Triggers**: "memory usage", "RAM", "what's eating memory", "out of memory"

```sql
SELECT name, pid, uid,
ROUND(resident_size / 1024.0 / 1024.0, 2) AS resident_mb,
ROUND(total_size / 1024.0 / 1024.0, 2) AS total_mb
FROM processes ORDER BY resident_size DESC LIMIT 10
```

**Baseline guidance**:
- Check total RAM: `SELECT physical_memory FROM system_info`
- Process using > 25% of total RAM = significant
- Browsers, IDEs, Docker commonly use 1-4GB each
- `kernel_task` memory is normal and managed by macOS

---

## Network Connections

**Triggers**: "network connections", "what's using internet", "connected to", "network activity"

```sql
SELECT DISTINCT p.name, p.pid, pos.local_address, pos.local_port,
pos.remote_address, pos.remote_port, pos.state
FROM process_open_sockets pos
JOIN processes p ON pos.pid = p.pid
WHERE pos.state = 'ESTABLISHED' OR pos.state = 'LISTEN'
```

**Interpreting states**:
- `ESTABLISHED` = active bidirectional connection
- `LISTEN` = server waiting for connections
- `TIME_WAIT` = connection closing (normal cleanup)

**Common legitimate connections**:
- `cloudd`, `apsd` = Apple cloud services
- `Dropbox`, `OneDrive` = file sync
- Browsers to ports 443 (HTTPS), 80 (HTTP)
- `ssh`, `sshd` on port 22

---

## Temperature and Fan Info (macOS)

**Triggers**: "fan running", "overheating", "temperature", "hot computer", "thermal"

```sql
-- Temperature sensors
SELECT name, celsius FROM temperature_sensors

-- Fan speeds
SELECT fan, name, actual, min, max FROM fan_speed_sensors
```

**Baseline guidance**:
- **Idle CPU**: 40-60C is normal
- **Under load**: 70-85C is acceptable
- **> 90C sustained**: Cooling problem, check vents/fans
- Fan RPM increases automatically with temperature
- High fan + normal temp = cooling working correctly
- High fan + high temp = heavy workload or blocked airflow

---

## Suspicious Processes

**Triggers**: "suspicious", "malware", "security check", "compromised", "virus"

```sql
SELECT p.name, p.pid, p.parent, p.uid, p.path,
CASE
    WHEN p.parent = 0 AND p.pid != 1 THEN 'No parent process'
    WHEN p.path LIKE '/tmp/%' OR p.path LIKE '/var/tmp/%' THEN 'Running from temp directory'
    WHEN p.on_disk = 0 THEN 'Not on disk'
    ELSE 'Flagged'
END as suspicious_reason,
(p.user_time + p.system_time) as cpu_time
FROM processes p
WHERE (p.parent = 0 AND p.pid != 1)
   OR p.path LIKE '/tmp/%'
   OR p.path LIKE '/var/tmp/%'
   OR p.on_disk = 0
ORDER BY cpu_time DESC
LIMIT 20
```

**Understanding the flags**:
- **No parent process**: Process outlived parent. Common for daemons, but could indicate orphaned malware.
- **Running from temp**: Installers, updaters run from /tmp. Persistence from temp is suspicious.
- **Not on disk**: Binary no longer exists on filesystem. Could be deleted malware or staged Apple services (often false positive).

**Follow-up investigation**:
```sql
-- Check what files a process has open
SELECT path FROM process_open_files WHERE pid = <pid>

-- Check network connections for a process
SELECT * FROM process_open_sockets WHERE pid = <pid>

-- Get detailed process info
SELECT * FROM processes WHERE pid = <pid>
```

---

## High Disk I/O Processes

**Triggers**: "disk activity", "disk slow", "hard drive busy", "disk usage"

```sql
SELECT p.name, p.pid, p.uid,
ROUND(p.disk_bytes_read / 1024.0 / 1024.0, 2) AS disk_read_mb,
ROUND(p.disk_bytes_written / 1024.0 / 1024.0, 2) AS disk_write_mb,
ROUND((p.disk_bytes_read + p.disk_bytes_written) / 1024.0 / 1024.0, 2) AS total_disk_mb,
p.path
FROM processes p
WHERE p.disk_bytes_read > 0 OR p.disk_bytes_written > 0
ORDER BY (p.disk_bytes_read + p.disk_bytes_written) DESC
LIMIT 15
```

**Common high-I/O processes**:
- `mds`, `mdworker` = Spotlight indexing (temporary)
- `Time Machine` = backup in progress
- `fsck` = disk repair
- IDEs indexing large projects

---

## System Health Summary

**Triggers**: "system health", "overview", "status", "how's my system"

Run multiple queries and combine:
1. High CPU processes
2. High Memory processes
3. Disk usage: `SELECT path, blocks_available, blocks, inodes_free FROM mounts WHERE path = '/'`
4. Network connections
5. Temperature and fans (macOS)

---

## Utility Queries

### List Available Tables
```sql
SELECT name FROM osquery_registry WHERE active = 1
```

### Get Table Schema
```sql
PRAGMA table_info(TABLE_NAME)
```

### System Information
```sql
SELECT hostname, cpu_brand, physical_memory, hardware_vendor, hardware_model FROM system_info
```

### Disk Space
```sql
SELECT path, ROUND(blocks_available * blocks_size / 1024.0 / 1024.0 / 1024.0, 2) AS free_gb,
ROUND(blocks * blocks_size / 1024.0 / 1024.0 / 1024.0, 2) AS total_gb
FROM mounts WHERE path = '/'
```

### Logged In Users
```sql
SELECT user, host, time FROM logged_in_users
```

### Recently Modified Files (last hour)
```sql
SELECT path, mtime, size FROM file
WHERE path LIKE '/Users/%' AND mtime > (strftime('%s', 'now') - 3600)
```

### Running Services (macOS)
```sql
SELECT name, label, program, disabled FROM launchd WHERE disabled = '0'
```

---

## Find Application Processes

**Triggers**: "is X running", "find app", "what sessions", "Claude processes", "Docker processes"

```sql
-- Generic pattern: replace APP_NAME with the application
SELECT name, pid, path, cmdline
FROM processes
WHERE name LIKE '%APP_NAME%'
   OR cmdline LIKE '%APP_NAME%'
   OR path LIKE '%APP_NAME%'
```

**Common applications**:
```sql
-- Claude (Desktop + Code CLI)
SELECT name, pid, path, cmdline FROM processes
WHERE name LIKE '%claude%' OR cmdline LIKE '%claude%' OR path LIKE '%claude%'

-- Docker
SELECT name, pid, path FROM processes WHERE name LIKE '%docker%'

-- Node.js applications
SELECT name, pid, cmdline FROM processes WHERE name = 'node'

-- Python scripts
SELECT name, pid, cmdline FROM processes WHERE name LIKE '%python%' OR name LIKE '%Python%'
```

---

## Debugging: Check Table Schema

**Triggers**: "what columns", "table schema", "column names"

When a query fails with "no such column", check the actual schema:

```sql
PRAGMA table_info(TABLE_NAME)
```

Example output shows column names and types available.

---

## Example Queries for Common Scenarios

| Scenario | Query |
|----------|-------|
| "What Chrome tabs are using memory?" | `SELECT name, pid, resident_size FROM processes WHERE name LIKE '%Chrome%' ORDER BY resident_size DESC` |
| "Is Docker running?" | `SELECT name, pid, state FROM processes WHERE name LIKE '%docker%'` |
| "What's listening on port 8080?" | `SELECT p.name, pos.* FROM process_open_sockets pos JOIN processes p ON pos.pid = p.pid WHERE pos.local_port = 8080` |
| "Show me Java processes" | `SELECT name, pid, path, cmdline FROM processes WHERE name LIKE '%java%'` |
| "What started in the last 10 minutes?" | `SELECT name, pid, start_time FROM processes WHERE start_time > (strftime('%s', 'now') - 600) ORDER BY start_time DESC` |
| "Find Claude sessions" | `SELECT name, pid, cmdline FROM processes WHERE cmdline LIKE '%claude%'` |

---

# Advanced Queries

These queries cover scenarios beyond basic system diagnostics. For full documentation, see https://osquery.readthedocs.io/en/stable/

---

## File Integrity and Hashing

**Triggers**: "file changes", "modified files", "file hash", "checksum", "verify file"

### Recently Modified Files

```sql
-- Files modified in the last hour in a specific directory
SELECT path, mtime, size, uid FROM file
WHERE path LIKE '/etc/%' AND mtime > (strftime('%s', 'now') - 3600)

-- Modified config files (last 24 hours)
SELECT path, mtime, size FROM file
WHERE (path LIKE '/etc/%' OR path LIKE '%.conf')
AND mtime > (strftime('%s', 'now') - 86400)
ORDER BY mtime DESC
```

**Important**: Always constrain the `file` table with a `WHERE path` clause to avoid full filesystem scans.

### File Hash Verification

```sql
-- Get all hashes for a specific file
SELECT path, md5, sha1, sha256 FROM hash WHERE path = '/usr/bin/ssh'

-- Hash all files in a directory
SELECT path, sha256 FROM hash WHERE directory = '/usr/local/bin'

-- Compare file to known hash
SELECT path, sha256,
CASE WHEN sha256 = 'expected_hash_here' THEN 'MATCH' ELSE 'MISMATCH' END as status
FROM hash WHERE path = '/path/to/file'
```

---

## Browser Extensions and Add-ons

**Triggers**: "browser extensions", "Chrome extensions", "Firefox addons", "Safari extensions"

```sql
-- Chrome extensions
SELECT name, identifier, version, description, path
FROM chrome_extensions
ORDER BY name

-- Firefox addons
SELECT name, identifier, version, active, visible, path
FROM firefox_addons
WHERE active = 1

-- Safari extensions (macOS)
SELECT name, identifier, version
FROM safari_extensions
```

**Interpreting results**:
- Check `identifier` for known malicious extension IDs
- Extensions with generic names + recent install = suspicious
- Extensions with excessive permissions warrant review

---

## Installed Applications

**Triggers**: "installed apps", "what apps", "application list", "software inventory"

```sql
-- macOS: All installed applications
SELECT name, bundle_identifier, bundle_version, path
FROM apps
ORDER BY name

-- macOS: Recently installed apps (by install receipt)
SELECT name, version, location, install_time
FROM package_receipts
ORDER BY install_time DESC
LIMIT 20

-- Linux: Installed packages (Debian/Ubuntu)
SELECT name, version, source, size
FROM deb_packages
ORDER BY name

-- Linux: Installed packages (RHEL/CentOS)
SELECT name, version, release, arch
FROM rpm_packages
ORDER BY name
```

---

## Startup and Persistence

**Triggers**: "startup programs", "auto-start", "what runs at boot", "persistence", "launch agents"

### macOS

```sql
-- Launch agents and daemons configured to run at load
SELECT name, label, program, program_arguments, run_at_load, keep_alive
FROM launchd
WHERE run_at_load = '1'
ORDER BY name

-- Login items
SELECT name, path, hidden FROM login_items
```

### Linux

```sql
-- Active systemd services
SELECT id, description, active_state, sub_state, fragment_path
FROM systemd_units
WHERE active_state = 'active' AND sub_state = 'running'
ORDER BY id

-- Cron jobs (scheduled tasks)
SELECT minute, hour, day_of_month, month, day_of_week, command, path
FROM crontab
```

### Windows

```sql
-- Scheduled tasks
SELECT name, action, path, enabled, last_run_time, next_run_time
FROM scheduled_tasks
WHERE enabled = 1
ORDER BY name

-- Startup items from registry
SELECT name, path, source
FROM startup_items
```

---

## Docker and Containers

**Triggers**: "Docker containers", "running containers", "container images", "Docker status"

```sql
-- Running containers
SELECT id, name, image, state, status, created, started_at
FROM docker_containers
WHERE state = 'running'

-- All containers (including stopped)
SELECT id, name, image, state, status
FROM docker_containers
ORDER BY created DESC

-- Docker images
SELECT id, tags, size, created
FROM docker_images
ORDER BY created DESC

-- Docker networks
SELECT id, name, driver, scope
FROM docker_networks

-- Docker volumes
SELECT name, driver, mount_point
FROM docker_volumes
```

---

## Advanced SQL Patterns

### Using Regex

```sql
-- Find processes with suspicious command lines
SELECT name, pid, cmdline FROM processes
WHERE regex_match('(curl|wget).*\|.*sh', cmdline, 0) IS NOT NULL

-- Find local network connections
SELECT p.name, pos.remote_address, pos.remote_port
FROM process_open_sockets pos
JOIN processes p ON pos.pid = p.pid
WHERE regex_match('^(192\.168\.|10\.|172\.1[6-9]\.|172\.2[0-9]\.|172\.3[01]\.)', pos.remote_address, 0) IS NOT NULL
```

### Using CIDR Blocks

```sql
-- Find connections to private networks
SELECT p.name, pos.remote_address, pos.remote_port
FROM process_open_sockets pos
JOIN processes p ON pos.pid = p.pid
WHERE in_cidr_block(pos.remote_address, '10.0.0.0/8')
   OR in_cidr_block(pos.remote_address, '172.16.0.0/12')
   OR in_cidr_block(pos.remote_address, '192.168.0.0/16')

-- Find connections outside private ranges (potential data exfiltration)
SELECT p.name, pos.remote_address, pos.remote_port
FROM process_open_sockets pos
JOIN processes p ON pos.pid = p.pid
WHERE pos.remote_address != ''
  AND NOT in_cidr_block(pos.remote_address, '10.0.0.0/8')
  AND NOT in_cidr_block(pos.remote_address, '172.16.0.0/12')
  AND NOT in_cidr_block(pos.remote_address, '192.168.0.0/16')
  AND NOT in_cidr_block(pos.remote_address, '127.0.0.0/8')
```

### Version Comparisons

```sql
-- Find outdated packages (version less than target)
SELECT name, version FROM deb_packages
WHERE version_compare(version, '2.0.0') < 0

-- Chrome extensions older than a specific version
SELECT name, version FROM chrome_extensions
WHERE version_compare(version, '1.5.0') < 0
```

---

## Security Investigation Queries

**Triggers**: "security audit", "incident response", "forensics", "threat hunting"

```sql
-- Processes with open files in sensitive locations
SELECT DISTINCT p.name, p.pid, pof.path
FROM process_open_files pof
JOIN processes p ON pof.pid = p.pid
WHERE pof.path LIKE '/etc/%'
   OR pof.path LIKE '%/.ssh/%'
   OR pof.path LIKE '%/passwd%'

-- Users with login shells
SELECT username, uid, gid, shell, directory
FROM users
WHERE shell NOT LIKE '%nologin%' AND shell NOT LIKE '%false%'

-- SUID binaries (potential privilege escalation)
SELECT path, mode, uid, gid FROM file
WHERE path LIKE '/usr/%' AND mode LIKE '%s%'

-- Listening services on non-standard ports
SELECT p.name, pos.local_port, pos.protocol
FROM process_open_sockets pos
JOIN processes p ON pos.pid = p.pid
WHERE pos.state = 'LISTEN'
  AND pos.local_port NOT IN (22, 80, 443, 8080, 3000, 5000)
ORDER BY pos.local_port
```

---

## Documentation References

| Topic | URL |
|-------|-----|
| Complete schema reference | https://osquery.io/schema/ |
| SQL functions | https://osquery.readthedocs.io/en/stable/introduction/sql/ |
| File Integrity Monitoring | https://osquery.readthedocs.io/en/stable/deployment/file-integrity-monitoring/ |
| Performance tuning | https://osquery.readthedocs.io/en/stable/deployment/performance-safety/ |
| Process auditing | https://osquery.readthedocs.io/en/stable/deployment/process-auditing/ |
