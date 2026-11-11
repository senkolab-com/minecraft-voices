"""Pixel-art textures (16x16) for the garden plant models. All drawn here, no game assets."""
import os
import numpy as np
from PIL import Image

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'res', 'assets', 'garden-education', 'textures', 'plant')
rng = np.random.default_rng(42)


def hexc(h):
    h = h.lstrip('#'); return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], float)


def base(col, noise=10, size=16):
    a = np.zeros((size, size, 3)) + hexc(col)
    a += rng.normal(0, noise, (size, size, 1))
    return a


def save(name, a, alpha=None):
    os.makedirs(OUT, exist_ok=True)
    a = np.clip(a, 0, 255).astype(np.uint8)
    if alpha is None:
        alpha = np.full(a.shape[:2], 255, np.uint8)
    Image.fromarray(np.dstack([a, alpha]), 'RGBA').save(os.path.join(OUT, name + '.png'))


def shade(a, top=1.12, bottom=0.88):
    s = np.linspace(top, bottom, a.shape[0])[:, None, None]
    return a * s


def leaf(name, col, vein, dark):
    a = base(col, 9)
    for y in range(16):
        for x in range(16):
            if x in (7, 8):
                a[y, x] = hexc(vein) + rng.normal(0, 5, 3)
            elif abs((x - 7.5)) + (15 - y) * 0.5 in (5.5, 6, 6.5) and y % 3 == 0:
                a[y, x] = hexc(vein) * 0.95
    edge = (rng.random((16, 16)) < 0.10)
    a[edge] = hexc(dark)
    save(name, shade(a))


def fruit(name, col, hi, lo, seeds=None, seedcol=None):
    a = base(col, 6)
    yy, xx = np.mgrid[0:16, 0:16]
    d = np.hypot(xx - 5, yy - 4)
    a = a * (1.0 + 0.22 * np.clip(1 - d / 7, 0, 1)[..., None])
    a[(xx >= 3) & (xx <= 5) & (yy >= 2) & (yy <= 4)] = hexc(hi)
    a[yy >= 13] = a[yy >= 13] * 0.85
    a[(xx >= 14) | (yy >= 15)] = a[(xx >= 14) | (yy >= 15)] * 0.85
    if seeds:
        for (sx, sy) in seeds:
            a[sy, sx] = hexc(seedcol)
    save(name, a)


def main():
    # tomato plant
    leaf('tomato_leaf', '#3f8a2e', '#5aa83f', '#2a6420')
    save('stem', shade(base('#4d8f32', 8)))
    a = base('#9a6b3c', 8)
    for x in range(16):
        a[:, x] *= 0.9 + 0.1 * np.sin(x * 1.7)
    save('stake', a)
    fruit('tomato_red', '#d8261d', '#ff8a7a', '#8f1410')
    fruit('tomato_orange', '#e8741f', '#ffc08a', '#a04a10')
    fruit('tomato_green', '#7fb63a', '#c4e88a', '#4f7f20')
    a = base('#d8261d', 6); s = hexc('#3e8a2a')
    for (x, y) in [(7, 7), (8, 7), (7, 8), (8, 8), (7, 5), (8, 5), (7, 6), (8, 10), (7, 9), (5, 7), (4, 8), (10, 8), (11, 7), (5, 10), (10, 5)]:
        a[y, x] = s
    save('tomato_top', a)
    # cucumber
    a = base('#2f6b2a', 7)
    for y in range(16):
        for x in range(16):
            if (x % 4 == 1) and rng.random() < 0.6:
                a[y, x] = hexc('#5f9a3d')
            if rng.random() < 0.06:
                a[y, x] = hexc('#a8d080')
    save('cucumber', a)
    leaf('cuc_leaf', '#3d8f36', '#68b04a', '#276a22')
    a = base('#f2d132', 8); a[6:10, 6:10] = hexc('#d89a12'); save('cuc_flower', a)
    a = base('#c8b07a', 6)
    for i in range(16):
        a[i, :] *= 0.92 + 0.08 * ((i % 3) == 0)
    save('twine', a)
    a = base('#6f4e2c', 8)
    for x in range(0, 16, 5):
        a[:, x] *= 0.8
    save('post', a)
    # onion
    a = base('#c48a3a', 7)
    for x in range(16):
        if x % 3 == 0:
            a[:, x] = a[:, x] * 0.82
        if x % 3 == 1:
            a[:, x] = a[:, x] * 1.08
    a[:3] = a[:3] * 1.12
    save('onion_bulb', a)
    a = base('#e8d6a8', 6)
    yy, xx = np.mgrid[0:16, 0:16]
    a[np.hypot(xx - 7.5, yy - 7.5) < 3] = hexc('#8faa58')
    save('onion_top', a)
    a = base('#5f9a6a', 7)
    for x in range(16):
        a[:, x] *= 0.9 + 0.12 * (x % 4 == 0)
    a[12:] = a[12:] * 1.08
    save('onion_leaf', a)
    # rice
    a = base('#6fae3e', 7)
    for x in range(16):
        a[:, x] *= 0.92 + 0.1 * (x % 3 == 0)
    save('rice_stalk', shade(a))
    a = base('#d6b24a', 8)
    for y in range(16):
        for x in range(16):
            if (x + 2 * (y % 2)) % 4 == 0:
                a[y, x] = hexc('#f0d888')
            elif (x + 2 * (y % 2)) % 4 == 2:
                a[y, x] = hexc('#a8842a')
    save('rice_grain', a)
    # blueberry
    leaf('blue_leaf', '#3d7a3a', '#5a9a4a', '#2c5a2a')
    a = base('#3a4f9a', 6)
    a = a * (1.0 + 0.25 * np.clip(1 - np.hypot(xx - 5, yy - 4) / 7, 0, 1)[..., None])
    a[(rng.random((16, 16)) < 0.18)] = hexc('#8a9ac8')
    a[6:9, 6:9] = hexc('#1e2550'); a[7, 7] = hexc('#5a3a6a')
    save('blueberry', a)
    a = base('#6a4a30', 8); save('bush_wood', a)
    # strawberry
    leaf('straw_leaf', '#3f9a3a', '#66b84e', '#2a6a26')
    seeds = [(x, y) for y in range(1, 16, 3) for x in range((y // 3) % 2 * 2 + 1, 16, 4)]
    fruit('strawberry', '#e0202a', '#ff7a80', '#8a0e14', seeds, '#f2d34a')
    a = base('#f4f2ea', 5); a[5:11, 5:11] = hexc('#f0c832'); a[6:10, 6:10] = hexc('#e0a820'); save('straw_flower', a)
    a = base('#d8b85a', 10)
    for y in range(16):
        for x in range(16):
            if (x * 3 + y * 5) % 7 == 0:
                a[y, x] = hexc('#f0d888')
            if (x * 5 + y * 3) % 11 == 0:
                a[y, x] = hexc('#a88a3a')
    save('straw', a)
    # carrot (pulled one on show)
    a = base('#e87a1e', 6)
    for y in range(1, 16, 4):
        a[y, :] *= 0.85
    save('carrot', a)
    leaf('carrot_leaf', '#4fa83a', '#7ac85a', '#2f7a26')
    print('textures in', OUT)


if __name__ == '__main__':
    main()
