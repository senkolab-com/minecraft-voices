"""Titanic talking NPCs: roles, characters, lines (content only; the engine is talklib.py).

Every speaking NPC is a fictional character (A6). The real people already in the model (Captain Smith, the
officers, Hichens, Fleet, Lee, Rowe, Phillips, Bride, Hartley, Barrett, Bell, Gatti, McElroy, McCawley, Wright,
O'Loughlin) stay silent with their names. The generic crew villagers in the same places are replaced by speakers.
Characters speak as crew on the maiden voyage, at sea after Queenstown: no line mentions the iceberg or the
sinking (A5); facts are about the ship, its people and daily life (sources in titanic_talk_sources.md).
Audio tags in [brackets] direct Eleven v4 and are stripped from the subtitles.
"""

MODEL = 'titanic'

ROLES = {
    'steward': {'label': 'Steward', 'colour': 'gold', 'voice': 'oliver', 'voice_id': 'L1aJrPa7pLJEyYlh3Ilq'},
    'stewardess': {'label': 'Stewardess', 'colour': 'light_purple', 'voice': 'elizabeth', 'voice_id': 'AXdMgz6evoL7OPd7eU12'},
    'stoker': {'label': 'Stoker', 'colour': 'red', 'voice': 'wilf', 'voice_id': 'yZ3w1DL4ZAxIdOscv2t8'},
    'seaman': {'label': 'Seaman', 'colour': 'aqua', 'voice': 'john_ni', 'voice_id': '7uDxvtPDB7zMehaRUyXh'},
}

