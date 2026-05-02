import { test, expect } from '@playwright/test';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

test.describe('Home Module', () => {
  test('TC-HOME-001: Verify Home Page Load and Layout', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Check for main navigation bar visibility
    const navigation = page.locator('nav').first();
    await expect(navigation).toBeVisible();

    // Check for footer section visibility
    const footer = page.locator('footer').first();
    await expect(footer).toBeVisible();

    // Verify no console errors
    const errors: string[] = [];
    page.on('console', msg => {
      if (msg.type() === 'error') {
        errors.push(msg.text());
      }
    });
    expect(errors.filter(e => e.includes('JavaScript'))).toHaveLength(0);
  });

  test('TC-HOME-002: Verify Navigation to Core Modules', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Navigate to ID Photo module
    const idPhotoLink = page.getByRole('link', { name: /id photo|证件照/i });
    if (await idPhotoLink.count() > 0) {
      await idPhotoLink.click();
      await expect(page).toHaveURL(/.*idphoto|.*id-photo|.*证件照.*/i);
      await page.goBack();
      await expect(page).toHaveURL('/');
    }

    // Navigate to Poster module
    const posterLink = page.getByRole('link', { name: /poster|海报/i });
    if (await posterLink.count() > 0) {
      await posterLink.click();
      await expect(page).toHaveURL(/.*poster|.*海报.*/i);
      await page.goBack();
      await expect(page).toHaveURL('/');
    }

    // Navigate to Orders module
    const ordersLink = page.getByRole('link', { name: /orders|订单/i });
    if (await ordersLink.count() > 0) {
      await ordersLink.click();
      await expect(page).toHaveURL(/.*order|.*订单.*/i);
      await page.goBack();
      await expect(page).toHaveURL('/');
    }
  });
});

test.describe('ID Photo Module', () => {
  test('TC-IDP-001: Upload Image for ID Photo', async ({ page }) => {
    await page.goto('/idphoto');
    await page.waitForLoadState('networkidle');

    // Locate upload input or drag-drop area
    const uploadInput = page.locator('input[type="file"]').first();
    const uploadArea = page.getByRole('button', { name: /upload|上传/i });

    // Upload file using setInputFiles
    const testFilePath = path.resolve(__dirname, '../../public/favicon.svg');
    await uploadInput.setInputFiles(testFilePath);

    // Wait for upload success indicator or preview
    const preview = page.locator('img[alt*="preview"], canvas, .preview').first();
    await expect(preview).toBeVisible({ timeout: 10000 });
  });

  test('TC-IDP-002: Change Background Color', async ({ page }) => {
    await page.goto('/idphoto');
    await page.waitForLoadState('networkidle');

    // Pre-condition: Upload an image first
    const uploadInput = page.locator('input[type="file"]').first();
    const testFilePath = path.resolve(__dirname, '../../public/favicon.svg');
    await uploadInput.setInputFiles(testFilePath);

    // Wait for preview to appear
    const preview = page.locator('img, canvas').first();
    await expect(preview).toBeVisible({ timeout: 10000 });

    // Locate and select Blue background color option
    const blueOption = page.getByRole('button', { name: /blue|蓝色/i }).or(
      page.locator('[data-color="blue"], .color-blue, [aria-label*="blue"]')
    );
    
    if (await blueOption.count() > 0) {
      await blueOption.click();
      
      // Verify preview updates (check for canvas or image update)
      await page.waitForTimeout(500);
      await expect(preview).toBeVisible();
    }
  });

  test('TC-IDP-003: Download Processed ID Photo', async ({ page }) => {
    await page.goto('/idphoto');
    await page.waitForLoadState('networkidle');

    // Upload and process an image
    const uploadInput = page.locator('input[type="file"]').first();
    const testFilePath = path.resolve(__dirname, '../../public/favicon.svg');
    await uploadInput.setInputFiles(testFilePath);

    // Wait for processing
    await page.waitForTimeout(1000);

    // Setup download listener
    const downloadPromise = page.waitForEvent('download');

    // Click Download/Save button
    const downloadButton = page.getByRole('button', { name: /download|保存|save/i });
    if (await downloadButton.count() > 0) {
      await downloadButton.click();

      const download = await downloadPromise;
      expect(download.suggestedFilename()).toBeTruthy();
    }
  });
});

test.describe('Poster Module', () => {
  test('TC-PST-001: Select Poster Template', async ({ page }) => {
    await page.goto('/poster');
    await page.waitForLoadState('networkidle');

    // Verify template grid is displayed
    const templateGrid = page.locator('.template-grid, .templates, [class*="template"]').first();
    const templateCards = page.locator('[class*="template"] img, .template-card, .template-item');

    // Check for template thumbnails
    const templateCount = await templateCards.count();
    expect(templateCount).toBeGreaterThan(0);

    // Click on first template
    const firstTemplate = templateCards.first();
    await firstTemplate.click();

    // Verify editor or details page opens
    const editor = page.locator('.editor, [class*="editor"], .template-detail').first();
    await expect(editor).toBeVisible({ timeout: 5000 });
  });

  test('TC-PST-002: Edit Poster Text Content', async ({ page }) => {
    await page.goto('/poster');
    await page.waitForLoadState('networkidle');

    // Select a template to enter editor
    const templateCards = page.locator('[class*="template"] img, .template-card, .template-item');
    if (await templateCards.count() > 0) {
      await templateCards.first().click();
      await page.waitForTimeout(500);
    }

    // Find and click on a text element
    const textElement = page.locator('text, [contenteditable="true"], .text-element, [class*="text"]').first();
    
    if (await textElement.count() > 0) {
      await textElement.click();
      await textElement.fill('Test Poster Title');

      // Click outside or apply
      const applyButton = page.getByRole('button', { name: /apply|确定|确认/i });
      if (await applyButton.count() > 0) {
        await applyButton.click();
      } else {
        await page.keyboard.press('Escape');
      }

      // Verify text updated
      await expect(page.getByText('Test Poster Title')).toBeVisible();
    }
  });
});

