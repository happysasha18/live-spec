## Requirement 309: The work board shows the whole queue in columns — the work in hand, the work done, and what each took  [feature: F-work-board]
   [target]

**Context:** The person leads several windows and asks at any moment what the agent is doing. The work board holds that answer on a page, open whenever the person looks. It is the rendered status page the pack already promises, grown up, so one surface keeps one name. That page is one source file in the host's tree, published at one stable link the person opens from any device. A task reaches the work board when its wish is captured, before its statement is validated: validation gates entry into work, never entry onto the page. A row stays after the task closes, so the page carries what is being done and what was done, each with its time. The chat's departures board keeps its own job. The page carries the whole queue in columns, the work in hand among them. Every row the page shows stands in one column: an open row by the state its queue row records, a closed row in the done column read from the queue archive. The far tier stays off the page under its own request law, and the queued rows standing below the runnable head collapse into a stated count. A card reads as a task at a glance — its echo-name first, then what the change does, then its chips — and the technical detail sits behind the card. Each running step names the worker on it by a craft name and an icon, so which worker runs which task reads at one glance. The work board's form follows the sketch the person already approved, frozen as a norm copy under `docs/norms/` and cited by the form clause's norm pointer. Nothing of this scenario is built yet.

**User Story:** As a person leading several windows, I want one page showing work in hand and work done, so that I need not ask.

### Acceptance Criteria

**Case: the promises this work board leaves standing**

1. The system *shall* keep the chat's departures board at its own scope and shape, taking over none of its report duty. [INV-27]
2. The system *shall* keep narration whole, no board row standing in for a beat the session owes in the chat. [INV-35]
3. The system *shall* keep the capture echo's honest range and the delivery report's estimate beside actual as they stand. [INV-93]
4. The system *shall* keep the routine report's scope and the status report's chat home unchanged, its report-shape check riding the suite. [INV-38, INV-222]
5. The system *shall* keep the chat's live status line whole once the work board ships, the work board adding a view and reducing no chat duty. [INV-71]

**Case: the work board is the rendered status page, grown up**

6. The system *shall* read the work board as the rendered status page the pack already promises, one rendered surface under one name. [INV-308, INV-71]
7. The system *shall* hold the work board as one source file in the host's tree. [INV-308]
8. The system *shall* publish that source file at one stable link, updated from it, so the person opens the work board from any device. [INV-308, INV-67]
   [target]
9. The system *shall* register the work board in the host's surface registry `SURFACES.md`, with the marker text the completeness check reads in the rendered page and the spec anchors it answers to, before it renders. [E-10]
10. The system *shall* lead the work board with the one-line identifier every opened artifact carries — its project, and what it needs of the person. [INV-51]
11. The system *shall* keep one work board per host project and *shall* name the session on every row. [INV-308]
12. *when* a session writes the work board, the system *shall* pass the concurrent-edit fence like any shared-document write, and *shall* have a blocked write re-read the work board and re-apply its own row. [INV-308, INV-11]
13. The system *shall* read both surfaces off the same work, the chat's departures board answering inside every status report and on ask. [INV-308, INV-27]
14. The system *shall* keep the work board standing whether or not anyone asks. [INV-308]

**Case: the form the work board takes**

15. The system *shall* take the work board's form from the sketch the person approved, landing that approved form as a frozen copy under `docs/norms/` and citing it by this clause's norm pointer from the approval on. `norm: docs/norms/work-board.html` [INV-308, INV-43]
16. The system *shall* show board rows in feature language, the work in hand, and a timestamped feed. [INV-308]
17. The system *shall* have the work board's waiting region render the waiting board `WAITING.md` and keep no list of its own, so one clearing rule and one gate hold every waiting item. [INV-308, INV-206]
18. *when* a board row stands blocked — on the person through the waiting board, on another task, or on something outside the project — the system *shall* mark it blocked with the time it has stood so, leaving it in the column its own state names. [INV-308, INV-206]
19. The system *shall* carry every mark the work board shows with its meaning beside it in place, the page shipping no legend block. [INV-308]

