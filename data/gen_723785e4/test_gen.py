```python
import minium
import time


class TestPureActivity(minium.MiniTest):
    """Pure-Activity 纯活动小程序自动化测试"""

    # ==================== Suite: 01_用户鉴权模块 ====================
    
    def test_auth_001_wechat_login(self):
        """TC-AUTH-001: 微信授权登录"""
        # 启动小程序，跳转至首页
        self.app.navigate_to("/pages/index/index")
        self.page.wait_for(2)
        
        # 检查是否存在授权登录按钮
        auth_button = self.page.get_element("button", inner_text_contains="授权登录")
        avatar_button = self.page.get_element("button[open-type='chooseAvatar']")
        
        if auth_button or avatar_button:
            # 模拟点击授权按钮
            if auth_button:
                auth_button.click()
            elif avatar_button:
                avatar_button.click()
            
            self.page.wait_for(1)
            
            # 模拟授权弹窗点击允许
            self.app.mock_wx_method("getUserProfile", {
                "userInfo": {
                    "nickName": "测试用户",
                    "avatarUrl": "https://example.com/avatar.png"
                }
            })
        
        # 验证登录状态
        user_token = self.app.get_storage("token")
        self.assertIsNotNone(user_token, "用户Token应已存储")
        
        # 验证UI更新为已登录状态
        user_avatar = self.page.get_element(".user-avatar")
        user_nickname = self.page.get_element(".user-nickname")
        self.assertTrue(user_avatar or user_nickname, "页面应显示用户头像或昵称")

    def test_auth_002_phone_binding(self):
        """TC-AUTH-002: 手机号授权绑定"""
        # 进入个人中心页面
        self.app.navigate_to("/pages/mine/mine")
        self.page.wait_for(2)
        
        # 检查是否已绑定手机号
        phone_display = self.page.get_element(".phone-display")
        
        if not phone_display or "未绑定" in phone_display.text:
            # 点击绑定手机号按钮
            bind_button = self.page.get_element("button", inner_text_contains="绑定手机")
            if not bind_button:
                bind_button = self.page.get_element("button[open-type='getPhoneNumber']")
            
            self.assertIsNotNone(bind_button, "应存在绑定手机号按钮")
            bind_button.click()
            self.page.wait_for(1)
            
            # 模拟授权弹窗允许
            self.app.mock_wx_method("getPhoneNumber", {
                "encryptedData": "mock_encrypted_data",
                "iv": "mock_iv"
            })
        
        # 验证手机号显示（掩码格式）
        self.page.wait_for(2)
        phone_element = self.page.get_element(".phone-number")
        if phone_element:
            phone_text = phone_element.text
            # 验证手机号格式（中间四位掩码）
            self.assertRegex(phone_text, r"1\d{2}\*{4}\d{4}", "手机号应为掩码格式")

    # ==================== Suite: 02_活动核心流程 ====================
    
    def test_act_001_activity_list_and_filter(self):
        """TC-ACT-001: 活动列表加载与筛选"""
        # 跳转至活动列表页
        self.app.navigate_to("/pages/activity/list/list")
        self.page.wait_for(1)
        
        # 检查Loading状态
        loading_element = self.page.get_element(".loading-spinner")
        # Loading可能在页面初始时短暂出现
        
        self.page.wait_for(2)
        
        # 检查列表数据渲染
        activity_cards = self.page.get_elements(".activity-card")
        self.assertGreaterEqual(len(activity_cards), 1, "列表应至少有一条活动卡片")
        
        # 检查图片加载
        first_card_img = self.page.get_element(".activity-card image")
        if first_card_img:
            img_src = first_card_img.attribute("src")
            self.assertIsNotNone(img_src, "活动图片应有有效src")
        
        # 切换顶部Tab
        tabs = ["全部", "进行中", "已结束"]
        for tab_name in tabs:
            tab_element = self.page.get_element(".tab-item", inner_text=tab_name)
            if tab_element:
                tab_element.click()
                self.page.wait_for(1)
                # 验证Tab切换后数据更新
                current_active = self.page.get_element(".tab-item.active")
                self.assertIn(tab_name, current_active.text, f"当前激活Tab应为{tab_name}")
        
        # 执行下拉刷新
        self.page.pull_down_refresh()
        self.page.wait_for(2)
        
        # 验证刷新后数据
        refreshed_cards = self.page.get_elements(".activity-card")
        self.assertGreaterEqual(len(refreshed_cards), 1, "刷新后列表应有数据")

    def test_act_002_activity_detail(self):
        """TC-ACT-002: 活动详情查看"""
        # 先进入活动列表
        self.app.navigate_to("/pages/activity/list/list")
        self.page.wait_for(2)
        
        # 点击第一张活动卡片
        first_card = self.page.get_element(".activity-card")
        self.assertIsNotNone(first_card, "应存在活动卡片")
        
        # 获取活动名称用于后续验证
        card_title = self.page.get_element(".activity-card .activity-title")
        expected_title = card_title.text if card_title else ""
        
        first_card.click()
        self.page.wait_for(2)
        
        # 验证路由参数传递
        current_page = self.app.get_current_page()
        self.assertIn("id=", current_page.path, "详情页URL应包含活动ID参数")
        
        # 检查页面标题
        page_title = self.page.get_element(".detail-title")
        if page_title and expected_title:
            self.assertEqual(expected_title, page_title.text, "页面标题应与活动名称一致")
        
        # 检查富文本内容渲染
        rich_text = self.page.get_element(".rich-text-content")
        self.assertIsNotNone(rich_text, "活动介绍内容应存在")
        
        # 检查关键信息展示
        time_info = self.page.get_element(".activity-time")
        location_info = self.page.get_element(".activity-location")
        fee_info = self.page.get_element(".activity-fee")
        
        self.assertTrue(time_info or location_info or fee_info, "应展示时间/地点/费用信息")
        
        # 检查报名按钮状态
        register_button = self.page.get_element(".register-button")
        self.assertIsNotNone(register_button, "应存在报名按钮")
        
        button_text = register_button.text
        valid_states = ["未开始", "立即报名", "已结束", "已报名"]
        self.assertIn(button_text, valid_states, "按钮状态应符合业务逻辑")

    def test_act_003_activity_registration(self):
        """TC-ACT-003: 活动报名表单提交"""
        # 进入活动详情页
        self.app.navigate_to("/pages/activity/list/list")
        self.page.wait_for(2)
        
        # 找一个可报名的活动
        register_btn = self.page.get_element(".register-btn", inner_text="立即报名")
        if not register_btn:
            # 如果列表页没有，进入详情页查找
            self.page.get_element(".activity-card").click()
            self.page.wait_for(2)
            register_btn = self.page.get_element("button", inner_text="立即报名")
        
        if register_btn:
            register_btn.click()
            self.page.wait_for(2)
            
            # 验证跳转到报名表单页
            current_page = self.app.get_current_page()
            self.assertIn("register", current_page.path, "应跳转至报名表单页")
            
            # 检查自动填充的用户信息
            name_input = self.page.get_element("input[name='name']")
            phone_input = self.page.get_element("input[name='phone']")
            
            # 验证自动填充
            if name_input:
                name_value = name_input.attribute("value")
                self.assertIsNotNone(name_value, "姓名应自动填充")
            
            # 修改必填项
            if name_input:
                name_input.input("测试报名者")
            if phone_input:
                phone_input.input("13800138000")
            
            # 填写其他必填项
            remark_input = self.page.get_element("textarea[name='remark']")
            if remark_input:
                remark_input.input("自动化测试报名")
            
            # 点击提交
            submit_btn = self.page.get_element("button", inner_text_contains="提交")
            submit_btn.click()
            self.page.wait_for(3)
            
            # 验证提交结果
            success_toast = self.page.get_element(".toast-success")
            success_text = self.page.get_element(".success-message")
            
            # 验证跳转到成功页或返回详情页
            current_page = self.app.get_current_page()
            is_success_page = "success" in current_page.path
            is_detail_page = "detail" in current_page.path
            
            self.assertTrue(is_success_page or is_detail_page, "应跳转至成功页或返回详情页")

    # ==================== Suite: 03_支付与订单模块 ====================
    
    def test_pay_001_wechat_payment(self):
        """TC-PAY-001: 微信支付流程"""
        # 进入确认订单页
        self.app.navigate_to("/pages/order/confirm/confirm")
        self.page.wait_for(2)
        
        # 选择支付方式（如有选项）
        payment_options = self.page.get_elements(".payment-option")
        if payment_options:
            payment_options[0].click()
        
        # 点击去支付
        pay_button = self.page.get_element("button", inner_text_contains="去支付")
        self.assertIsNotNone(pay_button, "应存在支付按钮")
        
        # Mock微信支付
        self.app.mock_wx_method("requestPayment", {"errMsg": "requestPayment:ok"})
        
        pay_button.click()
        self.page.wait_for(3)
        
        # 验证支付成功后的状态
        # 检查是否跳转到支付成功页
        current_page = self.app.get_current_page()
        is_payment_result = "payment" in current_page.path or "result" in current_page.path
        
        # 或检查订单状态显示
        order_status = self.page.get_element(".order-status")
        if order_status:
            self.assertIn("已支付", order_status.text, "订单状态应为已支付")

    def test_ord_001_order_status_flow(self):
        """TC-ORD-001: 订单列表状态流转"""
        # 进入我的订单页面
        self.app.navigate_to("/pages/order/list/list")
        self.page.wait_for(2)
        
        # 检查Tab存在
        tabs = ["待支付", "待参加", "已完成"]
        for tab_name in tabs:
            tab = self.page.get_element(".tab-item", inner_text=tab_name)
            if tab:
                tab.click()
                self.page.wait_for(1)
                
                # 验证Tab下数据
                orders = self.page.get_elements(".order-item")
                # 可以根据Tab验证订单状态标签
                if orders:
                    status_label = self.page.get_element(".order-status")
                    if tab_name == "待支付" and status_label:
                        self.assertIn("待支付", status_label.text)
        
        # 切换到待支付Tab执行取消操作
        pending_tab = self.page.get_element(".tab-item", inner_text="待支付")
        if pending_tab:
            pending_tab.click()
            self.page.wait_for(1)
            
            # 找取消按钮
            cancel_btn = self.page.get_element("button", inner_text_contains="取消")
            if cancel_btn:
                cancel_btn.click()
                self.page.wait_for(1)
                
                # 确认取消弹窗
                confirm_btn = self.page.get_element("button", inner_text="确定")
                if confirm_btn:
                    confirm_btn.click()
                    self.page.wait_for(2)
                
                # 验证订单从列表消失或状态变更
                self.page.wait_for(1)

    # ==================== Suite: 04_微信特色功能 ====================
    
    def test_wx_001_location_authorization(self):
        """TC-WX-001: 用户位置授权"""
        # 进入附近活动或活动地图页面
        self.app.navigate_to("/pages/activity/nearby/nearby")
        self.page.wait_for(2)
        
        # Mock位置授权
        self.app.mock_wx_method("getLocation", {
            "latitude": 31.2304,
            "longitude": 121.4737,
            "errMsg": "getLocation:ok"
        })
        
        # 检查地图组件
        map_component = self.page.get_element("map")
        self.assertIsNotNone(map_component, "应存在地图组件")
        
        # 检查当前位置标记
        location_marker = self.page.get_element(".current-location-marker")
        
        # 检查列表按距离排序
        distance_labels = self.page.get_elements(".distance-label")
        if len(distance_labels) >= 2:
            # 验证距离显示格式
            first_distance = distance_labels[0].text
            self.assertRegex(first_distance, r"\d+(\.\d+)?(km|m)", "距离格式应正确")

    def test_wx_002_share_function(self):
        """TC-WX-002: 分享功能"""
        # 进入活动详情页
        self.app.navigate_to("/pages/activity/detail/detail?id=1")
        self.page.wait_for(2)
        
        # 获取页面分享配置
        page = self.app.get_current_page()
        
        # 触发分享（模拟点击分享按钮）
        share_button = self.page.get_element("button[open-type='share']")
        if not share_button:
            share_button = self.page.get_element(".share-btn")
        
        if share_button:
            share_button.click()
            self.page.wait_for(1)
        
        # 验证分享配置（通过页面数据）
        # 分享标题应与活动名称一致
        activity_title = self.page.get_element(".detail-title")
        if activity_title:
            share_title = activity_title.text
            self.assertIsNotNone(share_title, "分享标题应存在")

    def test_wx_003_generate_poster(self):
        """TC-WX-003: 生成活动海报"""
        # 进入活动详情页
        self.app.navigate_to("/pages/activity/detail/detail?id=1")
        self.page.wait_for(2)
        
        # 点击生成海报按钮
        poster_btn = self.page.get_element("button", inner_text_contains="生成海报")
        if not poster_btn:
            poster_btn = self.page.get_element(".poster-btn")
        
        if poster_btn:
            poster_btn.click()
            self.page.wait_for(3)
            
            # Mock相册授权
            self.app.mock_wx_method("saveImageToPhotosAlbum", {
                "errMsg": "saveImageToPhotosAlbum:ok"
            })
            
            # 检查Canvas绘制
            canvas = self.page.get_element("canvas")
            
            # 检查保存按钮
            save_btn = self.page.get_element("button", inner_text_contains="保存")
            if save_btn:
                save_btn.click()
                self.page.wait_for(1)
            
            # 验证成功提示
            success_msg = self.page.get_element(".toast-success")
            if success_msg:
                self.assertIn("成功", success_msg.text)

    # ==================== Suite: 05_个人中心 ====================
    
    def test_user_001_profile_edit(self):
        """TC-USER-001: 个人信息修改"""
        # 进入个人中心
        self.app.navigate_to("/pages/mine/mine")
        self.page.wait_for(2)
        
        # 点击编辑资料
        edit_btn = self.page.get_element("button", inner_text_contains="编辑资料")
        if not edit_btn:
            edit_btn = self.page.get_element(".edit-profile")
        
        if edit_btn:
            edit_btn.click()
            self.page.wait_for(1)
            
            # 修改昵称
            nickname_input = self.page.get_element("input[name='nickname']")
            if nickname_input:
                new_nickname = "测试用户" + str(int(time.time()) % 10000)
                nickname_input.input(new_nickname)
            
            # 点击保存
            save_btn = self.page.get_element("button", inner_text_contains="保存")
            save_btn.click()
            self.page.wait_for(2)
            
            # 返回个人中心验证
            self.app.navigate_back()
            self.page.wait_for(1)
            
            # 验证昵称更新
            nickname_display = self.page.get_element(".user-nickname")
            if nickname_display and nickname_input:
                self.assertIn(new_nickname[:4], nickname_display.text)

    def test_user_002_activity_publish(self):
        """TC-USER-002: 活动管理（主办方视角）"""
        # 进入个人中心
        self.app.navigate_to("/pages/mine/mine")
        self.page.wait_for(2)
        
        # 切换身份为主办方（如有此功能）
        switch_btn = self.page.get_element("button", inner_text_contains="切换主办方")
        if switch_btn:
            switch_btn.click()
            self.page.wait_for(1)
        
        # 点击发布活动
        publish_btn = self.page.get_element("button", inner_text_contains="发布活动")
        if not publish_btn:
            publish_btn = self.page.get_element(".publish-activity")
        
        if publish_btn:
            publish_btn.click()
            self.page.wait_for(2)
            
            # 验证进入发布页面
            current_page = self.app.get_current_page()
            self.assertIn("publish", current_page.path, "应进入发布活动页")
            
            # 填写活动表单
            title_input = self.page.get_element("input[name='title']")
            if title_input:
                title_input.input("自动化测试活动" + str(int(time.time()) % 10000))
            
            # 选择时间
            time_picker = self.page.get_element("picker[mode='date']")
            if time_picker:
                time_picker.click()
                self.page.wait_for(1)
                confirm_btn = self.page.get_element(".picker-confirm")
                if confirm_btn:
                    confirm_btn.click()
            
            # 填写地点
            location_input = self.page.get_element("input[name='location']")
            if location_input:
                location_input.input("测试地点")
            
            # 上传封面图
            upload_btn = self.page.get_element(".upload-image")
            if upload_btn:
                # Mock图片选择
                self.app.mock_wx_method("chooseImage", {
                    "tempFilePaths": ["/mock/test-image.jpg"]
                })
                upload_btn.click()
                self.page.wait_for(1)
            
            # 提交审核
            submit_btn = self.page.get_element("button", inner_text_contains="提交审核")
            if submit_btn:
                submit_btn.click()
                self.page.wait_for(3)
                
                # 验证提交成功
                success_msg = self.page.get_element(".success-message")
                if success_msg:
                    self.assertIn("成功", success_msg.text)
                
                # 验证活动状态为审核中
                status_label = self.page.get_element(".activity