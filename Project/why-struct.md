# למה צריך struct בפייתון

## הבעיה

בפייתון מספר הוא אובייקט, לא רצף בתים. ל-`int` אין גודל קבוע, אין לו סדר בתים, והוא לא "יושב בזיכרון" בצורה שאפשר לשלוח כמו שהיא. לעומת זאת פרוטוקול תקשורת בינארי מגדיר בדיוק כמה בתים תופס כל שדה ובאיזה סדר הם נשלחים.

לכן בכל פעם ששולחים או מקבלים הודעה בינארית צריך להמיר בין שני העולמות:

- **אריזה (pack):** ערכים של פייתון ← רצף בתים לפי מבנה ההודעה.
- **פירוק (unpack):** רצף בתים שהתקבל ← ערכים של פייתון.

אפשר לעשות את זה ידנית, ואפשר עם המודול `struct`. שתי הדוגמאות הבאות מממשות את אותה הודעה בשתי הדרכים.

## מבנה ההודעה בדוגמאות

| שדה | גודל | תיאור |
|---|---|---|
| SOF | 2 |  `0xAA 0x55` |
| LEN | 1 | אורך ה-DATA |
| DATA | LEN | הנתונים |
| CHECKSUM | 1 | `(LEN + סכום בתי ה-DATA) & 0xFF` |

עבור `b"Hello"` ההודעה היא:

```
AA 55 05 48 65 6C 6C 6F F9
```

בדיקת ה-checksum: `5 + 0x48 + 0x65 + 0x6C + 0x6C + 0x6F = 505`, ו-`505 & 0xFF = 249 = 0xF9`.

## דוגמה 1: בלי struct

```python
SOF = [0xAA, 0x55]

def build_packet(data):
    length = len(data)
    checksum = (length + sum(data)) & 0xFF

    packet = bytearray()
    packet.extend(SOF)
    packet.append(length)
    packet.extend(data)
    packet.append(checksum)

    return packet

def decode_packet(packet):
    if len(packet) < 4:
        raise ValueError("Packet too short")

    sof = packet[0:2]
    length = packet[2]
    data = packet[3:3 + length]
    checksum = packet[3 + length]

    if sof != bytes([0xAA, 0x55]):
        raise ValueError("Invalid SOF")

    if len(packet) != length + 4:
        raise ValueError("Invalid length")

    if checksum != (length + sum(data)) & 0xFF:
        raise ValueError("Invalid checksum")

    return data
```

כאן בונים את ההודעה בית אחרי בית עם `append` ו-`extend`, וקוראים אותה לפי אינדקסים: `packet[2]` הוא האורך, `packet[3 + length]` הוא ה-checksum.

## דוגמה 2: עם struct

```python
import struct

SOF = 0xAA55

def pack_packet(data: bytes) -> bytes:
    length = len(data)

    if length > 255:
        raise ValueError("Data too long")

    checksum = (length + sum(data)) & 0xFF

    return struct.pack(">HB", SOF, length) + data + struct.pack("B", checksum)


def unpack_packet(packet: bytes):
    if len(packet) < 4:
        raise ValueError("Packet too short")

    sof, length = struct.unpack(">HB", packet[:3])

    if sof != SOF:
        raise ValueError("Invalid SOF")

    if len(packet) != length + 4:
        raise ValueError("Invalid packet length")

    data = packet[3:3 + length]
    checksum = struct.unpack("B", packet[-1:])[0]

    expected = (length + sum(data)) & 0xFF

    if checksum != expected:
        raise ValueError("Checksum error")

    return data
```

כאן הכותרת מתוארת במחרוזת פורמט אחת, `">HB"`: מספר של 2 בתים (ה-SOF) ואחריו מספר של בית אחד (האורך), בסדר big-endian. אותה מחרוזת משמשת גם לאריזה וגם לפירוק.

## אז מה ההבדל?

