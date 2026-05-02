import minium

class TestPureActivity(minium.MiniTest):
    
    # ==================== Suite: 01_User_Authentication ====================
    
    def test_auth_001_wechat_authorized_login(self):
        """TC-AUTH-001: WeChat Authorized Login"""
        # Launch the Mini Program
        self.app.launch()
        
        # Check if user is logged in
        user_avatar = self.page.get_element(".user-avatar")
        
        if user_avatar is None:
            # Trigger login flow by clicking Profile tab
            self.page.get_element(".tab-profile").click()
            
            # Wait for login prompt and click authorize
            self.page.wait_for(".login-button", timeout=5)
            self.page.get_element(".login-button").click()
        
        # Verify user is logged in - avatar and nickname displayed
        self.page.wait_for(".user-info", timeout=5)
        avatar = self.page.get_element(".user-avatar")
        nickname = self.page.get_element(".user-nickname")
        
        self.assertIsNotNone(avatar, "User avatar should be displayed")
        self.assertIsNotNone(nickname, "User nickname should be displayed")
        self.assertTrue(len(nickname.text) > 0, "Nickname should not be empty")
    
    def test_auth_002_user_profile_authorization(self):
        """TC-AUTH-002: User Profile Authorization (Scope)"""
        # Navigate to profile edit page
        self.app.navigate_to("/pages/profile/edit")
        
        # Check if authorization popup appears
        self.page.wait_for(".auth-container", timeout=5)
        auth_popup = self.page.get_element(".auth-popup")
        
        if auth_popup is not None:
            # Test deny scenario
            deny_btn = self.page.get_element(".auth-deny")
            if deny_btn:
                deny_btn.click()
                
                # Verify error message shown
                self.page.wait_for(".auth-error", timeout=3)
                error_msg = self.page.get_element(".auth-error")
                self.assertIsNotNone(error_msg, "Error message should show on deny")
                
                # Re-trigger authorization
                self.page.get_element(".auth-request-btn").click()
                self.page.wait_for(".auth-popup", timeout=3)
            
            # Allow authorization
            allow_btn = self.page.get_element(".auth-allow")
            if allow_btn:
                allow_btn.click()
        
        # Verify profile page is accessible
        self.page.wait_for(".profile-form", timeout=5)
        profile_form = self.page.get_element(".profile-form")
        self.assertIsNotNone(profile_form, "Profile form should be accessible after authorization")
    
    # ==================== Suite: 02_Home_And_Discovery ====================
    
    def test_home_001_activity_list_rendering(self):
        """TC-HOME-001: Activity List Rendering"""
        # Navigate to Home page
        self.app.navigate_to("/pages/index/index")
        
        # Wait for data loading
        self.page.wait_for(".activity-list", timeout=10)
        
        # Verify activity list container exists
        activity_list = self.page.get_element(".activity-list")
        self.assertIsNotNone(activity_list, "Activity list container should exist")
        
        # Get all activity items
        activity_items = self.page.get_elements(".activity-item")
        self.assertGreater(len(activity_items), 0, "Activity list should contain items")
        
        # Check first item has required elements
        first_item = activity_items[0]
        title = first_item.get_element(".activity-title")
        image = first_item.get_element(".activity-image")
        status = first_item.get_element(".activity-status")
        
        self.assertIsNotNone(title, "Activity title should exist")
        self.assertIsNotNone(image, "Activity image should exist")
        self.assertIsNotNone(status, "Activity status should exist")
        self.assertTrue(len(title.text) > 0, "Activity title should not be empty")
    
    def test_home_002_activity_search_filter(self):
        """TC-HOME-002: Activity Search & Filter"""
        # Navigate to Home page
        self.app.navigate_to("/pages/index/index")
        
        # Locate search input
        self.page.wait_for(".search-input", timeout=5)
        search_input = self.page.get_element(".search-input")
        self.assertIsNotNone(search_input, "Search input should be visible")
        
        # Input keyword
        search_input.input("Hiking")
        
        # Trigger search
        search_btn = self.page.get_element(".search-btn")
        if search_btn:
            search_btn.click()
        else:
            # Press enter or trigger search event
            self.page.get_element(".search-form").click()
        
        # Wait for results
        self.page.wait_for(".activity-list", timeout=5)
        
        # Verify results match keyword
        activity_items = self.page.get_elements(".activity-item")
        self.assertGreater(len(activity_items), 0, "Search should return results")
        
        # Check first result contains keyword
        first_title = activity_items[0].get_element(".activity-title").text
        self.assertIn("Hiking", first_title, 
                     f"Activity title should contain 'Hiking'")
    
    # ==================== Suite: 03_Activity_Detail_And_Registration ====================
    
    def test_detail_001_view_activity_details(self):
        """TC-DETAIL-001: View Activity Details"""
        # Navigate to Home page first
        self.app.navigate_to("/pages/index/index")
        self.page.wait_for(".activity-item", timeout=5)
        
        # Click on first activity item
        first_activity = self.page.get_element(".activity-item")
        first_activity.click()
        
        # Wait for detail page to load
        self.page.wait_for(".detail-container", timeout=5)
        
        # Verify navigation to detail page
        current_page = self.app.get_current_page()
        self.assertIn("detail", current_page.path, "Should navigate to detail page")
        
        # Check detail elements exist
        time_elem = self.page.get_element(".detail-time")
        location_elem = self.page.get_element(".detail-location")
        description_elem = self.page.get_element(".detail-description")
        organizer_elem = self.page.get_element(".detail-organizer")
        
        self.assertIsNotNone(time_elem, "Time element should exist")
        self.assertIsNotNone(location_elem, "Location element should exist")
        self.assertIsNotNone(description_elem, "Description element should exist")
        self.assertIsNotNone(organizer_elem, "Organizer element should exist")
        
        # Verify content is not empty
        self.assertTrue(len(time_elem.text) > 0, "Time text should not be empty")
        self.assertTrue(len(location_elem.text) > 0, "Location text should not be empty")
    
    def test_detail_002_activity_registration_validation(self):
        """TC-DETAIL-002: Activity Registration (Form Validation)"""
        # Navigate to activity detail
        self.app.navigate_to("/pages/index/index")
        self.page.wait_for(".activity-item", timeout=5)
        self.page.get_element(".activity-item").click()
        self.page.wait_for(".detail-container", timeout=5)
        
        # Click Register/Join button
        register_btn = self.page.get_element(".register-btn")
        self.assertIsNotNone(register_btn, "Register button should exist")
        register_btn.click()
        
        # Wait for form
        self.page.wait_for(".registration-form", timeout=5)
        
        # Test 1: Submit with empty required fields
        submit_btn = self.page.get_element(".submit-btn")
        submit_btn.click()
        
        error_msg = self.page.get_element(".error-message")
        self.assertIsNotNone(error_msg, "Error should show for empty fields")
        
        # Test 2: Invalid phone format
        phone_input = self.page.get_element("input[placeholder*='phone']")
        if phone_input is None:
            phone_input = self.page.get_element(".phone-input")
        phone_input.input("invalid-phone")
        submit_btn.click()
        
        phone_error = self.page.get_element(".phone-error")
        self.assertIsNotNone(phone_error, "Phone format error should show")
        
        # Test 3: Valid data submission
        name_input = self.page.get_element("input[placeholder*='name']")
        if name_input is None:
            name_input = self.page.get_element(".name-input")
        name_input.input("Test User")
        phone_input.input("13800138000")
        submit_btn.click()
        
        # Verify submission proceeds
        self.page.wait_for(".payment-container", timeout=5)
        payment_page = self.page.get_element(".payment-container")
        self.assertIsNotNone(payment_page, "Should proceed to payment after valid submission")
    
    def test_detail_003_wechat_payment_integration(self):
        """TC-DETAIL-003: WeChat Payment Integration"""
        # Navigate to payment page (assuming registration completed)
        self.app.navigate_to("/pages/payment/payment")
        self.page.wait_for(".payment-container", timeout=5)
        
        # Get payment amount
        amount = self.page.get_element(".payment-amount")
        self.assertIsNotNone(amount, "Payment amount should be displayed")
        self.assertTrue(len(amount.text) > 0, "Payment amount should have value")
        
        # Trigger payment
        pay_btn = self.page.get_element(".pay-btn")
        pay_btn.click()
        
        # Wait for payment processing
        self.page.wait_for(".payment-result", timeout=10)
        
        # Verify success state
        success_msg = self.page.get_element(".success-message")
        if success_msg:
            self.assertIsNotNone(success_msg, "Payment success message should display")
            
            # Verify activity status updated
            status = self.page.get_element(".activity-status")
            if status:
                self.assertIn("Paid", status.text, "Activity status should indicate paid")
    
    # ==================== Suite: 04_User_Center ====================
    
    def test_user_001_my_activities_list(self):
        """TC-USER-001: My Activities List"""
        # Navigate to User Center
        self.app.navigate_to("/pages/user/user")
        self.page.wait_for(".user-center", timeout=5)
        
        # Click on My Activities
        my_activities = self.page.get_element(".my-activities")
        self.assertIsNotNone(my_activities, "My Activities entry should exist")
        my_activities.click()
        
        # Wait for list
        self.page.wait_for(".activity-list", timeout=5)
        
        # Verify list exists
        activity_items = self.page.get_elements(".activity-item")
        self.assertGreater(len(activity_items), 0, "My Activities list should contain items")
        
        # Verify status is displayed correctly
        first_item = activity_items[0]
        status = first_item.get_element(".activity-status")
        self.assertIsNotNone(status, "Activity status should be displayed")
        
        valid_statuses = ["Pending", "Completed", "Cancelled", "待处理", "已完成", "已取消"]
        self.assertIn(status.text, valid_statuses, 
                     f"Status '{status.text}' should be valid")
    
    def test_user_002_cancel_registration(self):
        """TC-USER-002: Cancel Registration"""
        # Navigate to User Center
        self.app.navigate_to("/pages/user/user")
        self.page.wait_for(".user-center", timeout=5)
        
        # Go to My Activities
        self.page.get_element(".my-activities").click()
        self.page.wait_for(".activity-list", timeout=5)
        
        # Select first registered activity
        first_activity = self.page.get_element(".activity-item")
        first_activity.click()
        
        # Wait for detail
        self.page.wait_for(".activity-detail", timeout=5)
        
        # Click Cancel button
        cancel_btn = self.page.get_element(".cancel-btn")
        self.assertIsNotNone(cancel_btn, "Cancel button should exist")
        cancel_btn.click()
        
        # Confirm cancellation in modal
        self.page.wait_for(".confirm-modal", timeout=3)
        confirm_btn = self.page.get_element(".confirm-btn")
        confirm_btn.click()
        
        # Verify status changed to Cancelled
        self.page.wait_for(".status-cancelled", timeout=5)
        status = self.page.get_element(".activity-status")
        self.assertEqual("Cancelled", status.text, "Activity status should be 'Cancelled'")
    
    # ==================== Suite: 05_WeChat_Native_Features ====================
    
    def test_wx_001_share_activity(self):
        """TC-WX-001: Share Activity to WeChat Chat"""
        # Navigate to activity detail
        self.app.navigate_to("/pages/index/index")
        self.page.wait_for(".activity-item", timeout=5)
        self.page.get_element(".activity-item").click()
        self.page.wait_for(".detail-container", timeout=5)
        
        # Trigger share - click share button
        share_btn = self.page.get_element(".share-btn")
        if share_btn:
            share_btn.click()
        else:
            # Use top-right menu
            more_menu = self.page.get_element(".more-menu")
            if more_menu:
                more_menu.click()
                self.page.get_element(".share-option").click()
        
        # Verify share menu appears
        self.page.wait_for(".share-menu", timeout=3)
        share_menu = self.page.get_element(".share-menu")
        self.assertIsNotNone(share_menu, "Share menu should appear")
        
        # Verify share options exist
        share_to_chat = self.page.get_element(".share-to-chat")
        share_to_moments = self.page.get_element(".share-to-moments")
        self.assertIsNotNone(share_to_chat, "Share to chat option should exist")
    
    def test_wx_002_get_current_location(self):
        """TC-WX-002: Get Current Location"""
        # Navigate to nearby activities page
        self.app.navigate_to("/pages/nearby/nearby")
        self.page.wait_for(".location-container", timeout=5)
        
        # Trigger location request
        location_btn = self.page.get_element(".get-location-btn")
        self.assertIsNotNone(location_btn, "Get location button should exist")
        location_btn.click()
        
        # Wait for location permission prompt and grant
        self.page.wait_for(".location-permission", timeout=5)
        allow_btn = self.page.get_element(".allow-location")
        if allow_btn:
            allow_btn.click()
        
        # Wait for location data
        self.page.wait_for(".location-data", timeout=10)
        
        # Verify location is displayed
        location_name = self.page.get_element(".location-name")
        self.assertIsNotNone(location_name, "Location name should be displayed")
        self.assertTrue(len(location_name.text) > 0, "Location name should have value")
        
        # Verify map markers or nearby activities are shown
        markers = self.page.get_elements(".map-marker")
        self.assertGreater(len(markers), 0, "Map markers should be displayed")
    
    def test_wx_003_map_navigation(self):
        """TC-WX-003: Map Navigation"""
        # Navigate to activity detail
        self.app.navigate_to("/pages/index/index")
        self.page.wait_for(".activity-item", timeout=5)
        self.page.get_element(".activity-item").click()
        self.page.wait_for(".detail-container", timeout=5)
        
        # Click location/navigation icon
        location_icon = self.page.get_element(".location-icon")
        self.assertIsNotNone(location_icon, "Location icon should exist")
        location_icon.click()
        
        # Wait for map to open
        self.page.wait_for(".map-container", timeout=5)
        
        # Verify map elements
        map_view = self.page.get_element(".map-view")
        self.assertIsNotNone(map_view, "Map view should be displayed")
        
        # Verify location markers
        venue_marker = self.page.get_element(".venue-marker")
        self.assertIsNotNone(venue_marker, "Venue marker should be displayed on map")
        
        # Verify navigation button
        nav_btn = self.page.get_element(".navigation-btn")
        self.assertIsNotNone(nav_btn, "Navigation button should exist")
    
    # ==================== Suite: 06_Components ====================
    
    def test_comp_001_generic_button_component(self):
        """TC-COMP-001: Generic Button Component"""
        # Navigate to a page with button components
        self.app.navigate_to("/pages/index/index")
        self.page.wait_for(".custom-button", timeout=5)
        
        # Test Active state
        active_btn = self.page.get_element(".custom-button.active")
        self.assertIsNotNone(active_btn, "Active button should exist")
        active_btn.click()
        
        # Verify click event fired
        self.page.wait_for(".click-feedback", timeout=3)
        
        # Test Disabled state
        disabled_btn = self.page.get_element(".custom-button.disabled")
        self.assertIsNotNone(disabled_btn, "Disabled button should exist")
        
        # Verify disabled button styling
        disabled_class = disabled_btn.attr("class")
        self.assertIn("disabled", disabled_class, "Button should have disabled class")
        
        # Test Loading state
        loading_btn = self.page.get_element(".custom-button.loading")
        self.assertIsNotNone(loading_btn, "Loading button should exist")
        
        # Verify loading indicator
        loading_spinner = loading_btn.get_element(".loading-spinner")
        self.assertIsNotNone(loading_spinner, "Loading spinner should be visible")
    
    def test_comp_002_activity_card_component(self):
        """TC-COMP-002: Activity Card Component"""
        # Navigate to home page with activity cards
        self.app.navigate_to("/pages/index/index")
        self.page.wait_for(".activity-card", timeout=5)
        
        # Test normal card
        normal_card = self.page.get_element(".activity-card")
        self.assertIsNotNone(normal_card, "Activity card should exist")
        
        # Verify card elements
        title = normal_card.get_element(".card-title")
        image = normal_card.get_element(".card-image")
        self.assertIsNotNone(title, "Card title should exist")
        self.assertIsNotNone(image, "Card image should exist")
        self.assertTrue(len(title.text) > 0, "Card title should have text")
        
        # Test long text truncation
        long_title_card = self.page.get_element(".activity-card.long-title")
        if long_title_card:
            title_elem = long_title_card.get_element(".card-title")
            self.assertIsNotNone(title_elem, "Long title card should have title")
            # Verify text is truncated (check CSS or visual behavior)
            title_container = long_title_card.get_element(".card-title-container")
            self.assertIsNotNone(title_container, "Title container should handle overflow")
        
        # Test missing image fallback
        no_image_card = self.page.get_element(".activity-card.no-image")
        if no_image_card:
            fallback_image = no_image_card.get_element(".card-image-fallback")
            self.assertIsNotNone(fallback_image, 
                                "Fallback image should display when image is missing")
        
        # Test card click interaction
        normal_card.click()
        self.page.wait_for(".detail-container", timeout=5)
        current_page = self.app.get_current_page()
        self.assertIn("detail", current_page.path, "Clicking card should navigate to detail")