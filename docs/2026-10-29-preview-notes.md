# Talent website preview

This branch is a local preview for review. It has not been pushed or deployed.

The homepage introduces Bloomfield and links to a separate Talent index. Agency leadership remains unnamed. All inquiries retain the existing hello@getbloomfield.com route; each profile carries the talent's name into the email subject. Vincenzo is described as the founder of Business of Speed only.

## Portraits still needed

Supply one approved portrait for Amy, Vincenzo and Lali, ideally at least 1200 pixels on the short edge, with space for a 4:5 crop. The preview labels every portrait space. No stock or generated person has been used. Confirm framing and reuse rights before replacing the frames.

## Public work linked

- Amy's official biography: https://amylandino.com/about
- Amy's keynote archive: https://amylandino.com/standoutwithvideo/
- One Squared keynote: https://www.youtube.com/watch?v=UVP0tHbTnbA
- Good Morning, Good Life: https://www.goodmorninggoodlife.com/
- Vincenzo's podcast work: https://podcast.bizofspeed.com/people/vincenzo-landino
- Business of Speed: https://www.bizofspeed.com/
- Lali's public creative work: https://www.lalimichelsen.com/
- Lali's podcast work: https://podcast.bizofspeed.com/people/lali-michelsen
- Lali's Grosjean interview: https://www.linkedin.com/posts/vincenzolandino_lali-michelsen-introduces-romain-grosjean-activity-7398695607156056064-zrdY

These links were checked on October 29, 2026. Clips are linked on their existing public platforms. No clip files, thumbnails or third-party logos were copied. Private planning documents, fees and prospect information remain outside the repository.

## Checks

Run `node --test tests/site.test.mjs` and `node --check assets/js/site.js` from the repository root. Use an existing Netlify CLI local preview for browser checks: `netlify dev --offline --dir . --port 4173 --no-open --skip-gitignore`. Run `python3 tests/browser_check.py` against that preview. No package installation or remote deployment is required.

The owner requested the separate Talent page and unnamed agency representation after the first preview. The final layout, copy, portraits and proof selection need Dana's review before a production action.
