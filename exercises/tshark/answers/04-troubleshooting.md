# שלב 4 · פתרונות — זיהוי בעיות

> חזרה לתרגילים: [../04-troubleshooting.md](../04-troubleshooting.md)

**1. Connection refused — הפרש זמן בין SYN ל-RST**

```bash
tshark -r /tmp/refused.pcapng -t d -Y "tcp.flags.syn == 1 || tcp.flags.reset == 1"
```

ההפרש (עמודת ה-delta על חבילת ה-RST) הוא בדרך כלל **פחות ממילישנייה** על רשת מקומית — הקרנל של היעד משיב RST מיד, בלי שום timeout. זה מה שמבדיל "פורט סגור" (מהיר) מ"פיירוול חוסם" (איטי, עם retransmissions).

---

**2. iptables DROP — כמה פעמים חזר ה-SYN**

```bash
sudo iptables -A OUTPUT -p tcp --dport 9000 -d 192.168.0.2 -j DROP
tshark -i "$QNET" -f "tcp port 9000" -a duration:15 -w /tmp/blocked.pcapng &
python3 ../lab-apps/tcp_client.py 192.168.0.2 9000
wait
sudo iptables -D OUTPUT -p tcp --dport 9000 -d 192.168.0.2 -j DROP

tshark -r /tmp/blocked.pcapng -Y "tcp.flags.syn == 1" | wc -l
```

לרוב רואים **5–6 חבילות SYN** (המקורית + שידורים חוזרים במרווחים 1s, 2s, 4s...) לפני שהלקוח מוותר. המספר המדויק תלוי ב-`net.ipv4.tcp_syn_retries` של הקרנל (ברירת מחדל 6).

---

**3. REJECT במקום DROP — מה שונה**

```bash
sudo iptables -A OUTPUT -p tcp --dport 9000 -d 192.168.0.2 -j REJECT
# ... capture + run client ...
sudo iptables -D OUTPUT -p tcp --dport 9000 -d 192.168.0.2 -j REJECT
```

ההבדל:
- `DROP` — שתיקה מוחלטת → SYN חוזר שוב ושוב, הלקוח נתקע שניות ואז timeout.
- `REJECT` — הפיירוול מחזיר מיד שגיאה (ברירת מחדל ICMP `port-unreachable`, או RST עם `--reject-with tcp-reset`) → הלקוח נכשל **מהר**, בלי retransmissions.

זיהוי:

```bash
tshark -r /tmp/rejected.pcapng -Y "icmp || tcp.flags.reset == 1"
```

מסקנה: המהירות של הכישלון + נוכחות/היעדר RST/ICMP מרמזים אם מדובר ב-DROP או REJECT.

---

**4. 20% אובדן — כמה retransmissions**

```bash
sudo tc qdisc add dev "$QNET" root netem loss 20%
# ... capture + send a large payload ...
sudo tc qdisc del dev "$QNET" root

tshark -r /tmp/loss.pcapng -q -z expert
tshark -r /tmp/loss.pcapng -Y "tcp.analysis.retransmission" | wc -l
```

המספר משתנה בין הרצות (אובדן אקראי), אבל עם 20% loss על עברת מידע גדולה מצפים לעשרות retransmissions ו-duplicate ACKs. ככל שה-payload גדול יותר — יותר אנומליות.

---

**5. UDP פורט סגור, ואז חסום ב-iptables**

מצב א' (שרת כבוי, בלי פיירוול):

```bash
python3 ../lab-apps/udp_client.py 192.168.0.2 9001
tshark -r /tmp/udp.pcapng -Y "icmp.type == 3 && icmp.code == 3"
```

רואים `ICMP Destination unreachable (Port unreachable)` חוזר.

מצב ב' (חוסמים גם את ה-UDP):

```bash
sudo iptables -A OUTPUT -p udp --dport 9001 -d 192.168.0.2 -j DROP
python3 ../lab-apps/udp_client.py 192.168.0.2 9001
sudo iptables -D OUTPUT -p udp --dport 9001 -d 192.168.0.2 -j DROP
```

מה שהשתנה: **ה-ICMP נעלם.** עכשיו רואים רק את חבילת ה-UDP היוצאת, בלי שום תשובה. כלומר: ICMP port-unreachable = "אין שרת"; שתיקה מוחלטת = "חסום / החבילה לא הגיעה".

---

**6. Flask 404 + 500 — פקודה אחת לכל קוד ≥ 400**

```bash
tshark -r /tmp/http.pcapng -Y "http.response.code >= 400" -T fields \
  -e frame.time_relative -e http.response.code -e http.response.phrase
```

```
1.204  404  NOT FOUND
3.880  500  INTERNAL SERVER ERROR
```

---

**7. (אתגר) צ'ק-ליסט 4 פקודות ל-pcap "עיוור"**

```bash
# 1) What protocols are even in here?
tshark -r unknown.pcapng -q -z io,phs

# 2) Who talked to whom, and how much?
tshark -r unknown.pcapng -q -z conv,tcp

# 3) Did tshark itself flag any trouble? (retransmissions, resets, zero-window...)
tshark -r unknown.pcapng -q -z expert

# 4) Any application-layer errors? (separates "network" from "app")
tshark -r unknown.pcapng -Y "http.response.code >= 400 || tcp.flags.reset == 1 || icmp"
```

ההיגיון: סקירה כללית → מי מדבר → אנומליות רשת → שכבת אפליקציה. אחרי ארבע הפקודות האלה כבר יודעים אם הבעיה ברשת (RST/retransmissions/ICMP) או באפליקציה (4xx/5xx).

---

**8. (אתגר) סקריפט זיהוי אוטומטי**

```python
# scripts/diagnose.py  —  usage: python3 diagnose.py file.pcapng
import subprocess, sys

PCAP = sys.argv[1] if len(sys.argv) > 1 else "/tmp/lab.pcapng"

def count(dfilter):
    out = subprocess.run(
        ["tshark", "-r", PCAP, "-Y", dfilter, "-T", "fields", "-e", "frame.number"],
        capture_output=True, text=True).stdout
    return len([l for l in out.splitlines() if l.strip()])

checks = {
    "TCP port closed (RST)":        "tcp.flags.reset == 1",
    "Firewall/loss (SYN retrans)":  "tcp.analysis.retransmission && tcp.flags.syn == 1",
    "Packet loss (retransmissions)":"tcp.analysis.retransmission",
    "UDP port unreachable (ICMP)":  "icmp.type == 3 && icmp.code == 3",
    "App errors (HTTP 4xx/5xx)":    "http.response.code >= 400",
    "Slow peer (TCP ZeroWindow)":   "tcp.analysis.zero_window",
}

print(f"diagnosing {PCAP}\n")
found = False
for name, dfilter in checks.items():
    n = count(dfilter)
    if n:
        found = True
        print(f"  [DETECTED] {name:32} ({n} packets)")
if not found:
    print("  no known problem signatures found — capture looks clean")
```

הרצה:

```bash
python3 ../scripts/diagnose.py /tmp/refused.pcapng
```

```
diagnosing /tmp/refused.pcapng

  [DETECTED] TCP port closed (RST)            (1 packets)
```
