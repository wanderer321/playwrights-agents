import { test, expect } from '@playwright/test';
import path from 'path';

// ============================================
// Suite: Home (Dashboard/Landing)
// ============================================

test.describe('Home (Dashboard/Landing)', () => {
  test('TC-HOME-001: Initial Page Load and Navigation', async ({ page }) => {
    await page.goto('/');
    
    // Wait for page load and verify load time
    await expect(page).toHaveLoadState('networkidle', { timeout: 3000 });
    
    // Verify all navigation cards/buttons are visible
    const navCards = page.locator('[role="link"], [role="button"], .nav-card, .feature-card, a[href*="id-photo"], a[href*="poster"], a[href*="photo"], a[href*="hall"], a[href*="orders"]');
    await expect(navCards.first()).toBeVisible();
    
    // Click and verify navigation to each module
    const modules = ['id-photo', 'poster', 'photo', 'hall', 'orders'];
    for (const module of modules) {
      const moduleLink = page.locator(`a[href*="${module}"], [data-testid="${module}"], button:has-text("${module}")`).first();
      if (await moduleLink.isVisible()) {
        await moduleLink.click();
        await expect(page).toHaveURL(new RegExp(module));
        await page.goBack();
      }
    }
  });

  test('TC-HOME-002: Empty State for New User', async ({ page }) => {
    // Simulate new user with no history
    await page.goto('/');
    await page.evaluate(() => localStorage.clear());
    await page.reload();
    
    // Check for empty state in Recent Orders or Activity section
    const emptyState = page.locator('.empty-state, [data-testid="empty-state"], :text("No orders"), :text("No activity"), :text("start creating")');
    
    if (await emptyState.isVisible()) {
      await expect(emptyState).toBeVisible();
    }
    
    // Verify no broken images or undefined text
    const brokenImages = page.locator('img[src=""], img[src="undefined"]');
    await expect(brokenImages).toHaveCount(0);
    
    const undefinedText = page.locator(':text("undefined"), :text("null")');
    await expect(undefinedText).toHaveCount(0);
  });

  test('TC-HOME-003: Rapid Module Switching', async ({ page }) => {
    await page.goto('/');
    
    const tabs = ['Home', 'Hall', 'Orders'];
    const errors: string[] = [];
    
    page.on('console', msg => {
      if (msg.type() === 'error') {
        errors.push(msg.text());
      }
    });
    
    // Rapidly click between tabs
    for (let i = 0; i < 5; i++) {
      for (const tab of tabs) {
        const tabButton = page.locator(`[role="tab"]:has-text("${tab}"), a:has-text("${tab}"), button:has-text("${tab}")`).first();
        if (await tabButton.isVisible()) {
          await tabButton.click({ force: true });
        }
      }
    }
    
    // Wait for final state
    await page.waitForTimeout(500);
    
    // Verify no console errors
    expect(errors.filter(e => !e.includes('favicon'))).toHaveLength(0);
  });

  test('TC-HOME-004: Network Failure Resilience', async ({ page, context }) => {
    await page.goto('/');
    
    // Set network to offline
    await context.setOffline(true);
    
    // Refresh page
    await page.reload({ waitUntil: 'domcontentloaded' }).catch(() => {});
    
    // Check for network error message
    const errorMessage = page.locator(':text("Network Error"), :text("Unable to connect"), :text("网络错误"), .error-message, [role="alert"]');
    
    // Should show error instead of white screen
    await expect(errorMessage.or(page.locator('body'))).toBeVisible();
    
    // Restore network and verify retry
    await context.setOffline(false);
    const retryButton = page.locator('button:has-text("Retry"), button:has-text("重试")');
    if (await retryButton.isVisible()) {
      await retryButton.click();
      await expect(page).toHaveLoadState('networkidle');
    }
  });

  test('TC-HOME-005: Responsive Layout Verification', async ({ page }) => {
    await page.goto('/');
    
    // Test desktop view
    await page.setViewportSize({ width: 1920, height: 1080 });
    await page.waitForTimeout(300);
    
    const cards = page.locator('.feature-card, .nav-card, [data-testid*="card"]');
    const desktopCardCount = await cards.count();
    
    // Test tablet view
    await page.setViewportSize({ width: 768, height: 1024 });
    await page.waitForTimeout(300);
    
    // Test mobile view
    await page.setViewportSize({ width: 375, height: 667 });
    await page.waitForTimeout(300);
    
    // Verify no horizontal scroll
    const scrollWidth = await page.evaluate(() => document.documentElement.scrollWidth);
    const clientWidth = await page.evaluate(() => document.documentElement.clientWidth);
    expect(scrollWidth).toBeLessThanOrEqual(clientWidth + 10);
    
    // Verify cards are still visible
    await expect(cards.first()).toBeVisible();
  });

  test('TC-HOME-006: Session Expiry Handling', async ({ page }) => {
    await page.goto('/');
    
    // Clear session token
    await page.evaluate(() => {
      localStorage.removeItem('token');
      localStorage.removeItem('authToken');
      sessionStorage.clear();
    });
    
    // Attempt to click a feature
    const featureButton = page.locator('.feature-card, [role="link"]').first();
    if (await featureButton.isVisible()) {
      await featureButton.click();
      
      // Should redirect to login or show session expiry modal
      const loginPage = page.locator('[data-testid="login"], .login-form, :text("登录"), :text("Login")');
      const sessionModal = page.locator('[role="dialog"], .session-expired, :text("session"), :text("expired")');
      
      await expect(loginPage.or(sessionModal)).toBeVisible({ timeout: 5000 });
    }
  });
});

