#!/usr/bin/python
import string

used = ["J10", "J11", "I11", "I10", "I9", "J8", "K8", "L9", "L10", "L11", "K12"]
tmpr =	      ["J9", "K9", "K10", "K11", "J12", "I12", "H11", "H10", "H9", "I8"] 

for move in used[1 : ]:
	print move

#for move in tmpr:
#	used.append(move)
#
#for i in range(1, 20):
#	for j in range(19):
#		ans = string.ascii_uppercase[j]+str(i)
#		rev = string.ascii_uppercase[18-j]+str(20-i)
#		if not (ans in used):
#			print ans
#			used.append(ans)
#			used.append(rev)
