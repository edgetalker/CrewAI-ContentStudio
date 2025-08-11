"""
CrewAI-ContentStudio 演示版本 - 完整文件
快速测试界面功能，使用模拟数据
修复了 st.download_button() 在表单内使用的问题
"""
import streamlit as st
import time
import random
from datetime import datetime
import pandas as pd

# 设置页面配置
st.set_page_config(
    page_title="CrewAI ContentStudio - Demo",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 模拟ContentCrew类
class MockContentCrew:
    """模拟的ContentCrew，用于演示"""

    def create_content(self, topic, content_type, target_audience, word_count, additional_requirements=None):
        """模拟内容创作过程"""

        # 模拟处理时间
        time.sleep(2)

        # 生成模拟内容
        mock_content = f"""
# {topic}

## 引言

在当今快速发展的技术时代，{topic}已成为各行业关注的焦点。本文将深入探讨这一主题的各个方面，为{target_audience}提供有价值的洞察。

## 核心观点

### 1. 技术发展趋势
当前的技术发展呈现出以下几个重要特征：
- 自动化程度不断提升
- 跨领域融合加速
- 用户体验持续优化

### 2. 应用场景分析
在实际应用中，我们观察到以下几个重要场景：
- 企业数字化转型
- 个人工作效率提升
- 行业标准化建设

### 3. 未来发展方向
展望未来，该领域将朝着以下方向发展：
- 更加智能化的解决方案
- 更广泛的应用覆盖
- 更深入的行业整合

## 实际案例

以某知名企业为例，他们通过采用相关技术，在短短6个月内实现了：
- 效率提升35%
- 成本降低20%
- 用户满意度提高40%

## 专家观点

业内专家认为，{topic}的发展将经历以下几个阶段：

1. **初期探索阶段**：技术概念验证和小规模试点
2. **快速发展阶段**：技术成熟度提升，应用场景扩大
3. **全面普及阶段**：成为行业标准配置
4. **深度融合阶段**：与其他技术深度融合创新

## 市场数据分析

根据最新的市场研究报告：
- 全球市场规模预计将达到1000亿美元
- 年复合增长率保持在25%以上
- {target_audience}是主要的采用群体

## 实施建议

对于{target_audience}而言，我们建议：

1. **积极学习**：持续关注技术发展动态
2. **小步试错**：从小规模项目开始实践
3. **团队建设**：培养相关技术人才
4. **生态合作**：与产业链上下游建立合作关系

## 风险评估

在推进过程中，需要注意以下风险：
- 技术更新迭代风险
- 投资回报不确定性
- 人才短缺问题
- 行业标准化滞后

## 结论与建议

{topic}代表了未来发展的重要方向，{target_audience}应该：

- **提前布局**：在技术成熟前进行战略规划
- **持续投入**：保持研发和人才投入
- **开放合作**：积极参与行业生态建设
- **风险控制**：建立完善的风险管理机制

通过合理的规划和实施，{target_audience}能够充分利用{topic}带来的机遇，实现可持续发展。

## 未来展望

展望未来3-5年，{topic}将在以下方面取得重大突破：
- 技术标准化程度大幅提升
- 应用成本显著降低
- 用户体验持续优化
- 商业模式日趋成熟

我们有理由相信，{topic}将成为推动行业变革的重要力量。

---

*本文由AI智能体协作生成，经过研究、分析、写作、编辑四个阶段，确保内容质量和准确性。*
*生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
*目标字数：{word_count}字 | 实际字数：约{word_count + random.randint(-100, 200)}字*
        """.strip()

        # 返回模拟结果
        return {
            'content': mock_content,
            'metadata': {
                'topic': topic,
                'content_type': content_type,
                'target_audience': target_audience,
                'target_word_count': word_count,
                'actual_length': len(mock_content)
            },
            'execution_info': {
                'start_time': datetime.now().isoformat(),
                'end_time': datetime.now().isoformat(),
                'total_time': '0:02:15',
                'workflow_steps': 4
            },
            'quality_metrics': {
                'content_length_match': True,
                'workflow_completed': True,
                'all_agents_executed': True,
                'overall_score': random.randint(85, 98)
            }
        }


def load_demo_css():
    """加载演示版CSS样式"""
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .demo-banner {
        background: linear-gradient(135deg, #FF6B6B, #4ECDC4);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 600;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-left: 4px solid #2E86AB;
        margin-bottom: 1rem;
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-2px);
    }
    
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
    }
    
    .status-success {
        background-color: #06D6A0;
        color: white;
    }
    
    .agent-progress {
        display: flex;
        align-items: center;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        background: #f8f9fa;
        border-left: 4px solid #28a745;
        transition: all 0.3s ease;
    }
    
    .agent-progress.active {
        background: #e3f2fd;
        border-left-color: #2196f3;
        animation: glow 1.5s ease-in-out infinite alternate;
    }
    
    .agent-progress.pending {
        background: #f5f5f5;
        border-left-color: #9e9e9e;
    }
    
    @keyframes glow {
        from { box-shadow: 0 0 5px rgba(33, 150, 243, 0.3); }
        to { box-shadow: 0 0 15px rgba(33, 150, 243, 0.6); }
    }
    
    .download-section {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 1px solid #dee2e6;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    .preview-container {
        background: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        max-height: 400px;
        overflow-y: auto;
    }
    
    /* 隐藏Streamlit默认元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* 自定义滚动条 */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #2E86AB;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #1976D2;
    }
    </style>
    """, unsafe_allow_html=True)


def init_demo_session_state():
    """初始化演示会话状态"""
    if 'demo_crew' not in st.session_state:
        st.session_state.demo_crew = MockContentCrew()

    if 'demo_history' not in st.session_state:
        # 添加一些示例历史记录
        st.session_state.demo_history = [
            {
                'topic': '人工智能在医疗领域的应用',
                'content_type': 'article',
                'target_audience': '医疗专业人士',
                'timestamp': '2025-08-11 10:30:00',
                'status': 'completed',
                'word_count': 1850,
                'quality_score': 92,
                'content': '''# 人工智能在医疗领域的应用

## 引言
人工智能（AI）技术正在革命性地改变医疗行业，为医疗专业人士提供前所未有的诊断和治疗能力。

## 核心应用领域

### 1. 医学影像诊断
- CT、MRI图像分析：AI算法能够快速准确地识别异常组织
- 早期癌症检测：通过深度学习模型提高早期诊断准确率
- 效果提升：诊断准确率提升40%，大幅减少误诊率

### 2. 药物研发
- 分子结构预测：利用AI预测药物分子的有效性和安全性
- 临床试验优化：智能化设计和管理临床试验流程
- 效率提升：研发周期缩短30%，降低研发成本

## 结论
AI技术为医疗领域带来革命性变革，医疗专业人士应积极拥抱这一技术趋势。'''
            },
            {
                'topic': '区块链技术发展趋势',
                'content_type': 'blog_post',
                'target_audience': '技术爱好者',
                'timestamp': '2025-08-11 14:15:00',
                'status': 'completed',
                'word_count': 1200,
                'quality_score': 88,
                'content': '''# 区块链技术发展趋势

## 引言
区块链技术作为新兴的分布式账本技术，正在为技术爱好者带来全新的创新机遇。

## 技术特点
- 去中心化架构
- 不可篡改性
- 透明可追溯

## 应用前景
区块链将在金融、供应链、数字身份等领域发挥重要作用。

## 结论
对于技术爱好者而言，区块链代表了技术创新的重要方向。'''
            }
        ]

    if 'demo_current_task' not in st.session_state:
        st.session_state.demo_current_task = None


def render_demo_header():
    """渲染演示版头部"""
    st.markdown("""
    <div class="demo-banner">
        🎭 这是CrewAI ContentStudio的演示版本 | 使用模拟数据展示功能
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="main-header">
        <h1>🚀 CrewAI ContentStudio</h1>
        <p>基于多智能体协作的AI内容创作平台 - 演示版</p>
    </div>
    """, unsafe_allow_html=True)


def render_demo_sidebar():
    """渲染演示版侧边栏"""
    with st.sidebar:
        st.markdown("## 🛠️ 演示控制面板")

        # 系统状态
        st.subheader("📊 系统状态")
        st.markdown('<span class="status-badge status-success">✅ 演示就绪</span>', unsafe_allow_html=True)
        st.success("模拟系统已加载")

        st.divider()

        # 统计信息
        st.subheader("📈 演示统计")
        col1, col2 = st.columns(2)

        with col1:
            st.metric("总创作数", len(st.session_state.demo_history))

        with col2:
            if st.session_state.demo_history:
                avg_score = sum(item.get('quality_score', 90) for item in st.session_state.demo_history) / len(st.session_state.demo_history)
                st.metric("平均质量", f"{avg_score:.0f}/100")
            else:
                st.metric("平均质量", "0/100")

        st.divider()

        # 演示历史
        st.subheader("📚 演示历史")

        for item in st.session_state.demo_history[-3:]:
            with st.expander(f"📝 {item['topic'][:15]}..."):
                st.write(f"**类型**: {item['content_type']}")
                st.write(f"**时间**: {item['timestamp']}")
                st.write(f"**质量**: {item['quality_score']}/100")

        st.divider()

        # 智能体状态模拟
        st.subheader("🤖 智能体状态")

        agents_status = [
            {"name": "🔍 研究员", "status": "ready"},
            {"name": "📊 分析师", "status": "ready"},
            {"name": "✍️ 写作者", "status": "ready"},
            {"name": "📝 编辑员", "status": "ready"}
        ]

        for agent in agents_status:
            st.success(f"{agent['name']}: 就绪")

        st.divider()

        # 演示说明
        st.subheader("ℹ️ 演示说明")
        st.info("""
        本演示版本使用模拟数据展示界面功能。
        
        **特点:**
        - 2-3秒快速创作
        - 模拟智能体协作
        - 完整功能演示
        - 无需API配置
        
        在实际版本中，系统会调用真实的AI智能体进行内容创作。
        """)

        # 版本信息
        st.markdown("---")
        st.caption("演示版 v1.0.0")


def render_demo_content():
    """渲染演示版主要内容"""
    tab1, tab2, tab3 = st.tabs(["🎯 创建内容", "📊 实时监控", "📁 结果管理"])

    with tab1:
        render_demo_creation_tab()

    with tab2:
        render_demo_monitoring_tab()

    with tab3:
        render_demo_results_tab()


def render_demo_creation_tab():
    """渲染演示版创建选项卡 - 修复后版本"""
    st.markdown("## 🎯 AI内容创作演示")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### 📝 内容参数设置")

        # ✅ 修复：表单区域只包含输入和提交
        with st.form("demo_creation_form"):
            topic = st.text_input(
                "📋 内容主题",
                value="量子计算在2025年的发展前景",
                help="演示版：可自定义主题"
            )

            content_type = st.selectbox(
                "📄 内容类型",
                options=["blog_post", "article", "report", "news", "tutorial"],
                format_func=lambda x: {
                    "blog_post": "📝 博客文章",
                    "article": "📰 技术文章",
                    "report": "📊 研究报告",
                    "news": "📢 新闻稿",
                    "tutorial": "🎓 教程指南"
                }[x]
            )

            target_audience = st.selectbox(
                "👥 目标受众",
                options=["技术专业人士", "企业决策者", "技术爱好者", "普通消费者", "学生群体"]
            )

            word_count = st.slider(
                "📏 目标字数",
                min_value=500,
                max_value=3000,
                value=1200,
                step=100
            )

            # 高级选项
            with st.expander("🔧 高级选项"):
                additional_requirements = st.text_area(
                    "额外要求",
                    placeholder="例如：重点关注实用性、包含具体案例、面向初学者等",
                    help="可选：描述特殊要求"
                )

            # 表单内只有提交按钮
            submitted = st.form_submit_button(
                "🚀 开始演示创作",
                type="primary",
                use_container_width=True
            )

        # ✅ 修复：处理逻辑移到表单外部
        if submitted:
            start_demo_creation(topic, content_type, target_audience, word_count, additional_requirements)

        # ✅ 修复：下载功能独立区域（在表单外部）
        render_demo_download_section()

    with col2:
        st.markdown("### 💡 演示功能")

        st.markdown("""
        <div class="feature-card">
            <h4>🎭 演示特色</h4>
            <ul>
                <li>模拟四智能体协作</li>
                <li>实时进度动画</li>
                <li>2-3秒快速生成</li>
                <li>质量评估展示</li>
                <li>完整下载功能</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.info("💡 演示版将在2-3秒内完成创作流程，展示真实系统的所有功能")

        # 内容类型说明
        st.markdown("### 📋 内容类型说明")

        content_info = {
            "📝 博客文章": "1200字，适合技术分享和观点表达",
            "📰 技术文章": "1500字，深度技术分析和教程",
            "📊 研究报告": "2500字，全面的行业分析报告",
            "📢 新闻稿": "800字，快速传播的新闻内容",
            "🎓 教程指南": "2000字，详细的操作指导"
        }

        for content_type, description in content_info.items():
            st.caption(f"**{content_type}**: {description}")


