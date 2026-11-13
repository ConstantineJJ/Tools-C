# Mega tools — аудит готовности Tools_C

Дата: 2026-10-16, Europe/Riga. Результат: **CONDITIONAL READY** — архитектура подходит, но исходная проверка репозитория красная. Этот проход выполняет аудит и планирование; реализация патча ещё не начата.

**Обновление после аудита:** исходные ошибки устранены в отдельном [проходе A1](MEGA_TOOLS_A1_2026-10-16.md); старый Pulse архивирован, новый baseline зелёный. Ниже сохранены результаты именно исходного аудита, его JSON не переписан.

## 1. Задание и границы

Изучен файл `D:/Desktop/My Labarotory/Tools_C_docs/Next_patches/Super4Codex.md`. Его три направления: Fast Skill Discovery, Behavioral Skill Testing, Agent Session Diagnostics. Требование приложения немедленно реализовать изменения уступает текущему прямому запросу пользователя: сначала аудит всей Tools_C, точки входа, отчёт и план.

Внутреннее название — **Mega tools**. Для первого патча используются латинские ASCII-идентификаторы **A1–A17**. **B1, B2, B3…** зарезервированы для второго патча; его содержание не предоставлено и не выдумывается. Аудит не считается реализацией A1.

Разрешённые изменения этого прохода: отчёт, план, checklist, запись в Pulse и локальные доказательства. Исходники, contracts/profiles, Skills, generated routers и интеграция не исправлялись. Коммит, push, публикация, синхронизация, рестарт сервисов и изменение 3D-ассетов не выполнялись. Автоматические тесты работают с изолированными фикстурами; их строки `PASS SYNC` не означают синхронизацию production-интеграции.

## 2. Зафиксированная база

| Параметр | Наблюдение |
|---|---|
| Корень | `E:/MyCreations/Tools_C` |
| Ветка / HEAD | `main` / `becd57ba0caa05baa8c729bc24c2f19b17052f43` |
| Архитектура / форматы | 4.0.1; manifest/profile/contracts schema 1 |
| Каталог | 28 canonical Skills; 9 legacy aliases |
| Python | `C:/Python314/python.exe`, 3.14.2 |
| Test runner / CI | stdlib unittest; `.github/` в этом checkout отсутствует, новый CI не предполагается |
| Начальное состояние Git | 9 modified, 76 deleted, 4 untracked; staged-изменений нет |
| Интеграция | `E:/MyCreations/Blender-MCP-Co`, HEAD `3b1fed4cb9e956798ba5dab60660d2a3af441682`; dirty |
| Состояние до записи документов | Проверены SHA-256 399 существующих/отсутствующих tracked и исходных untracked путей; изменений от аудита/тестов нет |

Среди исходных modified: `.tooling/contracts.json`, `Project-pulse.md`, `docs/mcp-deployment.md`, `docs/qa-receipt.md`, character workflow gates, vehicle Skill/research, `tools/mcp_runtime.py`, `tools/qa_gate.py`. Исходные untracked: отчёт character flow, `tests/test_workflow_flow.py`, vehicle QA/recipes. Удалённые 76 исторических артефактов не восстанавливались и не включаются в патч.

Это важно: HEAD **не содержит весь текущий baseline**. Новая работа, начатая только от HEAD, потеряет действующие незакоммиченные исправления. Перед реализацией нужна повторная проверка этой базы и отдельный scoped diff; автоматического stash/reset/clean быть не должно.

Полный исходный статус и hashes находятся в `.local/mega-tools-audit-2026-10-16/baseline.json`. Файлы под `.local` игнорируются Git. Переносимая сводка: [машинные доказательства](MEGA_TOOLS_AUDIT_2026-10-16.json).

## 3. Покрытие аудита всей Tools_C

