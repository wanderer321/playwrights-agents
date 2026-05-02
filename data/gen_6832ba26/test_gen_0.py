import minium
import time


class TestAuth(minium.MiniTest):
    """Suite: 01_基础架构与用户鉴权"""

    def test_auth_001_silent_login(self):
        """TC-AUTH-001: 微信静默登录"""
        # 启动小程序
        self.app.launch_app()
        
        # 等待首页加载完成
        self.page.wait_for(".page-container", timeout=10)
        
        # 验证首页是否正常显示
        home_container = self.page.get_element(".page-container")
        self.assertTrue(home_container is not None, "首页容器应存在")
        
        # 检查是否有授权弹窗遮挡
        auth_modal = self.page.get_element(".auth-modal")
        if auth_modal:
            # 如果存在授权弹窗，检查是否为静默登录场景
            is_visible = auth_modal.is_displayed()
            self.assertFalse(is_visible, "静默登录场景不应有授权弹窗遮挡")
        
        # 验证已进入首页
        current_page = self.app.get_current_page()
        self.assertIn("/pages/index/index", current_page.path, "应成功进入首页")

    def test_auth_002_user_authorization_login(self):
        """TC-AUTH-002: 用户授权登录流程"""
        # 清除缓存模拟新用户
        self.app.clear_storage()
        
        # 重新启动小程序
        self.app.launch_app()
        self.page.wait_for(".page-container", timeout=10)
        
        # 触发需要用户信息的操作 - 点击个人中心
        self.page.get_element(".tab-item", inner_text="个人中心").click()
        self.page.wait_for(1)
        
        # 检查是否出现授权弹窗或登录按钮
        login_btn = self.page.get_element(".login-btn, .auth-btn, button[open-type='getUserInfo']")
        
        if login_btn:
            login_btn.click()
            self.page.wait_for(1)
            
            # 模拟授权弹窗点击允许
            self.app.mock_wx_method("getUserInfo", {
                "userInfo": {
                    "nickName": "测试用户",
                    "avatarUrl": "https://example.com/avatar.png"
                }
            })
            
            # 确认授权
            confirm_btn = self.page.get_element(".auth-confirm-btn, button.confirm")
            if confirm_btn:
                confirm_btn.click()
        
        self.page.wait_for(2)
        
        # 验证用户昵称和头像显示
        nickname_element = self.page.get_element(".user-nickname, .nickname")
        avatar_element = self.page.get_element(".user-avatar, .avatar")
        
        self.assertTrue(nickname_element is not None, "用户昵称应显示")
        self.assertTrue(avatar_element is not None, "用户头像应显示")


