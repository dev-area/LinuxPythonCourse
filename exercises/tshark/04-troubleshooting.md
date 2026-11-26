# שלב 4 · סימולציה של בעיות מוכרות וזיהוין ב-tshark

> הקודם: [שלב 3](03-capture-and-code.md) · חזרה ל-[README](README.md)

זה החלק הכי שימושי: לכל בעיה קלאסית ברשת נראה **איך לייצר אותה בכוונה** עם האפליקציות שלכם,
**מה חותם האצבע שלה** ב-tshark, ו**בפקודה אחת** איך לזהות אותה.

כל תרחיש בנוי אותו דבר:
**התסמין → איך מדמים → איך מזהים → הסבר.**

הגדירו לנוחות:

```bash
export QNET=tap0        # your real interface
```

---

## 4.1 Connection refused — אין שרת שמאזין (TCP RST)

**התסמין:** הלקוח מקבל מיד `ConnectionRefusedError`. אין שרת על הפורט.

**איך מדמים:** אל תריצו את השרת, והריצו לקוח מול פורט סגור:

```bash
# server NOT running
python3 lab-apps/tcp_client.py 192.168.0.2 9000 "hi"
```

**איך מזהים:**

```bash
tshark -i "$QNET" -f "tcp port 9000" -a duration:5 -w /tmp/refused.pcapng
tshark -r /tmp/refused.pcapng -n
```

```
1 0.000000 192.168.0.1 → 192.168.0.2 TCP 74 50124 → 9000 [SYN] Seq=0
2 0.000200 192.168.0.2 → 192.168.0.1 TCP 54 9000 → 50124 [RST, ACK] Seq=1 Ack=1
```

חתימה: **SYN שמקבל מיד RST, ACK** (ולא SYN/ACK). פקודת זיהוי ישירה:

```bash
tshark -r /tmp/refused.pcapng -Y "tcp.flags.reset == 1" -T fields -e ip.src -e tcp.srcport
```

**הסבר:** כש-TCP מגיע לפורט סגור, הקרנל של היעד משיב RST. לחיצת היד לא מסתיימת. מהיר מאוד (אין timeout).

---

## 4.2 אין נתיב / פיירוול חוסם — SYN בלי תשובה (retransmissions)

**התסמין:** הלקוח "נתקע" לכמה שניות ואז נכשל ב-timeout. שונה מ-4.1 — כאן **אין RST**.

**איך מדמים:** חסמו את החבילות לפורט בעזרת פיירוול ב-DEBIAN host, ואז נסו להתחבר:

```bash
# DROP (silently discard) outbound SYNs to the guest's port 9000:
sudo iptables -A OUTPUT -p tcp --dport 9000 -d 192.168.0.2 -j DROP
python3 lab-apps/tcp_client.py 192.168.0.2 9000 "hi"
# cleanup afterwards:
sudo iptables -D OUTPUT -p tcp --dport 9000 -d 192.168.0.2 -j DROP
```

**איך מזהים:**

```bash
tshark -r /tmp/blocked.pcapng -n
```

```
1 0.000000 192.168.0.1 → 192.168.0.2 TCP [SYN] Seq=0
2 1.001000 192.168.0.1 → 192.168.0.2 TCP [TCP Retransmission] [SYN] Seq=0
3 3.005000 192.168.0.1 → 192.168.0.2 TCP [TCP Retransmission] [SYN] Seq=0
```

חתימה: **SYN שחוזר שוב ושוב** במרווחים גדלים (1s, 2s, 4s...) **ללא שום תשובה**. פקודת זיהוי:

```bash
tshark -r /tmp/blocked.pcapng -Y "tcp.analysis.retransmission && tcp.flags.syn == 1"
```

**הבחנה חשובה — DROP מול REJECT:**
- `-j DROP` → שתיקה → retransmissions (מה שראינו).
- `-j REJECT` → הקרנל מחזיר ICMP "port unreachable" או RST → נראה כמו 4.1 אבל עם ICMP.

**הסבר:** כשחבילה "נבלעת" בשקט, הצד השולח לא יודע אם היא אבדה, אז הוא משדר מחדש עם backoff מעריכי עד timeout.

---

## 4.3 אובדן חבילות ושידור חוזר (packet loss / retransmission)

