#!/usr/bin/env python3

import matplotlib.pyplot as plt

num_workers = range(1, 7)

avg_time = [26.85954914331436,
            16.175037524700166,
            14.492223372459412,
            12.997688200473785,
            12.662781839370728,
            11.682750639915467]

std_dev = [7.190067211125091,
           3.782355493196975,
           2.2953260769859742,
           1.7855038783578996,
           1.712593620799448,
           1.7690275739991372]

plt.plot(num_workers, avg_time, label="average response time")
plt.xlabel('number of workers')
plt.ylabel('seconds')
plt.savefig("graph1.png")

plt.cla()
std_dev = plt.plot(num_workers, std_dev, label="standard deviation")
plt.xlabel('number of workers')
plt.savefig("graph2.png")
