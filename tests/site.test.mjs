import test from 'node:test';
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { access, readFile } from 'node:fs/promises';

const origin = 'https://getbloomfield.com';
const profiles = [
  { path: '/talent/amy-landino/', name: 'Amy Landino' },
  { path: '/talent/vincenzo-landino/', name: 'Vincenzo Landino' },
  { path: '/talent/lali-michelsen/', name: 'Lali Michelsen' },
];
const pages = ['/', '/talent/', ...profiles.map(({ path }) => path), '/410.html'];
const fileFor = (path) => path.endsWith('/') ? path.slice(1) + 'index.html' : path.slice(1);
const read = (path) => readFile(path, 'utf8');
const scripts = (html) => [...html.matchAll(/<script\b([^>]*)>([\s\S]*?)<\/script>/g)];

test('published page links and local resources resolve, including fragment targets', async () => {
  for (const path of pages) {
    const html = await read(fileFor(path));
    for (const [, value] of html.matchAll(/\b(?:href|src)="([^"]+)"/g)) {
      const url = new URL(value.replaceAll('&amp;', '&'), origin + path);
      if (url.origin !== origin) continue;
      const target = fileFor(url.pathname);
      await access(target);
      if (url.hash && /\.html$/.test(target)) {
        const targetHtml = await read(target);
        assert.ok(targetHtml.includes('id="' + decodeURIComponent(url.hash.slice(1)) + '"'), 'missing fragment ' + value + ' on ' + path);
      }
    }
  }
});

test('buyers reach the separate Talent page before choosing a profile', async () => {
  const home = await read('index.html');
  assert.ok(home.includes('href="/talent/"'));
  const html = await read('talent/index.html');
  for (const { path } of profiles) {
    assert.ok(html.includes('href="' + path + '"'), 'homepage has no route to ' + path);
    const profile = await read(fileFor(path));
    assert.ok(profile.includes('href="/talent/"'), path + ' has no route back to the roster');
  }
});

test('profile inquiries retain the talent name and the existing inbox', async () => {
  for (const { path, name } of profiles) {
    const html = await read(fileFor(path));
    const inquiries = [...html.matchAll(/href="(mailto:[^"]+)"/g)]
      .map(([, value]) => new URL(value.replaceAll('&amp;', '&')));
    assert.ok(inquiries.length >= 2, 'missing inquiry actions on ' + path);
    for (const url of inquiries) {
      assert.equal(url.pathname, 'hello@getbloomfield.com');
      assert.ok(url.searchParams.get('subject')?.includes(name), path + ' loses the selected talent');
    }
  }
});

test('each talent has canonical metadata and valid structured data', async () => {
  const seen = new Set();
  for (const path of pages.filter((page) => page !== '/410.html')) {
    const html = await read(fileFor(path));
    const canonical = html.match(/<link rel="canonical" href="([^"]+)"/);
    assert.equal(canonical?.[1], origin + path);
    assert.ok(!seen.has(canonical[1]), 'two pages share one canonical URL');
    seen.add(canonical[1]);
    assert.equal((html.match(/<h1\b/g) || []).length, 1);
    const jsonScripts = scripts(html).filter(([, attrs]) => attrs.includes('application/ld+json'));
    assert.ok(jsonScripts.length > 0);
    for (const [, , json] of jsonScripts) assert.equal(JSON.parse(json)['@context'], 'https://schema.org');
  }
});

test('the security policy authorizes every inline schema script', async () => {
  const headers = await read('_headers');
  for (const path of pages) {
    const html = await read(fileFor(path));
    for (const [, attrs, body] of scripts(html)) {
      if (/\bsrc=/.test(attrs)) continue;
      const hash = createHash('sha256').update(body).digest('base64');
      assert.ok(headers.includes("'sha256-" + hash + "'"), 'CSP blocks inline metadata on ' + path);
    }
  }
  assert.ok(headers.includes("img-src 'self' data:"));
  assert.ok(headers.includes("frame-ancestors 'none'"));
});

test('talent routes are explicit before the retired-route fallback', async () => {
  const rules = (await read('_redirects')).split('\n')
    .map((line) => line.trim().split(/\s+/))
    .filter(([path]) => path && !path.startsWith('#'));
  const talentRoute = rules.find(([path]) => path === '/talent/');
  assert.deepEqual(talentRoute, ['/talent/', '/talent/index.html', '200']);
  const fallback = rules.findIndex(([path]) => path === '/*');
  assert.ok(fallback >= 0);
  for (const { path } of profiles) {
    const index = rules.findIndex(([from]) => from === path);
    assert.ok(index >= 0 && index < fallback, 'missing explicit route for ' + path);
    assert.equal(rules[index][1], path + 'index.html');
    assert.equal(rules[index][2], '200');
  }
  assert.equal(rules[fallback][2], '410');
});

test('the sitemap exposes every canonical buyer page', async () => {
  const sitemap = await read('sitemap.xml');
  const locations = [...sitemap.matchAll(/<loc>([^<]+)<\/loc>/g)].map(([, url]) => url);
  assert.deepEqual(locations.sort(), ['/', '/talent/', ...profiles.map(({ path }) => path)].map((path) => origin + path).sort());
});
