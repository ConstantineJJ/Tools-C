# Research notes — weapon module (2026-11-18)

Not loaded by default. Paraphrased takeaways; sources keep their own wording and rights.
Selection criterion: useful for stylized mid-poly game weapons with purposeful detail.

| Source | Type | Adopted takeaway | Caveat |
|---|---|---|---|
| [80 Level — Creating highly detailed weapons for games (Ben Leary)](https://80.lv/articles/creating-highly-detailed-weapons-for-games/) | Professional interview | Build parts as real manufactured components; work out the weapon's anatomy (feed, aiming, heat, recoil) first; every detail has a reason; avoid shotgun greebles; macro → micro; keep animating parts separate, merge the rest; cables carry power/data between communicating parts | Realistic FPS focus; high/low bake specifics not adopted |
| [80 Level — Notes on weapon concept art](https://80.lv/articles/notes-on-weapon-concept-art) | Concept artist article | Form follows function; build from an internal skeleton outward; rest areas lead the eye to focal points; avoid details so small they read as noise; minimum-maximum: fewer, well-chosen parts | Concept stage, not mesh-level guidance |
| [80 Level — Hard surface tips, vintage gun (Remedy artist)](https://80.lv/articles/hard-surface-modeling-tips-tricks-for-creating-a-vintage-quirky-looking-gun) | Production breakdown | Bevel (arc miter, weight limit) + Weighted Normal workflow; build parts by cutting simple stock; name each part by its function — if you cannot, you do not understand it yet | Settings must be tuned per object |
| [CG Master Academy — 5 details from good to real](https://cgmasteracademy.com/blog/5-hard-surface-modeling-details-to-advance-your-weapon-from-good-to-real.html) | Studio blog | Wear follows plausible contact/handling/drop paths; precise small details (e.g. optic angles) matter; story details add life | Realism-oriented; stylized projects exaggerate instead |
| [Warframe — Basic art guide](https://www.warframe.com/steamworkshop/basic-art-guide) | Studio guideline | Primary/secondary/tertiary layering; balance forms roughly 2:1 and avoid equal splits or repeated spacing; avoid long thin shapes that read poorly | Written for Warframe's style |
| [80 Level — Mid-poly workflow in UE5](https://80.lv/articles/creating-assets-within-the-mid-poly-workflow-in-ue5/) and Polycount mid-poly threads | Production practice | Mid-poly with face-weighted normals gives clean shading and fast iteration without high/low re-rolls | Engine/normal export must preserve custom normals |
| [Power & Motion — cylinder mounting](https://www.powermotiontech.com/technologies/cylinders-actuators/article/21882875/wrestling-with-cylinder-mounting-options) | Engineering trade article | Clevis/eye mounts provide pivots at both ends; long strokes need adequate rod strength | Engineering, not art; used only for plausibility |
| [80 Level — flintlock pepperbox (gunsmith pipelines)](https://80.lv/articles/crafting-intricate-flintlock-pepperbox-pistol-in-3d/) | Production breakdown | For swappable modules, organize objects and texture sets by functional purpose and position | Hand-held firearm context |

Rejected for the skill: tool-specific add-on workflows, photoreal texturing recipes,
universal triangle budgets and any claim that one fixed polycount fits all games.
