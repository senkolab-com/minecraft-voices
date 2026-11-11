"""Build the garden-education datapack (Garden School island over the sea, all four facings, labels, plant models,
strolling gardeners that talk, one at a time).

  /function garden-education:build    hover over open sea where the island's front edge (the entrance arch side)
                                      should be, facing the way the garden should go; the island starts 3 blocks
                                      ahead, the entrance path on your line
  /function garden-education:remove   remove the nearest one (the sea comes back)
  /function garden-education:cancel   stop an unfinished build/removal
"""
import json
import math
import os
import shutil
import sys
import zipfile

import numpy as np

import garden as chocf
import garden_talk as T
import talklib

NS = 'garden-education'
TAG = NS
I_OFF = 3
J_OFF = 39
FACES = ('north', 'east', 'south', 'west')
VEC = {'south': (0, 0, 1), 'west': (-1, 0, 0), 'north': (0, 0, -1), 'east': (1, 0, 0)}
RIGHT = {'south': 'west', 'west': 'north', 'north': 'east', 'east': 'south'}
YAW = {'south': 0, 'west': 90, 'north': 180, 'east': -90}
STEP_VOL = 120000          # blocks per build step
STEP_CMDS = 3000
SEA_Y = 62                 # marker y = 63 + Y0 (y=0 of the model is the grass at world y 63)


def rot_dir(d, face):
    """a direction named for the north-facing build -> the same direction for another facing."""
    order = ['north', 'east', 'south', 'west']
    if d not in order:
        return d
    return order[(order.index(d) + order.index(face)) % 4]


def rot_state(state, face):
    if '[' not in state or face == 'north':
        return state
    name, props = state.split('[', 1)
    props = props.rstrip(']').split(',')
    out = []
    swap = face in ('east', 'west')
    conn = {}
    for p in props:
        k, v = p.split('=')
        if k == 'facing':
            v = rot_dir(v, face)
        elif k == 'rotation':
            v = str((int(v) + 4 * ['north', 'east', 'south', 'west'].index(face)) % 16)
        elif k == 'axis' and swap and v in ('x', 'z'):
            v = 'z' if v == 'x' else 'x'
        elif k in ('north', 'east', 'south', 'west'):
            conn[rot_dir(k, face)] = v
            continue
        out.append(f'{k}={v}')
    for k in ('east', 'north', 'south', 'west'):
        if k in conn:
            out.append(f'{k}={conn[k]}')
    return name + '[' + ','.join(out) + ']'


def world(x, y, z, face):
    """concept (x, y, z) -> marker-relative world offset for a facing. i = forward from the player, j = to the right."""
    i = (chocf.NZ - 1 - z) + I_OFF
    j = x - J_OFF
    F, R = VEC[face], VEC[RIGHT[face]]
    k = y - chocf.Y0
    return tuple(i * F[n] + j * R[n] + (k if n == 1 else 0) for n in range(3))


def rel(p):
    return ' '.join('~' if v == 0 else f'~{v}' for v in p)


def rects(layer):
    """greedy maximal rectangles of equal non-zero values in a 2D array: [(x0, x1, z0, z1, v)]."""
    X, Z = layer.shape
    done = np.zeros(layer.shape, bool)
    out = []
    for x in range(X):
        z = 0
        while z < Z:
            v = layer[x, z]
            if v == 0 or done[x, z]:
                z += 1
                continue
            z1 = z
            while z1 + 1 < Z and layer[x, z1 + 1] == v and not done[x, z1 + 1]:
                z1 += 1
            x1 = x
            while x1 + 1 < X and (layer[x1 + 1, z:z1 + 1] == v).all() and not done[x1 + 1, z:z1 + 1].any():
                x1 += 1
            done[x:x1 + 1, z:z1 + 1] = True
            out.append((x, x1, z, z1, v))
            z = z1 + 1
    return out


