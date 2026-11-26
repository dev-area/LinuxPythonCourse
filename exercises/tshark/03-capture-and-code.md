# שלב 3 · הקלטת תעבורה וניתוח באמצעות קוד

> הקודם: [שלב 2](02-analyzing-output.md) · הבא: [שלב 4 — זיהוי בעיות](04-troubleshooting.md)

אתם כבר יודעים Python. בשלב הזה נחבר את tshark לקוד: נלכוד תעבורה, ננתח אותה אוטומטית,
ונבנה כלים קטנים משלנו. שלוש גישות, מהפשוטה למתוחכמת:

1. **`subprocess` + `-T fields`** — להריץ tshark ולפרסר טקסט (הכי פשוט ויציב).
2. **`-T json` / `-T ek`** — פלט מובנה שמתפרסר ישירות ל-dict.
3. **`pyshark`** — ספריית Python שעוטפת את tshark (נוחה, אבל תלות נוספת).

כל הסקריפטים בשלב זה נמצאים ב-[`scripts/`](scripts/).

---

## 3.1 להקליט מתוך הקוד

הגישה המומלצת: Python מפעיל את ה-`tshark` כתהליך, ו-tshark עושה את הלכידה בפועל
(הוא כתוב ב-C ויעיל). שמרו תמיד לקובץ ואז נתחו.

```python
# scripts/capture.py
import subprocess

IFACE = "tap0"          # replace with your $QNET
OUT = "/tmp/lab.pcapng"

cmd = [
    "tshark", "-i", IFACE,
    "-f", "host 192.168.0.2",   # capture filter: only guest traffic
    "-a", "duration:20",        # autostop after 20s
    "-w", OUT,
]
print("capturing...", " ".join(cmd))
subprocess.run(cmd, check=True)
print(f"saved to {OUT}")
```

```bash
python3 scripts/capture.py
```

> אם לא הוספתם את המשתמש לקבוצת `wireshark` (ראו README), הריצו עם `sudo python3 ...`.

---

## 3.2 גישה א': `subprocess` + `-T fields`

הכי קל לפרסור: מבקשים שדות עם מפריד, וקוראים שורה-שורה.

```python
# scripts/analyze_fields.py
import subprocess

PCAP = "/tmp/lab.pcapng"
FIELDS = ["frame.time_relative", "ip.src", "ip.dst", "tcp.dstport", "frame.len"]

cmd = ["tshark", "-r", PCAP, "-Y", "tcp", "-T", "fields"]
for f in FIELDS:
    cmd += ["-e", f]
cmd += ["-E", "separator=|"]

out = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout

total_bytes = 0
per_port = {}
for line in out.splitlines():
    t, src, dst, dport, length = line.split("|")
    length = int(length) if length else 0
    total_bytes += length
    per_port[dport] = per_port.get(dport, 0) + 1

print(f"total TCP bytes: {total_bytes}")
print("packets per destination port:")
for port, count in sorted(per_port.items(), key=lambda kv: -kv[1]):
    print(f"  port {port or '(none)'}: {count}")
```

```
total TCP bytes: 15640
packets per destination port:
  port 9000: 42
  port 5000: 30
```

**למה הגישה הזו טובה:** אין תלויות, יציבה, קלה לדיבוג (רואים בדיוק מה tshark מחזיר).
**החיסרון:** צריך לדעת מראש אילו שדות לבקש.

---

## 3.3 גישה ב': פלט JSON

כש-tshark מוציא `-T json`, מקבלים מבנה מלא של כל חבילה — אפשר `json.loads` ישירות.

```python
# scripts/analyze_json.py
import json
import subprocess

PCAP = "/tmp/lab.pcapng"

cmd = ["tshark", "-r", PCAP, "-Y", "http", "-T", "json"]
packets = json.loads(subprocess.run(cmd, capture_output=True, text=True, check=True).stdout)

for pkt in packets:
    layers = pkt["_source"]["layers"]
    if "http" in layers:
        http = layers["http"]
        # request vs response live under different keys:
        if any("request" in k for k in http):
            method = http.get("http.request.method")
            uri = http.get("http.request.uri")
            print(f"REQ  {method} {uri}")
        elif any("response" in k for k in http):
            code = http.get("http.response.code")
            print(f"RESP {code}")
```

