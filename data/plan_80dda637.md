# Expanded Test Plan: zhihui-workshop

## Overview
This test plan provides comprehensive, adversarial coverage for the "zhihui-workshop" React application. Based on the project structure, the application appears to be a creative workshop platform featuring modules for ID photos (`idphoto`), general photo editing (`photo`), poster creation (`poster`), an exhibition hall (`hall`), order management (`orders`), and a home dashboard (`home`).

The strategy focuses on robustness beyond the happy path, targeting file handling limits, canvas manipulation edge cases, state resilience during async operations, and cross-module data integrity.

---

## Suite: Home (Dashboard/Landing)
*Focus: Initial load, navigation integrity, and empty state handling.*

### TC-HOME-001: Initial Load and Navigation Integrity
- **Category**: happy-path
- **Steps**:
  1. Navigate to the root URL.
  2. Verify the presence of key navigation elements (links to Hall, ID Photo, Poster, Orders).
  3. Click each navigation link and verify URL changes.
- **Expect**: Dashboard loads within performance budget; all navigation links are responsive and route correctly.

### TC-HOME-002: Dashboard Zero State
- **Category**: empty
- **Steps**:
  1. Log in as a new user with no order history or created assets.
  2. Observe the Home dashboard and "Recent Activity" sections.
- **Expect**: Friendly empty states are displayed (e.g., "No orders yet", "Create your first poster") with Call-to-Action buttons, no broken image icons or "undefined" text.

### TC-HOME-003: Rapid Navigation Stress Test
- **Category**: concurrent
- **Steps**:
  1. Rapidly click between "Home", "Hall", and "Orders" tabs before page content fully renders.
  2. Repeat 10 times randomly.
- **Expect**: No console errors, no memory leaks, UI remains responsive, and the final displayed content matches the active tab.

### TC-HOME-004: Network Failure Resilience
- **Category**: negative
- **Steps**:
  1. Open DevTools and set Network to "Offline".
  2. Load the Home page.
  3. Attempt to refresh data.
- **Expect**: Application catches the network error and displays a user-friendly error boundary or toast notification, rather than a white screen or infinite spinner.

### TC-HOME-005: Responsive Layout Shift Check
- **Category**: ui
- **Steps**:
  1. Resize viewport from Desktop (1920px) to Mobile (320px) incrementally.
  2. Check for layout shifts, overlapping text, or hidden buttons.
- **Expect**: Layout adapts fluidly; no elements overlap or disappear off-screen; hamburger menu appears on mobile.

---

## Suite: IdPhoto (ID Photo Processing)
*Focus: File upload constraints, image processing boundaries, and state persistence.*

### TC-IDP-001: Standard ID Photo Generation
- **Category**: happy-path
- **Steps**:
  1. Navigate to ID Photo module.
  2. Upload a standard portrait JPG (2MB, 2000x2000px).
  3. Select a background color (e.g., Blue).
  4. Click "Process".
- **Expect**: Image processes successfully; background is replaced; download button appears.

### TC-IDP-002: Invalid File Format Upload
- **Category**: negative
- **Steps**:
  1. Attempt to upload a non-image file (e.g., `.txt`, `.pdf`, `.exe`).
  2. Attempt to upload a corrupted image file (renamed text file to .jpg).
- **Expect**: System rejects the file immediately with a clear error message "Invalid file format" or "Corrupted image". No crash occurs.

### TC-IDP-003: Extreme Aspect Ratio & Size
- **Category**: boundary
- **Steps**:
  1. Upload a panoramic image (e.g., 5000x500px).
  2. Upload a 50MB high-resolution image.
- **Expect**: System either rejects with "Image too large" or processes gracefully without freezing the browser tab. If processed, the crop logic should handle the extreme ratio without stretching.

### TC-IDP-004: Processing Interruption
- **Category**: state
- **Steps**:
  1. Upload a large image to trigger a longer processing time.
  2. Click the browser "Back" button immediately while the spinner is active.
  3. Navigate forward again to the ID Photo module.
- **Expect**: Processing is cancelled or handled statelessly. Returning to the page shows a clean state, not a stuck "Processing" spinner.

### TC-IDP-005: Double-Submit Prevention
- **Category**: concurrent
- **Steps**:
  1. Upload image.
  2. Rapidly click the "Process" or "Download" button 5 times.
- **Expect**: Only one request is sent to the server; button is disabled after the first click; no duplicate orders are generated.

### TC-IDP-006: No Face Detected Scenario
- **Category**: negative
- **Steps**:
  1. Upload an image of a landscape, object, or a photo with multiple faces (group shot).
- **Expect**: System displays specific error: "No face detected" or "Multiple faces detected". Does not proceed to background removal.

---

## Suite: Poster (Poster Design Tool)
*Focus: Canvas interactions, text inputs, and template handling.*

### TC-PST-001: Create and Save Poster
- **Category**: happy-path
- 1. Select a template from the gallery.
  2. Edit text fields (Title, Subtitle).
  3. Upload a custom logo/image into the poster frame.
  4. Save/Export the poster.
- **Expect**: Poster renders correctly with new text and image; exported file matches preview.

### TC-PST-002: Text Overflow and Special Characters
- **Category**: boundary
- **Steps**:
  1. Select a text box.
  2. Paste a massive block of text (10,000 characters).
  3. Enter special characters (Emojis, `<script>` tags, RTL text).
- **Expect**: Text box does not expand infinitely; text is clipped or scrolls gracefully. Special characters render correctly or are sanitized; no XSS execution.

### TC-PST-003: Template Loading Failure
- **Category**: negative
- **Steps**:
  1. Intercept the API call for template assets and return 404 or 500.
  2. Open the Poster module.
