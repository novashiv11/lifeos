# Code map (read only when app work is asked for)

- `app/lifeos.html` (~860 lines): shell, parser (mirror of `lifeos/parse.py`, guarded by `tests/test_parity.py`), Jarvis bridge (`askClaude` opens Claude with the list; `parseClaude`/`applyPaste` take LIFEOS lines back), reminders glue, hooks (`LIFEOS_HOOKS`, `EXTRA_VIEWS`)
- `app/ui/records.js` typed records (`lifeos.v2`, Trash, undo) · `v4.js` migration + Trash UI · `today.js` home "Yaad" (`now`): Late / Is hafte / Baad mein / Bina date list + one Jarvis button · `money-core.js` + `money.js` (+ xlsx/esb importers)
- Classic List view (`vToday`, view `today`) lives in `lifeos.html`; older tests use it as home via `settings.home="today"`
- Removed in v5.0 (see `docs/PONYTAIL_REVIEW.md`): in-app AI chat, voice orb, Cases, Claim, letters, camera, Drive sync
- `lifeos/life.json` areas, keywords, lead times, guides (run `scripts/build_app.py` after editing) · `lifeos/*.py` CLI, frozen at v1
- `pwa/` (pwa.js nudges/install, sw.js offline + periodic sync, privacy.html) · `scripts/build_pwa.py` → `dist/`; deploy = merge into `dev`, `.github/workflows/ci.yml` builds and publishes to `main` (GitHub Pages)
- Tests: `tests/test_e2e.py` has `PhoneBase` (headless Chromium at `/opt/pw-browsers/chromium`, needs `pip install playwright`, 390×844); `test_v2_*`, `test_money_*`, `test_home_feed.py`
- Plans: `docs/MASTER_PLAN.md`, `docs/PONYTAIL_REVIEW.md`, `docs/PLAY_STORE.md`
