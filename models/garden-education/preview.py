"""Render the plant models in their beds with three.js (self-contained HTML) for checking and for the preview page."""
import base64, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import layout
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'res', 'assets', 'garden-education')
KINDS = ['carrot', 'cucumber', 'tomato', 'onion', 'rice', 'blueberry', 'strawberry']


def data(three_src):
    models, tex = {}, {}
    for f in os.listdir(os.path.join(ROOT, 'models', 'plant')):
        models[f[:-5]] = json.load(open(os.path.join(ROOT, 'models', 'plant', f)))
    for f in os.listdir(os.path.join(ROOT, 'textures', 'plant')):
        tex['garden-education:plant/' + f[:-4]] = 'data:image/png;base64,' + base64.b64encode(open(os.path.join(ROOT, 'textures', 'plant', f), 'rb').read()).decode()
    beds = {k: layout.bed_plants(k) for k in KINDS}
    return models, tex, beds


JS = r"""
const {models, tex, beds, kinds, view} = DATA;
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x9fd3f0);
const W = innerWidth, H = innerHeight;
const renderer = new THREE.WebGLRenderer({antialias: true, preserveDrawingBuffer: true});
renderer.setPixelRatio(devicePixelRatio); renderer.setSize(W, H); document.body.appendChild(renderer.domElement);
const cam = new THREE.PerspectiveCamera(40, W / H, 0.1, 500);
scene.add(new THREE.HemisphereLight(0xffffff, 0x667755, 0.75));
const sun = new THREE.DirectionalLight(0xffffff, 0.75); sun.position.set(30, 50, 20); scene.add(sun);
const loader = new THREE.TextureLoader(); const mats = {};
function mat(key, col) {
  if (col) { if (!mats[col]) mats[col] = new THREE.MeshLambertMaterial({color: col}); return mats[col]; }
  if (!mats[key]) { const t = loader.load(tex[key]); t.magFilter = THREE.NearestFilter; t.minFilter = THREE.NearestFilter;
    mats[key] = new THREE.MeshLambertMaterial({map: t, transparent: false}); }
  return mats[key];
}
const order = ['east', 'west', 'up', 'down', 'south', 'north'];
function element(e, textures) {
  const f = e.from, t = e.to;
  const sx = Math.max(t[0] - f[0], 0.01), sy = Math.max(t[1] - f[1], 0.01), sz = Math.max(t[2] - f[2], 0.01);
  const g = new THREE.BoxGeometry(sx / 16, sy / 16, sz / 16);
  const uv = g.attributes.uv; const ms = [];
  order.forEach((side, i) => {
    const fc = e.faces[side]; let u = fc ? fc.uv : [0, 0, 16, 16];
    const [u1, v1, u2, v2] = u.map(v => v / 16);
    uv.setXY(i * 4 + 0, u1, 1 - v1); uv.setXY(i * 4 + 1, u2, 1 - v1); uv.setXY(i * 4 + 2, u1, 1 - v2); uv.setXY(i * 4 + 3, u2, 1 - v2);
    let k = fc ? fc.texture.slice(1) : 'particle'; ms.push(mat(textures[k]));
  });
  const mesh = new THREE.Mesh(g, ms);
  mesh.position.set((f[0] + t[0]) / 32 - 0.5, (f[1] + t[1]) / 32, (f[2] + t[2]) / 32 - 0.5);
  if (!e.rotation) return mesh;
  const o = e.rotation.origin, piv = new THREE.Group();
  piv.position.set(o[0] / 16 - 0.5, o[1] / 16, o[2] / 16 - 0.5);
  mesh.position.sub(piv.position); piv.add(mesh);
  const a = e.rotation.angle * Math.PI / 180;
  if (e.rotation.axis === 'x') piv.rotation.x = a; else if (e.rotation.axis === 'y') piv.rotation.y = a; else piv.rotation.z = a;
  return piv;
}
function model(name) {
  const m = models[name], grp = new THREE.Group();
  m.elements.forEach(e => grp.add(element(e, m.textures))); return grp;
}
function block(x, y, z, col, h = 1) {
  const b = new THREE.Mesh(new THREE.BoxGeometry(1, h, 1), mat(null, col)); b.position.set(x + 0.5, y + h / 2, z + 0.5); scene.add(b);
}
const soil = {carrot: 0x5a3a22, cucumber: 0x6b4a2e, tomato: 0x6b4a2e, onion: 0x7a5636, rice: 0x4a3a2a, blueberry: 0x3e2c1e, strawberry: 0x6b4a2e};
for (let x = -6; x < kinds.length * 11 + 2; x++) for (let z = -6; z < 7; z++) block(x, -1, z, ((x + z) & 1) ? 0x6aa84f : 0x64a04a);
kinds.forEach((k, n) => {
  const cx = n * 11 + 4;
  for (let dx = -4; dx <= 4; dx++) for (let dz = -2; dz <= 2; dz++) {
    const edge = Math.abs(dx) === 4 || Math.abs(dz) === 2;
    if (!edge && k === 'rice') { block(cx + dx, -1, dz, soil[k]); block(cx + dx, 0, dz, 0x3f76e4, 0.88); }
    else block(cx + dx, 0, dz, edge ? 0x7a5a3a : soil[k]);
    if (!edge && k === 'carrot') { const c = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.45, 0.5), mat(null, 0x4fa83a)); c.position.set(cx + dx + 0.5, 1.22, dz + 0.5); scene.add(c); }
  }
  beds[k].forEach(([dx, dz, name, yaw, s]) => {
    const g = model(name); g.scale.setScalar(s); g.rotation.y = -yaw * Math.PI / 180;
    const y = (k === 'rice') ? 0 : 1;
    g.position.set(cx + dx + 0.5, y, dz + 0.5); scene.add(g);
  });
});
function shot(cx, d, h, tx, ty) { cam.position.set(cx + d * 0.6, h, d); cam.lookAt(cx, ty, 0); renderer.render(scene, cam); }
window.views = kinds.map((k, n) => n * 11 + 4.5);
if (view === 'spin') {
  let a = 0; const cx = (kinds.length * 11) / 2;
  (function loop() { a += 0.002; cam.position.set(cx + Math.cos(a) * 46, 22, Math.sin(a) * 46); cam.lookAt(cx, 0, 0); renderer.render(scene, cam); requestAnimationFrame(loop); })();
} else {
  window.shoot = (i) => { if (i < 0) { const cx = (kinds.length * 11) / 2; cam.position.set(cx, 26, 34); cam.lookAt(cx, 0, 0); renderer.render(scene, cam); } else shot(window.views[i], 8, 4.2, 0, 1.2); };
  window.shoot(-1);
}
"""


def html(three_tag, view):
    models, tex, beds = data(None)
    d = json.dumps({'models': models, 'tex': tex, 'beds': beds, 'kinds': KINDS, 'view': view})
    return f'<!doctype html><meta charset="utf-8"><style>body{{margin:0;overflow:hidden}}</style><body>{three_tag}<script>const DATA={d};{JS}</script>'


if __name__ == '__main__':
    three = open(sys.argv[1]).read()
    out = sys.argv[2]
    open(out, 'w').write(html(f'<script>{three}</script>', 'shots'))
