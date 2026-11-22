# דף 8 – פקודות בדיקה ואבחון בלינוקס (Cheat Sheet)

➡️ חזרה ל[תוכן העניינים](README.md)

דף עזר מעשי לבדיקת מצב המערכת ואבחון תקלות. כל פקודה מלווה בהסבר קצר.
אפשר לשלב את הפקודות האלה בסקריפטים (ראו דפים 1–7).

> 💡 טיפ כללי: הוסיפו `man <command>` כדי לקרוא את המדריך המלא של כל פקודה,
> או `<command> --help` לסיכום מהיר.

---

## 1. זיכרון (Memory / RAM)

```bash
free -h                 # כמות זיכרון פנוי/בשימוש (h = קריא לאדם: MB/GB)
free -m                 # אותו דבר במגה-בייט
cat /proc/meminfo       # מידע גולמי ומפורט על הזיכרון
vmstat 1 5              # סטטיסטיקת זיכרון+מעבד, כל שנייה, 5 פעמים
top                     # תצוגה חיה (לחצו Shift+M למיון לפי זיכרון)
ps aux --sort=-%mem | head    # 10 התהליכים שצורכים הכי הרבה זיכרון
```

**מה בודקים:** בעמודה `available` ב‑`free -h` – כמה זיכרון באמת זמין.
אם `swap` בשימוש גבוה – ייתכן שחסר RAM.

---

## 2. מעבד (CPU)

```bash
top                     # עומס חי לפי תהליכים (q ליציאה)
htop                    # גרסה ידידותית יותר (אם מותקנת)
uptime                  # load average ל-1/5/15 הדקות האחרונות
nproc                   # מספר הליבות (cores) במעבד
lscpu                   # פרטי המעבד: דגם, ליבות, מהירות
mpstat 1 5              # ניצול CPU כל שנייה (מחבילת sysstat)
ps aux --sort=-%cpu | head    # 10 התהליכים העמוסים ביותר
```

**מה בודקים:** `load average`. כלל אצבע: אם הוא גבוה ממספר הליבות (`nproc`)
לאורך זמן – המערכת עמוסה.

---

## 3. דיסק ואחסון (Disk)

```bash
df -h                   # שטח פנוי בכל הדיסקים/מחיצות
df -i                   # שימוש ב-inodes (יכול להיגמר גם כשיש מקום!)
du -sh *                # גודל כל קובץ/תיקייה בתיקייה הנוכחית
du -sh /var/log         # גודל תיקייה מסוימת
du -ah / | sort -rh | head -20   # 20 הפריטים הגדולים ביותר במערכת
lsblk                   # רשימת דיסקים ומחיצות (מבנה עץ)
iostat -x 1 5           # עומס קלט/פלט על הדיסקים (מחבילת sysstat)
```

**מה בודקים:** אם `df -h` מראה שימוש של 100% – הדיסק מלא (תקלה נפוצה מאוד!).
בדקו גם `df -i` – לפעמים נגמרים ה‑inodes לפני המקום.

---

## 4. תהליכים (Processes)

```bash
ps aux                  # כל התהליכים במערכת
ps aux | grep nginx     # חיפוש תהליך לפי שם
pgrep -a sshd           # מציאת PID של תהליך לפי שם
top                     # תצוגה חיה
kill <PID>              # שליחת SIGTERM (סיום מנומס)
kill -9 <PID>           # SIGKILL (כפייה - מוצא אחרון)
pkill firefox           # הריגת תהליך לפי שם
jobs                    # משימות רקע ב-shell הנוכחי
```

**מה בודקים:** תהליך "תקוע" (state `D` ב‑`ps` = ממתין ל‑I/O), או תהליך zombie (`Z`).

---

## 5. רשת (Network)

```bash
ip a                    # כתובות IP של כל הממשקים (מחליף ifconfig)
ip route                # טבלת הניתוב (ברירת המחדל / gateway)
ping -c 4 8.8.8.8       # בדיקת קישוריות (4 פינגים)
ping -c 4 google.com    # בדיקת קישוריות + רזולוציית DNS
curl -I https://example.com     # בדיקת תגובת שרת (כותרות בלבד)
ss -tulpn               # פורטים פתוחים ומי מאזין להם (מחליף netstat)
ss -tan                 # כל חיבורי ה-TCP ומצבם
dig google.com          # בדיקת DNS מפורטת
nslookup google.com     # בדיקת DNS פשוטה
traceroute google.com   # מסלול החבילות עד היעד
```

**אבחון תקלת רשת – שלב אחר שלב:**

```bash
ip a                    # 1. יש בכלל כתובת IP?
ping -c 2 <gateway>     # 2. מגיעים לנתב המקומי?
ping -c 2 8.8.8.8       # 3. מגיעים לאינטרנט (לפי IP)?
ping -c 2 google.com    # 4. אם 3 עבד אבל זה לא → בעיית DNS
```

