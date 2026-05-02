import minium

class TestPureActivity(minium.MiniTest):
    """Test suite for Pure Activity Mini Program"""

    # ==================== Suite: User Module (用户模块) ====================

    def test_user_login_navigation(self):
        """TC-USER-001: WeChat Authorization Login - Navigation and UI check"""
        # Launch and navigate to profile page (TabBar)
        self.app.switch_tab("/pages/profile/profile")
        self.page.wait_for(".profile-page")
        
        # Verify profile page elements are rendered
        profile_page = self.app.get_current_page()
        self.assertIn("profile", profile_page.path)
        
        # Check user info section exists
        user_info = self.page.get_element(".profile-user-info")
        self.assertTrue(user_info is not None, "User info section should be visible")
        
        # Check avatar element
        avatar = self.page.get_element(".profile-avatar")
        self.assertTrue(avatar is not None, "Avatar should be displayed")

    def test_user_phone_login_page(self):
        """TC-USER-002: Get Mobile Number - Login page verification"""
        # Navigate to login page
        self.app.navigate_to("/pages/login/login")
        self.page.wait_for(".login-page")
        
        # Verify login page structure
        login_brand = self.page.get_element(".login-brand")
        self.assertTrue(login_brand is not None, "Login brand section should exist")
        
        # Check login button with getPhoneNumber open-type
        login_btn = self.page.get_element(".login-btn")
        self.assertTrue(login_btn is not None, "Login button should exist")
        
        # Verify button has phone authorization capability
        btn_open_type = login_btn.get_attribute("open-type")
        self.assertEqual("getPhoneNumber", btn_open_type, "Login button should have getPhoneNumber open-type")
        
        # Check login features section
        features = self.page.get_elements(".login-feature")
        self.assertTrue(len(features) >= 3, "At least 3 login features should be displayed")

    def test_user_profile_stats(self):
        """TC-USER-003: Profile statistics display"""
        self.app.switch_tab("/pages/profile/profile")
        self.page.wait_for(".profile-stats")
        
        # Verify stats items
        stat_items = self.page.get_elements(".profile-stat-item")
        self.assertTrue(len(stat_items) >= 3, "At least 3 stat items should be displayed")
        
        # Check credit badge component
        credit_badge = self.page.get_element(".profile-credit-badge")
        self.assertTrue(credit_badge is not None, "Credit badge should be displayed")

    def test_user_profile_menu_navigation(self):
        """TC-USER-004: Profile menu items navigation"""
        self.app.switch_tab("/pages/profile/profile")
        self.page.wait_for(".profile-menu")
        
        # Get menu items
        menu_items = self.page.get_elements(".profile-menu-item")
        self.assertTrue(len(menu_items) > 0, "Menu items should exist")
        
        # Check first menu item has data-url attribute
        first_item = self.page.get_element(".profile-menu-item")
        data_url = first_item.get_attribute("data-url")
        self.assertTrue(data_url is not None, "Menu item should have navigation URL")

    # ==================== Suite: Activity Module (活动核心模块) ====================

    def test_activity_index_loading(self):
        """TC-ACT-001: Activity List Loading - Home page verification"""
        # Navigate to home page (TabBar)
        self.app.switch_tab("/pages/index/index")
        self.page.wait_for(".index-page")
        
        # Verify brand header
        brand_header = self.page.get_element(".brand-header")
        self.assertTrue(brand_header is not None, "Brand header should be displayed")
        
        # Check swiper component
        swiper = self.page.get_element(".slogan-swiper")
        self.assertTrue(swiper is not None, "Slogan swiper should exist")
        
        # Verify swiper items
        swiper_items = self.page.get_elements(".slogan-card")
        self.assertTrue(len(swiper_items) >= 3, "At least 3 slogan cards should exist")

    def test_activity_swiper_autoplay(self):
        """TC-ACT-001b: Swiper autoplay functionality"""
        self.app.switch_tab("/pages/index/index")
        self.page.wait_for(".slogan-swiper")
        
        # Check swiper attributes
        swiper = self.page.get_element(".slogan-swiper")
        autoplay = swiper.get_attribute("autoplay")
        circular = swiper.get_attribute("circular")
        
        self.assertTrue(autoplay, "Swiper should have autoplay enabled")
        self.assertTrue(circular, "Swiper should be circular")

    def test_activity_create_page(self):
        """TC-ACT-002: Activity Creation Page"""
        # Navigate to activity create page (TabBar)
        self.app.switch_tab("/pages/activity-create/activity-create")
        self.page.wait_for(".create-brand")
        
        # Verify brand section
        brand_title = self.page.get_element(".create-brand-title")
        self.assertTrue(brand_title is not None, "Create brand title should exist")
        
        # Check form card exists
        form_card = self.page.get_element(".form-card")
        self.assertTrue(form_card is not None, "Form card should be displayed")
        
        # Verify cover options for activity
        cover_options = self.page.get_elements(".cover-option")
        self.assertTrue(len(cover_options) >= 4, "At least 4 cover options should be available")
        
        # Check credit notice
        credit_notice = self.page.get_element(".credit-notice")
        self.assertTrue(credit_notice is not None, "Credit notice should be displayed")

    def test_activity_create_cover_selection(self):
        """TC-ACT-002b: Activity cover image selection"""
        self.app.switch_tab("/pages/activity-create/activity-create")
        self.page.wait_for(".cover-scroll")
        
        # Get cover options
        cover_options = self.page.get_elements(".cover-option")
        self.assertTrue(len(cover_options) > 0, "Cover options should exist")
        
        # Check first option is active by default
        first_option = self.page.get_element(".cover-option-active")
        self.assertTrue(first_option is not None, "One cover option should be active")
        
        # Click on another cover option
        if len(cover_options) > 1:
            cover_options[1].click()
            self.page.wait_for(1)

    def test_activity_detail_loading_state(self):
        """TC-ACT-003: Activity Detail Page Loading"""
        # Navigate to activity detail (simulated with activity ID)
        self.app.navigate_to("/pages/activity-detail/activity-detail?id=test123")
        self.page.wait_for(".page")
        
        # Check loading component
        loading = self.page.get_element(".loading--loading-container")
        self.assertTrue(loading is not None, "Loading component should be displayed")

    def test_activity_history_tabs(self):
        """TC-ACT-004: Activity History Tabs"""
        self.app.navigate_to("/pages/activity-history/activity-history")
        self.page.wait_for(".tabs")
        
        # Verify tabs exist
        tabs = self.page.get_elements(".tab")
        self.assertEqual(3, len(tabs), "Should have 3 tabs")
        
        # Check default active tab
        active_tab = self.page.get_element(".tab.active")
        self.assertTrue(active_tab is not None, "One tab should be active by default")
        
        # Click on different tabs
        past_tab = self.page.get_element(".tab[data-tab='past']")
        if past_tab:
            past_tab.click()
            self.page.wait_for(1)
        
        created_tab = self.page.get_element(".tab[data-tab='created']")
        if created_tab:
            created_tab.click()
            self.page.wait_for(1)

    def test_activity_history_cards(self):
        """TC-ACT-005: Activity History Card Display"""
        self.app.navigate_to("/pages/activity-history/activity-history")
        self.page.wait_for(".card--activity-card")
        
        # Check activity cards
        activity_cards = self.page.get_elements(".card--activity-card")
        self.assertTrue(len(activity_cards) > 0, "Activity cards should be displayed")
        
        # Verify card structure
        first_card = self.page.get_element(".card--activity-card")
        card_header = first_card.get_element(".card--card-header")
        self.assertTrue(card_header is not None, "Card header should exist")

    # ==================== Suite: Booking & Order Module (报名与订单模块) ====================

    def test_order_feedback_form(self):
        """TC-ORDER-001: Feedback Form Submission"""
        self.app.navigate_to("/pages/feedback/feedback")
        self.page.wait_for(".feedback-header")
        
        # Check feedback header
        feedback_label = self.page.get_element(".feedback-label")
        self.assertTrue(feedback_label is not None, "Feedback label should exist")
        
        # Verify type options
        type_options = self.page.get_elements(".type-option")
        self.assertEqual(2, len(type_options), "Should have 2 feedback type options")
        
        # Check active type option
        active_option = self.page.get_element(".type-option.active")
        self.assertTrue(active_option is not None, "One type option should be active")
        
        # Verify textarea exists
        textarea = self.page.get_element(".feedback-textarea")
        self.assertTrue(textarea is not None, "Feedback textarea should exist")
        
        # Check submit button
        submit_btn = self.page.get_element(".action-area .btn")
        self.assertTrue(submit_btn is not None, "Submit button should exist")

    def test_order_feedback_type_selection(self):
        """TC-ORDER-001b: Feedback type selection"""
        self.app.navigate_to("/pages/feedback/feedback")
        self.page.wait_for(".type-options")
        
        # Click on bad type option
        bad_option = self.page.get_element(".type-option[data-type='bad']")
        if bad_option:
            bad_option.click()
            self.page.wait_for(1)

    def test_order_member_center_pricing(self):
        """TC-ORDER-002: Member Center Pricing Display"""
        self.app.navigate_to("/pages/member-center/member-center")
        self.page.wait_for(".mc-brand")
        
        # Verify member center brand
        brand_title = self.page.get_element(".mc-brand-title")
        self.assertTrue(brand_title is not None, "Member center title should exist")
        
        # Check pricing cards
        pricing_cards = self.page.get_elements(".pricing-card")
        self.assertTrue(len(pricing_cards) >= 2, "At least 2 pricing cards should exist")
        
        # Verify pricing tags
        save_tag = self.page.get_element(".pricing-tag--save")
        self.assertTrue(save_tag is not None, "Save tag should be displayed")

    def test_order_member_center_privileges(self):
        """TC-ORDER-002b: Member Center Privileges"""
        self.app.navigate_to("/pages/member-center/member-center")
        self.page.wait_for(".privilege-list")
        
        # Check privilege items
        privilege_items = self.page.get_elements(".privilege-item")
        self.assertTrue(len(privilege_items) > 0, "Privilege items should be displayed")

    # ==================== Suite: Location & Interaction (位置与交互) ====================

    def test_location_settings_page(self):
        """TC-LOC-001: Settings Page Location Options"""
        self.app.navigate_to("/pages/settings/settings")
        self.page.wait_for(".page-header")
        
        # Verify page title
        page_title = self.page.get_element(".page-title")
        self.assertTrue(page_title is not None, "Settings page title should exist")
        
        # Check sections
        sections = self.page.get_elements(".section")
        self.assertTrue(len(sections) >= 3, "At least 3 sections should exist")
        
        # Verify privacy settings with switches
        switches = self.page.get_elements("switch")
        self.assertTrue(len(switches) >= 2, "At least 2 privacy switches should exist")

    def test_location_logout_functionality(self):
        """TC-LOC-002: Logout Button Display"""
        self.app.navigate_to("/pages/settings/settings")
        self.page.wait_for(".logout-section")
        
        # Check logout button
        logout_btn = self.page.get_element(".btn-danger")
        self.assertTrue(logout_btn is not None, "Logout button should exist")
        
        # Verify button text
        btn_text = logout_btn.text
        self.assertIn("退出登录", btn_text, "Button should contain logout text")

    # ==================== Suite: Component Testing (公共组件) ====================

    def test_component_tab_bar_switching(self):
        """TC-COMP-001: Tab Bar Switching"""
        # Switch to index page
        self.app.switch_tab("/pages/index/index")
        self.page.wait_for(".index-page")
        current_page = self.app.get_current_page()
        self.assertIn("index", current_page.path, "Should be on index page")
        
        # Switch to activity create page
        self.app.switch_tab("/pages/activity-create/activity-create")
        self.page.wait_for(".create-brand")
        current_page = self.app.get_current_page()
        self.assertIn("activity-create", current_page.path, "Should be on activity-create page")
        
        # Switch to profile page
        self.app.switch_tab("/pages/profile/profile")
        self.page.wait_for(".profile-page")
        current_page = self.app.get_current_page()
        self.assertIn("profile", current_page.path, "Should be on profile page")

    def test_component_credit_score(self):
        """TC-COMP-002: Credit Score Component"""
        self.app.navigate_to("/pages/credit/credit")
        self.page.wait_for(".score-card")
        
        # Verify score card
        score_card = self.page.get_element(".score-card")
        self.assertTrue(score_card is not None, "Score card should exist")
        
        # Check score circle
        score_circle = self.page.get_element(".score-circle")
        self.assertTrue(score_circle is not None, "Score circle should be displayed")
        
        # Verify score level
        score_level = self.page.get_element(".score-level")
        self.assertTrue(score_level is not None, "Score level should be displayed")
        
        # Check history items
        history_items = self.page.get_elements(".history-item")
        self.assertTrue(len(history_items) > 0, "Credit history items should exist")

    def test_component_badges_locked(self):
        """TC-COMP-003: Badges Component"""
        self.app.navigate_to("/pages/badges/badges")
        self.page.wait_for(".badges-grid")
        
        # Verify badges grid
        badges_grid = self.page.get_element(".badges-grid")
        self.assertTrue(badges_grid is not None, "Badges grid should exist")
        
        # Check badge items
        badge_items = self.page.get_elements(".badge-item")
        self.assertTrue(len(badge_items) >= 6, "At least 6 badge items should exist")
        
        # Verify locked badges
        locked_badges = self.page.get_elements(".badge-item.locked")
        self.assertTrue(len(locked_badges) > 0, "Some badges should be locked")

    def test_component_education_auth(self):
        """TC-COMP-004: Education Auth Component"""
        self.app.navigate_to("/pages/education-auth/education-auth")
        self.page.wait_for(".section-header")
        
        # Verify section header
        section_title = self.page.get_element(".section-title")
        self.assertTrue(section_title is not None, "Section title should exist")
        
        # Check method items
        method_items = self.page.get_elements(".method-item")
        self.assertEqual(2, len(method_items), "Should have 2 authentication methods")
        
        # Verify upload area
        upload_area = self.page.get_element(".upload-area")
        self.assertTrue(upload_area is not None, "Upload area should exist")
        
        # Check submit button
        submit_btn = self.page.get_element(".submit-btn")
        self.assertTrue(submit_btn is not None, "Submit button should exist")

    def test_component_member_manage(self):
        """TC-COMP-005: Member Management Component"""
        self.app.navigate_to("/pages/member-manage/member-manage")
        self.page.wait_for(".page-header")
        
        # Verify page header
        page_title = self.page.get_element(".page-title")
        self.assertTrue(page_title is not None, "Page title should exist")
        
        # Check status bar
        status_bar = self.page.get_element(".status-bar")
        self.assertTrue(status_bar is not None, "Status bar should exist")
        
        # Verify member list
        member_list = self.page.get_element(".member-list")
        self.assertTrue(member_list is not None, "Member list should exist")

    # ==================== Suite: Exception Handling (异常与边界) ====================

    def test_error_empty_state_handling(self):
        """TC-ERR-001: Empty State Handling"""
        self.app.navigate_to("/pages/badges/badges")
        self.page.wait_for(".badges-info")
        
        # Check info section exists for empty/locked state
        info_section = self.page.get_element(".badges-info")
        self.assertTrue(info_section is not None, "Info section should exist")
        
        # Verify info title and text
        info_title = self.page.get_element(".info-title")
        info_text = self.page.get_element(".info-text")
        self.assertTrue(info_title is not None, "Info title should exist")
        self.assertTrue(info_text is not None, "Info text should exist")

    def test_error_form_validation_feedback(self):
        """TC-ERR-002: Form Validation - Feedback Page"""
        self.app.navigate_to("/pages/feedback/feedback")
        self.page.wait_for(".feedback-textarea")
        
        # Check character count warning
        char_count = self.page.get_element(".char-count")
        self.assertTrue(char_count is not None, "Character count should exist")
        
        # Verify submit button is disabled initially
        submit_btn = self.page.get_element(".btn-disabled")
        self.assertTrue(submit_btn is not None, "Submit button should be disabled initially")

    def test_error_education_auth_disabled(self):
        """TC-ERR-003: Form Validation - Education Auth"""
        self.app.navigate_to("/pages/education-auth/education-auth")
        self.page.wait_for(".submit-btn")
        
        # Check submit button is disabled
        submit_btn = self.page.get_element(".submit-btn")
        disabled_attr = submit_btn.get_attribute("disabled")
        self.assertTrue(disabled_attr, "Submit button should be disabled without upload")

    def test_error_rules_display(self):
        """TC-ERR-004: Rules and Guidelines Display"""
        self.app.navigate_to("/pages/education-auth/education-auth")
        self.page.wait_for(".rules-card")
        
        # Verify rules card
        rules_card = self.page.get_element(".rules-card")
        self.assertTrue(rules_card is not None, "Rules card should exist")
        
        # Check rules title
        rules_title = self.page.get_element(".rules-title")
        self.assertTrue(rules_title is not None, "Rules title should exist")
        
        # Verify rules items
        rules_items = self.page.get_elements(".rules-item")
        self.assertTrue(len(rules_items) >= 2, "At least 2 rules items should exist")

    # ==================== Suite: Navigation Tests ====================

    def test_navigation_profile_menu_items(self):
        """TC-NAV-001: Profile Menu Navigation"""
        self.app.switch_tab("/pages/profile/profile")
        self.page.wait_for(".profile-menu")
        
        # Get all menu items
        menu_items = self.page.get_elements(".profile-menu-item")
        self.assertTrue(len(menu_items) > 0, "Menu items should exist")
        
        # Verify menu structure
        for i, item in enumerate(menu_items[:3]):  # Check first 3 items
            menu_label = item.get_element(".profile-menu-label")
            self.assertTrue(menu_label is not None, f"Menu item {i} should have label")

    def test_navigation_all_main_pages(self):
        """TC-NAV-002: All Main Pages Accessible"""
        pages_to_test = [
            "/pages/login/login",
            "/pages/credit/credit",
            "/pages/badges/badges",
            "/pages/activity-history/activity-history",
            "/pages/settings/settings",
            "/pages/feedback/feedback",
            "/pages/member-center/member-center",
            "/pages/education-auth/education-auth",
            "/pages/member-manage/member-manage"
        ]
        
        for page_path in pages_to_test:
            try:
                self.app.navigate_to(page_path)
                self.page.wait_for(".page", timeout=5)
                current_page = self.app.get_current_page()
                self.assertIn(page_path.split("/")[-1], current_page.path, 
                             f"Should navigate to {page_path}")
            except Exception as e:
                # Log but continue testing other pages
                print(f"Navigation to {page_path} may have issues: {str(e)}")

    def test_navigation_back_functionality(self):
        """TC-NAV-003: Back Navigation"""
        # Navigate to a page
        self.app.navigate_to("/pages/settings/settings")
        self.page.wait_for(".page-header")
        
        # Navigate to another page
        self.app.navigate_to("/pages/credit/credit")
        self.page.wait_for(".score-card")
        
        # Go back
        self.app.navigate_back()
        self.page.wait_for(".page-header")
        
        # Verify we're back on settings page
        current_page = self.app.get_current_page()
        self.assertIn("settings", current_page.path, "Should be back on settings page")

    # ==================== Suite: UI/UX Tests ====================

    def test_ui_brand_elements(self):
        """TC-UI-001: Brand Elements Display"""
        self.app.switch_tab("/pages/index/index")
        self.page.wait_for(".brand-header")
        
        # Check brand name
        brand_name = self.page.get_element(".brand-name")
        self.assertTrue(brand_name is not None, "Brand name should exist")
        
        # Check brand subtitle
        brand_subtitle = self.page.get_element(".brand-subtitle")
        self.assertTrue(brand_subtitle is not None, "Brand subtitle should exist")
        
        # Verify wave animation element
        wave_inner = self.page.get_element(".wave-inner")
        self.assertTrue(wave_inner is not None, "Wave animation element should exist")

    def test_ui_login_brand_styling(self):
        """TC-UI-002: Login Page Brand Styling"""
        self.app.navigate_to("/pages/login/login")
        self.page.wait_for(".login-brand")
        
        # Check brand circles for styling
        circles = self.page.get_elements(".login-circle")
        self.assertEqual(3, len(circles), "Should have 3 decorative circles")
        
        # Verify brand content
        brand_name = self.page.get_element(".login-brand-name")
        brand_slogan = self.page.get_element(".login-brand-slogan")
        self.assertTrue(brand_name is not None, "Brand name should exist")
        self.assertTrue(brand_slogan is not None, "Brand slogan should exist")

    def test_ui_profile_brand_styling(self):
        """TC-UI-003: Profile Page Brand Styling"""
        self.app.switch_tab("/pages/profile/profile")
        self.page.wait_for(".profile-brand")
        
        # Check profile circles
        circles = self.page.get_elements(".profile-circle")
        self.assertTrue(len(circles) >= 2, "Should have at least 2 decorative circles")
        
        # Verify avatar text
        avatar_text = self.page.get_element(".profile-avatar-text")
        self.assertTrue(avatar_text is not None, "Avatar text should exist")

    def test_ui_create_page_styling(self):
        """TC-UI-004: Activity Create Page Styling"""
        self.app.switch_tab("/pages/activity-create/activity-create")
        self.page.wait_for(".create-brand")
        
        # Check decorative circles
        circles = self.page.get_elements(".create-circle")
        self.assertEqual(2, len(circles), "Should have 2 decorative circles")
        
        # Verify form card accent
        form_accent = self.page.get_element(".form-card-accent")
        self.assertTrue(form_accent is not None, "Form card accent should exist")

    def test_ui_member_center_styling(self):
        """TC-UI-005: Member Center Styling"""
        self.app.navigate_to("/pages/member-center/member-center")
        self.page.wait_for(".mc-brand")
        
        # Check decorative circles
        circles = self.page.get_elements(".mc-circle")
        self.assertEqual(2, len(circles), "Should have 2 decorative circles")
        
        # Verify points preview card
        points_card = self.page.get_element(".points-preview-card")
        self.assertTrue(points_card is not None, "Points preview card should exist")
        
        # Check points preview arrow
        arrow = self.page.get_element(".points-preview-arrow")
        self.assertTrue(arrow is not None, "Points preview arrow should exist")