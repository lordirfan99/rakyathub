# Hermes Task — Fix Netlify Build-Minutes Quota Exhaustion (RakyatHub)

## The problem

The Netlify **free tier gives 300 build minutes/month**. RakyatHub is blowing past it and builds are now blocked.

## Root-cause diagnosis (already done — don't re-investigate, act on it)

- **~417 git commits in the last 30 days.** Of those, only ~132 carry `[skip netlify]`; the other **~285 commits each trigger a full Netlify cloud build**.
- Each cloud build compiles **1,804 pages** (Astro) + runs Python data-fetch scripts → **~2 minutes each**. 285 × 2 = **~570 min/month vs the 300-min cap.**
- **You already have the correct low-cost path:** `scripts/full-deploy.py` builds the site **locally**, tags its commit `[skip netlify]` (line 66), and uploads the pre-built `dist/` **directly via the Netlify deploy API** (`zip_deploy()`). Direct/manual deploys **consume ZERO build minutes.**
- The quota is burned by commits that **bypass** `full-deploy.py` and hit git directly — manual fixes AND some auto-posts (e.g. "Scam of the Week", "batch deploy") that were pushed with a plain `git commit`/`git push` and **no `[skip netlify]` tag**, so Netlify rebuilds each one in the cloud.
- **Secondary waste:** the cloud build command is duplicated. `netlify.toml` runs `fetch-income-data.py && fetch-gov-data.py && deploy-api.py && npm run build`, but `npm run build` (package.json) ALSO runs `update-harga-makanan.py && fetch-election-data.py && fetch-income-data.py && fetch-gov-data.py && astro build`. So **fetch-income and fetch-gov run twice** on every cloud build.

---

## Fixes — do these in order

### FIX 1 (biggest win) — Stop git pushes from triggering cloud builds; deploy only via local build + direct upload

The site already deploys fine through `full-deploy.py` (local build → direct `dist/` upload = 0 build minutes). Make that the **only** way the live site updates, so no git commit ever spends a build minute.

**Two ways to enforce it — pick ONE:**