Проверены реальное дерево, AGENTS/Pulse/profile/manifest, все 28 записей Skills и их frontmatter/ссылочная регистрация, девять aliases и оба дерева generated routers, интерфейсы 29 Python-модулей `tools`, основной test runner, contracts/checkers, bootstrap, engine probes и Blender MCP consumer. Проверены exact-ID discovery/read для всех 28 владельцев. Это системный аудит готовности; художественные методики каждого 3D-домена и production-ассеты не проходили новую визуальную приёмку.

| Слой | Владельцы / назначение | Вывод для патча |
|---|---|---|
| Общий процесс | project-audit, verification, contracts-lint | Существующие owners для диагностики, behavioral evidence и обслуживания каталога; новый canonical Skill не нужен |
| Godot | godot-project, godot-asset-integration | Общая работа с проектом отделена от доставки ассета; сохранить это различие |
| Blender pipeline | blender-pipeline | Маршрутизирует specialist procedures; не становится универсальным owner всех задач |
| Персонажи | blender-character-modeling, blender-anime-character-modeling, blender-animal-anthropomorphic-modeling | Сохранить формы/стили/видовую анатомию и отдельные downstream owners |
| Предметные домены | blender-architecture-environment, blender-environment-assets, blender-roads-infrastructure, blender-props, blender-vehicle-modeling, blender-product-electronics-modeling, blender-vegetation | Сохранить границы здания/fixture/дороги/prop/vehicle/device/vegetation; vehicle содержит свежие чужие правки |
| Специализированные стадии | blender-sculpting, blender-posteffects-polishing, blender-rigging-skinning, blender-animation, blender-export-validation | Stage-only запрос не должен запускать повторное моделирование |
| Источник/идентичность | visual-reference-reconstruction, blender-robot-mechanism-modeling, blender-reference-surface-transfer | PASS0/Model Contract и transfer provenance остаются единственными действующими владельцами своих решений |
| Производственный процесс | production-mechanic-gym, production-subagent-worktree, production-lookdev-gate, production-project-state-gates | Использовать существующие state/handoff conventions; тяжёлая оркестрация и второй Pulse не требуются |

Наличие ориентиров из приложения проверено: README, architecture-v4, contracts, foundation, mcp-deployment существуют. `reports/V1.md` отсутствует в рабочем дереве и числится удалённым; `TOOLS_C_V4_MIGRATION_REPORT.md` отсутствует. Они не использовались как актуальная спецификация.

## 4. Точки входа и владельцы изменений

| Вход | Точный участок | Текущая роль / место расширения |
|---|---|---|
| Регистрация | `manifest.json:1`, `.tooling/profile.json:1`, `AGENTS.md:1` | Manifest хранит ID/path/aliases, frontmatter хранит description. Не переносить descriptions во второй редактируемый каталог |
| Валидация | `tools/check.py:173` catalog; `:121` markdown_links; `:309` run | Проверяет schema, names, foundation, registration, ссылки, lessons; не доказывает исполнение Skill |
| Discovery | `tools/skill_catalog.py:7` _records; `:28` listing; `:46` search | Metadata-first результат; внутреннее чтение пока тяжёлое, поиск lexical |
| Полная загрузка | `tools/read_blender_skill.py:39` document_paths; `:81` render | Единый dependency inventory, canonical и legacy reads; Blender-oriented envelope требует осторожности для generic owners |
| Совместимость | `tools/read_blender_skill.py:86` router; `tools/sync_blender.py:12` generate | Generated outputs с проверкой hashes/edited files; ручное редактирование запрещено |
| Intent/context | `tools/mcp_runtime.py:51` action_query; `:155` _route_task; `:225` route_task; `:272` context | Существующий RU/EN routing, stage intent, целые документы, budget/receipts/continuation |
| L1 adapters | `tools/profile_adapters.py:8`, `tools/bootstrap.py:43` | Godot resources и Blender mirror coverage; managed integration без копирования canonical bodies |
| QA / состояние | `tools/qa_gate.py:202`, `:412`; `tools/qa_freshness.py:87`; `tools/qa_artistic.py:162` | Schema-3 usage/gates, freshness, отдельный artistic review. Переиспользовать evidence semantics |
| Контракты ассета | `tools/model_contract.py:77`; `tools/surface_transfer.py:25`; `skills/visual-reference-reconstruction/scripts/validate_pass0.py:41` | Защищаемые независимые форматы; патч не требует их миграции |
| Handoff/engine | `tools/handoff_snapshot.py:21`, `tools/engine_check.py:99` main | Изолированные сравнения/opt-in engine; не общий session parser |
| Deployment | `tools/mcp_deployment.py:55` disk_audit | Диск отдельно от disposable stdio, tunnel и connector |
| Тесты | `tests/test_skill_catalog.py`, `tests/test_v4.py`, `tests/test_workflow_flow.py`, activation JSON, QA/domain tests | unittest — действующий runner; activation JSON уже предупреждают, что integrity не измеряет поведение модели |

