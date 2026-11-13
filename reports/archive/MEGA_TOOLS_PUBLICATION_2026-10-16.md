# Mega tools A — публикация и передача к B

Дата: 2026-10-16. Пользователь явно разрешил commit/push и подготовку B.
Пользователь лично подтвердил визуальное улучшение обычного чата после A.
Это актуальное решение для завершения A; независимые замечания о точном
сходстве и непроверенный контролируемый эффект G5 сохранены в истории.
Новые модельные/генеративные эксперименты для этой передачи не требуются.

## Ветка и состав

Tools_C baseline `becd57ba0caa05baa8c729bc24c2f19b17052f43`, ветка публикации
`codex/mega-tools-a`. После fetch локальная main и origin/main расходились
(11 local / 5 remote commits: исторические squash-релизы). Публикация идёт
отдельной веткой без force, merge или перезаписи main. Реализация B не входит.

Состав будущего A commit: **36 явно перечисленных файлов**. Это A1 archive/audit,
A implementation/docs/tests и evidence ручных проверок; никакие модельные
рендеры, .blend или raw session transcripts не добавляются.

Смешанные файлы рассмотрены отдельно:
- `.tooling/contracts.json`: в индекс идёт A schema-preserving required-path
  delta; прежняя строка `tests/test_workflow_flow.py` остаётся только в worktree.
- `tools/mcp_runtime.py`: текущие routing/dependency corrections рассмотрены
  целиком. Предшествующие A human-form RU/EN recognition, conservative review
  routing и единый dependency inventory необходимы для закреплённых A cases;
  они включены как явно проверенные зависимости A, а не скрытый общий checkpoint.
- `docs/mcp-deployment.md`: default 60000 соответствует реальной существующей
  сигнатуре context и исправляет устаревшее описание 50000.

Character workflow/QA edits и их tests, vehicle Skills/research/recipes/QA,
76 прежних удалений исторических reports и остальные unrelated paths исключены.
Файлы worktree не перезаписывались ради формирования индекса. HEAD-версии
исключённых файлов, включая локально удалённые reports, остаются в коммите.

## Проверки точного кандидата

HEAD export + allowlisted A contents, без unrelated files/hunks:
- `python -m unittest discover -s tests -v`: **355 tests, 0 failures/errors/skips**,
  228.208 s unittest time, exit 0.
- `python tools/check.py --self --json`: **50 PASS / 0 WARN / 0 FAIL** L1.
- Integration L1: **9 PASS / 0 WARN / 0 FAIL**.

Ранее 367/367 относится к полному рабочему дереву; дополнительные 12 tests —
незакоммиченный `test_workflow_flow.py`. Они не «удалены ради green», а остаются
за пределами A вместе со своей прежней работой. Полная проверка кандидата
потребовалась именно для исключения зависимости A от этого dirty state.
После suite меняются только status/evidence docs, с повторным link/L1/diff review.
Подробные logs и before-byte maps сохранены локально в
`.local/mega-tools-publication-2026-10-16/`.

## Blender-MCP-Co

Только 20 generated routers/manifests, созданных ранее canonical sync, сохранены
коммитом `317a9690fc77c023cb3008f3e92c82930c7320d7` в `codex/mega-tools-a`.
User-owned server, launcher, profiles, binaries и untracked backups не включены.
Фактический `git push --set-upstream origin codex/mega-tools-a` завершился exit 128:
GitHub `Repository not found` для настроенного ConstantineJJ/Blender-MCP-Co.
Поэтому **router commit local-only**; удалённая публикация не заявляется.
Remote/config/credentials не заменялись. Runtime не рестартовал.

## Фактическая публикация и B preparation

Tools_C A commit: `be926e45be927b61f0acc446898fe56f660af852`.
`git push --set-upstream origin codex/mega-tools-a` завершился exit 0;
`git ls-remote origin refs/heads/codex/mega-tools-a` вернул тот же SHA.
Это публикация topic branch, не release/tag и не merge в main.

Следующий documentation-only checkpoint подготавливает B1–B10 в существующих
`tasks/plan.md` и `tasks/todo.md`, обновляет Pulse и этот отчёт. Scope — ровно эти
четыре Markdown-файла. Runtime, schemas, Skills, test logic и assets не меняются.
R0 OPEN; реализация B NOT_STARTED. Предварительно проверена доступность пяти
исходных файлов Spec Kit на commit `f6e72bc8523de8ec8368129cbdea78d45f27cef8`;
полный source/architecture review остаётся B1. Код внешнего проекта не копировался.

Полезный start baseline B — A commit выше плюс documentation preparation
checkpoint; текущий hash получать из Git, а не из старых отчётов. Все оставшиеся
dirty/untracked изменения перечисляются/хэшируются заново перед B1.

## Явный allowlist A

```text
.tooling/contracts.json
Project-pulse.md
README.md
docs/architecture-v4.md
docs/mcp-deployment.md
docs/mega-tools.md
reports/MEGA_TOOLS_A1_2026-10-16.json
reports/MEGA_TOOLS_A1_2026-10-16.md
reports/MEGA_TOOLS_AUDIT_2026-10-16.json
reports/MEGA_TOOLS_AUDIT_2026-10-16.md
reports/MEGA_TOOLS_IMPLEMENTATION_2026-10-16.json
reports/MEGA_TOOLS_IMPLEMENTATION_2026-10-16.md
reports/MEGA_TOOLS_MANUAL_REVIEW_2026-10-16.md
reports/MEGA_TOOLS_PUBLICATION_2026-10-16.md
reports/MEGA_TOOLS_VEHICLE_REVIEW_2026-10-16.json
reports/MEGA_TOOLS_VEHICLE_REVIEW_2026-10-16.md
reports/archive/Project-pulse_2026-10-16_before-A1.zip
skills/blender-reference-surface-transfer/SKILL.md
skills/contracts-lint/SKILL.md
skills/project-audit/SKILL.md
skills/verification/SKILL.md
skills/verification/references/behavioral-tests.md
skills/visual-reference-reconstruction/SKILL.md
tasks/plan.md
tasks/todo.md
tests/fixtures/session_diagnostics.jsonl
tests/skill_behavior_cases.json
tests/test_session_diagnostics.py
tests/test_skill_behavior.py
tests/test_skill_catalog.py
tools/check.py
tools/mcp_runtime.py
tools/read_blender_skill.py
tools/session_diagnostics.py
tools/skill_behavior.py
tools/skill_catalog.py
```

[Implementation](MEGA_TOOLS_IMPLEMENTATION_2026-10-16.md) ·
[Vehicle observations and user decision](MEGA_TOOLS_VEHICLE_REVIEW_2026-10-16.md) ·
[Plan](../tasks/plan.md)
