# Mega tools — план разработки первого патча

Дата: 2026-10-16. Статус: **A1–A17 выполнены технически; behavioral G5 SKIP**. Подготовительный аудит завершён: [отчёт](../reports/MEGA_TOOLS_AUDIT_2026-10-16.md), [evidence](../reports/MEGA_TOOLS_AUDIT_2026-10-16.json). [A1 проверен](../reports/MEGA_TOOLS_A1_2026-10-16.md). Задачи отслеживаются только в [todo.md](todo.md); этот документ содержит их спецификацию.

## Результат реализации A2–A17

Выполнено 2026-10-16: 367/367 regressions PASS; self/integration L1 50/9 PASS;
17 source tools и реальные MCP search/context/hash/sequence checks подтверждены.
[Итоговый отчёт](../reports/MEGA_TOOLS_IMPLEMENTATION_2026-10-16.md) разделяет
technical implementation и незавершённую model-валидацию. A16 выполнен в части
bounded attempts/manual protocol: оба реальных дочерних harness read заблокированы
execution policy, поэтому G5 SKIP, улучшение поведения не заявляется.
Ниже сохранены исходные спецификации задач; фактический статус — в todo/Pulse.

## Цель и инварианты

Улучшить существующие discovery/context, добавить маленький optional behavioral protocol и read-only session diagnostics. Использовать существующих owners project-audit / verification / contracts-lint. Новый canonical Skill, второй каталог или общий Ledger не требуются.

Сохранить 28 IDs, 9 aliases и их существующую семантику read, profile/contract schema 1, canonical authority, hashes/whole-document delivery, QA/PASS0/Model Contract/transfer formats. Search relevance не равно разрешению операции. Сохранить различия DISCOVERED → READ → SELECTED → EXECUTED → VERIFIED и L1–L4. Ни одна утилита не должна присваивать visual/behavioral PASS только по строковым совпадениям.

Основа реализации — HEAD `becd57b` **плюс зафиксированный dirty baseline**, не чистый checkout от HEAD. Повторить status/hashes перед работой. Наши документы не дают разрешения перезаписывать чужие правки, рестартовать MCP, изменять credentials/production-сцены или публиковать. Коммиты — только при авторизации и с явным allowlist. После A17 остановиться; второй патч автоматически не начинать.

## Порядок и зависимости

```text
A1 → A2 → A3 → checkpoint 1
A2+A3 → A4 → A5 → A6 → checkpoint 2
A6 → A7 → A8 → A9 → checkpoint 3
A2 → A10 → A11 → A12 → checkpoint 4
A5 → A13
A7+A9+A12+A13 → A14 → A15 → A16 → A17 → итоговая приёмка
```

Выполнение по умолчанию последовательное. Наличие независимых узлов не является запросом на запуск субагентов. Каждая задача должна оставлять работоспособный bounded slice. Checkpoint — запись проверок и reviewable diff; он не требует нового подтверждения каждой стадии после авторизации реализации.

Оценка S = 1–2, M = 3–5 предполагаемых файлов. Новые CLI ниже **предлагаются**, сейчас в checkout они отсутствуют. Точные flags закрепляются в A2/A8 до реализации и документируются только после появления интерфейса.

## A1 — восстановить проверяемый исходный baseline

**DONE, 2026-10-16:** по прямому запросу пользователя старый Pulse сохранён побайтно в ZIP, создан новый активный Pulse. Исторические ссылки остались в архиве; checker не ослаблялся. Self L1 50/0/0, четыре исходных теста PASS, полный dirty-tree suite 337/337; отдельный HEAD + 8-path candidate suite 325/325. Архив/hash/scope: [отчёт A1](../reports/MEGA_TOOLS_A1_2026-10-16.md). Коммит и staging не выполнялись. Следующая задача — A2.

**Результат:** исправить две несовместимые абсолютные Markdown-ссылки Pulse без ослабления проверки containment и сохранения смысла исторических записей. Использовать текстовые paths либо существующую переносимую ссылку; не перемещать исходные артефакты ради green.

**Приёмка:** self L1 50/0/0; четыре исходных падавших теста PASS; unrelated dirty hashes не изменены.

