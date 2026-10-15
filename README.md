# Ascension FR

**Traduction française de Conquest of Azeroth / Ascension (WoW 3.3.5a).**
Sorts, quêtes, PNJ, objets : le client reste en `enUS`, le français est écrit dans les emplacements anglais.

> Projet de fans. Non affilié à Blizzard Entertainment ni à Project Ascension. Ce dépôt ne contient **aucun fichier du jeu** : les outils lisent votre propre client.

## Contenu du dépôt

| Dossier | Rôle |
|---|---|
| `outils/` | Script Python `ascension_fr.py` : **construire** le `patch-T.MPQ`, **trouver** ce qui reste à traduire, **vérifier** les traductions |
| `donnees/` | Les traductions (`sorts_fr.tsv.gz`, ~620 000 textes de sorts), le glossaire et les termes de référence |
| `docs/` | Guide de style, format des données, comment reprendre le projet |
| `sql/` | Scripts serveur (livrés dans les *Releases*, voir `sql/LISEZMOI.md`) |

## Installer la traduction (joueur / serveur)

Téléchargez la dernière **Release** (onglet *Releases*), puis :

1. Copiez `patch-T.MPQ` dans `Data\` de votre client, **videz le dossier `Cache`**, gardez la locale **enUS**.
2. Serveur : lancez les scripts SQL de la Release (voir `sql/LISEZMOI.md`).

## Reprendre / continuer le projet (développeur)

Prérequis : Python 3.9+, aucune bibliothèque externe.

```bash
cd outils
python ascension_fr.py manquants  --data "C:/Jeux/Ascension/Data" --sortie manquants.tsv   # ce qui reste en anglais
python ascension_fr.py verifier   --data "C:/Jeux/Ascension/Data"                          # jetons ($s1, |cff…|r…) cassés ?
python ascension_fr.py construire --data "C:/Jeux/Ascension/Data" --sortie patch-T.MPQ     # fabrique le patch
```

Le flux de travail complet est dans [`docs/REPRENDRE_LE_PROJET.md`](docs/REPRENDRE_LE_PROJET.md). Résumé : `manquants` → traduire → ajouter dans `donnees/sorts_fr.tsv.gz` → `verifier` → `construire` → tester en jeu.

## Avancement

- [x] Sorts joueur (1 186), descriptions serveur
- [x] PNJ, quêtes, récompenses, noms d'objets (SQL)
- [ ] Textes divers, phrases de PNJ, descriptions d'objets (SQL)
- [ ] Sorts techniques / PNJ restants, vérification en jeu

Version SQL disponible : **V0.1** (Release).

## Contribuer

Voir [`CONTRIBUTING.md`](CONTRIBUTING.md). Une correction = une ligne dans `donnees/`, une Pull Request.

## Crédits

LePetitDan (addon de traduction, utilisé comme référence), Blizzard Entertainment (textes d'origine), Project Ascension, communauté AzerothCore, Claude.

Licence MIT pour les outils et les textes français (voir `LICENSE`). Les textes d'origine restent la propriété de leurs ayants droit.

---

### English summary
French localisation of *Conquest of Azeroth* (WoW 3.3.5a): a Python toolkit to build the client `patch-T.MPQ` from a TSV translation database, list untranslated spell strings, and validate formatting tokens. The client stays enUS. Server SQL scripts are published in Releases. No game files included.
