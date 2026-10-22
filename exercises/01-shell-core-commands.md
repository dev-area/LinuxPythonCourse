# 1 · The Shell & Core Commands — Exercises

> Answers: [answers/01-shell-core-commands.md](../answers/01-shell-core-commands.md)

**1.** Write one command that lists all files (including hidden) in `/var/log`, long format, oldest first.

**2.** A directory contains: `a.txt`, `b.log`, `c.txt`. What does the shell expand this to?

```bash
echo *.txt
```

**3.** Print the absolute path of your current directory.

**4.** Create the directory tree `project/src/tests` with a single command.

**5.** Create an empty file `log.txt` without an editor — two different ways.

**6.** Copy `file1` into `dir/`, then copy the whole tree `src/` into `backup/`.

**7.** Rename `report.txt` to `report.bak`, then move it into the `archive/` directory.

**8.** Show the first 5 lines and (separately) the last 5 lines of `/etc/passwd`.

**9.** Explain the difference between `>` and `>>` and give one example of each.

**10.** Redirect BOTH stdout and stderr of `make` into `build.log`.

**11.** Write a pipeline that counts how many lines of `access.log` contain "404".

**12.** Use a pipe to show the 3 largest files in the current directory.

**13.** Predict the output of `ls file?.txt` when `file1.txt`, `file12.txt` and `fileA.txt` exist.

**14.** What is the difference between `cmd1 && cmd2` and `cmd1 ; cmd2`?

**15.** What do each of these do: `cd ~`, `cd -`, `cd ..`?

**16.** Is `ls` a program and `cd` a builtin? How would you check?

**17.** How do you re-run the previous command, and search your command history?
