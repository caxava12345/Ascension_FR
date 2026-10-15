import struct, zlib, bz2
def _table():
    t=[0]*0x500; seed=0x00100001
    for i in range(0x100):
        idx=i
        for _ in range(5):
            seed=(seed*125+3)%0x2AAAAB; a=(seed&0xFFFF)<<16
            seed=(seed*125+3)%0x2AAAAB; t[idx]=a|(seed&0xFFFF); idx+=0x100
    return t
T=_table()
def h(s,typ):
    s1,s2=0x7FED7FED,0xEEEEEEEE
    for c in s.upper().replace('/','\\'):
        c=ord(c); s1=(T[(typ<<8)+c]^(s1+s2))&0xFFFFFFFF; s2=(c+s1+s2+(s2<<5)+3)&0xFFFFFFFF
    return s1
def dec(data,key):
    out=[]; s2=0xEEEEEEEE
    for (v,) in struct.iter_unpack('<I',data[:len(data)//4*4]):
        s2=(s2+T[0x400+(key&0xFF)])&0xFFFFFFFF
        v^=(key+s2)&0xFFFFFFFF
        key=((((~key)<<0x15)+0x11111111)|(key>>0x0B))&0xFFFFFFFF
        s2=(v+s2+(s2<<5)+3)&0xFFFFFFFF; out.append(v)
    return struct.pack('<%dI'%len(out),*out)
class MPQ:
    def __init__(s,path):
        s.f=open(path,'rb'); d=s.f.read(64)
        assert d[:4]==b'MPQ\x1a', d[:4]
        hs,arc,fv,bs,ht,bt,hn,bn=struct.unpack_from('<IIHHIIII',d,4)
        s.ssize=512<<bs; hi_ht=hi_bt=0
        if fv>=1:
            _,hi_ht,hi_bt=struct.unpack_from('<QHH',d,32)
        s.f.seek(ht|(hi_ht<<32)); s.hash=dec(s.f.read(hn*16),h('(hash table)',3))
        s.f.seek(bt|(hi_bt<<32)); s.block=dec(s.f.read(bn*16),h('(block table)',3))
        s.hn=hn
    def find(s,name):
        a,b,i0=h(name,1),h(name,2),h(name,0)%s.hn; i=i0
        while True:
            ha,hb,loc,plat,bi=struct.unpack_from('<IIHHI',s.hash,i*16)
            if bi==0xFFFFFFFF: return None
            if ha==a and hb==b and bi!=0xFFFFFFFE: return bi
            i=(i+1)%s.hn
            if i==i0: return None
    def finds(s,name):
        a,b=h(name,1),h(name,2); r=[]
        for i in range(s.hn):
            ha,hb,loc,plat,bi=struct.unpack_from('<IIHHI',s.hash,i*16)
            if ha==a and hb==b and bi<0xFFFFFFFE: r.append((loc,bi))
        return r
    def read(s,name,bi=None):
        if bi is None: bi=s.find(name)
        if bi is None: return None
        off,csize,fsize,flags=struct.unpack_from('<IIII',s.block,bi*16)
        if not flags&0x80000000: return None
        s.f.seek(off); raw=s.f.read(csize)
        key=None
        if flags&0x10000:
            key=h(name.split('\\')[-1],3)
            if flags&0x20000: key=((key+off)^fsize)&0xFFFFFFFF
        def unc(blk,size):
            if len(blk)>=size: return blk[:size]
            m=blk[0]; blk=blk[1:]
            if m&0x10: blk=bz2.decompress(blk)
            elif m&0x02: blk=zlib.decompress(blk)
            elif m&0x08: raise Exception('pkware')
            return blk
        if flags&0x01000000:
            return unc(raw,fsize) if flags&0x200 else raw[:fsize]
        if not flags&0x300:
            return raw[:fsize]
        if fsize==0: return b""
        ns=(fsize+s.ssize-1)//s.ssize
        tbl=raw[:(ns+1)*4]
        if key is not None: tbl=dec(tbl,(key-1)&0xFFFFFFFF)
        offs=struct.unpack('<%dI'%(ns+1),tbl); out=[]
        for k in range(ns):
            blk=raw[offs[k]:offs[k+1]]
            if key is not None: blk=dec(blk+b'\0'*((4-len(blk)%4)%4),(key+k)&0xFFFFFFFF)[:offs[k+1]-offs[k]]
            out.append(unc(blk,min(s.ssize,fsize-k*s.ssize)))
        return b''.join(out)
    def listfile(s):
        d=s.read('(listfile)')
        return [] if d is None else [x for x in d.decode('latin-1').replace('\r','').split('\n') if x]
