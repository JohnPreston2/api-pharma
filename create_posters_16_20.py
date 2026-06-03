#!/usr/bin/env python3
"""Create pathology posters 16-20."""
import os

OUTPUT_DIR = "/home/user/api-pharma/posters"

CSS_COMMON = """
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  @page { size: A4 portrait; margin: 0; }
  body { font-family: 'Inter', Arial, sans-serif; width: 210mm; min-height: 297mm; margin: 0 auto; background: #fff; font-size: 7.5pt; color: #1a1a2e; line-height: 1.35; }
  .header { background: linear-gradient(135deg, var(--c1) 0%, var(--c2) 60%, var(--c3) 100%); padding: 9mm 8mm 7mm; display: grid; grid-template-columns: 1fr auto; align-items: center; gap: 6mm; position: relative; overflow: hidden; }
  .header::after { content: ''; position: absolute; right: -15mm; top: -15mm; width: 55mm; height: 55mm; border-radius: 50%; background: rgba(255,255,255,0.05); }
  .header h1 { font-size: 19pt; font-weight: 900; color: #fff; letter-spacing: -0.5px; line-height: 1; }
  .header .subtitle { font-size: 8pt; color: rgba(255,255,255,0.75); font-weight: 400; margin-top: 1.5mm; letter-spacing: 1.5px; text-transform: uppercase; }
  .header-stats { display: flex; gap: 4mm; }
  .stat-pill { background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.25); border-radius: 6px; padding: 3mm 4mm; text-align: center; }
  .stat-pill .val { font-size: 13pt; font-weight: 800; color: #fff; display: block; line-height: 1; }
  .stat-pill .lbl { font-size: 5.5pt; color: rgba(255,255,255,0.7); text-transform: uppercase; letter-spacing: 0.5px; margin-top: 1mm; }
  .tag-bar { background: var(--c1); padding: 2mm 8mm; display: flex; gap: 3mm; flex-wrap: wrap; }
  .tag { background: rgba(255,255,255,0.1); color: rgba(255,255,255,0.85); font-size: 5.5pt; padding: 0.8mm 2.5mm; border-radius: 20px; font-weight: 500; }
  .body-grid { display: grid; grid-template-columns: 55mm 1fr; gap: 0; padding: 5mm 8mm 4mm; column-gap: 5mm; }
  .section-label { font-size: 5.5pt; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; color: var(--c2); margin-bottom: 2mm; display: flex; align-items: center; gap: 1.5mm; }
  .section-label::before { content: ''; display: inline-block; width: 2.5mm; height: 2.5mm; background: var(--c2); border-radius: 50%; flex-shrink: 0; }
  .physio-card { background: var(--cl); border-radius: 7px; padding: 3mm; margin-bottom: 3mm; border-left: 3px solid var(--c2); }
  .cascade { display: flex; flex-direction: column; gap: 1.2mm; }
  .cascade-step { background: white; border-radius: 5px; padding: 1.8mm 2.5mm; font-size: 6.5pt; font-weight: 500; color: var(--c1); display: flex; align-items: center; gap: 2mm; box-shadow: 0 1px 3px rgba(0,0,0,0.06); }
  .cascade-arrow { text-align: center; color: var(--c2); font-size: 8pt; font-weight: 700; line-height: 1; }
  .targets-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5mm; margin-top: 2mm; }
  .target-box { background: white; border-radius: 5px; padding: 2mm; border-top: 2.5px solid var(--c2); }
  .target-box .t { font-size: 6pt; font-weight: 700; color: var(--c1); }
  .target-box .d { font-size: 5.5pt; color: #37474f; }
  .diag-card { background: #f4f6f8; border-radius: 7px; padding: 3mm; margin-bottom: 3mm; }
  .diag-row { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5mm; margin-bottom: 1.5mm; }
  .diag-item { background: white; border-radius: 5px; padding: 2mm 2.5mm; border-top: 2.5px solid var(--c2); }
  .diag-item .val { font-size: 8.5pt; font-weight: 800; color: var(--c2); line-height: 1; }
  .diag-item .lbl { font-size: 5.5pt; color: #37474f; margin-top: 0.5mm; }
  .drugs-col { display: flex; flex-direction: column; gap: 2.5mm; }
  .drug-class { border-radius: 7px; overflow: hidden; border: 1px solid #cfd8dc; }
  .drug-class-header { padding: 2mm 3mm; display: flex; align-items: center; justify-content: space-between; }
  .drug-class-header .name { font-size: 7pt; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px; }
  .drug-class-header .badge { font-size: 5pt; font-weight: 700; padding: 0.5mm 2mm; border-radius: 20px; text-transform: uppercase; }
  .drug-class-body { background: white; padding: 2mm 3mm; }
  .drug-row { display: grid; grid-template-columns: 32mm 1fr 1fr; gap: 1.5mm; padding: 1.2mm 0; border-bottom: 1px solid #cfd8dc; align-items: start; }
  .drug-row:last-child { border-bottom: none; }
  .drug-dci { font-weight: 700; font-size: 6.5pt; color: var(--c1); }
  .drug-dose { font-size: 6pt; color: #37474f; }
  .drug-watch { font-size: 6pt; color: #e65100; font-weight: 600; }
  .drug-watch::before { content: '⚠ '; }
  .drug-dci .princeps { display: block; font-style: italic; font-size: 5.5pt; color: #546e7a; font-weight: 400; margin-top: 0.3mm; }
  .drug-dci .vol-data { display: block; font-size: 5pt; font-weight: 700; color: rgba(0,0,0,0.38); margin-top: 0.2mm; letter-spacing: 0.2px; }
  .strategy-bar { margin: 3mm 8mm 0; background: linear-gradient(90deg, var(--c1), var(--c2)); border-radius: 7px; padding: 3mm 4mm; display: flex; align-items: center; gap: 3mm; }
  .strategy-bar .label { color: rgba(255,255,255,0.65); font-size: 5.5pt; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; white-space: nowrap; }
  .strategy-steps { display: flex; align-items: center; gap: 1.5mm; flex: 1; }
  .strat-step { background: rgba(255,255,255,0.12); border: 1px solid rgba(255,255,255,0.2); border-radius: 5px; padding: 1.5mm 2.5mm; text-align: center; flex: 1; }
  .strat-step .num { font-size: 5pt; color: rgba(255,255,255,0.6); text-transform: uppercase; }
  .strat-step .content { font-size: 6pt; font-weight: 700; color: white; margin-top: 0.5mm; }
  .strat-arrow { color: rgba(255,255,255,0.5); font-size: 9pt; font-weight: 700; }
  .nouveaute-bar { background: #ede7f6; border: 1px solid #ce93d8; border-radius: 6px; padding: 1.8mm 3mm; margin: 2mm 8mm 0; display: flex; align-items: flex-start; gap: 2mm; }
  .n-badge { background: #7b1fa2; color: white; font-size: 4.8pt; font-weight: 800; padding: 0.5mm 1.5mm; border-radius: 3px; white-space: nowrap; flex-shrink: 0; margin-top: 0.3mm; letter-spacing: 0.2px; }
  .n-text { font-size: 5.5pt; color: #4a148c; line-height: 1.35; }
  .n-text strong { font-weight: 700; color: #6a1b9a; }
  .footer-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 3mm; padding: 3mm 8mm 5mm; }
  .reflexes-card { background: #e8f5e9; border-radius: 7px; padding: 3mm; border-left: 3px solid #1b5e20; }
  .reflex-item { display: flex; gap: 2mm; align-items: flex-start; margin-bottom: 2mm; }
  .reflex-item:last-child { margin-bottom: 0; }
  .reflex-num { background: #1b5e20; color: white; font-size: 6pt; font-weight: 800; width: 4mm; height: 4mm; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0; margin-top: 0.3mm; }
  .reflex-text { font-size: 6pt; color: #1b5e20; font-weight: 500; }
  .inter-card { background: #fff3e0; border-radius: 7px; padding: 3mm; border-left: 3px solid #e65100; }
  .inter-item { padding: 1.5mm 0; border-bottom: 1px solid rgba(230,81,0,0.15); }
  .inter-item:last-child { border-bottom: none; }
  .inter-drug { font-size: 6.5pt; font-weight: 700; color: #e65100; }
  .inter-effect { font-size: 5.5pt; color: #bf360c; margin-top: 0.3mm; }
  .patient-card { background: #fafafa; border-radius: 7px; padding: 3mm; border: 1px solid #cfd8dc; }
  .patient-item { margin-bottom: 2mm; }
  .patient-item:last-child { margin-bottom: 0; }
  .speech-bubble { background: var(--cl); border-radius: 4px; padding: 1.5mm 2mm; font-size: 6pt; color: var(--c1); font-style: italic; font-weight: 500; }
  .speech-resp { font-size: 5.5pt; color: #37474f; padding: 1mm 2mm 0; font-weight: 500; }
  .speech-resp::before { content: '→ '; color: var(--c2); font-weight: 700; }
  .speech-hide { font-size: 5pt; color: #7f0000; background: #ffebee; border-radius: 3px; padding: 0.5mm 2mm; margin-top: 0.3mm; font-weight: 500; line-height: 1.3; }
  .speech-hide::before { content: '↳ '; font-weight: 800; color: #b71c1c; }
  .footer-strip { background: var(--c1); padding: 2mm 8mm; display: flex; justify-content: space-between; align-items: center; }
  .footer-strip span { color: rgba(255,255,255,0.5); font-size: 5pt; letter-spacing: 0.5px; }
  .footer-strip .brand { color: rgba(255,255,255,0.8); font-weight: 700; letter-spacing: 1px; font-size: 5.5pt; }
  @media print { body { width: 210mm; margin: 0; } * { -webkit-print-color-adjust: exact; print-color-adjust: exact; } }
"""

