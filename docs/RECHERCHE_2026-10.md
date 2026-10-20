# Recherche poussée — octobre 2026

Relance du projet après 6 mois, à partir du but formulé par l'utilisateur : **les pharmaciens n'ont pas accès aux données de leur propre officine (enfermées dans le LGO, ici Winpharma) ; construire un outil maison à partir de ce que l'open data et les API publiques permettent.**

## Méthode et limites (à lire d'abord)

- 7 axes confiés à des agents de recherche (modèle léger), outil **WebSearch uniquement**. Aucune page n'a pu être ouverte (accès réseau direct bloqué) : tout vient d'extraits de résultats. Aucun texte du JO, aucun RCP, aucun arrêté relu.
- Le **quota de recherches de la session a été atteint** par plusieurs agents : les rapports sont partiels. Les trous sont listés au §10.
- Niveaux de confiance : **✅** recoupé par plusieurs sources ou source officielle · **🟡** source unique ou secondaire · **⚠** sources contradictoires.
- Les **noms et versions de modèles d'IA de 2026** (§5) viennent d'un seul rapport et dépassent ce que je peux vérifier moi-même : à confirmer avant de s'en servir.
- Rien ici n'est un avis juridique ni clinique.

## 1. Verdict

1. **Le point différenciant n'est plus l'agrégation de données publiques** (elle se banalise : serveur MCP officiel de data.gouv, fichiers BDPM convertis en CSV, projets de RAG sur la BDPM). C'est le **croisement entre les ventes de l'officine et des signaux publics** (épidémie, météo, calendrier), que seul le pharmacien peut apporter.
2. **L'espace « pilotage indépendant du LGO » est vide** d'après les recherches : les tableaux de bord trouvés (Winstat, Smart Rx 360, My Pilot, Offisanté) vivent dans l'écosystème des éditeurs ou dépendent d'eux. 🟡 (absence non démontrée)
3. **Le goulot est la sortie des données du LGO**, pas la technique : aucune API ni programme développeur public trouvé pour Winpharma. Voies légitimes au §2.
4. **Commencer par des données non nominatives** (ventes par produit et par jour) réduit fortement le risque juridique : pas de donnée de patient, pas d'envoi vers un LLM cloud.
5. **Deux sources ont disparu ou changé** : le Thésaurus ANSM des interactions est gelé (aucune alternative ouverte en français trouvée) et le RNSA (pollens) est en liquidation depuis mars 2025.

## 2. Les données de l'officine (le cœur du projet)

**Marché des LGO** 🟡 (Clempo, source secondaire) : LGPI/Pharmagest ≈ 40 %, **Winpharma ≈ 36–37 %**, Smart Rx ≈ 10–11 %, Léo ≈ 7–8 % ; les quatre premiers ≈ 95 %.

**Winpharma** :
- Se présente comme « premier éditeur indépendant de LGO » (agrément Ségur revendiqué). ✅ site éditeur
- Module de statistiques **Winstat** (prix, marges, comparaison panel). Export non documenté. 🟡
- **Aucune API ni programme développeur publics trouvés.** Indices d'intégrations existantes : connecteur e-commerce « WinPasserelle », passerelle API réalisée par un prestataire, middlewares tiers. 🟡
- Propriétaire et base installée : **⚠** (une seule mention « Everys », chiffres de 6 600 à 8 000 officines).

**Autres LGO** : LGPI affirme s'ouvrir à des tiers par API (déclaratif) ; Smart Rx : connexions exclusives avec certains tiers. **Aucun format d'export standard ni marketplace multi-éditeurs trouvé.** Le Ségur n'impose pas d'API ouverte aux tiers (vague 2 en pré-publication). 🟡

**Solutions tierces qui se branchent aux LGO** (déclaratif, aucun test) : Digipharmacie (connecteurs LGPI, Pharmagest, Winpharma, Smart Rx), Apotekisto, API Développement. Modes de connexion observés : connecteur installé par l'éditeur, API, middleware, passerelle ; **extraction de fichiers : non documentée**.

