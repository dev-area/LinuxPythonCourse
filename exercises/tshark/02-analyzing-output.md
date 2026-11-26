# שלב 2 · ניתוח תוצאות

> הקודם: [שלב 1](01-basic-commands.md) · הבא: [שלב 3 — ניתוח עם קוד](03-capture-and-code.md)

עכשיו שאנחנו יודעים ללכוד ולשמור, נלמד **להפיק משמעות** מהתעבורה: לחלץ שדות מדויקים,
להפוך את הפלט לטבלאות, ולהשתמש במנוע הסטטיסטיקות המובנה של tshark.

נעבוד על קובץ שהקלטנו בשלב 1 (או הקליטו חדש):

```bash
tshark -i "$QNET" -a duration:20 -w /tmp/capture.pcapng
# meanwhile: run the tcp/udp/flask clients to generate traffic
```

---

## 2.1 חילוץ שדות מדויקים (`-T fields`)

במקום שורת הסיכום המלאה, אפשר לבקש **רק שדות מסוימים**. זה הבסיס לכל ניתוח אוטומטי.

```bash
tshark -r /tmp/capture.pcapng -T fields \
  -e frame.number -e ip.src -e ip.dst -e tcp.srcport -e tcp.dstport
```

```
1   192.168.0.1   192.168.0.2   50124   9000
2   192.168.0.2   192.168.0.1   9000    50124
3   192.168.0.1   192.168.0.2   50124   9000
```

הוספת כותרות ומפריד (CSV אמיתי):

```bash
tshark -r /tmp/capture.pcapng -T fields \
  -e frame.time_relative -e ip.src -e ip.dst -e _ws.col.Protocol -e frame.len \
  -E header=y -E separator=,
```

```
frame.time_relative,ip.src,ip.dst,_ws.col.Protocol,frame.len
0.000000,192.168.0.1,192.168.0.2,TCP,74
0.000210,192.168.0.2,192.168.0.1,TCP,74
```

> `-E header=y` מוסיף שורת כותרת, `-E separator=,` קובע פסיק כמפריד, `-E quote=d` יוסיף מרכאות.
> `_ws.col.Protocol` ו-`_ws.col.Info` נותנים בדיוק את מה שרואים בעמודות ברירת המחדל.

### איך למצוא שמות שדות?

הטריק: הפעילו `-V` על חבילה אחת, וכל שורה בעץ מציגה פרוטוקול; את שם השדה המדויק רואים עם:

```bash
tshark -r /tmp/capture.pcapng -c 1 -V        # see the full tree
tshark -r /tmp/capture.pcapng -c 1 -O tcp    # expand ONLY the tcp layer in detail
```

שדות שימושיים לזכור:
`ip.src`, `ip.dst`, `tcp.srcport`, `tcp.dstport`, `udp.srcport`, `udp.dstport`,
`tcp.flags`, `tcp.seq`, `tcp.ack`, `tcp.len`, `frame.len`, `frame.time_delta`,
`http.request.method`, `http.request.uri`, `http.response.code`, `http.host`.

---

## 2.2 שילוב display filter עם field extraction

הכוח האמיתי — לסנן ואז לחלץ. למשל, כל בקשות ה-HTTP ל-Flask API:

```bash
tshark -r /tmp/capture.pcapng -Y "http.request" -T fields \
  -e ip.src -e http.request.method -e http.host -e http.request.uri
```

```
192.168.0.1   GET    192.168.0.2:5000   /api/items
192.168.0.1   GET    192.168.0.2:5000   /api/items/1
192.168.0.1   POST   192.168.0.2:5000   /api/items
```

וכל התשובות עם קוד הסטטוס:

```bash
tshark -r /tmp/capture.pcapng -Y "http.response" -T fields \
  -e frame.time_relative -e http.response.code -e http.response.phrase
```

```
0.004120   200   OK
0.009880   404   NOT FOUND
0.014200   201   CREATED
```

---

## 2.3 מנוע הסטטיסטיקות (`-z`)

tshark כולל מנוע סטטיסטיקות עשיר. מריצים אותו עם `-q -z <name>` (ה-`-q` מכבה את הפלט לכל חבילה).

### היררכיית פרוטוקולים — "מה בכלל יש בקובץ?"

```bash
tshark -r /tmp/capture.pcapng -q -z io,phs
```

```
Protocol Hierarchy Statistics
eth                    frames:142 bytes:18240
  ip                   frames:142 bytes:18240
    tcp                frames:120 bytes:15600
      http             frames:12  bytes:3100
    udp                frames:22  bytes:2640
```

