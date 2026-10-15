# LifeOS

Life admin on your phone, built for people living in Ireland: type, say or scan anything ("IRP card expires 2027-01-20", "NCT due 10 feb", "rent every month", "kal dentist 4pm") and LifeOS sorts it, dates it and reminds you in time.

**Open:** https://novashiv11.github.io/lifeos/ in Chrome on Android, then tap **📲 Install app** (or ⋮ → Install app). On iPhone: Safari → Share → Add to Home Screen.

- **Morning brief** and notifications for due dates and renewal windows (IRP opens 12 weeks before expiry, NCT, passport…)
- **Guides** with official links for IRP, NCT, motor tax, NDLS, passport, PPSN, Revenue, RTB and insurance
- **🎤 Voice** and **📷 camera**: scan food barcodes (Open Food Facts) and log portions; scan QR codes
- **Jarvis**: chat with Claude using your own API key; it answers from your list and saves things for you
- Works offline. Your data stays on your phone ([privacy](https://novashiv11.github.io/lifeos/privacy.html)); back it up from **All → Back up now**.

This repo holds the built app only; it is generated from the private source repo with `scripts/build_pwa.py`.
