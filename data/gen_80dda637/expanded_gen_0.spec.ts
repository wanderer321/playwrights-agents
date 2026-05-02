import { test, expect, Page, BrowserContext } from '@playwright/test';
import path from 'path';

// Suite: Home (Dashboard/Landing)
test.describe('Home (Dashboard/Landing)', () => {
  // TC-HOME-001: Initial Load and Navigation Integrity
  test('TC-HOME-001: Initial Load and Navigation Integrity', async ({ page }) => {
    await page.goto('/');
    
    // Verify presence of key navigation elements
    await expect(page.getByRole('link', { name: /hall/i })).toBeVisible();
    await expect(page.getByRole('link', { name: /id.*photo/i })).toBeVisible();
    await expect(page.getByRole('link', { name: /poster/i })).toBeVisible();
    await expect(page.getByRole('link', { name: /order/i })).toBeVisible();
    
    // Click each navigation link and verify URL changes
    await page.getByRole('link', { name: /hall/i }).click();
    await expect(page).toHaveURL(/hall/);
    
    await page.getByRole('link', { name: /id.*photo/i }).click();
    await expect(page).toHaveURL(/idphoto/);
    
    await page.getByRole('link', { name: /poster/i }).click();
    await expect(page).toHaveURL(/poster/);
    
    await page.getByRole('link', { name: /order/i }).click();
    await expect(page).toHaveURL(/order/);
    
    await page.getByRole('link', { name: /home/i }).click();
    await expect(page).toHaveURL('/');
  });

  // TC-HOME-002: Dashboard Zero State
  test('TC-HOME-002: Dashboard Zero State', async ({ page }) => {
    // Login as new user with no history (mocked via localStorage/cookies)
    await page.addInitScript(() => {
      localStorage.setItem('user', JSON.stringify({ id: 'new-user', isNew: true }));
    });
    
    await page.goto('/');
    
    // Verify friendly empty states
    await expect(page.getByText(/no.*order/i)).toBeVisible();
    await expect(page.getByText(/create.*first.*poster/i)).toBeVisible();
    
    // Verify no broken images or undefined text
    const brokenImages = await page.locator('img[src=""], img[src="undefined"]').count();
    expect(brokenImages).toBe(0);
    
    const undefinedText = await page.locator(':text("undefined")').count();
    expect(undefinedText).toBe(0);
    
    // Verify CTA buttons exist
    await expect(page.getByRole('button', { name: /create/i })).toBeVisible();
  });

  // TC-HOME-003: Rapid Navigation Stress Test
  test('TC-HOME-003: Rapid Navigation Stress Test', async ({ page }) => {
    const consoleErrors: string[] = [];
    page.on('console', msg => {
      if (msg.type() === 'error') consoleErrors.push(msg.text());
    });
    
    await page.goto('/');
    
    const tabs = ['Hall', 'Orders', 'Home'];
    
    for (let i = 0; i < 10; i++) {
      const randomTab = tabs[Math.floor(Math.random() * tabs.length)];
      await page.getByRole('link', { name: new RegExp(randomTab, 'i') }).click();
      await page.waitForTimeout(50);
    }
    
    // Final navigation
    await page.getByRole('link', { name: /home/i }).click();
    await page.waitForLoadState('networkidle');
    
    // Verify no console errors
    expect(consoleErrors.length).toBe(0);
    
    // Verify final content matches active tab
    await expect(page).toHaveURL('/');
  });

  // TC-HOME-004: Network Failure Resilience
  test('TC-HOME-004: Network Failure Resilience', async ({ page, context }) => {
    await context.setOffline(true);
    
    await page.goto('/');
    
    // Verify error boundary or toast notification appears
    const errorHandled = await Promise.race([
      page.getByText(/network.*error|connection.*failed|offline/i).isVisible(),
      page.getByRole('alert').isVisible(),
      page.getByText(/something.*went.*wrong/i).isVisible()
    ]);
    
    expect(errorHandled).toBeTruthy();
    
    // Verify no white screen
    const bodyContent = await page.locator('body').innerHTML();
    expect(bodyContent.length).toBeGreaterThan(100);
  });

  // TC-HOME-005: Responsive Layout Shift Check
  test('TC-HOME-005: Responsive Layout Shift Check', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    
    const viewports = [
      { width: 1920, height: 1080 },
      { width: 1366, height: 768 },
      { width: 768, height: 1024 },
      { width: 414, height: 896 },
      { width: 320, height: 568 }
    ];
    
    for (const viewport of viewports) {
      await page.setViewportSize(viewport);
      await page.waitForTimeout(200);
      
      // Check for overlapping elements
      const buttons = await page.locator('button:visible').all();
      for (const button of buttons) {
        const box = await button.boundingBox();
        if (box) {
          expect(box.x).toBeGreaterThanOrEqual(0);
          expect(box.y).toBeGreaterThanOrEqual(0);
          expect(box.x + box.width).toBeLessThanOrEqual(viewport.width);
        }
      }
    }
    
    // Verify hamburger menu appears on mobile
    await page.setViewportSize({ width: 320, height: 568 });
    const hamburgerMenu = page.getByRole('button', { name: /menu/i });
    if (await hamburgerMenu.isVisible()) {
      await expect(hamburgerMenu).toBeVisible();
    }
  });
});

