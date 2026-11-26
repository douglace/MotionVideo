# Spec motion design : « Pompéi : ce que la cendre a gardé »

La vidéo est refaite de zéro avec le skill [`LottieFiles/motion-design-skill`](https://github.com/LottieFiles/motion-design-skill). Seule la voix off d'origine est conservée, avec un timing mot à mot relevé dans les sous-titres d'origine puis recalé sur les respirations de la voix (`assets/timing.json`).

Nouveauté de cet épisode : la **structure narrative** du skill (`director/narrative-structure.md`) est appliquée explicitement, à deux échelles :
1. **toute la vidéo** suit un enchaînement de temps forts (section 2) ;
2. **chaque animation principale** suit les 4 actes : anticipation → action → réaction → résolution (section 3).

---

## 1. Les trois piliers (`core-philosophy.md`)

| Pilier | Réponse |
|---|---|
| Intention émotionnelle | Mystère (une découverte) → chaleur (la ville vivante) → urgence puis tristesse (l'éruption) → calme (les siècles qui passent) → curiosité (les fouilles) → émotion (les moulages) → réflexion (et nous ?) |
| Récit visuel | Un objet sert de fil rouge : **le pain**. Il est carbonisé au début, redevient doré quand on remonte à l'an 79, puis réapparaît parmi les objets du quotidien à la fin. |
| Exécution | Univers de la série (personnages articulés en aplats), avec des **coupes géologiques** pour rendre visible le temps qui passe. |

**Personnalité** : Premium (continuité de la série). Seul emprunt : le motif **Impact** pour l'éruption (`narrative-structure › Impact`).
**Identité de mouvement** : identique aux épisodes précédents (`M` : courbe (.4,0,.2,1), 350 / 500 / 800 ms, montée de 20 px, sorties à 70 %, 0 % de dépassement).

## 2. L'histoire entière : progression *Cycle* (`narrative-structure › Multi-Beat Narratives`)

Le skill propose trois progressions : *Build-Up*, *Cycle* et *Impact*. Ce texte est un **Cycle** : départ → sommet → retour → répétition.

| Phase du Cycle | Phrases | Contenu |
|---|---|---|
| **Départ** | 1-3 | Les fouilles aujourd'hui : on trouve du pain. |
| **Montée** | 4-7 | Retour en l'an 79 : la ville vivante. |
| **Sommet** | 8-12 | L'éruption (motif *Impact* à l'intérieur du Cycle). |
| **Retour** | 13-21 | Les siècles passent, puis les fouilles de 1748 et 1863 nous ramènent au point de départ. |
| **Répétition** | 22-23 | « Imagine notre propre ville… » : le cycle recommence avec nous. |

Pour rendre le cycle visible, la **même coupe de terrain** sert à l'enfouissement (scène I) et à la projection finale (scène N), et la **même composition** sert au pain du début et au pain des objets du quotidien.

Transitions entre temps forts (`Multi-Beat › Transitions`) :
- **séquentielles** (claires) dans les passages explicatifs ;
- **en chevauchement** (fluides) quand le temps continue : de la ville vivante à l'éruption ;
- **par le noir** pour les sauts dans le temps : an 79 ↔ 1748 ↔ 1863.

## 3. Chaque animation : les 4 actes

La fonction `beat(t, t0, d)` découpe une animation en 4 phases, avec les proportions du tableau *Scaling to Duration* :

| Durée | Anticipation | Action | Réaction | Résolution |
|---|---|---|---|---|
| 400-800 ms | 15-20 % | 30-40 % | 15-20 % | 20-25 % |
| ≥ 800 ms | 20 % | 30-35 % | 15-20 % | 25-30 % |

À la fin de chaque temps fort, **100 à 200 ms d'immobilité** (« breathing room ») avant le suivant. Une vérification automatique (`checkBreathing()`) liste les temps forts qui se chevauchent.

Motifs du skill utilisés (`narrative-structure › Common Patterns`) :

| Motif | Déroulé selon le skill | Utilisé pour |
|---|---|---|
| **Reveal** | tension (assombri, 95 %) → apparition (100 %) → l'entourage s'ajuste → posé | le pain dans la cendre, les rues et les fresques dégagées, le moulage |
| **Transformation** | déstabilisation (vibration) → métamorphose → un élément secondaire apparaît → le nouvel état respire | le pain carbonisé redevient doré (retour en 79), le plâtre qui remplit la cavité |
| **Departure** | rassemblement (98 %) → sortie → l'espace se referme → posé | les habitants qui fuient, la puissance de Rome qui s'efface |
| **Impact** | action soudaine → onde → stabilisation lente | l'éruption |
| **Cycle** (ambiance) | départ → sommet → retour → répétition | soleil et lune pendant les siècles qui passent |

## 4. Scène par scène

| # | Voix | Phase du Cycle | Motif | Héros (action) | Réaction | Résolution |
|---|---|---|---|---|---|---|
| A | « Des archéologues… du pain. » | Départ | Reveal | Le pinceau dégage le pain dans la cendre | Poussière, l'archéologue se penche | Le pain se pose, lueur dorée |
| B | « Pas une sculpture. Du vrai pain romain, carbonisé. » | Départ | Reveal / staging | Pain en gros plan, étiquettes | « Sculpture » est barré | Tenue sur « carbonisé » |
| C | « Retour en l'an 79. » | Montée | **Transformation** | Compteur d'années à rebours, le pain redevient doré | Le fond passe de la nuit au matin | Le pain chaud respire (vapeur) |
| D | « Au pied du Vésuve… ville commerçante. On y achète… » | Montée | Reveal (décor) | La rue s'assemble, le Vésuve encore vert | Le marchand tend un bol | Le client le prend, pause |
| E | « On écrit sur les murs, on travaille… » | Montée | 3 temps séquentiels | Graffiti « SALVE », boulanger, pièces de monnaie | Chaque temps a sa réaction | 150 ms entre chaque |
| F | « Puis le volcan entre en éruption. » | **Sommet** | **Impact** | Grondement (anticipation) → panache expo | Les gens lèvent la tête, le ciel s'assombrit | Le panache s'étale en parasol |
| G | « Des pierres, la cendre s'accumulent… » | Sommet | Accumulation | Lapilli, le niveau de cendre monte | Les toits disparaissent | Tenue |
| H | « Une partie fuit. D'autres restent… » | Sommet | **Departure** | Des habitants quittent l'écran (ease-in) | Ceux qui restent se blottissent | La rue se vide (l'espace se referme) |
| I | « La ville disparaît… Des siècles passent. » | Retour | Reveal inversé + **Cycle** | Les couches de terrain s'empilent (cascade) | L'herbe pousse en surface | Soleil et lune, compteur 79 → 1748 |
| J | « En 1748… murs peints. » | Retour | Reveal × 3 | Les ouvriers creusent, une rue, une boutique et une fresque apparaissent | Chaque découverte brille | Pause après « peints » |
| K | « Cavités étranges dans la cendre durcie. » | Retour | Reveal | Coupe : une cavité en forme de silhouette | Point d'interrogation | Tenue |
| L | « En 1863, Giuseppe Fiorelli… moulages. » | Retour | **Transformation** | Le plâtre remplit la cavité, puis la cendre est retirée | Statue barrée, « MOULAGE » validé | Le moulage respire, projecteur |
| M | « Bien plus que la puissance de Rome… objets du quotidien. » | Retour | **Departure** + Reveal | Rome (colonnes, aigle) s'efface, les objets montent | Le pain revient (fil rouge) | Tenue |
| N | « Imagine notre ville… Quel objet… ? » | **Répétition** | Reveal | Une ville moderne recouverte, coupe avec des objets modernes | Point d'interrogation | Appel à commenter qui respire (2,5 s) |

---

## 5. Contrôles prévus (`quality-checklist.md`)

Ce sont les mêmes que pour les épisodes 1 et 2 : règle du 1/3 (distance et nombre d'éléments), cascades < 500 ms (600 ms pour une cascade dramatique), aucun linéaire dans l'espace, sorties à 70 %, pas d'opacité seule, ambiance ≤ 20 %, plus la vérification des pauses entre temps forts. Les résultats sont dans la section 6, complétée après le rendu.

---

## 6. Audit : résultats

### Structure narrative (`narrative-structure.md`)
| Contrôle | Résultat |
|---|---|
| Pause entre temps forts ≥ 100 ms (`checkBreathing()`) | **0 chevauchement** sur 17 temps forts enregistrés |
| 4 actes par animation principale | `beat()` appliqué aux 17 temps forts (Reveal ×7, Transformation ×2, Departure ×2, Impact ×1, plus les 3 temps séquentiels de la scène E) |
| Progression d'ensemble | **Cycle** : départ (A-B) → montée (C-E) → sommet (F-H) → retour (I-M) → répétition (N) |
| Fil rouge | le pain : carbonisé (A-B) → doré (C) → objet du quotidien (M) |

### Corrections faites pendant la production
| Constat | Règle du skill | Correction |
|---|---|---|
| Le panache sortait du cadre par le haut (parallaxe verticale du Vésuve) | Staging : le héros doit rester lisible | Parallaxe horizontale seulement pour l'arrière-plan |
| Panache trop fin pour un temps fort | *Impact* : l'action doit être « soudaine » et lisible | Panache 2,2 fois plus large, parasol 1,3 fois plus large |
| Objets du quotidien apparus après la fin de la phrase | Chaque mouvement sert le récit au bon moment | Le temps fort est calé sur « les traces » au lieu de « objets » |
| Archéologues trop petits | Quality › éléments > 100 px pour le détail | Échelle 0,85 → 1,1 |

### Vérifications passées
Ce sont les mêmes que pour les épisodes précédents. Cascades : objets 5 × 80 = 400 ms, objets modernes 3 × 100 = 300 ms, réactions de la foule pendant l'éruption 4 × 60 = 180 ms. Règle du 1/3 : caméra de la scène E en 3 segments de 320 px, fugitifs sortant un groupe à la fois. Pas de linéaire dans l'espace : seuls l'écriture du graffiti, le cycle soleil/lune et les lapilli sont linéaires. Sorties à 70 % de l'entrée. Ambiance ≤ 20 %.
