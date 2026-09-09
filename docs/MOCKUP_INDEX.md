# MOCKUP INDEX — Moonveil: Eclipse

Этот файл является индексом визуальных и производственных артефактов. Каждая папка получает реальные файлы по мере закрытия соответствующего этапа ROADMAP.md.

## Правила хранения

- Один результат имеет уникальный идентификатор и версию.
- `*.png`/`*.jpg` — preview или concept image.
- `*.svg` — векторный UI/иконка, если он действительно нужен для реализации.
- `*.md` — описание, размеры, состояния, поведение и критерии проверки.
- `*.json` — машиночитаемая привязка контента к игре.
- Нельзя заменять отсутствующий результат пустым README и отмечать этап DONE.

## Каталоги

| Этап | Каталог | Содержание | Статус |
|---:|---|---|---|
| 1 | `docs/mockups/01-menu/` | Главное меню и навигация | IN PROGRESS |
| 2 | `docs/mockups/02-arena/` | Живой ландшафт, вода, растения, частицы и след боя | IN PROGRESS |
| 3 | `docs/mockups/03-heroes/` | Две героини и боевые силуэты | PLANNED |
| 4 | `docs/mockups/04-enemies/` | Десять противников | PLANNED |
| 5 | `docs/mockups/05-bosses/` | Четыре босса и фазы | PLANNED |
| 6 | `docs/mockups/06-weapons/` | Иконки, атаки и эволюции оружия | PLANNED |
| 7 | `docs/mockups/07-passives/` | Иконки и карточки пассивок | PLANNED |
| 8 | `docs/mockups/08-artifacts/` | Артефакты и Кодекс реликвий | PLANNED |
| 9 | `docs/mockups/09-xp/` | XP-точки/кристаллы, магнитный подбор и шкала | PLANNED |
| 10 | `docs/mockups/10-hud/` | HUD игрового забега | PLANNED |
| 11 | `docs/manifests/11-weapon-animation/` | Manifest анимаций и привязок оружия | PLANNED |
| 12 | `docs/manifests/12-passive-binding/` | Manifest пассивок и привязок | PLANNED |
| 13 | `docs/audio/13-plan/` | Аудиоплан, naming и лицензии | PLANNED |
| 14 | `docs/mockups/14-enemy-death/` | Смерть, трупы, конечности и накопленный след боя | PLANNED |
| 15 | `docs/mockups/15-boss-death/` | Распад боссов и изменение состояния арены | PLANNED |
| 16 | `docs/mockups/16-upgrade-offers/` | Карточки предложений улучшений | PLANNED |
| 17 | `docs/mockups/17-artifact-ui/` | Интерфейс артефактов | PLANNED |
| 18 | `docs/manifests/18-synergy-logic/` | Логика синергий | PLANNED |
| 19 | `docs/mockups/19-synergy-info/` | Информационный интерфейс синергий | PLANNED |
| 20 | `docs/roadmap/20-proposals/` | Дополнительные предложения | DOCUMENTED |

## Именование

Формат: `STAGE##_AREA_TYPE_v##.ext`.

Примеры:

- `STAGE01_MENU_HOME_v01.png`
- `STAGE03_HERO_LIN_YUE_v01.md`
- `STAGE11_WEAPON_JADE_TALISMANS_v01.json`
- `STAGE13_AUDIO_EVENT_TABLE_v01.md`

## Текущий активный результат

Этап 1 остаётся IN PROGRESS. По явному решению пользователя активирован этап 2: docs/mockups/02-arena/ теперь содержит макро-схему большого мира 4×3 экранов, открытый кадр камеры, слои, контрольные кадры, карту данных и Godot runtime-preview. Этап 3 не начинается до закрытия текущих критериев арены.