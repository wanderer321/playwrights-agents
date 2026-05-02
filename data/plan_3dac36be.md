# Expanded Test Plan: zhihui-workshop

## Overview
This test plan provides comprehensive coverage for the "zhihui-workshop" React application. Based on the project structure, the application appears to be a multi-functional utility platform offering services like ID photo processing, general photo editing, poster creation, and order management. The plan covers functional, UI, negative, and cross-module integration scenarios to ensure robustness.

---

## Suite: Home (Landing & Navigation)
Covers the main entry point, navigation flow, and initial state of the application.

### TC-HOME-001: Successful Application Load
- **Category**: happy-path
- **Steps**:
  1. Navigate to the root URL.
  2. Wait for page load state 'networkidle'.
- **Expect**: The home page renders correctly with visible navigation links to Hall, ID Photo, Poster, and Orders. No console errors.

### TC-HOME-002: Navigation to All Modules
- **Category**: happy-path
- **Steps**:
  1. From Home, click the link/button for 'Hall'.
  2. Verify URL change.
  3. Navigate back.
  4. Repeat for 'ID Photo', 'Poster', and 'Orders'.
- **Expect**: Each navigation successfully loads the respective module. Browser history works correctly (Back button functions).

### TC-HOME-003: Responsive Layout Verification
- **Category**: ui
- **Steps**:
  1. Set viewport to 1920x1080 (Desktop).
  2. Set viewport to 375x667 (Mobile).
  3. Check for layout shifts, overlapping elements, or hidden buttons.
- **Expect**: UI adapts gracefully. No horizontal scroll bars on mobile. Key CTA buttons remain clickable.

### TC-HOME-004: Network Failure on Load
- **Category**: negative
- **Steps**:
  1. Intercept main API call (e.g., user info or config) and force 500 Internal Server Error.
  2. Load Home page.
- **Expect**: Application handles the error gracefully (e.g., shows error boundary or toast notification) rather than crashing or showing a blank screen.

### TC-HOME-005: Rapid Navigation Stress Test
- **Category**: concurrent
- **Steps**:
  1. Rapidly click navigation links between Home and Hall 5-10 times quickly before animations/transitions finish.
- **Expect**: Application state remains consistent. No memory leaks, duplicate route entries, or stuck loading spinners.

---

## Suite: Hall (Service Lobby/Selection)
Covers the service selection interface where users likely choose specific tools or templates.

### TC-HALL-001: Service Category Selection
- **Category**: happy-path
- **Steps**:
  1. Navigate to Hall.
  2. Select a category (e.g., "Photo Services").
  3. Verify sub-services are displayed.
- **Expect**: Correct filtering of services. UI updates immediately.

### TC-HALL-002: Empty State for Categories
- **Category**: empty
- **Steps**:
  1. Mock API to return an empty list of services/categories.
  2. Load Hall page.
- **Expect**: A user-friendly "No services available" message is displayed instead of an empty grid.

### TC-HALL-003: Search/Filter Boundary Test
- **Category**: boundary
- **Steps**:
  1. Enter search query with special characters (e.g., `<script>alert(1)</script>`).
  2. Enter a query with 500+ characters.
  3. Enter query with only spaces.
- **Expect**: Input is sanitized. No XSS execution. Long text is truncated or wrapped properly. Empty search returns all results or specific prompt.

### TC-HALL-004: Service Item Click Responsiveness
- **Category**: concurrent
- **Steps**:
  1. Rapidly double-click a service item.
- **Expect**: Only one navigation event/page load is triggered. Prevents duplicate history entries.

### TC-HALL-005: Session Expiry Handling
- **Category**: state
- **Steps**:
  1. Load Hall.
  2. Clear localStorage/cookies (simulate session timeout).
  3. Attempt to click a restricted service.
- **Expect**: Application redirects to login or shows "Session Expired" modal.

---

## Suite: ID Photo (Core Feature)
Covers the ID photo generation tool, likely involving upload, cropping, and background processing.

