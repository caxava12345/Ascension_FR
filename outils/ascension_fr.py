#!/usr/bin/env python3
"""Ascension FR - outils de traduction du Spell.dbc (client WoW 3.3.5 / Conquest of Azeroth).

Commandes :
  python ascension_fr.py construire --data "C:/.../Data" --sortie patch-T.MPQ
  python ascension_fr.py manquants  --data "C:/.../Data" --sortie manquants.tsv
  python ascension_fr.py verifier   --data "C:/.../Data"

Le client reste en enUS : le francais est ecrit dans les emplacements anglais du Spell.dbc.
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


RANGS_FR = {'Passive':'Passif','Spec Passive':'Passif de spécialisation','Specialization':'Spécialisation','Trigger':'Déclencheur','trigger':'Déclencheur','trigger2':'Déclencheur 2', 'Proc':'Déclenchement','proc':'Déclenchement','Proc 2':'Déclenchement 2','Proc2':'Déclenchement 2','Hidden':'Caché','hidden':'Caché','Deprecated':'Obsolète','DEPRECATED':'OBSOLÈTE', 'Aura':'Aura','aura':'Aura','Aura1':'Aura 1','Aura2':'Aura 2','Buff':'Amélioration','Debuff':'Affaiblissement','Damage':'Dégâts','Heal':'Soins','Healing':'Soins', 'Periodic':'Périodique','Periodic Heal':'Soins périodiques','Shield':'Bouclier','Stun':'Étourdissement','Slow':'Ralentissement','Root':'Enracinement','Sleep':'Sommeil', 'Dispel':'Dissipation','Knockback':'Repoussement','Transform':'Transformation','Visual':'Visuel','Effect':'Effet','Enemy':'Ennemi','Ally':'Allié','Allies':'Alliés', 'Caster':'Lanceur','Refresh':'Rafraîchissement','Resource':'Ressource','Restore':'Restauration','Absorb':'Absorption','Stacks':'Cumuls','Incapacitate':'Incapacitation', 'Passive Pet':'Passif du familier','Passive PVP':'Passif JcJ','Selfcast':'Lancement sur soi','Linked':'Lié','UNUSED':'INUTILISÉ','Delayer':'Retardateur', 'Enemy Trigger':'Déclencheur ennemi','Ally Trigger':'Déclencheur allié','Target Trigger':'Déclencheur de cible','Delay Trigger':'Déclencheur différé','Applier':'Applicateur', 'Area Slow':'Ralentissement de zone','Crit Bonus':'Bonus critique','Healing Reduction':'Réduction des soins','Damage/Movement':'Dégâts/Déplacement','Root & Haste':'Enracinement et hâte', 'Giga Heal':'Soins géants','Blocker':'Bloqueur','Stacker':'Cumulateur','Duration Increaser':'Augmentation de durée','Energize Self':'Énergisation de soi','Generate Ember':'Génération de braise', 'Incarnation':'Incarnation','Trinket':'Bijou','Mana Burn':'Brûlure de mana','Soar':'Envol','Missile Visual':'Visuel de projectile','Radial Expander':'Expanseur radial','Charge Back Down':'Recharge à la baisse', 'Heat Out of Combat Only':'Chaleur hors combat uniquement','ICD':'Délai interne','ICD tracker':'Suivi du délai interne','Selfcast Check':'Vérification du lancement sur soi','Forcecast':'Lancement forcé','Hidden Overheat Bonus':'Bonus de surchauffe caché','DoT':'Dégâts sur la durée', }
RANGS_FR.update({'Heroic': 'Héroïque', 'Mythic': 'Mythique', 'Challenge': 'Défi'})


def rang_fr(en):
    """Traduction automatique des rangs courants ('Rank 3' -> 'Rang 3')."""
    m = re.fullmatch(r'Rank (\d+)', en)
    return ('Rang ' + m[1]) if m else RANGS_FR.get(en)


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
    """Choisit le MPQ qui contient le Spell.dbc anglais le plus complet (le plus de sorts)."""
    if force:
        return force
    meilleur = (0, None)
    for f in glob.glob(os.path.join(data, '**', '*.MPQ'), recursive=True) + glob.glob(os.path.join(data, '**', '*.mpq'), recursive=True):
        nom = os.path.basename(f).lower()
        if nom == 'patch-t.mpq' or os.sep + 'frfr' + os.sep in f.lower():
            continue  # on ne relit ni notre propre patch ni la locale francaise
        try:
            m = MPQ(f)
            bi = m.find(SPELL)
            if bi is None:
                continue
            d = m.read(SPELL, bi)
            n = struct.unpack_from('<I', d, 4)[0]
            if n > meilleur[0]:
                meilleur = (n, f)
        except Exception as e:
            print('  ignore', f, e, file=sys.stderr)
    if not meilleur[1]:
        sys.exit('Aucun Spell.dbc trouve dans ' + data)
    print(f'Source : {meilleur[1]} ({meilleur[0]} sorts)')
    return meilleur[1]


def charger_dbc(args):
    src = trouver_source(args.data, args.source)
    return DBC(MPQ(src).read(SPELL))


def texte_en(d, r, f):
    """Texte anglais d'un champ : l'emplacement f+2 (miroir) en priorite, sinon f."""
    return d.sz(d.u(r, f + 2)) or d.sz(d.u(r, f))


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
            t = tr[champ].get(sid) or (rang_fr(en) if champ == 'Rank' else None)
            if t and t != en:
                p = ajouter(t)
                for g in (f, f + 2):  # emplacement enUS + son miroir
                    struct.pack_into('<I', rec, r * d.rs + g * 4, p)
                modifs += 1
    dbc = b'WDBC' + struct.pack('<IIII', d.n, d.nf, d.rs, len(strs)) + bytes(rec) + bytes(strs)
    write_z(args.sortie, {SPELL: dbc}, ss_shift=7)
    print(f'{modifs} textes remplaces -> {args.sortie} ({os.path.getsize(args.sortie)//1024//1024} Mo)')
    print('Copiez-le dans Data/, videz le dossier Cache, gardez la locale enUS.')


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
    p.add_argument('commande', choices=['construire', 'manquants', 'verifier'])
    p.add_argument('--data', required=True, help='dossier Data du client')
    p.add_argument('--source', help='forcer le MPQ contenant le Spell.dbc anglais')
    p.add_argument('--sortie', default=None)
    a = p.parse_args()
    a.sortie = a.sortie or {'construire': 'patch-T.MPQ', 'manquants': 'manquants.tsv'}.get(a.commande)
    {'construire': construire, 'manquants': manquants, 'verifier': verifier}[a.commande](a)


if __name__ == '__main__':
    main()
