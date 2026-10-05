# visual-reference-reconstruction — DESCRIPTION MODE

Реализованы два входа в общий PASS 0 перед сложным 3D-моделированием:

- REFERENCE: image → reconstruction → auxiliary views; исходное изображение
  сохраняет authority и CONFIRMED / INFERRED / SPECULATIVE.
- DESCRIPTION: text → PASS0.1 constraints → PASS0.2 hero candidates → PASS0.3
  selection/Identity Lock → PASS0.4 multiview FROM frozen image → PASS0.5 consistency QA.
  REQUIRED / CANONICAL / SPECULATIVE разделяют указания пользователя, принятый
  дизайн и нерешённую конструкцию.

Основной [skill](../skills/visual-reference-reconstruction/SKILL.md) сохраняет
входной gate и общий контракт. Подробности text-only вынесены в
[description-mode](../skills/visual-reference-reconstruction/references/description-mode.md).
[Contract](../skills/visual-reference-reconstruction/references/pass0-contract.md)
документирует новые поля; валидатор и отдельный модуль проверяют их смысловые связи.

## Архитектура и safeguards

Сохранены имя owner, девять legacy aliases, provider neutrality и разделение
визуальной подготовки/Blender-конструкции. Новые task packets имеют schema_version 2
и mode; schema 1 остаётся совместимым REFERENCE. Catalog/profile/contracts остаются
schema 1. Components, relative dimensions, silhouette, relationships, uncertainty,
auxiliaries и gate сохраняют общий вид для следующего агента.

DESCRIPTION дополнительно хранит исходный brief/hash, REQUIRED constraint IDs,
проверку каждого требования для каждого кандидата, пять оценок качества,
selector/rationale, выбранную canonical image/hash и отдельный frozen manifest.
Один кандидат достаточен для определённого/ограниченного задания; три — рекомендуемый
вариант для exploration в рамках бюджета. Автономный агент выбирает eligible candidate;
интерактивное ожидание выбора применяется только к соответствующему workflow.

FAIL/UNKNOWN обязательного требования запрещает lock, независимо от качества картинки.
REQUIRED цитирует BRIEF, CANONICAL — единственный selected concept. Проигравшие
концепты и auxiliary images не становятся authority. Count/claim targets связывают
требования с компонентами и сохраняют требуемые значения и REQUIRED labels.

Identity snapshot хранит независимую копию данных: изменение count/shape/ranges/pose
не изменяет frozen manifest вместе с пакетом. Проверяются source/image/prompt/manifest
hashes и равенство embedded/on-disk lock. Relock требует версии, причины и predecessor;
auxiliary records обязаны ссылаться на текущие hero hash/lock version. Старые виды
не проходят проверку новой версии. Переименование или перезапись старого lock не
является процедурой изменения дизайна.

Генерация скрытых частей не повышает их certainty. Без usable concept, при pending
выборе или нерешённой ключевой конструкции dependent Blender work останавливается.
При доступном hero и непригодных derived views возможен только явно ограниченный
source-only macro handoff. Text list/procedural proxy не подменяют успешный visual pass.

## Реальный workflow

На примере пользователя про сферического разведывательного меха выполнены две
операции built-in imagegen: один hero из текста, затем multiview из его точных байтов.
Извлечены шесть REQUIRED требований. Hero прошёл их визуальный review и был locked
агентом: шесть component groups, шесть relative ranges, два attachment relationships,
три зоны deferred construction. Качество 20/25; механическая работоспособность не доказана.

[Анализ](pass0-description-workflow/PASS0_analysis.md),
[единый packet](pass0-description-workflow/pass0.json),
[canonical hero](pass0-description-workflow/canonical-hero.png),
[Identity Lock](pass0-description-workflow/identity-lock.json),
[multiview](pass0-description-workflow/auxiliary-multiview.png),
[visual review](pass0-description-workflow/visual-review.json).
Точные [concept prompt](pass0-description-workflow/concept_prompt.txt) и
[multiview prompt](pass0-description-workflow/multiview_prompt.txt) сохранены.

Identity bytes после multiview не изменились. Лист получил RESTRICTED:
identity/silhouette/handedness PASS, proportions/part counts/construction WARN.
Крайние пушки обрезаны, боковая поза не метрически идентична фронту, задние панели
и некоторые закрытые детали придуманы. Задний круглый access panel записан отдельной
SPECULATIVE гипотезой и не попал в frozen design. Gate READY_WITH_LIMITS, только
MACRO_BLOCKOUT. Blender production сцена не изменялась; качество финальной 3D-модели,
rigging, animation, engineering и target renderer не проверялись.

## Проверки и границы

- 159 unit/regression tests PASS; из них 17 новых проверок DESCRIPTION: provenance,
  modes, hard requirements vs scores, three-candidate eligibility, drift, hashes,
  pending lock, revisions и stage routing.
- Tools_C L1: 41 PASS / 0 WARN / 0 FAIL; Blender integration L1: 9 PASS / 0 WARN / 0 FAIL.
  Blanket L2-L4 остаются SKIP по штатному контракту, а не подразумеваются из L1.
- Старый supplied-mech schema 1 и новый DESCRIPTION packet проходят verify-files.
- Actual live Blender MCP возвращает полный PASS 0 → robot context для русского
  text-only brief, без missing documents. [Receipt](pass0-description-workflow/live-context.json).
- Оба дерева совместимых роутеров регенерированы штатным sync; сервер/Hub/launcher
  не изменялись. Existing unrelated dirty work сохранён.
- Optional skill-creator quick_validate SKIP: отсутствует PyYAML; dependency-free
  checks/tests выполнены, новая зависимость ради этого не установлена.

Три реальных image candidates здесь не генерировались: выбор из трёх, включая
высоко оценённый нарушающий требование вариант, проверен синтетическими regression
cases. Manual scoring не является объективным измерителем искусства. Валидатор не
понимает язык brief, не обнаружит ложный pixel review или пропущенное пользователем
требование автоматически. Хеши обнаруживают изменение заявленных байтов, но не
предотвращают намеренное переписывание всех receipts. Нужны человеческие/агентские
review исходного текста, hero и последующей clay-конструкции.

Работа подготовлена локально; ранее опубликованный v4.1.0 остаётся неизменным.
