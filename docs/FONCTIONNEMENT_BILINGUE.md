# Fonctionnement bilingue

## Principe

Les fichiers de textes du client (`*.dbc`) stockent chaque texte en **17 champs** : 16 emplacements de langue plus un champ de drapeaux. Un client lit l'emplacement qui correspond à sa locale. Les tables personnalisées d'Ascension ne remplissent que l'emplacement 0 (enUS).

Le patch laisse l'emplacement 0 **intact** et écrit le français dans les emplacements **2 et 3** :

- l'emplacement 3 est celui de `frFR` dans la table de langues d'Ascension (enUS, enGB, koKR, **frFR**, deDE, …) ;
- l'emplacement 2 est celui que lisent certaines tables natives de Blizzard.

Écrire le même texte aux deux endroits couvre les deux cas. Un texte sans traduction reçoit une **copie de l'anglais** dans ces emplacements : un client `frFR` ne voit jamais de vide.

## Chaînes globales

Ascension ne charge pas `GlobalStrings.lua` : toutes les chaînes globales de l'interface viennent de `GlobalStrings.dbc`, injectées dans l'état Lua par `Extensions.dll`. Une valeur manquante pour la locale donne un nom brut (`FACTION_ALLIANCE`) ou `nil`, ce qui cassait des addons (AceDB, Postal, plaques de nom, PvP). Le patch remplit donc aussi les emplacements frFR de cette table et des noms de races, classes et factions.

## Interface Lua

Les fichiers Lua d'interface sont fusionnés texte par texte avec l'original :

```lua
__ASCFR=GetLocale()=="frFR";                       -- première ligne du fichier
text = (__ASCFR and "Annuler" or "Cancel")          -- chaque texte qui diffère
```

En `enUS` le fichier se comporte comme l'original ; en `frFR` il utilise le français. Trois fichiers qui ajoutent du code (tutoriels, police réduite) sont entourés d'un bloc `if GetLocale()=="frFR" then … end`. Un texte écrit dans un attribut `text="…"` d'un fichier **XML** ne peut pas dépendre de la locale : ces 7 fichiers restent en anglais (voir `LIMITES_CONNUES.md`).

## Ordre de chargement

Le client charge `patch-?.MPQ` (une seule lettre) puis les archives de langue ; `patch-T.MPQ` l'emporte pour les fichiers qu'il contient. Les autres archives du paquet Conquest of Azeroth (A, TA, TW, U, V, WA, etc.) ont été inspectées : aucune ne contient les tables ni les fichiers Lua / XML du patch, donc rien ne masque le patch-T (sept archives sans liste de fichiers n'ont pu être testées que sur les noms connus).

## Serveur

Le pack SQL fait la même chose côté base : lignes `frFR` dans `creature_template_locale`, `quest_template_locale`, `item_template_locale`, `npc_text_locale`, etc. AzerothCore les envoie aux clients qui se déclarent en `frFR`. Les tables de base (anglais) ne sont jamais modifiées, et une cellule frFR déjà remplie n'est jamais remplacée (`@FR_FORCER = 0`).

## Ce qui est vérifié à chaque version

- Chaque emplacement 0 du patch est **identique** à l'original (anglais intact).
- Les emplacements 2 et 3 sont égaux entre eux et jamais vides quand l'anglais existe (`ascension_fr.py controle` pour les sorts).
- Les fichiers Lua fusionnés redonnent l'original en `enUS` et le texte français en `frFR` ; syntaxe Lua 5.1 valide.
- Pack SQL : tables de base identiques avant / après (checksum), frFR existant conservé, installation / annulation / réinstallation reproductibles.
