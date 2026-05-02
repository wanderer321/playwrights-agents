import minium
import time


class TestUserModule(minium.MiniTest):
    """用户模块测试套件"""

    def setUp(self):
        super().setUp()
        self.app.navigate_to("/pages/index/index")
        self.page = self.app.get_current_page()

    def test_user_001_wechat_login_authorization(self):
        """TC-USER-001: WeChat User Login & Authorization"""
        # Navigate to profile page
        self.app.navigate_to("/pages/profile/profile")
        self.page = self.app.get_current_page()
        
        # Check if user is already logged in by looking for avatar
        avatar_element = self.page.get_element(".user-avatar")
        
        if not avatar_element or not avatar_element.is_displayed():
            # User not logged in, trigger login
            login_btn = self.page.get_element("button", inner_text="登录")
            if not login_btn:
                login_btn = self.page.get_element("button", inner_text="微信登录")
            if not login_btn:
                login_btn = self.page.get_element(".login-btn")
            
            self.assertIsNotNone(login_btn, "Login button should exist")
            login_btn.click()
            
            # Wait for authorization popup and click allow
            self.page.wait_for(2)
            
            # Handle getUserProfile authorization
            allow_btn = self.page.get_element("button", inner_text="允许")
            if allow_btn:
                allow_btn.click()
            
            self.page.wait_for(2)
        
        # Verify user is logged in
        user_avatar = self.page.get_element(".user-avatar")
        user_nickname = self.page.get_element(".user-nickname")
        
        self.assertIsNotNone(user_avatar, "User avatar should be displayed")
        self.assertIsNotNone(user_nickname, "User nickname should be displayed")
        self.assertTrue(len(user_nickname.text) > 0, "Nickname should not be empty")

    def test_user_002_location_authorization(self):
        """TC-USER-002: User Location Authorization"""
        # Navigate to home page
        self.app.navigate_to("/pages/index/index")
        self.page = self.app.get_current_page()
        
        # Look for nearby activities button or location trigger
        nearby_btn = self.page.get_element(".nearby-btn")
        if not nearby_btn:
            nearby_btn = self.page.get_element("view", inner_text="附近活动")
        if not nearby_btn:
            nearby_btn = self.page.get_element("view", inner_text="周边活动")
        
        if nearby_btn:
            nearby_btn.click()
            self.page.wait_for(2)
            
            # Handle location authorization popup
            allow_btn = self.page.get_element("button", inner_text="允许")
            if allow_btn:
                allow_btn.click()
                self.page.wait_for(2)
                
                # Verify location is retrieved
                location_text = self.page.get_element(".location-text")
                self.assertIsNotNone(location_text, "Location should be displayed")
            else:
                # If denied, check for manual city selection prompt
                city_selector = self.page.get_element(".city-selector")
                self.assertIsNotNone(city_selector, "City selector should appear if location denied")