**Cadre juridique** (R1 et R4, sources secondaires) :
- Le **titulaire** est responsable de traitement ; l'éditeur est **sous-traitant** (art. 28 RGPD) avec restitution des données en fin de contrat ; un salarié ne peut pas être responsable de traitement. 🟡
- Le **secret professionnel** s'impose à tout pharmacien, salarié compris. ✅
- Portabilité (art. 20) : peu applicable aux données patients (la dispensation repose sur une obligation légale d'après le référentiel CNIL) ; pour les **données de gestion** (ventes, stocks) : non tranché.
- Historique : l'UDGPO a dénoncé en 2016-2017 des bases verrouillées par des codes liés à la licence ; saisine de la DGCCRF. Aucune position récente de l'Ordre ou de la CNIL sur la réutilisation des données de dispensation.
- Un outil personnel nourri des données de l'officine **sans accord écrit du titulaire** serait un traitement non encadré (inférence de l'agent).

**Voies réalistes pour sortir les données** (à l'exclusion de tout contournement de code ou de chiffrement) :
1. Demande écrite du **titulaire** à l'éditeur d'un export complet ventes / délivrances / stocks, fondée sur la clause de restitution ou de réversibilité du contrat.
2. Demande au support Winpharma des **exports natifs** (Winstat, états, CSV) et de la liste de leurs champs.
3. Demande d'accès API ou de documentation pour un usage interne validé par le titulaire ; sinon connecteur ou middleware existant.
4. Compléter avec les rapports de panel déjà reçus (groupement, IQVIA/GERS) et les données publiques.

**Contexte de sensibilité** : la CNIL a sanctionné IQVIA France de 5 M€ pour des entrepôts de données d'officines (données pseudonymisées, pas anonymes ; information des patients à la charge des officines). 🟡

## 3. Données publiques : état en octobre 2026

| Source | Statut | Accès | Licence / réserve | Confiance |
|---|---|---|---|---|
| **Open Medic 2025** | Publié (titre Cnam « 2014 à 2025 », data.gouv maj 24/08/2026). Anomalie « région » détectée le 25/06, corrigée le 10/07/2026. | Fichiers, ~84 ; âge, sexe, **région** (pas de département trouvé), spécialité du prescripteur | À vérifier | ✅ / ⚠ (description data.gouv encore « 2014-2024 ») |
| **Medic'AM** | Mensuel depuis 2015, par type de prescripteur, CIP13, ATC1-5 | data.gouv | À vérifier | ✅ |
| **Open PHMEV** | Prescriptions hospitalières délivrées en ville, 2014-2025 | data.gouv | À vérifier | ✅ |
| **BDPM** | Fichiers texte à tabulations sans en-tête, mise à jour mensuelle (page officielle datée 29/09/2026). **Pas d'API officielle trouvée.** Migration annoncée vers Info Médicament. | Téléchargement ; miroir CSV mensuel tiers (10 fichiers sur 11, maj 13/10/2026) | Licence ouverte, **citer la source et la date de mise à jour**, ne pas altérer ; version de la licence ⚠ (LO 1.0 ou LOv2) | ✅ / ⚠ |
| **Thésaurus ANSM des interactions** | **Gelé** : dernière version 15/09/2023, consultable jusqu'au 15/06/2027, plus aucune mise à jour | PDF | Licence de réutilisation non trouvée | ✅ |
| **RCP structurés, fichier médicaments-pathologies** | **Non trouvés** | — | — | 🟡 |
| **data.ansm** | Bilan annuel A-1 agrégé (effets indésirables, erreurs, ruptures) | Pas d'API | — | ✅ |
| **ANSM retraits de lots et ruptures** | Une notice HTML par rappel, liste de ruptures en ligne ; **pas de flux ni d'API trouvé** | Collecte (scraping) à étudier | — | 🟡 |
| **Prix (CEPS)** | Base exportée chaque jour vers les éditeurs de LGO ; **aucun export public trouvé** | — | — | 🟡 |
| **Annuaire santé (ANS)** | API FHIR consolidée, RPPS/FINESS | API + téléchargement | — | 🟡 |
| **Odissé (SPF)** | Plus de 250 jeux (urgences, SOS Médecins…) | **API Opendatasoft Explore v2.1**, GET, JSON | — | ✅ |
| **Sentiweb / Sentinelles (Inserm)** | Diarrhée aiguë depuis 1990 ; IRA depuis mars 2020 (série « syndromes grippaux » antérieure à distinguer) | **API REST** (JSON/CSV ; niveaux PAY/REG/RDD) | ⚠ licence (« non spécifiée » sur data.gouv, « libre accès » sur le site) | ✅ |
| **SUM'Eau (eaux usées)** | SARS-CoV-2 seul confirmé ; extension grippe/VRS annoncée, **non confirmée** | data.gouv, Odissé | — | ✅ / 🟡 |
| **Pollens** | **RNSA en liquidation judiciaire (26/03/2025)** ; coordination confiée aux AASQA (arrêté du 2/03/2026) ; historique 1987-2024 en Licence Ouverte 2.0 ; temps réel via Atmo Data | API sur inscription | — | ✅ / 🟡 |
| **Météo-France** | Données publiques sans redevance ; API climatologie (50 requêtes/min), API Bulletin Vigilance (dernière maj juillet 2025) | Compte | Tarif 2026 non vérifié | 🟡 |
| **Indice ATMO** | Par commune, 1 à 6, prévision publiée à 14 h | data.gouv | ⚠ ODbL ou Licence Ouverte 2.0 | 🟡 |
| **Calendrier scolaire** | Zones A/B/C, .ics | data.gouv | Licence Ouverte 2.0 | ✅ |
| **Serveur MCP data.gouv.fr** | Officiel, **expérimental**, lecture seule, sans clé, ~74 000 jeux (juillet 2026) ; 7 ou 10 outils selon les sources | `mcp.data.gouv.fr/mcp` | Code MIT (annuaire tiers) | ✅ / ⚠ |
| **RappelConso V2** | Remplace la V1 (archivée) ; **ne couvre pas les médicaments ni les dispositifs médicaux** | API | — | ✅ |
| **Transparence Santé** | Plus de 10 M de lignes, seuil 10 € | data.gouv | **Réutilisation limitée à la finalité de transparence, usage purement commercial exclu** ; licence ⚠ | 🟡 |
| Références internationales | WHO ATC/DDD 2026 (licence non trouvée) ; RxNorm (UMLS, gratuit) ; **DrugBank CC BY-NC, exclu d'un produit commercial** ; **DDInter 2.0 CC BY-NC-SA** (non commercial) | | | 🟡 |

## 4. Signaux publics × ventes d'officine

**Ce que dit la littérature trouvée** 🟡 :
- Brésil (npj Digital Public Health, avril 2026) : les ventes de médicaments sans ordonnance anticipent les pics d'hospitalisations respiratoires (au moins un flux précis dans 76,7 % des régions ; 68,8 % et 1 à 3 semaines d'avance dans le preprint ⚠).
- Pittsburgh (preprint 2025) : ventes OTC et syndromes grippaux, r = 0,66 avec les passages aux urgences.
- Revue systématique : 17 comparaisons sur 19 montrent une corrélation significative.
- New York (CDC) : les antidiarrhéiques suivent norovirus et grippe.
- **Aucune étude française trouvée** liant ventes officinales et surveillance : espace non exploité.

