#!/usr/bin/env python2
from pwn import *
from IPython import embed

#p = process('./RNote')
p = remote('127.0.0.1', 7122)

def recv(s):
	print 'waiting', s
	p.recvuntil(s)

def menu():
	recv('choice:')

def add(size, title, content, r=True):
	if r: menu()
	p.sendline('1')
	recv('size:')
	p.sendline(str(size))
	recv('title:')
	if len(title) < 17:
		p.sendline(title)
	else:
		p.send(title)
	recv('content:')
	p.send(content)
	sleep(0.1)

def dele(index, r=True):
	if r: menu()
	p.sendline('2')
	recv('delete:')
	p.sendline(str(index))

def show(index, r=True):
	if r: menu()
	p.sendline('3')
	recv('show:')
	p.sendline(str(index))
	recv('title:')
	title = p.recvline()
	recv('content:')
	content = p.recvline()
	return title, content

def ex(r=True):
	if r: menu()
	p.sendline('4')




