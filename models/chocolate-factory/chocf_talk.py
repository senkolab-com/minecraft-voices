"""chocolate-factory: the tour guides. One guide per place, each its own role with its own (fancy) voice.
First meeting: the guide's story of the place (what it is and what happens there). Later visits: the guide's
other lines in turn (chocolate facts and a joke). All characters are invented. Facts: see chocf_sources.md.
Audio tags in [brackets] direct Eleven v4 and are stripped from the subtitles."""

MODEL = 'chocolate-factory'

# role -> label, name colour, voice slug, ElevenLabs voice id (None until Sergey picks the voices)
ROLES = {
    'gate': {'label': 'Gatekeeper', 'colour': 'gold', 'voice': 'tarquin', 'voice_id': '7cOBG34AiHrAzs842Rdi'},
    'fountain': {'label': 'Fountain Fairy', 'colour': 'light_purple', 'voice': 'flicker', 'voice_id': 'piI8Kku0DcvcL6TTSeQt'},
    'roast': {'label': 'Roastmaster', 'colour': 'gold', 'voice': 'cornelius', 'voice_id': '6sFKzaJr574YWVu4UuJF'},
    'mix': {'label': 'Mixing Master', 'colour': 'aqua', 'voice': 'drvon', 'voice_id': 'yjJ45q8TVCrtMhEKurxY'},
    'taste': {'label': 'Chief Taster', 'colour': 'light_purple', 'voice': 'lucy', 'voice_id': 'k9kFjM4M02PYt2PvKMYq'},
    'clock': {'label': 'Clockkeeper', 'colour': 'yellow', 'voice': 'pip', 'voice_id': 'jcm0A25XPeyOWvAQUhFK'},
    'caramel': {'label': 'Keeper of the Tower', 'colour': 'gold', 'voice': 'verity', 'voice_id': 'oW8bn5YtBB89X2nJ0DT9'},
    'garden': {'label': 'Head Gardener', 'colour': 'green', 'voice': 'beezle', 'voice_id': 'BBfN7Spa3cqLPH1xAS22'},
    'wrap': {'label': 'Mistress of Wrapping', 'colour': 'light_purple', 'voice': 'annabel', 'voice_id': 'rWArYo7a2NWuBYf5BE4V'},
    'lookout': {'label': 'Lookout Keeper', 'colour': 'aqua', 'voice': 'vedasky', 'voice_id': 'IR4Yywb88oVWHqzWLjAs'},
}

