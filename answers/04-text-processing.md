# 4 · Text Processing — grep, regex, sed, awk — Answers

> Model answers — many tasks have more than one correct solution.  
> Exercises: [exercises/04-text-processing.md](../exercises/04-text-processing.md)

**1.** `-i` ignore case, `-n` line numbers.

```bash
grep -in error app.log
```

**2.**

```bash
grep -rn TODO src/
```

**3.** `-v` inverts the match, `-c` counts.

```bash
grep -vc 200 access.log
```

**4.** `$` anchors the end of the line.

```bash
grep '/bin/bash$' /etc/passwd
```

**5.** `^` start, `$` end, `\.` literal dot.

```bash
grep -E '^[A-Z].*\.$' file
```

**6.**

```bash
grep -E '^[[:space:]]*$' file
```

**7.** Four dot-separated groups of 1–3 digits.

```bash
grep -E '([0-9]{1,3}\.){3}[0-9]{1,3}' file
```

**8.** `[ae]` is a character class.

```bash
grep -E 'gr[ae]y' file
```

**9.** `g` = every match on the line.

```bash
sed 's/DEBUG/INFO/g' app.log
```

**10.**

```bash
sed -i.bak '/^$/d' notes.txt
```

**11.**

```bash
sed '/^#/d' config
```

**12.** `-n` suppresses auto-print; the range selects.

```bash
sed -n '10,20p' file
```

**13.** An address range before the `s` command.

```bash
sed '4,9 s/nologin/virtual/' file
```

**14.** `1i` inserts before line 1.

```bash
sed '1i NAME,AGE' file
```

**15.** `\1` and `\2` are the captured groups.

```bash
sed -E 's/([^,]*),([^,]*)/\2,\1/' file
```

**16.** Only the lines of `/etc/passwd` that begin with `root` — `-n` turns off auto-printing so only matched lines show.

**17.**

```bash
awk '{print $1, $3}' emp
```

**18.** `-F` sets the input field separator.

```bash
awk -F: '{print $1, $7}' /etc/passwd
```

**19.** A condition before the action filters rows.

```bash
awk -F: '$3 >= 1000 {print $1}' /etc/passwd
```

**20.** `NR` is the record (line) number.

```bash
awk '{print NR": "$0}' file
```

**21.** `$NF` is the last field.

```bash
awk '{print $NF}' file
```

**22.** Vars start at 0; `END` runs after the last line.

```bash
awk '{s += $5} END{print s}' file
```

**23.**

```bash
awk '{s += $2} END{print s/NR}' file
```

**24.** Array keyed by the field; `for-in` walks the keys.

```bash
awk '{c[$1]++} END{for(k in c) print c[k], k}' file
```

**25.**

```bash
awk 'BEGIN{print "Report"; print "======"}
     {print}
     END{print "records:", NR}' file
```
