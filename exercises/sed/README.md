# מדריך tshark — ניתוח תעבורת רשת משורת הפקודה

מדריך מעשי ללימוד `tshark` (גרסת שורת הפקודה של Wireshark) בסביבת Linux.
ההסברים בעברית; הפקודות, הקוד והפלט באנגלית.

---

## סביבת המעבדה (Lab topology)

```
                 ens33                      192.168.0.1        192.168.0.2
   [ Internet ] ────────► [ DEBIAN host ] ──────────────────► [ QEMU / ARM guest ]
                          (Debian Linux)   point-to-point      (Debian on ARM)
                                            lab network
```

- **DEBIAN host** — מכונת הבסיס. יש לה גישה לאינטרנט דרך הממשק `ens33`.
- **QEMU / ARM guest** — מכונה וירטואלית מבוססת ARM שרצה מעל ה-DEBIAN host.
- בין שתי המכונות קיימת רשת פרטית:
  - צד DEBIAN: `192.168.0.1`
  - צד QEMU: `192.168.0.2`

נשתמש ברשת הזו כדי להריץ שרתי/לקוחות Python (TCP, UDP, Flask REST) ולנתח את התעבורה ביניהם.

---

## זיהוי הממשקים (חשוב לפני שמתחילים)

ל-`tshark` צריך לתת ממשק נכון להקלטה. יש שני ממשקים שמעניינים אותנו:

1. `ens33` — התעבורה אל/מהאינטרנט.
2. הממשק שנושא את `192.168.0.1` — התעבורה אל/מה-QEMU. השם שלו משתנה לפי אופן ההגדרה (לרוב `tap0`, `br0`, `virbr0` או `qemu0`).

הדרך הבטוחה לזהות את הממשק של רשת ה-QEMU:

```bash
ip -brief address | grep 192.168.0.1
```

פלט לדוגמה:

```
tap0   UP   192.168.0.1/24
```

כאן הממשק הוא `tap0`. **בכל המדריך, החליפו את `tap0` בשם האמיתי אצלכם.**
כדי לחסוך הקלדה אפשר להגדיר משתנה סביבה:

```bash
export QNET=tap0       # replace with your real interface name
```

ואז להשתמש ב-`"$QNET"` בפקודות.

רשימת כל ממשקי ההקלטה שה-`tshark` רואה:

```bash
tshark -D
```

פלט לדוגמה:

```
1. ens33
2. tap0
3. lo (Loopback)
4. any
```

---

## הרשאות — להריץ tshark בלי root

לכידת תעבורה דורשת הרשאות מיוחדות. שתי אפשרויות:

**אפשרות א' (מומלצת) — להוסיף את המשתמש לקבוצת `wireshark`:**

```bash
sudo apt install tshark
sudo dpkg-reconfigure wireshark-common   # choose "Yes" to allow non-root capture
sudo usermod -aG wireshark "$USER"
# log out and back in for the group change to take effect
```

בדיקה שזה עובד:

```bash
groups                 # should include: wireshark
tshark -i "$QNET" -c 1 # should capture without sudo
```

**אפשרות ב' — פשוט להריץ עם sudo:**

```bash
sudo tshark -i "$QNET" -c 5
```

> שימו לב: אם מריצים עם `sudo`, קובצי הפלט (`-w`) ייווצרו בבעלות root. עדיפה אפשרות א'.

---

## מבנה המדריך (השלבים)

| שלב | נושא | קובץ |
|---|---|---|
| 1 | פקודות בסיסיות — לכידה, קריאה, סינון | [01-basic-commands.md](01-basic-commands.md) |
| 2 | ניתוח תוצאות — שדות, סטטיסטיקות, מעקב אחר stream | [02-analyzing-output.md](02-analyzing-output.md) |
| 3 | הקלטת תעבורה וניתוח באמצעות קוד Python | [03-capture-and-code.md](03-capture-and-code.md) |
| 4 | סימולציה של בעיות מוכרות וזיהוין ב-tshark | [04-troubleshooting.md](04-troubleshooting.md) |
| 5 | אתגר מסכם — חקירת תקרית שמשלבת הכל | [05-final-challenge.md](05-final-challenge.md) |

מומלץ לעבור לפי הסדר. כל שלב בונה על הקודם ומסתיים בתרגילים.
פתרונות לכל התרגילים נמצאים בתיקיית [`answers/`](answers/) — נסו קודם לבד.

---

## אפליקציות העזר ל-Lab

בכל המדריך נשתמש באפליקציות Python פשוטות שאתם כבר יודעים לכתוב. קבצים מוכנים נמצאים בתיקיית [`lab-apps/`](lab-apps/):

- `tcp_echo_server.py` / `tcp_client.py` — שרת/לקוח TCP
- `udp_server.py` / `udp_client.py` — שרת/לקוח UDP
- `flask_api.py` — שרת Flask REST API

**מוסכמה:** השרתים רצים על ה-QEMU guest (`192.168.0.2`), הלקוחות רצים על ה-DEBIAN host (`192.168.0.1`), וה-`tshark` מקליט על ה-DEBIAN host על גבי `"$QNET"`.
