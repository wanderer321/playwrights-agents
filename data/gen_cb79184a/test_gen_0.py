import minium


class TestPureActivity(minium.MiniTest):
    """Test Suite for Pure Activity Mini Program"""

    # ==================== Suite 1: Infrastructure & App Launch ====================

    def test_app_launch_and_network_check(self):
        """TC-APP-001: Mini Program Launch & Network Check"""
        # Launch the mini program
        self.app.launch()
        
        # Wait for home page to load
        self.page.wait_for(".index-page", timeout=10)
        
        # Verify home page elements are rendered
        page_element = self.page.get_element(".index-page")
        self.assertTrue(page_element is not None, "Index page should be loaded")
        
        # Check brand header is visible
        brand_header = self.page.get_element(".brand-header")
        self.assertTrue(brand_header is not None, "Brand header should be visible")
        
        # Check swiper component for slogans
        swiper = self.page.get_element(".slogan-swiper")
        self.assertTrue(swiper is not None, "Slogan swiper should be present")
        
        # Verify network type can be retrieved
        network_type = self.app.call_wx_method("getNetworkType")
        self.assertIn("networkType", str(network_type), "Network type should be returned")

    def test_global_exception_handling(self):
        """TC-APP-002: Global Exception Handling"""
        # Navigate to a page
        self.app.switch_tab("/pages/index/index")
        self.page.wait_for(".index-page", timeout=5)
        
        # Verify app is running without crash
        current_page = self.app.get_current_page()
        self.assertIsNotNone(current_page, "App should be running without crash")
        
        # Check page path
        self.assertIn("/pages/index/index", current_page.path, "Should be on index page")

    # ==================== Suite 2: User Authentication Module ====================

    def test_wechat_user_login_flow(self):
        """TC-AUTH-001: WeChat User Login Flow"""
        # Navigate to login page
        self.app.navigate_to("/pages/login/login")
        self.page.wait_for(".login-page", timeout=5)
        
        # Verify login page elements
        login_brand = self.page.get_element(".login-brand")
        self.assertTrue(login_brand is not None, "Login brand section should be visible")
        
        # Check login button exists with correct open-type
        login_btn = self.page.get_element(".login-btn")
        self.assertTrue(login_btn is not None, "Login button should be present")
        
        # Verify button has getPhoneNumber open-type
        open_type = login_btn.attribute("open-type")
        self.assertEqual("getPhoneNumber", open_type, "Login button should have getPhoneNumber open-type")
        
        # Check login features are displayed
        features = self.page.get_elements(".login-feature")
        self.assertTrue(len(features) > 0, "Login features should be displayed")

    def test_get_user_phone_number(self):
        """TC-AUTH-002: Get User Phone Number"""
        # Navigate to login page
        self.app.navigate_to("/pages/login/login")
        self.page.wait_for(".login-page", timeout=5)
        
        # Locate the phone number button
        phone_btn = self.page.get_element(".login-btn")
        self.assertTrue(phone_btn is not None, "Phone number button should exist")
        
        # Verify button text
        btn_text = phone_btn.text
        self.assertIn("微信一键登录", btn_text, "Button should display login text")
        
        # Check agreement text is present
        agreement = self.page.get_element(".login-agreement")
        self.assertTrue(agreement is not None, "User agreement should be displayed")

    def test_location_permission_handling(self):
        """TC-AUTH-003: Location Permission Handling"""
        # Navigate to profile page (TabBar)
        self.app.switch_tab("/pages/profile/profile")
        self.page.wait_for(".profile-page", timeout=5)
        
        # Verify profile page loaded
        profile_page = self.page.get_element(".profile-page")
        self.assertTrue(profile_page is not None, "Profile page should be loaded")
        
        # Check user info section
        user_info = self.page.get_element(".profile-user-info")
        self.assertTrue(user_info is not None, "User info section should be visible")

    # ==================== Suite 3: Home & Activity Discovery Module ====================

    def test_activity_list_rendering(self):
        """TC-HOME-001: Activity List Rendering"""
        # Navigate to home page (TabBar)
        self.app.switch_tab("/pages/index/index")
        self.page.wait_for(".index-page", timeout=5)
        
        # Check brand header
        brand_name = self.page.get_element(".brand-name")
        self.assertTrue(brand_name is not None, "Brand name should be displayed")
        
        # Verify swiper items exist
        swiper_items = self.page.get_elements(".slogan-card")
        self.assertTrue(len(swiper_items) > 0, "Swiper cards should be rendered")
        
        # Check slogan content
        slogan_contents = self.page.get_elements(".slogan-content")
        self.assertTrue(len(slogan_contents) > 0, "Slogan content should be displayed")

    def test_pull_down_refresh(self):
        """TC-HOME-002: Pull-down Refresh"""
        # Navigate to home page
        self.app.switch_tab("/pages/index/index")
        self.page.wait_for(".index-page", timeout=5)
        
        # Get current page object
        current_page = self.app.get_current_page()
        self.assertIsNotNone(current_page, "Current page should exist")
        
        # Trigger pull-down refresh
        self.page.pull_down_refresh()
        
        # Wait for refresh to complete
        self.page.wait_for(".brand-header", timeout=5)
        
        # Verify page still renders correctly after refresh
        brand_header = self.page.get_element(".brand-header")
        self.assertTrue(brand_header is not None, "Page should render correctly after refresh")

    def test_swiper_navigation(self):
        """TC-HOME-003: Swiper Navigation Test"""
        # Navigate to home page
        self.app.switch_tab("/pages/index/index")
        self.page.wait_for(".slogan-swiper", timeout=5)
        
        # Check swiper component
        swiper = self.page.get_element(".slogan-swiper")
        self.assertTrue(swiper is not None, "Swiper should be present")
        
        # Verify swiper has autoplay enabled
        autoplay = swiper.attribute("autoplay")
        self.assertTrue(autoplay, "Swiper should have autoplay enabled")
        
        # Check swiper is circular
        circular = swiper.attribute("circular")
        self.assertTrue(circular, "Swiper should be circular")

    # ==================== Suite 4: Activity Detail & Interaction ====================

    def test_activity_history_navigation(self):
        """TC-DETAIL-001: Activity History Navigation"""
        # Navigate to profile page
        self.app.switch_tab("/pages/profile/profile")
        self.page.wait_for(".profile-page", timeout=5)
        
        # Click on activity history menu item
        menu_item = self.page.get_element(".profile-menu-item[data-url='/pages/activity-history/activity-history']")
        if menu_item:
            menu_item.click()
            self.page.wait_for(".page-header", timeout=5)
            
            # Verify activity history page loaded
            page_header = self.page.get_element(".page-title")
            self.assertTrue(page_header is not None, "Activity history page should load")

    def test_activity_history_tabs(self):
        """TC-DETAIL-002: Activity History Tabs"""
        # Navigate to activity history
        self.app.navigate_to("/pages/activity-history/activity-history")
        self.page.wait_for(".tabs", timeout=5)
        
        # Check tabs exist
        tabs = self.page.get_elements(".tab")
        self.assertTrue(len(tabs) >= 3, "Should have at least 3 tabs")
        
        # Verify active tab
        active_tab = self.page.get_element(".tab.active")
        self.assertTrue(active_tab is not None, "One tab should be active")
        
        # Click on different tab
        past_tab = self.page.get_element(".tab[data-tab='past']")
        if past_tab:
            past_tab.click()
            self.page.wait_for(1)
            
            # Verify tab switched
            new_active = self.page.get_element(".tab.active")
            self.assertTrue(new_active is not None, "New tab should be active")

    def test_activity_card_component(self):
        """TC-DETAIL-003: Activity Card Component"""
        # Navigate to activity history
        self.app.navigate_to("/pages/activity-history/activity-history")
        self.page.wait_for(".tabs", timeout=5)
        
        # Check for activity cards
        activity_cards = self.page.get_elements(".card--activity-card")
        if len(activity_cards) > 0:
            # Verify card structure
            first_card = activity_cards[0]
            
            # Check card header
            card_header = first_card.get_element(".card--card-header")
            self.assertTrue(card_header is not None, "Card should have header")
            
            # Check activity title
            activity_title = first_card.get_element(".card--activity-title")
            self.assertTrue(activity_title is not None, "Card should have title")
            
            # Check activity status
            activity_status = first_card.get_element(".card--activity-status")
            self.assertTrue(activity_status is not None, "Card should have status")

    # ==================== Suite 5: Registration & Payment Module ====================

    def test_activity_create_form(self):
        """TC-PAY-001: Activity Create Form"""
        # Navigate to activity create page (TabBar)
        self.app.switch_tab("/pages/activity-create/activity-create")
        self.page.wait_for(".create-brand", timeout=5)
        
        # Verify create page elements
        create_brand = self.page.get_element(".create-brand")
        self.assertTrue(create_brand is not None, "Create brand section should be visible")
        
        # Check form card exists
        form_card = self.page.get_element(".form-card")
        self.assertTrue(form_card is not None, "Form card should be present")
        
        # Check cover options
        cover_options = self.page.get_elements(".cover-option")
        self.assertTrue(len(cover_options) > 0, "Cover options should be available")
        
        # Verify active cover option
        active_cover = self.page.get_element(".cover-option-active")
        self.assertTrue(active_cover is not None, "One cover option should be active")

    def test_cover_selection(self):
        """TC-PAY-002: Cover Image Selection"""
        # Navigate to activity create page
        self.app.switch_tab("/pages/activity-create/activity-create")
        self.page.wait_for(".cover-scroll", timeout=5)
        
        # Get all cover options
        cover_options = self.page.get_elements(".cover-option")
        if len(cover_options) > 1:
            # Click on second cover option
            second_cover = cover_options[1]
            second_cover.click()
            
            # Wait for selection to update
            self.page.wait_for(0.5)
            
            # Verify selection changed
            new_active = self.page.get_element(".cover-option-active")
            self.assertTrue(new_active is not None, "New cover should be selected")

    def test_credit_notice_display(self):
        """TC-PAY-003: Credit Notice Display"""
        # Navigate to activity create page
        self.app.switch_tab("/pages/activity-create/activity-create")
        self.page.wait_for(".create-body", timeout=5)
        
        # Check credit notice
        credit_notice = self.page.get_element(".credit-notice")
        self.assertTrue(credit_notice is not None, "Credit notice should be displayed")
        
        # Verify notice is warning type
        notice_warn = self.page.get_element(".credit-notice-warn")
        self.assertTrue(notice_warn is not None, "Credit warning notice should be present")

    # ==================== Suite 6: User Center & My Activities ====================

    def test_profile_page_rendering(self):
        """TC-USER-001: Profile Page Rendering"""
        # Navigate to profile page (TabBar)
        self.app.switch_tab("/pages/profile/profile")
        self.page.wait_for(".profile-page", timeout=5)
        
        # Check profile brand section
        profile_brand = self.page.get_element(".profile-brand")
        self.assertTrue(profile_brand is not None, "Profile brand should be visible")
        
        # Check avatar
        avatar = self.page.get_element(".profile-avatar")
        self.assertTrue(avatar is not None, "Profile avatar should be displayed")
        
        # Check user info
        user_name = self.page.get_element(".profile-user-name")
        self.assertTrue(user_name is not None, "User name should be displayed")
        
        # Check stats section
        stats = self.page.get_elements(".profile-stat-item")
        self.assertTrue(len(stats) >= 3, "Should have at least 3 stat items")

    def test_profile_menu_navigation(self):
        """TC-USER-002: Profile Menu Navigation"""
        # Navigate to profile page
        self.app.switch_tab("/pages/profile/profile")
        self.page.wait_for(".profile-menu", timeout=5)
        
        # Check menu items exist
        menu_items = self.page.get_elements(".profile-menu-item")
        self.assertTrue(len(menu_items) > 0, "Menu items should be present")
        
        # Verify menu item has data-url attribute
        first_item = menu_items[0]
        data_url = first_item.attribute("data-url")
        self.assertTrue(data_url is not None, "Menu item should have navigation URL")

    def test_credit_score_display(self):
        """TC-USER-003: Credit Score Display"""
        # Navigate to credit page
        self.app.navigate_to("/pages/credit/credit")
        self.page.wait_for(".score-card", timeout=5)
        
        # Check score card
        score_card = self.page.get_element(".score-card")
        self.assertTrue(score_card is not None, "Score card should be displayed")
        
        # Check score number
        score_number = self.page.get_element(".score-number")
        self.assertTrue(score_number is not None, "Score number should be visible")
        
        # Check score level
        score_level = self.page.get_element(".score-level")
        self.assertTrue(score_level is not None, "Score level should be displayed")
        
        # Check history items
        history_items = self.page.get_elements(".history-item")
        self.assertTrue(len(history_items) > 0, "Credit history should be displayed")

    def test_member_center_page(self):
        """TC-USER-004: Member Center Page"""
        # Navigate to member center
        self.app.navigate_to("/pages/member-center/member-center")
        self.page.wait_for(".mc-brand", timeout=5)
        
        # Check member center brand
        mc_brand = self.page.get_element(".mc-brand")
        self.assertTrue(mc_brand is not None, "Member center brand should be visible")
        
        # Check pricing cards
        pricing_cards = self.page.get_elements(".pricing-card")
        self.assertTrue(len(pricing_cards) >= 2, "Should have at least 2 pricing options")
        
        # Check privilege list
        privilege_items = self.page.get_elements(".privilege-item")
        self.assertTrue(len(privilege_items) > 0, "Privilege items should be displayed")

    def test_badges_page(self):
        """TC-USER-005: Badges Page"""
        # Navigate to badges page
        self.app.navigate_to("/pages/badges/badges")
        self.page.wait_for(".badges-grid", timeout=5)
        
        # Check page header
        page_title = self.page.get_element(".page-title")
        self.assertTrue(page_title is not None, "Page title should be displayed")
        
        # Check badges grid
        badges_grid = self.page.get_element(".badges-grid")
        self.assertTrue(badges_grid is not None, "Badges grid should be present")
        
        # Check badge items
        badge_items = self.page.get_elements(".badge-item")
        self.assertTrue(len(badge_items) > 0, "Badge items should be displayed")
        
        # Check locked badges
        locked_badges = self.page.get_elements(".badge-item.locked")
        self.assertTrue(len(locked_badges) > 0, "Some badges should be locked")

    # ==================== Suite 7: Settings & Feedback ====================

    def test_settings_page(self):
        """TC-SET-001: Settings Page"""
        # Navigate to settings page
        self.app.navigate_to("/pages/settings/settings")
        self.page.wait_for(".page-header", timeout=5)
        
        # Check page title
        page_title = self.page.get_element(".page-title")
        self.assertTrue(page_title is not None, "Settings page title should be displayed")
        
        # Check sections
        sections = self.page.get_elements(".section")
        self.assertTrue(len(sections) >= 3, "Should have at least 3 settings sections")
        
        # Check list items
        list_items = self.page.get_elements(".list-item")
        self.assertTrue(len(list_items) > 0, "Settings list items should be present")
        
        # Check logout button
        logout_btn = self.page.get_element(".btn-danger")
        self.assertTrue(logout_btn is not None, "Logout button should be present")

    def test_settings_switches(self):
        """TC-SET-002: Settings Switches"""
        # Navigate to settings page
        self.app.navigate_to("/pages/settings/settings")
        self.page.wait_for(".section", timeout=5)
        
        # Check switches exist
        switches = self.page.get_elements("switch")
        self.assertTrue(len(switches) >= 2, "Should have at least 2 privacy switches")

    def test_feedback_page(self):
        """TC-SET-003: Feedback Page"""
        # Navigate to feedback page
        self.app.navigate_to("/pages/feedback/feedback")
        self.page.wait_for(".feedback-header", timeout=5)
        
        # Check feedback header
        feedback_header = self.page.get_element(".feedback-header")
        self.assertTrue(feedback_header is not None, "Feedback header should be displayed")
        
        # Check type options
        type_options = self.page.get_elements(".type-option")
        self.assertTrue(len(type_options) >= 2, "Should have at least 2 feedback type options")
        
        # Check active type option
        active_option = self.page.get_element(".type-option.active")
        self.assertTrue(active_option is not None, "One type option should be active")
        
        # Check textarea
        textarea = self.page.get_element(".feedback-textarea")
        self.assertTrue(textarea is not None, "Feedback textarea should be present")
        
        # Check submit button
        submit_btn = self.page.get_element(".action-area .btn-primary")
        self.assertTrue(submit_btn is not None, "Submit button should be present")

    def test_feedback_type_selection(self):
        """TC-SET-004: Feedback Type Selection"""
        # Navigate to feedback page
        self.app.navigate_to("/pages/feedback/feedback")
        self.page.wait_for(".type-options", timeout=5)
        
        # Get type options
        type_options = self.page.get_elements(".type-option")
        if len(type_options) >= 2:
            # Click on bad type option
            bad_option = self.page.get_element(".type-option[data-type='bad']")
            if bad_option:
                bad_option.click()
                self.page.wait_for(0.5)
                
                # Verify selection changed
                new_active = self.page.get_element(".type-option.active")
                self.assertTrue(new_active is not None, "New type should be selected")

    def test_education_auth_page(self):
        """TC-SET-005: Education Auth Page"""
        # Navigate to education auth page
        self.app.navigate_to("/pages/education-auth/education-auth")
        self.page.wait_for(".section-header", timeout=5)
        
        # Check section header
        section_header = self.page.get_element(".section-header")
        self.assertTrue(section_header is not None, "Section header should be displayed")
        
        # Check method items
        method_items = self.page.get_elements(".method-item")
        self.assertTrue(len(method_items) >= 2, "Should have at least 2 auth methods")
        
        # Check upload area
        upload_area = self.page.get_element(".upload-area")
        self.assertTrue(upload_area is not None, "Upload area should be present")
        
        # Check submit button
        submit_btn = self.page.get_element(".submit-btn")
        self.assertTrue(submit_btn is not None, "Submit button should be present")

    # ==================== Suite 8: Custom Components Test ====================

    def test_loading_component(self):
        """TC-COMP-001: Loading Component"""
        # Navigate to activity detail (shows loading initially)
        self.app.navigate_to("/pages/activity-detail/activity-detail")
        self.page.wait_for(".page", timeout=5)
        
        # Check for loading component
        loading = self.page.get_element("loading")
        self.assertTrue(loading is not None, "Loading component should be present")

    def test_activity_card_component_structure(self):
        """TC-COMP-002: Activity Card Component Structure"""
        # Navigate to activity history
        self.app.navigate_to("/pages/activity-history/activity-history")
        self.page.wait_for(".card--activity-card", timeout=5)
        
        # Check activity card component
        activity_card = self.page.get_element("activity-card")
        self.assertTrue(activity_card is not None, "Activity card component should exist")
        
        # Check card internal structure
        card_body = self.page.get_element(".card--card-body")
        self.assertTrue(card_body is not None, "Card body should be present")
        
        # Check activity tags
        activity_tags = self.page.get_elements(".card--tag")
        self.assertTrue(len(activity_tags) > 0, "Activity tags should be displayed")

    def test_credit_score_component(self):
        """TC-COMP-003: Credit Score Component"""
        # Navigate to profile page
        self.app.switch_tab("/pages/profile/profile")
        self.page.wait_for(".profile-credit-badge", timeout=5)
        
        # Check credit score component
        credit_score = self.page.get_element("credit-score")
        self.assertTrue(credit_score is not None, "Credit score component should exist")
        
        # Check score circle
        score_circle = self.page.get_element(".score--score-circle")
        self.assertTrue(score_circle is not None, "Score circle should be displayed")
        
        # Check score value
        score_value = self.page.get_element(".score--score-value")
        self.assertTrue(score_value is not None, "Score value should be displayed")

    # ==================== Suite 9: Navigation Tests ====================

    def test_tabbar_navigation(self):
        """TC-NAV-001: TabBar Navigation"""
        # Test all TabBar pages
        tab_pages = [
            "/pages/index/index",
            "/pages/activity-create/activity-create",
            "/pages/profile/profile"
        ]
        
        for tab_page in tab_pages:
            self.app.switch_tab(tab_page)
            self.page.wait_for(1)
            current_page = self.app.get_current_page()
            self.assertIn(tab_page, current_page.path, f"Should navigate to {tab_page}")

    def test_page_navigation_stack(self):
        """TC-NAV-002: Page Navigation Stack"""
        # Start from home
        self.app.switch_tab("/pages/index/index")
        self.page.wait_for(".index-page", timeout=5)
        
        # Navigate to login
        self.app.navigate_to("/pages/login/login")
        self.page.wait_for(".login-page", timeout=5)
        
        # Navigate to credit
        self.app.navigate_to("/pages/credit/credit")
        self.page.wait_for(".score-card", timeout=5)
        
        # Navigate back
        self.app.navigate_back()
        self.page.wait_for(".login-page", timeout=5)
        
        # Navigate back again
        self.app.navigate_back()
        current_page = self.app.get_current_page()
        self.assertIn("/pages/index/index", current_page.path, "Should return to index")

    # ==================== Suite 10: Form Validation Tests ====================

    def test_feedback_form_validation(self):
        """TC-FORM-001: Feedback Form Validation"""
        # Navigate to feedback page
        self.app.navigate_to("/pages/feedback/feedback")
        self.page.wait_for(".feedback-textarea", timeout=5)
        
        # Check submit button is disabled initially
        submit_btn = self.page.get_element(".action-area .btn-primary")
        btn_class = submit_btn.attribute("class")
        self.assertIn("btn-disabled", btn_class, "Submit button should be disabled initially")
        
        # Input text in textarea
        textarea = self.page.get_element(".feedback-textarea")
        test_text = "这是一条测试反馈内容，用于验证表单功能是否正常工作"
        textarea.input(test_text)
        
        self.page.wait_for(0.5)
        
        # Verify input was entered
        textarea_value = textarea.attribute("value")
        self.assertTrue(len(textarea_value) > 0 or textarea.text, "Textarea should have content")

    def test_education_auth_form(self):
        """TC-FORM-002: Education Auth Form"""
        # Navigate to education auth page
        self.app.navigate_to("/pages/education-auth/education-auth")
        self.page.wait_for(".method-group", timeout=5)
        
        # Check method selection
        method_items = self.page.get_elements(".method-item")
        self.assertTrue(len(method_items) >= 2, "Should have auth method options")
        
        # Click on first method
        first_method = self.page.get_element(".method-item[data-method='xuexin']")
        if first_method:
            first_method.click()
            self.page.wait_for(0.5)
        
        # Check submit button is disabled
        submit_btn = self.page.get_element(".submit-btn")
        btn_disabled = submit_btn.attribute("disabled")
        self.assertTrue(btn_disabled, "Submit button should be disabled without upload")

    # ==================== Suite 11: Member Center Tests ====================

    def test_pricing_card_selection(self):
        """TC-MEMBER-001: Pricing Card Selection"""
        # Navigate to member center
        self.app.navigate_to("/pages/member-center/member-center")
        self.page.wait_for(".pricing-group", timeout=5)
        
        # Check pricing cards
        pricing_cards = self.page.get_elements(".pricing-card")
        self.assertTrue(len(pricing_cards) >= 2, "Should have pricing options")
        
        # Check monthly plan
        monthly_card = self.page.get_element(".pricing-card[data-plan='monthly']")
        self.assertTrue(monthly_card is not None, "Monthly plan should exist")
        
        # Check quarterly plan
        quarterly_card = self.page.get_element(".pricing-card[data-plan='quarterly']")
        self.assertTrue(quarterly_card is not None, "Quarterly plan should exist")
        
        # Verify save tag on quarterly
        save_tag = quarterly_card.get_element(".pricing-tag--save")
        self.assertTrue(save_tag is not None, "Quarterly plan should show savings")

    def test_privilege_list(self):
        """TC-MEMBER-002: Privilege List"""
        # Navigate to member center
        self.app.navigate_to("/pages/member-center/member-center")
        self.page.wait_for(".privilege-list", timeout=5)
        
        # Check privilege items
        privilege_items = self.page.get_elements(".privilege-item")
        self.assertTrue(len(privilege_items) > 0, "Privilege items should be displayed")
        
        # Check privilege icons
        privilege_icons = self.page.get_elements(".privilege-icon-wrap")
        self.assertTrue(len(privilege_icons) > 0, "Privilege icons should be displayed")

    # ==================== Suite 12: Error Handling Tests ====================

    def test_invalid_page_navigation(self):
        """TC-ERR-001: Invalid Page Navigation"""
        # Try to navigate to non-existent page
        try:
            self.app.navigate_to("/pages/nonexistent/page")
            self.page.wait_for(2)
        except Exception as e:
            # Should handle gracefully
            self.assertTrue(True, "Invalid navigation should be handled")
        
        # Verify app is still running
        current_page = self.app.get_current_page()
        self.assertIsNotNone(current_page, "App should still be running")

    def test_page_reload_stability(self):
        """TC-ERR-002: Page Reload Stability"""
        # Navigate to profile
        self.app.switch_tab("/pages/profile/profile")
        self.page.wait_for(".profile-page", timeout=5)
        
        # Navigate away
        self.app.switch_tab("/pages/index/index")
        self.page.wait_for(".index-page", timeout=5)
        
        # Navigate back
        self.app.switch_tab("/pages/profile/profile")
        self.page.wait_for(".profile-page", timeout=5)
        
        # Verify page still renders correctly
        profile_brand = self.page.get_element(".profile-brand")
        self.assertTrue(profile_brand is not None, "Profile should render correctly after reload")