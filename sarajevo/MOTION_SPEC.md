# Spec motion design : « Sarajevo, 1914 : comment un assassinat a déclenché la Première Guerre mondiale »

La vidéo est refaite de zéro avec le skill [`LottieFiles/motion-design-skill`](https://github.com/LottieFiles/motion-design-skill). Seules la voix off et sa musique d'origine sont conservées, avec un timing mot à mot relevé dans les sous-titres d'origine (`assets/timing.json`).
Les renvois `skill › fichier › section` pointent vers `skills/motion-design/…`.

Ordre de travail imposé par le skill (`decision-framework.md › Decision Quick-Path`) :
**objectif → personnalité → propriétés → timing → courbes d'accélération**, puis l'audit (`quality-checklist.md`) avant la livraison.

---

## 1. Les trois piliers (`director/core-philosophy.md`)

| Pilier | Réponse |
|---|---|
| **Intention émotionnelle** | Curiosité (comment est-ce possible ?), puis tension qui monte, puis **fatalité** (les dominos), puis gravité (le bilan), et enfin une réflexion qui reste en suspens. |
| **Récit visuel** | Progression *Build-Up* (`narrative-structure.md › Multi-Beat Narratives`) : calme → montée → sommet (les dominos et la guerre totale) → retombée (le bilan, la machine qui s'arrête). |
| **Exécution du mouvement** | Même univers graphique que « La trêve de Noël 1914 » (personnages articulés), complété par des infographies : carte en tuiles, chaînes d'alliances, dominos, compteur. |

## 2. Décisions globales

### Personnalité
- Le sujet (histoire, explication, gravité) et le tableau *Content Type* (« Editorial → Premium ») mènent à **Premium**, comme le premier épisode. La personnalité reste ainsi cohérente sur toute la série (troubleshooting › *Inconsistent Feel*).
- La règle *Mixing Archetypes* (90 % Premium) s'applique, avec un seul emprunt : le motif **Impact** pour les coups de feu, la chute des dominos et le tampon de l'ultimatum (`narrative-structure › Impact`).
- Le skill met **Playful** par défaut pour l'illustration. Je l'écarte : un ton léger trahirait l'émotion visée (le pilier 1 passe avant).

### Identité de mouvement (objet `M`, identique à l'épisode 1)
Courbe signature `(.4,0,.2,1)` · palette de durées 350 / 500 / 800 ms · entrée = montée de 20 px + fondu + échelle 98 → 100 % · sorties = 70 % de l'entrée · 0 % de dépassement · jamais d'écrasement ni d'étirement.

### Codes couleur (`emotion-mapping.md › Color Psychology`)
- **Rouge** = Triple Alliance, et le danger. Règle *Error* : le rouge apparaît, puis se calme ; il ne reste jamais saturé longtemps.
- **Bleu** = Triple Entente (le skill associe le bleu à la confiance ; ici, c'est un code d'identification des camps).
- **Or** = les mots-clés et l'emphase. **Sable** = pays neutres.
- Le passage de la crise locale à la guerre totale se fait **vers le rouge** (on ne commence pas par lui : règle « transition TO »).

### Couches
- **Primaire** : le personnage ou l'objet qui porte la phrase.
- **Secondaire** (30-50 %, décalée de +50 à 100 ms) : ombres, étiquettes, ondes, poussière.
- **Ambiante** (10-20 %) : poussière en suspension (au plus 15 particules), mèche qui grésille, engrenages, grain.

### Transitions entre scènes
- **Fondu de 500 ms + échelle 103 → 100 %** quand l'histoire continue.
- **Passage par le noir** quand le temps saute (retour au 28 juin, quatre ans plus tard).
- **Coupe** pour un choc (les coups de feu).

---

## 3. Scène par scène

| # | Voix (début) | Objectif · émotion | Direction | Héros (primaire) | Secondaire | Ambiante | Règles du skill |
|---|---|---|---|---|---|---|---|
| A | « Le 28 juin 1914, deux coups de feu… embrasent la planète » | Accroche · surprise | vers l'extérieur (rayonnement) | Voiture de l'archiduc → 2 éclairs → globe | Onde rouge sur le globe | Poussière | Coupe sèche · *Impact* (expo 150-300 ms) · le rouge se propage **vers** le monde entier |
| B | « Comment un seul assassinat… ? » | Curiosité | vers la droite = progression | Rangée de dominos, du minuscule à l'immense | Point d'interrogation | — | Échelle = importance (property-selection) · cascade de 80 ms × 6 = 480 ms (< 500) |
| C | « En réalité, l'Europe est déjà une poudrière. » | Menace | vers le bas (le baril se pose) | Baril « EUROPE » | Mèche qui s'allume | Étincelles (ambiance) | Entrée émergente 98 → 100 % · mèche qui grésille = ambiance continue |
| D | « Depuis 40 ans… colonies, mers, frontières » | Expliquer | vers la droite (frise) | Frise 1871 → 1914 | 3 icônes synchronisées sur les mots | — | Assembled entrance · chaque icône au mot près |
| E | « La France veut reprendre l'Alsace-Lorraine » | Relation | vers l'Est | Tuile Alsace-Lorraine (zébrée) | Flèche France → Alsace | Pulsation 2 s | Carte en tuiles = solution lisible sur un écran 9:16 |
| F | « L'Allemagne réclame un empire mondial » | Ambition | vers l'extérieur | L'Allemagne grandit (échelle) | Ancres et navires sur les océans | — | Échelle vers le haut = importance (property-selection) |
| G | « Dans les Balkans, les peuples… » | Pression | vers le haut | Foule de petits personnages, drapeaux levés | Tuile Serbie | Foule qui piétine | Cascade de 60 ms dans la foule (< 400 ms) |
| H | « …l'Europe se coupe en deux blocs armés » | Rupture | vers l'extérieur | La carte se sépare (contre-mouvement gauche ↔ droite) | Fissure | — | Contre-mouvement (choreography) · 1/3 d'écran respecté |
| I | « la Triple Alliance… face à la Triple Entente… » | Hiérarchie | du haut vers le bas | Cartes des pays (une par mot) | Liens de chaîne | — | Même origine pour toutes les cartes (montée de 20 px) · cascade calée sur la voix |
| J | « Le piège est simple… » | Mécanique · tension | chaîne → propagation | Un pays attaque → les liens se tendent → tous passent au rouge | Onde le long de la chaîne | — | Événement partagé : départ sous 50 ms, arrivées décalées (choreography › Shared Motion Events) |
| K | « Le 28 juin, à Sarajevo, Gavrilo Princip… » | Récit · tension → choc | horizontale (la voiture avance) | Princip sort de la foule → éclairs → l'archiduc s'effondre | Étiquettes d'identité | Foule, drapeaux qui flottent | Staging (projecteur) · anticipation (Princip avance d'un pas) · *Impact* |
| L | « Vienne accuse la Serbie… ultimatum » | Pression | Vienne → Belgrade | Télégramme en arc | Horloge 48 h, tampon | Aiguille | Arc (disney § 7) · anticipation du tampon |
| M | « Alors les dominos tombent en 5 semaines » + dates | **Fatalité** | vers la droite, en chaîne | 7 dominos, chacun tombe **sur son mot** | Calendrier, poussière à l'impact | — | Chute = accélération (ease-in, comme la gravité) · caméra en segments ≤ 1/3 d'écran · un domino actif à la fois |
| N | « Chaque camp jure… rentrer avant Noël » | Illusion · ironie | vers la droite (départ) | Soldats français et allemands qui partent, fleur au fusil | Wagon « À BERLIN » / « NACH PARIS » | Vapeur | Marche avec anticipation et mouvements décalés · clin d'œil à l'épisode « Noël » |
| O | « Mais la course aux armements… guerre totale » | Escalade | vers le haut puis vers l'extérieur | Barres d'armement, puis cercle « crise locale » qui envahit tout | Passage au rouge | — | Couleur **vers** le rouge · révélation spectaculaire |
| P | « Quatre ans plus tard, 18 millions… » | Gravité | vers le bas (effondrement) | Compteur, puis 4 couronnes qui se fissurent et tombent | Étiquettes des empires | — | Tristesse = lent (600-1200 ms) · cascade de 150 ms × 4 |
| Q | « En 1914, personne n'a voulu… la machine. » | Réflexion | vers le bas (ralentissement) | Engrenages géants qui ralentissent puis s'arrêtent | 2 lignes de texte | Grain | Ralentissement en sine · 800 ms et plus · calme final |

---

## 4. Audit avec `reference/quality-checklist.md`

Pour cet épisode, les règles du skill ont été intégrées **dès la conception** : identité `M`, fonctions `poseT` et `lean`, `camKF` avec arcs, ambiance plafonnée. L'audit n'a donc relevé qu'une violation, qui a été corrigée.

| Gravité | Constat | Règle | Correction |
|---|---|---|---|
| CRITIQUE | Entrée de la voiture : 410 px d'un seul segment (scènes A et K) | 1/3 d'écran (distance) | Premier segment ramené à 340 px, puis ralentissement en deuxième segment |

### Vérifications passées

| Vérification | Mesure |
|---|---|
| Cascades < 500 ms | dominos 7 × 60 = 420 ms · transfert des tuiles 10 × 50 = 450 ms · foule 7 × 60 = 420 ms · pays 5 × 60 = 240 ms · navires 4 × 100 = 300 ms · couronnes 4 × 150 = 600 ms (cascade « dramatique » : ≤ 600 ms) |
| 1/3 d'écran (distance) | dominos : 280 px par segment · soldats : 170 px · tuiles : déplacement en arc (arc adjustments) |
| 1/3 des éléments | un domino actif à la fois · la foule réagit comme un seul événement partagé |
| Aucun linéaire dans l'espace | linéaire seulement pour les roues, l'aiguille de l'horloge, les éclairs (opacité) et la machine à écrire |
| Sortie = 70 % de l'entrée | sous-titres 350 / 250 ms · modules 500 / 350 ms |
| Pas d'opacité seule | chaque entrée combine montée de 20 px, fondu et échelle 98 → 100 % |
| Ambiance ≤ 20 % | 12 particules de poussière, grain à 6 %, vapeur, mèche |
| Rouge : apparaît puis se calme | ultimatum et tampon à −15 %, cadres « en guerre » à −40 % |
| Mouvement réduit | `index.html?reduced` : caméra fixe |

## 5. Modes de rendu
```bash
node render.mjs           # build/sarajevo.mp4
node render.mjs --annot   # build/sarajevo-annote.mp4 : règles du skill affichées à l'écran
```
