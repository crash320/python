# !/usr/bin/env python2
# cooding=utf-8

def findMax_of_List(paramter):
    if len(paramter) > 2:
		paramter.sort()
		#the above expression return None
		print paramter
		return paramter[-2:]
	else:
		return "the len(list) is < 2"

print findMax_of_List([2,3,34,23,56])

# test = [2, 3, 34, 54, 43]
# print test.sort()
