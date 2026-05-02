# Test Plan: zhihui-workshop

## Overview
**Project Name**: zhihui-workshop (智慧车间)
**Framework**: React
**Test Tool**: Playwright

This application appears to be a comprehensive workshop/service platform, likely involving image processing and order management. Based on the directory structure (`home`, `hall`, `idphoto`, `photo`, `poster`, `orders`), the application allows users to manage photos, create ID photos, design posters, and handle corresponding orders.

The test plan focuses on the core business modules identified in the `tests` directory, ensuring end-to-end functionality for the user journey from landing on the site to processing photos and managing orders.

---

## Suite: Home Module (tests/home)
Focuses on the landing page and initial user interaction.

### TC-HOME-001: Verify Home Page Load and Layout
- **Steps**:
  1. Navigate to the base URL of the application.
  2. Wait for the page load state to be 'networkidle'.
  3. Check for the presence of the header, footer, and main navigation bar.
- **Expect**: The home page renders correctly without console errors. Key navigation elements are visible.

### TC-HOME-002: Navigation to Feature Modules
- **Steps**:
  1. On the Home page, locate the navigation link for 'Hall' (or main feature area).
  2. Click the link.
  3. Verify the URL changes to the expected path.
- **Expect**: Application navigates successfully to the target module.

---

## Suite: Hall Module (tests/hall)
Focuses on the main exhibition or service selection area.

### TC-HALL-001: Display Service Categories
- **Steps**:
  1. Navigate to the Hall page.
  2. Verify that service categories (e.g., ID Photo, Poster, General Photo) are displayed as cards or list items.
- **Expect**: All service categories defined in the application data are visible and clickable.

### TC-HALL-002: Search and Filter Functionality
- **Steps**:
  1. Enter a keyword in the search bar (e.g., "ID Photo").
  2. Press Enter or click the Search button.
- **Expect**: The list updates to show only items matching the keyword.

---

## Suite: ID Photo Module (tests/idphoto)
Focuses on the specific workflow for creating ID photos.

### TC-IDP-001: Upload Photo for ID Photo Processing
- **Steps**:
  1. Navigate to the ID Photo module.
  2. Click the 'Upload' button.
  3. Select a valid image file (JPG/PNG) using `.setInputFiles`.
  4. Verify the upload progress/completion.
- **Expect**: The image is uploaded successfully and a preview is displayed in the editing interface.

### TC-IDP-002: Change Background Color
- **Steps**:
  1. Assuming a photo is uploaded, locate the background color options (e.g., Blue, White, Red).
  2. Select 'Blue'.
- **Expect**: The background of the preview image changes to Blue immediately.

### TC-IDP-003: Select Photo Specifications
- **Steps**:
  1. Open the specifications dropdown or selector.
  2. Choose a specific size (e.g., "One Inch" or "Passport Size").
- **Expect**: The preview crops or adjusts to the selected aspect ratio, and the specification text updates.

---

## Suite: Photo Module (tests/photo)
Focuses on general photo editing or management features.

### TC-PHOTO-001: Basic Photo Editing Tools
- **Steps**:
  1. Upload a photo to the general Photo editor.
  2. Test basic tools: Rotate, Flip, or Crop.
  3. Apply a change.
- **Expect**: The image preview reflects the applied changes (e.g., image rotates 90 degrees).

### TC-PHOTO-002: Download Edited Photo
- **Steps**:
  1. Make a minor edit to a photo.
  2. Click the 'Download' or 'Save' button.
  3. Verify the download event is triggered.
- **Expect**: The file downloads successfully to the local system.

---

## Suite: Poster Module (tests/poster)
Focuses on poster design and generation.

### TC-POSTER-001: Select Poster Template
- **Steps**:
  1. Navigate to the Poster module.
  2. Browse the template gallery.
  3. Click on a specific template to select it.
- **Expect**: The editor loads with the selected template ready for customization.

### TC-POSTER-002: Customize Text and Image
- **Steps**:
  1. Select a template.
  2. Click on a text area and modify the content.
  3. Upload an image to replace a placeholder image.
- **Expect**: The template updates with the new text and image in real-time.

---

## Suite: Orders Module (tests/orders)
Focuses on transaction history and order management.

### TC-ORD-001: View Order List
- **Steps**:
  1. Navigate to the 'My Orders' or 'Orders' section.
  2. Verify the list of existing orders loads.
- **Expect**: A list of orders is displayed showing key info (Order ID, Date, Status, Price).

### TC-ORD-002: Filter Orders by Status
- **Steps**:
  1. Locate the status filter tabs (e.g., 'Pending', 'Completed', 'Cancelled').
  2. Click on 'Completed'.
- **Expect**: The list refreshes to show only orders with 'Completed' status.

### TC-ORD-003: View Order Details
- **Steps**:
  1. Click on a specific order item from the list.
  2. Verify the detail page or modal opens.
- **Expect**: Detailed information about the order (product type, parameters, download links) is displayed correctly.