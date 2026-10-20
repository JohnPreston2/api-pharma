#!/usr/bin/env python3
"""Create pathology posters 11-20."""
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
    <div class="drug-class {cls_id}" style="">
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
# 11. OSTÉOPOROSE
# ─────────────────────────────────────────
make_poster(
    filename="osteoporose_poster.html",
    title="Ostéoporose",
    subtitle="Fiche officine · Pathologie 11 · Pratique comptoir · 2026",
    stats=[("1/3", "Femmes > 50 ans"), ("DXA", "T-score ≤ −2.5"), ("50%", "Fractures non traitées")],
    tags=["Bisphosphonates oraux = à jeun 30 min", "Ostéonécrose mâchoire IV", "Ca + VitD obligatoires", "Dénosumab 6 mois injecteur", "Romosozumab 12 mois max", "FRAX calcul risque"],
    c1="#014a6b", c2="#0277bd", c3="#4fc3f7", cl="#e1f5fe", cm="#b3e5fc",
    physio_steps=[
        "🦴 Déséquilibre ostéoblastes (formation) / ostéoclastes (résorption)",
        "📉 Ménopause → chute œstrogènes → résorption accélérée x2",
        "⚠ Carence VitD + Ca → PTH ↑ → déminéralisation compensatrice",
        "💊 Corticoïdes au long cours → ostéoporose cortisonique"
    ],
    target_boxes=[("Vertèbres", "Tassement, cyphose"), ("Col fémoral", "Fracture de hanche"), ("Poignet", "Fracture Pouteau-Colles"), ("Côtes", "Fractures spontanées")],
    diag_items=[("T ≤ −2.5", "Ostéoporose DXA"), ("T −1/−2.5", "Ostéopénie DXA"), ("FRAX", "Score fracture 10 ans"), ("VitD < 30", "Carence ng/mL")],
    diag_note="📋 DXA hanche + rachis lombaire · FRAX si T entre −1 et −2.5 · Ca urinaire · Créatinine",
    drug_classes=[
        {"cls": "cls-bp", "header_bg": "#e3f2fd", "name_color": "#0d47a1", "badge_bg": "#1565c0",
         "name": "Bisphosphonates — 1ère ligne", "badge": "1ère ligne",
         "rows": [
             {"dci": "Alendronate · Risédronate", "princeps": "Fosamax · Actonel · Génériques",
              "vol": "📦 8M boîtes · 3,20€ · 26M€/an",
              "dose": "Alendronate 70 mg/sem · Risédronate 35 mg/sem", "watch": "À jeun, eau plate, debout 30 min · Œsophage"},
             {"dci": "Zolédronate (IV)", "princeps": "Aclasta 5 mg/100 mL",
              "vol": "📦 120K perf · 280€ · 34M€/an",
              "dose": "5 mg/an IV perfusion 15 min", "watch": "Réaction post-injection J1-J2 · Ostéonécrose mâchoire"},
             {"dci": "Ibandonate (IV mensuel)", "princeps": "Bonviva 3 mg/3 mL",
              "vol": "📦 200K inj · 145€ · 29M€/an",
              "dose": "3 mg IV/3 mois ou 150 mg PO/mois", "watch": "Soins dentaires avant tout traitement IV"},
         ]},
        {"cls": "cls-denosumab", "header_bg": "#f3e5f5", "name_color": "#4a148c", "badge_bg": "#6a1b9a",
         "name": "Dénosumab — Anti-RANK-L", "badge": "SC 6 mois",
         "rows": [
             {"dci": "Dénosumab", "princeps": "Prolia 60 mg/mL seringue",
              "vol": "📦 380K inj · 205€ · 78M€/an",
              "dose": "60 mg SC/6 mois · Injection sous-cutanée", "watch": "JAMAIS arrêt brutal → fracture rebond · Hypocalcémie"},
         ]},
        {"cls": "cls-romoso", "header_bg": "#fff3e0", "name_color": "#e65100", "badge_bg": "#bf360c",
         "name": "Romosozumab — Anti-Sclérostine", "badge": "Nouveau 2020",
         "rows": [
             {"dci": "Romosozumab", "princeps": "Evenity 105 mg/1.17 mL",
              "vol": "📦 15K boîtes · 420€/mois · AMM 2019",
              "dose": "210 mg SC/mois · 12 mois max puis relais", "watch": "CI si ATCD CV (IDM/AVC) · 12 mois max · Relais bisphosphonate"},
         ]},
        {"cls": "cls-vitd", "header_bg": "#e8f5e9", "name_color": "#1b5e20", "badge_bg": "#2e7d32",
         "name": "Supplémentation Ca + VitD — Toujours associée", "badge": "Obligatoire",
         "rows": [
             {"dci": "Cholécalciférol + Carbonate Ca", "princeps": "Calcidose · Orocal D3 · Caltrate D3",
              "vol": "📦 12M boîtes · 4,20€ · 50M€/an",
              "dose": "VitD 800–1200 UI/j · Ca 1000–1200 mg/j", "watch": "Hypercalcémie si excès · Lithiase rénale · Espacer de 2h le zinc"},
         ]},
    ],
    ci_block="""<div style="font-size:6pt;color:#b71c1c;font-weight:600;margin-bottom:1.5mm;">⛔ Bisphosphonates — CI si DFG &lt; 35 mL/min (sauf zolédronate DFG &gt; 35)</div>
      <div style="font-size:6pt;color:#b71c1c;font-weight:600;margin-bottom:1.5mm;">⛔ Dénosumab arrêt brutal → rebond fracturaire sévère → TOUJOURS relais</div>
      <div style="font-size:6pt;color:#b71c1c;font-weight:600;">⛔ Soins dentaires invasifs interdits sous bisphosphonates IV (ostéonécrose mâchoire)</div>""",
    strat_label="Stratégie HAS",
    strat_steps=[("Supplémentation", "Ca + VitD systématique"), ("1ère ligne", "Bisphosphonate oral"), ("Intolérance orale", "Zolédronate IV 1×/an"), ("Haut risque", "Romosozumab 12 mois")],
    nouveaute_text="<strong>Romosozumab (Evenity)</strong> AMM FR 2020 · Formation osseuse + inhibition résorption · 12 mois max si haut risque · CI cardiovasculaire · <strong>Arrêt dénosumab</strong> = rebond fracturaire reconnu → toujours relais bisphosphonate · DXA remboursée tous les 3 ans sous traitement",
    reflexes=["Bisphosphonates oraux : à jeun eau plate, rester debout 30 min, attendre avant repas",
              "Avant tout traitement IV → consultation dentaire obligatoire (ostéonécrose mâchoire)",
              "Dénosumab : jamais d'arrêt sans relais → fractures vertébrales multiples en rebond"],
    interactions=[("Corticoïdes au long cours", "Accélèrent perte osseuse → prévention ostéoporose cortisonique"),
                  ("IPP (oméprazole)", "Réduisent absorption Ca oral → espacer ou privilégier Ca citrate"),
                  ("Antiacides / Zinc", "Chélatent bisphosphonates oraux → prendre à 2h d'intervalle"),
                  ("Tétracyclines + Ca", "Chélation → espacer de 3h")],
    patient_items=[
        ('"Je dois vraiment prendre ce cachet à jeun ?"',
         "Bisphosphonate oral mal absorbé avec nourriture (< 1% biodispo) et risque irritation œsophage si couché",
         "Oui : eau plate, rester assis/debout 30 min, puis petit-déjeuner"),
        ('"Je suis allée chez le dentiste et il m\'a dit d\'arrêter"',
         "Risque réel d'ostéonécrose mâchoire avec bisphosphonates IV — chirurgie osseuse déconseillée sous traitement",
         "Soins conservateurs OK · Pour extraction/implant → avis médecin traitant"),
        ('"J\'ai arrêté Prolia il y a 2 mois, le médecin est en vacances"',
         "URGENCE : arrêt dénosumab > 6 mois = risque fractures vertébrales multiples en quelques semaines",
         "Urgence → contact médecin remplaçant · Relais bisphosphonate indispensable"),
        ('"Ça fait 2 ans que je prends Cacit D3, c\'est bien ?"',
         "Supplémentation Ca/VitD = traitement adjuvant, insuffisant seul sans traitement anti-ostéoporotique si T ≤ −2.5",
         "Vérifier si DXA faite · Signaler médecin si T-score ≤ −2.5 sans traitement spécifique"),
    ],
    footer_left="Ostéoporose · Bisphosphonates · Dénosumab · Romosozumab · BDPM 2026",
    footer_right="Pathologie 11 · 80/20 · Pratique comptoir"
)