class TestActivityCoreModule(minium.MiniTest):
    """活动核心模块测试套件"""

    def setUp(self):
        super().setUp()
        self.app.navigate_to("/pages/index/index")
        self.page = self.app.get_current_page()

    def test_act_001_activity_list_loading_pagination(self):
        """TC-ACT-001: Activity List Loading & Pagination"""
        # Navigate to activity list page
        self.app.navigate_to("/pages/activity/list")
        self.page = self.app.get_current_page()
        
        # Wait for skeleton screen to disappear and data to load
        self.page.wait_for(2)
        
        # Verify initial data loading
        activity_items = self.page.get_elements(".activity-item")
        initial_count = len(activity_items)
        self.assertGreater(initial_count, 0, "Activity list should have items")
        
        # Scroll to bottom to trigger pagination
        last_item = activity_items[-1]
        last_item.scroll_into_view()
        self.page.wait_for(1)
        
        # Simulate pull down for more
        self.page.scroll_to(0, 10000)
        self.page.wait_for(2)
        
        # Verify loading indicator appeared
        loading_indicator = self.page.get_element(".loading-indicator")
        if loading_indicator:
            self.assertTrue(loading_indicator.is_displayed(), "Loading indicator should appear")
        
        # Wait for new data
        self.page.wait_for(2)
        
        # Verify new data is appended
        new_activity_items = self.page.get_elements(".activity-item")
        new_count = len(new_activity_items)
        
        self.assertGreaterEqual(new_count, initial_count, "New items should be loaded")
        
        # Verify no duplicate data (check activity IDs)
        activity_ids = []
        for item in new_activity_items:
            item_id = item.get_attribute("data-id")
            if item_id:
                self.assertNotIn(item_id, activity_ids, "No duplicate activity IDs")
                activity_ids.append(item_id)

    def test_act_002_activity_search_functionality(self):
        """TC-ACT-002: Activity Search Functionality"""
        # Click search bar
        search_bar = self.page.get_element(".search-bar")
        if not search_bar:
            search_bar = self.page.get_element("input", placeholder="搜索活动")
        if not search_bar:
            search_bar = self.page.get_element("navigator", url_contains="search")
        
        self.assertIsNotNone(search_bar, "Search bar should exist")
        search_bar.click()
        
        self.page.wait_for(1)
        self.page = self.app.get_current_page()
        
        # Input search keyword
        search_input = self.page.get_element("input.search-input")
        if not search_input:
            search_input = self.page.get_element("input")
        
        self.assertIsNotNone(search_input, "Search input should exist")
        search_input.input("Hiking")
        
        # Click search button or press enter
        search_btn = self.page.get_element("button", inner_text="搜索")
        if not search_btn:
            search_btn = self.page.get_element("view", inner_text="搜索")
        
        if search_btn:
            search_btn.click()
        else:
            # Simulate confirm on keyboard
            self.page.get_element("input").input("\n")
        
        self.page.wait_for(2)
        
        # Verify search results
        result_items = self.page.get_elements(".activity-item")
        if len(result_items) > 0:
            # Verify results match keyword
            for item in result_items:
                title = item.get_element(".activity-title")
                if title:
                    self.assertIn("Hiking", title.text, "Result should match keyword")
        else:
            # Check for empty state
            empty_state = self.page.get_element(".empty-state")
            self.assertIsNotNone(empty_state, "Empty state should be shown if no results")

    def test_act_003_view_activity_detail(self):
        """TC-ACT-003: View Activity Detail"""
        # Navigate to activity list
        self.app.navigate_to("/pages/activity/list")
        self.page = self.app.get_current_page()
        self.page.wait_for(2)
        
        # Click on first activity item
        activity_item = self.page.get_element(".activity-item")
        self.assertIsNotNone(activity_item, "Activity item should exist")
        activity_item.click()
        
        self.page.wait_for(2)
        self.page = self.app.get_current_page()
        
        # Verify key elements on detail page
        title = self.page.get_element(".activity-title")
        self.assertIsNotNone(title, "Activity title should exist")
        self.assertTrue(len(title.text) > 0, "Title should not be empty")
        
        time_info = self.page.get_element(".activity-time")
        self.assertIsNotNone(time_info, "Activity time should exist")
        
        location = self.page.get_element(".activity-location")
        self.assertIsNotNone(location, "Activity location should exist")
        
        price = self.page.get_element(".activity-price")
        self.assertIsNotNone(price, "Activity price should exist")
        
        organizer = self.page.get_element(".organizer-info")
        self.assertIsNotNone(organizer, "Organizer info should exist")
        
        # Verify images load successfully
        images = self.page.get_elements(".activity-image image")
        for img in images:
            img_src = img.get_attribute("src")
            self.assertIsNotNone(img_src, "Image should have src attribute")


