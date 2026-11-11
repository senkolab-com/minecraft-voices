"""garden-education: a small teaching garden on a grassy island ("Garden School").

Concept coordinates as in the other island models: x 0..NX-1 east, z 0..NZ-1 south (the entrance arch is on the
south edge), y up with y = 0 the grass surface; island bottom y = -6, sea level y = -1 (world 62).
Eight beds (7 x 3 soil inside a spruce border, raised one block) each ringed by a path the gardener strolls on.
Plants that exist in Minecraft are real blocks (carrots, cocoa); the others are item_display models (see models.py).
"""
import math
import numpy as np

NX, NZ = 78, 62
Y0, Y1 = -6, 16
NY = Y1 - Y0 + 1

ROW_A, ROW_B = 18, 36
BEDS = [  # kind, centre x, centre z
    ('carrot', 14, ROW_A), ('cucumber', 28, ROW_A), ('tomato', 50, ROW_A), ('cacao', 64, ROW_A),
    ('onion', 14, ROW_B), ('rice', 28, ROW_B), ('blueberry', 50, ROW_B), ('strawberry', 64, ROW_B),
]
TITLES = {
    'carrot': ('CARROTS', 'Root vegetable · loose, stone-free soil'),
    'cucumber': ('CUCUMBERS', 'Climbing vine · warm sun, lots of water'),
    'tomato': ('TOMATOES', 'A fruit! · staked up, 6-8 hours of sun'),
    'onion': ('ONIONS', 'Bulb in layers · well-drained soil'),
    'cacao': ('CACAO', 'The chocolate tree · warm, damp, a little shade'),
    'rice': ('RICE', 'A grass grown in water · flooded paddy'),
    'blueberry': ('BLUEBERRIES', 'Bush berries · acidic soil'),
    'strawberry': ('STRAWBERRIES', 'Seeds on the outside · straw keeps them clean'),
}
SOIL = {'cucumber': 'minecraft:dirt', 'tomato': 'minecraft:dirt', 'onion': 'minecraft:coarse_dirt',
        'blueberry': 'minecraft:podzol[snowy=false]', 'strawberry': 'minecraft:dirt'}


class M:
    def __init__(self):
        self.g = np.zeros((NX, NY, NZ), np.int32)
        self.pal = ['air']
        self.idx = {'air': 0}
        self.labels = []          # (x, y, z, title, sub, facing)
        self.signs = []           # (x, y, z, state, lines)  standing or wall signs with text
        self.walks = {}           # kind -> [4 corners (x, y, z)] the gardener's loop
        self.plants = []          # (x, y, z, model, yaw, scale)  item_display plants
        self.repair = []          # (x0, x1, y, z0, z1, state, replace)  re-placed every few seconds

    def b(self, name):
        if name not in self.idx:
            self.idx[name] = len(self.pal)
            self.pal.append(name)
        return self.idx[name]

    def put(self, x, y, z, name):
        if 0 <= x < NX and Y0 <= y <= Y1 and 0 <= z < NZ:
            self.g[x, y - Y0, z] = self.b(name)

    def get(self, x, y, z):
        if 0 <= x < NX and Y0 <= y <= Y1 and 0 <= z < NZ:
            return self.pal[self.g[x, y - Y0, z]]
        return 'air'

    def box(self, x0, x1, y0, y1, z0, z1, name):
        x0, x1 = sorted((x0, x1)); y0, y1 = sorted((y0, y1)); z0, z1 = sorted((z0, z1))
        x0, z0, y0 = max(x0, 0), max(z0, 0), max(y0, Y0)
        x1, z1, y1 = min(x1, NX - 1), min(z1, NZ - 1), min(y1, Y1)
        if x0 <= x1 and y0 <= y1 and z0 <= z1:
            self.g[x0:x1 + 1, y0 - Y0:y1 - Y0 + 1, z0:z1 + 1] = self.b(name)

    def sphere(self, cx, cy, cz, r, name, cond=None):
        for x in range(int(cx - r - 1), int(cx + r + 2)):
            for y in range(int(cy - r - 1), int(cy + r + 2)):
                for z in range(int(cz - r - 1), int(cz + r + 2)):
                    if math.dist((x, y, z), (cx, cy, cz)) <= r and (cond is None or cond(x, y, z)):
                        self.put(x, y, z, name)

    def label(self, x, y, z, title, sub):
        self.labels.append((x, y, z, title, sub, 'south'))

    def sign(self, x, y, z, state, lines):
        self.put(x, y, z, state)
        self.signs.append((x, y, z, state, lines))


