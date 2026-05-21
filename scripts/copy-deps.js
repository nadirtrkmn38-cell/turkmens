/**
 * Postinstall: socket.io-client UMD dağıtımını renderer'a kopyala
 * Renderer (sandboxed) node_modules'tan doğrudan require yapamaz.
 */
const fs = require('fs');
const path = require('path');

const candidates = [
  path.join(__dirname, '..', 'node_modules', 'socket.io-client', 'dist', 'socket.io.min.js'),
  path.join(__dirname, '..', 'node_modules', 'socket.io-client', 'dist', 'socket.io.js')
];

const dst = path.join(__dirname, '..', 'renderer', 'socket.io.min.js');

try {
  const src = candidates.find(p => fs.existsSync(p));
  if (!src) {
    console.warn('[copy-deps] socket.io-client bulunamadı, atlanıyor. Önce `npm install` yapın.');
    process.exit(0);
  }
  fs.mkdirSync(path.dirname(dst), { recursive: true });
  fs.copyFileSync(src, dst);
  console.log('[copy-deps] socket.io kopyalandı:', dst);
} catch (err) {
  console.warn('[copy-deps] hata:', err.message);
  process.exit(0);
}
