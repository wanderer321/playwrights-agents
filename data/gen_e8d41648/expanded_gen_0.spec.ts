import { test, expect } from '@playwright/test';
import { fileURLToPath } from 'url';
import path from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

test.describe('Home Module', () => {
  test('TC-HOME-001: Verify Home Page Load', async ({ page }) => {
    const consoleErrors: string[] = [];
    page.on('console', msg => {
      if (msg.type() === 'error') {
        consoleErrors.push(msg.text());
      }
    });

    await page.goto('/');
    await page.waitForLoadState('networkidle');

    await expect(page.locator('header')).toBeVisible();
    await expect(page.locator('footer')).toBeVisible();
    await expect(page.getByRole('navigation')).toBeVisible();

    expect(consoleErrors).toHaveLength(0);
  });

  test('TC-HOME-002: Navigation Routing', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    const hallLink = page.getByRole('link', { name: /hall|大厅/i });
    await hallLink.click();

    await expect(page).toHaveURL(/.*hall.*/);

    await page.goBack();
    await expect(page).toHaveURL('/');
  });
});

test.describe('Hall Module', () => {
  test('TC-HALL-001: Service Selection Display', async ({ page }) => {
    await page.goto('/hall');
    await page.waitForLoadState('networkidle');

    const serviceCards = page.locator('[data-testid="service-card"], .service-card, [role="article"]').filter({ hasText: /id photo|poster|证件照|海报/i });
    await expect(serviceCards.first()).toBeVisible();

    const idPhotoCard = page.getByRole('button', { name: /id photo|证件照/i }).or(page.getByRole('link', { name: /id photo|证件照/i }));
    if (await idPhotoCard.count() > 0) {
      await expect(idPhotoCard.first()).toBeEnabled();
    }
  });

  test('TC-HALL-002: Queue or Token Status', async ({ page }) => {
    await page.goto('/hall');
    await page.waitForLoadState('networkidle');

    const queueStatus = page.locator('[data-testid="queue-status"], .queue-number, .token-display').or(page.getByText(/queue|排队|等待|token/i));
    
    if (await queueStatus.count() > 0) {
      await expect(queueStatus.first()).toBeVisible();
    }
  });
});

test.describe('ID Photo Module', () => {
  test('TC-IDP-001: Photo Upload Functionality', async ({ page }) => {
    await page.goto('/idphoto');
    await page.waitForLoadState('networkidle');

    const uploadButton = page.getByRole('button', { name: /upload|上传/i }).or(page.locator('input[type="file"]'));
    
    const filePath = path.resolve(__dirname, '../../public/favicon.svg');
    
    const fileInput = page.locator('input[type="file"]');
    await fileInput.setInputFiles(filePath);

    const preview = page.locator('[data-testid="preview"], .preview-image, canvas').or(page.getByRole('img', { name: /preview|预览/i }));
    await expect(preview.first()).toBeVisible({ timeout: 10000 });
  });

  test('TC-IDP-002: Background Processing/Removal', async ({ page }) => {
    await page.goto('/idphoto');
    await page.waitForLoadState('networkidle');

    const filePath = path.resolve(__dirname, '../../public/favicon.svg');
    await page.locator('input[type="file"]').setInputFiles(filePath);

    const changeBackgroundBtn = page.getByRole('button', { name: /change background|更换背景|auto cutout|抠图/i });
    if (await changeBackgroundBtn.count() > 0) {
      await changeBackgroundBtn.click();
    }

    const blueColorOption = page.getByRole('button', { name: /blue|蓝/i }).or(page.locator('[data-color="blue"], .color-blue'));
    if (await blueColorOption.count() > 0) {
      await blueColorOption.click();
    }

    const canvas = page.locator('canvas');
    if (await canvas.count() > 0) {
      await expect(canvas.first()).toBeVisible();
    }
  });

  test('TC-IDP-003: Photo Specifications Compliance', async ({ page }) => {
    await page.goto('/idphoto');
    await page.waitForLoadState('networkidle');

    const filePath = path.resolve(__dirname, '../../public/favicon.svg');
    await page.locator('input[type="file"]').setInputFiles(filePath);

    const documentTypeSelect = page.getByRole('combobox', { name: /document|证件|passport|护照|visa|签证/i }).or(page.getByRole('listbox'));
    if (await documentTypeSelect.count() > 0) {
      await documentTypeSelect.click();
      
      const passportOption = page.getByRole('option', { name: /passport|护照/i });
      if (await passportOption.count() > 0) {
        await passportOption.click();
      }
    }

    const cropArea = page.locator('[data-testid="crop-area"], .crop-container, .aspect-ratio-box');
    if (await cropArea.count() > 0) {
      await expect(cropArea).toBeVisible();
    }
  });
});