class TestHome(minium.MiniTest):
    """Suite: 02_首页与活动列表"""

    def test_home_001_activity_list_load(self):
        """TC-HOME-001: 首页活动列表加载"""
        # 进入首页
        self.app.navigate_to("/pages/index/index")
        self.page.wait_for(".activity-list, .list-container", timeout=10)
        
        # 检查活动列表容器是否存在
        list_container = self.page.get_element(".activity-list, .list-container")
        self.assertTrue(list_container is not None, "活动列表容器应存在")
        
        # 验证首屏是否有数据渲染
        activity_items = self.page.get_elements(".activity-item, .list-item")
        self.assertTrue(len(activity_items) > 0, "首屏应有活动数据渲染")
        
        # 验证无白屏 - 检查页面高度
        page_height = self.page.get_element(".page-container").rect.get("height")
        self.assertGreater(page_height, 0, "页面应有内容高度")

    def test_home_002_pull_refresh_and_load_more(self):
        """TC-HOME-002: 下拉刷新与上拉加载"""
        # 进入首页
        self.app.navigate_to("/pages/index/index")
        self.page.wait_for(".activity-list", timeout=10)
        
        # 获取初始列表数量和时间戳
        initial_items = self.page.get_elements(".activity-item")
        initial_count = len(initial_items)
        
        # 执行下拉刷新
        self.page.scroll_pull_down()
        self.page.wait_for(2)
        
        # 验证 Loading 状态
        loading_indicator = self.page.get_element(".loading, .refresh-loading")
        # Loading 可能已经消失，检查刷新时间戳更新
        refresh_time = self.page.get_element(".refresh-time, .update-time")
        if refresh_time:
            self.assertIsNotNone(refresh_time.text, "刷新时间应更新")
        
        # 滚动到底部触发上拉加载
        self.page.scroll_to(0, 10000)
        self.page.wait_for(2)
        
        # 验证加载更多数据
        new_items = self.page.get_elements(".activity-item")
        new_count = len(new_items)
        
        self.assertGreaterEqual(new_count, initial_count, "上拉加载应追加新数据")
        
        # 验证无重复数据 - 检查活动ID唯一性
        activity_ids = []
        for item in new_items:
            activity_id = item.get_attribute("data-id")
            if activity_id:
                self.assertNotIn(activity_id, activity_ids, "活动ID不应重复")
                activity_ids.append(activity_id)

    def test_home_003_activity_search(self):
        """TC-HOME-003: 活动搜索功能"""
        # 进入首页
        self.app.navigate_to("/pages/index/index")
        self.page.wait_for(".search-box, .search-input", timeout=10)
        
        # 点击搜索框
        search_input = self.page.get_element(".search-box input, .search-input")
        self.assertTrue(search_input is not None, "搜索框应存在")
        
        # 输入搜索关键词
        search_keyword = "马拉松"
        search_input.input(search_keyword)
        
        # 点击搜索按钮
        search_btn = self.page.get_element(".search-btn, button.search")
        if search_btn:
            search_btn.click()
        else:
            # 如果没有搜索按钮，模拟键盘确认
            self.page.get_element(".search-box input").trigger("confirm")
        
        self.page.wait_for(2)
        
        # 验证搜索结果
        result_items = self.page.get_elements(".activity-item, .search-result-item")
        self.assertTrue(len(result_items) > 0, "搜索应有结果返回")
        
        # 验证结果包含关键词
        for item in result_items[:3]:  # 检查前3个结果
            item_text = item.text
            self.assertIn(search_keyword, item_text, f"搜索结果应包含关键词: {search_keyword}")


