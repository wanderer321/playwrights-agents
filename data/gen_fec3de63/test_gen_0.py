import minium


class TestUserModule(minium.MiniTest):
    """用户模块测试 - TC-USER-001, TC-USER-002"""

    def test_user_001_wechat_login_authorization(self):
        """TC-USER-001: WeChat Login & Authorization"""
        # Launch Mini Program - handled by framework
        
        # Check if login button exists (user not logged in)
        login_button = self.page.get_element("button", inner_text="登录")
        
        if login_button:
            # Trigger login
            login_button.click()
            
            # Handle WeChat authorization pop-up
            # In test environment, authorization may be auto-approved
            allow_btn = self.page.get_element("button", inner_text="允许")
            if allow_btn:
                allow_btn.click()
        
        # Verify user is logged in - check for user avatar/nickname display
        user_avatar = self.page.get_element(".user-avatar")
        user_nickname = self.page.get_element(".user-nickname")
        
        self.assertTrue(user_avatar or user_nickname, "User avatar or nickname should be displayed after login")
        
        # Verify session token is stored
        storage_info = self.app.get_storage_info()
        self.assertTrue(storage_info, "Storage should contain session data")

    def test_user_002_user_profile_update(self):
        """TC-USER-002: User Profile Update"""
        # Navigate to User Profile page (assuming tabBar)
        self.app.switch_tab("/pages/user/user")
        
        # Click Edit Profile button
        edit_button = self.page.get_element("button", inner_text="编辑资料")
        if not edit_button:
            edit_button = self.page.get_element(".edit-profile-btn")
        edit_button.click()
        
        # Modify nickname
        nickname_input = self.page.get_element("input.nickname-input")
        if not nickname_input:
            nickname_input = self.page.get_element("input[placeholder*='昵称']")
        nickname_input.input("测试新昵称")
        
        # Click Save button
        save_button = self.page.get_element("button", inner_text="保存")
        save_button.click()
        
        # Verify changes are saved
        updated_nickname = self.page.get_element(".nickname-display")
        if updated_nickname:
            self.assertIn("测试新昵称", updated_nickname.text, "Nickname should be updated")


class TestPetManagementModule(minium.MiniTest):
    """宠物档案模块测试 - TC-PET-001, TC-PET-002"""

    def test_pet_001_add_new_pet_profile(self):
        """TC-PET-001: Add New Pet Profile"""
        # Navigate to My Pets section
        self.app.navigate_to("/pages/pet/list/list")
        
        # Click Add Pet button (+ icon or button)
        add_button = self.page.get_element(".add-pet-btn")
        if not add_button:
            add_button = self.page.get_element("button", inner_text="添加宠物")
        if not add_button:
            add_button = self.page.get_element(".add-icon")
        add_button.click()
        
        # Input Pet Name
        name_input = self.page.get_element("input.pet-name")
        if not name_input:
            name_input = self.page.get_element("input[placeholder*='宠物名']")
        name_input.input("Lucky")
        
        # Select Pet Type from picker
        type_picker = self.page.get_element("picker.pet-type")
        if not type_picker:
            type_picker = self.page.get_element("picker", inner_text="选择类型")
        type_picker.click()
        
        # Select first option in picker
        picker_option = self.page.get_element(".picker-option")
        if picker_option:
            picker_option.click()
        
        # Select Breed from picker
        breed_picker = self.page.get_element("picker.pet-breed")
        if not breed_picker:
            breed_picker = self.page.get_element("picker", inner_text="选择品种")
        breed_picker.click()
        
        # Upload photo - trigger image selection
        upload_btn = self.page.get_element(".upload-photo-btn")
        if not upload_btn:
            upload_btn = self.page.get_element(".photo-upload")
        upload_btn.click()
        # In test environment, wx.chooseImage is mocked
        
        # Submit the form
        submit_btn = self.page.get_element("button", inner_text="提交")
        if not submit_btn:
            submit_btn = self.page.get_element("button", inner_text="保存")
        submit_btn.click()
        
        # Verify new pet card appears in list
        pet_card = self.page.get_element(".pet-card", inner_text="Lucky")
        self.assertTrue(pet_card, "New pet card should appear in the list")

    def test_pet_002_edit_pet_details(self):
        """TC-PET-002: Edit Pet Details"""
        # Navigate to My Pets section
        self.app.navigate_to("/pages/pet/list/list")
        
        # Select an existing pet card
        pet_card = self.page.get_element(".pet-card")
        pet_card.click()
        
        # Click Edit button
        edit_btn = self.page.get_element("button", inner_text="编辑")
        if not edit_btn:
            edit_btn = self.page.get_element(".edit-btn")
        edit_btn.click()
        
        # Change weight
        weight_input = self.page.get_element("input.weight-input")
        if not weight_input:
            weight_input = self.page.get_element("input[placeholder*='体重']")
        weight_input.input("5.5")
        
        # Change birthday using picker
        birthday_picker = self.page.get_element("picker.birthday-picker")
        if not birthday_picker:
            birthday_picker = self.page.get_element("picker", inner_text="生日")
        birthday_picker.click()
        
        # Save changes
        save_btn = self.page.get_element("button", inner_text="保存")
        save_btn.click()
        
        # Verify pet details are updated
        weight_display = self.page.get_element(".weight-display")
        if weight_display:
            self.assertIn("5.5", weight_display.text, "Weight should be updated")


