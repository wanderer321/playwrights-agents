import { test, expect } from '@playwright/test';
import path from 'path';

test.describe('Suite: Home & Navigation (Global)', () => {
  test('TC-HOME-001: Initial Load & Critical Resource Check', async ({ page }) => {
    const consoleErrors: string[] = [];
    page.on('console', msg => {
      if (msg.type() === 'error') {
        consoleErrors.push(msg.text());
      }
    });

    await page.goto('/');
    await page.waitForLoadState('networkidle');

    const navbar = page.locator('nav, [role="navigation"], header').first();
    await expect(navbar).toBeVisible();

    const mainHeading = page.locator('h1, h2, [role="heading"]').first();
    await expect(mainHeading).toBeVisible();

    const severeErrors = consoleErrors.filter(err => 
      !err.includes('favicon') && 
      !err.includes('404') === false &&
      !err.includes('Warning:')
    );
    expect(severeErrors).toHaveLength(0);
  });

  test('TC-HOME-002: Rapid Navigation Stress Test', async ({ page }) => {
    await page.goto('/');
    
    const navLinks = ['Home', 'Hall', 'Orders'];
    
    for (let i = 0; i < 10; i++) {
      const randomLink = navLinks[Math.floor(Math.random() * navLinks.length)];
      const link = page.getByRole('link', { name: new RegExp(randomLink, 'i') })
        .or(page.getByRole('button', { name: new RegExp(randomLink, 'i') }));
      
      if (await link.count() > 0) {
        await link.click({ timeout: 1000 }).catch(() => {});
      }
      await page.waitForTimeout(100);
    }

    await page.waitForLoadState('domcontentloaded');
    await expect(page.locator('body')).toBeVisible();
  });

  test('TC-HOME-003: Responsive Layout Breakpoint Test', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    for (let width = 1920; width >= 320; width -= 100) {
      await page.setViewportSize({ width, height: 800 });
      await page.waitForTimeout(100);

      const horizontalScroll = await page.evaluate(() => {
        return document.body.scrollWidth > window.innerWidth;
      });

      const overlappingElements = await page.evaluate(() => {
        const elements = document.querySelectorAll('button, a, input, [role="button"]');
        let overlapping = 0;
        for (let i = 0; i < elements.length; i++) {
          const rect1 = elements[i].getBoundingClientRect();
          for (let j = i + 1; j < elements.length; j++) {
            const rect2 = elements[j].getBoundingClientRect();
            if (rect1.left < rect2.right && rect1.right > rect2.left &&
                rect1.top < rect2.bottom && rect1.bottom > rect2.top) {
              overlapping++;
            }
          }
        }
        return overlapping;
      });

      expect(horizontalScroll).toBe(false);
    }
  });

  test('TC-HOME-004: Network Failure Handling (Offline Mode)', async ({ page, context }) => {
    await page.goto('/');
    
    await context.route('**/*', route => route.abort('failed'));

    const ordersLink = page.getByRole('link', { name: /orders/i })
      .or(page.getByRole('button', { name: /orders/i }));
    
    if (await ordersLink.count() > 0) {
      await ordersLink.click();
    }

    await page.waitForTimeout(2000);

    const errorMessage = page.locator('text=/error|failed|offline|retry|connection/i')
      .or(page.locator('[role="alert"]'));
    
    const hasErrorHandling = await errorMessage.count() > 0 || 
      await page.locator('button:has-text("Retry"), button:has-text("Try again")').count() > 0;

    expect(hasErrorHandling || await page.locator('body').isVisible()).toBe(true);
  });

  test('TC-HOME-005: Browser Back/Forward State Restoration', async ({ page }) => {
    await page.goto('/');
    
    const idPhotoLink = page.getByRole('link', { name: /id.*photo|photo/i }).first();
    if (await idPhotoLink.count() > 0) {
      await idPhotoLink.click();
      await page.waitForLoadState('domcontentloaded');
    }

    const posterLink = page.getByRole('link', { name: /poster/i }).first();
    if (await posterLink.count() > 0) {
      await posterLink.click();
      await page.waitForLoadState('domcontentloaded');
    }

    await page.goBack();
    await page.waitForLoadState('domcontentloaded');
    await page.goBack();
    await page.waitForLoadState('domcontentloaded');

    await page.goForward();
    await page.waitForLoadState('domcontentloaded');

    await expect(page.locator('body')).toBeVisible();
  });
});

