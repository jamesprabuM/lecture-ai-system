const { chromium } = require('playwright');
const path = require('path');

async function wait(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 2200 } });

  const root = path.resolve(__dirname, '..');
  const outputDir = path.join(root, 'screenshots');
  const audioFile = path.join(
    root,
    'audio',
    'girl_scout_collection_1008_blb_librivox',
    '01-girl-scout-movement-in-the-public-schools_marsh_blb_64kb.mp3'
  );

  await page.goto('http://localhost:3000', { waitUntil: 'networkidle' });
  await wait(800);

  await page.screenshot({
    path: path.join(outputDir, '01-home.png'),
    fullPage: true,
  });

  const fileInput = page.locator('input[type="file"]');
  await fileInput.setInputFiles(audioFile);
  await wait(400);

  await page.screenshot({
    path: path.join(outputDir, '02-file-selected.png'),
    fullPage: true,
  });

  const processButton = page.getByRole('button', { name: /Process Lecture/i });
  await processButton.click();
  await wait(1800);

  await page.screenshot({
    path: path.join(outputDir, '03-processing.png'),
    fullPage: true,
  });

  // Wait for generated output panels to appear and capture a sample output view.
  await page.waitForSelector('text=Summary', { timeout: 180000 });
  await wait(1000);
  await page.screenshot({
    path: path.join(outputDir, '04-sample-output.png'),
    fullPage: true,
  });

  await browser.close();
  console.log('Screenshots captured in:', outputDir);
})().catch((error) => {
  console.error(error);
  process.exit(1);
});
