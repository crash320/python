# !/usr/bin/env python
# cooding=utf-8

dict = {'d':1, 'i':2, 'c':3}

for k in dict:
    print k, dict[k]


from math import sqrt
for k in range(90, 1,-1):
    s = sqrt(k)
    if int(s) == s:
        print s
        break
