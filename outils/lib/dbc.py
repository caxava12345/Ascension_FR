import struct
class DBC:
    def __init__(s,data):
        assert data[:4]==b'WDBC'
        s.n,s.nf,s.rs,s.ss=struct.unpack_from('<IIII',data,4)
        s.rec=data[20:20+s.n*s.rs]; s.str=data[20+s.n*s.rs:]
    def u(s,r,f): return struct.unpack_from('<I',s.rec,r*s.rs+f*4)[0]
    def sz(s,o):
        e=s.str.index(b'\0',o); return s.str[o:e].decode('utf-8','replace')
