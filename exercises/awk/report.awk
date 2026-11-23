# report.awk — salary report per department
NR > 1 {
    total[$2] += $3
    count[$2]++
}
END {
    printf "%-8s %5s %10s\n", "DEPT", "N", "TOTAL"
    for (d in total)
        printf "%-8s %5d %10d\n", d, count[d], total[d]
}
