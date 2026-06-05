# Audit Log

## 2026-06-05 12:39
- **QA Check**: Build and lint verification passed — 67 pages built successfully
- **Command**: `npm run build`, `npm run check`
- **Result**: Build: 0 errors. ESLint: 127 pre-existing issues, 6 fixed (see below)
- **Status**: resolved

### Fixes Applied
- **Fix**: Removed unused `Icon` import
- **File**: `src/components/blog/ListItem.astro:3`
- **Status**: resolved

- **Fix**: Removed unused `getFormattedDate` import
- **File**: `src/components/blog/ListItem.astro:12`
- **Status**: resolved

- **Fix**: Removed unused `Icon` import
- **File**: `src/components/blog/SinglePost.astro:2`
- **Status**: resolved

- **Fix**: Removed unused `getFormattedDate` import
- **File**: `src/components/blog/SinglePost.astro:11`
- **Status**: resolved

- **Fix**: Removed unused `theme` prop destructuring
- **File**: `src/components/widgets/Footer.astro:26`
- **Status**: resolved

- **Fix**: Removed unused `_index` parameter from map callback
- **File**: `src/components/widgets/AppDashboard.astro:163`
- **Status**: resolved

- **Fix**: Removed unused `Brands` import
- **File**: `src/pages/index.astro:8`
- **Status**: resolved

- **Fix**: Removed unused `label` variable
- **File**: `src/pages/kalkulator/zakat.astro:247`
- **Status**: resolved

- **Fix**: Removed unnecessary escape `\/` in regex character class
- **File**: `src/utils/crosslinks.ts:80`
- **Status**: resolved

## 2026-06-05 09:26
- **QA Check**: Build verification passed — 67 pages built successfully
- **Command**: `npm run build`
- **Result**: 0 errors, 0 warnings (exit code 0)
- **Status**: resolved

## 2026-06-05 07:50
- **Fix**: Replaced `netlify` attribute with `data-netlify="true"` to fix TypeScript error (netlify not a valid HTML form attribute)
- **File**: `src/pages/hubungi.astro:37`
- **Before**: `<form netlify name="contact" ...>`
- **After**: `<form data-netlify="true" name="contact" ...>`
- **Status**: resolved

- **Fix**: Added `as const` to variant property to fix TypeScript type mismatch (string vs literal union)
- **File**: `src/navigation.ts:56`
- **Before**: `variant: 'primary'`
- **After**: `variant: 'primary' as const`
- **Status**: resolved

## 2026-06-05 09:02
- **QA Check**: Build verification passed — 47 pages built successfully
- **Command**: `npm run build`
- **Result**: 0 errors, 0 warnings (astro check passed; 127 pre-existing ESLint style suggestions ignored — no impact on build or runtime)
- **Status**: resolved