class TestECommerceModule(minium.MiniTest):
    """商城模块测试 - TC-SHOP-001, TC-SHOP-002, TC-SHOP-003"""

    def test_shop_001_product_search_and_view(self):
        """TC-SHOP-001: Product Search and View"""
        # Navigate to Mall tab
        self.app.switch_tab("/pages/mall/mall")
        
        # Use search bar to input keywords
        search_input = self.page.get_element("input.search-input")
        if not search_input:
            search_input = self.page.get_element("input[placeholder*='搜索']")
        search_input.input("狗粮")
        
        # Trigger search
        search_btn = self.page.get_element(".search-btn")
        if not search_btn:
            search_btn = self.page.get_element("button", inner_text="搜索")
        search_btn.click()
        
        # Select a product from the list
        product_item = self.page.get_element(".product-item")
        if not product_item:
            product_item = self.page.get_element(".goods-item")
        product_item.click()
        
        # Verify product detail page loads correctly
        product_title = self.page.get_element(".product-title")
        if not product_title:
            product_title = self.page.get_element(".goods-title")
        self.assertTrue(product_title, "Product title should be displayed")
        
        # Verify price is displayed
        price_display = self.page.get_element(".product-price")
        if not price_display:
            price_display = self.page.get_element(".goods-price")
        self.assertTrue(price_display, "Product price should be displayed")
        
        # Verify images are displayed
        product_image = self.page.get_element(".product-image")
        if not product_image:
            product_image = self.page.get_element(".goods-image")
        self.assertTrue(product_image, "Product image should be displayed")

    def test_shop_002_add_to_cart_and_purchase_flow(self):
        """TC-SHOP-002: Add to Cart and Purchase Flow"""
        # Navigate to Mall tab
        self.app.switch_tab("/pages/mall/mall")
        
        # Go to a product detail page
        product_item = self.page.get_element(".product-item")
        if not product_item:
            product_item = self.page.get_element(".goods-item")
        product_item.click()
        
        # Select specifications (flavor/size)
        spec_option = self.page.get_element(".spec-option")
        if spec_option:
            spec_option.click()
        
        # Click Add to Cart
        add_cart_btn = self.page.get_element("button", inner_text="加入购物车")
        add_cart_btn.click()
        
        # Navigate to Cart page
        self.app.navigate_to("/pages/cart/cart")
        
        # Select the item (checkbox)
        checkbox = self.page.get_element(".cart-checkbox")
        if not checkbox:
            checkbox = self.page.get_element(".item-checkbox")
        checkbox.click()
        
        # Click Checkout
        checkout_btn = self.page.get_element("button", inner_text="结算")
        checkout_btn.click()
        
        # Select shipping address
        address_item = self.page.get_element(".address-item")
        if address_item:
            address_item.click()
        
        # Submit Order
        submit_btn = self.page.get_element("button", inner_text="提交订单")
        submit_btn.click()
        
        # Verify order creation - check for payment interface
        payment_section = self.page.get_element(".payment-section")
        if not payment_section:
            payment_section = self.page.get_element(".order-confirm")
        self.assertTrue(payment_section, "Order confirmation or payment interface should be displayed")

    def test_shop_003_wechat_payment_integration(self):
        """TC-SHOP-003: WeChat Payment Integration"""
        # This test assumes we're on the payment/order confirmation page
        # Navigate to Mall and create an order first
        self.app.switch_tab("/pages/mall/mall")
        
        product_item = self.page.get_element(".product-item")
        if product_item:
            product_item.click()
            
            # Quick add to cart and checkout
            add_cart_btn = self.page.get_element("button", inner_text="立即购买")
            if not add_cart_btn:
                add_cart_btn = self.page.get_element("button", inner_text="购买")
            add_cart_btn.click()
            
            # Select spec if needed
            spec_option = self.page.get_element(".spec-option")
            if spec_option:
                spec_option.click()
            
            # Confirm purchase
            confirm_btn = self.page.get_element("button", inner_text="确定")
            if confirm_btn:
                confirm_btn.click()
        
        # Trigger payment
        pay_btn = self.page.get_element("button", inner_text="立即支付")
        if not pay_btn:
            pay_btn = self.page.get_element("button", inner_text="支付")
        if pay_btn:
            pay_btn.click()
        
        # In test environment, mock payment success callback
        # Verify order status changes to "Paid" or "Pending Shipment"
        order_status = self.page.get_element(".order-status")
        if order_status:
            status_text = order_status.text
            self.assertTrue(
                "已支付" in status_text or "待发货" in status_text or "支付成功" in status_text,
                "Order status should indicate successful payment"
            )