def block_commands(m, face, sign_nbt):
    g = m.g
    cmds = []
    vols = []
    nbt_at = {(x, y, z): s for (x, y, z, s) in sign_nbt}
    for k in range(g.shape[1]):
        y = k + chocf.Y0
        for (x0, x1, z0, z1, v) in rects(g[:, k, :]):
            st = rot_state(m.pal[v], face)
            if 'sign' in st or 'door' in st:
                continue
            a, b = world(x0, y, z0, face), world(x1, y, z1, face)
            if a == b:
                cmds.append(f'setblock {rel(a)} {st} strict')
            else:
                cmds.append(f'fill {rel(a)} {rel(b)} {st} strict')
            vols.append((x1 - x0 + 1) * (z1 - z0 + 1))
    # doors (both halves, upper after lower) and signs with their text, last
    late = []
    X, Y, Z = g.shape
    for idx in np.argwhere(np.isin(g, [i for i, p in enumerate(m.pal) if 'door' in p])):
        x, k, z = map(int, idx)
        late.append((('half=upper' in m.pal[g[x, k, z]]), x, k, z))
    for up, x, k, z in sorted(late):
        st = rot_state(m.pal[g[x, k, z]], face)
        cmds.append(f'setblock {rel(world(x, k + chocf.Y0, z, face))} {st} strict')
        vols.append(1)
    for (x, y, z, state, lines) in m.signs:
        st = rot_state(state, face)
        msgs = ','.join(json.dumps(l) for l in (lines + [''] * 4)[:4])
        cmds.append(f'setblock {rel(world(x, y, z, face))} {st}{{front_text:{{messages:[{msgs}],color:"white",has_glowing_text:1b}},is_waxed:1b}} strict')
        vols.append(1)
    return cmds, vols


def split_steps(cmds, vols):
    steps, cur, cv = [], [], 0
    for c, v in zip(cmds, vols):
        if cur and (cv + v > STEP_VOL or len(cur) >= STEP_CMDS):
            steps.append(cur)
            cur, cv = [], 0
        cur.append(c)
        cv += v
    if cur:
        steps.append(cur)
    return steps


def bbox(face):
    pts = [world(x, y, z, face) for x in (0, chocf.NX - 1) for z in (0, chocf.NZ - 1) for y in (chocf.Y0, chocf.Y1)]
    lo = [min(p[n] for p in pts) for n in range(3)]
    hi = [max(p[n] for p in pts) for n in range(3)]
    return lo, hi


def clear_commands(face, air_from_y, water=False):
    """fill the model's box: air from concept y air_from_y up (and water below it down to the island bottom when
    removing). Split in layers (each <= 32768 blocks)."""
    lo, hi = bbox(face)
    out = []
    k_air = air_from_y - chocf.Y0
    for k in range(k_air, chocf.NY):
        out.append(f'fill ~{lo[0]} ~{k} ~{lo[2]} ~{hi[0]} ~{k} ~{hi[2]} minecraft:air strict')
    if water:
        for k in range(0, k_air):
            out.append(f'fill ~{lo[0]} ~{k} ~{lo[2]} ~{hi[0]} ~{k} ~{hi[2]} minecraft:water strict')
    return out


def forceload(face, add=True):
    lo, hi = bbox(face)
    return f'forceload {"add" if add else "remove"} ~{lo[0]} ~{lo[2]} ~{hi[0]} ~{hi[2]}'


def label_entities(m, face):
    out = []
    for (x, y, z, title, sub, facing) in m.labels:
        p = world(x, y + 2, z, face)
        txt = '{text:%s,color:"gold",bold:true%s}' % (
            json.dumps(title), (',extra:[{text:%s,color:"white",bold:false}]' % json.dumps('\n' + sub)) if sub else '')
        out.append(f'summon minecraft:text_display {rel(p)} {{text:{txt},billboard:"center",alignment:"center",'
                   f'background:1073741824,see_through:0b,shadow:1b,line_width:400,'
                   f'transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[1.6f,1.6f,1.6f]}},'
                   f'Tags:["{TAG}_npc","{TAG}_label"]}}')
    return out


WS = f'{TAG}_w'          # walker scores: _s = the corner being walked to (0..3), _p = pause ticks left
SPEED = 0.05             # blocks per tick (a slow stroll)


def plant_entities(m, face):
    out = []
    turn = 90 * ['north', 'east', 'south', 'west'].index(face)
    for (x, y, z, model, yaw, s) in m.plants:
        p = world(x, y, z, face)
        out.append(f'summon minecraft:item_display {rel(tuple(round(v, 3) for v in p))} {{item:{{id:"minecraft:paper",count:1,'
                   f'components:{{"minecraft:item_model":"{NS}:{model}"}}}},item_display:"none",'
                   f'Rotation:[{round((yaw + turn) % 360 - 180, 1)}f,0f],'
                   f'transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],'
                   f'translation:[0f,{round(0.5 * s, 3)}f,0f],scale:[{round(s, 3)}f,{round(s, 3)}f,{round(s, 3)}f]}},'
                   f'view_range:0.5f,Tags:["{TAG}_npc","{TAG}_plant"]}}')
    return out


