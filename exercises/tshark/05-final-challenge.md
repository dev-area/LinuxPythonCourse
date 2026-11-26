# שלב 5 · אתגר מסכם — "חקירת תקרית"

> הקודם: [שלב 4](04-troubleshooting.md) · פתרון: [answers/05-final-challenge.md](answers/05-final-challenge.md)

אתגר אינטגרטיבי שמשלב את כל מה שלמדתם: לכידה, סינון, ניתוח, קוד וזיהוי בעיות.
**התרחיש:** אתם מהנדסי ה-on-call. משתמשים מתלוננים שה-Flask API על ה-QEMU guest
"מתנהג מוזר ולפעמים לא עונה". המשימה שלכם: לאסוף ראיות ולהפיק **דוח תקרית** מלא —
מה תקין, מה לא, והאם האשם ברשת או באפליקציה.

> הגדירו: `export QNET=tap0` (הממשק האמיתי שלכם).
> השרתים רצים על ה-guest (`192.168.0.2`), הלקוחות על ה-host (`192.168.0.1`), ההקלטה על ה-host.

---

## חלק א' · איסוף ראיות (שלב 1)

1. ודאו איזה ממשק נושא את `192.168.0.1`, והציגו את רשימת הממשקים של tshark.
2. פתחו **לכידה אחת רחבה** שתופסת את כל התעבורה מול ה-guest לתוך קובץ, עם autostop של 60 שניות:
   ```bash
   tshark -i "$QNET" -f "host 192.168.0.2" -a duration:60 -w /tmp/incident.pcapng
   ```
   *(זו ההקלטה היחידה — כל שאר האתגר מנתח את הקובץ הזה.)*

---

## חלק ב' · ייצור התעבורה (שלבי ה-Lab)

בזמן שההקלטה מהחלק הקודם רצה, הפעילו את שלושת הפרוטוקולים — **וגם הזריקו תקלות בכוונה**.
הריצו את הרצף הבא ב-DEBIAN host (השרתים כבר צריכים לרוץ על ה-guest):

```bash
# 1) healthy TCP echo
python3 lab-apps/tcp_client.py 192.168.0.2 9000 "ping1"

# 2) healthy Flask requests
curl http://192.168.0.2:5000/api/items
curl -X POST -H "Content-Type: application/json" -d '{"name":"gamma"}' \
     http://192.168.0.2:5000/api/items

# 3) FAULT A — application errors
curl http://192.168.0.2:5000/api/items/999   # 404
curl http://192.168.0.2:5000/api/boom         # 500

# 4) FAULT B — closed TCP port (stop or never start a server on 9100)
python3 lab-apps/tcp_client.py 192.168.0.2 9100 "nobody-home" || true

# 5) FAULT C — packet loss on the link, then more echo traffic
sudo tc qdisc add dev "$QNET" root netem loss 25%
python3 lab-apps/tcp_client.py 192.168.0.2 9000 "$(head -c 20000 /dev/urandom | base64)"
sudo tc qdisc del dev "$QNET" root
```

בסוף יש לכם קובץ אחד, `/tmp/incident.pcapng`, שמכיל גם תעבורה בריאה וגם שלוש תקלות שונות.

---

## חלק ג' · ניתוח ראשוני (שלב 2)

ענו על השאלות הבאות **רק** בעזרת פקודות tshark על הקובץ:

3. אילו פרוטוקולים יש בקובץ ומה החלוקה ביניהם? (`-z io,phs`)
4. כמה שיחות TCP נפתחו ומי העמיסה הכי הרבה בייטים? (`-z conv,tcp`)
5. אילו קודי תשובה של HTTP מופיעים, וכמה מכל אחד? (`-z http,tree` או display filter)
6. האם tshark עצמו מסמן בעיות? כמה retransmissions / RST? (`-z expert`)

---

## חלק ד' · אבחון (שלב 4)

7. זהו כל אחת משלוש התקלות שהזרקתם, בפקודה ממוקדת אחת לכל אחת:
   - תקלת אפליקציה (HTTP ≥ 400)
   - פורט TCP סגור (RST)
   - אובדן חבילות (retransmissions)
8. לכל תקלה, הכריעו: **רשת או אפליקציה?** נמקו לפי מה שראיתם ב-tshark.

---

## חלק ה' · הדוח האוטומטי (שלב 3) — התוצר הסופי

9. כתבו סקריפט Python אחד, `incident_report.py`, שמקבל נתיב לקובץ pcap ומדפיס **דוח תקרית** שכולל את כל אלה:
   - **Summary** — פירוק פרוטוקולים ומספר שיחות TCP.
   - **Application health** — ספירת קודי HTTP (כמה 2xx, כמה 4xx, כמה 5xx).
   - **Network health** — חתימות הבעיות מטבלה 4.7 שזוהו (RST, retransmissions, ICMP, Zero-Window).
   - **Latency** — ממוצע/מינימום/מקסימום RTT של ה-echo (פורט 9000).
   - **Verdict** — שורת סיכום: "network issue", "application issue", "both", או "healthy".

   הסקריפט צריך להישען על `subprocess` + tshark (כמו בשלב 3), ולרוץ כך:
   ```bash
   python3 scripts/incident_report.py /tmp/incident.pcapng
   ```

**קריטריוני הצלחה:** הדוח מזהה את שלוש התקלות שהזרקתם, מפריד נכון בין בעיית רשת לבעיית אפליקציה,
ומדפיס פלט קריא שאפשר להעביר הלאה. פתרון ייחוס מלא נמצא ב-[answers](answers/05-final-challenge.md).
