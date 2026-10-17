# Reprendre le projet

## 1. Comprendre le principe
- Le client est **bilingue** : l'anglais reste dans l'emplacement enUS ; le français est écrit dans les emplacements frFR (2 et 3). Voir [`FONCTIONNEMENT_BILINGUE.md`](FONCTIONNEMENT_BILINGUE.md).
- Le script lit le `Spell.dbc` anglais de **votre** client (`patch-T.MPQ` de `Data\` ; `--source` pour imposer un autre MPQ), applique `donnees/sorts_fr.tsv.gz` et écrit un `patch-T.MPQ` qui ne contient que le `Spell.dbc` modifié. Les sorts sans traduction reçoivent l'anglais dans les emplacements frFR.
- Le patch complet de la Release contient en plus l'interface Lua et 77 autres tables ; ce dépôt reconstruit la partie sorts et sert de base de données de traduction.

## 2. Boucle de travail
1. `python ascension_fr.py manquants --data <Data>` -> `manquants.tsv` : `spell_id`, `champ`, `texte_en`. Triez/filtrez (par ID, par mot-clé de classe) et prenez un lot.
2. Traduisez en suivant [`GUIDE_STYLE.md`](GUIDE_STYLE.md) et `donnees/glossaire.tsv` / `termes_noyau.tsv`.
3. Ajoutez vos lignes au fichier de données (format : [`FORMAT_DES_DONNEES.md`](FORMAT_DES_DONNEES.md)).
4. `python ascension_fr.py verifier --data <Data>` : liste les textes dont les jetons diffèrent de l'anglais. À relire à la main (certains cas sont légitimes).
5. `python ascension_fr.py construire --data <Data> --sortie patch-T.MPQ`, puis `python ascension_fr.py controle --data <Data> --patch patch-T.MPQ` (l'anglais doit rester intact), copiez le patch dans `Data\`, videz `Cache`, testez en `frFR` **et** en `enUS`.

## 3. Pièges connus
- **Jetons** à conserver : `$s1`, `${...}`, `$?s123[..][..]`, `|cFFRRGGBB...|r`, `$B`, `$g..:..;`, `$l..:..;`, `\r\n`.
- Les noms de sorts cités dans une description doivent être identiques au nom FR du sort.
- Partez du `patch-T.MPQ` **d'origine** du paquet CoA (sorts propres au serveur). Le `Spell.dbc` de `area-52/patch-D.MPQ` est celui du client Ascension : plus gros, mais il ne correspond pas au serveur CoA.
- Ne jamais écrire dans l'emplacement enUS (le premier de chaque groupe) : c'est l'anglais d'origine. `controle` le vérifie.
- Certaines traductions héritées contiennent des erreurs (texte d'un autre sort, jetons modifiés) : voir `docs/LIMITES_CONNUES.md`.
- Pour le serveur : la table `coa_client_spell_description` remplace certaines descriptions de sorts côté client ; elle n'a pas de variante `_locale` (voir le dossier optionnel du pack SQL).

## 4. Idées de contributions
Les 7 fichiers XML, harmonisation des termes laissés en anglais, unification typographique (apostrophes, espaces avant `:;!?`), relecture des sorts Pyromancien, textes en dur de l'interface.
