// Debug image resolution
import { readdirSync, existsSync } from 'fs';
import path from 'path';

const srcDir = path.resolve('./src/assets/images');
console.log('=== Image directory exists:', existsSync(srcDir));
console.log('=== Files in images dir:');
const files = readdirSync(srcDir).filter(f => /\.(jpe?g|png|webp)$/i.test(f));
files.forEach(f => console.log(' -', f));

// Check specific files
const specificFiles = [
  'hero-insuran.jpg',
  'hero-beli-beras.jpg',
  'hero-gaji-rm1800.jpg'
];
console.log('\n=== Specific file checks:');
specificFiles.forEach(f => {
  const fullPath = path.join(srcDir, f);
  console.log(` - ${f}: ${existsSync(fullPath) ? 'EXISTS' : 'MISSING'}`);
});

// Simulate key generation as the code does
const imagePath = '~/assets/images/hero-insuran.jpg';
const key1 = imagePath.replace('~/', '/src/');
const key2 = imagePath.replace('~/', './src/');
console.log('\n=== Key comparison:');
console.log('Original:', imagePath);
console.log('With /src/:', key1);
console.log('With ./src/:', key2);