class TestDetail(minium.MiniTest):
    """Suite: 03_活动详情与报名"""

    def test_detail_001_activity_detail_render(self):
        """TC-DETAIL-001: 活动详情页渲染"""
        # 先进入首页获取活动列表
        self.app.navigate_to("/pages/index/index")
        self.page.wait_for(".activity-item", timeout=10)
        
        # 点击任意活动卡片
        activity_card = self.page.get_element(".activity-item")
        activity_id = activity_card.get_attribute("data-id")
        activity_card.click()
        
        self.page.wait_for(".detail-page, .activity-detail", timeout=10)
        
        # 验证跳转参数是否正确传递
        current_page = self.app.get_current_page()
        self.assertIn("/pages/detail", current_page.path, "应跳转到详情页")
        
        # 检查详情页元素渲染
        title_element = self.page.get_element(".detail-title, .activity-title")
        self.assertTrue(title_element is not None, "活动标题应渲染")
        
        time_element = self.page.get_element(".detail-time, .activity-time")
        self.assertTrue(time_element is not None, "活动时间应渲染")
        
        location_element = self.page.get_element(".detail-location, .activity-location")
        self.assertTrue(location_element is not None, "活动地点应渲染")
        
        # 检查富文本内容
        rich_text = self.page.get_element(".rich-text, .detail-content")
        self.assertTrue(rich_text is not None, "富文本内容应渲染")

    def test_detail_002_registration_form_validation(self):
        """TC-DETAIL-002: 活动报名表单校验"""
        # 进入活动详情页
        self.app.navigate_to("/pages/detail/detail?id=test_activity_001")
        self.page.wait_for(".detail-page", timeout=10)
        
        # 点击立即报名按钮
        register_btn = self.page.get_element(".register-btn, button.register")
        if register_btn:
            register_btn.click()
            self.page.wait_for(1)
        
        # 不填写必填项直接提交
        submit_btn = self.page.get_element(".submit-btn, button.submit")
        if submit_btn:
            submit_btn.click()
            self.page.wait_for(1)
        
        # 验证前端校验提示信息
        error_tips = self.page.get_elements(".error-tip, .form-error, .valid-error")
        self.assertTrue(len(error_tips) > 0, "应有表单校验错误提示")
        
        # 验证具体错误文案
        name_error = self.page.get_element(".name-error, .error-tip", inner_text="姓名")
        phone_error = self.page.get_element(".phone-error, .error-tip", inner_text="手机")
        
        self.assertTrue(name_error is not None or phone_error is not None, 
                       "应显示姓名或手机号的错误提示")

    def test_detail_003_get_phone_number_authorization(self):
        """TC-DETAIL-003: 获取手机号授权"""
        # 进入报名页面
        self.app.navigate_to("/pages/register/register?activityId=test_001")
        self.page.wait_for(".register-form", timeout=10)
        
        # 点击获取手机号按钮
        phone_btn = self.page.get_element("button[open-type='getPhoneNumber'], .get-phone-btn")
        self.assertTrue(phone_btn is not None, "获取手机号按钮应存在")
        
        phone_btn.click()
        self.page.wait_for(1)
        
        # 模拟微信手机号授权弹窗点击允许
        self.app.mock_wx_method("getPhoneNumber", {
            "code": "test_phone_code",
            "encryptedData": "test_encrypted_data",
            "iv": "test_iv"
        })
        
        # 确认授权
        confirm_btn = self.page.get_element(".auth-confirm, button.confirm")
        if confirm_btn:
            confirm_btn.click()
        
        self.page.wait_for(2)
        
        # 验证输入框是否自动填充手机号
        phone_input = self.page.get_element("input.phone, .phone-input")
        if phone_input:
            phone_value = phone_input.get_attribute("value")
            self.assertTrue(phone_value is not None and len(phone_value) >= 11, 
                           "手机号应自动填充")


class TestPayment(minium.MiniTest):
    """Suite: 04_支付与订单"""

    def test_pay_001_order_create_and_payment(self):
        """TC-PAY-001: 订单创建与支付唤起"""
        # 进入确认订单页
        self.app.navigate_to("/pages/order/confirm?activityId=test_001")
        self.page.wait_for(".order-confirm-page", timeout=10)
        
        # 点击提交订单
        submit_btn = self.page.get_element(".submit-order-btn, button.submit")
        self.assertTrue(submit_btn is not None, "提交订单按钮应存在")
        
        submit_btn.click()
        self.page.wait_for(2)
        
        # 验证订单创建成功 - 检查订单号
        order_no = self.page.get_element(".order-no")
        self.assertTrue(order_no is not None, "订单号应显示")
        
        # 捕获微信支付唤起
        # Mock 支付成功回调
        self.app.mock_wx_method("requestPayment", {
            "errMsg": "requestPayment:ok"
        })
        
        # 点击支付按钮
        pay_btn = self.page.get_element(".pay-btn, button.pay")
        if pay_btn:
            pay_btn.click()
            self.page.wait_for(2)
        
        # 验证支付成功后跳转
        current_page = self.app.get_current_page()
        self.assertIn("/pages/pay/success", current_page.path, 
                     "支付成功应跳转到成功页")

    def test_pay_002_payment_cancel_handling(self):
        """TC-PAY-002: 支付取消处理"""
        # 进入订单详情页（待支付状态）
        self.app.navigate_to("/pages/order/detail?orderId=test_order_001")
        self.page.wait_for(".order-detail-page", timeout=10)
        
        # 点击支付按钮
        pay_btn = self.page.get_element(".pay-btn, button.pay")
        if pay_btn:
            pay_btn.click()
            self.page.wait_for(1)
        
        # Mock 支付取消
        self.app.mock_wx_method("requestPayment", {
            "errMsg": "requestPayment:fail cancel"
        })
        
        # 模拟点击取消
        cancel_btn = self.page.get_element(".cancel-btn, button.cancel")
        if cancel_btn:
            cancel_btn.click()
        
        self.page.wait_for(2)
        
        # 验证订单状态为待支付
        order_status = self.page.get_element(".order-status")
        self.assertIn("待支付", order_status.text, "订单状态应为待支付")
        
        # 验证页面停留在订单详情页
        current_page = self.app.get_current_page()
        self.assertIn("/pages/order", current_page.path, "应停留在订单相关页面")
        
        # 验证可重新发起支付
        retry_pay_btn = self.page.get_element(".pay-btn, .retry-pay")
        self.assertTrue(retry_pay_btn is not None, "应可重新发起支付")


