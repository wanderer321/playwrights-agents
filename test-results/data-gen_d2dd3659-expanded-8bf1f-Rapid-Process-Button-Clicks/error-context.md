# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: data\gen_d2dd3659\expanded_gen_0.spec.ts >> Suite: ID Photo (IDPhoto Module) >> TC-IDP-007: Rapid "Process" Button Clicks
- Location: data\gen_d2dd3659\expanded_gen_0.spec.ts:255:7

# Error details

```
Error: page.goto: Protocol error (Page.navigate): Cannot navigate to invalid URL
Call log:
  - navigating to "/", waiting until "load"

```

# Test source

```ts
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
  132 | test.describe('Suite: ID Photo (IDPhoto Module)', () => {
  133 |   test.beforeEach(async ({ page }) => {
> 134 |     await page.goto('/');
      |                ^ Error: page.goto: Protocol error (Page.navigate): Cannot navigate to invalid URL
  135 |     const idPhotoLink = page.getByRole('link', { name: /id.*photo|证件照/i }).first();
  136 |     if (await idPhotoLink.count() > 0) {
  137 |       await idPhotoLink.click();
  138 |       await page.waitForLoadState('domcontentloaded');
  139 |     }
  140 |   });
  141 | 
  142 |   test('TC-IDP-001: Standard Upload and Process Flow', async ({ page }) => {
  143 |     const fileInput = page.locator('input[type="file"]').first();
  144 |     
  145 |     if (await fileInput.count() > 0) {
  146 |       const testImagePath = path.resolve('public/favicon.svg');
  147 |       await fileInput.setInputFiles(testImagePath);
  148 | 
  149 |       const preview = page.locator('img[src*="blob"], canvas, [data-testid="preview"]').first();
  150 |       await expect(preview).toBeVisible({ timeout: 5000 }).catch(() => {});
  151 | 
  152 |       const colorOption = page.locator('[data-color="blue"], button:has-text("Blue"), .color-blue').first();
  153 |       if (await colorOption.count() > 0) {
  154 |         await colorOption.click();
  155 |       }
  156 | 
  157 |       const processBtn = page.getByRole('button', { name: /process|download|生成|下载/i }).first();
  158 |       if (await processBtn.count() > 0) {
  159 |         await processBtn.click();
  160 |       }
  161 |     }
  162 |   });
  163 | 
  164 |   test('TC-IDP-002: Invalid File Type Upload', async ({ page }) => {
  165 |     const fileInput = page.locator('input[type="file"]').first();
  166 |     
  167 |     if (await fileInput.count() > 0) {
  168 |       await page.evaluate(() => {
  169 |         const input = document.querySelector('input[type="file"]') as HTMLInputElement;
  170 |         if (input) {
  171 |           input.removeAttribute('accept');
  172 |         }
  173 |       });
  174 | 
  175 |       const invalidFile = {
  176 |         name: 'test.txt',
  177 |         mimeType: 'text/plain',
  178 |         buffer: Buffer.from('This is not an image')
  179 |       };
  180 |       
  181 |       await fileInput.setInputFiles(invalidFile as any).catch(() => {});
  182 | 
  183 |       const errorMessage = page.locator('text=/invalid|error|unsupported|无效|错误/i')
  184 |         .or(page.locator('[role="alert"]'));
  185 |       
  186 |       await page.waitForTimeout(1000);
  187 |     }
  188 |   });
  189 | 
  190 |   test('TC-IDP-003: Maximum File Size Boundary', async ({ page }) => {
  191 |     const fileInput = page.locator('input[type="file"]').first();
  192 |     
  193 |     if (await fileInput.count() > 0) {
  194 |       const largeBuffer = Buffer.alloc(10 * 1024 * 1024, 'a');
  195 |       const largeFile = {
  196 |         name: 'large.jpg',
  197 |         mimeType: 'image/jpeg',
  198 |         buffer: largeBuffer
  199 |       };
  200 | 
  201 |       await fileInput.setInputFiles(largeFile as any).catch(() => {});
  202 | 
  203 |       const errorMessage = page.locator('text=/too large|size|exceeds|过大|超出/i');
  204 |       await page.waitForTimeout(1000);
  205 |     }
  206 |   });
  207 | 
  208 |   test('TC-IDP-004: Face Detection Failure Scenario', async ({ page }) => {
  209 |     const fileInput = page.locator('input[type="file"]').first();
  210 |     
  211 |     if (await fileInput.count() > 0) {
  212 |       const testImagePath = path.resolve('public/favicon.svg');
  213 |       await fileInput.setInputFiles(testImagePath);
  214 | 
  215 |       await page.waitForTimeout(3000);
  216 | 
  217 |       const noFaceMessage = page.locator('text=/no face|face not detected|无法识别人脸|未检测到人脸/i');
  218 |       const hasMessage = await noFaceMessage.count() > 0;
  219 |     }
  220 |   });
  221 | 
  222 |   test('TC-IDP-005: Multiple Faces Detected', async ({ page }) => {
  223 |     const fileInput = page.locator('input[type="file"]').first();
  224 |     
  225 |     if (await fileInput.count() > 0) {
  226 |       const testImagePath = path.resolve('public/favicon.svg');
  227 |       await fileInput.setInputFiles(testImagePath);
  228 | 
  229 |       await page.waitForTimeout(2000);
  230 | 
  231 |       const multiFacePrompt = page.locator('text=/multiple faces|select face|多张人脸|选择/i');
  232 |     }
  233 |   });
  234 | 
```