def repair_commands(m, face):
    """trampled farmland -> dirt and lost carrots: put them back (run every 5 s at the origin marker)."""
    out = []
    for (x0, x1, y, z0, z1, st, rep) in m.repair:
        a, b = world(x0, y, z0, face), world(x1, y, z1, face)
        out.append(f'fill {rel(a)} {rel(b)} {rot_state(st, face)} replace {rep}')
    return out


def walker_functions(npcs):
    """each gardener walks round the path of their bed, corner to corner, pausing at each corner; stops to face a
    player who comes near, and stands still while talking (busy)."""
    F = {}
    busy = f'{NS}_tk_busy'
    F['walk/tick'] = [f'execute as @e[type=minecraft:villager,tag={TAG}_walker] at @s run function {NS}:walk/n']
    F['walk/n'] = [f'execute if entity @s[tag={TAG}_t{n["id"]}] run return run function {NS}:walk/{n["id"]}' for n in npcs]
    for n in npcs:
        i = n['id']
        c = lambda k, extra='': f'@e[type=minecraft:marker,tag={TAG}_c{i}_{k % 4},{extra}limit=1]'
        body = [f'execute if score @s {busy} matches 1.. run return 0',
                f'execute if entity @a[distance=..3.5,gamemode=!spectator] run return run tp @s ~ ~ ~ facing entity @p[distance=..3.5,gamemode=!spectator] eyes',
                f'execute if score @s {WS}_p matches 1.. run return run scoreboard players remove @s {WS}_p 1']
        for k in range(4):
            body.append(f'execute if score @s {WS}_s matches {k} if entity {c(k, 'distance=..0.08,')} run return run function {NS}:walk/{i}_at{k}')
        for k in range(4):
            body.append(f'execute if score @s {WS}_s matches {k} facing entity {c(k)} feet run return run tp @s ^ ^ ^{SPEED} ~ ~')
        body.append(f'scoreboard players set @s {WS}_s 0')
        F[f'walk/{i}'] = body
        for k in range(4):
            F[f'walk/{i}_at{k}'] = [f'execute at {c(k)} facing entity {c(k + 1)} feet run tp @s ~ ~ ~ ~ ~',
                                    f'scoreboard players set @s {WS}_s {(k + 1) % 4}',
                                    f'execute store result score @s {WS}_p run random value 30..90']
    return F


