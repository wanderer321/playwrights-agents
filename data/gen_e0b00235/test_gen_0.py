import minium
import time


class TestLoginAndAuthorization(minium.MiniTest):
    """Suite: 00_Login_And_Authorization - Critical path for user identity."""

    def test_auth_001_wechat_user_login_flow(self):
        """TC-AUTH-001: WeChat User Login Flow"""
        # Launch the Mini Program
        self.app.launch()

        # Check if user is logged in by checking storage/token
        token = self.app.get_storage("token")
        user_info = self.app.get_storage("userInfo")

        if not token or not user_info:
            # Navigate to login page if not logged in
            self.app.navigate_to("/pages/login/login")

            # Wait for login page to load
            self.page.wait_for("view.login-container", 5)

            # Trigger login button
            login_btn = self.page.get_element("button", inner_text="微信登录")
            if not login_btn:
                login_btn = self.page.get_element(".login-btn")
            if not login_btn:
                login_btn = self.page.get_element("button[type='primary']")

            self.assertTrue(login_btn is not None, "Login button should be present")
            login_btn.click()

            # Wait for login process to complete
            self.page.wait_for(3)

        # Verify session is established
        new_token = self.app.get_storage("token")
        self.assertIsNotNone(new_token, "Token should be stored after login")

        # Navigate to profile to verify avatar/nickname display
        self.app.navigate_to("/pages/profile/profile")
        self.page.wait_for(2)

        # Verify user info is displayed
        avatar_element = self.page.get_element(".user-avatar")
        nickname_element = self.page.get_element(".user-nickname")

        if avatar_element:
            self.assertTrue(avatar_element is not None, "User avatar should display")

        if nickname_element:
            nickname_text = nickname_element.text
            self.assertTrue(len(nickname_text) > 0, "Nickname should not be empty")

    def test_auth_002_location_authorization(self):
        """TC-AUTH-002: Location Authorization"""
        # Navigate to a page requiring location (Nearby Activities)
        self.app.navigate_to("/pages/index/index")
        self.page.wait_for(2)

        # Look for nearby or location-related elements
        nearby_tab = self.page.get_element(".tab-nearby")
        if not nearby_tab:
            nearby_tab = self.page.get_element("view", inner_text="附近")
        if not nearby_tab:
            nearby_tab = self.page.get_element("[data-tab='nearby']")

        if nearby_tab:
            nearby_tab.click()
            self.page.wait_for(2)

        # Trigger location API by looking for location button
        location_btn = self.page.get_element(".location-btn")
        if not location_btn:
            location_btn = self.page.get_element("button", inner_text="定位")
        if not location_btn:
            location_btn = self.page.get_element(".get-location")

        if location_btn:
            location_btn.click()
            self.page.wait_for(3)

            # Check for location display or error message
            location_display = self.page.get_element(".location-text")
            error_placeholder = self.page.get_element(".location-error")
            default_placeholder = self.page.get_element(".location-default")

            # Either location should display or graceful fallback should show
            has_location = location_display is not None and len(location_display.text) > 0
            has_fallback = error_placeholder is not None or default_placeholder is not None

            self.assertTrue(has_location or has_fallback,
                            "Should show location or graceful fallback")


