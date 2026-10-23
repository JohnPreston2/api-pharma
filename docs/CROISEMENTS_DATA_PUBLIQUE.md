# Données publiques et croisements — approfondissement pour Officina

Point au **23/10/2026**. Périmètre voulu : **données publiques et croisements uniquement** (ni juridique, ni code). Cadre : le business plan Officina du 21/10/2026, dont la valeur repose sur la lecture locale de la base Winpharma (stock ligne à ligne, 30 mois de ventes, prix, TVA, laboratoire, grossiste) et une veille quotidienne (ANSM, RappelConso, 4 flux métier) déjà croisée avec le stock.

## Méthode et limites

- 8 agents de recherche (modèle léger, WebSearch seul) ; plus 4 vérifications directes. **Aucune page, aucun fichier n'a pu être ouvert** (réseau direct bloqué) : tout vient d'extraits de résultats. Les en-têtes de colonnes sont donc souvent « non vus ».
- Confiance : **✅** recoupé ou officiel · **🟡** source unique ou secondaire · **⚠** contradictoire · **déduit** = inférence de ma part, pas un fait sourcé.
- Les études citées sont des **résumés d'extraits** : à relire avant de s'appuyer sur un chiffre.
- **Correction** : la synthèse du 20/10 affirmait qu'aucune étude française ne reliait ventes d'officine et surveillance. C'est faux : des travaux existent depuis 1999 (§4).

## 1. Verdict

1. **Le sens des délais change la conception.** Les ventes de médicaments en officine **devancent** la surveillance officielle (de 1 à 3 semaines selon les études françaises). Donc, pour *prévoir les ventes d'une officine*, les indicateurs Sentinelles / Odissé / SOS Médecins sont **simultanés ou en retard** : ils servent à *expliquer, caler le début de saison et se comparer*, pas à anticiper. Ce qui donne une vraie **avance** : les **prévisions** (météo, indice pollinique à J+2, qualité de l'air à J+1, UV), le **calendrier**, et la **propagation régionale** d'une vague (à tester).
2. **Le meilleur signal avancé est un panel d'officines.** Toutes les corrélations solides viennent de panels de 13 000 à 14 000 officines ; une officine seule est bien plus bruitée. L'ensemble des clients d'Officina est un embryon de panel (le business plan range le partage inter-officines parmi les points bloqués).
3. **Open Medic et Medic'AM ne couvrent que le remboursé** : ni OTC, ni parapharmacie. On ne peut donc **pas** benchmarker le « rayon du mois » avec elles. Le rayon se pilote avec l'environnement, l'épidémie, le calendrier et les ventes propres.
4. **La remise réelle contre le plafond ne se calcule pas avec des données publiques** : aucun fichier de prix fabricant HT par produit n'a été trouvé (le BDM_IT d'ameli est le seul candidat, contradictoire ⚠).
5. **Trois flux machine-lisibles et clés sur le code produit** existent et se branchent directement au stock : la **disponibilité BDPM** (ruptures, tensions, arrêts), la **base BDM_IT** hebdomadaire (radiés, tarifs) et **RappelConso par code-barres**.
6. **Rien n'a été vérifié sur fichier réel.** La première étape utile est de mettre quelques fichiers sous les yeux (§8).

## 2. Ce que l'officine apporte comme clés

D'après le business plan : stock et ventes par produit (CIP13 ou code-barres), prix d'achat et de vente, TVA, laboratoire, grossiste, 30 mois d'historique, commandes. **Jointure naturelle : CIP13** (médicaments) et **EAN/GTIN** (parapharmacie, hors préfixe 3400). Les croisements ci-dessous partent tous de là, ou de la **commune** de l'officine (météo, pollens, territoire, épidémiologie régionale).

## 3. Matrice des croisements

