"""Whole-garden three.js preview (blocks + plant models + gardeners) - for checking and the preview page."""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import garden, preview, garden_talk as T

COL = [('grass_block', '#6aa84f'), ('dirt_path', '#a08850'), ('coarse_dirt', '#7a5a3e'), ('podzol', '#5a3e22'), ('farmland', '#4e3220'),
       ('dirt', '#6b4a2e'), ('sand', '#dccc96'), ('sandstone', '#d8c890'), ('spruce_slab', '#6e4f30'), ('spruce_planks', '#6e4f30'), ('spruce_log', '#4e3a24'),
       ('spruce_stairs', '#6e4f30'), ('dark_oak_stairs', '#3e2a18'), ('dark_oak_slab', '#3e2a18'), ('spruce_fence', '#5a4028'), ('mud', '#3a302c'),
       ('water', '#3f76e4'), ('glass_pane', '#cfe8f0'), ('glass', '#cfe8f0'), ('white_concrete', '#f0f0f0'), ('moss', '#5a8a30'),
       ('jungle_log', '#5a4424'), ('jungle_leaves', '#3a8a2a'), ('oak_log', '#6a5232'), ('oak_leaves', '#4a9a3a'),
       ('stone_bricks', '#888888'), ('cobblestone', '#7a8a6a'), ('lantern', '#f0c060'), ('chain', '#444'), ('hay', '#d8b040'),
       ('pumpkin', '#e08020'), ('barrel', '#8a6038'), ('composter', '#7a5a30'), ('crafting', '#9a6a3a'), ('chest', '#b07830'),
       ('fern', '#4a8a30'), ('carrots', '#4fa83a'), ('cocoa', '#a0602a'), ('door', '#6e4f30'), ('sign', '#b08850'),
       ('poppy', '#d02020'), ('dandelion', '#f0d020'), ('cornflower', '#4060e0'), ('daisy', '#f0f0e0'), ('allium', '#b070e0'),
       ('bluet', '#e0e8ff'), ('short_grass', '#5a9a40')]
THIN = ('poppy', 'dandelion', 'cornflower', 'daisy', 'allium', 'bluet', 'short_grass', 'fern', 'carrots', 'lantern', 'chain', 'sign', 'cocoa', 'fence', 'door', 'glass_pane')


def col(name):
    name = name.split('[')[0]
    for k, c in COL:
        if k in name:
            return c
    return '#ff00ff'


def blocks(m):
    g = m.g
    solid = g > 0
    pad = np.zeros(np.array(g.shape) + 2, bool); pad[1:-1, 1:-1, 1:-1] = solid
    exp = solid & ~(pad[2:, 1:-1, 1:-1] & pad[:-2, 1:-1, 1:-1] & pad[1:-1, 2:, 1:-1] & pad[1:-1, :-2, 1:-1] & pad[1:-1, 1:-1, 2:] & pad[1:-1, 1:-1, :-2])
    out = {}
    for x, k, z in np.argwhere(exp):
        name = m.pal[g[x, k, z]]
        y = k + garden.Y0
        if y < -2:
            continue
        kind = 'glass' if ('glass' in name and 'pane' not in name) else ('water' if 'water[' in name else ('thin' if any(t in name for t in THIN) else 'cube'))
        out.setdefault(kind, []).append([int(x), int(y), int(z), col(name)])
    return out


