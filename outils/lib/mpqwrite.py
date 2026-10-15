import struct,sys
from .mpq import h, T
def enc(data,key):
    out=[]; s2=0xEEEEEEEE
    for (v,) in struct.iter_unpack('<I',data):
        s2=(s2+T[0x400+(key&0xFF)])&0xFFFFFFFF
        c=v^((key+s2)&0xFFFFFFFF)
        key=((((~key)<<0x15)+0x11111111)|(key>>0x0B))&0xFFFFFFFF
        s2=(v+s2+(s2<<5)+3)&0xFFFFFFFF; out.append(c)
    return struct.pack('<%dI'%len(out),*out)
import zlib
def write_z(path,files,ss_shift=3):
    ss=512<<ss_shift
    files=dict(files); files['(listfile)']='\r\n'.join(k for k in files).encode()+b'\r\n'
    names=list(files); hn=16
    while hn<len(names)*2: hn*=2
    chunks=[]; blocks=[]; pos=32
    for n in names:
        d=files[n]; ns=(len(d)+ss-1)//ss
        secs=[]
        for k in range(ns):
            raw=d[k*ss:(k+1)*ss]; c=b'\x02'+zlib.compress(raw,9)
            secs.append(c if len(c)<len(raw) else raw)
        offs=[(ns+1)*4]
        for s in secs: offs.append(offs[-1]+len(s))
        blob=struct.pack('<%dI'%(ns+1),*offs)+b''.join(secs)
        blocks.append((pos,len(blob),len(d),0x80000000|0x200)); chunks.append(blob); pos+=len(blob)
    ht=[(0xFFFFFFFF,0xFFFFFFFF,0xFFFF,0xFFFF,0xFFFFFFFF)]*hn
    for i,n in enumerate(names):
        j=h(n,0)%hn
        while ht[j][4]!=0xFFFFFFFF: j=(j+1)%hn
        ht[j]=(h(n,1),h(n,2),0,0,i)
    htb=enc(b''.join(struct.pack('<IIHHI',*e) for e in ht),h('(hash table)',3))
    btb=enc(b''.join(struct.pack('<IIII',*b) for b in blocks),h('(block table)',3))
    hpos=pos; bpos=hpos+len(htb)
    hdr=b'MPQ\x1a'+struct.pack('<IIHHIIII',32,bpos+len(btb),0,ss_shift,hpos,bpos,hn,len(blocks))
    with open(path,'wb') as f:
        f.write(hdr); [f.write(c) for c in chunks]; f.write(htb); f.write(btb)
