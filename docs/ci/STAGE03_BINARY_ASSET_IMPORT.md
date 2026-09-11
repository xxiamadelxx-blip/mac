# Stage 03 — individual GitHub PNG batch intake

Статус: **IMPLEMENTED / GITHUB BINARY INTAKE PENDING**.

Контур принимает уже существующие PNG героинь непосредственно в GitHub repository. Он не генерирует изображения, не мутирует героинь и не передаёт бинарные данные через чат.

## Канонический поток

готовые PNG на диске агента
  -> source manifest с github_path
  -> одна партия: 40 файлов или остаток
  -> отдельные GitHub blobs в docs/mockups/03-heroes/
  -> asset commit + batch evidence JSON
  -> CI проверяет каждый PNG, размер и SHA-256
  -> Godot использует локальный asset path

Для одного героя требуется 96 PNG: 8 направлений × 12 состояний. Для двух героинь — 192 PNG. Это пять отдельных запусков: `40`, `40`, `40`, `40`, `32`.

## Требуемая структура Stage 03

docs/mockups/03-heroes/
  lin_yue/<direction>/<state>.png
  soyeon_han/<direction>/<state>.png

Разрешены восемь направлений (`front`, `back`, `left`, `right`, `north_west`, `north_east`, `south_east`, `south_west`) и двенадцать состояний (`idle`, `move_01`, `move_02`, `move_03`, `attack_01`, `attack_02`, `attack_03`, `hit_01`, `hit_02`, `death_01`, `death_02`, `shadow`).

Каждый PNG проверяется как настоящий файл; для runtime Stage 03 дополнительно требуется 1024×1024, 8-bit true RGBA, прозрачный фон и корректная папка героя/направления/состояния.

## Статус текущего request

`docs/ci/STAGE03_IMPORT_REQUEST.json` имеет `PENDING_GITHUB_UPLOAD`: это план на 192 отдельных PNG, а не доказательство их наличия. Пока batch evidence не содержит фактических GitHub paths/blobs, runtime binary intake не закрыт.

## Приёмка

Партия считается `PLACED` только если:
- в `main` появились все заявленные PNG-файлы именно в `docs/mockups/03-heroes/...`;
- каждый path проверен как реальный GitHub file/blob;
- размер и SHA-256 совпали;
- evidence JSON содержит commit SHA и полный список партии;
- текущий запуск завершился и не начал следующую партию.

Это не означает artistic approval, `APPROVED GOLDEN`, `PRODUCTION` или Android release readiness.

## Ограничения

ZIP, архивы, PNG/Base64 в чат, GitHub Release assets, SVG/HTML/data URL и draw-код вместо реальных файлов запрещены. Линь Юэ и Соён Хан не перегенерируются и не мутируются.
