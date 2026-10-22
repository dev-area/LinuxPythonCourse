# 4 · Text Processing — grep, regex, sed, awk — Exercises

> Answers: [answers/04-text-processing.md](../answers/04-text-processing.md)

### grep & regular expressions

**1.** Print, with line numbers, all lines of `app.log` containing "error" (case-insensitive).

**2.** Recursively search `src/` for the word `TODO`, showing file name and line number.

**3.** Count the lines in `access.log` that do NOT contain "200".

**4.** Print the lines of `/etc/passwd` whose login shell is `/bin/bash`.

### regex

**5.** Write a `grep -E` pattern that matches a line starting with a capital letter and ending with a period.

**6.** Write a pattern matching a line that is empty or contains only whitespace.

**7.** Write a pattern matching an IPv4-looking address.

**8.** Write a pattern that matches both `gray` and `grey`.

### sed

**9.** Replace every "DEBUG" with "INFO" in `app.log`, printing the result (don't change the file).

**10.** Delete all blank lines from `notes.txt`, in place, keeping a `.bak` backup.

**11.** Delete all comment lines (starting with `#`) from a config file.

**12.** Using sed, print only lines 10 to 20 of a file.

**13.** On lines 4–9 only, replace `nologin` with `virtual`.

**14.** Insert a header line `NAME,AGE` before the first line of a file.

**15.** Swap the two comma-separated fields on each line using capture groups.

**16.** What does this print, and why?

```bash
sed -n '/^root/p' /etc/passwd
```

### awk

**17.** Print the 1st and 3rd whitespace-separated fields of every line of `emp`.

**18.** Print the username and login shell (fields 1 and 7) of `/etc/passwd`.

**19.** Print the usernames of accounts whose UID (field 3) is ≥ 1000.

**20.** Prefix every line of a file with its line number.

**21.** Print only the LAST field of each line, whatever the column count.

**22.** Sum the 5th column of a file and print the total.

**23.** Compute the average of column 2.

**24.** Count how many times each value appears in column 1 (associative array).

**25.** Write an awk program that prints a header (`BEGIN`), each line, and the record count (`END`).