**Проверка:** `python tools/check.py --self --json`; затем `python -m unittest discover -s tests -v` — чистая новая база 337/337 либо честный отчёт о другом выявленном baseline-дефекте. Диагностический in-memory контроль аудита не подменяет этот запуск.

**Зависимости:** нет. **Файлы:** `Project-pulse.md`; evidence этого этапа. **Размер:** S.

## A2 — закрепить наблюдаемый контракт трёх функций

**Результат:** таблица требований → scenarios → observable checkpoints → gate; определить границы global catalog и Blender-intent context. Зафиксировать metadata source, exact-ID/alias priority, unknown/ambiguous поведение и отсутствие новой edit authority.

**Приёмка:** все требования приложения покрыты сценарием/обоснованным SKIP; baseline/with-rule отличаются только выбранным правилом при сохранении остального harness; нормализованный finding содержит observed/expected/evidence/effect/limits/remediation.

**Проверка:** валидировать scenario JSON; сопоставить каждый G1–G8 с задачей и evidence. Включить все 14 audit cases и все canonical IDs/aliases без подмены search проверкой route_task.

**Зависимости:** A1. **Файлы:** `docs/mega-tools.md` (новый); `tests/skill_behavior_cases.json` (новый, с reuse существующих activation IDs); `tests/test_skill_behavior.py` (новый). **Размер:** M.

## A3 — сделать discovery лёгким внутри существующего каталога

**Результат:** отделить bounded metadata access от полной structural/link validation, не теряя строгую валидацию в self-check/tests. ID/path — manifest, description — canonical frontmatter; производные данные не редактируются как источник.

**Приёмка:** listing не перечитывает все canonical bodies/references; stale metadata после изменения description не выдаётся; malformed/duplicate/path-escape случаи fail closed.

**Проверка:** `python -m unittest discover -s tests -p test_skill_catalog.py -v`; instrument reads/UTF-8 bytes до/после тем же probe. Сохранить cold/warm условия; не обещать процент ускорения заранее. Проверить same-size/same-mtime изменение либо явно описать границу cache freshness и отказ от такого cache.

**Зависимости:** A2. **Файлы:** `tools/skill_catalog.py`, `tools/check.py` при необходимости выделения существующей validation-функции, `tests/test_skill_catalog.py`. **Размер:** M.

### Checkpoint 1

Baseline green; metadata owner единственный; malformed/path negative cases и замеры сохранены. Приёмка не зависит от модели или Blender.

## A4 — согласовать explicit IDs и legacy aliases

**Результат:** единый explicit resolver из текущего manifest. Сохранить direct read и исторический multi-stage alias; не ломать scoped/read-only guards в предложениях по task intent.

**Приёмка:** 28 exact IDs и 9 aliases доступны; неподдержанные generic context случаи имеют явный контракт A2, без тихого Blender fallback; schema/input compatibility сохранена.

**Проверка:** table-driven explicit ID/alias tests, canonical read/context hashes, unknown ID negative test; `python -m unittest discover -s tests -p test_v4.py -v` и focused catalog tests.

**Зависимости:** A2, A3. **Файлы:** `tools/skill_catalog.py`, `tools/mcp_runtime.py`, `tools/read_blender_skill.py` только при обоснованной необходимости, `tests/test_skill_catalog.py`, `tests/test_v4.py`. **Размер:** M.

## A5 — улучшить purpose search RU/EN

**Результат:** узкое ранжирование по применимости с synonyms, общими словами, опечаткой и честной неоднозначностью. Переиспользовать authoritative metadata, не создавать ручную дублирующую trigger-библиотеку.

**Приёмка:** natural-language head/weights/animation discovery находит подходящих owners; unrelated coffee и typo не дают уверенного нерелевантного owner; длинный body с чужими словами не выигрывает у purpose.

**Проверка:** baseline/after routing-search matrix с RU/EN, typo, ID, alias, mixed, unknown; focused catalog tests и measurements. Если fuzzy suggestion используется, он явно suggestion, без auto-execution.

**Зависимости:** A4. **Файлы:** `tools/skill_catalog.py`, `tests/test_skill_catalog.py`, scenario JSON; canonical metadata только для доказанно нужных synonyms, по малым отдельным slices. **Размер:** M.

## A6 — исправить intent/scope и консервативную диагностику