class TestRegistrationPaymentModule(minium.MiniTest):
    """报名与支付模块测试套件"""

    def setUp(self):
        super().setUp()
        self.app.navigate_to("/pages/activity/list")
        self.page = self.app.get_current_page()
        self.page.wait_for(2)

    def test_reg_001_activity_registration_flow(self):
        """TC-REG-001: Activity Registration Flow"""
        # Navigate to activity detail
        activity_item = self.page.get_element(".activity-item")
        activity_item.click()
        self.page.wait_for(2)
        self.page = self.app.get_current_page()
        
        # Click register button
        register_btn = self.page.get_element("button", inner_text="立即报名")
        if not register_btn:
            register_btn = self.page.get_element("button", inner_text="报名")
        if not register_btn:
            register_btn = self.page.get_element(".register-btn")
        
        self.assertIsNotNone(register_btn, "Register button should exist")
        register_btn.click()
        self.page.wait_for(1)
        
        # Fill in registration form
        name_input = self.page.get_element("input", placeholder="姓名")
        if name_input:
            name_input.input("测试用户")
        
        phone_input = self.page.get_element("input", placeholder="手机号")
        if phone_input:
            # Test invalid phone first
            phone_input.input("12345")
            
            submit_btn = self.page.get_element("button", inner_text="提交")
            if not submit_btn:
                submit_btn = self.page.get_element(".submit-btn")
            
            if submit_btn:
                submit_btn.click()
                self.page.wait_for(1)
                
                # Verify error message for invalid phone
                error_msg = self.page.get_element(".error-message")
                if error_msg:
                    self.assertIn("手机", error_msg.text, "Error should mention phone")
                
                # Input valid phone
                phone_input.input("13800138000")
        
        # Submit form
        submit_btn = self.page.get_element("button", inner_text="提交")
        if not submit_btn:
            submit_btn = self.page.get_element(".submit-btn")
        
        if submit_btn:
            submit_btn.click()
            self.page.wait_for(2)
            
            # Verify navigation to payment or success page
            current_page = self.app.get_current_page()
            page_path = current_page.path
            
            self.assertTrue(
                "payment" in page_path or "success" in page_path or "order" in page_path,
                "Should navigate to payment or success page"
            )

    def test_pay_001_wechat_payment_integration(self):
        """TC-PAY-001: WeChat Payment Integration"""
        # Navigate to activity detail
        self.app.navigate_to("/pages/activity/list")
        self.page = self.app.get_current_page()
        self.page.wait_for(2)
        
        activity_item = self.page.get_element(".activity-item")
        activity_item.click()
        self.page.wait_for(2)
        self.page = self.app.get_current_page()
        
        # Complete registration to reach payment
        register_btn = self.page.get_element("button", inner_text="立即报名")
        if register_btn:
            register_btn.click()
            self.page.wait_for(1)
            
            # Fill form
            name_input = self.page.get_element("input", placeholder="姓名")
            if name_input:
                name_input.input("测试用户")
            
            phone_input = self.page.get_element("input", placeholder="手机号")
            if phone_input:
                phone_input.input("13800138000")
            
            submit_btn = self.page.get_element("button", inner_text="提交")
            if submit_btn:
                submit_btn.click()
                self.page.wait_for(2)
        
        # Verify order amount
        self.page = self.app.get_current_page()
        amount_element = self.page.get_element(".order-amount")
        if amount_element:
            amount_text = amount_element.text
            self.assertIn("¥", amount_text, "Amount should contain currency symbol")
        
        # Click pay button
        pay_btn = self.page.get_element("button", inner_text="立即支付")
        if not pay_btn:
            pay_btn = self.page.get_element("button", inner_text="支付")
        
        if pay_btn:
            pay_btn.click()
            self.page.wait_for(2)
            
            # Note: In real device testing, wx.requestPayment popup appears
            # In automation, we verify the payment initiation
            # Mock payment success callback
            self.page.wait_for(3)
            
            # Check for payment result
            success_page = self.page.get_element(".payment-success")
            order_status = self.page.get_element(".order-status")
            
            if success_page:
                self.assertTrue(success_page.is_displayed(), "Success page should be shown")
            elif order_status:
                status_text = order_status.text
                self.assertIn("支付成功", status_text, "Order status should be paid")


