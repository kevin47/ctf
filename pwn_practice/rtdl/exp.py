#!/usr/bin/env python2

from pwn import *

dynamic_linker = 0x80482a0
buff = 0x8048300
dynstr = 0x80481fc
dynsym = 0x804818c
rel_plt = 0x8048270

