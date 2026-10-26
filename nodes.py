# -*- coding: utf-8 -*-
# © 2026 Franck Dupas (Franck D Digital AI) — Licence MIT (voir LICENSE).
"""
Cosmétiques Luxe — générateur de prompts pour visuels produits cosmétiques de luxe.
Deux nœuds ComfyUI :
  - CosmeticsLuxePrompt  : un produit -> un prompt (prompt / negative / gamme_id / filename_prefix)
  - CosmeticsLuxeGamme   : une gamme entière -> N prompts d'un coup + prompt de groupe

Principe : rendu TOUJOURS photoréaliste ; l'UNIVERS pilote la STRUCTURE (matières,
lumière, motifs, décor) ; la COULEUR est variable (palette + surcharge libre) ;
la mécanique ouvert/fermé de chaque produit est codée en dur.
"""

import re
import difflib
import unicodedata

# ---------------------------------------------------------------------------
# Bloc 1 — base photoréaliste (fixe)
# ---------------------------------------------------------------------------
BASE = ("Photoreal luxury cosmetics product photography, 100mm macro lens, "
        "shallow depth of field, studio-grade lighting, ultra-detailed, 4K")

NEGATIVE_BASE = ("illustration, cartoon, drawing, anime, cheap plastic look, "
                 "lowres, blurry, noisy, watermark, signature, deformed text, "
                 "misspelled brand name, extra fingers")

# ---------------------------------------------------------------------------
# Bloc 2 — UNIVERS -> STRUCTURE (sans couleur figée).
# Les couleurs par défaut vivent dans color_primary / color_secondary et
# peuvent être remplacées par une palette ou par les champs libres.
# {metal} et {primary} sont remplis à la génération.
# ---------------------------------------------------------------------------
UNIVERS = {
    "Gothique": {
        "surface": "on a black veined-marble surface with a deep velvet backdrop",
        "light": "chiaroscuro lighting, a single hard side light, deep shadows, a cold moonlight rim, faint drifting mist",
        "motifs": "a jewelled crown cap, {metal} filigree, cathedral-arch engraving and a jewelled gemstone signature",
        "color_primary": "deep blood red",
        "color_secondary": "antique gold",
        "metal": "gold",
        "grading": "deep blacks, rich {primary} midtones, {metal} highlights, cinematic contrast",
    },
    "Féérique": {
        "surface": "on a mother-of-pearl surface with soft moss, scattered petals and a rosy mist",
        "light": "soft diffused light, glowing halos and floating sparkling particles",
        "motifs": "delicate wings, flowers, fine spirals, {metal} accents and dewdrop pearls",
        "color_primary": "powder pink",
        "color_secondary": "pale gold",
        "metal": "pale gold",
        "grading": "bright airy pastels with {primary} tones, a soft {metal} glow and a gentle bloom",
    },
    "Elfique": {
        "surface": "on pale carved wood with mossy stone and foliage",
        "light": "dappled forest light with filtered sun rays",
        "motifs": "interlaced leaves, engraved runes and chiselled {metal}",
        "color_primary": "deep forest green",
        "color_secondary": "silver",
        "metal": "silver",
        "grading": "cool {primary} tones, {metal} highlights and a soft forest haze",
    },
}

# ---------------------------------------------------------------------------
# Palettes accordées (duos couleur primaire / secondaire + métal).
# "Signature de l'univers" = garder les couleurs par défaut de l'univers.
# ---------------------------------------------------------------------------
SIGNATURE = "Signature de l'univers"
PALETTES = {
    SIGNATURE: None,
    "Rouge sang & or": {"primary": "deep blood red", "secondary": "antique gold", "metal": "gold"},
    "Pourpre & argent": {"primary": "deep purple", "secondary": "aged silver", "metal": "silver"},
    "Améthyste & or": {"primary": "amethyst violet", "secondary": "antique gold", "metal": "gold"},
    "Violet profond & argent": {"primary": "deep violet", "secondary": "aged silver", "metal": "silver"},
    "Prune & bronze": {"primary": "dark plum", "secondary": "warm bronze", "metal": "bronze"},
    "Bordeaux & cuivre": {"primary": "dark bordeaux", "secondary": "copper", "metal": "copper"},
    "Émeraude & or": {"primary": "deep emerald green", "secondary": "antique gold", "metal": "gold"},
    "Bleu nuit & argent": {"primary": "midnight blue", "secondary": "aged silver", "metal": "silver"},
    "Noir & or (monochrome)": {"primary": "deep black", "secondary": "antique gold", "metal": "gold"},
    "Rose poudré & or": {"primary": "powder pink", "secondary": "pale gold", "metal": "pale gold"},
    "Lilas & argent": {"primary": "soft lilac", "secondary": "silver", "metal": "silver"},
    "Turquoise & argent": {"primary": "deep teal turquoise", "secondary": "silver", "metal": "silver"},
}