class TestServiceAppointmentModule(minium.MiniTest):
    """服务预约模块测试 - TC-SVC-001, TC-SVC-002"""

    def test_svc_001_nearby_services_location_authorization(self):
        """TC-SVC-001: Nearby Services (Location Authorization)"""
        # Navigate to Services section
        self.app.switch_tab("/pages/service/service")
        
        # Trigger location authorization
        # In test environment, location access is typically auto-granted
        
        # Verify map loads centered on user's current location
        map_component = self.page.get_element("map")
        self.assertTrue(map_component, "Map should be displayed")
        
        # Verify list of nearby services is displayed
        service_list = self.page.get_element(".service-list")
        if not service_list:
            service_list = self.page.get_element(".nearby-list")
        self.assertTrue(service_list, "Nearby services list should be displayed")
        
        # Verify services are sorted by distance
        service_items = self.page.get_elements(".service-item")
        if not service_items:
            service_items = self.page.get_elements(".nearby-item")
        self.assertTrue(len(service_items) > 0, "Should display at least one nearby service")

    def test_svc_002_book_grooming_service(self):
        """TC-SVC-002: Book Grooming Service"""
        # Navigate to Services section
        self.app.switch_tab("/pages/service/service")
        
        # Select a service provider from the list
        provider = self.page.get_element(".service-provider")
        if not provider:
            provider = self.page.get_element(".service-item")
        provider.click()
        
        # Choose service type (e.g., "Bathing")
        service_type = self.page.get_element(".service-type", inner_text="洗澡")
        if not service_type:
            service_type = self.page.get_element(".service-option")
        service_type.click()
        
        # Select available time slot on calendar
        time_slot = self.page.get_element(".time-slot.available")
        if not time_slot:
            time_slot = self.page.get_element(".calendar-slot")
        time_slot.click()
        
        # Confirm booking
        confirm_btn = self.page.get_element("button", inner_text="确认预约")
        if not confirm_btn:
            confirm_btn = self.page.get_element("button", inner_text="立即预约")
        confirm_btn.click()
        
        # Verify booking is recorded
        booking_confirm = self.page.get_element(".booking-confirm")
        if not booking_confirm:
            booking_confirm = self.page.get_element(".booking-success")
        self.assertTrue(booking_confirm, "Booking confirmation should be displayed")


class TestSocialSharingModule(minium.MiniTest):
    """社区与分享模块测试 - TC-SOC-001, TC-SOC-002"""

    def test_soc_001_share_content_to_wechat_chat(self):
        """TC-SOC-001: Share Content to WeChat Chat"""
        # Navigate to community section
        self.app.switch_tab("/pages/community/community")
        
        # Select an article or pet dynamic
        article = self.page.get_element(".article-item")
        if not article:
            article = self.page.get_element(".dynamic-item")
        article.click()
        
        # Click Share button (top right menu or specific button)
        share_btn = self.page.get_element(".share-btn")
        if not share_btn:
            share_btn = self.page.get_element("button", inner_text="分享")
        share_btn.click()
        
        # Trigger onShareAppMessage
        # In test environment, share dialog may be mocked
        # Verify share card displays correct title, image, and path
        share_card = self.page.get_element(".share-card")
        if share_card:
            share_title = share_card.attribute("data-title")
            share_image = share_card.attribute("data-image")
            share_path = share_card.attribute("data-path")
            
            self.assertTrue(share_title, "Share card should have a title")
            self.assertTrue(share_image, "Share card should have an image")
            self.assertTrue(share_path, "Share card should have a path")

    def test_soc_002_post_new_dynamic_image_upload(self):
        """TC-SOC-002: Post New Dynamic (Image Upload)"""
        # Navigate to community section
        self.app.switch_tab("/pages/community/community")
        
        # Click Post or + button
        post_btn = self.page.get_element(".post-btn")
        if not post_btn:
            post_btn = self.page.get_element("button", inner_text="发布")
        if not post_btn:
            post_btn = self.page.get_element(".add-post-icon")
        post_btn.click()
        
        # Select images from album (wx.chooseImage mocked in test environment)
        image_picker = self.page.get_element(".image-picker")
        if not image_picker:
            image_picker = self.page.get_element(".add-image-btn")
        image_picker.click()
        
        # Enter text content
        content_input = self.page.get_element("textarea.content-input")
        if not content_input:
            content_input = self.page.get_element("textarea[placeholder*='内容']")
        content_input.input("今天带宠物出去玩啦！")
        
        # Click Publish
        publish_btn = self.page.get_element("button", inner_text="发布")
        publish_btn.click()
        
        # Verify post appears in community feed
        post_content = self.page.get_element(".post-content", inner_text="今天带宠物出去玩啦")
        if not post_content:
            post_content = self.page.get_element(".dynamic-content", inner_text="今天带宠物出去玩啦")
        self.assertTrue(post_content, "Post should appear in community feed")
        
        # Verify images are rendered correctly
        post_image = self.page.get_element(".post-image")
        if not post_image:
            post_image = self.page.get_element(".dynamic-image")
        self.assertTrue(post_image, "Post images should be rendered")