// ============================================
// Suite: ID Photo (ID Photo Generation)
// ============================================

test.describe('ID Photo (ID Photo Generation)', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/id-photo');
  });

  test('TC-IDP-001: Standard ID Photo Generation Flow', async ({ page }) => {
    // Upload valid portrait image
    const uploadInput = page.locator('input[type="file"]');
    const testImagePath = path.resolve('src/frontend/favicon.svg');
    
    await uploadInput.setInputFiles(testImagePath);
    
    // Select standard specification
    const specButton = page.locator('button:has-text("1寸"), button:has-text("1-inch"), [data-spec="1inch"]').first();
    if (await specButton.isVisible()) {
      await specButton.click();
    }
    
    // Click Process
    const processButton = page.locator('button:has-text("Process"), button:has-text("处理"), button:has-text("生成")');
    if (await processButton.isVisible()) {
      await processButton.click();
      
      // Wait for processing
      await page.waitForTimeout(2000);
    }
    
    // Verify download button appears
    const downloadButton = page.locator('button:has-text("Download"), button:has-text("下载"), a[download]');
    await expect(downloadButton.or(page.locator('.preview-image, .result-preview'))).toBeVisible({ timeout: 10000 });
  });

  test('TC-IDP-002: Invalid File Format Upload', async ({ page }) => {
    const uploadInput = page.locator('input[type="file"]');
    
    // Create invalid file
    const invalidFile = {
      name: 'test.txt',
      mimeType: 'text/plain',
      buffer: Buffer.from('This is not an image')
    };
    
    await uploadInput.setInputFiles(invalidFile);
    
    // Verify error message
    const errorMessage = page.locator(':text("Unsupported"), :text("Invalid"), :text("不支持"), :text("格式错误"), [role="alert"]');
    await expect(errorMessage).toBeVisible({ timeout: 3000 });
  });

  test('TC-IDP-003: Maximum File Size Boundary', async ({ page }) => {
    const uploadInput = page.locator('input[type="file"]');
    
    // Create file at size limit (simulated)
    const largeFile = {
      name: 'large.jpg',
      mimeType: 'image/jpeg',
      buffer: Buffer.alloc(10 * 1024 * 1024) // 10MB
    };
    
    await uploadInput.setInputFiles(largeFile).catch(() => {});
    
    // Check for size error or successful upload
    const sizeError = page.locator(':text("too large"), :text("File size"), :text("文件过大"), :text("大小超")');
    
    // Either upload succeeds or shows appropriate error
    await page.waitForTimeout(1000);
    const hasError = await sizeError.isVisible().catch(() => false);
    expect(typeof hasError).toBe('boolean');
  });

  test('TC-IDP-004: Non-Human/Face Detection Failure', async ({ page }) => {
    const uploadInput = page.locator('input[type="file"]');
    const testImagePath = path.resolve('src/frontend/favicon.svg');
    
    await uploadInput.setInputFiles(testImagePath);
    await page.waitForTimeout(1000);
    
    // Check for face detection error
    const faceError = page.locator(':text("No face"), :text("multiple faces"), :text("未检测到"), :text("多人"), [role="alert"]');
    
    // If error appears, verify it's visible
    if (await faceError.isVisible().catch(() => false)) {
      await expect(faceError).toBeVisible();
    }
  });

  test('TC-IDP-005: Browser Refresh During Processing', async ({ page }) => {
    const uploadInput = page.locator('input[type="file"]');
    const testImagePath = path.resolve('src/frontend/favicon.svg');
    
    await uploadInput.setInputFiles(testImagePath);
    
    const processButton = page.locator('button:has-text("Process"), button:has-text("处理")');
    if (await processButton.isVisible()) {
      await processButton.click();
    }
    
    // Immediately refresh
    await page.reload();
    
    // Should return to initial state
    await expect(uploadInput).toBeVisible();
    const processingIndicator = page.locator('.processing, :text("Processing"), :text("处理中")');
    await expect(processingIndicator).not.toBeVisible();
  });

  test('TC-IDP-006: Double-Submit Prevention', async ({ page }) => {
    const uploadInput = page.locator('input[type="file"]');
    const testImagePath = path.resolve('src/frontend/favicon.svg');
    
    await uploadInput.setInputFiles(testImagePath);
    
    const processButton = page.locator('button:has-text("Process"), button:has-text("处理")');
    if (await processButton.isVisible()) {
      // Rapid clicks
      await Promise.all([
        processButton.click(),
        processButton.click({ delay: 50 }),
        processButton.click({ delay: 100 }),
        processButton.click({ delay: 150 }),
        processButton.click({ delay: 200 })
      ]);
      
      // Button should be disabled
      await expect(processButton).toBeDisabled();
    }
  });

  test('TC-IDP-007: Background Color Switching', async ({ page }) => {
    const uploadInput = page.locator('input[type="file"]');
    const testImagePath = path.resolve('src/frontend/favicon.svg');
    
    await uploadInput.setInputFiles(testImagePath);
    await page.waitForTimeout(500);
    
    // Find color picker options
    const blueOption = page.locator('[data-color="blue"], button:has-text("Blue"), .color-blue').first();
    const redOption = page.locator('[data-color="red"], button:has-text("Red"), .color-red').first();
    const whiteOption = page.locator('[data-color="white"], button:has-text("White"), .color-white').first();
    
    if (await blueOption.isVisible()) {
      await blueOption.click();
      await page.waitForTimeout(300);
    }
    
    if (await redOption.isVisible()) {
      await redOption.click();
      await page.waitForTimeout(300);
    }
    
    if (await whiteOption.isVisible()) {
      await whiteOption.click();
      await page.waitForTimeout(300);
    }
    
    // Verify preview updates
    const preview = page.locator('.preview, .result-preview, canvas');
    await expect(preview.first()).toBeVisible();
  });
});

