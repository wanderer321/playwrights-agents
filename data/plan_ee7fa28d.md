# Test Plan: zhihui-workshop

## Overview
**Project Name:** zhihui-workshop
**Framework:** React
**Test Tool:** Playwright

This application appears to be a smart workshop platform (likely "智慧工坊") focusing on image processing and printing services. Based on the directory structure (`idphoto`, `poster`, `photo`, `orders`), the core business involves:
1.  **Image Processing:** ID photo creation, poster design, general photo processing.
2.  **Service Management:** Ordering and tracking services.
3.  **User Interaction:** Home dashboard and a "Hall" (lobby) area.

The test plan prioritizes user flows critical to the business logic: uploading photos, processing them (ID/Poster), and managing the resulting orders.

---

## Suite: Home Module
**Path:** `tests/home`
**Description:** Verifies the landing page, navigation, and user authentication state.

### TC-HOME-001: Home Page Load and Layout
- **Steps**:
  1. Navigate to the root URL `/`.
  2. Wait for the page load state to be 'networkidle'.
- **Expect**:
  - The home page renders successfully.
  - Key navigation elements (Header, Footer, Menu) are visible.
  - No console errors are detected.

### TC-HOME-002: Navigation to Service Modules
- **Steps**:
  1. On the Home page, locate the navigation link for "ID Photo" (or relevant menu item).
  2. Click the link.
- **Expect**:
  - URL changes to the ID Photo module path.
  - Correct component/container loads for the ID Photo service.

---

## Suite: ID Photo Module
**Path:** `tests/idphoto`
**Description:** Tests the core ID photo creation flow, including upload, background processing, and preview.

### TC-ID-001: Photo Upload Functionality
- **Steps**:
  1. Navigate to the ID Photo module.
  2. Click the "Upload" button or drag-and-drop area.
  3. Use `page.setInputFiles` to upload a test image fixture (e.g., `portrait.jpg`).
- **Expect**:
  - Upload progress bar appears (if applicable).
  - Image preview is displayed on the canvas/edit area.
  - No "Upload Failed" error messages.

### TC-ID-002: Background Color Switching
- **Steps**:
  1. Precondition: An image is uploaded (TC-ID-001).
  2. Locate background color options (e.g., Blue, Red, White).
  3. Click on the "Blue" color option.
- **Expect**:
  - The background of the photo updates to Blue immediately.
  - The foreground (person) remains unaffected (segmentation integrity).

### TC-ID-003: Photo Download/Save
- **Steps**:
  1. Precondition: Photo is processed with desired background.
  2. Click the "Save" or "Download" button.
- **Expect**:
  - Browser download event is triggered.
  - Downloaded file name matches expected pattern.
  - (Optional) User is redirected to the Orders page.

---

## Suite: Poster Module
**Path:** `tests/poster`
**Description:** Validates the poster design editor tools and rendering.

### TC-POSTER-001: Template Selection
- **Steps**:
  1. Navigate to the Poster module.
  2. Scroll through the template gallery.
  3. Click on a specific template thumbnail.
- **Expect**:
  - The editor loads the selected template layout.
  - Placeholder elements (text, images) are visible in the correct positions.

### TC-POSTER-002: Text Editing in Poster
- **Steps**:
  1. Load a template.
  2. Double-click on a text element.
  3. Clear existing text and type "Test Event Name".
  4. Click outside the text box to deselect.
- **Expect**:
  - Text box enters edit mode.
  - The text updates to "Test Event Name".
  - Text auto-resizes or wraps correctly within the boundary.

---

## Suite: Photo Module
**Path:** `tests/photo`
**Description:** General photo management and album features.

### TC-PHOTO-001: Gallery View Pagination
- **Steps**:
  1. Navigate to the Photo/Album section.
  2. Verify the number of items on the first page.
  3. If pagination exists, click "Next" or scroll to bottom.
- **Expect**:
  - Photos load in a grid layout.
  - Lazy loading or pagination functions correctly without breaking layout.

### TC-PHOTO-002: Photo Deletion
- **Steps**:
  1. Select a photo from the gallery (checkbox or click).
  2. Click the "Delete" icon.
  3. Confirm the deletion in the modal dialog.
- **Expect**:
  - Photo is removed from the list.
  - A "Success" toast message appears.

---

## Suite: Orders Module
**Path:** `tests/orders`
**Description:** Order history, status tracking, and payment verification.

### TC-ORDER-001: Order List Display
- **Steps**:
  1. Navigate to the "My Orders" page.
  2. Verify the list container is visible.
- **Expect**:
  - Past orders are listed in reverse chronological order.
  - Each order card shows Order ID, Date, Status, and Thumbnail.

### TC-ORDER-002: Order Detail View
- **Steps**:
  1. Click on a specific order item in the list.
- **Expect**:
  - A detail page or modal opens.
  - Detailed information (Payment method, Delivery address, Price) matches the summary.

---

## Suite: Hall Module
**Path:** `tests/hall`
**Description:** Likely a public lobby, event hall, or service selection entry point.

### TC-HALL-001: Hall Entry Access
- **Steps**:
  1. Navigate to the Hall URL.
  2. Check for active sessions or public banners.
- **Expect**:
  - Hall page loads public resources.
  - If it's an event hall, current active events are displayed.

### TC-HALL-002: Service Navigation from Hall
- **Steps**:
  1. Locate a "Quick Link" or service card in the Hall.
  2. Click the link.
- **Expect**:
  - Navigation triggers successfully to the target service (e.g., ID Photo or Poster).