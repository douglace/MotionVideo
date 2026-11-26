# Spec motion design : « Mansa Moussa : l'or qui a fait chuter l'or »

La vidéo est refaite de zéro avec le skill [`LottieFiles/motion-design-skill`](https://github.com/LottieFiles/motion-design-skill). Seule la voix off d'origine est conservée, avec un timing relevé dans les sous-titres d'origine puis recalé sur les respirations de la voix (`assets/timing.json`).
Ordre de travail : piliers → narration (`narrative-structure.md`) → personnalité → scène par scène → audit.

---

## 1. Les trois piliers (`core-philosophy.md`)

| Pilier | Réponse |
|---|---|
| Intention émotionnelle | Émerveillement (un roi et son or) → curiosité (comment l'or peut-il perdre sa valeur ?) → grandeur (la caravane, Le Caire) → surprise (le cours s'effondre) → réflexion (le savoir, l'héritage, la question). |
| Récit visuel | L'**or** est le fil rouge : pépites dans le désert, courbe de prix, cadeaux, prix qui s'effondre, puis l'or qui **se transforme en manuscrits** à Tombouctou. Cette transformation prépare la question finale : « la richesse… ou ce qu'il en fait ? ». |
| Exécution | Univers de la série (personnages articulés en aplats), avec des infographies : carte de l'Afrique et itinéraire, courbe du cours de l'or, compteur. |

**Personnalité** : Premium, comme le reste de la série. Emprunts autorisés par la règle *Mixing Archetypes* :
- **Impact** pour l'effondrement du prix ;
- **Celebration** retenue (0 % de dépassement) pour la distribution de cadeaux au Caire.

**Identité de mouvement** : `M` (courbe (.4,0,.2,1), 350 / 500 / 800 ms, montée de 20 px, sorties à 70 %).

## 2. L'histoire entière : progression *Build-Up* (`narrative-structure › Multi-Beat Narratives`)

« calme → montée → sommet → retombée », précédé d'une **accroche en flash-forward**.

| Phase | Phrases | Contenu |
|---|---|---|
| **Accroche (flash-forward)** | 0-1 | Un roi, de l'or, une courbe qui **chute**. On montre le sommet en avance, sans l'expliquer. |
| **Calme** | 2-5 | 1324, l'empire du Mali, les échanges commerciaux, l'or comme source de puissance. |
| **Montée** | 6-8 | La caravane traverse le Sahara, l'arrivée au Caire, le sultan, les cadeaux. |
| **Sommet** | 9-13 | La même courbe que dans l'accroche, cette fois **expliquée** (motif *Impact*), le témoignage d'Al-Omari, la fortune impossible à calculer. |
| **Retombée** | 14-17 | La Mecque, Tombouctou (l'or devient savoir), l'Atlas catalan, puis la question. |

Le flash-forward ne figure pas dans le skill : c'est un procédé de narration classique. Je l'ai relié au skill en réutilisant **exactement la même courbe** dans l'accroche et au sommet. Le spectateur reconnaît le motif : c'est la règle *Consistent : same interaction = same motion*.

Transitions entre temps forts (`Multi-Beat › Transitions`) :
- **chevauchées** pendant le voyage (Sahara → Le Caire) ;
- **séquentielles** dans les passages explicatifs (carte, courbe) ;
- **par le noir** pour les sauts dans le temps (1324, 1375).

## 3. Chaque animation : 4 actes et motifs du skill

`beat()` découpe chaque animation en anticipation → action → réaction → résolution, avec les proportions du tableau *Scaling to Duration*. `checkBreathing()` vérifie qu'aucun temps fort ne commence moins de 100 ms après la fin du précédent.

| Motif (`Common Patterns`) | Utilisé pour |
|---|---|
| **Reveal** | le roi, Le Caire, le sultan, l'Atlas catalan |
| **Departure** | la caravane qui quitte le Mali |
| **Celebration** (retenue) | les cadeaux au Caire : compression → éclatement de pièces → stabilisation (0 % de dépassement) |
| **Impact** | l'effondrement du prix de l'or |
| **Transformation** | l'or qui devient manuscrits à Tombouctou |

## 4. Scène par scène

| # | Voix | Phase | Motif | Héros (action) | Réaction | Résolution |
|---|---|---|---|---|---|---|
| A | « Un roi traverse le désert avec une fortune en or. » | Accroche | Reveal | La caravane sur une crête de dune | Reflets d'or | Tenue |
| B | « …le prix du métal précieux va même chuter. » | Accroche | Impact (aperçu) | La courbe chute | Pièce qui pâlit | Point d'interrogation |
| C | « Nous sommes en 1324. » | Calme | Reveal | Année | Filet doré | Pause |
| D | « Mansa Moussa… part en pèlerinage vers La Mecque. » | Calme | Reveal | Le roi (projecteur), puis l'itinéraire tracé sur la carte | Étiquettes | Point « La Mecque » |
| E | « Son royaume est au cœur des échanges… » | Calme | Séquentiel | Routes transsahariennes, or ↔ sel | Flèches | Tenue |
| F | « L'or contribue à sa puissance. » | Calme | Reveal | Piles de pièces (cascade) | Couronne | Tenue |
| G | « Avec sa caravane… Le Caire, capitale du sultanat mamelouk. » | Montée | Departure → Reveal | Chameaux qui marchent, puis la silhouette du Caire | Poussière | Le Caire se pose |
| H | « Là, il est reçu par le sultan d'Égypte. » | Montée | Reveal | Le sultan et Moussa face à face, salut | Les cours se rapprochent | Pause |
| I | « Moussa distribue des cadeaux… » | Montée | **Celebration** | Éclatement de pièces | Les marchands réagissent | Les pièces se posent |
| J | « Mais cette abondance… perd de sa valeur. » | **Sommet** | **Impact** | La courbe s'effondre (la même que dans B) | La pièce rétrécit et pâlit | Stabilisation lente |
| K | « Des années plus tard… Al-Omari… » | Sommet | Reveal | Le chroniqueur écrit | La courbe reste basse | Les témoins apparaissent |
| L | « Impossible de calculer exactement sa fortune… » | Sommet | Transformation (impossible) | Compteur de chiffres qui ne se stabilise pas | Point d'interrogation | Tenue |
| M | « Le pèlerinage continue jusqu'à La Mecque. » | Retombée | Itinéraire | Le tracé atteint La Mecque | Onde au point d'arrivée | Pause |
| N | « Puis Moussa rentre… Tombouctou… centre du savoir. » | Retombée | **Transformation** | Les pièces deviennent des manuscrits | La mosquée, les savants | Les livres respirent |
| O | « En 1375, l'Atlas catalan… » | Retombée | Reveal | Le roi sur un parchemin, tenant de l'or | Filet de carte | Tenue |
| P | « Alors, qu'est-ce qui marque… ce qu'il en fait ? » | Question | même origine | A : la richesse (or) / B : ce qu'il en fait (savoir) | Le cadre de l'option lue s'éclaire | Appel à commenter qui respire |

---

## 5. Audit : résultats

### Structure narrative
| Contrôle | Résultat |
|---|---|
| Pause entre temps forts ≥ 100 ms (`checkBreathing()`) | **0 chevauchement** sur 14 temps forts enregistrés |
| 4 actes par animation principale | `beat()` appliqué à tous les temps forts. Motifs : Reveal ×7, Departure, Celebration, Impact ×2 (aperçu + sommet), Transformation |
| Progression d'ensemble | **Build-Up** avec accroche en flash-forward : la courbe de B est rejouée à l'identique en J |
| Fil rouge | l'or : reflets dans le désert → courbe → piles de pièces → cadeaux → effondrement → **manuscrits** → la question A/B |

### Corrections faites pendant la production
| Constat | Règle du skill | Correction |
|---|---|---|
| Bande noire pendant le travelling de la caravane (décor en coordonnées du monde) | Qualité visuelle | Décor dessiné en coordonnées écran avec parallaxe, caravane dans le monde |
| Travelling de 720 px | 1/3 d'écran (distance) | 2 segments de 320 px |
| Fond de carte incomplet (bandes noires en haut et en bas) | Cohérence | Fond de carte en plein écran |

### Vérifications passées
- **Cascades** : piles de pièces 5 × 80 = 400 ms, témoins 4 × 80 = 320 ms.
- **Celebration** retenue : 0 % de dépassement, compression de 80 ms.
- **Pas de linéaire dans l'espace** : linéaire seulement pour le tracé d'écriture et le défilement du compteur.
- **Sorties** à 70 % de l'entrée, **ambiance** ≤ 20 % (12 particules de poussière, grain à 6 %).
