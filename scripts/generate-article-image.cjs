#!/usr/bin/env node
/**
 * RakyatHub Article Image Generator
 * Usage: node scripts/generate-article-image.js <slug> <strategy> [url|agency|prompt]
 *
 * Strategies:
 *   screenshot <url>    - Take screenshot of URL
 *   banner <agency>     - Generate banner with agency logo + title
 *   ai_gen <prompt>     - Print prompt (agent handles generation)
 */

const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

const PROJECT = 'C:\\Users\\irfan\\rakyathub';
const IMG_DIR = path.join(PROJECT, 'src', 'assets', 'images');

const [, , slug, strategy, ...args] = process.argv;

if (!slug || !strategy) {
  console.error('Usage: node scripts/generate-article-image.js <slug> <strategy> [args...]');
  console.error('  screenshot <url>');
  console.error('  banner <agency_name>');
  console.error('  ai_gen <prompt>');
  process.exit(1);
}

const outputPath = path.join(IMG_DIR, `hero-${slug}.jpg`);

async function takeScreenshot(url) {
  console.log(`Taking screenshot of: ${url}`);
  const browser = await puppeteer.launch({
    headless: true,
    defaultViewport: { width: 1280, height: 720 }
  });
  const page = await browser.newPage();
  await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/125.0.0.0 Safari/537.36');
  await page.goto(url, { waitUntil: 'networkidle2', timeout: 30000 });
  await new Promise(r => setTimeout(r, 2000));
  await page.screenshot({ path: outputPath, fullPage: false, type: 'jpeg', quality: 85 });
  await browser.close();
  console.log(`Screenshot saved: ${outputPath}`);
  return true;
}

async function generateBanner(agency) {
  console.log(`Generating banner for agency: ${agency}`);

  // Agency logo mapping - official colour schemes
  const agencies = {
    'LHDN': { color: '#0033A0', label: 'LHDN' },
    'KWSP': { color: '#E02020', label: 'KWSP' },
    'MOF': { color: '#1A237E', label: 'MOF' },
    'BNM': { color: '#004B87', label: 'BNM' },
    'JPJ': { color: '#003D7A', label: 'JPJ' },
    'JKM': { color: '#E67E22', label: 'JKM' },
    'KPDN': { color: '#2E7D32', label: 'KPDN' },
    'KESUMA': { color: '#6A1B9A', label: 'KESUMA' },
    'ICU': { color: '#1B5E20', label: 'ICU JPM' },
    'STR': { color: '#0D47A1', label: 'STR' },
    'SARA': { color: '#B71C1C', label: 'SARA' },
    'PTPTN': { color: '#1565C0', label: 'PTPTN' },
    default: { color: '#37474F', label: agency },
  };

  const ag = agencies[agency.toUpperCase()] || agencies.default;
  const html = `<!DOCTYPE html>
<html><head><style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  width: 1200px; height: 630px;
  background: linear-gradient(135deg, ${ag.color} 0%, ${ag.color}dd 100%);
  font-family: 'Segoe UI', Arial, sans-serif;
  display: flex; flex-direction: column; justify-content: center; align-items: center;
  text-align: center; padding: 60px;
  position: relative;
}
.badge {
  position: absolute; top: 40px; left: 50%; transform: translateX(-50%);
  background: rgba(255,255,255,0.2); color: white;
  padding: 8px 24px; border-radius: 20px;
  font-size: 18px; letter-spacing: 2px;
}
h1 {
  color: white; font-size: 48px; font-weight: 700;
  line-height: 1.3; margin-bottom: 20px;
  text-shadow: 0 2px 10px rgba(0,0,0,0.2);
}
.tagline {
  color: rgba(255,255,255,0.85);
  font-size: 20px;
}
.jalur {
  position: absolute; bottom: 0; left: 0; right: 0; height: 8px;
  background: repeating-linear-gradient(
    90deg, #fff 0px, #fff 25px,
      #cc0000 25px, #cc0000 50px,
      #fff 50px, #fff 75px,
      #0033a0 75px, #0033a0 100px
  );
}
</style></head><body>
<div class="badge">${ag.label}</div>
<h1>Panduan & Perkhidmatan<br>${agency.toUpperCase()}</h1>
<p class="tagline">rakyathub.my</p>
<div class="jalur"></div>
</body></html>`;

  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();
  await page.setContent(html, { waitUntil: 'networkidle0' });
  await page.screenshot({ path: outputPath, type: 'jpeg', quality: 90, clip: { x: 0, y: 0, width: 1200, height: 630 } });
  await browser.close();
  console.log(`Banner saved: ${outputPath}`);
  return true;
}

async function main() {
  fs.mkdirSync(IMG_DIR, { recursive: true });

  switch (strategy) {
    case 'screenshot':
      const url = args[0];
      if (!url) { console.error('Error: URL required for screenshot strategy'); process.exit(1); }
      await takeScreenshot(url);
      break;

    case 'banner':
      const agency = args[0] || 'Kerajaan';
      await generateBanner(agency);
      break;

    case 'ai_gen':
      const prompt = args.join(' ') || `Professional banner for Malaysian ${slug.replace(/-/g, ' ')}`;
      console.log('AI_GEN_NEEDED');
      console.log(JSON.stringify({
        strategy: 'ai_gen',
        slug: slug,
        image_prompt: prompt,
        note: 'Use image_generate tool to create this image'
      }));
      console.log('AI_GEN_END');
      break;

    default:
      console.error(`Unknown strategy: ${strategy}`);
      process.exit(1);
  }

  // Verify output
  const stats = fs.statSync(outputPath);
  console.log(`File: ${outputPath} (${(stats.size / 1024).toFixed(1)} KB)`);
  console.log('DONE');
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