**התסמין:** החיבור עובד אבל איטי; יש "תקיעות" והעברות חוזרות.

**איך מדמים:** נכניס אובדן מלאכותי עם `tc netem` על הממשק:

```bash
# add 20% packet loss on the QEMU link:
sudo tc qdisc add dev "$QNET" root netem loss 20%
# now run a larger transfer so loss is visible, e.g. a bigger echo message:
python3 lab-apps/tcp_client.py 192.168.0.2 9000 "$(head -c 20000 /dev/urandom | base64)"
# cleanup:
sudo tc qdisc del dev "$QNET" root
```

**איך מזהים:**

```bash
tshark -r /tmp/loss.pcapng -q -z expert          # summary
tshark -r /tmp/loss.pcapng -Y "tcp.analysis.flags"   # all flagged anomalies
```

```
Notes (14)
   6  This frame is a (suspected) retransmission
   4  Duplicate ACK
   2  Fast retransmission
   2  Previous segment(s) not captured
```

שדות שימושיים לסינון:

```bash
tshark -r /tmp/loss.pcapng -Y "tcp.analysis.retransmission"
tshark -r /tmp/loss.pcapng -Y "tcp.analysis.duplicate_ack"
tshark -r /tmp/loss.pcapng -Y "tcp.analysis.lost_segment"
```

ספירה לאורך זמן:

```bash
tshark -r /tmp/loss.pcapng -q -z io,stat,1,"COUNT(tcp.analysis.retransmission)tcp.analysis.retransmission"
```

**הסבר:** אובדן חבילה גורם ל-duplicate ACKs מהצד המקבל, שמפעילים fast-retransmission מהצד השולח. ריבוי כאלה = בעיית אמינות ברשת.

---

## 4.4 בעיית UDP — אין תשובה (ICMP port unreachable)

**התסמין:** לקוח UDP שולח ולא מקבל כלום (timeout). UDP לא יוצר חיבור, אז אין RST.

**איך מדמים:** אל תריצו את שרת ה-UDP, ושלחו:

```bash
# udp_server NOT running
python3 lab-apps/udp_client.py 192.168.0.2 9001 "anybody?"
```

**איך מזהים:**

```bash
tshark -r /tmp/udp.pcapng -n -Y "udp || icmp"
```

```
1 0.000000 192.168.0.1 → 192.168.0.2 UDP 50 40000 → 9001 Len=8
2 0.000300 192.168.0.2 → 192.168.0.1 ICMP 78 Destination unreachable (Port unreachable)
```

חתימה: **חבילת UDP יוצאת, וחוזר ICMP type 3 code 3** (port unreachable). פקודת זיהוי:

```bash
tshark -r /tmp/udp.pcapng -Y "icmp.type == 3 && icmp.code == 3"
```

**הבחנה:** אם במקום ICMP פשוט *אין שום תשובה* — זה לא פורט סגור אלא פיירוול שחוסם (DROP), או שהבקשה בכלל לא יצאה. ככה tshark מבדיל בין "אין שרת" ל"חסום".

**הסבר:** כשאין socket שמאזין על פורט UDP, הקרנל מחזיר ICMP port-unreachable. אבל פיירוול לרוב משתיק גם את זה — ואז אין שום אינדיקציה חוץ מהבקשה היוצאת.

---

## 4.5 שגיאות בשכבת האפליקציה — Flask 404 / 500

**התסמין:** החיבור והרשת תקינים לחלוטין, אבל האפליקציה מחזירה שגיאות. ברמת ה-TCP הכל "ירוק".

**איך מדמים:** הריצו את ה-Flask API ופנו ל-endpoints בעייתיים:

```bash
# on the guest: python3 lab-apps/flask_api.py
curl http://192.168.0.2:5000/api/items/999   # -> 404
curl http://192.168.0.2:5000/api/boom         # -> 500
```

**איך מזהים:**

```bash
tshark -i "$QNET" -f "tcp port 5000" -a duration:10 -w /tmp/http.pcapng
tshark -r /tmp/http.pcapng -Y "http.response.code >= 400" -T fields \
  -e frame.time_relative -e http.response.code -e http.response.phrase
```

```
1.204  404  NOT FOUND
3.880  500  INTERNAL SERVER ERROR
```

סיכום לפי קוד:

```bash
tshark -r /tmp/http.pcapng -q -z http,tree
```

**הסבר:** זה הלקח החשוב — **לא כל בעיה היא בעיית רשת.** ה-handshake הצליח, אין retransmissions, אבל השרת מחזיר שגיאה. tshark מאפשר להפריד בין "הרשת אשמה" ל"האפליקציה אשמה".

---

## 4.6 חלון קבלה אפס / צוואר בקבוק (TCP Zero Window)

**התסמין:** החיבור חי אבל התעבורה "נעצרת" מדי פעם. צד אחד לא מספיק לעבד.

**איך מדמים (קונספטואלי):** צד מקבל שקורא לאט ממלא את ה-receive buffer. אפשר להדגים עם
`tc netem` שמגביל קצב, או שרת שמעכב `recv`. הדגמה פשוטה של האטת קצב:

```bash
sudo tc qdisc add dev "$QNET" root netem rate 64kbit
# send a large payload...
python3 lab-apps/tcp_client.py 192.168.0.2 9000 "$(head -c 100000 /dev/urandom | base64)"
sudo tc qdisc del dev "$QNET" root
```

**איך מזהים:**

```bash
tshark -r /tmp/zw.pcapng -Y "tcp.analysis.zero_window || tcp.analysis.window_update"
```

חתימה: הודעות **`[TCP ZeroWindow]`** (המקבל אומר "תפסיק לשלוח") ואחריהן **`[TCP Window Update]`**.

**הסבר:** `tcp.window_size` יורד ל-0 כשה-buffer מלא. ריבוי Zero-Window מצביע על צד איטי (CPU, דיסק, אפליקציה שלא קוראת), לא על בעיית רשת.

---

## 4.7 טבלת סיכום — חתימות לזיהוי מהיר

| בעיה | חתימה ב-tshark | פקודת זיהוי מהירה |
|---|---|---|
| פורט TCP סגור | SYN → RST,ACK | `-Y "tcp.flags.reset==1"` |
| פיירוול חוסם (DROP) | SYN חוזר שוב ושוב, בלי תשובה | `-Y "tcp.analysis.retransmission && tcp.flags.syn==1"` |
| אובדן חבילות | retransmissions + duplicate ACKs | `-q -z expert` · `-Y "tcp.analysis.retransmission"` |
| פורט UDP סגור | ICMP type 3 code 3 | `-Y "icmp.type==3 && icmp.code==3"` |
| שגיאת אפליקציה | HTTP 4xx/5xx (TCP תקין) | `-Y "http.response.code >= 400"` |
| צד איטי / צוואר בקבוק | TCP ZeroWindow / Window Update | `-Y "tcp.analysis.zero_window"` |
| כל אנומליית TCP | הכל יחד | `-Y "tcp.analysis.flags"` |

> נקודת פתיחה אוניברסלית לכל חקירה: `tshark -r file.pcapng -q -z expert` — tshark יצביע לכם על רוב החשודים לבד.

---

## תרגילים

1. ייצרו "connection refused" וזהו את חבילת ה-RST. מה ההפרש בזמן בין ה-SYN ל-RST?
2. בעזרת `iptables ... -j DROP` חסמו פורט, לכדו, והראו את ה-retransmissions. כמה פעמים חזר ה-SYN?
3. חזרו על 2 עם `-j REJECT` במקום `DROP`. במה הפלט שונה?
4. הפעילו 20% אובדן עם `tc netem`, לכדו תעבורה, והריצו `-z expert`. כמה retransmissions נספרו?
5. שלחו UDP לפורט סגור וזהו את ה-ICMP port-unreachable. עכשיו חסמו את ה-UDP ב-iptables — מה השתנה בפלט?
6. גרמו ל-Flask להחזיר 404 ו-500. כתבו פקודה אחת שמציגה את כל התשובות עם קוד ≥ 400.
7. (אתגר) בהינתן קובץ pcap "עיוור" שלא יצרתם — בנו צ'ק-ליסט של 4 פקודות tshark שתריצו כדי לאבחן במהירות אם הבעיה היא ברשת או באפליקציה.
8. (אתגר) כתבו סקריפט Python (על בסיס שלב 3) שמקבל קובץ pcap ומדפיס אוטומטית איזו מהבעיות בטבלה 4.7 הוא מזהה.
