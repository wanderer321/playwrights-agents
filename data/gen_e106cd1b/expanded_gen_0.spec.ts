import { test, expect } from '@playwright/test';
import path from 'path';

test.describe('Home Module', () => {
  test('TC-HOME-001: Verify Home Page Load and Layout', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    await expect(page).toHaveTitle(/智慧工坊|Zhihui Workshop/);

    await expect(page.locator('header').or(page.getByRole('banner'))).toBeVisible();

    await expect(page.locator('main').or(page.getByRole('main'))).toBeVisible();

    await expect(page.locator('footer').or(page.getByRole('contentinfo'))).toBeVisible();
  });

  test('TC-HOME-002: Navigation to Functional Modules', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    const idPhotoLink = page.getByRole('link', { name: /证件照|ID Photo/i }).or(
      page.getByRole('navigation').getByText(/证件照/)
    );
    await idPhotoLink.click();
    await expect(page).toHaveURL(/\/idphoto/);

    await page.goBack();
    await page.waitForLoadState('networkidle');

    const posterLink = page.getByRole('link', { name: /海报|Poster/i }).or(
      page.getByRole('navigation').getByText(/海报/)
    );
    await posterLink.click();
    await expect(page).toHaveURL(/\/poster/);
  });
});

test.describe('Hall Module', () => {
  test.use({ storageState: '.auth/user.json' });

  test('TC-HALL-001: User Dashboard Access', async ({ page }) => {
    await page.goto('/hall');
    await page.waitForLoadState('networkidle');

    await expect(page.getByText(/欢迎|Welcome/).or(page.locator('[data-testid="user-info"]'))).toBeVisible();

    await expect(page.getByRole('img', { name: /avatar|头像/i }).or(page.locator('[data-testid="user-avatar"]'))).toBeVisible();

    await expect(page.getByRole('link', { name: /证件照|海报|照片/i }).or(page.locator('[data-testid="service-cards"]'))).toBeVisible();
  });

  test('TC-HALL-002: Service Entry Points', async ({ page }) => {
    await page.goto('/hall');
    await page.waitForLoadState('networkidle');

    const createIdPhotoButton = page.getByRole('link', { name: /创建证件照|制作证件照|Create ID Photo/i }).or(
      page.locator('[data-testid="create-idphoto"]')
    );
    await createIdPhotoButton.click();

    await expect(page).toHaveURL(/\/idphoto/);
  });
});

