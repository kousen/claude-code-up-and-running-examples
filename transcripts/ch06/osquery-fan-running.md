# Chapter 6 osquery fan-running capture

Date captured: 2026-06-30

Skill: `/osquery` (companion examples repo: `examples/ch06/skills/osquery/`)

Prompt:

```text
/osquery why is my fan running?
```

Follow-up:

```text
Tell me what processes were invoked and what osquery returned.
```

## Processes invoked

The skill executed `osqueryi --json` three times:

| # | Query | Why |
| --- | --- | --- |
| 1 | `SELECT * FROM fan_speed_sensors` | Get actual fan RPM vs min/max |
| 2 | `SELECT * FROM temperature_sensors` | Find heat that would drive the fan |
| 3 | Top five by `(user_time + system_time)` from `processes` | Identify CPU load, the usual cause of heat |

Plus a one-off `osqueryi --version` to confirm installation (5.23.0).

## Data returned

### Fans

Both essentially at idle:

| Fan | Actual RPM | Min | Max |
| --- | --- | --- | --- |
| 0 | 2318 | 2317 | 7826 |
| 1 | 2508 | 2317 | 7826 |

### Temperatures

| Sensor | °C | °F |
| --- | --- | --- |
| Battery TS_MAX | 35.3 | 95.5 |
| GPU Heatsink | 35.0 | 95.0 |
| Airport Proximity | 54.5 | 130.0 |
| Power Supply | 40.0 | 104.0 |
| Palm Rest | 32.8 | 91.1 |

### Top CPU consumers (cumulative)

| Process | CPU % | RSS (MB) |
| --- | --- | --- |
| logioptionsplus_agent | 76.3 | 265 |
| iTerm2 | 34.7 | 369 |
| corespotlightd | 26.0 | 1019 |
| ControlCenter | 25.5 | 108 |
| idea (IntelliJ) | 23.0 | 4305 |

## Verdict

Fans spinning one RPM above their floor (2318 vs min 2317). Hottest core
component was the GPU heatsink at 35°C, far below the ~80°C range where fans
ramp up. Diagnosis: fan at idle baseline, not working hard.

## Manuscript notes

- CPU percentages are **lifetime averages** (`user_time` + `system_time`
  divided by process uptime), not instantaneous load. `logioptionsplus_agent`
  at 76.3% is a long-lived average, not current burn.
- `fan_speed_sensors` and `temperature_sensors` are macOS-oriented; Linux
  readers may see different table names.
- Negative result is the teaching point: skill reported real data instead of
  inventing a culprit.
