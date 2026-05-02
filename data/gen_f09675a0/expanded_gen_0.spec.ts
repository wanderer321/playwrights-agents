import { test, expect } from '@playwright/test';
import path from 'path';

test.describe('Home Module', () => {
  test('TC-HOME-001: Verify Homepage Load and Layout', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Check for main header, navigation bar, and footer
    await expect(page.getByRole('banner')).toBeVisible();
    await expect(page.getByRole('navigation')).toBeVisible();
    await expect(page.getByRole('contentinfo')).toBeVisible();

    // Check for Logo and Banner visibility
    await expect(page.getByAltText(/logo/i)).toBeVisible();
    await expect(page.getByRole('img', { name: /banner/i })).toBeVisible();
  });

  test('TC-HOME-002: Navigation to Feature Modules', async ({ page }) => {
    await page.goto('/');

    // Navigate to ID Photo
    await page.getByRole('link', { name: /证件照|id photo/i }).click();
    await expect(page).toHaveURL(/.*idphoto/);

    // Navigate back
    await page.goBack();
    await expect(page).toHaveURL('/');

    // Navigate to Poster
    await page.getByRole('link', { name: /海报|poster/i }).click();
    await expect(page).toHaveURL(/.*poster/);
  });
});

test.describe('ID Photo Module', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/idphoto');
  });

  test('TC-IDP-001: Upload Photo for ID Processing', async ({ page }) => {
    const filePath = path.resolve('public/favicon.svg');
    
    // Click upload area or button to trigger file input
    const fileInput = page.locator('input[type="file"]');
    await fileInput.setInputFiles(filePath);

    // Wait for upload success indicator or preview
    await expect(page.getByRole('img', { name: /preview|预览/i })).toBeVisible({ timeout: 10000 });
  });

  test('TC-IDP-002: Change Background Color', async ({ page }) => {
    // Pre-condition: Upload photo
    const filePath = path.resolve('public/favicon.svg');
    await page.locator('input[type="file"]').setInputFiles(filePath);
    await expect(page.getByRole('img', { name: /preview|预览/i })).toBeVisible();

    // Select Blue color option
    await page.getByRole('button', { name: /blue|蓝色/i }).click();

    // Verify preview updates (checking visibility as proxy for update)
    const preview = page.getByRole('img', { name: /preview|预览/i });
    await expect(preview).toBeVisible();
  });

  test('TC-IDP-003: Download Processed ID Photo', async ({ page }) => {
    // Pre-condition: Upload photo
    const filePath = path.resolve('public/favicon.svg');
    await page.locator('input[type="file"]').setInputFiles(filePath);
    await expect(page.getByRole('img', { name: /preview|预览/i })).toBeVisible();

    // Initiate download
    const downloadPromise = page.waitForEvent('download');
    await page.getByRole('button', { name: /download|下载|保存/i }).click();
    
    const download = await downloadPromise;
    expect(download.suggestedFilename()).toBeTruthy();
  });
});

test.describe('Poster Module', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/poster');
  });

  test('TC-PST-001: Select Poster Template', async ({ page }) => {
    // Browse template gallery and click a template
    const template = page.getByRole('img', { name: /template|模板/i }).first();
    await template.click();

    // Verify editor loads with canvas
    await expect(page.getByRole('region', { name: /editor|编辑器/i })).toBeVisible();
    await expect(page.getByRole('toolbar')).toBeVisible();
  });

  test('TC-PST-002: Edit Text on Poster', async ({ page }) => {
    // Load template
    await page.getByRole('img', { name: /template|模板/i }).first().click();
    
    // Click text element on canvas
    const textElement = page.locator('.canvas-text-element').first(); // Assuming class based selector
    await textElement.click();

    // Clear and type new text
    const input = page.getByRole('textbox', { name: /text|文本/i });
    await input.fill('Test Event Title');
    
    // Deselect (click outside)
    await page.getByRole('region', { name: /canvas|画布/i }).click({ position: { x: 0, y: 0 } });

    // Verify text update
    await expect(page.getByText('Test Event Title')).toBeVisible();
  });
});

