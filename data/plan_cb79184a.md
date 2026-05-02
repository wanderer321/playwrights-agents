Based on the project analysis, this is a large-scale native WeChat Mini Program with 316 pages and 5 custom components. Given the project name "pure-activity" and the scale, it is highly likely a comprehensive event management, marketing, or ticketing platform.

Below is the structured test plan designed for Minium automation.

```markdown
# Test Plan: Pure Activity (pure-activity)

## Overview
- **Project Name**: pure-activity
- **Framework**: Native WeChat Mini Program
- **Scale**: Large (316 Pages, 5 Components)
- **Nature**: Likely an Event/Activity management platform (based on name).
- **Test Strategy**: Due to the large number of pages, this test plan prioritizes core business flows (P0), key WeChat capabilities (Login/Payment/Share), and stability. Test suites are organized by functional modules rather than individual pages to ensure maintainability.

---

## Suite: 1. Infrastructure & App Launch
### TC-APP-001: Mini Program Launch & Network Check
- **Steps**:
  1. Initialize Minium connection: `mini.connect()`.
  2. Launch the mini program: `mini.launch()`.
  3. Verify `App.onLaunch` lifecycle triggers.
  4. Check network status via `wx.getNetworkType`.
- **Expect**: App launches successfully; Home page loads without crash; Network type is returned correctly.

### TC-APP-002: Global Exception Handling
- **Steps**:
  1. Simulate a JS execution error on a page.
  2. Check if the global `onError` hook captures the error log.
- **Expect**: Error is logged; App does not crash or exit unexpectedly.

---

## Suite: 2. User Authentication Module
### TC-AUTH-001: WeChat User Login Flow
- **Steps**:
  1. Navigate to the profile or login page.
  2. Click the "WeChat Login" button.
  3. Mock `wx.login` API to return a valid code.
  4. Verify backend exchange (token retrieval).
- **Expect**: User avatar and nickname displayed; User state changes to "Logged In".

### TC-AUTH-002: Get User Phone Number
- **Steps**:
  1. Locate the "Bind Phone Number" button (`open-type="getPhoneNumber"`).
  2. Simulate user click and confirm authorization.
  3. Mock `getPhoneNumber` success callback.
- **Expect**: Phone number is successfully bound to the account; UI updates to show verified status.

### TC-AUTH-003: Location Permission Handling
- **Steps**:
  1. Trigger a feature requiring location (e.g., "Nearby Activities").
  2. Handle the system authorization popup (Allow/Deny).
  3. If denied, check for fallback UI or guidance text.
- **Expect**: Location retrieved if allowed; Graceful error handling if denied.

---

## Suite: 3. Home & Activity Discovery Module
### TC-HOME-001: Activity List Rendering
- **Steps**:
  1. Navigate to the Home page.
  2. Wait for data loading (`page.data` check).
  3. Verify the `wx:for` list renders items > 0.
- **Expect**: Activity cards display correct image, title, and date; No layout breaks.

### TC-HOME-002: Pull-down Refresh
- **Steps**:
  1. Perform pull-down gesture on the Home page.
  2. Verify `onPullDownRefresh` triggers.
  3. Check for loading indicator.
- **Expect**: List data refreshes; Loading indicator appears and dismisses; `wx.stopPullDownRefresh` is called.

### TC-HOME-003: Search Functionality
- **Steps**:
  1. Focus on the search input component.
  2. Input a keyword (e.g., "Marathon").
  3. Click Search/Enter.
  4. Verify navigation to result page or list filtering.
- **Expect**: Results match the keyword; Empty state shown if no results.

---

## Suite: 4. Activity Detail & Interaction
### TC-DETAIL-001: Detail Page Navigation
- **Steps**:
  1. Click an item from the Activity List.
  2. Verify `wx.navigateTo` URL contains the correct Activity ID.
  3. Check if detail page requests specific API data.
- **Expect**: Detail page loads correct content (Rich text, images, maps).

### TC-DETAIL-002: Share to Friends/Groups
- **Steps**:
  1. On Detail page, click the "Share" button (`<button open-type="share">`).
  2. Verify `onShareAppMessage` options (title, path, imageUrl).
- **Expect**: Share menu pops up; Shared card displays correct title and image.

### TC-DETAIL-003: Add to Favorites
- **Steps**:
  1. Click the "Favorite/Star" icon.
  2. Check API request status.
  3. Verify icon state toggle (Filled vs. Outlined).
- **Expect**: Icon toggles immediately; Data persists on reload.

---

## Suite: 5. Registration & Payment Module
### TC-PAY-001: Activity Registration Flow
- **Steps**:
  1. Click "Sign Up" or "Buy Ticket".
  2. Fill in required form fields (Name, ID, etc.).
  3. Submit form.
- **Expect**: Validation works for empty fields; Data submitted successfully; Transitions to payment.

### TC-PAY-002: WeChat Payment Integration
- **Steps**:
  1. Initiate payment for a paid activity.
  2. Mock `wx.requestPayment` API (Success scenario).
  3. Verify order status update in backend/UI.
- **Expect**: Payment success callback triggers; User is redirected to "Payment Success" page or Ticket page.

### TC-PAY-003: Payment Failure/Cancel
- **Steps**:
  1. Initiate payment.
  2. Mock `wx.requestPayment` API (Fail/Cancel scenario).
  3. Check UI feedback.
- **Expect**: User remains on payment page; Order status remains "Unpaid"; Error message displayed.

---

## Suite: 6. User Center & My Activities
### TC-USER-001: My Registered Activities
- **Steps**:
  1. Navigate to "My Profile" -> "My Activities".
  2. Check list rendering based on user ID.
- **Expect**: List shows only activities relevant to the logged-in user.

### TC-USER-002: Check-in / QR Code
- **Steps**:
  1. Navigate to a specific registered activity.
  2. Click "Show Check-in QR Code".
  3. Verify Canvas rendering or image display.
- **Expect**: QR code is generated and visible; Long press to save works.

---

## Suite: 7. Custom Components Test
*Note: The project has 5 custom components. These should be tested in isolation or within pages.*

### TC-COMP-001: Component Interaction
- **Steps**:
  1. Identify a key custom component (e.g., a Calendar Picker or Ticket Selector).
  2. Trigger component events (e.g., select date).
  3. Verify event propagation to parent page.
- **Expect**: Component emits correct event details; Parent page handles the event logic correctly.
```