| # | Croisement | Clé | Brique d'Officina | Preuve / état | Verdict |
|---|---|---|---|---|---|
| A | **Disponibilité BDPM** (rupture, tension, arrêt) × stock et ventes | CIP13 (+ CIS ; CIP13 vide = toute la spécialité) | Veille, bilan d'ouverture, « proches de la rupture » | Fichier décrit dans la doc officielle ✅ ; colonnes et fréquence non vues | **Prêt à tester** |
| B | **BDM_IT** hebdo (radiés, modifiés, tarif en vigueur) × stock | CIP13 / CIP7 / UCD | Valeur du stock, dormant, alerte de changement | Mise à jour chaque vendredi 🟡 ; PFHT et TFR ⚠ | **À vérifier sur fichier** |
| C | **BDPM statut + SMR/ASMR + groupes génériques** × stock | CIS via CIP13 | Risque de dormant, taux de génériques | Fichiers existants ✅ ; erreurs de CIS signalées dans les groupes génériques 🟡 | Prêt, avec garde-fous |
| D | **MITM + plan hivernal ANSM** × couverture en jours | CIS / ATC | Stock de sécurité des molécules critiques | Liste MITM ✅ ; liste des 14 molécules 2026-27 non obtenue (2 PDF datés 13 et 16/10 divergent) ⚠ | À curer à la main |
| E | **Calendrier** (vacances A/B/C, fériés) × ventes | date, zone | Prévision, rayon du mois, campagnes | CSV et API ✅ ; ponts non vus | **Immédiat** |
| F | **Météo** (observations, prévisions, vigilance) × ventes saisonnières | commune → station | Prévision, rayon du mois | Données ouvertes ✅ ; effet chiffré au Japon et sur les insecticides 🟡 | **Fort potentiel** |
| G | **Indice pollinique commune** × antihistaminiques, collyres, sprays nasaux | commune, date | Rayon du mois, réassort | Indice J à J+2 ✅ ; **rupture de série en 04/2025** ⚠ | À tester |
| H | **Sentinelles / Odissé / SOS Médecins / SUM'Eau** × familles ATC | région, semaine ISO | Contexte, calage de saison, benchmark | Sentinelles régional ✅ ; département non vu | **Utile, mais en retard sur les ventes** |
| I | **Grippe : vaccination en officine** (jeu data.gouv, panel) × vos délivrances J07E1 | date, âge | Campagnes, point Expert | Jeu existant 🟡 ; maille départementale non confirmée | À vérifier |
| J | **RappelConso V2 par GTIN** × stock parapharmacie | EAN/GTIN | Veille (déjà en service : passer à la clé exacte) | Champ GTIN depuis 29/11/2024 ✅ ; produits sans GTIN exclus ✅ | Prêt |
| K | **ANSM informations de sécurité** (retraits de lots) × stock | CIP, lot | Veille | Lots en texte libre ou PDF ⚠ ; aucun flux | Collecte à parser |
| L | **Open Medic / Medic'AM** × ventes remboursées | CIP13, ATC | Benchmark de mix, saisonnalité nationale | Voir §5-L ; ne couvre pas l'OTC | Partiel |
| M | **INSEE population × Open Medic** → demande attendue relative | commune, région | Bilan d'ouverture, rayon, groupements | Aucune méthode publiée par âge ⚠ | **À prototyper** |
| N | **Open PHMEV × liste de biosimilaires substituables** × vos ventes | CIP13, région | Missions rémunérées (enveloppe biosimilaires de l'avenant n°2) | Jeu existant ✅ | À explorer |

## 4. Preuves disponibles : ce qui est validé, et dans quel sens

**Études françaises** (résumés d'extraits, à relire) :
- **Partenariat Sentinelles – panel IQVIA depuis 1999** : environ 14 000 officines (60 %), ventes de la semaine précédente livrées chaque lundi. ✅
- **Vergu et al. 2006** : ventes hebdomadaires décalées pour **prévoir** le syndrome grippal ; corrélation prévu / observé de 0,85 à 0,96 à 1 à 3 semaines (national). ✅
- **Pelat et al.** (gastro-entérite, environ 13 000 officines, 581 classes ATC4 criblées) : sur 2008-2013, les ventes sans ordonnance détectent l'épidémie **environ 2,25 semaines avant** le réseau sentinelle (résumé). 🟡
- **Vilcu et al. 2019** : corrélation hebdomadaire de 0,84 à 0,94 entre délivrances et médecine générale, sur 3 hivers. ✅
- Allergie, sud de la France 2004-2007 : pollen associé aux délivrances d'antihistaminiques. 🟡

**Autres** : Brésil (publication 2026, ventes OTC avancent les hospitalisations respiratoires de 1 à 3 semaines dans **26,9 à 32 % des régions**, résultat instable entre versions ⚠) ; New York (pollens d'arbres : effet maximal à 2 jours, +28,7 % de ventes) ; Japon (crème solaire : seuil à 10 °C, ventes ×4,7 à +5 °C au-delà ; prévision à 2 semaines utile) ; insecticides (régression avec météo, MAPE 8,66 % contre plus de 20 % pour des méthodes à historique seul, une seule étude). 🟡

**Mises en garde** :
- **Les « remèdes symptomatiques » ne marchent pas partout** : au Royaume-Uni en 2009 (ventes d'un supermarché), ils ne corrélaient pas au national, contrairement aux thermomètres et au gel antiviral.
- À New York, les ventes « syndrome grippal » montaient à l'épidémie mais **pas avant** les urgences, et **les saisons d'allergie les gonflaient**.
- **Aucun gain chiffré** (WAPE ou MAPE) n'a été trouvé pour une officine avec météo, pollen ou épidémie : il faut le mesurer (§7).
- Aucune donnée de ventes d'antidiarrhéiques en fonction de la chaleur ; aucune étude Google Trends contre ventes.

## 5. Détail des croisements prioritaires

### A. Disponibilité BDPM × stock (ruptures, tensions, arrêts)
- Le document officiel de la BDPM décrit un fichier « Disponibilité des spécialités pharmaceutiques ». ✅ Nom présumé `CIS_CIP_Dispo_Spec` (non confirmé).
- **Clés** : CIS et CIP13 ; un **CIP13 vide signifie que toutes les présentations commercialisées de la spécialité sont touchées** (à développer via la table des présentations). Statuts vus : 1 rupture, 2 tension, 3 arrêt de commercialisation (liste coupée) ; « remise à disposition » non vu dans ce fichier. 🟡
- Le miroir mensuel de data.gouv inclurait un fichier « disponibilité ». 🟡 Pas d'API officielle.
- **Piège** : la date de mise à jour est contradictoire (29/09/2026 pour la page officielle, 02/03/2026 pour un miroir) ⚠ : toujours conserver la date lue sur le fichier.
- **Apport** : un flux structuré qui remplace en partie la collecte web de l'ANSM, et qui qualifie les « produits proches de la rupture » du bilan d'ouverture (rupture réelle ou simple lenteur de rotation).

### B. BDM_IT (Assurance Maladie) × stock et valeur
- Base de référence des médicaments remboursables, **mise à jour chaque vendredi**, fichiers **DBF** : `UCD_TOTAL` (tarif en vigueur, sans historique), `UCD_MAJ` (enregistrements modifiés), `UCD_HISTO_PRIX` (cité, non décrit) ; liste CIP, modifications, radiés, collectivités. 🟡
- **⚠ Contradiction** entre deux lectures de la même page : l'une y voit « prix fabricant HT, prix public TTC, taux, TFR, dates », l'autre ne confirme ni PFHT, ni TFR, ni taux. **À trancher sur le fichier réel** : c'est le point qui décide si une partie de l'analyse des remises devient possible avec des données publiques.
- **Aucun historique de prix publié** : pour suivre les baisses, il faut **archiver soi-même chaque vendredi**.
- Dates d'effet observées pour les baisses : 1ᵉʳ janvier, 1ᵉʳ mars, 1ᵉʳ juillet, 1ᵉʳ octobre ; délai d'environ 50 jours avant visibilité en logiciel (à vérifier). Exemple : baisses de prix de génériques au 01/01/2027.
- **Apport** : alerter sur les changements de prix et de statut des références **en stock** (valorisation, risque de dormant).

### C. Statut, SMR et groupes génériques (BDPM) × stock
- Fichiers : spécialités, présentations, compositions, avis SMR/ASMR, liens des avis de la Commission de la transparence, groupes génériques, conditions de prescription, plus un 11ᵉ fichier (médicaments d'intérêt thérapeutique majeur) **non converti** dans le miroir CSV. ✅
- **Le code ATC n'est pas dans la BDPM** (sauf MITM, non vu) : le mapping CIP13 → ATC vient de **Medic'AM** ou d'Open Medic. 🟡
- Signal avancé de déremboursement : **SMR insuffisant**. Exemple de 2026 : prise en charge à 100 % supprimée au 01/10/2026 pour les SMR faibles en ALD (retour à 15 %). 🟡
- **Piège** : un utilisateur signale des erreurs de CIS dans le fichier des groupes génériques, qui faussent la jointure. 🟡

### D. MITM et plan hivernal × couverture
- Liste MITM (décembre 2024, ~8 100 à 10 000 présentations selon la source ⚠), stock de sécurité exigé des industriels de 2 mois (4 possibles).
- Plan hivernal 2026-27 activé (niveau 1 sur 2) ; 14 molécules sentinelles (antibiotiques, paracétamol, corticoïdes, asthme). **Liste précise non obtenue**, et deux PDF datés du 13 et du 16/10/2026 divergent ⚠.
- **Apport** : étiqueter les produits du stock (MITM, sentinelle) et calculer leur **couverture en jours** avant le pic.
- **Effet à ne pas oublier** : les ventes baissent d'environ 11 % pendant une rupture (7 % quand le risque est déclaré, données 2024) : **les ventes ne sont pas la demande**. Les périodes de rupture doivent être **écartées ou corrigées** dans l'historique d'une prévision. Le fichier de disponibilité est un instantané : **commencez dès maintenant à l'archiver**.

### E. Calendrier × ventes
- Vacances scolaires zones A/B/C (CSV, une ligne par date, un booléen par zone ; pas d'API trouvée ; changement de zones en 2016) ; jours fériés (API Etalab, 20 ans en arrière, 5 en avant, Code du travail seulement) ; ponts et événements locaux : non vus. ✅
- **Apport** : variables sans bruit pour la prévision, la trousse de voyage, la rentrée, les campagnes.

### F. Météo × ventes saisonnières
- **Observations** : fichiers par département, quotidiens (2 dernières années détaillées, mensuel au-delà selon la page : à confirmer) ; horaires (~100 paramètres). **13 362 stations ouvertes**. L'identifiant à 8 chiffres intègre le code INSEE de la commune ; **aucun outil « station la plus proche » trouvé** : à construire avec les coordonnées. 🟡
- **Prévisions** : AROME (1,3 km, toutes les 3 h, échéance 51 h), ARPEGE (10 km, toutes les 6 h, 114 h) ; accès par compte, quotas non confirmés. 🟡 **Vigilance** : bulletin JSON par département, archive depuis le 28/11/2022. ✅
- **UV** : pas de jeu ouvert Météo-France ; **CAMS (Copernicus)** donne des prévisions UV quotidiennes, à la maille européenne. Réanalyse **ERA5** : 0,25° horaire depuis 1940, décalage d'environ 5 jours, compte gratuit. 🟡
- **Piège** : « Température quotidienne départementale » sur data.gouv vient de Weathernews, pas de Météo-France.
- **Apport** : prévision à quelques jours pour solaires, après-soleil, hydratation, répulsifs ; le décalage seuil de température → ventes reste à mesurer sur vos données.

### G. Pollens × antihistaminiques, collyres, sprays nasaux
- **Dispositif en transition** : le RNSA est en liquidation depuis mars 2025 ; la coordination passe aux AASQA (arrêté du 2 mars 2026). ✅
- **Indice pollen Atmo France** : par commune, 6 taxons (ambroisie, armoise, aulne, bouleau, graminées, olivier), publié à 13 h pour J à J+2, par modèle statistique. Avant le 01/04/2025 : base RNSA départementale. 🟡
- **Historique RNSA 1987-2024** par jour et par taxon (deux archives, ~127 Mo, Licence Ouverte 2.0). ✅
- **⚠ Rupture de série** entre le RNSA (capteurs, jusqu'à 2024) et l'indice modélisé (depuis 04/2025) : un historique de 30 mois de ventes **chevauche les deux méthodes**. Ne pas entraîner un modèle sans traiter cette rupture.
- **Effet** : décalage de 0 à 2 jours (New York, sud de la France, Chine). L'**avance** utile vient donc surtout de la climatologie (début de saison par taxon) et de la prévision J+2.
- **Piège** : l'allergie gonfle les ventes de produits « rhume » : à séparer des croisements épidémiques.

### H. Surveillance épidémiologique × familles ATC
- **Sentinelles / Sentiweb** : API REST (JSON/CSV), **CSV en ISO-8859-1**, colonne `week` = année × 100 + semaine ISO, lignes de commentaires commençant par `#`, géographie par code INSEE ; **national et régional** (département non vu). Indicateurs : IRA, diarrhée aiguë, varicelle (zona, oreillons, Lyme, coqueluche selon les listes). Coupure le lundi, **publication le mercredi (environ 3 jours, déduit)** ; environ 70 % des déclarations à la parution, puis révision : **conserver chaque version**. ✅/🟡
- **Odissé** : API Opendatasoft (explore v2.1), niveaux national, régional, départemental et intercommunal selon le jeu ; **liste des jeux utiles, fréquences et historique non vus**. Un jeu grippe régional (SurSaUD) est confirmé. ✅/🟡
- **SOS Médecins** : taux par département et classes 0-4, 5-14, 15-64, 65+ ; **ne pas agréger les taux départementaux**. **OSCOUR** : environ 700 structures, 96 % des passages en 2024.
- **SUM'Eau** (eaux usées) : SARS-CoV-2 confirmé, réseau de 54 stations d'après data.gouv (un article plus ancien parle de 5) ; **grippe et VRS non confirmés**.
- **Saison grippale 2025-26** (BEH, probable) : début S49, pic en ville S51, fin S06. **Aucun seuil épidémique national vérifié** ; ne pas utiliser le seuil de 167 pour 100 000 (antérieur à 2016) : dériver le seuil de l'historique.
- **Biais saisonnier** : hausse habituelle des ventes en décembre sans lien épidémique (ANSM).
- **Apport réaliste** : attribuer une hausse de ventes à une vague, caler le début de saison, se situer face au national, détecter une vague régionale en avance.

### I. Vaccination grippe en officine (jeu data.gouv) × vos délivrances
- Jeu « Vaccination grippe 2025-2026 » : dispensations en officine (ATC J07E1) du panel IQVIA-Pharmastat (60 % des officines), par tranche d'âge, quotidien ou hebdomadaire selon la campagne. 🟡
- Couverture des 65 ans et plus : 56 % en 2025-26 (cible OMS 75 %). 🟡
- **Apport** : suivre votre campagne face à la courbe nationale (campagne 2026-27 : 13/10/2026 au 31/01/2027).

### J. RappelConso V2 par GTIN × stock parapharmacie
- Champ GTIN depuis le 29/11/2024 ; **le jeu « trié par GTIN » exclut les produits sans code-barres**. Médicaments et dispositifs médicaux : hors RappelConso.
- Catégories vues pertinentes (comptes de capture, variables) : cosmétiques, hygiène, dispositifs médicaux grand public, puériculture, aliments pour bébés, aliments diététiques et nutrition. **Compléments alimentaires comme sous-catégorie : non confirmé.**
- **Apport** : passer d'une recherche par nom à une **jointure exacte sur le code-barres** (la veille de l'officine collecte déjà RappelConso).

### K. ANSM informations de sécurité (retraits de lots)
- Fiches HTML par action, **détail dans un PDF joint, lots parfois seulement dans le titre**. Pas de flux ni d'API trouvé. Le canal officiel pour les officines est le **Dossier Pharmaceutique** (non public).
- Le contenu du fichier BDPM « informations importantes » **n'est pas confirmé** : ne pas supposer qu'il contient les retraits de lots.
- **Apport limité** tant que le stock n'est pas suivi au lot : alerte au niveau du produit (« vérifier vos lots »).

### L. Open Medic / Medic'AM × ventes remboursées
- **Open Medic** : délivrances **remboursées** en ville, tous régimes ; annuel (2025 publié, anomalie « région » corrigée le 10/07/2026, dernière mise à jour 24/08/2026). Colonnes vues : ATC1 à ATC5, CIP13, **BOITES, REM, BSE** ; `TOP_GEN` (valeurs 0, 1, 4, 9 ; **code 4 non documenté**), `GEN_NUM`. **Âge en 3 tranches : 0-19, 20-59, 60 et plus** (+ inconnu) ; sexe ; **région du bénéficiaire** (pas de département vu) ; spécialité du prescripteur (nom de colonne non confirmé). 🟡
- **Limites déjà établies** : **pas de dimension officine** ; cellules de moins de 10 bénéficiaires masquées ; REM sans honoraires ; un bénéficiaire peut apparaître sur plusieurs CIP13 ; **l'ATC d'un même CIP peut changer selon l'année** (joindre par année) ; pas d'OTC. 🟡
- **Medic'AM** : mensuel depuis 2015, par CIP13, ATC5 et ATC2, base, montant, boîtes, prescripteur libéral ou salarié ; **maille géographique non vue (probablement nationale)**.
- **Usage réaliste** : comparer votre **mix** (par ATC) à la tendance régionale ; situer votre **taux de générique** ; extraire une **saisonnalité nationale mensuelle** par produit (Medic'AM) ; repérer les molécules en hausse. **Ne permet pas** une part de marché locale.

### M. Demande attendue relative (population × consommation)
- **Idée** : consommation par produit, âge (3 tranches), sexe et région (Open Medic) rapportée à la population correspondante (INSEE), puis appliquée à la population de la zone de l'officine, donne un **indice relatif**. La part de marché de l'officine étant inconnue, on **calibre un facteur global sur son panier remboursé** puis on repère les produits très **sous- ou sur-représentés** (sous-vendus, ou cause d'un surstock).
- **Faisabilité des âges** : les tranches d'Open Medic se **reconstruisent exactement** à partir des tranches quinquennales du recensement (commune, IRIS), **pas** à partir des carreaux de 200 m (bandes incompatibles). 🟡 déduit
- **Aucune méthode publiée** de dépense par âge pour l'officine n'a été trouvée : seule la formule générique « habitants × dépense moyenne × indice de richesse locale » ; **à prototyper et à valider**, pas à promettre.
- **Clés territoriales** (chaque jeu a sa version du code officiel géographique) : populations de référence 2023 (communes au 01/01/2025), IRIS 2022 (géographie 01/01/2024), BPE 2024 (01/01/2024), mobilités 2022 (01/01/2025) : **table de correspondance indispensable**. Le **carreau 200 m est la seule clé stable** entre millésimes.
- **Autres entrées** : revenus (Filosofi **2021**, dernier millésime ; 2022 non produit), carreaux 200 m (publié 02/2026), FINESS (extraction gelée au 04/05/2026, nouvelle version « Finess+ » du 20/07/2026 ; EHPAD dans un jeu à part), Sirene (NAF 47.73Z ; nouvelle nomenclature au 01/01/2027), mobilités domicile-travail 2022, accessibilité aux généralistes (2021). **Pas de fichier national médecins par commune** trouvé (hors annuaires régionaux).

### N. Biosimilaires : lier les données aux missions rémunérées
- Avenant n°2 (signé le 07/04/2026) : enveloppe biosimilaires **répartie selon le nombre de boîtes substituées**. 🟡
- **Open PHMEV** : prescriptions hospitalières délivrées en ville, 2014-2025, classe d'âge et sexe, base régionale et base complète avec **géolocalisation de l'hôpital**. ✅
- **Liste substituable** : décisions ANSM et arrêté, **pas de fichier consolidé** (11 à 13 groupes) : à tenir en table de référence manuelle (peu de lignes).
- **Apport** : estimer le **potentiel de boîtes substituables** et suivre le taux de substitution par groupe.

## 6. Cartes des délais : qui devance qui

| Signal | Avance (+) ou retard (−) sur vos ventes | Niveau de preuve |
|---|---|---|
| Prévisions AROME / ARPEGE | **+2 à 5 jours** (par construction) ; prévision à 2 semaines jugée utile pour le solaire au Japon | 🟡 |
| Indice pollen commune, J+2 | **+0 à 2 jours** | 🟡 |
| Indice ATMO, J+1 | +1 jour ; **aucun lien quotidien démontré** avec asthme ou BPCO | 🟡 |
| UV CAMS, vigilance J / J+1 | quelques jours | déduit |
| Calendrier | connu d'avance | ✅ |
| Sentinelles diarrhée × antidiarrhéiques | **retard** : les ventes devancent d'environ 2,25 semaines | 🟡 |
| Sentinelles IRA × délivrances | **retard** : ventes prédictives à 1-3 semaines | ✅ |
| SOS Médecins, OSCOUR (bulletin du mercredi) | simultané ou en retard | déduit |
| Eaux usées SARS-CoV-2 | avance de quelques jours probable ; **à mesurer** | non vu |
| Propagation d'une vague entre régions | **inconnue** : à tester avec les séries régionales | à mesurer |

## 7. Protocole de validation (à faire avant de construire)

Sur les 30 mois de ventes de l'officine pilote :
1. **Référence** : le modèle saisonnier actuel, par famille de produits.
2. **Ajouter une famille de signaux à la fois** : calendrier, puis météo (observée puis prévue), puis pollen, puis épidémie régionale. Mesurer le gain d'erreur (WAPE par famille) sur la **dernière saison mise de côté**.
3. **Écarter ou corriger les périodes de rupture** (fichier de disponibilité archivé) : sinon la demande est sous-estimée.
4. **Séparer allergie et infections** pour les produits « rhume ».
5. **Ne garder que les croisements qui battent la référence** de façon stable d'une saison à l'autre.
Gardes : une officine isolée est bruyante ; ne pas extrapoler les corrélations des panels de 14 000 officines.

## 8. Pour passer de « non vu » à « vérifié » : fichiers à me confier

Des **échantillons sans aucune donnée de patient** suffisent (en-têtes et quelques dizaines de lignes) :
1. Fichiers BDPM : présentations, disponibilité, informations importantes, MITM, groupes génériques.
2. **BDM_IT** : fichier tarif en vigueur et sa notice (pour trancher PFHT et TFR).
3. **Open Medic 2025** et son descriptif des variables.
4. **Medic'AM**, un fichier mensuel (pour la maille géographique).
5. Un export **Sentiweb** régional (IRA) et la liste des jeux **Odissé**.
6. Début du CSV **RappelConso** par GTIN et du jeu **vaccination grippe**.
7. Un extrait **anonyme** d'export Winpharma (produit × jour) pour valider le code produit (CIP13 contre CIP7 et EAN).

## 9. Priorités proposées

**À tester en premier** (flux déjà clés sur le produit, gain direct sur le stock) : **A** (disponibilité), **B** (BDM_IT, après vérification), **J** (RappelConso par GTIN), **E** (calendrier). Archiver dès maintenant le fichier de disponibilité et BDM_IT (aucun historique publié).
**Ensuite** (prévision) : **F** (météo observée et prévue), **G** (pollen, avec traitement de la rupture de série), puis **H** (épidémie régionale pour l'attribution), en suivant le protocole du §7.
**À prototyper** : **M** (demande relative), **N** (biosimilaires), **I** (campagne grippe).
**À écarter ou différer** : remise réelle contre plafond (PFHT non public), benchmark OTC (aucune donnée publique), part de marché locale, retraits de lots au niveau du lot, eaux usées pour la grippe et le VRS.

## 10. Hors périmètre, mais utile au business plan

Le business plan indique « part de marché de Winpharma : non trouvée ». Une source secondaire (Clempo, télétransmissions) donne environ **36-37 % pour Winpharma**, **40 % pour LGPI**, 10-11 % pour Smart Rx, 7-8 % pour Léo, soit 95 % pour les quatre premiers 🟡 ; la base installée de Winpharma varie de 6 600 à 8 000 officines selon les sites ⚠. À recouper avant tout objectif chiffré.

## Principales sources (extraits de recherche, à rouvrir)

- BDPM : [documentation des fichiers (v3)](https://base-donnees-publique.medicaments.gouv.fr/docs/Contenu_et_format_des_fichiers_telechargeables_dans_la_BDM_v3.pdf) · [téléchargement](https://base-donnees-publique.medicaments.gouv.fr/telechargement) · [miroir CSV mensuel](https://www.data.gouv.fr/datasets/base-de-donnees-publique-des-medicaments-en-csv-conversion-mensuelle)
- Prix : [BDM_IT, présentation](http://www.codage.ext.cnamts.fr/codif/bdm_it/index_presentation.php) · [BDM_IT, fichiers UCD](http://www.codage.ext.cnamts.fr/codif/bdm_it/index_tele_ucd.php)
- Assurance Maladie : [Open Medic](https://www.data.gouv.fr/datasets/open-medic-base-complete-sur-les-depenses-de-medicaments-interregimes) · [Medic'AM](https://www.data.gouv.fr/datasets/536999d3a3a729239d20533a) · [Open PHMEV](https://www.data.gouv.fr/datasets/open-phmev-bases-sur-les-prescriptions-hospitalieres-de-medicaments-delivrees-en-ville) · [documentation SNDS, tables CIP](https://documentation-snds.health-data-hub.fr/tables/er_pha_f/)
- Épidémiologie : [schéma CSV Sentiweb](https://ns.sentiweb.fr/incidence/csv-schema-v1.json) · [Sentinelles, méthode des ventes](https://www.sentiweb.fr/document/methodes_ims) · [jeu Odissé grippe régional](https://odisse.santepubliquefrance.fr/explore/dataset/grippe-passages-urgences-et-actes-sos-medecin_reg) · [vaccination grippe 2025-2026](https://www.data.gouv.fr/datasets/vaccination-grippe-2025-2026/reuses_and_dataservices)
- Environnement : [indice pollen](https://www.data.gouv.fr/datasets/indice-pollen) · [pollens historiques RNSA](https://www.data.gouv.fr/datasets/687908a8e14f33edbc026da2) · [indices ATMO](https://www.data.gouv.fr/datasets/indices-atmo/reuses_and_dataservices) · [vigilance Météo-France](https://www.data.gouv.fr/dataservices/api-bulletin-vigilance/reuses) · [vacances scolaires](https://www.data.gouv.fr/datasets/vacances-scolaires-par-zones) · [jours fériés](https://www.data.gouv.fr/dataservices/jours-feries/) · [UV CAMS](https://health.hub.copernicus.eu/uv-index-forecasts)
- Alertes : [RappelConso V2 par GTIN](https://www.data.gouv.fr/datasets/rappelconso-v2-produits-tries-par-gtin) · [ANSM, plan hivernal 2026-27](https://ansm.sante.fr/actualites/lansm-active-le-plan-2026-2027-de-suivi-des-medicaments-et-des-dispositifs-medicaux-de-lhiver)
- Territoire : [populations de référence 2023 (INSEE)](https://insee.fr/fr/information/8683652) · [carreaux 200 m, Filosofi 2021](https://www.insee.fr/fr/statistiques/8735243) · [FINESS](https://www.data.gouv.fr/datasets/finess-extraction-du-fichier-des-etablissements)
- Études : [Vergu et al. 2006](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3291431/) · [Vilcu et al. 2019](https://link.springer.com/article/10.1186/s12874-019-0745-5) · [Pelat et al., gastro-entérite](https://knowledgerepository.syndromicsurveillance.org/sites/default/files/2022-10/Syndromic_Surveillance_Of_Gastroenteritis_Using_Medication_Sales_In_France_0.pdf) · [Brésil, 2026](https://www.nature.com/articles/s44482-026-00014-w) · [Japon, ventes de pharmacies et température](https://www.data.jma.go.jp/risk/en/drugstore.html)