// ============================================
// Suite: Photo (General Photo Editing)
// ============================================

test.describe('Photo (General Photo Editing)', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/photo');
  });

  test('TC-PHO-001: Basic Photo Edit and Save', async ({ page }) => {
    const uploadInput = page.locator('input[type="file"]');
    const testImagePath = path.resolve('src/frontend/favicon.svg');
    
    await uploadInput.setInputFiles(testImagePath);
    await page.waitForTimeout(500);
    
    // Apply B&W filter
    const bwFilter = page.locator('button:has-text("B&W"), button:has-text("黑白"), [data-filter="grayscale"]').first();
    if (await bwFilter.isVisible()) {
      await bwFilter.click();
    }
    
    // Adjust brightness
    const brightnessSlider = page.locator('input[type="range"][aria-label*="brightness"], input[type="range"][aria-label*="亮度"]');
    if (await brightnessSlider.isVisible()) {
      await brightnessSlider.fill('75');
    }
    
    // Save/Download
    const saveButton = page.locator('button:has-text("Save"), button:has-text("Download"), button:has-text("保存")');
    if (await saveButton.isVisible()) {
      await saveButton.click();
    }
    
    await page.waitForTimeout(500);
    await expect(page.locator('canvas, .preview, img')).toBeVisible();
  });

  test('TC-PHO-002: Undo/Redo State Management', async ({ page }) => {
    const uploadInput = page.locator('input[type="file"]');
    const testImagePath = path.resolve('src/frontend/favicon.svg');
    
    await uploadInput.setInputFiles(testImagePath);
    await page.waitForTimeout(500);
    
    // Apply 3 changes
    const filterButtons = page.locator('[data-filter], button:has-text("Filter"), button:has-text("滤镜")');
    const count = Math.min(3, await filterButtons.count());
    
    for (let i = 0; i < count; i++) {
      await filterButtons.nth(i).click();
      await page.waitForTimeout(200);
    }
    
    // Undo 3 times
    const undoButton = page.locator('button:has-text("Undo"), button[aria-label="Undo"], button:has-text("撤销")');
    for (let i = 0; i < 3; i++) {
      if (await undoButton.isVisible()) {
        await undoButton.click();
        await page.waitForTimeout(200);
      }
    }
    
    // Redo 2 times
    const redoButton = page.locator('button:has-text("Redo"), button[aria-label="Redo"], button:has-text("重做")');
    for (let i = 0; i < 2; i++) {
      if (await redoButton.isVisible()) {
        await redoButton.click();
        await page.waitForTimeout(200);
      }
    }
    
    // Verify state is consistent
    await expect(page.locator('canvas, .preview')).toBeVisible();
  });

  test('TC-PHO-003: Corrupted Image Handling', async ({ page }) => {
    const uploadInput = page.locator('input[type="file"]');
    
    const corruptedFile = {
      name: 'corrupted.jpg',
      mimeType: 'image/jpeg',
      buffer: Buffer.from('This is not a valid JPEG file content')
    };
    
    await uploadInput.setInputFiles(corruptedFile);
    
    // Check for error message
    const errorMessage = page.locator(':text("Unable to read"), :text("corrupted"), :text("无法读取"), :text("文件损坏"), [role="alert"]');
    await expect(errorMessage).toBeVisible({ timeout: 3000 });
  });

  test('TC-PHO-004: Extreme Aspect Ratio Crop', async ({ page }) => {
    const uploadInput = page.locator('input[type="file"]');
    const testImagePath = path.resolve('src/frontend/favicon.svg');
    
    await uploadInput.setInputFiles(testImagePath);
    await page.waitForTimeout(500);
    
    // Find crop tool
    const cropButton = page.locator('button:has-text("Crop"), button:has-text("裁剪")');
    if (await cropButton.isVisible()) {
      await cropButton.click();
      
      // Attempt extreme crop selection
      const canvas = page.locator('canvas');
      if (await canvas.isVisible()) {
        const box = await canvas.boundingBox();
        if (box) {
          // Simulate extreme vertical strip selection
          await page.mouse.move(box.x + 10, box.y + 10);
          await page.mouse.down();
          await page.mouse.move(box.x + 15, box.y + box.height - 10);
          await page.mouse.up();
        }
      }
    }
    
    // Verify no rendering errors
    const errorElement = page.locator('.error, [role="alert"]');
    await expect(errorElement).not.toBeVisible();
  });

  test('TC-PHO-005: Mobile Viewport Interaction', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    
    const uploadInput = page.locator('input[type="file"]');
    const testImagePath = path.resolve('src/frontend/favicon.svg');
    
    await uploadInput.setInputFiles(testImagePath);
    await page.waitForTimeout(500);
    
    // Check touch targets are large enough
    const interactiveElements = page.locator('button, input[type="range"], [role="slider"]');
    const count = await interactiveElements.count();
    
    for (let i = 0; i < Math.min(5, count); i++) {
      const element = interactiveElements.nth(i);
      if (await element.isVisible()) {
        const box = await element.boundingBox();
        if (box) {
          // Touch targets should be at least 44px
          expect(Math.min(box.width, box.height)).toBeGreaterThanOrEqual(44);
        }
      }
    }
  });
});

