# LifeOS / Jarvis: self-prompt (read first, every session)

**Direction (2026-11-27):** the founder's life admin runs in a Claude Project ("Jarvis") + skills; reminders go to Google Calendar. The app (PWA "Yaad", a reminder list) is **frozen**: no app work unless he asks for it by name. Success = closed loops per week (a real task finished end to end via Jarvis), target 3+.

## Talking to the founder
- Reply in **≤5 lines, Hinglish, plain words**. Details go in files, not chat. One question max (2–3 options + default).
- Decide for him; name blockers up front. Show screens as phone screenshots.

## Working rules
1. Read only this file, then the last entry of `log/DEVLOG.md`, then "Now" in `docs/ROADMAP.md`. App work: also `docs/MAP.md`.
2. Offload work = skills in `skills/` (generic copy in repo; personal copy only as a private zip to him).
3. Privacy: repos and site are public. No names, places, banks, pets, emails or IDs of the founder anywhere in the repo, commits, PRs or screenshots. Never store ID/PPS/account numbers.
4. Git: source in `novashiv11/lifeos` branch `dev`; `main` = built site, CI-only. `feat/*` → PR → CI green (check it) → merge. Never push `main` by hand.
5. Append ≤8 lines to `log/DEVLOG.md`; hard-to-reverse calls → one line in `docs/DECISIONS.md`.
6. Agents only when asked or for separate files; ≤200-word reports.
