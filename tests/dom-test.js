/**
 * DOM test for the K3 stroke-player UI.
 *
 * The site under test is generated into a throwaway temp directory by a tiny
 * Python stub that imports ui.py with characters that carry ONLY a "char" key,
 * so the UI layer is proven independent of the renderer's metadata and nothing
 * is written into site/.
 */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { execFileSync } = require('node:child_process');
const { JSDOM } = require('jsdom');

const ROOT = path.resolve(__dirname, '..');
const ORDER = '我有爸媽姐妹弟哥和祖父母老師消防員警察醫生';
const ORIGINAL = '我有爸媽姐妹弟哥和';
const WORDS = ['爸爸', '媽媽', '祖父', '祖母', '老師', '消防員', '警察', '醫生'];

function buildFixture() {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'k3-ui-'));
  const stub = path.join(dir, 'stub.py');
  fs.writeFileSync(stub, [
    'import sys, pathlib',
    `sys.path.insert(0, ${JSON.stringify(ROOT)})`,
    'import ui',
    `out = pathlib.Path(${JSON.stringify(dir)})`,
    `characters = [{"char": c} for c in ${JSON.stringify(ORDER)}]`,
    'ui.write_ui(out, characters)',
  ].join('\n'));
  process.on('exit', () => fs.rmSync(dir, { recursive: true, force: true }));
  execFileSync('python3', [stub], { stdio: 'inherit' });
  return dir;
}

function load(dir) {
  const html = fs.readFileSync(path.join(dir, 'index.html'), 'utf8');
  const app = fs.readFileSync(path.join(dir, 'app.js'), 'utf8');
  const dom = new JSDOM(html, { runScripts: 'outside-only', url: 'http://127.0.0.1:8877/' });
  const { window } = dom;
  const doc = window.document;
  const dialog = doc.querySelector('#player');
  const calls = { play: 0, pause: 0, rejectNext: false };

  // jsdom 30 implements neither <dialog> modality nor media playback; stub both
  // so the test exercises our code, and emulate the browser's Escape behaviour
  // (fire "cancel", then close, which fires "close").
  dialog.showModal = () => { dialog.setAttribute('open', ''); };
  dialog.close = () => {
    if (!dialog.hasAttribute('open')) return;
    dialog.removeAttribute('open');
    dialog.dispatchEvent(new window.Event('close'));
  };
  Object.defineProperty(dialog, 'open', { get: () => dialog.hasAttribute('open') });
  window.HTMLMediaElement.prototype.play = function () {
    calls.play += 1;
    if (calls.rejectNext) { calls.rejectNext = false; return Promise.reject(new Error('NotAllowedError')); }
    return Promise.resolve();
  };
  window.HTMLMediaElement.prototype.pause = function () { calls.pause += 1; };
  window.eval(app);

  const pressEscape = () => {
    if (!dialog.hasAttribute('open')) return;
    const cancel = new window.Event('cancel', { cancelable: true });
    dialog.dispatchEvent(cancel);
    if (!cancel.defaultPrevented) dialog.close();
  };
  return { window, doc, dialog, calls, pressEscape };
}

const dir = buildFixture();
const { doc, dialog, calls, pressEscape } = load(dir);
const video = doc.querySelector('#video');
const download = doc.querySelector('#dialog-download');
const text = (selector) => doc.querySelector(selector).textContent;

// ---- structure: 21 character cards, canonical order, correct targets ----
const cards = [...doc.querySelectorAll('.character-card')];
assert.equal(cards.length, 21);
assert.equal(cards.map((card) => card.querySelector('.character-button').dataset.char).join(''), ORDER);
for (const card of cards) {
  const button = card.querySelector('.character-button');
  const char = button.dataset.char;
  const link = card.querySelector('a.download');
  assert.equal(button.dataset.video, `videos/${char}.mp4`);
  assert.equal(button.getAttribute('aria-label'), `播放「${char}」字筆順`);
  assert.equal(button.querySelector('.character').textContent, char);
  assert.equal(link.getAttribute('href'), `videos/${char}.mp4`);
  assert.equal(link.getAttribute('download'), `${char}字彩色筆順動畫.mp4`);
}