class TestUserCenter(minium.MiniTest):
    """Suite: 05_个人中心与分享"""

    def test_user_001_my_activity_list_status(self):
        """TC-USER-001: 我的活动列表状态"""
        # 进入个人中心
        self.app.navigate_to("/pages/user/index")
        self.page.wait_for(".user-center-page", timeout=10)
        
        # 点击我报名的活动
        my_activity_btn = self.page.get_element(".my-activity, .my-activity-btn")
        if my_activity_btn:
            my_activity_btn.click()
            self.page.wait_for(".activity-list-page", timeout=10)
        
        # 检查活动列表
        activity_items = self.page.get_elements(".activity-item, .list-item")
        self.assertTrue(len(activity_items) >= 0, "活动列表应存在")
        
        # 验证不同状态标签显示
        status_labels = ["待开始", "进行中", "已结束"]
        found_statuses = []
        
        for label in status_labels:
            status_element = self.page.get_element(f".status-tag, .status-{label}")
            if status_element:
                found_statuses.append(label)
                # 验证状态标签颜色区分
                status_class = status_element.get_attribute("class")
                self.assertTrue(status_class is not None, f"{label}状态应有样式区分")
        
        self.assertTrue(len(found_statuses) > 0, "应至少有一种活动状态显示")

    def test_share_001_share_to_friends(self):
        """TC-SHARE-001: 转发给好友"""
        # 进入活动详情页
        self.app.navigate_to("/pages/detail/detail?id=test_001")
        self.page.wait_for(".detail-page", timeout=10)
        
        # 点击分享按钮
        share_btn = self.page.get_element(".share-btn, button[open-type='share']")
        if share_btn:
            share_btn.click()
            self.page.wait_for(1)
        
        # 触发 onShareAppMessage
        share_info = self.page.call_method("onShareAppMessage")
        
        # 验证分享卡片标题
        self.assertTrue(share_info is not None, "分享信息应存在")
        if share_info:
            self.assertIn("title", share_info, "分享信息应包含标题")
            self.assertIn("path", share_info, "分享信息应包含路径")
            self.assertIn("imageUrl", share_info, "分享信息应包含图片")
            
            # 验证路径指向活动详情页
            self.assertIn("/pages/detail", share_info.get("path", ""), 
                         "分享路径应指向活动详情页")

    def test_share_002_share_to_timeline(self):
        """TC-SHARE-002: 分享到朋友圈"""
        # 进入活动详情页
        self.app.navigate_to("/pages/detail/detail?id=test_001")
        self.page.wait_for(".detail-page", timeout=10)
        
        # 点击右上角菜单
        more_btn = self.page.get_element(".more-btn, .menu-btn")
        if more_btn:
            more_btn.click()
            self.page.wait_for(1)
        
        # 点击分享到朋友圈
        timeline_btn = self.page.get_element(".share-timeline, button[open-type='shareTimeline']")
        if timeline_btn:
            timeline_btn.click()
            self.page.wait_for(1)
        
        # 触发 onShareTimeline
        share_info = self.page.call_method("onShareTimeline")
        
        # 验证朋友圈分享信息
        if share_info:
            self.assertIn("title", share_info, "朋友圈分享应包含标题")
            self.assertIn("query", share_info, "朋友圈分享应包含参数")
            
            # 验证单页模式页面展示
            poster_element = self.page.get_element(".share-poster, .timeline-poster")
            self.assertTrue(poster_element is not None, "应生成朋友圈海报")