**Case: the whole queue stands in columns**

20. The system *shall* show the whole queue on the board in columns, one column per recorded state. [INV-308] [default]
   - the columns are awaiting validation, ready, in work, and done.
21. The system *shall* state on the page, under each column, the one condition a card meets to leave that column. [INV-308]
22. The system *shall* stand every row it shows in exactly one column, dropping none, an open row's column read off the status its queue row records. [INV-308, INV-277]
   - awaiting validation reads off *queued*, ready off *ready*, and in work off *in-work*.
23. The system *shall* keep the far tier off the board, standing it down by name and opening its rows only on the person's request, as the runnable report does. [INV-308, INV-222, INV-223]
24. The system *shall* collapse the *queued* rows standing below the runnable head into a stated count that opens on the person's act, and *shall* drop none in silence. [INV-308] [default]
   - the retunable value is how many *queued* rows stand visible at the head before the rest collapse.
25. The system *shall* show the *deferred* rows as a stated count alone, each row's revisit trigger standing behind an expand. [INV-308, INV-222] [default]
26. The system *shall* place a parked row in the in-work column and *shall* leave its parked mark to the preemption case below. [INV-308, T-9]
27. The system *shall* split the in-work column into lanes, one lane for each build lane the lane cap allows. [INV-308, T-18]
28. The system *shall* show a lane holding no row as free. [INV-308, T-18]
29. The system *shall* have a free lane draw the head *ready* task into it, a lane already holding a row drawing none. [INV-308, T-18]

**Case: a card reads as a task at a glance**

30. The system *shall* order a card's reading: the echo-name first as the recognition hook, then the description of the behaviour, then the chips. It *shall* hold every other detail behind the card in a details layer. [INV-308, INV-28] [default]
   - the echo-name runs three to five plain words.
31. The system *shall* expand every count and reference in a card's details into plain words an outside reader follows, a bare number standing as a defect. [INV-308, INV-28]
32. The system *shall* show a placement tag, as a chip on every board row, read from the queue row's own map and footprint notes. [INV-308, INV-37, INV-128]
   - the tag names the feature the row belongs to, or the several modules the row reaches across.
33. The system *shall* have every board row name and link the part of the product spec its task changes, read from that placement note and the spec delta's own anchors. [INV-308, INV-37]
34. The system *shall* show an in-work row's plan — the deliverables of the task's own statement — on its board row. [INV-308]
35. The system *shall* mark beside that plan the one pipeline stage of the nine the row now stands at. [INV-308, INV-27]
36. The system *shall* keep the fine-grained trail of activity off the card, in the delivery report and the journal the trail criterion below already names. [INV-308, INV-311]
37. The system *shall* lead each deliverable's line with its state mark alone, that line carrying no numbering beside the mark. [INV-308]
38. The system *shall* show a card in work with its settled deliverables and their progress, no line on such a card phrased as an option or an open choice. [INV-308, INV-28]
39. *when* a genuine fork opens mid-work, the system *shall* mark that card blocked under the rule above and *shall* put the question to the person. [INV-308, INV-206]
40. The system *shall* name an in-work row's branch and worktree in the row's details, read from the lane's own claim commit and checkpoint. [INV-308, E-34, INV-69]

**Case: a task enters work only through a validated statement**

41. The system *shall* give every task a statement carrying its echo-name, its description, its plan, and its time estimate. [INV-309, INV-28]
42. The system *shall* keep a task's statement and its validation record in the work board's own source file, keyed by the queue row's id, the queue row keeping its five cells. [INV-309, INV-277]
43. The system *shall* have the plan list the deliverables in the order they run, each a slice of the change that shows value on its own and can be tested on its own. [INV-309]
44. The system *shall* hold an activity that carries value only alongside others — writing the tests, say — outside a plan's deliverables. [INV-309]
45. The system *shall* keep a plan's deliverables to a handful. [INV-309] [default]
   - the retunable value is the most deliverables one plan holds, standing at five.
