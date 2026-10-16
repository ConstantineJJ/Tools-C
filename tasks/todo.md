# Mega tools — задачи первого патча

Подготовительный аудит завершён 2026-10-16. **A1–A17 выполнены технически; G5 behavioral SKIP.** Спецификация задач, проверки, dependencies и размер — в [плане](plan.md). Состояние проекта остаётся в [Pulse](../Project-pulse.md).

- [x] A1 — Восстановить исходный green baseline без ослабления checker. Проверено: self L1 50/0/0, focused 4/4, working tree 337/337, изолированный кандидат 325/325; Pulse архивирован и заменён новым. [Отчёт](../reports/MEGA_TOOLS_A1_2026-10-16.md).
- [x] A2 — Закрепить контракты discovery, behavioral evidence и diagnostics.
- [x] A3 — Облегчить внутреннее чтение metadata.
- [x] Checkpoint 1 — baseline, single source, negative checks, bytes/reads.
- [x] A4 — Согласовать explicit canonical IDs и legacy aliases.
- [x] A5 — Проверить purpose search RU/EN, typo, unknown и collisions.
- [x] A6 — Исправить preservation intent и conservative QA routing.
- [x] Checkpoint 2 — discovery matrix, compatibility, scope preserved.
- [x] A7 — Проверить staged/whole-document context и continuation.
- [x] A8 — Оформить reusable behavioral protocol.
- [x] A9 — Добавить optional evidence runner/manual adapter.
- [x] Checkpoint 3 — offline/real-agent/visual outcomes разделены.
- [x] A10 — Добавить bounded reader обнаруженного session JSONL.
- [x] A11 — Формировать findings с точными source lines и limits.
- [x] A12 — Проверить redaction, malformed inputs и false-confidence cases.
- [x] Checkpoint 4 — diagnostics evidence и privacy tests проходят.
- [x] A13 — Уточнить descriptions PASS0 и Surface Transfer.
- [x] A14 — Интегрировать команды в существующих owners/docs.
- [x] A15 — Проверить generated routers и deployment boundaries.
- [x] A16 — Discovery/diagnostics PASS; два реальных agent attempts выполнены, но fixture reads заблокированы policy → behavioral SKIP; manual protocol готов.
- [x] A17 — Полная регрессия, отчёт G1–G8, Pulse и scope review.

Пользователь подтвердил визуальное улучшение обычного чата после A и разрешил
commit/push A, подготовку B. Controlled causal G5 остаётся SKIP; дополнительный
расход модельной квоты для этой передачи не требуется.

[Результаты и границы](../reports/MEGA_TOOLS_IMPLEMENTATION_2026-10-16.md): working tree
367 tests PASS; отдельно проверенный A publication candidate — **355 tests PASS**,
L1 50/9 PASS. [Scope публикации](../reports/MEGA_TOOLS_PUBLICATION_2026-10-16.md).

## Патч B — поэтапная реализация

Детальные критерии/owners/dependencies — в [плане](plan.md).
[Ревью R0](../reports/PATCH_B_R0_2026-10-16.md) завершено. B2/B3 реализованы;
[отчёт](../reports/PATCH_B_B2_B3_2026-10-16.md): full regression 385 PASS, 18 новых
focused tests PASS, self/integration L1 50/9 PASS. B4/B5 implementation завершена;
[новый отчёт](../reports/PATCH_B_B4_B5_2026-10-16.md), 39 focused tests PASS,
checkpoint B-II PASS: full 406, L1 50/9; 421 outside-scope paths preserved.
B6 boundary review и B7 DONE: focused 60, full 427, L1 50/9 PASS; [B-III отчёт](../reports/PATCH_B_B6_B7_2026-10-16.md), checkpoint B-III PASS, 425 outside-scope paths preserved. B8+ остаются открытыми.

- [x] B1 — Актуальный audit, 9 external source files, owners/options review и Gate R0 PASS по пяти функциям. Свежие L1 50/9, Model Contract 28 и freshness 17 tests PASS.
- [x] B2 — Optional bounded review packet v1, строгие ID/source/hash/line/ref проверки; legacy schema не менялась.
- [x] B3 — CORE-001 → B2 → result → C1: CLI PASS, actual missing FAIL, manual/L4 OPEN; reproducible temporary fixtures.
- [x] Checkpoint B-I — 385 full tests PASS, 18 focused PASS, L1 50/9 PASS; only validate/narrow converge доступны, task writes отсутствуют.
- [x] B4 — Read-only Cross-Artifact Analysis: formal conflicts/duplicates, orphan/unmapped/coverage; semantic review отдельно.
- [x] B5 — Четыре observed gap types, bounded history и explicit task upsert; repeated state NO-OP, closed history сохранена.
- [x] Checkpoint B-II — Full 406, focused 39 PASS; повтор NO-OP, history/closed occurrence и stale/concurrent refusal подтверждены.
- [x] B6 — Boundary review: existing state/freshness сохранены; separate Ledger/resume DEFER, ложного reuse/manual PASS нет.
- [x] B7 — Read-only Sync Impact: direct/possible/unknown, selected source/hash/line/pointer chains; recommended/executed checks отдельно.
- [x] Checkpoint B-III — Full 427, focused review 60, freshness 17, state 16 и L1 50/9 PASS; no new state authority.
- [ ] B8 — Интеграция в действующих owners с legacy compatibility.
- [ ] B9 — Изолированный доменный кейс, regression и preservation review.
- [ ] B10 — Инженерный отчёт R0 + K1–K10, Pulse и передача.
- [ ] Checkpoint B-IV — Проверяемая финальная приёмка B.