### שיחות (conversations) — "מי מדבר עם מי וכמה?"

```bash
tshark -r /tmp/capture.pcapng -q -z conv,tcp
```

```
TCP Conversations
                                          |       <-      | |       ->      |
192.168.0.1:50124 <-> 192.168.0.2:9000        6   420 bytes     6   480 bytes
192.168.0.1:50130 <-> 192.168.0.2:5000       10  2100 bytes     8  1200 bytes
```

### נקודות קצה (endpoints) — "מי הכתובות/פורטים הפעילים?"

```bash
tshark -r /tmp/capture.pcapng -q -z endpoints,ip
```

### גרף תעבורה לאורך זמן (I/O statistics)

```bash
tshark -r /tmp/capture.pcapng -q -z io,stat,1
```

```
| Interval   | Frames | Bytes |
|   0 <> 1   |    48  |  6200 |
|   1 <> 2   |    12  |  1500 |
|   2 <> 3   |    82  | 10540 |
```

אפשר אפילו ספירה מותנית בתוך האינטרוול — למשל כמה retransmissions בכל שנייה:

```bash
tshark -r /tmp/capture.pcapng -q -z io,stat,1,"COUNT(tcp.analysis.retransmission)tcp.analysis.retransmission"
```

### ניתוח HTTP

```bash
tshark -r /tmp/capture.pcapng -q -z http,tree     # requests/responses breakdown by code
tshark -r /tmp/capture.pcapng -q -z http_req,tree # requests by URI
```

### Expert info — tshark מסמן בעיות בעצמו

```bash
tshark -r /tmp/capture.pcapng -q -z expert
```

```
Errors (0)
Warnings (2)
   Frequency  Summary
           2  Previous segment(s) not captured (common at capture start)
Notes (5)
           3  Duplicate ACK
           2  This frame is a (suspected) retransmission
```

> `-z expert` הוא נקודת זינוק מצוינת לשלב 4: tshark כבר מצביע לכם על החשודים.

---

## 2.4 מעקב אחר stream שלם (follow stream)

לראות את כל ה-payload של שיחת TCP אחת כרצף אחד:

```bash
# first find the stream index you want:
tshark -r /tmp/capture.pcapng -Y "tcp.port == 9000" -T fields -e tcp.stream | sort -u
# then follow it (stream 0 here):
tshark -r /tmp/capture.pcapng -q -z follow,tcp,ascii,0
```

```
===================================================================
Follow: tcp,ascii
Filter: tcp.stream eq 0
Node 0: 192.168.0.1:50124
Node 1: 192.168.0.2:9000
       12  capture me
       12  capture me
===================================================================
```

לראות את ה-payload של ה-HTTP:

```bash
tshark -r /tmp/capture.pcapng -q -z follow,http,ascii,0
```

---

## 2.5 עיבוד הפלט ב-shell

מכיוון ש-`-T fields` נותן טקסט מופרד, אפשר לחבר לכלי ה-Unix שכבר למדתם:

```bash
# Top talkers by destination IP:
tshark -r /tmp/capture.pcapng -T fields -e ip.dst | sort | uniq -c | sort -rn

# Count packets per TCP flag combination:
tshark -r /tmp/capture.pcapng -Y tcp -T fields -e tcp.flags | sort | uniq -c | sort -rn

# Average frame length with awk:
tshark -r /tmp/capture.pcapng -T fields -e frame.len \
  | awk '{sum+=$1; n++} END {printf "avg=%.1f bytes over %d frames\n", sum/n, n}'
```

> זה הגשר לשלב 3: ברגע שהפלט הוא טקסט מובנה, אפשר לנתח אותו בכל שפה — כולל Python.

---

## תרגילים

1. חלצו ל-CSV (עם כותרות) את העמודות: זמן יחסי, מקור, יעד, פרוטוקול, אורך.
2. הציגו את כל בקשות ה-HTTP עם method ו-URI בלבד.
3. מצאו בעזרת `-z conv,tcp` איזו שיחה העבירה הכי הרבה בייטים.
4. הריצו `-z io,phs`. איזה אחוז מהחבילות היו TCP ואיזה UDP?
5. בעזרת `-z expert`, האם tshark מצא retransmissions או duplicate ACKs? כמה?
6. עקבו אחרי stream ה-TCP של אפליקציית ה-echo. האם ה-payload ששלח הלקוח זהה למה שחזר?
7. בעזרת `-T fields` + `sort | uniq -c`, בנו "top talkers" לפי `ip.src`.
8. כתבו pipeline שמחשב בעזרת `awk` את מספר החבילות הממוצע לשנייה (רמז: `frame.time_relative`).