B = {
    'grass': 'minecraft:grass_block[snowy=false]', 'dirt': 'minecraft:dirt', 'sand': 'minecraft:sand',
    'path': 'minecraft:dirt_path', 'border': 'minecraft:spruce_planks', 'mud': 'minecraft:mud',
    'water': 'minecraft:water[level=0]', 'glass': 'minecraft:glass', 'frame': 'minecraft:white_concrete',
    'moss': 'minecraft:moss_block', 'log': 'minecraft:jungle_log[axis=y]',
    'leaves': 'minecraft:jungle_leaves[persistent=true,distance=1,waterlogged=false]',
    'oaklog': 'minecraft:oak_log[axis=y]', 'oakleaves': 'minecraft:oak_leaves[persistent=true,distance=1,waterlogged=false]',
    'spruce': 'minecraft:spruce_planks', 'slog': 'minecraft:spruce_log[axis=y]', 'stone': 'minecraft:stone_bricks',
    'cobble': 'minecraft:mossy_cobblestone', 'lantern': 'minecraft:lantern[hanging=false,waterlogged=false]',
    'hlantern': 'minecraft:lantern[hanging=true,waterlogged=false]', 'fence': 'minecraft:spruce_fence[east=false,north=false,south=false,west=false,waterlogged=false]',
    'hay': 'minecraft:hay_block[axis=y]', 'pumpkin': 'minecraft:carved_pumpkin[facing=south]',
    'barrel': 'minecraft:barrel[facing=up,open=false]', 'composter': 'minecraft:composter[level=4]',
    'table': 'minecraft:crafting_table', 'chest': 'minecraft:chest[facing=south,type=single,waterlogged=false]',
    'fern': 'minecraft:fern', 'carrots': 'minecraft:carrots[age=7]', 'farmland': 'minecraft:farmland[moisture=7]',
    'hidden_water': 'minecraft:spruce_slab[type=top,waterlogged=true]',
}


def stairs(mat, facing, half='bottom'):
    return f'minecraft:{mat}_stairs[facing={facing},half={half},shape=straight,waterlogged=false]'


def door(m, x, y, z, facing, wood='spruce', hinge='left'):
    m.put(x, y, z, f'minecraft:{wood}_door[facing={facing},half=lower,hinge={hinge},open=false,powered=false]')
    m.put(x, y + 1, z, f'minecraft:{wood}_door[facing={facing},half=upper,hinge={hinge},open=false,powered=false]')


def standing_sign(m, x, y, z, lines, rotation=0):
    m.sign(x, y, z, f'minecraft:oak_sign[rotation={rotation},waterlogged=false]', lines)


# ------------------------------------------------------------------ island
def island(m):
    for x in range(NX):
        for z in range(NZ):
            dx = max(0, 12 - x, x - (NX - 13))
            dz = max(0, 12 - z, z - (NZ - 13))
            d = math.hypot(dx, dz)
            if d <= 8:
                m.box(x, x, -6, -1, z, z, B['dirt'])
                m.put(x, 0, z, B['grass'] if d <= 6 else B['sand'])
                if d > 6:
                    m.put(x, -1, z, B['sand'])
            elif d <= 10.5:
                m.box(x, x, -6, -2, z, z, 'minecraft:sandstone')
                m.put(x, -1, z, B['sand'])


def ring(m, cx, cz, kind):
    for x in range(cx - 5, cx + 6):
        for z in range(cz - 3, cz + 4):
            if abs(x - cx) == 5 or abs(z - cz) == 3:
                m.put(x, 0, z, B['path'])
    m.walks[kind] = [(cx - 5, 1, cz + 3), (cx + 5, 1, cz + 3), (cx + 5, 1, cz - 3), (cx - 5, 1, cz - 3)]


