# api-pharma — Contexte de session

## Qui est l'utilisateur
Pharmacien qui a repris son officine après **5 ans d'absence**.
Objectif : se remettre à niveau rapidement sur les pathologies chroniques les plus dispensées.
Approche : 80/20 — 20 pathologies qui représentent ~85% des prescriptions chroniques.

---

## Ce qui a été construit (branche `claude/pharma-api-analysis-NqHvg`)

### Fiches Markdown — `fiches/`
**20 fiches** de référence (physiopatho · diagnostic · classes thérapeutiques · interactions · réflexes · vocabulaire patient) :

**Session 1 (fiches 01-10) :**
- `01_HTA.md` · `02_diabete_type2.md` · `03_dyslipidémie.md` · `04_douleur_paliers_OMS.md`
- `05_asthme_BPCO.md` · `06_depression_anxiete_insomnie.md` · `07_hypothyroidie.md`
- `08_RGO_ulcere_IPP.md` · `09_anticoagulation_AVK_NACO.md` · `10_insuffisance_cardiaque.md`

**Session 2 (fiches 11-20) :**
- `11_osteoporose.md` · `12_allergie_rhinite.md` · `13_contraception.md` · `14_prostate_HBP.md`
- `15_migraine.md` · `16_eczema_DA.md` · `17_polyarthrite_rhumato.md` · `18_addictologie.md`
- `19_menopause.md` · `20_goutte.md`

- `INDEX.md` (mis à jour avec toutes les 20 fiches + liens posters)

Enrichissements inclus : **DCI + Princeps** (noms de marque) + **volumes open-medic 2023** (boîtes/prix/CA).

### Posters HTML A4 — `posters/`
Prêts à imprimer (`Ctrl+P → A4 · couleurs activées`). **36 fichiers** :

| Fichier | Couleur | Contenu |
|---|---|---|
| `HTA_poster.html` | Crimson/rouge | HTA |
| `diabete_type2_poster.html` | Bleu-teal | Diabète T2 |
| `dyslipidémie_poster.html` | Violet-orange | Dyslipidémie |
| `douleur_poster.html` | Violet | Douleur paliers OMS |
| `asthme_BPCO_poster.html` | Bleu ciel | Asthme/BPCO |
| `depression_anxiete_poster.html` | Indigo | Dépression/Anxiété/Insomnie |
| `hypothyroidie_poster.html` | Teal | Hypothyroïdie |
| `RGO_IPP_poster.html` | Orange brûlé | RGO/IPP |
| `anticoagulation_poster.html` | Bordeaux | AVK/NACO |
| `insuffisance_cardiaque_poster.html` | Rouge sombre | Insuffisance cardiaque |
| `osteoporose_poster.html` | Bleu acier | Ostéoporose · Bisphosphonates · Dénosumab |
| `allergie_rhinite_poster.html` | Vert forêt | Allergie · AH2G · Corticoïdes nasaux · ITA |
| `contraception_poster.html` | Rose/framboise | Contraception · EP · CU · DIU |
| `prostate_HBP_poster.html` | Bleu marine | HBP · α-bloquants · I5AR · Tadalafil |
| `migraine_poster.html` | Violet profond | Migraine · Triptans · Anti-CGRP · Rimégépant |
| `eczema_DA_poster.html` | Orange ambré | Eczéma/DA · DC · Dupilumab · JAK-i |
| `polyarthrite_rhumato_poster.html` | Gris ardoise | PR · MTX · Anti-TNF · JAK-i |
| `addictologie_poster.html` | Vert sombre | Tabac · Alcool · Opioïdes · BHD |
| `menopause_poster.html` | Mauve/rose | Ménopause · THS · Estradiol · Utrogestan |
| `goutte_poster.html` | Bordeaux chaud | Goutte · Allopurinol · Colchicine |
| `comptoir_ete_poster.html` | Orange soleil | 9 situations été |
| `reprise_comptoir_poster.html` | Indigo | Guide reprise après 5 ans |
| `quiz_revision_poster.html` | Multi-couleurs | 30 questions · 3 niveaux · 10 pathologies |
| `quiz_revision_poster_2.html` | Rose/pink | 30 questions · 3 niveaux · pathologies 11-20 |
| `soins_postop_cicatrisation_poster.html` | Teal/vert | Soins post-op · 4 phases cicatrisation · crèmes |
| `conseil_bienetre_poster.html` | Vert teal | Compléments alimentaires · Probiotiques · Oméga-3 · Nicorette |
| `huiles_essentielles_poster.html` | Vert forêt | HE LCA · Safety banner · 6 indications · Dilution · HV |
| `arko_phytotherapie_poster.html` | Teal sombre | 8 gammes Arko · ⚠️ Levure riz rouge CI statines · Griffonia/ISRS |
| `hollis_femme_poster.html` | Rose/magenta | Lifecycle féminin · Grossesse · Fer bis. · Folates 5-MTHF · Vit D bébé |
| `glp1_obesite_poster.html` | Bleu électrique | GLP-1/GIP 2026 · Ozempic/Wegovy/Mounjaro · Pénurie · SE · CI |
| `urgences_comptoir_poster.html` | Rouge | 6 protocoles urgence · Adrénaline · AVC FAST · Nalscue · Glucagen |
| `vaccinations_officine_poster.html` | Violet | 10 vaccins officine 2024-2026 · Protocol 9 étapes · CI · Anaphylaxie |
| `interactions_frequentes_poster.html` | Magenta/rose | Top 15 interactions · DANGER/ÉLEVÉ/MODÉRÉ · Aliments/plantes |
| `stupefiants_risques_poster.html` | Gris acier | Ordo sécurisées · BZD règles · Prégabaline stupéfiant 2021 · BHD |
| `pediatrie_poster.html` | Orange | CI par âge · Doses poids · Otite/Rhino/Gastro · Vaccins 2024 |
| `polypharmacie_PA_poster.html` | Gris bleu acier | Chutes · STOPP/START · Cascade médicamenteuse · BPM · Cockroft |