```
REQ  GET /api/items
RESP 200
REQ  GET /api/items/999
RESP 404
REQ  POST /api/items
RESP 201
```

> מבנה ה-JSON עמוק ומשתנה לפי פרוטוקול. טיפ: הדפיסו `json.dumps(packets[0], indent=2)` של חבילה אחת כדי לראות את המפתחות המדויקים לפני שכותבים לוגיקה.
>
> לקבצים גדולים מאוד, `-T ek` נותן JSON שורה-לכל-חבילה (newline-delimited) שאפשר לקרוא בזרימה בלי לטעון הכל לזיכרון.

---

## 3.4 גישה ג': pyshark

`pyshark` עוטף את tshark ומחזיר אובייקטים של Python. נוח מאוד, אבל דורש התקנה והוא איטי יותר.

```bash
pip install pyshark
```

### ניתוח קובץ שמור

```python
# scripts/analyze_pyshark.py
import pyshark

cap = pyshark.FileCapture("/tmp/lab.pcapng", display_filter="tcp")
syn_count = 0
for pkt in cap:
    if hasattr(pkt, "tcp"):
        flags = int(pkt.tcp.flags, 16)
        if flags & 0x02:            # SYN bit
            syn_count += 1
            print(f"SYN  {pkt.ip.src}:{pkt.tcp.srcport} -> {pkt.ip.dst}:{pkt.tcp.dstport}")
cap.close()
print(f"total SYN packets (connection attempts): {syn_count}")
```

### לכידה חיה מתוך הקוד

```python
# scripts/live_pyshark.py
import pyshark

cap = pyshark.LiveCapture(interface="tap0", bpf_filter="tcp port 9000")
print("listening for 10 packets on tcp/9000 ...")
for pkt in cap.sniff_continuously(packet_count=10):
    print(pkt.ip.src, "->", pkt.ip.dst, pkt.tcp.flags)
```

> `LiveCapture` מריץ dumpcap ברקע, לכן גם כאן צריך הרשאות לכידה (קבוצת wireshark או sudo).

---

## 3.5 פרויקט קטן: מד השהיה (latency) ל-echo

נחבר הכל. הסקריפט מחשב את זמן ה-round-trip לכל בקשת echo:
מוצאים כל חבילת PSH מהלקוח (`192.168.0.1`) לשרת (פורט 9000), ואת התגובה המתאימה.

```python
# scripts/echo_latency.py
import subprocess

PCAP = "/tmp/lab.pcapng"
cmd = [
    "tshark", "-r", PCAP, "-Y", "tcp.port == 9000 && tcp.len > 0",
    "-T", "fields",
    "-e", "frame.time_relative", "-e", "ip.src", "-e", "tcp.len",
    "-E", "separator=|",
]
out = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout

sent = []
for line in out.splitlines():
    t, src, length = line.split("|")
    t = float(t)
    if src == "192.168.0.1":        # request from client
        sent.append(t)
    else:                           # echo back from server
        if sent:
            req = sent.pop(0)
            print(f"RTT = {(t - req) * 1000:.2f} ms")
```

```
RTT = 0.41 ms
RTT = 0.38 ms
RTT = 0.55 ms
```

---

## תרגילים

1. הריצו את `scripts/capture.py` (עם ה-IFACE שלכם) ואז את `analyze_fields.py`. כמה בייטים של TCP נלכדו?
2. שנו את `analyze_fields.py` כך שיספור חבילות **לכל זוג `ip.src → ip.dst`**.
3. בגישת ה-JSON, הדפיסו `json.dumps(packets[0], indent=2)` וזהו שלושה שמות שדה חדשים.
4. כתבו סקריפט שמוצא בעזרת `-T fields` את כל חבילות ה-RST (`tcp.flags.reset == 1`) ומדפיס את הפורט שאליו ניסו להתחבר.
5. בעזרת pyshark, ספרו כמה בקשות UDP נשלחו לפורט 9001 שלא קיבלו תשובה (רמז: השוו מספר בקשות למספר תשובות).
6. הרחיבו את `echo_latency.py` שידפיס גם ממוצע, מינימום ומקסימום של ה-RTT.
7. (אתגר) כתבו סקריפט "monitor" עם `LiveCapture` שמדפיס התראה בכל פעם שהוא רואה חבילת SYN לפורט שאין עליו שרת (רמז: SYN שאחריו RST).
