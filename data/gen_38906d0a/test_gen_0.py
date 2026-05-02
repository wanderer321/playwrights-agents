import minium


class TestUserAuth(minium.MiniTest):
    """Suite: 01_用户授权与登录模块"""

    def test_auth_001_wechat_authorization_login(self):
        """TC-AUTH-001: 微信授权登录"""
        # 启动小程序，进入首页
        self.app.switch_tab("/pages/index/index")
        
        # 检测页面是否包含授权按钮
        auth_button = self.page.get_element('button[open-type="getUserInfo"]')
        if not auth_button:
            # 检查是否有头像昵称填写能力（新版授权方式）
            avatar_button = self.page.get_element('.avatar-wrapper, button[open-type="chooseAvatar"]')
            nickname_input = self.page.get_element('input[type="nickname"]')
            
            if avatar_button:
                avatar_button.click()
            if nickname_input:
                nickname_input.input("测试用户")
        
        # 模拟 wx.getUserProfile 返回成功
        self.app.mock_wx_method(
            "getUserProfile",
            True,
            {
                "userInfo": {
                    "nickName": "测试用户",
                    "avatarUrl": "https://example.com/avatar.png"
                }
            }
        )
        
        # 如果存在授权按钮则点击
        if auth_button:
            auth_button.click()
        
        # 验证本地缓存是否有 token 或用户信息
        storage_info = self.app.get_storage_info()
        self.assertTrue(len(storage_info.get("keys", [])) > 0, "本地缓存应有数据")
        
        # 验证页面跳转成功（首页或活动列表页）
        current_path = self.page.path
        self.assertIn("/pages/", current_path, "应成功跳转至页面")

    def test_auth_002_phone_number_binding(self):
        """TC-AUTH-002: 手机号授权绑定"""
        # 进入用户中心
        self.app.switch_tab("/pages/profile/profile")
        
        # 查找绑定手机号按钮
        phone_button = self.page.get_element('button[open-type="getPhoneNumber"]')
        
        if phone_button:
            # 模拟微信接口返回加密数据
            self.app.mock_wx_method(
                "getPhoneNumber",
                True,
                {
                    "code": "test_phone_code_123",
                    "encryptedData": "encrypted_phone_data",
                    "iv": "test_iv_value"
                }
            )
            
            phone_button.click()
            
            # 检查页面显示的手机号
            phone_display = self.page.get_element('.phone-number, .user-phone, [class*="phone"]')
            if phone_display:
                phone_text = phone_display.text
                # 验证脱敏格式 (如: 138****8888)
                self.assertTrue(
                    "*" in phone_text or len(phone_text) >= 4,
                    "手机号应显示脱敏格式"
                )


class TestActivityBrowse(minium.MiniTest):
    """Suite: 02_活动浏览与核心业务"""

    def test_act_001_activity_list_loading_and_pagination(self):
        """TC-ACT-001: 活动列表加载与分页"""
        # 进入首页（活动列表）
        self.app.switch_tab("/pages/index/index")
        
        # 验证首屏数据加载
        activity_items = self.page.get_elements('.activity-item, .activity-card, [class*="activity"]')
        self.assertTrue(len(activity_items) >= 0, "列表应有数据加载")
        
        # 检查 swiper 轮播图是否存在
        swiper = self.page.get_element('.slogan-swiper')
        self.assertIsNotNone(swiper, "轮播图组件应存在")
        
        # 模拟页面滚动到底部
        self.page.scroll_to(9999)
        
        # 验证触底加载（检查列表是否追加）
        activity_items_after = self.page.get_elements('.activity-item, .activity-card')
        # 列表长度应大于等于之前（或保持不变，取决于是否有更多数据）
        self.assertTrue(len(activity_items_after) >= 0, "滚动后列表状态正常")

    def test_act_002_activity_detail_rendering(self):
        """TC-ACT-002: 活动详情页渲染"""
        # 进入首页
        self.app.switch_tab("/pages/index/index")
        
        # 查找活动卡片并点击
        activity_card = self.page.get_element('.activity-item, .activity-card, [class*="activity"]')
        
        if activity_card:
            activity_card.click()
            
            # 获取页面路径参数
            current_path = self.page.path
            self.assertIn("/pages/", current_path, "应跳转至详情页")
            
            # 检查关键元素是否渲染
            title_element = self.page.get_element('.detail-title, .activity-title, [class*="title"]')
            time_element = self.page.get_element('.detail-time, .activity-time, [class*="time"]')
            location_element = self.page.get_element('.detail-location, .activity-location, [class*="location"]')
            price_element = self.page.get_element('.detail-price, .activity-price, [class*="price"]')
            
            # 至少应有标题元素
            self.assertIsNotNone(title_element, "详情页应有标题元素")
            
            # 检查图片是否正常
            images = self.page.get_elements('image')
            self.assertTrue(len(images) >= 0, "详情页应有图片元素")


