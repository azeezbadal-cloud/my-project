# Activity Validation Report

Source of truth: `02_CONTENT/Activity_Manifest.csv` and `Piece_Inventory.csv`, both generated from the same data that draws the pages.

- PASS: **[US_Letter] exactly 48 pages, numbered 1-48** - 48 pages built
- PASS: **[US_Letter] exactly 36 distinct mission pages on pages 5-40** - 36 missions, 36 distinct titles
- PASS: **[US_Letter] every mission has title, instruction, objective and adult guidance** - 36/36 complete
- PASS: **[US_Letter] all piece IDs unique** - 97 piece IDs; duplicates: none
- PASS: **[US_Letter] every inventory piece printed exactly once on the cut-out sheets** - 97 printed; missing none; duplicated none
- PASS: **[US_Letter] no orphan pieces (every piece used by a mission)** - orphans: none
- PASS: **[US_Letter] every required piece ID exists** - unknown: none
- PASS: **[US_Letter] boards <-> pieces mapping complete and every board solvable** - 26 piece missions solvable (bipartite matching), 10 no-cut missions with answers
- PASS: **[US_Letter] all cut-out pieces inside the 0.4in safe area with >=0.25in cutting space, no overlapping cut lines** - piece 1.55in square, gap >= 0.25in, all inside safe area
- PASS: **[US_Letter] no detachable piece smaller than 1.5in (small-parts cylinder is 1.25in)** - smallest piece 1.55in x 1.55in
- PASS: **[US_Letter] every board slot is large enough for its card and inside the safe area** - 124 slots checked (min 1.60in vs card 1.55in)
- PASS: **[US_Letter] number answers match pictured quantities** - 37 counted groups verified (balloons, cupcakes, cookies orders, card dots, comparison rows, tower helpers, finale apples)
- PASS: **[US_Letter] no unreadably small text (min 6pt adult notes; mission instructions >= 12pt)** - smallest text 6.1pt (adult reference table); smallest child-facing heading 9.0pt
- PASS: **[A4] exactly 48 pages, numbered 1-48** - 48 pages built
- PASS: **[A4] exactly 36 distinct mission pages on pages 5-40** - 36 missions, 36 distinct titles
- PASS: **[A4] every mission has title, instruction, objective and adult guidance** - 36/36 complete
- PASS: **[A4] all piece IDs unique** - 97 piece IDs; duplicates: none
- PASS: **[A4] every inventory piece printed exactly once on the cut-out sheets** - 97 printed; missing none; duplicated none
- PASS: **[A4] no orphan pieces (every piece used by a mission)** - orphans: none
- PASS: **[A4] every required piece ID exists** - unknown: none
- PASS: **[A4] boards <-> pieces mapping complete and every board solvable** - 26 piece missions solvable (bipartite matching), 10 no-cut missions with answers
- PASS: **[A4] all cut-out pieces inside the 0.4in safe area with >=0.25in cutting space, no overlapping cut lines** - piece 1.55in square, gap >= 0.25in, all inside safe area
- PASS: **[A4] no detachable piece smaller than 1.5in (small-parts cylinder is 1.25in)** - smallest piece 1.55in x 1.55in
- PASS: **[A4] every board slot is large enough for its card and inside the safe area** - 124 slots checked (min 1.60in vs card 1.55in)
- PASS: **[A4] number answers match pictured quantities** - 37 counted groups verified (balloons, cupcakes, cookies orders, card dots, comparison rows, tower helpers, finale apples)
- PASS: **[A4] no unreadably small text (min 6pt adult notes; mission instructions >= 12pt)** - smallest text 6.1pt (adult reference table); smallest child-facing heading 9.0pt
- PASS: **AB / AAB patterns, sequences and matching orders are logically correct** - 6 patterns solved programmatically; every answer offered exactly once among 3 choices; line-matching columns are shuffled
- PASS: **US Letter and A4 editions have identical page order, boards, slots and piece-sheet allocation** - page numbers, answers and piece IDs identical in both editions

## Mission-by-mission