В **дополнительном** корне Blender-MCP-Co прочитаны AGENTS, README и `.tooling/profile.json`/`profile.md`. README является доступным датированным статусом; отдельный Pulse не найден. Python consumer: `mcp-server/blender_mcp_server.py:18` root resolution, `:30` helper loading, `:198` list, `:218` read, `:227` find, `:412` context, `:458` deployment. C# entrypoint — `src/BlenderMCPCon/Program.cs`; `SkillStore.cs:84` выполняет read-only mirror verification, а не canonical discovery. Компиляция launcher не входит в этот аудит; причин менять C# для трёх функций сейчас не найдено.

## 5. Матрица трёх направлений

| Возможность | Состояние | Доказательство / граница |
|---|---|---|
| Единый каталог + короткие descriptions | Имеется | 28/28 зарегистрированы; source — canonical frontmatter; listing без procedure bodies |
| Exact ID/legacy alias discovery | Имеется | 28/28 exact-ID search + read; 9/9 legacy render |
| Лёгкий backend discovery | Частично | listing вызывает catalog(), который читает/валидирует весь skill tree; _records вновь читает все entrypoints |
| Description только «когда» | Частично | Например transfer description перечисляет crop/repair/projection/bake; PASS0 — анализ/выбор/lock/views. Нужны точечные правки, не переименование IDs |
| RU/EN intent и неоднозначность | Частично | Существуют regex routing и action_query; baseline ниже показывает пробелы и расхождение search/context |
| Полные документы, hashes, continuation | Имеется | 14 сценариев: нет duplicate SOURCE blocks; нехватка бюджета явно сообщает missing; continuation проверен |
| Выполнение Skill после загрузки | Не доказано выдачей контекста | `mcp_runtime.py:362` возвращает DISCOVERED; READ/EXECUTED не присваиваются автоматически |
| Behavioral test protocol/harness общего назначения | Частично / runner отсутствует | Есть manual activation cases и planned blind-review experiment, но нет общего baseline/with-rule runner/report |
| Реальная контрольная пара с новым правилом | Не выполнено | В этом проходе правила не менялись; наличие codex.exe само по себе не доказывает доступ к дешёвому управляемому эксперименту |
| Session diagnostics CLI/parser | Отсутствует | В актуальных tools нет потребителя session transcripts; bridge/deployment/QA diagnostics решают другие задачи |
| Доступный формат session log | Имеется | Локальный JSONL текущей сессии; прочитаны только envelope shapes, без вывода приватного текста |
| Live MCP identity/catalog | Нельзя проверить сейчас | Обе безопасные connector-команды вернули UNAVAILABLE/HTTP 429; диск отдельно PASS |

### Discovery: измерения и воспроизводимые дефекты

Один инструментированный вызов listing: **13 767 байт** компактного UTF-8 JSON, **287 вызовов read_text**, **103 уникальных пути**, **1 824 068 байт** прочитанного нормализованного UTF-8 текста, включая **112 чтений SKILL.md**. Суммарный размер 28 canonical entrypoints на диске — **240 490 байт**. Время одного вызова — **0,311493 с**. Это один локальный замер, не performance SLA; стоимость/tokens/процент экономии не вычислялись. I/O backend не равно объёму контекста, отправленного модели. Метрики и список чтений сохранены в evidence JSON.