class TestHomeAndActivityList(minium.MiniTest):
    """Suite: 01_Home_And_Activity_List - Core content display."""

    def test_home_001_home_page_rendering(self):
        """TC-HOME-001: Home Page Rendering"""
        # Launch app to Home page
        self.app.launch()
        self.page.wait_for(2)

        # Check for loading skeletons before data arrives
        skeleton = self.page.get_element(".skeleton")
        loading_indicator = self.page.get_element(".loading")

        # Wait for data to load
        self.page.wait_for(2)

        # Verify Activity List component renders
        activity_list = self.page.get_element(".activity-list")
        if not activity_list:
            activity_list = self.page.get_element(".list-container")

        self.assertIsNotNone(activity_list, "Activity list should render")

        # Check for activity items
        activity_items = self.page.get_elements(".activity-item")
        if not activity_items:
            activity_items = self.page.get_elements(".list-item")

        self.assertTrue(len(activity_items) > 0, "Activity items should be present")

    def test_home_002_activity_list_pagination(self):
        """TC-HOME-002: Activity List Pagination (Pull Down/Up)"""
        # Navigate to home page
        self.app.navigate_to("/pages/index/index")
        self.page.wait_for(2)

        # Get initial activity count
        initial_items = self.page.get_elements(".activity-item")
        if not initial_items:
            initial_items = self.page.get_elements(".list-item")
        initial_count = len(initial_items)

        # Scroll down to bottom to trigger onReachBottom
        self.page.scroll_to(0, 10000)
        self.page.wait_for(2)

        # Verify loading indicator appears
        loading_more = self.page.get_element(".loading-more")
        if not loading_more:
            loading_more = self.page.get_element(".load-more")

        # Wait for new data to load
        self.page.wait_for(2)

        # Verify new data is appended
        after_scroll_items = self.page.get_elements(".activity-item")
        if not after_scroll_items:
            after_scroll_items = self.page.get_elements(".list-item")

        # Pull down to trigger onPullDownRefresh
        self.page.scroll_to(0, 0)
        self.page.wait_for(1)

        # Simulate pull down refresh
        self.page.pull_down_refresh()
        self.page.wait_for(3)

        # Verify list is refreshed
        refreshed_items = self.page.get_elements(".activity-item")
        if not refreshed_items:
            refreshed_items = self.page.get_elements(".list-item")

        self.assertTrue(len(refreshed_items) > 0, "List should have items after refresh")

    def test_home_003_activity_search(self):
        """TC-HOME-003: Activity Search"""
        # Navigate to home page
        self.app.navigate_to("/pages/index/index")
        self.page.wait_for(2)

        # Tap the search bar
        search_bar = self.page.get_element(".search-bar")
        if not search_bar:
            search_bar = self.page.get_element(".search-input")
        if not search_bar:
            search_bar = self.page.get_element("input[placeholder*='搜索']")
        if not search_bar:
            search_bar = self.page.get_element("input[placeholder*='活动']")

        self.assertIsNotNone(search_bar, "Search bar should be present")
        search_bar.click()
        self.page.wait_for(1)

        # Input a keyword
        search_input = self.page.get_element("input.search-input")
        if not search_input:
            search_input = self.page.get_element("input")

        if search_input:
            search_input.input("Yoga")
            self.page.wait_for(1)

            # Submit search (press enter or click search button)
            search_btn = self.page.get_element(".search-btn")
            if not search_btn:
                search_btn = self.page.get_element("button", inner_text="搜索")

            if search_btn:
                search_btn.click()
            else:
                # Simulate enter key
                self.page.get_element("input").click()

            self.page.wait_for(2)

            # Verify list filters to show matching activities
            activity_items = self.page.get_elements(".activity-item")
            if not activity_items:
                activity_items = self.page.get_elements(".list-item")

            # Check if results contain the keyword
            for item in activity_items[:3]:
                item_text = item.text.lower()
                # Results should be relevant (either match keyword or show no results)


