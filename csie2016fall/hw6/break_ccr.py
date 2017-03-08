#!/usr/bin/env python2
arr = [405, 434,457,506,467,449,465,398,381,459,465,466,538,542,546,467,449,453,463,448,523,457,448,442,455,452,521,536,463,460,467,466,453,467,483,372]
flag = 'FLAG{'
for i in range(34):
	s = arr[i]
	s -= ord(flag[i])
	curr = arr[i+1]-s
	flag += chr(curr)
print flag
