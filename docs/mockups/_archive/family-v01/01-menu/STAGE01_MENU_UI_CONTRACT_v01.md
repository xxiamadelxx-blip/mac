# Stage 01 — Menu UI Contract v01

Status: **IN PROGRESS** — visual screen-flow mockups exist; implementation in Godot and final copy pass are pending.

## 1. Screen inventory

| screen_id | Экран | Вход | Главные действия |
|---|---|---|---|
| `home` | Home | запуск приложения, Return Home | Heroes, Arsenal, Artifacts, Settings, Start Run |
| `heroes` | Heroes | Home → Heroes | выбрать Lin Yue или Soyeon Han, открыть Run Setup |
| `run_setup` | Run Setup | Home → Start Run или Heroes | выбрать героиню/артефакты, подтвердить Start Run |
| `loading` | Loading | Run Setup → Start Run | показать progress и короткую подсказку |
| `victory` | Victory | Arena → 20:00 | посмотреть результат, Claim Rewards, Return Home |
| `run_ended` | Run Ended | Arena → поражение | Claim Rewards, Try Again, Return Home |

## 2. Navigation contract

`Home → Heroes → Run Setup → Loading → Arena`

`Home → Run Setup → Loading → Arena`

`Arena → Victory → Claim Rewards → Home`

`Arena → Run Ended → Claim Rewards → Home`

`Run Ended → Try Again → Run Setup`

Правила:

- Back из Heroes и Run Setup возвращает на предыдущий экран;
- Loading не имеет обычной кнопки Back после начала загрузки;
- Claim Rewards сначала атомарно завершает reward ledger, затем открывает Home;
- повторное нажатие Claim Rewards не должно начислять Gold, Lunar Seals или Boss Essence повторно;
- Return Home с экрана результата открывает подтверждение, если reward ledger ещё не обработан;
- любой экран должен иметь один понятный следующий шаг и не оставлять пользователя в тупике.

## 3. Required button states

| state | Внешний вид | Поведение |
|---|---|---|
| `normal` | полный контраст, доступный accent | принимает tap |
| `pressed` | короткое scale/brightness feedback | блокирует повторный tap на время transition |
| `disabled` | сниженный контраст, без свечения | tap не меняет состояние и объясняется причиной |
| `locked` | замок/условие разблокировки | открывает tooltip или экран условия, но не запускает действие |
| `loading` | progress/spinner, текст действия сохраняется | блокирует повторный tap до результата |

Минимальный touch-target: **48×48 dp**. Важные кнопки Start Run, Claim Rewards и Try Again должны иметь визуально большую область, чем минимальный target.

## 4. String keys

До сборки интерактивного UI все строки переносятся в локализационный ресурс. Сгенерированные PNG не являются источником текста.

| key | English baseline | Русский baseline |
|---|---|---|
| `menu.start_run` | Start Run | Начать забег |
| `menu.heroes` | Heroes | Героини |
| `menu.arsenal` | Arsenal | Арсенал |
| `menu.artifacts` | Artifacts | Артефакты |
| `menu.settings` | Settings | Настройки |
| `menu.select_hero` | Select Hero | Выбрать героиню |
| `menu.run_setup` | Run Setup | Подготовка забега |
| `menu.loading` | Loading | Загрузка |
| `menu.claim_rewards` | Claim Rewards | Забрать награды |
| `menu.try_again` | Try Again | Повторить |
| `menu.return_home` | Return Home | В меню |
| `menu.run_ended` | Run Ended | Забег завершён |
| `menu.victory` | Victory | Победа |
| `menu.checkpoint_saved` | Checkpoint Reward Saved | Награда контрольной точки сохранена |

Имена героинь и content_id не переводятся: `lin_yue` → Lin Yue / Линь Юэ, `soyeon_han` → Soyeon Han / Соён Хан.

## 5. Layout contract

- базовый preview: **390×844**, portrait 9:16;
- safe area: минимум 16 dp по бокам и 24 dp сверху/снизу, если устройство имеет вырез или системную панель;
- навигационная полоса не перекрывает primary action;
- текст контрастен относительно фона; цвет не является единственным маркером состояния;
- портреты могут быть детализированными, но мелкий текст и декоративные печати не должны быть обязательными для понимания действия;
- верхняя зона валют показывает Gold и Lunar Seals; Boss Essence не показывается как обычный доступный кошелёк, если он не нужен на данном экране;
- значения валют берутся из локального profile state, а не захардкожены в UI;
- reward cards получают значение из завершённого reward ledger, а не из картинки или локального display-only state.

## 6. Art layer contract

Каждый экран должен быть разложен на отдельные Godot-слои:

1. background / environment;
2. character art;
3. decorative VFX;
4. panels and frames;
5. icons;
6. text and localization;
7. buttons and interaction state;
8. accessibility/feedback layer.

Сгенерированные изображения используются для направления композиции и палитры. В финальной сцене нельзя оставлять PNG единственным слоем интерактивного меню.

## Русская слоёная версия

Для каждого экрана добавлены отдельные PNG:

- ART — исходный неизменённый арт;
- UI_RU — прозрачный слой с непрозрачными масками и русским текстом;
- COMPOSITE_RU — контрольная сборка арт + UI_RU.

Это сделано специально, чтобы не перерисовывать героинь и не получать новые мутации лица, причёски или костюма. UI-слой закрывает старые английские подписи и не использует текст, сгенерированный вместе с картинкой.

## 7. Navigation prototype status

A first Godot navigation prototype is present:

- `project.godot` sets Godot 4.x, portrait 390×844 viewport and mobile-compatible renderer;
- `scenes/menu/menu.tscn` is the entry scene;
- `scripts/menu/menu_controller.gd` creates real buttons and routes Home, Heroes, Run Setup, Loading, preview result states and placeholder sections;
- the Loading route intentionally stops at an Arena handoff because Stage 02 gameplay is not implemented yet.

The prototype is evidence of route wiring only. It is not evidence of a finished menu, APK, reward ledger or arena.

## 8. Stage 01 closure

Stage 01 можно перевести в DONE только после:

- реализации экранов `home`, `heroes`, `run_setup`, `loading`, `victory`, `run_ended` в Godot;
- реализации normal/pressed/disabled/locked/loading states;
- проверки safe area на реальном Android-экране;
- проверки переходов и Back;
- проверки идемпотентного Claim Rewards;
- замены placeholder/generated текста локализационными строками;
- прикреплённого evidence: APK или screen recording полного маршрута.