שתי הדוגמאות מייצרות בדיוק את אותם בתים. בהודעה הזאת struct כמעט לא חוסך כלום, והסיבה פשוטה: **כל השדות המספריים הם בגודל בית אחד**. בית אחד הוא מספר בין 0 ל-255, ו-`bytearray.append` יודע לטפל בו ישירות.

גם כאן יש כבר שלושה הבדלים קטנים:

- **ה-SOF הוא ערך אחד.** בדוגמה 2 הוא מוגדר פעם אחת כ-`0xAA55` ומושווה כמספר. בדוגמה 1 הוא מוגדר כרשימה `[0xAA, 0x55]` ובבדיקה נכתב שוב כ-`bytes([0xAA, 0x55])`, כלומר אותו קבוע מופיע פעמיים בשתי צורות.
- **המבנה כתוב במקום אחד.** `">HB"` מתאר את הכותרת. בדוגמה 1 המבנה מפוזר בין האינדקסים `0:2`, `2`, `3`.
- **בדיקת טווח.** אורך מעל 255 לא נכנס לבית אחד. בדוגמה 2 זה נבדק במפורש. בדוגמה 1 `append(length)` יזרוק שגיאה כללית של `bytearray`, בלי הסבר מה לא בסדר בהודעה.

ההבדל האמיתי מתגלה ברגע שהפרוטוקול גדל.

## איפה הגישה הידנית נשברת

נניח שמוסיפים לפרוטוקול שלושה דברים: אורך של 2 בתים (כדי לתמוך בהודעות ארוכות), טמפרטורה כמספר **עם סימן** של 2 בתים, וחותמת זמן של 4 בתים.

### שדה של יותר מבית אחד

ידנית צריך לפרק את המספר לבתים עם הזזות ומסכות, ולהרכיב אותו חזרה:

```python
# pack: length = 300 -> 01 2C
packet.append((length >> 8) & 0xFF)
packet.append(length & 0xFF)

# unpack
length = (packet[2] << 8) | packet[3]
```

עם struct:

```python
struct.pack(">H", 300)                 # b'\x01\x2c'
(length,) = struct.unpack(">H", packet[2:4])
```

### סדר בתים (endianness)

האם הבית הגבוה נשלח ראשון או אחרון? בגרסה הידנית התשובה מוסתרת בסדר של שתי שורות ה-`append`. טעות בסדר לא גורמת לשגיאה, רק לערך שגוי בצד השני. עם struct זה תו אחד במחרוזת הפורמט:

```python
struct.pack(">H", 300)    # big-endian:    01 2C
struct.pack("<H", 300)    # little-endian: 2C 01
```

### מספרים עם סימן

טמפרטורה של 50- צריכה להישלח כ-`FF CE` (משלים ל-2). ידנית:

```python
# pack
value = -50 & 0xFFFF                   # 0xFFCE
packet.append(value >> 8)
packet.append(value & 0xFF)

# unpack
value = (packet[0] << 8) | packet[1]
if value >= 0x8000:
    value -= 0x10000
```

עם struct ההבדל בין מספר עם סימן לבלי סימן הוא אות קטנה מול אות גדולה:

```python
struct.pack(">h", -50)                 # b'\xff\xce'
(value,) = struct.unpack(">h", b"\xff\xce")   # -50
```

### מספרים עשרוניים

להמיר `float` לארבעה בתים בפורמט IEEE 754 בעזרת הזזות ומסכות זה כבר לא מעשי. עם struct:

```python
struct.pack(">f", 36.6)
```

### כמה שדות ביחד

כותרת עם SOF, פקודה, אורך וטמפרטורה נארזת בקריאה אחת, ומתפרקת בקריאה אחת לכמה משתנים:

```python
header = struct.pack(">HBHh", 0xAA55, 2, 300, -50)
# AA 55 02 01 2C FF CE

sof, cmd, length, temp = struct.unpack(">HBHh", header)
```

