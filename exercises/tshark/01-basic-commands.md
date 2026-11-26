# שלב 1 · פקודות בסיסיות

> חזרה ל-[README](README.md) · הבא: [שלב 2 — ניתוח תוצאות](02-analyzing-output.md)

בשלב הזה נלמד את אבני היסוד: לכידת חבילות, שמירה לקובץ, קריאה מקובץ, וסינון בסיסי.
נניח שהגדרתם `export QNET=tap0` (החליפו בשם הממשק האמיתי — ראו README).

---

## 1.1 רשימת ממשקים

לפני כל לכידה — לאיזה ממשק להאזין?

```bash
tshark -D
```

```
1. ens33
2. tap0
3. lo (Loopback)
4. any
```

- `ens33` — תעבורה לאינטרנט.
- `tap0` — הרשת מול ה-QEMU (זה ה-`$QNET` שלנו).
- `any` — פסאודו-ממשק שמאזין לכל הממשקים יחד (שימושי, אבל בלי פרטי Ethernet מלאים).

---

## 1.2 לכידה בסיסית

להאזין ולהדפיס כל חבילה שורה-אחת-לכל-חבילה:

```bash
tshark -i "$QNET"
```

עוצרים עם `Ctrl+C`. בחלון אחר הריצו `python3 lab-apps/tcp_client.py` כדי לייצר תעבורה.
פלט לדוגמה (לחיצת יד TCP + echo):

```
    1 0.000000000 192.168.0.1 → 192.168.0.2 TCP 74 50124 → 9000 [SYN] Seq=0 Win=64240 Len=0
    2 0.000210000 192.168.0.2 → 192.168.0.1 TCP 74 9000 → 50124 [SYN, ACK] Seq=0 Ack=1 Win=65160 Len=0
    3 0.000240000 192.168.0.1 → 192.168.0.2 TCP 66 50124 → 9000 [ACK] Seq=1 Ack=1 Win=64256 Len=0
    4 0.000500000 192.168.0.1 → 192.168.0.2 TCP 78 50124 → 9000 [PSH, ACK] Seq=1 Ack=1 Win=64256 Len=12
    5 0.000900000 192.168.0.2 → 192.168.0.1 TCP 78 9000 → 50124 [PSH, ACK] Seq=1 Ack=13 Win=65160 Len=12
```

**איך קוראים את זה (משמאל לימין):** מספר חבילה · זמן יחסי · כתובת מקור ← יעד · פרוטוקול · אורך · פרטי שכבה.

---

## 1.3 הגבלת כמות ומשך הלכידה

כמעט תמיד לא רוצים לכידה אינסופית.

```bash
tshark -i "$QNET" -c 20          # stop after 20 packets
tshark -i "$QNET" -a duration:10 # stop after 10 seconds
tshark -i "$QNET" -a filesize:512 # stop after ~512 KB
```

`-c` = count, `-a` = autostop.

---

## 1.4 שמירה לקובץ וקריאה ממנו

כלל ברזל בעבודה עם tshark: **קודם מקליטים לקובץ `.pcapng`, אחר כך מנתחים שוב ושוב בלי להקליט מחדש.**

לכתוב לקובץ (`-w`):

```bash
tshark -i "$QNET" -a duration:15 -w /tmp/capture.pcapng
```

> כשמשתמשים ב-`-w` אין פלט למסך — זה תקין. ה-`tshark` עסוק בכתיבה לקובץ.

לקרוא מקובץ (`-r`):

```bash
tshark -r /tmp/capture.pcapng
```

מעכשיו כל פקודה שמשתמשת ב-`-i "$QNET"` אפשר להריץ גם על קובץ עם `-r /tmp/capture.pcapng`.

---

## 1.5 Capture filters מול Display filters — ההבדל הכי חשוב

ל-`tshark` שני סוגי מסננים שונים לגמרי, וחשוב לא להתבלבל ביניהם:

| | Capture filter | Display filter |
|---|---|---|
| דגל | `-f` | `-Y` |
| תחביר | BPF (כמו tcpdump) | Wireshark display filter |
| מתי פועל | **בזמן הלכידה** — מה בכלל נשמר | **אחרי הלכידה** — מה מוצג |
| דוגמה | `-f "tcp port 9000"` | `-Y "tcp.port == 9000"` |

