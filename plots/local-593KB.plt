reset


set terminal postscript eps color enhanced "Times-Roman, 46"

set output "local-593KB.eps"

set key right top outside
set key horizontal maxcols 3
set key spacing 1
set key font ",46pt"
set size 1.5,1.5


set xrange[25:200]
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

25	4.993347476
50	10.89030585
75	16.38977997
100	20.96038068
125	26.76369662
150	31.7304059
175	37.08660146
200	41.31353389
e

25	3.689396826
50	5.659724245
75	8.813358216
100	10.7329652
125	12.67393752
150	15.91400875
175	19.27024891
200	21.04657862
e

25	3.85932992
50	6.323598682
75	8.744712043
100	8.968627292
125	11.06026157
150	12.21775664
175	12.72505551
200	14.68373139
e

25	3.873005972
50	4.582134589
75	5.891555972
100	7.96584739
125	8.790848371
150	10.58856187
175	11.87596781
200	12.32145332
e

25	3.829458621
50	4.394950566
75	6.08173191
100	8.741539179
125	9.329251326
150	11.75903567
175	13.36016593
200	13.71756689
e

25	4.069866336
50	4.797948025
75	5.739386657
100	7.710865654
125	9.819242458
150	10.54524759
175	12.21360206
200	13.36056629
e
