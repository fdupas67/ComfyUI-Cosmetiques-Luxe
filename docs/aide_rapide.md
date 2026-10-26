# Cosmétiques Luxe — aide rapide

Les nodes préparent les prompts. Le générateur relié crée les images ; Save Image les enregistre.

## Produit

1. Choisir univers, produit, plan, marque et nom.
2. Ajuster palette et silhouette ; les champs libres prennent la priorité.
3. Relier `prompt` au générateur et son image à Save Image.
4. Relier `filename_prefix` au préfixe de Save Image.
5. Régler les dimensions sur le générateur. `ratio` ne les modifie pas.

`negative` ne se branche que si le générateur et le workflow le prennent en charge. `gamme_id` est un identifiant textuel, pas un verrou visuel.

## Gamme

Une ligne par produit : `Parfum | Black Swan`.

- `prompts` : toutes les descriptions dans un seul texte, sans exécution automatique en lot.
- `prompt_index` : un produit choisi avec `index`, à partir de 1.
- `filename_index` : le nom du produit sélectionné.
- `group_prompt` : une composition guidée par les images de référence, sans les noms individuels de la liste dans ce prompt.
- `count` et `ignored` : contrôler les produits retenus et les types non reconnus.

Le workflow fourni utilise `group_prompt` : Index ne sélectionne pas l'image à générer dans cette branche. Pour une collection, utiliser un préfixe d'enregistrement comme `NOCTURIA-Gamme`.

## Références et corrections

Le groupe « CREER PLANCHE PRODUITS » fonctionne avec son propre prompt et des Load Image. Vérifier le nombre et l'ordre des connexions : le prompt exporté mentionne six images mais quatre seulement sont branchées.

Pour une retouche, charger l'image retenue, demander une modification précise et vérifier le masque s'il est connecté. Contrôler les inscriptions, les contenants et le reste de l'image après correction.

## Avant un rendu

Charger vos propres références, vérifier les nodes manquants, activer la branche utile, contrôler les accès et crédits du générateur, le format et le préfixe de sortie. Les références nommées dans l'export ne sont pas embarquées dans les JSON.

Manuel complet : `docs/manuel.md` ou `docs/manuel.html` dans le paquet.

Franck Dupas — Franck D Digital AI. Voir LICENSE.