# ---------------------------------------------------------------------------
# Silhouettes facultatives du contenant (forme du flacon / tube / boîtier).
# "Signature du produit" = garder la forme d'origine du produit.
# ---------------------------------------------------------------------------
SIG_SIL = "Signature du produit"
# Forme ADJECTIVALE : elle remplace la forme par défaut du contenant (pas un
# complément collé en fin de phrase), pour que le modèle change vraiment la forme.
SILHOUETTES = {
    SIG_SIL: None,
    "Haute et élancée": "tall and slender",
    "Ronde et galbée": "rounded and bulbous",
    "Anguleuse / facettée": "sharply angular and heavily faceted",
    "Art déco (gradins)": "stepped art-deco",
    "Cœur": "heart-shaped",
    "Hexagonale": "hexagonal",
    "Cylindrique épurée": "clean cylindrical",
    "Goutte / teardrop": "teardrop-shaped",
    "Sphère / orbe": "spherical, orb-like",
    "Rectangulaire minimaliste": "minimalist rectangular",
    "Baroque ornementée": "ornately sculpted, baroque",
    "Obélisque (flacon haut)": "tall, obelisk-like",
}

# ---------------------------------------------------------------------------
# Bloc 3 — PRODUIT -> forme + mécanique ouvert/fermé
# ---------------------------------------------------------------------------
PRODUITS = {
    # noun = le contenant ; base_shape = forme par défaut (remplacée par la silhouette) ;
    # detail = matières + ornements + fermeture (jamais touché par la silhouette).
    # family = flacon / tube / boitier (pour les silhouettes pertinentes).
    "Parfum": {
        "noun": "perfume bottle", "base_shape": "faceted crystal", "family": "flacon",
        "detail": "with ornate metal filigree and a jewelled crown cap",
        "closed": "the cap seated on the bottle",
        "open": "the cap removed and set upright beside it, the atomizer visible, the bottle neck open; only one cap in frame",
    },
    "Rouge à lèvres (bâton)": {
        "noun": "lipstick case", "base_shape": "faceted", "family": "tube",
        "detail": "with an ornate metal body, housing a twist-up oxblood bullet",
        "closed": "capped, the bullet retracted",
        "open": "the cap removed and set beside it, the bullet wound half-up; only one cap in frame",
    },
    "Rouge liquide (doe-foot)": {
        "noun": "liquid-lipstick tube", "base_shape": "tall faceted crystal", "family": "tube",
        "detail": "filled with glossy lacquer, with ornate filigree and a jewelled crown cap",
        "closed": "the cap screwed on top, no applicator visible",
        "open": ("the tube UNCAPPED with its neck open and empty, the cap held upright beside it "
                 "with the doe-foot wand attached to the underside of that SAME cap, the tip coated in glossy lacquer; "
                 "only one cap and one wand in frame"),
    },
    "Fard à paupières (palette)": {
        "noun": "eyeshadow palette", "base_shape": "rectangular lacquered", "family": "boitier",
        "detail": "with ornate metalwork",
        "closed": "the lid closed, front view",
        "open": "the lid open to reveal the mirror and the embossed pressed-powder pans",
    },
    "Eye-liner (feutre)": {
        "noun": "liquid eyeliner pen", "base_shape": "slim", "family": "tube",
        "detail": "with a fine felt tip and an ornate metal body",
        "closed": "capped",
        "open": "the cap removed and set beside it, the fine felt tip visible, a single sharp wing-line drawn on ivory paper; only one cap in frame",
    },
    "Mascara": {
        "noun": "mascara tube", "base_shape": "slender", "family": "tube",
        "detail": "with an ornate metal collar",
        "closed": "capped, the wand inside",
        "open": "the glossy wand lifted beside it, attached to the underside of the cap; only one cap in frame",
    },
    "Vernis à ongles": {
        "noun": "nail-lacquer bottle", "base_shape": "small faceted glass", "family": "flacon",
        "detail": "with an ornate collar and a jewelled crown cap",
        "closed": "the cap-brush screwed on",
        "open": "the cap-brush lifted out beside it, one glossy drop of lacquer caught mid-fall, the neck open; only one cap in frame",
    },
    "Highlighter (compact)": {
        "noun": "highlighter compact", "base_shape": "round lacquered", "family": "boitier",
        "detail": "with ornate metalwork",
        "closed": "closed, front view",
        "open": "open to reveal the mirror and the embossed pressed powder",
    },
    "Sérum (compte-gouttes)": {
        "noun": "serum bottle", "base_shape": "faceted crystal", "family": "flacon",
        "detail": "with ornate filigree and a dropper cap",
        "closed": "the dropper seated in the bottle",
        "open": "the dropper lifted above it, a single luminous drop suspended at the tip, the neck open",
    },
    "Poudre (compact)": {
        "noun": "powder compact", "base_shape": "round lacquered", "family": "boitier",
        "detail": "with ornate metalwork",
        "closed": "closed, front view",
        "open": "open to reveal the mirror and the puff",
    },
    "Blush (compact)": {
        "noun": "blush compact", "base_shape": "round lacquered", "family": "boitier",
        "detail": "with ornate metalwork",
        "closed": "closed, front view",
        "open": "open to reveal the mirror and the embossed pressed blush powder",
    },
    # ---- Teint ----
    "Fond de teint (pompe)": {
        "noun": "foundation bottle", "base_shape": "faceted glass", "family": "flacon",
        "detail": "with an ornate metal collar and a pump dispenser",
        "closed": "the pump capped",
        "open": "the cap removed and set beside it, the pump exposed, a single drop of foundation on the nozzle; only one cap in frame",
    },
    "Correcteur (anti-cernes)": {
        "noun": "concealer tube", "base_shape": "slim", "family": "tube",
        "detail": "with an ornate metal cap",
        "closed": "capped, the wand inside",
        "open": "the cap held beside it with the doe-foot wand attached to its underside, the tip coated; only one cap in frame",
    },
    "Bronzer (compact)": {
        "noun": "bronzer compact", "base_shape": "round lacquered", "family": "boitier",
        "detail": "with ornate metalwork",
        "closed": "closed, front view",
        "open": "open to reveal the mirror and the embossed pressed bronzer",
    },
    "Poudre libre (pot)": {
        "noun": "loose-powder jar", "base_shape": "round faceted glass", "family": "boitier",
        "detail": "with an ornate metal lid and a sifter",
        "closed": "the lid closed",
        "open": "the lid removed and set beside it, the sifter visible with a fine dusting of powder",
    },
    # ---- Lèvres ----
    "Gloss (doe-foot)": {
        "noun": "lip-gloss tube", "base_shape": "tall faceted crystal", "family": "tube",
        "detail": "filled with glossy translucent gloss, with ornate filigree and a jewelled cap",
        "closed": "capped, no applicator visible",
        "open": ("the tube UNCAPPED with its neck open and empty, the cap held upright beside it "
                 "with the doe-foot wand attached to the underside of that SAME cap, the tip glossy; "
                 "only one cap and one wand in frame"),
    },
    "Baume à lèvres (stick)": {
        "noun": "lip-balm stick", "base_shape": "slim cylindrical", "family": "tube",
        "detail": "in an ornate metal case",
        "closed": "capped, the balm retracted",
        "open": "the cap removed and set beside it, the balm wound up; only one cap in frame",
    },
    "Crayon à lèvres": {
        "noun": "lip pencil", "base_shape": "slim", "family": "tube",
        "detail": "with an ornate metal cap and a sharpened tip",
        "closed": "capped",
        "open": "the cap removed and set beside it, the sharpened tip visible; only one cap in frame",
    },
    # ---- Yeux ----
    "Crayon yeux": {
        "noun": "eye pencil", "base_shape": "slim", "family": "tube",
        "detail": "with an ornate metal cap and a sharpened tip",
        "closed": "capped",
        "open": "the cap removed and set beside it, the sharpened tip visible, a single soft line drawn on ivory paper; only one cap in frame",
    },
    "Sourcils (crayon/gel)": {
        "noun": "brow pencil", "base_shape": "slim", "family": "tube",
        "detail": "with an ornate metal cap and a spoolie brush at the other end",
        "closed": "capped",
        "open": "the cap removed and set beside it, the fine tip visible; only one cap in frame",
    },
    # ---- Soin ----
    "Crème (pot)": {
        "noun": "cream jar", "base_shape": "round faceted glass", "family": "boitier",
        "detail": "with an ornate metal lid",
        "closed": "the lid closed",
        "open": "the lid removed and set beside it, the smooth cream surface visible with a single swirl",
    },
    "Huile (compte-gouttes)": {
        "noun": "facial-oil bottle", "base_shape": "faceted crystal", "family": "flacon",
        "detail": "with ornate filigree and a dropper cap",
        "closed": "the dropper seated in the bottle",
        "open": "the dropper lifted above it, a single golden drop of oil suspended at the tip, the neck open",
    },
    "Brume / lotion (spray)": {
        "noun": "mist spray bottle", "base_shape": "tall faceted glass", "family": "flacon",
        "detail": "with an ornate metal collar and a fine-mist atomizer",
        "closed": "the cap on the atomizer",
        "open": "the cap removed and set beside it, a fine mist spraying from the atomizer; only one cap in frame",
    },
    "Démaquillant (pompe)": {
        "noun": "cleansing bottle", "base_shape": "tall faceted glass", "family": "flacon",
        "detail": "with an ornate metal collar and a pump",
        "closed": "the pump locked down",
        "open": "the pump raised, a single drop at the nozzle",
    },
    "Masque (tube)": {
        "noun": "face-mask tube", "base_shape": "sleek", "family": "tube",
        "detail": "with an ornate metal cap",
        "closed": "capped",
        "open": "the cap removed and set beside it, a ribbon of mask squeezed onto the surface; only one cap in frame",
    },
    # ---- Maison / parfum ----
    "Bougie parfumée": {
        "noun": "scented candle", "base_shape": "faceted glass", "family": "boitier",
        "detail": "in an ornate glass vessel with a metal lid",
        "closed": "the lid closed, the candle unlit",
        "open": "the lid removed and set beside it, the wick lit with a soft steady flame",
    },
    "Eau de toilette": {
        "noun": "eau de toilette bottle", "base_shape": "faceted crystal", "family": "flacon",
        "detail": "with ornate metal filigree and a jewelled cap",
        "closed": "the cap seated on the bottle",
        "open": "the cap removed and set beside it, the atomizer visible, the neck open; only one cap in frame",
    },
    "Parfum solide (compact)": {
        "noun": "solid-perfume compact", "base_shape": "round lacquered", "family": "boitier",
        "detail": "with ornate metalwork",
        "closed": "closed, front view",
        "open": "open to reveal the mirror and the smooth scented balm",
    },
}

