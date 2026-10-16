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

## Патч B — подготовлен, реализация не начата

Детальные критерии/owners/dependencies — в [плане](plan.md). R0 пока OPEN.

- [ ] B1 — Актуальный audit, source review и Gate R0 по пяти функциям.
- [ ] B2 — Минимальный совместимый traceability contract и устойчивые IDs.
- [ ] B3 — Один воспроизводимый сквозной offline slice.
- [ ] Checkpoint B-I — Vertical slice и сохранение совместимости.
- [ ] B4 — Read-only Cross-Artifact Analysis с evidence.
- [ ] B5 — Convergence, четыре gap types и идемпотентные corrective tasks.
- [ ] Checkpoint B-II — Нет дубликатов/потери истории/ложного PASS.
- [ ] B6 — Resume/Ledger reuse или обоснованный DEFER.
- [ ] B7 — Sync Impact: direct/possible/unknown и уровни проверок.
- [ ] Checkpoint B-III — State/impact без второго source of truth.
- [ ] B8 — Интеграция в действующих owners с legacy compatibility.
- [ ] B9 — Изолированный доменный кейс, regression и preservation review.
- [ ] B10 — Инженерный отчёт R0 + K1–K10, Pulse и передача.
- [ ] Checkpoint B-IV — Проверяемая финальная приёмка B.
