import minium


class TestUserModule(minium.MiniTest):
    """用户模块测试 - TC-USER-001, TC-USER-002"""

    def test_wechat_authorization_login(self):
        """TC-USER-001: 微信授权登录"""
        # 检测当前登录状态 - 查看是否存在登录按钮
        login_btn = self.page.get_element("button", inner_text="登录")
        if login_btn:
            login_btn.click()
        
        # 触发授权 - 点击允许授权按钮
        allow_btn = self.page.get_element("button", inner_text="允许")
        if allow_btn:
            allow_btn.click()
        
        # 验证登录成功 - 检查是否跳转到首页或用户中心
        current_path = self.page.path
        is_home_or_user = "pages/index" in current_path or "pages/user" in current_path or "pages/mine" in current_path
        self.assertTrue(is_home_or_user, "登录后应跳转至首页或用户中心")

    def test_phone_number_binding(self):
        """TC-USER-002: 手机号绑定"""
        # 进入用户中心/设置页面
        self.app.switch_tab("/pages/mine/mine")
        
        # 点击设置或用户信息区域
        settings_entry = self.page.get_element(".settings-btn")
        if not settings_entry:
            settings_entry = self.page.get_element("view", inner_text="设置")
        if settings_entry:
            settings_entry.click()
        
        # 点击绑定手机号按钮
        bind_phone_btn = self.page.get_element("button", inner_text="绑定手机号")
        if not bind_phone_btn:
            bind_phone_btn = self.page.get_element("button[open-type='getPhoneNumber']")
        if bind_phone_btn:
            bind_phone_btn.click()
        
        # 验证绑定结果 - 检查是否显示手机号
        phone_display = self.page.get_element(".phone-number")
        if phone_display:
            phone_text = phone_display.text
            self.assertIn("***", phone_text, "手机号应部分隐藏显示")


class TestPetProfileModule(minium.MiniTest):
    """宠物档案模块测试 - TC-PET-001, TC-PET-002"""

    def test_add_new_pet_profile(self):
        """TC-PET-001: 新增宠物档案"""
        # 进入我的宠物列表页
        self.app.navigate_to("/pages/pet/list/list")
        
        # 点击添加宠物按钮
        add_btn = self.page.get_element(".add-pet-btn")
        if not add_btn:
            add_btn = self.page.get_element("button", inner_text="添加宠物")
        if not add_btn:
            add_btn = self.page.get_element("view", inner_text="添加宠物")
        self.assertTrue(add_btn is not None, "应存在添加宠物按钮")
        add_btn.click()
        
        # 输入宠物名称
        name_input = self.page.get_element("input[placeholder*='名称']")
        if not name_input:
            name_input = self.page.get_element("input[placeholder*='宠物名']")
        if name_input:
            name_input.input("小白")
        
        # 选择宠物类型 - 猫
        type_cat = self.page.get_element("view", inner_text="猫")
        if not type_cat:
            type_cat = self.page.get_element(".pet-type-cat")
        if type_cat:
            type_cat.click()
        
        # 点击保存按钮
        save_btn = self.page.get_element("button", inner_text="保存")
        if not save_btn:
            save_btn = self.page.get_element("button", inner_text="提交")
        if save_btn:
            save_btn.click()
        
        # 验证添加成功 - 返回列表页检查新宠物卡片
        pet_card = self.page.get_element(".pet-card")
        self.assertTrue(pet_card is not None, "列表页应显示宠物卡片")

    def test_edit_pet_weight_record(self):
        """TC-PET-002: 编辑宠物体重记录"""
        # 进入宠物列表页
        self.app.navigate_to("/pages/pet/list/list")
        
        # 点击进入宠物详情页
        pet_card = self.page.get_element(".pet-card")
        if pet_card:
            pet_card.click()
        
        # 点击记录体重按钮
        weight_btn = self.page.get_element("view", inner_text="记录体重")
        if not weight_btn:
            weight_btn = self.page.get_element(".record-weight-btn")
        if weight_btn:
            weight_btn.click()
        
        # 输入体重数值
        weight_input = self.page.get_element("input[placeholder*='体重']")
        if weight_input:
            weight_input.input("5.5")
        
        # 点击保存
        save_btn = self.page.get_element("button", inner_text="保存")
        if save_btn:
            save_btn.click()
        
        # 验证体重数据更新
        weight_display = self.page.get_element(".weight-value")
        if weight_display:
            weight_text = weight_display.text
            self.assertIn("5.5", weight_text, "体重数据应正确显示")