# id, role (= place), name, profession (villager look), story (first meeting)
NPCS = [
    (1, 'gate', 'Sir Percival Toffeeworth', 'cartographer',
     "[grandly] Welcome, welcome, WELCOME to the Cocoa Clockworks! I am Sir Percival Toffeeworth, keeper of this gingerbread gate. "
     "Every visitor starts their tour right here. Inside, you will find the Great Hall where chocolate is roasted, melted and moulded, "
     "the Caramel Tower, the Cocoa Conservatory, the Fudge Fountain and the Wrapping Hall. [conspiratorially] And do pop into the ticket booth. "
     "No tickets needed today... I simply like the look of it!"),
    (2, 'fountain', 'Pippa Sprinkle', 'cleric',
     "[sparkling] Ooh, hello! I'm Pippa Sprinkle, the Fountain Fairy! This is the Fudge Fountain, the beating heart of our courtyard. "
     "Every morning I make sure the fudge flows round and round, smooth and shiny. [giggles] The lollipop trees all around are my little garden. "
     "I polish every lollipop by hand. Well... by wand!"),
    (3, 'roast', 'Professor Bartholomew Bean', 'librarian',
     "[warmly, like a wise old storyteller] Ah, a visitor! I am Professor Bartholomew Bean, the Roastmaster. This is the Roasting Room, "
     "where every bar of chocolate begins its journey. The cocoa beans arrive in those big sacks, ride along the conveyor, and tumble into the roasters. "
     "Roasting brings out their deep chocolatey smell. [sniffs happily] Then the grinding stones crack them into little pieces called nibs. "
     "The stairs at the far end lead up to the Melting Room."),
    (4, 'mix', 'Doctor Fizzlewick', 'cleric',
     "[excited, quirky] Aha! A new assistant! I'm Doctor Fizzlewick, Mixing Master of the Melting and Mixing Room. "
     "These six great copper vats hold rivers of melted chocolate. The paddles stir it for hours and hours, which makes it silky smooth. "
     "[proudly] Milk, sugar, a pinch of this, a dash of that... my recipes are top secret! Mostly because I forget them myself."),
    (5, 'taste', 'Madame Cordelia Truffle', 'cleric',
     "[elegantly] Good day, darling. I am Madame Cordelia Truffle, Chief Taster. Up here in the Moulding and Tasting Room, the chocolate is poured into moulds, "
     "rides through the cooling tunnel, and comes out as perfect, shiny bars. [delighted] And then... I taste them. Every single one. "
     "It's a very serious job. Someone has to do it! The ladder in the middle of the room climbs up to the Clock Room."),
    (6, 'clock', 'Tobias Tick', 'toolsmith',
     "[cheerfully absent-minded] Oh! Hello there! Tobias Tick, Clockkeeper, at your service! You're inside the great clock of the Cocoa Clockworks. "
     "These golden gears turn the hands you can see from the courtyard. [proudly] The whole factory runs on this clock: when to roast, when to stir, when to cool. "
     "Chocolate is all about perfect timing, you know. Tick... tock... TASTE!"),
    (7, 'caramel', 'Clementine Caramel', 'farmer',
     "[bubbly, chatty] Hiya! I'm Clementine Caramel, Keeper of the Caramel Tower! Down here is my caramel kitchen, where sugar bubbles in the cauldrons "
     "until it turns golden brown. [excited] Climb the spiral stairs all the way to the lookout at the top, the best view on the island! "
     "Halfway up there's a door to the Bonbon Bridge, where the sweets ride across to the Great Hall in a glass tunnel."),
    (8, 'garden', 'Old Rowan Greenleaf', 'farmer',
     "[softly, wise and kind] Welcome, little traveller. I am Rowan Greenleaf, Head Gardener of the Cocoa Conservatory. "
     "Under this glass dome it is always warm and damp, just like a tropical rainforest, because that is where cacao trees love to grow. "
     "[warmly] See those pods hanging right from the trunks? Inside every pod are the beans that become chocolate. Everything in this factory starts right here."),
    (9, 'wrap', 'Lady Ribbonsworth', 'shepherd',
     "[elegantly, with a flourish] Enchantée! I am Lady Ribbonsworth, Mistress of Wrapping. This is the Wrapping Hall, the last stop of every chocolate. "
     "At these long tables, each bar is wrapped in shiny paper, tied with ribbon and packed into gift boxes. [proudly] The chests by the wall are ready to be sent "
     "all around the world. A present is not finished until it has a bow!"),
    (10, 'lookout', 'Captain Skye Meringue', 'cartographer',
     "[breathless, delighted] Phew! You climbed all those stairs? Well done! I'm Captain Skye Meringue, Lookout Keeper of the Caramel Tower. "
     "This is the highest floor on the whole island. [excited] Look around! There's the Great Hall with its three candy chimneys, the glass dome of the Cocoa Conservatory, "
     "the Fudge Fountain down in the courtyard, and the Wrapping Hall by the gate. [proudly] From up here I keep watch for ships bringing cocoa beans across the sea. "
     "And the yellow ribbon spiralling round the tower? That's the slide!"),
]