# ---------------------------------------------------------------------------
# Bloc 4 — PLAN -> mise en scène (+ négatifs, + mode)
# ---------------------------------------------------------------------------
PLANS = {
    "Héro fermé": {
        "mode": "closed",
        "staging": "A single hero product shot, the product centred, elegant and still",
        "negative": "",
    },
    "Ouvert avec applicateur": {
        "mode": "open",
        "staging": "An open-product shot, the product shown opened with its applicator beside it",
        "negative": "two caps, a second cap, a closed cap on an open tube, duplicated applicator",
    },
    "Planche produit (4 vues)": {
        "mode": "closed",
        "staging": ("A product sheet layout on one image, four labelled views: full product (front view), "
                    "open product, material detail close-up, and texture swatch"),
        "negative": "",
    },
    "Plan de groupe (gamme)": {
        "mode": "group",
        "staging": ("A group shot of the whole collection: the products shown EXACTLY as in the reference images, "
                    "arranged together on the shared surface, consistent lighting across all of them"),
        "negative": "redesigned products, altered packaging, inconsistent lighting",
    },
    "Texture / swatch": {
        "mode": "swatch",
        "staging": "An extreme macro of the product texture and swatch only, rich pigment, glossy finish",
        "negative": "",
    },
}

RATIOS = ["3:4", "9:16", "16:9", "1:1"]

