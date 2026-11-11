"""talklib - talking NPCs for Minecraft datapacks (Java 26.x), shared by every model.

A model gives: MODEL (namespace + prefix), ROLES, LINES (per role: (type, text)), LAUGHS (per role: texts),
NPCS (id, role, name, ...) with spots, and the clip durations (seconds) measured after audio generation.

Behaviour (handover requirements D/E):
- proximity trigger 3 blocks, re-armed when the player is 6+ blocks away (player tag <m>_n<id>);
- first meeting -> the NPC's introduction (player tag <m>_m<id>, persistent), later -> the next line of the role's
  list for that player (score <m>_tk_p_<role>, persistent), cycling through a build-time shuffle;
- one clip at a time per NPC (score <m>_tk_busy, ticks); the NPC turns to the player; subtitles in chat to players
  within 8 blocks; the sound goes to players within 8 blocks (D7);
- quiet (optional): an NPC does not start while another talker of the model within `quiet` blocks is speaking
  (tag <m>_spk); it starts as soon as that one has finished, if the player is still there;
- long clips: subtitles are split at sentences into chunks of about 150 characters and shown in time with the
  speech (score <m>_tk_el counts the ticks since the clip started, <m>_tk_cl is the clip's subtitle number);
- a role without lines repeats its NPCs' introductions on every visit;
- jokes: other idle talkers within 8 blocks turn to the speaker and laugh when the punchline lands, each a few ticks
  apart with one of 3 recorded laughs in their own role's voice at one of 3 pitches, with happy-villager particles.
Everything global is named after the model (scores <m>_tk*, tags <m>_*, sounds <m>.voice.*).
Sound events live in the minecraft namespace (minecraft:<m>.voice.x) so Geyser forwards them to Bedrock as
'<m>.voice.x', the same key as in the Bedrock pack's sound_definitions.json.
"""
import json
import os
import random
import re

STEP = 2                # ticks between NPC updates
NEAR, FAR, HEAR = 3, 6, 8


def strip_tags(t):
    t = re.sub(r'\[[^\]]*\]\s*', '', t)
    return re.sub(r'\s+', ' ', t).strip()


def jtext(s):
    return json.dumps(s, ensure_ascii=False)


