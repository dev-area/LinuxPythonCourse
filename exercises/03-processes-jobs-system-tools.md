# 3 · Processes, Jobs & System Tools — Exercises

> Answers: [answers/03-processes-jobs-system-tools.md](../answers/03-processes-jobs-system-tools.md)

**1.** Which command gives a live, sorted view of processes, and how do you sort it by memory?

**2.** Find the PIDs of all running `bash` processes.

**3.** Display the process tree.

**4.** What is the difference between `kill PID` and `kill -9 PID`?

**5.** Kill every process named `firefox`, by name.

**6.** Start `./long_task.sh` in the background, list your jobs, then bring it to the foreground.

**7.** Suspend the current foreground job and resume it in the background.

**8.** Run `backup.sh` so it keeps running after you log out and discards its output.

**9.** Write the commands to restart the `ssh` service and make it start at boot.

**10.** Check whether `nginx` is currently active and whether it is enabled at boot.

**11.** Show the `ssh` service log from the systemd journal since 1 hour ago.

**12.** Follow new kernel messages live.

**13.** Show the 5 processes using the most CPU right now (a snapshot).

**14.** Which commands report (a) free space on `/` and (b) the total size of `/var/log`?

**15.** Show memory and swap usage in human units, and the system load averages.

**16.** What is a zombie process (`STAT Z`), and how does it usually get cleaned up?

**17.** List all listening TCP ports together with the process that owns each.

**18.** Install the package `htop` on a Debian/Ubuntu system.