# each guide's other lines, told one per later visit, in turn (type, text)
LINES = {
    'gate': [
        ('fact', "[grandly] Did you know? The cacao tree's scientific name is Theobroma cacao, which means 'food of the gods'. Quite right too!"),
        ('fact', "[proudly] Hundreds of years ago, the Aztecs used cacao beans as money. Imagine paying for your lunch with chocolate beans!"),
        ('joke', "[playfully] I have a jolly joke for you! Why did the chocolate bar go to school? ... To become a smarty-pants!"),
    ],
    'fountain': [
        ('fact', "[sparkling] Guess what? Fudge was invented in America in the eighteen-eighties, and some say it began as a cooking mistake. A very tasty mistake!"),
        ('fact', "[excited] Fun fact! Chocolate melts at about thirty-four degrees, just below the temperature inside your mouth. That's why it melts on your tongue!"),
        ('joke', "[giggling] Ooh, here's a funny one! What did the fudge say to the fountain? ... Stop going round in circles, you're making me melt!"),
    ],
    'roast': [
        ('fact', "[wisely] Did you know? Before the beans come to me, they are fermented for about a week and dried in the sun. That's where much of the flavour comes from."),
        ('fact', "[warmly] A curious fact: the shells around the beans are blown away by a fan in a step called winnowing, leaving just the little nibs."),
        ('joke', "[chuckling] Here is a joke I have told for fifty years. What do you call a cocoa bean that tells jokes? ... A real roast!"),
    ],
    'mix': [
        ('fact', "[excitedly] Did you know? In eighteen seventy-nine, a Swiss chocolate maker called Rodolphe Lindt invented conching, stirring chocolate for hours to make it smooth. Like my paddles!"),
        ('fact', "[proudly] Fact! Milk chocolate was first made in Switzerland in eighteen seventy-five, by Daniel Peter. Before that, chocolate was mostly dark and a bit bitter."),
        ('joke', "[cackling happily] Joke time! Why was the chocolate vat so calm? ... Because it always kept stirring its problems away!"),
    ],
    'taste': [
        ('fact', "[elegantly] Did you know, darling? Tempering, warming and cooling chocolate very carefully, is what gives a bar its shine and that lovely SNAP."),
        ('fact', "[delighted] A little secret: white chocolate has no cocoa solids at all. It is made from cocoa butter, sugar and milk. Scandalous, but delicious!"),
        ('joke', "[amused] I have a funny joke for you. What is a chocolate's favourite kind of music? ... Rock and roll... because it loves being ROLLED into truffles! Oh, I do crack myself up."),
    ],
    'clock': [
        ('fact', "[cheerfully] Did you know? The world's first chocolate bar to eat, rather than drink, was made in England in eighteen forty-seven. Before that, chocolate was a drink!"),
        ('fact', "[excitedly] Tick-tock fact! When chocolate cools too quickly, it can turn dull and stripy. So timing really is everything up here!"),
        ('joke', "[giggling] Joke o'clock! Why did the boy eat his homework? ... Because his teacher said it was a piece of cake! ... Wait, wrong factory."),
    ],
    'caramel': [
        ('fact', "[chatty] Fun fact! When sugar is heated to about one hundred and seventy degrees, it melts and turns golden. That's caramel! Too hot to touch though."),
        ('fact', "[excited] Guess what? Toffee and soft caramels are cousins. Toffee is cooked longer and hotter, so it goes hard and crunchy, while soft caramels stay chewy."),
        ('joke', "[laughing] Here's a funny one! Why did the caramel get a medal? ... Because it was so out-STANDING at sticking around!"),
    ],
    'garden': [
        ('fact', "[softly] Did you know? Cacao trees only grow in warm, rainy places near the equator, like West Africa and South America."),
        ('fact', "[wisely] A small wonder: cacao flowers are pollinated by tiny flies called midges, no bigger than a pinhead. Without them, there would be no chocolate."),
        ('joke', "[chuckling gently] I have a little joke. Why don't cacao trees ever get lost? ... Because they always stick to their roots!"),
    ],
    'wrap': [
        ('fact', "[elegantly] Did you know? Decorated chocolate boxes became popular in Victorian England, in the eighteen-sixties. People kept the pretty boxes long after the chocolates were gone."),
        ('fact', "[proudly] A wrapping fact: shiny foil keeps chocolate fresh, because it stops air, light and smells from getting in. A wrapper is a little suit of armour!"),
        ('joke', "[playfully] I have a funny joke for you! What did one gift box say to the other? ... You're so well WRAPPED up in yourself!"),
    ],
    'lookout': [
        ('fact', "[excited] Did you know? Most of the world's cocoa beans grow in West Africa, and they travel to chocolate makers by ship, packed in big sacks, just like the ones in our Roasting Room."),
        ('fact', "[amazed] Guess what? It takes about four hundred cocoa beans to make just one pound of chocolate. That's a lot of beans for one big bar!"),
        ('joke', "[giggling] Here's my favourite joke! Why is it never lonely up here at the lookout? ... Because the seagulls are always DROPPING by!"),
    ],
}

LAUGHS = {r: [] for r in ROLES}
