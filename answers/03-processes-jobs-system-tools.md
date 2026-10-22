# 3 · Processes, Jobs & System Tools — Answers

> Model answers — many tasks have more than one correct solution.  
> Exercises: [exercises/03-processes-jobs-system-tools.md](../exercises/03-processes-jobs-system-tools.md)

**1.** `top` (or `htop`). Inside `top` press `Shift+M` for memory (`P` = CPU, `T` = time, `q` = quit).

**2.**

```bash
pgrep bash
# or: ps -e | grep bash
```

**3.**

```bash
pstree
# or: ps auxf
```

**4.** `kill` sends `SIGTERM` — a polite request; the process can clean up and exit. `kill -9` sends `SIGKILL` — the kernel kills it at once, no cleanup. Try `SIGTERM` first.

**5.**

```bash
pkill firefox
# or: killall firefox
```

**6.**

```bash
./long_task.sh &
jobs
fg %1
```

**7.** `Ctrl+Z` suspends; `bg` resumes it in the background.

```bash
^Z
bg
```

**8.** `nohup` detaches from the terminal; `&` backgrounds it.

```bash
nohup ./backup.sh &>/dev/null &
```

**9.**

```bash
sudo systemctl restart ssh
sudo systemctl enable ssh
```

**10.**

```bash
systemctl status nginx
systemctl is-enabled nginx
```

**11.**

```bash
journalctl -u ssh --since "1 hour ago"
```

**12.** `journalctl -kf` (or `dmesg -w`).

```bash
journalctl -kf
```

**13.**

```bash
ps -eo pid,%cpu,comm --sort=-%cpu | head -6
```

**14.** `df` for filesystem free space, `du` for a directory's size.

```bash
df -h /
du -sh /var/log
```

**15.**

```bash
free -h
uptime
```

**16.** A child that has finished but whose parent hasn't read its exit status yet. It's reaped when the parent calls `wait()`; if the parent dies, init/systemd adopts and reaps it.

**17.**

```bash
sudo ss -tlnp
```

**18.** Always update the index first.

```bash
sudo apt update
sudo apt install htop
```