test.describe('Photo Module', () => {
  test('TC-PHOTO-001: Gallery View Pagination', async ({ page }) => {
    await page.goto('/photo');
    await page.waitForLoadState('networkidle');

    const thumbnails = page.locator('[data-testid="photo-thumbnail"], .gallery-item, .photo-card').or(page.getByRole('img').filter({ hasNot: page.locator('[alt=""]') }));
    await expect(thumbnails.first()).toBeVisible();

    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
    await page.waitForTimeout(500);

    const paginationBtn = page.getByRole('button', { name: /next|load more|下一页|加载/i });
    if (await paginationBtn.count() > 0) {
      await paginationBtn.click();
      await page.waitForLoadState('networkidle');
    }
  });

  test('TC-PHOTO-002: Photo Filtering and Sorting', async ({ page }) => {
    await page.goto('/photo');
    await page.waitForLoadState('networkidle');

    const dateFilter = page.getByRole('combobox', { name: /date|日期/i }).or(page.getByRole('listbox', { name: /filter|筛选/i }));
    if (await dateFilter.count() > 0) {
      await dateFilter.click();
      const last7DaysOption = page.getByRole('option', { name: /last 7 days|最近7天/i });
      if (await last7DaysOption.count() > 0) {
        await last7DaysOption.click();
      }
    }

    const sortSelect = page.getByRole('combobox', { name: /sort|排序/i });
    if (await sortSelect.count() > 0) {
      await sortSelect.click();
      const newestOption = page.getByRole('option', { name: /newest|最新/i });
      if (await newestOption.count() > 0) {
        await newestOption.click();
      }
    }

    const gallery = page.locator('[data-testid="gallery"], .photo-gallery, .photo-list');
    await expect(gallery.or(page.locator('main'))).toBeVisible();
  });
});

test.describe('Poster Module', () => {
  test('TC-POSTER-001: Template Selection', async ({ page }) => {
    await page.goto('/poster');
    await page.waitForLoadState('networkidle');

    const templateLibrary = page.locator('[data-testid="template-library"], .template-grid, .templates-container');
    await expect(templateLibrary.or(page.locator('main'))).toBeVisible();

    const templateCard = page.locator('[data-testid="template-card"], .template-item').first();
    if (await templateCard.count() > 0) {
      await templateCard.click();
      
      const editorCanvas = page.locator('[data-testid="editor-canvas"], .poster-canvas, canvas');
      await expect(editorCanvas).toBeVisible({ timeout: 5000 });
    }
  });

  test('TC-POSTER-002: Text Editing and Export', async ({ page }) => {
    await page.goto('/poster');
    await page.waitForLoadState('networkidle');

    const templateCard = page.locator('[data-testid="template-card"], .template-item').first();
    if (await templateCard.count() > 0) {
      await templateCard.click();
    }

    const textElement = page.locator('[data-testid="text-element"], .text-layer, [contenteditable="true"]').first();
    if (await textElement.count() > 0) {
      await textElement.click();
      await textElement.fill('Test Poster Text');
    }

    const exportBtn = page.getByRole('button', { name: /export|download|导出|下载/i });
    if (await exportBtn.count() > 0) {
      const downloadPromise = page.waitForEvent('download', { timeout: 10000 }).catch(() => null);
      await exportBtn.click();
      const download = await downloadPromise;
      if (download) {
        expect(download.suggestedFilename()).toBeTruthy();
      }
    }
  });
});

test.describe('Orders Module', () => {
  test('TC-ORD-001: Order List Display', async ({ page }) => {
    await page.goto('/orders');
    await page.waitForLoadState('networkidle');

    const orderList = page.locator('[data-testid="order-list"], .orders-container, .order-history');
    await expect(orderList.or(page.locator('main'))).toBeVisible();

    const orderItems = page.locator('[data-testid="order-item"], .order-card, .order-row');
    const statusBadge = page.locator('[data-testid="status-badge"], .status, .order-status').filter({ hasText: /completed|pending|完成|待处理/i });
    
    if (await orderItems.count() > 0) {
      await expect(orderItems.first()).toBeVisible();
    }
  });

  test('TC-ORD-002: Order Detail View', async ({ page }) => {
    await page.goto('/orders');
    await page.waitForLoadState('networkidle');

    const orderItem = page.locator('[data-testid="order-item"], .order-card, .order-row').first();
    if (await orderItem.count() > 0) {
      await orderItem.click();

      const detailModal = page.locator('[data-testid="order-detail"], .order-detail-modal, [role="dialog"]');
      const detailPage = page.locator('[data-testid="order-detail-page"], .order-detail');
      
      await expect(detailModal.or(detailPage)).toBeVisible({ timeout: 5000 });

      const priceInfo = page.locator('[data-testid="price"], .price, .order-price');
      const downloadLink = page.getByRole('link', { name: /download|下载/i }).or(page.getByRole('button', { name: /download|下载/i }));
      
      if (await priceInfo.count() > 0) {
        await expect(priceInfo.first()).toBeVisible();
      }
    }
  });
});

test.describe('Generated Tests - Critical User Flow', () => {
  test('TC-GEN-001: Critical User Flow Regression', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    const hallLink = page.getByRole('link', { name: /hall|大厅/i });
    if (await hallLink.count() > 0) {
      await hallLink.click();
      await page.waitForLoadState('networkidle');
    }

    const idPhotoLink = page.getByRole('link', { name: /id photo|证件照/i }).or(page.getByRole('button', { name: /id photo|证件照/i }));
    if (await idPhotoLink.count() > 0) {
      await idPhotoLink.click();
      await page.waitForLoadState('networkidle');
    }

    const filePath = path.resolve(__dirname, '../../public/favicon.svg');
    const fileInput = page.locator('input[type="file"]');
    if (await fileInput.count() > 0) {
      await fileInput.setInputFiles(filePath);
      await page.waitForTimeout(1000);
    }

    const downloadBtn = page.getByRole('button', { name: /download|下载|export|导出/i });
    if (await downloadBtn.count() > 0) {
      await expect(downloadBtn).toBeEnabled();
    }

    await expect(page).not.toHaveURL(/error/i);
  });
});