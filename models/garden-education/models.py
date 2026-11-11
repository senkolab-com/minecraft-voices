"""Item models of the garden plants (Java resource pack): assets/garden-education/models/plant/<name>.json and
items/<name>.json. Shown by item_display entities (item_display "none": model 0..16 = one block, centred on the
entity; the pack places the entity half a block up so 0 is the soil surface)."""
import json
import math
import os
import random

NS = 'garden-education'
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'res', 'assets', NS)


def uvs(f, t):
    dx, dy, dz = (abs(t[i] - f[i]) for i in range(3))
    c = lambda a, b: [0, 0, round(min(a, 16), 3), round(min(b, 16), 3)]
    return {'north': c(dx, dy), 'south': c(dx, dy), 'east': c(dz, dy), 'west': c(dz, dy), 'up': c(dx, dz), 'down': c(dx, dz)}


class Model:
    def __init__(self, name):
        self.name, self.els, self.tex = name, [], {}

    def box(self, f, t, tex, rot=None, faces=None, top=None):
        f = [round(v, 3) for v in f]; t = [round(v, 3) for v in t]
        for k in ([tex, top] if top else [tex]):
            self.tex[k] = f'{NS}:plant/{k}'
        uv = uvs(f, t)
        fs = {}
        for side in (faces or ('north', 'south', 'east', 'west', 'up', 'down')):
            k = top if (top and side in ('up', 'down')) else tex
            fs[side] = {'texture': '#' + k, 'uv': uv[side]}
        e = {'from': f, 'to': t, 'faces': fs}
        if rot:
            ang, axis, origin = rot
            e['rotation'] = {'angle': ang, 'axis': axis, 'origin': [round(v, 3) for v in origin]}
        self.els.append(e)

    def cube(self, c, s, tex, rot=None, top=None, h=None):
        h = s if h is None else h
        self.box([c[0] - s / 2, c[1], c[2] - s / 2], [c[0] + s / 2, c[1] + h, c[2] + s / 2], tex, rot, top=top)

    def json(self):
        tx = dict((k, v) for k, v in sorted(self.tex.items()))
        tx['particle'] = next(iter(tx.values()))
        return {'textures': tx, 'elements': self.els}


A = (-45, -22.5, 0, 22.5, 45)


def leaf_flat(m, cx, y, cz, length, width, direction, tilt, tex):
    """a flat leaf sticking out from (cx, y, cz) towards direction (n/s/e/w), tilted up/down by tilt (deg)."""
    th = 0.5
    if direction in ('e', 'w'):
        x0, x1 = (cx, cx + length) if direction == 'e' else (cx - length, cx)
        f, t = [x0, y, cz - width / 2], [x1, y + th, cz + width / 2]
        sign = 1 if direction == 'e' else -1
        rot = (tilt * sign, 'z', [cx, y, cz]) if tilt else None
    else:
        z0, z1 = (cz, cz + length) if direction == 's' else (cz - length, cz)
        f, t = [cx - width / 2, y, z0], [cx + width / 2, y + th, z1]
        sign = -1 if direction == 's' else 1
        rot = (tilt * sign, 'x', [cx, y, cz]) if tilt else None
    m.box(f, t, tex, rot)