**Croisements les plus prometteurs** (à tester sur vos propres ventes, aucune garantie) :
1. IRA Sentiweb + eaux usées × antitussifs, expectorants, antigrippaux (avance de 1 à 3 semaines à vérifier).
2. Diarrhée aiguë Sentiweb × antidiarrhéiques et sels de réhydratation.
3. Indice pollinique (AASQA) × antihistaminiques, collyres, sprays nasaux (attention : biais allergique dans les ventes de produits « grippe »).
4. Calendrier scolaire × antipyrétiques et antitussifs pédiatriques (hypothèse, pas de source directe).
5. Arboviroses (surveillance du 1ᵉʳ mai au 30 novembre) et CiTIQUE × répulsifs et tire-tiques (hypothèse).

## 5. LLM et pile technique

**Établi (✅ / 🟡 selon les points)** :
- **Embeddings BGE-M3** (licence MIT, 8 K tokens, disponible dans Ollama) et **reranker bge-reranker-v2-m3** : références retenues par l'API Albert. Les classements d'embeddings sont **instables d'un tableau à l'autre** ⚠ : valider sur votre corpus. `nomic-embed-text` est déconseillé pour le français.
- Recherche **hybride (dense + BM25) puis reranking** : bonne pratique courante. Avec un petit modèle local, découper par section de RCP avec métadonnées ; document entier envisageable avec un gros modèle.
- **Text-to-SQL** : fiabilité encore limitée sur les bases d'entreprise (Spider 2.0 : 21,3 % à la publication, 44,8 % pour un agent de janvier 2026) ; les jeux de référence contiennent beaucoup d'erreurs d'annotation. **Évaluer sur des requêtes validées par un pharmacien** ; préférer des vues et requêtes préparées à un LLM libre sur la base ; **rôle SQL en lecture seule** (le drapeau « read-only » des serveurs MCP n'est pas une frontière : contournement signalé).
- **Albert API (DINUM) est réservée aux agents de l'État** : inutilisable ici.
- **HDS** : aucune certification trouvée pour les API directes de Mistral, OpenAI ou Anthropic ; envoyer des données de santé à un LLM américain est un transfert hors UE. **Données identifiantes = local ou hébergeur HDS ; API cloud réservée aux données publiques.**
- Offres grand public santé de 2026 (Health in ChatGPT, Claude for Healthcare, Copilot Health) : **américaines, sans HDS français, rien pour l'officine.**
- Évaluation : **MediQAl** (32 603 questions d'examens français, Scientific Data, février 2026) ; HealthBench (OpenAI). Références inventées par les modèles : taux élevés en l'absence d'outils de recherche (jusqu'à 28 % de citations inventées dans une étude de neuro-réanimation). Un test sur des questions de RCP (presse pro, ancien) : un modèle généraliste réussit les questions simples et échoue sur les complexes.
- Agents « computer use » pour piloter un LGO : **à écarter** (données patients exposées, CGU de l'éditeur) ; privilégier des exports programmés.

**À confirmer par vos propres essais (noms et versions rapportés par un seul agent, non vérifiés par moi)** : séries Qwen 3.5 / 3.6, Gemma 4, Mistral Small 4 et Medium 3.5, MedGemma 1.5 (licence HAI-DEF, pas Apache), EmbeddingGemma 2. Piste raisonnable : un modèle local de 4 à 9 milliards de paramètres si la carte graphique a moins de 16 Go, un modèle MoE de taille moyenne au-delà, **testés sur 200 à 300 questions annotées par un pharmacien** avant de figer le choix. Vos 60 questions de quiz (réponses déjà rédigées) peuvent en amorcer le jeu.

## 6. Cadre juridique : points de prudence

- **AI Act** 🟡 (cabinets, à confirmer sur EUR-Lex) : l'« omnibus » (règlement 2026/1744 d'après les sources) reporte le haut risque (annexe III au 02/12/2027, annexe I au 02/08/2028) ; **l'information « vous parlez à une IA » (art. 50) s'applique depuis le 02/08/2026** ; l'art. 4 (culture IA) depuis le 02/02/2025.
- **Dispositif médical** : la qualification dépend de la **finalité déclarée**. Révision personnelle sur sources générales : risque faible. **Recommandation de décision pour un patient identifié au comptoir : classe IIa probable** (règle 11, inférence). Séparer trois usages : révision personnelle, information générale, aide au comptoir.
- **HDS** : exigée pour l'hébergeur qui conserve des données de santé **pour autrui** ; un responsable qui héberge ses propres données n'y est pas soumis. Localisation EEE (décret 2026-209, date d'effet ⚠).
- **Données** : pseudonymisées = restent personnelles pour qui détient la clé (CJUE C-413/23 P, 04/09/2025) ; agrégats non identifiables = anonymes (aucun seuil chiffré) ; qualifier un agrégat de ventes de « donnée de santé » n'est pas tranché.
- **Responsabilité** : titulaire = responsable de traitement ; accord écrit du titulaire, registre (art. 30 RGPD), charte informatique, données fictives en développement.
- **EHDS** : application générale 26/03/2027, usage secondaire 26/03/2029 (dates à confirmer). Aucune API Mon espace santé / DMP ouverte aux tiers confirmée.
- **Réutilisation** : citer source, date de mise à jour et URL (BDPM, Licence Ouverte 2.0) ; Transparence Santé : pas d'usage commercial.

**Check-list courte** : (1) aucune donnée nominative vers une API LLM ; (2) accord écrit du titulaire ; (3) séparer révision, information, aide au comptoir ; (4) afficher « réponse d'une IA, à vérifier par le pharmacien » ; (5) citer source et date pour chaque donnée publique ; (6) conserver les versions de fichiers utilisées ; (7) HDS si l'outil héberge pour autrui ; (8) surveiller 02/12/2026, 26/03/2027, 02/08/2028.

## 7. Économie de l'officine et indicateurs

**Faits recoupés** : convention de 2022, **avenant n°2 signé le 7 avril 2026** (enveloppe biosimilaires répartie selon le nombre de boîtes substituées ; aide jusqu'à 20 000 € par an pour l'officine rurale fragile). Plafonds de remises de la LFSS 2026 : **40 %** (génériques, hybrides), **20 %** (biosimilaires), par année civile, par ligne de produits et par officine. Marge brute moyenne **28,1 %** (en recul), chiffre d'affaires moyen +5,6 % (Observatoire FIDUCIAL 2026). Environ 20 000 officines, ~260 fermetures par an.

**Chiffres contradictoires, à valider sur les tableaux officiels avant tout calcul** ⚠ : honoraire à la boîte (1,02 € ou 0,82 €), vaccination (9,60 € ou 7,50 € + 7,50 €), nombre d'indicateurs ROSP « bon usage » (5 ou 7), socle générique à 85 %, comptage d'officines (19 434 à 20 242).

**Indicateurs qu'un outil indépendant pourrait calculer** (à partir de l'export de ventes) : (1) taux de substitution générique ; (2) substitution biosimilaire par groupe ; (3) remise par ligne rapportée au plafond ; (4) taux de FSE sécurisées (cible 73 %, malus de 10 à 30 % sur la rémunération sur objectifs) ; (5) honoraires de dispensation générés ; (6) ruptures subies (boîtes non servies) ; (7) stock dormant et rotation ; (8) adhérence par pathologie chronique ; (9) part des 65 ans et plus polymédiqués ; (10) missions rémunérées réalisées. Les points 8 et 9 exigent des données nominatives ou pseudonymisées : **hors du périmètre de départ**.

