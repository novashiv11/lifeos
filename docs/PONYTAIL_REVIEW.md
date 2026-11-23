# Ponytail review (2026-11-22)

Question asked of every part: now that Jarvis lives in a Claude Project, does this still need to exist in the app?
The app's job is only what a chat can't do: **remind on time, capture in 2 seconds, hand the list to Jarvis and take dated lines back**, plus private money data that already lives on the phone.

| Where | Problem | Fix (done in v5.0) |
|---|---|---|
| `lifeos.html` Jarvis API chat, voice orb, daily/weekly/memory/refresh prompts, My-life teach panel, `#ctx=` link (~370 lines) | Duplicates the Claude Project, worse | Replaced by a ~50-line bridge: Ask Jarvis ↗ (opens Claude with the list) + Paste from Jarvis (LIFEOS lines → reminders) |
| `cases.js`, `case-draft.js` | Disputes are tracked and drafted in the Project | Deleted. Old case records stay as items in the List and keep their chase dates on the home feed |
| `benefits.js`, `entitle-core.js`, `schemes.js` | Static rules go stale; the Project checks gov.ie live | Deleted |
| `letters.js`, camera/barcode code | Claude reads photos better | Deleted |
| `sync.js` (+ DRIVE_SYNC.md) | Never switched on (no client ID) | Deleted |
| Settings: voice replies, daily update, API key | Features gone | Removed from the form (old values in storage are ignored) |
| Tests for removed features | — | Deleted; bridge test added (`test_jarvis_bridge.py`); 68 pass |

Kept on purpose: `records.js` + `v4.js` (phone may not be upgraded yet; data safety), `money*.js` (his encrypted data), `today.js` feed + 🌱 growth card, List, Trash, backup/restore, reminders, share target.

Deferred:
- `lifeos/*.py` CLI is still the parser's test oracle (`test_parity.py`); upgrade when the parser changes again.
- `money-xlsx.js` / `money-esb.js` stay until he confirms he never imported.
- The app is 1,255 → ~860 lines in `lifeos.html`; total JS 4,231 → ~2,250.

## Senior review of v5.0 (agent-skills /review, 2026-11-22)
| Sev | Where | Issue | Fix (v5.1) |
|---|---|---|---|
| High | `pwa/pwa.js` plan(), `pwa/sw.js` nudgeLines | Removed "Jarvis daily update" still scheduled a notification every day | Deleted the `daily` nudge kind; test `test_no_leftover_daily_jarvis_nudge` |
| Med | `app/ui/today.js` chase card | "›" opened the deleted Cases screen (fell back to the List) | ✓ = "I chased": logs it on the case, next chase in 5 working days; test added |
| Low | `app/lifeos.html` `<style>` | ~50 rules for removed screens (orb, chat, food, wheel, stats…) | Deleted |
| Low | `app/lifeos.html` | `CHAT_OK` unused | Deleted |
| Info | Security | Ask Jarvis copies the open list into the user's own Claude app only on tap; pasted lines are scrubbed for PPS numbers; all output escaped | No change |
| Deferred | `lifeos/*.py` | CLI unused except as the parser's test oracle | Keep until the parser changes |

Verify: 70 tests pass; browser check on 5 screens at 390px: no console errors, no horizontal scroll, every button has a label.
Ship: deployed to `lifeos` main. Live URL not smoke-tested from here (github.io blocked by this environment's network) — check on the phone.
