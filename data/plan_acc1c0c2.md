```markdown
# Test Plan: zhihui-workshop

## Overview
**Project Name**: zhihui-workshop (智慧工坊)
**Framework**: React
**Test Tool**: Playwright

**Application Summary**:
Based on the project structure and directory names, `zhihui-workshop` appears to be a comprehensive digital workshop platform. It focuses on image processing and document generation services. The core modules identified include:
1.  **Home**: The landing page or main dashboard.
2.  **Hall (大厅)**: A service lobby or portal where users can select different tools.
3.  **ID Photo (证件照)**: A specialized tool for creating/composing ID photos.
4.  **Photo (照片)**: General photo processing or gallery features.
5.  **Poster (海报)**: A tool for designing or generating posters.
6.  **Orders (订单)**: Order management and history viewing.

This test plan outlines the E2E (End-to-End) testing strategy to ensure functional stability and user flow integrity across these modules.

---

## Suite: Home Module (tests/home)
*Focus: Landing page stability, navigation, and user session handling.*

### TC-HOME-001: Verify Home Page Load and Layout
- **Steps**:
  1. Navigate to the root URL `/`.
  2. Wait for the page load state to be 'networkidle'.
  3. Check for the presence of the main header, navigation bar, and footer.
- **Expect**: The home page renders correctly without console errors. Key UI elements (Logo, Navigation Menu) are visible.

### TC-HOME-002: Navigation to Service Hall
- **Steps**:
  1. On the Home page, locate the "Enter Hall" or "Start Service" button.
  2. Click the button.
  3. Verify the URL changes to the Hall path.
- **Expect**: User is successfully redirected to the Hall module.

---

## Suite: Hall Module (tests/hall)
*Focus: Service selection and entry point to specific tools.*

### TC-HALL-001: Display Service Categories
- **Steps**:
  1. Navigate to the Hall page.
  2. Verify that service cards or list items are rendered.
  3. Check for specific entries: "ID Photo", "Poster", "Photo Processing".
- **Expect**: All service categories defined in the application configuration are displayed correctly with valid thumbnails and titles.

### TC-HALL-002: Access ID Photo Service
- **Steps**:
  1. Locate the "ID Photo" (证件照) card/button.
  2. Click the element.
  3. Verify navigation to the ID Photo module.
- **Expect**: The ID Photo tool interface loads successfully.

---

## Suite: ID Photo Module (tests/idphoto)
*Focus: Core business logic for ID photo generation.*

### TC-IDP-001: Upload Photo for Processing
- **Steps**:
  1. Navigate to the ID Photo module.
  2. Click the "Upload" button.
  3. Use `setInputFiles` to upload a sample JPG/PNG file.
  4. Wait for the upload success indicator or preview image.
- **Expect**: The image is uploaded successfully, and a preview is displayed to the user.

### TC-IDP-002: Change Background Color
- **Steps**:
  1. Assuming a photo is uploaded (Pre-condition).
  2. Select a background color option (e.g., Blue, Red, White) from the UI.
  3. Observe the preview area.
- **Expect**: The background of the photo in the preview updates to the selected color immediately.

### TC-IDP-003: Download Processed ID Photo
- **Steps**:
  1. Complete the photo editing (upload + background change).
  2. Click the "Download" or "Save" button.
  3. Verify the download behavior (either direct download or navigation to a payment/order confirmation).
- **Expect**: The processed file is downloaded to the local system, or the user is directed to the order confirmation page.

---

## Suite: Poster Module (tests/poster)
*Focus: Template selection and poster generation.*

### TC-POST-001: Select Poster Template
- **Steps**:
  1. Navigate to the Poster module.
  2. Scroll through the template list.
  3. Click on a specific template thumbnail.
- **Expect**: The template details page opens, showing a preview and editable areas.

### TC-POST-002: Edit Text Content
- **Steps**:
  1. Inside a selected template, click on a text placeholder.
  2. Clear existing text and input new text: "Test Event 2024".
  3. Click "Apply" or outside the text box.
- **Expect**: The text on the poster preview updates to reflect the new input.

---

## Suite: Orders Module (tests/orders)
*Focus: Transaction history and status verification.*

### TC-ORD-001: View Order History
- **Steps**:
  1. Navigate to the Orders page.
  2. Verify the list of past orders is loaded.
  3. Check for pagination or infinite scroll if applicable.
- **Expect**: A list of previous orders is displayed, sorted by date (newest first).

### TC-ORD-002: Filter Orders by Status
- **Steps**:
  1. On the Orders page, locate the filter dropdown/tab.
  2. Select a status (e.g., "Completed" or "Pending").
  3. Verify the list updates.
- **Expect**: Only orders matching the selected status are displayed in the list.

---

## Suite: Photo Module (tests/photo)
*Focus: General photo management and editing.*

### TC-PHOTO-001: Basic Photo Editing
- **Steps**:
  1. Navigate to the Photo module.
  2. Upload a test image.
  3. Apply a basic filter or crop operation.
  4. Save changes.
- **Expect**: The edit is applied to the preview, and changes are saved successfully without performance lag.

---

## Suite: Cross-Browser & Responsiveness
*Focus: Ensuring compatibility across environments.*

### TC-COMPAT-001: Mobile Viewport Responsiveness
- **Steps**:
  1. Configure Playwright to use `isMobile: true` or set viewport to 375x667.
  2. Navigate through Home -> Hall -> ID Photo.
  3. Check for layout shifts or hidden buttons.
- **Expect**: All pages are responsive. Navigation menus collapse into a hamburger menu if necessary, and core functions remain accessible.

### TC-COMPAT-002: Cross-Browser Execution
- **Steps**:
  1. Run the critical path (TC-HOME-001 -> TC-HALL-002 -> TC-IDP-001) on Chromium, WebKit, and Firefox.
- **Expect**: All tests pass consistently across the three browser engines.
```