**Non trouvé** : API ou données des répartiteurs (OCP, Alliance, CERP), tableaux de bord des groupements (PHR, Leadersanté, PharmaVie), chiffrage de l'effet des plafonds sur la marge.

## 8. Écosystème et espaces blancs

**Existant (déclaratif ou vu par titre)** : projet `bdpm-rag` (prototype, Ollama + Qdrant + LangGraph), conversion mensuelle de la BDPM en CSV, parseur HTML Info Médicament (betagouv), serveur MCP data.gouv ; **PharmAssistant** (commercial, hébergé en France), **MedGPT** (Synapse Medicine), guide IA de Smart Rx (31/03/2026) ; tableaux de bord **Winstat, Smart Rx 360, My Pilot (Pharmagest), Offisanté (O2)**, Digipharmacie. Références : Vidal, **Thériaque** (exploitée par Synapse Medicine depuis 2022, API sous licence commerciale), Base Claude Bernard, **Meddispar** (gratuit, par CIP13), LactMed.

**Espaces blancs** (jugement de l'agent appuyé sur ces faits ; absence non démontrée) :
1. **Base d'interactions ouverte, en français, réutilisable commercialement** (Thésaurus ANSM sans licence claire et gelé, DDInter non commercial, BCB et Thériaque propriétaires).
2. **Veille sur les changements de la BDPM et du Thésaurus** (différences entre mises à jour mensuelles, alertes sur statut, prix, ruptures, génériques) : aucun outil trouvé.
3. **Pilotage indépendant des éditeurs de LGO.**
4. **RAG français sur RCP et notices avec citations et jeu d'évaluation public** : aucun benchmark français trouvé.
5. **Lien entre données d'officine et formation continue** (besoins documentés par Crepoff, DQO 2026, FIDUCIAL).

Besoins exprimés par la profession : logiciels de gestion jugés trop limités, forte demande de formation (sondage Crepoff, mi-2025).

## 9. Feuille de route proposée

**0. Gouvernance (avant tout code sur les données de l'officine).** Accord écrit du titulaire ; périmètre **non nominatif** : produit (CIP13) × jour : quantités, chiffre d'affaires, stock ; traitement local uniquement.

**1. Données publiques seules (sans le LGO).**
- Rafraîchir **Open Medic 2025** (fichiers corrigés après le 10/07/2026) et ajouter **Medic'AM**.
- **Veille des changements BDPM** (différences mensuelles) : espace blanc n°2, utile tout de suite.
- Ingérer **Sentiweb, Odissé, SUM'Eau, vigilance Météo-France, ATMO, calendrier scolaire** dans la base SQLite, avec source et date pour chacune.
- Retirer RappelConso comme source de rappels de médicaments (hors périmètre) ; étudier la collecte des retraits de lots ANSM.

**2. Sortie des données du LGO.** Demande d'export Winstat / états en CSV avec la liste de champs ; étudier ensuite connecteur ou API avec l'accord du titulaire.

**3. Premier produit à valeur.** Prévision de la demande saisonnière : signaux publics comme variables explicatives, test de l'avance de 1 à 3 semaines sur vos ventes.

**4. RAG.** BGE-M3 + reranker, découpage par section de RCP, citation obligatoire, jeu d'évaluation annoté par un pharmacien (dont vos 60 questions de quiz), mesure des références inventées. Pour les interactions : extraire la rubrique 4.5 des RCP ; usage de **révision personnelle** tant que le statut dispositif médical n'est pas tranché.

**5. Indicateurs conventionnels** (§7), après validation des tarifs sur les sources officielles.

## 10. Ce qui n'a pas pu être couvert

Détail d'export de **Winstat** et documentation de l'API Winpharma ; API du Dossier Pharmaceutique ; répartiteurs ; densité de pharmacies et pharmacies de garde ; UV et Lig'Air ; ATIH ; Accès aux soins ; Health Data Hub 2026 ; Transparence Santé 2026 ; CRAT ; VIDAL Recos ; hackathons pharmacie 2026 ; licence exacte d'Open Medic ; portabilité des données de gestion ; contrat de travail et propriété des données de l'officine ; recommandations CNIL de mars 2026 (sources secondaires seulement).

Le plafond de recherches web étant partagé par la session, un agent indique qu'il peut être relevé par la variable d'environnement `CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION` (non vérifié ici) ; une nouvelle session avec un plafond plus haut permettrait de couvrir ces points.

## Sources principales (extraits de recherche, à rouvrir avant usage)

- Données de l'officine : [Winpharma](https://www.winpharma.com/qui-sommes-nous-editeur-de-logiciel/) · [parts de marché des LGO (Clempo)](https://www.clempo.fr/parts-de-marche-logiciels-medicaux/) · [propriété des données (Moniteur des pharmacies)](https://www.lemoniteurdespharmacies.fr/business/numerique/e-sante/a-qui-profitent-les-donnees-recoltees-dans-lofficine) · [référentiel CNIL officines](https://www.cnil.fr/sites/cnil/files/atoms/files/referentiel_-_officines_de_pharmacie.pdf) · [sanction IQVIA](https://cnil.fr/fr/donnees-sante-sanction-5-millions-iqvia) · [Ségur, LGO vague 2](https://esante.gouv.fr/sites/default/files/media/document/DSR-PHA-LGO-Va2_Pr%C3%A9publication.pdf)
- Open data : [BDPM, téléchargement](https://base-donnees-publique.medicaments.gouv.fr/telechargement) · [BDPM en CSV (mensuel)](https://www.data.gouv.fr/datasets/base-de-donnees-publique-des-medicaments-en-csv-conversion-mensuelle) · [Open Medic](https://www.data.gouv.fr/datasets/open-medic-base-complete-sur-les-depenses-de-medicaments-interregimes) · [Medic'AM](https://www.data.gouv.fr/datasets/536999d3a3a729239d20533a) · [Open PHMEV](https://www.data.gouv.fr/datasets/open-phmev-bases-sur-les-prescriptions-hospitalieres-de-medicaments-delivrees-en-ville) · [Thésaurus ANSM](https://ansm.sante.fr/documents/reference/thesaurus-des-interactions-medicamenteuses-1) · [serveur MCP data.gouv.fr](https://guides.data.gouv.fr/intelligence-artificielle/le-serveur-mcp-de-data.gouv.fr) · [Annuaire santé (ANS)](https://esante.gouv.fr/produits-services/annuaire-sante)
- Épidémiologie et environnement : [API Odissé](https://odisse.santepubliquefrance.fr/api-console/explore/v2.1/) · [API Sentiweb](https://www.sentiweb.fr/?page=api) · [SUM'Eau](https://www.data.gouv.fr/datasets/surveillance-du-sars-cov-2-dans-les-eaux-usees-sumeau) · [pollens, AASQA (CITEPA)](https://www.citepa.org/desormais-unifie-sous-legide-des-aasqa-le-dispositif-de-surveillance-des-pollens-entre-dans-le-droit-commun-de-la-qualite-de-lair/) · [Météo-France](https://portail-api.meteofrance.fr/web/) · [Brésil, npj Digital Public Health](https://www.nature.com/articles/s44482-026-00014-w) · [revue systématique](https://www.researchgate.net/publication/268743123_Drug_sales_data_analysis_for_outbreak_detection_of_infectious_diseases_A_systematic_literature_review)
- IA et réglementation : [AI Act, omnibus (Gibson Dunn)](https://www.gibsondunn.com/eu-ai-act-omnibus-agreement-postponed-high-risk-deadlines-and-other-key-changes/) · [HDS (ANS)](https://esante.gouv.fr/produits-services/hds) · [HAS, clefs d'usage de l'IA générative](https://has-sante.fr/jcms/p_3703115/fr/premieres-clefs-d-usage-de-l-ia-generative-en-sante) · [Ordre, cahier IA n°23](https://www.ordre.pharmacien.fr/les-communications/focus-sur/les-cahiers-thematiques/cahier-thematique-n-23-ia-en-sante-entre-promesses-et-prudence2) · [MediQAl](https://www.nature.com/articles/s41597-026-06680-y) · [Albert API](https://ia.numerique.gouv.fr/contactez-nous/acces-albert-api/)
- Économie : [Observatoire FIDUCIAL](https://www.fiducial.fr/Pharmacie/blog/observatoire-fiducial-pharmaciens) · [ROSP 2026 (Extencia)](https://www.extencia.fr/rosp-pharmacien-2026-indicateurs-remuneration) · [avenant n°2 (Moniteur des pharmacies)](https://www.lemoniteurdespharmacies.fr/profession/socio-professionnel/aides-aux-pharmacies-rurales-biosimilaires-teleconsultation-osys-ce-que-change-lavenant-n2-de-la-convention-pharmaceutique) · [plafond des remises (Pharmapex)](https://pharmapex.fr/actualites/plafond-remises-generiques-quel-taux-s-applique-reellement)
- Écosystème : [bdpm-rag](https://github.com/Yami9898/bdpm-rag) · [PharmAssistant](https://pharmassistant.fr/) · [Smart Rx, guide IA](https://www.cegedim.fr/Communique/SmartRx_GuideIA_31032026.pdf) · [Défi iDoc Santé (HAS)](https://www.has-sante.fr/jcms/p_3381855/fr/defi-idoc-sante-decouvrez-les-projets-developpes-et-les-laureats)