# ─────────────────────────────────────────
# 12. ALLERGIE / RHINITE CHRONIQUE
# ─────────────────────────────────────────
make_poster(
    filename="allergie_rhinite_poster.html",
    title="Allergie & Rhinite Chronique",
    subtitle="Fiche officine · Pathologie 12 · Pratique comptoir · 2026",
    stats=[("30%", "Français allergiques"), ("ARIA", "Score sévérité"), ("ITA", "Désensibilisation")],
    tags=["Antihistaminiques H1 2G = non sédatifs", "Corticoïdes nasaux = 1ère ligne", "ARIA légère/modérée/sévère", "Dupilumab polypose nasale", "Pas de croisement latex-alimentation", "IgE spécifiques > prick test"],
    c1="#1b5e20", c2="#388e3c", c3="#66bb6a", cl="#e8f5e9", cm="#c8e6c9",
    physio_steps=[
        "🤧 Sensibilisation allergène → production IgE spécifiques",
        "🔗 Re-exposition → fixation IgE sur mastocytes",
        "💥 Dégranulation → histamine + leucotriènes + prostaglandines",
        "🌊 Rhinorrhée · Obstruction · Prurit · Éternuements"
    ],
    target_boxes=[("Nez", "Rhinorrhée, obstruction"), ("Yeux", "Conjonctivite"), ("Bronches", "Asthme associé 30%"), ("Peau", "Urticaire, eczéma")],
    diag_items=[("Prick test", "Allergie IgE-médiée"), ("IgE spéc.", "RAST en labo"), ("ARIA", "Légère/Modérée/Sévère"), ("FeNO", "Éosinophilie bronchique")],
    diag_note="📋 Prick tests pneumallergènes + alimentaires · ARIA: épisodique vs persistante · ≥ 2 semaines",
    drug_classes=[
        {"cls": "cls-ah2g", "header_bg": "#e8f5e9", "name_color": "#1b5e20", "badge_bg": "#2e7d32",
         "name": "Antihistaminiques H1 2G — Non sédatifs", "badge": "1ère ligne crise",
         "rows": [
             {"dci": "Cétirizine · Loratadine · Fexofénadine", "princeps": "Zyrtec · Clarityne · Telfast · Génériques",
              "vol": "📦 28M boîtes · 3,10€ · 87M€/an",
              "dose": "Cétirizine 10 mg/j · Loratadine 10 mg/j", "watch": "Sédation modérée cétirizine · Conduite si métier risque"},
             {"dci": "Desloratadine · Bilastine · Rupatadine", "princeps": "Aerius · Bilaxten · Rupafin",
              "vol": "📦 12M boîtes · 4,80€ · 58M€/an",
              "dose": "Desloratadine 5 mg/j · Bilastine 20 mg/j à jeun", "watch": "Bilastine à jeun (absorption ↓ avec jus pamplemousse)"},
         ]},
        {"cls": "cls-cortinasal", "header_bg": "#f3e5f5", "name_color": "#4a148c", "badge_bg": "#6a1b9a",
         "name": "Corticoïdes Nasaux — 1ère ligne rhinite persistante", "badge": "Fondamental",
         "rows": [
             {"dci": "Fluticasone · Mométasone · Budésonide", "princeps": "Flixonase · Nasonex · Rhinocort · Avamys",
              "vol": "📦 14M boîtes · 6,20€ · 87M€/an",
              "dose": "2 pulvérisations/narine/matin · Efficacité J5-J7", "watch": "Épistaxis locaux (lavage nez avant) · Systémique négligeable"},
         ]},
        {"cls": "cls-decong", "header_bg": "#fff8e1", "name_color": "#f57f17", "badge_bg": "#f9a825",
         "name": "Décongestionnants — Usage court (3-5j max)", "badge": "Max 5 jours",
         "rows": [
             {"dci": "Pseudoéphédrine · Oxymétazoline", "princeps": "Sudafed · Actifed · Rhinofluimucil · Aturgyl",
              "vol": "📦 8M boîtes · 5,40€ · 43M€/an",
              "dose": "Pseudoéphédrine 60 mg x3/j · max 5j", "watch": "CI HTA · Glaucome · MAO · Rhinite rebond si > 5j"},
         ]},
        {"cls": "cls-dupil", "header_bg": "#fce4ec", "name_color": "#880e4f", "badge_bg": "#ad1457",
         "name": "Dupilumab — Polypose Nasale Sévère", "badge": "Biothérapie",
         "rows": [
             {"dci": "Dupilumab", "princeps": "Dupixent 300 mg/2 mL SC",
              "vol": "📦 remboursé 2022 polypose · 1200€/2 sem",
              "dose": "300 mg SC/2 semaines · Auto-injection", "watch": "Indication stricte : polypose + corticoïdes échec · Onéreux"},
         ]},
        {"cls": "cls-ita", "header_bg": "#e0f2f1", "name_color": "#004d40", "badge_bg": "#00695c",
         "name": "Immunothérapie Allergénique (ITA)", "badge": "Désensibilisation",
         "rows": [
             {"dci": "Extraits allergéniques sublingaux/SC", "princeps": "Staloral · Acarizax · Grazax · Actair",
              "vol": "📦 500K traitements/an · 300-600€/an",
              "dose": "3 à 5 ans de traitement · SL quotidien ou SC mensuel", "watch": "Réaction anaphylactique possible SC → kit urgence"},
         ]},
    ],
    ci_block="""<div style="font-size:6pt;color:#b71c1c;font-weight:600;margin-bottom:1.5mm;">⛔ Pseudoéphédrine CI : HTA, glaucome, MAO, ATCD AVC, hyperthyroïdie · Max 5 jours</div>
      <div style="font-size:6pt;color:#b71c1c;font-weight:600;margin-bottom:1.5mm;">⛔ AH1G (diphénhydramine, prométhazine) sédatifs : CI conduite, personnes âgées · Choisir 2G</div>
      <div style="font-size:6pt;color:#b71c1c;font-weight:600;">⛔ Décongestionnants en association = vigilance HTA, grossesse CI absolue</div>""",
    strat_label="Stratégie ARIA",
    strat_steps=[("Légère épisodique", "AH2G oral PRN"), ("Légère persistante", "AH2G + CN nasal"), ("Modérée/Sévère", "CN nasal + AH2G"), ("Réfractaire", "ITA ou biothérapie")],
    nouveaute_text="<strong>Dupilumab (Dupixent)</strong> remboursé polypose nasale sévère 2022 · <strong>Acarizax sublingual</strong> acariens remboursé · Actualisation ARIA 2020 : corticoïdes nasaux renforcés comme 1ère ligne persistante · Nouvelles recommandations EAACI désensibilisation accélérée",
    reflexes=["Corticoïdes nasaux = 1ère ligne rhinite persistante · Efficacité dès J5 · Enseigner bonne technique (viser paroi latérale)",
              "Pseudoéphédrine : toujours demander PA, antécédents CV/glaucome avant de délivrer",
              "Rhinite allergique + asthme chez 30% patients → penser bilan respiratoire si toux chronique"],
    interactions=[("Pseudoéphédrine + MAO", "Hypertension sévère, risque vital → CI absolue"),
                  ("AH1G + benzodiazépines", "Sédation additionnelle → chute PA → toujours préférer AH2G"),
                  ("Pseudoéphédrine + antihypertenseurs", "Antagonisme tensionnel → CI si HTA traitée"),
                  ("ITA (SC) + β-bloquants", "Réaction anaphylactique traitée par adrénaline inefficace → CI relative")],
    patient_items=[
        ('"Le spray nasal m\'a dit que c\'était pour le rhume"',
         "Corticoïdes nasaux = traitement préventif et continu de la rhinite allergique persistante · PAS un décongestionnant",
         "Prendre tous les jours même sans symptômes · Efficacité complète après 1-2 semaines"),
        ('"J\'ai pris Actifed 3 semaines pour déboucher mon nez"',
         "Rhinite rebond (rhinite médicamenteuse) par usage prolongé décongestionnants nasaux > 5 jours = terrain irrité chronique",
         "Stop décongestionnant, corticoïdes nasaux pour sevrage · Souvent 2-4 semaines"),
        ('"Mon enfant est allergique aux acariens, qu\'est-ce que vous conseillez ?"',
         "Immunothérapie allergénique (désensibilisation) = seul traitement curatif · Acarizax sublingual dès 5 ans remboursé",
         "Évoquer désensibilisation avec l'allergologue · Mesures éviction environnementale aussi"),
        ('"J\'ai pris Zyrtec et je me suis endormi au volant"',
         "Cétirizine = AH1G/2G intermédiaire · 10-20% sédation résiduelle · Loratadine ou fexofénadine moins sédatifs",
         "Switcher loratadine ou fexofénadine · Toujours tester avant conduite"),
    ],
    footer_left="Allergie · Rhinite · AH2G · Corticoïdes nasaux · ITA · Dupilumab · BDPM 2026",
    footer_right="Pathologie 12 · 80/20 · Pratique comptoir"
)

