# Aurea: new design + English/Spanish

## Context
Aurea (Django 4.2 restaurant site, repo Esteban-Jr/Aurea, live at aurea.206.189.176.206.sslip.io, cloned to `~/Aurea`) is one of the example sites linked from the portfolio. The user wants:
- **Style:** a fresh "elegant fine dining" look that keeps the black and gold.
- **Language:** the site in English and Spanish. English is the default, with an EN | ES switch.
- **Menu text:** dish names stay in Italian; descriptions are translated.
- **Bugs:** plan ahead for the bugs and errors this could cause.

## Status (22/10/26)
- [x] 0. Plan saved in the project
- [x] 1. Bilingual: 194 texts translated (`locale/es/LC_MESSAGES/django.po`), EN | ES switch in the navbar
- [x] 2. New design: every page restyled; menu, FAQ and gallery content now lives in `pages/content.py`
- [x] 3. Local preview works (see "How to preview" below)
- [x] Bugs 1–14 handled (9 was real: Spanish navbar overflowed at 1024px → menu now collapses below 1200px)
- [x] 27 tests pass (19 old + 8 new)
- [x] Extras asked for along the way: slimmer footer, scroll-down arrow on the home page, dish pop-up card on the menu (longer description, V/VG/GF tags, allergens)
- [ ] Push to GitHub and `deploy aurea` on the server
- [ ] Pick items from "Things you could add"

### How to preview on the Mac
```
cd ~/Aurea
DATABASE_URL=sqlite:///$PWD/db.sqlite3 SECRET_KEY=dev DEBUG=1 .venv/bin/python manage.py runserver
```
Open http://127.0.0.1:8000. Demo login: `demo` / `demo12345` (local database only).

### Changing a translation
Edit `locale/es/LC_MESSAGES/django.po`, then `python manage.py compilemessages`
(needs `brew install gettext`) and commit both the `.po` and `.mo` files.

## Approach

### 0. Save this plan in the project
Copy this plan to `~/Aurea/PLAN.md` so it's visible in VS Code (the folder is already open there). It's committed together with the work, and I tick items off as they're done.

### 1. Bilingual (Django's built-in translation, no new packages)
- **`aurea_project/settings.py`**
  - Add `LocaleMiddleware` after `SessionMiddleware` and before `CommonMiddleware`.
  - Add `LANGUAGES = [("en", "English"), ("es", "Español")]`, keep `LANGUAGE_CODE = "en"`, and add `LOCALE_PATHS = [BASE_DIR / "locale"]`.
  - Add the `django.template.context_processors.i18n` context processor.
- **`aurea_project/urls.py`:** add `path("i18n/", include("django.conf.urls.i18n"))`, Django's `set_language` view.
  - The language is kept in a cookie, so URLs don't change: no `/es/` prefixes, the existing links and tests keep working, and it's English first unless a visitor picks ES.
- **`templates/base.html`**
  - `<html lang="{{ LANGUAGE_CODE }}">`.
  - The EN | ES switch is a small POST form with `{% csrf_token %}` and `next={{ request.get_full_path }}`.
- **All templates** (pages, accounts, registration, reviews, `bookings/templates/bookings/*`):
  - Add `{% load i18n %}`.
  - Wrap short text in `{% translate %}`.
  - Wrap paragraphs (About, FAQ, menu descriptions) in `{% blocktranslate trimmed %}`.
  - Dish names stay untranslated.
- **Python messages:** wrap in `gettext` / `gettext_lazy`.
  - `bookings/forms.py` (4 ValidationErrors and the placeholders), `bookings/views.py`, `reviews/views.py`.
  - `accounts/forms.py` help_text and `bookings/models.py` help_text.
- **Translation files**
  - Run `brew install gettext` (Mac only), then `makemessages -l es`.
  - I write the Spanish into `locale/es/LC_MESSAGES/django.po`, then run `compilemessages`.
  - **Commit the `.mo` file too**, because the server has no gettext and `deploy` doesn't compile.

### 2. New design (elegant fine dining)
- **`static/css/style.css`:** rewrite around colour variables: ink #111, gold #c9a24a, cream #faf7f2, muted grey.
  - Headings in **Cormorant Garamond**, body text in **Inter** (Google Fonts).
  - Inline `<style>` blocks and `style=""` attributes move into this file.
- **Navbar:** slim black bar with the logo; links get a gold underline on hover and on the active page; "Book a table" becomes a gold outline button; the EN | ES switch sits at the right; it collapses properly on mobile.
- **Home:**
  - A full-width photo hero with a dark overlay, an "Aurea" serif headline, a tagline, and "Book a table" / "See the menu" buttons.
  - Then a short intro, three signature dishes using the existing Cloudinary photos, and a call-to-action band.
  - The floating social icons move into the footer.
- **Menu:** the carousel is replaced with an elegant list.
  - Category tabs or anchors: Entrées, Mains, Desserts, Extras, Drinks.
  - Each dish shows its name, a thin gold rule, the description and a small round photo.
- **Other pages:** About, Gallery, FAQ, Reviews, Booking, Login, Sign up and Profile all get the same page header (serif title and subtitle).
  - Forms and cards sit in a cream card with gold focus rings.
  - Gallery becomes an even grid.
- **Footer:** a real footer with address, opening hours, social icons and © Aurea, plus a subtle outlined "AUREA" wordmark.
  - It replaces the page-by-page `footer_text` block. The block stays so that nothing breaks.

### 3. Local preview so you can see it before it goes live
Two small changes in `settings.py`, with no effect on the server (its `.env` has neither):
- `DEBUG = os.environ.get("DEBUG") == "1"`.
- When DEBUG is on, use Django's normal static storage instead of Cloudinary.