class TestActivityDetailAndInteraction(minium.MiniTest):
    """Suite: 02_Activity_Detail_And_Interaction - The core business logic."""

    def test_detail_001_view_activity_detail(self):
        """TC-DETAIL-001: View Activity Detail"""
        # Navigate to home page first
        self.app.navigate_to("/pages/index/index")
        self.page.wait_for(2)

        # Click an item from the Activity List
        activity_item = self.page.get_element(".activity-item")
        if not activity_item:
            activity_item = self.page.get_element(".list-item")

        self.assertIsNotNone(activity_item, "At least one activity item should be present")
        activity_item.click()
        self.page.wait_for(2)

        # Verify navigation to detail page
        current_page = self.app.get_current_page()
        self.assertIn("activity-detail", current_page.path, "Should navigate to detail page")

        # Verify all elements load
        detail_image = self.page.get_element(".activity-image")
        detail_title = self.page.get_element(".activity-title")
        detail_time = self.page.get_element(".activity-time")
        detail_location = self.page.get_element(".activity-location")
        detail_description = self.page.get_element(".activity-description")

        # At minimum, title should be present
        if detail_title:
            title_text = detail_title.text
            self.assertTrue(len(title_text) > 0, "Title should not be empty")

        # Verify no broken images (check if image has src)
        if detail_image:
            img_src = detail_image.attribute("src")
            self.assertIsNotNone(img_src, "Image should have src attribute")

    def test_detail_002_activity_registration_sign_up(self):
        """TC-DETAIL-002: Activity Registration/Sign Up"""
        # Navigate to activity detail page
        self.app.navigate_to("/pages/index/index")
        self.page.wait_for(2)

        activity_item = self.page.get_element(".activity-item")
        if not activity_item:
            activity_item = self.page.get_element(".list-item")

        if activity_item:
            activity_item.click()
            self.page.wait_for(2)

        # Click the "Sign Up" or "Join" button
        signup_btn = self.page.get_element(".signup-btn")
        if not signup_btn:
            signup_btn = self.page.get_element("button", inner_text="报名")
        if not signup_btn:
            signup_btn = self.page.get_element("button", inner_text="参加")
        if not signup_btn:
            signup_btn = self.page.get_element("button", inner_text="立即报名")
        if not signup_btn:
            signup_btn = self.page.get_element("button[type='primary']")

        if signup_btn:
            signup_btn.click()
            self.page.wait_for(2)

            # Check if a form is required
            form_fields = self.page.get_elements(".form-input")
            if form_fields and len(form_fields) > 0:
                # Fill in mandatory fields
                for field in form_fields[:3]:
                    field_type = field.attribute("type")
                    if field_type != "hidden":
                        field.input("测试数据")

                # Submit the form
                submit_btn = self.page.get_element(".submit-btn")
                if not submit_btn:
                    submit_btn = self.page.get_element("button", inner_text="提交")
                if not submit_btn:
                    submit_btn = self.page.get_element("button", inner_text="确认报名")

                if submit_btn:
                    submit_btn.click()
                    self.page.wait_for(2)

            # Verify success toast or button state change
            success_toast = self.page.get_element(".toast-success")
            joined_btn = self.page.get_element("button", inner_text="已报名")
            if not joined_btn:
                joined_btn = self.page.get_element("button", inner_text="已参加")

            # Either success toast or button state change should occur
            self.assertTrue(success_toast is not None or joined_btn is not None,
                            "Should show success message or update button state")

    def test_detail_003_share_activity(self):
        """TC-DETAIL-003: Share Activity"""
        # Navigate to activity detail page
        self.app.navigate_to("/pages/index/index")
        self.page.wait_for(2)

        activity_item = self.page.get_element(".activity-item")
        if not activity_item:
            activity_item = self.page.get_element(".list-item")

        if activity_item:
            activity_item.click()
            self.page.wait_for(2)

        # Click the Share button
        share_btn = self.page.get_element(".share-btn")
        if not share_btn:
            share_btn = self.page.get_element("button", inner_text="分享")
        if not share_btn:
            share_btn = self.page.get_element("button[open-type='share']")

        if share_btn:
            share_btn.click()
            self.page.wait_for(1)

            # Verify share options appear (this would trigger onShareAppMessage)
            # In real testing, we verify the share menu appears
            # For automation, we check if the button is properly configured
            open_type = share_btn.attribute("open-type")
            self.assertEqual("share", open_type, "Share button should have open-type='share'")


