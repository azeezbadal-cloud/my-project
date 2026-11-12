"""My Magic Busy Book - master content (single source of truth).

Everything child-facing and adult-facing that is not artwork lives here so it
can be translated (Arabic / German / bilingual editions) without touching
layout code.
"""

PRODUCT = {
    "title": "MY MAGIC BUSY BOOK",
    "subtitle": "36 Little Missions to Match, Sort, Count & Play!",
    "brand": "LITTLE WORLDS LEARNING",
    "tagline": "Big Curiosity. Little Adventures.",
    "ages": "AGES 3–5",
    "version": "Version 1.0 · November 2026",
    "version_short": "v1.0",
    "price_aud": "9.99",
    "pages": 48,
}

BRAND_COLOURS = {
    "Sunshine Yellow": "#FFD348",
    "Sky Blue": "#64C8ED",
    "Lime Green": "#A8D849",
    "Coral": "#F26855",
    "Playful Pink": "#F7B6D2",
    "Warm Cream": "#FFF9EA",
    "Dark Navy": "#18354B",
    "White": "#FFFFFF",
}

SUPPORT_COLOURS = {
    "Explorer Purple (chapter 6 accent)": "#B58BE0",
    "Leo Gold": "#F4B940",
    "Leo Mane": "#E98A2E",
    "Activity Red": "#E8473B",
    "Activity Orange": "#F7923A",
    "Activity Green": "#6CC04A",
    "Activity Blue": "#3FA9E0",
    "Activity Purple": "#9B6BD3",
    "Hint Grey": "#8C9BA7",
}

CHAPTERS = [
    {"key": "colour", "num": 1, "name": "Colour Kingdom", "colour": "#F7B6D2", "deep": "#D8578F", "tint": "#FDEAF3", "world": "world_colour", "pages": (5, 10)},
    {"key": "animal", "num": 2, "name": "Animal Island", "colour": "#A8D849", "deep": "#5E9A1E", "tint": "#EFF8DD", "world": "world_animal", "pages": (11, 16)},
    {"key": "number", "num": 3, "name": "Number Town", "colour": "#64C8ED", "deep": "#1F86B3", "tint": "#E2F4FB", "world": "world_number", "pages": (17, 22)},
    {"key": "feelings", "num": 4, "name": "Feelings Forest", "colour": "#FFD348", "deep": "#B98700", "tint": "#FFF6D6", "world": "world_feelings", "pages": (23, 28)},
    {"key": "everyday", "num": 5, "name": "Everyday Village", "colour": "#F26855", "deep": "#C8402E", "tint": "#FDE4E0", "world": "world_everyday", "pages": (29, 34)},
    {"key": "adventure", "num": 6, "name": "Adventure Land", "colour": "#B58BE0", "deep": "#7A4FB8", "tint": "#F1E9FA", "world": "world_adventure", "pages": (35, 40)},
]

SKILLS = {
    "match": ("MATCH", "icon_match"),
    "sort": ("SORT", "icon_sort"),
    "count": ("COUNT", "icon_count"),
    "build": ("BUILD", "icon_build"),
    "imagine": ("IMAGINE", "icon_imagine"),
    "explore": ("EXPLORE", "icon_explore"),
}

