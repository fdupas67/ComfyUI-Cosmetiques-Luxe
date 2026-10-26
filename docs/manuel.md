# Manuel de Cosmétiques Luxe pour ComfyUI

Créez des visuels de produits, préparez une collection cohérente, puis utilisez vos images comme références pour une publicité animée. Ce guide accompagne les nodes **Cosmétiques Luxe — Produit** et **Cosmétiques Luxe — Gamme**, ainsi que les deux workflows du tutoriel de Franck D Digital AI.

Les nodes Cosmétiques Luxe préparent du texte : ils ne génèrent eux-mêmes ni images ni vidéos. Le résultat dépend du générateur relié à leurs sorties. Les réglages communs orientent l'apparence d'une collection ; ils ne verrouillent pas la forme exacte d'un flacon ou son inscription.

## 1. Choisir son point de départ

| Votre objectif | Point de départ |
|---|---|
| Créer un parfum ou un autre cosmétique | Node Produit, puis générateur d'images |
| Créer une collection avec des ajustements individuels | Réutiliser Produit pour chaque article |
| Préparer plusieurs descriptions avec des réglages communs | Node Gamme |
| Générer un seul article de cette liste | Sortie `prompt_index` de Gamme |
| Réunir des produits déjà créés | Groupe « CREER PLANCHE PRODUITS », avec images de référence |
| Retoucher un nom ou ouvrir un flacon existant | Groupe « Corriger une photo » |
| Animer un produit ou une scène publicitaire | Workflow vidéo WAN fourni |

**NOCTURIA est l'exemple du tutoriel.** Vous pouvez remplacer cette marque, les noms des produits, les palettes et les univers.

## 2. Installer le node et préparer ComfyUI

### Installer Cosmétiques Luxe

1. Décompressez le paquet téléchargé.
2. Placez le dossier `cosmetics_luxe` dans le dossier `custom_nodes` de votre installation ComfyUI. Avec ComfyUI Desktop, utilisez le dossier de données de l'installation, pas un emplacement supposé dans Program Files.
3. Vérifiez la structure ci-dessous. Évitez un double dossier `cosmetics_luxe/cosmetics_luxe`.
4. Redémarrez ComfyUI et recherchez « Cosmétiques Luxe » dans la recherche de nodes.

```text
ComfyUI/
  custom_nodes/
    cosmetics_luxe/
      __init__.py
      nodes.py
      README.md
      docs/
      workflows/
```

Les deux nodes utilisent uniquement la bibliothèque standard Python. Aucune installation de paquet Python supplémentaire n'est nécessaire pour ces deux nodes seuls.

### Préparer les workflows complets

Le workflow d'images utilise notamment `OpenAIGPTImageNodeV2`, `LoadImage`, `SaveImage` et `SaveText`. Le workflow vidéo utilise `Wan3ReferenceToVideoApi` et `SaveVideo`. Installer Cosmétiques Luxe ne fournit pas à lui seul tous ces composants.

Les branches de génération fournies utilisent des nodes API. Prévoyez les accès et crédits demandés par votre installation. Le coût affiché par le générateur doit être vérifié avant de lancer le rendu ; il ne correspond pas au coût du node Cosmétiques Luxe.

Si un node apparaît manquant, identifiez son type exact et installez ou mettez à jour l'extension correspondante. Le paquet d'origine de `SaveText` n'est pas identifié dans l'export fourni. Pour se passer de l'enregistrement des prompts, retirez uniquement les nodes `SaveText` et leurs connexions ; conservez `SaveImage`.

Les noms de modèles sauvegardés dans les workflows sont des réglages de l'auteur. Sélectionnez un modèle disponible dans votre installation si celui enregistré ne l'est pas. Les entrées d'images et leurs limites dépendent du générateur choisi.

### Charger les exemples

- `workflows/Tuto-Cosmétiques-Luxe.json` : création d'images, références, retouches et composition de produits.
- `workflows/Tuto-Cosmetics-Video-WAN-3.0.json` : animation d'une scène complète ou d'un produit seul.

Ouvrez ou glissez le JSON dans ComfyUI. Dans chaque **Load Image** utilisé, sélectionnez votre propre fichier. Un nom sauvegardé dans un node ne contient pas les pixels de l'image. Le paquet fournit seulement le parfum d'exemple `assets/NOCTURIA-Eau-de-Parfum.png` et sa version WebP, pas les autres références personnelles du tutoriel.

