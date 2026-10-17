# Limites connues

## Client
- **7 fichiers XML restent en anglais** en frFR (un attribut `text="…"` ne dépend pas de la langue) : `Ascension_CharacterAdvancement/CharacterAdvancement.xml`, `Ascension_MythicPlus/SocketKeystoneFrame.xml`, `Blizzard_TradeSkillUI.xml`, `Ascension_MythicalBoons.xml`, `PVPFrame.xml`, `QuickKeybindActionPicker.xml`, `GlueExtensionError.xml`. Correction possible par des crochets Lua (`SetText`) — à faire.
- **Textes écrits en dur** dans le code Lua d'Ascension, ou envoyés par le serveur sans passer par la base, restent en anglais.
- **Sept archives sans liste de fichiers** (`patch-4`, `patch-5`, `patch-C`, `patch-W`, `patch-WB`, `patch-WC`, `patch-CZZ`) n'ont été testées que sur les noms de fichiers connus.
- **Quelques lignes** présentes seulement dans la source française et absentes du client actuel n'ont pas de français.
- Seules les locales `enUS` et `frFR` sont gérées.
- Une mise à jour du jeu qui remplace des fichiers du client peut demander de reconstruire le patch.

## Terminologie
- Règle du projet : `Hardcore`, `Ascended`, `Worldforged`, `Bloodforged` restent en anglais. Environ 70 textes de sorts échappent encore à la règle (par ex. « Parchemin forgé par le monde : … » pour *Worldforged Scroll*, « Trio hardcore », « Sublimé »). À harmoniser.
- Environ 10 % des noms de sorts cités dans les tomes et parchemins sont approximatifs.
- `ascension_fr.py verifier` signale environ 3 500 textes de sorts dont les jetons (`$s1`, `|cff…|r`) diffèrent de l'anglais : à relire, certains cas sont légitimes.

## Données
- Le format TSV de `sorts_fr.tsv.gz` écrit les retours à la ligne `\r` `\n` en littéraux : le sort 653240 contient une vraie séquence `\r\n` écrite en toutes lettres, qui est relue comme un retour à la ligne (deux cellules concernées).

## Serveur (SQL)
- Pack testé sur **MariaDB 10.11** avec le schéma standard d'AzerothCore ; **pas** sur MySQL 8, ni sur une base Conquest of Azeroth réelle (colonnes supplémentaires éventuelles).
- `1_preparation.sql` passe `item_template_locale.Description` en `TEXT` (255 caractères ne suffisent pas).
- Les entrées ajoutées à la base après la traduction restent en anglais.
- Le dossier optionnel `OPTIONNEL_sorts_serveur_MODIFIE_L_ANGLAIS` remplace l'anglais de la table `coa_client_spell_description` (pas de table `_locale`) : à n'utiliser que si vous acceptez que l'anglais change pour tous.

## État du test
Le mécanisme (emplacements 2 et 3, chaînes globales, locale `frFR`) a été vérifié en jeu. Une relecture complète du jeu en français n'a pas été faite : signalez les textes qui restent en anglais.
