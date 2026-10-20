# api-pharma — Contexte de session

## But du projet (formulé par l'utilisateur, octobre 2026)
Constat de terrain : **les pharmaciens n'ont pas accès aux données de santé de leur propre officine**, car tout est géré par le LGO (logiciel de gestion d'officine). L'utilisateur travaille sur **Winpharma**. D'où l'idée : regarder ce qui est disponible côté **données et API publiques** pour se construire un **outil maison**, puis y brancher les données de l'officine.

Le projet a été conçu en avril 2026. En octobre 2026 il veut le relancer : les LLM ont beaucoup progressé et les données de santé ont évolué ; il craint d'être passé à côté de sujets (voir « Prochaines étapes »).

## Qui est l'utilisateur
Pharmacien en reconversion vers l'IA. Il a repris le métier après **5 ans d'absence** : le kit de fiches et de posters sert aussi à se remettre à niveau sur les pathologies chroniques (stratégie 80/20). Il valide lui-même le contenu clinique.

## Contenu du dépôt
- `fiches/` : 20 fiches Markdown de pathologies + `INDEX.md`.
- `posters/` : posters HTML A4 imprimables (Ctrl+P, A4, couleurs activées). **L'inventaire est généré dans `posters/INDEX.md`** : ne pas recopier de compteurs ici.
- `docs/` : `REVUE_CONTENU.md` (points à valider par le pharmacien), `veille_reglementaire_2026.md`.
- `tools/posters.py` : contrôle de fraîcheur, index, métadonnées. `tools/legacy/` : scripts obsolètes, **ne pas exécuter**.
- **Le code de l'application Flask décrite dans le README (app.py, RAG, clients API, index de 15 000 médicaments) n'est pas dans ce dépôt** : il est sur le poste de l'utilisateur. Ne pas supposer qu'il existe ici (le dépôt ne contient ni FastAPI, ni `rag/`, ni `data/`).

## Conventions
- Langue : **français** pour tout le contenu médical et pharmaceutique.
- Format posters : A4 portrait, `@media print { -webkit-print-color-adjust: exact; }`, noms de fichiers **ASCII** (pas d'accents).
- **Traçabilité obligatoire** : chaque poster porte dans `<head>` `sv:volatilite` (haute 90 j, moyenne 180 j, basse 365 j), `sv:maj`, `sv:sources`, et `sv:valide` seulement après relecture par le pharmacien. Poser les balises avec `python3 tools/posters.py meta`.
- Avant chaque commit touchant `posters/` ou `fiches/` : `python3 tools/posters.py check`, puis `python3 tools/posters.py index`.
- Les HTML de `posters/` sont la source de vérité (les scripts de génération sont périmés : 7 posters sur 10 ont divergé après les audits manuels).
- Ne jamais présenter un chiffre ou une règle réglementaire sans source et date. Une information issue d'une seule source ou contradictoire reçoit un encadré « À VÉRIF. » et une ligne dans `docs/REVUE_CONTENU.md`.
- Les recherches web déléguées à des sous-agents sont des **pistes à recouper**, pas des faits : aucun texte du JO n'a été relu.
- Le contrôle de rendu (nombre de pages A4, absence de débordement) se fait avec Chromium/Playwright ; il n'est pas versionné.
- Données open-medic : privilégier l'exactitude ; 2022-2024 dans l'index existant, 2025 publié (fichiers corrigés après le 10/07/2026).

## Prochaines étapes
1. **Synthèse de la recherche poussée d'octobre 2026** (accès aux données du LGO, open data médicament et santé, épidémiologie et environnement, état de l'art LLM, cadre réglementaire IA et données de santé, outils existants, économie de l'officine) : à consigner dans `docs/` une fois recoupée.
2. Importer le code de l'application dans le dépôt, puis audit technique.
3. Définir comment les données de l'officine sortent du LGO (exports, API, partenaires) en restant dans le cadre juridique.
4. Valider les posters P1 listés dans `docs/REVUE_CONTENU.md`.

## Idées déjà réalisées / restantes
- Fait : poster hiver, règles de substitution des biosimilaires, refonte du poster GLP-1 (remboursement de juin 2026), correction TROD angine.
- Restant : poster « situations difficiles au comptoir », poster Tier 3 supplémentaires (IRC, glaucome, arthrose), interactions checker (désormais fondé sur les RCP, le Thésaurus ANSM étant gelé), RAG au comptoir sur fiches et RCP.
