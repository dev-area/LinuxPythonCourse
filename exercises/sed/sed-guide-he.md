# מדריך פשוט לפקודת `sed`

`sed` (ראשי תיבות של **S**tream **ED**itor) היא פקודה בלינוקס לעריכת טקסט "על הזבוב" — היא קוראת טקסט שורה-שורה, מבצעת עליו שינוי, ומדפיסה את התוצאה. היא שימושית מאוד להחלפת טקסט, מחיקת שורות וסינון קבצים.

> **שים לב:** כברירת מחדל `sed` לא משנה את הקובץ המקורי — היא רק מדפיסה את התוצאה למסך. כדי לשמור את השינוי בקובץ צריך את הדגל `-i` (ראה בהמשך).

---

## קובץ הקלט לדוגמה (`file.txt`)

רוב הדוגמאות במדריך עובדות על הקובץ הבא. שמור אותו בשם `file.txt` כדי להריץ את הפקודות ולראות את התוצאות בעצמך:

```text
The cat sat on the mat
A cat and a dog played
TODO: fix the config
config: logging is off
config: cache is off

error: disk full
warning: low memory
DEBUG: starting module
David Cohen
```

אפשר ליצור אותו במהירות כך:

```bash
cat > file.txt << 'EOF'
The cat sat on the mat
A cat and a dog played
TODO: fix the config
config: logging is off
config: cache is off

error: disk full
warning: low memory
DEBUG: starting module
David Cohen
EOF
```

דוגמה מהירה — הפעלת החלפה על הקובץ:

```bash
sed 's/cat/dog/g' file.txt
# The dog sat on the mat
# A dog and a dog played
# ... שאר השורות ללא שינוי
```

---

## מבנה בסיסי

```bash
sed 'command' file
```

אפשר גם להעביר טקסט דרך צינור (pipe):

```bash
cat file | sed 'command'
echo "hello world" | sed 's/world/linux/'
```

---

## 1. החלפת טקסט (הפקודה הנפוצה ביותר)

התבנית: `s/search/replace/`

```bash
# replace the first match in each line
sed 's/cat/dog/' file.txt

# replace all matches in the line (g = global)
sed 's/cat/dog/g' file.txt

# case-insensitive replace (i = ignore case)
sed 's/cat/dog/gi' file.txt
```

דוגמה:

```bash
echo "cat cat cat" | sed 's/cat/dog/g'
# output: dog dog dog
```

---

## 2. שמירת השינוי בקובץ (`-i`)

```bash
# edit the file itself
sed -i 's/cat/dog/g' file.txt

# edit the file and keep a backup named file.txt.bak
sed -i.bak 's/cat/dog/g' file.txt
```

---

## 3. מחיקת שורות

```bash
# delete line number 3
sed '3d' file.txt

# delete lines 2 to 5
sed '2,5d' file.txt

# delete empty lines
sed '/^$/d' file.txt

# delete every line containing the word "error"
sed '/error/d' file.txt
```

---

## 4. הדפסת שורות ספציפיות (`-n` עם `p`)

הדגל `-n` מכבה את ההדפסה האוטומטית, והפקודה `p` מדפיסה רק מה שביקשנו.

```bash
# print only line 5
sed -n '5p' file.txt

# print lines 10 to 20
sed -n '10,20p' file.txt

# print only lines containing "warning"
sed -n '/warning/p' file.txt
```

---

## 5. עבודה לפי תבנית (regex)

```bash
# add "# " at the start of every line beginning with TODO
sed 's/^TODO/# TODO/' file.txt

# remove trailing spaces at the end of each line
sed 's/ *$//' file.txt

# replace only in lines containing the word "config"
sed '/config/ s/off/on/g' file.txt
```

| סימן | משמעות |
|------|---------|
| `^`  | תחילת שורה |
| `$`  | סוף שורה |
| `.`  | כל תו בודד |
| `*`  | אפס מופעים או יותר |
| `[abc]` | אחת מהאותיות a, b או c |

---

## 6. מספר פקודות יחד

```bash
# using -e for each command
sed -e 's/cat/dog/' -e 's/red/blue/' file.txt

# or using a semicolon
sed 's/cat/dog/; s/red/blue/' file.txt
```

