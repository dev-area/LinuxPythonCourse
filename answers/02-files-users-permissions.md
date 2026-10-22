# 2 · Files, Users & Permissions — Answers

> Model answers — many tasks have more than one correct solution.  
> Exercises: [exercises/02-files-users-permissions.md](../exercises/02-files-users-permissions.md)

**1.** Owner: read+write+execute. Group: read+execute. Others: nothing. (Leading `-` = regular file.)

**2.** `rwxr-xr--` = `754`. `640` = `rw-r-----`.

**3.** `750`.

**4.** `755` = `rwx` owner, `r-x` group & others.

```bash
chmod 755 deploy.sh
```

**5.**

```bash
chmod g+w shared.txt
```

**6.**

```bash
chmod o-r secret.conf
```

**7.**

```bash
whoami
id
groups
```

**8.**

```bash
chgrp devs report.txt
chgrp -R devs project/
```

**9.** `x` lets you enter/traverse the directory (`cd` into it, access files by name); `r` lets you list the names it contains. You often need both.

**10.** A hard link is another name for the same data (same inode) — same filesystem only, survives deleting the original. A symlink points to a path — can cross filesystems and dangles if the target is removed.

**11.**

```bash
ln -s releases/v2.3 latest
ls -l latest
```

**12.** `c` = create, `z` = gzip, `v` = verbose, `f` = file; `t` = list.

```bash
tar -czvf logs.tgz /var/log
tar -tzvf logs.tgz
```

**13.** Name the member after the archive.

```bash
tar -xzvf backup.tgz etc/hosts
```

**14.** `-mtime +7` = older than 7 days.

```bash
find . -name '*.tmp' -mtime +7 -delete
```

**15.**

```bash
find /var -type f -size +100M
```

**16.** `-user` filters by owner; `-exec ... {} +` runs `chown` on the matches.

```bash
sudo find /home -user pi -exec chown root {} +
```

**17.** No — `644` has no execute bit, so `./script.sh` gives 'Permission denied'. Either `chmod +x script.sh` or run it via the interpreter: `bash script.sh`.

**18.** `umask 022` → new files `644`, new dirs `755` (it removes those bits from the defaults). The sticky bit on a shared dir (`chmod +t /shared`) lets users delete only their own files.
