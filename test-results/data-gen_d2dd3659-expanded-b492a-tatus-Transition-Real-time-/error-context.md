# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: data\gen_d2dd3659\expanded_gen_0.spec.ts >> Suite: Orders Module >> TC-ORD-005: Order Status Transition (Real-time)
- Location: data\gen_d2dd3659\expanded_gen_0.spec.ts:444:7

# Error details

```
Error: page.goto: Protocol error (Page.navigate): Cannot navigate to invalid URL
Call log:
  - navigating to "/", waiting until "load"

```

# Test source

```ts
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
  378 |   });
  379 | });
  380 | 
  381 | test.describe('Suite: Orders Module', () => {
  382 |   test.beforeEach(async ({ page }) => {
> 383 |     await page.goto('/');
      |                ^ Error: page.goto: Protocol error (Page.navigate): Cannot navigate to invalid URL
  384 |     const ordersLink = page.getByRole('link', { name: /orders|订单/i }).first();
  385 |     if (await ordersLink.count() > 0) {
  386 |       await ordersLink.click();
  387 |       await page.waitForLoadState('domcontentloaded');
  388 |     }
  389 |   });
  390 | 
  391 |   test('TC-ORD-001: View Order History', async ({ page }) => {
  392 |     const orderList = page.locator('[data-testid="order-list"], .order-item, .orders-container').first();
  393 |     await expect(orderList).toBeVisible({ timeout: 5000 }).catch(() => {});
  394 | 
  395 |     const orderItem = page.locator('[data-testid="order-item"], .order-card, tr[data-order-id]').first();
  396 |     if (await orderItem.count() > 0) {
  397 |       await orderItem.click();
  398 | 
  399 |       const orderDetail = page.locator('[data-testid="order-detail"], .order-details, .detail-view');
  400 |       await expect(orderDetail).toBeVisible({ timeout: 3000 }).catch(() => {});
  401 |     }
  402 |   });
  403 | 
  404 |   test('TC-ORD-002: Zero State (No Orders)', async ({ page }) => {
  405 |     const emptyState = page.locator('text=/no orders|empty|没有订单|暂无订单/i');
  406 |     const createNowBtn = page.getByRole('button', { name: /create|start|创建|开始/i });
  407 | 
  408 |     const hasEmptyState = await emptyState.count() > 0;
  409 |     const hasCreateBtn = await createNowBtn.count() > 0;
  410 |   });
  411 | 
  412 |   test('TC-ORD-003: Pagination/Infinite Scroll Boundary', async ({ page }) => {
  413 |     await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
  414 |     await page.waitForTimeout(1000);
  415 | 
  416 |     const loadMoreBtn = page.getByRole('button', { name: /load more|more|加载更多/i });
  417 |     if (await loadMoreBtn.count() > 0) {
  418 |       await loadMoreBtn.click();
  419 |       await page.waitForTimeout(1000);
  420 |     }
  421 | 
  422 |     const orderItems = page.locator('[data-testid="order-item"], .order-card, tr[data-order-id]');
  423 |     const count = await orderItems.count();
  424 |   });
  425 | 
  426 |   test('TC-ORD-004: Filter by Invalid Date Range', async ({ page }) => {
  427 |     const startDateInput = page.locator('input[type="date"]').first();
  428 |     const endDateInput = page.locator('input[type="date"]').nth(1);
  429 | 
  430 |     if (await startDateInput.count() > 0 && await endDateInput.count() > 0) {
  431 |       await startDateInput.fill('2024-12-31');
  432 |       await endDateInput.fill('2024-01-01');
  433 | 
  434 |       const filterBtn = page.getByRole('button', { name: /filter|search|筛选|搜索/i });
  435 |       if (await filterBtn.count() > 0) {
  436 |         await filterBtn.click();
  437 |       }
  438 | 
  439 |       const errorMessage = page.locator('text=/invalid|cannot be after|start date|无效|开始日期/i');
  440 |       const hasError = await errorMessage.count() > 0;
  441 |     }
  442 |   });
  443 | 
  444 |   test('TC-ORD-005: Order Status Transition (Real-time)', async ({ page }) => {
  445 |     const pendingOrder = page.locator('text=/pending|waiting|待支付/i').first();
  446 |     if (await pendingOrder.count() > 0) {
  447 |       await pendingOrder.click();
  448 | 
  449 |       const payBtn = page.getByRole('button', { name: /pay|支付|付款/i }).first();
  450 |       if (await payBtn.count() > 0) {
  451 |         await payBtn.click();
  452 | 
  453 |         const statusUpdate = page.locator('text=/paid|processing|已支付|处理中/i');
  454 |       }
  455 |     }
  456 |   });
  457 | });
  458 | 
  459 | test.describe('Suite: Photo Module (General Editing)', () => {
  460 |   test.beforeEach(async ({ page }) => {
  461 |     await page.goto('/');
  462 |     const photoLink = page.getByRole('link', { name: /photo|edit|照片|编辑/i }).first();
  463 |     if (await photoLink.count() > 0) {
  464 |       await photoLink.click();
  465 |       await page.waitForLoadState('domcontentloaded');
  466 |     }
  467 |   });
  468 | 
  469 |   test('TC-PHO-001: Filter Application and Reset', async ({ page }) => {
  470 |     const fileInput = page.locator('input[type="file"]').first();
  471 |     if (await fileInput.count() > 0) {
  472 |       const testImagePath = path.resolve('public/favicon.svg');
  473 |       await fileInput.setInputFiles(testImagePath);
  474 | 
  475 |       const grayscaleFilter = page.getByRole('button', { name: /grayscale|黑白|灰度/i }).first();
  476 |       if (await grayscaleFilter.count() > 0) {
  477 |         await grayscaleFilter.click();
  478 |       }
  479 | 
  480 |       const blurFilter = page.getByRole('button', { name: /blur|模糊/i }).first();
  481 |       if (await blurFilter.count() > 0) {
  482 |         await blurFilter.click();
  483 |       }
```