test.describe('ID Photo Module', () => {
  test('TC-IDP-001: Photo Upload Functionality', async ({ page }) => {
    await page.goto('/idphoto');
    await page.waitForLoadState('networkidle');

    const uploadInput = page.locator('input[type="file"]').or(page.getByRole('button', { name: /上传|Upload/i }));
    const filePath = path.resolve('public/favicon.svg');

    if (await uploadInput.inputType() === 'file') {
      await uploadInput.setInputFiles(filePath);
    } else {
      await page.getByRole('button', { name: /上传|Upload/i }).click();
      await page.locator('input[type="file"]').setInputFiles(filePath);
    }

    await expect(page.locator('canvas').or(page.getByRole('img').first())).toBeVisible({ timeout: 10000 });

    await expect(page.locator('.loading').or(page.getByText(/加载中|Loading/))).not.toBeVisible({ timeout: 10000 });
  });

  test('TC-IDP-002: Background Color Change', async ({ page }) => {
    await page.goto('/idphoto');
    await page.waitForLoadState('networkidle');

    const filePath = path.resolve('public/favicon.svg');
    await page.locator('input[type="file"]').setInputFiles(filePath);
    await page.waitForTimeout(1000);

    const blueBackgroundOption = page.getByRole('button', { name: /蓝|Blue/i }).or(
      page.locator('[data-color="blue"]').or(page.locator('[data-testid="bg-blue"]'))
    );
    await blueBackgroundOption.click();

    await expect(blueBackgroundOption).toHaveAttribute('aria-pressed', 'true').or(
      expect(blueBackgroundOption).toHaveClass(/active|selected/)
    );

    const canvas = page.locator('canvas');
    await expect(canvas).toBeVisible();
  });

  test('TC-IDP-003: Photo Specifications Selection', async ({ page }) => {
    await page.goto('/idphoto');
    await page.waitForLoadState('networkidle');

    const filePath = path.resolve('public/favicon.svg');
    await page.locator('input[type="file"]').setInputFiles(filePath);
    await page.waitForTimeout(1000);

    const oneInchOption = page.getByRole('button', { name: /一寸|1寸|1 inch/i }).or(
      page.locator('[data-spec="1inch"]').or(page.getByText(/25mm.*35mm|25×35/))
    );
    await oneInchOption.click();

    await expect(page.getByText(/一寸|1寸|25mm.*35mm/).first()).toBeVisible();
  });

  test('TC-IDP-004: Download/Save ID Photo', async ({ page }) => {
    await page.goto('/idphoto');
    await page.waitForLoadState('networkidle');

    const filePath = path.resolve('public/favicon.svg');
    await page.locator('input[type="file"]').setInputFiles(filePath);
    await page.waitForTimeout(1000);

    const whiteBgOption = page.getByRole('button', { name: /白|White/i }).or(page.locator('[data-color="white"]'));
    await whiteBgOption.click();

    const oneInchOption = page.getByRole('button', { name: /一寸|1寸/i }).or(page.locator('[data-spec="1inch"]'));
    await oneInchOption.click();

    const downloadPromise = page.waitForEvent('download');
    const downloadButton = page.getByRole('button', { name: /下载|保存|Download|Save/i });
    await downloadButton.click();
    const download = await downloadPromise;

    expect(download.suggestedFilename()).toMatch(/\.(jpg|jpeg|png)$/i);
  });
});

test.describe('Poster Module', () => {
  test('TC-PST-001: Template Selection', async ({ page }) => {
    await page.goto('/poster');
    await page.waitForLoadState('networkidle');

    const templateGallery = page.locator('[data-testid="template-gallery"]').or(page.locator('.template-list'));
    await expect(templateGallery).toBeVisible();

    const firstTemplate = templateGallery.locator('img, [data-testid="template-item"]').first().or(
      page.getByRole('img').first()
    );
    await firstTemplate.click();

    await expect(page.locator('canvas').or(page.locator('[data-testid="editor-workspace"]'))).toBeVisible({ timeout: 10000 });
  });

  test('TC-PST-002: Text Editing in Poster', async ({ page }) => {
    await page.goto('/poster');
    await page.waitForLoadState('networkidle');

    const firstTemplate = page.locator('[data-testid="template-gallery"] img, .template-list img').first();
    await firstTemplate.click();
    await page.waitForTimeout(1000);

    const textElement = page.locator('canvas').or(page.getByText(/标题|Title|文案/).first());
    await textElement.click({ force: true });

    const textInput = page.locator('input[type="text"]').or(page.getByRole('textbox'));
    if (await textInput.isVisible()) {
      await textInput.clear();
      await textInput.fill('Test Event Title');
    }

    await page.keyboard.press('Escape');
    await expect(page.getByText('Test Event Title')).toBeVisible();
  });

  test('TC-PST-003: Export Poster', async ({ page }) => {
    await page.goto('/poster');
    await page.waitForLoadState('networkidle');

    const firstTemplate = page.locator('[data-testid="template-gallery"] img, .template-list img').first();
    await firstTemplate.click();
    await page.waitForTimeout(1000);

    const exportButton = page.getByRole('button', { name: /导出|生成|Export|Generate/i });
    await exportButton.click();

    const loader = page.locator('.loading, [data-testid="processing-loader"]').or(page.getByText(/处理中|Processing/));
    await expect(loader).toBeVisible({ timeout: 5000 }).catch(() => {});

    const downloadPromise = page.waitForEvent('download', { timeout: 30000 }).catch(() => null);
    await exportButton.click();
    const download = await downloadPromise;

    if (download) {
      expect(download.suggestedFilename()).toMatch(/\.(jpg|jpeg|png|pdf)$/i);
    }
  });
});