### TC-IDPHOTO-001: Standard Photo Upload and Process
- **Category**: happy-path
- **Steps**:
  1. Navigate to ID Photo module.
  2. Upload a standard JPG image (front-facing portrait).
  3. Select background color (e.g., Blue).
  4. Click "Process" or "Download".
- **Expect**: Image uploads successfully. Preview shows cropped portrait. Processed image has correct background color.

### TC-IDPHOTO-002: Invalid File Type Upload
- **Category**: negative
- **Steps**:
  1. Attempt to upload a `.txt` or `.exe` file using the upload input.
- **Expect**: File input rejects the file or UI displays an error message "Invalid file format". Upload button should not proceed.

### TC-IDPHOTO-003: Large File Upload Boundary
- **Category**: boundary
- **Steps**:
  1. Upload an image exceeding the size limit (e.g., 20MB+ or whatever the limit is).
- **Expect**: Client-side or server-side validation catches the size limit. User sees a clear "File too large" error message.

### TC-IDPHOTO-004: State Persistence on Refresh
- **Category**: state
- **Steps**:
  1. Upload a photo and crop it.
  2. Do not save/download.
  3. Refresh the page (F5).
- **Expect**: Application resets to initial state (standard behavior) OR attempts to recover draft (if supported). Verify no "zombie" data remains in memory.

### TC-IDPHOTO-005: No Face Detected Scenario
- **Category**: negative
- **Steps**:
  1. Upload an image without a human face (e.g., landscape, object, or pet).
  2. Trigger processing.
- **Expect**: System displays a specific error: "No face detected, please upload a valid portrait."

### TC-IDPHOTO-006: Browser Back Button During Edit
- **Category**: state
- **Steps**:
  1. Upload photo and enter edit mode.
  2. Click browser "Back" button.
  3. Click "Forward" button.
- **Expect**: Navigates away safely. Returning forward should ideally reset the tool or restore state (depending on implementation), but must not crash.

### TC-IDPHOTO-007: Concurrent Upload Prevention
- **Category**: concurrent
- **Steps**:
  1. Select 10 files simultaneously (if multi-upload is supported or allowed).
  2. Or click "Upload" rapidly while a previous upload is in progress.
- **Expect**: System queues files or disables the upload button during processing. No race conditions on the preview area.

---

## Suite: Photo (General Editor)
Covers general photo editing features (filters, cropping, adjustments).

### TC-PHOTO-001: Apply Filter and Download
- **Category**: happy-path
- **Steps**:
  1. Upload a photo.
  2. Select a filter (e.g., "Grayscale").
  3. Adjust brightness/contrast sliders.
  4. Click Download.
- **Expect**: Downloaded image reflects the applied filters and adjustments.

### TC-PHOTO-002: Slider Boundary Values
- **Category**: boundary
- **Steps**:
  1. Move brightness slider to absolute minimum (0).
  2. Move to absolute maximum (100 or 255).
  3. Rapidly drag slider back and forth.
- **Expect**: Image updates in real-time (or near real-time). No visual glitches or NaN errors in the UI value display.

### TC-PHOTO-003: Undo/Redo Functionality
- **Category**: state
- **Steps**:
  1. Apply Crop.
  2. Apply Filter.
  3. Click Undo.
  4. Click Redo.
- **Expect**: State history is managed correctly. Undo reverts to previous state. Redo restores the state.

### TC-PHOTO-004: Download Without Changes
- **Category**: boundary
- **Steps**:
  1. Upload photo.
  2. Immediately click "Download" without any edits.
- **Expect**: Original image is downloaded. No unnecessary processing artifacts added.

### TC-PHOTO-005: Missing Image Error Handling
- **Category**: negative
- **Steps**:
  1. Intercept image processing API and return 404/500.
  2. Attempt to apply a heavy filter or save.
- **Expect**: Loading spinner stops. Error toast "Processing failed" appears. User can retry.

---

## Suite: Poster (Creation Tool)
Covers poster creation, likely involving templates, text, and layering.

### TC-POSTER-001: Create Poster from Template
- **Category**: happy-path
- **Steps**:
  1. Navigate to Poster module.
  2. Select a template from the gallery.
  3. Edit main title text.
  4. Save/Export.
