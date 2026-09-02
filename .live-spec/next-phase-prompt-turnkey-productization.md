# Next phase — LiveSpec productization: the turnkey software house for one person

Saved 2026-09-01 23:xx, his own words, verbatim, before starting on it. Do this AFTER the current
`PLAN.md` is genuinely finished — verified against the real state of the repo, git, and each
remaining row's own DOD, nothing taken on faith. Most likely worked tomorrow in a fresh session; if
morning arrives with everything green and he hasn't written further, run it in a clean Opus session
once everything is confirmed green.

## Precondition — verify before starting, don't assume

Проверь по реальному состоянию репозитория, git и DOD каждой оставшейся задачи; ничего не принимай
на веру.

## The phase

После проверки начни следующую фазу LiveSpec: продуктализацию turnkey software house для одного
человека с идеей и вкусом, которому не нужно быть техлидом, PM, архитектором, QA или диспетчером
агентов. Он говорит свободно; система сама понимает смысл, выбирает обычные решения, хранит рабочий
контекст, строит нужные spec/architecture/test artifacts, доводит до продакшена и тревожит владельца
редко.

Сначала сделай короткий продуктовый контракт и отдай его product-prover на независимую проверку. Не
начинай код, пока не доказано, что контракт полон и не противоречит существующим полезным частям
системы.

## Decisions to lock in

- `PLAN.md` остаётся единственным каноном: план, очередь и полный текст тикетов уже живут в одном
  списке. Не возвращай отдельный ROADMAP, не создавай вторую базу задач.
- Board — только необязательное представление PLAN по явному запросу. Не строй сервер, event log,
  фоновый рендер, HTML-автоматизацию или отдельную доску.
- Контекст тикета — не копии документов. Это точные указатели на релевантные места PRODUCT_SPEC,
  ARCHITECTURE, TEST_MATRIX, код и проверку. Тикет содержит только то, что нужно именно этой работе.
- Не создавай inbox или отдельную полку для мыслей владельца. Если он явно хочет сохранить работу на
  потом, это нормальный queued тикет с целью и done. Остальное остаётся разговором в транскрипте.
- Director не получает отдельный дорогой model-call на каждое сообщение. Основная модель уже читает
  сообщение и применяет короткий Director-контракт. Любое изменение состояния выполняется через одну
  детерминированную операцию, а не свободной правкой нескольких файлов.
- Статусы надо определить исчерпывающе на реальных примерах до реализации. Базовая гипотеза: queued,
  in hand, blocked, done. `blocked` редок и означает, что продолжать сейчас объективно невозможно:
  техническое ограничение, внешняя зависимость или одно необходимое действие владельца. Порядок
  очереди и запрет лишней параллельности не являются blocker. Отдельный статус `needs his eyes` не
  сохраняй.
- Done определяется в самом тикете. Он включает только применимые условия: наблюдаемый результат для
  человека; целевое место доставки; нужные проверки; доставка в git/main по правилам проекта;
  независимая приёмка воркерской работы. `✅` запрещён, пока DOD не доказан.
- Новая просьба улучшить уже доставленный результат открывает старый тикет только если исходный DOD
  оказался ложным. Иначе это отдельная работа.

## Responsibilities, strictly separated

1. Prompt/Director: понимает смысл сообщения, определяет акт, выбирает нужные области и
   специалистов.
2. Код: хранит и валидирует состояние тикета/checkpoint, не даёт создать дубликат, не даёт закрыть
   тикет с упавшим DOD, выдаёт точный контекст воркеру и восстанавливает его в новой сессии.
3. Product-prover: проверяет полноту и противоречия продуктового контракта и его крайние случаи.
4. Test-author: по proven spec и architecture выводит TEST_MATRIX и тесты.

Сделай Director частью существующей PRODUCT_SPEC → ARCHITECTURE → TEST_MATRIX цепочки. Сейчас это
отсутствующая часть покрытия.

## Two kinds of proof Director needs

A. Живые model-evals, запускаемые только при изменении Director, его политики или модели. Реальные
   сообщения и контекст; проверяют вопрос, поручение, коррекцию, решение, halt и смешанные
   сообщения. Старые traces другой версии не считаются доказательством.

B. Детерминированные тесты state machine. Получают уже принятое решение Director и проверяют
   последствия: вопрос ничего не меняет; поручение создаёт ровно один тикет с указателями и DOD;
   correction меняет текущий тикет; воркер получает его точный текст; упавший DOD не даёт ✅;
   успешный DOD с доставкой даёт ✅; новая сессия продолжает тот же тикет; настоящий blocker имеет
   конкретную причину.

Не создавай ещё один параллельный тестовый контур: эти доказательства должны стать строками
существующей TEST_MATRIX, после product-prover и test-author.

## Serial, CI-green packages

1. Product contract: Director, тикет, контекст, статусы, DOD и граница редкого вопроса владельцу.
2. Один вертикальный путь на LiveSpec: поручение → тикет → воркер → независимая приёмка → доставка →
   done → продолжение новой сессией.
3. Director evals и полное включение его state machine в TEST_MATRIX.
4. Ревизия текущей TEST_MATRIX: сохранить полезные safety/behavior tests, разобрать todo, удалить
   только доказанно дублирующие фразовые проверки после появления равноценных пользовательских
   сценариев.
5. Только затем — изолированный пилот миграции TLV Photos.

Не возвращайся к историческому backlog ради самого backlog. Ничего не создавай, не меняй и не
удаляй до того, как покажешь владельцу короткий план первого CI-green пакета с точным DOD.

## His closing reminder, this same message

Меня не спрашивай ни о чём, там всё закрыто. Работай очень осторожно, чтобы воркеры друг другу не
давили ворктрисы. Ты только оркестратор.

## Addendum, 2026-09-02 09:12 — how the product-contract step is produced

Verbatim: «это сделай и сам в отдельном, и фейблом отдельно и потом дай фейблу все скомпоновать».

The product-contract step (the first item under "Serial, CI-green packages") is drafted twice,
independently, before it goes to product-prover:
1. The orchestrating session itself drafts the contract in its own file.
2. A separate Fable agent drafts the same contract independently, from this same prompt, with no
   sight of draft 1.
3. Fable is then handed both drafts and composes the one contract that goes to product-prover.

Still gated on the precondition above — this fires only once the current PLAN.md is verified
genuinely closed, not before.
