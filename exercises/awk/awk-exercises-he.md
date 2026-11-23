# תרגילי `awk` — עם פתרונות

כל התרגילים עובדים על קובץ הקלט `employees.txt` מהמדריך:

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

שדות: `$1`=שם, `$2`=מחלקה, `$3`=משכורת, `$4`=גיל. שורה 1 היא כותרת (מדלגים עליה עם `NR > 1`).

נסה לפתור בעצמך לפני שאתה פותח את הפתרון — הפתרונות מוסתרים ב-`<details>`.

---

## רמה בסיסית

### תרגיל 1
הדפס רק את עמודת השמות (`$1`).

<details>
<summary>פתרון</summary>

```bash
awk '{ print $1 }' employees.txt
```

</details>

---

### תרגיל 2
הדפס את השם והמשכורת (העמודה הראשונה והשלישית) של כל עובד, בלי שורת הכותרת.

<details>
<summary>פתרון</summary>

```bash
awk 'NR > 1 { print $1, $3 }' employees.txt
# Alice 9500
# Bob 7200
# ...
```

</details>

---

### תרגיל 3
הדפס רק את שורות העובדים ממחלקת `eng`.

<details>
<summary>פתרון</summary>

```bash
awk '$2 == "eng"' employees.txt
```

</details>

---

### תרגיל 4
כמה עובדים יש בקובץ (בלי לספור את הכותרת)?

<details>
<summary>פתרון</summary>

```bash
awk 'END { print NR - 1 }' employees.txt
# 7
```

</details>

---

### תרגיל 5
הדפס את העמודה האחרונה בכל שורה (בלי לדעת מראש כמה עמודות יש).

<details>
<summary>פתרון</summary>

```bash
awk '{ print $NF }' employees.txt
```

</details>

---

## רמה בינונית

### תרגיל 6
הדפס את שמות העובדים שמשכורתם גבוהה מ-8000.

<details>
<summary>פתרון</summary>

```bash
awk 'NR > 1 && $3 > 8000 { print $1 }' employees.txt
# Alice
# Carol
# Frank
```

</details>

---

### תרגיל 7
חשב את סך כל המשכורות.

<details>
<summary>פתרון</summary>

```bash
awk 'NR > 1 { sum += $3 } END { print sum }' employees.txt
# 56700
```

</details>

---

### תרגיל 8
חשב את המשכורת הממוצעת, עם ספרה עשרונית אחת.

<details>
<summary>פתרון</summary>

```bash
awk 'NR > 1 { s += $3; c++ } END { printf "%.1f\n", s/c }' employees.txt
# 8100.0
```

</details>

---

### תרגיל 9
הדפס את עמודת המחלקה באותיות גדולות.

<details>
<summary>פתרון</summary>

```bash
awk 'NR > 1 { print toupper($2) }' employees.txt
```

</details>

---

### תרגיל 10
הדפס טבלה מיושרת: שם ברוחב 8 (לשמאל) ומשכורת ברוחב 6 (לימין).

<details>
<summary>פתרון</summary>

```bash
awk 'NR > 1 { printf "%-8s %6d\n", $1, $3 }' employees.txt
# Alice      9500
# Bob        7200
# ...
```

</details>

---

## רמה מתקדמת

### תרגיל 11
ספור כמה עובדים יש בכל מחלקה.

<details>
<summary>פתרון</summary>

```bash
awk 'NR > 1 { c[$2]++ } END { for (d in c) print d, c[d] }' employees.txt
# eng 3
# hr 2
# sales 2
```

> הסדר עשוי להשתנות בין הרצות. לסדר קבוע: הוסף `| sort`.

</details>

---

### תרגיל 12
חשב את סך המשכורות לכל מחלקה.

<details>
<summary>פתרון</summary>

```bash
awk 'NR > 1 { t[$2] += $3 } END { for (d in t) print d, t[d] }' employees.txt
# eng 30300
# hr 13100
# sales 13300
```

</details>

---

### תרגיל 13
מצא מי מרוויח הכי הרבה ומהי המשכורת.

<details>
<summary>פתרון</summary>

```bash
awk 'NR > 1 && $3 > max { max = $3; who = $1 } END { print who, max }' employees.txt
# Frank 12000
```

</details>

---

### תרגיל 14
הדפס רק את העובד הראשון מכל מחלקה (dedup לפי מחלקה).

<details>
<summary>פתרון</summary>

```bash
awk 'NR > 1 && !seen[$2]++ { print $1, $2 }' employees.txt
# Alice eng
# Bob sales
# Eve hr
```

</details>

---

### תרגיל 15
הדפס לכל עובד את שמו ובונוס של 10% מהמשכורת (כמספר שלם).

<details>
<summary>פתרון</summary>

```bash
awk 'NR > 1 { printf "%-8s %d\n", $1, $3 * 0.1 }' employees.txt
# Alice    950
# Bob      720
# ...
```

</details>

---

## אתגר — סקריפט מלא

### תרגיל 16
כתוב סקריפט `awk` (קובץ `.awk`) שמדפיס לכל מחלקה את **מספר העובדים** ואת **המשכורת הממוצעת**, עם כותרת מיושרת.

<details>
<summary>פתרון</summary>

צור קובץ בשם `avg.awk`:

```awk
# avg.awk — average salary per department
NR > 1 {
    sum[$2] += $3
    count[$2]++
}
END {
    printf "%-8s %5s %10s\n", "DEPT", "N", "AVG"
    for (d in sum)
        printf "%-8s %5d %10.1f\n", d, count[d], sum[d] / count[d]
}
```

והרץ:

```bash
awk -f avg.awk employees.txt
# DEPT         N        AVG
# eng          3    10100.0
# hr           2     6550.0
# sales        2     6650.0
```

</details>

---

## טיפ לבדיקה עצמית

הרץ את הפקודה והשווה לפלט הצפוי. `awk` לא משנה את הקובץ המקורי — כדי לשמור תוצאה, הפנה לקובץ חדש:

```bash
awk 'NR > 1 { print $1, $3 }' employees.txt > output.txt
```