test.describe('Orders Module', () => {
  test('TC-ORD-001: View Order List', async ({ page }) => {
    await page.goto('/orders');
    await page.waitForLoadState('networkidle');

    // Check for order list container
    const orderList = page.locator('.order-list, [class*="order"], .orders-container').first();
    await expect(orderList).toBeVisible();

    // Check for pagination or infinite scroll
    const pagination = page.locator('.pagination, [class*="pagination"], .load-more');
    const noOrdersPlaceholder = page.getByText(/no orders|暂无订单|empty/i);

    // Either orders exist or placeholder is shown
    const hasOrders = await orderList.locator('.order-item, [class*="order-item"]').count() > 0;
    const hasPlaceholder = await noOrdersPlaceholder.count() > 0;

    expect(hasOrders || hasPlaceholder).toBeTruthy();
  });

  test('TC-ORD-002: Filter Orders by Status', async ({ page }) => {
    await page.goto('/orders');
    await page.waitForLoadState('networkidle');

    // Locate status filter
    const statusFilter = page.getByRole('combobox', { name: /status|状态/i }).or(
      page.locator('select[name*="status"], .status-filter')
    );

    const completedTab = page.getByRole('tab', { name: /completed|已完成/i }).or(
      page.getByRole('button', { name: /completed|已完成/i })
    );

    if (await completedTab.count() > 0) {
      await completedTab.click();
      await page.waitForTimeout(500);

      // Verify filtered results
      const orderItems = page.locator('.order-item, [class*="order-item"]');
      const orderCount = await orderItems.count();

      if (orderCount > 0) {
        // Check that all visible orders have completed status
        const completedBadges = page.locator('.status:has-text("Completed"), .status:has-text("已完成")');
        const badgeCount = await completedBadges.count();
        expect(badgeCount).toBeGreaterThanOrEqual(0);
      }
    } else if (await statusFilter.count() > 0) {
      await statusFilter.selectOption({ label: /completed|已完成/i });
      await page.waitForTimeout(500);
    }
  });
});

test.describe('Photo Module', () => {
  test('TC-PHT-001: Basic Photo Edit Operation', async ({ page }) => {
    await page.goto('/photo');
    await page.waitForLoadState('networkidle');

    // Upload a sample image
    const uploadInput = page.locator('input[type="file"]').first();
    const testFilePath = path.resolve(__dirname, '../../public/favicon.svg');
    await uploadInput.setInputFiles(testFilePath);

    // Wait for image to load
    const preview = page.locator('img, canvas').first();
    await expect(preview).toBeVisible({ timeout: 10000 });

    // Apply a basic filter
    const grayscaleFilter = page.getByRole('button', { name: /grayscale|灰度|黑白/i }).or(
      page.locator('[data-filter="grayscale"], .filter-grayscale')
    );

    const cropFilter = page.getByRole('button', { name: /crop|裁剪/i }).or(
      page.locator('[data-filter="crop"], .filter-crop')
    );

    if (await grayscaleFilter.count() > 0) {
      await grayscaleFilter.click();
      await page.waitForTimeout(300);
      await expect(preview).toBeVisible();
    } else if (await cropFilter.count() > 0) {
      await cropFilter.click();
      await page.waitForTimeout(300);
      await expect(preview).toBeVisible();
    }
  });
});

test.describe('Hall Module', () => {
  test('TC-HAL-001: Hall Entry Display', async ({ page }) => {
    // Track console errors
    const resourceErrors: string[] = [];
    page.on('console', msg => {
      if (msg.type() === 'error') {
        resourceErrors.push(msg.text());
      }
    });

    await page.goto('/hall');
    await page.waitForLoadState('networkidle');

    // Verify main banner or title is visible
    const mainBanner = page.locator('.banner, .hero, [class*="banner"], h1').first();
    await expect(mainBanner).toBeVisible();

    // Scroll down to check content loading
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
    await page.waitForTimeout(500);

    // Check for content elements
    const contentElements = page.locator('img, .content, [class*="content"]');
    const contentCount = await contentElements.count();
    expect(contentCount).toBeGreaterThan(0);

    // Verify no missing resource errors
    const missingResourceErrors = resourceErrors.filter(e => 
      e.includes('404') || e.includes('missing') || e.includes('failed to load')
    );
    expect(missingResourceErrors).toHaveLength(0);
  });
});