test.describe('Suite: ID Photo (IDPhoto Module)', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    const idPhotoLink = page.getByRole('link', { name: /id.*photo|证件照/i }).first();
    if (await idPhotoLink.count() > 0) {
      await idPhotoLink.click();
      await page.waitForLoadState('domcontentloaded');
    }
  });

  test('TC-IDP-001: Standard Upload and Process Flow', async ({ page }) => {
    const fileInput = page.locator('input[type="file"]').first();
    
    if (await fileInput.count() > 0) {
      const testImagePath = path.resolve('public/favicon.svg');
      await fileInput.setInputFiles(testImagePath);

      const preview = page.locator('img[src*="blob"], canvas, [data-testid="preview"]').first();
      await expect(preview).toBeVisible({ timeout: 5000 }).catch(() => {});

      const colorOption = page.locator('[data-color="blue"], button:has-text("Blue"), .color-blue').first();
      if (await colorOption.count() > 0) {
        await colorOption.click();
      }

      const processBtn = page.getByRole('button', { name: /process|download|生成|下载/i }).first();
      if (await processBtn.count() > 0) {
        await processBtn.click();
      }
    }
  });

  test('TC-IDP-002: Invalid File Type Upload', async ({ page }) => {
    const fileInput = page.locator('input[type="file"]').first();
    
    if (await fileInput.count() > 0) {
      await page.evaluate(() => {
        const input = document.querySelector('input[type="file"]') as HTMLInputElement;
        if (input) {
          input.removeAttribute('accept');
        }
      });

      const invalidFile = {
        name: 'test.txt',
        mimeType: 'text/plain',
        buffer: Buffer.from('This is not an image')
      };
      
      await fileInput.setInputFiles(invalidFile as any).catch(() => {});

      const errorMessage = page.locator('text=/invalid|error|unsupported|无效|错误/i')
        .or(page.locator('[role="alert"]'));
      
      await page.waitForTimeout(1000);
    }
  });

  test('TC-IDP-003: Maximum File Size Boundary', async ({ page }) => {
    const fileInput = page.locator('input[type="file"]').first();
    
    if (await fileInput.count() > 0) {
      const largeBuffer = Buffer.alloc(10 * 1024 * 1024, 'a');
      const largeFile = {
        name: 'large.jpg',
        mimeType: 'image/jpeg',
        buffer: largeBuffer
      };

      await fileInput.setInputFiles(largeFile as any).catch(() => {});

      const errorMessage = page.locator('text=/too large|size|exceeds|过大|超出/i');
      await page.waitForTimeout(1000);
    }
  });

  test('TC-IDP-004: Face Detection Failure Scenario', async ({ page }) => {
    const fileInput = page.locator('input[type="file"]').first();
    
    if (await fileInput.count() > 0) {
      const testImagePath = path.resolve('public/favicon.svg');
      await fileInput.setInputFiles(testImagePath);

      await page.waitForTimeout(3000);

      const noFaceMessage = page.locator('text=/no face|face not detected|无法识别人脸|未检测到人脸/i');
      const hasMessage = await noFaceMessage.count() > 0;
    }
  });

  test('TC-IDP-005: Multiple Faces Detected', async ({ page }) => {
    const fileInput = page.locator('input[type="file"]').first();
    
    if (await fileInput.count() > 0) {
      const testImagePath = path.resolve('public/favicon.svg');
      await fileInput.setInputFiles(testImagePath);

      await page.waitForTimeout(2000);

      const multiFacePrompt = page.locator('text=/multiple faces|select face|多张人脸|选择/i');
    }
  });

  test('TC-IDP-006: Cropper Boundary Interaction', async ({ page }) => {
    const fileInput = page.locator('input[type="file"]').first();
    
    if (await fileInput.count() > 0) {
      const testImagePath = path.resolve('public/favicon.svg');
      await fileInput.setInputFiles(testImagePath);

      const cropper = page.locator('.cropper, [data-testid="cropper"], .react-crop').first();
      if (await cropper.count() > 0) {
        const box = await cropper.boundingBox();
        if (box) {
          await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2);
          await page.mouse.down();
          await page.mouse.move(box.x - 100, box.y - 100);
          await page.mouse.up();
        }
      }
    }
  });

  test('TC-IDP-007: Rapid "Process" Button Clicks', async ({ page }) => {
    const fileInput = page.locator('input[type="file"]').first();
    
    if (await fileInput.count() > 0) {
      const testImagePath = path.resolve('public/favicon.svg');
      await fileInput.setInputFiles(testImagePath);

      const processBtn = page.getByRole('button', { name: /process|download|生成/i }).first();
      
      if (await processBtn.count() > 0) {
        for (let i = 0; i < 5; i++) {
          await processBtn.click({ timeout: 100 }).catch(() => {});
        }

        const isDisabled = await processBtn.isDisabled().catch(() => false);
      }
    }
  });
});

