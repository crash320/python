# !/usr/bin/env python
# cooding=utf-8

n = int(raw_input("Please input the nth of the fe numbers:\n"))

#the solution 1: loop
fab = [1, 1]	
for i in range(2,n):
	# print fab[i-1],fab[i-2]
	fab_num = fab[i-1] + fab[i-2]
	fab.append(fab_num)
print "fab(%d) = %d" % (n, fab[n-1])

#the solution 2: the recursion

def fab_function(end_iter):
	if end_iter == 1 or end_iter == 2:
		return 1
	else:
		return fab_function(end_iter-1) \
		+ fab_function(end_iter-2)

print fab_function(n)