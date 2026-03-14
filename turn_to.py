import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl

from markdown_it import MarkdownIt


md_path = Path(r"C:\Users\xia\Desktop\可能有用\dist\data\markdowns\【喜欢】最近鼠鼠喜欢一个直男_7684216867_see_lz.md")   # 这里换成你的 md


md_text = md_path.read_text(encoding="utf-8")

md = MarkdownIt("commonmark", {"html": True})
html_body = md.render(md_text)

html = f'''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>

/* --- 基础设置 --- */
body {{
    background: #eef1f5;
    margin: 0;
    padding: 20px;
    font-family: "Segoe UI","Microsoft YaHei",sans-serif;
    transition: background 0.3s ease;
}}

/* 布局容器：Flex 布局，左侧 TOC，右侧内容 */
.layout {{
    display: flex;
    justify-content: center;
    gap: 20px;
    max-width: 1200px;
    margin: 0 auto;
    align-items: flex-start;
}}

/* --- 侧边栏 TOC --- */
.toc-wrapper {{
    width: 140px;
    flex-shrink: 0;
    position: sticky;
    top: 20px;
    max-height: 93vh;
    overflow-y: auto;
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(5px);
    border-radius: 8px;
    padding: 10px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    
    /* 滚动条在左侧 */
    direction: rtl;
}}

.toc {{
    display: flex;
    flex-direction: column;
    gap: 5px;
    direction: ltr; /* 内容保持从左到右 */
}}

/* 自定义滚动条样式 */
.toc-wrapper::-webkit-scrollbar {{
    width: 6px;
}}
.toc-wrapper::-webkit-scrollbar-thumb {{
    background-color: #ccc;
    border-radius: 3px;
}}
.toc-wrapper::-webkit-scrollbar-track {{
    background: transparent;
}}

.toc a {{
    text-decoration: none;
    color: #555;
    font-size: 14px;
    padding: 6px 8px;
    border-radius: 4px;
    transition: all 0.2s;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}}

.toc a:hover {{
    color: #4a90e2;
    background: rgba(74, 144, 226, 0.1);
}}

/* --- 主内容区域 --- */
.container {{
    flex: 1;
    max-width: 900px;
    font-family: "Segoe UI","Microsoft YaHei",sans-serif;
    min-width: 0;
}}

/* 标题 H1 居中 */
h1 {{
    text-align: center;
    color: #333;
    margin-bottom: 30px;
}}

/* 引用块信息 */
blockquote {{
    border-left: 4px solid #ddd;
    margin: 0 0 20px 0;
    padding: 10px 16px;
    background: #fafafa;
    color: #666;
    border-radius: 6px;
}}

/* 楼层标题 H3 */
h3 {{
    margin-top: 35px;
    margin-bottom: 0;
    padding: 12px 16px;
    background: #ffffff;
    border-left: 4px solid #4a90e2;
    border-radius: 6px;
    font-size: 18px;
    color: #333;
    scroll-margin-top: 20px;
}}

/* 段落与列表样式 */
h3 ~ p,
h3 ~ ul,
h3 ~ ol,
h3 ~ blockquote,
h3 ~ img,
h3 ~ pre {{
    background: white;
    padding-left: 16px;
    padding-right: 16px;
}}

/* 连续段落的间距处理 */
h3 + p,
h3 + p + p,
h3 + p + p + p,
h3 + p + p + p + p {{
    margin: 0;
}}




p {{
    background: white;
    padding: 8px 16px;
    margin: 0;
    line-height: 1.6;
    color: #333;
}}


a {{
    color: #4a90e2;
    text-decoration: none;
}}


a:hover {{
    text-decoration: underline;
}}

/* 图片样式 - 修复边框和圆角 */
img {{
    display: block;
    margin: 0 auto;
    background: white;
    max-width: 100%;
    height: auto;
    padding: 10px 16px;
    border-radius: 6px; /* 四个角统一圆角 */
    cursor: zoom-in;
    box-sizing: border-box;
    border: 1px solid #eee; /* 浅色细边框代替黑色边框 */
}}

/* 代码块 */
code {{
    background: #f2f2f2;
    padding: 2px 4px;
    border-radius: 3px;
    font-family: Consolas, monospace;
    color: #d63384;
}}

pre {{
    background: #f6f8fa;
    padding: 10px;
    overflow-x: auto;
    border-radius: 6px;
    margin: 0;
}}

hr {{
    border: none;
    height: 1px;
    background: #ddd;
    margin: 30px 0;
}}

/* --- 灯箱 (Lightbox) --- */
.lightbox {{
    position: fixed;
    display: none;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.85);
    justify-content: center;
    align-items: center;
    z-index: 9999;
    opacity: 0;
    transition: opacity 0.3s ease;
}}

.lightbox.active {{
    display: flex;
    opacity: 1;
}}

.lightbox img {{
    max-width: 90%;
    max-height: 90%;
    background: transparent;
    padding: 0;
    border-radius: 4px;
    box-shadow: 0 0 20px rgba(0,0,0,0.5);
    cursor: zoom-out;
    transition: transform 0.2s ease;
}}

/* --- 日夜模式切换按钮 --- */
.theme-toggle {{
    position: fixed;
    top: 20px;
    right: 20px;
    width: 44px;
    height: 44px;
    border-radius: 50%;
    border: none;
    cursor: pointer;
    background: #ffffff;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    z-index: 1000;
    transition: all 0.3s ease;
}}

.theme-toggle:hover {{
    transform: scale(1.1);
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}}

/* 太阳图标 (白天模式显示) */
.sun-icon {{
    display: block;
}}

/* 月亮图标 (夜晚模式显示) */
.moon-icon {{
    display: none;
}}

/* --- 深色模式样式 --- */
body.dark-mode {{
    background: #1a1a2e;
}}

body.dark-mode .toc-wrapper {{
    background: rgba(43, 43, 58, 0.95);
}}

body.dark-mode a {{
    color: #7eb8ff;
}}

body.dark-mode .toc a {{
    color: #b8b8d1;
}}

body.dark-mode .toc a:hover {{
    color: #7eb8ff;
    background: rgba(126, 184, 255, 0.15);
}}

body.dark-mode h1 {{
    color: #e8e8f0;
}}

body.dark-mode h3 {{
    background: #2d2d44;
    color: #e8e8f0;
    border-left-color: #7eb8ff;
}}

body.dark-mode p,
body.dark-mode img,
body.dark-mode blockquote,
body.dark-mode pre {{
    background: #2d2d44;
    color: #d0d0e0;
}}

body.dark-mode blockquote {{
    border-left-color: #555577;
}}

body.dark-mode code {{
    background: #3d3d5c;
    color: #ff9ebb;
}}

body.dark-mode hr {{
    background: #444466;
}}

body.dark-mode img {{
    border-color: #444466;
}}

body.dark-mode .theme-toggle {{
    background: #2d2d44;
    box-shadow: 0 2px 8px rgba(0,0,0,0.3);
}}

body.dark-mode .sun-icon {{
    display: none;
}}

body.dark-mode .moon-icon {{
    display: block;
}}

/* --- 灯箱导航按钮 --- */
.nav {{
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    font-size: 40px;
    background: rgba(255,255,255,0.1);
    border: none;
    color: white;
    cursor: pointer;
    padding: 20px 15px;
    border-radius: 8px;
    transition: all 0.2s;
    user-select: none;
}}

.nav:hover {{
    background: rgba(255,255,255,0.3);
}}

.prev {{ left: 20px; }}
.next {{ right: 20px; }}

/* --- 灯箱工具栏 --- */
.toolbar {{
    position: absolute;
    bottom: 30px;
    display: flex;
    gap: 10px;
    background: rgba(0,0,0,0.6);
    padding: 10px 15px;
    border-radius: 8px;
}}

.toolbar button {{
    padding: 8px 12px;
    font-size: 16px;
    background: rgba(255,255,255,0.2);
    border: none;
    color: white;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.2s;
}}

.toolbar button:hover {{
    background: rgba(255,255,255,0.4);
}}

/* 图片计数器 */
.image-counter {{
    position: absolute;
    top: 20px;
    left: 50%;
    transform: translateX(-50%);
    color: white;
    font-size: 14px;
    background: rgba(0,0,0,0.6);
    padding: 6px 12px;
    border-radius: 4px;
}}

</style>
</head>

<body>

<!-- 日夜模式切换按钮 -->
<button class="theme-toggle" id="themeToggle" title="切换日夜模式">
    <span class="sun-icon">☀️</span>
    <span class="moon-icon">🌙</span>
</button>

<div class="layout">
    <!-- 侧边栏目录 -->
    <div class="toc-wrapper">
        <div class="toc" id="toc">
            <div style="font-size:12px; color:#999; padding:10px;">加载中...</div>
        </div>
    </div>

    <!-- 主内容区 -->
    <div class="container">
        {html_body}
    </div>
</div>

<!-- 图片放大灯箱 -->
<div class="lightbox" id="lightbox">

<button class="nav prev" id="prevBtn">◀</button>

<div class="image-counter" id="imageCounter">1 / 1</div>

<img id="lightbox-img" src="">

<button class="nav next" id="nextBtn">▶</button>

<div class="toolbar" id="toolbar">
<button id="zoom-in">＋</button>
<button id="zoom-out">－</button>
<button id="rotate">⟳</button>
<button id="flip-h">⇋</button>
<button id="flip-v">⇅</button>
<button id="reset">Reset</button>
</div>

</div>

<script>
document.addEventListener('DOMContentLoaded', () => {{
    // 1. 生成目录
    const headings = document.querySelectorAll("h1, h3");
    const tocContainer = document.getElementById("toc");
    
    if (headings.length === 0) {{
        tocContainer.innerHTML = '<div style="padding:10px; color:#999;">无楼层目录</div>';
    }} else {{
        tocContainer.innerHTML = '';
        headings.forEach((h, i) => {{
            const id = "floor_" + i;
            h.id = id;


            const a = document.createElement("a");
            a.href = "#" + id;
            let text = h.textContent.trim().split('\\n')[0];
            if(text.length > 10) text = text.substring(0, 10) + "...";
            
            if (h.tagName === "H1") {{
                a.textContent = "简介";
            }} else {{
                a.textContent = "楼层 " + i;
            }}
            a.title = h.textContent.trim();
            
            a.onclick = (e) => {{
                e.preventDefault();
                h.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
                history.pushState(null, null, '#' + id);
            }};
            
            tocContainer.appendChild(a);
        }});
    }}

    // 2. 图片灯箱功能
    const imgs = document.querySelectorAll(".container img");
    const lightbox = document.getElementById("lightbox");
    const lightboxImg = document.getElementById("lightbox-img");
    const imageCounter = document.getElementById("imageCounter");

    let currentIndex = 0;
    let scale = 1;
    let rotate = 0;
    let flipH = 1;
    let flipV = 1;

    function updateTransform() {{
        lightboxImg.style.transform =
            `scale(${{scale}}) rotate(${{rotate}}deg) scaleX(${{flipH}}) scaleY(${{flipV}})`;
    }}

    function updateCounter() {{
        if (imgs.length > 0) {{
            imageCounter.textContent = (currentIndex + 1) + " / " + imgs.length;
        }}
    }}

    function showImage(index) {{
        if(index < 0) index = imgs.length - 1;
        if(index >= imgs.length) index = 0;


        currentIndex = index;


        lightboxImg.src = imgs[index].src;


        // 重置变换
        scale = 1;
        rotate = 0;
        flipH = 1;
        flipV = 1;
        updateTransform();
        updateCounter();
    }}

    // 为每张图片绑定点击事件
    imgs.forEach((img, i) => {{
        img.onclick = (e) => {{
            e.stopPropagation(); // 阻止冒泡
            lightbox.classList.add("active");
            document.body.style.overflow = 'hidden';
            showImage(i);
        }}
    }});

    // 灯箱背景点击关闭（只有点击背景才关闭，点击图片和按钮不关闭）
    lightbox.onclick = (e) => {{
        if (e.target === lightbox) {{
            closeLightbox();
        }}
    }};

    // 左右切换按钮 - 阻止冒泡
    document.getElementById("prevBtn").onclick = (e) => {{
        e.stopPropagation();
        showImage(currentIndex - 1);
    }}

    document.getElementById("nextBtn").onclick = (e) => {{
        e.stopPropagation();
        showImage(currentIndex + 1);
    }}

    // 工具按钮 - 阻止冒泡
    document.getElementById("zoom-in").onclick = (e) => {{
        e.stopPropagation();
        scale *= 1.2;
        updateTransform();
    }}

    document.getElementById("zoom-out").onclick = (e) => {{
        e.stopPropagation();
        scale /= 1.2;
        updateTransform();
    }}

    document.getElementById("rotate").onclick = (e) => {{
        e.stopPropagation();
        rotate += 90;
        updateTransform();
    }}

    document.getElementById("flip-h").onclick = (e) => {{
        e.stopPropagation();
        flipH *= -1;
        updateTransform();
    }}

    document.getElementById("flip-v").onclick = (e) => {{
        e.stopPropagation();
        flipV *= -1;
        updateTransform();
    }}

    document.getElementById("reset").onclick = (e) => {{
        e.stopPropagation();
        scale = 1;
        rotate = 0;
        flipH = 1;
        flipV = 1;
        updateTransform();
    }}

    // 关闭灯箱函数
    const closeLightbox = () => {{
        lightbox.classList.remove('active');
        setTimeout(() => {{
            lightboxImg.src = "";
        }}, 300);
        document.body.style.overflow = '';
    }};

    // ESC 键关闭
    document.addEventListener('keydown', (e) => {{
        if (e.key === "Escape" && lightbox.classList.contains('active')) {{
            closeLightbox();
        }}
        
        // 方向键切换图片
        if (lightbox.classList.contains('active')) {{
            if (e.key === "ArrowRight") {{
                showImage(currentIndex + 1);
            }}
            if (e.key === "ArrowLeft") {{
                showImage(currentIndex - 1);
            }}
        }}
    }});

    // 3. 日夜模式切换
    const themeToggle = document.getElementById('themeToggle');
    const body = document.body;
    
    // 检查本地存储的偏好
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {{
        body.classList.add('dark-mode');
    }}
    
    themeToggle.onclick = () => {{
        body.classList.toggle('dark-mode');
        // 保存偏好
        if (body.classList.contains('dark-mode')) {{
            localStorage.setItem('theme', 'dark');
        }} else {{
            localStorage.setItem('theme', 'light');
        }}
    }};
}});
</script>

</body>
</html>'''



# ---------------- 启动应用 ----------------
app = QApplication(sys.argv)

view = QWebEngineView()
# 设置基础URL，以便相对路径的图片（如 ../images/...）能正常加载
base_url = QUrl.fromLocalFile(str(md_path.parent.absolute()) + "/")
view.setHtml(html, base_url)

view.resize(1200, 800)
view.setWindowTitle("Markdown 阅读器 - 年终有感")
view.show()

sys.exit(app.exec())