def make_poster(filename, title, subtitle, stats, tags,
                c1, c2, c3, cl, cm,
                physio_steps, target_boxes, diag_items, diag_note,
                drug_classes, ci_block,
                strat_label, strat_steps,
                nouveaute_text,
                reflexes, interactions, patient_items,
                footer_left, footer_right):

    stats_html = "".join(f'<div class="stat-pill"><span class="val">{v}</span><span class="lbl">{l}</span></div>' for v, l in stats)
    tags_html = "".join(f'<span class="tag">{t}</span>' for t in tags)
    physio_html = "".join(f'<div class="cascade-step">{s}</div>' + ('<div class="cascade-arrow">↓</div>' if i < len(physio_steps)-1 else '') for i, s in enumerate(physio_steps))
    targets_html = "".join(f'<div class="target-box"><div class="t">{t}</div><div class="d">{d}</div></div>' for t, d in target_boxes)
    diag_html = "".join(f'<div class="diag-item"><div class="val">{v}</div><div class="lbl">{l}</div></div>' for v, l in diag_items)

    drug_classes_html = ""
    for dc in drug_classes:
        cls_id = dc['cls']
        header_bg = dc.get('header_bg', cl)
        name_color = dc.get('name_color', c1)
        badge_bg = dc.get('badge_bg', c2)
        rows_html = ""
        for row in dc['rows']:
            rows_html += f"""
        <div class="drug-row">
          <div class="drug-dci">{row['dci']}<span class="princeps">{row['princeps']}</span><span class="vol-data">{row['vol']}</span></div>
          <div class="drug-dose">{row['dose']}</div>
          <div class="drug-watch">{row['watch']}</div>
        </div>"""
        drug_classes_html += f"""
    <div class="drug-class {cls_id}">
      <div class="drug-class-header" style="background:{header_bg};">
        <div class="name" style="color:{name_color};">{dc['name']}</div>
        <div class="badge" style="background:{badge_bg};color:white;">{dc['badge']}</div>
      </div>
      <div class="drug-class-body">{rows_html}
      </div>
    </div>"""

    strat_steps_html = ""
    for i, (num, content) in enumerate(strat_steps):
        strat_steps_html += f'<div class="strat-step"><div class="num">{num}</div><div class="content">{content}</div></div>'
        if i < len(strat_steps) - 1:
            strat_steps_html += '<div class="strat-arrow">›</div>'

    reflexes_html = "".join(f'<div class="reflex-item"><div class="reflex-num">{i+1}</div><div class="reflex-text">{r}</div></div>' for i, r in enumerate(reflexes))
    inter_html = "".join(f'<div class="inter-item"><div class="inter-drug">{d}</div><div class="inter-effect">{e}</div></div>' for d, e in interactions)
    patient_html = ""
    for bubble, hide, resp in patient_items:
        patient_html += f"""      <div class="patient-item"><div class="speech-bubble">{bubble}</div><div class="speech-hide">{hide}</div><div class="speech-resp">{resp}</div></div>
"""

    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>{title} — Fiche Officine</title>
<style>
  :root {{
    --c1: {c1}; --c2: {c2}; --c3: {c3};
    --cl: {cl}; --cm: {cm};
  }}
{CSS_COMMON}
</style>
</head>
<body>

<div class="header">
  <div>
    <h1>{title}</h1>
    <div class="subtitle">{subtitle}</div>
  </div>
  <div class="header-stats">
    {stats_html}
  </div>
</div>

<div class="tag-bar">
  {tags_html}
</div>

<div class="body-grid">
  <div>
    <div class="section-label">Physiopathologie</div>
    <div class="physio-card">
      <div class="cascade">
        {physio_html}
      </div>
      <div class="targets-grid">
        {targets_html}
      </div>
    </div>

    <div class="section-label">Diagnostic & Bilan</div>
    <div class="diag-card">
      <div class="diag-row">
        {diag_html}
      </div>
      <div style="background:var(--cl);border-radius:5px;padding:2mm;border-left:3px solid var(--c2);font-size:6pt;color:var(--c1);font-weight:600;">{diag_note}</div>
    </div>

    <div class="section-label">CI / Précautions ⛔</div>
    <div style="background:#ffebee;border-radius:7px;padding:3mm;border-left:3px solid #c62828;">
      {ci_block}
    </div>
  </div>

  <div class="drugs-col">
    <div class="section-label">Classes thérapeutiques</div>
    {drug_classes_html}
  </div>
</div>

<div class="strategy-bar">
  <div class="label">{strat_label}</div>
  <div class="strategy-steps">
    {strat_steps_html}
  </div>
</div>

<div class="nouveaute-bar">
  <span class="n-badge">🆕 NOUVEAUTÉS 2020–2026</span>
  <span class="n-text">{nouveaute_text}</span>
</div>

<div class="footer-grid">
  <div>
    <div class="section-label" style="color:#1b5e20;">3 Réflexes Officine</div>
    <div class="reflexes-card">
      {reflexes_html}
    </div>
  </div>
  <div>
    <div class="section-label" style="color:#e65100;">Interactions Majeures</div>
    <div class="inter-card">
      {inter_html}
    </div>
  </div>
  <div>
    <div class="section-label">Ce que dit le patient 🗣</div>
    <div class="patient-card">
{patient_html}    </div>
  </div>
</div>

<div class="footer-strip">
  <span>{footer_left}</span>
  <span class="brand">SANTÉVEILLE · OFFICINE</span>
  <span>{footer_right}</span>