כלל אצבע:
- **Capture filter (`-f`)** — להשתמש כשרוצים לצמצם את כמות החבילות שנלכדות מלכתחילה (תעבורה כבדה, קובץ גדול). מה שלא נתפס — אבד.
- **Display filter (`-Y`)** — להשתמש בניתוח. לוכדים רחב, ואז מסננים שוב ושוב מכיוונים שונים.

### דוגמאות Capture filter (`-f`, תחביר BPF)

```bash
tshark -i "$QNET" -f "host 192.168.0.2"          # only traffic to/from the guest
tshark -i "$QNET" -f "tcp port 9000"             # only our TCP echo app
tshark -i "$QNET" -f "udp port 9001"             # only our UDP app
tshark -i "$QNET" -f "tcp port 5000"             # only the Flask API
tshark -i ens33   -f "port 53"                   # only DNS on the internet-facing NIC
```

### דוגמאות Display filter (`-Y`, תחביר Wireshark)

```bash
tshark -r /tmp/capture.pcapng -Y "tcp.port == 9000"
tshark -r /tmp/capture.pcapng -Y "ip.addr == 192.168.0.2"
tshark -r /tmp/capture.pcapng -Y "tcp.flags.syn == 1 && tcp.flags.ack == 0"  # SYN only
tshark -r /tmp/capture.pcapng -Y "http.request"
tshark -r /tmp/capture.pcapng -Y "http.response.code == 404"
```

> שימו לב לתחביר: ב-BPF כותבים `tcp port 9000`, ב-display filter כותבים `tcp.port == 9000` (עם נקודה ועם `==`).

---

## 1.6 שליטה בפרטי הפלט

```bash
tshark -r /tmp/capture.pcapng -V      # Verbose: full protocol tree per packet
tshark -r /tmp/capture.pcapng -x      # Hex + ASCII dump of each packet
tshark -r /tmp/capture.pcapng -q      # Quiet: no per-packet lines (use with -z stats)
```

פורמטי חותמת זמן (`-t`):

```bash
tshark -r /tmp/capture.pcapng -t ad   # absolute date+time
tshark -r /tmp/capture.pcapng -t r    # relative to first packet (default)
tshark -r /tmp/capture.pcapng -t d    # delta from previous packet (great for latency)
```

כיבוי פענוח שמות (`-n`) — מאיץ מאוד ומונע בלבול של DNS לא רצוי:

```bash
tshark -r /tmp/capture.pcapng -n      # no name resolution (show IPs and port numbers)
```

---

## 1.7 תרגול מודרך

הריצו בשלושה חלונות:

1. ב-QEMU guest: `python3 lab-apps/tcp_echo_server.py`
2. ב-DEBIAN host חלון הקלטה:
   ```bash
   tshark -i "$QNET" -f "tcp port 9000" -w /tmp/tcp.pcapng -a duration:20
   ```
3. ב-DEBIAN host חלון שלישי, בזמן ההקלטה:
   ```bash
   python3 lab-apps/tcp_client.py 192.168.0.2 9000 "capture me"
   ```

ואז נתחו:

```bash
tshark -r /tmp/tcp.pcapng -n
```

---

## תרגילים

1. הדפיסו את רשימת הממשקים וזהו את שם הממשק שנושא את `192.168.0.1`.
2. לכדו בדיוק 5 חבילות על רשת ה-QEMU ושמרו ל-`/tmp/five.pcapng`.
3. כתבו capture filter שלוכד **רק** תעבורת UDP של אפליקציית ה-`udp_server` (פורט 9001).
4. מתוך הקובץ מ-1.7, כתבו display filter שמציג רק את חבילת ה-SYN (בלי ה-SYN/ACK).
5. הציגו את אותו קובץ עם delta-time בין חבילות. באיזה שלב בלחיצת היד יש הכי הרבה זמן?
6. הסבירו במילים שלכם מתי תעדיפו `-f` ומתי `-Y`.
7. הריצו את הלקוח מול פורט **שגוי** (למשל 9999). לכדו, ותארו מה רואים (רמז: שלב 4 ידבר על זה לעומק).