46. The system *shall* read the plan's parallel mark as the plan's expectation, the take-up lane decision deciding what actually runs together, and *shall* record a divergence plainly in the delivery report's trail. [INV-309, INV-49]
47. The system *shall* bound the deliverables running together inside one task by the same lane cap that bounds build lanes. [INV-309, T-18] [default]
48. The system *shall* read the statement's estimate as the one estimate every other surface cites — the capture echo's range, the board row, and the settling at the close. [INV-309, INV-93]
49. The system *shall* let no task enter work before its statement passes validation's mechanical floor — echo-name, description, plan and estimate each present, an estimate stated, and the register check clean. [INV-309]
50. The system *shall* put every statement before a clean-context reader that carries no project vocabulary and answers three questions from the statement alone — what is to be done, why, and how long — and a question the reader cannot answer fails the statement. [INV-309]
51. The system *shall* hold every outcome comment the board shows to the same plain reading the statement meets, judged by that same reader. [INV-309]
52. The system *shall* have that same reader pass the echo-name test — shown the echo-name alone later, it names which change the task is — a name it cannot place failing the statement. [INV-309, INV-28]
53. *when* a statement fails validation, the system *shall* have it rewritten and validated again, its task staying out of work until it passes. [INV-309]
54. The system *shall* read a passed validation as approval, since routing every statement to the person would stall the granted autonomy. [INV-309] [default]
55. *when* a task's statement passes validation, the system *shall* set its queue row's status to *ready*, dated like every other status. [INV-309, INV-277]
56. The system *shall* read that passing as the task's commitment point, the moment the pack takes the task on and stands behind delivering it. [INV-309]
57. The system *shall* hold the gate-and-reader approval as the standing road and the person's word on a single task as the exception, that standing policy recorded in `DECISIONS.md`. [INV-309] [default]

**Case: approved wording freezes**

58. *when* a statement passes, the system *shall* freeze its wording and speak the task in those words letter for letter, its echo-name standing as the task's one name in every communication that names the task — the chat, the reports, and a worker's brief. [INV-309, INV-28]
59. The system *shall* hold that wording at take-up, along the way, and at the close. [INV-309]
60. *when* the person re-words a statement, the system *shall* take the new wording and freeze it anew. [INV-309]
61. The system *shall* let a task's estimate and its plan be revised only before the task is taken up, the revision running statement validation again and freezing the statement anew. [INV-309, INV-93]
62. *when* a task has been taken up, the system *shall* hold its estimate as it stands and *shall* state any overrun plainly at the close. [INV-309, INV-93]

**Case: the row carries the time promised and the time spent**

63. *when* a task is taken up, the system *shall* write its statement's estimate on its board row. [INV-310, INV-93]
64. *when* a task closes, the system *shall* stand the actual beside that estimate on the same row. [INV-310, INV-93]
65. The system *shall* extend the landing's own settling of estimate against actual onto the work board. [INV-310, INV-93]
66. The system *shall* stand each closed task's end-to-end time beside that pair, from its statement passing validation to its close, read off the board's own stamps. [INV-310, INV-93] [default]
67. The system *shall* show how many tasks closed on the day the page is read, counted off those same stamps. [INV-310] [default]
   - the retunable value is the stretch the count covers, standing at one day.

**Case: a closed task keeps its row**

68. The system *shall* keep every closed task's row on the work board rather than clear it. [INV-311]
69. The system *shall* render each closed task in the done column as one line — state mark, echo-name, time pair — the rest behind a fold the person opens. [INV-311, INV-28] [default]
70. The system *shall* read the done column from the month's archive file under `docs/queue-archive/`, the current month standing by default and an older month opening on the person's ask. [INV-311, INV-276] [default]
71. The system *shall* show each closed row's own terminal state — landed, declined, superseded, or decided — so a declined row shows as declined. [INV-311, INV-276]
72. The system *shall* tag each closed row with its door — feature, bug, refactor, docs-only, or skip — read from the archived row's own intake note. [INV-311, INV-134] [default]
   - the door is the default axis here; the person may prefer the work-kind axis — product, infra, skill, or prose — in its place.