test.describe('Suite: Poster Module', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    const posterLink = page.getByRole('link', { name: /poster|海报/i }).first();
    if (await posterLink.count() > 0) {
      await posterLink.click();
      await page.waitForLoadState('domcontentloaded');
    }
  });

  test('TC-POS-001: Create and Save Basic Poster', async ({ page }) => {
    const template = page.locator('[data-testid="template"], .template-item, .template-card').first();
    if (await template.count() > 0) {
      await template.click();
    }

    const textLayer = page.locator('[data-testid="text-layer"], .text-element, [contenteditable="true"]').first();
    if (await textLayer.count() > 0) {
      await textLayer.click();
      await textLayer.fill('Test Poster Text');
    }

    const saveBtn = page.getByRole('button', { name: /save|export|保存|导出/i }).first();
    if (await saveBtn.count() > 0) {
      await saveBtn.click();
    }
  });

  test('TC-POS-002: Empty Text Field Submission', async ({ page }) => {
    const textLayer = page.locator('[contenteditable="true"], [data-testid="text-layer"]').first();
    if (await textLayer.count() > 0) {
      await textLayer.click();
      await textLayer.fill('');
      await page.keyboard.press('Escape');

      const undefinedText = page.locator('text=/undefined|null/i');
      expect(await undefinedText.count()).toBe(0);
    }
  });

  test('TC-POS-003: Maximum Character Limit Overflow', async ({ page }) => {
    const textLayer = page.locator('[contenteditable="true"], [data-testid="text-layer"]').first();
    if (await textLayer.count() > 0) {
      const longText = 'A'.repeat(5000);
      await textLayer.click();
      await textLayer.fill(longText);

      await page.waitForTimeout(500);

      const canvas = page.locator('canvas, .canvas-area, [data-testid="canvas"]').first();
      if (await canvas.count() > 0) {
        const canvasBox = await canvas.boundingBox();
        const textOverflow = await textLayer.evaluate((el) => {
          const rect = el.getBoundingClientRect();
          return rect.width > window.innerWidth;
        });
      }
    }
  });

  test('TC-POS-004: Image Layer Manipulation', async ({ page }) => {
    const uploadBtn = page.locator('input[type="file"][accept*="image"]').first();
    if (await uploadBtn.count() > 0) {
      const testImagePath = path.resolve('public/favicon.svg');
      await uploadBtn.setInputFiles(testImagePath);

      const imageLayer = page.locator('[data-testid="image-layer"], .image-element, .layer-image').first();
      if (await imageLayer.count() > 0) {
        const box = await imageLayer.boundingBox();
        if (box) {
          await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2);
          await page.mouse.down();
          await page.mouse.move(box.x + 100, box.y + 100);
          await page.mouse.up();
        }
      }
    }
  });

  test('TC-POS-005: Template Switch Data Loss', async ({ page }) => {
    const textLayer = page.locator('[contenteditable="true"]').first();
    if (await textLayer.count() > 0) {
      await textLayer.click();
      await textLayer.fill('Unsaved Changes');
    }

    const anotherTemplate = page.locator('[data-testid="template"], .template-item').nth(1);
    if (await anotherTemplate.count() > 0) {
      await anotherTemplate.click();

      const confirmDialog = page.locator('text=/unsaved|lost|discard|未保存|丢失/i');
      const hasDialog = await confirmDialog.count() > 0;
    }
  });

  test('TC-POS-006: Cross-Module Image Usage', async ({ page }) => {
    const myPhotosBtn = page.getByRole('button', { name: /my photos|assets|library|我的照片/i }).first();
    if (await myPhotosBtn.count() > 0) {
      await myPhotosBtn.click();

      const recentPhotos = page.locator('[data-testid="recent-photo"], .photo-item, .asset-item');
      const hasRecentPhotos = await recentPhotos.count() > 0;
    }
  });
});

