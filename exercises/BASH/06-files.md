# דף 6 – עבודה עם קבצים

➡️ חזרה ל[דף 5](05-loops.md)

בדף האחרון נלמד כיצד ליצור, לקרוא, לכתוב ולעבד קבצים – הלב של הרבה סקריפטים.

## יצירה וכתיבה לקבצים

| פעולה | פקודה |
|-------|-------|
| כתיבה (**דורס** תוכן קיים) | `echo "טקסט" > file.txt` |
| הוספה (**מוסיף** לסוף) | `echo "טקסט" >> file.txt` |
| יצירת קובץ ריק | `touch file.txt` |

```bash
#!/bin/bash

# דריסה – מתחילים קובץ חדש
echo "שורה ראשונה" > diary.txt

# הוספה – מוסיפים שורות
echo "שורה שנייה" >> diary.txt
echo "שורה שלישית" >> diary.txt
```

> שימו לב להבדל: `>` **מוחק** מה שהיה בקובץ, `>>` **מוסיף** בסוף.

### כתיבת מספר שורות בבת אחת – Here Document

```bash
#!/bin/bash

cat > config.txt << EOF
שם: דנה
עיר: חיפה
תפקיד: מפתחת
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
| `grep "מילה" file.txt` | שורות שמכילות את המילה |

```bash
#!/bin/bash

echo "--- כל הקובץ ---"
cat diary.txt

echo "--- 2 שורות ראשונות ---"
head -n 2 diary.txt

echo "--- מספר שורות ---"
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
    echo "שגיאה: הקובץ $file לא קיים"
    exit 1
fi

echo "מעבד את $file..."
```

---

## פעולות נפוצות נוספות

```bash
cp source.txt backup.txt      # העתקה
mv old.txt new.txt            # העברה / שינוי שם
rm file.txt                   # מחיקה
mkdir mydir                   # יצירת תיקייה
ls -l                         # רשימת קבצים מפורטת
```

### עיבוד תוכן עם צינורות (pipes)

ה‑`|` מעביר את הפלט של פקודה אחת כקלט לפקודה הבאה:

```bash
#!/bin/bash

# כמה שורות מכילות את המילה "error" בלוג?
grep "error" app.log | wc -l

# ממיין קובץ שמות, מסיר כפילויות
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

ולמסך יודפס: `עובדו 3 שורות`.

נסו לבד! 👇

---

## פתרון

```bash
#!/bin/bash

input="$1"

# בדיקת ארגומנט
if [ -z "$input" ]; then
    echo "שימוש: $0 <שם קובץ>"
    exit 1
fi

# בדיקת קיום הקובץ
if [ ! -f "$input" ]; then
    echo "שגיאה: הקובץ $input לא קיים"
    exit 1
fi

output="${input}.numbered"

# מתחילים קובץ פלט ריק
> "$output"

count=0
while read -r line; do
    count=$(( count + 1 ))
    echo "$count: $line" >> "$output"
done < "$input"

echo "עובדו $count שורות"
echo "הפלט נשמר ב: $output"
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

**מה הלאה?** נסו לשלב את כל מה שלמדתם בפרויקט אמיתי – למשל סקריפט גיבוי,
מעבד לוגים, או כלי קטן לניהול רשימת מטלות.

➡️ חזרה ל[תוכן העניינים](README.md)