# ------------------------------------------------------------------------------------------
# Piece sets.  (id, asset, short label).  Every piece is a 1.55in square card.
PIECE_SETS = [
    {"code": "RD", "name": "Rainbow drops", "tab": "#F7B6D2", "items": [
        ("RD1", "drop_red", "red drop"), ("RD2", "drop_orange", "orange drop"), ("RD3", "drop_yellow", "yellow drop"),
        ("RD4", "drop_green", "green drop"), ("RD5", "drop_blue", "blue drop"), ("RD6", "drop_purple", "purple drop")]},
    {"code": "SH", "name": "Shapes", "tab": "#F7B6D2", "items": [
        ("SH1", "shape_circle", "circle"), ("SH2", "shape_square", "square"), ("SH3", "shape_triangle", "triangle"),
        ("SH4", "shape_rectangle", "rectangle"), ("SH5", "shape_star", "star")]},
    {"code": "IC", "name": "Ice-cream scoops", "tab": "#F7B6D2", "items": [
        ("IC1", "scoop_strawberry", "strawberry scoop"), ("IC2", "scoop_chocolate", "chocolate scoop"), ("IC3", "scoop_mint", "mint scoop"),
        ("IC4", "scoop_lemon", "lemon scoop"), ("IC5", "scoop_blueberry", "blueberry scoop"), ("IC6", "scoop_orange", "orange scoop")]},
    {"code": "RB", "name": "Robot parts", "tab": "#F7B6D2", "items": [
        ("RB1", "robot_antenna", "antenna"), ("RB2", "robot_head", "robot head"), ("RB3", "robot_body", "robot body"), ("RB4", "robot_wheels", "wheels")]},
    {"code": "AN", "name": "Animal friends", "tab": "#A8D849", "items": [
        ("AN1", "fish", "fish"), ("AN2", "cow", "cow"), ("AN3", "monkey", "monkey"),
        ("AN4", "penguin", "penguin"), ("AN5", "camel", "camel"), ("AN6", "frog", "frog")]},
    {"code": "AP", "name": "Animal parts", "tab": "#A8D849", "items": [
        ("AP1", "part_rabbit_ears", "rabbit ears"), ("AP2", "part_fox_tail", "fox tail"), ("AP3", "part_elephant_trunk", "elephant trunk")]},
    {"code": "FM", "name": "Farm friends", "tab": "#A8D849", "items": [
        ("FM1", "hen", "hen"), ("FM2", "pig", "pig"), ("FM3", "duck", "duck")]},
    {"code": "OC", "name": "Sea friends", "tab": "#A8D849", "items": [
        ("OC1", "octopus", "octopus"), ("OC2", "turtle", "turtle"), ("OC3", "crab", "crab")]},
    {"code": "NU", "name": "Number cards", "tab": "#64C8ED", "items": [
        (f"NU{i}", None, f"number {i}") for i in range(1, 11)]},
    {"code": "TR", "name": "Monster cookies", "tab": "#64C8ED", "items": [
        (f"TR{i}", "cookie", "cookie") for i in range(1, 6)]},
    {"code": "WE", "name": "Weather wear", "tab": "#FFD348", "items": [
        ("WE1", "sunhat", "sun hat"), ("WE2", "rainboots", "rain boots"), ("WE3", "scarf", "warm scarf")]},
    {"code": "FA", "name": "Face features", "tab": "#FFD348", "items": [
        ("FA1", "eyes_round", "round eyes"), ("FA2", "eyes_happy", "smiley eyes"), ("FA3", "mouth_smile", "big smile"),
        ("FA4", "mouth_o", "'oh!' mouth"), ("FA5", "mouth_wobbly", "wobbly mouth")]},
    {"code": "RT", "name": "Morning routine", "tab": "#FFD348", "items": [
        ("RT1", "rt_wake", "wake up"), ("RT2", "rt_wash", "wash"), ("RT3", "rt_brush", "brush teeth"), ("RT4", "rt_dress", "get dressed")]},
    {"code": "TD", "name": "Teddy's outfit", "tab": "#FFD348", "items": [
        ("TD1", "teddy_hat", "hat"), ("TD2", "jumper", "jumper"), ("TD3", "teddy_boots", "boots")]},
    {"code": "SM", "name": "Shopping", "tab": "#F26855", "items": [
        ("SM1", "apple", "apple"), ("SM2", "carrot", "carrot"), ("SM3", "bread", "bread"),
        ("SM4", "croissant", "croissant"), ("SM5", "milk", "milk"), ("SM6", "cheese", "cheese")]},
    {"code": "HO", "name": "Home things", "tab": "#F26855", "items": [
        ("HO1", "toothbrush", "toothbrush"), ("HO2", "pillow", "pillow"), ("HO3", "saucepan", "saucepan")]},
    {"code": "CH", "name": "Sandwich fillings", "tab": "#F26855", "items": [
        ("CH1", "lettuce", "lettuce"), ("CH2", "cheese_slice", "cheese"), ("CH3", "tomato_slices", "tomato")]},
    {"code": "VE", "name": "Vehicles", "tab": "#F26855", "items": [
        ("VE1", "plane", "plane"), ("VE2", "car", "car"), ("VE3", "train", "train"), ("VE4", "boat", "boat")]},
    {"code": "TM", "name": "Map landmarks", "tab": "#B58BE0", "items": [
        ("TM1", "palm", "palm tree"), ("TM2", "bridge", "bridge"), ("TM3", "lighthouse", "lighthouse")]},
    {"code": "CA", "name": "Castle pieces", "tab": "#B58BE0", "items": [
        ("CA1", "roof_left", "blue roof"), ("CA2", "roof_right", "purple roof"), ("CA3", "castle_door", "door"), ("CA4", "castle_flag", "flag")]},
    {"code": "MP", "name": "Memory pairs", "tab": "#B58BE0", "items": [
        ("MP1", "sun", "sun"), ("MP2", "sun", "sun"), ("MP3", "boat", "boat"), ("MP4", "boat", "boat"),
        ("MP5", "apple", "apple"), ("MP6", "apple", "apple"), ("MP7", "tulip", "tulip"), ("MP8", "tulip", "tulip")]},
]

