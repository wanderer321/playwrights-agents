# Test Plan: zhihui-workshop

## Overview
**Project Name**: zhihui-workshop
**Framework**: React
**Test Tool**: Playwright
**Description**: This application appears to be a smart workshop or service platform (likely B2C) offering services such as ID photo processing, poster creation, general photo editing, and order management. The test plan focuses on the core user modules identified in the test directory structure: Home, Hall, ID Photo, Photo, Poster, and Orders.

---

## Suite: Home Module (tests/home)
*Focus: Landing page, navigation, and user onboarding.*

### TC-HOME-001: Verify Home Page Loads Successfully
- **Steps**:
  1. Navigate to the root URL `/`.
  2. Wait for the page load state to be 'networkidle'.
- **Expect**: The home page renders correctly with the main header, footer, and navigation bar visible. No console errors are present.

### TC-HOME-002: Verify Navigation to Service Modules
- **Steps**:
  1. On the Home page, locate navigation links/buttons for 'ID Photo', 'Poster', and 'Photo'.
  2. Click on the 'ID Photo' entry point.
- **Expect**: Application navigates to the ID Photo module URL and renders the corresponding UI.

### TC-HOME-003: Check Responsiveness of Home Layout
- **Steps**:
  1. Set viewport to Desktop (1920x1080).
  2. Set viewport to Mobile (375x667).
- **Expect**: The layout adjusts without horizontal scrollbars on mobile, and key elements remain accessible.

---

## Suite: ID Photo Module (tests/idphoto)
*Focus: ID photo creation, background processing, and compliance.*

### TC-IDP-001: Upload Valid Image for ID Photo
- **Steps**:
  1. Navigate to the ID Photo page.
  2. Click the upload button.
  3. Select a valid JPG/PNG file from the fixture folder.
- **Expect**: The image uploads successfully and displays a preview/crop interface.

### TC-IDP-002: Verify Background Processing
- **Steps**:
  1. Upload an image with a non-standard background.
  2. Select a specific background color (e.g., Blue or White) from the options.
  3. Trigger the processing action.
- **Expect**: The application processes the image and the background changes to the selected color while preserving the subject.

### TC-IDP-003: Download Processed ID Photo
- **Steps**:
  1. Complete the ID photo processing (TC-IDP-002).
  2. Click the 'Download' button.
- **Expect**: The browser downloads the processed image file successfully.

### TC-IDP-004: Invalid File Type Upload
- **Steps**:
  1. Attempt to upload a non-image file (e.g., `.txt` or `.pdf`).
- **Expect**: The system displays an error message indicating invalid file format.

---

## Suite: Poster Module (tests/poster)
*Focus: Poster template selection, editing, and generation.*

### TC-PST-001: Select Poster Template
- **Steps**:
  1. Navigate to the Poster module.
  2. Browse the template gallery.
  3. Click on a specific template thumbnail.
- **Expect**: The template details page opens, allowing the user to preview or edit.

### TC-PST-002: Edit Text on Poster
- **Steps**:
  1. Select a template.
  2. Click on a text element within the poster editor.
  3. Input new text content.
- **Expect**: The text on the canvas updates in real-time to reflect the user's input.

### TC-PST-003: Save and Export Poster
- **Steps**:
  1. Make modifications to a poster.
  2. Click 'Save' or 'Export'.
- **Expect**: A high-resolution image or PDF is generated/downloaded successfully.

---

## Suite: Photo Module (tests/photo)
*Focus: General photo editing tools and filters.*

### TC-PHO-001: Apply Filter to Photo
- **Steps**:
  1. Navigate to the Photo module.
  2. Upload a sample photo.
  3. Select a filter (e.g., 'Grayscale' or 'Vintage') from the toolbar.
- **Expect**: The photo preview updates with the selected filter applied.

### TC-PHO-002: Adjust Brightness/Contrast
- **Steps**:
  1. Upload a photo.
  2. Use sliders to adjust brightness and contrast values.
- **Expect**: The image preview updates dynamically as sliders are moved.

---

## Suite: Orders Module (tests/orders)
*Focus: Order history, payment status, and transaction details.*

### TC-ORD-001: View Order History
- **Steps**:
  1. Navigate to the 'Orders' section.
  2. Verify the list of past orders is loaded.
- **Expect**: A list of orders is displayed, showing Order ID, Date, and Status.

### TC-ORD-002: Filter Orders by Status
- **Steps**:
  1. On the Orders page, select a status filter (e.g., 'Completed').
- **Expect**: The list updates to show only orders with 'Completed' status.

### TC-ORD-003: View Order Detail
- **Steps**:
  1. Click on a specific order row/item.
- **Expect**: A detail view or modal opens showing specific items purchased, total price, and download links (if applicable).

---

## Suite: Hall Module (tests/hall)
*Focus: Workshop hall, event listing, or service queue.*

### TC-HAL-001: Access Hall Page
- **Steps**:
  1. Navigate to the Hall URL.
  2. Check for the main container/component.
- **Expect**: The Hall page loads with active sessions or service items visible.

### TC-HAL-002: Interact with Hall Item
- **Steps**:
  1. Identify an active item/card in the Hall.
  2. Click the 'Join' or 'View' button.
- **Expect**: The user is redirected to the specific session or service detail page.