# LifeOS

Pocket companion for **Jarvis** (a Claude Project): reminders on time, 2-second capture, private money view, and a bridge to and from Jarvis.

- **Live app:** https://novashiv11.github.io/lifeos/ (installable PWA)
- **Branches:** `dev` = source (default for work) · `main` = built site, written only by CI · `feat/*` = one change each
- **Flow:** `feat/x` → PR into `dev` → CI tests → merge → CI builds and publishes to `main` → Pages
- **Run tests:** `pip install playwright && python -m playwright install chromium && python -m unittest -q`
- **Build locally:** `python scripts/build_pwa.py` → `dist/`

Plain JS + Python stdlib. Everything stays on the phone; see `pwa/privacy.html`.
