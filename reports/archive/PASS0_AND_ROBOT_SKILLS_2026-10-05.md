# Два новых Skills: PASS 0 и механическая конструкция

Дата: 5 октября 2026. Канонический источник — Tools_C. Реализация выполнена в порядке
приоритетов: сначала visual-reference-reconstruction, затем robot/mechanism modeling.

## Что реализовано

- [visual-reference-reconstruction](../skills/visual-reference-reconstruction/SKILL.md):
  обязательный PASS 0 перед сложным моделированием/существенной реконструкцией по
  изображениям; анализ до Blender; компоненты, относительные размеры, silhouette/
  proportion notes, связи, ambiguity map, конфликты, auxiliary references и review.
- [blender-robot-mechanism-modeling](../skills/blender-robot-mechanism-modeling/SKILL.md):
  крупные формы, механический каркас, оси/подшипники/приводы, статическая достижимость,
  слои брони, зазоры, производственная логика и detail hierarchy. Отдельные G0–G7
  checkpoints обеспечивают geometry → clay → materials → wear.
- [Контракт пакета](../skills/visual-reference-reconstruction/references/pass0-contract.md)
  и [валидатор](../skills/visual-reference-reconstruction/scripts/validate_pass0.py)
  проверяют происхождение выводов, связи/IDs, размеры, review и условия перехода.
  Это стандартная библиотека Python; провайдер генерации заменяем и необязателен.
- Практические решения второго skill связаны с [уроками Report4.0.3](../skills/blender-robot-mechanism-modeling/references/report-lessons.md).
  Отчёт использован как данные: старое уточнение о сквозных трубах не перенесено
  в универсальное требование для любого нового меха.

Материалы/UV, polishing/wear, sculpt, rigging, animation, export и engine integration
сохраняют существующих владельцев. Новый механический skill задаёт критерии и
передачу стадий, не дублирует их реализацию. Vehicles/buildings/props сохраняют
своих владельцев; PASS 0 применим к ним всем, механический skill — только к
действительно запрошенным сочленённым узлам.

## Интеграция

Skills добавлены в manifest/profile/AGENTS и pipeline, защищены активными
декларативными контрактами. Старый `Blender_Reference_Reconstruction_SKILL` теперь
указывает на новый canonical owner; прежний reference.md оставлен тонким указателем.
Сохранены девять compatibility aliases; обе router-деревья Blender-MCP-Co
регенерированы стандартным sync без ручной правки.

Live Blender MCP уже видит **27 canonical skills** и читает оба новых skill.
Запрос `Create a mech from the reference image` возвращает PASS 0 первым, затем
robot modeling, без пропущенных документов. Legacy read тоже загружает PASS 0.
Проверены отдельные маршруты создания меха, переделки силуэта + scratches,
surface-only wear, rig, animation и export. [Live context](pass0-mech-workflow/live_context.json),
[discovery/read evidence](pass0-mech-workflow/live_discovery.json).

Существующий механизм целых SOURCE-документов и receipts сохранён. Сокращение
повторяющегося текста pipeline восстановило прежние маршруты в лимите контекста;
необходимые операции по-прежнему требуют чтения своих conditional references.

## Реальный workflow

Использованы все четыре приложенных изображения и практический отчёт. Рабочий
source of truth — mech-big.png; остальные изображения — сравнительные производные
входы. Все входные файлы сохранены с SHA-256 в task-local пакете.

Создан [PASS 0 анализ](pass0-mech-workflow/PASS0_analysis.md) и
[JSON](pass0-mech-workflow/pass0.json): 11 компонентных групп, 15 диапазонов размеров,
property-level claims, 7 отношений, 4 ambiguity entries и 4 записи различий/конфликтов.
Исходник задаёт две сетки по 4×3 видимых круговых элементов; сквозные каналы этим
не доказаны. Спина, скрытые крепления и масштабы остаются явно неопределёнными.

Встроенный image generation создал [front / side / rear / 3/4](pass0-mech-workflow/auxiliary_multiview.png)
из исходного изображения, с сохранённым [prompt](pass0-mech-workflow/auxiliary_prompt.txt).
Лист просмотрен и получил **RESTRICTED**: общий образ/крупный счёт сохранены,
часть скрытой геометрии помечена, но задняя броня конечностей маркирована не полностью,
а панели/стопы/пропорции расходятся. Статус пакета **READY_WITH_LIMITS** разрешает
только макроблокаут и запрещает неподтверждённую заднюю/внутреннюю конструкцию.

