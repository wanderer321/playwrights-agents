```markdown
# Test Plan: pure-activity

## Overview
**Project Name**: pure-activity
**Framework**: WeChat Native (原生小程序)
**Scale**: 66 Pages, 5 Components
**Type**: Activity Management / Social Platform (Inferred from name)

This test plan outlines the strategy for testing the "pure-activity" WeChat Mini Program using the Minium automation framework. Given the large number of pages (66), this plan prioritizes core business flows and WeChat-specific integrations. The testing scope includes user authentication, activity lifecycle management, payment integration, and social sharing features.

**Key Testing Areas**:
- User Login & Authorization (WeChat specific)
- Activity Browsing & Search
- Activity Registration & Payment (WeChat Pay)
- User Center & Order Management
- Social Sharing & Forwarding

---

## Suite: 01 - User Authentication & Authorization
*Focus: WeChat login flow and user info handling.*

### TC-AUTH-001: WeChat Silent Login
- **Steps**:
  1. Launch the Mini Program for the first time (clear storage).
  2. Observe the network request for `wx.login` code.
  3. Check if the user is redirected to the home page or a welcome page without manual intervention.
- **Expect**: The app obtains a session token automatically; user can view public content without explicit authorization.

### TC-AUTH-002: User Profile Authorization (GetUserInfo)
- **Steps**:
  1. Navigate to a feature requiring user info (e.g., "My Profile" or "Publish Activity").
  2. Trigger the button with `open-type="getUserInfo"`.
  3. In the simulated WeChat environment, allow the authorization.
  4. Verify the UI updates with the user's WeChat nickname and avatar.
- **Expect**: Authorization popup appears; upon confirmation, user info is displayed correctly in the UI.

### TC-AUTH-003: Mobile Number Binding
- **Steps**:
  1. Go to "Settings" or "Account Security".
  2. Click "Bind Phone Number".
  3. Trigger button with `open-type="getPhoneNumber"`.
  4. Verify the encrypted data is sent to the backend and the phone number is masked/displayed.
- **Expect**: Phone number successfully bound; UI reflects the updated status.

---

## Suite: 02 - Activity Browsing & Discovery (Home Module)
*Focus: Core navigation, list rendering, and filtering.*

### TC-HOME-001: Activity List Rendering
- **Steps**:
  1. Launch the app and land on the home page.
  2. Check if the activity list loads default data.
  3. Scroll down to trigger `onReachBottom` (pagination).
- **Expect**: Activity cards display image, title, date, and location; loading more data works without duplication or crash.

### TC-HOME-002: Activity Search
- **Steps**:
  1. Tap the search bar.
  2. Input a keyword (e.g., "Hiking").
  3. Submit the search.
- **Expect**: List refreshes with results matching the keyword; empty state is shown if no results found.

### TC-HOME-003: Activity Category Filtering
- **Steps**:
  1. Tap on different category tabs (e.g., "Sports", "Social", "Workshop").
  2. Verify the request parameters change according to the tab.
- **Expect**: List content updates to match the selected category.

---

## Suite: 03 - Activity Detail & Registration
*Focus: Detailed view and WeChat specific location features.*

### TC-DETAIL-001: View Activity Detail
- **Steps**:
  1. Click on an activity card from the list.
  2. Verify page elements: Banner image, Description, Time, Location map, Organizer info.
- **Expect**: All data renders correctly; no layout overflow issues.

### TC-DETAIL-002: Location & Navigation (WeChat Map)
- **Steps**:
  1. Find the location section in the detail page.
  2. Click the "Navigate" or "View Map" button.
  3. Verify `wx.openLocation` is called.
- **Expect**: WeChat map opens showing the specific latitude/longitude; navigation controls are available.

### TC-DETAIL-003: Activity Registration Flow
- **Steps**:
  1. Click "Register" or "Join" button.
  2. Fill in required fields (Name, Phone, custom fields).
  3. Submit the form.
- **Expect**: Form validation works (checks empty/invalid inputs); submission triggers the payment flow or success message.

---

## Suite: 04 - Payment Module
*Focus: WeChat Pay integration.*

### TC-PAY-001: WeChat Pay Invocation
- **Steps**:
  1. Proceed to checkout/payment page from registration.
  2. Click "Pay Now".
  3. Verify the parameters passed to `wx.requestPayment`.
- **Expect**: WeChat Payment modal appears (or simulated success in test env); correct amount is displayed.

### TC-PAY-002: Payment Success Handling
- **Steps**:
  1. Complete a successful payment (mock or sandbox).
  2. Verify redirection to the "Payment Success" page.
  3. Check the order status in "My Orders".
- **Expect**: Order status updates to "Paid"; user receives a success notification or template message.

### TC-PAY-003: Payment Cancellation/Failure
- **Steps**:
  1. Initiate payment.
  2. Click "Cancel" on the WeChat Payment interface.
- **Expect**: App handles the cancel callback gracefully; UI shows "Payment Unpaid" or allows retry; no crash occurs.

---

## Suite: 05 - User Center & Social Sharing
*Focus: User data management and WeChat sharing.*

### TC-USER-001: My Orders/Activities
- **Steps**:
  1. Navigate to "User Center" page.
  2. Click "My Registrations" or "My Orders".
  3. Verify the list shows activities the user has joined.
- **Expect**: Correct historical data is displayed; status (Pending, Paid, Completed) is accurate.

### TC-SHARE-001: Share to Friends (Forward)
- **Steps**:
  1. On an Activity Detail page, click the "Share" button (or top right menu -> Forward).
  2. Verify `onShareAppMessage` configuration.
- **Expect**: Share card displays correct title, image, and path; recipient can click the card to open the specific activity page.

### TC-SHARE-002: Share to Timeline (Moments)
- **Steps**:
  1. On Activity Detail page, click "Share to Timeline".
  2. Verify `onShareTimeline` configuration.
- **Expect**: Single page mode is enabled; user can post the activity card to their WeChat Moments.

---

## Suite: 06 - Exception & Compatibility
*Focus: Network handling and permission denial.*

### TC-EXC-001: Network Disconnection
- **Steps**:
  1. Disable network connection in the developer tools/simulator.
  2. Launch the app or perform a pull-to-refresh.
- **Expect**: App shows a "No Network" placeholder or toast; app does not crash.

### TC-EXC-002: Location Permission Denial
- **Steps**:
  1. Trigger a feature requiring location (`wx.getLocation`).
  2. Deny the permission request in the popup.
- **Expect**: App shows a friendly prompt explaining why location is needed and guides user to settings, rather than crashing or freezing.
```