# Spec motion design — « La trêve de Noël 1914 »

Ce document montre comment le skill [`LottieFiles/motion-design-skill`](https://github.com/LottieFiles/motion-design-skill) a été appliqué à cette vidéo, étape par étape.
Les renvois `skill › fichier › section` pointent vers `skills/motion-design/…` du dépôt du skill.

---

## 1. Avant tout : les trois piliers (`director/core-philosophy.md`)

| Pilier | Question du skill | Réponse pour cette vidéo |
|---|---|---|
| **Intention émotionnelle** | Que doit *ressentir* le spectateur ? | Gravité, tension, puis une chaleur fragile (Noël), et pour finir une question qui reste ouverte. |
| **Récit visuel** | Quelle est la micro-histoire ? | Ennemis → lumière → rencontre → retour à la guerre → question. Chaque phrase de la voix devient une scène en mise en place → action → résolution. |
| **Exécution du mouvement** | Comment le rendre crédible ? | Personnages articulés, marche avec rebond, anticipation, mouvements décalés entre parties du corps, ombres, parallaxe. |

## 2. Décisions globales

### Personnalité (`director/motion-personality.md` et `director/context-adaptation.md`)
- Les mots-clés du sujet (historique, grave, éditorial) et le tableau *Content Type Adaptation* (« Editorial → Premium ») mènent à **Premium**.
- Le skill met **Playful** par défaut pour l'illustration. Je ne l'ai pas retenu : des rebonds sur un sujet de guerre trahiraient l'émotion visée. Le pilier 1 passe avant le choix par défaut.
- Règle *Mixing Archetypes* : Premium pour 90 % de la vidéo, avec un seul emprunt assumé. Le **tampon « CONDAMNÉE »** utilise le motif *Impact* (expo rapide), comme le permet `narrative-structure.md › Impact`.

### Identité de mouvement (*Brand Motion Identity*), codée dans l'objet `M`

| Constante | Valeur | Source dans le skill |
|---|---|---|
| Courbe signature (80 % des animations) | `cubic-bezier(.4,0,.2,1)` → `E.premium` | motion-personality › Signature Easing |
| Palette de durées | rapide 350 ms · standard 500 ms · lente 800 ms | motion-personality › Duration Palette (Premium) |
| Style d'entrée | montée de 20 px + fondu + échelle 98 → 100 % | entrance-exit › Premium offset 15-25 px |
| Courbe d'entrée | `(.05,.7,.1,1)` (décélération) | timing-easing › MD3 Emphasized |
| Courbe de sortie | `(.3,0,1,1)` (accélération), durée = 70 % de l'entrée | timing-easing › Enter vs Exit (65-75 %) |
| Dépassement | 0 % | Overshoot Budget › Premium |
| Écrasement / étirement | jamais | disney-principles § 1 (« Skip for premium ») |

### Trois couches de mouvement sur toute la vidéo (`core-philosophy › Three Motion Layers`)
- **Primaire (100 %)** : les personnages, ou l'objet principal de la scène (lettre, carte, ordre).
- **Secondaire (30-50 %, décalée de 50 à 100 ms)** : ombres au sol, lueurs, onde de la poignée de main, onde d'encre du tampon, étiquettes.
- **Ambiante (10-20 %)** : 20 flocons, 12 étoiles qui scintillent, flammes des bougies, respiration des personnages (cycle de 3,5 s), grain.

### Transitions entre scènes (même interaction = même mouvement)
- **Fondu de 500 ms + échelle 103 → 100 %** quand le temps continue (entrance-exit › Premium « slow fade + scale »).
- **Passage par le noir** quand le temps saute ou que l'humeur bascule (1914, l'enterrement, le retournement).
- **Coupe** quand on veut un choc (la reprise des combats).

---

## 3. Le personnage : un rig 2D construit avec les principes Disney (`director/disney-principles.md`)