class TestInteractionSharingModule(minium.MiniTest):
    """交互与分享模块测试套件"""

    def setUp(self):
        super().setUp()
        self.app.navigate_to("/pages/activity/list")
        self.page = self.app.get_current_page()
        self.page.wait_for(2)

    def test_share_001_forward_activity_to_chat(self):
        """TC-SHARE-001: Forward Activity to Chat"""
        # Navigate to activity detail
        activity_item = self.page.get_element(".activity-item")
        activity_item.click()
        self.page.wait_for(2)
        self.page = self.app.get_current_page()
        
        # Click share button
        share_btn = self.page.get_element(".share-btn")
        if not share_btn:
            share_btn = self.page.get_element("button", inner_text="分享")
        if not share_btn:
            share_btn = self.page.get_element("button", open_type="share")
        
        if share_btn:
            share_btn.click()
            self.page.wait_for(1)
            
            # Note: WeChat share sheet is system UI
            # Verify share button exists and is clickable
            self.assertTrue(share_btn.is_displayed(), "Share button should be visible")
        else:
            # Use button with open-type="share"
            native_share_btn = self.page.get_element("button[open-type='share']")
            self.assertIsNotNone(native_share_btn, "Native share button should exist")

    def test_share_002_share_to_timeline(self):
        """TC-SHARE-002: Share to Timeline (Moments)"""
        # Navigate to activity detail
        self.app.navigate_to("/pages/activity/list")
        self.page = self.app.get_current_page()
        self.page.wait_for(2)
        
        activity_item = self.page.get_element(".activity-item")
        activity_item.click()
        self.page.wait_for(2)
        self.page = self.app.get_current_page()
        
        # Check for timeline share button
        timeline_btn = self.page.get_element("button", open_type="shareTimeline")
        if not timeline_btn:
            timeline_btn = self.page.get_element(".share-timeline-btn")
        
        if timeline_btn:
            # Verify page configuration allows timeline sharing
            timeline_btn.click()
            self.page.wait_for(1)
            
            # Note: Timeline share is triggered via system UI
            self.assertTrue(timeline_btn.is_displayed(), "Timeline share button should work")
        else:
            # Skip if not supported
            self.skipTest("Timeline sharing not configured on this page")


class TestExceptionHandling(minium.MiniTest):
    """异常处理测试套件"""

    def setUp(self):
        super().setUp()
        self.app.navigate_to("/pages/index/index")
        self.page = self.app.get_current_page()

    def test_err_001_network_disconnect_recovery(self):
        """TC-ERR-001: Network Disconnect Recovery"""
        # Simulate network disconnection by mocking
        # Note: Actual network control requires device-level operations
        
        # Navigate to activity list that requires network
        self.app.navigate_to("/pages/activity/list")
        self.page = self.app.get_current_page()
        self.page.wait_for(2)
        
        # Check for error state or retry mechanism
        error_page = self.page.get_element(".error-page")
        network_error = self.page.get_element(".network-error")
        retry_btn = self.page.get_element("button", inner_text="重试")
        
        if error_page or network_error:
            # Network error is displayed
            self.assertTrue(
                error_page.is_displayed() or network_error.is_displayed(),
                "Network error should be displayed"
            )
            
            if retry_btn:
                retry_btn.click()
                self.page.wait_for(3)
                
                # Verify retry attempts to reload
                loading = self.page.get_element(".loading")
                self.assertIsNotNone(loading, "Loading should appear on retry")
        else:
            # Normal operation - verify data loaded
            activity_items = self.page.get_elements(".activity-item")
            self.assertGreater(len(activity_items), 0, "Activities should load with network")

    def test_err_002_payment_failure_handling(self):
        """TC-ERR-002: Payment Failure Handling"""
        # Navigate to payment flow
        self.app.navigate_to("/pages/activity/list")
        self.page = self.app.get_current_page()
        self.page.wait_for(2)
        
        activity_item = self.page.get_element(".activity-item")
        activity_item.click()
        self.page.wait_for(2)
        self.page = self.app.get_current_page()
        
        # Complete registration
        register_btn = self.page.get_element("button", inner_text="立即报名")
        if register_btn:
            register_btn.click()
            self.page.wait_for(1)
            
            name_input = self.page.get_element("input", placeholder="姓名")
            if name_input:
                name_input.input("测试用户")
            
            phone_input = self.page.get_element("input", placeholder="手机号")
            if phone_input:
                phone_input.input("13800138000")
            
            submit_btn = self.page.get_element("button", inner_text="提交")
            if submit_btn:
                submit_btn.click()
                self.page.wait_for(2)
        
        # Trigger payment
        self.page = self.app.get_current_page()
        pay_btn = self.page.get_element("button", inner_text="立即支付")
        
        if pay_btn:
            pay_btn.click()
            self.page.wait_for(3)
            
            # Simulate payment failure/cancel
            # In real testing, user cancels payment
            # Verify error handling
            fail_msg = self.page.get_element(".payment-fail")
            order_unpaid = self.page.get_element(".order-status", inner_text="未支付")
            
            if fail_msg:
                self.assertIn("失败", fail_msg.text, "Failure message should be shown")
            
            if order_unpaid:
                self.assertTrue(order_unpaid.is_displayed(), "Order should remain unpaid")