def bed(m, kind, cx, cz):
    import layout
    ring(m, cx, cz, kind)
    m.box(cx - 4, cx + 4, 1, 1, cz - 2, cz + 2, B['border'])
    m.box(cx - 4, cx + 4, 0, 0, cz - 2, cz + 2, B['dirt'])
    x0, x1, z0, z1 = cx - 3, cx + 3, cz - 1, cz + 1
    if kind == 'carrot':
        m.box(x0, x1, 1, 1, z0, z1, B['farmland'])
        m.box(x0, x1, 2, 2, z0, z1, B['carrots'])
        m.put(cx, 1, cz - 2, B['hidden_water']); m.put(cx, 1, cz + 2, B['hidden_water'])    # keeps the farmland wet
        m.repair += [(x0, x1, 1, z0, z1, B['farmland'], 'minecraft:dirt'), (x0, x1, 2, z0, z1, B['carrots'], 'minecraft:air')]
    elif kind == 'rice':
        m.box(x0, x1, 0, 0, z0, z1, B['mud'])
        m.box(x0, x1, 1, 1, z0, z1, B['water'])
    else:
        m.box(x0, x1, 1, 1, z0, z1, SOIL[kind])
    if kind == 'cucumber':                      # the trellis's end posts
        for x in (cx - 4, cx + 4):
            m.box(x, x, 2, 3, cz, cz, B['fence'])
    base = 1 if kind == 'rice' else 2
    for (dx, dz, model, yaw, s) in layout.bed_plants(kind):
        y = 2 if model == 'carrot_pulled' else base
        m.plants.append((cx + dx, y, cz + dz, model, yaw, s))
    t, sub = TITLES[kind]
    m.label(cx, 3.5, cz, t, sub)
    standing_sign(m, cx + (1 if kind == 'cucumber' else 0), 2, cz + 2, ['', t.title(), '', ''])
    if kind == 'cucumber':
        pass


def greenhouse(m, cx, cz):
    """the cacao bed inside a small glass house (warm and damp), the gardener's loop inside the walls."""
    x0, x1, z0, z1 = cx - 6, cx + 6, cz - 4, cz + 4
    m.box(x0, x1, 0, 0, z0, z1, B['moss'])
    for y in range(1, 6):
        for x in range(x0, x1 + 1):
            for z in (z0, z1):
                m.put(x, y, z, B['glass'])
        for z in range(z0, z1 + 1):
            for x in (x0, x1):
                m.put(x, y, z, B['glass'])
    for (x, z) in ((x0, z0), (x0, z1), (x1, z0), (x1, z1)):
        m.box(x, x, 1, 5, z, z, B['frame'])
    for x in (x0, x1):
        m.box(x, x, 6, 9, cz, cz, B['frame'])
    # gable roof along x
    for (y, dz) in ((6, 4), (6, 3), (7, 2), (8, 1), (9, 0)):
        for s in (-1, 1):
            m.box(x0, x1, y, y, cz + s * dz, cz + s * dz, B['glass'])
    for (y, dz) in ((6, 4), (7, 3), (8, 2)):        # the end walls of the gable
        for x in (x0, x1):
            m.box(x, x, y, y, cz - dz + 1, cz + dz - 1, B['glass'])
    m.box(x0, x1, 9, 9, cz, cz, B['frame'])          # ridge
    m.box(x0, x1, 5, 5, z0, z0, B['frame']); m.box(x0, x1, 5, 5, z1, z1, B['frame'])
    ring(m, cx, cz, 'cacao')
    m.box(cx - 4, cx + 4, 1, 1, cz - 2, cz + 2, B['border'])
    m.box(cx - 3, cx + 3, 1, 1, cz - 1, cz + 1, B['moss'])
    # two cacao trees: trunks with pods, leafy crowns under the roof
    for tx in (cx - 2, cx + 2):
        m.box(tx, tx, 2, 5, cz, cz, B['log'])
        for (dx, dz, f) in ((1, 0, 'west'), (-1, 0, 'east'), (0, 1, 'north'), (0, -1, 'south')):
            for yy in (2, 4):
                if m.get(tx + dx, yy, cz + dz) == 'air':
                    m.put(tx + dx, yy, cz + dz, f'minecraft:cocoa[age={2 if yy == 2 else 1},facing={f}]')
        for x in range(tx - 2, tx + 3):
            for z in range(cz - 2, cz + 3):
                for y in (6, 7):
                    if (abs(x - tx) + abs(z - cz) <= (3 if y == 6 else 1)) and m.get(x, y, z) == 'air':
                        m.put(x, y, z, B['leaves'])
    for (x, z) in ((cx - 3, cz - 1), (cx + 3, cz + 1), (cx, cz - 1), (cx, cz + 1), (cx - 3, cz + 1), (cx + 3, cz - 1)):
        m.put(x, 2, z, B['fern'])
    m.put(cx, 8, cz, B['hlantern'])
    # door in the middle of the south wall
    m.box(cx, cx, 1, 2, z1, z1, 'air')
    door(m, cx, 1, z1, 'south')
    m.label(cx, 8, z1 + 1, *TITLES['cacao'])
    standing_sign(m, cx + 2, 1, z1 + 1, ['', 'Cacao', 'greenhouse', ''])
    m.put(cx - 2, 1, z1 + 1, B['lantern'])