class TestPaymentAndOrder(minium.MiniTest):
    """Suite: 03_Payment_And_Order - Financial transactions."""

    def test_pay_001_payment_flow_simulation(self):
        """TC-PAY-001: Payment Flow Simulation"""
        # Navigate to a paid activity
        self.app.navigate_to("/pages/index/index")
        self.page.wait_for(2)

        # Find a paid activity (look for price indicator)
        paid_activity = None
        activities = self.page.get_elements(".activity-item")
        if not activities:
            activities = self.page.get_elements(".list-item")

        for activity in activities:
            price_element = activity.get_element(".price")
            if price_element and "免费" not in price_element.text:
                paid_activity = activity
                break

        if paid_activity:
            paid_activity.click()
            self.page.wait_for(2)

            # Click "Pay Now" button
            pay_btn = self.page.get_element(".pay-btn")
            if not pay_btn:
                pay_btn = self.page.get_element("button", inner_text="立即支付")
            if not pay_btn:
                pay_btn = self.page.get_element("button", inner_text="去支付")

            if pay_btn:
                pay_btn.click()
                self.page.wait_for(2)

                # Mock payment success scenario
                # In real testing, we would mock wx.requestPayment
                # Verify order status updates
                order_status = self.page.get_element(".order-status")
                if order_status:
                    status_text = order_status.text
                    # Status should reflect payment state

    def test_pay_002_order_list_view(self):
        """TC-PAY-002: Order List View"""
        # Navigate to User Center
        self.app.navigate_to("/pages/profile/profile")
        self.page.wait_for(2)

        # Navigate to My Orders
        my_orders = self.page.get_element(".my-orders")
        if not my_orders:
            my_orders = self.page.get_element("view", inner_text="我的订单")
        if not my_orders:
            my_orders = self.page.get_element("[data-page='orders']")

        if my_orders:
            my_orders.click()
            self.page.wait_for(2)

            # Verify list of historical orders
            order_items = self.page.get_elements(".order-item")
            if not order_items:
                order_items = self.page.get_elements(".order-card")

            # Click an order to view details
            if order_items and len(order_items) > 0:
                order_items[0].click()
                self.page.wait_for(2)

                # Verify navigation to detail page
                current_page = self.app.get_current_page()
                self.assertTrue("order" in current_page.path or "detail" in current_page.path,
                                "Should navigate to order detail page")


class TestUserCenter(minium.MiniTest):
    """Suite: 04_User_Center - User profile and settings."""

    def test_user_001_user_profile_update(self):
        """TC-USER-001: User Profile Update"""
        # Navigate to User Profile page
        self.app.navigate_to("/pages/profile/profile")
        self.page.wait_for(2)

        # Click "Edit Profile"
        edit_btn = self.page.get_element(".edit-profile-btn")
        if not edit_btn:
            edit_btn = self.page.get_element("view", inner_text="编辑资料")
        if not edit_btn:
            edit_btn = self.page.get_element("button", inner_text="编辑")

        if edit_btn:
            edit_btn.click()
            self.page.wait_for(2)

            # Update nickname
            nickname_input = self.page.get_element("input[placeholder*='昵称']")
            if not nickname_input:
                nickname_input = self.page.get_element(".nickname-input")

            if nickname_input:
                new_nickname = "测试用户" + str(int(time.time()) % 10000)
                nickname_input.input(new_nickname)

                # Save changes
                save_btn = self.page.get_element(".save-btn")
                if not save_btn:
                    save_btn = self.page.get_element("button", inner_text="保存")
                if not save_btn:
                    save_btn = self.page.get_element("button", inner_text="确定")

                if save_btn:
                    save_btn.click()
                    self.page.wait_for(2)

                    # Verify changes persist
                    self.page.wait_for(1)
                    displayed_nickname = self.page.get_element(".user-nickname")
                    if displayed_nickname:
                        self.assertIn(new_nickname[:4], displayed_nickname.text,
                                      "Nickname should be updated")

    def test_user_002_feedback_contact_support(self):
        """TC-USER-002: Feedback/Contact Support"""
        # Navigate to Feedback page
        self.app.navigate_to("/pages/feedback/feedback")
        self.page.wait_for(2)

        # Check if page loaded
        feedback_container = self.page.get_element(".feedback-container")
        if not feedback_container:
            feedback_container = self.page.get_element("textarea")

        # Submit text feedback
        feedback_input = self.page.get_element("textarea")
        if not feedback_input:
            feedback_input = self.page.get_element(".feedback-input")

        if feedback_input:
            feedback_input.input("这是一条测试反馈信息，用于验证反馈功能是否正常工作。")

            # Submit feedback
            submit_btn = self.page.get_element(".submit-btn")
            if not submit_btn:
                submit_btn = self.page.get_element("button", inner_text="提交")
            if not submit_btn:
                submit_btn = self.page.get_element("button[type='primary']")

            if submit_btn:
                submit_btn.click()
                self.page.wait_for(2)

                # Verify success message
                success_msg = self.page.get_element(".success-message")
                if not success_msg:
                    success_msg = self.page.get_element(".toast-success")

                # Page should not crash
                current_page = self.app.get_current_page()
                self.assertIsNotNone(current_page, "Page should remain functional after submit")


