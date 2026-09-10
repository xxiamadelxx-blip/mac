# Stage 03 — binary asset import

Статус: **IMPLEMENTED / CANDIDATE INTAKE**.

Этот контур решает только передачу готовых бинарных PNG в репозиторий. Он не
генерирует изображения и не прогоняет PNG или Base64 через чат.

## Канонический поток

```text
готовые PNG -> один ZIP -> GitHub Release asset -> GitHub Actions
-> проверка -> docs/mockups/03-heroes/<hero>/...png -> commit в main
```

Источник ZIP остаётся прикреплённым к Release. Это даёт один устойчивый
источник байтов и позволяет повторить импорт без копирования содержимого в
переписку.

## Что положить в ZIP

Для одного героя архив содержит полный набор из 96 файлов:

```text
lin_yue/
  front/idle.png
  front/move_01.png
  ...
  south_west/shadow.png
```

Разрешены два героя в одном архиве, тогда всего 192 PNG:

```text
lin_yue/<direction>/<state>.png
soyeon_han/<direction>/<state>.png
```

Также принимается архив, в котором перед этими путями уже стоит префикс
`docs/mockups/03-heroes/`. `hero_manifest.json`, README и другие файлы в ZIP
не нужны и будут отклонены.

Проверяются:

- только полный набор одного или двух героев;
- восемь направлений и двенадцать состояний по текущему contract;
- каждый файл — PNG 1024×1024, 8-bit true RGBA;
- отсутствие `..`, абсолютных путей, symlink и дубликатов;
- запрет перезаписи уже существующего файла.

Импортёр не меняет существующие `hero_manifest.json`, stage manifest,
provenance или runtime code. Попавшие PNG остаются candidate/technical intake,
пока Creative Director отдельно не подтвердит exact candidate.

## Загрузка с телефона

1. Выбери готовые PNG в файловом менеджере Android и создай ZIP. Для первого
   прогона используй только `lin_yue` и имя
   `stage03-assets-lin-yue-v01.zip`.
2. Открой GitHub в браузере и создай новый Release в
   `xxiamadelxx-blip/mac`.
3. Используй новый tag, например `stage03-assets-lin-yue-v01`, прикрепи ZIP
   как Release asset и опубликуй Release.
4. Workflow `Import Stage 03 binary hero assets` запустится автоматически.
   Он скачает ZIP внутри GitHub Actions, проверит его и сам создаст commit в
   `main`.

Если автоматический запуск не сработал, запусти этот workflow вручную через
Actions и укажи тот же tag и точное имя ZIP. Новый исправленный набор отправляй
с новым tag: существующие PNG намеренно не перезаписываются.

## Приёмка

Успешный импорт означает только следующее:

- ZIP найден и его SHA-256 записан в Actions summary;
- все файлы прошли структурную и PNG-проверку;
- PNG появились в правильной hero-папке;
- Actions создал commit в `main`;
- evidence `import.log` и `archive.sha256` сохранены как workflow artifact.

Это не означает artistic approval, APPROVED GOLDEN или PRODUCTION. Для этих
статусов остаются действующими Visual Lab и пользовательская приёмка.

## Причины типичного отказа

- `Asset name must match...` — имя должно начинаться с `stage03-assets-` и
  заканчиваться `.zip`.
- `incomplete` — в архиве не хватает одного из 96 файлов героя либо есть
  лишний путь.
- `expected 1024x1024` — экспорт сделан в другом размере.
- `expected 8-bit true RGBA` — PNG палитровый, RGB без alpha или с другим
  bit depth.
- `refusing to overwrite` — этот путь уже импортирован; создай новый candidate
  с новым именем/путём после отдельного решения о замене.
