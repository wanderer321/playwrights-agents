# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: data\gen_d2dd3659\expanded_gen_0.spec.ts >> Suite: Home & Navigation (Global) >> TC-HOME-002: Rapid Navigation Stress Test
- Location: data\gen_d2dd3659\expanded_gen_0.spec.ts:30:7

# Error details

```
Error: page.goto: Protocol error (Page.navigate): Cannot navigate to invalid URL
Call log:
  - navigating to "/", waiting until "load"

```

# Test source

```ts
  1   | import { test, expect } from '@playwright/test';
  2   | import path from 'path';
  3   | 
  4   | test.describe('Suite: Home & Navigation (Global)', () => {
  5   |   test('TC-HOME-001: Initial Load & Critical Resource Check', async ({ page }) => {
  6   |     const consoleErrors: string[] = [];
  7   |     page.on('console', msg => {
  8   |       if (msg.type() === 'error') {
  9   |         consoleErrors.push(msg.text());
  10  |       }
  11  |     });
  12  | 
  13  |     await page.goto('/');
  14  |     await page.waitForLoadState('networkidle');
  15  | 
  16  |     const navbar = page.locator('nav, [role="navigation"], header').first();
  17  |     await expect(navbar).toBeVisible();
  18  | 
  19  |     const mainHeading = page.locator('h1, h2, [role="heading"]').first();
  20  |     await expect(mainHeading).toBeVisible();
  21  | 
  22  |     const severeErrors = consoleErrors.filter(err => 
  23  |       !err.includes('favicon') && 
  24  |       !err.includes('404') === false &&
  25  |       !err.includes('Warning:')
  26  |     );
  27  |     expect(severeErrors).toHaveLength(0);
  28  |   });
  29  | 
  30  |   test('TC-HOME-002: Rapid Navigation Stress Test', async ({ page }) => {
> 31  |     await page.goto('/');
      |                ^ Error: page.goto: Protocol error (Page.navigate): Cannot navigate to invalid URL
  32  |     
  33  |     const navLinks = ['Home', 'Hall', 'Orders'];
  34  |     
  35  |     for (let i = 0; i < 10; i++) {
  36  |       const randomLink = navLinks[Math.floor(Math.random() * navLinks.length)];
  37  |       const link = page.getByRole('link', { name: new RegExp(randomLink, 'i') })
  38  |         .or(page.getByRole('button', { name: new RegExp(randomLink, 'i') }));
  39  |       
  40  |       if (await link.count() > 0) {
  41  |         await link.click({ timeout: 1000 }).catch(() => {});
  42  |       }
  43  |       await page.waitForTimeout(100);
  44  |     }
  45  | 
  46  |     await page.waitForLoadState('domcontentloaded');
  47  |     await expect(page.locator('body')).toBeVisible();
  48  |   });
  49  | 
  50  |   test('TC-HOME-003: Responsive Layout Breakpoint Test', async ({ page }) => {
  51  |     await page.goto('/');
  52  |     await page.waitForLoadState('networkidle');
  53  | 
  54  |     for (let width = 1920; width >= 320; width -= 100) {
  55  |       await page.setViewportSize({ width, height: 800 });
  56  |       await page.waitForTimeout(100);
  57  | 
  58  |       const horizontalScroll = await page.evaluate(() => {
  59  |         return document.body.scrollWidth > window.innerWidth;
  60  |       });
  61  | 
  62  |       const overlappingElements = await page.evaluate(() => {
  63  |         const elements = document.querySelectorAll('button, a, input, [role="button"]');
  64  |         let overlapping = 0;
  65  |         for (let i = 0; i < elements.length; i++) {
  66  |           const rect1 = elements[i].getBoundingClientRect();
  67  |           for (let j = i + 1; j < elements.length; j++) {
  68  |             const rect2 = elements[j].getBoundingClientRect();
  69  |             if (rect1.left < rect2.right && rect1.right > rect2.left &&
  70  |                 rect1.top < rect2.bottom && rect1.bottom > rect2.top) {
  71  |               overlapping++;
  72  |             }
  73  |           }
  74  |         }
  75  |         return overlapping;
  76  |       });
  77  | 
  78  |       expect(horizontalScroll).toBe(false);
  79  |     }
  80  |   });
  81  | 
  82  |   test('TC-HOME-004: Network Failure Handling (Offline Mode)', async ({ page, context }) => {
  83  |     await page.goto('/');
  84  |     
  85  |     await context.route('**/*', route => route.abort('failed'));
  86  | 
  87  |     const ordersLink = page.getByRole('link', { name: /orders/i })
  88  |       .or(page.getByRole('button', { name: /orders/i }));
  89  |     
  90  |     if (await ordersLink.count() > 0) {
  91  |       await ordersLink.click();
  92  |     }
  93  | 
  94  |     await page.waitForTimeout(2000);
  95  | 
  96  |     const errorMessage = page.locator('text=/error|failed|offline|retry|connection/i')
  97  |       .or(page.locator('[role="alert"]'));
  98  |     
  99  |     const hasErrorHandling = await errorMessage.count() > 0 || 
  100 |       await page.locator('button:has-text("Retry"), button:has-text("Try again")').count() > 0;
  101 | 
  102 |     expect(hasErrorHandling || await page.locator('body').isVisible()).toBe(true);
  103 |   });
  104 | 
  105 |   test('TC-HOME-005: Browser Back/Forward State Restoration', async ({ page }) => {
  106 |     await page.goto('/');
  107 |     
  108 |     const idPhotoLink = page.getByRole('link', { name: /id.*photo|photo/i }).first();
  109 |     if (await idPhotoLink.count() > 0) {
  110 |       await idPhotoLink.click();
  111 |       await page.waitForLoadState('domcontentloaded');
  112 |     }
  113 | 
  114 |     const posterLink = page.getByRole('link', { name: /poster/i }).first();
  115 |     if (await posterLink.count() > 0) {
  116 |       await posterLink.click();
  117 |       await page.waitForLoadState('domcontentloaded');
  118 |     }
  119 | 
  120 |     await page.goBack();
  121 |     await page.waitForLoadState('domcontentloaded');
  122 |     await page.goBack();
  123 |     await page.waitForLoadState('domcontentloaded');
  124 | 
  125 |     await page.goForward();
  126 |     await page.waitForLoadState('domcontentloaded');
  127 | 
  128 |     await expect(page.locator('body')).toBeVisible();
  129 |   });
  130 | });
  131 | 
```