// ---- the original nine stay one tap away in their own quick row ----
const quick = [...doc.querySelectorAll('.quick-button')];
assert.equal(quick.map((button) => button.dataset.char).join(''), ORIGINAL);
for (const button of quick) {
  assert.equal(button.dataset.video, `videos/${button.dataset.char}.mp4`);
  assert.equal(button.getAttribute('aria-label'), `快速播放「${button.dataset.char}」字筆順`);
}

// ---- eight word cards, each with per-character buttons (duplicates included) ----
const wordCards = [...doc.querySelectorAll('.word-card')];
assert.deepEqual(wordCards.map((card) => card.dataset.word), WORDS);
let wordButtons = 0;
for (const card of wordCards) {
  const word = card.dataset.word;
  assert.equal(card.querySelector('.word').textContent, word);
  const buttons = [...card.querySelectorAll('.word-button')];
  assert.equal(buttons.length, word.length, `${word} needs one button per character`);
  buttons.forEach((button, index) => {
    const char = word[index];
    assert.equal(button.dataset.char, char);
    assert.equal(button.dataset.word, word);
    assert.equal(button.dataset.video, `videos/${char}.mp4`);
    assert.equal(button.textContent, char);
    assert.equal(button.getAttribute('aria-label'), `播放「${word}」第${'一二三'[index]}個字「${char}」筆順`);
    assert.ok(ORDER.includes(char), `${char} must be one of the 21 rendered characters`);
  });
  wordButtons += buttons.length;
}
assert.equal(wordButtons, 17); // 爸爸媽媽祖父祖母老師警察醫生 = 2 each, 消防員 = 3

// ---- modal: open from a character card ----
doc.querySelector('[aria-label="播放「姐」字筆順"]').click();
assert.equal(dialog.hasAttribute('open'), true);
assert.equal(text('#current-char'), '姐');
assert.equal(text('#current-word'), '');
assert.equal(video.getAttribute('src'), 'videos/姐.mp4');
assert.equal(download.getAttribute('href'), 'videos/姐.mp4');
assert.equal(download.getAttribute('download'), '姐字彩色筆順動畫.mp4');
assert.equal(calls.play, 1);

// ---- switching character pauses and rewinds the previous clip ----
video.currentTime = 4.2;
doc.querySelector('[aria-label="播放「消防員」第二個字「防」筆順"]').click();
assert.equal(calls.pause, 2); // one pause per open, so the previous clip never keeps playing
assert.equal(video.currentTime, 0);
assert.equal(text('#current-char'), '防');
assert.equal(text('#current-word'), '消防員');
assert.equal(video.getAttribute('src'), 'videos/防.mp4');
assert.equal(download.getAttribute('download'), '防字彩色筆順動畫.mp4');
assert.equal(calls.play, 2);

// ---- replay restarts the same clip ----
video.currentTime = 2.5;
doc.querySelector('#replay').click();
assert.equal(video.currentTime, 0);
assert.equal(calls.play, 3);
assert.equal(video.getAttribute('src'), 'videos/防.mp4');

// ---- close button stops playback ----
doc.querySelector('#close').click();
assert.equal(dialog.hasAttribute('open'), false);
assert.equal(calls.pause, 3);

// ---- Escape (dialog "cancel") also stops playback ----
doc.querySelector('.quick-button[data-char="我"]').click();
assert.equal(dialog.hasAttribute('open'), true);
assert.equal(video.getAttribute('src'), 'videos/我.mp4');
video.currentTime = 1.4;
pressEscape();
assert.equal(dialog.hasAttribute('open'), false);
assert.equal(video.currentTime, 0);
assert.equal(calls.pause, 5); // pause on open (4) and again on close (5)

// ---- a rejected play() promise must not surface as an unhandled rejection ----
process.on('unhandledRejection', (error) => {
  console.error('unhandled rejection from play():', error);
  process.exit(1);
});
calls.rejectNext = true;
doc.querySelector('[aria-label="播放「醫生」第一個字「醫」筆順"]').click();
assert.equal(dialog.hasAttribute('open'), true);
doc.querySelector('#close').click();

setTimeout(() => {
  console.log('DOM test passed: 21 cards, 9 quick buttons, 8 word cards (17 character buttons), modal open/switch/replay/close/cancel, safe play() rejection');
}, 20);
