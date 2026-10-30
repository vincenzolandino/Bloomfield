import { cp, mkdir, rm } from 'node:fs/promises';
import { dirname } from 'node:path';

// Publish only the public website. Keep working notes and tests out of deploys.
const files = [
  'index.html', '410.html', '_headers', '_redirects', 'robots.txt', 'sitemap.xml',
  'assets/css/site.css', 'assets/js/site.js',
  'assets/media/favicon.svg', 'assets/media/social-card.svg',
  'talent/index.html', 'talent/amy-landino/index.html',
  'talent/vincenzo-landino/index.html', 'talent/lali-michelsen/index.html',
];
await rm('dist', { recursive: true, force: true });
await mkdir('dist', { recursive: true });
for (const file of files) {
  await mkdir(dirname(`dist/${file}`), { recursive: true });
  await cp(file, `dist/${file}`);
}
console.log(`Built ${files.length} public files in dist/`);