# ---------------------------------------------------------------- shared line lists (type, text)
LINES_RAW = {
    'steward': [
        ('fact', "[proudly] This ship is two hundred and sixty-nine metres long. That's longer than two and a half football pitches, end to end!"),
        ('fact', "The first-class dining saloon seats almost six hundred people at once. [amused] That is a LOT of soup to carry."),
        ('fact', "We loaded forty thousand fresh eggs before we sailed. Scrambled, fried, boiled... [cheerfully] we are ready for anything!"),
        ('fact', "Our pantries hold forty-four thousand pieces of cutlery. [sighs dramatically] And yes, every single fork has to be polished."),
        ('fact', "We brought twelve hundred quarts of ice cream on board. [conspiratorially] Pudding is taken very seriously on this ship."),
        ('fact', "There are three passenger lifts beside the Grand Staircase for first class, and one for second class. Lifts! On a ship! [excited] The very latest thing."),
        ('fact', "Fancy a swim? There's a saltwater swimming bath down on F deck, seven feet deep. [amazed] A swimming pool, out in the middle of the ocean!"),
        ('fact', "The Turkish bath has a hot room, a warm room and a cooling room. There's even an electric bath. [playfully] Sounds shocking, but it's really just a cabinet full of warm light bulbs."),
        ('fact', "The Café Parisien looks just like a pavement café in Paris, with wicker chairs and climbing ivy. [in a French flourish] Ooh la la!"),
        ('fact', "Our bakers have two hundred and fifty barrels of flour to work with. [delighted] That's a mountain of bread rolls!"),
        ('fact', "We carry over fifty-seven thousand pieces of crockery. If I broke one plate every minute, it would take me forty days to break them all! [quickly] Not that I would, of course."),
        ('fact', "Every first-class cabin has its own electric heater. Passengers just turn a little switch, and [warmly] it's lovely and cosy."),
        ('joke', "Why did the cookie go to see the ship's doctor?... Because it was feeling crummy!"),
        ('joke', "Why did the tomato blush at dinner?... Because it saw the salad dressing!"),
        ('joke', "What do sea monsters like best for dinner?... Fish and ships!"),
        ('joke', "Why don't eggs tell each other jokes? They'd crack each other up! [chuckles] With forty thousand of them on board, the larder is VERY noisy."),
        ('joke', "What's the very best thing to put into a pudding?... Your spoon!"),
        ('joke', "What did one dinner plate say to the other?... Dinner's on me!"),
    ],
    'stewardess': [
        ('fact', "Our Grand Staircase runs from the boat deck down to D deck, under a glass dome. [dreamily] When the sun shines through, it sparkles like a jewel box."),
        ('fact', "At the top of the Grand Staircase there's a carved clock called Honour and Glory Crowning Time. [laughs softly] And still everybody asks me what time it is!"),
        ('fact', "At the foot of the staircase stands a little bronze cherub holding up a lamp. [warmly] The children always give him a wave."),
        ('fact', "First class has four grand parlour suites, each with a sitting room, two bedrooms and a private bathroom. [impressed] Fancy that!"),
        ('fact', "There are a hundred and seven children on this voyage. [cheerfully] So if you hear giggling in the corridors, now you know why!"),
        ('fact', "This ship can carry over three and a half thousand people, passengers and crew together. [amazed] A whole town, floating on the sea."),
        ('fact', "First class even has kennels for the passengers' dogs, up on the boat deck. [playfully] Some of those dogs are better travelled than I am!"),
        ('fact', "Second-class cabins have white walls and mahogany furniture. [proudly] On many other ships, they would count as first class!"),
        ('fact', "The third-class dining saloon seats four hundred and seventy-three people. [happily] Lots of chatter, and plenty of singing."),
        ('fact', "This is a Royal Mail Steamship, that's what the letters R, M, S stand for. Down below, postal clerks sort letters all the way across the ocean."),
        ('fact', "We're carrying more than six million letters and parcels to America. [delighted] That's an awful lot of birthday cards!"),
        ('fact', "The gymnasium has an electric camel! You sit on it, it bumps along, and you pretend you're crossing the desert. [laughs] In the middle of the ocean!"),
        ('fact', "After Southampton we called at Cherbourg in France, then Queenstown in Ireland, and now we're out on the Atlantic, heading for New York."),
        ('joke', "Why did the teddy bear say no to pudding?... Because he was already stuffed!"),
        ('joke', "What's the most musical part of a fish?... The scales!"),
        ('joke', "Why are fish so clever?... Because they live in schools!"),
        ('joke', "What do you call a sleeping dinosaur? A dino-snore! [giggles] I hear plenty of those, tucking passengers in at night."),
        ('joke', "What kind of room has no doors and no windows?... A mushroom!"),
        ('joke', "What kind of key opens a banana?... A mon-key!"),
    ],
    'stoker': [
        ('fact', "Down here we've got twenty-nine boilers with a hundred and fifty-nine furnaces. [excited] And every single one of them is hungry for coal!"),
        ('fact', "This ship burns more than six hundred tonnes of coal a day. [amazed] That's about as heavy as a hundred elephants!"),
        ('fact', "We work in shifts called watches. Four hours on, eight hours off, [cheerfully] then back to the shovel!"),
        ('fact', "Each of these boilers is nearly five metres across and weighs over ninety tonnes. [impressed] That's heavier than fifteen elephants. Each!"),
        ('fact', "We clear away about a hundred tonnes of ash every single day. [laughs] Sweeping up after these fires is a big job!"),
        ('fact', "There are a hundred and seventy-six of us firemen keeping the fires going, [proudly] all day and all night."),
        ('fact', "The trimmers fetch coal from the bunkers in their barrows, so we stokers never run out. [warmly] Teamwork, that is."),
        ('fact', "Our steam drives two giant engines and a turbine, about forty-six thousand horsepower. [amazed] Imagine forty-six thousand horses pulling one ship!"),
        ('fact', "At full steam she does twenty-one knots. That's about thirty-nine kilometres an hour. [proudly] Not bad for something this big!"),
        ('fact', "The steam also spins four big generators. They make electricity for about ten thousand light bulbs all over the ship."),
        ('fact', "People call us the black gang, because the coal dust gets everywhere. [laughs] I wash my face, and the towel turns grey!"),
        ('fact', "Only three of the four funnels carry smoke from our fires. [conspiratorially] The fourth one is mostly for fresh air, to ventilate the ship."),
        ('fact', "The two outside propellers are over seven metres across. [amazed] That's taller than a double-decker bus!"),
        ('joke', "Why did the scarecrow win a prize? Because he was outstanding in his field! [proudly] Me, I'm outstanding in my boiler room."),
        ('joke', "What do you call a pig that does karate?... A pork chop!"),
        ('joke', "Why did the man keep his money in the freezer? He wanted cold, hard cash! [laughs] No chance of freezing anything down here, it's toasty."),
        ('joke', "Why did the bicycle fall over? Because it was two tyred! [sighs] I know just how it feels after a long watch."),
        ('joke', "What do you call a bear with no teeth?... A gummy bear!"),
        ('joke', "Why did the boy take a ladder to school?... Because he wanted to go to high school!"),
    ],
    'seaman': [
        ('fact', "This ship was built in Belfast, at the Harland and Wolff shipyard. [proudly] About fifteen thousand men worked in that yard!"),
        ('fact', "When she was launched, they greased the slipway with twenty-two tonnes of soap and tallow. [excited] She slid into the water in just sixty-two seconds!"),
        ('fact', "A hundred thousand people came to watch her launch, back in May nineteen eleven. [amazed] Biggest crowd I ever saw."),
        ('fact', "Her hull is held together by more than three million rivets. [laughs] Somebody had to hammer in every single one!"),
        ('fact', "Our centre anchor weighs about sixteen tonnes. It took twenty big Clydesdale horses to pull it to the railway station!"),
        ('fact', "The rudder is twenty-four metres tall and weighs over a hundred tonnes. [impressed] Like a door the size of a building!"),
        ('fact', "These funnels are so wide, you could drive a railway train right through one!"),
        ('fact', "The masts stand forty-seven metres tall. [amazed] That's higher than ten double-decker buses stacked up!"),
        ('fact', "Leaving Southampton, we passed so close to another ship, the New York, there was barely a metre between us! [relieved] Phew!"),
        ('fact', "Our wireless men can send Morse code messages over five hundred kilometres. Our call sign is M, G, Y. [playfully] Dot dot dash!"),
        ('fact', "The boat deck is the highest deck for passengers. [contentedly] From up here you can see for miles and miles of sea."),
        ('fact', "In the water, this ship weighs over fifty-two thousand tonnes. [warmly] And still she sits on the sea as proud as a swan."),
        ('fact', "She has ten decks, and eight of them are for passengers. [encouragingly] Go on, explore them all, right down to the boiler rooms!"),
        ('joke', "Why are pirates called pirates?... Because they arrrrr!"),
        ('joke', "What do you call a fish with no eyes?... A fsh!"),
        ('joke', "What's the best way to talk to a fish?... Drop it a line!"),
        ('joke', "Why would the crab never share his sandwich?... Because he was shellfish!"),
        ('joke', "How do seagulls keep up with the news?... They read the tide-ings!"),
        ('joke', "What did the ocean say to the sailor?... Nothing. It just waved!"),
    ],
}

