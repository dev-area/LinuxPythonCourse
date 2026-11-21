# דף 2 – משתנים, ארגומנטים ו‑`set --`

➡️ חזרה ל[דף 1](01-intro.md)

## משתנים

**משתנה** הוא שם ששומר ערך. ב‑BASH מגדירים משתנה **בלי רווחים** סביב ה‑`=`:

```bash
name="Dana"
age=25
```

> חשוב: `name = "Dana"` (עם רווחים) **לא יעבוד**! חייב להיות צמוד: `name="Dana"`.

כדי **לקרוא** את ערך המשתנה, מוסיפים `$` לפני השם:

```bash
echo "$name"
echo "The age is $age"
```

דוגמה להעתקה והרצה (קובץ `vars.sh`):

```bash
#!/bin/bash

name="Dana"
age=25

echo "Name: $name"
echo "Age: $age"

# It is recommended to wrap in curly braces when attaching text
echo "Next year she will be ${age} and a bit"
```

### גרשיים – ההבדל החשוב

- **גרשיים כפולים** `"..."` – המשתנים **מוחלפים** בערכם.
- **גרש בודד** `'...'` – הטקסט נשאר **בדיוק כמו שהוא**, בלי החלפה.

```bash
#!/bin/bash
word="BASH"
echo "I am learning $word"   # prints: I am learning BASH
echo 'I am learning $word'   # prints: I am learning $word
```

### קליטת פלט של פקודה למשתנה

```bash
#!/bin/bash
today=$(date +%Y-%m-%d)
files_count=$(ls | wc -l)

echo "Today's date: $today"
echo "Number of files in the folder: $files_count"
```

- `$(command)` מריץ את הפקודה ושם את הפלט שלה במשתנה.

---

## ארגומנטים לסקריפט

ארגומנטים הם ערכים שמעבירים לסקריפט **בזמן ההרצה**:

```bash
./myscript.sh apple banana cherry
```

בתוך הסקריפט ניגשים אליהם כך:

| משתנה | משמעות |
|-------|--------|
| `$0` | שם הסקריפט עצמו |
| `$1`, `$2`, `$3` ... | הארגומנט הראשון, השני, השלישי... |
| `$#` | מספר הארגומנטים |
| `$@` | כל הארגומנטים (כרשימה) |
| `$*` | כל הארגומנטים (כמחרוזת אחת) |

דוגמה (קובץ `args.sh`):

```bash
#!/bin/bash

echo "Script name: $0"
echo "First argument: $1"
echo "Second argument: $2"
echo "Number of arguments: $#"
echo "All arguments: $@"
```

הרצה:

```bash
chmod +x args.sh
./args.sh apple banana
```

פלט צפוי:

```
Script name: ./args.sh
First argument: apple
Second argument: banana
Number of arguments: 2
All arguments: apple banana
```

### מעבר על כל הארגומנטים

```bash
#!/bin/bash
echo "I received $# items:"
for item in "$@"; do
    echo " - $item"
done
```

---

## הפקודה `set --`

הפקודה `set --` מאפשרת **לקבוע מחדש** את הארגומנטים (`$1`, `$2`, ...) מתוך הסקריפט,
גם אם הסקריפט לא קיבל אותם מבחוץ. זה שימושי מאוד כשרוצים לפרק מחרוזת לחלקים.

דוגמה בסיסית (קובץ `set_demo.sh`):

```bash
#!/bin/bash

# Set the arguments manually
set -- red green blue

echo "Now \$1 is: $1"
echo "Now \$2 is: $2"
echo "Number of items: $#"
```

פלט:

```
Now $1 is: red
Now $2 is: green
Number of items: 3
```

### שימוש אמיתי – פירוק מחרוזת

נניח שיש לנו תאריך כמחרוזת ואנחנו רוצים לפרק אותו לחלקים:

```bash
#!/bin/bash

date_str="2026-11-21"

# Split the string into arguments using "-" as the separator
IFS='-' set -- $date_str

echo "Year:  $1"
echo "Month: $2"
echo "Day:   $3"
```

> `IFS` (Internal Field Separator) קובע לפי איזה תו לפצל. כאן בחרנו ב‑`-`.

> שימו לב ל‑`--`: הוא מסמן ש"כאן נגמרות האפשרויות ומתחילים הערכים",
> וחשוב במיוחד כשהערך הראשון עלול להתחיל ב‑`-`.

---

## תרגיל

כתבו סקריפט `fullname.sh` ש:

1. מקבל שם מלא כארגומנט אחד במרכאות, לדוגמה: `./fullname.sh "Israel Israeli"`.
2. משתמש ב‑`set --` כדי לפצל את השם הפרטי ושם המשפחה.
3. מדפיס:
   - שם פרטי
   - שם משפחה
   - מספר המילים בשם

דוגמה להרצה ולפלט:

```
./fullname.sh "Israel Israeli"
First name: Israel
Last name: Israeli
Word count: 2
```

נסו לבד! 👇

---

## פתרון

```bash
#!/bin/bash

# The full argument arrives in $1 (because it is wrapped in quotes)
full_name="$1"

# Split by spaces: set -- scatters the string into separate words
set -- $full_name

echo "First name: $1"
echo "Last name: $2"
echo "Word count: $#"
```

הרצה:

```bash
chmod +x fullname.sh
./fullname.sh "Israel Israeli"
```

**מה למדנו:** `set --` הופך מחרוזת אחת לרשימת ארגומנטים ניתנת לגישה דרך `$1`, `$2`, `$#`.

---

➡️ המשך ל[דף 3 – סיגנלים](03-signals.md)