| Principe | Mise en œuvre dans `soldier()` |
|---|---|
| § 2 Anticipation | `lean()` : petit recul de 6 % pendant 150 ms avant de marcher. Avant de sortir de la tranchée, le soldat s'accroupit de 12 px pendant 180 ms. Il lève légèrement le fusil avant de le baisser. |
| § 5 Mouvements décalés (follow-through) | `poseT()` : le bras arrière suit le bras avant avec **100 ms** de retard. Le pan de capote, le fusil porté dans le dos et la tête sont déphasés par rapport aux jambes. |
| § 6 Accélération et ralentissement | Aucun déplacement dans l'espace n'est linéaire : marche en `sine`, caméra en `premium`. |
| § 7 Arcs | La caméra ajoute 15 px perpendiculaires au milieu de chaque mouvement (`camKF`). La boîte de ration et les cigarettes suivent un arc. |
| § 8 Action secondaire | Ombre, rebond de la marche, lueur de la poignée de main. |
| § 11 Dessin solide | Ombre portée cohérente : quand le corps se soulève, l'ombre **s'étale et pâlit** (choreography › Counter-Motion « Lifts »). |
| § 3 Mise en scène (staging) | Un **projecteur** assombrit tout sauf le personnage principal du moment (scènes E, F, H). |

---

## 4. Scène par scène (cadre de décision `director/decision-framework.md`)

Pour chaque scène : objectif → émotion → direction du mouvement → propriétés animées → durées et courbes → personnage principal (héros) / couche secondaire / couche ambiante.

