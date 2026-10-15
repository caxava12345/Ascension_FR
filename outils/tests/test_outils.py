import os, sys, tempfile, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from lib.mpq import MPQ
from lib.mpqwrite import write_z
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


if __name__ == '__main__':
    unittest.main()