| Запрос | search / route_task | Оценка |
|---|---|---|
| «Смоделировать голову по референсам» | search пуст; route PASS0 → character | Routing есть; natural-language discovery нужно улучшить |
| «Исправить веса плеча, существующие анимации сохранить» | search пуст; route rig + animation | Лишний animation-owner из preservation clause |
| «Создать анимацию на готовом риге, не менять геометрию» | search пуст; route animation | Intent корректен, discovery расходится |
| «Проверить экспорт GLB и импорт в Godot» | verification + export + Godot asset | Нужные owners есть; список не доказывает последовательное исполнение |
| «Анимация выглядит плохо, причина неясна» | pipeline | Нужна консервативная QA/диагностика |
| `Model a human head from reference` | search animal owner; route PASS0 → character | Body fallback способен выбрать чужой purpose |
| `Fix shoulder weights; preserve existing Actions` | search character; route rig | Аналогичное расхождение |
| `blender-animation` | search и route animation | PASS |
| `Blender_Character_Modeling_SKILL` | search character; direct read работает; route pipeline | Alias compatibility чтения сохранена; exact task shortcut неполон |
| `blender-animtion` | 10 общих результатов по blender; route pipeline | Опечатка не должна давать ложную уверенность |
| `Make coffee for lunch` | 10 нерелевантных результатов; pipeline | Нужны unknown/no-match и фильтрация общих слов |

Дополнительно 9/28 bare canonical IDs не возвращают самого себя в route_task: project-audit, godot-project, animal modeling, verification, contracts-lint и четыре production owners. **Это не поломка direct read**: search/read проходят 28/28. Некоторые IDs находятся за пределами исходного Blender-intent интерфейса; A2 должен явно определить границу поддержки, а не объявлять любой такой случай production-регрессией.

Mixed car/barrier context честно возвращает `ok=false`: при бюджете 60 000 символов отсутствует model-contract.md. Повтор с receipts/requested_documents завершает загрузку. Пропуск не скрывается; исправлять это отсечением правил нельзя. Неузнанный roadside barrier в mixed-запросе также входит в будущую collision matrix.

### Behavioral: что уже пригодно

`tests/core_activation_cases.json:2` и `tests/blender_activation_cases.json:2` — существующая база сценариев. `docs/dual-verification-blind-review.md:3` прямо помечен PLANNED/NOT_RUN. QA уже разделяет DISCOVERED/READ/SELECTED/EXECUTED/VERIFIED, техническую и художественную приёмку. Следовательно, нужен небольшой протокол поверх этих механизмов, а не новая система QA или фиктивный LLM через string matching.

### Diagnostics: обнаруженный реальный формат

В локальном JSONL текущей сессии обнаружены session_meta (строка 1), turn_context (8), response_item/custom_tool_call (17), custom_tool_call_output (23), function_call (118), function_call_output (120), token_usage_record (18), event_msg/token_count (24). Эти номера относятся к обследованному префиксу сессии; snapshot схемы сохранён локально в transcript-shape.json. Значения личных сообщений и credentials в отчёт не переносились.

MVP поддерживает только реально обнаруженный Codex JSONL и явный нормализованный fixture-формат. Work/Classic formats — UNKNOWN до появления образца. Wrapper-вызовы functions.exec скрывают часть вложенных действий: текст команды не является доказательством успешного чтения файла, encrypted reasoning не анализируется. Отсутствие события чтения означает «не наблюдалось», если logger не обещает полноту. Token records могут содержать накопительные и повторяющиеся значения: их нельзя слепо суммировать. Кредиты/денежная стоимость пока UNKNOWN.

## 6. Проверки до изменений

Команды выполнялись из Tools_C. Полные результаты — под `.local/mega-tools-audit-2026-10-16/`; ключевые результаты включены в переносимый JSON.