**Результат:** исправить preservation clause «анимации сохранить», unclear animation, unknown fallback и mixed domain collisions. Сохранить действующие read-only/RU flow fixes и узких stage owners.

**Приёмка:** weight repair не добавляет animation authoring; unclear defect идёт к QA без edit authorization; reference head, ready-rig animation, export→Godot и mixed запросы имеют ожидаемые bounded routes.

**Проверка:** `python -m unittest discover -s tests -p test_workflow_flow.py -v`; `python -m unittest discover -s tests -p test_form_tools.py -v`; smoke текущих domain routing fixtures. Отдельно проверить negation/preservation/explicit ID collisions.

**Зависимости:** A4, A5. **Файлы:** `tools/mcp_runtime.py`, `tests/test_workflow_flow.py`, `tests/test_form_tools.py`, scenario JSON. **Размер:** M.

### Checkpoint 2

Полная discovery matrix проходит. Search, context delivery и факт выполнения показываются отдельно. Чужие workflow changes не потеряны.

## A7 — сохранить адресную, поэтапную выдачу контекста

**Результат:** уточнить current owner/deferred downstream recommendations без загрузки всех будущих стадий. Исправлять бюджет только уменьшением ненужной загрузки или continuation; обязательные gate documents не обрезать.

**Приёмка:** whole-document delivery и dedup сохранены; changed description/body/receipt правильно инвалидируются; mixed context продолжает missing documents с retained receipts, а после compaction receipts сбрасываются.

**Проверка:** focused `test_v4.py`, `test_character_workflow.py`, `test_workflow_flow.py`; tiny/default/large budget, stale hash и context-loss cases. Не добавлять execution orchestrator или жёсткую блокировку произвольного Blender Python.

**Зависимости:** A6. **Файлы:** `tools/mcp_runtime.py`, `tools/read_blender_skill.py`, до трёх соответствующих test modules. **Размер:** M.

## A8 — оформить behavioral protocol поверх существующей Verification

**Результат:** маленький reusable protocol: baseline без нового правила → with-rule → минимум два pressure cases → repeats → report. Использовать существующие activation cases/QA usage vocabulary.

**Приёмка:** сценарий указывает hashes/environment/budget/observables; fixture/offline PASS невозможно выдать за behavioral PASS; отсутствующие visual/model данные дают SKIP/UNKNOWN.

**Проверка:** schema/negative tests нового scenario/report format. Pressure cases: требование VISUAL PASS по неоткрытому PNG; попытка нарушить Action preservation; дополнительно face/detail ordering на безопасном prepared evidence.

**Зависимости:** A2, A7. **Файлы:** `skills/verification/references/behavioral-tests.md` (новый), `tests/skill_behavior_cases.json`, `tests/test_skill_behavior.py`. **Размер:** M.

## A9 — добавить optional evidence runner/manual adapter

**Результат:** предлагаемый stdlib `tools/skill_behavior.py` готовит/проверяет trial manifests и принимает фактические evidence из доступного harness. Default offline режим не запускает модели, Blender или платные API.

**Приёмка:** baseline/with-rule условия сравнимы; source read/action evidence различаются; unavailable real harness даёт исполнимый manual protocol и SKIP с причиной. Повторы не усредняются в выдуманную статистическую гарантию.

**Проверка:** valid trial, missing read evidence, differing model/budget, altered hashes, partial transcript, offline-only results. `python -m unittest discover -s tests -p test_skill_behavior.py -v`.

**Зависимости:** A8. **Файлы:** `tools/skill_behavior.py` (новый), `tests/test_skill_behavior.py`, Verification supporting reference. **Размер:** M.

### Checkpoint 3

Delivery tests green; behavioral protocol воспроизводим; наличие runner не объявляется успешным model experiment. Контрольная пара будет проверена в A16.

## A10 — читать обнаруженный session JSONL безопасно

**Результат:** предлагаемый `tools/session_diagnostics.py` принимает явно выбранный transcript; streaming decoder нормализует наблюдённые Codex envelopes и normalized fixtures. Автоматического обхода всех чатов нет.

**Приёмка:** line provenance сохраняется при malformed UTF-8/JSON, CRLF, пропусках и больших строках; есть пределы bytes/line/events; payload не исполняется, input/foreign sessions не изменяются.