PIECE_INDEX = {pid: (s, asset, label) for s in PIECE_SETS for pid, asset, label in s["items"]}


def ids(prefix, a, b):
    return [f"{prefix}{i}" for i in range(a, b + 1)]


# ------------------------------------------------------------------------------------------
# Missions. 'modes' = (finger/pencil, paper cut-outs, reusable fasteners)
MISSIONS = [
    # ---------------- Colour Kingdom
    dict(n=1, page=5, ch="colour", title="RAINBOW RESCUE", instr="Match each raindrop to its cloud!", skill="match",
         goal="Recognise and name six colours; match by colour and symbol", diff="Easy",
         pieces=ids("RD", 1, 6), leo=("leo_wave", "Can you help me?"),
         guide="Name each colour together. If colours are tricky, match the white symbols instead (heart, circle, star, leaf, wave, diamond).",
         modes=("Yes - point to the matching cloud", "Yes", "Yes")),
    dict(n=2, page=6, ch="colour", title="SHAPE DETECTIVES", instr="Find the shape that fits each shadow!", skill="match",
         goal="Recognise circle, square, triangle, rectangle and star", diff="Easy",
         pieces=ids("SH", 1, 5), leo=("leo_point", "Let's find it!"),
         guide="Trace each outline with a finger and count the corners together. A circle has no corners!",
         modes=("Yes - trace the outlines", "Yes", "Yes")),
    dict(n=3, page=7, ch="colour", title="ICE CREAM SHOP", instr="Make each ice cream match the order!", skill="build",
         goal="Follow a picture order; match colours; place items bottom-to-top", diff="Medium",
         pieces=ids("IC", 1, 6), leo=None,
         guide="Read each order ticket from the bottom up. Afterwards, invite your child to invent their own ice cream.",
         modes=("Partly - name the scoops on each ticket", "Yes", "Yes")),
    dict(n=4, page=8, ch="colour", title="COLOUR SORTING GARDEN", instr="Draw a line from each flower to its pot!", skill="sort",
         goal="Sort objects into groups by colour", diff="Easy", pieces=[], leo=None,
         guide="No cutting needed. Use a finger, a crayon or (if laminated) a dry-erase pen. Each pot shows a symbol as well as a colour.",
         modes=("Yes", "No - no-cut activity", "No")),
    dict(n=5, page=9, ch="colour", title="FINISH THE PATTERN", instr="What comes next? Circle it!", skill="explore",
         goal="Continue simple AB and AAB repeating patterns", diff="Medium", pieces=[], leo=("leo_think", "Hmm... what comes next?"),
         guide="Say the pattern aloud together ('red, blue, red, blue...'). Clapping or tapping the rhythm helps.",
         modes=("Yes", "No - no-cut activity", "No")),
    dict(n=6, page=10, ch="colour", title="BUILD A FUNNY ROBOT", instr="Stack the pieces to build a robot!", skill="build",
         goal="Build a whole picture from parts; top / middle / bottom vocabulary", diff="Easy",
         pieces=ids("RB", 1, 4), leo=("leo_cheer", "Beep boop!"),
         guide="Once the robot is built, try a silly order on the table (wheels on top!) and talk about what changed.",
         modes=("Partly - point to each part", "Yes", "Yes")),
    # ---------------- Animal Island
    dict(n=7, page=11, ch="animal", title="FIND MY HOME", instr="Help each animal find its home!", skill="match",
         goal="Match animals to habitats; habitat vocabulary", diff="Medium",
         pieces=ids("AN", 1, 6), leo=None,
         guide="Talk about each place: Is it wet or dry? Hot or cold? Many animals can live in more than one kind of place.",
         modes=("Partly - point to each home", "Yes", "Yes")),
    dict(n=8, page=12, ch="animal", title="WHAT DO I EAT?", instr="Draw a line from each animal to its food!", skill="match",
         goal="Match animals with a food they really eat", diff="Medium", pieces=[], leo=None,
         guide="No cutting needed. Each animal eats other foods too - this page shows one favourite. Pets should only eat food made for them.",
         modes=("Yes", "No - no-cut activity", "No")),
    dict(n=9, page=13, ch="animal", title="ANIMAL SHADOW SEARCH", instr="Match each animal to its shadow!", skill="match",
         goal="Visual discrimination: match an outline to a picture", diff="Easy",
         pieces=ids("AN", 1, 6), leo=("leo_surprised", "Who's hiding?"),
         guide="Uses the same animal cards as Mission 07. Look at ears, tails and feet to tell the shadows apart.",
         modes=("Partly - point to each shadow", "Yes", "Yes")),
    dict(n=10, page=14, ch="animal", title="MISSING ANIMAL PARTS", instr="Find the missing part!", skill="build",
         goal="Notice what is missing; animal body-part vocabulary", diff="Easy",
         pieces=ids("AP", 1, 3), leo=None,
         guide="Ask 'What is missing?' before showing the pieces. The dashed lines show where each part goes.",
         modes=("Partly - name the missing part", "Yes", "Yes")),
    dict(n=11, page=15, ch="animal", title="FARMYARD FRIENDS", instr="Put each farm friend in its place!", skill="explore",
         goal="Match farm animals to where they like to be", diff="Easy",
         pieces=ids("FM", 1, 3), leo=None,
         guide="Hens rest in the hen house, pigs cool off in mud and ducks love the pond. Make the animal sounds together!",
         modes=("Partly - point to each place", "Yes", "Yes")),
    dict(n=12, page=16, ch="animal", title="OCEAN EXPLORERS", instr="Place each sea friend in the ocean!", skill="imagine",
         goal="Ocean-animal vocabulary; match shapes to outlines; story play", diff="Easy",
         pieces=ids("OC", 1, 3), leo=None,
         guide="After placing the animals, make up a story: Where is the turtle swimming to?",
         modes=("Partly - point and name", "Yes", "Yes")),
    # ---------------- Number Town
    dict(n=13, page=17, ch="number", title="NUMBER TRAIN", instr="Put the numbers in order, 1 to 10!", skill="count",
         goal="Recognise numerals 1-10 and put them in order", diff="Medium",
         pieces=ids("NU", 1, 10), leo=("leo_happy", "All aboard!"),
         guide="Start with 1 to 5 for younger children. The small grey numbers can be covered with paper for an extra challenge.",
         modes=("Yes - point and count along the train", "Yes", "Yes")),
    dict(n=14, page=18, ch="number", title="COUNT THE BALLOONS", instr="Count the balloons. Find the number!", skill="count",
         goal="Count up to 6 objects and match the quantity to a numeral", diff="Easy",
         pieces=ids("NU", 1, 6), leo=None,
         guide="Touch each balloon once while counting aloud. Uses number cards 1-6 (shared with Missions 13, 16, 18 and 36).",
         modes=("Yes - count with a finger", "Yes", "Yes")),
    dict(n=15, page=19, ch="number", title="FEED THE MONSTER", instr="Give the monster the right number of cookies!", skill="count",
         goal="Count out a set of 2, 3 or 5 objects", diff="Medium",
         pieces=ids("TR", 1, 5), leo=None,
         guide="Play one order at a time. Put the cookies on the plate, count them together, then 'feed' the monster and start again.",
         modes=("Partly - count the cookies on the plate", "Yes", "Yes")),
    dict(n=16, page=20, ch="number", title="LITTLE NUMBER BAKERY", instr="Count the cupcakes. Add the number!", skill="count",
         goal="Count 7 to 10 objects arranged in rows of five", diff="Hard",
         pieces=ids("NU", 7, 10), leo=None,
         guide="Each full row has 5 cupcakes. Count the full row, then keep counting: 'five... six, seven'. Uses number cards 7-10.",
         modes=("Yes - count with a finger", "Yes", "Yes")),
    dict(n=17, page=21, ch="number", title="MORE OR LESS?", instr="Circle the group with MORE!", skill="count",
         goal="Compare two groups and say which has more", diff="Easy", pieces=[], leo=("leo_think", "Which has more?"),
         guide="No cutting needed. Count each side together, or line the pictures up with a finger to compare.",
         modes=("Yes", "No - no-cut activity", "No")),
    dict(n=18, page=22, ch="number", title="BUILD A NUMBER TOWER", instr="Build towers from 1 at the bottom!", skill="build",
         goal="Order numerals from smallest to largest", diff="Hard",
         pieces=ids("NU", 1, 10), leo=None,
         guide="Easier: build only the 1-5 tower (it shows helper dots). Challenge: build the 6-10 tower too.",
         modes=("Yes - point from bottom to top", "Yes", "Yes")),
    # ---------------- Feelings Forest
    dict(n=19, page=23, ch="feelings", title="DRESS FOR THE WEATHER", instr="What should Leo wear today?", skill="sort",
         goal="Connect clothing choices to sunny, rainy and cold weather", diff="Easy",
         pieces=ids("WE", 1, 3), leo=("leo_think", "What should I wear?"),
         guide="Look out of the window together. Which piece would you choose today?",
         modes=("Partly - point to the right clothes", "Yes", "Yes")),
    dict(n=20, page=24, ch="feelings", title="MAKE A HAPPY FACE", instr="Change Leo's eyes and mouth!", skill="imagine",
         goal="Explore how faces can show feelings", diff="Easy",
         pieces=ids("FA", 1, 5), leo=None,
         guide="There is no wrong answer. Try different eyes and mouths and ask 'How might Leo feel now? When do you feel like that?'",
         modes=("Partly - draw features on a copy", "Yes", "Yes")),
    dict(n=21, page=25, ch="feelings", title="HOW DO I FEEL?", instr="Draw a line from each face to a feeling word!", skill="match",
         goal="Name common feelings", diff="Medium", pieces=[], leo=None,
         guide="No cutting needed. Read the words aloud. Faces can mean different things to different people - talk about other ideas too.",
         modes=("Yes", "No - no-cut activity", "No")),
    dict(n=22, page=26, ch="feelings", title="WASH, BRUSH, GET READY!", instr="Put the morning cards in order!", skill="sort",
         goal="Sequence four everyday steps; first / next / last", diff="Medium",
         pieces=ids("RT", 1, 4), leo=None,
         guide="Every family's morning is different. The answer key shows one common order - any order your child can explain is fine.",
         modes=("Partly - point in order", "Yes", "Yes")),
    dict(n=23, page=27, ch="feelings", title="MY TEDDY'S OUTFIT", instr="Dress Teddy for a cosy day out!", skill="imagine",
         goal="Clothing vocabulary; head / body / feet", diff="Easy",
         pieces=ids("TD", 1, 3), leo=None,
         guide="Ask where each piece goes on our own bodies. Teddy can wear anything they like for pretend play too!",
         modes=("Partly - point and name", "Yes", "Yes")),
    dict(n=24, page=28, ch="feelings", title="KINDNESS GARDEN", instr="Draw a line to a kind way to help!", skill="explore",
         goal="Think about kind and helpful actions", diff="Medium", pieces=[], leo=("leo_proud", "Kindness helps us grow!"),
         guide="No cutting needed. Read each situation aloud. Ask: 'What else could we do to help?' - there are many kind answers.",
         modes=("Yes", "No - no-cut activity", "No")),
    # ---------------- Everyday Village
    dict(n=25, page=29, ch="everyday", title="MY LITTLE SUPERMARKET", instr="Put each food on the right shelf!", skill="sort",
         goal="Sort foods into three simple groups", diff="Medium",
         pieces=ids("SM", 1, 6), leo=None,
         guide="Fruit & veg, bakery and dairy are common supermarket groups. Play shop afterwards!",
         modes=("Partly - point to each shelf", "Yes", "Yes")),
    dict(n=26, page=30, ch="everyday", title="PACK MY BACKPACK", instr="Circle the things to take to preschool!", skill="sort",
         goal="Decide which objects are useful for a day out", diff="Easy", pieces=[], leo=("leo_side", "Off we go!"),
         guide="No cutting needed. The bathtub, sofa and piano are silly choices - enjoy the giggles!",
         modes=("Yes", "No - no-cut activity", "No")),
    dict(n=27, page=31, ch="everyday", title="WHAT GOES WHERE?", instr="Find the room for each thing!", skill="sort",
         goal="Match household objects to rooms", diff="Easy",
         pieces=ids("HO", 1, 3), leo=None,
         guide="Walk around your home and find these rooms together.",
         modes=("Partly - point to each room", "Yes", "Yes")),
    dict(n=28, page=32, ch="everyday", title="LITTLE CHEF'S KITCHEN", instr="Follow the recipe to build a sandwich!", skill="build",
         goal="Follow a picture recipe in order (1, 2, 3)", diff="Medium",
         pieces=ids("CH", 1, 3), leo=("leo_happy", "Yum!"),
         guide="Point to each step of the recipe card in order. Afterwards make a real snack together if you like.",
         modes=("Partly - point to each step", "Yes", "Yes")),
    dict(n=29, page=33, ch="everyday", title="ON THE ROAD", instr="Where does each vehicle go?", skill="match",
         goal="Match vehicles to sky, road, railway and water", diff="Easy",
         pieces=ids("VE", 1, 4), leo=None,
         guide="Make the vehicle sounds together! Talk about which vehicles you have seen.",
         modes=("Partly - point to each place", "Yes", "Yes")),
    dict(n=30, page=34, ch="everyday", title="MY DAY, MY WAY", instr="When do you do these? Draw a line!", skill="sort",
         goal="Morning, daytime and evening vocabulary", diff="Medium", pieces=[], leo=None,
         guide="No cutting needed. Every family's day is different - accept any answer your child can explain.",
         modes=("Yes", "No - no-cut activity", "No")),
    # ---------------- Adventure Land
    dict(n=31, page=35, ch="adventure", title="TREASURE MAP MATCH", instr="Put each landmark on the map!", skill="explore",
         goal="Match pictures to outlines on a simple map", diff="Easy",
         pieces=ids("TM", 1, 3), leo=("leo_point", "X marks the spot!"),
         guide="Follow the dotted path with a finger from the bridge to the treasure.",
         modes=("Partly - point to each spot", "Yes", "Yes")),
    dict(n=32, page=36, ch="adventure", title="BUILD A LITTLE CASTLE", instr="Add the roofs, the door and the flag!", skill="build",
         goal="Complete a picture with shape pieces; triangle and arch shapes", diff="Easy",
         pieces=ids("CA", 1, 4), leo=None,
         guide="Name the shapes together: triangle roofs, an arch door, a flag.",
         modes=("Partly - point to each space", "Yes", "Yes")),
    dict(n=33, page=37, ch="adventure", title="WHAT COMES NEXT?", instr="Circle what happens next!", skill="explore",
         goal="Simple visual sequences: first, next, last", diff="Medium", pieces=[], leo=None,
         guide="No cutting needed. Tell each story aloud: 'First... then... next...'.",
         modes=("Yes", "No - no-cut activity", "No")),
    dict(n=34, page=38, ch="adventure", title="NATURE DISCOVERY", instr="Draw a line to the right basket!", skill="sort",
         goal="Sort natural objects: leaves, flowers and stones", diff="Easy", pieces=[], leo=None,
         guide="No cutting needed. On a walk, look at (but do not pick) leaves, flowers and stones together.",
         modes=("Yes", "No - no-cut activity", "No")),
    dict(n=35, page=39, ch="adventure", title="FIND THE PAIRS", instr="Turn over two cards. Do they match?", skill="match",
         goal="Visual memory and turn-taking", diff="Medium",
         pieces=ids("MP", 1, 8), leo=None,
         guide="Start with the cards face-up for younger children. Use only 2 or 3 pairs at first.",
         modes=("No - cards are needed", "Yes", "Optional")),
    dict(n=36, page=40, ch="adventure", title="GRAND FINALE: HELP LEO GET HOME", instr="Finish every stop to get Leo home!", skill="explore",
         goal="Combine colour, shape, counting and picture matching", diff="Medium",
         pieces=["RD5", "SH5", "NU4", "AN4"], leo=("leo_cheer", "Mission complete!"),
         guide="Uses cards from earlier missions: the blue drop (RD5), the star (SH5), number card 4 (NU4) and the penguin (AN4).",
         modes=("Partly - point at each stop", "Yes", "Yes")),
]

