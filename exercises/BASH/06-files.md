# דף 6 – עבודה עם קבצים

➡️ חזרה ל[דף 5](05-loops.md)

בדף האחרון נלמד כיצד ליצור, לקרוא, לכתוב ולעבד קבצים – הלב של הרבה סקריפטים.

## יצירה וכתיבה לקבצים

| פעולה | פקודה |
|-------|-------|
| כתיבה (**דורס** תוכן קיים) | `echo "text" > file.txt` |
| הוספה (**מוסיף** לסוף) | `echo "text" >> file.txt` |
| יצירת קובץ ריק | `touch file.txt` |

```bash
#!/bin/bash

# Overwrite - start a new file
echo "First line" > diary.txt

# Append - add more lines
echo "Second line" >> diary.txt
echo "Third line" >> diary.txt
```

> שימו לב להבדל: `>` **מוחק** מה שהיה בקובץ, `>>` **מוסיף** בסוף.

### כתיבת מספר שורות בבת אחת – Here Document

```bash
#!/bin/bash

cat > config.txt << EOF
Name: Dana
City: Haifa
Role: Developer
EOF
```

- כל מה שבין `<< EOF` ל‑`EOF` נכתב לקובץ.

---

## קריאת קבצים

| פקודה | מה היא עושה |
|-------|-------------|
| `cat file.txt` | מדפיס את כל הקובץ |
| `head -n 5 file.txt` | 5 השורות הראשונות |
| `tail -n 5 file.txt` | 5 השורות האחרונות |
| `wc -l file.txt` | מספר השורות בקובץ |
| `grep "word" file.txt` | שורות שמכילות את המילה |

```bash
#!/bin/bash

echo "--- The whole file ---"
cat diary.txt

echo "--- First 2 lines ---"
head -n 2 diary.txt

echo "--- Number of lines ---"
wc -l < diary.txt
```

### קריאה שורה‑שורה בסקריפט

```bash
#!/bin/bash

line_num=1
while read -r line; do
    echo "$line_num: $line"
    line_num=$(( line_num + 1 ))
done < diary.txt
```

---

## בדיקה לפני פעולה

תמיד כדאי לבדוק שקובץ קיים לפני שעובדים איתו (ראו דף 4):

```bash
#!/bin/bash
file="data.txt"

if [ ! -f "$file" ]; then
    echo "Error: the file $file does not exist"
    exit 1
fi

echo "Processing $file..."
```

---

## פעולות נפוצות נוספות

```bash
cp source.txt backup.txt      # copy
mv old.txt new.txt            # move / rename
rm file.txt                   # delete
mkdir mydir                   # create a directory
ls -l                         # detailed file listing
```

### עיבוד תוכן עם צינורות (pipes)

ה‑`|` מעביר את הפלט של פקודה אחת כקלט לפקודה הבאה:

```bash
#!/bin/bash

# How many lines contain the word "error" in the log?
grep "error" app.log | wc -l

# Sort a names file and remove duplicates
sort names.txt | uniq
```

---

## תרגיל

כתבו סקריפט `line_counter.sh` ש:

1. מקבל שם קובץ כארגומנט (`$1`).
2. בודק שהקובץ קיים – אחרת מדפיס שגיאה ויוצא.
3. יוצר קובץ פלט חדש בשם `<שם הקובץ>.numbered` שבו כל שורה מהמקור
   מופיעה עם מספר השורה לפניה.
4. בסוף מדפיס כמה שורות עובדו.

דוגמה: אם `fruits.txt` מכיל:

```
apple
banana
cherry
```

אז אחרי `./line_counter.sh fruits.txt`, הקובץ `fruits.txt.numbered` יכיל:

```
1: apple
2: banana
3: cherry
```

ולמסך יודפס: `Processed 3 lines`.

נסו לבד! 👇

---

## פתרון

```bash
#!/bin/bash

input="$1"

# Check the argument
if [ -z "$input" ]; then
    echo "Usage: $0 <file name>"
    exit 1
fi

# Check the file exists
if [ ! -f "$input" ]; then
    echo "Error: the file $input does not exist"
    exit 1
fi

output="${input}.numbered"

# Start an empty output file
> "$output"

count=0
while read -r line; do
    count=$(( count + 1 ))
    echo "$count: $line" >> "$output"
done < "$input"

echo "Processed $count lines"
echo "Output saved to: $output"
```

הרצה ובדיקה:

```bash
chmod +x line_counter.sh
printf "apple\nbanana\ncherry\n" > fruits.txt
./line_counter.sh fruits.txt
cat fruits.txt.numbered
```

> טיפ: בעצם אפשר להשיג את אותו דבר בפקודה אחת: `cat -n fruits.txt`
> או `nl fruits.txt`. אבל עשינו זאת "ידנית" כדי לתרגל קריאת קובץ בלולאה.

**מה למדנו:** בדיקת קיום קובץ, קריאה שורה‑שורה עם `while read`, כתיבה והוספה לקובץ פלט,
וצבירת מונה.

---

## 🎉 סיימתם את המדריך!

עברתם על:
1. הסקריפט הראשון ופונקציות
2. משתנים, ארגומנטים ו‑`set --`
3. סיגנלים ו‑`trap`
4. תנאים מכל הסוגים
5. לולאות
6. עבודה עם קבצים

**מה הלאה?** עברו ל[דף 7 – פרויקטים אמיתיים](07-real-world-projects.md) ותרגלו סקריפטים
שימושיים באמת: גיבוי, ניתוח לוגים, ניהול מטלות, ניטור ועוד.

➡️ המשך ל[דף 7 – פרויקטים אמיתיים](07-real-world-projects.md)
➡️ חזרה ל[תוכן העניינים](README.md)
