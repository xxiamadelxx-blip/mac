# Ink Beetle — transparent asset package

Статус: **CANDIDATE**.

Жук приведён к тому же техническому виду, что и приложенный reference asset: отдельный прозрачный RGBA PNG, 1024×1024, общий pivot bottom-center, 8 направлений и 12 состояний.

```
ink_beetle/{direction}/{state}.png
```

Для обратной совместимости старые root-файлы (`idle.png`, `move_01.png`, `attack_01.png`, `hit.png` и т.д.) сохранены как front-direction aliases и также переведены на новый 1024×1024 RGBA стандарт.

Манифест: `enemy_manifest.json`.
