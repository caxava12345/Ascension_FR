#!/usr/bin/env python3
"""Ascension FR - outils de traduction du Spell.dbc (client WoW 3.3.5 / Conquest of Azeroth).

Commandes :
  python ascension_fr.py construire --data "C:/.../Data" --sortie patch-T.MPQ
  python ascension_fr.py manquants  --data "C:/.../Data" --sortie manquants.tsv
  python ascension_fr.py verifier   --data "C:/.../Data"
  python ascension_fr.py controle   --data "C:/.../Data" --patch patch-T.MPQ

Mode bilingue : l'anglais d'origine reste dans l'emplacement enUS du Spell.dbc ; le francais est
ajoute dans les emplacements frFR (2 et 3). Le client affiche l'anglais en enUS, le francais en frFR.
Aucun fichier du jeu n'est fourni : le script lit VOTRE client.
"""
import argparse, glob, gzip, os, re, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib.mpq import MPQ
from lib.mpqwrite import write_z
from lib.dbc import DBC

SPELL = 'DBFilesClient\\Spell.dbc'
CHAMPS = {'Name': 136, 'Rank': 153, 'Description': 170, 'Tooltip': 187}  # index du champ (emplacement enUS)
DONNEES = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'donnees', 'sorts_fr.tsv.gz')
# Jetons du moteur de texte WoW qui doivent rester identiques entre EN et FR.
JETONS = re.compile(r'\$\{[^}]*\}|\$\?[a-z]*\d*|\$[a-zA-Z]+\d*|\|c[0-9a-fA-F]{8}|\|r')


def lire_traductions(chemin=DONNEES):
    """-> {champ: {spell_id: texte_fr}}"""
    out = {c: {} for c in CHAMPS}
    with gzip.open(chemin, 'rt', encoding='utf8', newline='') as f:
        next(f)
        for ligne in f:
            i, champ, txt = ligne.rstrip('\n').split('\t', 2)
            out[champ][int(i)] = txt.replace('\\r', '\r').replace('\\n', '\n')
    return out


def trouver_source(data, force=None):
    """MPQ contenant le Spell.dbc de reference : le patch-T.MPQ du client Conquest of Azeroth.

    C'est le fichier que le jeu charge en dernier pour les sorts (patch-T passe apres les
    patchs de royaume comme area-52/patch-D.MPQ) et celui que fournit le paquet client CoA.
    Utilisez --source pour imposer un autre MPQ.
    """
    if force:
        return force
    p = os.path.join(data, 'patch-T.MPQ')
    if not os.path.exists(p):
        sys.exit('patch-T.MPQ introuvable dans ' + data + ' (utilisez --source)')
    if MPQ(p).find(SPELL) is None:
        sys.exit('Pas de Spell.dbc dans ' + p + ' (utilisez --source)')
    print('Source :', p)
    return p


def charger_dbc(args):
    src = trouver_source(args.data, args.source)
    return DBC(MPQ(src).read(SPELL))


def texte_en(d, r, f):
    """Texte anglais d'un champ : toujours l'emplacement enUS (f), jamais modifie par le patch."""
    return d.sz(d.u(r, f))


def construire(args):
    d = charger_dbc(args)
    tr = lire_traductions()
    rec = bytearray(d.rec)
    strs = bytearray(d.str)
    cache, modifs = {}, 0

    def ajouter(s):
        if s not in cache:
            cache[s] = len(strs)
            strs.extend(s.encode('utf-8') + b'\0')
        return cache[s]

    for r in range(d.n):
        sid = d.u(r, 0)
        for champ, f in CHAMPS.items():
            en = texte_en(d, r, f)
            t = tr[champ].get(sid)
            if t and t != en:
                p = ajouter(t)
                modifs += 1
            else:
                p = d.u(r, f)  # pas de traduction : le client frFR affiche l'anglais plutot qu'un vide
            for g in (f + 2, f + 3):  # emplacements frFR ; l'emplacement enUS (f) n'est jamais touche
                struct.pack_into('<I', rec, r * d.rs + g * 4, p)
    dbc = b'WDBC' + struct.pack('<IIII', d.n, d.nf, d.rs, len(strs)) + bytes(rec) + bytes(strs)
    write_z(args.sortie, {SPELL: dbc}, ss_shift=7)
    print(f'{modifs} textes francais ajoutes -> {args.sortie} ({os.path.getsize(args.sortie)//1024//1024} Mo)')
    print('Copiez-le dans Data/, videz le dossier Cache. Langue : SET locale "frFR" ou "enUS" dans WTF/Config.wtf.')


