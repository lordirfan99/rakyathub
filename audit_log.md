# Audit Log

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
