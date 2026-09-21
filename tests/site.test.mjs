import test from 'node:test';
import assert from 'node:assert/strict';
import { access, readFile } from 'node:fs/promises';

const requiredFiles = [
  'index.html',
  '410.html',
  'assets/css/site.css',
  'assets/js/site.js',
  'assets/media/social-card.svg',
  '_headers',
  '_redirects',
  'robots.txt',
  'sitemap.xml',
];

const requiredCopy = [
  'Independent representation for internet-native talent.',
  'Representation and career strategy',
  'Brand partnerships',
  'Commercial development',
  'Deal operations',
  'hello@getbloomfield.com',
];

const requiredLandmarks = [
  '<header',
  '<main',
  '<footer',
  'id="point-of-view"',
  'id="capabilities"',
  'id="focus"',
  'id="process"',
  'id="contact"',
];

const forbiddenClaims = [
  /our clients/i,
  /our roster/i,
  /our team/i,
  /trusted by/i,
  /award-winning/i,
];

const escapeRegExp = (value) => value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
const read = (path) => readFile(path, 'utf8');

test('all required files exist', async () => {
  await Promise.all(requiredFiles.map((file) => access(file)));
});

test('the landing page uses the approved identity and structure', async () => {
  const html = await read('index.html');
  assert.equal((html.match(/<h1\b/g) || []).length, 1);
  requiredCopy.forEach((copy) => assert.match(html, new RegExp(escapeRegExp(copy), 'i')));
  requiredLandmarks.forEach((landmark) => assert.match(html, new RegExp(escapeRegExp(landmark), 'i')));
  assert.match(html, /href="mailto:hello@getbloomfield\.com"/i);
});

test('the landing page contains only defensible claims', async () => {
  const html = await read('index.html');
  forbiddenClaims.forEach((claim) => assert.doesNotMatch(html, claim));
  assert.doesNotMatch(html, /<form\b/i);
  assert.doesNotMatch(html, /google-analytics|googletagmanager|facebook\.com|instagram\.com|linkedin\.com/i);
});

test('metadata identifies the canonical organization', async () => {
  const html = await read('index.html');
  assert.match(html, /<title>Bloomfield \| Independent Creator Representation<\/title>/i);
  assert.match(html, /<link rel="canonical" href="https:\/\/getbloomfield\.com\/">/i);
  assert.match(html, /property="og:title"/i);
  assert.match(html, /property="og:image" content="https:\/\/getbloomfield\.com\/assets\/media\/social-card\.svg"/i);
  assert.match(html, /"@type":\s*"Organization"/i);
  assert.match(html, /"@type":\s*"WebSite"/i);
});

test('runtime resources stay local', async () => {
  const html = await read('index.html');
  assert.match(html, /href="\/assets\/css\/site\.css"/i);
  assert.match(html, /src="\/assets\/js\/site\.js"/i);
  assert.doesNotMatch(html, /<script[^>]+src="https?:/i);
});

test('the visual system includes approved tokens and accessibility states', async () => {
  const css = await read('assets/css/site.css');
  [
    '--ink: #0A0A0A',
    '--paper: #F1ECE2',
    '--accent: #FF4A2D',
    '--muted: #C9C2B6',
    '@media (prefers-reduced-motion: reduce)',
    ':focus-visible',
    '@media (max-width: 768px)',
  ].forEach((value) => assert.ok(css.includes(value), `missing CSS contract: ${value}`));
});

test('the motion layer is progressive and dependency free', async () => {
  const js = await read('assets/js/site.js');
  assert.match(js, /IntersectionObserver/);
  assert.match(js, /prefers-reduced-motion/);
  assert.doesNotMatch(js, /fetch\(|XMLHttpRequest|import\s|https?:\/\//);
});

test('the retired page is branded and useful', async () => {
  const html = await read('410.html');
  assert.match(html, /Bloomfield/i);
  assert.match(html, /This page has been retired\./i);
  assert.match(html, /href="\/"/i);
});

test('Netlify configuration protects the site and retires old routes', async () => {
  const headers = await read('_headers');
  const redirects = await read('_redirects');
  [
    'Content-Security-Policy',
    'Strict-Transport-Security',
    'X-Content-Type-Options: nosniff',
    'X-Frame-Options: DENY',
    'Referrer-Policy',
    'Permissions-Policy',
  ].forEach((value) => assert.ok(headers.includes(value), `missing header: ${value}`));
  assert.match(redirects, /^\/\s+\/index\.html\s+200/m);
  assert.match(redirects, /^\/assets\/\*\s+\/assets\/:splat\s+200/m);
  assert.match(redirects, /^\/\*\s+\/410\.html\s+410/m);
});

test('indexing files expose only the canonical landing page', async () => {
  const robots = await read('robots.txt');
  const sitemap = await read('sitemap.xml');
  assert.match(robots, /Allow: \/$/m);
  assert.match(robots, /Sitemap: https:\/\/getbloomfield\.com\/sitemap\.xml/);
  assert.equal((sitemap.match(/<url>/g) || []).length, 1);
  assert.match(sitemap, /<loc>https:\/\/getbloomfield\.com\/<\/loc>/);
});
