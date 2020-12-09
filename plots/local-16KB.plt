reset


set terminal postscript eps color enhanced "Times-Roman, 46"

set output "local-16KB.eps" 

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
    

25	3.200419935
50	6.571206841
75	10.12422344
100	13.70061663
125	17.44145265
150	20.22535907
175	23.88052849
200	26.85829164
e

25	3.188968293
50	3.421463259
75	5.222506599
100	7.27996116
125	9.235960513
150	11.533939
175	13.01229144
200	15.06255723
e

25	2.83189586
50	2.902863622
75	3.397133966
100	4.098766243
125	5.513310345
150	6.348621293
175	7.713005472
200	9.060656166
e

25	2.989542227
50	3.098060489
75	3.28926154
100	3.834640895
125	4.396900023
150	4.889943918
175	5.605942624
200	6.580358107
e

25	3.190442079
50	2.927135784
75	3.133300218
100	3.523620264
125	3.712924901
150	3.988051072
175	4.728805509
200	5.899192219

e

25	3.14258146
50	3.247784971
75	3.112020405
100	3.014770133
125	3.652479881
150	3.511624914
175	4.08442919
200	4.36383661
e










