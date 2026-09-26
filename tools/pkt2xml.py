"""
pkt2xml.py - Decode Cisco Packet Tracer .pkt/.pka files (PT 7.x - 9.x) to XML.
Usage: python pkt2xml.py input.pkt [output.xml]
Algorithm (as documented by the pka2xml project):
  1. reverse the bytes, XOR each byte i with (len - i*len)
  2. Twofish-EAX decrypt (key = 0x89*16, nonce = 0x10*16)
  3. XOR each byte i with (len - i)
  4. skip 4-byte big-endian length header, zlib-decompress
"""
import sys, zlib, struct
from twofish import Twofish

BLOCK = 16

def _xor_blocks(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def _dbl(b):
    n = int.from_bytes(b, 'big') << 1
    if b[0] & 0x80:
        n ^= 0x87
    return (n & ((1 << 128) - 1)).to_bytes(16, 'big')

def _omac(tf, tag, data):
    # OMAC1 / CMAC with tweak byte 'tag' prepended (EAX construction)
    L = tf.encrypt(b'\x00' * 16)
    K1 = _dbl(L); K2 = _dbl(K1)
    m = (b'\x00' * 15) + bytes([tag]) + data
    if len(m) % 16 == 0:
        blocks = [m[i:i+16] for i in range(0, len(m), 16)]
        blocks[-1] = _xor_blocks(blocks[-1], K1)
    else:
        pad = m + b'\x80' + b'\x00' * (15 - len(m) % 16)
        blocks = [pad[i:i+16] for i in range(0, len(pad), 16)]
        blocks[-1] = _xor_blocks(blocks[-1], K2)
    x = b'\x00' * 16
    for blk in blocks:
        x = tf.encrypt(_xor_blocks(x, blk))
    return x

def _ctr(tf, nonce_tag, data):
    out = bytearray()
    ctr = int.from_bytes(nonce_tag, 'big')
    for i in range(0, len(data), 16):
        ks = tf.encrypt((ctr & ((1 << 128) - 1)).to_bytes(16, 'big'))
        chunk = data[i:i+16]
        out += _xor_blocks(chunk, ks[:len(chunk)])
        ctr += 1
    return bytes(out)

def decrypt(data: bytes) -> bytes:
    n = len(data)
    s1 = bytes(data[n - 1 - i] ^ ((n - i * n) & 0xFF) for i in range(n))
    tf = Twofish(b'\x89' * 16)
    nonce_tag = _omac(tf, 0, b'\x10' * 16)
    body, tag = s1[:-16], s1[-16:]          # EAX appends a 16-byte tag
    s2 = _ctr(tf, nonce_tag, body)
    m = len(s2)
    s3 = bytes(s2[i] ^ ((m - i) & 0xFF) for i in range(m))
    (ulen,) = struct.unpack('>I', s3[:4])
    xml = zlib.decompress(s3[4:])
    return xml

if __name__ == '__main__':
    src = sys.argv[1]
    dst = sys.argv[2] if len(sys.argv) > 2 else src.rsplit('.', 1)[0] + '.xml'
    with open(src, 'rb') as f:
        raw = f.read()
    xml = decrypt(raw)
    with open(dst, 'wb') as f:
        f.write(xml)
    print(f'OK {src} -> {dst} ({len(xml)} bytes)')