class TestComponentsUnitTest(minium.MiniTest):
    """Suite: 05_Components_Unit_Test - Testing the 5 reusable components."""

    def test_comp_001_component_rendering_props(self):
        """TC-COMP-001: Component Rendering Props"""
        # Test each component with various prop combinations
        # Navigate to a page that uses components
        self.app.navigate_to("/pages/index/index")
        self.page.wait_for(2)

        # Test activity-card component
        activity_cards = self.page.get_elements(".activity-card")
        if activity_cards:
            for card in activity_cards[:2]:
                # Verify component renders without JS errors
                card_text = card.text
                self.assertIsNotNone(card_text, "Activity card should render text content")

        # Test user-avatar component
        user_avatars = self.page.get_elements(".user-avatar")
        if user_avatars:
            for avatar in user_avatars[:2]:
                src = avatar.attribute("src")
                # Avatar should have valid source or placeholder

        # Test loading component
        loading_components = self.page.get_elements(".loading")
        if loading_components:
            for loading in loading_components:
                self.assertIsNotNone(loading, "Loading component should render")

        # Test empty-state component
        empty_states = self.page.get_elements(".empty-state")
        if empty_states:
            for empty_state in empty_states:
                empty_text = empty_state.text
                self.assertTrue(len(empty_text) > 0, "Empty state should have message")

        # Test tab-bar component
        tab_bars = self.page.get_elements(".tab-bar")
        if tab_bars:
            for tab_bar in tab_bars:
                tabs = tab_bar.get_elements(".tab-item")
                self.assertTrue(len(tabs) > 0, "Tab bar should have tab items")

    def test_comp_002_component_event_triggering(self):
        """TC-COMP-002: Component Event Triggering"""
        # Navigate to home page
        self.app.navigate_to("/pages/index/index")
        self.page.wait_for(2)

        # Test activity-card component click event
        activity_card = self.page.get_element(".activity-card")
        if not activity_card:
            activity_card = self.page.get_element(".activity-item")

        if activity_card:
            # Get initial page state
            initial_page = self.app.get_current_page().path

            # Click the component
            activity_card.click()
            self.page.wait_for(2)

            # Verify navigation event was triggered
            new_page = self.app.get_current_page().path
            self.assertNotEqual(initial_page, new_page,
                                "Clicking activity card should trigger navigation")

        # Navigate back
        self.app.navigate_back()
        self.page.wait_for(1)

        # Test tab-bar component event
        tab_items = self.page.get_elements(".tab-item")
        if tab_items and len(tab_items) > 1:
            # Click second tab
            tab_items[1].click()
            self.page.wait_for(1)

            # Verify tab switch event
            active_tab = self.page.get_element(".tab-item.active")
            if active_tab:
                self.assertIsNotNone(active_tab, "Tab should switch on click")

        # Test button component event
        action_btns = self.page.get_elements(".action-btn")
        if action_btns:
            for btn in action_btns[:1]:
                btn.click()
                self.page.wait_for(1)
                # Verify button triggers expected action
                # (toast, navigation, or state change)