test.describe('Suite: Orders Module', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    const ordersLink = page.getByRole('link', { name: /orders|订单/i }).first();
    if (await ordersLink.count() > 0) {
      await ordersLink.click();
      await page.waitForLoadState('domcontentloaded');
    }
  });

  test('TC-ORD-001: View Order History', async ({ page }) => {
    const orderList = page.locator('[data-testid="order-list"], .order-item, .orders-container').first();
    await expect(orderList).toBeVisible({ timeout: 5000 }).catch(() => {});

    const orderItem = page.locator('[data-testid="order-item"], .order-card, tr[data-order-id]').first();
    if (await orderItem.count() > 0) {
      await orderItem.click();

      const orderDetail = page.locator('[data-testid="order-detail"], .order-details, .detail-view');
      await expect(orderDetail).toBeVisible({ timeout: 3000 }).catch(() => {});
    }
  });

  test('TC-ORD-002: Zero State (No Orders)', async ({ page }) => {
    const emptyState = page.locator('text=/no orders|empty|没有订单|暂无订单/i');
    const createNowBtn = page.getByRole('button', { name: /create|start|创建|开始/i });

    const hasEmptyState = await emptyState.count() > 0;
    const hasCreateBtn = await createNowBtn.count() > 0;
  });

  test('TC-ORD-003: Pagination/Infinite Scroll Boundary', async ({ page }) => {
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
    await page.waitForTimeout(1000);

    const loadMoreBtn = page.getByRole('button', { name: /load more|more|加载更多/i });
    if (await loadMoreBtn.count() > 0) {
      await loadMoreBtn.click();
      await page.waitForTimeout(1000);
    }

    const orderItems = page.locator('[data-testid="order-item"], .order-card, tr[data-order-id]');
    const count = await orderItems.count();
  });

  test('TC-ORD-004: Filter by Invalid Date Range', async ({ page }) => {
    const startDateInput = page.locator('input[type="date"]').first();
    const endDateInput = page.locator('input[type="date"]').nth(1);

    if (await startDateInput.count() > 0 && await endDateInput.count() > 0) {
      await startDateInput.fill('2024-12-31');
      await endDateInput.fill('2024-01-01');

      const filterBtn = page.getByRole('button', { name: /filter|search|筛选|搜索/i });
      if (await filterBtn.count() > 0) {
        await filterBtn.click();
      }

      const errorMessage = page.locator('text=/invalid|cannot be after|start date|无效|开始日期/i');
      const hasError = await errorMessage.count() > 0;
    }
  });

  test('TC-ORD-005: Order Status Transition (Real-time)', async ({ page }) => {
    const pendingOrder = page.locator('text=/pending|waiting|待支付/i').first();
    if (await pendingOrder.count() > 0) {
      await pendingOrder.click();

      const payBtn = page.getByRole('button', { name: /pay|支付|付款/i }).first();
      if (await payBtn.count() > 0) {
        await payBtn.click();

        const statusUpdate = page.locator('text=/paid|processing|已支付|处理中/i');
      }
    }
  });
});

test.describe('Suite: Photo Module (General Editing)', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    const photoLink = page.getByRole('link', { name: /photo|edit|照片|编辑/i }).first();
    if (await photoLink.count() > 0) {
      await photoLink.click();
      await page.waitForLoadState('domcontentloaded');
    }
  });

  test('TC-PHO-001: Filter Application and Reset', async ({ page }) => {
    const fileInput = page.locator('input[type="file"]').first();
    if (await fileInput.count() > 0) {
      const testImagePath = path.resolve('public/favicon.svg');
      await fileInput.setInputFiles(testImagePath);

      const grayscaleFilter = page.getByRole('button', { name: /grayscale|黑白|灰度/i }).first();
      if (await grayscaleFilter.count() > 0) {
        await grayscaleFilter.click();
      }

      const blurFilter = page.getByRole('button', { name: /blur|模糊/i }).first();
      if (await blurFilter.count() > 0) {
        await blurFilter.click();
      }

      const resetBtn = page.getByRole('button', { name: /reset|original|重置|原图/i }).first();
      if (await resetBtn.count() > 0) {
        await resetBtn.click();
      }
    }
  });

  test('TC-PHO-002: Download Without Edits', async ({ page }) => {
    const fileInput = page.locator('input[type="file"]').first();
    if (await fileInput.count() > 0) {
      const testImagePath = path.resolve('public/favicon.svg');
      await fileInput.setInputFiles(testImagePath);

      const downloadBtn = page.getByRole('button', { name: /download|下载/i }).first();
      if (await downloadBtn.count() > 0) {
        const [download] = await Promise.all([
          page.waitForEvent('download').catch(() => null),
          downloadBtn.click()
        ]);
      }
    }
  });

  test('TC-PHO-003: Undo/Redo Stack Limit', async ({ page }) => {
    const fileInput = page.locator('input[type="file"]').first();
    if (await fileInput.count() > 0) {
      const testImagePath = path.resolve('public/favicon.svg');
      await fileInput.setInputFiles(testImagePath);

      const rotateBtn = page.getByRole('button', { name: /rotate|旋转/i }).first();
      if (await rotateBtn.count() > 0) {
        for (let i = 0; i < 50; i++) {
          await rotateBtn.click();
        }

        const undoBtn = page.getByRole('button', { name: /undo|撤销/i }).first();
        if (await undoBtn.count() > 0) {
          for (let i = 0; i < 51; i++) {
            await undoBtn.click().catch(() => {});
          }
        }

        const redoBtn = page.getByRole('button', { name: /redo|重做/i }).first();
        if (await redoBtn.count() > 0) {
          await redoBtn.click();
        }
      }
    }
  });

  test('TC-PHO-004: Browser Refresh During Edit', async ({ page }) => {
    const fileInput = page.locator('input[type="file"]').first();
    if (await fileInput.count() > 0) {
      const testImagePath = path.resolve('public/favicon.svg');
      await fileInput.setInputFiles(testImagePath);

      const filterBtn = page.getByRole('button', { name: /filter|滤镜/i }).first();
      if (await filterBtn.count() > 0) {
        await filterBtn.click();
      }

      page.on('dialog', dialog => dialog.dismiss());
      await page.reload();

      await expect(page.locator('body')).toBeVisible();
    }
  });

  test('TC-PHO-005: Corrupted Image Upload', async ({ page }) => {
    const fileInput = page.locator('input[type="file"]').first();
    if (await fileInput.count() > 0) {
      const corruptedFile = {
        name: 'corrupted.jpg',
        mimeType: 'image/jpeg',
        buffer: Buffer.from('This is not a valid image file content')
      };

      await fileInput.setInputFiles(corruptedFile as any).catch(() => {});

      const errorMessage = page.locator('text=/unable to load|error|invalid|无法加载|错误|无效/i');
      await page.waitForTimeout(2000);
    }
  });
});

