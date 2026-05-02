# Expanded Test Plan: zhihui-workshop

## Overview
This test plan provides comprehensive, adversarial coverage for the **zhihui-workshop** React application. Based on the project structure, the application appears to be a "Smart Workshop" platform with modules for ID photos, general photo processing, poster creation, order management, and a main hall/home interface.

The plan focuses on maximum coverage, targeting edge cases, state transitions, and cross-module integrity often missed in standard happy-path testing.

---

## Suite: Home & Navigation (Global)
*Focus: Application shell, routing, and global state.*

### TC-HOME-001: Initial Load & Critical Resource Check
- **Category**: happy-path
- **Steps**:
  1. Navigate to the root URL.
  2. Wait for network idle.
  3. Verify main heading/navbar is visible.
  4. Check console for uncaught errors or failed API calls.
- **Expect**: Page loads without 404/500 errors. No severe console errors. Main navigation is interactive.

### TC-HOME-002: Rapid Navigation Stress Test
- **Category**: concurrent
- **Steps**:
  1. Rapidly click navigation links between 'Home', 'Hall', and 'Orders' before pages fully load.
  2. Repeat 5-10 times randomly.
- **Expect**: Application does not crash. No memory leaks observed. The final loaded page matches the last clicked link (race condition handling).

### TC-HOME-003: Responsive Layout Breakpoint Test
- **Category**: ui
- **Steps**:
  1. Resize viewport from 1920px width down to 320px in 100px increments.
  2. Check for horizontal scrollbars, overlapping text, or "hamburger" menu functionality.
- **Expect**: UI adapts fluidly. No elements disappear or become unclickable. No unintended horizontal scrolling.

### TC-HOME-004: Network Failure Handling (Offline Mode)
- **Category**: negative
- **Steps**:
  1. Intercept all network requests and force failure (Simulate offline).
  2. Attempt to navigate to a data-heavy module (e.g., Orders).
- **Expect**: Application shows a graceful error message or retry button. It does not show a blank screen or infinite spinner.

### TC-HOME-005: Browser Back/Forward State Restoration
- **Category**: state
- **Steps**:
  1. Navigate from Home -> ID Photo -> Poster.
  2. Click the browser "Back" button twice.
  3. Click the browser "Forward" button.
- **Expect**: Navigation history is correct. Form data (if any) entered in intermediate steps is either preserved or cleared according to app logic (no stale state).

---

## Suite: ID Photo (IDPhoto Module)
*Focus: Image processing, upload handling, and cropping.*

### TC-IDP-001: Standard Upload and Process Flow
- **Category**: happy-path
- **Steps**:
  1. Navigate to ID Photo module.
  2. Upload a valid JPG/PNG portrait image.
  3. Select a background color (e.g., Blue).
  4. Click "Process" or "Download".
- **Expect**: Image uploads successfully. Preview updates with new background. Download triggers correctly.

### TC-IDP-002: Invalid File Type Upload
- **Category**: negative
- **Steps**:
  1. Attempt to upload a non-image file (e.g., `.txt`, `.pdf`, `.exe`) by changing the file extension or using the file dialog.
- **Expect**: System rejects the file. An error toast/modal appears stating "Invalid file type". Upload input resets.

### TC-IDP-003: Maximum File Size Boundary
- **Category**: boundary
- **Steps**:
  1. Upload an image exactly at the size limit (e.g., 10MB if limit is 10MB).
  2. Upload an image 1 byte over the limit.
- **Expect**: Limit file uploads successfully. Over-limit file triggers a specific "File too large" error.

### TC-IDP-004: Face Detection Failure Scenario
- **Category**: negative
- **Steps**:
  1. Upload an image with no human face (e.g., a landscape, a cat, or a solid color block).
  2. Wait for processing.
- **Expect**: System detects no face. Displays a user-friendly message like "No face detected, please upload a portrait." Does not crash or infinite load.

### TC-IDP-005: Multiple Faces Detected
- **Category**: boundary
- **Steps**:
  1. Upload a group photo with 3+ people.
- **Expect**: System prompts user to select which face to process or rejects the photo asking for a single portrait.

### TC-IDP-006: Cropper Boundary Interaction
- **Category**: ui
- **Steps**:
  1. Upload image.
  2. In the cropper, attempt to drag the crop area completely outside the image bounds or invert it (drag right handle to left of left handle).
- **Expect**: Cropper constrains movement within bounds. Cannot create invalid/negative crop dimensions.

### TC-IDP-007: Rapid "Process" Button Clicks
- **Category**: concurrent
- **Steps**:
  1. Upload image.
  2. Click the "Process/Download" button 5 times rapidly.
- **Expect**: Only one request is sent (button disabled after first click) or only one download is triggered. No duplicate charges (if paid feature).

---

## Suite: Poster Module
*Focus: Design canvas, text editing, and template handling.*

### TC-POS-001: Create and Save Basic Poster
- **Category**: happy-path
- **Steps**:
  1. Select a template from the gallery.
  2. Click "Edit Text" on a text layer.
  3. Modify text content.
  4. Save/Export the poster.
- **Expect**: Text updates in real-time on canvas. Exported image reflects the changes.

### TC-POS-002: Empty Text Field Submission
- **Category**: boundary
- **Steps**:
  1. Select a text element.
  2. Delete all text content.
  3. Deselect/Save.
