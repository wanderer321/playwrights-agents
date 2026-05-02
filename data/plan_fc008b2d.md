```markdown
# Test Plan: zhihui-workshop

## Overview
**Project Name**: zhihui-workshop (智慧工坊)
**Framework**: React
**Test Tool**: Playwright

**Application Summary**:
Based on the project structure and directory names, `zhihui-workshop` appears to be a comprehensive digital workshop or utility platform. It focuses on image processing and document generation services, specifically offering features like ID photo creation, general photo editing, poster generation, and order management. The application likely serves end-users looking for quick, automated graphic design solutions.

**Test Scope**:
This test plan covers the end-to-end functional testing of the core modules identified in the `tests` directory: Home, Hall, ID Photo, Photo, Poster, and Orders. The goal is to ensure user flows operate correctly within the React application environment.

---

## Suite: Home Module (tests/home)
*Focus: Landing page, navigation, and initial user interaction.*

### TC-HOME-001: Verify Home Page Load and Layout
- **Steps**:
  1. Navigate to the application root URL.
  2. Wait for the page load state to be 'networkidle'.
  3. Verify the main banner or welcome text is visible.
  4. Check that the navigation bar/footer is rendered correctly.
- **Expect**: The home page loads successfully without console errors; core UI elements are visible and correctly positioned.

### TC-HOME-002: Verify Navigation to Core Modules
- **Steps**:
  1. On the Home page, locate the navigation link/button for "ID Photo" (or relevant entry).
  2. Click the link.
  3. Verify URL changes to the ID Photo route.
  4. Verify the ID Photo page component loads.
- **Expect**: Navigation functions correctly; routing works as expected for the React application.

---

## Suite: Hall Module (tests/hall)
*Focus: Service hall or main dashboard access points.*

### TC-HALL-001: Access Service Hall
- **Steps**:
  1. Navigate to the Hall URL path.
  2. Verify the list of available services or categories is displayed.
  3. Check for interactive elements (cards, buttons) representing services.
- **Expect**: The Hall page displays available services; elements are responsive and clickable.

### TC-HALL-002: Search or Filter Functionality (if applicable)
- **Steps**:
  1. Enter the Hall page.
  2. Input text into a search bar (if present).
  3. Verify the list updates dynamically.
- **Expect**: The list filters results matching the search criteria.

---

## Suite: ID Photo Module (tests/idphoto)
*Focus: Core feature for creating and editing ID photos.*

### TC-IDP-001: Upload Photo for ID Photo Creation
- **Steps**:
  1. Navigate to the ID Photo module.
  2. Click the "Upload" button.
  3. Simulate file upload using `.setInputFiles` with a test image (e.g., `test-image.jpg`).
  4. Verify the image preview appears on the canvas.
- **Expect**: Image uploads successfully; preview is displayed without distortion.

### TC-IDP-002: Change ID Photo Background Color
- **Steps**:
  1. With an image uploaded, click on a color option (e.g., "Blue Background").
  2. Wait for processing to complete.
  3. Verify the background color of the photo changes to the selected color.
- **Expect**: Background is replaced correctly; edges are smooth (visual check or snapshot comparison).

### TC-IDP-003: Download ID Photo
- **Steps**:
  1. Process an ID photo.
  2. Click the "Download" or "Save" button.
  3. Verify the download event is triggered.
- **Expect**: File downloads successfully in the correct format (JPG/PNG).

---

## Suite: Photo Module (tests/photo)
*Focus: General photo editing or beautification tools.*

### TC-PHT-001: Basic Photo Editing Tools
- **Steps**:
  1. Navigate to the Photo module.
  2. Upload a sample photo.
  3. Apply a filter or adjustment (e.g., "Brightness", "Crop").
  4. Verify the canvas updates to reflect the change.
- **Expect**: Editing controls respond to user input; changes are rendered on the preview.

---

## Suite: Poster Module (tests/poster)
*Focus: Template-based poster generation.*

### TC-PST-001: Select Poster Template
- **Steps**:
  1. Navigate to the Poster module.
  2. Browse the template gallery.
  3. Click on a specific template to select it.
- **Expect**: Template details page opens; template is highlighted as selected.

### TC-PST-002: Customize and Save Poster
- **Steps**:
  1. Select a template.
  2. Edit text fields (e.g., Title, Date) within the poster editor.
  3. Click "Generate" or "Preview".
  4. Verify the generated poster reflects the input text.
- **Expect**: Custom text appears correctly on the final poster preview.

---

## Suite: Orders Module (tests/orders)
*Focus: Transaction history and order management.*

### TC-ORD-001: View Order List
- **Steps**:
  1. Navigate to the Orders module.
  2. Verify the list of past orders is loaded.
  3. Check for empty state if no orders exist.
- **Expect**: Order history displays correct data (dates, status, item names).

### TC-ORD-002: View Order Detail
- **Steps**:
  1. Click on a specific order item in the list.
  2. Verify navigation to the Order Detail page.
  3. Check that details (price, download links) match the summary.
- **Expect**: Order detail page shows comprehensive information for the selected transaction.
```