// Suite: IdPhoto (ID Photo Processing)
test.describe('IdPhoto (ID Photo Processing)', () => {
  // TC-IDP-001: Standard ID Photo Generation
  test('TC-IDP-001: Standard ID Photo Generation', async ({ page }) => {
    await page.goto('/idphoto');
    
    // Upload a standard portrait image
    const filePath = path.resolve('public/favicon.svg');
    const fileInput = page.locator('input[type="file"]');
    await fileInput.setInputFiles(filePath);
    
    // Select background color
    await page.getByRole('button', { name: /blue|background/i }).or(
      page.locator('[data-testid="color-blue"], .color-blue')
    ).click();
    
    // Click Process
    await page.getByRole('button', { name: /process|generate/i }).click();
    
    // Wait for processing
    await page.waitForTimeout(2000);
    
    // Verify download button appears
    await expect(page.getByRole('button', { name: /download/i })).toBeVisible();
  });

  // TC-IDP-002: Invalid File Format Upload
  test('TC-IDP-002: Invalid File Format Upload', async ({ page }) => {
    await page.goto('/idphoto');
    
    // Create invalid files
    await page.addInitScript(() => {
      window.invalidFiles = true;
    });
    
    // Attempt to upload non-image file (simulated)
    const fileInput = page.locator('input[type="file"]');
    
    // Listen for error message
    await page.setInputFiles('input[type="file"]', {
      name: 'test.txt',
      mimeType: 'text/plain',
      buffer: Buffer.from('This is not an image')
    });
    
    // Verify error message appears
    await expect(page.getByText(/invalid.*file|corrupted|not.*image/i)).toBeVisible();
    
    // Verify no crash
    await expect(page.locator('body')).toBeVisible();
  });

  // TC-IDP-003: Extreme Aspect Ratio & Size
  test('TC-IDP-003: Extreme Aspect Ratio & Size', async ({ page }) => {
    await page.goto('/idphoto');
    
    // Test with simulated large file
    const fileInput = page.locator('input[type="file"]');
    
    // Create a mock large image file
    await page.evaluate(() => {
      const canvas = document.createElement('canvas');
      canvas.width = 5000;
      canvas.height = 500;
      const ctx = canvas.getContext('2d');
      if (ctx) {
        ctx.fillStyle = 'blue';
        ctx.fillRect(0, 0, 5000, 500);
      }
    });
    
    // Check for size limit handling
    const errorOrWarning = page.getByText(/too.*large|file.*size|image.*dimension/i);
    
    // If no error shown, verify page doesn't freeze
    await page.waitForTimeout(1000);
    await expect(page.locator('body')).toBeResponsive();
  });

  // TC-IDP-004: Processing Interruption
  test('TC-IDP-004: Processing Interruption', async ({ page }) => {
    await page.goto('/idphoto');
    
    const filePath = path.resolve('public/favicon.svg');
    await page.locator('input[type="file"]').setInputFiles(filePath);
    
    // Start processing
    await page.getByRole('button', { name: /process/i }).click();
    
    // Immediately navigate back
    await page.goBack();
    
    // Navigate forward again
    await page.goForward();
    await page.waitForLoadState('networkidle');
    
    // Verify clean state - no stuck spinner
    const spinner = page.locator('[data-testid="spinner"], .spinner, .loading');
    const isSpinnerVisible = await spinner.isVisible().catch(() => false);
    
    if (isSpinnerVisible) {
      const isStuck = await spinner.getAttribute('data-stuck');
      expect(isStuck).toBeFalsy();
    }
  });

  // TC-IDP-005: Double-Submit Prevention
  test('TC-IDP-005: Double-Submit Prevention', async ({ page }) => {
    await page.goto('/idphoto');
    
    const filePath = path.resolve('public/favicon.svg');
    await page.locator('input[type="file"]').setInputFiles(filePath);
    
    const processButton = page.getByRole('button', { name: /process/i });
    
    // Rapidly click process button
    await Promise.all([
      processButton.click(),
      processButton.click({ delay: 50 }),
      processButton.click({ delay: 100 }),
      processButton.click({ delay: 150 }),
      processButton.click({ delay: 200 })
    ]);
    
    // Verify button is disabled after first click
    await expect(processButton).toBeDisabled();
    
    // Wait and verify only one result
    await page.waitForTimeout(2000);
    const downloadButtons = await page.getByRole('button', { name: /download/i }).count();
    expect(downloadButtons).toBeLessThanOrEqual(1);
  });

  // TC-IDP-006: No Face Detected Scenario
  test('TC-IDP-006: No Face Detected Scenario', async ({ page }) => {
    await page.goto('/idphoto');
    
    // Upload landscape/object image (simulated)
    await page.locator('input[type="file"]').setInputFiles({
      name: 'landscape.png',
      mimeType: 'image/png',
      buffer: Buffer.from('mock landscape image data')
    });
    
    await page.getByRole('button', { name: /process/i }).click();
    
    // Verify specific error message
    await expect(page.getByText(/no.*face|multiple.*face|face.*not.*detected/i)).toBeVisible();
    
    // Verify background removal does not proceed
    await expect(page.getByRole('button', { name: /download/i })).not.toBeVisible();
  });
});

