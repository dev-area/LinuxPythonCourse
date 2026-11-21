# דף 4 – תנאים (Conditionals)

➡️ חזרה ל[דף 3](03-signals.md)

תנאים מאפשרים לסקריפט "לקבל החלטות" – להריץ קוד מסוים רק אם משהו נכון.

## מבנה בסיסי – `if`

```bash
if [ condition ]; then
    # code that runs if the condition is true
fi
```

> שימו לב לרווחים! חייבים רווח אחרי `[` ולפני `]`. זה טעות נפוצה מאוד.

דוגמה (קובץ `age_check.sh`):

```bash
#!/bin/bash
age=20

if [ "$age" -ge 18 ]; then
    echo "Adult"
fi
```

### `if ... else`

```bash
#!/bin/bash
age=15

if [ "$age" -ge 18 ]; then
    echo "Adult"
else
    echo "Minor"
fi
```

### `if ... elif ... else`

```bash
#!/bin/bash
grade=75

if [ "$grade" -ge 90 ]; then
    echo "Excellent"
elif [ "$grade" -ge 70 ]; then
    echo "Good"
elif [ "$grade" -ge 60 ]; then
    echo "Pass"
else
    echo "Fail"
fi
```

---

## השוואת מספרים

| אופרטור | משמעות | דוגמה |
|---------|--------|-------|
| `-eq` | שווה (equal) | `[ "$a" -eq "$b" ]` |
| `-ne` | לא שווה | `[ "$a" -ne "$b" ]` |
| `-gt` | גדול מ‑ (greater than) | `[ "$a" -gt "$b" ]` |
| `-ge` | גדול או שווה | `[ "$a" -ge "$b" ]` |
| `-lt` | קטן מ‑ (less than) | `[ "$a" -lt "$b" ]` |
| `-le` | קטן או שווה | `[ "$a" -le "$b" ]` |

---

## השוואת מחרוזות

| אופרטור | משמעות |
|---------|--------|
| `=` | שתי מחרוזות זהות |
| `!=` | מחרוזות שונות |
| `-z` | המחרוזת ריקה (zero length) |
| `-n` | המחרוזת לא ריקה |

```bash
#!/bin/bash
name="Dana"

if [ "$name" = "Dana" ]; then
    echo "Hello Dana!"
fi

if [ -z "$password" ]; then
    echo "No password entered"
fi
```

---

## בדיקות על קבצים

| אופרטור | נכון אם... |
|---------|-----------|
| `-e` | הקובץ קיים (exists) |
| `-f` | זהו קובץ רגיל |
| `-d` | זו תיקייה (directory) |
| `-r` | יש הרשאת קריאה |
| `-w` | יש הרשאת כתיבה |
| `-x` | יש הרשאת הרצה |
| `-s` | הקובץ לא ריק (size > 0) |

```bash
#!/bin/bash
file="data.txt"

if [ -f "$file" ]; then
    echo "The file exists"
else
    echo "File not found"
fi
```

---

## תנאים מורכבים – AND, OR, NOT

| מפעיל | משמעות |
|-------|--------|
| `&&` | וגם (AND) |
| `\|\|` | או (OR) |
| `!` | שלילה (NOT) |

```bash
#!/bin/bash
age=25
has_license="yes"

if [ "$age" -ge 18 ] && [ "$has_license" = "yes" ]; then
    echo "Allowed to drive"
fi

if [ "$age" -lt 16 ] || [ "$age" -gt 120 ]; then
    echo "Unreasonable age for driving"
fi
```

> אפשר גם להשתמש בסוגריים כפולים `[[ ... ]]`, שהם גמישים יותר ב‑BASH
> ומאפשרים לכתוב `&&` ו‑`||` בתוך אותם סוגריים:
> ```bash
> if [[ "$age" -ge 18 && "$has_license" = "yes" ]]; then
>     echo "Allowed to drive"
> fi
> ```

---

## מבנה `case` – בחירה מרובת אפשרויות

כש‑`elif` רבים הופכים את הקוד למסורבל, `case` נקי יותר:

```bash
#!/bin/bash
read -p "Choose an option (a/b/c): " choice

case "$choice" in
    a)
        echo "You chose A"
        ;;
    b)
        echo "You chose B"
        ;;
    c)
        echo "You chose C"
        ;;
    *)
        echo "Invalid choice"
        ;;
esac
```

- כל אפשרות מסתיימת ב‑`;;`.
- `*)` הוא "כל השאר" (ברירת מחדל).
- `read -p` מקבל קלט מהמשתמש.

---

## תרגיל

כתבו סקריפט `filecheck.sh` שמקבל שם קובץ כארגומנט (`$1`) ו:

1. אם לא הועבר ארגומנט כלל – ידפיס "Please provide a file name" ויצא.
2. אם הקובץ לא קיים – ידפיס "File does not exist".
3. אם הקובץ קיים אך ריק – ידפיס "File is empty".
4. אם הקובץ קיים ולא ריק – ידפיס "File exists and contains data".

נסו לבד! 👇

---

## פתרון

```bash
#!/bin/bash

filename="$1"

# 1. Check an argument was passed (empty string?)
if [ -z "$filename" ]; then
    echo "Please provide a file name"
    exit 1
fi

# 2-4. Checks on the file
if [ ! -e "$filename" ]; then
    echo "File does not exist"
elif [ ! -s "$filename" ]; then
    echo "File is empty"
else
    echo "File exists and contains data"
fi
```

הרצה ובדיקה:

```bash
chmod +x filecheck.sh
./filecheck.sh                 # no argument
./filecheck.sh nofile.txt      # a file that doesn't exist
touch empty.txt
./filecheck.sh empty.txt       # an empty file
echo "hello" > data.txt
./filecheck.sh data.txt        # a file with content
```

**מה למדנו:** שילוב של בדיקת מחרוזת ריקה (`-z`), קיום קובץ (`-e`), גודל (`-s`) ושלילה (`!`).

---

➡️ המשך ל[דף 5 – לולאות](05-loops.md)