| # | Page | Mission | Cut-outs | Pieces | Slots | Finger/pencil | Paper cut-outs | Fasteners | Status |
|---|---|---|---|---|---|---|---|---|---|
| 01 | 5 | RAINBOW RESCUE | yes | 6 | 6 answers | Yes - point to the matching cloud | Yes | Yes | automated PASS; visual check |
| 02 | 6 | SHAPE DETECTIVES | yes | 5 | 5 answers | Yes - trace the outlines | Yes | Yes | automated PASS; visual check |
| 03 | 7 | ICE CREAM SHOP | yes | 6 | 6 answers | Partly - name the scoops on each ticket | Yes | Yes | automated PASS; visual check |
| 04 | 8 | COLOUR SORTING GARDEN | no-cut | 0 | 6 answers | Yes | No - no-cut activity | No | automated PASS; visual check |
| 05 | 9 | FINISH THE PATTERN | no-cut | 0 | 6 answers | Yes | No - no-cut activity | No | automated PASS; visual check |
| 06 | 10 | BUILD A FUNNY ROBOT | yes | 4 | 4 answers | Partly - point to each part | Yes | Yes | automated PASS; visual check |
| 07 | 11 | FIND MY HOME | yes | 6 | 6 answers | Partly - point to each home | Yes | Yes | automated PASS; visual check |
| 08 | 12 | WHAT DO I EAT? | no-cut | 0 | 6 answers | Yes | No - no-cut activity | No | automated PASS; visual check |
| 09 | 13 | ANIMAL SHADOW SEARCH | yes | 6 | 6 answers | Partly - point to each shadow | Yes | Yes | automated PASS; visual check |
| 10 | 14 | MISSING ANIMAL PARTS | yes | 3 | 3 answers | Partly - name the missing part | Yes | Yes | automated PASS; visual check |
| 11 | 15 | FARMYARD FRIENDS | yes | 3 | 3 answers | Partly - point to each place | Yes | Yes | automated PASS; visual check |
| 12 | 16 | OCEAN EXPLORERS | yes | 3 | 3 answers | Partly - point and name | Yes | Yes | automated PASS; visual check |
| 13 | 17 | NUMBER TRAIN | yes | 10 | 10 answers | Yes - point and count along the train | Yes | Yes | automated PASS; visual check |
| 14 | 18 | COUNT THE BALLOONS | yes | 6 | 6 answers | Yes - count with a finger | Yes | Yes | automated PASS; visual check |
| 15 | 19 | FEED THE MONSTER | yes | 5 | 5 answers | Partly - count the cookies on the plate | Yes | Yes | automated PASS; visual check |
| 16 | 20 | LITTLE NUMBER BAKERY | yes | 4 | 4 answers | Yes - count with a finger | Yes | Yes | automated PASS; visual check |
| 17 | 21 | MORE OR LESS? | no-cut | 0 | 4 answers | Yes | No - no-cut activity | No | automated PASS; visual check |
| 18 | 22 | BUILD A NUMBER TOWER | yes | 10 | 10 answers | Yes - point from bottom to top | Yes | Yes | automated PASS; visual check |
| 19 | 23 | DRESS FOR THE WEATHER | yes | 3 | 3 answers | Partly - point to the right clothes | Yes | Yes | automated PASS; visual check |
| 20 | 24 | MAKE A HAPPY FACE | yes | 5 | 2 answers | Partly - draw features on a copy | Yes | Yes | automated PASS; visual check |
| 21 | 25 | HOW DO I FEEL? | no-cut | 0 | 6 answers | Yes | No - no-cut activity | No | automated PASS; visual check |
| 22 | 26 | WASH, BRUSH, GET READY! | yes | 4 | 4 answers | Partly - point in order | Yes | Yes | automated PASS; visual check |
| 23 | 27 | MY TEDDY'S OUTFIT | yes | 3 | 3 answers | Partly - point and name | Yes | Yes | automated PASS; visual check |
| 24 | 28 | KINDNESS GARDEN | no-cut | 0 | 3 answers | Yes | No - no-cut activity | No | automated PASS; visual check |
| 25 | 29 | MY LITTLE SUPERMARKET | yes | 6 | 6 answers | Partly - point to each shelf | Yes | Yes | automated PASS; visual check |
| 26 | 30 | PACK MY BACKPACK | no-cut | 0 | 8 answers | Yes | No - no-cut activity | No | automated PASS; visual check |
| 27 | 31 | WHAT GOES WHERE? | yes | 3 | 3 answers | Partly - point to each room | Yes | Yes | automated PASS; visual check |
| 28 | 32 | LITTLE CHEF'S KITCHEN | yes | 3 | 3 answers | Partly - point to each step | Yes | Yes | automated PASS; visual check |
| 29 | 33 | ON THE ROAD | yes | 4 | 4 answers | Partly - point to each place | Yes | Yes | automated PASS; visual check |
| 30 | 34 | MY DAY, MY WAY | no-cut | 0 | 5 answers | Yes | No - no-cut activity | No | automated PASS; visual check |
| 31 | 35 | TREASURE MAP MATCH | yes | 3 | 3 answers | Partly - point to each spot | Yes | Yes | automated PASS; visual check |
| 32 | 36 | BUILD A LITTLE CASTLE | yes | 4 | 4 answers | Partly - point to each space | Yes | Yes | automated PASS; visual check |
| 33 | 37 | WHAT COMES NEXT? | no-cut | 0 | 4 answers | Yes | No - no-cut activity | No | automated PASS; visual check |
| 34 | 38 | NATURE DISCOVERY | no-cut | 0 | 6 answers | Yes | No - no-cut activity | No | automated PASS; visual check |
| 35 | 39 | FIND THE PAIRS | yes | 8 | 8 answers | No - cards are needed | Yes | Optional | automated PASS; visual check |
| 36 | 40 | GRAND FINALE: HELP LEO GET HOME | yes | 4 | 4 answers | Partly - point at each stop | Yes | Yes | automated PASS; visual check |

## Piece budget

- 97 cards in 21 sets; capacity 5 sheets x 20 = 100 at a safe card size of 1.55 in (39 mm).
- To stay within five sheets without shrinking cards, sets are shared between boards (RD: p5 & p40; SH: p6 & p40; AN: p11, p13 & p40; NU: p17, p18, p20, p22 & p40) and 10 missions were designed as no-cut activities.
- Sets are never split across sheets; sheet allocation is first-fit by usage order, not by chapter.

## Accuracy notes (animals, food, habitats)

- Habitats: fish-ocean, cow-farm field, monkey-rainforest, penguin-icy land (many penguin species live in cold southern regions; some live in warmer places - adult note says animals can live in more than one kind of place), camel-desert, frog-pond.
- Foods: panda-bamboo (bamboo is almost all of a giant panda's diet); bee-flowers (nectar and pollen); penguin-fish; squirrel-acorns (nuts and seeds); cow-grass; monkey-banana (many monkeys eat fruit; bananas are a familiar example). Avoided the common inaccurate pairing rabbit-carrot. Adult note: animals eat other foods too.
- Farm: hen-hen house, pig-mud (pigs cool off in mud), duck-pond.
- Anatomy: each animal keeps the correct number of legs, ears, eyes for its simplified style; no hands with fingers are drawn.
