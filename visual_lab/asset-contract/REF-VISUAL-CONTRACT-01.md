# REF-VISUAL-CONTRACT-01 — аудит визуального контракта

TASK-ID: REF-VISUAL-CONTRACT-01
Репозиторий: `xxiamadelxx-blip/mac`, branch `main`
Аудитный baseline: `105b5ca75bda73fd61ddca52c169a14e193e32ae`
Граница работы: только визуальный контракт, манифесты и GitHub binary evidence. Исходный код клонов не изучался и не переносился.

## Итог

Статус: **PARTIAL / GITHUB_BINARY_INTAKE_PENDING**.

Проверка Git tree `baa870ec5e7d809731cdd275ce255edd3df300fe` на baseline `105b5ca75bda73fd61ddca52c169a14e193e32ae` показала: PNG-файлов в repository tree — 1 (USER REVIEW preview); ZIP-файлов — 0. Пакетные PNG пока не размещены.

Это означает только, что на каноническом GitHub path подтверждён один preview-кандидат. Он не заменяет пакетную выкладку и не может быть объявлен `APPROVED GOLDEN` или `PRODUCTION` без отдельного approval.

## Каноническая модель

| Слой | Где находится | Доказательство |
|---|---|---|
| Документация, manifests, evidence | GitHub | live path и commit SHA |
| USER REVIEW preview | GitHub repository, `docs/mockups/<stage>/` | отдельный PNG, blob и review pack |
| Партия | `docs/asset_batches/<stage>/batch-<NNN>.json` | status `PLACED`, полный список путей и commit SHA |
| Runtime | локальные импортированные asset paths | Godot import/runtime evidence |

## Известные слоты

- Stage 01 menu v04: 50 отдельных PNG; пока ожидаются две партии `40 + 10`.
- Stage 02 arena: видимые base, props, landscape, interior, ambient VFX, remains и foreground должны быть реальными файлами; кодовая арена не принимается.
- Stage 03 heroes: 192 PNG (`8 × 12 × 2`), пять партий `40 + 40 + 40 + 40 + 32`.
- Stage 04 enemies и последующие stages: binary slots считаются отсутствующими, пока соответствующие GitHub files и evidence не проверены.

## Допустимые runtime links

1. Runtime ссылается на локальные repository paths из утверждённого manifest; он не загружает ассеты из сети во время игры.
2. Ожидаемая форма Stage 03: `docs/mockups/03-heroes/{hero_id}/{direction}/{state}.png`.
3. Для арены, врагов, оружия, пассивок, артефактов, XP, HUD и VFX нельзя придумывать links по названиям контента; нужен фактический PNG path и manifest entry.
4. Technical file pass не является artistic approval. `USER_REVIEW`, `APPROVED_GOLDEN` и `PRODUCTION` должны быть разделены.

## Не принимать как финальный визуал

- папку или filename без реального PNG;
- manifest/evidence без связанного GitHub blob;
- GitHub Release asset вместо файла в repository tree;
- ZIP, archive, Base64, data URL, SVG/HTML replacement или draw-код вместо PNG;
- screenshot, preview или технический pass без exact candidate approval;
- любой candidate без explicit Creative Director approval;
- изменение или перегенерацию Линь Юэ и Соён Хан под видом транспортировки.

## Handoff

Parent HEAD: 105b5ca75bda73fd61ddca52c169a14e193e32ae
Changed path: `visual_lab/asset-contract/REF-VISUAL-CONTRACT-01.md`
Status: `PARTIAL / GITHUB_BINARY_INTAKE_PENDING`
Evidence: GitHub recursive tree baa870ec5e7d809731cdd275ce255edd3df300fe; pngCount=1 (review preview); zipCount=0.
Open blockers: first approved package is not yet committed; no package evidence exists; runtime import and artistic approval remain open.
Next action: after exact preview approval, upload only the first package (maximum 40 PNG), verify every GitHub blob, write its evidence file, and stop.