# Formulation de cadrage (les modèles à instruction, GPT Image / Nano Banana, suivent
# mieux une consigne de composition qu'un simple "aspect ratio"). La taille exacte
# en pixels reste réglée sur le générateur.
RATIO_PHRASE = {
    "3:4": "vertical 3:4 portrait composition",
    "9:16": "tall vertical 9:16 composition",
    "16:9": "wide horizontal 16:9 composition",
    "1:1": "square 1:1 composition",
}

# Token anglais propre (nom de fichier) par type de produit
PRODUIT_EN = {
    "Parfum": "Perfume",
    "Rouge à lèvres (bâton)": "Lipstick",
    "Rouge liquide (doe-foot)": "Liquid-Lipstick",
    "Fard à paupières (palette)": "Eyeshadow-Palette",
    "Eye-liner (feutre)": "Eyeliner",
    "Mascara": "Mascara",
    "Vernis à ongles": "Nail-Lacquer",
    "Highlighter (compact)": "Highlighter",
    "Sérum (compte-gouttes)": "Serum",
    "Poudre (compact)": "Powder",
    "Blush (compact)": "Blush",
    "Fond de teint (pompe)": "Foundation",
    "Correcteur (anti-cernes)": "Concealer",
    "Bronzer (compact)": "Bronzer",
    "Poudre libre (pot)": "Loose-Powder",
    "Gloss (doe-foot)": "Lip-Gloss",
    "Baume à lèvres (stick)": "Lip-Balm",
    "Crayon à lèvres": "Lip-Pencil",
    "Crayon yeux": "Eye-Pencil",
    "Sourcils (crayon/gel)": "Brow",
    "Crème (pot)": "Cream",
    "Huile (compte-gouttes)": "Oil",
    "Brume / lotion (spray)": "Mist",
    "Démaquillant (pompe)": "Cleanser",
    "Masque (tube)": "Mask",
    "Bougie parfumée": "Candle",
    "Eau de toilette": "Eau-de-Toilette",
    "Parfum solide (compact)": "Solid-Perfume",
}