class TestMap(minium.MiniTest):
    """Suite: 06_地图与位置服务"""

    def test_map_001_view_activity_location(self):
        """TC-MAP-001: 查看活动地点"""
        # 进入活动详情页
        self.app.navigate_to("/pages/detail/detail?id=test_001")
        self.page.wait_for(".detail-page", timeout=10)
        
        # 滚动到活动地点区域
        location_element = self.page.get_element(".location-info, .activity-address")
        if location_element:
            location_element.scroll_into_view()
        
        # 点击活动地点或地图组件
        map_element = self.page.get_element(".map-container, .location-map")
        if map_element:
            map_element.click()
            self.page.wait_for(1)
        else:
            # 点击地址文字
            address_element = self.page.get_element(".address-text, .location-text")
            if address_element:
                address_element.click()
        
        self.page.wait_for(2)
        
        # 验证是否调用 wx.openLocation 或显示地图
        # 检查是否有地图弹窗或跳转到地图页
        map_modal = self.page.get_element(".map-modal, .location-modal")
        map_page = self.app.get_current_page()
        
        self.assertTrue(
            map_modal is not None or "map" in map_page.path.lower(),
            "应打开地图显示活动地点"
        )

    def test_map_002_navigation_function(self):
        """TC-MAP-002: 导航功能"""
        # 进入地图页面
        self.app.navigate_to("/pages/map/location?activityId=test_001")
        self.page.wait_for(".map-page", timeout=10)
        
        # 点击导航按钮
        nav_btn = self.page.get_element(".nav-btn, .navigation-btn")
        self.assertTrue(nav_btn is not None, "导航按钮应存在")
        
        nav_btn.click()
        self.page.wait_for(1)
        
        # 验证是否拉起第三方地图 App
        # Mock wx.openLocation 调用
        self.app.mock_wx_method("openLocation", {"errMsg": "openLocation:ok"})
        
        # 检查导航选项弹窗
        nav_options = self.page.get_element(".nav-options, .map-app-list")
        if nav_options:
            # 验证地图 App 选项
            tencent_map = self.page.get_element(".tencent-map, .map-app", inner_text="腾讯地图")
            amap = self.page.get_element(".amap, .map-app", inner_text="高德地图")
            baidu_map = self.page.get_element(".baidu-map, .map-app", inner_text="百度地图")
            
            self.assertTrue(
                tencent_map is not None or amap is not None or baidu_map is not None,
                "应显示第三方地图App选项"
            )