Run locally with SQLite: `DATABASE_URL=sqlite:///db.sqlite3 SECRET_KEY=dev DEBUG=1 python manage.py runserver`.

## Bugs planned for ahead (and how each is handled)

**Bugs the site already has (fix them while we're in there)**
1. **Bootstrap JS loaded twice** in `base.html` (in head and at the bottom). This can make the mobile menu open and instantly close. Keep one copy, at the bottom.
2. **"Book Now" active link never lights up:** it checks `create_booking`, but the URL name is `create_bookings`.
3. **Footer HTML is wrong:** `home.html` puts a `<div><h1>` inside the base `<h1>`. The new footer removes this.
4. **Social icons are absolutely positioned** and overlap the photos on phones. They move to the footer.

**Bugs the translation could cause**

5. **Date input breaks in Spanish.** Spanish formats dates as 22/10/2026, but `<input type="date">` only accepts 2026-10-22, so the "Edit booking" date would show blank. Fix: `DateInput(format="%Y-%m-%d")`.
6. **Missing `.mo` file on the server** would quietly show English everywhere. It is committed, and I check it is not in `.gitignore`.
7. **Translating model `help_text`** makes Django want a new migration. Create and commit it (harmless, no database change). `deploy` runs migrate.
8. **Language switch errors.**
   - `set_language` needs POST plus a CSRF token, or it gives a 403.
   - `next` must be the current page, or the visitor lands on Home.
   - Both are tested.
9. **Text that is too long:** Spanish is about 20% longer, so the navbar could wrap at laptop width. Check widths of 1024px, 768px and 375px in both languages.
10. **`blocktranslate` text with `%`, quotes or variables.** Use `trimmed`, and run `makemessages` to catch syntax errors before compiling.
11. **Messages translated too early:** ValidationErrors and messages use `gettext` at request time, not at import, or they stay in English.

**Bugs the design could cause**

12. **Cloudinary static files.**
    - `collectstatic` uploads the new CSS on deploy, with hashed names, so no stale cache.
    - If it fails, `deploy` stops before restarting, so the old site stays up.
13. **Template errors that only show in production:** DEBUG is off, so they appear as a plain 500 page. Click through every page locally first. Every page must return 200, logged-in and logged-out, in EN and ES.
14. **The `psycopg2` package doesn't install on the Mac** (it needs PostgreSQL). For local preview, install the requirements without it; nothing changes in `requirements.txt`.

## Things you could add (not in this job unless you pick them)
Things most restaurant sites have that Aurea is missing, most useful first:

1. **Email doesn't actually send.** `EMAIL_BACKEND` is the console backend, so emails only go into the server log.
   - That means no booking confirmations, and "forgot password" can't work.
   - Fix: hook up Brevo, which SportsMode already uses. Then add booking confirmation emails and password reset.
2. **Opening hours, address and a map.** The site never says where or when the restaurant is open.
   - Add these to the footer, plus a Contact/Find us page with an embedded map.
   - Add click-to-call and WhatsApp buttons.
3. **Prices and allergens on the menu.**
   - Dishes have no prices.
   - Add dietary tags (V, VG, GF). Allergen info is expected for UK restaurants.
4. **Booking limits and a staff view.**
   - Right now any number of people can book the same time slot.
   - Add a maximum number of guests per slot and a simple staff page listing today's bookings.
5. **International phone numbers.** Only UK numbers work.
   - Spanish-speaking visitors with +34 or +57 numbers can't book.
   - Add a country code picker.
6. **Privacy and cookie policy page.** The site collects names, emails and phone numbers, so UK/EU rules (GDPR) expect one.
7. **Link previews and search.**
   - There's no favicon, meta description or share image (Open Graph). WhatsApp and Instagram links show a blank card.
   - Add a `sitemap.xml`.
8. **Custom 404 and 500 pages** in the new style, instead of the plain Django ones.
9. **Reviews on the home page:** the average star rating and the 3 latest reviews.
10. **Extras:** specials or events, gift vouchers, a newsletter sign-up, and privacy-friendly visitor stats.

## Files
- **Settings and URLs:** `aurea_project/settings.py`, `aurea_project/urls.py`.
- **Templates and CSS:** `templates/**` (16 files), `bookings/templates/bookings/*` (4), `static/css/style.css`.
- **Python:** `bookings/forms.py`, `bookings/views.py`, `bookings/models.py` (plus 1 new migration), `reviews/views.py`, `accounts/forms.py`.
- **New:** `locale/es/LC_MESSAGES/django.po` and `.mo`, plus tests for Spanish and the switch in `pages/tests.py`.

## Verification
1. **Tests:** run the existing 19 tests, plus new ones.
   - Home in Spanish when the `django_language=es` cookie is set.
   - The switch redirects back to the same page.
   - The booking form error is in Spanish.
2. **Local server:** click through every page in EN and ES, logged out and logged in.
   - Make, edit and cancel a booking, including in Spanish (date bug #5).
   - Leave a review.
   - Check phone width.
3. **`python manage.py check` and `makemigrations --check`:** must be clean.
4. **Ship:** commit on a branch, then merge to main and push to GitHub (I'll ask first).
   - You run `deploy aurea` on the server, since it needs sudo for the restart.
   - Open the live site in both languages.
   - If anything is wrong: `git revert` and deploy again.
5. **Afterwards:** offer a diary entry, and a new screenshot for the portfolio card (`portfolio-site/img/work-aurea.jpg`).