# v2 (Sergey): every fact opens with a "did you know" and every joke with an "I have a funny joke" phrase, in two
# variants per role that alternate; the phrase is recorded as part of each line, so the delivery runs on naturally
PREFIX = {
    'steward': {'fact': ["[curiously] Did you know?", "[proudly] Here's something remarkable."],
                'joke': ["[playfully] I have a funny joke for you!", "[chuckling] Oh, here's one that always gets a laugh!"]},
    'stewardess': {'fact': ["[brightly] Did you know?", "[warmly] Ooh, here's a lovely fact!"],
                   'joke': ["[playfully] I have a funny joke!", "[giggling] Would you like a joke? Here goes!"]},
    'stoker': {'fact': ["[excited] Did you know?", "[cheerfully] Here's a fact for you!"],
               'joke': ["[grinning] I've got a funny joke!", "[cheekily] Want to hear a joke? Here's one!"]},
    'seaman': {'fact': ["[warmly] Did you know?", "[proudly] Now, here's a grand fact for you."],
               'joke': ["[playfully] I have a funny joke for you!", "[chuckling] Here's one my granny used to tell!"]},
}


def _with_prefix(role, lines):
    out, n = [], {'fact': 0, 'joke': 0}
    for typ, text in lines:
        out.append((typ, PREFIX[role][typ][n[typ] % 2] + ' ' + text))
        n[typ] += 1
    return out


