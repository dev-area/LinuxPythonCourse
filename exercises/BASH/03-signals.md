# דף 3 – סיגנלים (Signals)

➡️ חזרה ל[דף 2](02-variables-arguments.md)

## מה זה סיגנל?

**סיגנל** הוא "הודעה" קצרה שמערכת ההפעלה שולחת לתוכנית שרצה, כדי לבקש ממנה לעשות משהו –
בדרך כלל להיעצר. כשאתם לוחצים `Ctrl+C` בטרמינל כדי לעצור תוכנית – אתם למעשה שולחים סיגנל!

### סיגנלים נפוצים

| שם | מספר | נשלח על ידי | ניתן ללכידה? |
|----|------|-------------|-------------|
| `SIGINT`  | 2  | `Ctrl+C` – הפסקה (Interrupt) | כן |
| `SIGTERM` | 15 | `kill` – בקשת סיום מנומסת | כן |
| `SIGKILL` | 9  | `kill -9` – הרג מיידי | **לא** |
| `SIGHUP`  | 1  | סגירת הטרמינל (Hang Up) | כן |
| `SIGTSTP` | 20 | `Ctrl+Z` – השהיה | כן |

> `SIGKILL` (9) ו‑`SIGSTOP` הם היחידים שאי אפשר ללכוד או להתעלם מהם – הם תמיד "חזקים".

---

## שליחת סיגנל – הפקודה `kill`

למרות השם, `kill` פשוט **שולחת סיגנל** לתהליך לפי מספר התהליך (PID):

```bash
kill 12345          # sends SIGTERM (default) to process 12345
kill -9 12345       # sends SIGKILL
kill -SIGINT 12345  # sends SIGINT
```

כדי למצוא PID של תהליך:

```bash
ps aux | grep myscript
```

---

## לכידת סיגנלים – הפקודה `trap`

הפקודה `trap` מאפשרת לסקריפט **להגיב** לסיגנל במקום פשוט להיעצר.
התחביר:

```bash
trap 'commands' SIGNAL
```

דוגמה להעתקה והרצה (קובץ `trap_demo.sh`):

```bash
#!/bin/bash

# When SIGINT (Ctrl+C) arrives, run this code instead of stopping immediately
trap 'echo ""; echo "Caught Ctrl+C! But I am still here :)"' SIGINT

echo "The script is running. Try pressing Ctrl+C..."
echo "(To really exit, close the terminal or send kill)"

# Infinite loop to keep the script running
count=0
while true; do
    count=$((count + 1))
    echo "Tick... $count"
    sleep 2
done
```

הריצו, ולחצו `Ctrl+C` – תראו שהסקריפט מגיב בהודעה במקום להיסגר.

---

## ניקוי לפני יציאה – הסיגנל המדומה `EXIT`

שימוש נפוץ מאוד ל‑`trap` הוא **ניקיון**: למחוק קבצים זמניים כשהסקריפט נגמר,
לא משנה אם הסתיים כרגיל או נקטע. משתמשים בסיגנל המיוחד `EXIT`:

```bash
#!/bin/bash

tmpfile="/tmp/mydata_$$"   # $$ is the PID of the script (a unique name)

# This code runs on any exit, whether normal or due to a signal
trap 'echo "Cleaning up..."; rm -f "$tmpfile"' EXIT

echo "Temporary data" > "$tmpfile"
echo "Temp file created: $tmpfile"
cat "$tmpfile"

echo "Finishing work."
# Here the trap runs automatically and deletes the file
```

---

## ביטול trap

כדי לבטל לכידה ולחזור להתנהגות הרגילה:

```bash
trap - SIGINT    # restores SIGINT to its default behavior
```

---

## תרגיל

כתבו סקריפט `safe_worker.sh` ש:

1. יוצר קובץ זמני בשם `work.tmp` עם תוכן כלשהו.
2. מגדיר `trap` שימחק את הקובץ הזמני ביציאה (`EXIT`).
3. מגדיר `trap` נוסף: אם המשתמש לוחץ `Ctrl+C` (`SIGINT`), ידפיס
   "Work cancelled by the user" ואז יצא.
4. מדמה עבודה: לולאה שסופרת מ‑1 עד 5 עם `sleep 1` בין מספר למספר, ומדפיסה כל מספר.

נסו ללחוץ `Ctrl+C` באמצע ולראות שהקובץ נמחק בכל זאת.

נסו לבד! 👇

---

## פתרון

```bash
#!/bin/bash

tmpfile="work.tmp"

# Clean up on any exit, normal or forced
trap 'echo "Cleaning up temp file..."; rm -f "$tmpfile"' EXIT

# Respond to Ctrl+C: message and exit (exit also triggers the EXIT trap)
trap 'echo ""; echo "Work cancelled by the user"; exit 1' SIGINT

# Create the temp file
echo "Work data" > "$tmpfile"
echo "Started working (file: $tmpfile)"

# Simulate work
for i in 1 2 3 4 5; do
    echo "Processing step $i..."
    sleep 1
done

echo "Work finished successfully!"
```

הרצה:

```bash
chmod +x safe_worker.sh
./safe_worker.sh
```

**מה למדנו:** `trap` נותן לסקריפט שליטה על מה שקורה כשמגיע סיגנל – במיוחד ניקוי בטוח עם `EXIT`.

---

➡️ המשך ל[דף 4 – תנאים](04-conditionals.md)