JS = r"""
const {models, tex, blocks, plants, npcs, labels} = SCENE;
const scene = new THREE.Scene(); scene.background = new THREE.Color(0x9fd3f0);
scene.fog = new THREE.Fog(0x9fd3f0, 120, 260);
const renderer = new THREE.WebGLRenderer({antialias: true, preserveDrawingBuffer: true});
renderer.setPixelRatio(Math.min(devicePixelRatio, 2)); renderer.setSize(innerWidth, innerHeight); document.body.appendChild(renderer.domElement);
const cam = new THREE.PerspectiveCamera(40, innerWidth / innerHeight, 0.1, 600);
scene.add(new THREE.HemisphereLight(0xffffff, 0x667755, 0.8));
const sun = new THREE.DirectionalLight(0xffffff, 0.7); sun.position.set(40, 80, 60); scene.add(sun);
const sea = new THREE.Mesh(new THREE.PlaneGeometry(600, 600), new THREE.MeshLambertMaterial({color: 0x2f6fc8}));
sea.rotation.x = -Math.PI / 2; sea.position.set(39, -0.12, 31); scene.add(sea);
function inst(list, geo, matOpts, yoff) {
  if (!list) return;
  const mesh = new THREE.InstancedMesh(geo, new THREE.MeshLambertMaterial(matOpts), list.length);
  const o = new THREE.Object3D(), c = new THREE.Color();
  list.forEach(([x, y, z, h], i) => { o.position.set(x + 0.5, y + yoff, z + 0.5); o.updateMatrix(); mesh.setMatrixAt(i, o.matrix); mesh.setColorAt(i, c.set(h)); });
  scene.add(mesh);
}
inst(blocks.cube, new THREE.BoxGeometry(1, 1, 1), {}, 0.5);
inst(blocks.thin, new THREE.BoxGeometry(0.4, 0.6, 0.4), {}, 0.3);
inst(blocks.water, new THREE.BoxGeometry(1, 0.88, 1), {transparent: true, opacity: 0.75}, 0.44);
inst(blocks.glass, new THREE.BoxGeometry(1, 1, 1), {transparent: true, opacity: 0.28, depthWrite: false}, 0.5);
plants.forEach(([x, y, z, name, yaw, s]) => { const g = model(name); g.scale.setScalar(s); g.rotation.y = -yaw * Math.PI / 180; g.position.set(x + 0.5, y, z + 0.5); scene.add(g); });
const robe = new THREE.MeshLambertMaterial({color: 0x7a5a3a}), skin = new THREE.MeshLambertMaterial({color: 0xc89a78}), hat = new THREE.MeshLambertMaterial({color: 0xd8c070});
npcs.forEach(([x, y, z, rgb]) => {
  const g = new THREE.Group();
  const b = new THREE.Mesh(new THREE.BoxGeometry(0.5, 1.2, 0.4), new THREE.MeshLambertMaterial({color: rgb})); b.position.y = 0.6; g.add(b);
  const h = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.6, 0.5), skin); h.position.y = 1.5; g.add(h);
  const t = new THREE.Mesh(new THREE.BoxGeometry(0.9, 0.08, 0.9), hat); t.position.y = 1.84; g.add(t);
  g.position.set(x + 0.5, y, z + 0.5); scene.add(g);
});
labels.forEach(([x, y, z, text]) => {
  const c = document.createElement('canvas'); c.width = 512; c.height = 96; const k = c.getContext('2d');
  k.fillStyle = 'rgba(0,0,0,0.35)'; k.fillRect(0, 0, 512, 96); k.font = 'bold 54px sans-serif'; k.fillStyle = '#f5c542'; k.textAlign = 'center'; k.fillText(text, 256, 66);
  const sp = new THREE.Sprite(new THREE.SpriteMaterial({map: new THREE.CanvasTexture(c)})); sp.scale.set(5, 0.95, 1); sp.position.set(x + 0.5, y + 2, z + 0.5); scene.add(sp);
});
let ang = 0.9, dist = 72, elev = 0.62, drag = null;
function place() { const cx = 39, cz = 31; cam.position.set(cx + Math.sin(ang) * dist * Math.cos(elev), Math.sin(elev) * dist, cz + Math.cos(ang) * dist * Math.cos(elev)); cam.lookAt(cx, 0, cz); }
renderer.domElement.addEventListener('pointerdown', e => drag = [e.clientX, e.clientY]);
addEventListener('pointerup', () => drag = null);
addEventListener('pointermove', e => { if (!drag) return; ang -= (e.clientX - drag[0]) * 0.006; elev = Math.max(0.12, Math.min(1.45, elev + (e.clientY - drag[1]) * 0.005)); drag = [e.clientX, e.clientY]; });
renderer.domElement.addEventListener('wheel', e => { e.preventDefault(); dist = Math.max(14, Math.min(160, dist * (1 + Math.sign(e.deltaY) * 0.1))); }, {passive: false});
addEventListener('resize', () => { renderer.setSize(innerWidth, innerHeight); cam.aspect = innerWidth / innerHeight; cam.updateProjectionMatrix(); });
window.setView = (a, d, e, cx, cz) => { ang = a; dist = d; elev = e; if (cx !== undefined) { place(); cam.lookAt(cx, 1, cz); } };
let auto = SCENE.auto;
renderer.domElement.addEventListener('pointerdown', () => auto = false);
(function loop() { if (auto) ang += 0.0012; place(); renderer.render(scene, cam); requestAnimationFrame(loop); })();
"""

# reuse the model builder from preview.JS (functions mat/element/model) by slicing it out
MODEL_JS = preview.JS[preview.JS.index('const loader'):preview.JS.index('function block(')]


def scene_html(three_tag, auto=True, extra_head=''):
    m = garden.build()
    models, tex, _ = preview.data(None)
    npcs = []
    colours = {'gold': '#c8962a', 'green': '#3a8a3a', 'red': '#c03030', 'yellow': '#d8c040', 'aqua': '#3aa8b8', 'blue': '#3a5ac8', 'light_purple': '#c070c0'}
    for (nid, role, name, prof, talk) in T.NPCS:
        x, y, z = m.walks[role][0]
        npcs.append([x, y, z, colours[T.ROLES[role]['colour']]])
    labels = [[x, y, z, t] for (x, y, z, t, sub, f) in m.labels]
    d = json.dumps({'models': models, 'tex': tex, 'blocks': blocks(m), 'plants': m.plants, 'npcs': npcs, 'labels': labels, 'auto': auto})
    return (f'<!doctype html><html><head><meta charset="utf-8"><title>Garden School</title>{extra_head}'
            f'<style>html,body{{margin:0;height:100%;overflow:hidden;background:#9fd3f0}}</style></head><body>{three_tag}'
            f'<script>const SCENE={d};const scene0=null;</script><script>{JS.replace("const {models, tex, blocks, plants, npcs, labels} = SCENE;", "const {models, tex, blocks, plants, npcs, labels} = SCENE;" + MODEL_JS)}</script></body></html>')


if __name__ == '__main__':
    open(sys.argv[2], 'w').write(scene_html(f'<script>{open(sys.argv[1]).read()}</script>', auto=False))
