# Upstream и лицензии

Проверено 2026-10-28. Закреплённые SHA находятся в `catalog/projects.lock.json`; применяются тексты лицензий именно выбранных версий.

| Компонент | Условия, существенные для выбора |
|---|---|
| RTK-OSS | Apache-2.0. Используем release-asset `rtk-oss-aarch64-apple-darwin.tar.gz`, не full RTK с BUSL engine |
| ccusage | MIT |
| Serena 2.x | Приложение GPL-3.0-or-later, SolidLSP MIT |
| Headroom | Apache-2.0; условия дополнительных моделей проверяются отдельно |
| jCodeMunch | Dual-Use; коммерческое применение требует отдельной лицензии |
| Token Optimizer | PolyForm Noncommercial и дополнительные разрешения автора; не считать MIT |
| Semantic Router | MIT; выбранные providers имеют собственные условия |
| FastEmbed | Apache-2.0; отдельная лицензия у каждой embedding-модели |

Submodules сохраняют оригинальные copyright notices и историю происхождения. Этот каталог не предоставляет дополнительных прав на upstream-код. Наличие исходников не означает разрешения активировать платный сервис или автоматически отправлять ему данные.

Основные источники: README/LICENSE каждого upstream; RTK `hooks/codex/README.md`; ccusage Codex guide; https://learn.chatgpt.com/docs/hooks.
