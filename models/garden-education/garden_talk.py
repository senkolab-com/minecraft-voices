"""garden-education: the gardeners. One gardener per bed, each its own role and voice. Every visit: the gardener's
talk about the plant (30-60 s: what it is, sun, water, special care) ending with a joke. All characters are invented.
Facts: see garden_sources.md. Audio tags in [brackets] direct Eleven v4 and are stripped from the subtitles."""

MODEL = 'garden-education'

# role (= bed) -> label, name colour, voice slug, ElevenLabs voice id, villager type
ROLES = {
    'carrot': {'label': 'Carrot Gardener', 'colour': 'gold', 'voice': 'eldrin', 'voice_id': 'LvmvHEBEmMJBJw9UuhwO', 'vtype': 'plains'},
    'cucumber': {'label': 'Cucumber Gardener', 'colour': 'green', 'voice': 'ziggy', 'voice_id': 'fjgAVa6FpNYGo4UpjqML', 'vtype': 'savanna'},
    'tomato': {'label': 'Tomato Gardener', 'colour': 'red', 'voice': 'pixie', 'voice_id': 'z12gfZvqqjJ9oHFbB5i6', 'vtype': 'desert'},
    'onion': {'label': 'Onion Gardener', 'colour': 'yellow', 'voice': 'daniel', 'voice_id': 'htZQqY7WtacRNV7s62Iy', 'vtype': 'taiga'},
    'cacao': {'label': 'Cacao Gardener', 'colour': 'gold', 'voice': 'summer', 'voice_id': 'Oqy85UMasXzUjUxF0ta5', 'vtype': 'jungle'},
    'rice': {'label': 'Rice Farmer', 'colour': 'aqua', 'voice': 'lee', 'voice_id': '7QwDAfHpHjPD14XYTSiq', 'vtype': 'swamp'},
    'blueberry': {'label': 'Blueberry Gardener', 'colour': 'blue', 'voice': 'jayjay', 'voice_id': 'nuNMqNdrDex14QQRI9Jq', 'vtype': 'snow'},
    'strawberry': {'label': 'Strawberry Gardener', 'colour': 'light_purple', 'voice': 'daisy', 'voice_id': 'DVP0tUPMxAGcT3nZxz0b', 'vtype': 'plains'},
}

