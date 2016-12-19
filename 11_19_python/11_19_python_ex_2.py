#!/usr/bin/env python
# cooding=utf-8


date = raw_input("Please input the date:\n")

#map() is a function that has two parameter,one is function ,the other is 
# is a list ,turpe or the dict,than the function will apply the function 
# to the every element of list ..
year, mon, day = map(int, date.split('-'))

print year, mon, day

if (year%4 == 0 or (year % 100 and year % 400)):
	leap = 1
else:
	leap = 0
# this is a dict contains the days of every months 
mon_day = {'1':31, '2':28 + leap, '3':31, '4':30, \
		'5':31, '6':30, '7':31, '8':31, '9':30, \
		'10':31, '11': 30, '12':31}
# calcuate the total days from 1-1 to mon-day of the input year
day_sum = 0
for k in range(1,13):
	if k < mon:
		day_sum += mon_day[str(k)]
	else:
		day_sum += day
		break

print day_sum