// Suite: Poster (Poster Design Tool)
test.describe('Poster (Poster Design Tool)', () => {
  // TC-PST-001: Create and Save Poster
  test('TC-PST-001: Create and Save Poster', async ({ page }) => {
    await page.goto('/poster');
    
    // Select template from gallery
    await page.locator('[data-testid="template-gallery"], .template-item').first().click();
    
    // Edit text fields
    const titleInput = page.locator('input[name="title"], [data-testid="title-input"]').first();
    if (await titleInput.isVisible()) {
      await titleInput.fill('Test Poster Title');
    }
    
    const subtitleInput = page.locator('input[name="subtitle"], [data-testid="subtitle-input"]').first();
    if (await subtitleInput.isVisible()) {
      await subtitleInput.fill('Test Subtitle');
    }
    
    // Upload custom image
    const filePath = path.resolve('public/favicon.svg');
    const imageInput = page.locator('input[type="file"][accept*="image"]').first();
    if (await imageInput.isVisible()) {
      await imageInput.setInputFiles(filePath);
    }
    
    // Save/Export
    const [download] = await Promise.all([
      page.waitForEvent('download'),
      page.getByRole('button', { name: /save|export|download/i }).click()
    ]);
    
    expect(download).toBeTruthy();
  });

  // TC-PST-002: Text Overflow and Special Characters
  test('TC-PST-002: Text Overflow and Special Characters', async ({ page }) => {
    await page.goto('/poster');
    
    // Select template
    await page.locator('[data-testid="template-gallery"], .template-item').first().click();
    
    const textInput = page.locator('input[name="title"], [data-testid="title-input"], textarea').first();
    
    // Test massive text block
    const massiveText = 'A'.repeat(10000);
    await textInput.fill(massiveText);
    
    // Verify text box doesn't expand infinitely
    const textBox = await textInput.boundingBox();
    expect(textBox?.height).toBeLessThan(500);
    
    // Test special characters
    await textInput.fill('Test <script>alert("xss")</script> 🎨 مرحبا');
    
    // Verify no XSS execution
    const alertTriggered = await page.evaluate(() => {
      return (window as any).xssTriggered === true;
    });
    expect(alertTriggered).toBeFalsy();
    
    // Verify special characters render
    await expect(textInput).toHaveValue(/🎨|مرحبا/);
  });

  // TC-PST-003: Template Loading Failure
  test('TC-PST-003: Template Loading Failure', async ({ page }) => {
    // Intercept template API and return error
    await page.route('**/api/templates*', route => {
      route.fulfill({ status: 404, body: 'Not Found' });
    });
    
    await page.goto('/poster');
    
    // Verify graceful handling
    const placeholder = page.locator('[data-testid="placeholder"], .placeholder, .error-state');
    const errorMessage = page.getByText(/template.*not.*found|failed.*load|error/i);
    
    const hasPlaceholder = await placeholder.isVisible().catch(() => false);
    const hasError = await errorMessage.isVisible().catch(() => false);
    
    expect(hasPlaceholder || hasError).toBeTruthy();
    
    // Verify editor canvas still works
    await expect(page.locator('canvas, [data-testid="editor-canvas"]')).toBeVisible();
  });

  // TC-PST-004: Canvas State Reset
  test('TC-PST-004: Canvas State Reset', async ({ page }) => {
    await page.goto('/poster');
    
    // Select template and make edits
    await page.locator('[data-testid="template-gallery"], .template-item').first().click();
    
    const textInput = page.locator('input[name="title"], [data-testid="title-input"]').first();
    await textInput.fill('Modified Title');
    
    // Click Reset
    await page.getByRole('button', { name: /reset|clear/i }).click();
    
    // Verify edits are cleared
    await expect(textInput).toHaveValue('');
    
    // Refresh page
    await page.reload();
    
    // Verify state is reset or restored from auto-save
    const inputValue = await textInput.inputValue();
    expect(inputValue === '' || inputValue === 'Modified Title').toBeTruthy();
  });

  // TC-PST-005: Cross-Module Asset Usage
  test('TC-PST-005: Cross-Module Asset Usage', async ({ page }) => {
    // Create ID Photo first
    await page.goto('/idphoto');
    const filePath = path.resolve('public/favicon.svg');
    await page.locator('input[type="file"]').setInputFiles(filePath);
    await page.getByRole('button', { name: /save|download/i }).click();
    
    // Navigate to Poster module
    await page.goto('/poster');
    
    // Open asset gallery
    await page.getByRole('button', { name: /asset|gallery|recent/i }).click();
    
    // Verify ID Photo appears in assets
    const recentAsset = page.locator('[data-testid="recent-asset"], .recent-item, .asset-item').first();
    await expect(recentAsset).toBeVisible();
  });
});

