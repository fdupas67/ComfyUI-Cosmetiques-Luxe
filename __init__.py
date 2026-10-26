# -*- coding: utf-8 -*-
# © 2026 Franck Dupas (Franck D Digital AI) — Licence MIT (voir LICENSE).
"""Cosmétiques Luxe — custom nodes ComfyUI (générateur de prompts)."""

from .nodes import CosmeticsLuxePrompt, CosmeticsLuxeGamme

NODE_CLASS_MAPPINGS = {
    "CosmeticsLuxePrompt": CosmeticsLuxePrompt,
    "CosmeticsLuxeGamme": CosmeticsLuxeGamme,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CosmeticsLuxePrompt": "Cosmétiques Luxe — Produit",
    "CosmeticsLuxeGamme": "Cosmétiques Luxe — Gamme",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
