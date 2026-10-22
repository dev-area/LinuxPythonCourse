# 6 · BASH Scripting — Answers

> Model answers — many tasks have more than one correct solution.  
> Exercises: [exercises/06-bash-scripting.md](../exercises/06-bash-scripting.md)

**1.**

```bash
#!/bin/bash
name="Liran"
echo "Hello, $name"
```

**2.** `read -p` shows a prompt and stores the reply.

```bash
#!/bin/bash
read -p "Name: " n
echo "Hi, $n"
```

**3.** `$#` is the count; `${!#}` is indirect expansion of the last positional.

```bash
#!/bin/bash
echo "count: $#"
echo "last:  ${!#}"
```

**4.** `$(...)` is command substitution.

```bash
today=$(date +%F)
echo "$today"
```

**5.** `${1:-default}` supplies a fallback.

```bash
name=${1:-world}
echo "Hello, $name"
```

**6.**

```bash
#!/bin/bash
if [ $# -eq 0 ]; then
  echo "usage: $0 <file>"; exit 1
fi
```

**7.**

```bash
#!/bin/bash
if [ -r "$1" ]; then
  echo readable
else
  echo "not readable"
fi
```

**8.** `[[ ]]` is the bash form; use `&&` instead of `-a`.

```bash
if [[ -f /etc/passwd && -r /etc/passwd ]]; then
  echo ok
fi
```

**9.** `||` runs the right side only if the test fails.

```bash
[ -d "$1" ] || mkdir -p "$1"
```

**10.**

```bash
for (( i=1; i<=10; i++ )); do
  echo $i
done
```

**11.** A descending brace range (or `seq 10 -1 1`).

```bash
for i in {10..1}; do echo $i; done
```

**12.**

```bash
i=0
while [ $i -lt 5 ]; do
  echo $i
  ((i++))
done
```

**13.** Quote `"$f"` to survive spaces.

```bash
for f in *.log; do
  gzip "$f"
done
```

**14.** `read -r` one line at a time; redirect the file into the loop.

```bash
#!/bin/bash
n=1
while read -r line; do
  echo "$n: $line"
  ((n++))
done < "$1"
```

**15.**

```bash
case "$1" in
  start)   echo "starting" ;;
  stop)    echo "stopping" ;;
  restart) echo "restarting" ;;
  *)       echo "usage: $0 start|stop|restart" ;;
esac
```

**16.** `return` passes only 0–255; read it with `$?`.

```bash
add(){ return $(( $1 + $2 )); }
add 3 4
echo $?      # 7
```

**17.** The `(( ))` result becomes the function's exit status.

```bash
is_even(){ (( $1 % 2 == 0 )); }
is_even 8 && echo even
```

**18.** Loop over `"$@"` and accumulate.

```bash
s=0
for n in "$@"; do (( s += n )); done
echo "$s"
```

**19.** Quote `"${arr[@]}"` so each element stays intact.

```bash
hosts=(web1 web2 db1)
for h in "${hosts[@]}"; do
  ping -c1 "$h"
done
```

**20.** `${f%.txt}` strips the suffix; `${f^^}` upper-cases.

```bash
f="report.txt"
echo "${f%.txt}"   # report
echo "${f^^}"      # REPORT.TXT
```

**21.** The colon after `o` means it takes a value (in `$OPTARG`).

```bash
while getopts vo: opt; do
  case $opt in
    v) echo "verbose" ;;
    o) echo "output = $OPTARG" ;;
  esac
done
```

**22.** It expands to `A`, but if `A` is unset or empty it prints an error to stderr and aborts the script. Use it to enforce a required variable/argument, e.g. `: ${1:?need a filename}`.

**23.** `trap` on `INT` runs the handler instead of terminating.

```bash
#!/bin/bash
trap 'echo Interrupted' INT
while true; do
  sleep 1
done
```

**24.** Always quote `"$@"` and the loop variable.

```bash
for f in "$@"; do
  echo "[$f]"
done
```

**25.** `mkfifo` makes the named pipe; the reader blocks on `cat` until another shell writes.

```bash
mkfifo myfifo
while true; do cat myfifo; done   # reader
# another shell:
echo hello > myfifo
```
