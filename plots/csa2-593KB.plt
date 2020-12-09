reset


set terminal postscript eps color enhanced "Times-Roman, 46"

set output "csa2-593KB.eps" 

set key right top outside
set key horizontal maxcols 3
set key spacing 1
set key font ",46pt"
set size 1.5,1.5


set xrange[25:75]
#set yrange[0:45]
set xtics 25 font ",36pt"
set ytics 5 font ",36pt"
set xlabel '{#Concurrent requests}' font ",64pt"
set ylabel 'Response time (s)' font ",64pt"
#set format y "%.2f"

plot '-' using 1:2 with lp lc 'green' lt 1 lw 10 pt 3 ps 3  t 'W=1', \
'-' using 1:2 with lp lc 'brown' lt 1 lw 10 pt 5 ps 3  t 'W=2', \
'-' using 1:2 with lp lc 'orange' lt 1 lw 10 pt 6 ps 3  t 'W=3', \
'-' using 1:2 with lp lc 'red' lt 1 lw 10 pt 7 ps 3  t 'W=4', \
'-' using 1:2 with lp lc 'blue' lt 1 lw 10 pt 7 ps 3  t 'W=5', \
'-' using 1:2 with lp lc 'cyan' lt 1 lw 10 pt 7 ps 3  t 'W=6',
    

25	6.211806822
50	11.94844446
75	18.83393936
e

25	5.096394478
50	8.618931788
75	13.00000841
e

25	4.901257184
50	6.753033911
75	10.01257118
e

25	5.035823015
50	7.428450405
75	9.902406095
e

25	4.999594959
50	6.882957131
75	9.325663095
e

25	5.26346557
50	6.860837485
75	9.804623497
e