MISSION_BY_PAGE = {m["page"]: m for m in MISSIONS}
CHAPTER = {c["key"]: c for c in CHAPTERS}

# ------------------------------------------------------------------------------------------
# Activity data that must stay verifiable
PATTERNS = [  # (sequence shown, answer, choices)
    (["red", "blue", "red", "blue", "red"], "blue", ["green", "blue", "yellow"]),
    (["yellow", "green", "yellow", "green", "yellow"], "green", ["green", "purple", "red"]),
    (["purple", "purple", "orange", "purple", "purple"], "orange", ["blue", "purple", "orange"]),
    (["red", "red", "yellow", "red", "red"], "yellow", ["yellow", "red", "green"]),
    (["blue", "orange", "blue", "orange", "blue"], "orange", ["purple", "red", "orange"]),
    (["green", "green", "purple", "green", "green"], "purple", ["green", "purple", "blue"]),
]

BALLOON_COUNTS = [2, 4, 1, 5, 3, 6]          # Mission 14 -> number cards
CUPCAKE_COUNTS = [7, 10, 8, 9]               # Mission 16 -> number cards
MONSTER_ORDERS = [2, 3, 5]                   # Mission 15 (needs <= 5 cookies)
MORE_LESS = [("apple", 3, 5), ("star_item", 6, 2), ("duck", 4, 1), ("car", 2, 3)]  # (asset, left, right)
FINALE_APPLES = 4