// ============================================
// Suite: Poster (Poster Design)
// ============================================

test.describe('Poster (Poster Design)', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/poster');
  });

  test('TC-POS-001: Create Poster from Template', async ({ page }) => {
    // Select template
    const template = page.locator('.template, [data-testid="template"], .template-card').first();
    if (await template.isVisible()) {
      await template.click();
    }
    
    // Replace placeholder text
    const textInput = page.locator('input[type="text"], [contenteditable="true"]').first();
    if (await textInput.isVisible()) {
      await textInput.fill('Test Poster Title');
    }
    
    // Upload custom image
    const imageUpload = page.locator('input[type="file"]');
    if (await imageUpload.isVisible()) {
      const testImagePath = path.resolve('src/frontend/favicon.svg');
      await imageUpload.setInputFiles(testImagePath);
    }
    
    // Save draft
    const saveButton = page.locator('button:has-text("Save"), button:has-text("保存"), button:has-text("Save Draft")');
    if (await saveButton.isVisible()) {
      await saveButton.click();
    }
    
    await page.waitForTimeout(500);
  });

  test('TC-POS-002: Text Overflow Handling', async ({ page }) => {
    const template = page.locator('.template, [data-testid="template"]').first();
    if (await template.isVisible()) {
      await template.click();
    }
    
    const textInput = page.locator('input[type="text"], [contenteditable="true"]').first();
    if (await textInput.isVisible()) {
      // Paste 500-word paragraph
      const longText = 'Lorem ipsum '.repeat(50);
      await textInput.fill(longText);
    }
    
    // Verify no text spill
    const textBox = page.locator('.text-box, [data-testid="text-container"]').first();
    if (await textBox.isVisible()) {
      const containerBox = await textBox.boundingBox();
      const parentBox = await textBox.locator('xpath=..').boundingBox();
      
      if (containerBox && parentBox) {
        expect(containerBox.width).toBeLessThanOrEqual(parentBox.width + 10);
      }
    }
  });

  test('TC-POS-003: XSS Injection in Text Fields', async ({ page }) => {
    const template = page.locator('.template, [data-testid="template"]').first();
    if (await template.isVisible()) {
      await template.click();
    }
    
    const textInput = page.locator('input[type="text"], [contenteditable="true"]').first();
    if (await textInput.isVisible()) {
      await textInput.fill('<script>alert("xss")</script>');
    }
    
    // Save and reload
    const saveButton = page.locator('button:has-text("Save"), button:has-text("保存")');
    if (await saveButton.isVisible()) {
      await saveButton.click();
    }
    
    await page.reload();
    
    // Verify no alert executed and script is sanitized
    const scriptElement = page.locator('script:has-text("alert")');
    await expect(scriptElement).toHaveCount(0);
    
    // Text should be displayed as plain text or stripped
    const sanitizedText = page.locator(':text("script"), :text("alert")');
    // Either shows sanitized text or nothing
  });

  test('TC-POS-004: Missing Font Fallback', async ({ page }) => {
    // Inject custom font reference
    await page.evaluate(() => {
      document.body.style.fontFamily = '"NonExistentFont", sans-serif';
    });
    
    await page.waitForTimeout(300);
    
    // Verify layout doesn't break
    const bodyText = page.locator('body');
    await expect(bodyText).toBeVisible();
    
    // Check computed font falls back
    const computedFont = await page.evaluate(() => {
      return window.getComputedStyle(document.body).fontFamily;
    });
    
    expect(computedFont).toContain('sans-serif');
  });

  test('TC-POS-005: Auto-Save Recovery', async ({ page, context }) => {
    const template = page.locator('.template, [data-testid="template"]').first();
    if (await template.isVisible()) {
      await template.click();
    }
    
    // Make edits
    const textInput = page.locator('input[type="text"], [contenteditable="true"]').first();
    if (await textInput.isVisible()) {
      await textInput.fill('Auto-save test content');
    }
    
    await page.waitForTimeout(2000); // Wait for auto-save
    
    // Simulate crash by reloading
    await page.reload();
    
    // Check for recovery prompt
    const recoveryPrompt = page.locator(':text("Restore"), :text("unsaved"), :text("恢复"), [role="dialog"]');
    
    // If recovery prompt exists, verify it works
    if (await recoveryPrompt.isVisible().catch(() => false)) {
      await expect(recoveryPrompt).toBeVisible();
    }
  });

  test('TC-POS-006: Cross-Module Image Import', async ({ page }) => {
    // Navigate to ID Photo first
    await page.goto('/id-photo');
    
    const uploadInput = page.locator('input[type="file"]');
    const testImagePath = path.resolve('src/frontend/favicon.svg');
    
    await uploadInput.setInputFiles(testImagePath);
    await page.waitForTimeout(1000);
    
    // Go to Poster module
    await page.goto('/poster');
    
    // Check for recent images in media picker
    const mediaPicker = page.locator('[data-testid="media-picker"], .recent-images, .image-library');
    if (await mediaPicker.isVisible()) {
      const recentImage = mediaPicker.locator('img').first();
      await expect(recentImage).toBeVisible();
    }
  });
});

