# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: data\gen_d2dd3659\expanded_gen_0.spec.ts >> Suite: Photo Module (General Editing) >> TC-PHO-003: Undo/Redo Stack Limit
- Location: data\gen_d2dd3659\expanded_gen_0.spec.ts:508:7

# Error details

```
Error: page.goto: Protocol error (Page.navigate): Cannot navigate to invalid URL
Call log:
  - navigating to "/", waiting until "load"

```

# Test source

```ts
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
  383 |     await page.goto('/');
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
> 461 |     await page.goto('/');
      |                ^ Error: page.goto: Protocol error (Page.navigate): Cannot navigate to invalid URL
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
  484 | 
  485 |       const resetBtn = page.getByRole('button', { name: /reset|original|重置|原图/i }).first();
  486 |       if (await resetBtn.count() > 0) {
  487 |         await resetBtn.click();
  488 |       }
  489 |     }
  490 |   });
  491 | 
  492 |   test('TC-PHO-002: Download Without Edits', async ({ page }) => {
  493 |     const fileInput = page.locator('input[type="file"]').first();
  494 |     if (await fileInput.count() > 0) {
  495 |       const testImagePath = path.resolve('public/favicon.svg');
  496 |       await fileInput.setInputFiles(testImagePath);
  497 | 
  498 |       const downloadBtn = page.getByRole('button', { name: /download|下载/i }).first();
  499 |       if (await downloadBtn.count() > 0) {
  500 |         const [download] = await Promise.all([
  501 |           page.waitForEvent('download').catch(() => null),
  502 |           downloadBtn.click()
  503 |         ]);
  504 |       }
  505 |     }
  506 |   });
  507 | 
  508 |   test('TC-PHO-003: Undo/Redo Stack Limit', async ({ page }) => {
  509 |     const fileInput = page.locator('input[type="file"]').first();
  510 |     if (await fileInput.count() > 0) {
  511 |       const testImagePath = path.resolve('public/favicon.svg');
  512 |       await fileInput.setInputFiles(testImagePath);
  513 | 
  514 |       const rotateBtn = page.getByRole('button', { name: /rotate|旋转/i }).first();
  515 |       if (await rotateBtn.count() > 0) {
  516 |         for (let i = 0; i < 50; i++) {
  517 |           await rotateBtn.click();
  518 |         }
  519 | 
  520 |         const undoBtn = page.getByRole('button', { name: /undo|撤销/i }).first();
  521 |         if (await undoBtn.count() > 0) {
  522 |           for (let i = 0; i < 51; i++) {
  523 |             await undoBtn.click().catch(() => {});
  524 |           }
  525 |         }
  526 | 
  527 |         const redoBtn = page.getByRole('button', { name: /redo|重做/i }).first();
  528 |         if (await redoBtn.count() > 0) {
  529 |           await redoBtn.click();
  530 |         }
  531 |       }
  532 |     }
  533 |   });
  534 | 
  535 |   test('TC-PHO-004: Browser Refresh During Edit', async ({ page }) => {
  536 |     const fileInput = page.locator('input[type="file"]').first();
  537 |     if (await fileInput.count() > 0) {
  538 |       const testImagePath = path.resolve('public/favicon.svg');
  539 |       await fileInput.setInputFiles(testImagePath);
  540 | 
  541 |       const filterBtn = page.getByRole('button', { name: /filter|滤镜/i }).first();
  542 |       if (await filterBtn.count() > 0) {
  543 |         await filterBtn.click();
  544 |       }
  545 | 
  546 |       page.on('dialog', dialog => dialog.dismiss());
  547 |       await page.reload();
  548 | 
  549 |       await expect(page.locator('body')).toBeVisible();
  550 |     }
  551 |   });
  552 | 
  553 |   test('TC-PHO-005: Corrupted Image Upload', async ({ page }) => {
  554 |     const fileInput = page.locator('input[type="file"]').first();
  555 |     if (await fileInput.count() > 0) {
  556 |       const corruptedFile = {
  557 |         name: 'corrupted.jpg',
  558 |         mimeType: 'image/jpeg',
  559 |         buffer: Buffer.from('This is not a valid image file content')
  560 |       };
  561 | 
```