# דף 7 – פרויקטים אמיתיים (תרגילים מתקדמים)

➡️ חזרה ל[דף 6](06-files.md)

הגיע הזמן לשלב הכול! הדף הזה מכיל **סקריפטים אמיתיים** – כאלה שבאמת שימושיים ביומיום.
כל תרגיל משלב כמה נושאים שלמדנו: משתנים, ארגומנטים, תנאים, לולאות, פונקציות, trap וקבצים.

> המלצה: כתבו כל סקריפט בעצמכם מההתחלה, הריצו, ותקנו שגיאות. רק אחר כך הציצו בפתרון.

---

## פרויקט 1 – סקריפט גיבוי (Backup)

### המשימה

כתבו סקריפט `backup.sh` ש:

1. מקבל נתיב לתיקייה כארגומנט (`$1`).
2. בודק שהתיקייה קיימת – אחרת מדפיס שגיאה ויוצא.
3. יוצר קובץ ארכיון דחוס (`.tar.gz`) עם **חותמת זמן** בשם, למשל `backup_2026-11-21_14-30-05.tar.gz`.
4. שומר אותו בתיקיית `~/backups` (יוצר אותה אם היא לא קיימת).
5. מדפיס הודעת הצלחה עם גודל הקובץ.

נסו לבד! 👇

### פתרון

```bash
#!/bin/bash

source_dir="$1"

# 1-2. Validate input
if [ -z "$source_dir" ]; then
    echo "Usage: $0 <directory-to-backup>"
    exit 1
fi

if [ ! -d "$source_dir" ]; then
    echo "Error: '$source_dir' is not a directory"
    exit 1
fi

# 4. Make sure the backups folder exists
backup_dir="$HOME/backups"
mkdir -p "$backup_dir"

# 3. Build a timestamped archive name
timestamp=$(date +%Y-%m-%d_%H-%M-%S)
archive="$backup_dir/backup_${timestamp}.tar.gz"

# Create the compressed archive
tar -czf "$archive" "$source_dir"

# 5. Report success with the file size
if [ -f "$archive" ]; then
    size=$(du -h "$archive" | cut -f1)
    echo "Backup created: $archive ($size)"
else
    echo "Backup failed"
    exit 1
fi
```

**מה חדש כאן:** `mkdir -p`, `date` לחותמת זמן, `tar -czf` לדחיסה, `du -h` ו‑`cut` לקבלת גודל.

---

## פרויקט 2 – ניתוח קובץ לוג (Log Analyzer)

### המשימה

כתבו סקריפט `log_stats.sh` ש:

1. מקבל קובץ לוג כארגומנט.
2. סופר כמה שורות מכילות `ERROR`, כמה `WARNING`, וכמה `INFO`.
3. מדפיס את 3 ההודעות האחרונות מסוג `ERROR`.
4. מדפיס סיכום מסודר.

כדי לבדוק, צרו קובץ לוג לדוגמה:

```bash
cat > app.log << EOF
2026-11-21 10:00 INFO Server started
2026-11-21 10:05 WARNING High memory usage
2026-11-21 10:06 ERROR Database connection failed
2026-11-21 10:07 INFO Retrying
2026-11-21 10:08 ERROR Timeout on query
EOF
```

נסו לבד! 👇

### פתרון

```bash
#!/bin/bash

logfile="$1"

if [ ! -f "$logfile" ]; then
    echo "Error: log file not found"
    exit 1
fi

# 2. Count each level
errors=$(grep -c "ERROR" "$logfile")
warnings=$(grep -c "WARNING" "$logfile")
infos=$(grep -c "INFO" "$logfile")

# 4. Summary
echo "===== Log summary for $logfile ====="
echo "ERRORS:   $errors"
echo "WARNINGS: $warnings"
echo "INFO:     $infos"
echo ""

# 3. Last 3 error messages
echo "----- Last 3 errors -----"
grep "ERROR" "$logfile" | tail -n 3
```

**מה חדש כאן:** `grep -c` לספירת התאמות, שרשור צינורות (`grep ... | tail`), בניית דוח קריא.

---

## פרויקט 3 – שינוי שם קבצים בכמות (Batch Rename)

### המשימה