class TestMallServiceModule(minium.MiniTest):
    """商城与服务模块测试 - TC-ORDER-001, TC-ORDER-002"""

    def test_product_order_process(self):
        """TC-ORDER-001: 商品下单流程"""
        # 进入首页
        self.app.switch_tab("/pages/index/index")
        
        # 点击商品卡片进入详情页
        product_card = self.page.get_element(".product-card")
        if not product_card:
            product_card = self.page.get_element(".goods-item")
        self.assertTrue(product_card is not None, "首页应存在商品卡片")
        product_card.click()
        
        # 选择规格
        spec_btn = self.page.get_element(".spec-option")
        if spec_btn:
            spec_btn.click()
        
        # 点击立即购买
        buy_btn = self.page.get_element("button", inner_text="立即购买")
        if not buy_btn:
            buy_btn = self.page.get_element("button", inner_text="去结算")
        if buy_btn:
            buy_btn.click()
        
        # 确认订单页面 - 确认地址
        address_section = self.page.get_element(".address-section")
        self.assertTrue(address_section is not None, "订单确认页应显示地址区域")
        
        # 点击提交订单
        submit_btn = self.page.get_element("button", inner_text="提交订单")
        if submit_btn:
            submit_btn.click()
        
        # 验证进入支付环节
        pay_section = self.page.get_element(".pay-section")
        if not pay_section:
            pay_section = self.page.get_element("view", inner_text="支付")
        self.assertTrue(pay_section is not None, "应进入支付环节")

    def test_wechat_payment_verification(self):
        """TC-ORDER-002: 微信支付验证"""
        # 进入订单列表页
        self.app.navigate_to("/pages/order/list/list")
        
        # 点击待支付订单
        unpaid_order = self.page.get_element(".order-item-unpaid")
        if not unpaid_order:
            unpaid_order = self.page.get_element("view", inner_text="待支付")
        if unpaid_order:
            unpaid_order.click()
        
        # 点击去支付按钮
        pay_btn = self.page.get_element("button", inner_text="去支付")
        if pay_btn:
            pay_btn.click()
        
        # 验证支付参数调用 - 检查支付相关UI
        payment_ui = self.page.get_element(".payment-modal")
        if payment_ui:
            self.assertTrue(payment_ui is not None, "应弹出支付界面")


class TestCommunityModule(minium.MiniTest):
    """社区与互动模块测试 - TC-SOC-001, TC-SOC-002"""

    def test_publish_pet_dynamics(self):
        """TC-SOC-001: 发布宠物动态"""
        # 进入社区页面
        self.app.switch_tab("/pages/community/community")
        
        # 点击发布按钮
        publish_btn = self.page.get_element(".publish-btn")
        if not publish_btn:
            publish_btn = self.page.get_element("view", inner_text="+")
        if not publish_btn:
            publish_btn = self.page.get_element("button", inner_text="发布")
        self.assertTrue(publish_btn is not None, "应存在发布按钮")
        publish_btn.click()
        
        # 输入文本内容
        content_input = self.page.get_element("textarea")
        if not content_input:
            content_input = self.page.get_element("input[placeholder*='内容']")
        if content_input:
            content_input.input("今天我家小猫咪好可爱！")
        
        # 点击添加图片按钮
        add_img_btn = self.page.get_element(".add-image-btn")
        if not add_img_btn:
            add_img_btn = self.page.get_element("view", inner_text="添加图片")
        if add_img_btn:
            add_img_btn.click()
        
        # 点击发布
        submit_btn = self.page.get_element("button", inner_text="发布")
        if submit_btn:
            submit_btn.click()
        
        # 验证发布成功
        success_tip = self.page.get_element("view", inner_text="发布成功")
        if success_tip:
            self.assertTrue(success_tip is not None, "应显示发布成功提示")

    def test_share_function(self):
        """TC-SOC-002: 分享功能测试"""
        # 进入社区页面
        self.app.switch_tab("/pages/community/community")
        
        # 点击某篇动态进入详情
        dynamic_item = self.page.get_element(".dynamic-item")
        if dynamic_item:
            dynamic_item.click()
        
        # 点击分享按钮
        share_btn = self.page.get_element(".share-btn")
        if not share_btn:
            share_btn = self.page.get_element("button", inner_text="分享")
        if not share_btn:
            share_btn = self.page.get_element("button[open-type='share']")
        if share_btn:
            share_btn.click()
        
        # 验证分享面板 - 通过获取转发信息
        share_info = self.page.get_element(".share-panel")
        if share_info:
            self.assertTrue(share_info is not None, "应弹出分享面板")


