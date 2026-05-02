```markdown
# Test Plan: zhihui-workshop

## Overview
**Project Name**: zhihui-workshop
**Framework**: React
**Test Tool**: Playwright
**Description**: This project appears to be a "Smart Workshop" (Zhihui) platform, likely offering services related to photo processing, ID photo generation, poster creation, and order management. The application seems to be a consumer-facing web application with specific functional modules.

**Test Scope**: The test plan covers the core user-facing modules identified in the test directory structure: Home, Hall, ID Photo, Orders, Photo, and Poster.

---

## Suite: Home Module (tests/home)
*Focus: Landing page functionality, navigation, and user session entry.*

### TC-HOME-001: Verify Home Page Load and Layout
- **Steps**:
  1. Navigate to the root URL of the application.
  2. Wait for the page to reach the 'networkidle' state.
  3. Check for the visibility of the main navigation bar.
  4. Check for the visibility of the footer section.
- **Expect**: The home page loads successfully without JavaScript errors. Navigation bar and footer are visible and correctly aligned.

### TC-HOME-002: Verify Navigation to Core Modules
- **Steps**:
  1. On the Home page, locate the navigation link for 'ID Photo' (or relevant menu item).
  2. Click the link.
  3. Verify the URL changes to the ID Photo route.
  4. Navigate back to Home.
  5. Repeat for 'Poster' and 'Orders' links.
- **Expect**: Clicking navigation links directs the user to the correct module URLs. The browser history functions correctly (back button works).

---

## Suite: ID Photo Module (tests/idphoto)
*Focus: ID photo creation workflow, including upload, background processing, and preview.*

### TC-IDP-001: Upload Image for ID Photo
- **Steps**:
  1. Navigate to the ID Photo module.
  2. Click the 'Upload' button or drag-and-drop area.
  3. Select a valid JPG/PNG image file from the local filesystem using Playwright's `setInputFiles`.
  4. Wait for the upload success indicator or preview image to appear.
- **Expect**: The file uploads successfully. A preview of the uploaded image is displayed on the canvas/screen.

### TC-IDP-002: Change Background Color
- **Steps**:
  1. Assuming an image is already uploaded (Pre-condition).
  2. Locate the background color options (e.g., Blue, White, Red).
  3. Select 'Blue' background.
  4. Observe the preview area.
- **Expect**: The background of the ID photo in the preview updates to the selected color (Blue) without distorting the subject.

### TC-IDP-003: Download Processed ID Photo
- **Steps**:
  1. Process an ID photo with a specific background.
  2. Click the 'Download' or 'Save' button.
  3. Verify the download event is triggered.
- **Expect**: The processed image file downloads successfully to the designated download path.

---

## Suite: Poster Module (tests/poster)
*Focus: Poster template selection, customization, and generation.*

### TC-PST-001: Select Poster Template
- **Steps**:
  1. Navigate to the Poster module.
  2. Verify a grid of poster templates is displayed.
  3. Click on a specific template thumbnail.
- **Expect**: The template details page or editor opens, displaying the selected template ready for editing.

### TC-PST-002: Edit Poster Text Content
- **Steps**:
  1. Inside the Poster editor, click on a text element.
  2. Clear existing text and input "Test Poster Title".
  3. Click outside the text box or 'Apply' button.
- **Expect**: The text on the poster preview updates to display "Test Poster Title".

---

## Suite: Orders Module (tests/orders)
*Focus: Order history viewing, status checks, and transaction details.*

### TC-ORD-001: View Order List
- **Steps**:
  1. Navigate to the Orders module.
  2. Verify the presence of the order list container.
  3. Check if pagination or infinite scroll controls exist.
- **Expect**: A list of historical orders is displayed. If no orders exist, a "No Orders" placeholder is shown.

### TC-ORD-002: Filter Orders by Status
- **Steps**:
  1. On the Orders page, locate the status filter (e.g., All, Completed, Pending).
  2. Select 'Completed'.
- **Expect**: The list refreshes to show only orders with 'Completed' status.

---

## Suite: Photo Module (tests/photo)
*Focus: General photo editing or gallery features.*

### TC-PHT-001: Basic Photo Edit Operation
- **Steps**:
  1. Navigate to the Photo module.
  2. Upload a sample image.
  3. Apply a basic filter (e.g., 'Grayscale' or 'Crop').
  4. Verify the preview updates.
- **Expect**: The applied effect is immediately reflected in the photo preview.

---

## Suite: Hall Module (tests/hall)
*Focus: Exhibition hall or showcase feature.*

### TC-HAL-001: Hall Entry Display
- **Steps**:
  1. Navigate to the Hall module URL.
  2. Verify the main banner or title is visible.
  3. Scroll down to check content loading.
- **Expect**: The Hall page renders correctly with all assets (images/text) loaded. No console errors regarding missing resources.
```