**1a. Netlify dashboard (preferred, cleanest):**
- Netlify → Site configuration → Build & deploy → Continuous deployment → **"Stop builds"** (locks the site so pushes don't build), OR set **Branch deploys / Production branch build** to off.
- You have Netlify API access already (`scripts/netlify_env_check.py`, `netlify_env_set.py`). You can also do this via API: `PATCH /api/v1/sites/{site_id}` with `{ "build_settings": { "stop_builds": true } }` (verify field name against current Netlify API docs).

**1b. In-repo `netlify.toml` ignore rule (works without dashboard):**
Add a build-ignore command that skips every git-triggered build:
```toml
[build]
  publish = "dist"
  command = "npm run build"
  ignore = "exit 0"   # exit 0 = "nothing changed, skip build" → skips ALL git-triggered cloud builds
```
With `ignore = "exit 0"`, Netlify skips every auto-build. The site is then updated **only** by `full-deploy.py`'s direct upload. (If you ever DO want a one-off cloud build, temporarily change `ignore` to `exit 1` or use "Trigger deploy" in the dashboard.)

**CRITICAL caveat — functions.** `full-deploy.py`'s `zip_deploy()` zips **only `dist/`**, NOT `netlify/functions/`. The site depends on 3 functions: `harga-makanan.mjs`, `harga-minyak.mjs`, `kewangan.mjs`. If you fully disable cloud builds, a direct `dist/`-only deploy may drop the functions. **Before shipping Fix 1, do ONE of:**
- (a) Extend `zip_deploy()` to also include the functions — add `netlify/functions/**` into the zip under the path Netlify expects (`.netlify/functions-internal/` for pre-bundled, or include a `netlify/functions/` folder and let Netlify bundle; verify with the [Netlify deploy-a-zip docs](https://docs.netlify.com/api/get-started/#deploy-with-the-api)). Simplest reliable route: use the **Netlify CLI** in `full-deploy.py` instead of the raw zip API — `netlify deploy --prod --dir=dist --functions=netlify/functions` — which handles functions correctly and still doesn't spend build minutes (it's a direct deploy).
- (b) Keep cloud builds ENABLED but allow at most **one per day** (see Fix 2 below) — this is the safer option if porting the function upload is risky.

**Recommendation:** use the Netlify CLI direct-deploy (`netlify deploy --prod --dir=dist --functions=netlify/functions --message "..."`) inside `full-deploy.py`, then apply Fix 1b (`ignore = "exit 0"`). That gives correct function deploys + zero build minutes.

### FIX 2 — Make EVERY commit path tag `[skip netlify]`, and rebuild at most once/day

Even if you keep cloud builds on as a fallback, cut them to ~1/day.
- **Audit every script/automation that commits.** Find any `git commit` that does NOT append `[skip netlify]`:
  - `scripts/full-deploy.py` line 66 already appends it — good.
  - The content generators behind "Scam of the Week", "News React", "batch deploy", "update harga makanan" — some appended `[skip netlify]`, some did NOT. Make them ALL append ` [skip netlify]` to the commit message (Netlify skips builds when the message contains `[skip netlify]` or `[skip ci]`).
- **Then trigger one deploy/day** via a Netlify **Build Hook** (Site config → Build & deploy → Build hooks → create → gives a URL). Call it once daily from your existing scheduler/cron (`curl -X POST <build-hook-url>`), OR just rely on `full-deploy.py`'s nightly direct deploy (already runs, per "nightly deploy … [skip netlify]" commits). One build/day = ~60 min/month, well under quota.

### FIX 3 — De-duplicate the cloud build command (saves minutes on any build that does run)

`netlify.toml` currently runs the Python fetchers AND `npm run build` (which runs them again). Change the command so each fetcher runs once:
```toml
[build]
  command = "python3 scripts/deploy-api.py && npm run build"
```
(`npm run build` already runs `update-harga-makanan.py`, `fetch-election-data.py`, `fetch-income-data.py`, `fetch-gov-data.py`, then `astro build`. Only `deploy-api.py` is unique to the netlify.toml command — keep just that one, drop the duplicated `fetch-income-data.py` and `fetch-gov-data.py`.) Verify `deploy-api.py` isn't already invoked elsewhere in the npm chain before keeping it.

### FIX 4 (optional / alternative host) — Migrate to Cloudflare Pages

If you'd rather not manage direct deploys, Cloudflare Pages free tier = **500 builds/month + unlimited bandwidth/requests** (more generous than Netlify's 300 min). But you MUST port the 3 Netlify Functions:
- `netlify/functions/harga-makanan.mjs`, `harga-minyak.mjs`, `kewangan.mjs` → Cloudflare **Pages Functions** (`/functions/*.js`) or Workers. Rewrite handler signature from Netlify (`export default async (req, context)` / `exports.handler`) to Pages Functions (`export async function onRequest(context)`).
- Update every client `fetch('/.netlify/functions/<name>')` in the source to the new path (`/api/<name>` or wherever you route the Pages Function). Search: `grep -rn "/.netlify/functions/" src/`.
- Set the build command (`npm run build`), output dir (`dist`), and the same env vars (`scripts/netlify_env_check.py` lists them) in the Cloudflare Pages dashboard.
- Update `public/_redirects` (the DocuKilat proxy `200!` rewrite + others) — Cloudflare Pages supports `_redirects` but syntax/edge-cases differ; verify each rule.
- Keep the build-frequency discipline (Fix 2) regardless — 417 commits > 500 builds is still close.

Only pursue Fix 4 if you want off Netlify; Fixes 1–3 solve the quota on Netlify without migrating.

---

## Immediate relief (while implementing)

- Netlify build minutes **reset on your billing-cycle date** each month — check Netlify → Billing for the reset date. Until then, deploy via `full-deploy.py` (direct upload, no build minutes) so the site can still update.
- Do NOT push more no-op/"trigger redeploy" commits — each one that lacks `[skip netlify]` costs ~2 build minutes.

## Acceptance criteria
1. A normal `git push` to `main` **does not** start a Netlify cloud build (verify in Netlify → Deploys: pushes show "skipped"/no build).
2. The live site still updates — via `full-deploy.py` direct deploy (or the once-daily build hook).
3. The 3 Netlify Functions still respond (test the live-price fetches on `/harga-minyak/`, `/harga-makanan-hari-ini/`, and the gold price on `/kalkulator/emas/`).
4. If any cloud build runs, its command no longer double-runs the Python fetchers.
5. Netlify → Billing shows build-minute usage flat-lining after the change.

## Files & facts
- `netlify.toml` — build command + (add) `ignore` rule.
- `package.json` `"build"` script — the canonical build chain (don't duplicate it in netlify.toml).
- `scripts/full-deploy.py` — `git_commit_push()` (line 55, appends `[skip netlify]`), `npm_build()` (line 71), `zip_deploy()` (line 78, dist-only — needs functions handling for Fix 1).
- `netlify/functions/` — `harga-makanan.mjs`, `harga-minyak.mjs`, `kewangan.mjs` (must stay deployed).
- Netlify API token / env: `scripts/netlify_env_check.py`, `netlify_env_set.py`.
- Client function calls: `grep -rn "/.netlify/functions/" src/`.

## Owner
irfanthefast@gmail.com · https://rakyathub.my · repo `lordirfan99/rakyathub` (branch `main`)