73. The system *shall* extend the delivery report to carry a trail over the plan's steps — each step's outcome, the worker tier or role that ran it, and the step's share of the task's time. [INV-311, INV-103]
74. The system *shall* draw a closed row's step trail from that delivery report. [INV-311, INV-103]

**Case: a preempted task keeps its row**

75. *when* a bug preempts the lane, the system *shall* keep the parked task's row on the work board marked parked, naming the row that preempted it, and *shall* return it to the work in hand once the bug clears. [INV-308, T-9]
76. The system *shall* name that preemption on the page as the board's one queue-jumping class, open to the bug door alone. [INV-308, T-9, INV-134]

**Case: the worker on each running step**

77. The system *shall* name the worker on each running step of the plan by a fixed craft name and icon. [INV-308, INV-33]
78. The system *shall* have the seat name a step's craft in the worker's brief at spawn. The movement's checkpoint record *shall* carry that craft, its icon and the logged tier while the step runs, a mid-flight tier change updating it, and the board *shall* read a running step's worker there. [INV-308, INV-69, D-2]
79. The system *shall* hold the fixed craft set and its icons in the work board's own source file as their one home. [INV-308]
80. The system *shall* read the board's craft names as display names of the pipeline's craft standards, keeping the skill names internal. [INV-308, INV-33, INV-137]
   - Reader stands for the reader worker, Drafter the product-manager craft, Reviewer the formal-reviewer role, Builder the developer craft, Checker the quality-assurance craft.
   - the board's Reviewer names the proving craft, and the design-review role keeps its name.
81. The system *shall* stand a muted note of that worker's tier beside the craft name. [INV-308, INV-69]
82. The system *shall* take the starter crafts as the Reader, the Drafter, the Reviewer, the Builder, and the Checker. [INV-308] [default]
83. The system *shall* hold a worker's identity at its craft name, its icon, and its tier note, and *shall* take a fuller personality only on the person's word. [INV-308]
84. *when* a step's record names no craft, the system *shall* show that step with its craft unnamed rather than guess one. [INV-308]
85. The system *shall* keep which worker runs which task readable at one glance across the whole in-work column. [INV-308]

**Case: the work board refreshes at every moment the person could look**

86. The system *shall* update the work board at every pipeline stage change, at take-up, and at a worker's spawn and finish. [INV-312, INV-71]
87. The system *shall* update it at a landing, and at every state that waits on the person. [INV-312, INV-71]
88. *while* a stretch runs long with no stage change, the system *shall* refresh the work board's stamp on the same heartbeat the chat's narration already carries, so a quiet stretch reads apart from a stalled one. [INV-312, INV-35, INV-71]
89. The system *shall* carry the work board file's update inside the landing's own commit. [INV-312]
90. The system *shall* complete a work board update within about five seconds of the stage change it records, and *shall* never delay that stage. [INV-312] [default]
   - the generator's own suite timing assertion watches this number once the generator ships.

**Case: the work board reads on any screen**

91. The system *shall* lay the work board out in one column on a narrow screen, the work in hand at the top. [INV-313] [default]
92. The system *shall* make every control reachable by touch and *shall* hide nothing behind a hover. [INV-313]
93. The system *shall* keep the work board reachable by keyboard and readable at the contrast the pack's pages hold. [INV-313] [default]

**Case: the empty work board and the stale work board**

94. *when* no work is in hand, the system *shall* say so and show the queue's head in its place. [INV-313]
95. The system *shall* stamp the work board with the time it last updated, so a reader judges its freshness. [INV-313]
96. The system *shall* have an open page re-read itself about every five seconds. [INV-313] [default]

**Case: what the work board is not, and how its working shows**

97. The system *shall* merge no other project's work into a host's work board. [INV-308]
98. The system *shall* write on the work board no history the journal already owns. [INV-308]
99. The system *shall* count the work board working *when* the person answers four questions from the page alone over one real working stretch. The four are what is now being done, who runs what, what was done, and how long each took against its estimate. [INV-308]

---

