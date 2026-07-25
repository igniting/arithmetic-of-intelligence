#!/usr/bin/env node
/**
 * Pre-render every \( ... \) and \[ ... \] expression in src/*.html into static
 * KaTeX markup, writing the result to .cache/rendered/.
 *
 * The web edition loads KaTeX from a CDN and renders math in the browser. The
 * PDF renderer executes no JavaScript and has no network, so the math has to be
 * turned into plain HTML + CSS first. That is what this does.
 *
 * Run:  node build/prerender.js
 */
const katex = require('katex');
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const SRC = path.join(ROOT, 'src');
const OUT = path.join(ROOT, '.cache', 'rendered');

fs.mkdirSync(OUT, { recursive: true });

// Entities that can appear inside math must be decoded before KaTeX sees them.
function decode(s) {
  return s
    .replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"').replace(/&middot;/g, '\u00b7')
    .replace(/&mdash;/g, '\u2014').replace(/&ndash;/g, '\u2013')
    .replace(/&nbsp;/g, ' ');
}

const counts = { inline: 0, display: 0, errors: 0 };
const failures = [];

function render(tex, displayMode, file) {
  try {
    return katex.renderToString(decode(tex), {
      displayMode, throwOnError: true, strict: false, trust: false,
    });
  } catch (e) {
    counts.errors++;
    failures.push(`${file}: ${tex.slice(0, 60)} :: ${e.message.slice(0, 80)}`);
    // Fail visibly rather than silently dropping the expression.
    return `<code class="mathfail">${tex}</code>`;
  }
}

for (const file of fs.readdirSync(SRC).filter(f => f.endsWith('.html'))) {
  let html = fs.readFileSync(path.join(SRC, file), 'utf8');

  // Strip CDN assets FIRST. The auto-render config block contains literal
  // \\( and \\) delimiters that would otherwise be parsed as math.
  html = html.replace(/<link[^>]*katex[^>]*>\s*/gi, '');
  html = html.replace(/<script\b[^>]*>[\s\S]*?<\/script>\s*/gi, '');

  html = html.replace(/\\\[([\s\S]*?)\\\]/g, (_, tex) => {
    counts.display++; return render(tex, true, file);
  });
  html = html.replace(/\\\(([\s\S]*?)\\\)/g, (_, tex) => {
    counts.inline++; return render(tex, false, file);
  });

  fs.writeFileSync(path.join(OUT, file), html);
}

console.log(`prerender: ${counts.inline} inline, ${counts.display} display, ${counts.errors} errors`);
if (failures.length) {
  console.log('--- failures ---');
  failures.slice(0, 25).forEach(f => console.log('  ' + f));
  process.exitCode = 1;
}
