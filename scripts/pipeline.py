#!/usr/bin/env python3
"""
RakyatHub Full Article Pipeline
Usage: python3 scripts/pipeline.py <slug> [--strategy screenshot|banner|ai_gen] [--url URL] [--agency AGENCY] [--prompt PROMPT]

Steps:
  1. Validate article with SEO Guardian
  2. Generate hero image based on strategy
  3. Verify image is valid JPEG
  4. Update image: field in frontmatter
  5. Git add → commit → push
  6. npm run build
  7. python3 scripts/deploy_zip.py

Environment: requires GITHUB_TOKEN in env or .git-credentials
"""

import os, sys, subprocess, json, re, shutil, argparse
from pathlib import Path

PROJECT = Path("C:/Users/irfan/rakyathub")
VALIDATOR = Path("C:/Users/irfan/AppData/Local/hermes/skills/seo/rakyathub-seo-guardian/scripts/validate-article.py")
IMG_SCRIPT = PROJECT / "scripts" / "generate-article-image.cjs"
POST_DIR = PROJECT / "src" / "data" / "post"
IMG_DIR = PROJECT / "src" / "assets" / "images"

def run(cmd, cwd=PROJECT, timeout=120):
    print(f"\n$ {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    if result.stdout:
        print(result.stdout[-2000:] if len(result.stdout) > 2000 else result.stdout)
    if result.stderr:
        print(f"STDERR: {result.stderr[-500:]}")
    return result

def step(msg):
    print(f"\n{'='*60}")
    print(f"  {msg}")
    print(f"{'='*60}")

def main():
    parser = argparse.ArgumentParser(description="RakyatHub Article Pipeline")
    parser.add_argument("slug", help="Article slug (filename without .md)")
    parser.add_argument("--strategy", default="ai_gen", choices=["screenshot", "banner", "ai_gen"])
    parser.add_argument("--url", default="", help="URL for screenshot strategy")
    parser.add_argument("--agency", default="", help="Agency name for banner strategy")
    parser.add_argument("--prompt", default="", help="Prompt for ai_gen strategy")
    parser.add_argument("--skip-build", action="store_true", help="Skip build + deploy at end")
    args = parser.parse_args()

    slug = args.slug
    md_file = POST_DIR / f"{slug}.md"

    # Step 0: Verify article exists
    if not md_file.exists():
        print(f"❌ Article not found: {md_file}")
        sys.exit(1)
    print(f"✅ Article: {md_file}")

    # Step 1: SEO Validate
    step("1/6 — SEO Validation")
    result = run(f'python3 "{VALIDATOR}" "{md_file}"')
    if "FAIL" in result.stdout and "All SEO Guardian rules" not in result.stdout:
        print("❌ SEO validation FAILED. Fix issues and re-run.")
        sys.exit(1)
    # R10 might fail if no image yet — that's OK, we're generating it

    # Step 2: Generate image
    step("2/6 — Generate Hero Image")
    img_args = [f'node', f'"{IMG_SCRIPT}"', slug, args.strategy]
    if args.strategy == "screenshot" and args.url:
        img_args.append(f'"{args.url}"')
    elif args.strategy == "banner" and args.agency:
        img_args.append(args.agency)
    elif args.strategy == "ai_gen" and args.prompt:
        img_args.append(args.prompt)

    result = run(" ".join(img_args))
    if "DONE" not in result.stdout and "AI_GEN_NEEDED" not in result.stdout:
        print("❌ Image generation failed.")
        sys.exit(1)

    if "AI_GEN_NEEDED" in result.stdout:
        print("⚠️ AI image generation required. Use image_generate tool manually.")
        print("Then re-run pipeline with --skip-build after image is saved.")
        return

    # Step 3: Verify image
    step("3/6 — Verify Image")
    expected_img = IMG_DIR / f"hero-{slug}.jpg"
    result = run(f'file "{expected_img}"')
    if "JPEG image data" not in result.stdout and "PNG image data" not in result.stdout:
        print(f"❌ Image verification failed for {expected_img}")
        sys.exit(1)
    print(f"✅ Image OK: {expected_img}")

    # Step 4: Git
    step("4/6 — Git Commit & Push")
    # Fix image: field quotes in frontmatter
    content = md_file.read_text(encoding="utf-8")
    # Ensure image: field has quotes
    content = re.sub(
        r'^image:\s*(~?/?[^\s"\']+\.(jpg|jpeg|png))$',
        r'image: "\1"',
        content,
        flags=re.MULTILINE
    )
    md_file.write_text(content, encoding="utf-8")

    run(f'git add "{md_file}" "{expected_img}"')
    run(f'git commit -m "feat: BOF - {slug} [skip netlify]"')
    
    # Push with token from git-credentials
    creds_file = Path.home() / ".git-credentials"
    if creds_file.exists():
        token = creds_file.read_text().strip()
        # Extract token from URL
        m = re.search(r'://[^:]+:([^@]+)@', token)
        if m:
            token_val = m.group(1)
            remote = f"https://lordirfan99:{token_val}@github.com/lordirfan99/rakyathub.git"
            run(f'git push "{remote}" HEAD:main')

    # Step 5: Build
    step("5/6 — Build")
    result = run("npm run build", timeout=180)
    if "Complete" not in result.stdout:
        print("❌ Build failed")
        sys.exit(1)
    print("✅ Build OK")

    # Step 6: Deploy
    if not args.skip_build:
        step("6/6 — Deploy")
        result = run("python3 scripts/deploy_zip.py", timeout=120)
        print("✅ Deploy attempted — check live URL to confirm")

    print(f"\n{'='*60}")
    print(f"  ✅ PIPELINE COMPLETE: {slug}")
    print(f"  🔗 https://rakyathub.my/{slug}/")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
