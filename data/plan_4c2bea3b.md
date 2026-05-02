Based on the project information provided (Native WeChat Mini Program, 278 pages, named "pure-activity"), this appears to be a large-scale application, likely focused on event management, booking, or social activities.

Since the specific `app.json` content (page paths) was not provided, I have constructed a comprehensive test plan based on standard industry practices for "Activity/Event" type Mini Programs.

```markdown
# Test Plan: Pure Activity (pure-activity)

## Overview
- **Project Name**: pure-activity
- **Framework**: WeChat Native (原生)
- **Scale**: Large (278 Pages, 5 Components)
- **Testing Tool**: Minium
- **Strategy**: Given the large number of pages (278), this test plan prioritizes **Core Business Flows (P0)** and **WeChat Specific Features**. Full coverage requires modular regression testing.

---

## Suite: User Module (用户模块)
*Path Inference: pages/user/* or pages/mine/*

### TC-USER-001: WeChat Authorization Login
- **Steps**:
  1. Launch the Mini Program.
  2. Navigate to the "Profile/Mine" page.
  3. Click the "Login/Authorize" button.
  4. In the native popup, click "Allow".
- **Expect**: 
  - User avatar and nickname are displayed correctly.
  - `wx.getStorageSync('userInfo')` contains valid data.

### TC-USER-002: Get Mobile Number
- **Steps**:
  1. Navigate to the Account Binding or Settings page.
  2. Click the "Bind Phone Number" button.
  3. Trigger the `<button open-type="getPhoneNumber">` functionality.
  4. Click "Allow" in the system popup.
- **Expect**: 
  - The backend API successfully decrypts the mobile number.
  - The UI updates to show the masked phone number (e.g., 138****1234).

---

## Suite: Activity Module (活动核心模块)
*Path Inference: pages/index/*, pages/activity/*, pages/detail/*

### TC-ACT-001: Activity List Loading & Paging
- **Steps**:
  1. Launch the Mini Program to the Home/Activity List page.
  2. Verify the first page of data loads correctly.
  3. Scroll to the bottom of the page to trigger `onReachBottom`.
  4. Verify loading indicator appears and new data is appended.
- **Expect**: 
  - List renders without layout issues.
  - No duplicate data in the list.
  - "No more data" prompt appears when the list is exhausted.

### TC-ACT-002: Activity Detail Rendering
- **Steps**:
  1. Click on an item in the Activity List.
  2. Navigate to the Detail page (`onLoad` with ID).
  3. Verify Rich-text rendering (images, text) and countdown timers.
- **Expect**: 
  - Page title is set correctly.
  - Images load without 404 errors.
  - Activity status (e.g., "Not Started", "Ongoing", "Ended") is accurate.

### TC-ACT-003: Activity Sharing (WeChat Feature)
- **Steps**:
  1. On the Activity Detail page, click the top-right "..." menu or a specific "Share" button.
  2. Select "Share to Friends" (转发给朋友).
- **Expect**: 
  - The share card displays the correct Title, Image, and Path.
  - When a friend clicks the share card, they open the specific activity detail page.

---

## Suite: Booking & Order Module (报名与订单模块)
*Path Inference: pages/order/*, pages/booking/*

### TC-ORDER-001: Create Order Flow
- **Steps**:
  1. On the Activity Detail page, click "Sign Up" or "Buy Now".
  2. Fill in the required form fields (Name, Age, etc.).
  3. Click "Submit Order".
- **Expect**: 
  - Form validation works (checking empty fields, phone format).
  - Order is created in the database, and the user is redirected to the Payment or Order Detail page.

### TC-ORDER-002: WeChat Payment Integration
- **Steps**:
  1. Proceed to the Payment page.
  2. Click "Pay Now".
  3. Trigger `wx.requestPayment`.
  4. Enter password/Fingerprint in the WeChat payment popup.
- **Expect**: 
  - The WeChat Payment sheet appears with the correct amount.
  - Upon success, the order status updates to "Paid".
  - Upon cancellation, the order status remains "Unpaid".

---

## Suite: Location & Interaction (位置与交互)
*Path Inference: pages/map/* or components within detail*

### TC-LOC-001: Get User Location
- **Steps**:
  1. Navigate to the "Nearby Activities" or "Navigation" feature.
  2. Trigger `wx.getLocation` or `wx.authorize`.
  3. If prompted for permission, click "Allow".
- **Expect**: 
  - The map component centers on the user's current location.
  - If permission is denied, a friendly prompt guides the user to settings.

### TC-LOC-002: Navigate to Destination
- **Steps**:
  1. Click the "Navigation/Location" icon on an Activity Detail page.
  2. Trigger `wx.openLocation`.
- **Expect**: 
  - WeChat Maps open in full screen.
  - The destination pin matches the activity address.

---

## Suite: Component Testing (公共组件)
*Note: Project has 5 components.*

### TC-COMP-001: Custom Navbar Component
- **Steps**:
  1. Navigate through multiple pages that use the custom navbar.
  2. Test the "Back" button behavior.
  3. Test the "Home" button behavior.
- **Expect**: 
  - `mini.navigateBack` is called correctly.
  - If on the entry page, the back button should be hidden or navigate to Home.

### TC-COMP-002: Tab Bar Switching
- **Steps**:
  1. Click each item in the Tab Bar (e.g., Home, Activity, Mine).
  2. Verify page switching logic.
- **Expect**: 
  - Correct page is loaded.
  - Tab bar icon state toggles between active/inactive.

---

## Suite: Exception Handling (异常与边界)

### TC-ERR-001: Network Disconnect Handling
- **Steps**:
  1. Turn off phone network/WiFi.
  2. Launch the Mini Program or perform a pull-to-refresh.
- **Expect**: 
  - A "Network Error" or "Request Failed" toast/modal is displayed.
  - The app does not crash or show a white screen.

### TC-ERR-002: API Data Exception
- **Steps**:
  1. Mock an API response returning `null` or empty list for the Activity List.
- **Expect**: 
  - An "Empty State" component is displayed (e.g., "No activities found").
```