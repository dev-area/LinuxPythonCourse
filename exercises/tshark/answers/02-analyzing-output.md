# שלב 2 · פתרונות — ניתוח תוצאות

> חזרה לתרגילים: [../02-analyzing-output.md](../02-analyzing-output.md)

**1. CSV עם כותרות: זמן יחסי, מקור, יעד, פרוטוקול, אורך**

```bash
tshark -r /tmp/capture.pcapng -T fields \
  -e frame.time_relative -e ip.src -e ip.dst -e _ws.col.Protocol -e frame.len \
  -E header=y -E separator=,
```

---

**2. כל בקשות ה-HTTP עם method ו-URI בלבד**

```bash
tshark -r /tmp/capture.pcapng -Y "http.request" -T fields \
  -e http.request.method -e http.request.uri
```

---

**3. איזו שיחת TCP העבירה הכי הרבה בייטים**

```bash
tshark -r /tmp/capture.pcapng -q -z conv,tcp
```

בטבלה מסתכלים על עמודות ה-Bytes (הסכום של `->` ו-`<-`). השורה עם הסכום הגבוה ביותר היא השיחה העמוסה. בדרך כלל זו השיחה מול Flask (פורט 5000), כי בה עוברים headers ו-JSON, בעוד ה-echo מעביר מעט בתים.

---

**4. אחוז TCP מול UDP (io,phs)**

```bash
tshark -r /tmp/capture.pcapng -q -z io,phs
```

מחלקים את `frames` של `tcp` ושל `udp` בסך כל ה-frames. למשל אם `tcp frames:120` ו-`udp frames:22` מתוך 142 — זה בערך 85% TCP ו-15% UDP.

---

**5. כמה retransmissions / duplicate ACKs (expert)**

```bash
tshark -r /tmp/capture.pcapng -q -z expert
```

הספירות מופיעות ליד כל סוג הערה תחת `Notes`/`Warnings`. בלכידה נקייה על רשת מקומית לרוב יהיו 0 retransmissions. אימות ממוקד:

```bash
tshark -r /tmp/capture.pcapng -Y "tcp.analysis.retransmission" | wc -l
tshark -r /tmp/capture.pcapng -Y "tcp.analysis.duplicate_ack"   | wc -l
```

---

**6. follow TCP stream של echo — האם ה-payload זהה**

```bash
tshark -r /tmp/capture.pcapng -Y "tcp.port == 9000" -T fields -e tcp.stream | sort -u
tshark -r /tmp/capture.pcapng -q -z follow,tcp,ascii,0
```

כן — מכיוון שהשרת הוא echo, ה-payload שחוזר (Node 1 → Node 0) זהה למה שנשלח (Node 0 → Node 1). שתי השורות ב-follow יציגו את אותו טקסט.

---

**7. Top talkers לפי ip.src**

```bash
tshark -r /tmp/capture.pcapng -T fields -e ip.src | sort | uniq -c | sort -rn
```

```
    92 192.168.0.1
    50 192.168.0.2
```

---

**8. ממוצע חבילות לשנייה (awk)**

```bash
tshark -r /tmp/capture.pcapng -T fields -e frame.time_relative \
  | awk 'END {print NR/$1, "packets/sec"}'
```

`NR` = מספר החבילות הכולל, `$1` בשורה האחרונה = זמן יחסי של החבילה האחרונה (= משך הלכידה). החלוקה נותנת ממוצע חבילות לשנייה.

> דרך חלופית מובנית: `tshark -r /tmp/capture.pcapng -q -z io,stat,1` ואז ממצעים את עמודת ה-Frames.