---

## טיפים מהירים

- רוצה להשתמש בתו `/` בתוך החיפוש? אפשר להחליף את המפריד לכל תו אחר:
  ```bash
  sed 's#/old/path#/new/path#g' file.txt
  ```
- תמיד כדאי להריץ **קודם בלי `-i`** כדי לראות שהתוצאה נכונה, ורק אז להוסיף `-i`.
- `&` בצד המחליף מייצג את הטקסט שנמצא:
  ```bash
  echo "123" | sed 's/[0-9]*/[&]/'
  # output: [123]
  ```

---

## סיכום הדגלים החשובים

| דגל | מה הוא עושה |
|-----|--------------|
| `-i` | עורך את הקובץ במקום (in-place) |
| `-n` | לא מדפיס אוטומטית (משולב עם `p`) |
| `-e` | מאפשר מספר פקודות |
| `g`  | החלפה של כל המופעים בשורה |
| `i`  | התעלמות מאותיות גדולות/קטנות |
| `d`  | מחיקת שורה |
| `p`  | הדפסת שורה |

---

## דוגמאות מתקדמות

### 1. קבוצות לכידה (Capture Groups)

אפשר ללכוד חלקים מהטקסט בעזרת `\( \)` ולהשתמש בהם בצד המחליף עם `\1`, `\2` וכו'.

```bash
# swap the order of first name and last name
echo "David Cohen" | sed 's/\([A-Za-z]*\) \([A-Za-z]*\)/\2 \1/'
# output: Cohen David

# extract the username from an email address
echo "user@example.com" | sed 's/\(.*\)@.*/\1/'
# output: user
```

> **טיפ:** עם הדגל `-E` (או `-r`) אפשר לכתוב regex מורחב בלי להבריח סוגריים: `sed -E 's/(\w+) (\w+)/\2 \1/'`

---

### 2. החלפה רק במופע מסוים

```bash
# replace only the second match in each line
echo "a a a a" | sed 's/a/X/2'
# output: a X a a

# replace from the second match onward (2 + g)
echo "a a a a" | sed 's/a/X/2g'
# output: a X X X
```

---

### 3. עבודה על טווחים לפי תבנית

```bash
# print all lines between START and END (inclusive)
sed -n '/START/,/END/p' file.txt

# delete the whole block between two patterns
sed '/BEGIN/,/END/d' file.txt

# replace only inside the range
sed '/<body>/,/<\/body>/ s/old/new/g' page.html
```

---

### 4. הוספת שורות (`a`, `i`, `c`)

```bash
# a = append — add a line after line 3
sed '3a new appended line' file.txt

# i = insert — add a line before every line containing "error"
sed '/error/i --- warning below ---' file.txt

# c = change — replace an entire line with other text
sed '/DEBUG/c # line removed' file.txt
```

---

### 5. שינויים מרובי שורות (Hold Space)

ל-`sed` יש "זיכרון" נוסף שנקרא **hold space** המאפשר לעבוד על כמה שורות יחד.

```bash
# reverse the order of lines in the file (like tac)
sed -n '1!G;h;$p' file.txt

# join all lines into one line separated by spaces
sed ':a;N;$!ba;s/\n/ /g' file.txt
```

הסבר קצר ל-`:a;N;$!ba`:
- `:a` — מגדיר תווית (label) בשם `a`.
- `N` — מצרף את השורה הבאה ל-pattern space.
- `$!ba` — אם זו לא השורה האחרונה, חוזר לתווית `a`.

---

### 6. מספור שורות ועבודה עם מספרים

```bash
# add a line number at the start of each line (= then N)
sed '=' file.txt | sed 'N;s/\n/\t/'

# delete the first and last line
sed '1d;$d' file.txt

# print every other line
sed -n '1~2p' file.txt      # odd-numbered lines (GNU sed)
```

---

### 7. דוגמאות שימושיות מהחיים האמיתיים