---

## 6. לוגים ושגיאות מערכת (Logs)

```bash
journalctl -xe          # לוגים אחרונים של systemd (שגיאות בסוף)
journalctl -u nginx     # לוגים של שירות מסוים
journalctl -f           # מעקב חי אחר הלוגים (כמו tail -f)
journalctl --since "10 min ago"   # לוגים מהזמן האחרון
dmesg -T | tail -30     # הודעות ה-kernel (תקלות חומרה, OOM וכו')
tail -f /var/log/syslog # מעקב חי אחר לוג המערכת (דביאן/אובונטו)
tail -f /var/log/messages   # (רד-האט/סנטוס)
grep -i error /var/log/syslog   # חיפוש שגיאות בלוג
```

**מה בודקים:** בשגיאות "המערכת איטית" או "תהליך נהרג" – חפשו `Out of memory`
או `oom-killer` ב‑`dmesg`.

---

## 7. שירותים (Services – systemd)

```bash
systemctl status nginx          # מצב שירות (רץ? נכשל?)
systemctl start nginx           # הפעלת שירות
systemctl stop nginx            # עצירת שירות
systemctl restart nginx         # הפעלה מחדש
systemctl enable nginx          # הפעלה אוטומטית בעלייה
systemctl is-active nginx       # האם פעיל (מתאים לסקריפטים)
systemctl --failed              # כל השירותים שנכשלו
```

---

## 8. מערכת ומשתמשים (System Info)

```bash
uname -a                # גרעין, ארכיטקטורה, שם המכונה
hostnamectl             # פרטי מערכת ההפעלה והמכונה
cat /etc/os-release     # איזו הפצת לינוקס וגרסה
uptime                  # כמה זמן המערכת פועלת
who                     # מי מחובר כרגע
w                       # מי מחובר + מה הוא עושה
last -n 10              # 10 ההתחברויות האחרונות
id                      # המשתמש והקבוצות שלי
```

---

## 9. הרשאות וקבצים (Permissions & Files)

```bash
ls -l file.txt          # הרשאות, בעלים, גודל, תאריך
stat file.txt           # מידע מלא על קובץ
chmod 644 file.txt      # קביעת הרשאות (rw-r--r--)
chown user:group file   # שינוי בעלות
lsof file.txt           # איזה תהליך פתח את הקובץ
lsof -i :80             # איזה תהליך מאזין על פורט 80
find / -name "*.conf" 2>/dev/null   # חיפוש קבצים (מתעלם משגיאות)
```

---

## 10. תקלות נפוצות – מדריך זריז 🔧

| תסמין | פקודות לבדיקה | סיבה נפוצה |
|-------|---------------|-------------|
| **המערכת איטית** | `top`, `uptime`, `free -h` | load גבוה, חוסר RAM, swapping |
| **"No space left on device"** | `df -h`, `df -i`, `du -sh /*` | דיסק מלא או inodes נגמרו |
| **אין אינטרנט** | `ip a`, `ping 8.8.8.8`, `ping google.com` | אין IP / נתב / DNS |
| **שירות לא עולה** | `systemctl status X`, `journalctl -u X` | שגיאת קונפיגורציה, פורט תפוס |
| **"port already in use"** | `ss -tulpn`, `lsof -i :<port>` | תהליך אחר תפס את הפורט |
| **תהליך נהרג מעצמו** | `dmesg -T \| grep -i oom` | ה-OOM killer (חוסר זיכרון) |
| **"Permission denied"** | `ls -l`, `id`, `namei -l <path>` | הרשאות קובץ / בעלות |
| **לא ניתן להתחבר ב-SSH** | `systemctl status sshd`, `ss -tulpn \| grep 22` | השירות כבוי / פורט חסום |

---

## 11. פקודת "בדיקה כוללת" לשילוב בסקריפט

דוגמה לסקריפט `sysreport.sh` שאוסף תמונת מצב מהירה (שילוב של דף 1 ודף זה):

```bash
#!/bin/bash

echo "===== System Report: $(date) ====="

echo ""
echo "--- Uptime & Load ---"
uptime

echo ""
echo "--- Memory ---"
free -h

echo ""
echo "--- Disk ---"
df -h | grep -v tmpfs

echo ""
echo "--- Top 5 CPU ---"
ps aux --sort=-%cpu | head -6

echo ""
echo "--- Network interfaces ---"
ip -brief a

echo ""
echo "===== End of report ====="
```

הרצה:

```bash
chmod +x sysreport.sh
./sysreport.sh
```

> אפשר לשלב עם דף 7: לשמור את הדוח לקובץ עם חותמת זמן, או להריץ אותו
> כל כמה דקות עם לולאה ו‑`sleep`.

---

➡️ המשך ל[דף 9 – תרגילי אבחון ופתרונות](09-diagnostics-exercises.md)
➡️ חזרה ל[תוכן העניינים](README.md)
