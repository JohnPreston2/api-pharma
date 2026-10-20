# Scripts de génération — OBSOLÈTES

`create_posters_11_20.py` et `create_posters_16_20.py` ont servi à produire la
1re version des posters 11 à 20. **Ne plus les exécuter.**

Vérifié le 2026-10-20 : en régénérant les 10 posters dans un dossier temporaire,
seuls 3 sont identiques aux fichiers commités (`contraception`, `addictologie`,
`menopause`). Les 7 autres (`allergie_rhinite`, `migraine`, `osteoporose`,
`prostate_HBP`, `eczema_DA`, `goutte`, `polyarthrite_rhumato`) ont été corrigés à
la main lors des audits de juin 2026 : relancer les scripts **écraserait ces
corrections**.

Les fichiers HTML de `posters/` sont la source de vérité. Les scripts sont
conservés pour l'historique uniquement (chemin de sortie codé en dur, 1 CSS
embarqué par script).
