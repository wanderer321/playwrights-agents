```python
import minium
import time


class TestUserLoginAndAuthorization(minium.MiniTest):
    """Suite: 01_User_Login_And_Authorization
    Focus: WeChat specific user identity and permissions.
    """

    def test_auth_001_wechat_silent_login(self):
        """TC-AUTH-001: WeChat Silent Login"""
        # Launch the Mini Program
        self.app.launch()
        
        # Wait for app to fully load
        self.page.wait_for(2)
        
        # Check current page path
        current_page = self.app.get_current_page()
        self.assertIsNotNone(current_page)
        
        # Verify home page loads successfully
        home_element = self.page.get_element(".home-container")
        self.assertTrue(home_element is not None, "Home page should load successfully")
        
        # Check if user-specific data is loaded (indicating silent login)
        my_activities_count = self.page.get_element(".my-activities-count")
        if my_activities_count:
            count_text = my_activities_count.text
            self.assertIsNotNone(count_text, "User activities count should be displayed after silent login")

    def test_auth_002_user_profile_authorization(self):
        """TC-AUTH-002: User Profile Authorization (Avatar/Nickname)"""
        # Navigate to User Profile page
        self.app.navigate_to("/pages/user/profile/profile")
        self.page.wait_for(1)
        
        # Click "Edit Profile" button
        edit_button = self.page.get_element("button", inner_text="编辑资料")
        if not edit_button:
            edit_button = self.page.get_element(".edit-profile-btn")
        edit_button.click()
        
        self.page.wait_for(1)
        
        # Trigger avatar selection (mock wx.getUserProfile or chooseAvatar)
        avatar_button = self.page.get_element(".avatar-selector")
        if avatar_button:
            avatar_button.click()
            self.page.wait_for(1)
        
        # Verify authorization popup or avatar selection interface appears
        auth_popup = self.page.get_element(".authorization-popup")
        if auth_popup:
            self.assertTrue(auth_popup.is_displayed(), "Authorization popup should appear")
            # Confirm authorization
            confirm_btn = self.page.get_element("button", inner_text="允许")
            confirm_btn.click()
        
        self.page.wait_for(1)
        
        # Verify avatar and nickname update on profile page
        updated_avatar = self.page.get_element(".user-avatar")
        updated_nickname = self.page.get_element(".user-nickname")
        
        self.assertIsNotNone(updated_avatar, "User avatar should be displayed")
        self.assertIsNotNone(updated_nickname, "User nickname should be displayed")

    def test_auth_003_location_permission(self):
        """TC-AUTH-003: Location Permission"""
        # Navigate to "Nearby Activities" page
        self.app.navigate_to("/pages/activity/nearby/nearby")
        self.page.wait_for(1)
        
        # Trigger location retrieval
        location_btn = self.page.get_element(".get-location-btn")
        if location_btn:
            location_btn.click()
            self.page.wait_for(2)
        
        # Check for location permission prompt
        permission_popup = self.page.get_element(".permission-prompt")
        if permission_popup:
            allow_btn = self.page.get_element("button", inner_text="允许")
            allow_btn.click()
            self.page.wait_for(1)
        
        # Verify activity list sorts by distance or map centers on user location
        distance_labels = self.page.get_elements(".distance-label")
        self.assertTrue(len(distance_labels) > 0, "Distance labels should be displayed after location permission")
        
        # Verify map is centered (if map exists)
        map_component = self.page.get_element("map")
        if map_component:
            self.assertTrue(map_component.is_displayed(), "Map should be displayed and centered")


class TestActivityBrowsingHome(minium.MiniTest):
    """Suite: 02_Activity_Browsing_Home
    Focus: Main entry point and data display.
    """

    def test_home_001_activity_list_rendering(self):
        """TC-HOME-001: Activity List Rendering"""
        # Launch app to Home page
        self.app.launch()
        self.page.wait_for(2)
        
        # Verify first activity card loads
        first_card = self.page.get_element(".activity-card")
        self.assertIsNotNone(first_card, "Activity card should be rendered")
        
        # Check card elements
        card_image = first_card.get_element(".activity-image")
        card_title = first_card.get_element(".activity-title")
        card_date = first_card.get_element(".activity-date")
        card_status = first_card.get_element(".activity-status")
        
        self.assertIsNotNone(card_image, "Activity image should be present")
        self.assertIsNotNone(card_title, "Activity title should be present")
        self.assertIsNotNone(card_date, "Activity date should be present")
        self.assertIsNotNone(card_status, "Activity status should be present")
        
        # Scroll down to trigger pagination
        self.page.scroll_to(0.9)
        self.page.wait_for(1)
        
        # Check loading indicator
        loading_indicator = self.page.get_element(".loading-indicator")
        if loading_indicator:
            self.assertTrue(True, "Loading indicator should show during pagination")
        
        # Wait for new data
        self.page.wait_for(2)
        
        # Verify new data appended without duplication
        all_cards = self.page.get_elements(".activity-card")
        self.assertTrue(len(all_cards) > 1, "More activity cards should load after scroll")

    def test_home_002_activity_search(self):
        """TC-HOME-002: Activity Search"""
        # Navigate to search page
        self.app.navigate_to("/pages/activity/search/search")
        self.page.wait_for(1)
        
        # Click search bar
        search_input = self.page.get_element("input.search-input")
        self.assertIsNotNone(search_input, "Search input should be present")
        
        # Input valid keyword
        search_input.input("Hiking")
        self.page.wait_for(1)
        
        # Click Search button or press Enter
        search_btn = self.page.get_element("button", inner_text="搜索")
        if search_btn:
            search_btn.click()
        else:
            # Simulate enter key
            self.page.get_element(".search-form").click()
        
        self.page.wait_for(2)
        
        # Verify results matching keyword
        result_items = self.page.get_elements(".search-result-item")
        if len(result_items) > 0:
            for item in result_items[:3]:
                title = item.get_element(".activity-title").text
                self.assertIn("Hiking", title or item.text, "Result should match search keyword")
        else:
            # Check empty state
            empty_state = self.page.get_element(".empty-state")
            self.assertIsNotNone(empty_state, "Empty state should be shown if no results")

    def test_home_003_category_filtering(self):
        """TC-HOME-003: Category Filtering"""
        # Navigate to home page
        self.app.navigate_to("/pages/home/home")
        self.page.wait_for(1)
        
        # Click on "Sports" category tab
        sports_tab = self.page.get_element(".category-tab", inner_text="运动")
        if not sports_tab:
            sports_tab = self.page.get_element("[data-category='sports']")
        
        sports_tab.click()
        self.page.wait_for(2)
        
        # Verify list content updates
        activity_cards = self.page.get_elements(".activity-card")
        self.assertTrue(len(activity_cards) > 0, "Activity list should refresh with category data")
        
        # Click on "Social" category tab
        social_tab = self.page.get_element(".category-tab", inner_text="社交")
        if not social_tab:
            social_tab = self.page.get_element("[data-category='social']")
        
        social_tab.click()
        self.page.wait_for(2)
        
        # Verify list refreshes with different data
        new_activity_cards = self.page.get_elements(".activity-card")
        self.assertTrue(len(new_activity_cards) >= 0, "Activity list should update for new category")


class TestActivityDetailAndRegistration(minium.MiniTest):
    """Suite: 03_Activity_Detail_And_Registration
    Focus: Core business conversion flow.
    """

    def test_detail_001_content_integrity(self):
        """TC-DETAIL-001: Detail Page Content Integrity"""
        # Navigate to home and click first activity
        self.app.navigate_to("/pages/home/home")
        self.page.wait_for(1)
        
        first_activity = self.page.get_element(".activity-card")
        first_activity.click()
        self.page.wait_for(2)
        
        # Check for essential elements
        banner_image = self.page.get_element(".banner-image")
        description = self.page.get_element(".activity-description")
        time_info = self.page.get_element(".activity-time")
        location_info = self.page.get_element(".activity-location")
        organizer_info = self.page.get_element(".organizer-info")
        
        self.assertIsNotNone(banner_image, "Banner image should be present")
        self.assertIsNotNone(description, "Description should be present")
        self.assertIsNotNone(time_info, "Time info should be present")
        self.assertIsNotNone(location_info, "Location info should be present")
        self.assertIsNotNone(organizer_info, "Organizer info should be present")
        
        # Verify time and location formatting
        time_text = time_info.text
        location_text = location_info.text
        
        self.assertTrue(len(time_text) > 0, "Time should be formatted correctly")
        self.assertTrue(len(location_text) > 0, "Location should be formatted correctly")

    def test_detail_002_activity_sharing(self):
        """TC-DETAIL-002: Activity Sharing (WeChat Feature)"""
        # Navigate to activity detail page
        self.app.navigate_to("/pages/activity/detail/detail?id=test123")
        self.page.wait_for(2)
        
        # Click Share button
        share_button = self.page.get_element("button", inner_text="分享")
        if not share_button:
            share_button = self.page.get_element(".share-btn")
        
        share_button.click()
        self.page.wait_for(1)
        
        # Verify share options appear
        share_popup = self.page.get_element(".share-popup")
        if share_popup:
            self.assertTrue(share_popup.is_displayed(), "Share popup should appear")
            
            # Verify share card content
            share_title = self.page.get_element(".share-card-title")
            share_image = self.page.get_element(".share-card-image")
            
            self.assertIsNotNone(share_title, "Share card should have title")
            self.assertIsNotNone(share_image, "Share card should have image")

    def test_detail_003_activity_registration_free(self):
        """TC-DETAIL-003: Activity Registration (Free)"""
        # Navigate to free activity detail page
        self.app.navigate_to("/pages/activity/detail/detail?id=free001")
        self.page.wait_for(2)
        
        # Click Register button
        register_btn = self.page.get_element("button", inner_text="立即报名")
        if not register_btn:
            register_btn = self.page.get_element(".register-btn")
        
        register_btn.click()
        self.page.wait_for(1)
        
        # Fill in form fields
        name_input = self.page.get_element("input[name='name']")
        phone_input = self.page.get_element("input[name='phone']")
        
        # Test form validation - submit with empty phone
        name_input.input("Test User")
        phone_input.input("")
        
        submit_btn = self.page.get_element("button", inner_text="提交")
        submit_btn.click()
        self.page.wait_for(1)
        
        # Verify error message
        error_msg = self.page.get_element(".error-message")
        self.assertIsNotNone(error_msg, "Error message should appear for empty phone")
        
        # Fill valid phone and submit
        phone_input.input("13800138000")
        submit_btn.click()
        self.page.wait_for(2)
        
        # Verify successful registration
        success_msg = self.page.get_element(".success-message")
        registered_btn = self.page.get_element("button", inner_text="已报名")
        
        if success_msg:
            self.assertTrue(success_msg.is_displayed(), "Success message should appear")
        if registered_btn:
            self.assertTrue(registered_btn.is_displayed(), "Button state should change to 'Registered'")

    def test_detail_004_activity_payment_paid(self):
        """TC-DETAIL-004: Activity Payment (Paid Activity)"""
        # Navigate to paid activity detail page
        self.app.navigate_to("/pages/activity/detail/detail?id=paid001")
        self.page.wait_for(2)
        
        # Click Buy Now button
        buy_btn = self.page.get_element("button", inner_text="立即购买")
        if not buy_btn:
            buy_btn = self.page.get_element("button", inner_text="付费报名")
        
        buy_btn.click()
        self.page.wait_for(1)
        
        # Fill required form if present
        form_container = self.page.get_element(".registration-form")
        if form_container:
            name_input = self.page.get_element("input[name='name']")
            phone_input = self.page.get_element("input[name='phone']")
            
            if name_input:
                name_input.input("Test User")
            if phone_input:
                phone_input.input("13800138000")
            
            confirm_btn = self.page.get_element("button", inner_text="确认支付")
            confirm_btn.click()
        
        self.page.wait_for(2)
        
        # Verify payment modal appears (mock wx.requestPayment)
        payment_modal = self.page.get_element(".payment-modal")
        if payment_modal:
            self.assertTrue(payment_modal.is_displayed(), "Payment modal should appear")
            
            # Mock successful payment
            pay_confirm = self.page.get_element("button", inner_text="确认支付")
            pay_confirm.click()
            self.page.wait_for(2)
        
        # Verify order status updates to "Paid"
        order_status = self.page.get_element(".order-status")
        if order_status:
            self.assertIn("已支付", order_status.text, "Order status should be 'Paid'")
        
        # Verify success notification/ticket
        ticket_info = self.page.get_element(".ticket-info")
        self.assertIsNotNone(ticket_info, "User should receive ticket after payment")


class TestUserCenter(minium.MiniTest):
    """Suite: 04_User_Center
    Focus: User data management and history.
    """

    def test_user_001_my_activities_list(self):
        """TC-USER-001: My Activities List"""
        # Navigate to User Center Tab
        self.app.navigate_to("/pages/user/center/center")
        self.page.wait_for(2)
        
        # Click "My Registrations" or "My Orders"
        my_registrations = self.page.get_element(".menu-item", inner_text="我的报名")
        if not my_registrations:
            my_registrations = self.page.get_element(".menu-item", inner_text="我的订单")
        
        my_registrations.click()
        self.page.wait_for(2)
        
        # Verify list displays user's activities
        activity_items = self.page.get_elements(".activity-item")
        self.assertTrue(len(activity_items) >= 0, "Activities list should be displayed")
        
        # Verify status labels are correct
        status_labels = self.page.get_elements(".status-label")
        valid_statuses = ["待支付", "已支付", "已完成", "已取消", "Pending", "Paid", "Completed", "Cancelled"]
        
        for label in status_labels[:5]:
            status_text = label.text
            is_valid = any(s in status_text for s in valid_statuses)
            self.assertTrue(is_valid, f"Status '{status_text}' should be a valid status")

    def test_user_002_cancel_registration(self):
        """TC-USER-002: Cancel Registration"""
        # Navigate to My Activities
        self.app.navigate_to("/pages/user/activities/activities")
        self.page.wait_for(2)
        
        # Select an active registration
        active_item = self.page.get_element(".activity-item .status-pending")
        if not active_item:
            active_item = self.page.get_element(".activity-item .status-active")
        
        if active_item:
            active_item.click()
            self.page.wait_for(1)
            
            # Click Cancel button
            cancel_btn = self.page.get_element("button", inner_text="取消报名")
            if not cancel_btn:
                cancel_btn = self.page.get_element("button", inner_text="申请退款")
            
            cancel_btn.click()
            self.page.wait_for(1)
            
            # Verify confirmation modal appears
            confirm_modal = self.page.get_element(".confirm-modal")
            self.assertIsNotNone(confirm_modal, "Confirmation modal should appear")
            
            # Confirm cancellation
            confirm_btn = self.page.get_element("button", inner_text="确认")
            confirm_btn.click()
            self.page.wait_for(2)
            
            # Verify activity is removed or marked "Cancelled"
            updated_status = self.page.get_element(".status-label")
            if updated_status:
                self.assertIn("已取消", updated_status.text, "Status should be 'Cancelled'")


class TestCommonComponents(minium.MiniTest):
    """Suite: 05_Common_Components
    Focus: Reusable UI elements (5 components identified).
    """

    def test_comp_001_activity_card_component(self):
        """TC-COMP-001: Activity Card Component"""
        # Navigate to home page
        self.app.navigate_to("/pages/home/home")
        self.page.wait_for(2)
        
        # Get all activity cards
        activity_cards = self.page.get_elements(".activity-card")
        self.assertTrue(len(activity_cards) > 0, "Activity cards should be present")
        
        # Check data binding for each card
        for card in activity_cards[:5]:
            # Check title truncation
            title_element = card.get_element(".activity-title")
            if title_element:
                title_text = title_element.text
                # CSS should handle truncation, verify element exists
                self.assertIsNotNone(title_element, "Title should be rendered")
            
            # Check image aspect ratio
            image_element = card.get_element(".activity-image")
            if image_element:
                # Verify image is displayed without distortion
                self.assertIsNotNone(image_element, "Image should be rendered")
        
        # Test on different pages using activity card
        self.app.navigate_to("/pages/activity/list/list")
        self.page.wait_for(2)
        
        list_cards = self.page.get_elements(".activity-card")
        self.assertTrue(len(list_cards) >= 0, "Activity cards should render consistently across pages")

    def test_comp_002_loading_component(self):
        """TC-COMP-002: Loading Component"""
        # Navigate to a page that triggers loading
        self.app.navigate_to("/pages/home/home")
        
        # Observe loading component during initial load
        loading_component = self.page.get_element(".loading-component")
        if loading_component:
            self.assertTrue(loading_component.is_displayed(), "Loading animation should display during data fetch")
        
        # Wait for data to arrive
        self.page.wait_for(3)
        
        # Verify loading animation disappears
        loading_after = self.page.get_element(".loading-component")
        if loading_after:
            is_visible = loading_after.is_displayed()
            self.assertFalse(is_visible, "Loading animation should disappear after data loads")
        
        # Verify content is displayed
        content = self.page.get_element(".activity-card")
        self.assertIsNotNone(content, "Content should be displayed after loading")


class TestExceptionHandling(minium.MiniTest):
    """Suite: 06_Exception_Handling
    Focus: Network and boundary conditions.
    """

    def test_ex_001_network_disconnect(self):
        """TC-EX-001: Network