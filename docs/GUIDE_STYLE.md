# Guide de style — traduction WoW EN → FR (Conquest of Azeroth)

## Priorité des sources
0. `donnees/termes_noyau.tsv` (termes curatés, fait foi) → 1. officiel 3.3.5 (client frFR, GlobalStrings) → 2. officiel retail (formulation parfois moderne, ex. « Coffre » au lieu de « Torse ») → 3. dérivé/base → 4. traductions CoA déjà faites (cohérence interne, mais typographie parfois incohérente).
Un terme déjà traduit dans le projet garde sa traduction (ex. Dawn = Aurore, Vow = Vœu, Sunwell = Puits de soleil).

## Règles
- Vouvoiement (« vous », « votre »). Registre sobre, lore Blizzard.
- Noms propres canoniques FR officiels : Scourge = Fléau, Burning Legion = Légion ardente, Lich King = Roi-liche, Forsaken = Réprouvés, Void = Vide, Light = Lumière, Outland = Outreterre, Northrend = Norfendre, Stormwind = Hurlevent, Ironforge = Forgefer, Undercity = Fossoyeuse.
- Noms de sorts : majuscule initiale seule (« Nova de givre »). Noms d'écoles : minuscule dans le texte (« dégâts de givre »).
- Unités : « mètres » (officiel) ; « sec » ou « secondes » ; espace insécable avant `:` `;` `!` `?` `%`. Apostrophe typographique ’ (officiel) — l'API normalise ' et ’.
- Conserver à l'identique : `$s1` `${…}` `$?s123[..][..]` `|cFFRRGGBB…|r` `%s` `%d` `@s:123:0@` `@ext:..:ext@` `@ifknown:..:ifknown@` `\r\n` `$g..:..;` (genre : garder la forme FR `$gil:elle;`).
- Pluriels `$leffect:effects;` → `$leffet:effets;` ; `$lspell:spells;` → `$lsort:sorts;`.
- Les noms de sorts cités dans le texte (balises couleur) utilisent le nom FR du sort.
- Ne pas traduire : noms de joueurs, clés techniques, chemins de fichiers, SQL/colonnes.
- Texte de quête/PNJ : ton narratif, « vous » au joueur ; garder `$N` `$C` `$R` `$B` `$g`.

## Cas particuliers adoptés
- Goldshire = **Comté-de-l'Or** (forme officielle).
- Pyromancien : Ember = Braise, Flamecasting = Incantation de flammes.
