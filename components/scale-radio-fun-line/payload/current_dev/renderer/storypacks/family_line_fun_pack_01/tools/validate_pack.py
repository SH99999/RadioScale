#!/usr/bin/env python3
import json
from pathlib import Path
root = Path(__file__).resolve().parents[1]
manifest = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
scenes = json.loads((root / 'stories/generated/scene_index_2880.json').read_text(encoding='utf-8'))
assert len(scenes) == manifest['counts']['generated_playable_scenes']
actor_ids = {p.stem for p in (root / 'actors').glob('*.json')}
prop_ids = {p.stem for p in (root / 'props').glob('*.json')}
for scene in scenes:
    assert scene['prop'] in prop_ids, scene['prop']
    for actor in scene['cast']:
        assert actor in actor_ids, actor
print('OK: content pack validated', len(scenes), 'scenes')