def shed(m):
    x0, x1, z0, z1 = 35, 43, 6, 11
    m.box(x0, x1, 0, 0, z0, z1, B['spruce'])
    for y in range(1, 4):
        for x in range(x0, x1 + 1):
            for z in (z0, z1):
                m.put(x, y, z, B['spruce'])
        for z in range(z0, z1 + 1):
            for x in (x0, x1):
                m.put(x, y, z, B['spruce'])
    for (x, z) in ((x0, z0), (x0, z1), (x1, z0), (x1, z1)):
        m.box(x, x, 1, 3, z, z, B['slog'])
    for (y, dz) in ((4, 0), (5, 1), (6, 2)):          # roof (gable along x, from the north and south eaves)
        m.box(x0 - 1, x1 + 1, y, y, z0 - 1 + dz, z0 - 1 + dz, stairs('dark_oak', 'south'))
        m.box(x0 - 1, x1 + 1, y, y, z1 + 1 - dz, z1 + 1 - dz, stairs('dark_oak', 'north'))
    m.box(x0 - 1, x1 + 1, 6, 6, z0 + 2, z1 - 2, 'minecraft:dark_oak_slab[type=bottom,waterlogged=false]')
    for (y, dz) in ((4, 1), (5, 2)):
        for x in (x0, x1):
            m.box(x, x, y, y, z0 + dz, z1 - dz, B['spruce'])
    m.box(x0 + 1, x1 - 1, 4, 4, z0 + 1, z1 - 1, 'air')
    for x in (37, 41):
        m.box(x, x, 2, 2, z1, z1, 'minecraft:glass_pane[east=true,north=false,south=false,west=true,waterlogged=false]')
    m.box(39, 39, 1, 2, z1, z1, 'air')
    door(m, 39, 1, z1, 'south')
    m.put(x0 + 1, 1, z0 + 1, B['barrel']); m.put(x0 + 2, 1, z0 + 1, B['barrel']); m.put(x0 + 1, 2, z0 + 1, B['barrel'])
    m.put(x1 - 1, 1, z0 + 1, B['table']); m.put(x1 - 2, 1, z0 + 1, B['chest'])
    m.put(x0 + 1, 1, z1 - 1, B['hay']); m.put(x1 - 1, 1, z1 - 1, B['composter'])
    m.put(39, 3, 8, B['hlantern'])
    for x in (x0 - 2, x1 + 2):                         # compost bins outside
        m.put(x, 1, z1 - 1, B['composter'])
    m.label(39, 5.5, z1 + 1, 'TOOL SHED', 'Spades, seeds and compost')
    m.sign(40, 2, z1 + 1, 'minecraft:spruce_wall_sign[facing=south,waterlogged=false]', ['', 'Tool shed', '', ''])