LINES = {r: _with_prefix(r, ls) for r, ls in LINES_RAW.items()}

LAUGHS = {
    'steward': ["[laughs heartily] Ha ha ha!", "[chuckles] Oh, that's a good one!", "[laughs] Ha! Very good, very good."],
    'stewardess': ["[giggles] Hee hee hee!", "[laughs] Oh, you are funny!", "[laughs warmly] Ha ha ha!"],
    'stoker': ["[laughs loudly] Ha ha ha ha!", "[chuckles] Heh heh, good one!", "[laughs] Ha! Brilliant!"],
    'seaman': ["[laughs heartily] Ha ha ha!", "[chuckles] Oh, that's a grand one!", "[laughs] Ho ho ho!"],
}

# ---------------------------------------------------------------- the speaking NPCs
# (id, role, name, deck, xr, y, facing, intro) - xr metres aft of the stem, y metres to port(+)/starboard(-) as in
# tpeople.py; groups (2-3, sometimes 4, sometimes alone) are listed together. Placement snaps to a standing cell.
NPCS = [
    # --- boiler rooms and engine room (tank top)
    (1, 'stoker', 'Alfie', 'tank', 75.0, 1.5, '+i', "[cheerfully] Alright? I'm Alfie, a stoker. I'm feeding this furnace, and believe me, she eats more than my whole family put together!"),
    (2, 'stoker', 'Jimmy', 'tank', 76.5, -1.0, '-i', "[brightly] Hello! I'm Jimmy, a stoker. This is my very first voyage, and I've already got coal dust in places I didn't know I had!"),
    (3, 'stoker', 'Fred', 'tank', 93.0, 1.5, '+i', "[warmly] Evening! I'm Fred, a stoker. I'm keeping an eye on the steam gauge. When that needle climbs, we're doing our job right."),
    (4, 'stoker', 'Charlie', 'tank', 94.5, -1.0, '-i', "[playfully] Watch your step! I'm Charlie, a trimmer. I wheel the coal from the bunkers to the furnaces. I must have pushed this barrow halfway to New York already!"),
    (5, 'stoker', 'Billy', 'tank', 110.5, 1.5, '+i', "[cheerfully] Hello there! I'm Billy, a stoker. I'm on the four-to-eight watch, and I'm counting the shovels till supper. Only about three thousand to go!"),
    (6, 'stoker', 'Sam', 'tank', 112.0, -1.0, '-i', "[friendly] Hiya! I'm Sam, a stoker. I'm cleaning out the ash from this fire. Tidy fires burn the brightest, my old dad always said."),
    (7, 'stoker', 'Ted', 'tank', 111.0, 3.0, '-i', "[enthusiastic] Hello! I'm Ted, a stoker. I'm on my break, sort of. I'm teaching Sam a new song to shovel to. It helps keep the rhythm!"),
    (8, 'stoker', 'Harry', 'tank', 128.0, 1.5, '+i', "[proudly] Hello! I'm Harry, a stoker. I've been at sea for ten years, and this is the finest boiler room I've ever worked in."),
    (9, 'stoker', 'Joe', 'tank', 129.5, -1.0, '-i', "[cheerfully] Ey up! I'm Joe, a stoker. I'm checking the fire bars, and keeping my eyebrows well away from the flames!"),
    (10, 'stoker', 'Ned', 'tank', 146.0, 1.5, '+i', "[warmly] Hello, young explorer! I'm Ned, a stoker. I'm the oldest fellow down here, so the lads call me Grandad. I don't mind one bit."),
    (11, 'stoker', 'Davy', 'tank', 147.5, -1.0, '-i', "[brightly] Alright! I'm Davy, a stoker. I'm opening the furnace door just a crack. Ooh, feel that warm glow!"),
    (12, 'stoker', 'Bert', 'tank', 170.0, -3.0, '+j', "[friendly] Hello! I'm Bert, a greaser. I oil the giant engines, so everything runs smooth as butter. I go through buckets of oil!"),
    (13, 'stoker', 'Tommy', 'tank', 171.5, -1.0, '+j', "[excited] Hello there! I'm Tommy, a greaser too. I'm listening to the engines. When they hum just right, it sounds like music to me!"),
    # --- Scotland Road (E deck crew passage)
    (14, 'stoker', 'Jack', 'E', 100.0, -9.7, '-i', "[cheerfully] Hello! I'm Jack, a stoker. I'm heading down to start my watch. This long passage is called Scotland Road, and we walk it every day."),
    (15, 'stoker', 'Walter', 'E', 101.5, -9.7, '+i', "[warmly] Hiya! I'm Walter, a stoker. I've just finished my watch, and I'm off for a wash and a big plate of stew!"),
    # --- first-class dining saloon and reception (D deck)
    (20, 'steward', 'Percy', 'D', 118.0, 0.0, '-i', "[warmly, a little grand] Good evening! I'm Percy, head steward of the dining saloon. I'm checking every table is perfect before the bugle calls for dinner."),
    (21, 'steward', 'Wilfred', 'D', 119.5, 2.0, '+i', "[cheerfully] Hello! I'm Wilfred, a dining saloon steward. I'm folding napkins into little swans. This is my two hundredth one today!"),
    (22, 'steward', 'Cyril', 'D', 120.0, -1.5, '-i', "[friendly] Good evening! I'm Cyril, a steward. I'm laying out the silver, and I'm making sure every spoon can see its own reflection."),
    (23, 'stewardess', 'Mabel', 'D', 108.0, 1.5, '-i', "[warmly] Hello, dear! I'm Mabel, a stewardess. I'm waiting here at the Grand Staircase to help passengers find their way to dinner."),
    (24, 'steward', 'Herbert', 'D', 109.5, -1.0, '+i', "[politely] Good evening! I'm Herbert, a steward in the Reception Room. I'm keeping the band's sheet music in order. It blew all over the place this morning!"),
    # --- Turkish bath and swimming bath (F deck)
    (25, 'steward', 'Stanley', 'F', 99.0, 7.0, '+j', "[calmly] Hello there! I'm Stanley, a bath steward. I'm warming the towels for the Turkish bath. Toasty towels are the secret of a happy passenger."),
    (26, 'steward', 'Leonard', 'F', 97.5, 5.5, '-j', "[cheerfully] Hello! I'm Leonard, the swimming bath steward. I'm checking the water. It's seawater, so don't be surprised if it tastes salty!"),
    # --- grand staircase top / lifts (A deck), reading and writing room
    (27, 'steward', 'Albert', 'A', 92.0, 2.0, '-i', "[brightly] Going down? I'm Albert, a steward, and I run one of the lifts. Up and down, all day long. I'm the only person on board who goes everywhere!"),
    (28, 'stewardess', 'Edith', 'A', 93.5, 0.0, '+i', "[cheerfully] Hello! I'm Edith, a stewardess. I'm taking a breakfast tray up to a lady who loves her toast extra crispy. Very, very crispy!"),
    (29, 'stewardess', 'Florence', 'A', 112.0, 4.0, '-i', "[warmly] Hello! I'm Florence, but everyone calls me Flo. I'm a stewardess, and I'm tidying the Reading and Writing Room. People write so many postcards!"),
    (30, 'stewardess', 'Winifred', 'A', 113.5, 2.5, '+i', "[softly cheerful] Hello! I'm Winifred, a stewardess. I'm sharpening pencils for the writing desks. I've done forty this morning, and I've only snapped two!"),
    # --- first-class cabin corridors (B and C decks)
    (31, 'stewardess', 'Ada', 'B', 75.0, 1.0, '-i', "[friendly] Hello! I'm Ada, a stewardess. I look after twenty cabins on B deck, and I know every passenger's favourite kind of tea."),
    (32, 'stewardess', 'Lily', 'B', 76.5, -0.5, '+i', "[brightly] Hello! I'm Lily, a stewardess. I'm carrying fresh flowers to the parlour suites. These roses came all the way from Southampton!"),
    (33, 'stewardess', 'Elsie', 'C', 128.0, 1.5, '-i', "[cheerfully] Hello! I'm Elsie, a stewardess. I'm turning down the beds for tonight. I fold every sheet into a perfect triangle. Forty beds, forty triangles!"),
    (34, 'stewardess', 'Rose', 'C', 129.5, 0.0, '+i', "[warmly] Hello there! I'm Rose, a stewardess. I'm mending a button on a gentleman's coat. My needle and thread go everywhere with me."),
    # --- second-class (E deck cabins, D deck dining saloon)
    (35, 'stewardess', 'Nellie', 'E', 195.0, 1.0, '-i', "[cheerfully] Hello! I'm Nellie, a second-class stewardess. I'm bringing hot water bottles round. The Atlantic gets chilly at night!"),
    (36, 'stewardess', 'Ivy', 'E', 196.5, -0.5, '+i', "[friendly] Hello! I'm Ivy, a stewardess. I'm helping a family find their cabin. These corridors are long, so I always say, follow the numbers!"),
    (37, 'steward', 'Reginald', 'D', 205.0, 1.5, '-i', "[cheerfully] Good evening! I'm Reginald, a second-class saloon steward. Tonight it's roast turkey, and I've already had a sneaky sniff of the gravy!"),
    (38, 'steward', 'Frank', 'D', 206.5, -1.0, '+i', "[friendly] Hello! I'm Frank, a steward. I'm counting the chairs in the second-class saloon. Three hundred and ninety-four. Every time!"),
    # --- à la carte restaurant (B deck) and smoking room (A deck)
    (39, 'steward', 'Edwin', 'B', 179.0, -8.0, '+j', "[politely] Good evening! I'm Edwin, a waiter in the à la carte restaurant. I'm polishing the glasses until they sparkle like stars."),
    (40, 'steward', 'Arthur', 'B', 177.5, -6.5, '+i', "[cheerfully] Hello! I'm Arthur, a waiter. I'm learning the French names on tonight's menu. Pommes de terre... that just means potatoes!"),
    (41, 'steward', 'Bertie', 'C', 164.0, -8.0, '+j', "[friendly] Hello! I'm Bertie, a steward in the barber's shop. I'm sweeping up the hair. This morning I swept up enough for a whole new moustache!"),
    # --- third class (C deck general room aft)
    (42, 'stewardess', 'Daisy', 'C', 244.0, 3.0, '-i', "[warmly] Hello! I'm Daisy, a third-class stewardess. I'm helping with the sing-song tonight. Somebody brought a fiddle, and somebody brought bagpipes!"),
    (43, 'steward', 'Harold', 'C', 245.5, 1.0, '+i', "[cheerfully] Hello! I'm Harold, a third-class steward. I'm handing out programmes for tonight's music. Everybody's welcome!"),
    # --- outside: forecastle, forward well deck, boat deck, poop
    (50, 'seaman', 'Michael', 'B', 14.0, 1.5, '-i', "[warmly] Hello there! I'm Michael, an able seaman. I'm checking the anchor chains are snug. Each link of that chain is as heavy as a grown man!"),
    (51, 'seaman', 'Thomas', 'B', 15.5, -1.0, '+i', "[cheerfully] Hello! I'm Thomas, a seaman. I'm coiling ropes on the forecastle. A tidy rope is a happy rope, my granny used to say!"),
    (52, 'seaman', 'Francis', 'B', 17.0, 0.5, '-i', "[friendly] Hello! I'm Francis, a seaman. I'm greasing the capstans so the anchors come up nice and smooth."),
    (53, 'seaman', 'Peter', 'C', 48.0, 3.0, '-i', "[cheerfully] Hello! I'm Peter, a seaman. I work the cargo crane in this well deck. Back in Southampton, I lifted a whole motor car on board! Very carefully."),
    (54, 'seaman', 'Daniel', 'C', 49.5, 1.5, '+i', "[warmly] Hello! I'm Daniel, a seaman. I'm painting the railings. It's my favourite job, because you can see the sea the whole time."),
    (55, 'seaman', 'Joseph', 'boat', 70.0, 10.0, '-i', "[friendly] Hello! I'm Joseph, a seaman. I'm polishing the brass on the bridge deck. If the sun catches it right, you can see it from a mile away!"),
    (56, 'seaman', 'Liam', 'boat', 71.5, 8.5, '+i', "[cheerfully] Hello there! I'm Liam, a seaman. I'm scrubbing the boat deck. We scrub it every morning with sand and seawater. It's called holystoning!"),
    (57, 'seaman', 'James', 'boat', 195.0, -10.0, '+i', "[warmly] Hello! I'm James, a seaman. I'm checking the ropes on the boat deck. I learned all my knots from my father, back home in Ireland."),
    (58, 'seaman', 'Kieran', 'boat', 196.5, -8.5, '-i', "[brightly] Hello! I'm Kieran, a seaman. I'm on lookout for whales and dolphins. Keep your eyes open, you never know what might pop up!"),
    (59, 'seaman', 'Conor', 'B', 250.0, 2.0, '-i', "[cheerfully] Hello! I'm Conor, a seaman. I'm raising the flag at the stern. The White Star flag, with its red swallowtail. Isn't she grand?"),
    (60, 'seaman', 'Seán', 'B', 251.5, -1.0, '+i', "[warmly] Hello there! I'm Seán, a seaman. I joined the ship at Queenstown, so I've only been aboard a little while, and I'm still finding my way around!"),
]

# generic crew villagers in npcs.mcfunction replaced by speakers (real, named crew stay as they are)
REPLACE_GENERIC = ['Fireman', 'Trimmer', 'Leading Fireman', 'Greaser', 'Engineer', 'Dining Saloon Steward', 'Head Waiter',
                   'Restaurant Waiter', 'Lift Attendant', 'Turkish Bath Attendant', 'Barber', 'Bosun']

# lines in use (v1, 2026-11-10): Sergey asked to start with half of each role's facts and jokes. Clip names keep the
# full-list index, so the other half is added later by widening this (and generating those clips).
def _half(ls):
    f = [i for i, (t, _) in enumerate(ls) if t == 'fact']
    j = [i for i, (t, _) in enumerate(ls) if t == 'joke']
    return f[:(len(f) + 1) // 2] + j[:len(j) // 2]


ACTIVE = {r: _half(ls) for r, ls in LINES.items()}

# for the second half (Sergey, 2026-11-10): more varied openers ("Fun fact!", "Guess what?", ...), informal ones for the
# stoker and seaman, refined ones for the steward and stewardess; skip the opener on some lines, randomly or where
# the line reads better without one.