# ─────────────────────────────────────────
# 13. CONTRACEPTION
# ─────────────────────────────────────────
make_poster(
    filename="contraception_poster.html",
    title="Contraception",
    subtitle="Fiche officine · Pathologie 13 · Pratique comptoir · 2026",
    stats=[("96%", "Femmes utilisent contraception"), ("CU", "72h ou 5j (DIU)"), ("99.7%", "Efficacité pilule idéale")],
    tags=["Oubli pilule < 12h = prendre", "Oubli > 12h = préservatif", "Pilule progestative = fenêtre 3h", "DIU cuivre = urgence 5j", "EllaOne > Norlevo si > 72h", "ATCD thrombose → progestative seule"],
    c1="#880e4f", c2="#c2185b", c3="#f06292", cl="#fce4ec", cm="#f8bbd0",
    physio_steps=[
        "🔵 Œstrogènes → inhibition FSH → blocage folliculogenèse",
        "🟡 Progestatifs → inhibition LH → blocage ovulation",
        "🔒 Progestatifs → glaire cervicale épaissie → imperméable spermatozoïdes",
        "🏠 Atrophie endomètre → implantation impossible (DIU, micropilule)"
    ],
    target_boxes=[("Ovulation", "Inhibée par E+P"), ("Glaire", "Imperméable (P)"), ("Endomètre", "Atrophié (P)"), ("Trompes", "Motilité réduite (P)")],
    diag_items=[("Indice Pearl", "Échecs/100 femmes/an"), ("< 1", "Pilule bien prise"), ("0.1", "DIU, implant"), ("CU Délai", "72h LNG / 120h DIU")],
    diag_note="📋 TA avant prescription · Bilan lipidique si FdR · Frottis col à jour · Pas d'exam gynéco obligatoire pour délivrance CU",
    drug_classes=[
        {"cls": "cls-eop", "header_bg": "#fce4ec", "name_color": "#880e4f", "badge_bg": "#ad1457",
         "name": "Pilules Œstroprogestatives — EP", "badge": "1ère prescrite",
         "rows": [
             {"dci": "EE + Lévonorgestrel · EE + Norgestimate", "princeps": "Trinordiol · Triafemi · Adepal · Nordette",
              "vol": "📦 20M boîtes · 3,80€ · 76M€/an",
              "dose": "Monophasique ou triphasique · 21j/7j ou 24j/4j", "watch": "Thrombose VTE · Migraine avec aura CI · Tabac > 35 ans CI"},
             {"dci": "EE + Drospirénone · EE + Gestodène", "princeps": "Jasminelle · Minulet · Désobel",
              "vol": "📦 9M boîtes · 5,20€ · 47M€/an",
              "dose": "EE 20-30 mcg + progestatif 3G", "watch": "Risque VTE légèrement > 1G/2G · Possible si tolérance meilleure"},
         ]},
        {"cls": "cls-prog", "header_bg": "#f3e5f5", "name_color": "#4a148c", "badge_bg": "#6a1b9a",
         "name": "Pilules Progestatives Seules — Microprogestatives", "badge": "ATCD CV / Allaitante",
         "rows": [
             {"dci": "Désogestrel 75 mcg", "princeps": "Cerazette · Desogrel · Génériques",
              "vol": "📦 11M boîtes · 4,10€ · 45M€/an",
              "dose": "1 cp/j en continu · Fenêtre 12h", "watch": "Spottings fréquents · Acné · Pas d'effet VTE"},
             {"dci": "Lévonorgestrel 30 mcg", "princeps": "Microval",
              "vol": "📦 2M boîtes · 3,60€ · 7M€/an",
              "dose": "1 cp/j en continu · Fenêtre 3h stricte", "watch": "Fenêtre de prise 3h → plus contraignant"},
         ]},
        {"cls": "cls-diu", "header_bg": "#e8eaf6", "name_color": "#1a237e", "badge_bg": "#283593",
         "name": "DIU — Dispositif Intra-Utérin", "badge": "LT / Urgence",
         "rows": [
             {"dci": "Lévonorgestrel 52 mg (DIU hormonal)", "princeps": "Mirena · Kyleena · Jaydess",
              "vol": "📦 250K insertions/an · 120-180€",
              "dose": "Mirena 5 ans · Kyleena 5 ans (moins progestatif)", "watch": "Expulsion 5% · Douleurs insertion · Aménorrhée fréquente"},
             {"dci": "DIU Cuivre (non hormonal)", "princeps": "Nova-T · Gynefix · UT380",
              "vol": "📦 180K insertions/an · 30-45€",
              "dose": "5-10 ans selon modèle · Contraception urgence 5j", "watch": "Dysménorrhée · Métrorragies · CI utérus malformé"},
         ]},
        {"cls": "cls-urgence", "header_bg": "#fff3e0", "name_color": "#e65100", "badge_bg": "#bf360c",
         "name": "Contraception d'Urgence", "badge": "Sans ordonnance",
         "rows": [
             {"dci": "Lévonorgestrel 1,5 mg", "princeps": "Norlevo · NorLevo Generics · Vikela",
              "vol": "📦 1,8M boîtes/an · 7,50€ · 14M€/an",
              "dose": "1 cp dès que possible · Efficacité décroit avec délai", "watch": "Efficace 72h · Moins efficace > 72h · Gratuit mineurs"},
             {"dci": "Ulipristal acétate 30 mg", "princeps": "EllaOne",
              "vol": "📦 400K boîtes/an · 24€ · 10M€/an",
              "dose": "1 cp jusqu'à 120h (5j) · Supérieur LNG si > 72h", "watch": "CI si progestative en cours · Reprendre contraception après"},
         ]},
    ],
    ci_block="""<div style="font-size:6pt;color:#b71c1c;font-weight:600;margin-bottom:1.5mm;">⛔ EP CI absolues : ATCD TVP/EP, thrombophilie, migraine avec aura, HTA sévère, tabac > 35 ans, cancer sein/endomètre</div>
      <div style="font-size:6pt;color:#b71c1c;font-weight:600;margin-bottom:1.5mm;">⛔ EllaOne CI avec pilule progestative (compétition récepteur) → utiliser LNG ou DIU cuivre</div>
      <div style="font-size:6pt;color:#b71c1c;font-weight:600;">⛔ Pilule + inducteurs enzymatiques (rifampicine, antiépileptiques) → efficacité réduite → préservatif + DIU</div>""",
    strat_label="Stratégie contraceptive",
    strat_steps=[("Jeune sans FdR", "EP ou progestative"), ("ATCD CV/Allait.", "Microprogestative/DIU"), ("LT / Nullipare OK", "DIU LNG ou cuivre"), ("Urgence", "LNG 72h ou EllaOne 120h")],
    nouveaute_text="<strong>Contraception d'urgence</strong> sans ordonnance ni avance de frais pour mineures depuis 2023 · <strong>Pilule remboursée</strong> jusqu'à 26 ans depuis 2022 · DIU remboursé sans prescription chez les pharmaciens (projet pilote) · <strong>Consultations contraception 100%</strong> jeunes jusqu'à 26 ans",
    reflexes=["Oubli pilule : < 12h → prendre immédiatement · > 12h → prendre + préservatif 7j · > 12h + rapport → CU",
              "EllaOne supérieur à Norlevo entre 72h et 120h · Toujours demander heure du rapport non protégé",
              "DIU cuivre = CU la plus efficace (> 99%) jusqu'à 5j après rapport · Et reste en place pour contraception LT"],
    interactions=[("Inducteurs enzymatiques (rifampicine, phénytoïne)", "↓ efficacité contraception hormonale → préservatif + avis médecin"),
                  ("EllaOne + progestatif", "Antagonisme récepteur progestérone → CU inefficace → préférer DIU cuivre ou LNG"),
                  ("Contraceptifs EP + AINS", "↑ risque thrombose modéré · Paracétamol préférable"),
                  ("Antibiotiques (rifampicine)", "Seule rifampicine réduit vraiment l'efficacité · Autres ATB : pas de CI formelle")],
    patient_items=[
        ('"J\'ai oublié ma pilule hier soir"',
         "Fenêtre tolérance EP = 12h · Microprogestative = 3h (LNG) ou 12h (désogestrel) · Après = risque grossesse réel",
         "Heure oubli ? Moins de 12h → prendre tout de suite · Plus de 12h → prendre + préservatif + évaluer CU si rapport"),
        ('"J\'ai eu un rapport hier soir sans protection"',
         "CU doit être prise dès que possible · Efficacité : 95% si <24h, 85% si 24-48h, 58% si 48-72h pour LNG",
         "LNG si ≤ 72h · EllaOne si 72-120h · DIU cuivre si ≤ 120h et veut contraception LT"),
        ('"Je prends Topiramate pour la migraine, ma pilule marche-t-elle ?"',
         "Topiramate = inducteur enzymatique modéré → réduit efficacité pilule hormonale → grossesses non désirées documentées",
         "Signaler médecin · Envisager DIU non hormonal ou préservatif systématique"),
        ('"Je suis sous Cerazette et j\'ai pris EllaOne"',
         "EllaOne = modulateur récepteur progestérone → compétition avec microprogestative = CU inefficace dans ce contexte",
         "Arrêt immédiat Cerazette et/ou proposer DIU cuivre · Avis médecin"),
    ],
    footer_left="Contraception · EP · Progestative · DIU · CU · Lévonorgestrel · BDPM 2026",
    footer_right="Pathologie 13 · 80/20 · Pratique comptoir"
)