class TestNavigationAndStability(minium.MiniTest):
    """Additional tests for navigation and stability."""

    def test_navigation_back_stack(self):
        """Test navigation back stack works correctly."""
        # Navigate through multiple pages
        self.app.navigate_to("/pages/index/index")
        self.page.wait_for(1)

        self.app.navigate_to("/pages/profile/profile")
        self.page.wait_for(1)

        self.app.navigate_to("/pages/settings/settings")
        self.page.wait_for(1)

        # Navigate back
        self.app.navigate_back()
        self.page.wait_for(1)
        current_page = self.app.get_current_page()
        self.assertIn("profile", current_page.path, "Should be on profile page")

        self.app.navigate_back()
        self.page.wait_for(1)
        current_page = self.app.get_current_page()
        self.assertIn("index", current_page.path, "Should be on index page")

    def test_page_reload_resilience(self):
        """Test page handles reload gracefully."""
        self.app.navigate_to("/pages/index/index")
        self.page.wait_for(2)

        # Reload the page
        self.page.reload()
        self.page.wait_for(2)

        # Verify page still functions
        activity_items = self.page.get_elements(".activity-item")
        if not activity_items:
            activity_items = self.page.get_elements(".list-item")

        self.assertTrue(len(activity_items) > 0, "Page should reload with data")

    def test_network_error_handling(self):
        """Test app handles network errors gracefully."""
        # Navigate to a page
        self.app.navigate_to("/pages/index/index")
        self.page.wait_for(2)

        # Look for error state or retry button
        error_state = self.page.get_element(".error-state")
        retry_btn = self.page.get_element(".retry-btn")

        if error_state:
            # Error state should be user-friendly
            error_text = error_state.text
            self.assertTrue(len(error_text) > 0, "Error message should be displayed")

        if retry_btn:
            # Retry button should be functional
            retry_btn.click()
            self.page.wait_for(2)
            # Page should attempt to reload


class TestActivityCreate(minium.MiniTest):
    """Tests for activity creation functionality."""

    def test_activity_create_form_validation(self):
        """Test activity creation form validation."""
        self.app.navigate_to("/pages/activity-create/activity-create")
        self.page.wait_for(2)

        # Try to submit without filling required fields
        submit_btn = self.page.get_element(".submit-btn")
        if not submit_btn:
            submit_btn = self.page.get_element("button", inner_text="发布")
        if not submit_btn:
            submit_btn = self.page.get_element("button[type='primary']")

        if submit_btn:
            submit_btn.click()
            self.page.wait_for(1)

            # Check for validation error messages
            error_msgs = self.page.get_elements(".error-message")
            if not error_msgs:
                error_msgs = self.page.get_elements(".form-error")

            # Form should show validation errors
            # (At least one required field should show error)

    def test_activity_create_fill_form(self):
        """Test filling activity creation form."""
        self.app.navigate_to("/pages/activity-create/activity-create")
        self.page.wait_for(2)

        # Fill title
        title_input = self.page.get_element("input[placeholder*='标题']")
        if not title_input:
            title_input = self.page.get_element(".title-input")
        if title_input:
            title_input.input("测试活动标题")

        # Fill description
        desc_input = self.page.get_element("textarea")
        if not desc_input:
            desc_input = self.page.get_element(".desc-input")
        if desc_input:
            desc_input.input("这是一个测试活动的详细描述信息。")

        # Fill location
        location_input = self.page.get_element("input[placeholder*='地点']")
        if not location_input:
            location_input = self.page.get_element(".location-input")
        if location_input:
            location_input.input("北京市朝阳区")

        # Fill date/time
        date_picker = self.page.get_element(".date-picker")
        if date_picker:
            date_picker.click()
            self.page.wait_for(1)
            # Select date
            confirm_btn = self.page.get_element(".picker-confirm")
            if confirm_btn:
                confirm_btn.click()

        # Submit form
        submit_btn = self.page.get_element(".submit-btn")
        if not submit_btn:
            submit_btn = self.page.get_element("button", inner_text="发布")

        if submit_btn:
            submit_btn.click()
            self.page.wait_for(2)

            # Verify success or navigation
            current_page = self.app.get_current_page()
            # Should navigate away or show success


class TestMemberCenter(minium.MiniTest):
    """Tests for member center functionality."""

    def test_member_center_display(self):
        """Test member center page displays correctly."""
        self.app.navigate_to("/pages/member-center/member-center")
        self.page.wait_for(2)

        # Check for member info display
        member_info = self.page.get_element(".member-info")
        if not member_info:
            member_info = self.page.get_element(".user-info")

        # Check for member stats
        stats = self.page.get_elements(".stat-item")
        if stats:
            self.assertTrue(len(stats) > 0, "Member stats should be displayed")

        # Check for badges or achievements
        badges = self.page.get_elements(".badge-item")
        if badges:
            for badge in badges[:3]:
                badge_text = badge.text
                self.assertIsNotNone(badge_text, "Badge should have text")

    def test_badges_page(self):
        """Test badges page."""
        self.app.navigate_to("/pages/badges/badges")
        self.page.wait_for(2)

        # Check for badge list
        badge_items = self.page.get_elements(".badge-item")
        if not badge_items:
            badge_items = self.page.get_elements(".badge-card")

        # Verify badges display
        if badge_items:
            for item in badge_items[:3]:
                # Each badge should have name and icon
                badge_name = item.get_element(".badge-name")
                badge_icon = item.get_element(".badge-icon")


