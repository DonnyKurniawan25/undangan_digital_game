// Regression checks for the landing navigation; no npm dependencies.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

function element() {
  const listeners = {};
  const classes = new Set();
  return {
    attrs: {}, style: {}, listeners,
    classList: { contains: c => classes.has(c), add: c => classes.add(c), remove: c => classes.delete(c) },
    addEventListener: (name, fn) => { (listeners[name] ||= []).push(fn); },
    dispatch(name, event = {}) { (listeners[name] || []).forEach(fn => fn(event)); },
    setAttribute(name, value) { this.attrs[name] = value; },
    getAttribute(name) { return this.attrs[name]; },
    contains(target) { return target === this; },
    focus() { this.focused = true; },
  };
}
const toggle = element();
const nav = element();
const link = element();
const doc = element();
const win = element();
nav.querySelectorAll = () => [link];
doc.getElementById = id => ({ 'nav-toggle': toggle, 'nav-links': nav }[id] || null);
doc.querySelectorAll = () => [];
doc.body = { style: {} };
win.innerWidth = 390;
vm.runInNewContext(fs.readFileSync(path.join(__dirname, '../static/js/landing.js'), 'utf8'), {
  document: doc, window: win,
});
doc.dispatch('DOMContentLoaded');

toggle.dispatch('click');
assert.equal(nav.classList.contains('open'), true);
assert.equal(toggle.getAttribute('aria-expanded'), 'true', 'Open menu must expose expanded=true');
assert.equal(doc.body.style.overflow, 'hidden');
toggle.dispatch('click');
assert.equal(toggle.getAttribute('aria-expanded'), 'false');
assert.equal(doc.body.style.overflow, '');

toggle.dispatch('click');
link.dispatch('click');
assert.equal(nav.classList.contains('open'), false);
assert.equal(toggle.getAttribute('aria-expanded'), 'false');

toggle.dispatch('click');
doc.dispatch('keydown', { key: 'Escape' });
assert.equal(nav.classList.contains('open'), false, 'Escape must close the menu');
assert.equal(toggle.focused, true, 'Escape restores toggle focus');

toggle.dispatch('click');
doc.dispatch('click', { target: element() });
assert.equal(nav.classList.contains('open'), false);
assert.equal(toggle.getAttribute('aria-expanded'), 'false');

toggle.dispatch('click');
win.innerWidth = 1280;
win.dispatch('resize');
assert.equal(doc.body.style.overflow, '', 'Desktop resize must release mobile scroll lock');
assert.equal(nav.classList.contains('open'), false);
console.log('PASS: menu toggle, aria, link close, Escape focus, outside close, desktop resize');