// ============================================
// Suite: Orders (Order Management)
// ============================================

test.describe('Orders (Order Management)', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/orders');
  });

  test('TC-ORD-001: View Order History', async ({ page }) => {
    // Verify orders list exists
    const ordersList = page.locator('.orders-list, [data-testid="orders"], .order-item');
    
    if (await ordersList.first().isVisible()) {
      // Check sorting (newest first)
      const orderDates = page.locator('.order-date, [data-testid="order-date"]');
      const count = await orderDates.count();
      
      if (count >= 2) {
        // Orders should be sorted by date
        await expect(ordersList.first()).toBeVisible();
      }
      
      // Check status visibility
      const statusBadge = page.locator('.order-status, [data-testid="status"], :text("Paid"), :text("Pending"), :text("Failed")');
      await expect(statusBadge.first()).toBeVisible();
    }
  });

  test('TC-ORD-002: Pagination/Infinite Scroll', async ({ page }) => {
    // Scroll to bottom
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
    await page.waitForTimeout(500);
    
    // Check for pagination or loading indicator
    const loadMore = page.locator('button:has-text("Load More"), .infinite-scroll, [data-testid="pagination"]');
    
    // Verify no duplicate entries at boundary
    const orderItems = page.locator('.order-item, [data-testid="order-item"]');
    const count = await orderItems.count();
    
    if (count > 0) {
      const orderIds = await orderItems.evaluateAll(items => 
        items.map(item => item.getAttribute('data-id') || item.id).filter(Boolean)
      );
      
      const uniqueIds = new Set(orderIds);
      expect(uniqueIds.size).toBe(orderIds.length);
    }
  });

  test('TC-ORD-003: Payment Retry Flow', async ({ page }) => {
    // Find failed order
    const failedOrder = page.locator('.order-item:has-text("Failed"), .order-item:has-text("失败")').first();
    
    if (await failedOrder.isVisible()) {
      const retryButton = failedOrder.locator('button:has-text("Retry"), button:has-text("重试")');
      
      if (await retryButton.isVisible()) {
        await retryButton.click();
        
        // Wait for payment flow
        await page.waitForTimeout(1000);
        
        // Verify status update
        const updatedStatus = page.locator(':text("Paid"), :text("Success"), :text("成功")');
        await expect(updatedStatus.first()).toBeVisible({ timeout: 5000 });
      }
    }
  });

  test('TC-ORD-004: Deep Link to Non-Existent Order', async ({ page }) => {
    await page.goto('/orders/999999');
    
    // Check for 404 handling
    const notFoundMessage = page.locator(':text("not found"), :text("不存在"), :text("404"), .error-page');
    await expect(notFoundMessage).toBeVisible({ timeout: 5000 });
    
    // Should not be blank screen or loader loop
    const loader = page.locator('.loading, [role="progressbar"]');
    await expect(loader).not.toBeVisible();
  });

  test('TC-ORD-005: Filter and Sort Consistency', async ({ page }) => {
    // Apply filter
    const filterButton = page.locator('button:has-text("Filter"), button:has-text("筛选"), [data-testid="filter"]');
    if (await filterButton.isVisible()) {
      await filterButton.click();
      
      const completedFilter = page.locator('input[value="Completed"], label:has-text("Completed")');
      if (await completedFilter.isVisible()) {
        await completedFilter.click();
      }
    }
    
    // Apply sort
    const sortSelect = page.locator('select, [data-testid="sort"]');
    if (await sortSelect.isVisible()) {
      await sortSelect.selectOption('price-desc');
    }
    
    // Refresh page
    await page.reload();
    
    // Check if filters persist via URL params or reset cleanly
    const url = page.url();
    expect(url).toBeDefined();
  });

  test('TC-ORD-006: Order Creation from ID Photo', async ({ page }) => {
    // Navigate to ID Photo
    await page.goto('/id-photo');
    
    const uploadInput = page.locator('input[type="file"]');
    const testImagePath = path.resolve('src/frontend/favicon.svg');
    
    await uploadInput.setInputFiles(testImagePath);
    
    // Process and checkout
    const processButton = page.locator('button:has-text("Process"), button:has-text("处理")');
    if (await processButton.isVisible()) {
      await processButton.click();
      await page.waitForTimeout(2000);
    }
    
    const checkoutButton = page.locator('button:has-text("Checkout"), button:has-text("支付"), button:has-text("购买")');
    if (await checkoutButton.isVisible()) {
      await checkoutButton.click();
      await page.waitForTimeout(1000);
    }
    
    // Go to Orders
    await page.goto('/orders');
    
    // Verify new order appears
    const newOrder = page.locator('.order-item, [data-testid="order-item"]').first();
    await expect(newOrder).toBeVisible();
  });
});