# Noms proposés par univers (auto-nommage, mode Gamme)
NOMS = {
    "Gothique": ["Blood Moon", "Crimson Veil", "Midnight Ritual", "Lunar Halo",
                 "Moonlight Elixir", "Obsidian Kiss", "Nightshade", "Velvet Crypt"],
    "Féérique": ["Dew Bloom", "Rosewing", "Petal Dust", "Fairy Light",
                 "Morning Veil", "Blossom Charm", "Pixie Glow", "Spring Whisper"],
    "Elfique": ["Moonleaf", "Silverthorn", "Wildwood", "Elven Grace",
                "Forest Rune", "Mithril Shine", "Verdant Vow", "Starbark"],
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _slug(s):
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-") or "sans-nom"


def _gamme_id(marque, univers):
    return "{}-{}".format(_slug(marque), _slug(univers))


def _clean(s):
    """Nettoie un texte libre pour un nom de fichier : enlève les accents,
    remplace tout caractère non alphanumérique par un tiret, garde la casse."""
    if not s:
        return ""
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"[^A-Za-z0-9]+", "-", s)
    return s.strip("-")


def _filename_prefix(marque, nom, produit):
    """MARQUE-Nom-Produit prêt pour filename_prefix (Save Image)."""
    produit_en = PRODUIT_EN.get(produit, _clean(produit))
    parts = [_clean(marque), _clean(nom), produit_en]
    return "-".join(p for p in parts if p) or "cosmetic"