# id, role, name, profession, talk
NPCS = [
    (1, 'carrot', 'Grandpa Rootley', 'farmer',
     "[warmly] Hello there, young gardener! I'm Grandpa Rootley, and these are my carrots. The feathery green leaves are only the top. "
     "The carrot itself is hiding underground! [curious] Carrots love full sun, at least six hours a day, and soft, loose soil with no stones. "
     "If a growing carrot bumps into a stone, it can grow crooked, or even split into two legs! I water them gently once or twice a week, "
     "so the soil stays damp but never soggy. The seeds are tiny, so they come up crowded, and I pull some out to give the others room to grow big. "
     "After about ten to twelve weeks, they're ready to pull. [amazed] And long ago, most carrots were purple or yellow, not orange! "
     "[chuckles] Now, a riddle for you. What's orange, and sounds like a parrot? ... A carrot!"),
    (2, 'cucumber', 'Cooper Crisp', 'farmer',
     "[excited] G'day! I'm Cooper Crisp, and welcome to my cucumber patch! Cucumbers are climbers. Their curly little tendrils grab onto this trellis "
     "and pull the vine up towards the sunshine. They love heat and full sun, so we only plant them once the weather is properly warm. "
     "And they are THIRSTY! A cucumber is about ninety-five percent water, so the vines need a good deep drink, especially on hot days, "
     "or the cucumbers can taste bitter. See the yellow flowers? Bees carry pollen from flower to flower, and the flowers they visit grow into cucumbers. "
     "Pick them often, and the plant keeps making more! [laughs] Oh, and a joke. Why did the cucumber need a lawyer? ... Because it was in a pickle!"),
    (3, 'tomato', 'Rosie Redfield', 'farmer',
     "[cheerfully] Hi! I'm Rosie Redfield, and these are my tomatoes! Here's a surprise: a tomato is actually a fruit, because it grows from a flower "
     "and has seeds inside. Tomatoes are sun-lovers. They need six to eight hours of sunshine every day, and warm nights too. "
     "I water them deeply at the bottom, near the roots, not on the leaves, because wet leaves can catch plant diseases. "
     "Tomato plants grow tall and floppy, so I tie each one to a wooden stake to hold it up when it gets heavy with fruit. "
     "The tomatoes start green, and turn red as they ripen in the sun. [giggles] Want a joke? Why did the tomato turn red? ... Because it saw the salad dressing!"),
    (4, 'onion', 'Ollie Layers', 'farmer',
     "[warmly, unhurried] Hello, hello! I am Ollie Layers, keeper of the onions. An onion is a bulb, and it grows half hidden in the soil. "
     "Inside, it is made of many layers, one inside the other, like a set of little jackets. [thoughtfully] Onions like full sun, "
     "and soil that drains well. They do not like sitting in puddles! I water them regularly while the bulbs are growing. "
     "But when the green leaves flop over and turn yellow, I stop watering, because that means the onion is nearly ready. "
     "Then I pull them up and dry them in the sun for a week or two, so they keep for months. And why do onions make you cry when you cut them? "
     "They release a special gas to protect themselves! [chuckles] And now my joke. Why did the onion win the talent show? ... Because it brought the whole audience to tears!"),
    (5, 'cacao', 'Doctor Coco Bromley', 'farmer',
     "[warmly] Welcome to the warmest corner of the garden! I'm Doctor Coco Bromley, and this is my cacao, the tree that gives us chocolate! "
     "Cacao trees only grow in hot, rainy places near the equator, so in this greenhouse we keep them warm and damp all year round. "
     "Cacao actually likes a little shade. In the rainforest, it grows under taller trees that protect it from strong sun and wind. "
     "It needs moist soil, but never a flood. [amazed] Now look at the trunk! The flowers and pods grow straight out of the trunk and the thick branches. "
     "Each tiny flower is pollinated by a midge, a fly no bigger than a pinhead. A pod takes about five to six months to ripen, "
     "and inside are thirty or forty beans, wrapped in sweet white pulp. [giggles] And my joke! What did the cacao tree say to the chocolate bar? ... I'm so proud of how sweet you turned out!"),
    (6, 'rice', 'Lin Greenwater', 'farmer',
     "[cheerfully] Hello, hello! I'm Lin Greenwater, and this muddy pool is my rice paddy. Rice is a kind of grass, and its seeds are the rice grains we eat. "
     "More than half the people in the world eat rice almost every day! Rice loves warm weather and lots of sunshine. "
     "And here's what makes it special: many farmers grow it in fields flooded with shallow water, just like this one. "
     "Rice is happy with its feet in water, but most weeds are not, so the water helps keep the weeds away. "
     "When the grains are ripe, the heavy heads droop down, and the farmer drains the water so the field can dry out for the harvest. "
     "From planting to harvest takes about four to six months. [laughs] Now, a joke for you! Why is rice so polite? ... Because when it's ripe, it always takes a bow!"),
    (7, 'blueberry', 'Barney Blue', 'farmer',
     "[friendly] Hey there! I'm Barney Blue, and these bushes are my blueberries. Blueberries are a bit fussy about their soil. "
     "They like it acidic, a bit like the soil in a pine forest, so I mix in pine needles and bark to keep them happy. "
     "They want lots of sun, at least six hours a day. Their roots are shallow, so they dry out quickly. I water them often, "
     "and spread mulch on top to keep the soil cool and damp. Their flowers look like tiny white bells, and the bees that visit them make the berries grow. "
     "Here's a gardener's trick: plant two different kinds of blueberry near each other, and you'll get more and bigger berries. "
     "And I put nets over them, because birds love blueberries as much as we do! [laughs] Joke time! Why was the blueberry sad? ... Because it was feeling a little bit blue!"),
    (8, 'strawberry', 'Daisy Strawbridge', 'farmer',
     "[sweetly] Oh, hello! I'm Daisy Strawbridge, and welcome to my strawberry patch! Did you know a strawberry wears its seeds on the outside? "
     "There are about two hundred on every berry! Strawberries love sunshine, at least six hours a day, and soil that's damp but not soggy. "
     "I water them in the morning, right at the roots. See the straw under the plants? Gardeners tuck straw around them, "
     "so the berries stay clean and dry, and don't go mouldy sitting on wet soil. Strawberry plants also send out long runners: "
     "little stems with baby plants on the end, which put down roots and grow into new strawberry plants all by themselves! "
     "When the berries are bright red all over, they're ready to pick. [giggles] And my joke! What did one strawberry say to the other? ... If you weren't so sweet, we wouldn't be in this jam!"),
]

LINES = {r: [] for r in ROLES}      # no extra lines: every visit is the full talk
LAUGHS = {r: [] for r in ROLES}
