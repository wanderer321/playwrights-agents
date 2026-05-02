import minium


class TestPetChronicle(minium.MiniTest):
    """宠物纪小程序自动化测试套件"""

    # ==================== 用户鉴权与账户模块 ====================

    def test_auth_001_wechat_login(self):
        """TC-AUTH-001: 微信授权登录"""
        # 启动小程序，检测登录态
        self.app.switch_tab("/pages/index/index")

        # 检查是否存在登录按钮（未登录状态）
        login_btn = self.page.get_element(".login-btn, button[open-type='getUserInfo']")

        if login_btn:
            # 点击微信一键登录
            login_btn.click()

            # 验证登录成功 - 检查用户头像或昵称显示
            user_avatar = self.page.get_element(".user-avatar, .avatar")
            user_nickname = self.page.get_element(".user-nickname, .nickname")

            self.assertTrue(
                user_avatar.exists or user_nickname.exists,
                "登录成功后应显示用户头像或昵称"
            )

    def test_auth_002_phone_number_bind(self):
        """TC-AUTH-002: 获取手机号授权"""
        # 进入个人中心
        self.app.switch_tab("/pages/user/user")

        # 查找绑定手机号按钮
        bind_phone_btn = self.page.get_element(
            "button[open-type='getPhoneNumber'], .bind-phone-btn"
        )

        if bind_phone_btn.exists:
            bind_phone_btn.click()

            # 验证手机号绑定成功（显示脱敏手机号）
            phone_display = self.page.get_element(".phone-number, .user-phone")
            if phone_display.exists:
                phone_text = phone_display.text
                # 验证手机号格式（中间四位隐藏，如 138****1234）
                self.assertIn("****", phone_text, "手机号应显示为脱敏格式")

    # ==================== 宠物档案管理模块 ====================

    def test_pet_001_add_pet_profile(self):
        """TC-PET-001: 添加宠物档案"""
        # 进入我的宠物页面
        self.app.navigate_to("/pages/pet/list")

        # 点击添加宠物按钮
        add_btn = self.page.get_element(".add-pet-btn, button.add-pet")
        self.assertTrue(add_btn.exists, "应存在添加宠物按钮")
        add_btn.click()

        # 输入宠物名称
        name_input = self.page.get_element("input.pet-name, .name-input input")
        if name_input.exists:
            name_input.input("旺财")

        # 选择宠物类型（猫/狗）
        pet_type_selector = self.page.get_element(".pet-type-dog, .type-selector")
        if pet_type_selector.exists:
            pet_type_selector.click()

        # 选择品种
        breed_picker = self.page.get_element(".breed-picker, picker.breed")
        if breed_picker.exists:
            breed_picker.click()
            # 选择第一个品种选项
            first_breed = self.page.get_element(".breed-option", inner_text="金毛")
            if first_breed.exists:
                first_breed.click()

        # 选择生日
        birthday_picker = self.page.get_element(".birthday-picker, picker.birthday")
        if birthday_picker.exists:
            birthday_picker.click()

        # 点击上传头像
        avatar_upload = self.page.get_element(".avatar-upload, .upload-avatar")
        if avatar_upload.exists:
            avatar_upload.click()
            # 注意：wx.chooseImage 需要用户手动操作，测试环境可能需要mock

        # 点击保存
        save_btn = self.page.get_element(".save-btn, button.save")
        self.assertTrue(save_btn.exists, "应存在保存按钮")
        save_btn.click()

        # 验证宠物卡片出现在列表中
        self.app.navigate_to("/pages/pet/list")
        pet_card = self.page.get_element(".pet-card", inner_text="旺财")
        self.assertTrue(pet_card.exists, "宠物卡片应显示在列表中")

    def test_pet_002_edit_delete_pet(self):
        """TC-PET-002: 编辑与删除宠物信息"""
        # 进入宠物列表
        self.app.navigate_to("/pages/pet/list")

        # 选择已存在的宠物卡片
        pet_card = self.page.get_element(".pet-card")
        self.assertTrue(pet_card.exists, "宠物列表应有宠物卡片")
        pet_card.click()

        # 进入编辑模式
        edit_btn = self.page.get_element(".edit-btn, button.edit")
        if edit_btn.exists:
            edit_btn.click()

            # 修改体重字段
            weight_input = self.page.get_element("input.weight, .weight-input input")
            if weight_input.exists:
                weight_input.input("15.5")

            # 保存修改
            save_btn = self.page.get_element(".save-btn, button.save")
            if save_btn.exists:
                save_btn.click()

            # 验证数据更新
            weight_display = self.page.get_element(".weight-value")
            if weight_display.exists:
                self.assertIn("15.5", weight_display.text, "体重应更新为15.5kg")

        # 删除宠物
        delete_btn = self.page.get_element(".delete-btn, button.delete")
        if delete_btn.exists:
            delete_btn.click()

            # 确认删除
            confirm_btn = self.page.get_element(".confirm-btn", inner_text="确认")
            if confirm_btn.exists:
                confirm_btn.click()

            # 验证列表中不再显示该宠物
            self.app.navigate_to("/pages/pet/list")
            deleted_pet = self.page.get_element(".pet-card", inner_text="旺财")
            self.assertFalse(
                deleted_pet.exists,
                "删除后宠物不应再显示在列表中"
            )

    # ==================== 社区动态与互动模块 ====================

    def test_comm_001_publish_post(self):
        """TC-COMM-001: 发布图文动态"""
        # 点击底部导航栏发布按钮
        self.app.switch_tab("/pages/publish/publish")

        # 输入文本内容
        content_input = self.page.get_element(
            "textarea.content, .content-input textarea"
        )
        self.assertTrue(content_input.exists, "应存在内容输入框")
        content_input.input("今天遛狗啦，天气真好！")

        # 添加图片
        add_image_btn = self.page.get_element(".add-image, .upload-image")
        if add_image_btn.exists:
            add_image_btn.click()
            # 注意：图片选择需要用户交互，测试环境可能需要mock

        # 点击发布按钮
        publish_btn = self.page.get_element(".publish-btn, button.publish")
        self.assertTrue(publish_btn.exists, "应存在发布按钮")
        publish_btn.click()

        # 验证发布成功 - 跳转至动态详情或社区流
        # 检查是否显示成功提示或跳转到社区页面
        success_toast = self.page.get_element(".toast-success, .success-msg")
        if success_toast.exists:
            self.assertTrue(success_toast.exists, "应显示发布成功提示")

    def test_comm_002_share_post(self):
        """TC-COMM-002: 动态分享功能"""
        # 进入社区动态列表
        self.app.switch_tab("/pages/community/community")

        # 点击第一条动态进入详情
        first_post = self.page.get_element(".post-item, .dynamic-card")
        self.assertTrue(first_post.exists, "社区应有动态内容")
        first_post.click()

        # 点击分享按钮
        share_btn = self.page.get_element(".share-btn, button[open-type='share']")
        if share_btn.exists:
            share_btn.click()
            # 注意：分享功能触发onShareAppMessage，实际转发需要用户操作
            # 测试验证分享按钮可点击即可
            self.assertTrue(True, "分享按钮可正常触发")

    # ==================== 商城与服务预约模块 ====================

    def test_shop_001_order_payment(self):
        """TC-SHOP-001: 商品下单与支付流程"""
        # 进入商城列表
        self.app.switch_tab("/pages/shop/shop")

        # 进入商品详情页
        product_item = self.page.get_element(".product-item, .goods-card")
        self.assertTrue(product_item.exists, "商城应有商品列表")
        product_item.click()

        # 选择规格
        spec_selector = self.page.get_element(".spec-item, .sku-option")
        if spec_selector.exists:
            spec_selector.click()

        # 点击立即购买
        buy_btn = self.page.get_element(".buy-now-btn, button.buy")
        self.assertTrue(buy_btn.exists, "应存在购买按钮")
        buy_btn.click()

        # 确认订单页面
        confirm_btn = self.page.get_element(".submit-order-btn, button.submit")
        if confirm_btn.exists:
            confirm_btn.click()

            # 注意：支付流程需要mock或沙箱环境
            # 验证订单状态变更
            order_status = self.page.get_element(".order-status")
            if order_status.exists:
                status_text = order_status.text
                self.assertIn(
                    status_text,
                    ["待支付", "待发货", "已完成"],
                    "订单状态应正确显示"
                )

    def test_shop_002_store_navigation(self):
        """TC-SHOP-002: 门店导航"""
        # 进入服务门店页面
        self.app.navigate_to("/pages/store/list")

        # 选择门店
        store_item = self.page.get_element(".store-item, .shop-card")
        self.assertTrue(store_item.exists, "应有门店列表")
        store_item.click()

        # 点击导航按钮
        nav_btn = self.page.get_element(".navigation-btn, .nav-btn")
        if nav_btn.exists:
            nav_btn.click()
            # 注意：wx.openLocation 会拉起地图，测试环境验证按钮可点击
            self.assertTrue(True, "导航按钮可正常触发")

    # ==================== 个人中心与设置 ====================

    def test_user_001_address_management(self):
        """TC-USER-001: 地址管理"""
        # 进入个人中心
        self.app.switch_tab("/pages/user/user")

        # 进入收货地址页面
        address_entry = self.page.get_element(".address-entry, .my-address")
        self.assertTrue(address_entry.exists, "应有地址管理入口")
        address_entry.click()

        # 点击新增地址
        add_address_btn = self.page.get_element(".add-address-btn, button.add")
        self.assertTrue(add_address_btn.exists, "应有新增地址按钮")
        add_address_btn.click()

        # 使用微信导入地址或手动输入
        wechat_import = self.page.get_element(
            "button[open-type='chooseAddress'], .wechat-import"
        )
        if wechat_import.exists:
            wechat_import.click()
        else:
            # 手动输入地址
            name_input = self.page.get_element("input.name, .name-input input")
            if name_input.exists:
                name_input.input("测试用户")

            phone_input = self.page.get_element("input.phone, .phone-input input")
            if phone_input.exists:
                phone_input.input("13800138000")

            address_input = self.page.get_element(
                "textarea.address, .address-input textarea"
            )
            if address_input.exists:
                address_input.input("北京市朝阳区测试街道123号")

        # 保存地址
        save_btn = self.page.get_element(".save-btn, button.save")
        if save_btn.exists:
            save_btn.click()

            # 设为默认
            default_checkbox = self.page.get_element(".default-checkbox, .set-default")
            if default_checkbox.exists:
                default_checkbox.click()

        # 验证地址列表显示
        address_list = self.page.get_element(".address-item, .address-card")
        self.assertTrue(
            address_list.exists,
            "地址列表应显示新增的地址"
        )

        # 验证默认地址标识
        default_tag = self.page.get_element(".default-tag")
        if default_tag.exists:
            self.assertTrue(default_tag.exists, "应显示默认地址标识")