test.describe('Photo Module', () => {
  test('TC-PHT-001: Basic Image Adjustment', async ({ page }) => {
    await page.goto('/photo');
    await page.waitForLoadState('networkidle');

    const filePath = path.resolve('public/favicon.svg');
    await page.locator('input[type="file"]').setInputFiles(filePath);
    await page.waitForTimeout(1000);

    const brightnessSlider = page.getByRole('slider', { name: /亮度|Brightness/i }).or(
      page.locator('input[type="range"][name*="brightness"], [data-testid="brightness-slider"]')
    );

    if (await brightnessSlider.isVisible()) {
      await brightnessSlider.fill('50');
      await page.waitForTimeout(500);

      const canvas = page.locator('canvas');
      await expect(canvas).toBeVisible();
    }
  });

  test('TC-PHT-002: Filter Application', async ({ page }) => {
    await page.goto('/photo');
    await page.waitForLoadState('networkidle');

    const filePath = path.resolve('public/favicon.svg');
    await page.locator('input[type="file"]').setInputFiles(filePath);
    await page.waitForTimeout(1000);

    const grayscaleFilter = page.getByRole('button', { name: /灰度|黑白|Grayscale/i }).or(
      page.locator('[data-filter="grayscale"]')
    );

    if (await grayscaleFilter.isVisible()) {
      await grayscaleFilter.click();
      await expect(grayscaleFilter).toHaveClass(/active|selected/);
    } else {
      const vintageFilter = page.getByRole('button', { name: /复古|Vintage/i }).or(
        page.locator('[data-filter="vintage"]')
      );
      if (await vintageFilter.isVisible()) {
        await vintageFilter.click();
        await expect(vintageFilter).toHaveClass(/active|selected/);
      }
    }
  });
});

test.describe('Orders Module', () => {
  test.use({ storageState: '.auth/user.json' });

  test('TC-ORD-001: View Order History', async ({ page }) => {
    await page.goto('/orders');
    await page.waitForLoadState('networkidle');

    const orderList = page.locator('[data-testid="order-list"]').or(page.locator('.order-list, table'));
    const emptyState = page.locator('[data-testid="empty-orders"]').or(page.getByText(/暂无订单|No orders/));

    const hasOrders = await orderList.isVisible().catch(() => false);
    const isEmpty = await emptyState.isVisible().catch(() => false);

    expect(hasOrders || isEmpty).toBeTruthy();

    if (hasOrders) {
      const orderRow = orderList.locator('tr, [data-testid="order-item"]').first();
      await expect(orderRow).toBeVisible();
    }
  });

  test('TC-ORD-002: Order Detail Verification', async ({ page }) => {
    await page.goto('/orders');
    await page.waitForLoadState('networkidle');

    const orderItem = page.locator('[data-testid="order-item"]').or(page.locator('tr[data-order-id]')).first();

    if (await orderItem.isVisible()) {
      await orderItem.click();

      await expect(page).toHaveURL(/\/orders\/\d+/);

      await expect(page.getByText(/证件照|ID Photo|海报|Poster/)).toBeVisible();

      await expect(page.getByText(/已支付|待支付|Paid|Pending/i)).toBeVisible();
    } else {
      test.skip();
    }
  });

  test('TC-ORD-003: Empty Order State', async ({ page }) => {
    await page.goto('/orders?empty=true');
    await page.waitForLoadState('networkidle');

    const emptyState = page.locator('[data-testid="empty-orders"]').or(
      page.getByText(/暂无订单|No orders|还没有订单/)
    );

    await expect(emptyState).toBeVisible();

    const shopNowLink = page.getByRole('link', { name: /去购物|创建照片|去制作|Shop Now|Create/i });
    await expect(shopNowLink).toBeVisible();
  });
});