def controle(args):
    """Verifie qu'un patch ne change pas l'anglais et remplit bien les emplacements frFR."""
    o, p = charger_dbc(args), DBC(MPQ(args.patch).read(SPELL))
    if (o.n, o.rs) != (p.n, p.rs):
        sys.exit('Le patch n a pas la meme structure que la source.')
    anglais, vides, ecarts = 0, 0, 0
    for r in range(o.n):
        for f in CHAMPS.values():
            en = o.sz(o.u(r, f))
            if p.sz(p.u(r, f)) != en:
                anglais += 1
            fr2, fr3 = p.sz(p.u(r, f + 2)), p.sz(p.u(r, f + 3))
            vides += bool(en) and not fr2
            ecarts += fr2 != fr3
    print(f'anglais modifie : {anglais} | frFR vide alors que l anglais existe : {vides} | emplacements 2 et 3 differents : {ecarts}')
    ok = anglais == vides == ecarts == 0
    print('OK' if ok else 'A VERIFIER')
    sys.exit(0 if ok else 1)


def a_traduire(t):
    return bool(t) and re.search(r'[A-Za-z]{3}', re.sub(r'\$\{[^}]*\}|\$\??[a-zA-Z]*\d*|\|c[0-9a-fA-F]{8}|\|r|\[|\]', '', t))


def manquants(args):
    d = charger_dbc(args)
    tr = lire_traductions()
    n = 0
    with open(args.sortie, 'w', encoding='utf8', newline='\n') as out:
        out.write('spell_id\tchamp\ttexte_en\n')
        for r in range(d.n):
            sid = d.u(r, 0)
            for champ, f in CHAMPS.items():
                en = texte_en(d, r, f)
                if a_traduire(en) and sid not in tr[champ]:
                    out.write(f"{sid}\t{champ}\t{en.replace(chr(13),chr(92)+'r').replace(chr(10),chr(92)+'n').replace(chr(9),' ')}\n")
                    n += 1
    print(f'{n} textes sans traduction -> {args.sortie}')


def verifier(args):
    d = charger_dbc(args)
    tr = lire_traductions()
    mauvais = 0
    for r in range(d.n):
        sid = d.u(r, 0)
        for champ, f in CHAMPS.items():
            fr = tr[champ].get(sid)
            if not fr:
                continue
            en = texte_en(d, r, f)
            # $g..;/$l..; : les mots changent selon la langue, on les ignore
            norm = lambda x: sorted(JETONS.findall(re.sub(r'\$[lLgG][^;$]*;', '', x)))
            if norm(en) != norm(fr) and en != fr:
                mauvais += 1
                print(f'{sid}\t{champ}\tjetons differents')
    print(f'{mauvais} textes avec jetons differents (a relire)')


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('commande', choices=['construire', 'manquants', 'verifier', 'controle'])
    p.add_argument('--data', required=True, help='dossier Data du client')
    p.add_argument('--source', help='forcer le MPQ contenant le Spell.dbc anglais')
    p.add_argument('--sortie', default=None)
    p.add_argument('--patch', help='controle : le patch-T a verifier')
    a = p.parse_args()
    a.sortie = a.sortie or {'construire': 'patch-T.MPQ', 'manquants': 'manquants.tsv'}.get(a.commande)
    {'construire': construire, 'manquants': manquants, 'verifier': verifier, 'controle': controle}[a.commande](a)


if __name__ == '__main__':
    main()
