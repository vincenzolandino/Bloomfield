# Bloomfield Creator Agency Rebuild

Date: September 20, 2026  
Status: Approved for planning

## 1. Objective

Rebuild getbloomfield.com as a single-page website for an independent creator representation office. The site supports commercial outreach from Bloomfield and routes every inquiry to `hello@getbloomfield.com`.

The finished repository begins from a clean root commit. It contains no legacy pages, assets, copy, metadata, branches, tags, or reachable history.

## 2. Positioning

Bloomfield provides independent representation for internet-native talent.

The offer covers:

- Representation and career strategy
- Brand partnerships
- Commercial development
- Negotiation and deal operations

The site speaks to creators, podcasters, founders, athletes, digital personalities, brands, and collaborators. These are focus areas, not claims about an existing roster.

## 3. Truth and Identity Rules

The site and its outreach use the following identity:

- Brand: Bloomfield
- Contact address: `hello@getbloomfield.com`
- Public sender name: Bloomfield

The site will not publish or imply:

- A fictional employee, agent, founder, or team
- A current roster that does not exist
- Brand relationships that do not exist
- Campaign results, testimonials, press, or awards that do not exist
- A public operating-company name

Authority comes from art direction, clear services, disciplined language, and a polished interaction system.

## 4. Information Architecture

The public site contains one landing page with six sections.

### 4.1 Hero

Eyebrow:

> Representation / Partnerships / Strategy

Headline:

> Independent representation for internet-native talent.

Supporting copy:

> Bloomfield handles partnerships, positioning, negotiations, and the business behind the work.

Primary action:

> Start a conversation

The action opens a new email addressed to `hello@getbloomfield.com`.

### 4.2 Point of View

Working copy:

> An audience can open a door. A career needs structure. Bloomfield manages the commercial work around the creative work, from the first conversation through signed agreement and final delivery.

This section establishes the agency's purpose without making historical claims.

### 4.3 Capabilities

Four concise capability blocks:

1. **Representation and career strategy**  
   Position the work, choose the right opportunities, and build a commercial direction that can hold beyond one platform.
2. **Brand partnerships**  
   Source, shape, negotiate, and manage partnerships that fit the creator and the audience.
3. **Commercial development**  
   Develop opportunities across sponsorships, media, products, appearances, licensing, and advisory work.
4. **Deal operations**  
   Handle communication, negotiation, contracting coordination, timelines, approvals, and delivery.

### 4.4 Focus Areas

Display the following disciplines as an editorial typographic sequence:

- Creators
- Podcasters
- Founders
- Athletes
- Digital personalities

The section label is "Focus," avoiding roster language.

### 4.5 Operating Model

Three stages:

1. **Position**  
   Define the opportunity, audience, commercial fit, and terms.
2. **Partner**  
   Bring the right people together and structure the agreement.
3. **Manage**  
   Keep communication, approvals, timelines, and delivery moving.

### 4.6 Contact

Headline:

> Make the introduction.

Supporting copy:

> Talent, brands, and collaborators can reach Bloomfield directly.

Primary action:

> hello@getbloomfield.com

The footer contains the Bloomfield wordmark, Connecticut, USA, and the copyright notice. It contains no staff list, social links, newsletter form, or competing action.

## 5. Visual System

### 5.1 Art Direction

The page combines a private management office with an editorial fashion publication. The visual system uses scale, cropping, rhythm, and motion to create authority.

Reference principles:

- Talent presented as culture, rather than inventory
- Institutional restraint in navigation and supporting copy
- Clear commercial services beneath the editorial surface

The implementation will not reproduce the composition, typography, or branded elements of any reference site.

### 5.2 Color

- Ink: `#0A0A0A`
- Warm paper: `#F1ECE2`
- Vermilion: `#FF4A2D`
- Muted paper: `#C9C2B6`

Ink and warm paper carry most of the interface. Vermilion appears on one primary action, active states, and selected motion details.

### 5.3 Typography

- Display: Bodoni Moda
- Interface and body: Familjen Grotesk

Display type uses extreme scale and tight line spacing. Interface copy stays compact and functional. Font files load from Google Fonts with local fallbacks and `font-display: swap`.

### 5.4 Imagery

Atmospheric images may show cameras, lighting, screens, crowds, production details, hands, architecture, and abstract material studies. Identifiable people will not be presented as represented talent.

Every image must be original, generated for the site, owned by Bloomfield, or distributed under a license that permits commercial use. Decorative images use empty alternative text. Informative images receive concise descriptions.

### 5.5 Motion

Motion supports one clear sequence:

