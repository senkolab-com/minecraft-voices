"""Where the plant models go in each bed: (dx, dz, model, yaw, scale) around the bed centre (interior dx -3..3,
dz -1..1, soil top = the entity's y). yaw is degrees in the model's own frame (rotated with the build facing)."""
import random


def bed_plants(kind):
    r = random.Random(hash(kind) % 1000)
    out = []
    if kind == 'tomato':
        for dz in (-1, 1):
            for dx in ((-3, -1, 1, 3) if dz < 0 else (-2.5, -0.5, 1.5, 3)):
                out.append((dx, dz, 'tomato', r.choice((0, 90, 180, 270)) + r.uniform(-15, 15), r.uniform(0.92, 1.08)))
    elif kind == 'cucumber':
        for dx in range(-3, 4):
            out.append((dx, 0, 'cucumber', 0, 1.0))
    elif kind == 'strawberry':
        for dx in range(-3, 4):
            for dz in (-1, 0, 1):
                out.append((dx, dz, kind, r.choice((0, 90, 180, 270)), 1.0))
    elif kind in ('onion', 'rice'):
        for dx in range(-3, 4):
            for dz in (-1, 0, 1):
                out.append((dx, dz, kind, r.uniform(0, 360), r.uniform(0.9, 1.1)))
    elif kind == 'blueberry':
        for dx in (-2.2, 0, 2.2):
            out.append((dx, 0, 'blueberry', r.uniform(0, 360), r.uniform(1.3, 1.45)))
    elif kind == 'carrot':
        out.append((4, 2, 'carrot_pulled', 200, 1.0))       # one pulled carrot on the border corner, for show
    return out