**Chaque poster pathologie contient :**
- DCI + Princeps + `📦 volume open-medic 2023`
- Barre violette `🆕 Nouveauté` (ce qui a changé 2020–2026)
- Section patient enrichie avec `↳ Ce que ça cache` (rouge) + réponse scriptée
- Stratégie thérapeutique · Interactions · 3 réflexes officine

---

## Stack technique du repo
```
api-pharma/
├── app.py              # FastAPI — endpoints /query, /drugs, /interactions
├── rag/                # ChromaDB + Ollama (Qwen 4B) — RAG pharmaceutique
├── data/               # BDPM JSON + open-medic CSV
├── fiches/             # 20 fiches Markdown pathologies + INDEX.md
└── posters/            # 36 HTML A4 posters
```

**RAG non encore déployé** (données sur le PC de l'utilisateur, pas dans le repo).
Prochaine étape possible : brancher le RAG sur les fiches/BDPM pour Q&A en langage naturel au comptoir.

---

## Conventions de travail
- Branche active : `claude/pharma-api-analysis-NqHvg`
- Langue : **français** pour tout le contenu médical/pharmaceutique
- Format posters : A4 portrait, `@media print { -webkit-print-color-adjust: exact; }`
- Données open-medic : approximations publiques 2022-2023 (accuracy prioritaire)
- Push systématique après chaque session de travail

---

## Idées de suite (non démarrées)
1. **RAG au comptoir** — brancher ChromaDB+Ollama sur les fiches pour Q&A naturel
2. **Poster hiver** — équivalent du `comptoir_ete_poster.html` pour nov–jan (bronchiolite, grippe, gastro enfant)
3. **Interactions checker** — UI simple pour entrer une liste de médicaments et voir les CI
4. **Poster Tier 3 supplémentaires** — IRC, glaucome, épilepsie, arthrose
5. **Situations difficiles au comptoir** — refus d'ordonnance, erreur médicamenteuse, patient agressif
6. **Biosimilaires substituables** — liste en vigueur, règles de substitution
7. **Mise à jour quiz** — intégrer pathologies 11-20 + sujets transverses dans le quiz révision
