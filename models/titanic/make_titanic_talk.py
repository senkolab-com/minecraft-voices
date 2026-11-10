"""Build the Titanic talking-NPC patch: datapack functions (data/titanic/function/talk/...), the new npcs.mcfunction
for every facing, tag files, and the Java + Bedrock resource packs from the processed clips.

  python3 make_titanic_talk.py <installed_titanic_pack_dir> <clips_dir_with_ogg_and_durations.json> <out_dir>
"""
import json, math, os, sys, shutil, zipfile, uuid
import talklib
import titanic_talk as T

PROF = {'steward': 'butcher', 'stewardess': 'librarian', 'stoker': 'armorer', 'seaman': 'fisherman'}
VEC = {'south': (0, 0, 1), 'west': (-1, 0, 0), 'north': (0, 0, -1), 'east': (1, 0, 0)}
RIGHT = {'south': 'west', 'west': 'north', 'north': 'east', 'east': 'south'}


def to_face(p, face):                      # south-frame marker-relative (x, y, z) -> the same spot for a facing
    x, y, z = p
    f, r = z, -x
    F, R = VEC[face], VEC[RIGHT[face]]
    return tuple(f * F[n] + r * R[n] + (y if n == 1 else 0) for n in range(3))


def rel(p):
    return ' '.join('~' if v == 0 else f'~{v}' for v in p)


def yaw(dx, dz):
    return round(math.degrees(math.atan2(-dx, dz)), 1)


def main(pack, clips_dir, out):
    spots = {s[0]: s for s in json.load(open('titanic_spots.json'))}
    npcs = []
    for (nid, role, name, deck, xr, y, face, intro) in T.NPCS:
        if nid not in spots:
            continue
        npcs.append({'id': nid, 'role': role, 'name': name, 'intro': intro, 'prof': PROF[role], 'pos': tuple(spots[nid][3])})
    durs = json.load(open(os.path.join(clips_dir, 'durations.json'))) if os.path.exists(os.path.join(clips_dir, 'durations.json')) else {}
    tk = talklib.Talk(T.MODEL, T.ROLES, T.LINES, T.LAUGHS, npcs, durs, active=getattr(T, 'ACTIVE', None))
    fn = os.path.join(out, 'datapack', 'data', 'titanic', 'function')
    talklib.write_functions(tk.functions(), fn)
    # npcs.mcfunction per facing: drop the generic crew that the speakers replace, add the speakers
    for face in VEC:
        src = os.path.join(pack, 'data', 'titanic', 'function', 'internal', face, 'npcs.mcfunction')
        keep = []
        for l in open(src, encoding='utf-8').read().splitlines():
            if any(f'CustomName:"{g}"' in l for g in T.REPLACE_GENERIC):
                continue
            keep.append(l)
        for n in npcs:
            grp = [o for o in npcs if o is not n and math.dist(o['pos'], n['pos']) <= 8]
            p = to_face(n['pos'], face)
            if grp:
                cx = sum(to_face(o['pos'], face)[0] for o in grp) / len(grp)
                cz = sum(to_face(o['pos'], face)[2] for o in grp) / len(grp)
                rot = yaw(cx - p[0], cz - p[2])
            else:
                fwd = to_face((0, 0, 1), face)
                rot = yaw(-fwd[0], -fwd[2])                 # alone: face aft, towards a player coming from the stern
            keep.append(tk.summon(n, rel(p), rot))
        d = os.path.join(fn, 'internal', face)
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, 'npcs.mcfunction'), 'w', newline='\n', encoding='utf-8').write('\n'.join(keep) + '\n')
    tags = os.path.join(out, 'datapack', 'data', 'minecraft', 'tags', 'function')
    os.makedirs(tags, exist_ok=True)
    for t, f in (('load', 'titanic:talk/init'), ('tick', 'titanic:talk/tick')):
        p0 = os.path.join(pack, 'data', 'minecraft', 'tags', 'function', t + '.json')
        d = json.load(open(p0)) if os.path.exists(p0) else {'values': []}
        if f not in d['values']:
            d['values'].append(f)
        json.dump(d, open(os.path.join(tags, t + '.json'), 'w'))
    # ---- resource packs (only when the clips exist)
    clips = tk.clips()
    have = [k for k in clips if os.path.exists(os.path.join(clips_dir, k + '.ogg'))]
    print('npcs', len(npcs), 'clips', len(clips), 'ogg present', len(have))
    json.dump({k: {'role': v[0], 'text': v[1]} for k, v in clips.items()}, open(os.path.join(out, 'clips.json'), 'w'), indent=1, ensure_ascii=False)
    if len(have) != len(clips):
        return tk
    jr = os.path.join(out, 'java_rp')
    shutil.rmtree(jr, ignore_errors=True)
    os.makedirs(os.path.join(jr, 'assets', 'minecraft', 'sounds', 'titanic', 'voice'), exist_ok=True)
    for k in clips:
        dst = os.path.join(jr, 'assets', 'minecraft', 'sounds', k.replace('.', '/') + '.ogg')
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(os.path.join(clips_dir, k + '.ogg'), dst)
    json.dump(tk.java_sounds_json(), open(os.path.join(jr, 'assets', 'minecraft', 'sounds.json'), 'w'), indent=1)
    json.dump({'pack': {'description': 'Talking NPC voices (Titanic)', 'min_format': 88, 'max_format': 107}},
              open(os.path.join(jr, 'pack.mcmeta'), 'w'), indent=2)
    br = os.path.join(out, 'bedrock_rp')
    shutil.rmtree(br, ignore_errors=True)
    for k in clips:
        dst = os.path.join(br, 'sounds', k.replace('.', '/') + '.ogg')
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(os.path.join(clips_dir, k + '.ogg'), dst)
    json.dump(tk.bedrock_sound_definitions(), open(os.path.join(br, 'sounds', 'sound_definitions.json'), 'w'), indent=1)
    ns = uuid.uuid5(uuid.NAMESPACE_URL, 'senkolab-minecraft/talking-npc-voices')
    man = {'format_version': 2, 'header': {'name': 'Talking NPC voices', 'description': 'Titanic voices',
                                           'uuid': str(uuid.uuid5(ns, 'header')), 'version': [1, 0, 0], 'min_engine_version': [1, 21, 0]},
           'modules': [{'type': 'resources', 'uuid': str(uuid.uuid5(ns, 'resources')), 'version': [1, 0, 0]}]}
    json.dump(man, open(os.path.join(br, 'manifest.json'), 'w'), indent=1)
    for src, name in ((jr, 'voices_java.zip'), (br, 'voices_bedrock.mcpack')):
        with zipfile.ZipFile(os.path.join(out, name), 'w', zipfile.ZIP_DEFLATED) as z:
            for rt, _, fs in os.walk(src):
                for f in fs:
                    z.write(os.path.join(rt, f), os.path.relpath(os.path.join(rt, f), src))
    return tk


if __name__ == '__main__':
    main(*sys.argv[1:4])
