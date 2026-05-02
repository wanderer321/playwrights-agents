# Test Plan: zhihui-workshop

## Overview
**Project Name**: zhihui-workshop (智慧工坊)
**Framework**: React
**Test Tool**: Playwright
**Description**: Based on the project structure, this appears to be a smart workshop or photo processing service platform. It includes modules for a Hall (展厅/大厅), Home (首页), ID Photos (证件照), Photo Printing (照片打印), Poster creation (海报), and Order management (订单).

**Scope**: This test plan covers End-to-End (E2E) testing for the core user flows identified by the directory structure.

---

## Suite: Home Module (tests/home)
*Focus: Landing page, navigation, and user authentication entry points.*

### TC-HOME-001: Verify Home Page Load and Layout
- **Steps**:
  1. Navigate to the application root URL.
  2. Wait for the page load state to be 'networkidle'.
  3. Check for the presence of the header, footer, and main promotional banner.
- **Expect**: The home page renders correctly without console errors. Key navigation elements are visible.

### TC-HOME-002: Navigation to Service Modules
- **Steps**:
  1. On the Home page, locate the navigation menu.
  2. Click on the "ID Photo" (证件照) link.
  3. Verify URL change.
  4. Navigate back and click "Poster" (海报).
- **Expect**: Clicking links successfully routes the user to the correct modules (`/idphoto`, `/poster`) corresponding to the navigation items.

---

## Suite: ID Photo Module (tests/idphoto)
*Focus: Photo upload, background processing, and preview functionality.*

### TC-IDP-001: Upload Photo for ID Processing
- **Steps**:
  1. Navigate to the ID Photo module.
  2. Click the "Upload Photo" button.
  3. Select a valid JPG/PNG file from the test fixtures.
  4. Wait for the upload success indicator.
- **Expect**: The photo uploads successfully, and a preview of the uploaded image is displayed.

### TC-IDP-002: Change Background Color
- **Steps**:
  1. Assuming a photo is uploaded (Pre-condition).
  2. Select a background color option (e.g., Blue) from the color palette.
  3. Observe the preview area.
- **Expect**: The background of the photo in the preview updates to the selected color immediately.

### TC-IDP-003: Select Photo Specifications
- **Steps**:
  1. Open the specification dropdown/list.
  2. Select a specific size (e.g., "One Inch" / "一寸").
  3. Check the preview cropping.
- **Expect**: The photo is cropped/resized according to the "One Inch" specification standards.

---

## Suite: Photo Module (tests/photo)
*Focus: General photo printing and basic editing features.*

### TC-PHO-001: Batch Photo Upload
- **Steps**:
  1. Navigate to the Photo Printing module.
  2. Upload multiple image files simultaneously (e.g., 3 images).
- **Expect**: All 3 images are displayed in the upload list/queue with correct thumbnails.

### TC-PHO-002: Select Print Size and Quantity
- **Steps**:
  1. For an uploaded photo, select a print size (e.g., 4x6 inches).
  2. Set the print quantity to '2'.
  3. Verify the price calculation updates.
- **Expect**: The UI reflects the selected size and quantity, and the estimated price updates correctly.

---

## Suite: Poster Module (tests/poster)
*Focus: Template selection and poster customization.*

### TC-POS-001: Select Poster Template
- **Steps**:
  1. Navigate to the Poster module.
  2. Scroll through the template gallery.
  3. Click on a specific template to select it.
- **Expect**: The selected template loads into the editor canvas.

### TC-POS-002: Edit Text on Poster
- **Steps**:
  1. Select a template with text elements.
  2. Click on a text placeholder.
  3. Input new text: "Test Event 2024".
  4. Click outside or "Apply".
- **Expect**: The text on the poster preview updates to "Test Event 2024".

---

## Suite: Orders Module (tests/orders)
*Focus: Order creation, listing, and status verification.*

### TC-ORD-001: Create New Order
- **Steps**:
  1. Complete a workflow (e.g., ID Photo creation) to reach the "Confirm Order" page.
  2. Verify the item details and total price.
  3. Click "Submit Order".
- **Expect**: A new order ID is generated, and the user is redirected to the payment or order success page.

### TC-ORD-002: View Order History
- **Steps**:
  1. Navigate to the "My Orders" section.
  2. Verify the list of orders loads.
  3. Check the status of the most recent order.
- **Expect**: The order list displays past orders sorted by date. The most recent order status matches the created state (e.g., "Pending Payment").

---

## Suite: Hall Module (tests/hall)
*Focus: Workshop hall information or service center.*

### TC-HAL-001: View Hall Information
- **Steps**:
  1. Navigate to the Hall module.
  2. Check for the display of service categories or workshop information.
- **Expect**: The Hall page displays relevant service cards or information sections correctly.

### TC-HAL-002: Search Functionality (if applicable)
- **Steps**:
  1. Locate the search bar in the Hall section.
  2. Type a keyword related to a service.
  3. Press Enter.
- **Expect**: The results list filters to show only items matching the keyword.