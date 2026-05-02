```markdown
# Test Plan: 宠物纪

## Overview
- **Project Name**: 宠物纪
- **Project Path**: D:\ShiGoTo\宠物纪
- **Framework**: 原生微信小程序
- **Scale**: Large (249 Pages, 3 Components)
- **Testing Tool**: Minium

**Summary**:
"宠物纪" is a large-scale native WeChat Mini Program. Given the high page count (249 pages), the application likely covers comprehensive business scenarios including pet management, e-commerce (pet supplies), community/social features, and service appointments (grooming/veterinary).

**Test Strategy**:
Due to the large scale, this test plan prioritizes core business paths and WeChat-specific functionalities. Testing will be modularized into:
1.  **User Module**: Login, Authorization, Profile.
2.  **Pet Management Module**: Core business logic.
3.  **Mall/Order Module**: Product browsing, Cart, Payment.
4.  **Community Module**: Posts, Comments, Sharing.
5.  **Service/Location Module**: Nearby services, Map usage.

---

## Suite: User Module (用户模块)
**Focus**: WeChat Authorization, User State Management.

### TC-USER-001: WeChat One-Click Login
- **Steps**:
  1. Launch the Mini Program.
  2. Check if the login state exists.
  3. If not logged in, trigger the login button.
  4. Mock/Handle the `wx.login` API callback.
  5. Verify if the user avatar and nickname are displayed on the profile page.
- **Expect**: User successfully logs in; token is stored; UI updates with user info.

### TC-USER-002: User Profile Update
- **Steps**:
  1. Navigate to the "Me" (Profile) page.
  2. Click "Edit Profile".
  3. Modify the user's nickname or avatar.
  4. Save changes.
- **Expect**: Profile data updates successfully; changes persist after re-launching the app.

### TC-USER-003: Get Phone Number Authorization
- **Steps**:
  1. Navigate to the phone number binding page.
  2. Click the "Get Phone Number" button.
  3. Simulate the popup for phone number authorization (Allow).
  4. Verify the backend receives the encrypted data and decrypts the number.
- **Expect**: Phone number is successfully bound to the account.

---

## Suite: Pet Management Module (宠物档案模块)
**Focus**: Core business data CRUD operations.

### TC-PET-001: Add New Pet Profile
- **Steps**:
  1. Navigate to "My Pets" list.
  2. Click the "Add Pet" button.
  3. Fill in required details: Name, Type (Dog/Cat), Breed, Birthday.
  4. Upload a photo (Test image upload component).
  5. Click "Save".
- **Expect**: New pet card appears in the list; data matches input.

### TC-PET-002: Edit Pet Information
- **Steps**:
  1. Select an existing pet from the list.
  2. Click "Edit".
  3. Change the weight or age.
  4. Save changes.
- **Expect**: Pet details are updated on the detail page and list page.

---

## Suite: Mall & Order Module (商城与订单模块)
**Focus**: Shopping flow, WeChat Payment.

### TC-MALL-001: Product Search and Filter
- **Steps**:
  1. Navigate to the "Mall" tab.
  2. Enter "Dog Food" in the search bar.
  3. Verify search results list.
  4. Apply a price filter (e.g., Low to High).
- **Expect**: List displays relevant products; list is sorted correctly by price.

### TC-MALL-002: Add to Cart and Purchase
- **Steps**:
  1. Select a product from the list.
  2. Select specifications (flavor, weight).
  3. Click "Add to Cart".
  4. Navigate to Cart page.
  5. Select the item and click "Checkout".
- **Expect**: Item is added to cart; Checkout page shows correct total price.

### TC-MALL-003: WeChat Payment Integration
- **Steps**:
  1. Proceed from Checkout to Payment.
  2. Invoke `wx.requestPayment`.
  3. **Mock**: Simulate successful payment callback (if testing in sandbox/mock environment).
  4. Verify redirection to the "Payment Success" page.
  5. Check order status in "My Orders".
- **Expect**: Payment interface is called; Order status changes to "Paid".

---

## Suite: Community Module (社区模块)
**Focus**: UGC (User Generated Content), WeChat Sharing.

### TC-COM-001: Publish New Post
- **Steps**:
  1. Navigate to Community page.
  2. Click "+" or "Publish" button.
  3. Input text content.
  4. Select images from local album.
  5. Submit the post.
- **Expect**: Post appears in the community feed immediately; Images load correctly.

### TC-COM-002: Share Post to WeChat Chat
- **Steps**:
  1. Open a specific post detail page.
  2. Click the "Share" button (or trigger `onShareAppMessage` via menu).
  3. Select a recent chat or create a mock share action.
- **Expect**: Share card is generated with correct title and image; Navigation to shared page works correctly.

---

## Suite: Service & Location Module (服务与位置模块)
**Focus**: WeChat Location API, Maps.

### TC-SVC-001: Nearby Services (Location Authorization)
- **Steps**:
  1. Navigate to "Nearby Services" or "Grooming" module.
  2. Trigger `wx.getLocation` or `wx.authorize('scope.userLocation')`.
  3. Allow location access.
  4. Verify the map centers on the user's current location.
- **Expect**: Map displays current location; Nearby stores list is populated based on location.

### TC-SVC-002: Navigate to Store
- **Steps**:
  1. Select a store from the "Nearby" list.
  2. Click "Navigate" or "View on Map".
  3. Check if map markers are set correctly.
- **Expect**: Map shows store location; Distance calculation is displayed.

---

## Suite: Exception Handling (异常与兼容性)
**Focus**: Network errors, Permission denials.

### TC-ERR-001: Network Disconnection Handling
- **Steps**:
  1. Disable network connection on the testing device/simulator.
  2. Launch the Mini Program or perform an action requiring API call.
- **Expect**: App shows a "No Network" placeholder or toast message; App does not crash.

### TC-ERR-002: Location Permission Denied
- **Steps**:
  1. Clear location permissions.
  2. Navigate to a feature requiring location.
  3. Click "Deny" on the authorization popup.
- **Expect**: App shows a friendly prompt guiding the user to enable permissions in settings; App functions in a degraded mode (e.g., manual location entry).
```