כתבו סקריפט `add_prefix.sh` ש:

1. מקבל שני ארגומנטים: תחילית (prefix) וסיומת קבצים (למשל `jpg`).
2. עובר על כל הקבצים עם הסיומת הזו בתיקייה הנוכחית.
3. מוסיף את התחילית לשם של כל קובץ (למשל `photo.jpg` → `vacation_photo.jpg`).
4. מדפיס כל פעולת שינוי, ובסוף כמה קבצים שונו.

נסו לבד! 👇

### פתרון

```bash
#!/bin/bash

prefix="$1"
extension="$2"

# Validate both arguments were given
if [ -z "$prefix" ] || [ -z "$extension" ]; then
    echo "Usage: $0 <prefix> <extension>"
    echo "Example: $0 vacation_ jpg"
    exit 1
fi

count=0

for file in *."$extension"; do
    # If no files match, the pattern stays literal - skip it
    if [ ! -f "$file" ]; then
        echo "No .$extension files found"
        break
    fi

    newname="${prefix}${file}"
    mv "$file" "$newname"
    echo "Renamed: $file -> $newname"
    count=$(( count + 1 ))
done

echo "Done. Renamed $count file(s)."
```

**מה חדש כאן:** עבודה עם תבניות (`*.jpg`), בניית שם חדש בעזרת `${prefix}${file}`, ו‑`mv` בלולאה.

---

## פרויקט 4 – מנהל רשימת מטלות (TODO Manager)

### המשימה

כתבו סקריפט `todo.sh` – כלי קטן לניהול מטלות ששומר אותן בקובץ `todo.txt`.
הסקריפט מקבל פקודה כארגומנט ראשון:

- `./todo.sh add "Buy milk"` – מוסיף מטלה.
- `./todo.sh list` – מציג את כל המטלות ממוספרות.
- `./todo.sh done 2` – מוחק את המטלה מספר 2.

השתמשו ב‑`case` כדי לבחור את הפעולה.

נסו לבד! 👇

### פתרון

```bash
#!/bin/bash

TODO_FILE="todo.txt"
touch "$TODO_FILE"   # make sure it exists

command="$1"

case "$command" in
    add)
        task="$2"
        if [ -z "$task" ]; then
            echo "Usage: $0 add \"task text\""
            exit 1
        fi
        echo "$task" >> "$TODO_FILE"
        echo "Added: $task"
        ;;

    list)
        if [ ! -s "$TODO_FILE" ]; then
            echo "No tasks yet. Add one with: $0 add \"...\""
            exit 0
        fi
        echo "===== TODO =====" 
        num=1
        while read -r line; do
            echo "$num. $line"
            num=$(( num + 1 ))
        done < "$TODO_FILE"
        ;;

    done)
        target="$2"
        if [ -z "$target" ]; then
            echo "Usage: $0 done <task-number>"
            exit 1
        fi
        # Keep every line except the chosen one
        tmp=$(mktemp)
        num=1
        while read -r line; do
            if [ "$num" -ne "$target" ]; then
                echo "$line" >> "$tmp"
            fi
            num=$(( num + 1 ))
        done < "$TODO_FILE"
        mv "$tmp" "$TODO_FILE"
        echo "Removed task $target"
        ;;

    *)
        echo "Usage: $0 {add|list|done}"
        exit 1
        ;;
esac
```

הרצה לדוגמה:

```bash
chmod +x todo.sh
./todo.sh add "Buy milk"
./todo.sh add "Call the dentist"
./todo.sh list
./todo.sh done 1
./todo.sh list
```

**מה חדש כאן:** `case` כתפריט פקודות, `mktemp` לקובץ זמני בטוח, ומחיקת שורה על ידי בנייה מחדש של הקובץ.

---

## פרויקט 5 – בדיקת תקינות שירות (Health Check) עם trap

### המשימה

כתבו סקריפט `health_check.sh` ש:

1. מקבל כתובת אתר (URL) כארגומנט.
2. כל 5 שניות בודק אם האתר מגיב (באמצעות `curl`), ומדפיס `UP` או `DOWN` עם חותמת זמן.
3. רושם כל בדיקה לקובץ `health.log`.
4. כשלוחצים `Ctrl+C`, מדפיס סיכום: כמה בדיקות בוצעו, ויוצא בצורה נקייה (`trap`).