- Initial wordmark and headline reveal
- Slow editorial image drift
- Horizontal discipline rail
- Capability rows that respond to focus and hover
- Contact action with a restrained directional transition

Motion uses CSS where practical and a small JavaScript layer where state is required. `prefers-reduced-motion` removes transforms, drift, and staggered entrances while preserving content.

## 6. Interaction Design

The fixed header contains the Bloomfield wordmark and one contact action. Section navigation appears only if it improves orientation at the final page length.

All interactive targets meet a minimum 44 by 44 pixel touch area. Keyboard focus remains visible against every background. Hover treatments have matching focus treatments.

The email action uses a normal `mailto:` URL. The address remains visible and selectable if the visitor has no configured email client.

The page contains no modal, carousel, cookie banner, autoplay audio, contact form, or hidden navigation drawer.

## 7. Technical Architecture

The site uses a static architecture:

- `index.html` for structure and metadata
- `assets/css/site.css` for the complete visual system
- `assets/js/site.js` for progressive motion and small interactions
- `assets/media/` for optimized images and the social preview
- `_headers` for Netlify security and cache rules
- `_redirects` for public routes and retired URL responses
- `robots.txt` and `sitemap.xml` for indexing
- `410.html` for retired URLs

No framework, package manager, build command, CMS, database, or client-side router is required.

JavaScript is progressive. The complete page and email action work when JavaScript is unavailable.

## 8. Metadata and Indexing

Page title:

> Bloomfield | Independent Creator Representation

Meta description:

> Bloomfield provides independent representation, brand partnerships, commercial strategy, and deal operations for internet-native talent.

The page includes canonical, Open Graph, and social-card metadata. Structured data uses `Organization` and `WebSite`. It lists no invented employees, clients, reviews, or social profiles.

Former public URLs return HTTP 410. Root, required assets, `robots.txt`, `sitemap.xml`, and the social preview remain available. The deployed response behavior must be tested against Netlify before publication.

Analytics and advertising scripts are excluded from the initial release.

## 9. Security and Privacy

Netlify headers will define:

- A restrictive Content Security Policy limited to the site and selected font hosts
- Strict Transport Security
- `X-Content-Type-Options: nosniff`
- A restrictive referrer policy
- Permissions Policy disabling camera, microphone, and geolocation
- Frame protection through CSP and `X-Frame-Options`

The site collects no form data, cookies, or visitor identifiers.

## 10. Repository Reset

The final migration will:

1. Create an orphan history containing the approved site and documentation.
2. Verify the complete new tree before any remote change.
3. Replace remote `main` with the new root history.
4. Remove every other remote branch and tag.
5. Confirm that a fresh clone exposes only the new history.
6. Confirm that Netlify builds the replacement commit.

The GitHub repository and Netlify project remain in place so their connection and domain configuration survive.

Git hosting providers may retain unreachable objects internally until garbage collection. The old history will have no reachable reference through the repository interface or a normal clone.

## 11. Error Handling

- Missing public paths receive the branded 410 response.
- Missing decorative media does not hide core copy or actions.
- Failed font requests fall back to high-contrast local serif and sans-serif families.
- JavaScript failure leaves the page visible, readable, and navigable.
- The email address remains plain text beside its clickable action.

## 12. Verification

Before the remote history changes:

- Validate HTML and metadata.
- Check CSS and JavaScript for syntax errors.
- Test at 360, 390, 768, 1024, 1440, and 1920 pixel widths.
- Test keyboard-only navigation and visible focus.
- Test reduced-motion behavior.
- Confirm sufficient color contrast.
- Confirm all public copy follows the approved identity rules.
- Scan the complete new tree for legacy vocabulary and assets.
- Confirm that no unsupported claims appear in visible copy or metadata.

After deployment:

- Confirm `https://getbloomfield.com/` returns the new page.
- Confirm HTTPS, headers, canonical metadata, and social preview.
- Confirm `hello@getbloomfield.com` is visible and linked correctly.
- Confirm a sample of former URLs returns HTTP 410.
- Confirm a fresh repository clone contains one clean history.
- Run performance and accessibility audits against the live domain.

## 13. Acceptance Criteria

The rebuild is complete when:

- The live domain presents Bloomfield as an independent creator representation office.
- The site contains one public landing page and one branded retired-content response.
- The design is responsive, accessible, and usable without JavaScript.
- Every inquiry route points to `hello@getbloomfield.com`.
- The public site and metadata contain no fabricated people, clients, roster, results, testimonials, or partnerships.
- The repository contains no reachable legacy history, branches, tags, copy, or assets.
- Former URLs no longer serve legacy material.
- Netlify deploys the clean-root commit successfully.