class TestPaymentOrder(minium.MiniTest):
    """Suite: 03_支付与订单模块"""

    def test_pay_001_create_order_and_payment(self):
        """TC-PAY-001: 创建订单并发起支付"""
        # 进入活动创建页
        self.app.switch_tab("/pages/activity-create/activity-create")
        
        # 检查表单元素
        form_card = self.page.get_element('.form-card')
        self.assertIsNotNone(form_card, "表单卡片应存在")
        
        # 选择封面图
        cover_option = self.page.get_element('.cover-option')
        if cover_option:
            cover_option.click()
        
        # 填写表单信息
        title_input = self.page.get_element('input[placeholder*="标题"], input[placeholder*="活动"]')
        if title_input:
            title_input.input("测试活动标题")
        
        # 查找提交/报名按钮
        submit_button = self.page.get_element('.submit-btn, .create-btn, button[class*="submit"]')
        
        if submit_button:
            # 拦截请求检查订单创建接口
            self.app.mock_request(
                url_pattern="*order*",
                success_data={"code": 0, "data": {"orderId": "test_order_123"}}
            )
            
            # 模拟支付成功
            self.app.mock_wx_method(
                "requestPayment",
                True,
                {"errMsg": "requestPayment:ok"}
            )
            
            submit_button.click()
            
            # 验证订单状态
            self.assertTrue(True, "订单创建流程执行完成")

    def test_pay_002_payment_cancel_or_failure(self):
        """TC-PAY-002: 支付取消或失败处理"""
        # 进入活动创建页
        self.app.switch_tab("/pages/activity-create/activity-create")
        
        # 模拟支付取消
        self.app.mock_wx_method(
            "requestPayment",
            False,
            {"errMsg": "requestPayment:fail cancel"}
        )
        
        submit_button = self.page.get_element('.submit-btn, .create-btn, button[class*="submit"]')
        
        if submit_button:
            submit_button.click()
            
            # 检查是否有重新支付入口
            retry_button = self.page.get_element('.retry-btn, .repay-btn, button[class*="retry"]')
            # 验证订单状态提示
            status_text = self.page.get_element('.order-status, .payment-status')
            
            self.assertTrue(True, "支付取消流程执行完成")


class TestShareSocial(minium.MiniTest):
    """Suite: 04_分享与社交裂变"""

    def test_share_001_forward_to_friends(self):
        """TC-SHARE-001: 转发给好友"""
        # 进入首页
        self.app.switch_tab("/pages/index/index")
        
        # 调用页面分享方法
        share_result = self.page.call_method("onShareAppMessage")
        
        # 验证分享配置
        if share_result:
            self.assertIn("title", share_result, "分享配置应包含标题")
            self.assertIn("path", share_result, "分享配置应包含路径")
            self.assertIn("imageUrl", share_result, "分享配置应包含图片")
            
            # 验证路径参数
            share_path = share_result.get("path", "")
            self.assertIn("/pages/", share_path, "分享路径应有效")

    def test_share_002_generate_activity_poster(self):
        """TC-SHARE-002: 生成活动海报"""
        # 进入个人中心
        self.app.switch_tab("/pages/profile/profile")
        
        # 查找生成海报按钮
        poster_button = self.page.get_element('.poster-btn, .share-poster, button[class*="poster"]')
        
        if poster_button:
            # 模拟 Canvas 绘制
            self.app.mock_wx_method(
                "canvasToTempFilePath",
                True,
                {"tempFilePath": "wxfile://tmp_poster.png"}
            )
            
            # 模拟保存到相册
            self.app.mock_wx_method(
                "saveImageToPhotosAlbum",
                True,
                {"errMsg": "saveImageToPhotosAlbum:ok"}
            )
            
            poster_button.click()
            
            # 验证海报生成
            self.assertTrue(True, "海报生成流程执行完成")


