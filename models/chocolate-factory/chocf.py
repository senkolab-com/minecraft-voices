"""chocolate-factory: an original candy factory on a small island (the "Cocoa Clockworks").

Concept coordinates: x 0..NX-1 east (to the right of a player standing at the gate), z 0..NZ-1 south (towards the
player), y up with y = 0 the grass surface. The island's bottom is at y = -6 (sea level is y = -1: world 62).
Block palette: real Minecraft block states (written for the north-facing build; oriented states are rotated by the
pack writer). Each building is labelled (sign + floating text) and has a tour guide.
"""
import math
import numpy as np

NX, NZ = 170, 150
Y0, Y1 = -6, 74
NY = Y1 - Y0 + 1


class M:
    def __init__(self):
        self.g = np.zeros((NX, NY, NZ), np.int32)
        self.pal = ['air']
        self.idx = {'air': 0}
        self.labels = []          # (x, y, z, text_lines, facing) floating text above entrances
        self.signs = []
        self.guides = {}          # id -> (x, y, z, facing)
        self.lights = []
        self.zones = []           # interiors (x0,x1,y0,y1,z0,z1) for lights

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

    def hollow(self, x0, x1, y0, y1, z0, z1, wall):
        self.box(x0, x1, y0, y1, z0, z1, wall)
        self.box(x0 + 1, x1 - 1, y0, y1, z0 + 1, z1 - 1, 'air')

    def cyl(self, cx, cz, r, y0, y1, name, shell=False, t=1.2):
        for x in range(int(cx - r - 1), int(cx + r + 2)):
            for z in range(int(cz - r - 1), int(cz + r + 2)):
                d = math.hypot(x - cx, z - cz)
                if d <= r and (not shell or d > r - t):
                    self.box(x, x, y0, y1, z, z, name)

    def sphere(self, cx, cy, cz, r, name, shell=False, cond=None):
        for x in range(int(cx - r - 1), int(cx + r + 2)):
            for y in range(int(cy - r - 1), int(cy + r + 2)):
                for z in range(int(cz - r - 1), int(cz + r + 2)):
                    d = math.dist((x, y, z), (cx, cy, cz))
                    if d <= r and (not shell or d > r - 1.2) and (cond is None or cond(x, y, z)):
                        self.put(x, y, z, name)

    def label(self, x, y, z, title, sub, facing):
        self.labels.append((x, y, z, title, sub, facing))

    def sign(self, x, y, z, facing, lines):
        self.put(x, y, z, f'minecraft:dark_oak_wall_sign[facing={facing},waterlogged=false]')
        self.signs.append((x, y, z, facing, lines))


B = {
    'grass': 'minecraft:grass_block[snowy=false]', 'dirt': 'minecraft:dirt', 'sand': 'minecraft:sand',
    'choc': 'minecraft:brown_terracotta', 'chocd': 'minecraft:mud_bricks', 'chocdk': 'minecraft:dark_oak_planks',
    'sugar': 'minecraft:smooth_quartz', 'pink': 'minecraft:pink_terracotta', 'pinkc': 'minecraft:pink_concrete',
    'mint': 'minecraft:lime_terracotta', 'mintc': 'minecraft:cyan_terracotta', 'lemon': 'minecraft:yellow_concrete',
    'white': 'minecraft:white_concrete', 'caramel': 'minecraft:orange_terracotta', 'honey': 'minecraft:honeycomb_block',
    'glass': 'minecraft:glass', 'pane': 'minecraft:light_blue_stained_glass', 'gold': 'minecraft:gold_block',
    'fudge': 'minecraft:brown_concrete', 'ginger': 'minecraft:stripped_jungle_wood[axis=y]',
    'ginger2': 'minecraft:jungle_planks', 'floor': 'minecraft:polished_andesite', 'oak': 'minecraft:oak_planks',
    'cherry': 'minecraft:cherry_planks', 'iron': 'minecraft:iron_block', 'copper': 'minecraft:waxed_cut_copper',
    'path_p': 'minecraft:pink_concrete', 'path_w': 'minecraft:white_concrete', 'stone': 'minecraft:smooth_stone',
    'black': 'minecraft:polished_blackstone', 'leaves': 'minecraft:jungle_leaves[persistent=true,distance=1,waterlogged=false]',
    'log': 'minecraft:jungle_log[axis=y]', 'hay': 'minecraft:hay_block[axis=y]',
    'campfire': 'minecraft:campfire[lit=true,signal_fire=true,facing=north,waterlogged=false]',
    'lantern': 'minecraft:lantern[hanging=false,waterlogged=false]', 'hlantern': 'minecraft:lantern[hanging=true,waterlogged=false]',
    'light': 'minecraft:light[level=14,waterlogged=false]', 'barrel': 'minecraft:barrel[facing=up,open=false]',
    'smoker': 'minecraft:smoker[facing=south,lit=true]', 'grind': 'minecraft:grindstone[face=floor,facing=north]',
    'brownwool': 'minecraft:brown_wool', 'cauldron': 'minecraft:cauldron', 'chest': 'minecraft:chest[facing=south,type=single,waterlogged=false]',
    'red': 'minecraft:red_concrete', 'blue': 'minecraft:light_blue_concrete', 'purple': 'minecraft:magenta_concrete',
    'carpet_b': 'minecraft:brown_carpet', 'table': 'minecraft:smooth_stone_slab[type=bottom,waterlogged=false]',
    'fence': 'minecraft:dark_oak_fence[east=false,north=false,south=false,west=false,waterlogged=false]',
    'cocoa_n': 'minecraft:cocoa[age=2,facing=north]', 'cocoa_s': 'minecraft:cocoa[age=2,facing=south]',
    'cocoa_e': 'minecraft:cocoa[age=2,facing=east]', 'cocoa_w': 'minecraft:cocoa[age=2,facing=west]',
    'flower1': 'minecraft:pink_tulip', 'flower2': 'minecraft:allium', 'flower3': 'minecraft:oxeye_daisy',
    'water': 'minecraft:water[level=0]', 'pchain': 'minecraft:iron_chain[axis=y,waterlogged=false]',
}


