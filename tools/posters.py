#!/usr/bin/env python3
"""Suivi de fraîcheur et d'inventaire des posters (posters/*.html).

Chaque poster porte ses métadonnées dans <head> :

    <meta name="sv:volatilite" content="haute|moyenne|basse">
    <meta name="sv:maj"        content="AAAA-MM-JJ">   date de la dernière mise à jour sourcée
    <meta name="sv:sources"    content="texte libre, séparé par ' ; '">
    <meta name="sv:valide"     content="AAAA-MM-JJ">   validation par le pharmacien (absente = non validé)

Commandes :
    python3 tools/posters.py check [--strict] [--today AAAA-MM-JJ]
    python3 tools/posters.py index
    python3 tools/posters.py meta posters/x.html [--volatilite V] [--maj D] [--sources S] [--valide D]
"""
import argparse
import html
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POSTERS = ROOT / "posters"
FICHES = ROOT / "fiches"

# Âge maximal (jours) de la dernière mise à jour sourcée, selon la volatilité du sujet.
MAX_AGE = {"haute": 90, "moyenne": 180, "basse": 365}
META_KEYS = ("sv:volatilite", "sv:maj", "sv:sources", "sv:valide")
META_RE = re.compile(r'<meta\s+name="(sv:[a-z]+)"\s+content="([^"]*)"\s*/?>')
TITLE_RE = re.compile(r"<title>(.*?)</title>", re.S)


def read_meta(text):
    return {k: html.unescape(v) for k, v in META_RE.findall(text)}


def title_of(text):
    m = TITLE_RE.search(text)
    t = html.unescape(m.group(1)).strip() if m else ""
    return re.sub(r"\s+—\s+(SantéVeille Officine|Fiche Officine)$", "", t)


def parse_date(s):
    try:
        return date.fromisoformat(s)
    except (TypeError, ValueError):
        return None


def load():
    for p in sorted(POSTERS.glob("*.html")):
        text = p.read_text(encoding="utf-8")
        yield p, text, read_meta(text)


def norm(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def check(today, strict):
    errors, warnings = [], []
    titles = {}
    for p, text, meta in load():
        name = p.name
        vol = meta.get("sv:volatilite")
        if vol not in MAX_AGE:
            warnings.append((name, "volatilité non renseignée"))
            vol = "moyenne"
        maj, sources, valide = parse_date(meta.get("sv:maj")), meta.get("sv:sources"), meta.get("sv:valide")
        bucket = errors if vol == "haute" else warnings
        if not sources:
            bucket.append((name, f"sources absentes (volatilité {vol})"))
        if not maj:
            bucket.append((name, f"jamais revu contre des sources (volatilité {vol})"))
        else:
            age = (today - maj).days
            if age > MAX_AGE[vol]:
                bucket.append((name, f"périmé : {age} j depuis la mise à jour, max {MAX_AGE[vol]} j ({vol})"))
            elif not parse_date(valide):
                warnings.append((name, "à valider par le pharmacien (sv:valide absent)"))
        if not title_of(text):
            errors.append((name, "balise <title> absente"))
        titles.setdefault(norm(title_of(text)), []).append(name)
        if not p.name.isascii():
            errors.append((name, "nom de fichier non ASCII"))
    for names in titles.values():
        if len(names) > 1:
            errors.append((", ".join(names), "titres identiques : doublon probable"))
    index = FICHES / "INDEX.md"
    if index.exists():
        for link in re.findall(r"\]\((\.[^)]+)\)", index.read_text(encoding="utf-8")):
            if not (FICHES / link).resolve().exists():
                errors.append(("fiches/INDEX.md", f"lien cassé : {link}"))

    for label, rows in (("ERREURS", errors), ("AVERTISSEMENTS", warnings)):
        print(f"\n{label} ({len(rows)})")
        for name, msg in rows:
            print(f"  - {name} : {msg}")
    n = sum(1 for _ in POSTERS.glob("*.html"))
    print(f"\n{n} posters · {len(errors)} erreur(s) · {len(warnings)} avertissement(s)")
    return 1 if (strict and errors) else 0


def index():
    rows = []
    for p, text, meta in load():
        rows.append((title_of(text) or p.stem, p.name, meta))
    rows.sort(key=lambda r: norm(r[0]))
    out = [
        "# Index des posters",
        "",
        "Généré par `python3 tools/posters.py index` — ne pas éditer à la main.",
        "",
        "| Poster | Fichier | Volatilité | MàJ sourcée | Sources | Validé |",
        "|---|---|---|---|---|---|",
    ]
    for title, fname, meta in rows:
        out.append(
            "| {} | [{}]({}) | {} | {} | {} | {} |".format(
                title.replace("|", "/"),
                fname,
                fname,
                meta.get("sv:volatilite", "?"),
                meta.get("sv:maj", "—"),
                "oui" if meta.get("sv:sources") else "—",
                meta.get("sv:valide", "—"),
            )
        )
    out += ["", f"{len(rows)} posters.", ""]
    (POSTERS / "INDEX.md").write_text("\n".join(out), encoding="utf-8")
    print(f"posters/INDEX.md écrit ({len(rows)} posters)")


def set_meta(path, values):
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    for key, val in values.items():
        if val is None:
            continue
        tag = '<meta name="{}" content="{}">'.format(key, html.escape(val, quote=True))
        pat = re.compile(r'<meta\s+name="{}"\s+content="[^"]*"\s*/?>'.format(re.escape(key)))
        if pat.search(text):
            text = pat.sub(lambda _m: tag, text, count=1)
        else:
            text, n = re.subn(
                r"(<meta charset=\"utf-8\">[ \t]*\n)", lambda m: m.group(1) + tag + "\n", text, count=1, flags=re.I
            )
            if n == 0:
                sys.exit(f"{p.name} : <meta charset=\"UTF-8\"> introuvable, balise non insérée")
    p.write_text(text, encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check")
    c.add_argument("--strict", action="store_true", help="code de sortie 1 s'il y a des erreurs")
    c.add_argument("--today", help="date de référence AAAA-MM-JJ (défaut : aujourd'hui)")
    sub.add_parser("index")
    m = sub.add_parser("meta")
    m.add_argument("poster")
    m.add_argument("--volatilite", choices=sorted(MAX_AGE))
    m.add_argument("--maj")
    m.add_argument("--sources")
    m.add_argument("--valide")
    a = ap.parse_args()
    if a.cmd == "check":
        sys.exit(check(parse_date(a.today) or date.today(), a.strict))
    if a.cmd == "index":
        index()
    else:
        set_meta(a.poster, {"sv:volatilite": a.volatilite, "sv:maj": a.maj, "sv:sources": a.sources, "sv:valide": a.valide})


if __name__ == "__main__":
    main()
