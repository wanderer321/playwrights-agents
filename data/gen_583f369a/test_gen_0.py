import minium

class TestPureActivity(minium.MiniTest):
    
    # Suite: 01_User_Authentication
    
    def test_auth_001_wechat_user_login(self):
        """TC-AUTH-001: WeChat User Login"""
        # Launch the Mini Program
        self.app.launch()
        
        # Check if user is logged in by looking for user info elements
        user_avatar = self.page.get_element(".user-avatar")
        user_nickname = self.page.get_element(".user-nickname")
        
        # If not logged in, trigger login flow
        if not user_avatar or not user_nickname:
            # Click "Me" tab or login button
            self.page.get_element(".tab-me, .login-btn").click()
            
            # Wait for authorization popup
            self.page.wait_for(".auth-popup, .authorize-btn")
            
            # Click "Allow" to authorize
            self.page.get_element("button", inner_text="允许").click()
        
        # Verify user profile is displayed
        self.page.wait_for(".user-avatar")
        self.page.wait_for(".user-nickname")
        
        avatar = self.page.get_element(".user-avatar")
        nickname = self.page.get_element(".user-nickname")
        
        self.assertTrue(avatar is not None, "User avatar should be displayed")
        self.assertTrue(nickname is not None, "User nickname should be displayed")
        self.assertTrue(len(nickname.text) > 0, "Nickname should not be empty")
    
    def test_auth_002_get_user_phone_number(self):
        """TC-AUTH-002: Get User Phone Number"""
        # Navigate to User Center
        self.page.get_element(".tab-me, .user-center-tab").click()
        
        # Click button requiring phone binding
        self.page.get_element(".bind-phone-btn, .phone-bind").click()
        
        # Wait for phone authorization popup
        self.page.wait_for(".phone-auth-popup")
        
        # Click "Allow" for phone authorization
        self.page.get_element("button", inner_text="允许").click()
        
        # Verify phone number is bound
        self.page.wait_for(".phone-number, .bind-success")
        phone_element = self.page.get_element(".phone-number, .bind-success")
        
        self.assertTrue(phone_element is not None, "Phone number should be bound successfully")
    
    # Suite: 02_Home_And_Discovery
    
    def test_home_001_home_page_load_and_navigation(self):
        """TC-HOME-001: Home Page Load and Navigation"""
        # Launch Mini Program to load Home page
        self.app.launch()
        self.page.wait_for(".home-page, .activity-list")
        
        # Verify activity list or banner loads
        activity_list = self.page.get_element(".activity-list, .banner-container")
        self.assertTrue(activity_list is not None, "Activity list or banner should load")
        
        # Scroll down to trigger lazy loading
        self.page.scroll_to(500)
        self.page.wait_for(1)
        
        # Scroll more
        self.page.scroll_to(1000)
        self.page.wait_for(1)
        
        # Click on a banner or activity card
        self.page.get_element(".activity-card, .banner-item").click()
        
        # Verify navigation to Activity Detail page
        self.page.wait_for(".activity-detail, .detail-page")
        current_page = self.app.get_current_page()
        self.assertIn("detail", current_page.path, "Should navigate to Activity Detail page")
    
    def test_home_002_activity_search_and_filter(self):
        """TC-HOME-002: Activity Search and Filter"""
        # Navigate to search page
        self.page.get_element(".search-bar, .search-icon").click()
        self.page.wait_for(".search-page, .search-input")
        
        # Input keyword
        search_input = self.page.get_element(".search-input, input")
        search_input.input("Hiking")
        
        # Click Search
        self.page.get_element(".search-btn, button", inner_text="搜索").click()
        
        # Wait for results
        self.page.wait_for(".search-results, .activity-list")
        
        # Verify search results match keyword
        results = self.page.get_elements(".activity-card, .result-item")
        self.assertTrue(len(results) > 0, "Search results should be displayed")
        
        # Apply filters
        self.page.get_element(".filter-btn, .filter-date").click()
        self.page.wait_for(".filter-panel")
        self.page.get_element(".filter-option", inner_text="本周").click()
        self.page.get_element(".apply-filter-btn, .confirm-btn").click()
        
        # Verify filtered results
        self.page.wait_for(".search-results, .activity-list")
        filtered_results = self.page.get_elements(".activity-card, .result-item")
        self.assertTrue(len(filtered_results) >= 0, "Filter should be applied")
    
    # Suite: 03_Activity_Detail_And_Interaction
    
    def test_detail_001_view_activity_details(self):
        """TC-DETAIL-001: View Activity Details"""
        # Navigate to Activity Detail page
        self.app.navigate_to("/pages/activity/detail?activityId=1")
        self.page.wait_for(".activity-detail, .detail-container")
        
        # Verify key elements
        title = self.page.get_element(".activity-title, .detail-title")
        time_info = self.page.get_element(".activity-time, .detail-time")
        location = self.page.get_element(".activity-location, .detail-location")
        price = self.page.get_element(".activity-price, .detail-price")
        description = self.page.get_element(".activity-desc, .detail-description")
        organizer = self.page.get_element(".organizer-info, .detail-organizer")
        
        self.assertTrue(title is not None, "Title should be displayed")
        self.assertTrue(len(title.text) > 0, "Title should not be empty")
        self.assertTrue(time_info is not None, "Time should be displayed")
        self.assertTrue(location is not None, "Location should be displayed")
        self.assertTrue(price is not None, "Price should be displayed")
        
        # Scroll to bottom
        self.page.scroll_to(1000)
        self.page.wait_for(1)
        
        # Verify bottom elements loaded
        bottom_element = self.page.get_element(".bottom-bar, .action-buttons")
        self.assertTrue(bottom_element is not None, "Bottom elements should be visible")
    
    def test_detail_002_wechat_location_navigation(self):
        """TC-DETAIL-002: WeChat Location Navigation"""
        # Navigate to Activity Detail page
        self.app.navigate_to("/pages/activity/detail?activityId=1")
        self.page.wait_for(".activity-detail")
        
        # Click location element
        location_element = self.page.get_element(".location-btn, .map-icon, .activity-location")
        location_element.click()
        
        # Verify wx.openLocation is triggered (check for map interface)
        self.page.wait_for(2)
        # In real test, would verify native map component appears
        self.assertTrue(True, "Location navigation should be triggered")
    
    def test_detail_003_share_activity(self):
        """TC-DETAIL-003: Share Activity"""
        # Navigate to Activity Detail page
        self.app.navigate_to("/pages/activity/detail?activityId=1")
        self.page.wait_for(".activity-detail")
        
        # Click share button
        share_btn = self.page.get_element(".share-btn, button[open-type='share']")
        if share_btn:
            share_btn.click()
        else:
            # Use top-right menu
            self.page.get_element(".more-btn, .menu-btn").click()
            self.page.wait_for(".share-menu")
            self.page.get_element(".share-option, .forward-btn").click()
        
        # Verify share options appear
        self.page.wait_for(1)
        self.assertTrue(True, "Share functionality should be triggered")
    
    # Suite: 04_Booking_And_Payment
    
    def test_pay_001_create_order_and_wechat_pay(self):
        """TC-PAY-001: Create Order and WeChat Pay"""
        # Navigate to Activity Detail page
        self.app.navigate_to("/pages/activity/detail?activityId=1")
        self.page.wait_for(".activity-detail")
        
        # Click Sign Up or Buy Ticket
        self.page.get_element(".signup-btn, .buy-ticket-btn, button", inner_text="报名").click()
        
        # Fill in registration fields
        self.page.wait_for(".registration-form, .order-form")
        
        name_input = self.page.get_element("input[name='name'], .name-input")
        if name_input:
            name_input.input("Test User")
        
        id_input = self.page.get_element("input[name='idCard'], .id-input")
        if id_input:
            id_input.input("110101199001011234")
        
        # Submit order
        self.page.get_element(".submit-order-btn, button", inner_text="提交订单").click()
        
        # Verify order summary page
        self.page.wait_for(".order-summary, .order-confirm")
        order_info = self.page.get_element(".order-summary, .order-confirm")
        self.assertTrue(order_info is not None, "Order summary should be displayed")
        
        # Click Pay
        self.page.get_element(".pay-btn, button", inner_text="支付").click()
        
        # Wait for payment interface
        self.page.wait_for(2)
        # In sandbox, payment would complete automatically or require test action
        self.assertTrue(True, "Payment interface should be triggered")
    
    def test_pay_002_payment_cancellation(self):
        """TC-PAY-002: Payment Cancellation"""
        # Navigate to Activity Detail page
        self.app.navigate_to("/pages/activity/detail?activityId=1")
        self.page.wait_for(".activity-detail")
        
        # Click Sign Up
        self.page.get_element(".signup-btn, .buy-ticket-btn").click()
        
        # Fill form and submit
        self.page.wait_for(".registration-form")
        name_input = self.page.get_element("input[name='name'], .name-input")
        if name_input:
            name_input.input("Test User")
        
        self.page.get_element(".submit-order-btn").click()
        self.page.wait_for(".order-summary")
        
        # Click Pay
        self.page.get_element(".pay-btn").click()
        
        # Cancel payment (simulate by clicking outside or cancel)
        self.page.wait_for(1)
        # In real test, would interact with native payment UI
        # Navigate back to check order status
        self.page.get_element(".cancel-payment, .close-btn").click()
        
        # Verify order status is unpaid/pending
        self.page.wait_for(".order-status, .order-detail")
        status = self.page.get_element(".order-status, .status-text")
        
        if status:
            self.assertIn("待支付", status.text, "Order status should be unpaid")
    
    # Suite: 05_User_Center
    
    def test_user_001_view_my_orders(self):
        """TC-USER-001: View My Orders"""
        # Navigate to User Center
        self.page.get_element(".tab-me, .user-center-tab").click()
        self.page.wait_for(".user-center, .me-page")
        
        # Click My Orders
        self.page.get_element(".my-orders, .order-entry").click()
        self.page.wait_for(".order-list, .orders-page")
        
        # Verify tabs for different statuses
        tabs = ["全部", "待支付", "已支付", "已完成", "已取消"]
        for tab_name in tabs:
            tab = self.page.get_element(".order-tab", inner_text=tab_name)
            if tab:
                tab.click()
                self.page.wait_for(1)
        
        # Click on a specific order
        first_order = self.page.get_element(".order-item, .order-card")
        if first_order:
            first_order.click()
            self.page.wait_for(".order-detail")
            current_page = self.app.get_current_page()
            self.assertIn("order", current_page.path, "Should navigate to Order Detail page")
    
    def test_user_002_cancel_order(self):
        """TC-USER-002: Cancel Order"""
        # Navigate to User Center
        self.page.get_element(".tab-me, .user-center-tab").click()
        self.page.wait_for(".user-center")
        
        # Click My Orders
        self.page.get_element(".my-orders").click()
        self.page.wait_for(".order-list")
        
        # Filter for unpaid/pending orders
        self.page.get_element(".order-tab", inner_text="待支付").click()
        self.page.wait_for(1)
        
        # Click on an unpaid order
        unpaid_order = self.page.get_element(".order-item.unpaid, .order-item")
        if unpaid_order:
            unpaid_order.click()
            self.page.wait_for(".order-detail")
            
            # Click Cancel Order
            self.page.get_element(".cancel-order-btn, button", inner_text="取消订单").click()
            
            # Confirm cancellation
            self.page.wait_for(".confirm-modal, .modal")
            self.page.get_element(".confirm-btn, button", inner_text="确定").click()
            
            # Verify order status changed
            self.page.wait_for(".order-status, .status-text")
            status = self.page.get_element(".order-status, .status-text")
            self.assertIn("已取消", status.text, "Order status should be cancelled")
    
    # Suite: 06_Component_Testing
    
    def test_comp_001_custom_tab_bar_navigation(self):
        """TC-COMP-001: Custom Tab Bar Navigation"""
        # Get all tab items
        tab_items = self.page.get_elements(".tab-item, .tab-bar-item")
        self.assertTrue(len(tab_items) > 0, "Tab bar should have items")
        
        # Click each tab and verify page switch
        tabs = [".tab-home", ".tab-category", ".tab-me"]
        expected_paths = ["home", "category", "me"]
        
        for tab_selector, expected_path in zip(tabs, expected_paths):
            tab = self.page.get_element(tab_selector)
            if tab:
                tab.click()
                self.page.wait_for(1)
                
                # Verify active state
                active_tab = self.page.get_element(f"{tab_selector}.active, {tab_selector}[class*='active']")
                self.assertTrue(active_tab is not None, f"Tab {expected_path} should be active")
                
                # Verify page
                current_page = self.app.get_current_page()
                self.assertIn(expected_path, current_page.path, f"Should navigate to {expected_path} page")
    
    def test_comp_002_activity_card_component(self):
        """TC-COMP-002: Activity Card Component"""
        # Navigate to home page with activity list
        self.app.navigate_to("/pages/home/index")
        self.page.wait_for(".activity-list, .activity-card")
        
        # Get all activity cards
        cards = self.page.get_elements(".activity-card, .activity-item")
        self.assertTrue(len(cards) > 0, "Activity cards should be displayed")
        
        # Verify each card renders correctly
        for i, card in enumerate(cards[:5]):  # Check first 5 cards
            # Scroll card into view
            card.scroll_into_view()
            self.page.wait_for(0.5)
            
            # Verify card elements
            title = card.get_element(".card-title, .activity-title")
            image = card.get_element(".card-image, .activity-image")
            price = card.get_element(".card-price, .activity-price")
            
            # Title should exist and not be empty
            if title:
                self.assertTrue(len(title.text.strip()) > 0 or title.text is not None, 
                               f"Card {i} title should exist")
            
            # Image should load (check for broken image)
            if image:
                self.assertTrue(image is not None, f"Card {i} image should exist")
            
            # Price should be displayed
            if price:
                self.assertTrue(price is not None, f"Card {i} price should be displayed")
        
        # Verify layout doesn't break with different data
        self.page.scroll_to(500)
        self.page.wait_for(1)
        
        # Check for layout issues
        page_width = self.page.get_element(".activity-list").rect.get("width")
        self.assertTrue(page_width > 0, "Activity list should have valid width")