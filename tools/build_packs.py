"""Build the shared voice packs from everything under audio/ (all models together, one pack per edition).

  audio/<ns>/<path>/<name>.ogg  ->  sound event  minecraft:<ns>.<path>.<name>   (Java, assets/minecraft/sounds.json)
                                ->  sound        <ns>.<path>.<name>             (Bedrock, sounds/sound_definitions.json)

Geyser strips the 'minecraft:' namespace from a sound it has no mapping for and sends the rest to Bedrock, so the
two names match. Output: packs/voices_java.zip and packs/voices_bedrock.mcpack, plus packs/SHA1.txt.

  python3 tools/build_packs.py
"""
import hashlib
import json
import os
import uuid
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
AUDIO = os.path.join(ROOT, 'audio')
JAVA_ASSETS = os.path.join(ROOT, 'java_assets')     # extra Java assets (item models + textures): java_assets/<ns>/...
PACKS = os.path.join(ROOT, 'packs')
RESOURCE_FORMAT = (88, 107)          # Java 26.2 resource pack format 88 (and later until it changes)
VERSION = [1, 1, 0]                  # bump for every Bedrock release, so clients download it again
NS = uuid.uuid5(uuid.NAMESPACE_URL, 'senkolab-minecraft/talking-npc-voices')


def clips():
    out = []
    for rt, _, fs in os.walk(AUDIO):
        for f in sorted(fs):
            if f.endswith('.ogg'):
                rel = os.path.relpath(os.path.join(rt, f), AUDIO)[:-4].replace(os.sep, '/')
                out.append(rel)
    return sorted(out)


def zwrite(z, name, data):
    zi = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))     # fixed dates: same input, same zip, same SHA-1
    zi.compress_type = zipfile.ZIP_DEFLATED
    z.writestr(zi, data)


def main():
    os.makedirs(PACKS, exist_ok=True)
    cs = clips()
    java = {c.replace('/', '.'): {'sounds': [{'name': c, 'stream': True}]} for c in cs}
    bedrock = {'format_version': '1.14.0', 'sound_definitions': {
        c.replace('/', '.'): {'category': 'neutral', 'min_distance': 2.0, 'max_distance': 16.0,
                              'sounds': [{'name': 'sounds/' + c, 'stream': True, 'load_on_low_memory': True, 'volume': 1.0}]}
        for c in cs}}
    jp = os.path.join(PACKS, 'voices_java.zip')
    with zipfile.ZipFile(jp, 'w') as z:
        zwrite(z, 'pack.mcmeta', json.dumps({'pack': {'description': 'Talking NPC voices + garden plant models (senkolab-com/minecraft-voices)',
                                                      'min_format': RESOURCE_FORMAT[0], 'max_format': RESOURCE_FORMAT[1]}}, indent=2))
        zwrite(z, 'assets/minecraft/sounds.json', json.dumps(java, indent=1))
        for c in cs:
            zwrite(z, f'assets/minecraft/sounds/{c}.ogg', open(os.path.join(AUDIO, c + '.ogg'), 'rb').read())
        if os.path.isdir(JAVA_ASSETS):
            for rt, _, fs in sorted(os.walk(JAVA_ASSETS)):
                for f in sorted(fs):
                    full = os.path.join(rt, f)
                    zwrite(z, 'assets/' + os.path.relpath(full, JAVA_ASSETS).replace(os.sep, '/'), open(full, 'rb').read())
    bp = os.path.join(PACKS, 'voices_bedrock.mcpack')
    man = {'format_version': 2,
           'header': {'name': 'Talking NPC voices', 'description': 'senkolab-com/minecraft-voices',
                      'uuid': str(uuid.uuid5(NS, 'header')), 'version': VERSION, 'min_engine_version': [1, 21, 0]},
           'modules': [{'type': 'resources', 'uuid': str(uuid.uuid5(NS, 'resources')), 'version': VERSION}]}
    with zipfile.ZipFile(bp, 'w') as z:
        zwrite(z, 'manifest.json', json.dumps(man, indent=1))
        zwrite(z, 'sounds/sound_definitions.json', json.dumps(bedrock, indent=1))
        for c in cs:
            zwrite(z, f'sounds/{c}.ogg', open(os.path.join(AUDIO, c + '.ogg'), 'rb').read())
    sha = hashlib.sha1(open(jp, 'rb').read()).hexdigest()
    open(os.path.join(PACKS, 'SHA1.txt'), 'w').write(f'voices_java.zip {sha}\n')
    print(len(cs), 'clips; java sha1', sha, os.path.getsize(jp), 'bytes; bedrock', os.path.getsize(bp), 'bytes')


if __name__ == '__main__':
    main()