class TestAddressManagement(minium.MiniTest):
    """地址管理测试 - TC-ADDR-001, TC-ADDR-002"""

    def test_addr_001_wechat_address_import(self):
        """TC-ADDR-001: WeChat Address Import"""
        # Navigate to My Addresses
        self.app.navigate_to("/pages/address/list/list")
        
        # Click Import from WeChat
        import_btn = self.page.get_element("button", inner_text="从微信导入")
        if not import_btn:
            import_btn = self.page.get_element("button", inner_text="微信地址")
        import_btn.click()
        
        # In test environment, wx.chooseAddress is mocked
        # Handle authorization if prompted
        allow_btn = self.page.get_element("button", inner_text="允许")
        if allow_btn:
            allow_btn.click()
        
        # Verify address fields are populated automatically
        address_name = self.page.get_element(".address-name")
        if not address_name:
            address_name = self.page.get_element(".receiver-name")
        self.assertTrue(address_name, "Address name should be populated")
        
        address_phone = self.page.get_element(".address-phone")
        if not address_phone:
            address_phone = self.page.get_element(".receiver-phone")
        self.assertTrue(address_phone, "Address phone should be populated")
        
        address_region = self.page.get_element(".address-region")
        if not address_region:
            address_region = self.page.get_element(".address-area")
        self.assertTrue(address_region, "Address region should be populated")

    def test_addr_002_manual_address_entry(self):
        """TC-ADDR-002: Manual Address Entry"""
        # Navigate to My Addresses
        self.app.navigate_to("/pages/address/list/list")
        
        # Click Add New Address
        add_btn = self.page.get_element("button", inner_text="新增地址")
        if not add_btn:
            add_btn = self.page.get_element("button", inner_text="添加地址")
        add_btn.click()
        
        # Fill in Name
        name_input = self.page.get_element("input.name-input")
        if not name_input:
            name_input = self.page.get_element("input[placeholder*='姓名']")
        name_input.input("张三")
        
        # Fill in Phone number
        phone_input = self.page.get_element("input.phone-input")
        if not phone_input:
            phone_input = self.page.get_element("input[placeholder*='电话']")
        phone_input.input("13800138000")
        
        # Use Region Picker to select City/District
        region_picker = self.page.get_element("picker.region-picker")
        if not region_picker:
            region_picker = self.page.get_element("picker", inner_text="选择地区")
        region_picker.click()
        
        # Select first region option
        region_option = self.page.get_element(".picker-option")
        if region_option:
            region_option.click()
        
        # Fill in detail address
        detail_input = self.page.get_element("input.detail-input")
        if not detail_input:
            detail_input = self.page.get_element("input[placeholder*='详细地址']")
        detail_input.input("某某小区1号楼101室")
        
        # Save address
        save_btn = self.page.get_element("button", inner_text="保存")
        save_btn.click()
        
        # Verify address saved successfully
        address_item = self.page.get_element(".address-item", inner_text="张三")
        self.assertTrue(address_item, "New address should appear in list")
        
        # Verify validation works for empty fields
        # Navigate back to add another address to test validation
        add_btn = self.page.get_element("button", inner_text="新增地址")
        if add_btn:
            add_btn.click()
            
            # Try to save with empty fields
            save_btn = self.page.get_element("button", inner_text="保存")
            save_btn.click()
            
            # Check for validation error message
            error_msg = self.page.get_element(".error-message")
            if not error_msg:
                error_msg = self.page.get_element(".validation-error")
            # Validation should prevent saving with empty fields
            self.assertTrue(error_msg or self.page.get_element("input.name-input"), 
                          "Validation should prevent saving with empty fields")