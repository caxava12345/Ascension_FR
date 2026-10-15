# Scripts SQL

Les scripts serveur (PNJ, quêtes, objets, descriptions de sorts) sont publiés dans les **Releases**, pas dans le dépôt.
Version test prévue : **V0.1**.

Chaque lot contient `01_sauvegarde`, `02_appliquer`, `03_restaurer` : la sauvegarde crée des tables `zz_fr_bak_*`, `03_restaurer` annule. Appliquez les lots dans l'ordre indiqué par la Release.