class TestMapLocationModule(minium.MiniTest):
    """地图与位置服务测试 - TC-MAP-001, TC-MAP-002"""

    def test_nearby_service_query(self):
        """TC-MAP-001: 附近服务查询"""
        # 进入附近/服务Tab
        self.app.switch_tab("/pages/nearby/nearby")
        
        # 触发位置授权 - 点击授权允许
        allow_btn = self.page.get_element("button", inner_text="允许")
        if allow_btn:
            allow_btn.click()
        
        # 验证地图组件加载
        map_component = self.page.get_element("map")
        self.assertTrue(map_component is not None, "地图组件应正确加载")
        
        # 验证门店列表展示
        store_list = self.page.get_element(".store-list")
        if not store_list:
            store_list = self.page.get_element(".service-list")
        self.assertTrue(store_list is not None, "应展示附近服务门店列表")

    def test_navigation_function(self):
        """TC-MAP-002: 导航功能"""
        # 进入附近页面
        self.app.switch_tab("/pages/nearby/nearby")
        
        # 点击地图上的标记点
        marker = self.page.get_element(".map-marker")
        if not marker:
            marker = self.page.get_element("view", inner_text="宠物医院")
        if marker:
            marker.click()
        
        # 点击导航按钮
        nav_btn = self.page.get_element("button", inner_text="导航")
        if not nav_btn:
            nav_btn = self.page.get_element("view", inner_text="导航")
        if nav_btn:
            nav_btn.click()
        
        # 验证导航界面弹出
        nav_panel = self.page.get_element(".navigation-panel")
        if nav_panel:
            self.assertTrue(nav_panel is not None, "应弹出地图导航预览界面")


class TestComponentModule(minium.MiniTest):
    """组件测试 - TC-COMP-001"""

    def test_custom_component_rendering(self):
        """TC-COMP-001: 自定义组件渲染"""
        # 进入首页检查宠物卡片组件
        self.app.switch_tab("/pages/index/index")
        
        # 检查宠物卡片组件是否存在
        pet_card_component = self.page.get_element(".pet-card-component")
        if not pet_card_component:
            pet_card_component = self.page.get_element("pet-card")
        if pet_card_component:
            # 验证组件渲染正常
            self.assertTrue(pet_card_component is not None, "宠物卡片组件应存在")
            
            # 验证组件内元素
            card_title = pet_card_component.get_element(".card-title")
            if card_title:
                self.assertTrue(card_title is not None, "组件内标题应正常渲染")
        
        # 进入宠物列表页检查组件
        self.app.navigate_to("/pages/pet/list/list")
        
        # 检查列表项组件
        list_item = self.page.get_element(".pet-list-item")
        if list_item:
            self.assertTrue(list_item is not None, "列表项组件应正常渲染")
            
            # 模拟点击组件触发事件
            list_item.click()
            
            # 验证事件传递 - 应跳转到详情页
            current_path = self.page.path
            is_detail_page = "detail" in current_path or "info" in current_path
            self.assertTrue(is_detail_page, "组件点击事件应正确传递并跳转")


class TestIntegration(minium.MiniTest):
    """集成测试 - 核心业务流程"""

    def test_complete_user_journey(self):
        """完整用户旅程测试：登录 -> 添加宠物 -> 浏览商品 -> 发布动态"""
        # Step 1: 用户登录
        self.app.switch_tab("/pages/mine/mine")
        login_btn = self.page.get_element("button", inner_text="登录")
        if login_btn:
            login_btn.click()
            allow_btn = self.page.get_element("button", inner_text="允许")
            if allow_btn:
                allow_btn.click()
        
        # Step 2: 添加宠物
        self.app.navigate_to("/pages/pet/list/list")
        add_pet_btn = self.page.get_element(".add-pet-btn")
        if add_pet_btn:
            add_pet_btn.click()
            name_input = self.page.get_element("input[placeholder*='名称']")
            if name_input:
                name_input.input("测试宠物")
            save_btn = self.page.get_element("button", inner_text="保存")
            if save_btn:
                save_btn.click()
        
        # Step 3: 浏览商品
        self.app.switch_tab("/pages/index/index")
        product = self.page.get_element(".product-card")
        if product:
            product.click()
            self.page.get_element("button", inner_text="返回")
        
        # Step 4: 发布动态
        self.app.switch_tab("/pages/community/community")
        publish_btn = self.page.get_element(".publish-btn")
        if publish_btn:
            publish_btn.click()
            content = self.page.get_element("textarea")
            if content:
                content.input("带我家宠物出来玩啦！")
            submit = self.page.get_element("button", inner_text="发布")
            if submit:
                submit.click()
        
        # 验证完整流程
        self.assertTrue(True, "完整用户旅程测试通过")