הגרסה הידנית של אותה כותרת היא בערך 15 שורות של הזזות, וכל אחת מהן מקום לטעות.

## מה struct נותן

1. **המבנה מתועד בקוד.** מחרוזת הפורמט היא תיאור של ההודעה, ואפשר להשוות אותה ישירות לטבלה שבמסמך הפרוטוקול.
2. **סימטריה.** אותה מחרוזת משמשת לאריזה ולפירוק, כך ששני הצדדים לא יכולים "להתרחק" זה מזה.
3. **סדר בתים מפורש.** `>` או `<` בתחילת המחרוזת, במקום להסיק אותו מסדר השורות.
4. **סימן, גדלים ו-float** בלי חשבון ידני.
5. **בדיקת טווח.** `struct.pack(">B", 300)` זורק `struct.error` במקום לשלוח ערך קטוע.
6. **חישוב גודל.** `struct.calcsize(">HBHh")` מחזיר 7, וכך יודעים כמה בתים לקרוא מה-socket לפני שמפרקים.

## מחרוזת הפורמט בקצרה

התו הראשון קובע את סדר הבתים:

| תו | משמעות |
|---|---|
| `>` | big-endian (הבית הגבוה ראשון) |
| `<` | little-endian |
| `!` | network order, זהה ל-`>` |

התווים הבאים הם השדות, לפי הסדר:

| תו | גודל | סוג |
|---|---|---|
| `B` / `b` | 1 | בלי סימן / עם סימן |
| `H` / `h` | 2 | בלי סימן / עם סימן |
| `I` / `i` | 4 | בלי סימן / עם סימן |
| `Q` / `q` | 8 | בלי סימן / עם סימן |
| `f` | 4 | float |
| `d` | 8 | double |
| `5s` | 5 | רצף של 5 בתים |

שלושה דברים שכדאי לזכור:

- **תמיד לכתוב `>` או `<`.** בלי התו הזה struct משתמש בסדר הבתים וביישור (padding) של המחשב המקומי. למשל `struct.calcsize("BH")` מחזיר 4 ולא 3, כי נוסף בית ריפוד.
- **`unpack` מחזיר תמיד tuple**, גם לשדה אחד. לכן כותבים `(length,) = struct.unpack(...)` או `struct.unpack(...)[0]`.
- **מספר הבתים חייב להתאים בדיוק** לפורמט, אחרת נזרק `struct.error`. כדי לפרק מתוך אמצע buffer משתמשים ב-`struct.unpack_from(fmt, buffer, offset)`.

## ומה עם int.to_bytes?

לשדה בודד יש בפייתון גם `int.to_bytes` ו-`int.from_bytes`:

```python
(300).to_bytes(2, "big")                       # b'\x01\x2c'
int.from_bytes(b"\xff\xce", "big", signed=True)  # -50
```

זה פתרון טוב למספר אחד. struct עדיף כשיש כמה שדות ברצף, כי הוא מתאר את כל הכותרת בשורה אחת ותומך גם ב-float.

## סיכום

| | בלי struct | עם struct |
|---|---|---|
| שדות של בית אחד | פשוט | פשוט |
| שדות של 2, 4, 8 בתים | הזזות ומסכות | תו אחד בפורמט |
| סדר בתים | מוסתר בסדר השורות | `>` או `<` |
| מספרים שליליים | חשבון משלים ל-2 | אות קטנה |
| float | לא מעשי | `f` או `d` |
| תיאור המבנה | מפוזר באינדקסים | מחרוזת אחת |

כל עוד כל השדות הם בית אחד, אפשר להסתדר בלי struct. ברגע שמופיע שדה רחב יותר, מספר שלילי או float, struct הופך את הקוד לקצר יותר, קריא יותר וקשה יותר לטעות בו. בפרויקט הסיום הכותרת כוללת אורך של 2 בתים ו-CRC של 2 בתים, והחיישנים מחזירים `int16` עם סימן, ולכן הקוד שם משתמש ב-struct.