Plusieurs branches sont enregistrées en mode bypass. Activez les nodes de la branche que vous souhaitez utiliser, y compris son node d'enregistrement, et désactivez les autres branches de génération. La couleur du cadre d'un groupe n'est pas un interrupteur : contrôlez le mode de ses nodes. Pour un premier essai simple, travaillez dans une copie du workflow ne contenant que la branche utile.

## 3. Créer votre premier parfum

Utilisez la branche « CREATION DE PRODUITS COSMETIQUES AVEC NODE Cosmétiques Luxe - Produit ».

| Champ | Valeur d'exemple |
|---|---|
| `univers` | Gothique |
| `produit` | Parfum |
| `plan` | Héro fermé |
| `ratio` | 16:9 |
| `marque` | NOCTURIA |
| `nom_produit` | Black Swan |
| `palette` | Rouge sang & or |
| `couleur_primaire`, `couleur_secondaire` | Laisser vides |
| `silhouette` | Signature du produit |
| `silhouette_libre` | Laisser vide |

Ces valeurs sont à saisir : l'export peut s'ouvrir avec un parfum elfique et d'autres noms déjà sélectionnés.

### Brancher et lancer

```text
Produit.prompt ────────────────> Générateur d'images.prompt
Générateur d'images.IMAGE ──────> Save Image.images
Produit.filename_prefix ───────> Save Image.filename_prefix
```

Si `filename_prefix` est affiché comme champ de texte, utilisez l'option de conversion du champ en entrée proposée par votre interface, puis branchez la sortie.

1. Configurez le modèle et les dimensions dans le générateur. Le champ `ratio` de Produit ne modifie pas les dimensions à sa place. Pour du 16:9, choisissez un format horizontal disponible, par exemple 2048 × 1152 si le générateur le propose.
2. Pour commencer, demandez une seule image.
3. Lancez la branche et examinez le résultat.
4. Vérifiez le nom NOCTURIA, le nom Black Swan, le bouchon, les proportions et les matières.
5. Conservez l'image retenue comme référence. Le préfixe attendu est `NOCTURIA-Black-Swan-Perfume` ; Save Image peut lui ajouter sa numérotation.

Pour créer le produit suivant, gardez les réglages communs, changez son type et son nom, puis adaptez les réglages individuels nécessaires. Produit permet ainsi de construire toute une collection.

## 4. Comprendre les réglages de Produit

| Champ | Effet |
|---|---|
| `univers` | Oriente le décor, la lumière, les motifs et les couleurs par défaut : Gothique, Féérique ou Elfique. |
| `produit` | Choisit une description de contenant et des indications d'ouverture adaptées au type de cosmétique. |
| `plan` | Décrit la présentation souhaitée dans le prompt. |
| `marque`, `nom_produit` | Demandent les inscriptions sur le contenant et alimentent le nom de fichier. |
| `palette` | Remplace les couleurs par défaut de l'univers par une association prédéfinie. |
| `couleur_primaire`, `couleur_secondaire` | Remplacent individuellement les couleurs de la palette lorsqu'ils sont remplis. |
| `silhouette` | Remplace la description de forme par défaut du contenant. |
| `silhouette_libre` | Prend la priorité sur la liste de silhouettes lorsqu'il est rempli. |
| `ratio` | Ajoute une indication de composition : 3:4, 9:16, 16:9 ou 1:1. |

Pour les couleurs, la priorité est **univers → palette → champs libres**. La couleur secondaire peut modifier le métal si le texte contient un terme reconnu, par exemple `gold`, `silver`, `or`, `argent`, `bronze` ou `cuivre`. Une couleur libre quelconque ne garantit pas cette adaptation.

Pour la forme, la priorité est **forme du produit → silhouette choisie → silhouette libre**. Décrivez une forme concrète et vérifiez les matières obtenues : certaines descriptions de forme par défaut contiennent aussi des indications de matériau. Une référence visuelle peut mieux guider le générateur, sans garantir une copie exacte.

### Les cinq présentations

| Plan | Résultat demandé |
|---|---|
| Héro fermé | Produit principal fermé, seul et mis en valeur. |
| Ouvert avec applicateur | Produit ouvert avec son accessoire ou son bouchon séparé. Contrôler la mécanique propre au produit. |
| Planche produit (4 vues) | Une image comprenant produit de face, produit ouvert, détail de matière et échantillon de texture. Ce n'est pas une rotation face/profil/dos. |
| Plan de groupe (gamme) | Composition à partir des images de référence transmises au générateur. |
| Texture / swatch | Gros plan sur une texture ou un échantillon de couleur. |

