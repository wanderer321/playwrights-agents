```markdown
# Test Plan: 宠物纪

## Overview
- **Project Name**: 宠物纪
- **Project Path**: D:\ShiGoTo\宠物纪
- **Framework**: WeChat Native (原生小程序)
- **Scale**: Large (247 Pages, 3 Components)
- **Testing Tool**: Minium

**Summary**:
"宠物纪" is a large-scale native WeChat Mini Program focused on pet-related services. Given the high page count (247 pages), the application likely covers a wide range of complex business modules including pet social circles, e-commerce (pet supplies), service appointments (grooming/medical), and pet management tools.

This test plan prioritizes core business flows and WeChat-specific integration points (Login, Payment, Sharing, Location) suitable for automation with Minium.

---

## Suite: User Module (用户模块)
Focus: WeChat authorization, user identity, and profile management.

### TC-USER-001: WeChat Login & Authorization
- **Steps**:
  1. Launch the Mini Program.
  2. Detect if the user is logged in.
  3. If not logged in, trigger the `wx.getUserProfile` or dedicated login button.
  4. Mock/Handle the WeChat authorization pop-up (allowing access).
  5. Verify redirection to the homepage or user profile page.
- **Expect**: User is successfully logged in; User avatar and nickname are displayed correctly; Session token is stored.

### TC-USER-002: User Profile Update
- **Steps**:
  1. Navigate to the User Profile page.
  2. Click the "Edit Profile" button.
  3. Modify the nickname or pet information.
  4. Click "Save".
- **Expect**: Changes are saved successfully; UI updates immediately to reflect changes.

---

## Suite: Pet Management Module (宠物档案模块)
Focus: Core business logic for managing pet records.

### TC-PET-001: Add New Pet Profile
- **Steps**:
  1. Navigate to "My Pets" section.
  2. Click the "Add Pet" button (usually a '+' icon).
  3. Input Pet Name (e.g., "Lucky").
  4. Select Pet Type and Breed from pickers.
  5. Upload a photo using `wx.chooseImage` (Mock selection).
  6. Submit the form.
- **Expect**: New pet card appears in the list; Photo is uploaded and displayed; No JS errors in console.

### TC-PET-002: Edit Pet Details
- **Steps**:
  1. Select an existing pet card.
  2. Click "Edit".
  3. Change the weight or birthday.
  4. Save changes.
- **Expect**: Pet details are updated; History log (if applicable) records the change.

---

## Suite: E-Commerce Module (商城模块)
Focus: Product browsing, cart management, and WeChat Payment integration.

### TC-SHOP-001: Product Search and View
- **Steps**:
  1. Navigate to the "Mall" (商城) tab.
  2. Use the search bar to input "Dog Food".
  3. Select a product from the list.
- **Expect**: Search results match keywords; Product detail page loads correct price, description, and images.

### TC-SHOP-002: Add to Cart and Purchase Flow
- **Steps**:
  1. On a Product Detail Page, select specifications (flavor/size).
  2. Click "Add to Cart".
  3. Navigate to Cart page.
  4. Select the item and click "Checkout".
  5. Select shipping address.
  6. Click "Submit Order".
- **Expect**: Order is created; System redirects to payment interface.

### TC-SHOP-003: WeChat Payment Integration
- **Steps**:
  1. Proceed from the Order Confirmation page.
  2. Trigger `wx.requestPayment`.
  3. In the test environment, mock the payment success callback.
  4. Verify the order status changes to "Paid" or "Pending Shipment".
- **Expect**: Payment success message received; Order status updates correctly in the database/UI.

---

## Suite: Service Appointment Module (服务预约模块)
Focus: Location services and booking logic.

### TC-SVC-001: Nearby Services (Location Authorization)
- **Steps**:
  1. Navigate to "Services" or "Nearby" section.
  2. Trigger `wx.getLocation` or `wx.authorize('scope.userLocation')`.
  3. Allow location access.
- **Expect**: Map loads centered on user's current location; List of nearby pet stores/hospitals is displayed sorted by distance.

### TC-SVC-002: Book Grooming Service
- **Steps**:
  1. Select a service provider from the list.
  2. Choose a service type (e.g., "Bathing").
  3. Select an available time slot on the calendar.
  4. Confirm booking.
- **Expect**: Booking is recorded; Confirmation notification is triggered (or visible in 'My Orders').

---

## Suite: Social & Sharing Module (社区与分享模块)
Focus: WeChat specific sharing features and content interaction.

### TC-SOC-001: Share Content to WeChat Chat
- **Steps**:
  1. Navigate to a specific article or pet dynamic.
  2. Click the "Share" button (top right menu or specific button).
  3. Trigger `onShareAppMessage`.
  4. Simulate sharing to a friend/group.
- **Expect**: Share card displays correct title, image, and path; Mini Program can be opened via the shared card.

### TC-SOC-002: Post New Dynamic (Image Upload)
- **Steps**:
  1. Click "Post" or "+" button in the community section.
  2. Select images from album (`wx.chooseImage`).
  3. Enter text content.
  4. Click "Publish".
- **Expect**: Post appears in the community feed; Images are rendered correctly; Likes/Comments function works.

---

## Suite: Address Management (地址管理)
Focus: Address CRUD operations.

### TC-ADDR-001: WeChat Address Import
- **Steps**:
  1. Go to "My Addresses".
  2. Click "Import from WeChat" (`wx.chooseAddress`).
  3. Authorize and select an address.
- **Expect**: Address fields (Name, Phone, Region, Detail) are populated automatically.

### TC-ADDR-002: Manual Address Entry
- **Steps**:
  1. Click "Add New Address".
  2. Fill in Name, Phone number.
  3. Use Region Picker to select City/District.
  4. Save.
- **Expect**: Address saved successfully; Validation works for empty fields or invalid phone numbers.
```