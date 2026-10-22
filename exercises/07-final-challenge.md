# Final integrative challenge — Exercises

> Answers: [answers/07-final-challenge.md](../answers/07-final-challenge.md)

Write a script `health.sh` that produces a quick system-health report and logs it.

**1.** Write `health.sh` producing a quick system-health report and logging it. It must, in order:

- print the hostname and uptime
- report the disk usage of `/` (`df`)
- count the "error" lines in `/var/log/syslog` (`grep` + `wc`)
- list the top 3 memory-consuming processes (`ps` + `sort` + `head`)
- append one timestamped summary line to `health.log`

**2.** Make the script robust: add `set -euo pipefail` and a `log()` function for timestamped messages.

**3.** Add a WARNING line when the usage of `/` exceeds 80%.

**4.** Bonus: schedule `health.sh` to run every 5 minutes with `cron`. Write the crontab line.
