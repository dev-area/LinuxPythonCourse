# 1 · The Shell & Core Commands — Answers

> Model answers — many tasks have more than one correct solution.  
> Exercises: [exercises/01-shell-core-commands.md](../exercises/01-shell-core-commands.md)

**1.** `a` = all, `l` = long, `t` = by time, `r` = reverse.

```bash
ls -latr /var/log
```

**2.** The shell expands the glob before `echo` runs; `b.log` doesn't match.

```text
a.txt c.txt
```

**3.**

```bash
pwd
```

**4.** `-p` creates missing parents.

```bash
mkdir -p project/src/tests
```

**5.**

```bash
touch log.txt
> log.txt
```

**6.** `-r` (recursive) is needed for directories.

```bash
cp file1 dir/
cp -r src backup
```

**7.** `mv` both renames and moves.

```bash
mv report.txt report.bak
mv report.bak archive/
```

**8.**

```bash
head -n 5 /etc/passwd
tail -n 5 /etc/passwd
```

**9.** `>` creates/overwrites; `>>` appends.

```bash
ls > files.txt      # overwrite
date >> files.txt   # append
```

**10.** `2>&1` sends stderr to wherever stdout goes; `&>` is the bash shortcut.

```bash
make > build.log 2>&1
# or:  make &> build.log
```

**11.**

```bash
grep -c 404 access.log
# or: grep 404 access.log | wc -l
```

**12.** `-S` sorts by size (largest first); `head` takes the top rows.

```bash
ls -lS | head -4
```

**13.** `?` matches exactly one character, so `file12.txt` is excluded.

```text
file1.txt  fileA.txt
```

**14.** `&&` runs `cmd2` only if `cmd1` succeeded (exit 0); `;` runs `cmd2` regardless.

**15.** `cd ~` → home directory; `cd -` → the previous directory; `cd ..` → the parent directory.

**16.** Use `type`: `type ls` → an executable in `/bin`; `type cd` → a shell builtin (it must change the shell's own directory).

**17.** `!!` (or the Up arrow) re-runs the last command; `Ctrl+R` searches history interactively; `history` lists it.
