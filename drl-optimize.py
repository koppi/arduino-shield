#!/usr/bin/env python
#
# drl file TSP path optimizer
#

import sys
import math
import gerber
from tsp_solver.greedy import solve_tsp

# https://github.com/dmishin/tsp-solver
# https://github.com/curtacircuitos/pcb-tools

if len(sys.argv) != 2:
    print "usage: drl-optimize.py [drill-file.drl]"
    sys.exit(0)

f = gerber.read(sys.argv[1])
#print(f.report())

cnt = {}
l   = {}
t   = {}

for a,b in f.hits:
    n = a.number
    if n not in cnt.keys():
        cnt[n] = 0
        l[n]   = []
        t[n]   = (a,b)
    cnt[n] += 1
    l[n].append(b)

m = {}

for key, value in cnt.iteritems():
#    print key, value
    m[key] = [[0 for x in range(value)] for x in range(value)]

hits = {}

for key, value in cnt.iteritems():
    for i in range(0,value):
        for j in range(0,value):
            m[key][i][j] = math.hypot(l[key][i][0] - l[key][j][0], l[key][i][1] - l[key][j][1])
        
    path = solve_tsp( m[key] )
#    print path

    hits[key] = []

    for p in path:
#        print l[key][p]
        hits[key].append((t[key][0], l[key][p]))

print """
M48
FMAT,2
METRIC,TZ
"""

for i in t.keys():
    print "T%dC%f" % (t[i][0].number, t[i][0].diameter)

print """
%
G90
G05
M71
"""

for t in t.keys():
    print "T%d" % (t)
    for p in hits[t]:
        print "X%fY%f" % (p[1][0], p[1][1])

print """
T0
M30
"""