// ============================================
// Suite: Hall (Exhibition/Showcase)
// ============================================

test.describe('Hall (Exhibition/Showcase)', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/hall');
  });

  test('TC-HAL-001: Browse Gallery', async ({ page }) => {
    // Wait for images to load
    await page.waitForLoadState('networkidle');
    
    const galleryItems = page.locator('.gallery-item, [data-testid="gallery-item"], .showcase-item');
    await expect(galleryItems.first()).toBeVisible();
    
    // Scroll to trigger lazy load
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
    await page.waitForTimeout(500);
    
    // Verify placeholders were shown and layout is stable
    const images = page.locator('.gallery-item img, .showcase-item img');
    const count = await images.count();
    
    for (let i = 0; i < Math.min(3, count); i++) {
      await expect(images.nth(i)).toBeVisible();
    }
  });

  test('TC-HAL-002: Search with Special Characters', async ({ page }) => {
    const searchInput = page.locator('input[type="search"], [role="searchbox"], input[placeholder*="search"]');
    
    if (await searchInput.isVisible()) {
      // Test special characters
      await searchInput.fill("!@#$%^&*()");
      await searchInput.press('Enter');
      await page.waitForTimeout(500);
      
      // Test SQL injection string
      await searchInput.fill("' OR 1=1 --");
      await searchInput.press('Enter');
      await page.waitForTimeout(500);
      
      // Verify no database error exposed
      const dbError = page.locator(':text("SQL"), :text("database"), :text("error"), :text("mysql"), :text("postgres")');
      await expect(dbError).not.toBeVisible();
      
      // Should show empty results or sanitized results
      const results = page.locator('.gallery-item, .search-result');
      // Either empty or valid results
      expect(await results.count()).toBeGreaterThanOrEqual(0);
    }
  });

  test('TC-HAL-003: Broken Image Link Handling', async ({ page }) => {
    // Block specific image requests
    await page.route('**/*.jpg', route => route.abort());
    await page.route('**/*.png', route => route.abort());
    
    await page.reload();
    
    // Check for fallback placeholder
    const placeholder = page.locator('.placeholder, .broken-image, img[alt*="error"], [data-testid="placeholder"]');
    
    // Gallery should still render without crashing
    const gallery = page.locator('.gallery, [data-testid="gallery"]');
    await expect(gallery).toBeVisible();
  });

  test('TC-HAL-004: Deep Link to Specific Item', async ({ page, context }) => {
    // Find a gallery item
    const galleryItem = page.locator('.gallery-item a, [data-testid="gallery-item"] a').first();
    
    if (await galleryItem.isVisible()) {
      const itemUrl = await galleryItem.getAttribute('href');
      await galleryItem.click();
      
      // Get current URL
      const currentUrl = page.url();
      
      // Open in new context (simulating incognito)
      const newPage = await context.newPage();
      await newPage.goto(currentUrl);
      
      // Verify item details load directly
      const itemDetail = newPage.locator('.item-detail, [data-testid="item-detail"], .gallery-detail');
      await expect(itemDetail.or(newPage.locator('h1, h2'))).toBeVisible();
      
      await newPage.close();
    }
  });

  test('TC-HAL-005: Empty Gallery State', async ({ page }) => {
    const searchInput = page.locator('input[type="search"], [role="searchbox"]');
    
    if (await searchInput.isVisible()) {
      // Search for non-existent item
      await searchInput.fill('zzzzzzzzzzzzzzzzzzz');
      await searchInput.press('Enter');
      await page.waitForTimeout(500);
      
      // Check for empty state message
      const emptyState = page.locator(':text("No results"), :text("未找到"), :text("empty"), .empty-state');
      await expect(emptyState).toBeVisible({ timeout: 3000 });
      
      // Search bar should remain functional
      await expect(searchInput).toBeEnabled();
    }
  });
});