def tomato():
    m = Model('tomato')
    r = random.Random(3)
    m.box([7.3, -1, 7.3], [8.7, 28, 8.7], 'stake')
    m.box([7.9, 0, 8.7], [8.7, 24, 9.5], 'stem')
    for y in (5, 13, 21):                               # twine ties
        m.box([7.1, y, 7.1], [9.7, y + 0.6, 9.7], 'twine')
    dirs = ['e', 's', 'w', 'n']
    for n, y in enumerate((2.5, 5.5, 8.5, 11.5, 14.5, 17.5, 20.5, 23)):
        for k in range(4):
            if (n + k) % 4 == 3:
                continue
            d = dirs[(n + k) % 4]
            leaf_flat(m, 8.3, y + k * 0.4, 9.1, 6 + r.random() * 2 - (1.5 if y > 20 else 0), 4.6, d, 22.5 if y < 19 else 45, 'tomato_leaf')
        if n % 2 == 0:                                 # diagonal leaves
            ang = 45 if n % 4 == 0 else -45
            m.box([8.3, y + 1.2, 8.6], [14.5, y + 1.7, 12.6], 'tomato_leaf', (ang, 'y', [8.3, y, 9.1]))
            m.box([2.1, y + 1.2, 5.6], [8.3, y + 1.7, 9.6], 'tomato_leaf', (ang, 'y', [8.3, y, 9.1]))
    fr = [(4.3, 6.5, 9, 'tomato_red'), (12, 8.5, 10, 'tomato_red'), (5.5, 12, 12, 'tomato_orange'), (11.5, 14, 6, 'tomato_red'),
          (4.8, 16.5, 5.5, 'tomato_green'), (11.8, 18, 11.5, 'tomato_orange'), (4.6, 10, 5.2, 'tomato_green'), (10, 4.5, 13, 'tomato_red'),
          (8.5, 15, 13.2, 'tomato_red'), (3.6, 19.5, 10.5, 'tomato_green')]
    for (x, y, z, t) in fr:
        s = 3.8 if t != 'tomato_green' else 3.0
        m.cube((x, y, z), s, t, top='tomato_top')
        m.box([x - 0.3, y + s, z - 0.3], [x + 0.3, y + s + 1.2, z + 0.3], 'stem')
    return m


def cucumber():
    m = Model('cucumber')
    r = random.Random(5)
    z = 8
    m.box([0, -1, z - 0.8], [1.6, 30, z + 0.8], 'post')
    for x in (5.3, 10.6):                               # strings
        m.box([x, 0, z - 0.2], [x + 0.4, 29, z + 0.2], 'twine')
    for y in (8, 16, 24, 29):
        m.box([0, y, z - 0.2], [16, y + 0.4, z + 0.2], 'twine')
    m.box([1.6, 28.6, z - 0.5], [16, 30, z + 0.5], 'post')      # top rail
    # the vine climbing the strings
    for n, y in enumerate(range(0, 26, 4)):
        x = 5.3 if n % 2 == 0 else 10.6
        m.box([x - 0.5, y, z - 0.6], [x + 0.5, y + 4.4, z + 0.6], 'stem', (22.5 if n % 2 else -22.5, 'z', [x, y, z]))
    for n, y in enumerate((2, 6, 9, 13, 16, 20, 23, 26)):
        x = (4 + 3.3 * (n % 4)) % 15 + 0.5
        for side in ('s', 'n'):
            if r.random() < 0.75:
                leaf_flat(m, x, y, z + (0.6 if side == 's' else -0.6), 5, 5.5, side, 22.5, 'cuc_leaf')
    for (x, y) in ((3, 18), (12.5, 11), (8, 25), (14, 22)):
        m.box([x - 1, y, z - 1.8], [x + 1, y + 1.6, z - 0.4], 'cuc_flower')
    for (x, y, s) in ((3.5, 6, 'n'), (9, 9, 's'), (13, 15, 'n'), (6.5, 19, 's'), (11.5, 3, 's')):
        zz = z - 1.7 if s == 'n' else z + 1.7
        m.box([x - 1.1, y, zz - 1.1], [x + 1.1, y + 7, zz + 1.1], 'cucumber', (22.5 if x > 8 else -22.5, 'z', [x, y + 7, zz]))
        m.box([x - 0.25, y + 7, zz - 0.25], [x + 0.25, y + 8.5, zz + 0.25], 'stem')
    return m


