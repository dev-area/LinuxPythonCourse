# מדריך פשוט לפקודת `awk`

`awk` היא שפת עיבוד טקסט שמצטיינת בעבודה על **נתונים בעמודות** (טבלאות, לוגים, CSV). היא קוראת קובץ שורה-שורה, מפצלת כל שורה ל**שדות** (עמודות), ומריצה פעולה על כל שורה שמתאימה לתבנית. היא חזקה במיוחד לחישובים, סיכומים, סינון ועיצוב פלט.

> **ההבדל מ-`sed`:** `sed` מצוינת להחלפות טקסט פשוטות; `awk` מצוינת כשיש עמודות, מספרים וחישובים.

---

## קובץ הקלט לדוגמה (`employees.txt`)

רוב הדוגמאות עובדות על הקובץ הבא. שמור אותו בשם `employees.txt`:

```text
name dept salary age
Alice eng 9500 30
Bob sales 7200 45
Carol eng 8800 29
Dave sales 6100 38
Eve hr 5400 52
Frank eng 12000 41
Grace hr 7700 33
```

לכל שורה יש 4 שדות: `$1`=שם, `$2`=מחלקה, `$3`=משכורת, `$4`=גיל. השורה הראשונה היא כותרת.

אפשר ליצור אותו במהירות כך:

```bash
cat > employees.txt << 'EOF'
name dept salary age
Alice eng 9500 30
Bob sales 7200 45
Carol eng 8800 29
Dave sales 6100 38
Eve hr 5400 52
Frank eng 12000 41
Grace hr 7700 33
EOF
```

---

## מבנה בסיסי

```bash
awk 'pattern { action }' file
```

- **pattern** — תנאי שקובע על אילו שורות לפעול (אופציונלי; ריק = כל השורה).
- **action** — מה לעשות (בתוך `{ }`; ברירת מחדל = `print`).

```bash
# print every line (like cat)
awk '{ print }' employees.txt

# print only lines where the department is eng
awk '$2 == "eng"' employees.txt
```

---

## 1. שדות ועמודות (`$1`, `$2`, ... `$0`)

`awk` מפצל כל שורה אוטומטית לפי רווחים. `$0` = כל השורה, `$1` = העמודה הראשונה וכו'.

```bash
# print the first and third columns
awk '{ print $1, $3 }' employees.txt
# name salary
# Alice 9500
# Bob 7200
# ...
```

> הפסיק בין `$1, $3` מוסיף רווח מפריד. בלי פסיק (`print $1 $3`) הערכים יודבקו יחד.

---

## 2. משתנים מובנים: `NR` ו-`NF`

- `NR` = מספר השורה הנוכחית (Number of Record).
- `NF` = מספר השדות בשורה (Number of Fields).

```bash
# skip the header line (line 1)
awk 'NR > 1 { print $1 }' employees.txt

# print the last column of each line
awk '{ print $NF }' employees.txt

# add a line number at the start of each line
awk '{ print NR, $0 }' employees.txt
```

---

## 3. הדפסה מעוצבת עם `printf`

`printf` נותן שליטה מלאה בעיצוב (רוחב עמודות, מספר ספרות). שים לב — ל-`printf` צריך `\n` מפורש בסוף.

```bash
awk 'NR > 1 { printf "%-8s %-6s %6d\n", $1, $2, $3 }' employees.txt
# Alice    eng      9500
# Bob      sales    7200
# Carol    eng      8800
# ...
```

| תבנית | משמעות |
|-------|---------|
| `%s`   | מחרוזת |
| `%d`   | מספר שלם |
| `%.2f` | מספר עשרוני עם 2 ספרות |
| `%-8s` | מחרוזת מיושרת לשמאל ברוחב 8 |
| `%6d`  | מספר מיושר לימין ברוחב 6 |

---

## 4. תבניות וסינון

```bash
# lines where the salary is greater than 8000
awk 'NR > 1 && $3 > 8000 { print $1, $3 }' employees.txt

# lines where the department is sales
awk '$2 == "sales"' employees.txt

# lines containing the text "eng" (regex over the whole line)
awk '/eng/' employees.txt

# lines where the first column starts with A to C
awk '$1 ~ /^[A-C]/' employees.txt
```

| אופרטור | משמעות |
|---------|---------|
| `==` `!=` | שווה / לא שווה |
| `<` `>` `<=` `>=` | השוואות מספריות |
| `&&` `\|\|` | וגם / או |
| `~` `!~` | מתאים / לא מתאים ל-regex |

---

## 5. בלוקי `BEGIN` ו-`END`