- **Expect**: Editor loads with template. Text is editable. Export generates correct image/PDF.

### TC-POSTER-002: Text Overflow Handling
- **Category**: boundary
- **Steps**:
  1. Select a text box.
  2. Paste a massive block of text (1000+ words) or hold a key down to overflow.
- **Expect**: Text is clipped, scrollable within the box, or font size auto-shrinks. Text does not spill over other elements.

### TC-POSTER-003: Missing Font/Image Asset
- **Category**: negative
- **Steps**:
  1. Block a specific font URL or background image URL used in a template.
  2. Load the template.
- **Expect**: Fallback font is used. Broken image icon is handled or placeholder shown. Editor remains usable.

### TC-POSTER-004: Empty Canvas Save
- **Category**: empty
- **Steps**:
  1. Start with a blank canvas (no template).
  2. Add no elements.
  3. Click "Save" or "Export".
- **Expect**: System warns "Canvas is empty" or exports a blank image correctly without crashing.

### TC-POSTER-005: Element Layering Interaction
- **Category**: concurrent
- **Steps**:
  1. Add multiple elements (Image, Text, Shape).
  2. Rapidly click "Bring to Front" and "Send to Back" buttons.
- **Expect**: Z-index updates correctly. UI reflects the layer order immediately.

---

## Suite: Orders (Transaction History)
Covers order viewing, status checks, and payment history.

### TC-ORDERS-001: View Order History
- **Category**: happy-path
- **Steps**:
  1. Navigate to Orders module.
  2. Verify list of past orders loads.
  3. Check status of a specific order (e.g., "Completed").
- **Expect**: Orders are listed chronologically. Status badges are correct.

### TC-ORDERS-002: Zero Orders State
- **Category**: empty
- **Steps**:
  1. Ensure test user has no past transactions.
  2. Load Orders page.
- **Expect**: Page displays "No orders yet" illustration and message. "Create Order" CTA is visible.

### TC-ORDERS-003: Pagination or Infinite Scroll
- **Category**: boundary
- **Steps**:
  1. Mock data to generate 100+ orders.
  2. Scroll to bottom of list rapidly.
- **Expect**: Pagination controls work OR infinite scroll triggers loading correctly. No duplicate entries rendered.

### TC-ORDERS-004: Cross-Module Data Consistency
- **Category**: cross-module
- **Steps**:
  1. Go to ID Photo module.
  2. Complete a purchase/download action that creates an order.
  3. Navigate immediately to Orders module.
- **Expect**: The new order appears at the top of the list without requiring a manual page refresh.

### TC-ORDERS-005: Date Filter Invalid Range
- **Category**: negative
- **Steps**:
  1. Use date pickers to select a "From" date that is after the "To" date.
  2. Click "Search" or "Apply".
- **Expect**: Validation error "Start date must be before end date" or automatic correction. API is not called with invalid range.

### TC-ORDERS-006: Order Detail Navigation
- **Category**: state
- **Steps**:
  1. Click on an order to view details.
  2. Refresh the page (F5).
- **Expect**: Order details persist or reload correctly based on URL parameter. Not redirected to main list erroneously.

---

## Suite: UI Consistency & Accessibility (Global)
Global checks applicable to all modules.

### TC-UI-001: Text Overflow (Localization)
- **Category**: ui
- **Steps**:
  1. Inject long strings into UI labels (e.g., button text "Download" -> "Download this very long file now...").
  2. Check buttons and headers.
- **Expect**: Text truncates with ellipsis or wraps. Layout does not break.

### TC-UI-002: Keyboard Navigation
- **Category**: ui
- **Steps**:
  1. Navigate through the entire flow using only Tab and Enter keys.
- **Expect**: Focus indicators are visible. All interactive elements are reachable. Focus order is logical.

### TC-UI-003: Dark Mode / Theme Support (If applicable)
- **Category**: ui
- **Steps**:
  1. Toggle system theme to Dark Mode.
  2. Load application.
- **Expect**: Colors adapt. Text remains readable (contrast ratios). No "white flashes" on dark backgrounds.