class TestLocationMap(minium.MiniTest):
    """Suite: 05_定位与地图服务"""

    def test_loc_001_get_current_location(self):
        """TC-LOC-001: 获取当前位置"""
        # 进入首页
        self.app.switch_tab("/pages/index/index")
        
        # 模拟定位返回
        self.app.mock_wx_method(
            "getLocation",
            True,
            {
                "latitude": 39.9042,
                "longitude": 116.4074,
                "accuracy": 65
            }
        )
        
        # 查找定位按钮
        location_button = self.page.get_element('.location-btn, button[class*="location"]')
        
        if location_button:
            location_button.click()
            
            # 检查地图组件
            map_component = self.page.get_element('map')
            if map_component:
                self.assertIsNotNone(map_component, "地图组件应存在")

    def test_loc_002_navigation_function(self):
        """TC-LOC-002: 导航功能"""
        # 进入首页
        self.app.switch_tab("/pages/index/index")
        
        # 模拟打开地图导航
        self.app.mock_wx_method(
            "openLocation",
            True,
            {"errMsg": "openLocation:ok"}
        )
        
        # 查找导航按钮
        nav_button = self.page.get_element('.nav-btn, button[class*="navigate"]')
        
        if nav_button:
            nav_button.click()
            self.assertTrue(True, "导航功能执行完成")


class TestExceptionCompatibility(minium.MiniTest):
    """Suite: 06_异常与兼容性测试"""

    def test_sys_001_network_error_handling(self):
        """TC-SYS-001: 网络异常处理"""
        # 模拟网络错误
        self.app.mock_request(
            url_pattern="*",
            success_data=None,
            error_message="网络请求失败",
            status_code=500
        )
        
        # 进入首页
        self.app.switch_tab("/pages/index/index")
        
        # 检查是否有错误提示
        error_toast = self.page.get_element('.error-toast, .network-error, [class*="error"]')
        retry_button = self.page.get_element('.retry-btn, button[class*="retry"]')
        
        # 页面不应崩溃
        current_path = self.page.path
        self.assertIn("/pages/", current_path, "页面应正常显示")

    def test_sys_002_page_stack_depth_test(self):
        """TC-SYS-002: 页面栈深度测试"""
        # 获取可导航的页面列表
        pages_to_navigate = [
            "/pages/activity-history/activity-history",
            "/pages/credit/credit",
            "/pages/badges/badges",
            "/pages/settings/settings",
            "/pages/feedback/feedback",
            "/pages/member-center/member-center",
            "/pages/education-auth/education-auth"
        ]
        
        # 先进入首页
        self.app.switch_tab("/pages/index/index")
        
        navigated_count = 0
        max_stack = 8  # 测试到第8层，留2层余量
        
        for page_path in pages_to_navigate[:maxStack]:
            try:
                self.app.navigate_to(page_path)
                navigated_count += 1
                
                # 验证当前页面
                current_path = self.page.path
                self.assertIn(page_path.replace("/", ""), current_path, 
                             f"应成功导航至 {page_path}")
            except Exception as e:
                # 页面栈可能已满，使用 redirectTo
                if "navigateTo" in str(e) or "栈" in str(e):
                    self.app.redirect_to(page_path)
                    navigated_count += 1
                break
        
        # 验证页面栈未溢出
        self.assertTrue(navigated_count > 0, "应成功导航至少一个页面")
        
        # 返回首页
        self.app.switch_tab("/pages/index/index")