def onion():
    m = Model('onion')
    for (cx, cz, k) in ((4.8, 5, 0), (11.2, 11, 1), (11.5, 4.5, 2), (4.5, 11.5, 3)):
        s = 1.0 if k < 2 else 0.8
        m.box([cx - 2.6 * s, -1.5, cz - 2.6 * s], [cx + 2.6 * s, 2.2 * s, cz + 2.6 * s], 'onion_bulb', top='onion_top')
        m.box([cx - 1.8 * s, 2.2 * s, cz - 1.8 * s], [cx + 1.8 * s, 3.2 * s, cz + 1.8 * s], 'onion_bulb', top='onion_top')
        m.box([cx - 0.7, 3.2 * s, cz - 0.7], [cx + 0.7, 4.5 * s, cz + 0.7], 'onion_bulb', top='onion_top')
        for n, (ang, axis) in enumerate(((22.5, 'x'), (-22.5, 'x'), (22.5, 'z'), (-22.5, 'z'))):
            h = (11 + 2 * ((n + k) % 3)) * s
            if k == 3 and n == 1:
                ang = -45                               # a flopped leaf: this one is nearly ready
            m.box([cx - 0.45, 4.2 * s, cz - 0.45], [cx + 0.45, 4.2 * s + h, cz + 0.45], 'onion_leaf', (ang, axis, [cx, 4.2 * s, cz]))
    return m


def rice():
    m = Model('rice')
    r = random.Random(9)
    pts = [(4.5, 4.5), (11.5, 4), (8, 8.5), (4, 12), (12, 12)]
    for (x, z) in pts:
        for k in range(4):                              # upright stalks, each with a drooping golden head
            xx, zz = x + (-0.9, 0.9, 0, 0)[k], z + (0, 0, -0.9, 0.9)[k]
            h = 25 + r.random() * 5
            m.box([xx - 0.35, -1, zz - 0.35], [xx + 0.35, h, zz + 0.35], 'rice_stalk')
            if k < 3:
                ang, axis = ((45, 'z'), (-45, 'z'), (45, 'x'))[k]
                m.box([xx - 0.7, h - 6, zz - 0.7], [xx + 0.7, h, zz + 0.7], 'rice_grain', (ang, axis, [xx, h, zz]))
        for (ang, axis) in ((45, 'x'), (-45, 'x'), (45, 'z'), (-45, 'z'), (22.5, 'x'), (-22.5, 'z')):   # long leaves fanning out
            ln = 17 + r.random() * 4 if abs(ang) == 45 else 22
            m.box([x - 0.25, -1, z - 0.6], [x + 0.25, ln, z + 0.6], 'rice_stalk', (ang, axis, [x, -1, z]))
    return m


def blueberry():
    m = Model('blueberry')
    r = random.Random(11)
    for (x, z, a, ax) in ((8, 8, 0, 'x'), (6, 9, 22.5, 'z'), (10, 7, -22.5, 'x')):
        m.box([x - 0.6, -1, z - 0.6], [x + 0.6, 7, z + 0.6], 'bush_wood', (a, ax, [x, 0, z]) if a else None)
    mass = [([2, 5, 2], [14, 12, 14]), ([3.5, 12, 3.5], [12.5, 15.5, 12.5]), ([0.5, 6.5, 4], [15.5, 11, 12]),
            ([4, 6.5, 0.5], [12, 11, 15.5]), ([5, 3, 5], [11, 5, 11])]
    for f, t in mass:
        m.box(f, t, 'blue_leaf')
    berries = []
    for _ in range(34):
        side = r.choice(('n', 's', 'e', 'w', 'u'))
        if side == 'u':
            x, y, z = 4 + r.random() * 8, 15.4, 4 + r.random() * 8
        elif side in ('e', 'w'):
            x = 15.5 if side == 'e' else 0.5; y, z = 7 + r.random() * 3.5, 4.5 + r.random() * 7
        else:
            z = 15.5 if side == 's' else 0.5; y, x = 7 + r.random() * 3.5, 4.5 + r.random() * 7
        if side == 'n' and r.random() < 0.5:
            x, y, z = 2 + r.random() * 12, 12, 1.8
        berries.append((x, y, z))
    for n, (x, y, z) in enumerate(berries):
        tex = 'blueberry' if n % 7 else 'tomato_green'
        m.box([x - 1.1, y - 1.1, z - 1.1], [x + 1.1, y + 1.1, z + 1.1], tex)
    return m


