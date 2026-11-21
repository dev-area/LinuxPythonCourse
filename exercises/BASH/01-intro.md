# דף 1 – הקדמה, הסקריפט הראשון ופונקציות

## מה זה BASH?

**BASH** (ראשי תיבות של *Bourne Again SHell*) היא מעטפת (shell) – תוכנית שמקבלת פקודות
ומריצה אותן. כשאתם מקלידים פקודה בטרמינל, BASH היא זו שמפרשת ומריצה אותה.

**סקריפט** הוא פשוט קובץ טקסט שמכיל רשימת פקודות BASH, שרצות אחת אחרי השנייה.
במקום להקליד 20 פקודות ידנית בכל פעם – כותבים אותן פעם אחת בקובץ ומריצים את הקובץ.

---

## שורת ה‑Shebang

כל סקריפט מתחיל בשורה מיוחדת בשם **shebang**:

```bash
#!/bin/bash
```

השורה הזו אומרת למערכת ההפעלה באיזו תוכנית להשתמש כדי להריץ את הקובץ.
`#!/bin/bash` אומר: "הרץ את הקובץ הזה עם BASH".

> שימו לב: בכל שורה אחרת, תו ה‑`#` מתחיל **הערה** – טקסט שמתעלמים ממנו בהרצה.

---

## הדוגמה הראשונה – "Hello World"

העתיקו את הקוד הבא לקובץ בשם `hello.sh`:

```bash
#!/bin/bash

# This is our first comment
echo "Hello, World!"
echo "This is my first script"
```

- `echo` היא פקודה שמדפיסה טקסט למסך.

---

## איך מריצים את הסקריפט?

יש שלושה שלבים:

**1. צרו את הקובץ** (עם עורך טקסט, או בפקודה):

```bash
nano hello.sh
```

**2. תנו לקובץ הרשאת הרצה** (פעם אחת בלבד לכל קובץ):

```bash
chmod +x hello.sh
```

- `chmod +x` נותן לקובץ הרשאת "הרצה" (eXecute).

**3. הריצו את הסקריפט:**

```bash
./hello.sh
```

- ה‑`./` אומר "הקובץ נמצא בתיקייה הנוכחית".

דרך חלופית להרצה, בלי צורך בהרשאת הרצה:

```bash
bash hello.sh
```

הפלט הצפוי:

```
Hello, World!
This is my first script
```

---

## כתיבת פונקציה

**פונקציה** היא קטע קוד עם שם, שאפשר "לקרוא" לו שוב ושוב. זה חוסך כפילויות
ומסדר את הקוד. התחביר:

```bash
function_name() {
    # the function's commands
}
```

דוגמה – צרו קובץ `greet.sh` והריצו:

```bash
#!/bin/bash

# Define the function
say_hello() {
    echo "Hello! Welcome to BASH"
    echo "Today we are learning functions"
}

# Call the function (run it)
say_hello

echo "---"

# We can call it again and again
say_hello
```

שימו לב:
- מגדירים את הפונקציה **לפני** שקוראים לה.
- "קוראים" לפונקציה פשוט על ידי כתיבת שמה (בלי סוגריים).

---

## תרגיל

כתבו סקריפט בשם `about_me.sh` ש:

1. מגדיר פונקציה בשם `print_line` שמדפיסה שורת מפרידים: `=============`
2. מדפיס את השורה (באמצעות הפונקציה).
3. מדפיס שלוש שורות על עצמכם: שם, עיר, תחביב אהוב.
4. מדפיס שוב את שורת המפרידים (שימוש חוזר בפונקציה).

הפלט אמור להיראות בערך כך:

```
=============
Name: Dana
City: Haifa
Hobby: Painting
=============
```

נסו לפתור לבד לפני שתציצו בפתרון! 👇

---

## פתרון

צרו קובץ `about_me.sh`:

```bash
#!/bin/bash

# A function that prints a separator line
print_line() {
    echo "============="
}

# First use of the function
print_line

echo "Name: Dana"
echo "City: Haifa"
echo "Hobby: Painting"

# Reuse of the function
print_line
```

הרצה:

```bash
chmod +x about_me.sh
./about_me.sh
```

**מה למדנו:** הגדרת פונקציה פעם אחת ושימוש חוזר בה חוסך כתיבה חוזרת של אותו קוד.

---

➡️ המשך ל[דף 2 – משתנים וארגומנטים](02-variables-arguments.md)