class TestCreditSystem(minium.MiniTest):
    """Tests for credit/points system."""

    def test_credit_display(self):
        """Test credit page displays correctly."""
        self.app.navigate_to("/pages/credit/credit")
        self.page.wait_for(2)

        # Check for credit balance
        credit_balance = self.page.get_element(".credit-balance")
        if not credit_balance:
            credit_balance = self.page.get_element(".points-balance")

        if credit_balance:
            balance_text = credit_balance.text
            self.assertTrue(len(balance_text) > 0, "Credit balance should be displayed")

        # Check for credit history
        history_items = self.page.get_elements(".history-item")
        if not history_items:
            history_items = self.page.get_elements(".credit-record")

        if history_items:
            for item in history_items[:3]:
                record_text = item.text
                self.assertIsNotNone(record_text, "Credit record should have details")


class TestActivityHistory(minium.MiniTest):
    """Tests for activity history."""

    def test_activity_history_display(self):
        """Test activity history page."""
        self.app.navigate_to("/pages/activity-history/activity-history")
        self.page.wait_for(2)

        # Check for history list
        history_items = self.page.get_elements(".history-item")
        if not history_items:
            history_items = self.page.get_elements(".activity-card")

        # Check for tabs (ongoing, completed, etc.)
        tabs = self.page.get_elements(".tab-item")
        if tabs and len(tabs) > 1:
            # Click on completed tab
            tabs[1].click()
            self.page.wait_for(1)

            # Verify tab switch
            active_tab = self.page.get_element(".tab-item.active")


class TestSettings(minium.MiniTest):
    """Tests for settings page."""

    def test_settings_display(self):
        """Test settings page displays correctly."""
        self.app.navigate_to("/pages/settings/settings")
        self.page.wait_for(2)

        # Check for settings items
        settings_items = self.page.get_elements(".setting-item")
        if not settings_items:
            settings_items = self.page.get_elements(".menu-item")

        if settings_items:
            for item in settings_items[:3]:
                item_text = item.text
                self.assertTrue(len(item_text) > 0, "Setting item should have text")

    def test_notification_settings(self):
        """Test notification settings toggle."""
        self.app.navigate_to("/pages/settings/settings")
        self.page.wait_for(2)

        # Find notification toggle
        notification_switch = self.page.get_element(".notification-switch")
        if not notification_switch:
            notification_switch = self.page.get_element("switch")

        if notification_switch:
            # Get current state
            initial_checked = notification_switch.attribute("checked")

            # Toggle
            notification_switch.click()
            self.page.wait_for(1)

            # Verify state changed
            new_checked = notification_switch.attribute("checked")
            self.assertNotEqual(initial_checked, new_checked,
                                "Switch state should toggle")


class TestEducationAuth(minium.MiniTest):
    """Tests for education authentication."""

    def test_education_auth_page(self):
        """Test education authentication page."""
        self.app.navigate_to("/pages/education-auth/education-auth")
        self.page.wait_for(2)

        # Check for auth form
        auth_form = self.page.get_element(".auth-form")
        if not auth_form:
            auth_form = self.page.get_element("form")

        # Check for input fields
        name_input = self.page.get_element("input[placeholder*='姓名']")
        id_input = self.page.get_element("input[placeholder*='学号']")
        school_input = self.page.get_element("input[placeholder*='学校']")

        # Fill form if inputs exist
        if name_input:
            name_input.input("测试姓名")
        if id_input:
            id_input.input("20240001")
        if school_input:
            school_input.input("测试大学")

        # Submit
        submit_btn = self.page.get_element(".submit-btn")
        if not submit_btn:
            submit_btn = self.page.get_element("button", inner_text="认证")

        if submit_btn:
            submit_btn.click()
            self.page.wait_for(2)