def start_demo_creation(topic, content_type, target_audience, word_count, additional_requirements=None):
    """启动演示创作流程 - 修复后版本"""

    # 显示创作开始提示
    st.success("🚀 开始AI智能体协作创作...")

    # 显示进度
    progress_container = st.container()

    with progress_container:
        progress_bar = st.progress(0)
        status_text = st.empty()

        # 模拟各个阶段
        stages = [
            ("🔍 研究员智能体：正在收集最新信息和数据...", 25),
            ("📊 分析师智能体：正在分析策略和制定大纲...", 50),
            ("✍️ 写作者智能体：正在创作高质量内容...", 75),
            ("📝 编辑员智能体：正在进行质量控制和优化...", 100)
        ]

        for message, progress in stages:
            status_text.text(message)
            progress_bar.progress(progress)
            time.sleep(0.8)  # 模拟处理时间

    # 生成演示结果
    with st.spinner("🔄 AI智能体正在协作创作..."):
        result = st.session_state.demo_crew.create_content(
            topic=topic,
            content_type=content_type,
            target_audience=target_audience,
            word_count=word_count,
            additional_requirements=additional_requirements
        )

    # 更新当前任务状态
    st.session_state.demo_current_task = {
        'topic': topic,
        'content_type': content_type,
        'target_audience': target_audience,
        'word_count': word_count,
        'progress': 100,
        'status': 'completed',
        'start_time': datetime.now().strftime("%H:%M:%S")
    }

    # ✅ 修复：保存完整内容到会话状态，供下载区域使用
    demo_record = {
        'topic': topic,
        'content_type': content_type,
        'target_audience': target_audience,
        'word_count': len(result['content'].split()),
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'status': 'completed',
        'quality_score': result['quality_metrics']['overall_score'],
        'content': result['content'],  # ← 关键：保存完整内容
        'execution_time': result['execution_info']['total_time'],
        'additional_requirements': additional_requirements or ''
    }

    st.session_state.demo_history.append(demo_record)

    # 清除进度显示
    progress_container.empty()

    # 显示成功消息
    st.success(f"🎉 演示内容创作成功完成！")

    # 显示结果概要
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("⭐ 质量评分", f"{result['quality_metrics']['overall_score']}/100")
    with col2:
        st.metric("📝 内容字数", f"{len(result['content'].split())} 字")
    with col3:
        st.metric("⏱️ 执行时间", result['execution_info']['total_time'])
    with col4:
        st.metric("🎯 目标达成", "✅ 完成")

    # 显示预览（但不显示下载按钮）
    st.markdown("### 📄 内容预览")
    with st.expander("查看生成的内容", expanded=True):
        preview_content = result['content']
        if len(preview_content) > 800:
            st.markdown(f"""
            <div class="preview-container">
                {preview_content[:800]}...
            </div>
            """, unsafe_allow_html=True)
            st.info(f"预览显示前800字符，完整内容共{len(preview_content)}字符。完整内容请在下方下载区域获取。")
        else:
            st.markdown(f"""
            <div class="preview-container">
                {preview_content}
            </div>
            """, unsafe_allow_html=True)

    # 触发页面重新渲染以显示下载按钮
    st.rerun()