class Talk:
    def __init__(self, model, roles, lines, laughs, npcs, durations, seed=1912, active=None, quiet=None, chunk=150):
        self.m = model
        self.quiet, self.chunk = quiet, chunk
        self.subs = {}                             # clip key -> (subtitle number, [chunks]) for multi-chunk clips
        self.roles, self.lines, self.laughs, self.npcs = roles, lines, laughs, npcs
        self.dur = durations                       # {clip_key: seconds}
        rnd = random.Random(seed)
        # active: {role: [line indices in use]} - lines keep their index (and clip name) when more are added later
        self.active = active or {r: list(range(len(ls))) for r, ls in lines.items()}
        self.order = {}
        for r, ls in lines.items():               # build-time shuffle, keeping jokes spread out
            idx = list(self.active[r])
            for _ in range(200):
                rnd.shuffle(idx)
                if all(not (ls[idx[n]][0] == 'joke' and ls[idx[(n + 1) % len(idx)]][0] == 'joke') for n in range(len(idx))):
                    break
            self.order[r] = idx

    # ---- clip names (sound event keys without namespace, file stems)
    def k_intro(self, nid):
        return f'{self.m}.voice.n{nid:03d}'

    def k_line(self, role, n):
        return f'{self.m}.voice.{role}.l{n:02d}'

    def k_laugh(self, role, n):
        # laughs are shared by every model that uses the same voice (voice library: npcvoice.laugh.<voice>.<n>)
        return f'npcvoice.laugh.{self.roles[role]["voice"]}.{n + 1}'

    def clips(self):
        """every clip: key -> (role, text with audio tags)."""
        out = {}
        for n in self.npcs:
            out[self.k_intro(n['id'])] = (n['role'], n['intro'])
        for r, ls in self.lines.items():
            for i in self.active[r]:
                out[self.k_line(r, i)] = (r, ls[i][1])
        for r, ls in self.laughs.items():
            for i, t in enumerate(ls):
                out.setdefault(self.k_laugh(r, i), (r, t))
        return out

    def ticks(self, key, pad=0.4):
        return int(round((self.dur.get(key, 8.0) + pad) * 20))

    def chunks(self, text):
        t = strip_tags(text)
        if not self.chunk or len(t) <= self.chunk * 1.3:
            return [t]
        out, cur = [], ''
        for sen in re.split(r'(?<=[.!?])\s+', t):
            if cur and len(cur) + 1 + len(sen) > self.chunk:
                out.append(cur); cur = sen
            else:
                cur = (cur + ' ' + sen).strip()
        if cur:
            out.append(cur)
        return out

    def start(self, key, text, label_json):
        """commands that start clip `key` (run as the player, NPC tagged <m>_tk_cur): sound, first subtitle, busy, spk."""
        m, S = self.m, f'{self.m}_tk'
        ch = self.chunks(text)
        cur = f'@e[tag={m}_tk_cur,limit=1]'
        out = [f'playsound minecraft:{key} voice @a[distance=..{HEAR}] ~ ~1.6 ~ 1 1',
               'tellraw @a[distance=..%d] [%s,{"text":%s,"color":"white"}]' % (HEAR, label_json, jtext(ch[0])),
               f'scoreboard players set {cur} {S}_busy {self.ticks(key)}',
               f'scoreboard players set {cur} {S}_el 0',
               f'tag {cur} add {m}_spk',
               f'scoreboard players set #did {S} 1']
        if len(ch) > 1:
            num = self.subs[key][0] if key in self.subs else len(self.subs) + 1
            self.subs[key] = (num, ch)
            out.append(f'scoreboard players set {cur} {S}_cl {num}')
        else:
            out.append(f'scoreboard players set {cur} {S}_cl 0')
        return out

    # ---- datapack functions
    def functions(self):
        m = self.m
        S = f'{m}_tk'
        F = {}
        sel_talker = f'type=minecraft:villager,tag={m}_talker'
        F['talk/init'] = [f'scoreboard objectives add {S} dummy', f'scoreboard objectives add {S}_busy dummy',
                          f'scoreboard objectives add {S}_laugh dummy', f'scoreboard objectives add {S}_el dummy',
                          f'scoreboard objectives add {S}_cl dummy'] + \
                         [f'scoreboard objectives add {S}_p_{r} dummy' for r in self.roles]
        F['talk/tick'] = [f'scoreboard players add #t {S} 1',
                          f'execute if score #t {S} matches {STEP}.. run function {m}:talk/step']
        step = [f'scoreboard players set #t {S} 0',
                f'execute unless entity @e[{sel_talker}] run return 0']
        for n in self.npcs:
            step.append(f'execute as @e[{sel_talker},tag={m}_t{n["id"]},limit=1] at @s run function {m}:talk/n/{n["id"]}')
        F['talk/step'] = step
        for n in self.npcs:
            nid, role = n['id'], n['role']
            lab = f'{n["name"]} · {self.roles[role]["label"]}'
            F[f'talk/n/{nid}'] = [
                f'execute if score @s {S}_busy matches 1.. run scoreboard players remove @s {S}_busy {STEP}',
                f'execute unless entity @s[tag={m}_offers] run function {m}:talk/offers',
                f'execute if score @s {S}_laugh matches 1.. run function {m}:talk/r/{role}/laugh_tick',
                f'execute if score @s {S}_cl matches 1.. run function {m}:talk/sub',
                f'execute unless score @s {S}_busy matches 1.. run tag @s remove {m}_spk',
                f'execute unless score @s {S}_busy matches 1.. run scoreboard players set @s {S}_cl 0',
                f'execute if score @s {S}_busy matches 1.. run return 0',
                f'tag @a[tag={m}_n{nid},distance={FAR}..] remove {m}_n{nid}',
                f'execute unless entity @a[distance=..{NEAR},tag=!{m}_n{nid},gamemode=!spectator] run return 0'] + (
                [f'execute if entity @e[{sel_talker},tag={m}_spk,distance=..{self.quiet}] run return 0'] if self.quiet else []) + [
                f'tag @s add {m}_tk_cur',
                f'execute as @p[distance=..{NEAR},tag=!{m}_n{nid},gamemode=!spectator] run function {m}:talk/n/{nid}_speak',
                f'tag @s remove {m}_tk_cur']
            F[f'talk/n/{nid}_speak'] = [
                f'tag @a[distance=..{NEAR + 1}] add {m}_n{nid}',
                f'execute as @e[tag={m}_tk_cur,limit=1] at @s facing entity @p[distance=..{NEAR + 1}] eyes run tp @s ~ ~ ~ ~ 0',
                f'scoreboard players set #did {S} 0',
                (f'execute if entity @s[tag=!{m}_m{nid}] run function {m}:talk/n/{nid}_intro' if self.lines.get(role)
                 else f'function {m}:talk/n/{nid}_intro')] + (
                [f'execute if score #did {S} matches 0 run function {m}:talk/r/{role}/next'] if self.lines.get(role) else [])
            key = self.k_intro(nid)
            F[f'talk/n/{nid}_intro'] = [f'tag @s add {m}_m{nid}'] + self.start(
                key, n['intro'], '{"text":%s,"color":"%s"}' % (jtext(lab + ': '), self.roles[role]['colour']))
        for r, ls in self.lines.items():
            L = len(self.order[r])
            if not L:
                continue
            nxt = [f'execute unless score @s {S}_p_{r} matches 0..{L - 1} run scoreboard players set @s {S}_p_{r} 0',
                   f'scoreboard players operation #cur {S} = @s {S}_p_{r}',
                   f'scoreboard players add @s {S}_p_{r} 1',
                   f'execute if score @s {S}_p_{r} matches {L}.. run scoreboard players set @s {S}_p_{r} 0']
            for pos, li in enumerate(self.order[r]):
                nxt.append(f'execute if score #cur {S} matches {pos} run function {m}:talk/r/{r}/l{li:02d}')
            F[f'talk/r/{r}/next'] = nxt
            for li in self.active[r]:
                typ, text = ls[li]
                key = self.k_line(r, li)
                body = self.start(key, text, '{"selector":"@e[tag=%s_tk_cur,limit=1]","color":"%s"},{"text":": ","color":"%s"}' % (
                    m, self.roles[r]['colour'], self.roles[r]['colour']))
                if typ == 'joke':
                    at = max(self.ticks(key, pad=0.0) - 6, 10)          # just as the punchline lands
                    body += [f'scoreboard players set #lat {S} {at}',
                             f'execute as @e[{sel_talker},tag=!{m}_tk_cur,distance=..{HEAR}] at @s run function {m}:talk/laugh_arm']
                F[f'talk/r/{r}/l{li:02d}'] = body
            # laughs: 3 clips x 3 pitches, picked at random
            nl = len(self.laughs.get(r, []))
            lt = [f'scoreboard players remove @s {S}_laugh {STEP}',
                  f'execute if score @s {S}_laugh matches 1.. run return 0',
                  'particle minecraft:happy_villager ~ ~2.1 ~ 0.35 0.3 0.35 0 7 normal @a[distance=..24]']
            if nl:
                lt.append(f'execute store result score #lv {S} run random value 0..{nl * 3 - 1}')
            for v in range(nl * 3):
                clip, pitch = v // 3, (0.92, 1.0, 1.08)[v % 3]
                key = self.k_laugh(r, clip)
                lt.append(f'execute if score #lv {S} matches {v} run playsound minecraft:{key} voice @a[distance=..{HEAR + 4}] ~ ~1.6 ~ 0.9 {pitch}')
            F[f'talk/r/{r}/laugh_tick'] = lt
        F['talk/laugh_arm'] = [
            f'execute if score @s {S}_busy matches 1.. run return 0',
            f'tp @s ~ ~ ~ facing entity @e[tag={m}_tk_cur,limit=1] eyes',
            f'execute store result score @s {S}_laugh run random value 0..9',
            f'scoreboard players operation @s {S}_laugh += #lat {S}',
            f'scoreboard players operation @s {S}_busy = @s {S}_laugh',
            f'scoreboard players add @s {S}_busy 50']
        # timed subtitle chunks of long clips (run as and at the speaking NPC every STEP ticks)
        sub = [f'scoreboard players add @s {S}_el {STEP}']
        for key, (num, ch) in sorted(self.subs.items(), key=lambda kv: kv[1][0]):
            total = sum(len(c) for c in ch)
            dur = self.dur.get(key, 8.0) * 20
            done = 0
            col = self.roles[self.clips()[key][0]]['colour']
            for c in ch[:-1]:
                done += len(c)
                at = max(int(dur * done / total) - 10, STEP) // STEP * STEP   # a moment before the sentence starts
                sub.append(('execute if score @s %s_cl matches %d if score @s %s_el matches %d..%d run tellraw @a[distance=..%d] '
                            '[{"selector":"@s","color":"%s"},{"text":": ","color":"%s"},{"text":%s,"color":"white"}]') % (
                    S, num, S, at, at + STEP - 1, HEAR, col, col, jtext(ch[ch.index(c) + 1])))
        F['talk/sub'] = sub
        F['talk/offers'] = ['data merge entity @s {Offers:{Recipes:[]}}', f'tag @s add {m}_offers']
        # forget a player's progress (run as the player): introductions and line positions start again
        F['talk_reset'] = [f'tag @s remove {m}_m{n["id"]}' for n in self.npcs] + \
                          [f'tag @s remove {m}_n{n["id"]}' for n in self.npcs] + \
                          [f'scoreboard players reset @s {S}_p_{r}' for r in self.roles] + \
                          ['tellraw @s {"text":"Talking NPCs: you will hear every introduction again.","color":"yellow"}']
        return F

    def summon(self, n, rel, rotation, extra_tags=()):
        """summon line for a talker at a marker-relative position (n['vtype']: villager type, default plains)."""
        m = self.m
        lab = f'{n["name"]} · {self.roles[n["role"]]["label"]}'
        name = '{text:%s,color:"%s"}' % (jtext(lab), self.roles[n['role']]['colour'])
        return (f'summon minecraft:villager {rel} {{VillagerData:{{profession:"minecraft:{n["prof"]}",level:5,'
                f'type:"minecraft:{n.get("vtype", "plains")}"}},CustomName:{name},CustomNameVisible:1b,PersistenceRequired:1b,'
                f'Invulnerable:1b,NoAI:1b,Silent:1b,Offers:{{Recipes:[]}},Tags:["{m}_npc","{m}_talker","{m}_t{n["id"]}","{m}_r_{n["role"]}"{"".join(',"' + t + '"' for t in extra_tags)}],'
                f'Rotation:[{rotation}f,0f]}}')

    # ---- resource packs
    def java_sounds_json(self):
        return {k: {'sounds': [{'name': k.replace('.', '/', 1).replace('.', '/'), 'stream': True}]} for k in self.clips()}

    def bedrock_sound_definitions(self):
        return {'format_version': '1.14.0', 'sound_definitions': {
            k: {'category': 'neutral', 'min_distance': 2.0, 'max_distance': 16.0,
                'sounds': [{'name': 'sounds/' + k.replace('.', '/', 1).replace('.', '/'), 'stream': True,
                            'load_on_low_memory': True, 'volume': 1.0}]} for k in self.clips()}}


def write_functions(F, fn_dir):
    for name, ls in F.items():
        p = os.path.join(fn_dir, name + '.mcfunction')
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, 'w', newline='\n', encoding='utf-8').write('\n'.join(ls) + '\n')