def build_pack(out_dir, out_zip):
    m = chocf.build()
    npcs = []
    for (nid, role, name, prof, story) in T.NPCS:
        npcs.append({'id': nid, 'role': role, 'name': name, 'intro': story, 'prof': prof, 'vtype': T.ROLES[role]['vtype'],
                     'walk': m.walks[role]})
    durs = {}
    dp = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'durations.json')
    if os.path.exists(dp):
        durs = json.load(open(dp))
    tk = talklib.Talk(NS, T.ROLES, T.LINES, T.LAUGHS, npcs, durs, quiet=96)
    shutil.rmtree(out_dir, ignore_errors=True)
    fn = os.path.join(out_dir, 'data', NS, 'function')
    W = {}
    sel = f'type=minecraft:marker,tag={TAG}_origin'
    O = f'{TAG}_step'
    W['internal/init'] = [f'scoreboard objectives add {O} dummy']
    # ---- build
    W['build'] = [
        f'execute unless block ~ {SEA_Y} ~ minecraft:water run tellraw @s {{"text":"Garden School: there must be sea water under you at y {SEA_Y}. Hover over open ocean.","color":"red"}}',
        f'execute unless block ~ {SEA_Y} ~ minecraft:water run return 0',
        f'execute if entity @e[{sel},tag={TAG}_pending] run tellraw @s {{"text":"Garden School: a build is still running - wait, or /function {NS}:cancel.","color":"red"}}',
        f'execute if entity @e[{sel},tag={TAG}_pending] run return 0',
        f'execute if entity @e[{sel},tag={TAG}_removing] run tellraw @s {{"text":"Garden School: a removal is still running.","color":"red"}}',
        f'execute if entity @e[{sel},tag={TAG}_removing] run return 0',
        f'execute align xz positioned ~0.5 {SEA_Y + 1 + chocf.Y0} ~0.5 run summon minecraft:marker ~ ~ ~ {{Tags:["{TAG}_origin","{TAG}_new","{TAG}_pending"]}}',
        f'execute if entity @s[y_rotation=-45..45] run tag @e[{sel},tag={TAG}_new] add {TAG}_south',
        f'execute if entity @s[y_rotation=45..135] run tag @e[{sel},tag={TAG}_new] add {TAG}_west',
        f'execute if entity @s[y_rotation=135..180] run tag @e[{sel},tag={TAG}_new] add {TAG}_north',
        f'execute if entity @s[y_rotation=-180..-135] run tag @e[{sel},tag={TAG}_new] add {TAG}_north',
        f'execute if entity @s[y_rotation=-135..-45] run tag @e[{sel},tag={TAG}_new] add {TAG}_east',
        f'tag @e[{sel},tag={TAG}_new] remove {TAG}_new',
    ] + [f'execute as @e[{sel},tag={TAG}_pending,tag={TAG}_{f}] at @s run {forceload(f)}' for f in FACES] + [
        f'scoreboard players set #b {O} 0',
        f'tellraw @s {{"text":"Garden School: loading the area, building the island in 3 seconds...","color":"yellow"}}',
        f'schedule function {NS}:internal/tick 60t replace']
    nb = {}
    for f in FACES:
        d = f'internal/{f}'
        steps = split_steps(*block_commands(m, f, []))
        clears = clear_commands(f, 0)
        allsteps = [clears[:40], clears[40:]] + steps
        for n, s in enumerate(allsteps, 1):
            W[f'{d}/s{n}'] = s
        nb[f] = len(allsteps)
        npc_lines = []
        for n in npcs:
            c = n['walk']
            p = world(*c[0], f)
            q = world(*c[1], f)
            yaw = math.degrees(math.atan2(-(q[0] - p[0]), q[2] - p[2]))      # facing the next corner
            npc_lines.append(tk.summon(n, rel(p), round(yaw, 1), (f'{TAG}_walker',)))
            for k, cc in enumerate(c):
                npc_lines.append(f'summon minecraft:marker {rel(world(*cc, f))} {{Tags:["{TAG}_npc","{TAG}_corner","{TAG}_c{n["id"]}_{k}"]}}')
        npc_lines += [f'scoreboard players set @e[tag={TAG}_walker] {WS}_s 1', f'scoreboard players set @e[tag={TAG}_walker] {WS}_p 40']
        W[f'{d}/done'] = npc_lines + plant_entities(m, f) + label_entities(m, f) + [
            f'execute as @e[{sel},tag={TAG}_pending,tag={TAG}_{f}] at @s run {forceload(f, False)}',
            f'tag @e[{sel},tag={TAG}_pending,tag={TAG}_{f}] remove {TAG}_pending',
            'tellraw @a {"text":"Garden School is built! Walk up to a gardener to hear about their plants.","color":"green"}']
        W[f'{d}/repair'] = repair_commands(m, f)
        lo, hi = bbox(f)
        W[f'{d}/rsteps'] = []
        rc = clear_commands(f, 0, water=True)
        W[f'{d}/r1'] = [f'execute positioned ~{lo[0]} ~-2 ~{lo[2]} run kill @e[tag={TAG}_npc,dx={hi[0] - lo[0]},dy={chocf.NY + 4},dz={hi[2] - lo[2]}]'] + rc[:40]
        W[f'{d}/r2'] = rc[40:]
        W[f'{d}/rdone'] = [f'execute positioned ~{lo[0]} ~-2 ~{lo[2]} run kill @e[type=minecraft:item,dx={hi[0] - lo[0]},dy={chocf.NY + 4},dz={hi[2] - lo[2]}]',
                           forceload(f, False),
                           f'kill @s', 'tellraw @a {"text":"Garden School removed.","color":"green"}']
    tick = [f'scoreboard players add #b {O} 1']
    for f in FACES:
        for n in range(1, nb[f] + 1):
            tick.append(f'execute if score #b {O} matches {n} as @e[{sel},tag={TAG}_pending,tag={TAG}_{f}] at @s run function {NS}:internal/{f}/s{n}')
        tick.append(f'execute if score #b {O} matches {nb[f] + 1} as @e[{sel},tag={TAG}_pending,tag={TAG}_{f}] at @s run function {NS}:internal/{f}/done')
    mx = max(nb.values()) + 1
    tick.append(f'execute if score #b {O} matches ..{mx - 1} if entity @e[{sel},tag={TAG}_pending] run schedule function {NS}:internal/tick 4t replace')
    W['internal/tick'] = tick
    W['remove'] = [
        f'execute unless entity @e[{sel},tag=!{TAG}_pending,tag=!{TAG}_removing,distance=..300] run tellraw @s {{"text":"No Garden School within 300 blocks.","color":"red"}}',
        f'execute unless entity @e[{sel},tag=!{TAG}_pending,tag=!{TAG}_removing,distance=..300] run return 0',
        f'tag @e[{sel},tag=!{TAG}_pending,tag=!{TAG}_removing,distance=..300,sort=nearest,limit=1] add {TAG}_removing'] + \
        [f'execute as @e[{sel},tag={TAG}_removing,tag={TAG}_{f}] at @s run {forceload(f)}' for f in FACES] + [
        f'scoreboard players set #r {O} 0', 'tellraw @s {"text":"Garden School: removing it in 3 seconds...","color":"yellow"}',
        f'schedule function {NS}:internal/rtick 60t replace']
    rt = [f'scoreboard players add #r {O} 1']
    for f in FACES:
        for n, nm in ((1, 'r1'), (2, 'r2'), (3, 'rdone')):
            rt.append(f'execute if score #r {O} matches {n} as @e[{sel},tag={TAG}_removing,tag={TAG}_{f}] at @s run function {NS}:internal/{f}/{nm}')
    rt.append(f'execute if score #r {O} matches ..2 run schedule function {NS}:internal/rtick 4t replace')
    W['internal/rtick'] = rt
    W['cancel'] = [f'schedule clear {NS}:internal/tick', f'schedule clear {NS}:internal/rtick',
                   f'tag @e[{sel}] remove {TAG}_removing',
                   f'kill @e[{sel},tag={TAG}_pending]',
                   'tellraw @s {"text":"Garden School: stopped. Run remove to clear a half-built one.","color":"yellow"}']
    # strolling gardeners
    W['internal/init'] += [f'scoreboard objectives add {WS}_s dummy', f'scoreboard objectives add {WS}_p dummy']
    W.update(walker_functions(npcs))
    W['internal/rtick2'] = [f'execute as @e[{sel},tag=!{TAG}_pending,tag=!{TAG}_removing,tag={TAG}_{f}] at @s run function {NS}:internal/{f}/repair' for f in FACES] + [
        f'schedule function {NS}:internal/rtick2 100t replace']
    W['internal/init'] += [f'schedule function {NS}:internal/rtick2 100t replace']
    # talking gardeners
    W.update(tk.functions())
    talklib.write_functions(W, fn)
    tags = os.path.join(out_dir, 'data', 'minecraft', 'tags', 'function')
    os.makedirs(tags, exist_ok=True)
    json.dump({'values': [f'{NS}:internal/init', f'{NS}:talk/init']}, open(os.path.join(tags, 'load.json'), 'w'))
    json.dump({'values': [f'{NS}:talk/tick', f'{NS}:walk/tick']}, open(os.path.join(tags, 'tick.json'), 'w'))
    json.dump({'pack': {'description': 'Garden School - /function garden-education:build', 'min_format': 88, 'max_format': 107}},
              open(os.path.join(out_dir, 'pack.mcmeta'), 'w'), indent=2)
    if os.path.exists(out_zip):
        os.remove(out_zip)
    with zipfile.ZipFile(out_zip, 'w', zipfile.ZIP_DEFLATED) as z:
        for rt_, _, fs in os.walk(out_dir):
            for x in fs:
                full = os.path.join(rt_, x)
                z.write(full, os.path.relpath(full, out_dir))
    stats = {f: (nb[f], sum(len(W[f'internal/{f}/s{n}']) for n in range(1, nb[f] + 1))) for f in FACES}
    return m, tk, stats


if __name__ == '__main__':
    m, tk, st = build_pack('out/pack', 'out/garden-education_datapack.zip')
    print('steps/commands per face', st, 'clips', len(tk.clips()))
