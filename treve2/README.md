# La trêve de Noël 1914 — 100 % motion design

Tout est dessiné et animé en code (canvas 2D) : personnages articulés, décors, objets, carte, transitions.
Seuls la voix off et le timing mot à mot viennent de la vidéo d'origine (`../treve/assets`).

```bash
node render.mjs                        # -> build/treve-anime.mp4 (puis ré-encodage web CRF 24)
node render.mjs --stills 3,20,59.6     # images de contrôle
```

- **Personnages**: `soldier()` est un rig 2D (jambes, bras en 2 segments, tête, bouche, clignement, respiration, cycle de marche). Les poses (`POSE.aim`, `shake`, `sing`, `up`, `bow`…) sont interpolées entre elles.
- **Décor**: le « monde du front », avec les tranchées vues en coupe, le no man's land, les barbelés, le ciel étoilé et la lune.
- **Scènes**: 16 scènes calées sur les phrases de la voix. Les transitions sont de trois types : fondu, passage par le noir ou coupe.
- **Règles du skill motion-design**: personnalité Premium (ease (.4,0,.2,1), aucun rebond), entrées qui ralentissent et sorties qui accélèrent, trois couches (personnages et typographie / caméra / neige et grain), anticipation quand les fusils se baissent, motif « impact » pour le tampon, cascade des lumières sous 500 ms.
