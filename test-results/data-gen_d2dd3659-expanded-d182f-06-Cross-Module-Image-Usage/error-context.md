# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: data\gen_d2dd3659\expanded_gen_0.spec.ts >> Suite: Poster Module >> TC-POS-006: Cross-Module Image Usage
- Location: data\gen_d2dd3659\expanded_gen_0.spec.ts:370:7

# Error details

```
Error: page.goto: Protocol error (Page.navigate): Cannot navigate to invalid URL
Call log:
  - navigating to "/", waiting until "load"

```

# Test source

```ts
  177 |         mimeType: 'text/plain',
  178 |         buffer: Buffer.from('This is not an image')
  179 |       };
  180 |       
  181 |       await fileInput.setInputFiles(invalidFile as any).catch(() => {});
  182 | 
  183 |       const errorMessage = page.locator('text=/invalid|error|unsupported|无效|错误/i')
  184 |         .or(page.locator('[role="alert"]'));
  185 |       
  186 |       await page.waitForTimeout(1000);
  187 |     }
  188 |   });
  189 | 
  190 |   test('TC-IDP-003: Maximum File Size Boundary', async ({ page }) => {
  191 |     const fileInput = page.locator('input[type="file"]').first();
  192 |     
  193 |     if (await fileInput.count() > 0) {
  194 |       const largeBuffer = Buffer.alloc(10 * 1024 * 1024, 'a');
  195 |       const largeFile = {
  196 |         name: 'large.jpg',
  197 |         mimeType: 'image/jpeg',
  198 |         buffer: largeBuffer
  199 |       };
  200 | 
  201 |       await fileInput.setInputFiles(largeFile as any).catch(() => {});
  202 | 
  203 |       const errorMessage = page.locator('text=/too large|size|exceeds|过大|超出/i');
  204 |       await page.waitForTimeout(1000);
  205 |     }
  206 |   });
  207 | 
  208 |   test('TC-IDP-004: Face Detection Failure Scenario', async ({ page }) => {
  209 |     const fileInput = page.locator('input[type="file"]').first();
  210 |     
  211 |     if (await fileInput.count() > 0) {
  212 |       const testImagePath = path.resolve('public/favicon.svg');
  213 |       await fileInput.setInputFiles(testImagePath);
  214 | 
  215 |       await page.waitForTimeout(3000);
  216 | 
  217 |       const noFaceMessage = page.locator('text=/no face|face not detected|无法识别人脸|未检测到人脸/i');
  218 |       const hasMessage = await noFaceMessage.count() > 0;
  219 |     }
  220 |   });
  221 | 
  222 |   test('TC-IDP-005: Multiple Faces Detected', async ({ page }) => {
  223 |     const fileInput = page.locator('input[type="file"]').first();
  224 |     
  225 |     if (await fileInput.count() > 0) {
  226 |       const testImagePath = path.resolve('public/favicon.svg');
  227 |       await fileInput.setInputFiles(testImagePath);
  228 | 
  229 |       await page.waitForTimeout(2000);
  230 | 
  231 |       const multiFacePrompt = page.locator('text=/multiple faces|select face|多张人脸|选择/i');
  232 |     }
  233 |   });
  234 | 
  235 |   test('TC-IDP-006: Cropper Boundary Interaction', async ({ page }) => {
  236 |     const fileInput = page.locator('input[type="file"]').first();
  237 |     
  238 |     if (await fileInput.count() > 0) {
  239 |       const testImagePath = path.resolve('public/favicon.svg');
  240 |       await fileInput.setInputFiles(testImagePath);
  241 | 
  242 |       const cropper = page.locator('.cropper, [data-testid="cropper"], .react-crop').first();
  243 |       if (await cropper.count() > 0) {
  244 |         const box = await cropper.boundingBox();
  245 |         if (box) {
  246 |           await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2);
  247 |           await page.mouse.down();
  248 |           await page.mouse.move(box.x - 100, box.y - 100);
  249 |           await page.mouse.up();
  250 |         }
  251 |       }
  252 |     }
  253 |   });
  254 | 
  255 |   test('TC-IDP-007: Rapid "Process" Button Clicks', async ({ page }) => {
  256 |     const fileInput = page.locator('input[type="file"]').first();
  257 |     
  258 |     if (await fileInput.count() > 0) {
  259 |       const testImagePath = path.resolve('public/favicon.svg');
  260 |       await fileInput.setInputFiles(testImagePath);
  261 | 
  262 |       const processBtn = page.getByRole('button', { name: /process|download|生成/i }).first();
  263 |       
  264 |       if (await processBtn.count() > 0) {
  265 |         for (let i = 0; i < 5; i++) {
  266 |           await processBtn.click({ timeout: 100 }).catch(() => {});
  267 |         }
  268 | 
  269 |         const isDisabled = await processBtn.isDisabled().catch(() => false);
  270 |       }
  271 |     }
  272 |   });
  273 | });
  274 | 
  275 | test.describe('Suite: Poster Module', () => {
  276 |   test.beforeEach(async ({ page }) => {
> 277 |     await page.goto('/');
      |                ^ Error: page.goto: Protocol error (Page.navigate): Cannot navigate to invalid URL
  278 |     const posterLink = page.getByRole('link', { name: /poster|海报/i }).first();
  279 |     if (await posterLink.count() > 0) {
  280 |       await posterLink.click();
  281 |       await page.waitForLoadState('domcontentloaded');
  282 |     }
  283 |   });
  284 | 
  285 |   test('TC-POS-001: Create and Save Basic Poster', async ({ page }) => {
  286 |     const template = page.locator('[data-testid="template"], .template-item, .template-card').first();
  287 |     if (await template.count() > 0) {
  288 |       await template.click();
  289 |     }
  290 | 
  291 |     const textLayer = page.locator('[data-testid="text-layer"], .text-element, [contenteditable="true"]').first();
  292 |     if (await textLayer.count() > 0) {
  293 |       await textLayer.click();
  294 |       await textLayer.fill('Test Poster Text');
  295 |     }
  296 | 
  297 |     const saveBtn = page.getByRole('button', { name: /save|export|保存|导出/i }).first();
  298 |     if (await saveBtn.count() > 0) {
  299 |       await saveBtn.click();
  300 |     }
  301 |   });
  302 | 
  303 |   test('TC-POS-002: Empty Text Field Submission', async ({ page }) => {
  304 |     const textLayer = page.locator('[contenteditable="true"], [data-testid="text-layer"]').first();
  305 |     if (await textLayer.count() > 0) {
  306 |       await textLayer.click();
  307 |       await textLayer.fill('');
  308 |       await page.keyboard.press('Escape');
  309 | 
  310 |       const undefinedText = page.locator('text=/undefined|null/i');
  311 |       expect(await undefinedText.count()).toBe(0);
  312 |     }
  313 |   });
  314 | 
  315 |   test('TC-POS-003: Maximum Character Limit Overflow', async ({ page }) => {
  316 |     const textLayer = page.locator('[contenteditable="true"], [data-testid="text-layer"]').first();
  317 |     if (await textLayer.count() > 0) {
  318 |       const longText = 'A'.repeat(5000);
  319 |       await textLayer.click();
  320 |       await textLayer.fill(longText);
  321 | 
  322 |       await page.waitForTimeout(500);
  323 | 
  324 |       const canvas = page.locator('canvas, .canvas-area, [data-testid="canvas"]').first();
  325 |       if (await canvas.count() > 0) {
  326 |         const canvasBox = await canvas.boundingBox();
  327 |         const textOverflow = await textLayer.evaluate((el) => {
  328 |           const rect = el.getBoundingClientRect();
  329 |           return rect.width > window.innerWidth;
  330 |         });
  331 |       }
  332 |     }
  333 |   });
  334 | 
  335 |   test('TC-POS-004: Image Layer Manipulation', async ({ page }) => {
  336 |     const uploadBtn = page.locator('input[type="file"][accept*="image"]').first();
  337 |     if (await uploadBtn.count() > 0) {
  338 |       const testImagePath = path.resolve('public/favicon.svg');
  339 |       await uploadBtn.setInputFiles(testImagePath);
  340 | 
  341 |       const imageLayer = page.locator('[data-testid="image-layer"], .image-element, .layer-image').first();
  342 |       if (await imageLayer.count() > 0) {
  343 |         const box = await imageLayer.boundingBox();
  344 |         if (box) {
  345 |           await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2);
  346 |           await page.mouse.down();
  347 |           await page.mouse.move(box.x + 100, box.y + 100);
  348 |           await page.mouse.up();
  349 |         }
  350 |       }
  351 |     }
  352 |   });
  353 | 
  354 |   test('TC-POS-005: Template Switch Data Loss', async ({ page }) => {
  355 |     const textLayer = page.locator('[contenteditable="true"]').first();
  356 |     if (await textLayer.count() > 0) {
  357 |       await textLayer.click();
  358 |       await textLayer.fill('Unsaved Changes');
  359 |     }
  360 | 
  361 |     const anotherTemplate = page.locator('[data-testid="template"], .template-item').nth(1);
  362 |     if (await anotherTemplate.count() > 0) {
  363 |       await anotherTemplate.click();
  364 | 
  365 |       const confirmDialog = page.locator('text=/unsaved|lost|discard|未保存|丢失/i');
  366 |       const hasDialog = await confirmDialog.count() > 0;
  367 |     }
  368 |   });
  369 | 
  370 |   test('TC-POS-006: Cross-Module Image Usage', async ({ page }) => {
  371 |     const myPhotosBtn = page.getByRole('button', { name: /my photos|assets|library|我的照片/i }).first();
  372 |     if (await myPhotosBtn.count() > 0) {
  373 |       await myPhotosBtn.click();
  374 | 
  375 |       const recentPhotos = page.locator('[data-testid="recent-photo"], .photo-item, .asset-item');
  376 |       const hasRecentPhotos = await recentPhotos.count() > 0;
  377 |     }
```