Le plan ouvert utilise aussi une consigne générique d'applicateur. Pour une bougie ou un pot, une retouche explicite de l'image peut être plus facile à contrôler. La planche quatre vues combine des consignes de produit fermé et de vue ouverte ; si le générateur les mélange, créez les vues séparément. Le swatch utilise une formulation brillante : pour une poudre mate, précisez le fini attendu dans une consigne adaptée.

### Les sorties

| Sortie | Usage |
|---|---|
| `prompt` | Texte à envoyer au générateur. |
| `negative` | Éléments à éviter, uniquement si votre générateur et votre workflow prennent en charge cette entrée. Sinon, laisser débranché. |
| `gamme_id` | Identifiant textuel dérivé de la marque et de l'univers. Ce n'est ni une graine ni un verrou de cohérence. |
| `filename_prefix` | Préfixe à transmettre au node d'enregistrement. |

Changer un réglage ou relancer une génération peut modifier le design. Pour réutiliser un contenant précis, partez de son image retenue plutôt que de compter seulement sur le même texte.

## 5. Utiliser Gamme sans confondre ses sorties

Le node Gamme prépare les descriptions de plusieurs produits avec les mêmes réglages communs. Chaque ligne du champ `produits` correspond à un produit. À gauche de `|`, saisissez son type ; à droite, son nom.

```text
Parfum | Black Swan
Vernis à ongles | Blood Moon
Rouge à lèvres (bâton) | Bloody Lips
Rouge liquide (doe-foot) | Crimson Veil
Highlighter (compact) | Lunar Halo
Sérum (compte-gouttes) | Moonlight Elixir
```

Utilisez les types complets pour éviter les ambiguïtés. Les noms courts comme `Vernis`, `Fard` ou `Rouge liquide` sont également reconnus par les alias prévus. Les fautes mineures peuvent être rapprochées d'un produit connu, mais vérifiez la description obtenue.

### Réglages propres à Gamme

- `plan_produits` : Héro fermé ou Ouvert avec applicateur pour les descriptions individuelles.
- `auto_nom` : propose un nom lorsque la partie droite d'une ligne est vide. Un nom saisi explicitement est conservé. Les noms automatiques peuvent se répéter sur une longue liste.
- `produit_libre` : si activé, un type non reconnu reçoit une description générique. Si désactivé, la ligne non reconnue est écartée.
- `index` : sélectionne un produit parmi les lignes retenues, à partir de 1. Les lignes vides et celles écartées en mode strict ne comptent pas. Un index trop grand sélectionne le dernier produit disponible.

### Choisir la bonne sortie

| Sortie | Ce qu'elle contient |
|---|---|
| `prompts` | Toutes les descriptions individuelles dans un seul texte, séparées par `---`. Ce n'est pas une boucle de génération automatique. |
| `prompt_index` | Description du seul produit sélectionné par `index`. |
| `filename_index` | Nom de fichier de ce produit sélectionné. |
| `filename_prefixes` | Liste textuelle des noms de fichiers, un par ligne. |
| `group_prompt` | Consigne de composition d'images de référence, avec leur nombre attendu. |
| `gamme_id` | Identifiant textuel de marque et d'univers. |
| `count` | Nombre de produits retenus. |
| `ignored` | Message indiquant les types non reconnus, écartés ou traités en mode libre ; sinon, confirmation de reconnaissance. |

**Point essentiel :** dans ce code, `group_prompt` ne reprend pas les noms et descriptions individuels de la liste. Il demande au générateur de suivre les images de référence. Modifier un nom dans la liste ne suffit donc pas à remplacer une inscription lorsque cette sortie est utilisée.

### Générer un produit à la fois

```text
Gamme.prompt_index ────────────> Générateur.prompt
Gamme.filename_index ──────────> Save Image.filename_prefix
Générateur.IMAGE ──────────────> Save Image.images
```

Choisissez `index = 1`, générez, puis passez à 2. C'est dans ce branchement que l'index sélectionne le contenu demandé au générateur.

### Composer une gamme en un seul rendu

Dans la branche Gamme du workflow fourni, **`group_prompt` est relié au générateur avec quatre Load Image**. Elle produit une composition de groupe à partir de ces références. Le champ `index` ne modifie pas cette consigne ; il peut encore modifier le nom du fichier si `filename_index` reste branché.

