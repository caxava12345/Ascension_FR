import argparse, os, struct, sys, tempfile, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from lib.mpq import MPQ
from lib.mpqwrite import write_z
from lib.dbc import DBC
import ascension_fr as a


class Tests(unittest.TestCase):
    def test_mpq_aller_retour(self):
        d = tempfile.mkdtemp(); p = os.path.join(d, 'x.MPQ'); data = b'Bonjour' * 5000
        write_z(p, {'DBFilesClient\\Test.dbc': data}, ss_shift=3)
        self.assertEqual(MPQ(p).read('DBFilesClient\\Test.dbc'), data)

    def test_donnees(self):
        tr = a.lire_traductions()
        self.assertGreater(len(tr['Description']), 1000)

    def test_jetons(self):
        self.assertEqual(a.JETONS.findall('$s1 |cff00ff00x|r ${$m1*2}'), ['$s1', '|cff00ff00', '|r', '${$m1*2}'])

    def test_bilingue(self):
        # 2 sorts factices : #1 traduit, #2 non traduit. L'anglais (emplacement 136) ne doit pas bouger,
        # les emplacements frFR (138 et 139) doivent contenir le francais, ou l'anglais a defaut.
        nf, rs = 234, 936
        chaines = b'\0Bolt\0Fire\0'
        recs = bytearray(2 * rs)
        for r, (sid, off) in enumerate([(1, 1), (2, 6)]):
            struct.pack_into('<II', recs, r * rs, sid, 0)
            struct.pack_into('<I', recs, r * rs + 136 * 4, off)
        dbc = b'WDBC' + struct.pack('<IIII', 2, nf, rs, len(chaines)) + bytes(recs) + chaines
        d = tempfile.mkdtemp(); src, out = os.path.join(d, 'src.MPQ'), os.path.join(d, 'out.MPQ')
        write_z(src, {a.SPELL: dbc}, ss_shift=3)
        vide = {c: {} for c in a.CHAMPS}; vide['Name'] = {1: '\u00c9clair'}
        avant, a.lire_traductions = a.lire_traductions, lambda: vide
        try:
            a.construire(argparse.Namespace(data=d, source=src, sortie=out))
        finally:
            a.lire_traductions = avant
        n = DBC(MPQ(out).read(a.SPELL))
        lire = lambda r, f: n.sz(n.u(r, f))
        self.assertEqual([lire(0, 136), lire(1, 136)], ['Bolt', 'Fire'])
        self.assertEqual([lire(0, 138), lire(0, 139)], ['\u00c9clair'] * 2)
        self.assertEqual([lire(1, 138), lire(1, 139)], ['Fire'] * 2)


if __name__ == '__main__':
    unittest.main()
