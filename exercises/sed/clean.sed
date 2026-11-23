# clean.sed — tidy up a log file
s/#.*//        ;# remove inline comments
/^$/d          ;# delete empty lines
s/ *$//        ;# trim trailing spaces
s/error/ERROR/g ;# highlight errors
