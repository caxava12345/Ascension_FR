# Format des données

## `donnees/sorts_fr.tsv.gz`
TSV compressé en gzip, UTF-8, 3 colonnes avec en-tête :

```
spell_id	champ	texte_fr
1454	Name	Connexion de vie
```

- `champ` ∈ `Name`, `Rank`, `Description`, `Tooltip`.
- Les retours à la ligne sont écrits `\n` et `\r` (littéraux), les tabulations interdites.
- Une ligne par couple (sort, champ). Absent = non traduit (le client frFR affichera alors l'anglais).
- 325 455 lignes dans la version actuelle.
- Modifier : `gunzip -k`, éditer, `gzip -9`, ou lire/écrire avec `lire_traductions()` de `outils/ascension_fr.py`.

## `donnees/glossaire.tsv`
`anglais<TAB>français`, un terme par ligne (noms propres, lieux, termes de jeu).

## `donnees/termes_noyau.tsv`
Termes curatés qui font foi en cas de conflit (priorité maximale).