def render_demo_download_section():
    """渲染下载功能区域 - 新增函数"""

    # ✅ 修复：独立的下载区域，完全在表单外部

    if st.session_state.demo_history:
        # 检查是否有最新的创作内容
        latest_creation = st.session_state.demo_history[-1]

        if 'content' in latest_creation and latest_creation.get('status') == 'completed':

            st.markdown("""
            <div class="download-section">
                <h3>📥 下载最新创作内容</h3>
            </div>
            """, unsafe_allow_html=True)

            # 显示最新创作的基本信息
            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <h4>📋 主题</h4>
                    <p>{latest_creation['topic'][:20]}{'...' if len(latest_creation['topic']) > 20 else ''}</p>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <h4>📄 类型</h4>
                    <p>{latest_creation['content_type']}</p>
                </div>
                """, unsafe_allow_html=True)

            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <h4>⭐ 质量评分</h4>
                    <p>{latest_creation.get('quality_score', 90)}/100</p>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("---")

            # 下载功能区域
            col1, col2, col3 = st.columns([3, 2, 2])

            with col1:
                # ✅ 安全的下载按钮：完全在表单外部
                filename = f"{latest_creation['topic'][:20].replace(' ', '_').replace('/', '_')}_演示_{latest_creation['timestamp'].replace(':', '').replace('-', '').replace(' ', '_')}.txt"

                st.download_button(
                    label="📥 下载完整内容",
                    data=latest_creation['content'],
                    file_name=filename,
                    mime="text/plain",
                    key=f"download_latest_{len(st.session_state.demo_history)}",  # 唯一key
                    help="下载完整的创作内容到本地文件",
                    use_container_width=True
                )

            with col2:
                # 显示内容统计
                st.info(f"📊 字数：{latest_creation['word_count']} 字")

            with col3:
                # 清除最新结果
                if st.button("🗑️ 清除最新", use_container_width=True, help="清除最新的创作结果"):
                    if len(st.session_state.demo_history) > 2:  # 保留初始示例
                        st.session_state.demo_history = st.session_state.demo_history[:-1]
                        st.rerun()
                    else:
                        st.warning("至少保留示例记录")

            # 显示详细信息
            with st.expander("📊 创作详细信息"):
                info_data = {
                    "创作时间": latest_creation['timestamp'],
                    "目标受众": latest_creation['target_audience'],
                    "内容字数": latest_creation['word_count'],
                    "质量评分": latest_creation['quality_score'],
                    "执行时间": latest_creation.get('execution_time', '0:02:15'),
                    "额外要求": latest_creation.get('additional_requirements', '无') or '无'
                }

                for key, value in info_data.items():
                    st.text(f"{key}: {value}")


def render_demo_monitoring_tab():
    """渲染演示版监控选项卡"""
    st.markdown("## 📊 智能体协作演示")

    if st.session_state.demo_current_task:
        st.markdown("### 🔄 当前演示任务")

        task = st.session_state.demo_current_task

        # 任务基本信息
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("📋 主题", task['topic'][:15] + "..." if len(task['topic']) > 15 else task['topic'])
        with col2:
            st.metric("📄 类型", task['content_type'])
        with col3:
            st.metric("📈 进度", f"{task.get('progress', 100)}%")
        with col4:
            st.metric("⏰ 开始时间", task.get('start_time', 'N/A'))

        st.markdown("### 🤖 智能体协作流程")

        # 智能体状态展示
        agents = [
            {
                "name": "🔍 研究员智能体",
                "status": "completed",
                "desc": "收集最新信息和权威数据",
                "time": "45秒"
            },
            {
                "name": "📊 分析师智能体",
                "status": "completed",
                "desc": "制定内容策略和结构大纲",
                "time": "30秒"
            },
            {
                "name": "✍️ 写作者智能体",
                "status": "completed",
                "desc": "创作高质量原创内容",
                "time": "60秒"
            },
            {
                "name": "📝 编辑员智能体",
                "status": "completed",
                "desc": "质量控制和SEO优化",
                "time": "20秒"
            }
        ]

        for i, agent in enumerate(agents):
            st.markdown(f"""
            <div class="agent-progress">
                <div style="margin-right: 1rem; min-width: 200px;">
                    <strong>{agent['name']}</strong><br>
                    <small style="color: #666;">{agent['desc']}</small>
                </div>
                <div style="margin-left: auto; display: flex; align-items: center; gap: 1rem;">
                    <span style="color: #666; font-size: 0.9rem;">用时: {agent['time']}</span>
                    <span style="color: #28a745; font-weight: bold;">✅ 已完成</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # 总结信息
        st.success("🎉 所有智能体协作完成！内容创作流程成功结束。")

        # 工作流统计
        st.markdown("### 📈 工作流统计")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("总执行时间", "2分35秒")
        with col2:
            st.metric("智能体数量", "4个")
        with col3:
            st.metric("任务成功率", "100%")

        # 重置按钮
        if st.button("🔄 重置演示状态", type="secondary"):
            st.session_state.demo_current_task = None
            st.success("✅ 演示状态已重置")
            st.rerun()

    else:
        st.info("当前没有运行中的演示任务")

        st.markdown("""
        <div class="feature-card">
            <h3>🎬 开始演示</h3>
            <p>在"创建内容"选项卡中点击"开始演示创作"来观看智能体协作过程。</p>
            <ul>
                <li>实时进度追踪</li>
                <li>智能体状态监控</li>
                <li>工作流可视化</li>
                <li>性能指标统计</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        # 系统架构展示
        st.markdown("### 🏗️ 系统架构展示")

        st.markdown("""
        ```
        用户输入 → ResearcherAgent → AnalystAgent → WriterAgent → EditorAgent → 最终内容
            ↓              ↓               ↓             ↓            ↓
        参数配置      信息收集        策略分析      内容创作     质量控制
        ```
        """)

        # 智能体介绍
        st.markdown("### 🤖 智能体详细介绍")

        agent_details = [
            {
                "icon": "🔍",
                "name": "研究员智能体",
                "role": "信息收集专家",
                "capabilities": ["网络搜索", "数据验证", "信息源筛选", "事实核查"]
            },
            {
                "icon": "📊",
                "name": "分析师智能体",
                "role": "内容策略专家",
                "capabilities": ["受众分析", "结构设计", "SEO规划", "策略制定"]
            },
            {
                "icon": "✍️",
                "name": "写作者智能体",
                "role": "内容创作专家",
                "capabilities": ["文本生成", "风格适配", "逻辑组织", "创意表达"]
            },
            {
                "icon": "📝",
                "name": "编辑员智能体",
                "role": "质量控制专家",
                "capabilities": ["语法检查", "结构优化", "SEO优化", "格式规范"]
            }
        ]

        for agent in agent_details:
            with st.expander(f"{agent['icon']} {agent['name']} - {agent['role']}"):
                st.write("**核心能力:**")
                for capability in agent['capabilities']:
                    st.write(f"• {capability}")


def render_demo_results_tab():
    """渲染演示版结果选项卡 - 修复后版本"""
    st.markdown("## 📁 演示结果展示")

    if st.session_state.demo_history:
        st.markdown("### 📚 演示历史记录")

        # 创建表格
        df_data = []
        for i, item in enumerate(st.session_state.demo_history):
            df_data.append({
                "序号": i + 1,
                "主题": item['topic'][:40] + "..." if len(item['topic']) > 40 else item['topic'],
                "类型": item['content_type'],
                "受众": item['target_audience'],
                "质量评分": f"{item.get('quality_score', 90)}/100",
                "字数": item.get('word_count', 'N/A'),
                "创建时间": item['timestamp']
            })

        df = pd.DataFrame(df_data)

        # 显示表格
        st.dataframe(
            df,
            use_container_width=True,
            column_config={
                "序号": st.column_config.NumberColumn("序号", width="small"),
                "主题": st.column_config.TextColumn("主题", width="large"),
                "类型": st.column_config.TextColumn("类型", width="small"),
                "受众": st.column_config.TextColumn("受众", width="medium"),
                "质量评分": st.column_config.TextColumn("质量评分", width="small"),
                "字数": st.column_config.TextColumn("字数", width="small"),
                "创建时间": st.column_config.DatetimeColumn("创建时间", width="medium")
            }
        )

        st.markdown("### 🔍 查看历史内容")

        # 选择查看特定历史记录
        if len(st.session_state.demo_history) > 0:
            selected_index = st.selectbox(
                "选择要查看的历史记录",
                options=range(len(st.session_state.demo_history)),
                format_func=lambda x: f"{x+1}. {st.session_state.demo_history[x]['topic'][:50]}{'...' if len(st.session_state.demo_history[x]['topic']) > 50 else ''} ({st.session_state.demo_history[x]['timestamp']})",
                index=len(st.session_state.demo_history) - 1  # 默认选择最新的
            )

            selected_item = st.session_state.demo_history[selected_index]

            # 显示选中项的详细信息
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("📋 主题", selected_item['topic'][:15] + "..." if len(selected_item['topic']) > 15 else selected_item['topic'])
            with col2:
                st.metric("📄 类型", selected_item['content_type'])
            with col3:
                st.metric("⭐ 评分", f"{selected_item.get('quality_score', 90)}/100")
            with col4:
                st.metric("📝 字数", selected_item.get('word_count', 'N/A'))

            # 显示内容预览
            if 'content' in selected_item:
                st.markdown("#### 📄 内容预览")

                with st.expander("查看完整内容", expanded=False):
                    st.markdown(f"""
                    <div class="preview-container">
                        {selected_item['content']}
                    </div>
                    """, unsafe_allow_html=True)

                # ✅ 历史记录的下载功能（也在表单外部）
                st.markdown("#### 📥 下载此内容")

                filename = f"{selected_item['topic'][:20].replace(' ', '_').replace('/', '_')}_{selected_item['timestamp'].replace(':', '').replace('-', '').replace(' ', '_')}.txt"

                col1, col2 = st.columns([2, 1])

                with col1:
                    st.download_button(
                        label=f"📥 下载：{selected_item['topic'][:30]}{'...' if len(selected_item['topic']) > 30 else ''}",
                        data=selected_item['content'],
                        file_name=filename,
                        mime="text/plain",
                        key=f"download_history_{selected_index}",
                        help=f"下载历史记录 #{selected_index + 1}",
                        use_container_width=True
                    )

                with col2:
                    # 内容统计
                    st.info(f"📊 {len(selected_item['content'].split())} 字")

        # 批量操作
        st.markdown("### 🛠️ 批量操作")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("📥 下载所有内容", type="secondary", use_container_width=True):
                # 创建包含所有内容的文件
                all_content = f"# CrewAI ContentStudio 演示版 - 所有创作内容\n\n"
                all_content += f"导出时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                all_content += f"总计内容数量: {len(st.session_state.demo_history)}\n"
                all_content += f"{'='*80}\n\n"

                for i, item in enumerate(st.session_state.demo_history):
                    if 'content' in item:
                        all_content += f"\n## 内容 #{i+1}: {item['topic']}\n\n"
                        all_content += f"**类型**: {item['content_type']} | **受众**: {item['target_audience']}\n"
                        all_content += f"**创建时间**: {item['timestamp']} | **质量评分**: {item.get('quality_score', 90)}/100\n"
                        all_content += f"**字数**: {item.get('word_count', 'N/A')}\n\n"
                        all_content += f"{'-'*60}\n\n"
                        all_content += item['content']
                        all_content += f"\n\n{'='*80}\n"

                st.download_button(
                    label="📥 确认下载所有内容",
                    data=all_content,
                    file_name=f"CrewAI_ContentStudio_全部内容_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    key="download_all_content",
                    use_container_width=True
                )

        with col2:
            if st.button("📊 导出统计报告", type="secondary", use_container_width=True):
                # 生成统计报告
                report = f"# CrewAI ContentStudio 使用统计报告\n\n"
                report += f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                report += f"## 总体统计\n"
                report += f"- 总创作数量: {len(st.session_state.demo_history)}\n"

                if st.session_state.demo_history:
                    avg_score = sum(item.get('quality_score', 90) for item in st.session_state.demo_history) / len(st.session_state.demo_history)
                    total_words = sum(item.get('word_count', 0) for item in st.session_state.demo_history)

                    report += f"- 平均质量评分: {avg_score:.1f}/100\n"
                    report += f"- 总创作字数: {total_words:,} 字\n"

                    # 按类型统计
                    type_counts = {}
                    for item in st.session_state.demo_history:
                        content_type = item['content_type']
                        type_counts[content_type] = type_counts.get(content_type, 0) + 1

                    report += f"\n## 按类型统计\n"
                    for content_type, count in type_counts.items():
                        report += f"- {content_type}: {count} 篇\n"

                    # 按受众统计
                    audience_counts = {}
                    for item in st.session_state.demo_history:
                        audience = item['target_audience']
                        audience_counts[audience] = audience_counts.get(audience, 0) + 1

                    report += f"\n## 按受众统计\n"
                    for audience, count in audience_counts.items():
                        report += f"- {audience}: {count} 篇\n"

                st.download_button(
                    label="📊 下载统计报告",
                    data=report,
                    file_name=f"CrewAI_ContentStudio_统计报告_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                    mime="text/markdown",
                    key="download_stats_report",
                    use_container_width=True
                )

        with col3:
            if st.button("🗑️ 清空历史记录", type="secondary", use_container_width=True):
                # 保留前两个示例，清除用户创建的内容
                if len(st.session_state.demo_history) > 2:
                    if st.button("⚠️ 确认清空", type="secondary", key="confirm_clear"):
                        st.session_state.demo_history = st.session_state.demo_history[:2]
                        st.success("✅ 已清空用户创建的内容，保留示例记录")
                        st.rerun()
                    else:
                        st.warning("再次点击确认清空")
                else:
                    st.info("仅有示例记录，无需清空")

    else:
        st.info("暂无演示历史记录")

        # 显示示例内容
        st.markdown("### 📄 查看示例内容")

        if st.button("📄 生成示例内容预览", type="primary"):
            sample_content = """
# 人工智能在医疗领域的应用

## 引言

人工智能（AI）技术正在革命性地改变医疗行业，为医疗专业人士提供前所未有的诊断和治疗能力。本文将深入探讨AI在医疗领域的核心应用和未来发展趋势。

## 核心应用领域

### 1. 医学影像诊断
- **CT、MRI图像分析**：AI算法能够快速准确地识别异常组织
- **早期癌症检测**：通过深度学习模型提高早期诊断准确率
- **效果提升**：诊断准确率提升40%，大幅减少误诊率

### 2. 药物研发
- **分子结构预测**：利用AI预测药物分子的有效性和安全性
- **临床试验优化**：智能化设计和管理临床试验流程
- **效率提升**：研发周期缩短30%，降低研发成本

### 3. 个性化治疗
- **基因组学分析**：基于患者基因信息制定个性化治疗方案
- **精准医疗方案**：结合AI分析为每位患者定制最优治疗策略
- **效果显著**：治疗效果提升25%，副作用显著减少

## 技术优势分析

AI在医疗领域的应用具有以下显著优势：

1. **处理速度快**：能够在秒级时间内分析大量医疗数据
2. **准确性高**：通过深度学习不断提高诊断精确度
3. **成本效益**：长期来看能够显著降低医疗成本
4. **可扩展性**：一套AI系统可以服务多个医疗机构

## 未来发展趋势

AI技术将继续深化医疗应用，预计在未来5年内：

- **智能手术机器人**：实现更精确的微创手术
- **远程诊疗系统**：基于AI的远程医疗服务更加成熟
- **预防医学体系**：通过AI预测和预防疾病发生
- **医疗资源优化**：智能调度和管理医疗资源

## 挑战与应对

尽管前景广阔，AI医疗应用仍面临一些挑战：

- **数据隐私保护**：需要建立完善的医疗数据保护机制
- **监管政策完善**：需要相关法规跟上技术发展步伐
- **医生培训**：需要培训医疗人员熟练使用AI工具
- **技术标准化**：建立统一的AI医疗应用标准

## 结论

AI技术为医疗领域带来革命性变革，医疗专业人士应积极拥抱这一技术趋势。通过合理应用AI技术，我们能够提供更精确、更高效、更个性化的医疗服务，最终改善患者的治疗效果和生活质量。

---

*本内容由CrewAI ContentStudio演示系统生成，展示多智能体协作创作能力。*
            """.strip()

            st.markdown("#### 📝 示例内容")
            st.markdown(f"""
            <div class="preview-container">
                {sample_content}
            </div>
            """, unsafe_allow_html=True)

            # ✅ 示例内容的下载（也在表单外部）
            st.download_button(
                label="📥 下载示例内容",
                data=sample_content,
                file_name=f"AI医疗应用_示例_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                key="download_sample_content"
            )


def main():
    """演示版主函数"""
    # 加载样式
    load_demo_css()

    # 初始化会话状态
    init_demo_session_state()

    # 渲染页面
    render_demo_header()
    render_demo_sidebar()
    render_demo_content()

    # 页脚
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; margin-top: 2rem;">
        <p>🎭 CrewAI ContentStudio 演示版 v1.0.0 | 展示多智能体协作内容创作流程</p>
        <p>💡 在实际版本中集成真实的AI智能体系统</p>
        <p style="font-size: 0.9rem; margin-top: 1rem;">
            <strong>演示特点：</strong> 
            模拟数据 • 2-3秒快速创作 • 完整功能展示 • 无需API配置
        </p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()