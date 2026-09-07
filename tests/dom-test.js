const assert = require('node:assert/strict');
const fs = require('node:fs');
const { JSDOM } = require('jsdom');

const html = fs.readFileSync('site/index.html', 'utf8');
const app = fs.readFileSync('site/app.js', 'utf8');
const dom = new JSDOM(html, { runScripts: 'outside-only', url: 'http://127.0.0.1:8877/' });
const { window } = dom;
const dialog = window.document.querySelector('#player');
dialog.showModal = () => dialog.setAttribute('open', '');
dialog.close = () => dialog.removeAttribute('open');
window.HTMLMediaElement.prototype.play = () => Promise.resolve();
window.HTMLMediaElement.prototype.pause = () => {};
window.eval(app);

assert.equal(window.document.querySelectorAll('.character-card').length, 9);
window.document.querySelector('[aria-label="播放「姐」字筆順"]').click();
assert.equal(dialog.hasAttribute('open'), true);
assert.equal(window.document.querySelector('#current-char').textContent, '姐');
assert.equal(window.document.querySelector('#video').getAttribute('src'), 'videos/姐.mp4');
assert.equal(window.document.querySelector('#dialog-download').getAttribute('download'), '姐字彩色筆順動畫.mp4');
window.document.querySelector('#close').click();
assert.equal(dialog.hasAttribute('open'), false);
console.log('DOM interaction test passed: 9 cards, player open/close, video and download target');
