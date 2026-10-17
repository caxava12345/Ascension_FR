# Contribuer

1. Forkez, créez une branche, ouvrez une Pull Request.
2. Une contribution = des lignes dans `donnees/` (traductions, glossaire). Lancez `python outils/ascension_fr.py verifier …` avant de proposer, et `python -m unittest discover -s outils/tests`.
3. Respectez `docs/GUIDE_STYLE.md` (vouvoiement, jetons intacts, majuscule initiale seule pour les noms de sorts, termes laissés en anglais).
4. N'ajoutez jamais de fichiers du jeu (`*.MPQ`, `*.dbc`), de dumps SQL du serveur ni de contenus tiers sans autorisation.
5. Signalez une erreur de traduction via *Issues* : ID du sort (ou de l'entrée SQL), texte actuel, correction proposée, et la langue du client (`frFR`).
6. Un texte qui reste en anglais en jeu : indiquez où il apparaît (capture d'écran) et si votre client est bien en `frFR` avec le dossier `Cache` vidé.
