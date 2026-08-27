# live-spec Roadmap — retired 2026-08-27 (dated version: 2026-08-27; SPEC M-3)

The owner's decision, 27.08: "нет роадмапа нет бэклога есть только план" <!-- user-language --> (no roadmap, no backlog, only a plan). PLAN.md's own step 11 ("One queue of work, and the board shows its top") is executed by this rotation: every row this file carried live is superseded by the matching `q-<id>` task in `PLAN.md`'s `## Tasks` section, and this file carries no live rows from here on. The format-family rules below stand as a record of the row shape those rows once held; the mechanism itself is retired.
The wish queue: the live record of what is asked of the product and where each ask stands. A wish is a
request for a change the product does not yet carry, and it lands when the delivery that completes it
ships. Intake is continuous, a wish entering the moment it is spoken; execution runs at most three independent
landings at once — the lane cap — and a landing finishes before a colliding next starts.

The roadmap is a member of the format family. Its shared rules — the closed-vocabulary glossary, the
keyword form, the no-capitals rule, the trailing code anchor, the no-history law, the comprehension
gate — live once in `docs/spec-format.md` and hold here unchanged. Its own rules — the row shape, the
status and class vocabularies, the live-body law, the row lint — are defined in `docs/roadmap-format.md`.
The class cell names the wish's size, one vocabulary shared with the spec: *bug*, *small*, *surface*,
or *large*. The wish cell carries a priority mark when the wish's priority is other than normal. The status cell carries one of *queued*, *ready*,
*in-work*, *deferred*, or *far*, each with its date, a *deferred* row naming its revisit trigger. A row
reads *ready* once its task statement has passed validation and its wording is frozen. The status cell is the sole authority on a row's current state; the wish and acceptance cells carry
the ask and its criteria. Pre-conversion prose in those cells keeps its old words verbatim —
capitals and old state words included — and lowers as rows are edited; a bold landed or open there
is history, and the status cell alone says where the row stands. The pre-conversion status texts of the rows that stayed live are kept verbatim
in docs/queue-archive/status-notes-ROADMAP-2026-07-23.md. A
bracket code such as `[INV-277]` points to its home in `PRODUCT_SPEC.md`; a reader may ignore it.
Two bracket marks read as part of their sentence: `[target]` marks a feature or leg that is promised
but not yet built, owed an open row here (SPEC S-0), and `[default: …]` names a value the agent set
that the human may retune.

This file's live body is retired: it holds no rows. Every wish that stood here on 2026-08-27 moved, verbatim, to `docs/queue-archive/rotated-ROADMAP-2026-08-27-merged-into-plan.md`, and its new home is the matching `q-<id>` task in `PLAN.md`'s `## Tasks` section. The rotated-manifest block below records the move, the same way every earlier rotation in this file did.

<!-- rotated-manifest -->
Rotated closed rows (base rule 10 — nothing lost; the archive keeps every moved row, grepable by number; the live queue below holds live material):
- rows 14, 27, 33, 42, 43, 62, 63, 67, 101, 121, 172, 189, 194, 196, 200, 201, 202 → docs/queue-archive/rotated-ROADMAP-2026-07-18.md
- rows 47, 59, 64, 99, 107, 109, 110, 115, 128, 130, 135, 136, 137, 138, 139, 145, 149, 150, 151, 152, 154, 155, 156, 157, 158, 159, 160, 161, 162, 188, 195, 209, 210, 211, 212, 213, 214, 216, 218, 219, 222, 223, 224, 225, 226, 227, 228, 232, 233, 237, 239, 240, 242, 244, 245, 246, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 303, 304, 305, 306, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 333, 334, 335, 336, 337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 349, 350, 351, 352, 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 382, 383, 384, 387, 388, 390, 391, 392, 393, 394, 395, 397, 402, 403, 406, 407, 408, 409, 413, 414, 415, 416, 417, 418, 419, 420, 422, 423, 429, 430, 431, 433, 434, 438, 439, 441, 442, 443, 444, 445, 456, 461, 462, 463, 464, 468, 470, 476, 477, 478, 480, 482, 494, 495, 502, 506 → docs/queue-archive/rotated-ROADMAP-2026-07.md
- rows 522, 549, 555, 556, 557, 565, 569, 571, 572, 573, 574, 577, 602, 618, 619, 626, 700 → docs/queue-archive/rotated-ROADMAP-2026-08.md
- rows 69, 197, 198, 199, 302, 307, 308, 309, 332, 389, 401, 425, 426, 428, 432, 435, 446, 447, 448, 449, 450, 451, 452, 465, 466, 467, 472, 473, 474, 475, 483, 498, 499, 500, 505, 508, 512, 513, 514, 515, 516, 518, 519, 520, 521, 523, 524, 526, 528, 530, 532, 533, 534, 535, 538, 539, 540, 541, 543, 544, 545, 546, 547, 548, 551, 553, 559, 560, 561, 562, 563, 564, 578, 579, 580, 585, 587, 594, 599, 600, 601, 603, 604, 606, 607, 613, 614, 615, 616, 620, 621, 622, 750 → docs/queue-archive/rotated-ROADMAP-2026-08-27-provenance-purge.md
- rows 44, 48, 49, 54, 93, 95, 96, 100, 108, 117, 118, 119, 129, 131, 133, 134, 140, 141, 143, 144, 148, 163, 165, 166, 168, 170, 171, 190, 191, 192, 193, 203, 204, 205, 206, 207, 208, 215, 217, 220, 221, 229, 230, 231, 234, 235, 236, 238, 241, 243, 247, 261, 381, 385, 386, 396, 398, 399, 400, 404, 405, 410, 411, 412, 421, 424, 427, 436, 437, 440, 453, 454, 455, 457, 458, 459, 460, 469, 471, 479, 481, 484, 485, 486, 487, 488, 489, 490, 491, 492, 493, 496, 497, 501, 503, 504, 507, 509, 510, 511, 517, 525, 527, 529, 531, 536, 537, 542, 550, 552, 554, 566, 567, 568, 570, 575, 576, 581, 582, 583, 584, 586, 588, 589, 590, 591, 592, 593, 595, 596, 597, 598, 605, 608, 609, 610, 611, 612, 617, 623, 624, 625 → docs/queue-archive/rotated-ROADMAP-2026-08-27-merged-into-plan.md
<!-- /rotated-manifest -->