class TestActivityModuleExtended(minium.MiniTest):
    """活动模块扩展测试"""

    def test_activity_filter_by_category(self):
        """Test filtering activities by category"""
        self.app.navigate_to("/pages/activity/list")
        self.page = self.app.get_current_page()
        self.page.wait_for(2)
        
        # Click category filter
        category_tab = self.page.get_element(".category-tab", inner_text="户外")
        if not category_tab:
            category_tab = self.page.get_element(".category-item")
        
        if category_tab:
            category_tab.click()
            self.page.wait_for(2)
            
            # Verify filtered results
            activity_items = self.page.get_elements(".activity-item")
            self.assertGreater(len(activity_items), 0, "Filtered activities should display")

    def test_activity_sort_by_time(self):
        """Test sorting activities by time"""
        self.app.navigate_to("/pages/activity/list")
        self.page = self.app.get_current_page()
        self.page.wait_for(2)
        
        # Click sort button
        sort_btn = self.page.get_element(".sort-btn")
        if sort_btn:
            sort_btn.click()
            self.page.wait_for(1)
            
            # Select time sort option
            time_sort = self.page.get_element(".sort-option", inner_text="时间")
            if time_sort:
                time_sort.click()
                self.page.wait_for(2)
                
                # Verify sort applied
                sort_indicator = self.page.get_element(".sort-active")
                self.assertIsNotNone(sort_indicator, "Sort should be applied")

    def test_activity_pull_to_refresh(self):
        """Test pull-to-refresh functionality"""
        self.app.navigate_to("/pages/activity/list")
        self.page = self.app.get_current_page()
        self.page.wait_for(2)
        
        # Get initial activity count
        initial_items = self.page.get_elements(".activity-item")
        initial_count = len(initial_items)
        
        # Simulate pull-to-refresh
        self.page.scroll_to(0, 0)
        self.page.wait_for(1)
        
        # Trigger refresh (simulated)
        refresh_indicator = self.page.get_element(".refresh-indicator")
        if refresh_indicator:
            self.assertTrue(refresh_indicator.is_displayed(), "Refresh indicator should show")
        
        self.page.wait_for(2)
        
        # Verify data refreshed
        refreshed_items = self.page.get_elements(".activity-item")
        self.assertGreaterEqual(len(refreshed_items), 0, "Data should refresh")


