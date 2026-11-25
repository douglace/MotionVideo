# La trêve de Noël 1914 — version motion design

Refonte du montage « 1914 · Reconstitutions illustrées » (69,5 s, 1080×1920), réalisée avec le skill
[`LottieFiles/motion-design-skill`](https://github.com/LottieFiles/motion-design-skill).

```bash
node render.mjs                        # -> build/treve-motion.mp4
node render.mjs --stills 3,12.5,45     # images de contrôle
# aperçu temps réel : servir le dossier puis ouvrir index.html?play
```

## Fichiers
- `index.html`: toute la composition. `renderAt(t)` est déterministe : un même `t` donne toujours la même image.
- `render.mjs`: lance Chromium (Playwright), capture une image tous les 1/30 s et l'envoie à ffmpeg.
- `assets/plate_*.jpg`: les 7 illustrations sans le texte incrusté. Elles ont été reconstruites à partir de la vidéo d'origine : les images sont réalignées par ECC, puis on prend la médiane des pixels qui ne sont pas du texte.
- `assets/timing.json`: le texte et le timing de chaque mot. Ils viennent des sous-titres d'origine, recalés sur les respirations de la voix.
- `assets/voix.wav`: la voix off d'origine.

## Choix guidés par le skill
| Étape (checklist en 8 points) | Décision |
|---|---|
| Émotion | solennité puis tension, et une question finale ouverte |
| Personnalité | **Premium / éditorial** : 350–600 ms, `cubic-bezier(.4,0,.2,1)`, aucun dépassement |
| Easing directionnel | entrées `(.05,.7,.1,1)` (décélération), sorties `(.3,0,1,1)` (accélération), sorties ≈ 50 % plus courtes que les entrées |
| Trois couches | primaire = typographie et sous-titres ; secondaire = caméra Ken Burns et fondus ; ambiante = neige ou braises, grain, vignette, lueur des bougies |
| Récit | une typographie dédiée à chaque temps fort : accroche, date « 1914 », face-à-face des deux camps, chant qui traverse, sources, « trêves locales », rideau « retournement », calendrier, tampon « Condamnée », question A/B |
| Émotion → mouvement | tombes : image désaturée et neige ralentie (tristesse = lent) ; combats : légères secousses ; tampon : motif « impact » en expo |
| Règle du 1/3 | un seul module typographique à la fois ; les sous-titres disparaissent quand le module affiche déjà le texte |
