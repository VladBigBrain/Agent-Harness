# Agent Harness

Готовые инструменты для экономичной работы Codex: сжатие вывода, точное чтение кода и измерение расхода. Репозиторий объединяет существующие проекты; собственного агентного фреймворка здесь нет.

## Быстрый старт: macOS Apple Silicon

Нужны Git, Node.js/npm, curl и shasum. Сначала:

```sh
git clone https://github.com/VladBigBrain/Agent-Harness.git
cd Agent-Harness
npm run setup:core
npm run activate:codex
npm run doctor
npm run usage
```

`setup:core` ставит RTK-OSS 1.1.0 из проверенного SHA256 release-архива и ccusage 20.0.45 из npm lockfile. Бинарники и зависимости остаются в `.local/` и `node_modules/`, ссылки команд создаются в `~/.local/bin/`. Отчёты usage по умолчанию скрывают денежные API-оценки. Существующие чужие команды не перезаписываются. Веса моделей и optional-инструменты не загружаются.

`activate:codex` сохраняет локальные копии прежних настроек и вызывает штатную интеграцию RTK и закрепляет абсолютный путь её hook. Нужен новый чат/перезапуск клиента; если Codex запросит доверие к hook, его следует проверить через интерфейс клиента. Настройки permissions/sandbox не ослабляются.

## Состав

| Проект | Версия | Назначение | Этап |
|---|---|---|---|
| [RTK](https://github.com/rtk-ai/rtk) | 1.1.0, OSS binary | Сокращение shell-вывода до передачи модели | Установка core |
| [ccusage](https://github.com/ccusage/ccusage) | 20.0.45 | Локальные отчёты токенов Codex | Установка core |
| [Serena](https://github.com/oraios/serena) | 2.1.0 | Определения, references и точное чтение кода через MCP | Optional, сравнить с имеющимся codegraph |
| [Headroom](https://github.com/headroomlabs-ai/headroom) | 0.42.0 | Большие JSON/логи, компрессия с доступом к оригиналам | Optional, отдельный MCP/proxy пилот |
| [jCodeMunch](https://github.com/jgravelle/jcodemunch-mcp) | 1.108.400 | AST и получение исходника по символу | Optional, проверить коммерческую лицензию |
| [Token Optimizer](https://github.com/alexgreensh/token-optimizer) | 5.13.60, pinned SHA | Аудит, dashboard, обнаружение циклов | Установлен, balanced; лицензия имеет ограничения |
| [Semantic Router](https://github.com/aurelio-labs/semantic-router) | 1.1.1 | Маршрутизация в отдельном workflow | Optional library |
| [FastEmbed](https://github.com/qdrant/fastembed) | 0.9.1 | Локальные embeddings через ONNX | Optional library; модели отдельно |

Исходники закреплены Git submodules в `upstream/`. Полные SHA и upstream URL: [catalog/projects.lock.json](catalog/projects.lock.json). Для получения всех исходников:

```sh
git submodule update --init --depth 1 --jobs 4
```

Публикация submodule-ссылок не меняет лицензии upstream и не активирует инструменты. Не запускайте одновременно все альтернативные индексаторы и компрессоры.

## Что считать экономией

RTK `gain` измеряет сокращение обработанного вывода. ccusage показывает usage из доступной локальной истории; показанные API-оценки стоимости не равны списанию лимита подписки. Главный критерий — меньше total usage/повторных шагов на ту же корректно решённую задачу.

Начальный пилот: обычные чтения git/rg и результаты тестов. Сохранять полный вывод при диагностике, проверять реальные exit codes и возможность получить исходные факты. Внутренний router облачной модели Desktop эти инструменты не заменяют.

## Документы

- [Лицензии и источники](docs/third-party.md)
- [Проверка и откат](docs/operations.md)
- [Статус внедрения](docs/status.md)

Прежний набор Skills/Tools удалён из актуального дерева. Полная старая версия доступна в теге `archive/pre-token-stack-20261028`; история Git сохранена.

## Аудит Token Optimizer

Установлен Token Optimizer 5.13.60. Воспроизводимая установка из закреплённого local marketplace:

```sh
npm run setup:audit
```

Профиль balanced включает SessionStart, UserPromptSubmit и Stop. Дополнительное Bash-сжатие и subagent hooks отключены: shell-вывод обрабатывает RTK. Фоновые daemon/Keep-Warm не устанавливаются. Сначала установите core; затем после установки аудита перезапустите Codex. Подробности: [docs/token-optimizer.md](docs/token-optimizer.md).
