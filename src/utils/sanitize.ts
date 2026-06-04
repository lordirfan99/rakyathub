/**
 * Content sanitization utility for RakyatHub blog.
 * Strips raw WordPress/Markdown artifacts from excerpts and body content.
 */

/**
 * Sanitize a blog excerpt by removing:
 * - Raw URLs: (https://...) or bare https://...wp-content... URLs
 * - <figure> and <figcaption> HTML tags (complete and partial)
 * - [caption ...]...[/caption] WordPress shortcodes
 * - Escaped \[caption...\] delimiters
 * - caption id='attachment_N' attribute leaks
 * - Excess whitespace
 */
export function sanitizeExcerpt(raw: string | undefined): string | undefined {
  if (!raw) return raw;

  let text = raw;

  // 1. Remove escaped WordPress shortcodes
  text = text.replace(/\\\[caption[^\]]*\\\][\s\S]*?\\\[\/caption\\\]/gi, '');
  text = text.replace(/\\\[caption[^\]]*\\\]/gi, '');

  // 2. Remove unescaped WordPress shortcodes
  text = text.replace(/\[caption[^\]]*\][\s\S]*?\[\/caption\]/gi, '');

  // 3. Remove complete <figure>...</figure> blocks
  text = text.replace(/<figure[^>]*>[\s\S]*?<\/figure>/gi, '');

  // 4. Remove partial/opening figure/figcaption tags (without closing >)
  text = text.replace(/<figure\b[^>\n]*/gi, '');
  text = text.replace(/<figcaption\b[^>\n]*/gi, '');

  // 5. Remove orphaned closing tags
  text = text.replace(/<\/?figcaption[^>]*>/gi, '');
  text = text.replace(/<\/?figure[^>]*>/gi, '');

  // 6. Remove raw image URLs in parentheses: (https://...)
  text = text.replace(/\(https?:\/\/[^\s)]+\)/g, '');

  // 7. Remove caption attributes leaking as text
  text = text.replace(/caption\s+id\s*=\s*['"]attachment_\d+['"][^)]*/gi, '');

  // 8. Remove raw wp-content URLs not in markdown
  text = text.replace(/https?:\/\/[^\s]*wp-content[^\s]*/gi, '');

  // 9. Collapse multiple newlines and trim
  text = text.replace(/\n{3,}/g, '\n\n');
  
  // Trim leading/trailing blank lines
  const lines = text.split('\n').map(l => l.trim());
  while (lines.length && !lines[0]) lines.shift();
  while (lines.length && !lines[lines.length - 1]) lines.pop();
  text = lines.join('\n');

  return text.length > 0 ? text : undefined;
}

/**
 * Strip raw WordPress HTML/shortcode artifacts from markdown body content.
 */
export function sanitizeBody(raw: string): string {
  let text = raw;

  // Remove escaped shortcodes
  text = text.replace(/\\\[caption[^\]]*\\\][\s\S]*?\\\[\/caption\\\]/gi, '');
  
  // Remove unescaped shortcode tags but keep inner content
  text = text.replace(/\[caption[^\]]*\]/gi, '');
  text = text.replace(/\[\/caption\]/gi, '');

  // Remove figure/figcaption tags (complete and partial), keep inner content
  text = text.replace(/<figure\b[^>\n]*/gi, '');
  text = text.replace(/<figcaption\b[^>\n]*/gi, '');
  text = text.replace(/<\/?figcaption[^>]*>/gi, '');
  text = text.replace(/<\/?figure[^>]*>/gi, '');

  return text;
}
