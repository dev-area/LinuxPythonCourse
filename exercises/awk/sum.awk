#!/usr/bin/awk -f
# sum the salary column
NR > 1 { sum += $3 }
END    { print "total salary:", sum }
