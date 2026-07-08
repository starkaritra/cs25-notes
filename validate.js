const puppeteer = require('puppeteer');
const path = require('path');

const EDGE = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe";
const files = process.argv.slice(2);

(async () => {
  const browser = await puppeteer.launch({ executablePath: EDGE, headless: 'new',
    args: ['--no-sandbox','--disable-dev-shm-usage'] });
  let anyFail = false;
  for (const f of files) {
    const page = await browser.newPage();
    const consoleErrs = [];
    page.on('pageerror', e => consoleErrs.push('JS: ' + e.message));
    const url = 'file:///' + path.resolve(f).replace(/\\/g,'/');
    await page.goto(url, { waitUntil: 'networkidle0', timeout: 60000 });
    await new Promise(r => setTimeout(r, 3500)); // let mermaid+mathjax finish
    const res = await page.evaluate(() => {
      const mermaidSvgs = document.querySelectorAll('.mermaid svg').length;
      const mermaidBlocks = document.querySelectorAll('.mermaid').length;
      const mermaidErr = Array.from(document.querySelectorAll('.mermaid'))
        .filter(m => /Syntax error|error in text|mermaid version/i.test(m.textContent)).length;
      const mjx = document.querySelectorAll('mjx-container, .MathJax, svg[data-mml-node]').length;
      return { mermaidBlocks, mermaidSvgs, mermaidErr, mjx };
    });
    const ok = res.mermaidSvgs === res.mermaidBlocks && res.mermaidErr === 0 && consoleErrs.length === 0;
    if (!ok) anyFail = true;
    console.log(`\n[${ok ? 'PASS' : 'FAIL'}] ${path.basename(f)}`);
    console.log(`   mermaid: ${res.mermaidSvgs}/${res.mermaidBlocks} rendered, errors=${res.mermaidErr}`);
    console.log(`   mathjax containers: ${res.mjx}`);
    if (consoleErrs.length) console.log('   JS errors:\n     ' + consoleErrs.join('\n     '));
    await page.close();
  }
  await browser.close();
  process.exit(anyFail ? 1 : 0);
})();
