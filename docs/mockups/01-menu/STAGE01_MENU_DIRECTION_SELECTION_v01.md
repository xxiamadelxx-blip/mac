# Stage 01 — Menu Direction Selection v01

Status: **REVIEW** — три визуальных направления созданы. Направление B рекомендовано как основа, но финальная интерактивная UI-система ещё не утверждена.

## Варианты

| Вариант | Файл | Роль в сравнении |
|---|---|---|
| A | [STAGE01_MENU_DIRECTION_A_v01.png](./STAGE01_MENU_DIRECTION_A_v01.png) | Кинематографичный лунный сад; сильная атмосфера |
| B | [STAGE01_MENU_DIRECTION_B_v01.png](./STAGE01_MENU_DIRECTION_B_v01.png) | Основной кандидат: лучший баланс атмосферы, навигации и гача-иерархии |
| C | [STAGE01_MENU_DIRECTION_C_v01.png](./STAGE01_MENU_DIRECTION_C_v01.png) | Чернильно-фонарная композиция; самый тёмный и камерный вариант |

## Рекомендованная база: Direction B

Почему:

- хорошо читается вертикальная мобильная иерархия;
- валюты Gold и Lunar Seals видны сразу;
- есть одна очевидная главная кнопка **START RUN**;
- в меню одновременно присутствуют главная героиня и карточка второй героини;
- нижняя навигация естественно раскладывается на Heroes, Arsenal, Artifacts и Settings;
- визуальный язык подходит для премиальной японско-корейско-китайской fantasy gacha-подачи.

## Экранный пакет Direction B v01

Рекомендованное направление расширено связанными состояниями меню:

| Состояние | Файл | Назначение |
|---|---|---|
| Home / направление B | [STAGE01_MENU_DIRECTION_B_v01.png](./STAGE01_MENU_DIRECTION_B_v01.png) | Точка входа, валюты, START RUN и навигация |
| Heroes | [STAGE01_MENU_HEROES_v01.png](./STAGE01_MENU_HEROES_v01.png) | Выбор Линь Юэ/Соён Хан, роли и характеристики |
| Run Setup | [STAGE01_MENU_RUN_SETUP_v01.png](./STAGE01_MENU_RUN_SETUP_v01.png) | Карта, сложность, длительность, checkpoint, артефакты и стартовое оружие |
| Loading | [STAGE01_MENU_LOADING_v01.png](./STAGE01_MENU_LOADING_v01.png) | Переход в первый забег и короткая подсказка |
| Victory | [STAGE01_MENU_RESULT_VICTORY_v01.png](./STAGE01_MENU_RESULT_VICTORY_v01.png) | Успешный результат, reward ledger preview и Claim Rewards |
| Defeat / Run Ended | [STAGE01_MENU_RESULT_DEFEAT_v01.png](./STAGE01_MENU_RESULT_DEFEAT_v01.png) | Поражение, сохранённый checkpoint и Try Again |

Навигационный контракт v01:

`Home → Heroes → Run Setup → Loading → Arena`

`Arena → Victory/Run Ended → Claim Rewards → Home`

`Run Ended → Try Again → Run Setup`

Эти PNG показывают композицию и иерархию. Точные тексты, числовые значения наград, состояния кнопок и идемпотентное начисление наград должны быть реализованы по каноническим документам, а не считаны из сгенерированного изображения.

## Обязательная корректировка перед финальным UI

- заменить весь сгенерированный placeholder-текст на точные локализованные строки;
- исправить имена и подписи на **Lin Yue** и **Soyeon Han**;
- закрепить типографику, safe area 390×844 и размеры touch-target;
- подготовить состояния normal, pressed, disabled и locked;
- разложить арт на отдельные слои: фон, персонажи, карточки, панели, иконки, текст и эффекты;
- описать переходы Home → Heroes → Run Setup → Arena;
- не считать PNG финальным игровым интерфейсом: это art-direction reference для реализации в выбранном движке.

## Критерий утверждения направления

Направление можно перевести из REVIEW в APPROVED после проверки читаемости на телефоне, согласования точных строк и принятия набора экранов: Home, Heroes, Run Setup, Loading и Result.