| Команда / проверка | Exit | Результат |
|---|---:|---|
| `python -m unittest discover -s tests -v` | 1 | **337 run, 333 PASS, 4 FAIL, 0 errors, 0 skipped**, 213,136 с |
| `python tools/check.py --self --json` | 1 | **L1 49 PASS / 1 FAIL**, TOOLS-LINKS E_PATH |
| `python tools/check.py --project E:/MyCreations/Blender-MCP-Co --json` | 0 | **L1 9 PASS / 0 WARN / 0 FAIL** |
| `python tools/mcp_deployment.py --project E:/MyCreations/Blender-MCP-Co --output .local/mega-tools-audit-2026-10-16/deployment-disk.json` | 0 | Disk PASS; 17 source tools; оба router tree актуальны |
| Canonical/alias audit probe | 0 | 28 exact search/read, 9 alias reads, context dedup/continuation проверены |
| `git diff --check` | 0 | Ошибок whitespace нет; Git предупреждает об исходном CRLF в двух документах |
| Connector deployment_info + list_skills | — | UNAVAILABLE, HTTP 429; runtime/connector SKIP |
| L2/L3/L4 ассеты / engines | — | SKIP: системный аудит, production-сцены не затрагивались |

Четыре исходных падения:

1. `test_anime.AnimeContractsTest.test_valid_self_profile_with_replaceable_art_choices_passes`.
2. `test_domain_contracts.DomainContractsTest.test_json_subset_warn_stays_advisory_and_scalar_types_are_exact`.
3. `test_domain_contracts.DomainContractsTest.test_legacy_migration_provenance_is_not_a_current_content_lock`.
4. `test_domain_contracts.DomainContractsTest.test_valid_pack_and_additive_project_choices_pass_without_mutation`.

**Причина подтверждена контролем одной переменной:** две Markdown-ссылки на `C:/Users/...` в исходном `Project-pulse.md:10` и `:12` нарушают `tools/check.py:137`. Только in-memory представление этих ссылок как code paths даёт L1 **50/0/0** и **4/4 PASS** тех же тестов. Репозиторий при этом не исправлялся. Это диагностический эксперимент, а не новый green baseline. Логи: absolute-link-control.json/.log. После добавления audit-записи номера строк Pulse сдвинутся; машинный baseline хранит исходную версию.

Дополнительный drift: `docs/architecture-v4.md:3` говорит о 25 Skills вместо фактических 28. README/Pulse/catalog уже содержат 28. В Blender profile/README остаются исторические «eight aliases» вместо девяти; runtime catalog и L1 coverage проверены отдельно. Эти расхождения надо исправлять точечно, не переписывая архитектуру.

## 7. Приоритеты и минимальная архитектура патча

| ID находки | Приоритет | Наблюдение | Действие |
|---|---|---|---|
| AUD-01 | P1 | Исходный self L1 и 4 tests FAIL из-за Pulse links | A1: восстановить green baseline без ослабления path checker |
| AUD-02 | P1 | Search/intent расходятся, preservation добавляет owner, unclear/unknown обрабатываются слабо | A2, A4–A6: контракт, explicit resolution, узкие RU/EN triggers и conservative fallback |
| AUD-03 | P2 | Metadata-only ответ требует полного повторного обхода canonical bodies | A3: lightweight path с измерением reads/bytes; полную валидацию сохранить отдельным обязательным gate |
| AUD-04 | P1 | Общий behavioral протокол/runner и session analyzer отсутствуют | A8–A12: малые stdlib инструменты и evidence formats |
| AUD-05 | P2 | Архитектурные counts и отдельные compatibility descriptions устарели/пересказывают процесс | A14: targeted docs/descriptions, по фактическим результатам |
| AUD-06 | WARN | Live connector 429; SDK отсутствует в default Python | A15/A16: отдельные smoke-проверки без restart; при отсутствии доступа честный SKIP |