Pour enregistrer une collection, débranchez `filename_index` du préfixe d'enregistrement et utilisez un nom comme `NOCTURIA-Gamme`. Adaptez également le préfixe du SaveText éventuel. Faites correspondre le nombre de références connectées au nombre de produits prévu.

Si vous voulez expérimenter une collection à partir des descriptions seules, utilisez le texte de `prompts` et une consigne explicite de composition dans un générateur compatible. Cela demande de nouveaux visuels et ne reproduit pas automatiquement les produits déjà créés. Ce n'est pas le branchement du workflow fourni.

## 6. Ouvrir un flacon déjà créé

Utilisez le groupe **« Corriger une photo »** avec l'image retenue du flacon fermé. La retouche d'une référence permet de demander un changement local, plutôt que de recréer tout le produit depuis sa description.

```text
À partir de cette image, retire le bouchon du flacon de parfum
et pose ce même bouchon à côté sur la surface. Fais apparaître
le vaporisateur sur le col. Un seul flacon et un seul bouchon.
Conserve les proportions, matières, ornements, couleurs et
inscriptions. Préserve le décor et l'éclairage, avec une ombre
de contact naturelle sous le bouchon.
```

Pour le rouge liquide, le mascara ou le sérum, décrivez l'ensemble bouchon-tige-applicateur ou bouchon-pipette comme une seule pièce. Ne demandez pas de vaporisateur à un produit qui n'en possède pas.

Le groupe de correction exporté relie également la sortie MASK du Load Image à l'entrée de masque du générateur. Vérifiez ce masque si vous souhaitez une retouche locale. Si vous utilisez une modification globale par instruction, vérifiez si le générateur accepte l'entrée de masque débranchée. Un masque vide ou inadapté peut empêcher la correction attendue.

Après rendu, contrôlez le nombre de bouchons, leur échelle, les mains éventuelles, les inscriptions et tous les détails situés hors de la zone modifiée.

## 7. Réunir les produits dans une planche

Le groupe **« CREER PLANCHE PRODUITS »** utilise directement un prompt et des références : il ne nécessite pas de passer par le node Gamme.

1. Chargez une image retenue par produit.
2. Connectez chaque sortie IMAGE à une entrée de référence du générateur.
3. Faites correspondre les numéros du prompt à l'ordre réel des entrées. La position des nodes sur le canevas ne détermine pas cet ordre.
4. Décrivez la disposition, le décor, la lumière et les inscriptions attendues.
5. Réglez les dimensions dans le générateur, puis lancez la branche.

| Référence | Produit de l'exemple |
|---|---|
| @Image1 | Parfum Black Swan |
| @Image2 | Vernis Blood Moon |
| @Image3 | Rouge à lèvres Bloody Lips |
| @Image4 | Rouge liquide Crimson Veil |
| @Image5 | Highlighter Lunar Halo |
| @Image6 | Sérum Moonlight Elixir |

**Avant le premier rendu :** dans l'export fourni, le prompt annonce six références, mais seules les quatre premières sont connectées au générateur. Les Load Image de l'highlighter et du sérum sont présents ; connectez-les aux entrées supplémentaires si votre générateur les accepte. Si six références ne sont pas disponibles, adaptez la composition au nombre pris en charge ou choisissez un générateur adapté. La mention `@Image6` n'ajoute pas une image à elle seule.

Exemple de prompt pour un générateur recevant les six images :

```text
Crée une photographie publicitaire horizontale 16:9 réunissant
exactement six produits, chacun présent une seule fois.
@Image1 : parfum NOCTURIA Black Swan.
@Image2 : vernis NOCTURIA Blood Moon.
@Image3 : rouge à lèvres NOCTURIA Bloody Lips.
@Image4 : rouge liquide NOCTURIA Crimson Veil.
@Image5 : highlighter NOCTURIA Lunar Halo.
@Image6 : sérum NOCTURIA Moonlight Elixir.

Préserve les contenants distincts, leurs proportions, fermetures,
ornements et inscriptions. Tous restent fermés. Ne montre pas
la boîte en carton du vernis. Aucun bouchon supplémentaire.

Dispose les produits sur du marbre noir devant un velours bordeaux,
avec une lumière raffinée révélant le verre et l'or. Place le parfum
au centre, les autres produits autour, à des tailles crédibles.
Chaque produit doit rester entier, séparé et lisible, sans masquer
les autres. Une seule scène photographique, pas une grille.
N'ajoute aucun titre ni texte extérieur aux emballages.
```