```bash
# strip comments (#) and empty lines from a config file
sed -e 's/#.*//' -e '/^$/d' config.conf

# convert Windows line endings (CRLF) to Unix (LF)
sed 's/\r$//' windows_file.txt

# wrap every word in quotes
echo "red green blue" | sed 's/\w\+/"&"/g'
# output: "red" "green" "blue"

# extract IP addresses from a log
sed -n -E 's/.*([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+).*/\1/p' access.log
```

---

### טבלת תווים מיוחדים בצד המחליף

| סימן | משמעות |
|------|---------|
| `&`    | כל הטקסט שנמצא |
| `\1`–`\9` | קבוצת לכידה לפי סדר |
| `\n`   | שורה חדשה |
| `\t`   | טאב |
| `\U`   | הפיכת הטקסט שאחריו לאותיות גדולות (GNU) |
| `\L`   | הפיכת הטקסט שאחריו לאותיות קטנות (GNU) |

דוגמה להפיכת מילה לאותיות גדולות:

```bash
echo "hello world" | sed 's/\w\+/\U&/'
# output: HELLO world
```

---

## סקריפטים של `sed`

כשצריך להריץ הרבה פקודות `sed` יחד, נוח לשמור אותן בקובץ סקריפט נפרד במקום לדחוס הכל לשורה אחת. מריצים קובץ כזה עם הדגל `-f`.

### 1. קובץ סקריפט בסיסי (`-f`)

שומרים את הפקודות בקובץ, למשל `clean.sed`:

```sed
# clean.sed — tidy up a log file
s/#.*//        ;# remove inline comments
/^$/d          ;# delete empty lines
s/ *$//        ;# trim trailing spaces
s/error/ERROR/g ;# highlight errors
```

ומריצים אותו כך:

```bash
sed -f clean.sed file.txt
```

> בתוך קובץ סקריפט כל פקודה יכולה להיות בשורה נפרדת (בלי `;`), וזה קריא הרבה יותר. אפשר להוסיף הערות עם `#`.

---

### 2. סקריפט עם shebang (קובץ ריצה עצמאי)

אפשר להפוך סקריפט `sed` לתוכנית שרצה לבד. יוצרים קובץ בשם `upper.sed`:

```sed
#!/usr/bin/sed -f
# turn the first word of each line into UPPERCASE
s/\w\+/\U&/
```

נותנים הרשאת הרצה ומפעילים ישירות:

```bash
chmod +x upper.sed
./upper.sed file.txt
```

---

### 3. סקריפט רב-שלבי לדוגמה

הסקריפט הבא (`report.sed`) מנקה קובץ לוג ומסמן שורות חשובות — הוא מדגים כמה פקודות שעובדות יחד:

```sed
# report.sed — process a log file
/^$/d                  ;# 1. drop empty lines
s/^TODO:/[ ] TODO:/    ;# 2. mark TODO items with a checkbox
/error/i >>> ATTENTION ;# 3. add a line before each error
s/config/CONFIG/g      ;# 4. make config headers stand out
$a --- end of report ---  ;# 5. add a footer at the end
```

הרצה:

```bash
sed -f report.sed file.txt
```

---

### 4. שימוש ב-`-n` בתוך סקריפט

כשרוצים לשלוט בעצמנו מה מודפס (למשל להוציא רק שורות מסוימות), מוסיפים `-n` וב-סקריפט משתמשים ב-`p`:

```sed
# extract.sed — print only warnings and errors
/warning/p
/error/p
```

```bash
sed -n -f extract.sed file.txt
# warning: low memory
# error: disk full
```

---

### טיפים לכתיבת סקריפטים

- כל שורה בקובץ היא פקודה; אין צורך במרכאות מסביב לפקודה (בניגוד לשורת הפקודה).
- הערה מתחילה ב-`#`. הערה אחרי פקודה באותה שורה צריכה `;` לפניה: `s/a/b/ ;# comment`.
- אפשר לשלב כמה קבצי סקריפט או פקודות: `sed -f part1.sed -f part2.sed -e 's/x/y/' file.txt`.
- לבדיקה בטוחה — הרץ קודם בלי `-i`, וכשהתוצאה נכונה הוסף `-i` כדי לשמור בקובץ: `sed -i -f clean.sed file.txt`.
