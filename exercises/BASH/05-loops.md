# דף 5 – לולאות (Loops)

➡️ חזרה ל[דף 4](04-conditionals.md)

לולאה מאפשרת לחזור על אותו קוד כמה פעמים, בלי לכתוב אותו שוב ושוב.

## לולאת `for` – מעבר על רשימה

```bash
#!/bin/bash

for fruit in apple banana cherry; do
    echo "Fruit: $fruit"
done
```

פלט:

```
Fruit: apple
Fruit: banana
Fruit: cherry
```

### לולאת `for` על טווח מספרים

```bash
#!/bin/bash

for i in {1..5}; do
    echo "Number: $i"
done
```

- `{1..5}` יוצר את הרצף 1,2,3,4,5.
- עם קפיצות: `{0..10..2}` → 0,2,4,6,8,10.

### לולאת `for` בסגנון C

```bash
#!/bin/bash

for (( i=1; i<=5; i++ )); do
    echo "Iteration number $i"
done
```

### מעבר על ארגומנטים או קבצים

```bash
#!/bin/bash

# Over all the script's arguments
for arg in "$@"; do
    echo "Received: $arg"
done

# Over all .txt files in the folder
for file in *.txt; do
    echo "Found file: $file"
done
```

---

## לולאת `while` – כל עוד התנאי נכון

```bash
#!/bin/bash

count=1
while [ "$count" -le 5 ]; do
    echo "Counting: $count"
    count=$((count + 1))   # increment by 1
done
```

> `$(( ... ))` מבצע חישוב אריתמטי. בלי ההגדלה של `count`, הלולאה תרוץ לנצח!

### קריאת קובץ שורה‑שורה עם `while`

זהו שימוש נפוץ וחשוב מאוד:

```bash
#!/bin/bash

while read -r line; do
    echo "Line: $line"
done < "names.txt"
```

- `read -r line` קורא שורה אחת לתוך המשתנה `line`.
- `< "names.txt"` מפנה את תוכן הקובץ אל הלולאה.

---

## לולאת `until` – כל עוד התנאי **לא** נכון

`until` היא ההפך מ‑`while`: היא רצה **עד** שהתנאי הופך לנכון.

```bash
#!/bin/bash

count=1
until [ "$count" -gt 5 ]; do
    echo "Value: $count"
    count=$((count + 1))
done
```

---

## שליטה בלולאה – `break` ו‑`continue`

- `break` – יוצא מהלולאה מיד.
- `continue` – מדלג לאיטרציה הבאה.

```bash
#!/bin/bash

for i in {1..10}; do
    if [ "$i" -eq 8 ]; then
        echo "Reached 8, stopping"
        break
    fi

    # Skip even numbers
    if [ $((i % 2)) -eq 0 ]; then
        continue
    fi

    echo "Odd number: $i"
done
```

---

## שילוב פונקציה בלולאה

```bash
#!/bin/bash

square() {
    echo $(( $1 * $1 ))
}

for n in 1 2 3 4 5; do
    result=$(square "$n")
    echo "$n squared = $result"
done
```

---

## תרגיל

כתבו סקריפט `multiplication.sh` ש:

1. מקבל מספר כארגומנט (`$1`).
2. מדפיס את לוח הכפל של אותו מספר, מ‑1 עד 10.
3. בנוסף, מדפיס בסוף רק את **סכום** כל התוצאות.

דוגמת פלט עבור `./multiplication.sh 3`:

```
3 x 1 = 3
3 x 2 = 6
...
3 x 10 = 30
Total: 165
```

נסו לבד! 👇

---

## פתרון

```bash
#!/bin/bash

num="$1"

# Check a number was provided
if [ -z "$num" ]; then
    echo "Please provide a number"
    exit 1
fi

total=0

for i in {1..10}; do
    result=$(( num * i ))
    echo "$num x $i = $result"
    total=$(( total + result ))
done

echo "Total: $total"
```

הרצה:

```bash
chmod +x multiplication.sh
./multiplication.sh 3
```

**מה למדנו:** לולאת `for` על טווח, חישוב אריתמטי עם `$(( ))`, וצבירת סכום במשתנה.

---

➡️ המשך ל[דף 6 – עבודה עם קבצים](06-files.md)
