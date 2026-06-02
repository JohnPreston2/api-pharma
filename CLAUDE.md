# api-pharma — Contexte de session

## Qui est l'utilisateur
Pharmacien qui a repris son officine il y a quelques jours après **5 ans d'absence**.
Objectif : se remettre à niveau rapidement sur les pathologies chroniques les plus dispensées.
Approche : 80/20 — couvrir les 10 pathologies qui représentent ~80% des prescriptions chroniques.

---

## Ce qui a été construit (branche `claude/pharma-api-analysis-NqHvg`)

### Fiches Markdown — `fiches/`
10 fiches de référence (physiopatho · diagnostic · classes thérapeutiques · interactions · réflexes · vocabulaire patient) :
- `01_HTA.md` · `02_diabete_type2.md` · `03_dyslipidémie.md` · `04_douleur_paliers_OMS.md`
- `05_asthme_BPCO.md` · `06_depression_anxiete_insomnie.md` · `07_hypothyroidie.md`
- `08_RGO_ulcere_IPP.md` · `09_anticoagulation_AVK_NACO.md` · `10_insuffisance_cardiaque.md`
- `INDEX.md`

Enrichissements inclus : **DCI + Princeps** (noms de marque) + **volumes open-medic 2023** (boîtes/prix/CA).

### Posters HTML A4 — `posters/`
Prêts à imprimer (`Ctrl+P → A4 · couleurs activées`). 12 fichiers :

| Fichier | Contenu |
|---|---|
| `HTA_poster.html` | Crimson/rouge |
| `diabete_type2_poster.html` | Bleu-teal (structure plus riche) |
| `dyslipidémie_poster.html` | Violet-orange |
| `douleur_poster.html` | Violet |
| `asthme_BPCO_poster.html` | Bleu ciel |
| `depression_anxiete_poster.html` | Indigo |
| `hypothyroidie_poster.html` | Teal (structure unique — 1 seule molécule) |
| `RGO_IPP_poster.html` | Orange brûlé |
| `anticoagulation_poster.html` | Bordeaux |
| `insuffisance_cardiaque_poster.html` | Rouge sombre |
| `comptoir_ete_poster.html` | Orange soleil — 9 situations été |
| `reprise_comptoir_poster.html` | Indigo — guide personnel reprise après 5 ans |

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
├── fiches/             # Markdown pathologies
└── posters/            # HTML A4 posters
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
2. **Poster hiver** — équivalent du `comptoir_ete_poster.html` pour nov–jan
3. **Fiches pédiatriques** — dosages enfant, vaccins, fièvre/otite
4. **Quiz révision** — flashcards générées depuis les fiches pour s'auto-tester
5. **Interactions checker** — UI simple pour entrer une liste de médicaments et voir les CI