В отдельном factory-процессе Blender 5.2.2 LTS пакет действительно прочитан **до
создания геометрии**. Получены 48 редактируемых macro/proxy объектов, 24 лицевых
элемента на общем mesh, четыре clay-снимка и сохранённый файл. Независимое открытие
с отключённым auto-run сохранило объявленные исходные mesh counts, мировые матрицы
и shared datablock names. [Consumer result](pass0-mech-workflow/consumer_result.json),
[fresh reopen](pass0-mech-workflow/consumer_reopen.json).

Визуальная проверка G1 выявила плоский корпус, коробчатые ноги и отсутствие
сегментированных клиновидных стоп. Это **VISUAL FAIL для развитой формы**:
детали/материалы/wear не выполнялись. Тест подтверждает handoff и остановку на
непройденном clay gate; он не подтверждает готовность производственного меха,
полную механическую сборку, анимацию или инженерную работоспособность.

## Safeguards и границы доказательства

| Safeguard | Как работает | Ограничение |
|---|---|---|
| CONFIRMED / INFERRED / SPECULATIVE | Классификация по свойству с source region и reasoning | Валидатор не определяет истинность визуального наблюдения |
| Исходник — source of truth | Auxiliary/report не могут подтвердить исходную геометрию; сохраняется lineage/hash | Хеш и role не доказывают авторство/происхождение источника |
| Генерированные ракурсы одного объекта | Review identity/proportions/counts/construction/handedness/silhouette, ограничение/отказ при drift | Image generation не выполняет метрический multiview solve; точной 3D-consistency нет |
| Неизвестные скрытые части | DEFER/PROXY, при необходимости BLOCKING | Красивый rear view не восстанавливает фактическую спину |
| Машинная readiness | Валидатор отклоняет критические blockers и `require_stage` не разрешает другую стадию | Это gate pipeline и потребителей пакета, а не глобальный перехват любого произвольного Blender вызова |
| Shape before surface | G1/G3 clay gates; failed prerequisite останавливает escalation | Mesh PASS не доказывает силуэт/посадку брони |
| Механическая правдоподобность | Оси, фиксированные длины, якоря приводов, representative clearances | Статические проверки не доказывают кинематику, прочность или безопасность реальной машины |

Агент должен остановить зависимую работу, когда нет читаемого исходника/пакета;
конфликтует основной счёт/силуэт/интерфейс; скрытая часть нужна для результата, но
не выводится из данных; генерация упорно меняет конструкцию; поза недостижима без
растяжения; clay review не выполнен или выявил слабую форму. Независимые поддержанные
области могут продолжаться только при явно ограниченной readiness. После двух
неудачных targeted corrections генерации следует restrict/reject, а не уверенная
выдумка. В этом тесте достаточно одного restricted листа — точная спина не требовалась.

## Проверки и сохранность

Результаты финальных автоматических проверок записаны в [validation.json](pass0-mech-workflow/validation.json).
Финальный regression suite: **142 теста PASS**. Tools_C L1: **40 PASS**,
Blender-MCP-Co L1: **9 PASS**, по обоим **0 FAIL**. Проверка текущего PASS 0
с исходными/auxiliary/prompt хешами — **STRUCTURAL PASS**. Эти числа не заменяют
отдельно отмеченный G1 VISUAL FAIL и ограничения generated references.
Новый набор включает положительные/отрицательные случаи provenance laundering,
blockers, unit mismatch, hash drift, count-review failure, malformed JSON и
stage-only routing. Дополнительный quick_validate от skill-creator не запущен
успешно: в доступном runtime отсутствует PyYAML; это **SKIP**, не PASS.

Первоначальные dirty/untracked изменения Tools_C и Blender-MCP-Co сохранены;
production .blend и исходные вложения не редактировались. Изменения этой задачи
касаются новых skills, их регистрации/маршрутов, generated routers и отдельного
evidence-пакета. Коммит и публикация в рамках этого запроса не выполнялись.
