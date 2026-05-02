# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: data\gen_d2dd3659\expanded_gen_0.spec.ts >> Suite: Hall (Dashboard/Lobby) >> TC-HALL-003: Session Timeout Handling
- Location: data\gen_d2dd3659\expanded_gen_0.spec.ts:611:7

# Error details

```
Error: page.goto: Protocol error (Page.navigate): Cannot navigate to invalid URL
Call log:
  - navigating to "/", waiting until "load"

```

# Test source

```ts
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
  562 |       await fileInput.setInputFiles(corruptedFile as any).catch(() => {});
  563 | 
  564 |       const errorMessage = page.locator('text=/unable to load|error|invalid|无法加载|错误|无效/i');
  565 |       await page.waitForTimeout(2000);
  566 |     }
  567 |   });
  568 | });
  569 | 
  570 | test.describe('Suite: Hall (Dashboard/Lobby)', () => {
  571 |   test.beforeEach(async ({ page }) => {
> 572 |     await page.goto('/');
      |                ^ Error: page.goto: Protocol error (Page.navigate): Cannot navigate to invalid URL
  573 |     const hallLink = page.getByRole('link', { name: /hall|dashboard|大厅|主页/i }).first();
  574 |     if (await hallLink.count() > 0) {
  575 |       await hallLink.click();
  576 |       await page.waitForLoadState('domcontentloaded');
  577 |     }
  578 |   });
  579 | 
  580 |   test('TC-HALL-001: Dashboard Data Aggregation', async ({ page }) => {
  581 |     const widgets = page.locator('[data-testid="widget"], .widget, .dashboard-card');
  582 |     const widgetCount = await widgets.count();
  583 | 
  584 |     if (widgetCount > 0) {
  585 |       for (let i = 0; i < Math.min(widgetCount, 3); i++) {
  586 |         const widget = widgets.nth(i);
  587 |         await expect(widget).toBeVisible();
  588 |       }
  589 |     }
  590 |   });
  591 | 
  592 |   test('TC-HALL-002: Quick Action Navigation', async ({ page }) => {
  593 |     const quickActionIdPhoto = page.getByRole('link', { name: /create.*id.*photo|证件照/i })
  594 |       .or(page.getByRole('button', { name: /create.*id.*photo|证件照/i }));
  595 |     
  596 |     if (await quickActionIdPhoto.count() > 0) {
  597 |       await quickActionIdPhoto.first().click();
  598 |       await page.waitForLoadState('domcontentloaded');
  599 |       await page.goBack();
  600 |     }
  601 | 
  602 |     const quickActionPoster = page.getByRole('link', { name: /create.*poster|海报/i })
  603 |       .or(page.getByRole('button', { name: /create.*poster|海报/i }));
  604 |     
  605 |     if (await quickActionPoster.count() > 0) {
  606 |       await quickActionPoster.first().click();
  607 |       await page.waitForLoadState('domcontentloaded');
  608 |     }
  609 |   });
  610 | 
  611 |   test('TC-HALL-003: Session Timeout Handling', async ({ page }) => {
  612 |     await page.evaluate(() => {
  613 |       localStorage.setItem('sessionExpiry', Date.now().toString());
  614 |     });
  615 | 
  616 |     const actionBtn = page.getByRole('button').first();
  617 |     if (await actionBtn.count() > 0) {
  618 |       await actionBtn.click().catch(() => {});
  619 | 
  620 |       const sessionModal = page.locator('text=/session.*expired|login|会话|登录/i');
  621 |       const loginRedirect = page.url().includes('login');
  622 |     }
  623 |   });
  624 | 
  625 |   test('TC-HALL-004: Accessibility Check', async ({ page }) => {
  626 |     const focusableElements = await page.locator('button, a, input, select, textarea, [tabindex]:not([tabindex="-1"])').all();
  627 |     
  628 |     for (const element of focusableElements.slice(0, 10)) {
  629 |       await page.keyboard.press('Tab');
  630 |       
  631 |       const focusedElement = page.locator(':focus');
  632 |       await expect(focusedElement).toBeVisible();
  633 |     }
  634 | 
  635 |     const accessibilityViolations = await page.evaluate(() => {
  636 |       const issues: string[] = [];
  637 |       const buttons = document.querySelectorAll('button');
  638 |       buttons.forEach(btn => {
  639 |         if (!btn.textContent?.trim() && !btn.getAttribute('aria-label') && !btn.getAttribute('title')) {
  640 |           issues.push('Button without accessible name');
  641 |         }
  642 |       });
  643 |       return issues;
  644 |     });
  645 | 
  646 |     expect(accessibilityViolations.length).toBeLessThan(5);
  647 |   });
  648 | });
```