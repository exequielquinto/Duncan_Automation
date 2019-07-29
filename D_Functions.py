import struct

def float32_to_bin(num):
    return bin(struct.unpack('!I', struct.pack('!f', num))[0])[2:].zfill(32)

def bin_to_float32(binary):
    return struct.unpack('!f',struct.pack('!I', int(binary, 2)))[0]

def dec_to_bin(msb,lsb):
    x=bin(int(msb))
    y=bin(int(lsb))
    return str(x)[2:18].zfill(16)+str(y)[2:18].zfill(16)

def dec_to_float32(msb,lsb):
    return bin_to_float32(dec_to_bin(msb, lsb))

def float32_to_msb(num):
    return int(float32_to_bin(num)[0:16],2)

def float32_to_lsb(num):
    return int(float32_to_bin(num)[16:32],2)
