# 2 · Files, Users & Permissions — Exercises

> Answers: [answers/02-files-users-permissions.md](../answers/02-files-users-permissions.md)

**1.** Decode the permission string `-rwxr-x---`: who may read, write and execute?

**2.** Convert `rwxr-xr--` to octal, and convert `640` back to symbolic.

**3.** Which octal makes a directory `rwxr-x---`?

**4.** Make `deploy.sh` executable for everyone (owner keeps full access).

**5.** Give the group write permission on `shared.txt` using symbolic mode.

**6.** Remove read permission for others on `secret.conf`.

**7.** Who are you, and which groups do you belong to?

**8.** Change the group of `report.txt` to `devs`; then do it recursively for the dir `project/`.

**9.** Why do you need the `x` bit on a directory, and what does the `r` bit on a directory give you?

**10.** Explain the difference between a hard link and a symbolic link.

**11.** Create a symbolic link `latest` → `releases/v2.3`, then show it with `ls -l`.

**12.** Create a gzip-compressed tar archive of `/var/log` named `logs.tgz`, then list its contents.

**13.** Extract only the single file `etc/hosts` from the archive `backup.tgz`.

**14.** Find every `*.tmp` file under the current directory modified more than 7 days ago and delete it.

**15.** Find all files larger than 100 MB under `/var`.

**16.** Find all files under `/home` owned by user `pi` and change their owner to `root`.

**17.** After `chmod 644 script.sh`, can you run `./script.sh`? Why, and how would you run it anyway?

**18.** What files/dirs does `umask 022` produce by default, and what is the sticky bit for?
