# Reprendre le projet

## 1. Comprendre le principe
- Le client reste **enUS**. `Spell.dbc` contient chaque texte de sort dans plusieurs emplacements (Nom, Rang, Description, Infobulle) ; le français est écrit dans l'emplacement anglais **et** son miroir (+2).
- Le script lit le `Spell.dbc` anglais de **votre** client (il choisit le MPQ qui en contient le plus de sorts ; `--source` pour imposer un MPQ), applique `donnees/sorts_fr.tsv.gz` et écrit un `patch-T.MPQ` qui ne contient que le `Spell.dbc` modifié.
- Les rangs courants (`Rank 3`, `Passive`…) sont traduits automatiquement (`Rang 3`, `Passif`).

## 2. Boucle de travail
1. `python ascension_fr.py manquants --data <Data>` → `manquants.tsv` : `spell_id`, `champ`, `texte_en`. Triez/filtrez (par ID, par mot-clé de classe) et prenez un lot.
2. Traduisez en suivant [`GUIDE_STYLE.md`](GUIDE_STYLE.md) et `donnees/glossaire.tsv` / `termes_noyau.tsv`.
3. Ajoutez vos lignes au fichier de données (format : [`FORMAT_DES_DONNEES.md`](FORMAT_DES_DONNEES.md)).
4. `python ascension_fr.py verifier --data <Data>` : liste les textes dont les jetons diffèrent de l'anglais. À relire à la main (certains cas sont légitimes).
5. `python ascension_fr.py construire …`, copiez le patch dans `Data\`, videz `Cache`, vérifiez en jeu.

## 3. Pièges connus
- **Jetons** à conserver : `$s1`, `${…}`, `$?s123[..][..]`, `|cFFRRGGBB…|r`, `$B`, `$g..:..;`, `$l..:..;`, `\r\n`.
- Les noms de sorts cités dans une description doivent être identiques au nom FR du sort.
- Le patch publié a été construit sur le client du mainteneur ; une construction sur un autre client peut différer sur quelques centaines de textes (rangs ou infobulles absents de votre `Spell.dbc` source). Rien de bloquant.
- Pour le serveur : la table `coa_client_spell_description` remplace certaines descriptions de sorts côté client ; ses traductions sont dans le SQL des Releases.

## 4. Idées de contributions
Sorts techniques/PNJ, unification typographique (apostrophes, espaces avant `:;!?`), relecture des sorts Pyromancien, textes SQL restants.