def strawberry():
    m = Model('strawberry')
    m.box([0, 0, 0], [16, 0.5, 16], 'straw')
    m.box([7.2, 0.5, 7.2], [8.8, 2, 8.8], 'stem')
    for (d, t) in (('n', 22.5), ('e', 22.5), ('s', 22.5), ('w', 22.5)):
        cx, cz = 8, 8
        for k, (ln, y) in enumerate(((5.5, 4.5), (4, 3.2))):
            leaf_flat(m, cx, y, cz, ln + (0.8 if d in 'ns' else 0), 4.2 - k, d, t + (22.5 if k else 0), 'straw_leaf')
        # leaf stalk
    for (x, z) in ((3, 3), (13, 3), (13, 13), (3, 13)):
        m.box([min(x, 8) , 1.5, min(z, 8) - 0.3], [max(x, 8), 2.0, min(z, 8) + 0.3], 'stem') if False else None
    berries = [(3, 1.2, 11, 0), (12.5, 1.2, 4, 1), (12, 1.2, 12.5, 0), (4, 1.2, 4, 1), (10, 1.2, 14, 2)]
    for (x, y, z, k) in berries:
        tex = 'strawberry' if k < 2 else 'tomato_green'
        m.box([x - 1.6, 0.5, z - 1.4], [x + 1.6, 3.1, z + 1.4], tex)
        m.box([x - 1.1, 3.1, z - 1.0], [x + 1.1, 3.6, z + 1.0], 'straw_leaf')
        m.box([x - 0.3, 3.6, z - 0.3], [x + 0.3, 5.6, z + 0.3], 'stem', (22.5, 'x', [x, 3.6, z]))
    for (x, z) in ((6, 12.5), (11, 9)):
        m.box([x - 1, 5.2, z - 1], [x + 1, 5.7, z + 1], 'straw_flower')
        m.box([x - 0.2, 1, z - 0.2], [x + 0.2, 5.2, z + 0.2], 'stem')
    return m


def carrot_pulled():
    m = Model('carrot_pulled')
    # lying on its side along x: root tapering to the right, leaves to the left
    m.box([4, 0, 6.5], [8, 3, 9.5], 'carrot', top='carrot')
    m.box([8, 0.4, 6.9], [11, 2.6, 9.1], 'carrot')
    m.box([11, 0.8, 7.3], [13.5, 2.2, 8.7], 'carrot')
    m.box([13.5, 1.1, 7.7], [15, 1.9, 8.3], 'carrot')
    for (a, ax) in ((22.5, 'y'), (-22.5, 'y'), (0, 'y')):
        m.box([-2, 1, 7.5], [4, 2, 8.5], 'carrot_leaf', (a, ax, [4, 1.5, 8]) if a else None)
    for (a, ax) in ((45, 'y'), (-45, 'y')):
        m.box([-1, 1.2, 7.6], [4, 1.8, 8.4], 'carrot_leaf', (a, ax, [4, 1.5, 8]))
    return m


ALL = [tomato, cucumber, onion, rice, blueberry, strawberry, carrot_pulled]


def main():
    os.makedirs(os.path.join(ROOT, 'models', 'plant'), exist_ok=True)
    os.makedirs(os.path.join(ROOT, 'items'), exist_ok=True)
    names = []
    for fn in ALL:
        m = fn()
        for e in m.els:                                   # model limits: -16..32
            for v in e['from'] + e['to']:
                assert -16 <= v <= 32, (m.name, e)
        json.dump(m.json(), open(os.path.join(ROOT, 'models', 'plant', m.name + '.json'), 'w'), indent=1)
        json.dump({'model': {'type': 'minecraft:model', 'model': f'{NS}:plant/{m.name}'}},
                  open(os.path.join(ROOT, 'items', m.name + '.json'), 'w'), indent=1)
        names.append((m.name, len(m.els)))
    print(names)


if __name__ == '__main__':
    main()