def _norm(s):
    """Normalise un nom de produit : minuscules, sans accent, sans parenthèse,
    sans séparateur — pour une comparaison tolérante."""
    s = unicodedata.normalize("NFKD", s.lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.split("(")[0]                     # on retire le qualificatif entre parenthèses
    return re.sub(r"[^a-z0-9]+", "", s)


# table de correspondance : nom normalisé -> clé officielle du produit
_PRODUIT_LOOKUP = {_norm(k): k for k in PRODUITS}
# alias courants (FR / EN) tolérés en plus
_ALIASES = {
    "parfum": "Parfum", "perfume": "Parfum",
    "rougealevres": "Rouge à lèvres (bâton)", "rougebaton": "Rouge à lèvres (bâton)",
    "lipstick": "Rouge à lèvres (bâton)",
    "rougeliquide": "Rouge liquide (doe-foot)", "liquidlipstick": "Rouge liquide (doe-foot)",
    "gloss": "Gloss (doe-foot)", "lipgloss": "Gloss (doe-foot)",
    "fard": "Fard à paupières (palette)", "fardapaupieres": "Fard à paupières (palette)",
    "eyeshadow": "Fard à paupières (palette)", "palette": "Fard à paupières (palette)",
    "eyeliner": "Eye-liner (feutre)", "liner": "Eye-liner (feutre)",
    "mascara": "Mascara",
    "vernis": "Vernis à ongles", "vernisaongles": "Vernis à ongles",
    "naillacquer": "Vernis à ongles", "nailpolish": "Vernis à ongles",
    "highlighter": "Highlighter (compact)", "enlumineur": "Highlighter (compact)",
    "serum": "Sérum (compte-gouttes)",
    "poudre": "Poudre (compact)", "powder": "Poudre (compact)",
    "blush": "Blush (compact)", "fardajoues": "Blush (compact)",
    "fardenpoudre": "Blush (compact)", "rougeajoues": "Blush (compact)",
    "fonddeteint": "Fond de teint (pompe)", "foundation": "Fond de teint (pompe)",
    "correcteur": "Correcteur (anti-cernes)", "anticernes": "Correcteur (anti-cernes)",
    "concealer": "Correcteur (anti-cernes)",
    "bronzer": "Bronzer (compact)", "poudredesoleil": "Bronzer (compact)", "terracotta": "Bronzer (compact)",
    "poudrelibre": "Poudre libre (pot)", "loosepowder": "Poudre libre (pot)",
    "baume": "Baume à lèvres (stick)", "baumealevres": "Baume à lèvres (stick)", "lipbalm": "Baume à lèvres (stick)",
    "crayonalevres": "Crayon à lèvres", "lipliner": "Crayon à lèvres", "lippencil": "Crayon à lèvres",
    "crayonyeux": "Crayon yeux", "eyepencil": "Crayon yeux", "kohl": "Crayon yeux", "khol": "Crayon yeux",
    "sourcils": "Sourcils (crayon/gel)", "brow": "Sourcils (crayon/gel)", "eyebrow": "Sourcils (crayon/gel)",
    "crayonsourcils": "Sourcils (crayon/gel)", "gelsourcils": "Sourcils (crayon/gel)",
    "creme": "Crème (pot)", "cremevisage": "Crème (pot)", "facecream": "Crème (pot)",
    "moisturizer": "Crème (pot)", "hydratant": "Crème (pot)",
    "huile": "Huile (compte-gouttes)", "huilevisage": "Huile (compte-gouttes)", "oil": "Huile (compte-gouttes)",
    "brume": "Brume / lotion (spray)", "lotion": "Brume / lotion (spray)", "spray": "Brume / lotion (spray)",
    "mist": "Brume / lotion (spray)", "tonique": "Brume / lotion (spray)",
    "demaquillant": "Démaquillant (pompe)", "cleanser": "Démaquillant (pompe)", "nettoyant": "Démaquillant (pompe)",
    "masque": "Masque (tube)", "mask": "Masque (tube)",
    "bougie": "Bougie parfumée", "bougieparfumee": "Bougie parfumée", "candle": "Bougie parfumée",
    "eaudetoilette": "Eau de toilette", "edt": "Eau de toilette",
    "parfumsolide": "Parfum solide (compact)", "solidperfume": "Parfum solide (compact)",
}
for _a, _k in _ALIASES.items():
    _PRODUIT_LOOKUP.setdefault(_a, _k)


def _match_produit(s):
    """Renvoie la clé officielle du produit pour une saisie tolérante (casse,
    accents, séparateurs, parenthèses) avec repli sur les fautes de frappe, ou None."""
    n = _norm(s)
    if not n:
        return None
    if n in _PRODUIT_LOOKUP:
        return _PRODUIT_LOOKUP[n]
    close = difflib.get_close_matches(n, list(_PRODUIT_LOOKUP.keys()), n=1, cutoff=0.82)
    return _PRODUIT_LOOKUP[close[0]] if close else None


_METAL_TABLE = {
    "gold": "gold", "or": "gold", "dore": "gold", "golden": "gold",
    "silver": "silver", "argent": "silver", "argente": "silver",
    "bronze": "bronze", "copper": "copper", "cuivre": "copper",
    "platinum": "platinum", "platine": "platinum", "rose": "rose gold",
}


def _metal_from(text):
    """Déduit un métal d'un texte libre (pour la couleur secondaire)."""
    t = unicodedata.normalize("NFKD", text.lower())
    t = "".join(c for c in t if not unicodedata.combining(c))
    for w in re.findall(r"[a-z]+", t):
        if w in _METAL_TABLE:
            return _METAL_TABLE[w]
    return None


def _resolve_colors(univers, palette, c_prim, c_sec):
    """Détermine (primary, secondary, metal) : univers par défaut,
    puis palette éventuelle, puis surcharge par les champs libres."""
    u = UNIVERS[univers]
    primary = u["color_primary"]
    secondary = u["color_secondary"]
    metal = u["metal"]

    if palette and palette != SIGNATURE and PALETTES.get(palette):
        p = PALETTES[palette]
        primary, secondary, metal = p["primary"], p["secondary"], p["metal"]

    if c_prim and c_prim.strip():
        primary = c_prim.strip()
    if c_sec and c_sec.strip():
        secondary = c_sec.strip()
        m = _metal_from(secondary)
        if m:
            metal = m

    return primary, secondary, metal


def _brand_line(metal, marque, nom):
    text = '"{}"'.format(marque.strip()) if marque.strip() else '"BRAND"'
    if nom and nom.strip():
        text += ', "{}"'.format(nom.strip())
    return "{} serif text on the pack: {}".format(metal.capitalize(), text)


def _resolve_silhouette(silhouette, libre):
    """Renvoie l'adjectif de forme à utiliser, ou '' pour garder la forme d'origine."""
    if libre and libre.strip():
        return libre.strip()
    if silhouette and silhouette != SIG_SIL and SILHOUETTES.get(silhouette):
        return SILHOUETTES[silhouette]
    return ""


def _product_clause(produit_data, mode, shape_adj=""):
    # La silhouette remplace la forme par défaut ; matières et ornements restent.
    shape = shape_adj if shape_adj else produit_data["base_shape"]
    head = "a {} {} {}".format(shape, produit_data["noun"], produit_data["detail"])
    head = re.sub(r"\s+", " ", head).strip()
    if mode == "open":
        return "{}, {}".format(head, produit_data["open"])
    if mode == "swatch":
        return head
    return "{}, {}".format(head, produit_data["closed"])


def _generic_product(name):
    """Produit « libre » : un contenant générique construit à partir des mots de l'utilisateur."""
    return {
        "noun": name.strip(), "base_shape": "faceted crystal", "family": "generic",
        "detail": "with ornate metalwork and a jewelled cap",
        "closed": "closed, front view",
        "open": "opened, its lid or applicator set beside it; only one cap in frame",
    }


def build_single(univers, produit, plan, ratio, marque, nom,
                 palette=SIGNATURE, couleur_primaire="", couleur_secondaire="",
                 silhouette=SIG_SIL, silhouette_libre="", produit_data=None):
    """Assemble un prompt. Renvoie (prompt, negative, gamme_id, filename_prefix).
    produit_data : dictionnaire de produit à utiliser à la place de la table (mode libre)."""
    u = UNIVERS[univers]
    p = produit_data if produit_data is not None else PRODUITS[produit]
    pl = PLANS[plan]
    mode = pl["mode"]

    primary, secondary, metal = _resolve_colors(
        univers, palette, couleur_primaire, couleur_secondaire
    )

    palette_phrase = "{} and {}".format(primary, secondary)
    motifs = u["motifs"].format(metal=metal)
    grading = u["grading"].format(primary=primary, metal=metal)

    da = ("Universe — {}: {}; {}; palette of {}; signature details are {}.").format(
        univers, u["surface"], u["light"], palette_phrase, motifs)

    shape_adj = ""
    if mode == "group":
        product_clause = ("the products exactly as shown in the reference images "
                          "(@Image 1..N), unchanged")
        brand = _brand_line(metal, marque, "")
    else:
        shape_adj = _resolve_silhouette(silhouette, silhouette_libre)
        product_clause = _product_clause(p, mode, shape_adj)
        brand = _brand_line(metal, marque, nom)

    parts = [BASE, da, product_clause]
    # Renforcement : la silhouette est répétée en consigne forte, tôt dans le prompt.
    if shape_adj:
        parts.append(
            "IMPORTANT: the container's overall shape is distinctly {adj} — "
            "a {adj} {noun}, clearly not a standard {noun}.".format(
                adj=shape_adj, noun=p["noun"]))
    parts += [
        pl["staging"],
        brand,
        "Cinematic color grading: {}.".format(grading),
        "{}.".format(RATIO_PHRASE.get(ratio, "aspect ratio " + ratio)),
    ]
    prompt = " ".join(s.rstrip(" .") + "." for s in parts)

    neg_parts = [NEGATIVE_BASE]
    if pl["negative"]:
        neg_parts.append(pl["negative"])
    negative = ", ".join(neg_parts)

    fname = _filename_prefix(marque, nom, produit)
    return prompt, negative, _gamme_id(marque, univers), fname


# ---------------------------------------------------------------------------
# Nœud 1 — un produit
# ---------------------------------------------------------------------------
class CosmeticsLuxePrompt:
    """Un produit cosmétique de luxe -> un prompt photoréaliste cohérent."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "univers": (list(UNIVERS.keys()),),
                "produit": (list(PRODUITS.keys()),),
                "plan": (list(PLANS.keys()),),
                "ratio": (RATIOS,),
                "marque": ("STRING", {"default": "NOCTURIA", "multiline": False}),
                "nom_produit": ("STRING", {"default": "", "multiline": False}),
                "palette": (list(PALETTES.keys()),),
                "couleur_primaire": ("STRING", {"default": "", "multiline": False}),
                "couleur_secondaire": ("STRING", {"default": "", "multiline": False}),
                "silhouette": (list(SILHOUETTES.keys()),),
                "silhouette_libre": ("STRING", {"default": "", "multiline": False}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("prompt", "negative", "gamme_id", "filename_prefix")
    FUNCTION = "generate"
    CATEGORY = "Cosmétiques Luxe"

    def generate(self, univers, produit, plan, ratio, marque, nom_produit,
                 palette, couleur_primaire, couleur_secondaire,
                 silhouette, silhouette_libre):
        prompt, negative, gamme_id, filename_prefix = build_single(
            univers, produit, plan, ratio, marque, nom_produit,
            palette, couleur_primaire, couleur_secondaire,
            silhouette, silhouette_libre
        )
        return (prompt, negative, gamme_id, filename_prefix)


# ---------------------------------------------------------------------------
# Nœud 2 — une gamme entière
# ---------------------------------------------------------------------------
class CosmeticsLuxeGamme:
    """Une gamme -> N prompts partageant la même DA et la même palette, + le groupe.

    'produits' : un produit par ligne (nom exact de la liste), suivi
    éventuellement de '|' et d'un nom de produit.
    """

    @classmethod
    def INPUT_TYPES(cls):
        exemple = ("Parfum | Eau de Parfum\n"
                   "Rouge liquide (doe-foot) | Crimson Veil\n"
                   "Vernis à ongles | Blood Moon")
        return {
            "required": {
                "univers": (list(UNIVERS.keys()),),
                "plan_produits": (["Héro fermé", "Ouvert avec applicateur"],),
                "ratio": (RATIOS,),
                "marque": ("STRING", {"default": "NOCTURIA", "multiline": False}),
                "produits": ("STRING", {"default": exemple, "multiline": True}),
                "auto_nom": ("BOOLEAN", {"default": True}),
                "palette": (list(PALETTES.keys()),),
                "couleur_primaire": ("STRING", {"default": "", "multiline": False}),
                "couleur_secondaire": ("STRING", {"default": "", "multiline": False}),
                "silhouette": (list(SILHOUETTES.keys()),),
                "silhouette_libre": ("STRING", {"default": "", "multiline": False}),
                "index": ("INT", {"default": 1, "min": 1, "max": 999}),
                "produit_libre": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING", "INT", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("prompts", "group_prompt", "filename_prefixes", "gamme_id", "count",
                    "prompt_index", "filename_index", "ignored")
    FUNCTION = "generate"
    CATEGORY = "Cosmétiques Luxe"

    def generate(self, univers, plan_produits, ratio, marque, produits, auto_nom,
                 palette, couleur_primaire, couleur_secondaire,
                 silhouette, silhouette_libre, index, produit_libre=True):
        lignes = [l.strip() for l in produits.splitlines() if l.strip()]
        pool = list(NOMS.get(univers, []))
        labelled = []     # prompts avec en-tête "# nom"
        raw = []          # prompts bruts (pour la sortie index)
        prefixes = []
        noms_utilises = []
        ignores = []      # lignes écartées (mode libre désactivé)
        libres = []       # lignes traitées en mode libre (mécanique générique)

        for ligne in lignes:
            if "|" in ligne:
                prod_in, nom = [x.strip() for x in ligne.split("|", 1)]
            else:
                prod_in, nom = ligne.strip(), ""
            prod = _match_produit(prod_in)          # tolérance orthographe/casse/accents
            pdata = None
            if prod is None:
                if produit_libre and prod_in.strip():
                    pdata = _generic_product(prod_in)   # repli : contenant générique
                    prod = prod_in.strip()
                    libres.append(prod_in)
                else:
                    ignores.append(prod_in)
                    continue
            if not nom and auto_nom and pool:
                nom = pool[len(noms_utilises) % len(pool)]
            noms_utilises.append(nom or prod)
            pr, _neg, _gid, fname = build_single(
                univers, prod, plan_produits, ratio, marque, nom,
                palette, couleur_primaire, couleur_secondaire,
                silhouette, silhouette_libre, produit_data=pdata
            )
            labelled.append("# {}\n{}".format(nom or prod, pr))
            raw.append(pr)
            prefixes.append(fname)

        joined = "\n\n---\n\n".join(labelled)
        if ignores:
            joined += "\n\n---\n# ⚠ produits ignorés (nom inconnu) : " + ", ".join(ignores)

        filename_prefixes = "\n".join(prefixes)
        n = len(raw)

        # Sortie d'un seul produit, choisi par 'index' (1 = premier), à brancher
        # directement sur le générateur. Index borné à la plage disponible.
        if n:
            i = min(max(int(index), 1), n) - 1
            prompt_index = raw[i]
            filename_index = prefixes[i]
        else:
            prompt_index = ""
            filename_index = ""

        group_prompt, _n2, gid, _f = build_single(
            univers, "Parfum", "Plan de groupe (gamme)", ratio, marque, "",
            palette, couleur_primaire, couleur_secondaire,
            silhouette, silhouette_libre
        )
        group_prompt = group_prompt.replace("@Image 1..N",
                                            "@Image 1..{}".format(max(n, 1)))
        group_prompt = ("[Charger d'abord les {} produits rendus en Load Image, "
                        "un par entrée] ".format(n) + group_prompt)

        # Sortie dédiée : ce qui a été écarté ou traité en mode libre, visible d'un coup d'œil.
        msgs = []
        if ignores:
            msgs.append("⚠ {} ligne(s) ignorée(s) (nom non reconnu) : {}".format(
                len(ignores), " | ".join(ignores)))
        if libres:
            msgs.append("ℹ {} produit(s) en mode libre (mécanique générique) : {}".format(
                len(libres), " | ".join(libres)))
        ignored = "\n".join(msgs) if msgs else "✓ tous les produits reconnus ({})".format(n)

        return (joined, group_prompt, filename_prefixes, gid, n,
                prompt_index, filename_index, ignored)