FOODS = [  # Mission 08: animal -> food (accuracy notes in QA report)
    ("panda", "Panda", "bamboo", "bamboo"),
    ("bee", "Bee", "daisy", "flowers"),
    ("penguin", "Penguin", "fish", "fish"),
    ("squirrel", "Squirrel", "acorn", "acorns"),
    ("cow", "Cow", "grass", "grass"),
    ("monkey", "Monkey", "banana", "banana"),
]
FOOD_ORDER = [3, 0, 5, 1, 2, 4]   # right-hand column order (indexes into FOODS)

FEELINGS = [("happy", "happy"), ("sad", "sad"), ("surprised", "surprised"), ("sleepy", "sleepy"), ("cross", "cross"), ("worried", "worried")]
FEELING_ORDER = [2, 4, 0, 5, 1, 3]

KINDNESS = [
    ("k_blocks", "Oh no! The blocks fell down.", "k_tidy", "Help tidy up"),
    ("k_sad", "My friend feels sad.", "k_hug", "Ask 'Are you OK?'"),
    ("k_crayon", "My friend has no crayon.", "k_share", "Share a crayon"),
]
KIND_ORDER = [2, 0, 1]

FLOWERS = ["red", "blue", "yellow", "blue", "red", "yellow"]   # Mission 04 flowers (left to right)
POTS = ["red", "yellow", "blue"]

