# Hermes Task — Credit Card Art Acquisition for RakyatHub Cashback Optimizer

## Context

I run RakyatHub (https://rakyathub.my), a Malaysian personal finance website. I have built a Credit Card Cashback Combo Optimizer at https://rakyathub.my/kalkulator/cashback-combo/ that currently shows generic placeholder card designs. I want to replace these with real card artwork so users can visually recognise the cards.

I cannot scrape card images from bank websites — that is copyright infringement. I need official, licensed card artwork.

---

## Your Tasks

### Task 1 — Draft Official Email to Bank Partnership/PR Teams

Write a professional, concise email in English (and a Malay version) that I can send to the marketing or partnerships department of each Malaysian bank below. The email should:

- Introduce RakyatHub briefly (free personal finance tools for Malaysians, ~X monthly visitors)
- Explain that I am building a credit card comparison/optimizer tool
- Request permission to use their official card artwork (front-face card image) for non-commercial editorial display
- Offer to link directly to their official card application page (free traffic for them)
- Ask if they have a media/press kit or brand asset pack I can download
- Include a clear subject line
- Be under 200 words
- End with my contact: irfanthefast@gmail.com

Banks to contact (send one email per bank, personalise the card name):
1. Maybank — partnerships@maybank.com / media@maybank.com
2. CIMB — corporate.communications@cimb.com
3. Public Bank — publicbank@publicbank.com.my
4. Hong Leong Bank — hlb.comms@hlbb.hongleongbank.com
5. RHB Bank — rhb.media@rhbgroup.com
6. AmBank — ambank.communications@ambankgroup.com
7. Affin Bank — communications@affinbank.com.my
8. Alliance Bank — corporate.comms@alliancebank.com.my
9. Standard Chartered — scmy.media@sc.com
10. HSBC Malaysia — hsbc.media.malaysia@hsbc.com.my
11. Citibank Malaysia — citi.malaysia.media@citi.com
12. UOB Malaysia — uob.malaysia.pr@uobgroup.com
13. OCBC Malaysia — ocbc.malaysia.media@ocbc.com
14. AEON Credit — aeon.media@aeoncredit.com.my
15. BSN — bsn.communications@bsn.com.my

---

### Task 2 — Check for Publicly Available Press Kit / Media Asset Pages

For each bank below, search their official website for a "Media Centre", "Press Room", "Newsroom", or "Brand Assets" page that may have downloadable card images or brand kits. Return a table with:

| Bank | Press Kit / Media Page URL | Card Images Available? (Yes/No/Unknown) | Notes |
|---|---|---|---|

Banks to check:
- https://www.maybank2u.com.my
- https://www.cimb.com.my
- https://www.pbebank.com
- https://www.hlb.com.my
- https://www.rhbgroup.com
- https://www.ambankgroup.com
- https://www.affinbank.com.my
- https://www.alliancebank.com.my
- https://www.sc.com/my
- https://www.hsbc.com.my
- https://www.citibank.com.my
- https://www.uob.com.my
- https://www.ocbc.com.my
- https://www.aeoncredit.com.my
- https://www.bsn.com.my

---

### Task 3 — Alternative: Find Card Images from Licensed Aggregators

Check if the following Malaysian financial comparison sites expose card image URLs in their public HTML (not behind auth) that I could potentially license or link to. For each site, check one sample card page and note whether the card image is:
- Hosted on their own CDN (not hotlinkable)
- Loaded from the bank's own CDN (potentially stable)
- Behind authentication or JavaScript rendering only

Sites to check:
- https://ringgitplus.com/en/credit-card/
- https://www.imoney.my/credit-cards
- https://www.comparehero.my/credit-card

For each, find the `<img>` src attribute of one credit card image and report the full URL pattern.

---

### Task 4 — Interim Solution: Build Accurate CSS Card Mockups

While waiting for official art, I want visually accurate CSS card representations using each bank's official brand colours (from their public brand guidelines or website). For each bank, find:

1. The primary brand hex colour
2. The secondary/accent hex colour
3. Whether they use a gradient or solid background on their cards (based on card images visible on their website)

Return a JSON array like this:

```json
[
  {
    "bank": "Maybank",
    "primaryHex": "#E6B800",
    "secondaryHex": "#FFD700",
    "gradientStyle": "diagonal",
    "notes": "Gold gradient, tiger stripe pattern"
  }
]
```

Banks: Maybank, CIMB, Public Bank, Hong Leong Bank, RHB, AmBank, Affin, Alliance, Standard Chartered, HSBC, Citibank, UOB, OCBC, AEON Credit, BSN, Bank Islam, Bank Rakyat, Bank Muamalat, Touch n Go, Boost Credit, GX Bank.

---

## Deliverables Summary

1. Two email templates (English + Malay) ready to send
2. Table of press kit URLs per bank
3. Card image URL patterns from aggregator sites
4. JSON colour data for all 21 banks

## Priority

Do Task 4 first (immediate CSS improvement), then Task 2 (self-serve press kits), then Task 1 (outreach emails), then Task 3 (aggregator check).
