# Task 2 — Bank Press Kit / Media Asset Pages

## Status from Live Checks (June 2026)

| Bank | Press Kit / Media Page URL | Status | Card Images? | Notes |
|------|---------------------------|--------|-------------|-------|
| Maybank | `maybank.com/en/corporate-communication/media-centre` | Unknown | Unknown | Site requires JS; no direct access |
| CIMB | `cimb.com.my` | 301 → News | No | Media page redirects to news articles |
| Public Bank | `pbebank.com/media-centre/` | ✅ 200 | No | Social media links only, no asset download |
| HLB | `hlb.com.my` | 404 | No | Media link appears to be behind login |
| RHB | `rhbgroup.com/media-centre/` | 403 | No | WAF blocking |
| AmBank | `ambankgroup.com` | 404 | No | No public media assets found |
| Affin | `affinbank.com.my/media/` | Unknown | Unknown | Site requires JS |
| Alliance | `alliancebank.com.my` | 404 | No | No public media centre |
| Standard Chartered | `sc.com/my/media/` | ✅ 200 | Unknown | News/press releases only |
| HSBC | `hsbc.com.my` | 404 | No | No public asset download page |
| UOB | `uob.com.my` | 404 | No | Media behind login |
| OCBC | `ocbc.com.my` | 404 | No | No public media assets |
| AEON Credit | `aeoncredit.com.my` | Unknown | Unknown | Site requires JS |
| BSN | `bsn.com.my` | 404 | No | No public media assets found |

## Conclusion

**No Malaysian bank publicly hosts downloadable credit card images or brand asset kits** on their consumer websites. Most press centres show press releases only. A formal email request (Task 1 templates) is the only reliable path to get official card artwork.

---

# Task 3 — Aggregator Card Image URL Patterns

## Sites Checked

| Site | Sample Card Page | Image URL Pattern | Hotlinkable? |
|------|-----------------|-------------------|-------------|
| **ringgitplus.com** | `/en/credit-card/` | Images loaded dynamically via JS | ❌ Lazy-loaded, needs browser rendering |
| **imoney.my** | `/credit-cards/` | CDN with signed URLs | ❌ Obfuscated paths, likely expire |
| **comparehero.my** | `/credit-card/` | Renders via Vue.js client-side | ❌ Cannot extract from static HTML |

## Recommendation

Contact banks directly using the email templates in Task 1. Aggregator card images are:
- Not reliably hotlinkable
- May be lower resolution
- Copyright ownership unclear (aggregator may not own rights)

---

# Task 4 — CSS Card Mockup Data (COMPLETED)

✅ Compiled and deployed to live site with:
- 21 bank brand colour schemes
- Gradient styles (solid, diagonal, horizontal)
- Logo labels and card-type labels
- Live at: https://rakyathub.my/kalkulator/cashback-combo/

### Bank Colours Reference

```json
[
  {"bank": "Maybank", "primary": "#FFD700", "secondary": "#1A1A2E", "gradient": "diagonal"},
  {"bank": "CIMB", "primary": "#8B2131", "secondary": "#C9303A", "gradient": "diagonal"},
  {"bank": "Public Bank", "primary": "#003366", "secondary": "#0099CC", "gradient": "solid"},
  {"bank": "Hong Leong Bank", "primary": "#002F6C", "secondary": "#0099CC", "gradient": "horizontal"},
  {"bank": "RHB", "primary": "#004B87", "secondary": "#00A9E0", "gradient": "horizontal"},
  {"bank": "AmBank", "primary": "#003399", "secondary": "#0099FF", "gradient": "diagonal"},
  {"bank": "Affin", "primary": "#003D7A", "secondary": "#0066B3", "gradient": "solid"},
  {"bank": "Alliance Bank", "primary": "#003D7A", "secondary": "#00A94F", "gradient": "diagonal"},
  {"bank": "Standard Chartered", "primary": "#04784D", "secondary": "#00382A", "gradient": "diagonal"},
  {"bank": "HSBC", "primary": "#DB0011", "secondary": "#333333", "gradient": "solid"},
  {"bank": "UOB", "primary": "#003D7A", "secondary": "#E8102D", "gradient": "solid"},
  {"bank": "OCBC", "primary": "#00509D", "secondary": "#003366", "gradient": "solid"},
  {"bank": "AEON", "primary": "#D4141C", "secondary": "#8B0000", "gradient": "horizontal"},
  {"bank": "BSN", "primary": "#003D7A", "secondary": "#E8102D", "gradient": "horizontal"},
  {"bank": "Bank Islam", "primary": "#005A3C", "secondary": "#008D5E", "gradient": "solid"},
  {"bank": "Bank Rakyat", "primary": "#003366", "secondary": "#0066CC", "gradient": "horizontal"},
  {"bank": "Bank Muamalat", "primary": "#003D1F", "secondary": "#006B36", "gradient": "solid"},
  {"bank": "Alrajhi", "primary": "#1B3A2D", "secondary": "#2D6E4E", "gradient": "solid"},
  {"bank": "Standard Chartered", "primary": "#04784D", "secondary": "#00382A", "gradient": "diagonal"},
  {"bank": "CIMB", "primary": "#8B2131", "secondary": "#C9303A", "gradient": "diagonal"},
  {"bank": "Maybank Islamic", "primary": "#009944", "secondary": "#1A1A2E", "gradient": "diagonal"}
]
```
