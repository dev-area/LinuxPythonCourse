# תרגילי `sed` — עם פתרונות

כל התרגילים עובדים על קובץ הקלט `file.txt` מהמדריך:

```text
The cat sat on the mat
A cat and a dog played
TODO: fix the config
config: logging is off
config: cache is off

error: disk full
warning: low memory
DEBUG: starting module
David Cohen
```

נסה לפתור בעצמך לפני שאתה פותח את הפתרון. הפתרונות מוסתרים ב-`<details>` — לחץ עליהם כדי לחשוף.

---

## רמה בסיסית

### תרגיל 1
החלף כל `cat` ב-`dog` בכל הקובץ.

<details>
<summary>פתרון</summary>

```bash
sed 's/cat/dog/g' file.txt
```

</details>

---

### תרגיל 2
מחק את כל השורות הריקות.

<details>
<summary>פתרון</summary>

```bash
sed '/^$/d' file.txt
```

</details>

---

### תרגיל 3
הדפס רק את השורה השלישית בקובץ.

<details>
<summary>פתרון</summary>

```bash
sed -n '3p' file.txt
# TODO: fix the config
```

</details>

---

### תרגיל 4
מחק כל שורה שמכילה את המילה `config`.

<details>
<summary>פתרון</summary>

```bash
sed '/config/d' file.txt
```

</details>

---

### תרגיל 5
הדפס את שלוש השורות הראשונות בלבד.

<details>
<summary>פתרון</summary>

```bash
sed -n '1,3p' file.txt
```

או אפשר לעצור אחרי שורה 3:

```bash
sed '3q' file.txt
```

</details>

---

## רמה בינונית

### תרגיל 6
בשורות שמכילות `config` בלבד — החלף את `off` ב-`on`.

<details>
<summary>פתרון</summary>

```bash
sed '/config/ s/off/on/g' file.txt
```

</details>

---

### תרגיל 7
הוסף את הקידומת `>> ` בתחילת כל שורה שמתחילה ב-`error` או `warning`.

<details>
<summary>פתרון</summary>

```bash
sed -E 's/^(error|warning)/>> \1/' file.txt
```

</details>

---

### תרגיל 8
הפוך את המילה `DEBUG` לאותיות קטנות (`debug`).

<details>
<summary>פתרון</summary>

```bash
sed 's/DEBUG/debug/' file.txt
```

או באופן כללי עם GNU sed:

```bash
sed 's/DEBUG/\L&/' file.txt
```

</details>

---

### תרגיל 9
הפוך את הסדר של `David Cohen` ל-`Cohen David`.

<details>
<summary>פתרון</summary>

```bash
sed 's/\(David\) \(Cohen\)/\2 \1/' file.txt
```

או באופן כללי לכל שתי מילים:

```bash
sed -E 's/(\w+) (\w+)/\2 \1/' file.txt
```

</details>

---

### תרגיל 10
הדפס רק את השורות שבין `TODO` ל-`error` (כולל).

<details>
<summary>פתרון</summary>

```bash
sed -n '/TODO/,/error/p' file.txt
```

</details>

---

## רמה מתקדמת

### תרגיל 11
מספר את כל השורות (הוסף מספר שורה בתחילת כל שורה, מופרד בטאב).

<details>
<summary>פתרון</summary>

```bash
sed '=' file.txt | sed 'N;s/\n/\t/'
```

</details>

---

### תרגיל 12
מחק את השורה הראשונה ואת השורה האחרונה.

<details>
<summary>פתרון</summary>

```bash
sed '1d;$d' file.txt
```

</details>

---

### תרגיל 13
הוסף את השורה `--- END ---` בסוף הקובץ.

<details>
<summary>פתרון</summary>

```bash
sed '$a --- END ---' file.txt
```

</details>

---

### תרגיל 14
החלף את כל הרצפים של רווחים מרובים ברווח יחיד.

<details>
<summary>פתרון</summary>

```bash
sed 's/  */ /g' file.txt
```

</details>

---

### תרגיל 15
אחד את כל השורות לשורה אחת, מופרדת בפסיקים.

<details>
<summary>פתרון</summary>

```bash
sed ':a;N;$!ba;s/\n/, /g' file.txt
```

</details>

---

## אתגר — סקריפט מלא

### תרגיל 16
כתוב סקריפט `sed` (קובץ `.sed`) שעושה את כל הפעולות הבאות על `file.txt`:
1. מוחק שורות ריקות.
2. מסמן כל `error` כ-`ERROR`.
3. מוסיף את השורה `=== REPORT ===` בתחילת הקובץ.

<details>
<summary>פתרון</summary>

צור קובץ בשם `challenge.sed`:

```sed
# challenge.sed
1i === REPORT ===
/^$/d
s/error/ERROR/g
```

והרץ:

```bash
sed -f challenge.sed file.txt
```

> שים לב: הפקודה `1i` מוסיפה לפני השורה הראשונה **המקורית**. גם אם שורה 1 אינה ריקה, הטקסט ייכנס לראש הפלט.

</details>

---

## טיפ לבדיקה עצמית

כדי לראות אם הפתרון שלך נכון — הרץ את הפקודה והשווה לפלט הצפוי. אם אתה רוצה לשמור את התוצאה בקובץ חדש בלי לשנות את המקור:

```bash
sed 's/cat/dog/g' file.txt > output.txt
```

ורק כשאתה בטוח — הוסף `-i` כדי לערוך את הקובץ עצמו.