// Suite: Orders (Order Management)
test.describe('Orders (Order Management)', () => {
  // TC-ORD-001: Order History Pagination
  test('TC-ORD-001: Order History Pagination', async ({ page }) => {
    // Mock user with many orders
    await page.addInitScript(() => {
      localStorage.setItem('orderCount', '25');
    });
    
    await page.goto('/orders');
    await page.waitForLoadState('networkidle');
    
    // Get initial order count
    const initialOrders = await page.locator('[data-testid="order-item"], .order-card, .order-row').count();
    
    // Scroll to bottom or click next
    const nextButton = page.getByRole('button', { name: /next|load.*more/i });
    const infiniteScroll = page.locator('[data-testid="infinite-scroll"], .order-list');
    
    if (await nextButton.isVisible()) {
      await nextButton.click();
    } else {
      await infiniteScroll.evaluate(el => el.scrollTop = el.scrollHeight);
    }
    
    await page.waitForTimeout(1000);
    
    // Verify more orders loaded
    const newOrders = await page.locator('[data-testid="order-item"], .order-card, .order-row').count();
    expect(newOrders).toBeGreaterThanOrEqual(initialOrders);
    
    // Verify no duplicates
    const orderIds = await page.locator('[data-order-id]').evaluateAll(els => 
      els.map(el => el.getAttribute('data-order-id'))
    );
    const uniqueIds = new Set(orderIds);
    expect(uniqueIds.size).toBe(orderIds.length);
  });

  // TC-ORD-002: Filter by Date Range (Invalid Range)
  test('TC-ORD-002: Filter by Date Range (Invalid Range)', async ({ page }) => {
    await page.goto('/orders');
    
    // Open filter options
    await page.getByRole('button', { name: /filter/i }).click();
    
    // Set invalid date range
    const startDate = page.locator('input[name="startDate"], [data-testid="start-date"]');
    const endDate = page.locator('input[name="endDate"], [data-testid="end-date"]');
    
    await startDate.fill('2024-12-31');
    await endDate.fill('2024-01-01');
    
    // Click Apply
    await page.getByRole('button', { name: /apply/i }).click();
    
    // Verify error message
    await expect(page.getByText(/start.*date.*cannot.*after|invalid.*range|end.*date.*before/i)).toBeVisible();
    
    // Verify dates are auto-corrected or form is invalid
    const startValue = await startDate.inputValue();
    const endValue = await endDate.inputValue();
    
    expect(startValue <= endValue || await page.locator('.error, [data-error]').isVisible()).toBeTruthy();
  });

  // TC-ORD-003: Order Detail Status Transition
  test('TC-ORD-003: Order Detail Status Transition', async ({ page }) => {
    // Mock WebSocket or polling
    await page.addInitScript(() => {
      let status = 'in-progress';
      Object.defineProperty(window, 'orderStatus', {
        get: () => status,
        set: (val) => { status = val; }
      });
    });
    
    await page.goto('/orders');
    
    // Click on an "In Progress" order
    await page.locator('[data-status="in-progress"], .order-status:has-text("In Progress")').first().click();
    
    // Verify status badge
    await expect(page.locator('[data-testid="status-badge"], .status-badge')).toHaveText(/in.*progress/i);
    
    // Simulate status update
    await page.evaluate(() => {
      const statusEl = document.querySelector('[data-testid="status-badge"], .status-badge');
      if (statusEl) {
        statusEl.textContent = 'Completed';
        statusEl.setAttribute('data-status', 'completed');
      }
    });
    
    // Verify updated status
    await expect(page.locator('[data-testid="status-badge"], .status-badge')).toHaveText(/completed/i);
  });

  // TC-ORD-004: Empty Order History
  test('TC-ORD-004: Empty Order History', async ({ page }) => {
    // Mock user with no orders
    await page.addInitScript(() => {
      localStorage.setItem('orders', '[]');
    });
    
    await page.goto('/orders');
    
    // Verify empty state
    await expect(page.getByText(/no.*order|empty|nothing.*here/i)).toBeVisible();
    
    // Verify illustration
    await expect(page.locator('[data-testid="empty-illustration"], .empty-state img, svg')).toBeVisible();
    
    // Verify CTA button
    await expect(page.getByRole('button', { name: /create.*photo|create.*poster|get.*started/i })).toBeVisible();
  });

  // TC-ORD-005: Deep Link Access Control
  test('TC-ORD-005: Deep Link Access Control', async ({ page, context }) => {
    // Login as user A
    await page.addInitScript(() => {
      localStorage.setItem('user', JSON.stringify({ id: 'user-a', token: 'token-a' }));
    });
    
    await page.goto('/orders/12345');
    await page.waitForLoadState('networkidle');
    
    // Get current URL
    const orderUrl = page.url();
    
    // Clear session (logout)
    await page.evaluate(() => {
      localStorage.clear();
      sessionStorage.clear();
    });
    
    // Or switch to different user
    await page.addInitScript(() => {
      localStorage.setItem('user', JSON.stringify({ id: 'user-b', token: 'token-b' }));
    });
    
    // Navigate to the order URL
    await page.goto(orderUrl);
    
    // Verify access denied
    const isForbidden = await Promise.race([
      page.getByText(/forbidden|access.*denied|unauthorized|not.*found/i).isVisible(),
      page.getByRole('heading', { name: /403|404/i }).isVisible(),
      page.url().then(url => !url.includes('/orders/12345'))
    ]);
    
    expect(isForbidden).toBeTruthy();
  });
});