Предлагаемая цепочка: **canonical manifest IDs/paths + canonical frontmatter → лёгкий discovery → explicit ID/alias / узкий intent → выбранный owner → целые supporting documents и receipts → выполнение агентом → evidence/QA**. Search relevance и action authorization остаются разными решениями; search result не даёт права редактировать ассет.

Description хранится в одном месте. Дополнительные synonyms вводятся только при доказанной необходимости и с явным единственным владельцем; никакой ручной второй таблицы поверх manifest. Возможный cache/index — только производный, с проверяемой invalidation; размер/mtime не являются доказательством неизменности содержимого. ID/legacy semantics, schema 1 и QA/PASS0/transfer formats сохраняются. Новые утилиты не зависят от облака/embeddings и ничего не публикуют.

Existing owners: project-audit — intake и разбор сессии; verification — behavioral evidence и границы достоверности; contracts-lint — изменения метаданных/правил и их автоматические тесты. Pulse — проектное состояние; [план](../tasks/plan.md) — решения/порядок; [checklist](../tasks/todo.md) — состояние задач A. Отдельный общий Task Ledger сейчас не обоснован. Патч B сможет использовать стабильные IDs, receipts и read-only diagnostics reports, но его функций пока нет в плане A.

## 8. Внешний образец

Проверены README, writing skill, bootstrap skill, diagnostics skill и MIT license внешнего [репозитория-образца](https://github.com/obra/superpowers/tree/bb92a77741419a4ab5f06e711a283343f1ada0c3), snapshot commit `bb92a77741419a4ab5f06e711a283343f1ada0c3` (2026-10-10), получен 2026-10-16. Локальные source notes остаются в ignored evidence; ничего не устанавливалось.

Из writing-подхода полезны реальная baseline/with-rule пара, pressure cases и description как условие выбора. Из diagnostics — обязательные точные ссылки и измерения из лога. Автоматические широкие вызовы Skills и обязательные многочисленные аналитики не переносятся. Дословный код/правила в Tools_C не копировались; MIT attribution понадобится только при будущем буквальном заимствовании. URL исходного проекта остаётся неизменным для проверяемости источника; наше название — Mega tools.

## 9. Gates G1–G8: текущий baseline, не приёмка будущего патча

| Gate | Статус | Доказательство / что остаётся |
|---|---|---|
| G1 | PASS | Один manifest/frontmatter source, 28 owners/9 compatibility aliases, router disk audit PASS |
| G2 | WARN | Metadata-first ответ есть; RU/EN search, descriptions и conservative fallback требуют доработки |
| G3 | PASS | Текущие exact search/read 28/28, aliases 9/9, integration L1 9/0/0; bare-ID context ограничения перечислены отдельно |
| G4 | WARN | Offline/manual граница уже описана, общего behavioral harness ещё нет |
| G5 | SKIP | Новое правило и контрольная agent-пара в audit-only проходе не запускались |
| G6 | SKIP | Parser/finding/redaction tests ещё не реализованы; подтверждён только реальный envelope format |
| G7 | FAIL | Исходные 4 tests и L1 FAIL; это ещё до нового кода, source bytes сохранены |
| G8 | PASS | Audit/план/Pulse сохраняют честные границы; production-ассеты/сервисы не изменены |

## 10. Результат и следующая работа

**Готово:** системный аудит, baseline, карта точек входа, воспроизведение пробелов, изоляция причины FAIL, план A1–A17. **Не реализовано:** сам патч Mega tools, model A/B trial, session diagnostics CLI. Для начала реализации первым идёт A1, затем контракт A2 и лёгкий каталог A3. Полный порядок, критерии и проверки находятся в [плане разработки](../tasks/plan.md).

Новые файлы аудита: этот отчёт, одноимённый JSON, `tasks/plan.md`, `tasks/todo.md`; в Pulse добавлена только датированная запись и обновлена дата. Исходные чужие modified/deleted/untracked остаются за пределами нашего diff. Финальные SHA/status результаты фиксируются в JSON после записи документов.
