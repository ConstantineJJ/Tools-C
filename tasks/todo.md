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

**B1, B2, B3… зарезервированы для второго патча.** Документ B прочитан информативно; реализация B не начата.

[Результаты и границы](../reports/MEGA_TOOLS_IMPLEMENTATION_2026-10-16.md): 367 tests PASS, L1 50/9 PASS, live context PASS; code review SELF_REVIEW, art/model improvement не подтверждены.