BACKPACK = [("bottle", "water bottle", True), ("bathtub", "bathtub", False), ("lunchbox", "lunchbox", True), ("book", "book", True),
            ("sofa", "sofa", False), ("sunhat", "sun hat", True), ("piano", "piano", False), ("jumper", "jumper", True)]

DAY = [("breakfast", "breakfast", "morning"), ("slide", "playground", "daytime"), ("bedtime", "bedtime story", "evening"),
       ("park_lunch", "lunch", "daytime"), ("rt_brush", "brushing teeth", "morning or evening")]

SEQUENCES = [  # (first, second, answer, choices)
    ("seed", "sprout", "flower_grown", ["egg", "flower_grown", "moon"]),
    ("egg", "egg_crack", "chick", ["chick", "seed", "blocks_1"]),
    ("blocks_1", "blocks_2", "blocks_3", ["sprout", "night", "blocks_3"]),
    ("sunrise", "sun_high", "night", ["night", "egg_crack", "seed"]),
]

NATURE = [("leaf_green", "leaves"), ("stone_round", "stones"), ("daisy", "flowers"), ("leaf_oak", "leaves"), ("tulip", "flowers"), ("stone_flat", "stones")]
BASKETS = ["leaves", "flowers", "stones"]

COLOUR_WORDS = {"red": "red", "orange": "orange", "yellow": "yellow", "green": "green", "blue": "blue", "purple": "purple"}