Contrôlez les six silhouettes, les deux rouges à lèvres, le compte-gouttes et les inscriptions. Une composition de groupe peut redessiner certains détails malgré les références.

## 8. Corriger une inscription

Chargez la composition obtenue dans **« Corriger une photo »**. Identifiez le produit par sa position et son apparence, puis donnez le texte exact.

```text
Sur le flacon de parfum rouge situé au centre, remplace uniquement
« BLACK SWAM » par « BLACK SWAN ». Conserve la marque « NOCTURIA »,
le style, la couleur et la position du lettrage. Préserve le flacon,
ses ornements, les cinq autres produits et leurs inscriptions,
ainsi que la composition, le décor et l'éclairage.
```

Vérifiez le mot corrigé à taille réelle, puis inspectez le reste de l'image. Si la retouche dégrade les autres produits, repartez de la meilleure version et précisez la zone ou utilisez un masque adapté au générateur. Conservez les versions pour comparer.

## 9. Préparer une égérie et un lieu

Le workflow d'images contient aussi des groupes de création et retouche de personnages et de décors. Leurs prompts sont des exemples : choisissez une direction cohérente avec vos produits avant de lancer.

Pour une scène publicitaire, préparez séparément :

- le produit retenu, avec ses inscriptions lisibles ;
- un portrait de référence de la personne adulte ;
- une référence de tenue, si elle doit être conservée ;
- le lieu, avec une surface où présenter le produit et de l'espace pour la personne.

Pour une démonstration de cosmétique, laissez le visage, les mains et la zone d'application visibles. Utilisez le même portrait pour préparer les variantes du personnage. Si l'objectif est un décor vide, remplacez tout prompt de personnage et retirez les références de personne devenues inutiles, quelle que soit l'étiquette du groupe.

## 10. Animer les images

Ouvrez `Tuto-Cosmetics-Video-WAN-3.0.json`. Choisissez l'un des deux groupes et contrôlez ses nodes actifs, le prompt, les références, les réglages et l'enregistrement.

### Scène cosmétique complète

Le groupe « ANIMATION SCENE COSMETIQUE COMPLETE » prévoit quatre références :

| Entrée | Contenu |
|---|---|
| image1 | Produit |
| image2 | Visage de l'égérie |
| image3 | Tenue et silhouette |
| image4 | Lieu |

Pour un clip de 15 secondes, un découpage simple peut demander environ cinq secondes de présentation, cinq secondes de geste et cinq secondes de résultat. Les durées dans le prompt sont des intentions ; contrôlez les coupes dans la vidéo produite.

L'export contient un exemple consacré au sérum. Adaptez le produit, ses noms et les gestes avant de le réutiliser. Le préfixe de SaveVideo enregistré dans cette branche est encore `Gothic_Powder` : remplacez-le par un nom correspondant au clip, par exemple `NOCTURIA-Moonlight-Elixir-Scene`.

### Produit seul

Le groupe « ANIMATION SEULEMENT SUR PRODUIT » utilise le produit en image1 et le lieu en image2. Il est configuré dans l'export pour un clip de cinq secondes en 720p, 16:9, avec audio activé.

Le prompt sauvegardé contient des restes de formulations sur le sérum et trois plans. Pour un parfum seul, remplacez-le par une consigne cohérente comme celle-ci :

```text
Create a 5-second photorealistic luxury perfume commercial, 16:9.
@Image1 defines the NOCTURIA Black Swan bottle and its inscriptions.
@Image2 defines the gothic location.
One continuous close-up shot of the closed bottle on black marble.
Slow, subtle camera movement, realistic glass and gold reflections.
Keep the bottle shape, cap and label consistent throughout.
No hands, no opening, no additional products or added text.
Subtle gothic instrumental music, no speech.
```

Réglez aussi la durée et le ratio dans le node vidéo. Mentionner « 15 secondes » ou « 9:16 » dans le texte ne remplace pas ces réglages. Si vous comparez deux prompts, gardez la même seed lorsque le service le permet et désactivez sa randomisation ; cela ne garantit toutefois pas un résultat identique.

