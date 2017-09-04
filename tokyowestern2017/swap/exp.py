#!/usr/bin/env python2

from pwn import *

def delay(s=''):
	sleep(0.1)

r = remote('127.0.0.1', 7122)

r.sendline()
