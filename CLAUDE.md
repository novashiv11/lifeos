# LifeOS / Jarvis: self-prompt (read first, every session)

**Direction (2026-11-12):** the founder's daily life-admin now happens in a Claude Project ("Jarvis") with his context; this app is parked. Don't add app features unless he asks. Help him offload: skills, checklists, scheduled checks.

**App point (if resumed):** "Jarvis sorts your Irish life admin and gets you what you're owed." Phone PWA → Play Store (€1–2/month), Ireland first. Loop: Capture → Understand → Find (owed / due / stuck) → Do (draft, book, pay) → Remind → Learn. Plan of record: `docs/MASTER_PLAN.md`.

## Talking to the founder (most important)
- Reply in **≤5 lines, Hinglish, plain words**. Details go in files, not chat.
- "Next" = build the roadmap's Now item without asking. Ask only what truly needs him, ONE question (2–3 options + a default).
- Show it on **his phone** (screenshot), not terminal output. Name blockers up front.
- He dislikes overwhelming UI: home is one feed, max 5 cards, one button per card. Delete before adding.

## Working rules (token-optimised)
1. Read only: this file → last entry of `log/DEVLOG.md` → "Now" in `docs/ROADMAP.md`. Never read `log/ARCHIVE.md` or `docs/archive/`.
2. One roadmap item per session, end to end, with tests.
3. `app/lifeos.html` is ~860 lines: grep it, don't read it whole.
4. While working run only the touched tests (`python3 -m unittest -q tests.test_x`); run the full suite once before deploy.
5. Agents only for work in separate files; ask for ≤200-word reports. Screenshots only when a screen changed.
6. Append ≤8 lines to `log/DEVLOG.md`; hard-to-reverse calls → one line in `docs/DECISIONS.md`.
7. Nothing is "done" until it ran on the founder's real data on his phone.
8. Privacy: both repos are public. No personal data in code, tests, docs or screenshots (generic fixtures only). Never store ID/PPS/account numbers.
9. In-app LLM: rules first; Haiku 5.5 only with a key; cache the system prompt; never send full history.
10. Plain JS + Python stdlib; no framework, no new dependency without a clear payoff.
11. Git: source lives in `novashiv11/lifeos` branch `dev`; `main` is the built site and only CI writes it. One change per `feat/*` branch → PR into `dev` → CI green → merge → auto-deploy. Never push to `main` by hand. (Old home `novashiv11/Project-1` branch `ccr-5d630983-6cevgh` is history only; Project-1 `main` is ToolNest, an unrelated project.)

## Map
- `app/lifeos.html` (~860 lines): shell, parser (mirror of `lifeos/parse.py`, guarded by `tests/test_parity.py`), Jarvis bridge (`askClaude` opens Claude with the list; `parseClaude`/`applyPaste` take LIFEOS lines back), reminders glue, hooks (`LIFEOS_HOOKS`, `EXTRA_VIEWS`)
- `app/ui/records.js` typed records (`lifeos.v2`, Trash, undo) · `v4.js` migration + Trash UI · `today.js` home feed (`now`) + 🌱 growth card · `money-core.js` + `money.js` (+ xlsx/esb importers)
- Classic List view (`vToday`, view `today`) lives in `lifeos.html`; older tests use it as home via `settings.home="today"`
- Removed in v5.0 (see `docs/PONYTAIL_REVIEW.md`): in-app AI chat, voice orb, Cases, Claim, letters, camera, Drive sync
- `lifeos/life.json` areas, keywords, lead times, guides (run `scripts/build_app.py` after editing) · `lifeos/*.py` CLI, frozen at v1
- `pwa/` (pwa.js nudges/install, sw.js offline + periodic sync, privacy.html) · `scripts/build_pwa.py` → `dist/`; deploy = merge into `dev`, `.github/workflows/ci.yml` builds and publishes to `main` (GitHub Pages)
- Tests: `tests/test_e2e.py` has `PhoneBase` (headless Chromium at `/opt/pw-browsers/chromium`, needs `pip install playwright`, 390×844); `test_v2_*`, `test_money_*`, `test_home_feed.py`
- Plans: `docs/MASTER_PLAN.md`, `docs/PONYTAIL_REVIEW.md`, `docs/PLAY_STORE.md`

## Kickoff line the founder can paste
> "Jarvis: continue. Next 'Now' item, ask me if blocked, ship, 5-line update."
