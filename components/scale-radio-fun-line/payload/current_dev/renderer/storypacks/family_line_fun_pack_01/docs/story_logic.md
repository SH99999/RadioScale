# Story logic notes

The 2,880 scene count is generated deterministically from:
- 48 templates
- 5 ending styles
- 4 tempo profiles
- 3 reaction packs

Formula:
48 x 5 x 4 x 3 = 2880

The current pack ships both the raw templates and the pre-generated scene index.
A future engine can either:
1. load `stories/generated/scene_index_2880.json` directly, or
2. re-generate scenes from the templates and variant rules.

## Humour approach
The pack is designed around:
- anticipation
- wrong confidence
- delayed reaction
- animal interruption
- proud failure
- silent side-eye

## Family-safe double meanings
A handful of templates are flagged `double_meaning_light=true`.
These are still family-safe and rely on interrupted posing, vanity, timing, or misunderstanding rather than explicit content.
