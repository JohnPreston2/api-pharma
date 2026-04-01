# SantéVeille — Plateforme de veille pharmaceutique et épidémiologique

Application Flask qui agrège et croise les données de **4+ APIs publiques françaises de santé** pour produire des analyses qu'aucune source ne fournit seule.

Construit en solo en 3 semaines. 15 000 médicaments indexés, 2.9M enregistrements Transparence Santé, veille épidémiologique temps réel.

---

## Ce que fait le projet

### Sources de données intégrées

| Source | Producteur | Données | MAJ |
|--------|-----------|---------|-----|
| **BDPM** | ANSM | Base officielle des médicaments (AMM, compositions DCI, présentations, génériques) | Quotidienne |
| **open-medic** | Assurance Maladie / data.ameli | Volumes de remboursement par médicament (boîtes + €, 2022-2024) | Annuelle |
| **Transparence Santé** | Min. Santé | Versements des laboratoires aux professionnels de santé — 2.9M enregistrements | Semestrielle |
| **Odissé** | Santé Publique France | Signaux épidémiques temps réel (grippe, passages SAU, SOS Médecins) | Continue |
| **RappelConso** | DGCCRF | Rappels de produits de santé | Continue |
| **Accès aux Soins** | data.ameli | Scores d'accessibilité par département | Annuelle |

> Toutes ces APIs utilisent le moteur **Opendatasoft** → un seul pattern de requête générique (`opendatasoft_client.py`) pour toutes les sources.

### Croisements de données

**1. BDPM × open-medic** — Chaque fiche médicament affiche les volumes remboursés par l'Assurance Maladie, l'évolution 2022-2024, les génériques disponibles et les avis HAS. 15 000 médicaments en mémoire, zéro latence.

**2. Transparence Santé × fiche médicament** — Pour chaque médicament, remontée des versements du laboratoire titulaire aux professionnels de santé, par année et par motif (rémunérations, contrats recherche, congrès). Calcul du ratio paiements/remboursements.
> Exemple validé : FORXIGA / AstraZeneca → 158M€ remboursés, 32.6M€ versés aux médecins, ratio 16.8%

**3. Odissé × open-medic (Veille Épidémiologique)** — Signal grippe en temps réel × volumes de prescription historiques → prédiction automatique des prescriptions à venir pour Tamiflu, Amoxicilline, Ventoline, Doliprane.

### RAG pharmaceutique local

Système de question-réponse en langage naturel sur la base médicamenteuse :

```
"Quels médicaments contiennent de l'ibuprofène et sont remboursés ?"
→ Recherche sémantique dans ChromaDB → top 5 fiches → réponse factuelle
```

- **ChromaDB** — base vectorielle locale, indexation des 15 000 médicaments (compositions, SMR, DCI)
- **Ollama + Qwen** — LLM local pour la génération de réponses
- **nomic-embed-text** — modèle d'embeddings pour la recherche sémantique

---

## Interface

Frontend SPA (~3 200 lignes HTML/CSS/JS) avec 3 onglets principaux :

- **Médicaments** — table triable et filtrable, fiches complètes avec KPIs, conflits d'intérêts, volumes
- **Dashboard** — distribution SMR, top titulaires, top 5 volumes de vente
- **Veille Épidémiologique** — signaux Odissé temps réel + prédictions de prescriptions

---

## Architecture

```
api-pharma/
├── app.py                       # Flask — toutes les routes API
├── build_full_index.py          # Construction de l'index 15 000 médicaments (BDPM + open-medic)
├── pharma_rag.py                # RAG : indexation ChromaDB + Q&A avec Ollama
├── veille_epidemio.py           # Signaux Odissé × prédictions prescriptions
├── conflits_client.py           # Analyse Transparence Santé × BDPM
├── transparence_client.py       # Client API Transparence Santé
├── transparence_index.py        # Index local SQLite (2.9M enregistrements)
├── maladies_client.py           # Pathologies × médicaments × signaux
├── odisse_client.py             # Client API Odissé (Santé Publique France)
├── opendatasoft_client.py       # Client générique Opendatasoft (réutilisable)
├── acces_soins_client.py        # Scores accessibilité soins
├── rappelconso_client.py        # Client RappelConso (DGCCRF)
├── enriched_fiche.py            # Enrichissement fiche médicament à la volée
├── bdpm_collector.py            # Téléchargement fichiers BDPM
├── templates/index.html         # Frontend SPA
├── data/                        # Fichiers BDPM bruts (TSV)
├── static/maladies/             # Fiches cliniques par pathologie
└── top15000_medicaments.json    # Index principal pré-calculé
```

---

## Stack technique

| Composant | Technologie |
|-----------|-------------|
| Backend | Python / Flask |
| Base vectorielle | ChromaDB (local) |
| LLM local | Ollama + Qwen 4B |
| Embeddings | nomic-embed-text |
| Base relationnelle | SQLite (index Transparence Santé) |
| APIs | Opendatasoft (moteur commun), REST |
| Frontend | HTML / CSS / JS (vanilla, SPA) |

---

## Lancement

```bash
# Prérequis
pip install flask flask-cors requests chromadb

# Optionnel : RAG (nécessite Ollama installé)
ollama pull nomic-embed-text
ollama pull qwen4b-64k
python pharma_rag.py index

# Lancement
python app.py
# → http://localhost:5000
```

---

## Contexte

Projet construit par un pharmacien en reconversion vers l'IA. La connaissance métier (nomenclature BDPM, DCI, SMR/ASMR, logique de remboursement AM) a été déterminante pour identifier les bons croisements de données et produire des analyses pertinentes.

Le pattern Opendatasoft commun à toutes les APIs de santé publique françaises a été identifié et factorisé dans un client générique réutilisable — applicable à tout projet exploitant des données publiques FR.

---

## Licence

MIT