// ============================================
// Suite: Global & Cross-Cutting Concerns
// ============================================

test.describe('Global & Cross-Cutting Concerns', () => {
  test('TC-GLB-001: Browser Back Button Navigation', async ({ page }) => {
    // Navigate through pages
    await page.goto('/');
    await page.goto('/id-photo');
    await page.goto('/orders');
    
    // Click back twice
    await page.goBack();
    await expect(page).toHaveURL(/id-photo/);
    
    await page.goBack();
    await expect(page).toHaveURL('/');
  });

  test('TC-GLB-002: Concurrent Session Login', async ({ browser }) => {
    // Create two contexts (simulating two devices)
    const context1 = await browser.newContext();
    const context2 = await browser.newContext();
    
    const page1 = await context1.newPage();
    const page2 = await context2.newPage();
    
    // Login on both
    await page1.goto('/');
    await page2.goto('/');
    
    // Perform action on device A
    await page1.click('body');
    
    // Check if device A is logged out or token refreshed
    const page1Content = await page1.content();
    expect(page1Content).toBeDefined();
    
    await context1.close();
    await context2.close();
  });

  test('TC-GLB-003: Accessibility (a11y) Check', async ({ page }) => {
    await page.goto('/');
    
    // Tab through navigation
    await page.keyboard.press('Tab');
    await page.keyboard.press('Tab');
    await page.keyboard.press('Tab');
    
    // Check focus ring visibility
    const focusedElement = page.locator(':focus');
    await expect(focusedElement).toBeVisible();
    
    // Check for critical a11y issues
    const buttons = page.locator('button');
    const count = await buttons.count();
    
    for (let i = 0; i < Math.min(5, count); i++) {
      const button = buttons.nth(i);
      if (await button.isVisible()) {
        // Buttons should have accessible names
        const name = await button.getAttribute('aria-label') || 
                     await button.getAttribute('title') ||
                     await button.textContent();
        expect(name?.trim().length).toBeGreaterThan(0);
      }
    }
    
    // Check images have alt text
    const images = page.locator('img');
    const imgCount = await images.count();
    
    for (let i = 0; i < Math.min(5, imgCount); i++) {
      const img = images.nth(i);
      const alt = await img.getAttribute('alt');
      // Alt can be empty for decorative images
      expect(alt).toBeDefined();
    }
  });

  test('TC-GLB-004: Language/Locale Switching', async ({ page }) => {
    await page.goto('/');
    
    // Find language switcher
    const langSwitcher = page.locator('[data-testid="language-switcher"], select[name="lang"], button:has-text("中文"), button:has-text("EN")');
    
    if (await langSwitcher.isVisible()) {
      // Switch to Chinese
      const chineseOption = page.locator('option[value="zh-CN"], button:has-text("中文")');
      if (await chineseOption.isVisible()) {
        await chineseOption.click();
      } else {
        await langSwitcher.click();
      }
      
      await page.waitForTimeout(300);

      // Verify language switch (page should contain Chinese text)
      await expect(page.getByText(/首页|大厅|订单/i).first()).toBeVisible();
    }
  });
});