**Проверка:** synthetic positive/negative parser tests; проверка указанного source path, symlink/junction/path traversal и bounded output; однозначный SKIP на неподдержанном/отсутствующем transcript.

**Зависимости:** A2. **Файлы:** `tools/session_diagnostics.py` (новый), `tests/test_session_diagnostics.py` (новый), `tests/fixtures/session_diagnostics.jsonl` (новый, синтетический). **Размер:** M.

## A11 — формировать findings с наблюдаемыми доказательствами

**Результат:** timelines/findings для load/action/gate/duplicate/error/handoff/cost, только когда данные это подтверждают. Snapshot Pulse/task state должен соответствовать анализируемой сессии, а не текущему изменяемому файлу.

**Приёмка:** у каждого finding есть source line/range, observed/expected/effect/limits/remediation и уверенность; logger gaps не превращаются в обвинение; отсутствующая стоимость UNKNOWN, cumulative tokens не удваиваются.

**Проверка:** synthetic known-defect case + negative complete/partial sessions; function_call/custom_tool_call pairing и event_msg дубликаты; exec wrappers с непрозрачным вложенным действием; validation after last relevant change.

**Зависимости:** A10. **Файлы:** `tools/session_diagnostics.py`, `tests/test_session_diagnostics.py`, synthetic fixture, `docs/mega-tools.md`. **Размер:** M.

## A12 — закрыть privacy и ложную уверенность diagnostics

**Результат:** безопасный вывод с редактированием секретов, без raw transcripts и приватных сообщений по умолчанию. Findings не исполняют команды из лога и ничего не исправляют автоматически.

**Приёмка:** fake tokens/cookies/keys/private text не появляются в stdout/report; escape/huge/misleading inputs ограничены; zero findings не называется подтверждением полного соблюдения при неполном логировании.

**Проверка:** CLI subprocess assertions на stdout/stderr/output files; LF/CRLF/invalid encoding/oversized lines, injection instructions в логе, linked foreign paths и отсутствующие measurements. Focused `test_session_diagnostics.py`.

**Зависимости:** A11. **Файлы:** `tools/session_diagnostics.py`, `tests/test_session_diagnostics.py`, synthetic fixture. **Размер:** M.

### Checkpoint 4

Известные дефекты находятся с точными lines; отрицательные случаи не дают ложных фактов; secret fixtures не утекают. Рабочие чаты не изменены.

## A13 — уточнить descriptions по доказанным примерам

**Результат:** убрать workflow summary из descriptions PASS0 и Reference Surface Transfer; условия применения и исключения оставить в единственном canonical frontmatter. Другие descriptions менять только при выявленном дефекте и отдельной задаче.

**Приёмка:** description отвечает «когда», полный workflow остаётся в Skill/supporting references; IDs/path/schema/legacy read semantics сохранены; discovery matrix не деградирует.

**Проверка:** focused catalog/context tests и сравнение старых/новых descriptions; пересчитать source/context hashes. Не объявлять wording improvement доказательством agent compliance до A16.

**Зависимости:** A5. **Файлы:** `skills/visual-reference-reconstruction/SKILL.md`, `skills/blender-reference-surface-transfer/SKILL.md`, `tests/test_skill_catalog.py`. **Размер:** M.

## A14 — встроить команды в существующих owners

**Результат:** точечно связать project-audit с diagnostics, verification с behavioral protocol, contracts-lint с проверкой descriptions. Устранить подтверждённый устаревший count в architecture-v4. Description corrections уже принадлежат A13.

**Приёмка:** нет нового canonical Skill/второй authority; docs ссылаются на реализованные flags; descriptions отвечают «когда», supporting workflow остаётся полным.

**Проверка:** self L1, catalog registration/link tests, manual diff/readback. Расширение за пределы этих пяти файлов требует отдельной явно пронумерованной задачи.

**Зависимости:** A7, A9, A12, A13. **Файлы:** три существующих owning SKILL.md, `docs/architecture-v4.md`, `docs/mega-tools.md`. **Размер:** M.

## A15 — проверить compatibility и deployment boundaries