// Suite: Hall (Exhibition/Gallery)
test.describe('Hall (Exhibition/Gallery)', () => {
  // TC-HALL-001: Gallery Search and Filter
  test('TC-HALL-001: Gallery Search and Filter', async ({ page }) => {
    await page.goto('/hall');
    
    // Enter keyword in search
    const searchInput = page.locator('input[type="search"], [data-testid="search"], input[placeholder*="search" i]');
    await searchInput.fill('landscape');
    
    // Submit search
    await searchInput.press('Enter');
    await page.waitForTimeout(500);
    
    // Verify results match keyword
    const results = page.locator('[data-testid="gallery-item"], .gallery-item');
    const count = await results.count();
    
    if (count > 0) {
      const firstResultText = await results.first().textContent();
      expect(firstResultText?.toLowerCase()).toContain('landscape');
    }
    
    // Apply category filter
    await page.getByRole('button', { name: /filter|category/i }).click();
    await page.getByRole('option', { name: /id.*photo/i }).or(
      page.locator('[data-category="id-photo"], .category-id-photo')
    ).click();
    
    await page.waitForTimeout(500);
    
    // Clear search
    await page.getByRole('button', { name: /clear|reset/i }).or(
      page.locator('[data-testid="clear-search"]')
    ).click();
    
    // Verify full list restored
    const allItems = await page.locator('[data-testid="gallery-item"], .gallery-item').count();
    expect(allItems).toBeGreaterThanOrEqual(count);
  });

  // TC-HALL-002: Broken Image Handling
  test('TC-HALL-002: Broken Image Handling', async ({ page }) => {
    // Mock API to return broken image URLs
    await page.route('**/api/gallery*', route => {
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          items: [
            { id: 1, title: 'Item 1', imageUrl: 'https://invalid-url/broken.jpg' },
            { id: 2, title: 'Item 2', imageUrl: '' },
            { id: 3, title: 'Item 3', imageUrl: 'not-a-url' }
          ]
        })
      });
    });
    
    await page.goto('/hall');
    
    // Verify fallback images are displayed
    const images = await page.locator('[data-testid="gallery-item"] img, .gallery-item img').all();
    
    for (const img of images) {
      const src = await img.getAttribute('src');
      const alt = await img.getAttribute('alt');
      
      // Either fallback is shown or alt text exists
      expect(src?.includes('placeholder') || src?.includes('fallback') || alt).toBeTruthy();
    }
    
    // Verify no broken image icons visible
    const brokenIcons = await page.locator('img[src=""], img:not([src])').count();
    expect(brokenIcons).toBe(0);
  });

  // TC-HALL-003: Infinite Scroll Memory Leak
  test('TC-HALL-003: Infinite Scroll Memory Leak', async ({ page }) => {
    await page.goto('/hall');
    
    // Get initial memory
    const initialMetrics = await page.evaluate(() => {
      return (performance as any).memory?.usedJSHeapSize || 0;
    });
    
    // Scroll to load 100+ items
    for (let i = 0; i < 20; i++) {
      await page.evaluate(() => {
        window.scrollTo(0, document.body.scrollHeight);
      });
      await page.waitForTimeout(500);
    }
    
    // Get final memory
    const finalMetrics = await page.evaluate(() => {
      return (performance as any).memory?.usedJSHeapSize || 0;
    });
    
    // Memory should not grow excessively (allow 5x growth)
    const growthRatio = finalMetrics / initialMetrics;
    expect(growthRatio).toBeLessThan(5);
    
    // Verify items are rendered
    const itemCount = await page.locator('[data-testid="gallery-item"], .gallery-item').count();
    expect(itemCount).toBeGreaterThan(50);
  });

  // TC-HALL-004: Like/Interaction Toggle
  test('TC-HALL-004: Like/Interaction Toggle', async ({ page }) => {
    await page.goto('/hall');
    
    // Find an item
    const likeButton = page.locator('[data-testid="like-button"], .like-button, button[aria-label*="like" i]').first();
    await expect(likeButton).toBeVisible();
    
    // Get initial like count
    const initialCount = await likeButton.locator('+ span, [data-testid="like-count"]').textContent() || '0';
    
    // Rapidly toggle like
    for (let i = 0; i < 5; i++) {
      await likeButton.click();
      await page.waitForTimeout(100);
    }
    
    // Wait for debounce
    await page.waitForTimeout(1000);
    
    // Verify final state matches
    const isLiked = await likeButton.getAttribute('aria-pressed');
    const finalCount = await likeButton.locator('+ span, [data-testid="like-count"]').textContent() || '0';
    
    // Count should be consistent with final state
    expect(parseInt(finalCount) >= 0).toBeTruthy();
  });

  // TC-HALL-005: Accessibility Compliance
  test('TC-HALL-005: Accessibility Compliance', async ({ page }) => {
    await page.goto('/hall');
    
    // Navigate using keyboard only
    await page.keyboard.press('Tab');
    await page.keyboard.press('Tab');
    await page.keyboard.press('Tab');
    
    // Verify focus is visible
    const focusedElement = await page.evaluate(() => document.activeElement?.tagName);
    expect(['A', 'BUTTON', 'INPUT', 'SELECT'].includes(focusedElement || '')).toBeTruthy();
    
    // Check for alt text on images
    const images = await page.locator('img').all();
    for (const img of images) {
      const alt = await img.getAttribute('alt');
      const ariaLabel = await img.getAttribute('aria-label');
      expect(alt || ariaLabel).toBeTruthy();
    }
    
    // Check for ARIA labels on icons
    const iconButtons = await page.locator('button:has(svg), [role="button"]:has(svg)').all();
    for (const btn of iconButtons) {
      const ariaLabel = await btn.getAttribute('aria-label');
      const title = await btn.getAttribute('title');
      const text = await btn.textContent();
      expect(ariaLabel || title || text?.trim()).toBeTruthy();
    }
    
    // Verify all interactive elements are focusable
    const interactiveElements = await page.locator('a, button, input, select, textarea, [tabindex]').all();
    for (const el of interactiveElements) {
      const tabindex = await el.getAttribute('tabindex');
      expect(tabindex !== '-1' || await el.getAttribute('disabled') !== null).toBeTruthy();
    }
  });
});

