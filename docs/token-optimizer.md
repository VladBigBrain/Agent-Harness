# Token Optimizer

Установлена версия 5.13.60 из SHA, указанного в catalog/projects.lock.json. Local marketplace использует наш закреплённый upstream; автоматическое обновление до произвольного upstream main не требуется.

## Что включено

- Skills: token-optimizer, token-coach, fleet-auditor, token-dashboard, resume-checkpoint.
- Профиль balanced: SessionStart, UserPromptSubmit и Stop.
- Compact prompt для сохранения важного контекста при compaction.
- Существующий RTK PreToolUse сохранён. Дополнительное сжатие Bash, per-tool hooks и subagent hooks Token Optimizer выключены.
- Daemon, Keep-Warm, расписания и сторонние model endpoints не настраивались.

Установить/восстановить:

```sh
npm run setup:audit
```

Установщик использует имеющийся Homebrew Python 3.12. Для другого пути можно задать HARNESS_PYTHON. Дополнительные Python-пакеты не устанавливаются.

## Проверка

После перезапуска Codex завершить один обычный ход. Затем вызвать native doctor из установленного каталога:

```sh
/opt/homebrew/bin/python3.12 "$HOME/.codex/plugins/cache/alexgreensh-token-optimizer/token-optimizer/5.13.60/skills/token-optimizer/scripts/measure.py" --runtime codex codex-doctor --project "$PWD"
```

Важно различать registered hooks и фактическое выполнение. Сразу после установки Stop hook ещё не имеет run record. В интерфейсе доступны запросы «Run Token Optimizer», «Run Token Coach», «Run Fleet Auditor» и «Show the dashboard» после загрузки навыков новой сессией.

## Откат

Сначала native `measure.py --runtime codex codex-install --uninstall`, затем `codex plugin remove token-optimizer@alexgreensh-token-optimizer`. Нативный uninstall удаляет только managed hooks/compact prompt. Если конфигурация менялась позже, не восстанавливать весь старый config поверх новых изменений. Backup перед первой установкой отмечен в ignored `.local/last-token-optimizer-backup`.

## Лицензия и оценки

Применяется upstream LICENSE (PolyForm Noncommercial) и LICENSE-SMALL-BUSINESS.md. Сам факт установки не подтверждает наличие прав на применение в любой организации.

Показатели качества контекста и API-стоимости — диагностические оценки, не доказательство корректности задачи и не цена лимита подписки. Экономия на нашей workload ещё не установлена.