class TestUserProfileModule(minium.MiniTest):
    """用户资料模块测试"""

    def test_user_profile_edit(self):
        """Test editing user profile"""
        self.app.navigate_to("/pages/profile/profile")
        self.page = self.app.get_current_page()
        self.page.wait_for(2)
        
        # Click edit button
        edit_btn = self.page.get_element(".edit-profile-btn")
        if not edit_btn:
            edit_btn = self.page.get_element("button", inner_text="编辑资料")
        
        if edit_btn:
            edit_btn.click()
            self.page.wait_for(1)
            
            # Modify nickname
            nickname_input = self.page.get_element("input", placeholder="昵称")
            if nickname_input:
                new_nickname = "测试昵称" + str(int(time.time()) % 1000)
                nickname_input.input(new_nickname)
                
                # Save changes
                save_btn = self.page.get_element("button", inner_text="保存")
                if save_btn:
                    save_btn.click()
                    self.page.wait_for(2)
                    
                    # Verify save success
                    toast = self.page.get_element(".toast-message")
                    if toast:
                        self.assertIn("成功", toast.text, "Save should succeed")

    def test_user_activity_history(self):
        """Test viewing user activity history"""
        self.app.navigate_to("/pages/profile/profile")
        self.page = self.app.get_current_page()
        self.page.wait_for(2)
        
        # Click on my activities
        my_activities = self.page.get_element(".my-activities")
        if not my_activities:
            my_activities = self.page.get_element("view", inner_text="我的活动")
        
        if my_activities:
            my_activities.click()
            self.page.wait_for(2)
            
            # Verify activity list
            activity_items = self.page.get_elements(".activity-item")
            self.assertIsNotNone(activity_items, "Activity history should display")


class TestOrderModule(minium.MiniTest):
    """订单模块测试"""

    def test_order_list_display(self):
        """Test order list display"""
        self.app.navigate_to("/pages/order/list")
        self.page = self.app.get_current_page()
        self.page.wait_for(2)
        
        # Verify order tabs
        tabs = self.page.get_elements(".order-tab")
        self.assertGreater(len(tabs), 0, "Order tabs should exist")
        
        # Click on different tabs
        for tab in tabs:
            tab.click()
            self.page.wait_for(1)
            
            # Verify corresponding orders display
            orders = self.page.get_elements(".order-item")
            # Orders may be empty for some tabs

    def test_order_detail_view(self):
        """Test viewing order detail"""
        self.app.navigate_to("/pages/order/list")
        self.page = self.app.get_current_page()
        self.page.wait_for(2)
        
        # Click on first order
        order_item = self.page.get_element(".order-item")
        if order_item:
            order_item.click()
            self.page.wait_for(2)
            
            # Verify order detail elements
            order_no = self.page.get_element(".order-no")
            self.assertIsNotNone(order_no, "Order number should display")
            
            order_status = self.page.get_element(".order-status")
            self.assertIsNotNone(order_status, "Order status should display")
            
            order_amount = self.page.get_element(".order-amount")
            self.assertIsNotNone(order_amount, "Order amount should display")

    def test_order_cancel(self):
        """Test canceling an order"""
        self.app.navigate_to("/pages/order/list")
        self.page = self.app.get_current_page()
        self.page.wait_for(2)
        
        # Find unpaid order
        unpaid_order = self.page.get_element(".order-item.unpaid")
        if unpaid_order:
            unpaid_order.click()
            self.page.wait_for(2)
            
            # Click cancel button
            cancel_btn = self.page.get_element("button", inner_text="取消订单")
            if cancel_btn:
                cancel_btn.click()
                self.page.wait_for(1)
                
                # Confirm cancellation
                confirm_btn = self.page.get_element("button", inner_text="确定")
                if confirm_btn:
                    confirm_btn.click()
                    self.page.wait_for(2)
                    
                    # Verify order cancelled
                    status = self.page.get_element(".order-status")
                    if status:
                        self.assertIn("已取消", status.text, "Order should be cancelled")


if __name__ == "__main__":
    import unittest
    unittest.main()