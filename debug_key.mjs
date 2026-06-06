// Debug: test Vite-style glob key resolution
const imagePath = '~/assets/images/hero-insuran.jpg';

// Test 1: The 'as-is' replacement
const key1 = imagePath.replace('~/', './src/');
console.log('Key (./src/):', JSON.stringify(key1));

// Test 2: Try without the './' 
const key2 = imagePath.replace('~/', 'src/');
console.log('Key (src/):', JSON.stringify(key2));

// Test 3: Try with just '/'
const key3 = imagePath.replace('~/', '/src/');
console.log('Key (/src/):', JSON.stringify(key3));

// The issue: Vite's import.meta.glob with alias '~' -> './src'
// produces keys like './src/assets/images/hero-insuran.jpg' (forward slashes on Unix)
// or 'src/assets/images/hero-insuran.jpg' (without ./)

// But when the file is used in Astro, which also uses Vite, what format does the key have?
// Let me check what format Astro's content layer expects
console.log('\n--- Common Vite import.meta.glob key formats ---');
console.log('Note: Vite normalizes paths to forward slashes');
