#!/usr/bin/env python
# cooding=utf-8

# a = 2
# print a
# def test_function(paramter):
# 	if len(paramter) > 1:
# 	else:
# 		paramter += 4
# 	return 
# print a

#~~~~~~~~~~~~~~~~~~#
# b = [3, 4, 5]
# print b
# def test_function(paramter):
# 	paramter.reverse()
# 	return 
# test_function(b)
# print a
# print b

#~~~~~~~~~~~~~~~~~~~~#
# def test_function(name, age = 20):
# 	print "name:%s, age:%d" % (name, age)

# test_function(age = 23, name ='sss')
# test_function(name = 'kkkk')

#lamada expression:
#~~~~~~~~~~~~~~~~~~
#lambda 
sum = lambda i : i*i
for i in range(9):
	print sum(i)