NO_CUT_COUNT = sum(1 for m in MISSIONS if not m["pieces"])

ANSWER_SHORT = {
    1: "Each drop to the cloud with the same colour & symbol",
    2: "Each shape to its outline (count corners)",
    3: "Bottom to top: strawberry+chocolate, mint+lemon, blueberry+orange",
    4: "Each flower to the pot with its colour & symbol",
    5: "blue, green, orange, yellow, orange, purple",
    6: "Antenna, head, body, wheels (top to bottom)",
    7: "fish-ocean, cow-farm, monkey-rainforest, penguin-ice, camel-desert, frog-pond",
    8: "panda-bamboo, bee-flowers, penguin-fish, squirrel-acorns, cow-grass, monkey-banana",
    9: "Each animal card to its own shadow",
    10: "rabbit-ears, fox-tail, elephant-trunk",
    11: "hen-hen house, pig-mud, duck-pond",
    12: "Each sea animal to its matching outline",
    13: "1 to 10 along the train",
    14: "2, 4, 1 / 5, 3, 6 balloons",
    15: "Plate holds 2, then 3, then 5 cookies",
    16: "7, 10, 8, 9 cupcakes",
    17: "More: right, left, left, right",
    18: "1–5 and 6–10, smallest at the bottom",
    19: "sunny-sun hat, rainy-rain boots, cold-scarf",
    20: "Any eyes + any mouth – talk about the feeling",
    21: "Match face to word; other ideas welcome",
    22: "Suggested: wake, wash, brush, dress",
    23: "Hat on head, jumper on body, boots on feet",
    24: "blocks-tidy up, sad-ask, no crayon-share",
    25: "F&V: apple, carrot; bakery: bread, croissant; dairy: milk, cheese",
    26: "Take: bottle, lunchbox, book, hat, jumper",
    27: "toothbrush-bathroom, pillow-bedroom, pan-kitchen",
    28: "Bottom to top: bread, lettuce, cheese, tomato, bread",
    29: "plane-sky, car-road, train-railway, boat-water",
    30: "Any explained answer (see answer key)",
    31: "Palm, bridge, lighthouse to their outlines",
    32: "Roofs on towers, flag on wall, door in the arch",
    33: "flower, chick, 3 blocks, night",
    34: "2 leaves, 2 flowers, 2 stones to their baskets",
    35: "Pairs: sun, boat, apple, tulip",
    36: "Blue drop, star, number 4, penguin",
}