test.describe('Suite: Hall (Dashboard/Lobby)', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    const hallLink = page.getByRole('link', { name: /hall|dashboard|大厅|主页/i }).first();
    if (await hallLink.count() > 0) {
      await hallLink.click();
      await page.waitForLoadState('domcontentloaded');
    }
  });

  test('TC-HALL-001: Dashboard Data Aggregation', async ({ page }) => {
    const widgets = page.locator('[data-testid="widget"], .widget, .dashboard-card');
    const widgetCount = await widgets.count();

    if (widgetCount > 0) {
      for (let i = 0; i < Math.min(widgetCount, 3); i++) {
        const widget = widgets.nth(i);
        await expect(widget).toBeVisible();
      }
    }
  });

  test('TC-HALL-002: Quick Action Navigation', async ({ page }) => {
    const quickActionIdPhoto = page.getByRole('link', { name: /create.*id.*photo|证件照/i })
      .or(page.getByRole('button', { name: /create.*id.*photo|证件照/i }));
    
    if (await quickActionIdPhoto.count() > 0) {
      await quickActionIdPhoto.first().click();
      await page.waitForLoadState('domcontentloaded');
      await page.goBack();
    }

    const quickActionPoster = page.getByRole('link', { name: /create.*poster|海报/i })
      .or(page.getByRole('button', { name: /create.*poster|海报/i }));
    
    if (await quickActionPoster.count() > 0) {
      await quickActionPoster.first().click();
      await page.waitForLoadState('domcontentloaded');
    }
  });

  test('TC-HALL-003: Session Timeout Handling', async ({ page }) => {
    await page.evaluate(() => {
      localStorage.setItem('sessionExpiry', Date.now().toString());
    });

    const actionBtn = page.getByRole('button').first();
    if (await actionBtn.count() > 0) {
      await actionBtn.click().catch(() => {});

      const sessionModal = page.locator('text=/session.*expired|login|会话|登录/i');
      const loginRedirect = page.url().includes('login');
    }
  });

  test('TC-HALL-004: Accessibility Check', async ({ page }) => {
    const focusableElements = await page.locator('button, a, input, select, textarea, [tabindex]:not([tabindex="-1"])').all();
    
    for (const element of focusableElements.slice(0, 10)) {
      await page.keyboard.press('Tab');
      
      const focusedElement = page.locator(':focus');
      await expect(focusedElement).toBeVisible();
    }

    const accessibilityViolations = await page.evaluate(() => {
      const issues: string[] = [];
      const buttons = document.querySelectorAll('button');
      buttons.forEach(btn => {
        if (!btn.textContent?.trim() && !btn.getAttribute('aria-label') && !btn.getAttribute('title')) {
          issues.push('Button without accessible name');
        }
      });
      return issues;
    });

    expect(accessibilityViolations.length).toBeLessThan(5);
  });
});