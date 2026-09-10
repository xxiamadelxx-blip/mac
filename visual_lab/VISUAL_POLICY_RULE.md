# Visual Lab — Mandatory Visual Policy Rule

Статус: MANDATORY. Этот документ является коротким входным gate для любой visual/design/art задачи в Moonveil.

Перед генерацией, рисованием, редактированием, экспортом, review или promotion визуала прочитай:

1. AGENTS.md;
2. visual_lab/README.md;
3. этот документ;
4. visual_lab/VISUAL_LAB_PRODUCTION_LAW.md;
5. visual_lab/ASSET_PIPELINE_CODE.md;
6. relevant project/stage document из docs/mockups, docs/manifests или docs/audio.

## Hard rules

- Generated image, mockup, screenshot и технический экспорт — proposal или candidate, а не production truth.
- TECHNICAL PASS != ARTISTIC PASS.
- Для reusable character/creature/environment/UI families сначала фиксируется один representative hero master, затем строятся directions, variants и animation batch.
- World/battle candidates проверяются в enlarged view, true 1x gameplay scale и representative scene/map context.
- Каждый candidate получает immutable candidate ID, semantic asset/family ID и provenance настолько полный, насколько это поддерживает источник.
- Editable source сохраняется, если выбранный инструмент его поддерживает.
- Runtime export должен иметь стабильный путь, hash и связь с manifest.
- Playwright или другой автоматический capture может быть candidate evidence, но не выдаёт artistic approval и не создаёт golden baseline автоматически.
- Только Creative Director может перевести exact candidate в APPROVED GOLDEN.
- Отклонённый candidate остаётся non-promotable evidence и не возвращается в production молча.
- Повторяющийся дефект исправляется в family, template, prompt или validation rule, а не сериям ручных патчей на отдельных ассетах.
- Visual Lab не добавляет Pixelorama, Tiled, ComfyUI, Playwright или другой авторский инструмент в Godot runtime.

## Canonical short flow

SOURCE AUDIT -> FAMILY -> HERO MASTER -> USER IDENTITY APPROVAL -> EDITABLE SOURCE + PROVENANCE -> DERIVED VARIANTS -> TECHNICAL QA -> TRUE GAMEPLAY-SCALE / MAP PREVIEW -> USER FINAL APPROVAL -> APPROVED GOLDEN -> MANIFEST -> PRODUCTION

Если нужного источника, preview, provenance или approval нет, результат нельзя считать готовым production asset.
