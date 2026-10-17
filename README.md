# Ascension FR

**Traduction française de Conquest of Azeroth / Ascension (WoW 3.3.5a) — bilingue : le même client joue en anglais ou en français.**

Vous changez une seule ligne de `WTF\Config.wtf` pour passer d'une langue à l'autre :

```
SET locale "frFR"     ← français
SET locale "enUS"     ← anglais d'origine
```

> Projet de fans. Non affilié à Blizzard Entertainment ni à Project Ascension. Ce dépôt ne contient **aucun fichier du jeu** : les outils lisent votre propre client.

## Comment ça marche

Le patch `patch-T.MPQ` **ajoute** le français à côté de l'anglais ; il ne remplace jamais l'anglais d'origine. Un client `enUS` lit l'anglais, un client `frFR` lit le français. Pour le serveur, le pack SQL ajoute des lignes `frFR` dans les tables `*_locale` sans toucher aux tables anglaises ni à une traduction frFR déjà présente. Détails techniques : [`docs/FONCTIONNEMENT_BILINGUE.md`](docs/FONCTIONNEMENT_BILINGUE.md).

| Partie | Ce qu'elle contient | Où la trouver |
|---|---|---|
| **Patch client** `patch-T_v37.MPQ` | Interface (96 fichiers Lua), 78 tables de textes du client (sorts, objets, zones, succès, chaînes globales…) | [Releases](../../releases) |
| **Pack SQL** `SQL_Ascension_FR_v3.zip` | PNJ, quêtes, objets, dialogues, phrases de PNJ, livres, objets du monde : 165 547 textes, 11 tables | [Releases](../../releases) |
| **Outils** `outils/` | Reconstruire la partie sorts, trouver ce qui reste en anglais, vérifier | ce dépôt |
| **Données** `donnees/` | 325 455 textes de sorts, glossaire, termes de référence | ce dépôt |

## Installer (joueur)

1. Téléchargez les fichiers de la dernière [Release](../../releases).
2. Fermez le jeu et le lanceur. Dans `Data\`, renommez votre `patch-T.MPQ` en `patch-T.MPQ.orig` (sauvegarde), puis copiez `patch-T_v37.MPQ` **renommé en `patch-T.MPQ`**.
3. Videz le dossier `Cache`. Dans `WTF\Config.wtf`, mettez `SET locale "frFR"`.
4. Lancez le jeu.

Pas à pas, retour arrière et dépannage : [`docs/INSTALLATION.md`](docs/INSTALLATION.md).

## Installer (serveur)

Arrêtez le worldserver, faites un dump de `acore_world`, puis suivez `LISTE_INSTALLATION.md` dans `SQL_Ascension_FR_v3.zip` (ou lancez `installer.bat` / `installer.sh`). Voir [`sql/LISEZMOI.md`](sql/LISEZMOI.md).

## Limites connues

Le projet est en bêta. Les principales : 7 fichiers d'interface XML restent en anglais en français, les textes écrits en dur dans l'interface d'Ascension ou envoyés par le serveur hors de la base restent en anglais, et le pack SQL n'a pas été testé sur MySQL 8. Liste complète : [`docs/LIMITES_CONNUES.md`](docs/LIMITES_CONNUES.md).

## Reprendre / continuer le projet (développeur)

Prérequis : Python 3.9+, aucune bibliothèque externe.

```bash
cd outils
python ascension_fr.py manquants  --data "C:/Jeux/Ascension/Data" --sortie manquants.tsv   # sorts encore en anglais
python ascension_fr.py verifier   --data "C:/Jeux/Ascension/Data"                          # jetons ($s1, |cff…|r…) cassés ?
python ascension_fr.py construire --data "C:/Jeux/Ascension/Data" --sortie patch-T.MPQ     # patch sorts, bilingue
python ascension_fr.py controle   --data "C:/Jeux/Ascension/Data" --patch patch-T.MPQ      # l'anglais est-il intact ?
```

`construire` fabrique la partie **sorts** (`Spell.dbc`) à partir de `donnees/sorts_fr.tsv.gz`. Le patch complet de la Release contient en plus l'interface et les autres tables. Flux de travail : [`docs/REPRENDRE_LE_PROJET.md`](docs/REPRENDRE_LE_PROJET.md).

## Avancement

- [x] Sorts, objets, zones, succès, chaînes globales du client (bilingue enUS / frFR)
- [x] Interface Lua (96 fichiers, texte français seulement en frFR)
- [x] PNJ, quêtes, récompenses, objets, dialogues, phrases de PNJ, livres (SQL, tables `*_locale`)
- [ ] Interface XML (7 fichiers), textes en dur restants
- [ ] Relecture complète en jeu, harmonisation de quelques termes (voir limites)

## Contribuer

Voir [`CONTRIBUTING.md`](CONTRIBUTING.md). Une correction = une ligne dans `donnees/`, une Pull Request. Historique des versions : [`CHANGELOG.md`](CHANGELOG.md).

## Crédits

LePetitDan (addon de traduction, utilisé comme référence), Blizzard Entertainment (textes d'origine), Project Ascension, communauté AzerothCore.

Licence MIT pour les outils et les textes français (voir `LICENSE`). Les textes d'origine restent la propriété de leurs ayants droit.

---

### English summary
French localisation of *Conquest of Azeroth* (WoW 3.3.5a), **bilingual**: one client plays in English or French by switching `SET locale "enUS"` / `"frFR"` in `WTF\Config.wtf`. The client patch adds French next to the original English instead of overwriting it; the SQL pack inserts `frFR` rows into the `*_locale` tables and never touches the English base tables or existing frFR rows. This repository holds the Python tools (rebuild the spell part, list untranslated spell strings, validate formatting tokens) and the translation data; the patch and SQL pack are published in Releases. No game files included.