| # | Voix | Objectif · émotion | Direction | Héros (primaire) | Secondaire | Ambiante | Règles clés |
|---|---|---|---|---|---|---|---|
| A | « Ils devaient se tirer dessus… À Noël, ils se sont serré la main. » | Expliquer une relation · tension → tendresse | vers le centre = convergence | Les deux soldats : en joue → fusils baissés → marche → poignée de main | Ligne de mire rouge (tracé en 600 ms), étoile, onde dorée | Neige qui commence sur « Noël » | Anticipation (fusil levé, recul) · mouvement décalé du bras · rouge qui apparaît puis disparaît |
| B | « Décembre 1914… face à face dans les tranchées. » | Révéler · gravité | vers le bas = ancrage | Titre 1914, puis la caméra descend | Étiquettes des deux camps (500 ms), flèches face à face | Étoiles et lune en parallaxe 0,2x | 1/3 d'écran : la descente est coupée en 2 segments · révélation spectaculaire 600-1200 ms |
| C | « La nuit de Noël, des lumières… » | Attirer l'attention · émerveillement calme | vers l'avant (la caméra avance vers les Allemands) | 5 lumières en cascade | Les Britanniques tournent la tête | Flammes qui vacillent | Cascade de **90 ms × 5 = 360 ms** (< 400 ms, standard) |
| D | « Des chants traversent les lignes. » | Guider le regard · chaleur | vers la gauche = traversée | 2 phrases de 4 notes (cascade de 100 ms) | Chanteurs qui se balancent, Britanniques qui penchent la tête | Bouches qui chantent | 1/3 d'écran : panoramique en **5 segments** avec changements de zoom et arcs |
| E | « Puis des hommes sortent, sans savoir si l'autre camp va tirer. » | Tension · urgence retenue | vers le haut (sortir de la tranchée) | 1er temps : l'Allemand ; 2e temps : le Britannique qui vise | Mains levées, fusil qui se baisse sur « tirer » | **Battement de cœur** dans le vignettage | Mise en scène : le projecteur passe de l'un à l'autre (500 ms) · accroupi avant de grimper |
| F | « Dans certains secteurs, ils se rencontrent… » | Convergence · chaleur | vers le centre | Le premier duo marche, puis se serre la main | Lueur au moment de la poignée de main | Neige | **Règle du 1/3 des éléments** : le second duo ne part qu'au moment où le premier s'arrête |
| G | « Ils échangent nourriture et tabac. » | Expliquer · tendresse | arcs croisés | La boîte de ration, puis les cigarettes (700 ms chacune) | Étiquettes | Lueurs floues en arrière-plan | Arcs (disney § 7) · les mains entrent sur moins d'un tiers d'écran |
| H | « …enterrer leurs morts. » | Tristesse | vers le bas | Les croix sortent de terre (cascade de 200 ms) | Têtes qui s'inclinent | Neige ralentie à 45 % | Tristesse = lent (emotion-mapping : 600-1200 ms) · désaturation · projecteur sur les croix |
| I | « Ce n'est pas une légende… » | Preuve · confiance | vers le haut | La lettre sort de l'enveloppe, puis la photo tombe | Écriture qui se trace, photo qui se développe | Lignes du fond | Sceau « Témoignages » : apparition expo, 0 % de dépassement |
| J | « Mais attention… trêves locales… Ailleurs, on continue à combattre. » | Expliquer · nuance | le front se trace du nord au sud | Tracé du front (800 ms et plus) | Points des trêves (cascade de 120 ms, ≥ 36 px), étiquettes | Ondes autour des points | Explosions en **3 vagues de 5 (cascade de 80 ms)** au lieu de 22 explosions aléatoires · éléments animés > 40 px |
| L | « Et le retournement est là… armées toujours ennemies. » | Bascule · regret | vers l'extérieur = séparation | Mains qui se lâchent, demi-tour (300 ms), retour vers les tranchées | Ligne rouge « ENNEMIS » | Le ciel se refroidit | 1/3 d'écran : retour en 2 segments, avec une **pause regard en arrière** · le rouge apparaît puis s'apaise à 60 % |
| M | « Les combats reprennent… » | Urgence | horizontal | Tirs alternés d'un camp à l'autre | Calendrier qui défile | Fusées éclairantes (une à la fois) | Au plus 1 explosion à l'écran à la fois · coupe sèche (choc voulu) |
| N | « Les commandements condamnent la fraternisation. » | Autorité · choc | vers le bas (le tampon s'abat) | Ordre tapé à la machine, puis le tampon | Onde d'encre +60 ms, secousse du papier | — | Motif *Impact* : anticipation (le tampon se lève, 200 ms) → frappe expo en 180 ms → le rouge se pose |
| O | « Une poignée de main n'a pas suffi à arrêter la guerre. » | Tristesse | vers l'extérieur | Les mains se lâchent lentement (1,1 s) | Fissure rouge | Lueurs d'explosions lointaines | Tristesse = lent · fissure tracée en expo (surprise) |
| P | « Alors, cette trêve… ? » | Inviter à répondre · curiosité | vers le haut (même origine pour tout) | Option A, puis option B (montée de 20 px) | Le cadre de l'option lue s'éclaire | Bouton d'appel qui respire (2,5 s, ±3 %) | Même point de départ spatial pour tous les éléments (choreography › Spatial Origin Consistency) |

---

## 5. Audit avec `reference/quality-checklist.md` : avant → après

L'audit a été mené sur la première version animée (v1), avec les niveaux de gravité du skill.

| Gravité | Problème trouvé dans la v1 | Règle du skill | Correction |
|---|---|---|---|
| CRITIQUE | Descente de caméra de 700 px d'un seul tenant (scène B) et panoramique de 1 690 px (scène D) | 1/3 d'écran (distance) | Mouvements découpés en segments, avec arcs et changements de vitesse ou de zoom |
| CRITIQUE | Retour vers les tranchées de plus de 400 px d'un seul tenant (scène L) | 1/3 d'écran (distance) | 2 segments séparés par une pause regard en arrière |
| CRITIQUE | 9 notes avec 220 ms d'écart = 1,76 s ; 22 explosions aléatoires | Cascade totale < 500 ms | 2 phrases de 4 notes (300 ms) ; 3 vagues de 5 explosions (320 ms) |
| CRITIQUE | 4 soldats qui marchent en même temps (scène F) | 1/3 d'écran (éléments) | Un seul duo actif à la fois |
| ÉLEVÉE | Aucun décalage entre parties du corps | « No follow-through » | `poseT()` (bras +100 ms), capote, fusil et tête déphasés |
| ÉLEVÉE | Sous-titres : entrée 280 ms, sortie 120 ms (43 %) ; titre et calendrier à 50-60 % | Sortie = 65-75 % de l'entrée | Entrée 350 ms et sortie 250 ms (71 %) ; titre et calendrier entrée 500 ms, sortie 350 ms |
| ÉLEVÉE | Options A/B entrant par la gauche et par la droite | Origine spatiale cohérente | Les deux options montent depuis le bas (20 px) |
| ÉLEVÉE | Entrées décalées de 24 à 90 px selon les éléments | Premium : décalage de 15-25 px | Décalage unique `M.rise = 20` |
| ÉLEVÉE | Mot actif agrandi de 6 % | Premium : 98 → 100 %, 0 % d'exagération | Emphase ramenée à 3 % |
| MOYENNE | 150 flocons de 2 à 10 px, à 40-150 px/s | Ambiance neige : 10-20 éléments, 20-60 px/s | 20 flocons de 3 à 8 px, à 20-60 px/s, opacité 30-70 % |
| MOYENNE | 170 étoiles qui scintillent toutes | Scintillements : 8-15 éléments | Étoiles fixes, 12 seulement scintillent |
| MOYENNE | Pas d'anticipation avant la marche ni avant la sortie de tranchée | « No anticipation phase » | `lean()`, accroupi avant de grimper, le tampon se lève avant de frapper |
| MOYENNE | Pas d'ombres, rien en contre-mouvement | « Missing counter-motion » | Ombres qui s'étalent quand le corps se soulève ; ciel en parallaxe 0,2x, collines 0,5x |
| MOYENNE | Trajets de caméra en ligne droite | « Could use better arcs » | Arc de 15 px au milieu de chaque segment |
| MOYENNE | Plusieurs personnages se disputent l'attention | Staging : un héros par temps fort | Projecteur qui assombrit le reste d'environ 45 % |
| MOYENNE | Points de trêve de 24 px | Éléments animés > 40 px | 36 px, plus une onde de 100 px |
| MOYENNE | Le CTA pulse à 1,25 s et ±2,5 % | Attention du CTA : 2500 ms, 0,97-1,03 | Cycle de 2,5 s, ±3 % |
| MOYENNE | Le demi-tour est linéaire | Pas de linéaire hors rotation ou progression | `E.premium`, 300 ms |
| ACCESSIBILITÉ | Aucune alternative en mouvement réduit | prefers-reduced-motion | `index.html?reduced` : caméra fixe, pas de secousse ni de battement |

### Écarts assumés (et pourquoi)
- **Notes de musique et explosions** : ce sont des particules (*Straight Ahead*, disney § 4). Leur trajet dépasse le tiers d'écran, mais il suit un arc sinusoïdal, ce que la règle du 1/3 accepte (« arc adjustments »).
- **Transitions de scène en fondu** : un changement de plan n'est pas un changement d'état d'interface. Le fondu est donc combiné à une échelle 103 → 100 %, et pas seulement à l'opacité.
- **Alerte vidéo de plus de 5 s sans pause** : ne s'applique pas à une vidéo linéaire, c'est le lecteur qui gère la pause.

---

## 6. Vérification finale (`decision-framework › Evaluation Before Delivery`)

| Vérification | Résultat |
|---|---|
| Fonction claire ? | Chaque mouvement illustre un mot de la voix (minutage au mot près, `wt()`). |
| Personnalité cohérente ? | Premium partout, sauf l'emprunt *Impact* volontaire du tampon. |
| Supportable au 100e visionnage ? | Ambiance à 10-20 %, pas de clignotement agressif, rouge qui s'apaise. |
| Respecte l'attention ? | Un héros par temps fort, projecteur, au plus 1/3 des éléments actifs. |
| Hiérarchie ? | Primaire 100 %, secondaire 30-50 % décalée de 50 à 100 ms, ambiance 10-20 %. |
| Trois couches ? | Oui, dans chaque scène (voir le tableau de la section 4). |
| Durées adaptées ? | Palette 350/500/800 ms, plus durées longues pour la tristesse (600-1200 ms). |