- **Expect**: Application handles the missing template gracefully (e.g., placeholder image or error message) without breaking the entire editor canvas.

### TC-PST-004: Canvas State Reset
- **Category**: state
- **Steps**:
  1. Make several edits to a poster.
  2. Click the "Reset" or "Clear" button.
  3. Refresh the page (F5).
- **Expect**: "Reset" clears all user edits. Refresh reloads the last auto-saved state (if applicable) or returns to default template state.

### TC-PST-005: Cross-Module Asset Usage
- **Category**: cross-module
- **Steps**:
  1. Create an ID Photo and save it.
  2. Navigate to Poster module.
  3. Attempt to use the recently created ID Photo as an asset in the poster.
- **Expect**: The ID Photo appears in the "My Assets" or "Recent" gallery within the Poster editor.

---

## Suite: Orders (Order Management)
*Focus: Data integrity, filtering, and pagination.*

### TC-ORD-001: Order History Pagination
- **Category**: happy-path
- **Steps**:
  1. Ensure user has > 20 orders.
  2. Navigate to Orders page.
  3. Scroll to bottom and click "Next" or trigger infinite scroll.
- **Expect**: Next set of orders loads correctly; no duplicate orders displayed; scroll position maintained appropriately.

### TC-ORD-002: Filter by Date Range (Invalid Range)
- **Category**: negative
- **Steps**:
  1. Open filter options.
  2. Select "Start Date" later than "End Date".
  3. Click Apply.
- **Expect**: System validates date range; shows error "Start date cannot be after end date" or auto-corrects the dates.

### TC-ORD-003: Order Detail Status Transition
- **Category**: state
- **Steps**:
  1. Click on an "In Progress" order.
  2. Simulate a status update (e.g., via WebSocket mock or API polling) to "Completed".
- **Expect**: Order detail view updates the status badge in real-time or on focus return without requiring a full page refresh.

### TC-ORD-004: Empty Order History
- **Category**: empty
- **Steps**:
  1. Access Orders page for a user with 0 orders.
- **Expect**: Display "No orders found" illustration and a button directing user to "Create ID Photo" or "Create Poster".

### TC-ORD-005: Deep Link Access Control
- **Category**: negative
- **Steps**:
  1. Copy the URL of a specific order detail page.
  2. Log out or switch to a different user account.
  3. Paste the URL and navigate.
- **Expect**: System returns 403 Forbidden or redirects to login/404 page. User cannot view another user's order details.

---

## Suite: Hall (Exhibition/Gallery)
*Focus: Public content display, search, and interaction.*

### TC-HALL-001: Gallery Search and Filter
- **Category**: happy-path
- **Steps**:
  1. Enter a keyword in the search bar.
  2. Apply a category filter (e.g., "ID Photo").
  3. Clear search.
- **Expect**: Gallery updates in real-time or on submit; results match keyword and category; clearing search restores full list.

### TC-HALL-002: Broken Image Handling
- **Category**: negative
- **Steps**:
  1. Mock the gallery API to return items with invalid/broken image URLs.
  2. Load the Hall page.
- **Expect**: Fallback placeholder image is displayed; layout does not break (no broken image icon visible to user).

### TC-HALL-003: Infinite Scroll Memory Leak
- **Category**: boundary
- **Steps**:
  1. Scroll down the gallery continuously to load 100+ items.
  2. Monitor browser memory usage.
- **Expect**: Memory usage stabilizes (virtual scrolling/recycling implemented) rather than growing indefinitely until crash.

### TC-HALL-004: Like/Interaction Toggle
- **Category**: concurrent
- **Steps**:
  1. Find an item in the Hall.
  2. Rapidly click the "Like" button (toggle on/off quickly).
- **Expect**: UI updates to match the final state; API calls are debounced or the final state is sent; like count is accurate.

### TC-HALL-005: Accessibility Compliance
- **Category**: ui
- **Steps**:
  1. Navigate the Hall using only keyboard (Tab, Enter, Arrows).
  2. Use a screen reader to announce content.
- **Expect**: All interactive elements are focusable; images have alt text; ARIA labels are present for icons.

---

## Suite: Photo (General Photo Editing)
*Focus: Editor tools, filters, and export.*

### TC-PHT-001: Apply Filters and Revert
- **Category**: happy-path
- **Steps**:
  1. Upload a photo.
  2. Apply "Grayscale" filter.
  3. Apply "Blur" filter.
  4. Click "Undo" or "Reset".
- **Expect**: Filters stack correctly; Undo reverts the last action; Reset returns to original image.

### TC-PHT-002: Browser Refresh During Edit
- **Category**: state
- **Steps**:
  1. Upload photo and make edits.
  2. Do not save.
  3. Refresh the browser (F5).
- **Expect**: Browser prompts "Are you sure you want to leave? Changes may be lost." or auto-saves to local storage and restores state.

### TC-PHT-003: Download Without Saving
- **Category**: negative
- **Steps**:
  1. Upload photo.
  2. Click "Download" without making any changes or waiting for the canvas to initialize.
- **Expect**: System downloads the original file or prompts "No changes detected", does not download a corrupted 0-byte file.

### TC-PHT-004: Mobile Touch Gestures
- **Category**: boundary
- **Steps**:
  1. Switch to mobile viewport (touch simulation).
  2. Attempt to pinch-zoom and pan the image.
- **Expect**: Canvas handles touch events correctly; image does not fly off-screen or get stuck; zoom limits are enforced.

### TC-PHT-005: Large Canvas Export Timeout
- **Category**: boundary
- **Steps**:
  1. Upload a very large image (e.g., 20MB raw).
  2. Apply heavy filters.
  3. Click Export.
- **Expect**: UI shows a progress bar or loading spinner. If it takes too long, a timeout warning is shown, but the browser tab does not freeze.