# 5 · Command Reference (utilities) — Answers

> Model answers — many tasks have more than one correct solution.  
> Exercises: [exercises/05-command-reference.md](../exercises/05-command-reference.md)

**1.** `-d` delimiter, `-f` field.

```bash
cut -d: -f1 /etc/passwd
```

**2.** `-c` cuts by character position.

```bash
cut -c1-8 file
```

**3.** `-n` numeric, `-r` reverse.

```bash
sort -rn nums
```

**4.**

```bash
sort -u names.txt
```

**5.** `-t` sets the separator, `-k` the key field.

```bash
sort -t: -k3 -n /etc/passwd
```

**6.** Extract → sort (make dups adjacent) → `uniq -c` → sort by count → head.

```bash
awk '{print $1}' access.log | sort | uniq -c | sort -rn | head -5
```

**7.**

```bash
awk '{print $1}' access.log | sort -u | wc -l
```

**8.** `comm` columns: `-2 -3` suppress cols 2 and 3, leaving 'only in a'.

```bash
comm -23 a.txt b.txt
```

**9.** `wc` prints lines, words, bytes.

```bash
wc essay.txt
```

**10.** `scale` sets decimals.

```bash
echo "scale=4; 22/7" | bc
```

**11.** `paste -s` puts them on one line joined by `+`; `bc` evaluates.

```bash
paste -sd+ nums | bc
```

**12.** `-u` is the format git/patch use.

```bash
diff -u old.c new.c > change.patch
```

**13.** `-h` human sizes; `sort -h` orders by size (largest last).

```bash
du -h --max-depth=1 /home | sort -h
```

**14.** A file named `notes.txt` that is really a JPEG: `file notes.txt` → 'JPEG image data'. `file` reads the magic number, not the name.

**15.** `paste` joins corresponding lines; `-d` sets the delimiter.

```bash
paste -d, names.txt ages.txt
```

**16.** Both files must be sorted on the key first.

```bash
join employees.txt salaries.txt
```

**17.** `-s` breaks at spaces, `-w` sets the width.

```bash
fold -s -w 60 file
```

**18.** `od` (or `xxd`) dumps the bytes.

```bash
od -A x -t x1 file
```

**19.** `-l` lines per piece; `part_` is the prefix.

```bash
split -l 1000 big.log part_
```

**20.** Type the command at the `at>` prompt, then `Ctrl+D`.

```bash
at now + 10 minutes
at> ./backup.sh
at> ^D
```
