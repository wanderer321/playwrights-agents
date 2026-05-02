# Test Plan: zhihui-workshop

## Overview
**Project Name:** zhihui-workshop
**Framework:** React
**Test Tool:** Playwright
**Description:**
The application appears to be a "Smart Workshop" (Zhihui Workshop) platform, likely providing services related to image processing. Based on the directory structure (`idphoto`, `poster`, `photo`, `orders`), the core business involves ID photo generation, poster design, general photo processing, and order management. The application seems to be user-centric, offering both free tools and paid services.

**Current State:**
The project has an existing test suite with 168 test files distributed across functional modules (`hall`, `home`, `idphoto`, `orders`, `photo`, `poster`). This plan outlines the comprehensive coverage for these modules.

---

## Suite: Home Module (tests/home)
*Focus: Landing page, navigation, and initial user interaction.*

### TC-HOME-001: Verify Home Page Load and Layout
- **Steps**:
  1. Navigate to the root URL of the application.
  2. Wait for the page load state to be 'networkidle'.
- **Expect**:
  - The home page renders successfully without errors.
  - Key UI elements are visible: Header/Navigation bar, Hero section, and Footer.
  - The page title matches the application name.

### TC-HOME-002: Navigation to Functional Modules
- **Steps**:
  1. On the Home page, locate the navigation menu.
  2. Click on the "ID Photo" (证件照) link/button.
  3. Verify URL change.
  4. Navigate back and click on "Poster" (海报) link/button.
- **Expect**:
  - Clicking links redirects the user to the correct module URLs (`/idphoto`, `/poster`).
  - No 404 errors or console errors occur during navigation.

---

## Suite: Hall Module (tests/hall)
*Focus: User dashboard, workspace, or service selection hub.*

### TC-HALL-001: User Dashboard Access
- **Steps**:
  1. Log in as a valid user (or mock authentication state).
  2. Navigate to the Hall/Dashboard URL.
- **Expect**:
  - The Hall page displays user-specific information (e.g., username, avatar).
  - Quick access cards or links to recent services (Photo, Poster) are visible.

### TC-HALL-002: Service Entry Points
- **Steps**:
  1. Inside the Hall page, identify the entry point for "Create ID Photo".
  2. Click the entry point.
- **Expect**:
  - The system redirects to the ID Photo creation workflow.
  - Any required session context is maintained.

---

## Suite: ID Photo Module (tests/idphoto)
*Focus: Core business logic for ID photo creation and processing.*

### TC-IDP-001: Photo Upload Functionality
- **Steps**:
  1. Navigate to the ID Photo creation page.
  2. Click the "Upload" button.
  3. Select a valid JPG/PNG image file from the local filesystem using `.setInputFiles`.
- **Expect**:
  - The file uploads successfully.
  - A preview of the uploaded image appears on the canvas/preview area.
  - Loading indicators disappear after processing.

### TC-IDP-002: Background Color Change
- **Steps**:
  1. Ensure a photo is uploaded (Pre-condition).
  2. Locate the background color options (e.g., Blue, Red, White).
  3. Select "Blue" background.
- **Expect**:
  - The preview image updates to reflect the blue background.
  - The UI indicates the current selection.

### TC-IDP-003: Photo Specifications Selection
- **Steps**:
  1. Locate the size/specification selector (e.g., "1 inch", "2 inch", "Visa").
  2. Select "1 inch" (25mm x 35mm).
- **Expect**:
  - The preview crops or adjusts to match the aspect ratio of the selected spec.
  - The specification name is updated in the UI.

### TC-IDP-004: Download/Save ID Photo
- **Steps**:
  1. Process a photo with specific settings (Color: White, Size: 1 inch).
  2. Click the "Download" or "Save" button.
- **Expect**:
  - A download event is triggered.
  - The downloaded file exists and matches the processed image.

---

## Suite: Poster Module (tests/poster)
*Focus: Template-based design and poster generation.*

### TC-PST-001: Template Selection
- **Steps**:
  1. Navigate to the Poster module.
  2. Browse the template gallery.
  3. Click on a specific template thumbnail.
- **Expect**:
  - The editor loads with the selected template.
  - All template elements (text, images) are rendered in the edit workspace.

### TC-PST-002: Text Editing in Poster
- **Steps**:
  1. Load a template.
  2. Click on a text element within the canvas.
  3. Clear existing text and type "Test Event Title".
  4. Click outside the text box to deselect.
- **Expect**:
  - The text element updates to display "Test Event Title".
  - The font style and size remain consistent unless explicitly changed.

### TC-PST-003: Export Poster
- **Steps**:
  1. Create or modify a poster.
  2. Click the "Export" or "Generate" button.
- **Expect**:
  - A processing loader appears (if applicable).
  - The final image is generated and available for download or preview.

---

## Suite: Photo Module (tests/photo)
*Focus: General photo editing tools (filters, cropping, beauty).*

### TC-PHT-001: Basic Image Adjustment
- **Steps**:
  1. Upload a general photo to the Photo editor.
  2. Locate the adjustment tools (Brightness/Contrast).
  3. Increase Brightness slider to 50%.
- **Expect**:
  - The image preview updates in real-time or upon release of the slider.
  - The image appears brighter than the original.

### TC-PHT-002: Filter Application
- **Steps**:
  1. Upload a photo.
  2. Select a filter preset (e.g., "Grayscale" or "Vintage").
- **Expect**:
  - The filter effect is applied to the image preview immediately.

---

## Suite: Orders Module (tests/orders)
*Focus: Transaction history, payment status, and order details.*

### TC-ORD-001: View Order History
- **Steps**:
  1. Navigate to the "My Orders" section.
- **Expect**:
  - A list of past orders is displayed.
  - Each order row shows basic info: Order ID, Date, Status, and Total Amount.

### TC-ORD-002: Order Detail Verification
- **Steps**:
  1. Click on a specific order from the list.
- **Expect**:
  - The page navigates to the Order Detail view.
  - The detail view shows the breakdown of items purchased (e.g., "ID Photo Service x1").
  - Payment status is clearly visible (e.g., "Paid", "Pending").

### TC-ORD-003: Empty Order State
- **Steps**:
  1. Log in as a user with no transaction history (or clear orders).
  2. Navigate to the Orders page.
- **Expect**:
  - A "No Orders" placeholder image or message is displayed.
  - A prompt to "Go Shopping" or "Create Photo" is visible.