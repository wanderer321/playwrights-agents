```markdown
# Test Plan: zhihui-workshop

## Overview
**Project Name**: zhihui-workshop
**Framework**: React
**Type**: Web Application (Workshop/Design Tool Platform)

Based on the project structure and directory analysis, `zhihui-workshop` appears to be a comprehensive design and utility platform. It offers specific tools for creating ID photos, editing general photos, and designing posters. The application also includes a "Hall" (likely a showcase or template gallery), a "Home" dashboard, and an "Orders" section for managing transactions or service requests. The test plan focuses on the core user journeys within these modules.

---

## Suite: Home Module
**Path**: `tests/home`
**Description**: Verifies the landing page, navigation, and user dashboard functionality.

### TC-HOME-001: Homepage Load and Layout
- **Steps**:
  1. Navigate to the application root URL.
  2. Wait for the page to fully load.
  3. Check for the presence of the header, footer, and main content area.
- **Expect**: The homepage renders correctly without layout shifts. Key navigation elements are visible.

### TC-HOME-002: Navigation to Feature Modules
- **Steps**:
  1. Locate the main navigation menu on the Home page.
  2. Click on the link/button for "ID Photo".
  3. Verify URL change.
  4. Repeat for "Poster", "Photo", and "Hall" links.
- **Expect**: Clicking each link successfully routes the user to the correct module URL.

### TC-HOME-003: User Session Check
- **Steps**:
  1. Open the application.
  2. Check the header for user login status (Avatar or "Login" button).
  3. If logged in, verify username is displayed.
- **Expect**: The application correctly reflects the user's authentication state.

---

## Suite: ID Photo Module
**Path**: `tests/idphoto`
**Description**: Tests the specialized workflow for creating and editing ID photos.

### TC-IDP-001: Photo Upload Functionality
- **Steps**:
  1. Navigate to the ID Photo module.
  2. Click the "Upload" button or drag-and-drop area.
  3. Select a valid JPG/PNG image from the local filesystem.
  4. Wait for the upload and preview to render.
- **Expect**: The image uploads successfully and displays a preview in the editor.

### TC-IDP-002: Background Processing/Removal
- **Steps**:
  1. Upload a photo with a non-uniform background.
  2. Trigger the "Background Removal" or "Change Background" feature.
  3. Wait for processing to complete.
- **Expect**: The background is removed or replaced with the selected color (e.g., White/Blue/Red) automatically.

### TC-IDP-003: ID Photo Specifications Selection
- **Steps**:
  1. Upload a photo.
  2. Select a specific size specification from the list (e.g., "1 inch", "2 inch", "Passport").
  3. Verify the crop area adjusts to the selected aspect ratio.
- **Expect**: The editor canvas updates to match the selected dimension constraints.

### TC-IDP-004: Download ID Photo
- **Steps**:
  1. Process an ID photo.
  2. Click the "Download" or "Save" button.
  3. Verify the downloaded file exists and format is correct.
- **Expect**: The processed image downloads successfully to the local device.

---

## Suite: Photo Editor Module
**Path**: `tests/photo`
**Description**: Tests general photo editing capabilities (filters, cropping, adjustments).

### TC-PHO-001: Basic Image Adjustment
- **Steps**:
  1. Navigate to the Photo module.
  2. Upload a sample image.
  3. Adjust "Brightness" or "Contrast" sliders.
  4. Observe the real-time preview.
- **Expect**: The image preview updates immediately to reflect the adjustment values.

### TC-PHO-002: Applying Filters
- **Steps**:
  1. Upload an image.
  2. Select a filter from the filter list (e.g., "Grayscale", "Vintage").
  3. Apply the filter.
- **Expect**: The selected filter effect is applied to the image canvas.

### TC-PHO-003: Crop and Rotate
- **Steps**:
  1. Upload an image.
  2. Select the "Crop" tool.
  3. Define a crop area.
  4. Apply the crop.
  5. Use the "Rotate" tool to rotate the image 90 degrees.
- **Expect**: The image dimensions and orientation update correctly after operations.

---

## Suite: Poster Design Module
**Path**: `tests/poster`
**Description**: Tests the poster design editor, including template usage and element manipulation.

### TC-POS-001: Template Selection
- **Steps**:
  1. Navigate to the Poster module.
  2. Browse the template gallery.
  3. Click on a specific template to load it into the editor.
- **Expect**: The editor loads with the canvas populated by the selected template elements.

### TC-POS-002: Text Element Editing
- **Steps**:
  1. Load a poster template.
  2. Click on a text element within the canvas.
  3. Modify the text content via the input field or inline editing.
  4. Change font size or color using the toolbar.
- **Expect**: The text on the canvas updates content and style immediately.

### TC-POS-003: Save Poster Project
- **Steps**:
  1. Make changes to a poster design.
  2. Click "Save" or "Export".
  3. Choose export format (e.g., PNG/JPG).
- **Expect**: The final design is exported correctly without quality loss.

---

## Suite: Hall Module
**Path**: `tests/hall`
**Description**: Tests the gallery or showcase functionality where users can view public works or templates.

### TC-HAL-001: Gallery List Rendering
- **Steps**:
  1. Navigate to the Hall page.
  2. Observe the grid/list layout of items.
  3. Scroll down to trigger lazy loading or pagination.
- **Expect**: Items load correctly. Scrolling triggers loading of subsequent items if pagination exists.

### TC-HAL-002: Search and Filter
- **Steps**:
  1. Locate the search bar on the Hall page.
  2. Enter a keyword (e.g., "Summer").
  3. Verify results.
  4. Apply a category filter (if available).
- **Expect**: The list updates to show only items matching the search criteria and filters.

---

## Suite: Orders Module
**Path**: `tests/orders`
**Description**: Tests the order management and transaction history features.

### TC-ORD-001: Order History Display
- **Steps**:
  1. Navigate to the Orders page (requires logged-in user).
  2. Verify the list of past orders is displayed.
  3. Check for essential details: Order ID, Date, Status, Amount.
- **Expect**: The order list loads and displays accurate historical data.

### TC-ORD-002: Order Detail View
- **Steps**:
  1. Click on a specific order item from the list.
  2. Verify the detail view expands or navigates to a detail page.
- **Expect**: Detailed information about the selected order (items, payment info) is visible.

### TC-ORD-003: Empty Order State
- **Steps**:
  1. Log in as a user with no transaction history (or mock empty state).
  2. Navigate to the Orders page.
- **Expect**: A friendly "No Orders" placeholder message and image are displayed.
```