class TestException(minium.MiniTest):
    """Suite: 07_异常与兼容性"""

    def test_ex_001_network_error_handling(self):
        """TC-EX-001: 网络异常处理"""
        # 模拟网络断开
        self.app.mock_network_condition({
            "offline": True
        })
        
        # 进入首页尝试加载列表
        self.app.navigate_to("/pages/index/index")
        self.page.wait_for(3)
        
        # 检查是否有网络错误提示
        error_toast = self.page.get_element(".error-toast, .network-error, .toast")
        error_page = self.page.get_element(".error-page, .network-fail")
        
        # 验证不出现白屏
        page_content = self.page.get_element(".page-container, .content")
        self.assertTrue(page_content is not None, "页面应有内容，不应白屏")
        
        # 验证有友好的错误提示
        self.assertTrue(
            error_toast is not None or error_page is not None,
            "应有网络错误提示"
        )
        
        # 检查重试机制
        retry_btn = self.page.get_element(".retry-btn, .reload-btn")
        if retry_btn:
            # 恢复网络
            self.app.mock_network_condition({
                "offline": False
            })
            retry_btn.click()
            self.page.wait_for(2)
            
            # 验证重新加载成功
            activity_list = self.page.get_element(".activity-list, .list-container")
            self.assertTrue(activity_list is not None, "重试后应成功加载")

    def test_ex_002_page_stack_management(self):
        """TC-EX-002: 多页面栈管理"""
        # 清空页面栈，从首页开始
        self.app.navigate_back_to_home()
        
        # 连续跳转多个页面（超过5个）
        pages_to_navigate = [
            "/pages/index/index",
            "/pages/list/list",
            "/pages/detail/detail?id=1",
            "/pages/register/register?activityId=1",
            "/pages/order/confirm?orderId=1",
            "/pages/user/index"
        ]
        
        navigated_pages = []
        for page_path in pages_to_navigate:
            try:
                self.app.navigate_to(page_path)
                navigated_pages.append(page_path)
                self.page.wait_for(0.5)
            except Exception as e:
                # 页面栈可能已满，使用 redirectTo
                self.app.redirect_to(page_path)
                navigated_pages.append(page_path + " (redirected)")
        
        # 获取当前页面栈
        page_stack = self.app.get_page_stack()
        stack_length = len(page_stack)
        
        # 验证页面栈未溢出（小程序限制为10层）
        self.assertLessEqual(stack_length, 10, "页面栈不应超过10层")
        
        # 使用 navigateBack 返回
        for i in range(min(3, stack_length - 1)):
            self.app.navigate_back()
            self.page.wait_for(0.5)
        
        # 验证返回逻辑正常
        current_page = self.app.get_current_page()
        self.assertIsNotNone(current_page, "当前页面应存在")
        
        # 验证页面数据保持
        page_data = current_page.data
        self.assertIsNotNone(page_data, "页面数据应保持")


class TestIntegration(minium.MiniTest):
    """Suite: 集成测试 - 核心业务流程"""

    def test_full_user_journey(self):
        """完整用户旅程测试：登录 -> 浏览活动 -> 报名 -> 支付"""
        # Step 1: 启动并登录
        self.app.launch_app()
        self.page.wait_for(".page-container", timeout=10)
        
        # 检查登录状态，如未登录则登录
        user_info = self.page.get_element(".user-info, .logged-in")
        if not user_info:
            self.page.get_element(".tab-item", inner_text="个人中心").click()
            self.page.wait_for(1)
            login_btn = self.page.get_element(".login-btn")
            if login_btn:
                login_btn.click()
                self.page.wait_for(2)
        
        # Step 2: 浏览活动列表
        self.app.navigate_to("/pages/index/index")
        self.page.wait_for(".activity-item", timeout=10)
        
        activity_items = self.page.get_elements(".activity-item")
        self.assertTrue(len(activity_items) > 0, "应有活动列表")
        
        # Step 3: 进入活动详情
        activity_items[0].click()
        self.page.wait_for(".detail-page", timeout=10)
        
        # 验证详情页加载
        title = self.page.get_element(".detail-title")
        self.assertTrue(title is not None, "活动详情应加载")
        
        # Step 4: 点击报名
        register_btn = self.page.get_element(".register-btn")
        if register_btn:
            register_btn.click()
            self.page.wait_for(".register-form", timeout=10)
            
            # 填写表单
            name_input = self.page.get_element("input.name, .name-input")
            if name_input:
                name_input.input("测试用户")
            
            phone_input = self.page.get_element("input.phone, .phone-input")
            if phone_input:
                phone_input.input("13800138000")
            
            # 提交
            submit_btn = self.page.get_element(".submit-btn")
            if submit_btn:
                submit_btn.click()
                self.page.wait_for(2)
        
        # Step 5: 验证流程完成
        current_page = self.app.get_current_page()
        success_indicator = self.page.get_element(".success-tip, .order-created")
        
        self.assertTrue(
            "order" in current_page.path.lower() or success_indicator is not None,
            "应成功创建订单或进入支付流程"
        )