</div>
</body>
</html>"""
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"✓ {filename}")


# ─────────────────────────────────────────
# 16. ECZÉMA / DERMATITE ATOPIQUE
# ─────────────────────────────────────────
make_poster(
    filename="eczema_DA_poster.html",
    title="Eczéma & Dermatite Atopique",
    subtitle="Fiche officine · Pathologie 16 · Pratique comptoir · 2026",
    stats=[("20%", "Enfants touchés"), ("Th2", "Réponse immunitaire"), ("Dupilumab", "Révolution 2017+")],
    tags=["Émollients = base quotidienne", "Dermocorticoïdes = crise", "Tacrolimus hors-zone visage seulement", "Dupilumab = DA modérée-sévère", "JAK inhibiteurs per os = formes sévères", "Règle des doigts (FTU)"],
    c1="#bf360c", c2="#e64a19", c3="#ff7043", cl="#fbe9e7", cm="#ffccbc",
    physio_steps=[
        "🧬 Mutation gène Filaggrine → défaut barrière cutanée",
        "🦠 Pénétration allergènes/microbes → activation Th2",
        "💥 IL-4, IL-13, IL-31 → inflammation + prurit intense",
        "🔄 Grattage → excoriation → surinfection → cercle vicieux"
    ],
    target_boxes=[("Prurit", "IL-31, histamine"), ("Xérose", "Barrière rompue"), ("Lichenification", "Grattage chronique"), ("Surinfection", "Staph aureus 90%")],
    diag_items=[("SCORAD", "Score sévérité 0-103"), ("IGA", "Index 0-4"), ("EASI", "Score étendue"), ("IgE totales", "Souvent élevées")],
    diag_note="📋 Critères Hanifin & Rajka · Culture cutanée si surinfection · Bilan allergo si formes sévères · Pas de bilan systématique",
    drug_classes=[
        {"cls": "cls-emol", "header_bg": "#fff3e0", "name_color": "#e65100", "badge_bg": "#bf360c",
         "name": "Émollients — Traitement de Fond Quotidien", "badge": "Base indispensable",
         "rows": [
             {"dci": "Dexpanthénol · Urée · Glycérol · Paraffine", "princeps": "Dexeryl · Atoderm · A-Derma Exomega · Lipikar",
              "vol": "📦 18M boîtes · 8-15€ · 200M€/an",
              "dose": "2x/j sur peau propre · Appliquer après bain/douche tiède", "watch": "Jamais sur peau infectée (favorise macération) · Parfums CI"},
         ]},
        {"cls": "cls-dc", "header_bg": "#fbe9e7", "name_color": "#bf360c", "badge_bg": "#e64a19",
         "name": "Dermocorticoïdes — Poussées", "badge": "Traitement poussée",
         "rows": [
             {"dci": "Hydrocortisone 1% · Désonide", "princeps": "Hydracort · Locapred · Tridésonit",
              "vol": "📦 6M tubes · 4,50€ · 27M€/an",
              "dose": "Classe I-II (faible) · Visage, plis · Nourrissons", "watch": "Classe adaptée à la zone et l'âge · Règle du doigt FTU"},
             {"dci": "Bétaméthasone · Mométasone", "princeps": "Diprosone · Elocom · Betneval",
              "vol": "📦 8M tubes · 5,80€ · 46M€/an",
              "dose": "Classe III (forte) · Corps adulte · 2 semaines max", "watch": "Atrophie cutanée si usage prolongé · Rebond si arrêt brutal"},
             {"dci": "Clobétasol propionate 0,05%", "princeps": "Dermoval · Clarelux mousse",
              "vol": "📦 2M tubes · 6,20€ · 12M€/an",
              "dose": "Classe IV (très forte) · Formes sévères résistantes", "watch": "Usage court · Maximum 50g/sem · Jamais visage · Risque Cushingien"},
         ]},
        {"cls": "cls-ic", "header_bg": "#e8f5e9", "name_color": "#1b5e20", "badge_bg": "#2e7d32",
         "name": "Inhibiteurs Calcineurine Topiques", "badge": "Hors corticoïdes",
         "rows": [
             {"dci": "Tacrolimus 0,03% / 0,1% · Pimécrolimus", "princeps": "Protopic · Elidel",
              "vol": "📦 2M tubes · 22€ · 44M€/an",
              "dose": "Tacrolimus 0,1% adulte · 0,03% enfant > 2 ans", "watch": "Brûlure initiale 1ère semaine · Phototoxicité → protection solaire · Pas longue durée sans pause"},
         ]},
        {"cls": "cls-dupil", "header_bg": "#f3e5f5", "name_color": "#4a148c", "badge_bg": "#6a1b9a",
         "name": "Dupilumab — Biothérapie Anti-IL-4/IL-13", "badge": "Modérée-Sévère",
         "rows": [
             {"dci": "Dupilumab", "princeps": "Dupixent 300 mg/2 mL stylo",
              "vol": "📦 remboursé 2017 adulte, 2022 enfant · 800-1200€/2 sem",
              "dose": "600 mg SC dose initiale puis 300 mg/2 sem", "watch": "Conjonctivite (20%) · Réaction injection site · Très efficace"},
         ]},
        {"cls": "cls-jak", "header_bg": "#e8eaf6", "name_color": "#1a237e", "badge_bg": "#283593",
         "name": "Inhibiteurs JAK Oraux — Formes Sévères", "badge": "Nouveau 2021+",
         "rows": [
             {"dci": "Baricitinib · Abrocitinib · Upadacitinib", "princeps": "Olumiant 2-4 mg · Cibinqo 100-200 mg · Rinvoq 15-30 mg",
              "vol": "📦 AMM 2021-2022 · 800-1500€/mois",
              "dose": "Baricitinib 4 mg/j · Abrocitinib 200 mg/j · Upadacitinib 30 mg/j", "watch": "Infections sévères · MACE · DVT · Bilan pré-traitement obligatoire · Herpes"},
         ]},
    ],
    ci_block="""<div style="font-size:6pt;color:#b71c1c;font-weight:600;margin-bottom:1.5mm;">⛔ Dermocorticoïdes forts visage → atrophie + télangiectasies → utiliser classe I-II seulement</div>
      <div style="font-size:6pt;color:#b71c1c;font-weight:600;margin-bottom:1.5mm;">⛔ Tacrolimus / pimécrolimus : CI < 2 ans · Phototoxicité → protection solaire pendant traitement</div>
      <div style="font-size:6pt;color:#b71c1c;font-weight:600;">⛔ JAK inhibiteurs : bilan pré-traitement (TB latente, NFS, bilan hépatique, sérologies) · CI infections actives</div>""",
    strat_label="Stratégie HAS 2022",
    strat_steps=[("Base", "Émollient quotidien"), ("Poussée légère", "DC classe I-II"), ("Poussée modérée", "DC classe III + émollient"), ("Sévère", "Dupilumab ou JAK-i")],
    nouveaute_text="<strong>Abrocitinib (Cibinqo)</strong> AMM 2022 · <strong>Upadacitinib (Rinvoq)</strong> AMM DA sévère 2022 · Dupilumab remboursé enfant ≥ 6 ans 2022 · Tralokinumab (Adtralza) anti-IL-13 AMM 2021 · Crisaborole (inhibiteur PDE4 topique) AMM EU 2020 enfant",
    reflexes=["FTU (Fingertip Unit) : 1 FTU = ~0,5g · Corps adulte = 30-40 FTU pour une application · Prescrire assez",
              "Règle du pouce pour sévérité : SCORAD > 25 = modéré · > 50 = sévère → indication biothérapie",
              "Poussée + suintement/croûtes jaunes/odeur → suspicion surinfection Staphylococcus aureus → dermato urgent"],
    interactions=[("Tacrolimus + CYP3A4 inhibiteurs (azolés)", "↑ Concentration tacrolimus systémique (faible mais réel si grande surface)"),
                  ("JAK-i + immunosuppresseurs", "Risque infectieux majeur → ne pas combiner corticoïdes systémiques"),
                  ("JAK-i + vaccins vivants", "CI vaccins vivants atténués sous JAK inhibiteurs · Mettre à jour avant"),
                  ("Dupilumab + vaccins", "Vaccins non vivants OK · Vaccins vivants : attendre évaluation bénéfice/risque")],
    patient_items=[
        ('"La crème cortisone je préfère éviter ça pour mon bébé"',
         "Dermocorticoïdes = traitement de référence des poussées · Classe adaptée = efficace et sûr · Peur corticostéroïdes = corticostérophobie très fréquente = 1ère cause d'échec",
         "DC classe I (hydrocortisone 1%) sur visage nourrisson = très sûr · Appliquer correctement les 5-7 premiers jours"),
        ('"Je mets la crème tous les jours mais ça revient toujours"',
         "DA = maladie chronique récidivante · AUCUN traitement ne guérit · Émollient quotidien = réduction des poussées · Grattage = entretient inflammation",
         "Émollient 2x/j entre les poussées · DC dès début poussée · Éviter allergènes déclenchants"),
        ('"On m\'a proposé Dupixent pour ma fille de 10 ans"',
         "Dupilumab remboursé DA modérée-sévère ≥ 6 ans depuis 2022 · Anti-IL-4/IL-13 = révolution thérapeutique · Conjonctivite chez 20% = EI fréquent",
         "Traitement efficace · Injection SC/2 semaines · Conjonctivite → collyres · Résultat visible en 4-8 semaines"),
        ('"J\'ai mis Protopic et j\'ai eu des brûlures"',
         "Brûlure, prurit initiale avec tacrolimus = normale les 7-10 premiers jours · Disparaît spontanément · Arrêt = dommage",
         "Normal les 1ères semaines · Persévérer · Si persiste > 2 semaines → reconsulter · Ne pas exposer au soleil"),
    ],
    footer_left="Eczéma · DA · Dermocorticoïdes · Dupilumab · JAK-inhibiteurs · BDPM 2026",
    footer_right="Pathologie 16 · 80/20 · Pratique comptoir"
)

# ─────────────────────────────────────────
# 17. POLYARTHRITE RHUMATOÏDE
# ─────────────────────────────────────────
make_poster(
    filename="polyarthrite_rhumato_poster.html",
    title="Polyarthrite Rhumatoïde",
    subtitle="Fiche officine · Pathologie 17 · Pratique comptoir · 2026",
    stats=[("1%", "Population adulte"), ("3:1", "Femmes/Hommes"), ("MTX", "Ancre du traitement")],
    tags=["Méthotrexate = 1ère ligne incontournable", "Acide folique J+2 après MTX", "Adalimumab biosimilaires disponibles", "JAK-i prudence CV et oncologique", "Jamais vaccin vivant sous biothérapie", "DAS28 cible de rémission"],
    c1="#37474f", c2="#546e7a", c3="#90a4ae", cl="#eceff1", cm="#cfd8dc",
    physio_steps=[
        "🧬 Activation lymphocytes T → cytokines pro-inflammatoires (TNF, IL-6, IL-17)",
        "💥 Synovite → destruction cartilage et os → érosions radiologiques",
        "🔗 Auto-anticorps : FR (facteur rhumatoïde) + ACPA (anti-CCP)",
        "📊 Score DAS28 : activité maladie · Cible : rémission ou faible activité"
    ],
    target_boxes=[("Petites articulat.", "MCF, IPP symétriques"), ("Atteinte systémique", "Nodules, poumons, cœur"), ("Biologie", "CRP, VS, NFS"), ("Radiologie", "Érosions, pincement")],
    diag_items=[("DAS28", "< 2.6 = rémission"), ("ACPA", "Anti-CCP spécifique"), ("FR", "Facteur rhumatoïde"), ("CRP/VS", "Inflammation active")],
    diag_note="📋 FR + anti-CCP · Radiographies mains/pieds · Bilan pré-biothérapie : IGRA, NFS, BHC, sérologies",
    drug_classes=[
        {"cls": "cls-mtx", "header_bg": "#eceff1", "name_color": "#37474f", "badge_bg": "#546e7a",
         "name": "Méthotrexate — Ancre Thérapeutique", "badge": "1ère ligne",
         "rows": [
             {"dci": "Méthotrexate 2,5 mg · 10 mg · 25 mg/mL SC", "princeps": "Novatrex · Methofar · Imeth · Metoject SC",
              "vol": "📦 4M boîtes · 8,50€ · 34M€/an",
              "dose": "Débuter 7,5-10 mg/sem · Titrer jusqu'à 20-25 mg/sem", "watch": "Acide folique J+2 · Alcool strictement CI · Hépatotoxicité · NFS mensuelle · CI grossesse"},
             {"dci": "Acide folique 5 mg", "princeps": "Spéciafoldine · Génériques",
              "vol": "📦 prescrit systématiquement avec MTX",
              "dose": "5 mg J+2 après la prise de MTX (2j après)", "watch": "Ne PAS le jour du MTX → réduit l'efficacité"},
         ]},
        {"cls": "cls-dmard", "header_bg": "#e0f2f1", "name_color": "#004d40", "badge_bg": "#00695c",
         "name": "csDMARDs — Autres Conventionnels", "badge": "Alternatives ou combo",
         "rows": [
             {"dci": "Léflunomide · Hydroxychloroquine · Sulfasalazine", "princeps": "Arava · Plaquenil · Salazopyrine",
              "vol": "📦 1,5M boîtes combo · 9-25€",
              "dose": "Léflunomide 20 mg/j · Hydroxychloroquine 400 mg/j", "watch": "Léflunomide : washout si grossesse (demi-vie 2 ans) · Plaquenil : rétinopathie (fond d'œil/an)"},
         ]},
        {"cls": "cls-antitnf", "header_bg": "#fff3e0", "name_color": "#e65100", "badge_bg": "#bf360c",
         "name": "Anti-TNFα — 1ères Biothérapies", "badge": "MTX insuffisant",
         "rows": [
             {"dci": "Adalimumab · Étanercept · Infliximab", "princeps": "Humira (+ 14 biosimilaires) · Enbrel · Remicade",
              "vol": "📦 adalimumab 150K patients · 800-1500€/mois",
              "dose": "Adalimumab 40 mg SC/2 sem · Étanercept 50 mg SC/sem", "watch": "Réactivation TB (IGRA avant) · Infections sévères · Démyélinisation · Insuffisance cardiaque"},
             {"dci": "Certolizumab · Golimumab", "princeps": "Cimzia · Simponi",
              "vol": "📦 remboursé PR MTX-résistante",
              "dose": "Certolizumab 200 mg/2 sem · Golimumab 50 mg/mois", "watch": "Certolizumab : autorisé grossesse (pas transfert placentaire)"},
         ]},
        {"cls": "cls-autre-bio", "header_bg": "#f3e5f5", "name_color": "#4a148c", "badge_bg": "#6a1b9a",
         "name": "Autres Biothérapies — Anti-IL6 / Anti-CD20", "badge": "2ème ligne bio",
         "rows": [
             {"dci": "Tocilizumab · Sarilumab (anti-IL-6R)", "princeps": "Roactemra · Kevzara",
              "vol": "📦 remboursé PR réfractaire · 1200€/mois",
              "dose": "Tocilizumab 8 mg/kg IV/4 sem ou 162 mg SC/sem", "watch": "Masque fièvre infectieuse · Perforations digestives · Hyperlipidémie"},
             {"dci": "Rituximab (anti-CD20)", "princeps": "Mabthera · Truxima biosimilaire",
              "vol": "📦 1000 mg x2 (J1+J15)/6 mois",
              "dose": "1000 mg IV x2 à 15j d'intervalle / 6 mois", "watch": "Hypoglobulinémie progressive · Infections · Vaccins avant traitement"},
         ]},
        {"cls": "cls-jak-pr", "header_bg": "#e8eaf6", "name_color": "#1a237e", "badge_bg": "#283593",
         "name": "Inhibiteurs JAK Oraux", "badge": "Attention sécurité",
         "rows": [
             {"dci": "Baricitinib · Tofacitinib · Upadacitinib", "princeps": "Olumiant 4mg · Xeljanz 5mg · Rinvoq 15mg",
              "vol": "📦 remboursé PR réfractaire · 1000-1500€/mois",
              "dose": "Baricitinib 4 mg/j · Tofacitinib 5 mg x2/j", "watch": "MACE, DVT, cancers → prudence > 65 ans, ATCD CV/cancer · Herpès zona · Bilan NFS"},
         ]},
    ],
    ci_block="""<div style="font-size:6pt;color:#b71c1c;font-weight:600;margin-bottom:1.5mm;">⛔ MTX : CI grossesse (tératogène) · CI alcool · CI IRC sévère · Alcool même occasionnel = hépatotoxicité</div>
      <div style="font-size:6pt;color:#b71c1c;font-weight:600;margin-bottom:1.5mm;">⛔ Biothérapies + vaccins vivants : CI absolue (rougeole, BCG, fièvre jaune, varicelle)</div>
      <div style="font-size:6pt;color:#b71c1c;font-weight:600;">⛔ JAK-i : pas chez patients > 65 ans avec ATCD CV ou cancer → lettre EMA 2023 restreint utilisation</div>""",
    strat_label="Stratégie EULAR 2022",
    strat_steps=[("Précoce", "MTX ± HCQ + corticoïdes"), ("MTX insuffisant", "Anti-TNF ou anti-IL6"), ("Bio inefficace", "Switch bio ou JAK-i"), ("Rémission", "Déescalade possible")],
    nouveaute_text="<strong>Biosimilaires adalimumab</strong> (14 commercialisés en France, remboursés à parité) depuis 2018-2023 · <strong>Lettre EMA 2023</strong> : JAK inhibiteurs - restriction chez patients > 65 ans / ATCD CV / cancer / tabac · Filgotinib (Jyseleca) retiré USA mais maintenu EU · Ozoralizumab (nano-anticorps) AMM Japon",
    reflexes=["MTX : acide folique J+2 obligatoire (jamais le même jour) · NFS + BHC mensuel la 1ère année · Surveiller alcool",
              "Avant tout anti-TNF/biothérapie : IGRA (tuberculose latente) + sérologies VHB + VHC + bilan NFS/BHC",
              "Biothérapie + fièvre : arrêter le traitement et consulter en urgence (masque les signes d'infection)"],
    interactions=[("MTX + AINS (ibuprofène)", "↑ Toxicité MTX par compétition tubulaire · Paracétamol préférable"),
                  ("MTX + cotrimoxazole (Bactrim)", "Antifolate additif → pancytopénie · CI ou surveillance rapprochée"),
                  ("MTX + alcool", "Hépatotoxicité additive → CI · Même une bière/semaine risquée"),
                  ("Leflunomide + MTX", "Hépatotoxicité additionnelle → BHC obligatoire tous les 2 mois")],
    patient_items=[
        ('"Je n\'ai pas pris acide folique cette semaine"',
         "Acide folique réduit les EI digestifs et hématologiques du MTX SANS réduire son efficacité · J+2 = 2 jours après MTX",
         "Important de le prendre régulièrement · PAS le même jour que le MTX (réduit efficacité) · J+2"),
        ('"J\'ai de la fièvre sous Humira, j\'attends le médecin lundi"',
         "Biothérapies (anti-TNF) masquent la fièvre et les signes d'infection → risque sepsis méconnu → urgence médicale",
         "Urgences immédiates · Arrêt biothérapie · Infection sous biothérapie = urgence vitale"),
        ('"On me parle de biosimilaire d\'Humira, c\'est pareil ?"',
         "14 biosimilaires adalimumab commercialisés France · Bioéquivalents prouvés · Même efficacité et sécurité · Prix réduit 30-40%",
         "Oui, bioéquivalent cliniquement · Peut se faire sous surveillance rhumatologue · Économise le système de santé"),
        ('"J\'ai commencé le Plaquenil, dois-je consulter l\'ophtalmologue ?"',
         "Hydroxychloroquine → rétinopathie rare (1-2%) mais irréversible si dépistage tardif · Fond d'œil annuel recommandé",
         "Fond d'œil basal puis annuel à partir de 5 ans de traitement · Signaler au rhumatologue"),
    ],
    footer_left="PR · Méthotrexate · Anti-TNF · JAK-inhibiteurs · Biothérapies · BDPM 2026",
    footer_right="Pathologie 17 · 80/20 · Pratique comptoir"
)

# ─────────────────────────────────────────
# 18. ADDICTOLOGIE (TABAC, ALCOOL, OPIOÏDES)
# ─────────────────────────────────────────
make_poster(
    filename="addictologie_poster.html",
    title="Addictologie : Tabac · Alcool · Opioïdes",
    subtitle="Fiche officine · Pathologie 18 · Pratique comptoir · 2026",
    stats=[("13M", "Fumeurs France"), ("TSN", "Remboursé 150€/an"), ("CSAPA", "Centres addiction")],
    tags=["TNS remboursé 150€/an sur prescription", "Champix (varénicline) de retour 2024", "Buprénorphine HD = TAOD opioïdes", "Nalméfène = réduction consommation alcool", "Entretien motivationnel comptoir", "Pas de jugement = règle d'or"],
    c1="#004d40", c2="#00695c", c3="#26a69a", cl="#e0f2f1", cm="#b2dfdb",
    physio_steps=[
        "🧠 Nicotine/alcool/opioïdes → activation circuits mésolimbiques dopaminergiques",
        "⚡ Libération dopamine → renforcement positif · Dépendance psychologique",
        "🔄 Neuroadaptation → dépendance physique · Syndrome sevrage si arrêt",
        "📊 CAGE/AUDIT (alcool) · Fagerström (tabac) · Score CRAFt ados"
    ],
    target_boxes=[("Fagerström", "Score dép. tabac 0-10"), ("AUDIT-C", "Alcool 3 questions"), ("CIWA", "Sevrage alcool"), ("Score Dreyfus", "Intoxication aiguë")],
    diag_items=[("Fagerström > 5", "Forte dépendance nicotine"), ("AUDIT-C > 3", "Consommation risque"), ("CAGE ≥ 2", "Dépendance alcool"), ("CO expiré", "Mesure sevrage tabac")],
    diag_note="📋 CO expiré par alcootest tabac · Bilan hépatique alcool · NFS · Créatinine · GT · Test de grossesse si possible",
    drug_classes=[
        {"cls": "cls-tsn", "header_bg": "#e0f2f1", "name_color": "#004d40", "badge_bg": "#00695c",
         "name": "Substituts Nicotiniques (TNS) — Tabac", "badge": "1ère ligne tabac",
         "rows": [
             {"dci": "Nicotine transdermique (patchs)", "princeps": "Nicorette patch · Niquitin · Nicotinell · Generiques",
              "vol": "📦 8M boîtes/an · 12-18€ · 130M€/an",
              "dose": "7-21 mg/16h ou 24h · Durée 8-12 semaines · Titration selon Fagerström", "watch": "Rougeur sous patch · Rêves intenses si 24h → retirer la nuit · CI IFT récent (4 sem)"},
             {"dci": "Nicotine orale (gommes, pastilles, inhalateur)", "princeps": "Nicorette 2-4 mg gommes · Niquitin pastilles",
              "vol": "📦 6M boîtes/an · 8-12€ · 70M€/an",
              "dose": "Gomme 2 mg (< 20 cig/j) ou 4 mg (> 20 cig/j) · 8-12 sem", "watch": "Technique de mâchage stop-and-park · Inhalateur en cas de gestuelle"},
         ]},
        {"cls": "cls-vareni", "header_bg": "#fff8e1", "name_color": "#f57f17", "badge_bg": "#f9a825",
         "name": "Varénicline — Champix", "badge": "Retour 2024",
         "rows": [
             {"dci": "Varénicline", "princeps": "Champix 0,5 mg / 1 mg",
              "vol": "📦 Retiré 2021 (nitrosamines) · Retour prévu 2024",
              "dose": "0,5 mg/j sem 1 · 0,5 mg x2/j sem 2 · 1 mg x2/j sem 3-12", "watch": "Nausées (prendre avec repas) · Rêves inhabituels · Surveillance humeur (dépression rare)"},
         ]},
        {"cls": "cls-alcool", "header_bg": "#fce4ec", "name_color": "#880e4f", "badge_bg": "#ad1457",
         "name": "Pharmacothérapie — Alcool", "badge": "Dépendance alcool",
         "rows": [
             {"dci": "Acamprosate", "princeps": "Aotal 333 mg",
              "vol": "📦 400K traitements/an · 28€/mois",
              "dose": "2 cp x3/j (poids > 60 kg) · Dès sevrage · 12 mois", "watch": "Prise si abstinence · Inefficace si rechute · Bien toléré · Diarrhée"},
             {"dci": "Naltrexone orale", "princeps": "Revia 50 mg · Naltrexone Génériques",
              "vol": "📦 200K traitements/an · 45€/mois",
              "dose": "50 mg/j · Réduit le craving et l'effet récompense", "watch": "CI si traitement opioïde en cours (précipite sevrage) · Hépatotoxique doses élevées"},
             {"dci": "Nalméfène", "princeps": "Selincro 18 mg",
              "vol": "📦 100K traitements · 80€/mois",
              "dose": "18 mg PRN avant consommation · Réduction (pas abstinence)", "watch": "Nausées · Insomnie · Pas pour abstinence totale"},
         ]},
        {"cls": "cls-bup", "header_bg": "#f3e5f5", "name_color": "#4a148c", "badge_bg": "#6a1b9a",
         "name": "Traitement Substitution Opioïdes (TAOD)", "badge": "Dépendance opioïdes",
         "rows": [
             {"dci": "Buprénorphine Haut Dosage", "princeps": "Subutex 2-8 mg · BHD génériques",
              "vol": "📦 3,5M boîtes · 8-25€ · 75M€/an",
              "dose": "Sublingual 2-24 mg/j · Titration progressive", "watch": "Interactions benzodiazépines (dépression respi) · Détournement IV risque"},
             {"dci": "Buprénorphine + Naloxone", "princeps": "Suboxone 2/0,5 mg · 8/2 mg",
              "vol": "📦 1,5M boîtes · 15-35€",
              "dose": "SL 4-24 mg/j buprénorphine · Naloxone antagonise si IV", "watch": "Naloxone SL inactive (faible biodispo) → prévient injection IV"},
             {"dci": "Méthadone sirop", "princeps": "Méthadone AP-HP 5-60 mg/mL",
              "vol": "📦 dispensation quotidienne · 1,80€/j",
              "dose": "Démarrage CSAPA/hôpital obligatoire · Dispensation stricte", "watch": "QT long · Interactions dépresseurs SNC · Diluer en sirop (prévient IV)"},
         ]},
    ],
    ci_block="""<div style="font-size:6pt;color:#b71c1c;font-weight:600;margin-bottom:1.5mm;">⛔ Naltrexone CI si opioïde en cours (morphine, codéine, tramadol) → précipite sevrage brutal</div>
      <div style="font-size:6pt;color:#b71c1c;font-weight:600;margin-bottom:1.5mm;">⛔ BHD + benzodiazépines → dépression respiratoire · Association mortelle documentée → signaler médecin</div>
      <div style="font-size:6pt;color:#b71c1c;font-weight:600;">⛔ Méthadone + QT long (antifongiques azolés, macrolides, antipsychotiques) → torsade de pointes</div>""",
    strat_label="Stratégie officine",
    strat_steps=[("Repérage", "Fagerström/AUDIT-C"), ("Intervention courte", "5 min, sans jugement"), ("Pharmacothérapie", "TNS + accompagnement"), ("Orientation", "CSAPA si besoin")],
    nouveaute_text="<strong>Varénicline (Champix)</strong> retiré 2021 pour nitrosamines · Retour sur le marché FR attendu 2024 avec nouvelle formulation · <strong>TNS remboursé 150€/an</strong> sur ordonnance depuis 2019 · Bupropion (Zyban) toujours disponible · Cytisine (Tabex) AMM Europe 2023 (alternative naturelle varénicline)",
    reflexes=["TNS remboursé 150€/an : proposer prescription · Patch + forme orale = meilleure efficacité (+ 30%)",
              "BHD + benzo = association mortelle documentée → toujours vérifier l'ordonnance complète du patient TAOD",
              "Entretien motivationnel : pas de jugement · 'Qu'est-ce qui vous ferait changer ?' > 'vous devriez arrêter'"],
    interactions=[("BHD/Méthadone + benzodiazépines", "Dépression respiratoire mortelle → contre-indication relative, signaler médecin"),
                  ("Méthadone + CYP3A4 inhibiteurs (azolés, macrolides)", "↑ Méthadone → torsade de pointes · ECG avant"),
                  ("Naltrexone + opioïdes (morphine, codéine)", "Précipite sevrage brutal dans les 30 min → CI"),
                  ("TNS patch + tabac", "Double intoxication nicotinique → HTA, tachycardie · Arrêt tabac obligatoire avec patch")],
    patient_items=[
        ('"J\'essaie d\'arrêter de fumer mais les patchs m\'ont pas aidé"',
         "TNS seuls = 15-20% abstinence à 6 mois · Combinaison patch + forme orale = 25-30% · Varénicline = 30-35% · Échec = sous-dosage souvent",
         "Augmenter dose ou combiner patch + gomme · Orientation tabacologue · Champix si retour marché"),
        ('"Mon fils prend Subutex, il me demande une semaine de stock"',
         "BHD = stupéfiant en pratique · Dispensation hebdomadaire max sans ordonnance type · Délivrance prolongée possible sur ordonnance spéciale",
         "Délivrance selon ordonnance · Maximum légal précisé sur l'ordonnance · Pas de stock au domicile"),
        ('"J\'ai arrêté l\'alcool tout seul d\'un coup, je tremble"',
         "Sevrage alcool brutal peut être MORTEL (épilepsie, délirium tremens) si dépendance sévère → urgence médicale",
         "Urgences immédiates si dépendance sévère · Sevrage alcool doit être médicalisé · Ne jamais conseiller l'arrêt brutal"),
        ('"Est-ce que Suboxone c\'est mieux que Subutex ?"',
         "Suboxone = buprénorphine + naloxone · Naloxone inactive par voie SL → prévient usage IV (naloxone active = précipite sevrage)",
         "Suboxone préféré si risque injection · Subutex si SL strict ou certaines situations · Décision médicale"),
    ],
    footer_left="Tabac · Alcool · Opioïdes · TNS · BHD · Nalméfène · Varénicline · BDPM 2026",
    footer_right="Pathologie 18 · 80/20 · Pratique comptoir"
)

# ─────────────────────────────────────────
# 19. MÉNOPAUSE
# ─────────────────────────────────────────
make_poster(
    filename="menopause_poster.html",
    title="Ménopause & THS",
    subtitle="Fiche officine · Pathologie 19 · Pratique comptoir · 2026",
    stats=[("51 ans", "Âge moyen ménopause"), ("THS", "Bénéfices > risques confirmés"), ("80%", "Femmes avec symptômes")],
    tags=["THS = estradiol transdermique + progestérone naturelle", "Progestérone naturelle ≠ progestatifs synthétiques", "Estradiol seul si hystérectomie", "THS CI si cancer sein/endomètre", "Bouffées chaleur = signe cardinal", "Réévaluation annuelle obligatoire"],
    c1="#6a1b9a", c2="#8e24aa", c3="#ce93d8", cl="#f3e5f5", cm="#e1bee7",
    physio_steps=[
        "🧬 Ménopause = arrêt définitif ovulation → chute estradiol et progestérone",
        "🌡️ Bouffées chaleur : déréglementation thermorégulation centrale (hypothalamus)",
        "🦴 Carence œstrogénique → accélération perte osseuse × 3-5 pendant 5-10 ans",
        "💧 Atrophie uro-génitale : sécheresse vaginale, dyspareunie, incontinence"
    ],
    target_boxes=[("Vasomoteur", "Bouffées chaleur, sueurs"), ("Osseux", "Ostéoporose accélérée"), ("Génital", "Sécheresse, dyspareunie"), ("Cognitif", "Humeur, mémoire, sommeil")],
    diag_items=[("FSH > 40", "UI/L (post-ménopause)"), ("Estradiol", "< 20 pg/mL"), ("Aménorrhée", "12 mois consécutifs"), ("Score Kupperman", "Sévérité symptômes")],
    diag_note="📋 Pas de dosage systématique si > 50 ans + aménorrhée 12 mois · FSH si doute · Mammographie à jour · TA · Bilan lipidique",
    drug_classes=[
        {"cls": "cls-e2trans", "header_bg": "#f3e5f5", "name_color": "#6a1b9a", "badge_bg": "#8e24aa",
         "name": "Estradiol Transdermique — Voie Préférée", "badge": "Voie trans = référence",
         "rows": [
             {"dci": "Estradiol patch (25-100 mcg/j)", "princeps": "Vivelledot · Dermestril · Estraderm · Menorest",
              "vol": "📦 3M boîtes · 9€ · 27M€/an",
              "dose": "50-75 mcg/j · Changement x2/sem · Fesse, ventre", "watch": "Irritation locale · Pas de 1er passage hépatique (avantage) · CI thrombose"},
             {"dci": "Estradiol gel", "princeps": "Oestrogel 0,75 mg/dose · Estreva gel",
              "vol": "📦 4M boîtes · 8€ · 32M€/an",
              "dose": "1-2 doses/j sur bras/épaules · Laisser sécher", "watch": "Transfert par contact cutané (enfants, partenaire) → couvrir"},
         ]},
        {"cls": "cls-prog-nat", "header_bg": "#e8f5e9", "name_color": "#1b5e20", "badge_bg": "#2e7d32",
         "name": "Progestérone Naturelle — Associée Obligatoire (utérus)", "badge": "Protection endomètre",
         "rows": [
             {"dci": "Progestérone micronisée", "princeps": "Utrogestan 100-200 mg · Progestan 100-200 mg",
              "vol": "📦 5M boîtes · 5,50€ · 28M€/an",
              "dose": "200 mg/j HS pendant 12-14j/mois (séquentielle) ou 100 mg/j continu", "watch": "Sédation légère (HS = avantage pour sommeil) · Somnolence si PO jour · Voie vaginale possible"},
         ]},
        {"cls": "cls-e2oral", "header_bg": "#fff8e1", "name_color": "#f57f17", "badge_bg": "#f9a825",
         "name": "Estradiol Oral — Alternative", "badge": "Si patch mal toléré",
         "rows": [
             {"dci": "Estradiol valérate oral · Estradiol hemihydrate", "princeps": "Provames 1-2 mg · Estrofem",
              "vol": "📦 1,5M boîtes · 5,20€ · 8M€/an",
              "dose": "1-2 mg/j per os", "watch": "1er passage hépatique → ↑ SHBG · ↑ risque thrombose vs transdermique · Moins recommandé"},
         ]},
        {"cls": "cls-local", "header_bg": "#fce4ec", "name_color": "#880e4f", "badge_bg": "#ad1457",
         "name": "Traitement Local — Atrophie Uro-génitale", "badge": "Sécheresse vaginale",
         "rows": [
             {"dci": "Estriol local · Promestriène", "princeps": "Physiogine crème/ovules · Colpotrophine 1% crème",
              "vol": "📦 2M boîtes · 7,80€ · 16M€/an",
              "dose": "Estriol 0,5 mg crème ou ovule · 2-3x/sem", "watch": "Absorption systémique minime · Utilisable si THS CI (sauf cancer sein sous discussion) · Lubrifiant si refus hormoné"},
             {"dci": "Ospémifène (SERM oral)", "princeps": "Senshio 60 mg",
              "vol": "📦 AMM 2015 · non remboursé",
              "dose": "60 mg/j PO pour dyspareunie", "watch": "Bouffées chaleur paradoxales · CI cancer sein hormonodépendant"},
         ]},
    ],
    ci_block="""<div style="font-size:6pt;color:#b71c1c;font-weight:600;margin-bottom:1.5mm;">⛔ THS CI : cancer du sein actuel ou passé (hormonodépendant) · ATCD EP/TVP sévère · Saignements génitaux inexpliqués</div>
      <div style="font-size:6pt;color:#b71c1c;font-weight:600;margin-bottom:1.5mm;">⛔ Estrogènes oraux > transdermiques pour risque thrombose → voie transdermique recommandée en 1ère intention</div>
      <div style="font-size:6pt;color:#b71c1c;font-weight:600;">⛔ Progestatifs synthétiques (noréthistérone, médroxyprogestérone) → risque cancer sein > progestérone naturelle</div>""",
    strat_label="Stratégie HAS/IMS 2023",
    strat_steps=[("Symptômes modérés", "Traitement local seul"), ("THS séquentiel", "E2 trans + progest 12j/mois"), ("THS continu", "E2 + progest continu"), ("Hystérectomie", "Estradiol seul suffit")],
    nouveaute_text="<strong>Réévaluation THS 2022-2023</strong> : bénéfices confirmés sur symptômes + os · Risque cancer sein faible si progestérone naturelle transdermique · <strong>Voie transdermique estradiol préférée</strong> (moindre risque thrombose) · <strong>Progestérone naturelle</strong> (Utrogestan) = standard (≠ progestatifs synthétiques) · Traitements botanique : phytoestrogènes (isoflavones) efficacité limitée",
    reflexes=["THS = estradiol transdermique + progestérone NATURELLE (pas synthétique) → meilleur profil bénéfice/risque",
              "Mammographie à jour obligatoire avant THS · Réévaluation annuelle avec médecin",
              "Gel estradiol : laisser sécher, couvrir bras, éviter contact peau à peau (enfants, partenaire) les 1ères heures"],
    interactions=[("THS + inducteurs enzymatiques (rifampicine, CBZ)", "↓ Efficacité THS estrogènes · Adaptation dose"),
                  ("Estradiol oral + anticoagulants", "↑ Facteurs coagulation (1er passage hépatique) → surveiller INR"),
                  ("THS + tamoxifène (traitement cancer sein)", "Antagonisme thérapeutique CI · Jamais concomitant"),
                  ("Progestérone + alcool", "↑ Sédation · Somnolence potentialisée si prise vespérale")],
    patient_items=[
        ('"J\'ai des bouffées de chaleur terribles, le médecin ne veut pas me mettre sous THS"',
         "THS contre-indication principale = cancer sein personnel · Sans ATCD cancer, bénéfice > risque est confirmé par études récentes 2022-2023",
         "Discuter avec médecin · Critères CI précis · Souvent peur exagérée · Demander réévaluation"),
        ('"Ma gynécologue me donne Utrogestan, c\'est bien ?"',
         "Progestérone naturelle micronisée = meilleur profil risque cancer sein vs progestatifs synthétiques (lévonorgestrel, médroxyprogestérone) · Standard actuel",
         "Oui, Utrogestan est la référence actuelle · Progestérone naturelle = moins de risque cancer sein que les anciens progestatifs"),
        ('"J\'utilise Oestrogel mais mon mari dit que ça l\'affecte"',
         "Estradiol gel = transfert possible par contact cutané → concerne partenaire et enfants en bas âge si contact juste après application",
         "Laisser sécher 5 min · Couvrir le bras avec vêtement · Aucun risque si gel sec"),
        ('"J\'ai 62 ans, ça fait 10 ans que je prends THS, il faut arrêter ?"',
         "Durée THS = individuelle · Au-delà de 5-7 ans : réévaluation bénéfice/risque mais pas de limite absolue si bénéfice clair et surveillance correcte",
         "Pas d'arrêt automatique · Réévaluation annuelle avec médecin · Mammographie à jour · Décision partagée"),
    ],
    footer_left="Ménopause · THS · Estradiol · Progestérone · Utrogestan · BDPM 2026",
    footer_right="Pathologie 19 · 80/20 · Pratique comptoir"
)

# ─────────────────────────────────────────
# 20. GOUTTE
# ─────────────────────────────────────────
make_poster(
    filename="goutte_poster.html",
    title="Goutte & Hyperuricémie",
    subtitle="Fiche officine · Pathologie 20 · Pratique comptoir · 2026",
    stats=[("5%", "Adultes français"), ("Uricémie", "Cible < 360 µmol/L"), ("Allopurinol", "1ère ligne absolu")],
    tags=["Allopurinol = 1ère ligne hypo-uricémiant", "Fébuxostat = prudence CV", "Colchicine = crise en 1ère ligne", "Pas d'AINS si IRC", "Uratie à jeun pour diagnostic", "Alcool et viande rouge = déclencheurs"],
    c1="#4e342e", c2="#6d4c41", c3="#a1887f", cl="#efebe9", cm="#d7ccc8",
    physio_steps=[
        "🧬 Hyperuricémie → saturation plasma → cristaux urate mono-sodique (MSU)",
        "🦴 Dépôt cristaux dans articulations, bourses, tendons (tophus)",
        "💥 Macrophages → phagocytose MSU → NLRP3 inflammasome → IL-1β",
        "🔥 Inflammation intense, brutale, nocturne → classique gros orteil (métatarso-phalangienne)"
    ],
    target_boxes=[("Métatarso-phalang.", "Hallux (grosse orteil)"), ("Cheville/genou", "Crises sévères"), ("Tophus", "Dépôts chroniques"), ("Rein", "Lithiases urates")],
    diag_items=[("Uricémie", "> 420 µmol/L = risque"), ("Ponction art.", "Cristaux MSU confirmés"), ("CRP/VS", "Inflammation crise"), ("Créatinine", "Ajustement doses")],
    diag_note="📋 Uricémie à distance de la crise (faussement basse pendant) · Créatinine · Ponction si doute diagnostic · Imagerie si tophus",
    drug_classes=[
        {"cls": "cls-crise", "header_bg": "#fbe9e7", "name_color": "#bf360c", "badge_bg": "#e64a19",
         "name": "Traitement de la Crise — Dès les Premiers Signes", "badge": "Urgence J0",
         "rows": [
             {"dci": "Colchicine", "princeps": "Colchicine Opocalcium 1 mg · Colchimax",
              "vol": "📦 2M boîtes · 3,80€ · 8M€/an",
              "dose": "1 mg dès la crise · puis 0,5 mg 1h après · Max 3 mg J1", "watch": "Diarrhée dose-dépendante · CI IRC sévère (DFG < 30) · Interaction puissante CYP3A4"},
             {"dci": "AINS (ibuprofène, indométacine, naproxène)", "princeps": "Advil 400 mg · Indocid · Apranax",
              "vol": "📦 AINS crise goutte large usage",
              "dose": "Ibuprofène 400-600 mg x3/j · Naproxène 500 mg x2/j · 5-7j", "watch": "CI IRC, ulcère, insuffisance cardiaque, anticoagulants · Prendre avec repas"},
             {"dci": "Corticoïdes si CI aux 2 autres", "princeps": "Cortancyl 20-30 mg · Methylprednisolone IV",
              "vol": "📦 Prednisone 20-40 mg/j PO · 5 jours",
              "dose": "Prednisone 20-30 mg/j décroissant sur 5-7j", "watch": "Rebond à l'arrêt · CI diabète décompensé, infection locale"},
         ]},
        {"cls": "cls-allo", "header_bg": "#efebe9", "name_color": "#4e342e", "badge_bg": "#6d4c41",
         "name": "Allopurinol — Hypo-uricémiant 1ère Ligne", "badge": "Standard",
         "rows": [
             {"dci": "Allopurinol", "princeps": "Zyloric 100-300 mg · Génériques",
              "vol": "📦 4M boîtes · 4,20€ · 17M€/an",
              "dose": "Débuter 100 mg/j · Titrer selon uricémie · Max 900 mg/j", "watch": "JAMAIS pendant crise (déclenche/prolonge) · Démarrer 3-6 sem après crise · SJS rare (tester HLA-B*58:01 Asie)"},
         ]},
        {"cls": "cls-febuxo", "header_bg": "#e8eaf6", "name_color": "#1a237e", "badge_bg": "#283593",
         "name": "Fébuxostat — 2ème Ligne ou Intolérance Allopurinol", "badge": "Prudence CV",
         "rows": [
             {"dci": "Fébuxostat", "princeps": "Adenuric 80-120 mg",
              "vol": "📦 1M boîtes · 28€ · 28M€/an",
              "dose": "80 mg/j · si non contrôlé 120 mg/j", "watch": "CI si ATCD IDM/AVC récent · Surmortalité CV dans essai CARES → réservé en 2ème ligne"},
         ]},
        {"cls": "cls-colchi-prev", "header_bg": "#e0f2f1", "name_color": "#004d40", "badge_bg": "#00695c",
         "name": "Colchicine — Prophylaxie des Crises sous Hypo-uricémiant", "badge": "Prévention 6 mois",
         "rows": [
             {"dci": "Colchicine 0,5 mg", "princeps": "Colchicine 0,5 mg · Colchimaxil",
              "vol": "📦 prescription préventive 6 mois",
              "dose": "0,5 mg/j (ou x2/j) pendant démarrage allopurinol · 6 mois", "watch": "Évite les crises de mobilisation des cristaux lors de la baisse d'uricémie"},
         ]},
    ],
    ci_block="""<div style="font-size:6pt;color:#b71c1c;font-weight:600;margin-bottom:1.5mm;">⛔ Allopurinol JAMAIS pendant une crise aiguë → prolonge et aggrave la crise (mobilisation cristaux)</div>
      <div style="font-size:6pt;color:#b71c1c;font-weight:600;margin-bottom:1.5mm;">⛔ Fébuxostat CI si ATCD IDM ou AVC récent → allopurinol reste 1ère ligne · Rester prudent CV</div>
      <div style="font-size:6pt;color:#b71c1c;font-weight:600;">⛔ Colchicine + CYP3A4 inhibiteurs (cyclosporine, clarithromycine, vérapamil) → toxicité majeure</div>""",
    strat_label="Stratégie ACR 2020",
    strat_steps=[("Crise", "Colchicine ou AINS dès J0"), ("Intercrises", "Allopurinol 3-6 sem après"), ("Prévention crises", "Colchicine 6 mois avec allo"), ("Résistance", "Fébuxostat 80-120 mg")],
    nouveaute_text="<strong>Fébuxostat (Adenuric)</strong> : lettre EMA 2019 confirme restriction usage (2ème ligne uniquement) après surmortalité CV étude CARES · <strong>Recommandations ACR 2020</strong> : allopurinol cible uricémie < 360 µmol/L · Prévention systématique 3-6 mois au démarrage · Canakinumab (anti-IL-1β) disponible formes réfractaires",
    reflexes=["Crise goutte : colchicine 1 mg dès l'apparition + 0,5 mg 1h après · Ne jamais débuter/modifier allopurinol pendant la crise",
              "Régime : limiter alcool (surtout bière), abats, charcuterie, viande rouge, fructose · Hydratation +++",
              "Allopurinol = traitement à VIE si ≥ 2 crises/an · Titration lente (100 mg/mois) selon uricémie et DFG"],
    interactions=[("Allopurinol + azathioprine/mercaptopurine", "↑ Toxicité azathioprine × 4 (même voie catabolisme) → CI ou réduire dose azathioprine de 75%"),
                  ("Colchicine + clarithromycine/vérapamil/cyclosporine", "Toxicité colchicine majeure (myopathie, neuropathie) → éviter association"),
                  ("AINS + diurétiques thiazidiques", "Diurétiques augmentent uricémie → interaction pharmacodynamique · Surveiller"),
                  ("Allopurinol + ampicilline/amoxicilline", "↑ Risque éruptions cutanées allergiques · Alternative ATB si possible")],
    patient_items=[
        ('"J\'ai eu une crise de goutte, je dois prendre mon Zyloric ?"',
         "JAMAIS allopurinol pendant une crise aiguë → mobilise les cristaux = aggrave et prolonge la crise · Attendre 3-6 semaines après résolution",
         "Non → colchicine ou AINS pour cette crise · Reprendre/démarrer allopurinol quand la crise est totalement résolue"),
        ('"Mon médecin m\'a prescrit colchicine 0,5 mg tous les jours alors que je n\'ai pas de crise"',
         "Colchicine prophylactique pendant les 6 premiers mois de traitement hypo-uricémiant = standard · Évite les crises de mobilisation des cristaux lors de la baisse d'uricémie",
         "Normal et recommandé · Prévient les crises déclenchées par la baisse rapide d'uricémie · 6 mois minimum"),
        ('"J\'ai pris Adenuric mais mon médecin dit que c\'est dangereux pour le cœur"',
         "Étude CARES 2019 → surmortalité CV sous fébuxostat vs allopurinol chez patients ATCD CV → restriction EMA · CI si ATCD IDM/AVC récent",
         "Si ATCD CV → allopurinol préféré · Fébuxostat réservé intolérance allopurinol sans ATCD CV · Signaler cardiologue"),
        ('"Je mange très peu de viande mais j\'ai quand même de la goutte"',
         "Goutte = cause principale rénale (sous-excrétion rénale urates, 90% des cas) + génétique · Alimentation = facteur aggravant, pas seul causal",
         "Régime aide mais ne suffit pas seul · Traitement médicamenteux nécessaire si ≥ 2 crises/an · Hydratation 2L/j"),
    ],
    footer_left="Goutte · Allopurinol · Fébuxostat · Colchicine · Cristaux MSU · BDPM 2026",
    footer_right="Pathologie 20 · 80/20 · Pratique comptoir"
)

print("\n✅ Tous les posters 16-20 créés !")
print("Total : 20 posters pathologies + 2 posters spéciaux = 22 posters officine")
