# שלב 5 · פתרון — אתגר מסכם

> חזרה לאתגר: [../05-final-challenge.md](../05-final-challenge.md)

## חלק א' · איסוף ראיות

**1. ממשק + רשימה**

```bash
ip -brief address | grep 192.168.0.1     # find the interface, e.g. tap0
export QNET=tap0
tshark -D
```

**2. הלכידה הרחבה** — כפי שניתן באתגר:

```bash
tshark -i "$QNET" -f "host 192.168.0.2" -a duration:60 -w /tmp/incident.pcapng
```

> טיפ: הריצו את הלכידה ברקע (`&`) או בחלון נפרד, והפעילו את רצף התקלות מחלק ב' בזמן שהיא רצה.

---

## חלק ג' · ניתוח ראשוני

**3. פרוטוקולים**

```bash
tshark -r /tmp/incident.pcapng -q -z io,phs
```

מצפים לראות `tcp` (echo + Flask), `http` (תת-קבוצה של tcp), ו-`icmp` אם הייתה גם תקלת UDP.

**4. שיחות TCP**

```bash
tshark -r /tmp/incident.pcapng -q -z conv,tcp
```

השיחה מול פורט 9000 עם ה-payload הגדול (20KB) תהיה העמוסה ביותר בבייטים.

**5. קודי HTTP**

```bash
tshark -r /tmp/incident.pcapng -q -z http,tree
# or:
tshark -r /tmp/incident.pcapng -Y "http.response" -T fields -e http.response.code \
  | sort | uniq -c
```

```
      2 200
      1 201
      1 404
      1 500
```

**6. expert**

```bash
tshark -r /tmp/incident.pcapng -q -z expert
```

יופיעו retransmissions ו-duplicate ACKs (מתקלת האובדן) וכן ייתכן RST (מהפורט הסגור).

---

## חלק ד' · אבחון

**7. פקודה ממוקדת לכל תקלה**

```bash
# application error
tshark -r /tmp/incident.pcapng -Y "http.response.code >= 400" \
  -T fields -e http.response.code -e http.response.phrase

# closed TCP port
tshark -r /tmp/incident.pcapng -Y "tcp.flags.reset == 1" \
  -T fields -e ip.src -e tcp.srcport

# packet loss
tshark -r /tmp/incident.pcapng -Y "tcp.analysis.retransmission" | wc -l
```

**8. רשת או אפליקציה?**

| תקלה | חתימה | הכרעה |
|---|---|---|
| 404 / 500 | handshake תקין, בלי retransmissions, אבל HTTP ≥ 400 | **אפליקציה** — הרשת העבירה הכל, השרת החזיר שגיאה |
| RST על פורט 9100 | SYN → RST מיידי | **רשת/תצורה** — אין שירות שמאזין על הפורט |
| retransmissions | SYN/data חוזרים, duplicate ACKs | **רשת** — אובדן חבילות על הקו |

הלקח: שלוש התקלות נראות שונה לגמרי ב-tshark, ולכן אפשר להבחין ביניהן בוודאות.

---

## חלק ה' · הדוח האוטומטי (תוצר סופי)

פתרון ייחוס מלא: [`scripts/incident_report.py`](../scripts/incident_report.py). הרצה:

```bash
python3 ../scripts/incident_report.py /tmp/incident.pcapng
```

פלט לדוגמה:

```
SUMMARY
-------
  eth                    frames:320 bytes:...
  ip                     frames:320 bytes:...
  tcp                    frames:298 ...
  http                   frames:8 ...
  TCP conversations (streams): 4

APPLICATION HEALTH (HTTP)
-------------------------
  2xx: 2
  3xx: 0
  4xx: 1
  5xx: 1

NETWORK HEALTH
--------------
  [DETECTED] RST (port closed)        1
  [ok      ] SYN retransmissions      0
  [DETECTED] Retransmissions (loss)   14
  [DETECTED] Duplicate ACKs           9
  [ok      ] ICMP port unreachable    0
  [ok      ] TCP ZeroWindow           0

LATENCY (TCP echo, port 9000)
-----------------------------
  samples=2  min=0.38  avg=0.47  max=0.56  (ms)

VERDICT
-------
  BOTH network and application issues detected
```

**איך הסקריפט משלב את כל השלבים:**
- `io,phs` ו-`conv` → חלק ה-SUMMARY (שלב 2).
- פירוק קודי HTTP ל-2xx/4xx/5xx → APPLICATION HEALTH (שלב 2 + 4).
- לולאה על חתימות הבעיות מטבלה 4.7 → NETWORK HEALTH (שלב 4).
- זיווג בקשה↔תשובה לפי זמן → LATENCY (שלב 3, כמו `echo_latency.py`).
- דגלי `net_problem` / `app_problem` → VERDICT שמפריד רשת מאפליקציה.

> הרחבות אפשריות (לציון מצוין): להוסיף זיהוי UDP-unreachable, לייצא את הדוח ל-JSON, או לקבל את שם הממשק והכתובות כ-arguments במקום קבועים.
