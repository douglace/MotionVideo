# Spec motion design : « 9 novembre 1989 : le papier qui a ouvert le Mur »

La vidéo est refaite de zéro avec le skill [`LottieFiles/motion-design-skill`](https://github.com/LottieFiles/motion-design-skill). Seule la voix off d'origine est conservée, avec un timing relevé dans les sous-titres d'origine puis recalé sur les respirations de la voix (`assets/timing.json`).
Ordre de travail : piliers → narration (`narrative-structure.md`) → personnalité → scène par scène → audit.

---

## 1. Les trois piliers (`core-philosophy.md`)

| Pilier | Réponse |
|---|---|
| Intention émotionnelle | Mystère (« ce papier ») → poids du passé (28 ans de mur) → tension qui monte (manifestations, conférence) → **surprise** (« immédiatement ») → attente nerveuse (la foule grossit) → **libération et joie** (la barrière se lève, on s'embrasse) → réflexion (qui a fait tomber le mur ?). |
| Récit visuel | **Deux fils rouges** qui se rejoignent dans la dernière phrase : **le papier** (la décision d'en haut, petit, qui flotte) et **la foule** (la mobilisation d'en bas, qui grossit de scène en scène). La question finale reprend les deux : A = les dirigeants (le papier), B = les citoyens (la foule). |
| Exécution | Univers de la série (personnages articulés en aplats), avec horloges (18 h 50 → 23 h 30), plan de Berlin et carte de l'Allemagne. |

**Personnalité** : Premium, comme le reste de la série. Emprunts permis par la règle *Mixing Archetypes* :
- **Impact** pour « immédiatement, sans délai » ;
- **Celebration** retenue (0 % de dépassement) pour l'ouverture de la barrière et les retrouvailles.

**Identité de mouvement** : `M` (courbe (.4,0,.2,1), 350 / 500 / 800 ms, montée de 20 px, sorties à 70 %).
**Couleurs** : le gris béton du Mur et le vert-gris des gardes, contre l'**or des lumières** du passage. Le passage à l'or se fait « vers » la libération, selon la règle *transition TO* : il n'est pas là au départ.

## 2. L'histoire entière : *Build-Up* de tension, puis *Celebration* (`narrative-structure › Multi-Beat Narratives`)

| Phase | Phrases | Contenu |
|---|---|---|
| **Accroche** | 0 | Un papier tombe, une ligne de frontière apparaît : la question est posée. |
| **Calme (contexte)** | 1-2 | Berlin, 9 novembre 1989. Le Mur sépare la ville depuis 28 ans. |
| **Montée** | 3-8 | Le régime vacille, les manifestations, les départs, les nouvelles règles, la conférence de 18 h 50, la question du journaliste. |
| **Pic 1 (Impact)** | 9 | « Immédiatement, sans délai » : la phrase qui déclenche tout. |
| **Montée 2** | 10-14 | La télévision, la foule qui se rend aux points de passage, les gardes sans ordres, l'**attente**. Le ralentissement fait monter la tension. |
| **Pic 2 (Celebration)** | 15-17 | 23 h 30 : la barrière se lève, on traverse, on s'embrasse, les autres points de passage suivent. |
| **Retombée** | 18-20 | Le Mur reste debout mais n'enferme plus, la réunification, la morale. |
| **Question** | 21 | Les dirigeants ou les citoyens ? |

Les deux pics suivent la règle de rythme du skill : un **sommet bref et sec** (Impact, ~0,3 s), puis une **longue montée** jusqu'à un **sommet large et chaleureux** (Celebration).

## 3. Chaque animation : 4 actes et motifs

`beat()` découpe chaque animation (anticipation → action → réaction → résolution, avec les proportions de *Scaling to Duration*). `checkBreathing()` vérifie qu'aucun temps fort ne démarre moins de 100 ms après le précédent.

| Motif | Utilisé pour |
|---|---|
| **Reveal** | le papier, le Mur, Schabowski, le téléviseur, la carte de la réunification |
| **Transformation** | le régime qui **vacille** (déstabilisation), le Mur qui cesse d'enfermer (une porte s'ouvre dans le béton) |
| **Departure** | ceux qui quittent le pays, la famille qui quitte le salon pour aller aux points de passage |
| **Impact** | « immédiatement, sans délai » |
| **Celebration** | la barrière qui se lève (compression → éclatement de lumière → stabilisation) |

## 4. Scène par scène

| # | Voix | Phase | Motif | Héros (action) | Réaction | Résolution |
|---|---|---|---|---|---|---|
| A | « Ce papier va bouleverser une frontière. » | Accroche | Reveal | Le papier tombe en arc et se pose | Une ligne de frontière se trace | Tenue |
| B | « Berlin, 9 novembre 1989. » | Calme | Reveal | Silhouette de Berlin (tour de télévision, porte de Brandebourg) | Date | Pause |
| C | « Depuis 28 ans, un mur sépare la ville. » | Calme | Reveal | Le Mur se trace du haut vers le bas | OUEST / EST, compteur 1961 → 1989 | Tenue |
| D | « Le régime vacille… manifestent… quittent le pays. » | Montée | Transformation + Departure | Emblème qui vacille, foule avec banderoles, des silhouettes qui partent avec leurs valises | Les banderoles se lèvent | Une seule action à la fois |
| E | « Le pouvoir prépare de nouvelles règles… le lendemain. » | Montée | Reveal | Le document s'écrit | Calendrier : 10 novembre | Tenue |
| F | « À 18 h 50… un journaliste lui demande… » | Montée | Anticipation | Schabowski lit, le journaliste lève la main | Horloge 18 h 50, micros | « Ab wann? » |
| G | « Sa réponse… immédiatement, sans délai. » | **Pic 1** | **Impact** | « SOFORT » → « IMMÉDIATEMENT » | Onde, flash du papier | Stabilisation lente |
| H | « Les médias… comprennent… se rendent aux points de passage. » | Montée 2 | Reveal + Departure | Le téléviseur s'allume, la famille se lève puis sort | Les visages s'éclairent | La pièce se vide |
| I | « Pourtant… les gardes… L'attente… la foule grossit. » | Montée 2 | Accumulation | La foule grossit (cascade de 80 ms par vague) | Les gardes immobiles, l'horloge avance | Tension (battement de cœur) |
| J | « À Bornholmer Strasse… finalement ouvert. » | **Pic 2** | **Celebration** | La barrière se lève, la lumière dorée envahit l'image | La foule avance | Lumière stable |
| K | « Les habitants traversent… D'autres points de passage suivent. » | Pic 2 | Celebration + cascade | Deux personnes s'embrassent, puis un plan de Berlin où les points de passage s'allument | Points dorés | Tenue |
| L | « Le Mur n'est pas démoli… cesse d'enfermer. » | Retombée | **Transformation** | Une porte s'ouvre dans le Mur, des gens assis dessus | La lumière passe | Respiration |
| M | « Onze mois plus tard, l'Allemagne est réunifiée. » | Retombée | Reveal | RFA et RDA se rejoignent (contre-mouvement) | 3 octobre 1990 | Tenue |
| N | « La conférence a précipité… des mois de mobilisation… » | Retombée | Les deux fils rouges | Le papier (petit) et la foule (grandissante) | Une balance penche | Tenue |
| O | « À ton avis, qui a fait tomber le mur ? » | Question | même origine | A : les dirigeants (papier, micro) / B : les citoyens (foule) | Le cadre de l'option lue s'éclaire | Appel à commenter qui respire |

---

## 5. Audit : résultats

### Structure narrative
| Contrôle | Résultat |
|---|---|
| Pause entre temps forts ≥ 100 ms (`checkBreathing()`) | **0 chevauchement** sur 18 temps forts enregistrés |
| 4 actes par animation principale | `beat()` appliqué partout. Motifs : Reveal ×6, Transformation ×2, Departure ×2, Impact, Celebration |
| Progression | Build-Up en deux pics : **Impact** bref (« immédiatement »), puis **Celebration** large (la barrière se lève) |
| Fils rouges | le papier (A → G → N → O-A) et la foule (D → H → I → J → N → O-B) |

### Corrections faites pendant la production
| Constat | Règle du skill | Correction |
|---|---|---|
| La barrière s'abaissait vers le sol au lieu de se lever | Le mouvement doit porter le sens (direction vers le haut = libération, `decision-framework › Motion Direction`) | Sens de rotation inversé |
| Mots ambigus dans le texte (« citoyens », « d'autres » apparaissent deux fois) | Synchronisation au bon temps fort | Calage sur la bonne occurrence de chaque mot |

### Vérifications passées
- **Cascades** : foule 7 × 60 = 420 ms, vagues d'attente 5 × 80 = 400 ms, foule sur la balance 8 × 60 = 480 ms, points de passage 4 × 100 = 400 ms.
- **Celebration** retenue : 0 % de dépassement.
- **Pas de linéaire dans l'espace** : linéaire seulement pour les aiguilles d'horloge.
- **Couleur vers l'or** à l'ouverture, **rouge** qui apparaît puis disparaît.
- **Mouvement réduit** (`?reduced`) : sans battement de cœur ni secousse.
