# שלב 3 · פתרונות — ניתוח באמצעות קוד

> חזרה לתרגילים: [../03-capture-and-code.md](../03-capture-and-code.md)

**1. הרצת capture.py ואז analyze_fields.py**

```bash
# edit IFACE in scripts/capture.py to your $QNET first
python3 ../scripts/capture.py
python3 ../scripts/analyze_fields.py
```

מספר הבייטים מופיע בשורה `total TCP bytes: ...`. הערך תלוי בכמות התעבורה שייצרתם בזמן הלכידה.

---

**2. ספירה לכל זוג `ip.src → ip.dst`**

```python
# analyze_fields.py — replace the per_port logic with per_pair:
per_pair = {}
for line in out.splitlines():
    t, src, dst, dport, length = line.split("|")
    key = f"{src} -> {dst}"
    per_pair[key] = per_pair.get(key, 0) + 1

for pair, count in sorted(per_pair.items(), key=lambda kv: -kv[1]):
    print(f"  {pair}: {count}")
```

---

**3. חקר מבנה ה-JSON**

```python
import json, subprocess
cmd = ["tshark", "-r", "/tmp/lab.pcapng", "-Y", "tcp", "-T", "json"]
packets = json.loads(subprocess.run(cmd, capture_output=True, text=True).stdout)
print(json.dumps(packets[0], indent=2))
```

שלושה שמות שדה שסביר למצוא: `frame.time_epoch`, `ip.ttl`, `tcp.seq` (וכן `eth.src`, `tcp.window_size_value` ועוד — תלוי בחבילה).

---

**4. מציאת חבילות RST והדפסת הפורט**

```python
# scripts/find_rst.py
import subprocess
cmd = ["tshark", "-r", "/tmp/lab.pcapng", "-Y", "tcp.flags.reset == 1",
       "-T", "fields", "-e", "ip.src", "-e", "tcp.srcport", "-e", "tcp.dstport",
       "-E", "separator=|"]
out = subprocess.run(cmd, capture_output=True, text=True).stdout
for line in out.splitlines():
    src, sport, dport = line.split("|")
    print(f"RST from {src}:{sport} (connection attempt to port {sport} refused)")
```

> הערה: ב-RST שמחזיר השרת, הפורט של *השרת* הוא `tcp.srcport` (הפורט שאליו ניסו להתחבר).

---

**5. כמה בקשות UDP לא קיבלו תשובה**

```python
# scripts/udp_unanswered.py
import pyshark
cap = pyshark.FileCapture("/tmp/lab.pcapng", display_filter="udp.port == 9001")
req = resp = 0
for pkt in cap:
    if pkt.ip.src == "192.168.0.1":
        req += 1      # client -> server
    else:
        resp += 1     # server -> client
cap.close()
print(f"requests={req} responses={resp} unanswered={req - resp}")
```

אם `req > resp`, ההפרש הוא מספר הבקשות שלא נענו.

---

**6. הרחבת echo_latency.py — ממוצע/מינימום/מקסימום**

```python
# collect RTTs into a list, then summarize:
rtts = []
# ... inside the loop, instead of printing:
rtts.append((t - req) * 1000)

# after the loop:
if rtts:
    print(f"count={len(rtts)}  min={min(rtts):.2f}  "
          f"avg={sum(rtts)/len(rtts):.2f}  max={max(rtts):.2f}  (ms)")
```

---

**7. (אתגר) monitor חי — התראה על SYN לפורט ללא שרת**

הרעיון: SYN שאחריו RST באותו חיבור = ניסיון חיבור שנדחה.

```python
# scripts/syn_monitor.py
import pyshark

IFACE = "tap0"   # your $QNET
cap = pyshark.LiveCapture(interface=IFACE, bpf_filter="tcp")
pending = {}     # (src,sport,dst,dport) -> True once SYN seen

print("monitoring for refused connection attempts ...")
for pkt in cap.sniff_continuously():
    if not hasattr(pkt, "tcp"):
        continue
    flags = int(pkt.tcp.flags, 16)
    key = (pkt.ip.src, pkt.tcp.srcport, pkt.ip.dst, pkt.tcp.dstport)
    rkey = (pkt.ip.dst, pkt.tcp.dstport, pkt.ip.src, pkt.tcp.srcport)
    if flags & 0x02 and not (flags & 0x10):      # SYN without ACK
        pending[key] = True
    elif flags & 0x04 and rkey in pending:        # RST answering a pending SYN
        print(f"ALERT: connection to {pkt.ip.src}:{pkt.tcp.srcport} "
              f"REFUSED (no server on that port)")
        pending.pop(rkey, None)
```

בדיקה: הריצו אותו, ואז `python3 ../lab-apps/tcp_client.py 192.168.0.2 9999` — אמורה להופיע התראה.
