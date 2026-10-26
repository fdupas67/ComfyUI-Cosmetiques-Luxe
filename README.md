# Cosmétiques Luxe pour ComfyUI

Préparez les prompts de vos cosmétiques de luxe, déclinez leur présentation et utilisez vos images comme références pour des publicités animées.

Créé par **Franck Dupas — Franck D Digital AI**.

![Exemple de parfum NOCTURIA](assets/NOCTURIA-Eau-de-Parfum.webp)

## Ce que propose le paquet

- **Cosmétiques Luxe — Produit** : une description personnalisée pour un produit, avec univers, palette, silhouette, présentation et inscriptions.
- **Cosmétiques Luxe — Gamme** : plusieurs descriptions partageant des réglages communs, une sélection par index et un prompt de composition de références.
- **Trois univers** : Gothique, Féérique et Elfique.
- **28 types de produits** : parfums, maquillage, soins et vernis.
- **Deux workflows de démonstration** : création et retouche d'images, puis animation avec des références.

Les nodes Cosmétiques Luxe produisent du texte et des préfixes de fichiers. La génération d'images ou de vidéos est effectuée par les nodes reliés. La fidélité des contenants, des personnages et des inscriptions doit être contrôlée après chaque rendu.

## Installation rapide

1. Décompressez le paquet et copiez `cosmetics_luxe` dans le dossier `custom_nodes` de votre installation ComfyUI.
2. Vérifiez que `__init__.py` et `nodes.py` sont directement dans ce dossier, sans niveau `cosmetics_luxe` supplémentaire.
3. Redémarrez ComfyUI.
4. Recherchez **Cosmétiques Luxe** pour ajouter Produit ou Gamme.

Si vous téléchargez le code depuis GitHub, le dossier extrait peut porter le nom du dépôt suivi de la branche : son contenu doit aboutir directement dans `custom_nodes/cosmetics_luxe/`.

Les deux nodes utilisent uniquement Python standard. Les workflows complets demandent aussi leurs générateurs et éventuels nodes supplémentaires.

## Premier essai

Dans Produit, choisissez **Gothique**, **Parfum**, **Héro fermé**, marque **NOCTURIA**, nom **Black Swan**, palette **Rouge sang & or**. Laissez la silhouette sur **Signature du produit** et les champs libres vides.

```text
Produit.prompt → Générateur d'images.prompt
Générateur d'images.IMAGE → Save Image.images
Produit.filename_prefix → Save Image.filename_prefix
```

Réglez les dimensions dans le générateur : `ratio` dans Cosmétiques Luxe ne fait qu'ajouter une indication au prompt. Connectez `negative` seulement si votre générateur et le workflow le prennent en charge.

## Workflows fournis

| Fichier | Contenu |
|---|---|
| [Tuto-Cosmétiques-Luxe.json](workflows/Tuto-Cosmétiques-Luxe.json) | Produits, égéries, références, retouches et planche de produits. |
| [Tuto-Cosmetics-Video-WAN-3.0.json](workflows/Tuto-Cosmetics-Video-WAN-3.0.json) | Scène publicitaire complète ou animation d'un produit seul. |

Chargez le JSON dans ComfyUI, sélectionnez vos images dans les Load Image et activez uniquement la branche à utiliser. Plusieurs branches sont sauvegardées en bypass.

Les exemples utilisent notamment `OpenAIGPTImageNodeV2`, `Wan3ReferenceToVideoApi` et `SaveText`. Les deux générateurs API demandent les accès, modèles disponibles et crédits propres à votre installation. `SaveText` est facultatif si vous retirez ses nodes et connexions pour ne garder que l'enregistrement des images. Le node Cosmétiques Luxe ne fournit pas ces services.

Les références personnelles nommées dans les workflows ne sont pas incluses. Le parfum présent dans `assets/` sert d'exemple ; chargez vos propres produits, personnages et lieux.

## À vérifier avant de lancer les exports du tutoriel

- **Gamme** est branché via `group_prompt` avec quatre références. L'index n'y sélectionne pas le contenu de l'image ; `prompt_index` sert à la génération individuelle.
- **CREER PLANCHE PRODUITS** annonce six références dans le prompt, mais seules quatre sont connectées dans cet export. Complétez les connexions si le générateur accepte six références, ou adaptez le prompt.
- Dans le workflow vidéo, adaptez les noms de produits, les gestes, la durée, le ratio et le préfixe d'enregistrement. Le prompt de produit seul contient des restes de texte sur un sérum ; un remplacement cohérent est fourni dans le manuel.
- Si un champ ou une sortie manque sur un ancien node enregistré, ajoutez une instance neuve du node installé et reportez ses connexions dans une copie du workflow.

## Documentation

- [Manuel complet](docs/manuel.md) : installation, branchements, réglages, exemples de prompts, préparation vidéo et dépannage.
- [Version HTML du manuel](docs/manuel.html) : à ouvrir dans un navigateur après téléchargement.
- [Aide courte pour ComfyUI](docs/aide_rapide.md) : à copier dans une note Markdown.
- [Changements du paquet documentaire](docs/changements_documentation.md).

Le code de génération des prompts et les connexions des workflows sont conservés dans cette édition documentaire. Les observations et réglages à adapter sont explicités dans le manuel ; les résultats dépendent du générateur et des références utilisés.

## Licence

Voir [LICENSE](LICENSE) pour les conditions MIT du paquet. Les extensions, modèles et services utilisés ont leurs propres conditions.
