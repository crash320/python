#!/usr/bin/env python
# cooding=utf-8

from math import sqrt
for i in range(10000):
    x = int(sqrt(i + 100))
    y = int(sqrt(i + 268))
    if(x * x == i + 100) and (y * y == i + 268):
        print i,
        