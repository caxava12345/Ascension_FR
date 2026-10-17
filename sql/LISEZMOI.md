# Scripts SQL

Le pack serveur est publié dans les **Releases**, pas dans le dépôt : `SQL_Ascension_FR_v3.zip`.

Il **ajoute** des lignes `frFR` dans les tables `*_locale` d'AzerothCore (`creature_template_locale`, `quest_template_locale`, `item_template_locale`, `quest_offer_reward_locale`, `quest_request_items_locale`, `creature_text_locale`, `npc_text_locale`, `gossip_menu_option_locale`, `gameobject_template_locale`, `broadcast_text_locale`, `page_text_locale`).

- L'anglais des tables de base n'est jamais modifié.
- Une traduction frFR déjà présente n'est jamais remplacée (`@FR_FORCER = 0`).
- Contenu : `0_donnees_communes/`, `1_preparation`, `2_sauvegarde`, `3_appliquer`, `4_verifier`, `5_annuler`, `9_nettoyage_donnees`, `installer.bat` / `installer.sh`, `LISEZMOI.md`, `LISTE_INSTALLATION.md`.
- Testé sur MariaDB 10.11 (schéma AzerothCore). Faites un dump de `acore_world` avant, et lisez `docs/LIMITES_CONNUES.md`.
