from pwn import *
import sys

# grab the cyclic from argv[1]
provided_cyclic = int(sys.argv[1], base=16)
print(f'Checking provided cyclic: {provided_cyclic}')

# Find the offset of the value in the cyclic pattern
offset = cyclic_find(p64(provided_cyclic))  # Use p32 or p64 depending on the architecture

print(f"The offset of the value is: {offset}")