def well(m, cx=39, cz=27):
    m.box(cx - 2, cx + 2, 0, 1, cz - 2, cz + 2, B['cobble'])
    m.box(cx - 1, cx + 1, -1, 1, cz - 1, cz + 1, B['water'])
    for (x, z) in ((cx - 2, cz - 2), (cx + 2, cz + 2), (cx - 2, cz + 2), (cx + 2, cz - 2)):
        m.box(x, x, 2, 3, z, z, B['fence'])
    m.box(cx - 2, cx + 2, 4, 4, cz - 2, cz + 2, 'minecraft:spruce_slab[type=bottom,waterlogged=false]')
    m.put(cx, 3, cz, 'minecraft:iron_chain[axis=y,waterlogged=false]')
    m.put(cx, 2, cz, B['hlantern'])
    m.label(cx, 4, cz, 'THE WELL', 'Every garden needs water')
    m.put(cx, 1, cz + 3, B['path'])


def paths(m):
    for z in range(13, 56):
        for x in (38, 39, 40):
            if m.get(x, 0, z) == B['grass']:
                m.put(x, 0, z, B['path'])


def arch(m):
    z = 53
    for x in (35, 43):
        m.box(x, x, 1, 5, z, z, B['slog'])
        m.put(x, 6, z, B['lantern'])
    m.box(35, 43, 5, 5, z, z, 'minecraft:spruce_log[axis=x]')
    m.put(37, 4, z, B['hlantern']); m.put(41, 4, z, B['hlantern'])
    m.label(39, 6, z, 'GARDEN SCHOOL', 'Walk up to a gardener to hear about their plants')
    m.sign(39, 4, z + 1, 'minecraft:spruce_wall_sign[facing=south,waterlogged=false]', ['Garden', 'School', '', ''])
    for x in list(range(33, 37)) + list(range(42, 46)):
        m.put(x, 1, z + 1, ('minecraft:poppy', 'minecraft:dandelion', 'minecraft:cornflower', 'minecraft:oxeye_daisy')[x % 4])


def scarecrow(m, x=14, z=27):
    m.box(x, x, 1, 2, z, z, B['fence'])
    m.put(x, 3, z, B['hay']); m.put(x, 4, z, B['pumpkin'])
    m.put(x - 1, 3, z, B['fence'].replace('east=false', 'east=true')); m.put(x + 1, 3, z, B['fence'].replace('west=false', 'west=true'))


def trees(m):
    for (tx, tz) in ((8, 8), (70, 50), (8, 50), (24, 8), (56, 50)):
        m.box(tx, tx, 1, 4, tz, tz, B['oaklog'])
        m.sphere(tx, 5, tz, 2.4, B['oakleaves'], cond=lambda x, y, z: m.get(x, y, z) == 'air' and y >= 3)


def benches(m):
    for (x, z, f) in ((33, 27, 'east'), (45, 27, 'west'), (39, 46, 'north')):
        if f in ('east', 'west'):
            for dz in (-1, 0, 1):
                m.put(x, 1, z + dz, stairs('spruce', 'west' if f == 'east' else 'east'))
        else:
            for dx in (-1, 0, 1):
                m.put(x + dx, 1, z, stairs('spruce', 'north'))


def flowers(m):
    rng = np.random.default_rng(11)
    fl = ['minecraft:poppy', 'minecraft:dandelion', 'minecraft:cornflower', 'minecraft:oxeye_daisy', 'minecraft:allium',
          'minecraft:azure_bluet', 'minecraft:short_grass']
    busy = np.zeros((NX, NZ), bool)
    for (kind, cx, cz) in BEDS:
        busy[cx - 7:cx + 8, cz - 5:cz + 6] = True
    busy[33:46, 4:15] = True; busy[34:45, 22:33] = True; busy[33:46, 50:58] = True
    for _ in range(320):
        x, z = int(rng.integers(5, NX - 5)), int(rng.integers(5, NZ - 5))
        if not busy[x, z] and m.get(x, 0, z) == B['grass'] and m.get(x, 1, z) == 'air':
            m.put(x, 1, z, fl[int(rng.integers(0, len(fl)))])


def build():
    m = M()
    island(m)
    paths(m)
    for (kind, cx, cz) in BEDS:
        if kind == 'cacao':
            greenhouse(m, cx, cz)
        else:
            bed(m, kind, cx, cz)
    shed(m); well(m); arch(m); scarecrow(m); trees(m); benches(m); flowers(m)
    return m


if __name__ == '__main__':
    m = build()
    print('blocks', int((m.g > 0).sum()), 'palette', len(m.pal), 'plants', len(m.plants), 'labels', len(m.labels))
