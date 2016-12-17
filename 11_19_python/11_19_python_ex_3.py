# !/usr/bin/env python
# cooding=utf-8
# 

#input three integers, and sort them form the top down
x = []
for i in range(3):
	s = int(raw_input("Please input the interger:\n"))
	x.append(s)

x.sort()

print x
x.reverse()
print x