- **Expect**: Text element remains empty (or is auto-deleted if that's the logic). No visual glitches like "undefined" appearing on canvas.

### TC-POS-003: Maximum Character Limit Overflow
- **Category**: boundary
- **Steps**:
  1. Paste a massive block of text (e.g., 5000 chars) into a small text box.
- **Expect**: Text is truncated or box expands with scroll. Text does not overflow infinitely outside the canvas bounds breaking the layout.

### TC-POS-004: Image Layer Manipulation
- **Category**: happy-path
- **Steps**:
  1. Upload a custom image to the canvas.
  2. Resize, rotate, and drag the image.
  3. Move it behind/in front of text layers.
- **Expect**: Controls are responsive. Z-index ordering works correctly. Image quality remains acceptable during resize.

### TC-POS-005: Template Switch Data Loss
- **Category**: state
- **Steps**:
  1. Edit current poster (add text/images).
  2. Without saving, click "Back" or select a new template.
- **Expect**: Application prompts "Unsaved changes will be lost. Continue?". User choice is respected.

### TC-POS-006: Cross-Module Image Usage
- **Category**: cross-module
- **Steps**:
  1. Process an ID photo in the ID Photo module.
  2. Navigate to Poster module.
  3. Attempt to use the recently processed photo in the poster canvas.
- **Expect**: The processed image is accessible in the "My Photos" or asset library within the Poster module.

---

## Suite: Orders Module
*Focus: Transaction history, payment status, and data display.*

### TC-ORD-001: View Order History
- **Category**: happy-path
- **Steps**:
  1. Navigate to Orders page.
  2. Verify list of past orders loads.
  3. Click into an order detail.
- **Expect**: List displays correct thumbnails, dates, and statuses. Detail view matches list summary.

### TC-ORD-002: Zero State (No Orders)
- **Category**: empty
- **Steps**:
  1. Log in as a user with no transaction history (or clear DB state).
  2. Navigate to Orders.
- **Expect**: Page displays a friendly "No orders yet" message and a CTA (Call to Action) button like "Create Now". No empty table rows.

### TC-ORD-003: Pagination/Infinite Scroll Boundary
- **Category**: boundary
- **Steps**:
  1. Ensure user has > 20 orders (or mock data).
  2. Scroll to bottom of list.
  3. Trigger load more.
- **Expect**: Next set of orders loads. No duplicate entries. Scroll position is maintained or reset appropriately.

### TC-ORD-004: Filter by Invalid Date Range
- **Category**: negative
- **Steps**:
  1. Use date picker filters.
  2. Select "Start Date" later than "End Date".
- **Expect**: System prevents selection or shows validation error "Start date cannot be after end date". Does not send invalid API request.

### TC-ORD-005: Order Status Transition (Real-time)
- **Category**: state
- **Steps**:
  1. View a "Pending Payment" order.
  2. Simulate payment success (mock or test gateway).
  3. Observe the order status update.
- **Expect**: Status changes to "Paid/Processing" without requiring a full page refresh.

---

## Suite: Photo Module (General Editing)
*Focus: Standard photo manipulation features.*

### TC-PHO-001: Filter Application and Reset
- **Category**: happy-path
- **Steps**:
  1. Upload photo.
  2. Apply "Grayscale" filter.
  3. Apply "Blur" filter.
  4. Click "Reset/Original".
- **Expect**: Filters stack correctly. Reset returns image to original upload state.

### TC-PHO-002: Download Without Edits
- **Category**: boundary
- **Steps**:
  1. Upload photo.
  2. Immediately click "Download" without making any changes.
- **Expect**: Original file is downloaded. No unnecessary re-compression artifacts if possible.

### TC-PHO-003: Undo/Redo Stack Limit
- **Category**: boundary
- **Steps**:
  1. Perform 50 edit operations (e.g., rotate left by 1 degree 50 times).
  2. Click "Undo" 51 times.
  3. Click "Redo".
- **Expect**: Undo stack handles limit gracefully (either caps at 50 or allows all). Redo works correctly after hitting the bottom of the stack.

### TC-PHO-004: Browser Refresh During Edit
- **Category**: state
- **Steps**:
  1. Upload photo and make significant edits.
  2. Hit F5 (Refresh).
- **Expect**: Application warns "Changes may be lost" or resets to initial state. Edits are not persisted (unless app has auto-save feature).

### TC-PHO-005: Corrupted Image Upload
- **Category**: negative
- **Steps**:
  1. Upload a file that has a .jpg extension but contains random text/garbage data inside.
- **Expect**: Image preview fails. Error message "Unable to load image" displayed. Canvas area remains blank or shows placeholder.

---

## Suite: Hall (Dashboard/Lobby)
*Focus: Aggregation and session handling.*

### TC-HALL-001: Dashboard Data Aggregation
- **Category**: happy-path
- **Steps**:
  1. Login as a standard user.
  2. Check Hall/Dashboard widgets (e.g., "Recent Orders", "Quick Actions").
- **Expect**: Widgets load data independently. Failure in one widget (e.g., orders) does not crash the whole Hall page.

### TC-HALL-002: Quick Action Navigation
- **Category**: cross-module
- **Steps**:
  1. Click "Create ID Photo" quick action in Hall.
  2. Click Back.
  3. Click "Create Poster" quick action.
- **Expect**: Deep links navigate to the correct module with the correct initial state (e.g., ID Photo opens camera/upload ready).

### TC-HALL-003: Session Timeout Handling
- **Category**: state
- **Steps**:
  1. Log in.
  2. Wait for session to expire (or mock short timeout).
  3. Attempt to click a button in the Hall.
- **Expect**: User is redirected to Login or shown "Session Expired" modal. Action does not result in generic 401 error page.

### TC-HALL-004: Accessibility Check
- **Category**: ui
- **Steps**:
  1. Use Tab key to navigate through the Hall page elements.
  2. Check focus indicators.
- **Expect**: Logical tab order. All interactive elements (buttons, links) are reachable via keyboard. Focus is visible.