**Результат:** сначала disposable fixture regeneration/stdio; затем при необходимости regenerated outputs обоих Blender router trees через canonical sync. Повторно прочитать дополнительный root status/profile перед любой записью.

**Приёмка:** имена/семантика legacy aliases, canonical reads, прежние публичные MCP names/input schemas сохранены; edited routers fail before writes; disk/stdio/loaded process/connector имеют отдельные verdicts.

**Проверка:** `python tools/check.py --project E:/MyCreations/Blender-MCP-Co --json`; `python tools/mcp_deployment.py --project E:/MyCreations/Blender-MCP-Co`; optional disposable `--stdio --python PATH` только в среде с MCP SDK. Live read-only smoke без restart; 429/unavailable не превращать в runtime PASS.

**Зависимости:** A14. **Файлы:** generated outputs только при доказанной необходимости; `tools/sync_blender.py`/`tools/profile_adapters.py`/adapter source только если тесты выявят требуемую совместимую правку. **Размер:** S/M логики; generated outputs учтены отдельно.

## A16 — провести небольшую демонстрацию

**Результат:** baseline/after discovery matrix с bytes/reads; synthetic transcript → ожидаемые findings; реальная baseline/with-rule agent-пара и минимум два pressure cases, если доступен безопасный недорогой harness.

**Приёмка:** версии/hash/settings и доступный trace сохранены; реальные agent results отделены от offline; недоступный/неуправляемый harness даёт честный SKIP и готовые команды/manual steps, а не эмуляцию. Метрики стоимости только фактические.

**Проверка:** trial manifests проходят A9; diagnostics fixtures проходят A12; ручная проверка cited evidence и отсутствия private payload. Для визуальных правил применять существующие snapshots/receipts/critic, без изменения production-ассетов.

**Зависимости:** A9, A12, A15. **Файлы:** scoped reports/evidence, scenario JSON только при коррекции воспроизводимого кейса. **Размер:** S/M.

## A17 — финальная регрессия, отчёт и передача

**Результат:** отчёт «было/изменено/добавлено/не выполнено», G1–G8, source attribution, final status/hash preservation и текущий Pulse. Описать реальные публичные команды.

**Приёмка:** ранее green тесты не деградировали; unrelated files и все production data сохранены; L2–L4 и unavailable live проверки имеют честные SKIP; нет незапрошенного push/release или начала B.

**Проверка:** `python -m unittest discover -s tests -v`; self/integration L1; `git diff --check`; allowlist/diff/hash review; G1–G8 evidence review. Повторять полный suite только после реальных изменений/обнаруженного риска, не ради счётчика.

**Зависимости:** A16. **Файлы:** финальный scoped отчёт, `README.md`, `Project-pulse.md`, `tasks/todo.md`. **Размер:** M документации, проверки всего затронутого кода.

## Второй патч: B1, B2, B3…

Зарезервирован отдельный namespace **B**. Документ B получен и прочитан только для пересечений. Его реализации/детального backlog пользователь сейчас не запрашивал; convergence/traceability/cross-artifact/Ledger/impact остаются за пределами A. После A17 зафиксировать accepted/open interfaces и новый baseline; новый документ B должен ссылаться на этот результат и сохранять открытые проверки. Текущие задачи A не переименовывать и не перенумеровывать задним числом.

## Риски и границы

| Риск | Мера |
|---|---|
| Грязный baseline теряется при старте от HEAD | Повтор status/hash, scoped diff/checkpoint; preserve unrelated bytes |
| Новый индекс становится вторым source of truth | Только manifest + canonical frontmatter; производный cache с invalidation |
| Regex «исправляет» задачу вместо диагностики | Read-only/negation/unknown/ambiguity negative cases и conservative routing |
| Budget скрывает обязательный gate | Whole documents, missing/continuation/receipts, explicit context-loss tests |
| Offline tests объявляются доказательством поведения | Separate offline/agent/visual verdicts и raw observed checkpoints |
| Logs неполны или содержат инструкции/секреты | Bounded parsing, explicit coverage, no execution, minimal redacted evidence |
| Runtime отличается от диска, connector 429 | Раздельные disk/stdio/live/connector gates без автоматического restart |
| Второй патч заставит переделывать схемы | Малые additive interfaces; B определяется только после получения задания |