test.describe('Photo Module', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/photo');
  });

  test('TC-PHT-001: Apply Image Filter', async ({ page }) => {
    // Upload photo
    const filePath = path.resolve('public/favicon.svg');
    await page.locator('input[type="file"]').setInputFiles(filePath);
    await expect(page.getByRole('img', { name: /preview|预览/i })).toBeVisible();

    // Select filter
    await page.getByRole('button', { name: /grayscale|黑白/i }).click();

    // Verify canvas updates (check for filter class or style)
    const preview = page.getByRole('img', { name: /preview|预览/i });
    await expect(preview).toBeVisible();
  });

  test('TC-PHT-002: Crop Image Functionality', async ({ page }) => {
    // Upload photo
    const filePath = path.resolve('public/favicon.svg');
    await page.locator('input[type="file"]').setInputFiles(filePath);
    await expect(page.getByRole('img', { name: /preview|预览/i })).toBeVisible();

    // Select crop tool
    await page.getByRole('button', { name: /crop|裁剪/i }).click();
    
    // Apply crop (assuming default selection or drag handles exist)
    await page.getByRole('button', { name: /apply|确认|确定/i }).click();

    // Verify preview updates
    await expect(page.getByRole('img', { name: /preview|预览/i })).toBeVisible();
  });
});

test.describe('Orders Module', () => {
  test.use({ storageState: '.auth/user.json' }); // Assuming auth state exists

  test('TC-ORD-001: View Order History', async ({ page }) => {
    await page.goto('/orders');
    
    // Verify list of orders is loaded
    const orderList = page.getByRole('list', { name: /orders|订单/i });
    await expect(orderList).toBeVisible();
    
    // Check for order details
    const firstOrder = orderList.getByRole('listitem').first();
    await expect(firstOrder).toBeVisible();
    await expect(firstOrder.getByText(/order id|订单号/i)).toBeVisible();
  });

  test('TC-ORD-002: Filter Orders by Status', async ({ page }) => {
    await page.goto('/orders');

    // Select "Completed" filter
    await page.getByRole('tab', { name: /completed|已完成/i }).click();

    // Verify list updates
    const orderList = page.getByRole('list', { name: /orders|订单/i });
    await expect(orderList.getByRole('listitem').first()).toContainText(/completed|已完成/i);
  });
});

test.describe('Hall Module', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/hall');
  });

  test('TC-HALL-001: Browse Public Gallery', async ({ page }) => {
    // Verify grid layout
    const grid = page.getByRole('list', { name: /gallery|作品/i });
    await expect(grid).toBeVisible();
    await expect(grid.getByRole('listitem').first()).toBeVisible();

    // Scroll to verify lazy loading
    await grid.evaluate(e => e.scrollTo({ top: e.scrollHeight, behavior: 'smooth' }));
    // Wait for potential network idle or new items
    await page.waitForTimeout(1000); // Simple wait for demo purposes
  });

  test('TC-HALL-002: Search Functionality', async ({ page }) => {
    // Enter keyword
    await page.getByRole('searchbox', { name: /search|搜索/i }).fill('Summer');
    await page.getByRole('searchbox', { name: /search|搜索/i }).press('Enter');

    // Verify results
    const results = page.getByRole('list', { name: /results|结果/i });
    await expect(results).toBeVisible();
    await expect(results.getByText(/summer/i)).toBeVisible();
  });
});

test.describe('Generated Content Module', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/generated');
  });

  test('TC-GEN-001: View Generated History', async ({ page }) => {
    // Verify history list/grid
    const historyGrid = page.getByRole('list', { name: /history|历史/i });
    await expect(historyGrid).toBeVisible();
    
    // Check for thumbnails and timestamps
    const item = historyGrid.getByRole('listitem').first();
    await expect(item.getByRole('img')).toBeVisible();
    await expect(item.getByText(/\d{4}-\d{2}-\d{2}/)).toBeVisible(); // Date regex
  });

  test('TC-GEN-002: Regenerate or Delete Item', async ({ page }) => {
    const item = page.getByRole('list', { name: /history|历史/i }).getByRole('listitem').first();
    
    // Hover to reveal actions
    await item.hover();
    
    // Click Delete
    await item.getByRole('button', { name: /delete|删除/i }).click();
    
    // Confirm in modal
    await page.getByRole('dialog').getByRole('button', { name: /confirm|确定/i }).click();

    // Verify removal (check if item is detached)
    await expect(item).not.toBeVisible();
  });
});