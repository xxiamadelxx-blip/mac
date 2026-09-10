# Навыки и рабочие инструкции

## Обязательные навыки

Если они доступны в текущем чате, используй:

1. keystone:project-audit — read-only аудит репозитория, drift и evidence.
2. keystone:product-planning — формализация цели, поведения, trade-offs и acceptance.
3. keystone:task-creation — разбиение на проверяемые вертикальные срезы.
4. codex-engineering-guardrails:code-work — контролируемые изменения и scope.
5. codex-engineering-guardrails:code-verification — независимая проверка требований и результатов.

Для GitHub-навигации можно использовать atlas-scout:atlas-scout-code-navigation, но он необязателен.

## Если Atlas Scout недоступен

Это не блокер и не отдельная пользовательская задача. Используй разрешённые GitHub tree/file reads, поиск по символам/путям и локальный rg, если checkout доступен. В отчёте укажи fallback как ограничение окружения, но не выдумывай индекс.

## Что не нужно подключать

Balance-only работа не требует Visual Lab, image generation, art review или asset pipeline. Если задача внезапно начинает менять UI-art, sprite, VFX, environment или mockup, остановись на границе creative/visual решения и передай её Visual Lab-маршруту из корневого AGENTS.md.

## Протокол каждой итерации

1. Прочитать инструкции уровня репозитория.
2. Проверить живой source и состояние дерева.
3. Составить маленький change set.
4. Для каждого числа указать source/status/formula.
5. Запустить самый узкий релевантный тест/симуляцию.
6. Запустить независимую verification-проверку.
7. Обновить evidence и open decisions.
8. Только затем перейти к следующему срезу.

## Технические правила

- Не хранить баланс в UI-текстах или случайных controller constants.
- Не добавлять зависимость только ради красивого графика.
- Не использовать ручной результат одного «удачного» забега как доказательство.
- Не подменять runtime-test симуляцией.
- Не считать валидный JSON доказательством подключённого data source.
- Не исправлять unrelated drift.
- Не выполнять destructive commands.
- Не делать внешние GitHub writes, если текущий пользовательский запрос не разрешил изменение; для этого пакета разрешены изменения его рабочей папки.

## Формат evidence

Для каждого требования показывай:

Requirement → Source → Implementation/Model → Check → Observed → Status.

Различай:

- SPECIFIED — правило есть в источнике;
- DERIVED — получено из формулы;
- SIMULATED — проверено моделью;
- RUNTIME_VERIFIED — проверено в игре/тесте;
- NOT_IMPLEMENTED — ещё не подключено;
- BLOCKED — не хватает решения/инфраструктуры.