Pour chaque clip, inspectez le début, les changements de plan et la fin, puis regardez-le en lecture continue avec le son. Vérifiez les contenants, inscriptions, doigts, yeux, applicateurs et raccords de tenue. Pour un geste difficile, préférez un mouvement court ou une coupe entre produit posé et produit tenu. Une image corrigée ne corrige pas une vidéo déjà générée.

## 11. Résoudre les problèmes courants

| Problème | Vérification ou solution |
|---|---|
| Cosmétiques Luxe n'apparaît pas | Vérifier `__init__.py` et `nodes.py` au premier niveau du dossier installé, redémarrer ComfyUI et consulter l'erreur de chargement. |
| Node rouge ou inconnu | Identifier son type et installer le composant nécessaire. Cosmétiques Luxe ne fournit pas les générateurs du workflow. |
| Image absente | Recharger un fichier local dans chaque Load Image utilisé, y compris les références portant la mention `[output]`. |
| Index semble sans effet | Contrôler si le générateur reçoit `prompt_index`, `prompts` ou `group_prompt`. Index ne sélectionne le prompt qu'avec `prompt_index`. |
| Toute la gamme est enregistrée sous le nom d'un parfum | Remplacer la connexion `filename_index` par un préfixe de collection. |
| Il manque un produit | Vérifier `count`, `ignored`, les entrées IMAGE réellement branchées, l'ordre et le nombre de références. |
| Un type produit donne un résultat étrange | Utiliser son nom officiel ; contrôler si `produit_libre` l'a transformé en contenant générique. |
| L'image n'a pas le format annoncé | Régler les dimensions sur le générateur, pas seulement `ratio` sur Cosmétiques Luxe. |
| Le rendu ne se lance pas | Vérifier les nodes en bypass, le node d'enregistrement, les entrées requises, le modèle, l'accès API et les crédits affichés. |
| Une correction ne change rien | Examiner le prompt, la référence et le masque transmis. |
| Le flacon change entre deux vues | Utiliser l'image retenue comme référence de retouche et demander uniquement la modification nécessaire. |
| Double bouchon ou applicateur inventé | Décrire une seule pièce et une mécanique explicite, puis contrôler le résultat. |
| Les noms sont mal écrits | Corriger d'abord l'image ; recontrôler les inscriptions après composition et animation. |
| Il manque un champ ou une sortie du node | Dans une copie du workflow, ajouter une instance neuve du node installé, reporter ses réglages et reconnecter ses sorties avant de réexporter. |

## 12. Liste des produits disponibles

| Famille | Produits |
|---|---|
| Parfums et ambiance | Parfum ; Eau de toilette ; Parfum solide (compact) ; Bougie parfumée |
| Lèvres | Rouge à lèvres (bâton) ; Rouge liquide (doe-foot) ; Gloss (doe-foot) ; Baume à lèvres (stick) ; Crayon à lèvres |
| Yeux | Fard à paupières (palette) ; Eye-liner (feutre) ; Mascara ; Crayon yeux ; Sourcils (crayon/gel) |
| Teint | Highlighter (compact) ; Poudre (compact) ; Blush (compact) ; Fond de teint (pompe) ; Correcteur (anti-cernes) ; Bronzer (compact) ; Poudre libre (pot) |
| Soin | Sérum (compte-gouttes) ; Crème (pot) ; Huile (compte-gouttes) ; Brume / lotion (spray) ; Démaquillant (pompe) ; Masque (tube) |
| Ongles | Vernis à ongles |

## 13. Organiser les fichiers

Conservez séparément les images retenues, les essais, les références et les vidéos. Pour une image de collection, utilisez un préfixe de collection ; pour un produit, utilisez son nom ; pour une vidéo, ajoutez le geste ou le type de plan.

```text
NOCTURIA-Black-Swan-Ferme
NOCTURIA-Black-Swan-Ouvert
NOCTURIA-Collection-Six-Produits
NOCTURIA-Crimson-Veil-Application
NOCTURIA-Moonlight-Elixir-Scene
```

Le node prépare un préfixe ; c'est le node d'enregistrement qui écrit le fichier et gère sa destination. Les références et leur ordre doivent être conservés avec le workflow si vous voulez reprendre le projet.

## Crédit et licence

Créé par **Franck Dupas — Franck D Digital AI**. Le fichier [LICENSE](../LICENSE) contient les conditions MIT du paquet. Les modèles, services et extensions utilisés avec les workflows ont leurs propres conditions.

Retour à la [présentation et à l'installation rapide](../README.md).
