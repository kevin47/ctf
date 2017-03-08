#!/usr/bin/python
import socket
import re
import md5
import math
import sys
#import time

s = socket.socket()
s.connect(('csie.ctf.tw', 10124))
#time.sleep(3)
#s.setblocking(0)
cnt = 0
arr = []

def s5_create_arr(sub):
	for i in range(len(sub)):
		xx = recv[i2+i]
		yy = recv[i1+i]
		if recv[i2+i].isalpha():
			#print xx, yy, (ord(recv[i2+i]) - ord(recv[i1+i])+26)%26
			arr.append((ord(recv[i2+i]) - ord(recv[i1+i])+26)%26)

def s5_find_duplicate():
	for i in range(2, len(arr)):
		yes = 1
		for j in range(i):
			if i+j >= len(arr): break
			if arr[j] != arr[i+j]:
				yes = 0
				break
		if yes: return i

def s6_hex_xor(plain, cipher):
	key = []
	#print plain, cipher
	for i in range(len(plain)):
		key.append(ord(plain[i]) ^ int(cipher[i*2 : i*2+2], 16))
	#print key
	return key

def s8_cmp(ss, pat):
	for i in range(4):
		if ss[i] != pat[i]: return 0
	return 1

done = ''
def s8_dfs(ans, depth, pattern):
	global done
	if done: return
	if depth >= 20: return
	ans += ' '
	for i in range(ord('a'), ord('z')):
		ans = ans[ : depth] + chr(i) + ans[depth+1 : ]
		if s8_cmp(md5.new(ans).hexdigest(), pattern):
			done = ans
			return
		s8_dfs(ans, depth+1, pattern)

#s8_dfs('', 0, 'c754')
#print done, md5.new(done).hexdigest()

def s7_decipher(plain, cipher, lenght, beg):
	for key in range(beg, lenght+1):
		col = int(math.ceil(len(cipher)/float(key)))
		rem = len(cipher)%key
		#if rem == 0: rem = col
		#print col, key, rem, 'jizz'
		ans = ''
		for j in range(col):
			for i in range(key):
				if i < rem:
					#print key, j, i
					sys.stdout.flush()
					ans += cipher[col*i + j]
				elif j < (col-1):
					#print rem*col, key, i, j
					sys.stdout.flush()
					ans += cipher[rem*col + (i-rem)*(col-1) + j]
			#if j == col-1: print '= ='+ans, beg, range(beg, lenght+1)
			if ans == plain and beg == 1: return key
			elif j == col-1 and beg != 1:
				#print 'OAO '+ans, beg
				return ans
	return -1
#print s7_decipher('the road, but he immediately called me back, and a', 't, tla h ieecaebmldk umy ,rte m o dceaahia ndealbd', len('t, tla h ieecaebmldk umy ,rte m o dceaahia ndealbd'))

while True:
	recv = s.recv(1024)
	if recv: print recv
	if re.search('Congrats!', recv): break
	if re.search('STAGE', recv): cnt += 1
	if re.search('Round', recv) and cnt < 3:
		index = recv.rfind(':')+2
		sub = recv[index : ].rstrip()
		if cnt == 1: s.sendall(sub.decode('hex')+'\n')
		elif cnt == 2: s.sendall(sub.decode('base64')+'\n')
	elif (cnt == 3 or cnt == 4 or cnt == 5) and re.search('m0 = ', recv):
		#cnt == 4 has chance to go wrong but IDK why
		index = recv.find('c1 = ')+len('c1 = ')
		sub = recv[index : ].splitlines()[0]
		ans = ''
		pos = 0
		if cnt == 4 or cnt == 5:
			i1 = recv.find('c0 = ')+len('c0 = ')
			i2 = recv.find('m0 = ')+len('m0 = ')
			diff = ord(recv[i2]) - ord(recv[i1])
			if cnt == 5:
				s5_create_arr(sub)
				pos = s5_find_duplicate()

		it = 0
		for c in sub:
			if c.isalpha():
				if cnt == 3: tmp = chr(25-ord(c.lower())+ord('a')*2)	# mirror -(ord(c)-ord('a')-13)+13
				elif cnt == 4: tmp = chr((ord(c.lower())-ord('a')+diff+26)%26+ord('a'))
				elif cnt == 5:
					tmp = chr((ord(c.lower())-ord('a')+arr[it%pos]+26)%26+ord('a'))
					it += 1
				#print tmp
				if c.isupper(): ans += tmp.upper()
				else: ans += tmp
			else: ans += c
		s.sendall(ans+'\n')
	elif cnt == 6 and re.search('m0 = ', recv):
		#has chance to go wrong but IDK why
		cipher = [None]*3
		mx = 0
		for i in range(3):
			index = recv.find('c'+str(i)+' = ')+5
			cipher[i] = recv[index : ].splitlines()[0]
			if len(cipher[mx]) >= len(cipher[i]): mx = i
		index = recv.find('m'+str(mx)+' = ')+len('m'+str(mx)+' = ')
		plain = recv[index : ].splitlines()[0]
		key = s6_hex_xor(plain, cipher[mx])
		index = recv.find('c3 = ')+5
		cipher[0] = recv[index : ].splitlines()[0]
		ans = s6_hex_xor(map(chr, key), cipher[0])
		#print map(chr, ans)
		ans[0] = chr(ans[0])
		ANS = reduce(lambda x, y: x + chr(y),ans)+'\n'
		print ANS
		s.sendall(ANS)
	elif cnt == 7 and re.search('m0 = ', recv):
		index = recv.find('m0 = ')+5
		plain = recv[index : ].splitlines()[0]
		index = recv.find('c0 = ')+5
		cipher = recv[index : ].splitlines()[0]
		key = s7_decipher(plain, cipher, len(cipher), 1)
		print 'key is: ', key

		index = recv.find('c1 = ')+5
		sub = recv[index : ].splitlines()[0]
		ans = s7_decipher(plain, sub, key, key)
		print ans
		s.sendall(ans+'\n')
	elif cnt == 8:
		#print recv
		if not re.search('MD5', recv): continue
		index = recv.find('MD5(m) = ')+9
		sub = recv[index : ].splitlines()[0]
		print sub
		done = ''
		s8_dfs('', 0, sub)
		print done
		s.sendall(done+'\n')
	elif re.search('Wrong', recv): break

#https://csie.ctf.tw/files/BdbRwurcWgC4VkqHlFjGMuLn0ZJV0NIYn0qwMqfxDvP2fiWm9GfvfA2bJy3rXHqxruZgvIBsTmgmadrAIaLXRWR0wguMhBQggYjejBOp7i7eEVhv.png
#FLAG{Cryp70_c4n_h3lp_y0u_f1nd_th3_7re45ur3!}
