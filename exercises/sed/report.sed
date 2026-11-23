# report.sed — process a log file
/^$/d                  ;# 1. drop empty lines
s/^TODO:/[ ] TODO:/    ;# 2. mark TODO items with a checkbox
/error/i >>> ATTENTION ;# 3. add a line before each error
s/config/CONFIG/g      ;# 4. make config headers stand out
$a --- end of report ---  ;# 5. add a footer at the end