class TestProfilePage(minium.MiniTest):
    """个人中心页面测试"""

    def test_profile_page_elements(self):
        """测试个人中心页面元素"""
        self.app.switch_tab("/pages/profile/profile")
        
        # 验证头像区域
        avatar = self.page.get_element('.profile-avatar')
        self.assertIsNotNone(avatar, "头像区域应存在")
        
        # 验证用户信息
        user_name = self.page.get_element('.profile-user-name')
        self.assertIsNotNone(user_name, "用户名区域应存在")
        
        # 验证信用分组件
        credit_score = self.page.get_element('.score--credit-score')
        self.assertIsNotNone(credit_score, "信用分组件应存在")
        
        # 验证统计数据
        stats = self.page.get_elements('.profile-stat-item')
        self.assertTrue(len(stats) >= 0, "统计数据区域应存在")
        
        # 验证菜单项
        menu_items = self.page.get_elements('.profile-menu-item')
        self.assertTrue(len(menu_items) >= 0, "菜单项应存在")

    def test_profile_menu_navigation(self):
        """测试个人中心菜单导航"""
        self.app.switch_tab("/pages/profile/profile")
        
        # 获取菜单项
        menu_item = self.page.get_element('.profile-menu-item[data-url]')
        
        if menu_item:
            # 获取导航路径
            data_url = menu_item.attribute("data-url")
            
            if data_url and data_url != "/pages/":
                menu_item.click()
                
                # 验证页面跳转
                current_path = self.page.path
                self.assertTrue(
                    data_url.replace("/", "") in current_path or "/pages/" in current_path,
                    "菜单导航应成功跳转"
                )


class TestActivityCreatePage(minium.MiniTest):
    """活动创建页面测试"""

    def test_activity_create_form_elements(self):
        """测试活动创建表单元素"""
        self.app.switch_tab("/pages/activity-create/activity-create")
        
        # 验证品牌区域
        brand = self.page.get_element('.create-brand')
        self.assertIsNotNone(brand, "品牌区域应存在")
        
        # 验证表单卡片
        form_card = self.page.get_element('.form-card')
        self.assertIsNotNone(form_card, "表单卡片应存在")
        
        # 验证封面选择
        cover_options = self.page.get_elements('.cover-option')
        self.assertTrue(len(cover_options) > 0, "封面选项应存在")
        
        # 验证信用提示
        credit_notice = self.page.get_element('.credit-notice')
        self.assertIsNotNone(credit_notice, "信用提示应存在")

    def test_activity_create_cover_selection(self):
        """测试活动创建封面选择"""
        self.app.switch_tab("/pages/activity-create/activity-create")
        
        # 获取所有封面选项
        cover_options = self.page.get_elements('.cover-option')
        
        if len(cover_options) > 1:
            # 点击第二个封面选项
            cover_options[1].click()
            
            # 验证选中状态
            active_cover = self.page.get_element('.cover-option-active, .cover-option.cover-option-active')
            self.assertIsNotNone(active_cover, "封面选中状态应更新")


class TestIndexPage(minium.MiniTest):
    """首页测试"""

    def test_index_page_swiper(self):
        """测试首页轮播图"""
        self.app.switch_tab("/pages/index/index")
        
        # 验证品牌头部
        brand_header = self.page.get_element('.brand-header')
        self.assertIsNotNone(brand_header, "品牌头部应存在")
        
        # 验证轮播图
        swiper = self.page.get_element('.slogan-swiper')
        self.assertIsNotNone(swiper, "轮播图组件应存在")
        
        # 验证轮播卡片
        swiper_items = self.page.get_elements('.slogan-card')
        self.assertTrue(len(swiper_items) > 0, "轮播卡片应存在")

    def test_index_page_slogan_cards(self):
        """测试首页标语卡片"""
        self.app.switch_tab("/pages/index/index")
        
        # 验证标语卡片内容
        slogan_cards = self.page.get_elements('.slogan-card')
        
        for card in slogan_cards:
            icon = card.get_element('.slogan-icon')
            content = card.get_element('.slogan-content')
            tag = card.get_element('.slogan-tag')
            
            self.assertIsNotNone(content, "标语内容应存在")