- `BEGIN { }` — רץ **פעם אחת לפני** כל השורות (אתחול, כותרות).
- `END { }` — רץ **פעם אחת אחרי** כל השורות (סיכומים, סה"כ).

```bash
# sum of all salaries
awk 'NR > 1 { sum += $3 } END { print "total:", sum }' employees.txt
# total: 56700

# average salary
awk 'NR > 1 { s += $3; c++ } END { printf "avg: %.1f\n", s/c }' employees.txt
# avg: 8100.0

# our own header + row count
awk 'BEGIN { print "=== Report ===" } END { print "rows:", NR-1 }' employees.txt
```

---

## 6. חישובים ואגרגציה

```bash
# the highest salary
awk 'NR > 1 { if ($3 > max) max = $3 } END { print "max:", max }' employees.txt
# max: 12000

# count employees matching a condition
awk 'NR > 1 && $4 > 40 { c++ } END { print "over 40:", c }' employees.txt
# over 40: 3
```

---

## 7. מערכים — קיבוץ לפי ערך (Group By)

מערכים ב-`awk` ממופתחים לפי מחרוזת — מושלם לסיכום לפי קטגוריה.

```bash
# count employees in each department
awk 'NR > 1 { count[$2]++ } END { for (d in count) print d, count[d] }' employees.txt
# eng 3
# hr 2
# sales 2

# sum of salaries per department
awk 'NR > 1 { total[$2] += $3 } END { for (d in total) print d, total[d] }' employees.txt
# eng 30300
# hr 13100
# sales 13300
```

> **שים לב:** סדר המעבר על `for (d in array)` אינו מובטח — הוא עשוי להשתנות בין הרצות. אם צריך סדר קבוע, מעבירים את הפלט ל-`sort`.

---

## 8. שינוי המפריד: `FS` ו-`OFS`

- `FS` = מפריד הקלט (Field Separator). הדגל `-F` מגדיר אותו.
- `OFS` = מפריד הפלט (Output Field Separator).

```bash
# comma-separated input (CSV)
echo "a,b,c" | awk -F',' '{ print $2 }'
# b

# read separated by : and print separated by TAB
echo "root:x:0:0" | awk -F':' 'BEGIN { OFS="\t" } { print $1, $3 }'
# root	0
```

---

## 9. תנאים ולולאות

```bash
# if / else — tag by salary
awk 'NR > 1 { if ($3 >= 8000) print $1, "high"; else print $1, "normal" }' employees.txt

# for loop — print every field in the line
awk '{ for (i = 1; i <= NF; i++) print i, $i }' employees.txt
```

---

## 10. פונקציות שימושיות

```bash
# length — string length
awk '{ print $1, length($1) }' employees.txt

# toupper / tolower
awk 'NR > 1 { print toupper($2) }' employees.txt

# substr(str, start, len) — slice a string
echo "hello" | awk '{ print substr($0, 1, 3) }'   # hel

# gsub(regex, replacement) — global replace within the line
awk '{ gsub(/eng/, "ENGINEERING"); print }' employees.txt

# split — split a string into an array
echo "a-b-c" | awk '{ n = split($0, parts, "-"); print n, parts[2] }'   # 3 b
```

---

## דוגמאות מתקדמות

### 1. חישוב ביניים בעמודה חדשה

```bash
# add a tax column (10% of the salary)
awk 'NR > 1 { printf "%-8s %d\n", $1, $3 * 0.1 }' employees.txt
```

### 2. סיכום עם כותרת ותחתית

```bash
awk '
  BEGIN { printf "%-8s %8s\n", "NAME", "SALARY" }
  NR > 1 { printf "%-8s %8d\n", $1, $3; sum += $3 }
  END   { printf "%-8s %8d\n", "TOTAL", sum }
' employees.txt
```

### 3. מציאת הערך המקסימלי ומי מחזיק בו

```bash
awk 'NR > 1 && $3 > max { max = $3; who = $1 } END { print who, "earns the most:", max }' employees.txt
# Frank earns the most: 12000
```

### 4. סינון דו-שלבי (uniq לפי שדה)

```bash
# print only the first occurrence of each department
awk '!seen[$2]++' employees.txt
```

---

## סקריפטים של `awk`

כשהתוכנית מתארכת, שומרים אותה בקובץ `.awk` ומריצים עם `-f`.

### 1. קובץ סקריפט (`-f`)

צור קובץ `report.awk`:

```awk
# report.awk — salary report per department
NR > 1 {
    total[$2] += $3
    count[$2]++
}
END {
    printf "%-8s %5s %10s\n", "DEPT", "N", "TOTAL"
    for (d in total)
        printf "%-8s %5d %10d\n", d, count[d], total[d]
}
```

הרצה:

```bash
awk -f report.awk employees.txt
```

### 2. סקריפט עם shebang

צור קובץ `sum.awk`:

```awk
#!/usr/bin/awk -f
# sum the salary column
NR > 1 { sum += $3 }
END    { print "total salary:", sum }
```

```bash
chmod +x sum.awk
./sum.awk employees.txt
```

### 3. העברת משתנה מבחוץ (`-v`)

```bash
# filter by a department passed in at runtime
awk -v d=eng 'NR > 1 && $2 == d { print $1 }' employees.txt
```

---

## טבלת סיכום — משתנים מובנים

| משתנה | משמעות |
|-------|---------|
| `$0`  | כל השורה |
| `$1`..`$n` | שדה (עמודה) לפי מספר |
| `NR`  | מספר השורה הנוכחית |
| `NF`  | מספר השדות בשורה |
| `FS`  | מפריד הקלט (ברירת מחדל: רווח) |
| `OFS` | מפריד הפלט |
| `RS`  | מפריד הרשומות (ברירת מחדל: שורה חדשה) |
| `ORS` | מפריד רשומות בפלט |
| `FILENAME` | שם הקובץ הנוכחי |

---

## טיפים

- כל הדוגמאות עובדות על `employees.txt` — אפשר להעתיק ולהריץ ישירות.
- לדילוג על שורת הכותרת משתמשים ב-`NR > 1`.
- לבדיקה — הרץ והסתכל בפלט; `awk` לא משנה את הקובץ המקורי (אין לו `-i`). כדי לשמור, הפנה לקובץ חדש: `awk '...' employees.txt > out.txt`.
- על Windows הרץ דרך Git Bash או WSL; הדוגמאות נבדקו על GNU Awk (gawk).
