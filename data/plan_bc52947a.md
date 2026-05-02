```markdown
# Test Plan: zhihui-workshop

## Overview
**Project Name**: zhihui-workshop
**Framework**: React
**Test Tool**: Playwright

This application appears to be a "Smart Workshop" (智慧车间) platform, likely providing services related to image processing, printing, and photo management. Based on the directory structure, the application is divided into distinct functional modules: Home, Hall (Service Hall), ID Photos, General Photos, Posters, and Order Management. The test plan focuses on end-to-end testing of these modules to ensure user flows function correctly within the React application.

---

## Suite: Home Module (tests\home)
Focuses on the landing page, navigation, and initial user interaction.

### TC-HOME-001: Verify Home Page Load and Layout
- **Steps**:
  1. Navigate to the root URL of the application.
  2. Wait for the page to load completely (check for React hydration).
  3. Verify the presence of the header, footer, and main content area.
- **Expect**: The home page renders correctly without console errors. Key navigation elements are visible.

### TC-HOME-002: Navigation to Functional Modules
- **Steps**:
  1. On the Home page, locate navigation links/cards for 'ID Photo', 'Poster', and 'Hall'.
  2. Click on each link one by one.
  3. Verify the URL changes and the correct component/module loads.
- **Expect**: Each click navigates the user to the corresponding module page correctly.

---

## Suite: ID Photo Module (tests\idphoto)
Focuses on the specific workflow for ID photo processing.

### TC-IDP-001: ID Photo Upload Functionality
- **Steps**:
  1. Navigate to the ID Photo module.
  2. Click the upload button or drag-and-drop area.
  3. Select a valid image file (jpg/png) using `.setInputFiles`.
  4. Verify the image preview appears.
- **Expect**: The image is uploaded successfully, and a preview is displayed to the user.

### TC-IDP-002: ID Photo Specifications Selection
- **Steps**:
  1. After uploading a photo, verify the specification selection UI (e.g., 1-inch, 2-inch, passport size).
  2. Select a specific size (e.g., '2-inch').
  3. Verify the preview updates or the selection is highlighted.
- **Expect**: The application accepts the specification change, and the UI reflects the selected option.

### TC-IDP-003: ID Photo Processing and Download
- **Steps**:
  1. Upload a photo and select a specification.
  2. Trigger the processing action (e.g., click "Generate" or "Next").
  3. Wait for processing to complete.
  4. Verify the download button appears and is functional.
- **Expect**: The processed image is generated, and the user can initiate a download.

---

## Suite: Poster Module (tests\poster)
Focuses on poster creation and editing features.

### TC-POS-001: Poster Template Selection
- **Steps**:
  1. Navigate to the Poster module.
  2. Verify a list/grid of templates is displayed.
  3. Click on a specific template thumbnail.
- **Expect**: The selected template loads into the editor or preview area.

### TC-POS-002: Poster Text Editing
- **Steps**:
  1. Select a template containing text elements.
  2. Click on a text area to enable editing.
  3. Input new text content.
  4. Verify the preview updates in real-time.
- **Expect**: Text content is updated successfully in the poster preview.

### TC-POS-003: Poster Save and Export
- **Steps**:
  1. Make changes to a poster (upload image or edit text).
  2. Click the "Save" or "Export" button.
  3. Verify the success notification or download trigger.
- **Expect**: The poster is saved to the user's account or downloaded successfully.

---

## Suite: Photo Module (tests\photo)
Focuses on general photo processing or printing services.

### TC-PHO-001: General Photo Upload
- **Steps**:
  1. Navigate to the Photo module.
  2. Upload a high-resolution image file.
  3. Verify the upload progress and completion.
- **Expect**: The photo is uploaded and displayed in the user's gallery or editing interface.

### TC-PHO-002: Photo Print Settings Configuration
- **Steps**:
  1. Select an uploaded photo.
  2. Choose print settings (e.g., paper size 4R/6R, quantity).
  3. Verify price calculation updates (if applicable).
- **Expect**: Print settings are applied, and the interface reflects the user's choices.

---

## Suite: Hall Module (tests\hall)
Focuses on the service hall or information display section.

### TC-HAL-001: Service List Display
- **Steps**:
  1. Navigate to the Hall module.
  2. Check if the list of services or news items is rendered.
  3. Scroll to load more items (if pagination/infinite scroll exists).
- **Expect**: Service items are displayed correctly, and lazy loading works if implemented.

### TC-HAL-002: Service Detail View
- **Steps**:
  1. Click on an item in the Hall list.
  2. Verify the detail page loads with correct content.
- **Expect**: The detail page displays information corresponding to the selected item.

---

## Suite: Orders Module (tests\orders)
Focuses on transaction history and order management.

### TC-ORD-001: Order History List
- **Steps**:
  1. Navigate to the Orders module (assume user is logged in).
  2. Verify the list of past orders is displayed.
  3. Check for status indicators (e.g., 'Pending', 'Completed').
- **Expect**: The order list renders accurately with correct status badges.

### TC-ORD-002: Order Detail View
- **Steps**:
  1. Click on a specific order from the list.
  2. Verify order details: items, total price, date, and status.
- **Expect**: The detail view matches the data shown in the list and backend data.

### TC-ORD-003: Reorder Functionality
- **Steps**:
  1. Inside an order detail view, locate a "Reorder" or "Buy Again" button.
  2. Click the button.
  3. Verify redirection to the relevant product/service page with pre-filled data.
- **Expect**: User is redirected to the service page with the previous configuration loaded.
```