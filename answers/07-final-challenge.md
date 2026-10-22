# Final integrative challenge — Answers

> Model answers — many tasks have more than one correct solution.  
> Exercises: [exercises/07-final-challenge.md](../exercises/07-final-challenge.md)

**1.** A representative solution:

```bash
#!/bin/bash
set -euo pipefail
log(){ echo "[$(date '+%F %T')] $1"; }

echo "host: $(hostname)   $(uptime -p)"
df -h /
errors=$(grep -c -i error /var/log/syslog || true)
echo "syslog errors: $errors"
echo 'Top memory:'
ps -eo pid,%mem,comm --sort=-%mem | head -4

log "health check done (errors=$errors)" >> health.log
```

**2.** See the solution above — `-e` stops on error, `-u` errors on unset vars, `-o pipefail` catches failures inside pipelines; `log()` timestamps each message.

**3.** Read the percentage from df and test it numerically.

```bash
pct=$(df --output=pcent / | tr -dc '0-9')
(( pct > 80 )) && echo "WARNING: / is ${pct}% full"
```

**4.** Add it with `crontab -e`:

```bash
*/5 * * * * /home/pi/health.sh
```