def stairs(mat, facing, half='bottom'):
    return f'minecraft:{mat}_stairs[facing={facing},half={half},shape=straight,waterlogged=false]'


def door(m, x, y, z, facing, wood='dark_oak', hinge='left'):
    m.put(x, y, z, f'minecraft:{wood}_door[facing={facing},half=lower,hinge={hinge},open=false,powered=false]')
    m.put(x, y + 1, z, f'minecraft:{wood}_door[facing={facing},half=upper,hinge={hinge},open=false,powered=false]')


def light_zone(m, x0, x1, y0, y1, z0, z1, step=5):
    m.zones.append((x0, x1, y0, y1, z0, z1, step))


# ------------------------------------------------------------------ island
def island(m):
    for x in range(NX):
        for z in range(NZ):
            # rounded rectangle 6..163 x 6..143 with a 10-block corner radius; beach ring of 3
            dx = max(0, 16 - x, x - (NX - 17))
            dz = max(0, 16 - z, z - (NZ - 17))
            d = math.hypot(dx, dz)
            if d <= 10:
                m.box(x, x, -6, -2, z, z, B['dirt'])
                m.put(x, -1, z, B['dirt'])
                top = B['grass'] if d <= 7 else B['sand']
                m.put(x, 0, z, top)
                m.put(x, -1, z, B['dirt'] if d <= 7 else B['sand'])
            elif d <= 13:
                m.box(x, x, -6, -2, z, z, 'minecraft:sandstone')   # shallow shelf under the water's edge
                m.put(x, -1, z, B['sand'])
    # paths: the avenue from the island's south edge to the hall door, and the cross path
    for x in range(66, 81):
        for z in range(47, 142):
            m.put(x, 0, z, B['path_p'] if ((x + z) // 2) % 2 else B['path_w'])
    for x in range(14, 158):
        for z in range(86, 93):
            if m.get(x, 0, z) != 'air':
                m.put(x, 0, z, B['path_p'] if ((x + z) // 2) % 2 else B['path_w'])
    for x in range(28, 46):                                   # to the caramel tower door
        for z in range(40, 46):
            m.put(x, 0, z, B['path_w'] if (x // 2) % 2 else B['path_p'])
    for x in range(110, 118):                                 # to the conservatory door
        for z in range(28, 34):
            m.put(x, 0, z, B['path_w'] if (x // 2) % 2 else B['path_p'])
    rng = np.random.default_rng(7)
    for _ in range(420):                                      # flowers on the grass
        x, z = int(rng.integers(10, NX - 10)), int(rng.integers(50, NZ - 10))
        if m.get(x, 0, z) == B['grass'] and m.get(x, 1, z) == 'air':
            m.put(x, 1, z, B[['flower1', 'flower2', 'flower3'][int(rng.integers(0, 3))]])


# ------------------------------------------------------------------ the Great Hall (3 floors + clock room)
HX0, HX1, HZ0, HZ1 = 45, 110, 14, 46
FLOORS = (0, 8, 16)          # floor layers; ceilings at 8, 16, 24


def great_hall(m):
    m.hollow(HX0, HX1, 1, 24, HZ0, HZ1, B['choc'])
    m.box(HX0, HX1, 0, 0, HZ0, HZ1, B['floor'])
    for y in (8, 16):
        m.box(HX0, HX1, y, y, HZ0, HZ1, B['sugar'])
        m.box(HX0 + 1, HX1 - 1, y, y, HZ0 + 1, HZ1 - 1, B['oak'] if y == 8 else B['cherry'])
    m.box(HX0, HX1, 24, 24, HZ0, HZ1, B['sugar'])
    for x in range(HX0 + 3, HX1 - 2, 5):                      # windows, front and back, every floor
        for z in (HZ0, HZ1):
            for (y0, y1) in ((2, 6), (10, 14), (18, 22)):
                m.box(x, x + 1, y0, y1, z, z, B['pane'])
    for z in range(HZ0 + 4, HZ1 - 3, 6):                       # end walls
        for x in (HX0, HX1):
            for (y0, y1) in ((2, 6), (10, 14), (18, 22)):
                m.box(x, x, y0, y1, z, z + 1, B['pane'])
    # roof (stepped gable along x) with a hollow attic
    for n, y in enumerate(range(25, 41)):
        if HZ0 + n <= HZ1 - n:
            m.box(HX0, HX1, y, y, HZ0 + n, HZ1 - n, B['pink'])
            if HZ0 + n + 1 <= HZ1 - n - 1 and y < 38:
                m.box(HX0 + 1, HX1 - 1, y, y, HZ0 + n + 1, HZ1 - n - 1, 'air')
    # clock gable on the front: a giant chocolate bar framing a gold-rimmed clock, the clock room behind it
    gx0, gx1 = 62, 84
    m.box(gx0, gx1, 25, 44, HZ1 - 6, HZ1 + 1, B['choc'])
    m.box(gx0 + 1, gx1 - 1, 25, 43, HZ1 - 5, HZ1, 'air')
    m.box(gx0 + 1, gx1 - 1, 24, 24, HZ1 - 5, HZ1, B['oak'])
    for n, y in enumerate(range(45, 54)):
        if gx0 + n <= gx1 - n:
            m.box(gx0 + n, gx1 - n, y, y, HZ1 - 6, HZ1 + 1, B['pink'])
    for x in range(gx0 + 1, gx1):
        for y in range(26, 44):
            if (x - gx0 - 1) % 4 == 0 or (y - 26) % 4 == 0:
                m.put(x, y, HZ1 + 2, B['chocd'])
            else:
                m.put(x, y, HZ1 + 2, B['choc'])
    cx, cy = 73, 35
    for x in range(gx0 + 1, gx1):
        for y in range(26, 44):
            d = math.hypot(x - cx, y - cy)
            if d <= 7.5:
                m.put(x, y, HZ1 + 2, B['sugar'])
            elif d <= 8.5:
                m.put(x, y, HZ1 + 2, B['gold'])
    for t in range(0, 6):
        m.put(cx, cy + t, HZ1 + 3, B['black'])
    for t in range(0, 5):
        m.put(cx + t, cy, HZ1 + 3, B['black'])
    for a in range(12):                                       # hour marks
        x = int(round(cx + 6.3 * math.cos(a * math.pi / 6)))
        y = int(round(cy + 6.3 * math.sin(a * math.pi / 6)))
        m.put(x, y, HZ1 + 3, B['chocd'])
    # inside the clock room: the clockwork - big gears of iron and gold behind the face
    for (gcx, gcy, r, mat) in ((73, 35, 5.5, 'iron'), (66, 30, 3.5, 'gold'), (80, 40, 3.0, 'gold')):
        for x in range(int(gcx - r - 1), int(gcx + r + 2)):
            for y in range(int(gcy - r - 1), int(gcy + r + 2)):
                d = math.hypot(x - gcx, y - gcy)
                a = math.atan2(y - gcy, x - gcx)
                tooth = (int((a + math.pi) / (2 * math.pi) * 12) % 2 == 0)
                if d <= r - 1 and d > r - 2.2 or (r - 1 < d <= r and tooth) or d <= 1:
                    m.put(x, y, HZ1 - 2, B[mat])
    m.box(64, 82, 25, 25, HZ1 - 5, HZ1 - 1, B['oak'])           # clock room floor (over the attic)
    light_zone(m, 63, 83, 26, 42, HZ1 - 5, HZ1, 6)
    # front door (double) and the entrance porch
    m.box(70, 76, 1, 6, HZ1, HZ1, 'air')
    m.box(69, 77, 7, 7, HZ1, HZ1 + 1, B['gold'])
    door(m, 72, 1, HZ1, 'south', 'dark_oak', 'left')
    door(m, 74, 1, HZ1, 'south', 'dark_oak', 'right')
    m.box(70, 71, 1, 6, HZ1, HZ1, B['sugar']); m.box(75, 76, 1, 6, HZ1, HZ1, B['sugar'])
    m.box(73, 73, 1, 6, HZ1, HZ1, B['sugar'])
    # staircases: two flights at the west end, side by side: floor 1 -> 2 going south in lane x 47-48, floor 2 -> 3
    # going north in lane x 50-51; each arrives on a landing, with a railing round the stairwell
    for (fy, lane, d, zs) in ((0, (HX0 + 2, HX0 + 3), 'south', range(HZ0 + 4, HZ0 + 12)),
                              (8, (HX0 + 5, HX0 + 6), 'north', range(HZ0 + 11, HZ0 + 3, -1))):
        for n, z in enumerate(zs, 1):
            for x in lane:
                m.put(x, fy + n, z, stairs('dark_oak', d))
                m.box(x, x, fy + n + 1, fy + n + 3, z, z, 'air')
                if n > 1:
                    m.box(x, x, fy + 1, fy + n - 1, z, z, B['chocdk'])
        top = fy + 8
        zz = sorted(zs)
        m.box(lane[0], lane[1], top, top, zz[0], zz[-1], 'air')                       # stairwell hole in the floor above
        for z in zz:                                                                 # railings beside the hole
            for x in (lane[0] - 1, lane[1] + 1):
                if m.get(x, top, z) != 'air' and m.get(x, top + 1, z) == 'air':
                    m.put(x, top + 1, z, B['fence'])
    m.box(HX0 + 2, HX0 + 3, 8, 8, HZ0 + 12, HZ0 + 13, B['oak'])                         # landings
    m.box(HX0 + 5, HX0 + 6, 16, 16, HZ0 + 2, HZ0 + 3, B['cherry'])
    # ladder from the 3rd floor up to the clock room, on a pillar
    m.box(72, 72, 17, 23, HZ1 - 6, HZ1 - 6, B['chocdk'])
    for y in range(17, 27):
        m.put(72, y, HZ1 - 5, 'minecraft:ladder[facing=south,waterlogged=false]')
    # ---- floor 1: the Roasting Room
    for n, x in enumerate(range(52, 104, 13)):                # four roaster drums (smokers in brick) and bean sacks
        m.box(x, x + 4, 1, 3, HZ0 + 2, HZ0 + 5, B['chocd'])
        m.box(x + 1, x + 3, 4, 5, HZ0 + 3, HZ0 + 4, B['copper'])
        m.put(x + 2, 6, HZ0 + 3, B['pchain']); m.put(x + 2, 7, HZ0 + 3, B['pchain'])
        m.put(x + 1, 1, HZ0 + 6, B['smoker']); m.put(x + 3, 1, HZ0 + 6, B['smoker'])
        for k in range(3):
            m.put(x + 5, 1 + (k // 2), HZ0 + 2 + k, B['brownwool'])
    for x in range(52, 104):                                  # a bean conveyor down the middle
        m.put(x, 1, 30, B['black'])
        if x % 3 == 0:
            m.put(x, 2, 30, B['carpet_b'])
    for x in range(56, 100, 8):                               # grinding stones
        m.put(x, 1, 36, B['grind']); m.put(x + 1, 1, 36, B['barrel'])
    light_zone(m, HX0 + 1, HX1 - 1, 1, 7, HZ0 + 1, HZ1 - 1, 6)
    # ---- floor 2: Melting & Mixing (big chocolate vats with stirring paddles, pipes)
    for (vx, vz) in ((58, 24), (72, 24), (86, 24), (100, 24), (65, 37), (93, 37)):
        m.cyl(vx, vz, 3.2, 9, 12, B['copper'], shell=True)
        m.cyl(vx, vz, 2.2, 12, 12, B['fudge'])
        m.box(vx, vx, 13, 15, vz, vz, B['fence'])
        m.put(vx, 12, vz, B['fence'])
    for x in range(55, 104):                                  # pipe along the ceiling
        m.put(x, 15, 31, B['copper'])
    light_zone(m, HX0 + 1, HX1 - 1, 9, 15, HZ0 + 1, HZ1 - 1, 6)
    # ---- floor 3: Moulding & Tasting (moulding line, cooling tunnel, tasting table)
    for x in range(55, 100):
        m.put(x, 17, 24, B['stone']); m.put(x, 17, 25, B['stone'])
        if x % 3 == 0:
            m.put(x, 18, 24, B['carpet_b']); m.put(x, 18, 25, B['carpet_b'])
    for x in range(70, 86):                                   # cooling tunnel over the line
        m.box(x, x, 18, 20, 23, 23, B['pane']); m.box(x, x, 18, 20, 26, 26, B['pane'])
        m.box(x, x, 21, 21, 23, 26, B['pane'])
        m.box(x, x, 18, 20, 24, 25, 'air')
    for x in range(62, 92, 1):                                # tasting table with seats
        m.put(x, 17, 37, B['table'])
        if x % 3 == 1:
            m.put(x, 17, 35, stairs('cherry', 'south')); m.put(x, 17, 39, stairs('cherry', 'north'))
    for x in range(64, 92, 6):
        m.put(x, 18, 37, B['carpet_b'])
    light_zone(m, HX0 + 1, HX1 - 1, 17, 23, HZ0 + 1, HZ1 - 1, 6)
    # three striped chimneys on the roof, with candy-coloured smoke sculptures and real smoke
    for (x, z, c, sm) in ((52, 22, 'pinkc', 'minecraft:pink_wool'), (60, 38, 'mint', 'minecraft:lime_wool'), (100, 24, 'lemon', 'minecraft:yellow_wool')):
        for y in range(25, 56):
            m.cyl(x, z, 2.6, y, y, B[c] if (y // 3) % 2 else B['white'])
        m.cyl(x, z, 1.5, 54, 55, 'air')
        m.put(x, 54, z, B['hay']); m.put(x, 55, z, B['campfire'])
        for (dx, dy, dz, r) in ((4, 60, 0, 2.8), (8, 64, 2, 3.5)):
            m.sphere(x + dx, dy, z + dz, r, sm)
    # walkways: 3rd-floor door to the bridge on the west wall
    m.box(HX0, HX0, 17, 19, 29, 31, 'air')
    door(m, HX0, 17, 30, 'west', 'dark_oak')
    m.box(HX0, HX0, 17, 18, 29, 29, B['choc']); m.box(HX0, HX0, 17, 18, 31, 31, B['choc'])
    # labels + guides
    m.label(73, 9, HZ1 + 1, 'THE GREAT HALL', 'Roasting · Melting · Moulding', 'south')
    m.sign(69, 3, HZ1 + 1, 'south', ['', 'The Great Hall', 'Roasting Room', ''])
    m.sign(HX0 + 4, 10, HZ0 + 13, 'south', ['', 'Melting &', 'Mixing Room', ''])
    m.sign(HX0 + 4, 18, HZ0 + 13, 'south', ['', 'Moulding &', 'Tasting Room', ''])
    m.sign(70, 27, HZ1 - 5, 'south', ['', 'The Clock', 'Room', ''])
    m.guides['roast'] = (73, 1, HZ1 - 4, 'south')
    m.guides['mix'] = (HX0 + 6, 9, HZ0 + 14, 'east')
    m.guides['taste'] = (HX0 + 6, 17, HZ0 + 14, 'east')
    m.guides['clock'] = (76, 26, HZ1 - 3, 'south')


# ------------------------------------------------------------------ the Caramel Tower with its spiral stair and the slide
TX, TZ, TR = 22, 32, 7


def caramel_tower(m):
    m.cyl(TX, TZ, TR, 1, 44, B['caramel'], shell=True)
    m.cyl(TX, TZ, TR - 1, 0, 0, B['honey'])
    for y in range(4, 44, 5):
        m.cyl(TX, TZ, TR + 0.3, y, y, B['honey'], shell=True)
    m.cyl(TX, TZ, TR, 44, 44, B['honey'])                       # lookout floor
    m.cyl(TX, TZ, TR - 1, 45, 47, 'air')
    for a in range(0, 360, 45):                               # lookout arches
        x = int(round(TX + TR * math.cos(math.radians(a)))); z = int(round(TZ + TR * math.sin(math.radians(a))))
        m.put(x, 45, z, 'minecraft:yellow_stained_glass_pane[east=false,north=false,south=false,west=false,waterlogged=false]')
    m.cyl(TX, TZ, TR, 45, 47, B['caramel'], shell=True)
    for a in range(0, 360, 30):
        x = int(round(TX + TR * math.cos(math.radians(a)))); z = int(round(TZ + TR * math.sin(math.radians(a))))
        m.box(x, x, 45, 46, z, z, 'air')
    for n, y in enumerate(range(48, 62)):
        m.cyl(TX, TZ, max(8.4 - n * 0.6, 0.6), y, y, B['pink'])
    m.put(TX, 62, TZ, B['gold']); m.put(TX, 63, TZ, B['gold'])
    # central column and the spiral stair: one step up every 22.5 degrees, 5 wide, continuous, headroom 3
    m.cyl(TX, TZ, 1.2, 1, 43, B['honey'])
    last = []
    for a10 in range(0, 43 * 225):
        a = math.radians(a10 / 10)
        h = 1 + a10 // 225
        for rr in (2.0, 2.8, 3.6, 4.4, 5.2):
            x = int(round(TX + rr * math.cos(a))); z = int(round(TZ + rr * math.sin(a)))
            m.put(x, h, z, B['sugar'])
            m.box(x, x, h + 1, h + 3, z, z, 'air')
            if h >= 41:
                last.append((x, z))
    m.cyl(TX, TZ, TR - 1, 44, 44, B['honey'])
    for (x, z) in last:                                        # the hole into the lookout above the last steps
        m.box(x, x, 44, 44, z, z, 'air')
    m.cyl(TX, TZ, 1.2, 44, 44, B['honey'])
    # landing in front of the bridge door (3rd-floor level)
    m.box(TX + 4, TX + 6, 16, 16, TZ - 3, TZ - 1, B['sugar'])
    m.box(TX + 4, TX + 6, 17, 19, TZ - 3, TZ - 1, 'air')
    # the caramel kitchen on the ground: cauldrons and honey vats
    for (dx, dz) in ((-4, -2), (-4, 2), (4, -2), (4, 2)):
        m.put(TX + dx, 1, TZ + dz, B['cauldron'])
    # door (east, towards the hall) and the bridge door at 3rd-floor level
    m.box(TX + TR, TX + TR, 1, 2, TZ + 8 - 8, TZ + 8 - 8, 'air')
    m.box(TX + TR - 1, TX + TR - 1, 1, 3, TZ, TZ, 'air')
    door(m, TX + TR, 1, TZ, 'east', 'cherry')
    m.box(TX + TR, TX + TR, 17, 18, TZ - 2, TZ - 2, 'air')
    door(m, TX + TR, 17, TZ - 2, 'east', 'cherry')
    # the slide: a yellow spiral ribbon outside (decorative)
    for t in range(0, 420):
        a = t / 420 * 4.5 * 2 * math.pi
        yy = int(42 - t * 40 / 420)
        for w in (9.0, 10.0):
            x, z = int(round(TX + w * math.cos(a))), int(round(TZ + w * math.sin(a)))
            if m.get(x, yy, z) == 'air':
                m.put(x, yy, z, B['lemon'])
    light_zone(m, TX - 5, TX + 5, 1, 43, TZ - 5, TZ + 5, 5)
    m.label(TX + TR + 1, 6, TZ, 'THE CARAMEL TOWER', 'Caramel kitchen · Lookout', 'east')
    m.sign(TX + TR + 1, 3, TZ + 2, 'east', ['', 'The Caramel', 'Tower', ''])
    m.guides['caramel'] = (TX + TR + 2, 1, TZ + 3, 'east')
    m.guides['lookout'] = (TX + 3, 45, TZ + 3, 'west')


# ------------------------------------------------------------------ the Bonbon Bridge (tower -> hall, 3rd floor)
def bonbon_bridge(m):
    x0, x1 = TX + TR + 1, HX0 - 1
    m.box(x0, x1, 16, 16, 27, 33, B['sugar'])
    for x in range(x0, x1 + 1):
        m.box(x, x, 17, 20, 27, 27, B['glass']); m.box(x, x, 17, 20, 33, 33, B['glass'])
    m.box(x0, x1, 21, 21, 27, 33, B['glass'])
    m.box(x0, x1, 17, 20, 28, 32, 'air')
    for x in range(x0, x1 + 1):                               # the conveyor with giant sweets
        m.put(x, 17, 32, B['black'])
    for n, x in enumerate(range(x0 + 1, x1, 3)):
        m.put(x, 18, 32, B[('red', 'blue', 'mint', 'lemon', 'purple')[n % 5]])
    for (px, pz) in ((x0 + 2, 27), (x0 + 2, 33), (x1 - 2, 27), (x1 - 2, 33)):
        m.box(px, px, 1, 15, pz, pz, B['sugar'])
    light_zone(m, x0, x1, 17, 20, 28, 32, 5)
    m.label((x0 + x1) // 2, 23, 30, 'THE BONBON BRIDGE', '', 'south')


# ------------------------------------------------------------------ the Cocoa Conservatory (glass dome)
DX, DZ, DR = 138, 30, 19


def conservatory(m):
    m.sphere(DX, 0, DZ, DR, B['glass'], shell=True, cond=lambda x, y, z: y >= 1)
    for x in range(DX - DR - 1, DX + DR + 2):
        for y in range(1, DR + 1):
            for z in range(DZ - DR - 1, DZ + DR + 2):
                if m.get(x, y, z) == B['glass'] and (x == DX or z == DZ or y in (7, 13)):
                    m.put(x, y, z, B['white'])
    m.cyl(DX, DZ, DR - 1, 0, 0, B['grass'])
    m.cyl(DX, DZ, 9.5, 0, 0, B['path_w'])
    m.cyl(DX, DZ, 8.5, 0, 0, B['grass'])
    # cocoa trees: jungle log trunks with cocoa pods, leaf crowns
    for (tx, tz) in ((DX - 6, DZ - 5), (DX + 6, DZ - 5), (DX - 6, DZ + 6), (DX + 6, DZ + 6), (DX, DZ - 13), (DX - 13, DZ), (DX + 13, DZ), (DX, DZ + 13)):
        m.box(tx, tx, 1, 8, tz, tz, B['log'])
        m.sphere(tx, 10, tz, 3.2, B['leaves'], cond=lambda x, y, z: m.get(x, y, z) == 'air')
        for (dx, dz, f) in ((1, 0, 'cocoa_w'), (-1, 0, 'cocoa_e'), (0, 1, 'cocoa_n'), (0, -1, 'cocoa_s')):
            for yy in (3, 5):
                m.put(tx + dx, yy, tz + dz, B[f])
    for (bx, bz, f) in ((DX - 3, DZ, 'east'), (DX + 3, DZ, 'west')):
        m.put(bx, 1, bz - 1, stairs('cherry', f)); m.put(bx, 1, bz, stairs('cherry', f)); m.put(bx, 1, bz + 1, stairs('cherry', f))
    for z in range(DZ - 2, DZ + 3, 2):                         # bean drying trays
        m.put(DX, 1, z, B['barrel'])
    # door on the west side towards the hall
    wx = DX - DR
    for x in range(wx - 1, wx + 3):
        m.box(x, x, 1, 3, DZ - 1, DZ + 1, 'air')
    door(m, wx + 1, 1, DZ, 'west', 'cherry')
    m.box(wx + 1, wx + 1, 1, 3, DZ - 1, DZ - 1, B['white']); m.box(wx + 1, wx + 1, 1, 3, DZ + 1, DZ + 1, B['white'])
    m.box(wx + 1, wx + 1, 3, 3, DZ, DZ, B['white'])
    light_zone(m, DX - 14, DX + 14, 2, 14, DZ - 14, DZ + 14, 7)
    m.label(wx - 1, 6, DZ, 'THE COCOA CONSERVATORY', 'Where chocolate grows', 'west')
    m.sign(wx, 3, DZ + 3, 'west', ['', 'The Cocoa', 'Conservatory', ''])
    m.guides['garden'] = (wx + 3, 1, DZ + 3, 'east')


# ------------------------------------------------------------------ courtyard: fudge fountain and lollipop trees
def courtyard(m):
    cx, cz = 73, 66
    m.cyl(cx, cz, 7, 1, 2, B['sugar'])
    m.cyl(cx, cz, 6, 2, 2, B['fudge'])
    m.cyl(cx, cz, 1.2, 1, 8, B['sugar'])
    m.sphere(cx, 9, cz, 2.2, B['fudge'])
    m.put(cx, 12, cz, B['gold'])
    for (lx, lz, c) in ((52, 62, 'pinkc'), (95, 62, 'mint'), (52, 76, 'lemon'), (95, 76, 'blue'), (30, 104, 'red'), (122, 104, 'pinkc'),
                        (24, 70, 'purple'), (40, 120, 'mint'), (110, 122, 'lemon')):
        m.box(lx, lx, 1, 9, lz, lz, B['white'])
        for x in range(lx - 3, lx + 4):
            for y in range(9, 16):
                d = math.hypot(x - lx, y - 12.5)
                if d <= 3.3:
                    m.put(x, y, lz, B[c] if int(d * 1.3) % 2 else B['white'])
    for (bx, bz, f) in ((64, 66, 'east'), (82, 66, 'west')):
        for dz in (-1, 0, 1):
            m.put(bx, 1, bz + dz, stairs('cherry', f))
    m.label(cx, 15, cz, 'THE FUDGE FOUNTAIN', '', 'south')
    m.guides['fountain'] = (cx + 2, 1, cz + 9, 'north')


# ------------------------------------------------------------------ the Wrapping Hall (gingerbread)
def wrapping_hall(m):
    x0, x1, z0, z1 = 100, 132, 62, 82
    m.hollow(x0, x1, 1, 12, z0, z1, B['ginger'])
    m.box(x0, x1, 0, 0, z0, z1, B['floor'])
    m.box(x0, x1, 12, 12, z0, z1, B['ginger2'])
    for y in range(13, 23):
        n = y - 13
        if z0 + n <= z1 - n:
            m.box(x0, x1, y, y, z0 + n, z1 - n, B['white'] if n % 2 else B['pinkc'])
            if z0 + n + 1 <= z1 - n - 1 and y < 21:
                m.box(x0 + 1, x1 - 1, y, y, z0 + n + 1, z1 - n - 1, 'air')
    m.box(x0 + 1, x1 - 1, 12, 12, z0 + 1, z1 - 1, 'air')
    for x in range(x0 + 3, x1 - 2, 4):
        for z in (z0, z1):
            m.box(x, x + 1, 3, 7, z, z, B['pane'])
    for x in range(x0, x1 + 1):                               # striped awning on the courtyard side
        for z in (z1 + 1, z1 + 2):
            m.put(x, 9 - (z - z1 - 1), z, B['pinkc'] if (x // 3) % 2 else B['white'])
    m.box(x0, x0, 1, 3, 71, 73, 'air')                        # west door towards the courtyard
    door(m, x0, 1, 72, 'west', 'cherry')
    m.box(x0, x0, 1, 3, 71, 71, B['ginger']); m.box(x0, x0, 1, 3, 73, 73, B['ginger']); m.box(x0, x0, 3, 3, 72, 72, B['ginger'])
    # inside: wrapping tables, ribbon rolls, gift boxes, the dispatch chests
    for z in (66, 72, 78):
        for x in range(x0 + 6, x1 - 4):
            m.put(x, 1, z, B['table'])
            if x % 4 == 0:
                m.put(x, 2, z, ('minecraft:red_carpet', 'minecraft:light_blue_carpet', 'minecraft:yellow_carpet', 'minecraft:magenta_carpet')[(x // 4) % 4])
    for n, x in enumerate(range(x1 - 3, x1)):
        for z in range(z0 + 2, z1 - 1, 2):
            m.put(x, 1, z, B[('red', 'blue', 'lemon', 'purple', 'mint')[(n + z) % 5]])
            m.put(x, 2, z, B['white'] if (x + z) % 3 else B['gold'])
    for z in range(z0 + 2, z1 - 1, 3):
        m.put(x0 + 2, 1, z, B['chest'])
    light_zone(m, x0 + 1, x1 - 1, 1, 11, z0 + 1, z1 - 1, 6)
    m.label(x0 - 1, 6, 72, 'THE WRAPPING HALL', 'Bows, boxes and ribbons', 'west')
    m.sign(x0 - 1, 3, 75, 'west', ['', 'The Wrapping', 'Hall', ''])
    m.guides['wrap'] = (x0 - 2, 1, 69, 'west')


# ------------------------------------------------------------------ the Gingerbread Gate (with a ticket booth)
def gate(m):
    z0, z1 = 128, 134
    for (gx0, gx1) in ((61, 66), (80, 85)):
        m.hollow(gx0, gx1, 1, 16, z0, z1, B['ginger'])
        m.box(gx0, gx1, 0, 0, z0, z1, B['floor'])
        m.box(gx0 + 1, gx1 - 1, 15, 15, z0 + 1, z1 - 1, B['ginger2'])
        for n in range(4):
            if gx0 + n <= gx1 - n:
                m.box(gx0 + n, gx1 - n, 17 + n, 17 + n, z0, z1, B['pink'])
        m.box(gx0, gx1, 16, 16, z0, z1, B['white'])
        light_zone(m, gx0 + 1, gx1 - 1, 1, 14, z0 + 1, z1 - 1, 4)
    m.box(66, 80, 14, 18, z0 + 2, z1 - 2, B['ginger'])
    m.box(67, 79, 19, 20, z0 + 3, z0 + 3, B['gold'])
    # booth window and door (left pillar, opening into the archway)
    m.box(66, 66, 1, 2, 131, 131, 'air'); door(m, 66, 1, 131, 'east', 'cherry')
    m.box(80, 80, 1, 2, 131, 131, 'air'); door(m, 80, 1, 131, 'west', 'cherry')
    m.put(64, 1, 130, B['table']); m.put(63, 1, 130, B['table'])
    m.put(82, 1, 132, B['chest'])
    m.label(73, 22, z1, 'THE COCOA CLOCKWORKS', 'Welcome!', 'south')
    m.sign(66, 3, z1 + 1, 'south', ['', 'Ticket', 'Booth', ''])
    m.sign(80, 3, z1 + 1, 'south', ['', 'Cloak', 'Room', ''])
    m.guides['gate'] = (70, 1, z1 + 3, 'south')


def lights(m):
    lt = m.b(B['light'])
    for (x0, x1, y0, y1, z0, z1, step) in m.zones:
        for x in range(x0, x1 + 1, step):
            for z in range(z0, z1 + 1, step):
                for y in range(y1, y0 - 1, -1):
                    if m.get(x, y, z) == 'air' and m.get(x, y - 1, z) == 'air' and m.get(x, y - 2, z) == 'air':
                        m.put(x, y - 1, z, B['light'])
                        break


def build():
    m = M()
    island(m)
    great_hall(m)
    caramel_tower(m)
    bonbon_bridge(m)
    conservatory(m)
    courtyard(m)
    wrapping_hall(m)
    gate(m)
    lights(m)
    return m


if __name__ == '__main__':
    m = build()
    print('blocks', int((m.g > 0).sum()), 'palette', len(m.pal), 'guides', m.guides)
