# Installation

## Client (joueur)

**Prérequis :** le client Conquest of Azeroth / Ascension, avec son dossier `Data\frFR` (présent dans le paquet client). Le français passe par la locale `frFR` du client : le jeu doit pouvoir la charger.

1. **Fermez le jeu et le lanceur.** Le jeu verrouille `patch-T.MPQ` tant qu'il tourne.
2. Dans `Data\`, renommez `patch-T.MPQ` en `patch-T.MPQ.orig` : c'est votre sauvegarde.
3. Copiez `patch-T_v37.MPQ` dans `Data\` et renommez-le **exactement** `patch-T.MPQ`. Le jeu ne charge que les archives dont le nom est `patch-` + **une seule lettre** : un nom comme `patch-ZZ.MPQ` est ignoré.
4. Videz le dossier `Cache` du client.
5. Ouvrez `WTF\Config.wtf` (jeu fermé) et mettez la ligne :
   ```
   SET locale "frFR"
   ```
   Pour jouer en anglais : `SET locale "enUS"`. C'est le même patch dans les deux cas.
6. Lancez le jeu.

**Vérifier :** l'interface (menus, sorts, infobulles) est en français ; aucun message rouge d'erreur Lua (un addon comme BugSack permet de les voir). En `enUS`, tout doit être comme avant le patch.

**Revenir en arrière :** supprimez `patch-T.MPQ`, renommez `patch-T.MPQ.orig` en `patch-T.MPQ`, videz `Cache`.

## Serveur

Le patch client suffit à traduire l'interface, les sorts, les objets en tooltip, etc. Les noms de PNJ, les quêtes, les dialogues viennent du serveur : installez le pack SQL.

1. Arrêtez le worldserver, faites un dump complet de `acore_world`.
2. Décompressez `SQL_Ascension_FR_v3.zip`. Lancez `installer.bat` (Windows, client `mysql` dans le PATH) ou `bash installer.sh`, ou suivez `LISTE_INSTALLATION.md` fichier par fichier.
3. Contrôlez avec `4_verifier.sql` : la colonne `manquantes` doit valoir 0.
4. Redémarrez le worldserver. Annuler : `5_annuler.sql`.

Le pack ajoute des lignes `frFR` dans les tables `*_locale`. Il ne modifie pas l'anglais et ne remplace pas une traduction frFR déjà en base. Un joueur en `enUS` voit l'anglais, un joueur en `frFR` voit le français.

## Dépannage

| Symptôme | Piste |
|---|---|
| Rien n'a changé | Jeu lancé avec un autre `patch-T.MPQ` ? Nom exact ? `Cache` vidé ? `SET locale "frFR"` bien enregistré ? |
| Noms de touches ou de textes bruts (`FACTION_…`, `RACE_…`) | Ancien patch (avant v36) : le patch actuel remplit les chaînes globales pour frFR. |
| Erreurs Lua au démarrage en frFR | Envoyez le texte exact (BugSack) dans une *Issue*, avec la version du patch. |
| Le français disparaît après une mise à jour du jeu | Le lanceur a remis l'original : recopiez le patch (étapes 1 à 4). |
| Texte encore en anglais | Voir [`LIMITES_CONNUES.md`](LIMITES_CONNUES.md), sinon *Issue* avec capture d'écran. |
| Quêtes / PNJ en anglais | Pack SQL non installé, worldserver non redémarré, ou entrée ajoutée à la base après la traduction. |