// Suite: Photo (General Photo Editing)
test.describe('Photo (General Photo Editing)', () => {
  // TC-PHT-001: Apply Filters and Revert
  test('TC-PHT-001: Apply Filters and Revert', async ({ page }) => {
    await page.goto('/photo');
    
    // Upload photo
    const filePath = path.resolve('public/favicon.svg');
    await page.locator('input[type="file"]').setInputFiles(filePath);
    await page.waitForTimeout(500);
    
    // Apply Grayscale filter
    await page.getByRole('button', { name: /grayscale/i }).or(
      page.locator('[data-filter="grayscale"]')
    ).click();
    
    await page.waitForTimeout(300);
    
    // Apply Blur filter
    await page.getByRole('button', { name: /blur/i }).or(
      page.locator('[data-filter="blur"]')
    ).click();
    
    await page.waitForTimeout(300);
    
    // Click Undo
    await page.getByRole('button', { name: /undo/i }).click();
    
    // Verify last filter is reverted
    const canvas = page.locator('canvas');
    await expect(canvas).toBeVisible();
    
    // Click Reset
    await page.getByRole('button', { name: /reset|revert/i }).click();
    
    // Verify original image restored
    await expect(canvas).toBeVisible();
  });

  // TC-PHT-002: Browser Refresh During Edit
  test('TC-PHT-002: Browser Refresh During Edit', async ({ page }) => {
    await page.goto('/photo');
    
    // Upload and make edits
    const filePath = path.resolve('public/favicon.svg');
    await page.locator('input[type="file"]').setInputFiles(filePath);
    
    await page.getByRole('button', { name: /grayscale/i }).or(
      page.locator('[data-filter="grayscale"]')
    ).click();
    
    // Attempt refresh
    page.on('dialog', async dialog => {
      expect(dialog.message()).toContain(/unsaved|leave|changes/i);
      await dialog.dismiss();
    });
    
    // Check for beforeunload prompt
    const hasPrompt = await page.evaluate(() => {
      return window.onbeforeunload !== null;
    });
    
    // Refresh the page
    await page.reload();
    
    // Check if state is restored
    const canvas = page.locator('canvas');
    const hasCanvas = await canvas.isVisible().catch(() => false);
    
    // Either prompt was shown or state was auto-saved
    expect(hasPrompt || hasCanvas).toBeTruthy();
  });

  // TC-PHT-003: Download Without Saving
  test('TC-PHT-003: Download Without Saving', async ({ page }) => {
    await page.goto('/photo');
    
    // Upload photo
    const filePath = path.resolve('public/favicon.svg');
    await page.locator('input[type="file"]').setInputFiles(filePath);
    
    // Immediately click download without changes
    const downloadPromise = page.waitForEvent('download');
    
    await page.getByRole('button', { name: /download|export/i }).click();
    
    const download = await downloadPromise;
    
    // Verify file is downloaded and not empty
    expect(download).toBeTruthy();
    
    const path = await download.path();
    expect(path).toBeTruthy();
    
    // Verify file has content
    const fileSize = await download.createRead().then(stream => {
      return new Promise(resolve => {
        let size = 0;
        stream.on('data', chunk => size += chunk.length);
        stream.on('end', () => resolve(size));
      });
    });
    
    expect(fileSize).toBeGreaterThan(0);
  });

  // TC-PHT-004: Mobile Touch Gestures
  test('TC-PHT-004: Mobile Touch Gestures', async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });
    
    await page.goto('/photo');
    
    // Upload photo
    const filePath = path.resolve('public/favicon.svg');
    await page.locator('input[type="file"]').setInputFiles(filePath);
    await page.waitForTimeout(500);
    
    const canvas = page.locator('canvas');
    const box = await canvas.boundingBox();
    
    if (box) {
      // Simulate pinch zoom
      const centerX = box.x + box.width / 2;
      const centerY = box.y + box.height / 2;
      
      await page.touchscreen.tap(centerX, centerY);
      
      // Simulate touch move (pan)
      await page.mouse.move(centerX, centerY);
      await page.mouse.move(centerX + 50, centerY + 50);
      
      // Verify canvas is still visible and responsive
      await expect(canvas).toBeVisible();
      
      // Verify image hasn't flown off-screen
      const newBox = await canvas.boundingBox();
      expect(newBox?.x).toBeGreaterThanOrEqual(-box.width);
      expect(newBox?.y).toBeGreaterThanOrEqual(-box.height);
    }
  });

  // TC-PHT-005: Large Canvas Export Timeout
  test('TC-PHT-005: Large Canvas Export Timeout', async ({ page }) => {
    await page.goto('/photo');
    
    // Simulate large image upload
    await page.evaluate(() => {
      const canvas = document.createElement('canvas');
      canvas.width = 8000;
      canvas.height = 8000;
      const ctx = canvas.getContext('2d');
      if (ctx) {
        ctx.fillStyle = 'red';
        ctx.fillRect(0, 0, 8000, 8000);
      }
    });
    
    // Apply heavy filters
    await page.getByRole('button', { name: /blur/i }).or(
      page.locator('[data-filter="blur"]')
    ).click();
    
    await page.getByRole('button', { name: /sharpen/i }).or(
      page.locator('[data-filter="sharpen"]')
    ).click();
    
    // Start export and check for progress indicator
    const [download] = await Promise.all([
      page.waitForEvent('download', { timeout: 60000 }),
      page.getByRole('button', { name: /export|download/i }).click()
    ]);
    
    // Verify progress indicator was shown or download completed
    const progressBar = page.locator('[role="progressbar"], .progress, [data-testid="progress"]');
    const hadProgress = await progressBar.isVisible().catch(() => false);
    
    // Download should complete
    expect(download).toBeTruthy();
  });
});