reset


set terminal postscript eps color enhanced "Times-Roman, 46"

set output "csa2-16KB.eps" 

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

    

25	3.611879899
50	6.669319183
75	10.39909868
e

25	3.183042469
50	3.675142466
75	5.147270633
e

25	3.25103391
50	3.280978497
75	3.905463985
e

25	3.302337465
50	3.037443924
75	3.527384832
e

25	3.096344757
50	3.233243299
75	3.6780369
e

25	3.242567654
50	3.128415594
75	3.56262625
e