# ─────────────────────────────────────────
# 14. PROSTATE / HBP
# ─────────────────────────────────────────
make_poster(
    filename="prostate_HBP_poster.html",
    title="Prostate & HBP",
    subtitle="Fiche officine · Pathologie 14 · Pratique comptoir · 2026",
    stats=[("50%", "Hommes > 50 ans HBP"), ("IPSS", "Score symptômes"), ("PSA", "Dépistage/suivi")],
    tags=["α-bloquants = effet rapide (48h)", "I5AR = 6 mois pour effet", "Tamsulosine = hypo orthostatique", "Éjaculation rétrograde sous α-bloquants", "PSA divisé par 2 sous I5AR", "Tadalafil 5mg/j si aussi DE"],
    c1="#0d47a1", c2="#1565c0", c3="#42a5f5", cl="#e3f2fd", cm="#bbdefb",
    physio_steps=[
        "🧬 Testostérone → DHT par 5α-réductase dans prostate",
        "📐 DHT stimule croissance cellules prostatiques → HBP",
        "🚰 Compression urétrale → dysurie, pollakiurie, RAU",
        "📊 IPSS > 7 = symptômes modérés · > 19 = sévères"
    ],
    target_boxes=[("Urètre", "Obstruction, dysurie"), ("Vessie", "Hypertrophie detrusor"), ("Rein", "Obstruction chronique"), ("Qualité vie", "Nycturie, urgences")],
    diag_items=[("IPSS", "Score 0-35"), ("PSA total", "< 4 ng/mL normal"), ("ΔV prostate", "Écho > 30 mL HBP"), ("Débit max", "Qmax < 10 mL/s")],
    diag_note="📋 TR (toucher rectal) · PSA · Créatinine · Échographie vésico-prostatique · Débitmétrie · ECBU si infection",
    drug_classes=[
        {"cls": "cls-alpha", "header_bg": "#e3f2fd", "name_color": "#0d47a1", "badge_bg": "#1565c0",
         "name": "α-Bloquants — Relaxation muscle lisse", "badge": "Effet rapide 48h",
         "rows": [
             {"dci": "Tamsulosine · Alfuzosine", "princeps": "Omix · Josir LP · Xatral LP · Génériques",
              "vol": "📦 12M boîtes · 5,40€ · 65M€/an",
              "dose": "Tamsulosine 0,4 mg/j · Alfuzosine LP 10 mg/j", "watch": "Hypotension orthostatique (1ère dose) · Éjaculation rétrograde · IFIS chirurgie yeux"},
             {"dci": "Doxazosine · Térazosine", "princeps": "Zoxan · Hytrine",
              "vol": "📦 2M boîtes · 4,10€ · 8M€/an",
              "dose": "Doxazosine LP 4-8 mg/j", "watch": "Hypotension plus marquée · Titration progressive"},
         ]},
        {"cls": "cls-i5ar", "header_bg": "#f3e5f5", "name_color": "#4a148c", "badge_bg": "#6a1b9a",
         "name": "Inhibiteurs 5α-Réductase — Réduction volume", "badge": "Délai 6 mois",
         "rows": [
             {"dci": "Finastéride · Dutastéride", "princeps": "Chibro-Proscar · Avodart · Génériques",
              "vol": "📦 4M boîtes · 12€ · 48M€/an",
              "dose": "Finastéride 5 mg/j · Dutastéride 0,5 mg/j", "watch": "PSA divisé par 2 · Libido ↓ · Éjaculation rétrograde · ATCD dépression"},
         ]},
        {"cls": "cls-combi", "header_bg": "#e8f5e9", "name_color": "#1b5e20", "badge_bg": "#2e7d32",
         "name": "Association α-bloquant + I5AR", "badge": "HBP volumineuse",
         "rows": [
             {"dci": "Tamsulosine + Dutastéride", "princeps": "Combodart 0,4/0,5 mg",
              "vol": "📦 1,5M boîtes · 22€ · 33M€/an",
              "dose": "1 gélule/j · Combiner les deux effets", "watch": "Effets cumulés des 2 classes · Coûteux"},
         ]},
        {"cls": "cls-pde5", "header_bg": "#fff3e0", "name_color": "#e65100", "badge_bg": "#bf360c",
         "name": "Inhibiteurs PDE5 — Si HBP + Dysfonction Érectile", "badge": "Si aussi DE",
         "rows": [
             {"dci": "Tadalafil 5 mg/j", "princeps": "Cialis 5 mg · Tadalafil Generics",
              "vol": "📦 remboursé HBP 2022 · 5mg/j",
              "dose": "5 mg/j en continu · HBP + DE", "watch": "CI nitrés (hypotension sévère) · Hypotension orthostatique"},
         ]},
        {"cls": "cls-phyto", "header_bg": "#fafafa", "name_color": "#546e7a", "badge_bg": "#607d8b",
         "name": "Phytothérapie — Efficacité modeste", "badge": "Service médical rendu",
         "rows": [
             {"dci": "Serenoa repens (palmier nain)", "princeps": "Permixon 160 mg · Prostamol",
              "vol": "📦 2,5M boîtes · 8,50€ · 21M€/an",
              "dose": "160 mg x2/j", "watch": "Efficacité modest vs placebo · Non remboursé · Rassurant"},
         ]},
    ],
    ci_block="""<div style="font-size:6pt;color:#b71c1c;font-weight:600;margin-bottom:1.5mm;">⛔ Tadalafil CI absolue avec dérivés nitrés (hypotension sévère, risque vital)</div>
      <div style="font-size:6pt;color:#b71c1c;font-weight:600;margin-bottom:1.5mm;">⛔ Tamsulosine : IFIS (Intraoperative Floppy Iris Syndrome) lors chirurgie cataracte → informer chirurgien</div>
      <div style="font-size:6pt;color:#b71c1c;font-weight:600;">⛔ Finastéride/Dutastéride : PSA divisé par 2 → ne pas interpréter PSA sans tenir compte traitement</div>""",
    strat_label="Stratégie HAS",
    strat_steps=[("IPSS < 8", "Surveillance · RHD"), ("IPSS 8-19", "α-bloquant en 1ère ligne"), ("HBP volumineuse", "I5AR ou combinaison"), ("HBP + DE", "Tadalafil 5 mg/j")],
    nouveaute_text="<strong>Tadalafil 5 mg/j</strong> remboursé pour HBP symptomatique depuis 2022 · Recommandations EAU 2023 : chirurgie (résection) réservée aux formes sévères · <strong>Dutastéride biosimilaire</strong> disponible · Étude REDUCE : I5AR réduisent incidence cancer prostate haut grade controversée",
    reflexes=["α-bloquants : prévenir hypotension 1ère prise → prendre le soir au coucher, éviter lever brutal",
              "Finastéride/Dutastéride : PSA toujours interprété × 2 · Effets libido/érection → reversible à l'arrêt",
              "Tamsulosine + chirurgie yeux (cataracte) : IFIS grave → informer chirurgien à l'avance"],
    interactions=[("α-bloquants + antihypertenseurs", "Hypotension orthostatique potentialisée → surveillance TA"),
                  ("Tadalafil + nitrés", "Hypotension sévère, choc → CI absolue et formelle"),
                  ("Finastéride + warfarine", "Légère augmentation INR → surveiller"),
                  ("Tamsulosine + fluconazole/kétoconazole", "↑ concentration tamsulosine par CYP3A4 · Prudence")],
    patient_items=[
        ('"Mon médecin m\'a mis Avodart mais ça ne marche pas après 1 mois"',
         "I5AR agissent sur le volume prostatique → délai de 3-6 mois avant bénéfice symptomatique attendu",
         "Normal, l'effet se développe sur 3-6 mois · Vérifier observance · Ne pas arrêter"),
        ('"Depuis que je prends Josir, j\'ai du mal à éjaculer"',
         "Éjaculation rétrograde = effet de classe des α-bloquants · Bénin, réversible à l'arrêt · Pas dangereux",
         "Effet connu et réversible · Si insupportable → avis médecin pour switch"),
        ('"On m\'a opéré des yeux la semaine prochaine"',
         "Tamsulosine → IFIS (Intraoperative Floppy Iris Syndrome) = risque peropératoire grave · Le chirurgien doit le savoir",
         "Informer impérativement l'ophtalmologiste de la prise de tamsulosine même ancienne"),
        ('"Mon PSA était à 3 avant, maintenant à 1.5 sous Avodart, c\'est bien ?"',
         "Finastéride/dutastéride divisent le PSA par 2 · Un PSA 1.5 sous I5AR équivaut à 3 → surveillance normale",
         "PSA sous I5AR doit être multiplié par 2 pour interprétation réelle · Expliquer au médecin"),
    ],
    footer_left="Prostate · HBP · α-bloquants · I5AR · Tamsulosine · Tadalafil · BDPM 2026",
    footer_right="Pathologie 14 · 80/20 · Pratique comptoir"
)