נסו לבד! 👇

### פתרון

```bash
#!/bin/bash

url="$1"

if [ -z "$url" ]; then
    echo "Usage: $0 <url>"
    exit 1
fi

logfile="health.log"
checks=0

# On Ctrl+C: print a summary and exit cleanly
trap 'echo ""; echo "Stopped. Performed $checks checks. Log: $logfile"; exit 0' SIGINT

echo "Monitoring $url (press Ctrl+C to stop)..."

while true; do
    checks=$(( checks + 1 ))
    timestamp=$(date +"%Y-%m-%d %H:%M:%S")

    # -s silent, -o discard body, -w print the HTTP status code
    status=$(curl -s -o /dev/null -w "%{http_code}" "$url")

    if [ "$status" = "200" ]; then
        result="UP   (HTTP $status)"
    else
        result="DOWN (HTTP $status)"
    fi

    line="$timestamp  $result"
    echo "$line"
    echo "$line" >> "$logfile"

    sleep 5
done
```

הרצה:

```bash
chmod +x health_check.sh
./health_check.sh https://example.com
```

**מה חדש כאן:** `curl` לבדיקת שירות, לולאה אינסופית עם `sleep`, ו‑`trap SIGINT` ליציאה מסודרת עם סיכום.

---

## פרויקט 6 – מציאת וניקוי קבצים ישנים (Cleanup)

### המשימה

כתבו סקריפט `cleanup.sh` ש:

1. מקבל תיקייה ומספר ימים כארגומנטים: `./cleanup.sh /tmp/logs 7`.
2. מוצא את כל הקבצים בתיקייה שלא שונו ב‑N הימים האחרונים.
3. **לפני שמוחק** – מציג את הרשימה ושואל את המשתמש לאישור (y/n).
4. מוחק רק אם המשתמש אישר, ומדפיס כמה קבצים נמחקו.

> שימו לב: זהו סקריפט "מסוכן" (מוחק קבצים!), ולכן האישור לפני המחיקה הוא חלק מהתרגיל.

נסו לבד! 👇

### פתרון

```bash
#!/bin/bash

dir="$1"
days="$2"

# Validate input
if [ -z "$dir" ] || [ -z "$days" ]; then
    echo "Usage: $0 <directory> <days>"
    exit 1
fi

if [ ! -d "$dir" ]; then
    echo "Error: '$dir' is not a directory"
    exit 1
fi

# Find files older than N days (modified time)
echo "Files in '$dir' not modified in the last $days day(s):"
echo "-----------------------------------------------------"
old_files=$(find "$dir" -type f -mtime +"$days")

if [ -z "$old_files" ]; then
    echo "Nothing to clean up."
    exit 0
fi

echo "$old_files"
echo "-----------------------------------------------------"

# Count them
file_count=$(echo "$old_files" | wc -l)

# Ask for confirmation before deleting
read -p "Delete these $file_count file(s)? (y/n): " answer

if [ "$answer" = "y" ] || [ "$answer" = "Y" ]; then
    echo "$old_files" | while read -r f; do
        rm -f "$f"
        echo "Deleted: $f"
    done
    echo "Cleanup complete. Removed $file_count file(s)."
else
    echo "Cancelled. No files were deleted."
fi
```

**מה חדש כאן:** `find ... -mtime +N` למציאת קבצים ישנים, אישור מהמשתמש עם `read -p` לפני פעולה הרסנית,
ומעבר על רשימת קבצים בלולאה.

---

## 🏆 מעולה!

הפרויקטים האלה מדגימים את מה שסקריפטים של BASH עושים בעולם האמיתי:
גיבויים, ניתוח לוגים, אוטומציה של קבצים, כלי שורת־פקודה, ניטור וניקוי.

**אתגר אחרון:** בחרו אחד מהפרויקטים ושפרו אותו – למשל הוסיפו ל‑`todo.sh` פקודת `clear`,
או ל‑`backup.sh` מחיקה אוטומטית של גיבויים ישנים מלפני 30 יום (שילוב של פרויקט 1 ו‑6).

➡️ חזרה ל[תוכן העניינים](README.md)