# ─────────────────────────────────────────
# 15. MIGRAINE
# ─────────────────────────────────────────
make_poster(
    filename="migraine_poster.html",
    title="Migraine",
    subtitle="Fiche officine · Pathologie 15 · Pratique comptoir · 2026",
    stats=[("15%", "Population adulte"), ("3:1", "Femmes/Hommes"), ("CGRP", "Cible révolution 2020+")],
    tags=["Triptans = traitement de la crise", "10 jours/mois max antalgiques", "CGRP anticorps = prévention biologique", "Aura = jamais EP hormonale", "Valproate CI femme âge fertile", "Rimégépant = crise + prévention"],
    c1="#4a148c", c2="#7b1fa2", c3="#ce93d8", cl="#f3e5f5", cm="#e1bee7",
    physio_steps=[
        "⚡ Dysfonction trigémino-vasculaire → neuropeptides vasoactifs",
        "🔴 CGRP libéré → vasodilatation méningée + inflammation neurogène",
        "💥 Stimulation nocicepteurs duraux → douleur pulsatile unilatérale",
        "🌊 Aura (30%) : dépression corticale propagée (CSD) → signes focaux"
    ],
    target_boxes=[("Phase prodrome", "Bâillements, photophobie"), ("Aura", "Scotome, paresthésies 20-60min"), ("Crise", "Douleur 4-72h"), ("Postdrome", "Fatigue, confusion")],
    diag_items=[("IHS 2018", "Critères diagnostiques"), ("≥ 4j/mois", "Traitement fond"), ("MIDAS", "Score handicap"), ("Aura", "Typique vs atypique")],
    diag_note="📋 MIDAS score · Agenda migraineux · IRM si anomalie examen ou aura atypique · Pas d'IRM systématique",
    drug_classes=[
        {"cls": "cls-triptan", "header_bg": "#f3e5f5", "name_color": "#4a148c", "badge_bg": "#6a1b9a",
         "name": "Triptans — Traitement de la Crise", "badge": "1ère ligne crise",
         "rows": [
             {"dci": "Sumatriptan · Zolmitriptan", "princeps": "Imigrane · Zomig · Génériques",
              "vol": "📦 5M boîtes · 8,20€ · 41M€/an",
              "dose": "Sumatriptan 50-100 mg PO · 20 mg nasal · 6 mg SC", "watch": "CI CV (IDM, AVC, angor) · Rebond si > 10j/mois · Délai d'action 30-60 min"},
             {"dci": "Élétriptan · Rizatriptan · Naratriptan", "princeps": "Relpax · Maxalt · Naramig",
              "vol": "📦 4M boîtes · 9,80€ · 39M€/an",
              "dose": "Élétriptan 40 mg · Rizatriptan 10 mg · Naratriptan 2,5 mg", "watch": "Rizatriptan + propranolol → ↑ concentration · Naratriptan moins puissant mais moins rebond"},
         ]},
        {"cls": "cls-antalgiques", "header_bg": "#fff8e1", "name_color": "#f57f17", "badge_bg": "#f9a825",
         "name": "Antalgiques Crise — Si Triptan Insuffisant", "badge": "Adjuvant / 2ème ligne",
         "rows": [
             {"dci": "Ibuprofène · Naproxène sodique · Aspirine", "princeps": "Advil · Apranax · Aspirine Upsa",
              "vol": "📦 25M boîtes AINS crise · large usage",
              "dose": "Ibuprofène 400-600 mg · Naproxène 550 mg dès début", "watch": "Abus antalgiques > 10j/mois → céphalée chronique quotidienne"},
             {"dci": "Métoclopramide", "princeps": "Primpéran · Métoclopramide Generics",
              "vol": "📦 8M boîtes · 2,40€ · 19M€/an",
              "dose": "10 mg po avant triptan · Aide absorption gastrique", "watch": "Syndrome extrapyramidal · CI < 18 ans"},
         ]},
        {"cls": "cls-prevention-cl", "header_bg": "#e8f5e9", "name_color": "#1b5e20", "badge_bg": "#2e7d32",
         "name": "Prophylaxie Classique", "badge": "≥ 4 crises/mois",
         "rows": [
             {"dci": "Propranolol · Métoprolol", "princeps": "Avlocardyl · Lopressor · Génériques",
              "vol": "📦 8M boîtes BB · large usage",
              "dose": "Propranolol 40-240 mg/j · Métoprolol 50-200 mg/j", "watch": "CI asthme, BPCO, BAV, diabète (masque hypoglycémie)"},
             {"dci": "Topiramate · Valproate", "princeps": "Epitomax · Dépakine · Topamax",
              "vol": "📦 topiramate 4M boîtes",
              "dose": "Topiramate 25-100 mg/j · Valproate 500-1500 mg/j", "watch": "Valproate CI ABSOLUE femme âge fertile (tératogène) · Topiramate : lithiases, trouble mémoire"},
             {"dci": "Amitriptyline", "princeps": "Laroxyl · Elavil",
              "vol": "📦 8M boîtes · large usage",
              "dose": "10-75 mg/j HS · Petit dose migraine", "watch": "Sédation · Anticholinergique · PA debout"},
         ]},
        {"cls": "cls-cgrp", "header_bg": "#fce4ec", "name_color": "#880e4f", "badge_bg": "#ad1457",
         "name": "Anti-CGRP — Biothérapie Prophylactique", "badge": "Nouveau 2020+",
         "rows": [
             {"dci": "Galcanézumab · Frémanézumab", "princeps": "Emgality 120 mg · Ajovy 225 mg",
              "vol": "📦 remboursés 2022 · 500-600€/mois",
              "dose": "Emgality 120 mg SC/mois · Ajovy 225 mg SC/mois ou 675 mg/3 mois", "watch": "Injection SC · Constipation · CI grossesse · Très coûteux"},
             {"dci": "Rimégépant (gépant oral)", "princeps": "Vydura 75 mg",
              "vol": "📦 AMM Europe 2022 · 14€/cp",
              "dose": "75 mg à la demande OU j un/deux prophylaxie", "watch": "Crise + prophylaxie dans le même médicament · Moins rebond que triptan"},
         ]},
    ],
    ci_block="""<div style="font-size:6pt;color:#b71c1c;font-weight:600;margin-bottom:1.5mm;">⛔ Triptans CI : ATCD IDM/AVC/angor, HTA non contrôlée, arteriopathie, Raynaud sévère, grossesse</div>
      <div style="font-size:6pt;color:#b71c1c;font-weight:600;margin-bottom:1.5mm;">⛔ Valproate CI absolue femme en âge de procréer (tératogène majeur, 10% malformations) → topiramate préféré</div>
      <div style="font-size:6pt;color:#b71c1c;font-weight:600;">⛔ Aura migraineuse + contraception œstroprogestative → RISQUE AVC → pilule progestative ou DIU</div>""",
    strat_label="Stratégie crise",
    strat_steps=[("Légère-modérée", "AINS + métoclopramide"), ("Modérée-sévère", "Triptan d'emblée"), ("Résistance", "Triptan + AINS combo"), ("Chronique", "Anti-CGRP mensuel")],
    nouveaute_text="<strong>Galcanézumab (Emgality)</strong> et <strong>Frémanézumab (Ajovy)</strong> remboursés France 2022 pour migraine chronique réfractaire · <strong>Rimégépant (Vydura)</strong> AMM Europe 2022 : 1er médicament crise ET prévention · Eptinézumab (Vyepti) IV 2022 · Recommandations IHS 2021 révisées : TMS transcranial disponible",
    reflexes=["Triptans : prendre dès les 1ers signes de douleur (PAS pendant l'aura) · Max 2 prises/crise · Max 10 jours/mois",
              "Aura + pilule œstroprogestative → risque AVC multiplié par 8 → changer contraception",
              "Valproate chez une femme : TOUJOURS vérifier contraception efficace et carte de suivi ASMR"],
    interactions=[("Triptans + IMAO", "↑ concentration sérotoninergique · Syndrome sérotoninergique · CI"),
                  ("Rizatriptan + propranolol", "↑ AUC rizatriptan × 2 → réduire dose rizatriptan à 5 mg"),
                  ("Topiramate + contraceptifs hormonaux", "↑ métabolisme œstrogènes → efficacité réduite → DIU"),
                  ("Ergotamine + triptans", "Vasospasme additif → CI, délai 24h entre les deux")],
    patient_items=[
        ('"Je prends du Doliprane tous les jours pour ma migraine"',
         "Céphalée par abus d'antalgiques (CAMO) si > 10j/mois paracétamol/AINS ou > 10j triptans → migraine s'aggrave paradoxalement",
         "Sevrage progressif + traitement prophylactique · Médecin neurologue si > 4 crises/mois"),
        ('"Mon triptan ne marche pas si je le prends pendant l\'aura"',
         "Triptans sont vasoconstricteurs → contraindiqués pendant l'aura (ischémie) · À prendre au 1er signe de DOULEUR",
         "Attendre la fin de l'aura avant le triptan · AINS ou métoclopramide pendant l'aura"),
        ('"Je suis enceinte et j\'ai une migraine"',
         "Paracétamol = seul antalgique safe grossesse · AINS CI T3 · Triptans déconseillés · Magnésium prophylaxie",
         "Paracétamol 1g · Métoclopramide acceptable · Repos au calme · Signaler neurologue/obstétricien"),
        ('"On m\'a prescrit Emgality 120 mg, c\'est pour quoi ?"',
         "Galcanézumab = anticorps anti-CGRP injectable mensuel = traitement préventif migraine chronique sévère réfractaire",
         "Injection SC 1x/mois · Autoinjection · Réduction 50% crises chez 60% patients · Remboursé si ≥ 4 crises/mois"),
    ],
    footer_left="Migraine · Triptans · CGRP · Galcanézumab · Rimégépant · BDPM 2026",
    footer_right="Pathologie 15 · 80/20 · Pratique comptoir"
)

print("\n✅ Posters 11-15 créés !")
print("Posters 16-20 à créer dans le prochain script...")
